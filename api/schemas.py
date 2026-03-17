from pydantic import BaseModel, Field
from typing import Literal, List


class AuditRequest(BaseModel):
    reasoning: str
    evidence: List[str] = Field(default_factory=list)
    policies: List[str] = Field(default_factory=list)


class AuditResponse(BaseModel):
    verdict: Literal["ACCEPT", "REJECT", "ESCALATE"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    breakdown: dict = Field(default_factory=dict)

class ResolutionRequest(BaseModel):
    final_verdict: Literal["ACCEPT", "REJECT"]
    reviewer_notes: str