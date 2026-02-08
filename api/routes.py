from fastapi import APIRouter
from graph.audit_graph import audit_app
from api.schemas import AuditRequest,AuditResponse

router=APIRouter()

@router.post("/audit",response_model=AuditResponse)
def run_audit(request:AuditRequest):

    state=request.dict()

    result=audit_app.invoke(state)

    return result


