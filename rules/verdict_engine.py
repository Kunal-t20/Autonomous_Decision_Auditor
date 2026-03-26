from core.config import ACCEPT_THRESHOLD, ESCALATE_THRESHOLD
from core.constants import ACCEPT, REJECT, ESCALATE
from services.explanation import build_explanation
from services.persistence import save_audit


def verdict_engine(state):

    confidence = float(state.get("confidence", 0))
    confidence = max(0.0, min(1.0, confidence))

    claims = state.get("claims", [])
    evidence = state.get("evidence", [])

    inconsistencies = state.get("inconsistencies", [])
    policy_violations = state.get("policy_violations", [])
    counterfactual_issues = state.get("counterfactual_issues", [])

    risk = state.get("risk_level", "MEDIUM")

    # -----------------------------
    # HARD FAIL CONDITIONS
    # -----------------------------
    if not claims:
        verdict = "INSUFFICIENT_DATA"

    elif not evidence:
        verdict = "LOW_EVIDENCE"

    # HIGH severity policy violation → reject
    elif any(v.get("severity") == "HIGH" for v in policy_violations):
        verdict = REJECT

    # -----------------------------
    # ESCALATION CONDITIONS
    # -----------------------------
    elif counterfactual_issues:
        verdict = ESCALATE

    elif inconsistencies and risk != "LOW":
        verdict = ESCALATE

    elif risk == "HIGH":
        verdict = ESCALATE

    # -----------------------------
    # CONFIDENCE-BASED DECISION
    # -----------------------------
    else:
        if confidence >= ACCEPT_THRESHOLD:
            verdict = ACCEPT
        elif confidence >= ESCALATE_THRESHOLD:
            verdict = ESCALATE
        else:
            verdict = REJECT

    # -----------------------------
    # EXPLANATION
    # -----------------------------
    explanation = build_explanation(state)

    # -----------------------------
    # SAVE
    # -----------------------------
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