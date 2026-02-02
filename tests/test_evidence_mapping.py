from agents.evidence_mapper import evidence_mapper

test_state = {
    "decision": "Approve loan",
    "reasoning": "dummy",
    "claims": [
        "The applicant has a stable monthly income of 80,000 INR",
        "The applicant's credit score is 780",
        "The applicant has not defaulted on any loan in the past five years",
        "The financial risk is low"
    ],
    "evidence": [
        "Salary slips for last 12 months showing 80,000 INR income",
        "Official credit report with score 780",
        "Loan repayment history showing zero defaults"
    ]
}

updated_state = evidence_mapper(test_state)

print("\n=== CLAIM → EVIDENCE MAP ===\n")
for claim, ev in updated_state["claim_evidence_map"].items():
    print(f"CLAIM: {claim}")
    print(f"EVIDENCE: {ev}")
    print("------")
