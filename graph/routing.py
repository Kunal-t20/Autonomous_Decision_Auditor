MAX_RETRY = 2
INCONSISTENCY_THRESHOLD = 0.6


def route_after_evidence(state):

    evidence = state.get("evidence", [])
    retry = state.get("retry_count", 0)

    # Detect fallback evidence
    no_real_evidence = (
        len(evidence) == 0
        or evidence == ["No external evidence provided"]
    )

    if no_real_evidence:
        if retry >= MAX_RETRY:
            return "consistency_checker"

        state["retry_count"] = retry + 1
        return "claim_extractor"

    return "consistency_checker"


def route_after_consistency(state):

    score = state.get("inconsistency_score", 0.0)

    if score > INCONSISTENCY_THRESHOLD:
        return "counterfactual"

    return "confidence_scorer"