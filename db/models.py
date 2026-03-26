from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from db.session import Base


class AuditRecord(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # INPUT
    # -----------------------------
    reasoning = Column(String)
    evidence = Column(JSON)
    policies = Column(JSON)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    verdict = Column(String, index=True)
    confidence = Column(Float)
    risk_level = Column(String, index=True)

    explanation = Column(JSON)  # 🔥 FIXED

    # -----------------------------
    # ANALYSIS DETAILS
    # -----------------------------
    breakdown = Column(JSON)  # claims, inconsistencies, violations etc.

    # -----------------------------
    # SYSTEM / DEBUG
    # -----------------------------
    retry_count = Column(Integer, default=0)
    retry_history = Column(JSON)

    # -----------------------------
    # HITL
    # -----------------------------
    status = Column(String, default="COMPLETED", index=True)
    human_verdict = Column(String, nullable=True)
    reviewer_notes = Column(String, nullable=True)

    # -----------------------------
    # META
    # -----------------------------
    created_at = Column(DateTime, default=datetime.utcnow, index=True)