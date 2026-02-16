from agents.state import AuditState
from core.config import ACCEPT_THRESHOLD, ESCALATE_THRESHOLD
from core.constants import ACCEPT, REJECT, ESCALATE
from services.explanation import build_explanation
from services.persistence import save_audit


def verdict_engine(state: AuditState) -> AuditState:
    confidence = float(state.get("confidence", 0))

    if confidence >= ACCEPT_THRESHOLD:
        verdict = ACCEPT

    elif confidence >= ESCALATE_THRESHOLD:
        verdict = ESCALATE

    else:
        verdict = REJECT

    state["verdict"] = verdict
    state["explanation"] = build_explanation(state)

    save_audit(state)

    return state
