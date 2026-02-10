MAX_RETRY = 2
INCONSISTENCY_THRESHOLD = 0.6
CONFIDENCE_THRESHOLD = 0.5


def route_after_evidence(state):
    evidence = state.get("evidence", [])
    retry = state.get("retry_count", 0)

    if len(evidence) == 0 and retry < MAX_RETRY:
        state["retry_count"] = retry + 1
        return "claim_extractor"

    return "consistency_checker"


def route_after_consistency(state):
    score = state.get("inconsistency_score", 0.0)

    if score > INCONSISTENCY_THRESHOLD:
        return "counterfactual"

    return "confidence_scorer"


def route_after_confidence(state):
    confidence = state.get("confidence", 0.0)

    if confidence < CONFIDENCE_THRESHOLD:
        return "verdict_engine_escalate"

    return "verdict_engine"
