from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from graph.audit_graph import audit_app
from api.schemas import AuditRequest, AuditResponse, ResolutionRequest
from agents.state import AuditState
from db.models import AuditRecord
from db.session import SessionLocal
from services.redis_cache import rate_limit_exceeded

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/audit", response_model=AuditResponse)
def run_audit(payload: AuditRequest, http_request: Request):
    client_id = http_request.client.host if http_request.client else "unknown"
    if rate_limit_exceeded(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    state: AuditState = {
        "reasoning": payload.reasoning,
        "claims": [],
        "evidence": payload.evidence,
        "policies": payload.policies,
        "policy_violations": [],
        "claim_evidence_map": {},
        "inconsistencies": [],
        "counterfactual_issues": [],
        "inconsistency_score": 0.0,
        "confidence": 0.0,
        "verdict": "",
        "explanation": "",
        "retry_count": 0,
        "audit_id": 0,
    }

    result = audit_app.invoke(state)
    
    breakdown = {
        "claim_evidence_map": result.get("claim_evidence_map", {}),
        "inconsistencies": result.get("inconsistencies", []),
        "counterfactual_issues": result.get("counterfactual_issues", []),
        "policy_violations": result.get("policy_violations", [])
    }

    return {
        "verdict": result.get("verdict"),
        "confidence": result.get("confidence"),
        "explanation": result.get("explanation"),
        "breakdown": breakdown,
        "audit_id": result.get("audit_id"),
    }

@router.post("/audit/{audit_id}/resolve")
def resolve_audit(audit_id: int, request: ResolutionRequest, db: Session = Depends(get_db)):
    record = db.query(AuditRecord).filter(AuditRecord.id == audit_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Audit not found")
        
    if record.verdict != "ESCALATE" or record.status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Audit does not require resolution")
        
    record.human_verdict = request.final_verdict
    record.reviewer_notes = request.reviewer_notes
    record.status = "COMPLETED"
    
    db.commit()
    return {"status": "success", "audit_id": audit_id, "final_verdict": request.final_verdict}
