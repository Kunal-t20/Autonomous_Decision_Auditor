from db.session import SessionLocal
from db.models import AuditRecord
import json

def save_audit(state: dict):
    db = SessionLocal()

    verdict = state.get("verdict")
    status = "PENDING_REVIEW" if verdict == "ESCALATE" else "COMPLETED"
    
    breakdown = {
        "claim_evidence_map": state.get("claim_evidence_map", {}),
        "inconsistencies": state.get("inconsistencies", []),
        "counterfactual_issues": state.get("counterfactual_issues", []),
        "policy_violations": state.get("policy_violations", [])
    }

    record = AuditRecord(
        reasoning=state.get("reasoning"),
        verdict=verdict,
        confidence=state.get("confidence"),
        explanation=state.get("explanation"),
        breakdown=breakdown,
        status=status
    )

    db.add(record)
    db.commit()
    db.close()

