from agents.state import AuditState

def increment_retry(state: AuditState):
    state["retry_count"] = state.get("retry_count", 0) + 1
    return state