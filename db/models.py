from sqlalchemy import Column, Integer, String, Float, DateTime
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



