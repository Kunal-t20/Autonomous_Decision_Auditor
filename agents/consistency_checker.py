from agents.state import AuditState
from utils.llm import call_llm


def consistency_checker(state: AuditState):

    claims = state["claims"]
    claim_evidence_map = state["claim_evidence_map"]

    inconsistencies=[]

    for claim in claims:
        evidence_for_claim = claim_evidence_map.get(claim, [])

        prompt = f"""
You are a strict logical auditor.

Task:
Check whether the evidence contradicts the claim.

Claim:
{claim}

Evidence:
{evidence_for_claim}

Rules:
- If evidence clearly denies or conflicts with the claim -> INCONSISTENT
- Late payment, missed EMI, or default contradicts "no default"
- Different numbers contradict each other
- If evidence supports or does not conflict -> CONSISTENT
- Do NOT explain unless inconsistent

Return ONLY one line exactly in this format:
CONSISTENT
OR
INCONSISTENT: <short reason>
"""


        response = call_llm(prompt)

        raw_output = response.content if hasattr(response, "content") else str(response)
        raw_output = raw_output.strip()

        # if inconsistent, store it
        if raw_output.upper().startswith("INCONSISTENT"):
            inconsistencies.append({
                "claim": claim,
                "issue": raw_output
            })

    state["inconsistencies"] = inconsistencies
    return state
