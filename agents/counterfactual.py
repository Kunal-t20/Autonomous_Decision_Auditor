from agents.state import AuditState
from utils.llm import call_llm


def counterfactual(state: AuditState):

    claims = state.get("claims", [])
    reasoning = state.get("reasoning", "")
    original_decision = state.get("decision", "")

    if not claims:
        state["counterfactual_issues"] = []
        return state

    counterfactual_issues = []

    # -----------------------------
    # STEP 1: batch LLM call
    # -----------------------------
    claims_text = ""
    for i, c in enumerate(claims, start=1):
        claims_text += f"{i}. {c}\n"

    prompt = f"""
You are a strict reasoning auditor.

We have an original reasoning and decision.

Original Reasoning:
{reasoning}

Original Decision:
{original_decision}

Claims:
{claims_text}

Task:
For each claim:
1. Assume the claim is FALSE
2. Check if the final decision would change

Return ONLY JSON:

{{
  "1": {{"status": "ROBUST"}},
  "2": {{"status": "FRAGILE", "reason": "..."}}
}}
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

                if result.get("status") == "FRAGILE":
                    counterfactual_issues.append({
                        "claim": claim,
                        "issue": result.get("reason", "Decision depends on this claim"),
                        "type": "COUNTERFACTUAL_FAILURE",
                        "severity": "HIGH"
                    })

    except Exception:
        # -----------------------------
        # fallback: simple heuristic
        # -----------------------------
        for claim in claims:
            if len(claim.split()) < 4:
                counterfactual_issues.append({
                    "claim": claim,
                    "issue": "Weak claim, likely fragile",
                    "type": "WEAK_CLAIM",
                    "severity": "MEDIUM"
                })

    # -----------------------------
    # deduplicate
    # -----------------------------
    unique = []
    seen = set()

    for item in counterfactual_issues:
        key = (item["claim"], item["issue"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    state["counterfactual_issues"] = unique
    return state