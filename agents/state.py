from typing import TypedDict, List, Dict, Optional


class AuditState(TypedDict, total=False):

    # -----------------------------
    # INPUT
    # -----------------------------
    reasoning: str
    evidence: List[str]
    policies: List[str]

    # -----------------------------
    # EXTRACTION
    # -----------------------------
    claims: List[str]
    claim_evidence_map: Dict[str, List[str]]

    # -----------------------------
    # ANALYSIS
    # -----------------------------
    inconsistencies: List[Dict]
    inconsistency_score: float

    counterfactual_issues: List[Dict]

    policy_violations: List[Dict]

    # -----------------------------
    # SCORING
    # -----------------------------
    confidence: float
    risk_level: str  # LOW / MEDIUM / HIGH

    # -----------------------------
    # OUTPUT
    # -----------------------------
    verdict: str
    explanation: Dict[str, str]

    # -----------------------------
    # SYSTEM
    # -----------------------------
    retry_count: int
    retry_history: List[Dict]
    retry_exceeded: bool

    audit_id: Optional[int]