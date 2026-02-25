from agents.state import AuditState
from utils.llm import call_llm


def consistency_checker(state: AuditState):

    claims = state.get("claims", [])
    claim_evidence_map = state.get("claim_evidence_map", {})

    inconsistencies = []

    if not claims:
        state["inconsistencies"] = []
        state["inconsistency_score"] = 0.0
        return state

    for claim in claims:

        evidence_for_claim = claim_evidence_map.get(claim, [])

        prompt = f"""
You are a strict logical auditor.

Claim:
{claim}

Evidence:
{evidence_for_claim}

Return ONLY:
CONSISTENT
OR
INCONSISTENT: <reason>
"""

        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)
        raw_output = raw_output.strip()

        if "INCONSISTENT" in raw_output.upper():
            inconsistencies.append({
                "claim": claim,
                "issue": raw_output
            })

    state["inconsistencies"] = inconsistencies

    total = len(claims)
    state["inconsistency_score"] = len(inconsistencies) / total if total else 0.0

    return state