from agents.claim_extractor import claim_extractor

test_state = {
    "decision": "Approve loan",
    "reasoning": (
        "The applicant has a stable monthly income of 80,000 INR, "
        "their credit score is 780, and they have not defaulted on any loan "
        "in the past five years. Therefore the financial risk is low."
    ),
    "evidence": [
        "Salary slips for last 12 months",
        "Official credit report showing score 780",
        "Loan repayment history with zero defaults"
    ]
}

updated_state = claim_extractor(test_state)
print(updated_state["claims"])