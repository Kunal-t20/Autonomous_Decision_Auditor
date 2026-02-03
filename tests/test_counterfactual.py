
from agents.counterfactual import counterfactual

test_state = {
    "decision": "Approve loan",
    "reasoning": "dummy",

    "claims": [
        "The applicant's credit score is 780",
        "The applicant has a stable monthly income"
    ],

    "evidence": [
        "Official credit report showing score 780",
        "Salary slips for last 12 months"
    ],

    "claim_evidence_map": {},   # not used here
    "inconsistencies": []      
}

updated_state = counterfactual(test_state)

print("\n=== COUNTERFACTUAL ISSUES ===\n")
for item in updated_state["counterfactual_issues"]:
    print(item)
