from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any


# -----------------------------
# REQUEST
# -----------------------------
class AuditRequest(BaseModel):
    decision: Optional[str] = None  # optional for flexibility
    reasoning: str
    evidence: List[str] = Field(default_factory=list)
    policies: List[str] = Field(default_factory=list)


# -----------------------------
# OPTIONAL STRUCTURED TYPES
# -----------------------------
class RuleViolation(BaseModel):
    rule_name: str
    description: str


class StabilityCheck(BaseModel):
    stable: bool
    variations: List[str] = Field(default_factory=list)


class CounterfactualResult(BaseModel):
    changed: bool
    details: Optional[str] = None


class AuditBreakdown(BaseModel):
    rule_violations: List[RuleViolation] = Field(default_factory=list)
    stability: Optional[StabilityCheck] = None
    counterfactual: Optional[CounterfactualResult] = None


# -----------------------------
# RESPONSE
# -----------------------------
class AuditResponse(BaseModel):
    verdict: Literal["ACCEPT", "REJECT", "ESCALATE"]
    confidence: float = Field(..., ge=0.0, le=1.0)

    explanation: Dict[str, Any]

    breakdown: Dict[str, Any] = Field(default_factory=dict)

    audit_id: Optional[int] = None


# -----------------------------
# HUMAN REVIEW
# -----------------------------
class ResolutionRequest(BaseModel):
    final_verdict: Literal["ACCEPT", "REJECT"]
    reviewer_notes: str