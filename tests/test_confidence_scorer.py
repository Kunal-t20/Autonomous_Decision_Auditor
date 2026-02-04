from agents.confidence_scorer import confidence_score

test_state = {
    "claims": [
        "Claim A",
        "Claim B",
        "Claim C",
        "Claim D"
    ],

    "claim_evidence_map": {
        "Claim A": ["Evidence 1"],
        "Claim B": [],               
        "Claim C": ["Evidence 3"],
        "Claim D": []                 
    },

    "inconsistencies": [
        {"claim": "Claim C", "issue": "Number mismatch"}
    ],

    "counterfactual_issues": [
        {"claim": "Claim A", "issue": "Decision heavily depends"}
    ]
}

updated_state = confidence_score(test_state)

print("\n=== CONFIDENCE ===\n")
print(updated_state["confidence"])
