from db.session import SessionLocal
from db.models import AuditRecord


def save_audit(state: dict):
    db = SessionLocal()

    try:
        verdict = state.get("verdict", "UNKNOWN")
        confidence = float(state.get("confidence", 0))

        status = "PENDING_REVIEW" if verdict == "ESCALATE" else "COMPLETED"

        breakdown = {
            "claim_evidence_map": state.get("claim_evidence_map", {}),
            "inconsistencies": state.get("inconsistencies", []),
            "counterfactual_issues": state.get("counterfactual_issues", []),
            "policy_violations": state.get("policy_violations", []),
        }

        record = AuditRecord(
            # INPUT
            reasoning=state.get("reasoning"),
            evidence=state.get("evidence", []),
            policies=state.get("policies", []),

            # OUTPUT
            verdict=verdict,
            confidence=confidence,
            risk_level=state.get("risk_level"),

            explanation=state.get("explanation"),

            # DETAILS
            breakdown=breakdown,

            # SYSTEM
            retry_count=state.get("retry_count", 0),
            retry_history=state.get("retry_history", []),

            # HITL
            status=status,
        )

        db.add(record)

        # ensure ID generated
        db.flush()

        db.commit()

        return record.id

    except Exception as e:
        db.rollback()
        print(f"[DB ERROR] Failed to save audit: {e}")  #simple logging
        raise

    finally:
        db.close()