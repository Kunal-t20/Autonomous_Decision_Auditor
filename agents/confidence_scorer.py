from agents.state import AuditState


def severity_weight(s):
    s = str(s).upper()
    if s == "HIGH":
        return 0.4
    if s == "MEDIUM":
        return 0.2
    return 0.1


def confidence_score(state: AuditState):

    claims = state.get("claims", [])
    total_claims = len(claims)

    claim_evidence_map = state.get("claim_evidence_map", {})

    # -----------------------------
    # SUPPORT SCORE
    # -----------------------------
    supported = 0

    for _, ev_list in claim_evidence_map.items():
        if len(ev_list) > 0:
            supported += 1

    support_ratio = supported / total_claims if total_claims else 1.0

    score = support_ratio

    # -----------------------------
    # INCONSISTENCY PENALTY
    # -----------------------------
    for item in state.get("inconsistencies", []):
        score -= severity_weight(item.get("severity", "MEDIUM"))

    # -----------------------------
    # POLICY PENALTY
    # -----------------------------
    for item in state.get("policy_violations", []):
        score -= severity_weight(item.get("severity", "MEDIUM"))

    # -----------------------------
    # COUNTERFACTUAL PENALTY
    # -----------------------------
    for item in state.get("counterfactual_issues", []):
        score -= 0.3  # high impact

    # -----------------------------
    # NORMALIZE
    # -----------------------------
    score = max(0.0, min(1.0, score))

    # -----------------------------
    # OPTIONAL: RISK LABEL
    # -----------------------------
    if score > 0.75:
        risk = "LOW"
    elif score > 0.4:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    state["confidence"] = round(score, 3)
    state["risk_level"] = risk

    return state