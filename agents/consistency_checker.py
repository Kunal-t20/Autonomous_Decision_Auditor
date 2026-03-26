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

    # -----------------------------
    # STEP 1: deterministic checks
    # -----------------------------
    for claim in claims:
        evidence = claim_evidence_map.get(claim, [])

        if not evidence:
            inconsistencies.append({
                "claim": claim,
                "issue": "No supporting evidence",
                "type": "MISSING_EVIDENCE",
                "severity": "HIGH"
            })

    # -----------------------------
    # STEP 2: batch LLM check
    # -----------------------------
    claims_text = ""
    for i, c in enumerate(claims, start=1):
        ev = claim_evidence_map.get(c, [])
        claims_text += f"{i}. Claim: {c}\n   Evidence: {ev}\n"

    prompt = f"""
You are a strict logical auditor.

Analyze each claim with its evidence.

Return ONLY JSON.

Format:
{{
  "1": {{"status": "CONSISTENT"}},
  "2": {{"status": "INCONSISTENT", "reason": "..."}}
}}

Claims:
{claims_text}
"""

    try:
        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)

        import json
        parsed = json.loads(raw_output)

        for idx, claim in enumerate(claims, start=1):
            key = str(idx)

            if key in parsed:
                result = parsed[key]

                if result.get("status") == "INCONSISTENT":
                    inconsistencies.append({
                        "claim": claim,
                        "issue": result.get("reason", "Unknown inconsistency"),
                        "type": "LOGICAL_CONTRADICTION",
                        "severity": "MEDIUM"
                    })

    except Exception:
        # fallback: skip LLM layer
        pass

    # -----------------------------
    # STEP 3: deduplicate issues
    # -----------------------------
    unique = []
    seen = set()

    for item in inconsistencies:
        key = (item["claim"], item["issue"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    inconsistencies = unique

    # -----------------------------
    # scoring
    # -----------------------------
    total = len(claims)
    score = len(inconsistencies) / total if total else 0.0

    state["inconsistencies"] = inconsistencies
    state["inconsistency_score"] = round(score, 3)

    return state