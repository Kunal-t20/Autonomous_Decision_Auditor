from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from db.session import Base

class AuditRecord(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    reasoning = Column(String)
    verdict = Column(String)
    confidence = Column(Float)
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # NEW: Granular Details
    breakdown = Column(JSON)  # Stores claim_evidence_map and inconsistencies
    
    # NEW: HITL Support
    status = Column(String, default="COMPLETED") # Or "PENDING_REVIEW"
    human_verdict = Column(String, nullable=True)
    reviewer_notes = Column(String, nullable=True)
