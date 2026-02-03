from agents.state import AuditState
from utils.llm import call_llm


def counterfactual(state: AuditState):#stress testing

    claims = state["claims"]

    counterfactual_issues = []

    for claim in claims:

        prompt = f"""
You are stress-testing reasoning.

If this claim becomes FALSE, would the final decision change?

Claim:
{claim}

Return ONLY one line:
ROBUST
OR
FRAGILE: <short reason>
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
