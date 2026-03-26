from agents.state import AuditState


MAX_RETRIES = 3


def increment_retry(state: AuditState):

    retry_count = state.get("retry_count", 0) + 1
    state["retry_count"] = retry_count

    # -----------------------------
    # track retry reason
    # -----------------------------
    reason = state.get("last_error", "unknown")
    history = state.get("retry_history", [])

    history.append({
        "attempt": retry_count,
        "reason": reason
    })

    state["retry_history"] = history

    # -----------------------------
    # stop condition
    # -----------------------------
    if retry_count >= MAX_RETRIES:
        state["retry_exceeded"] = True
    else:
        state["retry_exceeded"] = False

    return state