from db.session import SessionLocal
from db.models import AuditRecord

def save_audit(state: dict):
    db = SessionLocal()

    record = AuditRecord(
        reasoning=state.get("reasoning"),
        verdict=state.get("verdict"),
        confidence=state.get("confidence"),
        explanation=state.get("explanation"),
    )

    db.add(record)
    db.commit()
    db.close()
