from core.config import ACCEPT_THRESHOLD, ESCALATE_THRESHOLD
from core.constants import ACCEPT, REJECT, ESCALATE
from services.explanation import build_explanation
from services.persistence import save_audit

def verdict_engine(state):
    confidence = float(state.get("confidence", 0))
    confidence = max(0.0, min(1.0, confidence))

    has_claims = len(state.get("claims", [])) > 0
    has_evidence = len(state.get("evidence", [])) > 0

    if not has_claims:
        verdict = "INSUFFICIENT_DATA"

    elif not has_evidence:
        verdict = "LOW_EVIDENCE"

    else:
        if confidence >= ACCEPT_THRESHOLD:
            verdict = ACCEPT
        elif confidence >= ESCALATE_THRESHOLD:
            verdict = ESCALATE
        else:
            verdict = REJECT

    explanation = build_explanation(state)

    audit_id = save_audit({
        **state,
        "verdict": verdict,
        "explanation": explanation,
    })

    return {
        "verdict": verdict,
        "confidence": confidence,
        "explanation": explanation,
        "audit_id": audit_id,
    }