from typing import TypedDict, List, Dict


class AuditState(TypedDict):
    reasoning: str
    claims: List[str]
    evidence: List[str]
    claim_evidence_map: Dict[str, List[str]]
    inconsistencies: List[Dict]
    counterfactual_issues: List[Dict]
    inconsistency_score: float
    confidence: float
    verdict: str
    explanation: str
    retry_count: int