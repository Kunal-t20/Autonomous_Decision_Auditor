from fastapi import APIRouter
from graph.audit_graph import audit_app
from api.schemas import AuditRequest, AuditResponse
from agents.state import AuditState

router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
def run_audit(request: AuditRequest):

    state: AuditState = {
        "reasoning": request.reasoning,
        "claims": [],
        "evidence": [],
        "claim_evidence_map": {},
        "inconsistencies": [],
        "counterfactual_issues": [],
        "inconsistency_score": 0.0,
        "confidence": 0.0,
        "verdict": "",
        "explanation": "",
        "retry_count": 0,
    }

    result = audit_app.invoke(state)

    return {
        "verdict": result.get("verdict"),
        "confidence": result.get("confidence"),
        "explanation": result.get("explanation"),
    }