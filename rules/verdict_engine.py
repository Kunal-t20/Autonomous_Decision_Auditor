from core.config import ACCEPT_THRESHOLD, ESCALATE_THRESHOLD
from core.constants import ACCEPT, REJECT, ESCALATE
from services.explanation import build_explanation
from services.persistence import save_audit


def verdict_engine(state):

    confidence = float(state.get("confidence", 0))
    confidence = max(0.0, min(1.0, confidence))

    if confidence >= ACCEPT_THRESHOLD:
        verdict = ACCEPT
    elif confidence >= ESCALATE_THRESHOLD:
        verdict = ESCALATE
    else:
        verdict = REJECT

    explanation = build_explanation(state)

    save_audit({
        **state,
        "verdict": verdict,
        "explanation": explanation
    })

    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation
    }