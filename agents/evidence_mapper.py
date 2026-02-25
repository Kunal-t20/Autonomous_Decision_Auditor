from agents.state import AuditState
from utils.llm import call_llm


def evidence_mapper(state: AuditState):

    claims = state.get("claims", [])
    evidence_list = state.get("evidence", [])

    if not evidence_list:
        evidence_list = ["No external evidence provided"]
        state["evidence"] = evidence_list

    claim_evidence_map = {}

    if not claims:
        state["claim_evidence_map"] = {}
        return state

    evidence_text = ""
    for i, ev in enumerate(evidence_list, start=1):
        evidence_text += f"{i}. {ev}\n"

    for claim in claims:

        prompt = f"""
You are mapping evidence to a claim.

Claim:
{claim}

Evidence List:
{evidence_text}

Return ONLY:
- Comma separated evidence numbers
- If none, return NONE
"""

        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)
        raw_output = raw_output.strip()

        if raw_output.upper() == "NONE":
            claim_evidence_map[claim] = []
            continue

        nums = raw_output.replace(" ", "").split(",")
        mapped = []

        for n in nums:
            if n.isdigit():
                idx = int(n) - 1
                if 0 <= idx < len(evidence_list):
                    mapped.append(evidence_list[idx])

        claim_evidence_map[claim] = mapped

    state["claim_evidence_map"] = claim_evidence_map
    return state