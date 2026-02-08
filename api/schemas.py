from pydantic import BaseModel, Field
from typing import List, Literal


class AuditRequest(BaseModel):
    decision: str
    reasoning: str
    evidence: List[str] = Field(..., min_items=1)


class AuditResponse(BaseModel):
    verdict: Literal["ACCEPT", "REJECT", "ESCALATE"]
    confidence: float = Field(..., ge=0.0, le=100.0)
    explanation: str
