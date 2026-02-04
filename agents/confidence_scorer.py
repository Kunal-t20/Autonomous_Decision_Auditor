from agents.state import AuditState

def confidence_score(state:AuditState):

    total_claims=len(state["claims"])

    claim_evidence_map=state["claim_evidence_map"]
    unsupported=0
    for claim,ev_list in claim_evidence_map.items():
        if len(ev_list)==0:
            unsupported+=1
    unsupported_ratio=unsupported/total_claims if total_claims>0 else 0

    inconsistencies_count=len(state["inconsistencies"])

    fragile_count=len(state["counterfactual_issues"])

    score=100
    score-=unsupported_ratio*30
    score-=inconsistencies_count*25
    score-=fragile_count*15

    if score<0:
        score=0
    if score>100:
        score=100

    state["confidence"]=score
    return state
