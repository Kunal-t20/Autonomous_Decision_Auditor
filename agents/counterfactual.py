from agents.state import AuditState
from utils.llm import call_llm


def counterfactual(state: AuditState):

    claims = state.get("claims", [])

    if not claims:
        state["counterfactual_issues"] = []
        return state

    counterfactual_issues = []

    for claim in claims:

        prompt = f"""
You are stress-testing reasoning.

If this claim becomes FALSE, would the final decision change?

Claim:
{claim}

Return ONLY:
ROBUST
OR
FRAGILE: <reason>
"""

        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)
        raw_output = raw_output.strip()

        if raw_output.upper().startswith("FRAGILE"):
            counterfactual_issues.append({
                "claim": claim,
                "issue": raw_output
            })

    state["counterfactual_issues"] = counterfactual_issues
    return state