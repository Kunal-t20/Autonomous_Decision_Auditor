from agents.state import AuditState
from core.config import ACCEPT_THRESHOLD, ESCALATE_THRESHOLD
from core.constants import ACCEPT, REJECT, ESCALATE

def verdict_engine(state:AuditState):

    confidence=state.get('confidence',0)

    if confidence >= ACCEPT_THRESHOLD:
        verdict = ACCEPT

    elif confidence >= ESCALATE_THRESHOLD:
        verdict = ESCALATE

    else:
        verdict = REJECT

    state["verdict"] = verdict
    return state

