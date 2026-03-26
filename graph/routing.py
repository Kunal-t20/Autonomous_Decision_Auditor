MAX_RETRY = 2
INCONSISTENCY_THRESHOLD = 0.6


def route_after_evidence(state):

    claims = state.get("claims", [])
    evidence = state.get("evidence", [])
    retry = state.get("retry_count", 0)

    # -----------------------------
    # Retry conditions (better)
    # -----------------------------
    if (not claims or len(claims) == 0) and retry < MAX_RETRY:
        return "retry_handler"

    # weak evidence case → still proceed (don’t loop blindly)
    if len(evidence) == 0 and retry < MAX_RETRY:
        return "retry_handler"

    return "consistency_checker"


def route_after_consistency(state):

    score = state.get("inconsistency_score", 0.0)
    inconsistencies = state.get("inconsistencies", [])

    # -----------------------------
    # High inconsistency → deeper check
    # -----------------------------
    if score > INCONSISTENCY_THRESHOLD or len(inconsistencies) > 0:
        return "policy_checker"

    # -----------------------------
    # Always run counterfactual (important)
    # -----------------------------
    return "policy_checker"