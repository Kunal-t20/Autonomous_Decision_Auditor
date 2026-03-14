from agents.counterfactual import counterfactual

def test_counterfactual():
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
         
    }

    updated_state = counterfactual(test_state)

    assert "counterfactual_issues" in updated_state
    assert isinstance(updated_state["counterfactual_issues"], list)
