MAX_RETRY = 2
INCONSISTENCY_THRESHOLD = 0.6


def route_after_evidence(state):

    evidence = state.get("evidence", [])
    retry = state.get("retry_count", 0)

    # stop retry loop
    if len(evidence) == 0 and retry < MAX_RETRY:
        return "retry_claim_extractor"

    return "consistency_checker"


def route_after_consistency(state):

    score = state.get("inconsistency_score", 0.0)

    if score > INCONSISTENCY_THRESHOLD:
        return "counterfactual"

    return "confidence_scorer"