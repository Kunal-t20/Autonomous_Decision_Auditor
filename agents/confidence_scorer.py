from agents.state import AuditState


def confidence_score(state: AuditState):

    total_claims = len(state.get("claims", []))

    claim_evidence_map = state.get("claim_evidence_map", {})

    unsupported = 0
    for _, ev_list in claim_evidence_map.items():
        if len(ev_list) == 0:
            unsupported += 1

    unsupported_ratio = unsupported / total_claims if total_claims else 0

    inconsistencies_count = len(state.get("inconsistencies", []))
    fragile_count = len(state.get("counterfactual_issues", []))

    score = 1.0
    score -= unsupported_ratio * 0.30
    score -= inconsistencies_count * 0.25
    score -= fragile_count * 0.15

    score = max(0.0, min(1.0, score))

    state["confidence"] = score
    return state