from agents.state import AuditState


def confidence_score(state: AuditState):

    claims = state.get("claims", [])
    total_claims = len(claims)

    claim_evidence_map = state.get("claim_evidence_map", {})

    supported = 0
    unsupported = 0

    for _, ev_list in claim_evidence_map.items():
        if len(ev_list) == 0:
            unsupported += 1
        else:
            supported += 1

    support_ratio = supported / total_claims if total_claims else 1.0

    inconsistencies = len(state.get("inconsistencies", []))
    policy_violations = len(state.get("policy_violations", []))

    score = support_ratio

    # penalties
    score -= inconsistencies * 0.20
    score -= policy_violations * 0.25

    score = max(0.0, min(1.0, score))

    state["confidence"] = score
    return state