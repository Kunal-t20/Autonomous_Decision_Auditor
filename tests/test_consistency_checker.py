from agents.consistency_checker import consistency_checker

test_state = {
    "decision": "Approve loan",
    "reasoning": "dummy",

    "claims": [
        "The applicant has not defaulted on any loan in the past five years",
        "The applicant's credit score is 780"
    ],

    "evidence": [
    "Loan repayment history shows LOAN DEFAULT in 2022",
    "Official credit report showing score 780"
    ],

    "claim_evidence_map": {
        "The applicant has not defaulted on any loan in the past five years": [
            "Loan repayment history shows 2 late EMIs in 2022"
        ],
        "The applicant's credit score is 780": [
            "Official credit report showing score 780"
        ]
    }
}

updated_state = consistency_checker(test_state)

print("\n=== INCONSISTENCIES ===\n")
for item in updated_state["inconsistencies"]:
    print(item)
