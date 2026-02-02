from agents.state import AuditState
from utils.llm import call_llm


def evidence_mapper(state: AuditState):

    #pick data 
    claims = state["claims"]
    evidence_list = state["evidence"]
    
    #numbering evidences
    evidence_text = ""
    for i, ev in enumerate(evidence_list, start=1):
        evidence_text += f"{i}. {ev}\n"

    claim_evidence_map = {}

    for claim in claims:

        prompt = f"""
You are mapping evidence to a claim.

Claim:
{claim}

Evidence List:
{evidence_text}

Return ONLY:
- Comma separated evidence numbers that support the claim
- If none, return NONE
"""

        # call llm
        response = call_llm(prompt)

        # retrieve content
        raw_output = response.content if hasattr(response, "content") else str(response)
        raw_output = raw_output.strip()

        # NONE case
        if raw_output.upper() == "NONE":
            claim_evidence_map[claim] = []
            continue

        # parse numbers
        nums = raw_output.replace(" ", "").split(",")
        mapped = []

        for n in nums:
            if n.isdigit():
                ind = int(n) - 1
                if 0 <= ind < len(evidence_list):
                    mapped.append(evidence_list[ind])

        claim_evidence_map[claim] = mapped

    state["claim_evidence_map"] = claim_evidence_map
    return state
