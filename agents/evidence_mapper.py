from agents.state import AuditState
from utils.llm import call_llm


def evidence_mapper(state: AuditState):

    claims = state.get("claims", [])
    evidence_list = state.get("evidence", [])

    if not evidence_list:
        evidence_list = ["No external evidence provided"]
        state["evidence"] = evidence_list

    if not claims:
        state["claim_evidence_map"] = {}
        return state

    # Prepare formatted text
    claims_text = ""
    for i, c in enumerate(claims, start=1):
        claims_text += f"{i}. {c}\n"

    evidence_text = ""
    for i, ev in enumerate(evidence_list, start=1):
        evidence_text += f"{i}. {ev}\n"

    prompt = f"""
You are mapping evidence to claims.

Claims:
{claims_text}

Evidence:
{evidence_text}

Rules:
1. Map relevant evidence numbers to each claim
2. Return ONLY JSON format
3. Use claim index as key
4. Value = list of evidence numbers
5. If none, return empty list

Example:
{{
  "1": [1,2],
  "2": [],
  "3": [2]
}}
"""

    claim_evidence_map = {}

    try:
        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)

        import json
        parsed = json.loads(raw_output)

        for idx, claim in enumerate(claims, start=1):
            key = str(idx)
            mapped = []

            if key in parsed and isinstance(parsed[key], list):
                for n in parsed[key]:
                    if isinstance(n, int):
                        i = n - 1
                        if 0 <= i < len(evidence_list):
                            mapped.append(evidence_list[i])

            # remove duplicates
            mapped = list(dict.fromkeys(mapped))

            claim_evidence_map[claim] = mapped

    except Exception:
        # fallback: simple keyword matching (deterministic)
        for claim in claims:
            mapped = []

            for ev in evidence_list:
                claim_words = set(claim.lower().split())
                ev_words = set(ev.lower().split())

                # overlap threshold
                if len(claim_words & ev_words) >= 2:
                    mapped.append(ev)

            claim_evidence_map[claim] = mapped

    state["claim_evidence_map"] = claim_evidence_map
    return state