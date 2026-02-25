from pydantic import BaseModel, Field
from typing import Literal


class AuditRequest(BaseModel):
    reasoning: str


class AuditResponse(BaseModel):
    verdict: Literal["ACCEPT", "REJECT", "ESCALATE"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str