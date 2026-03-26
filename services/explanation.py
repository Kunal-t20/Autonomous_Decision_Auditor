def build_explanation(state: dict) -> dict:

    verdict = state.get("verdict", "UNKNOWN")
    confidence = state.get("confidence", 0)
    risk = state.get("risk_level", "UNKNOWN")

    inconsistencies = state.get("inconsistencies", [])
    policy_violations = state.get("policy_violations", [])
    counterfactual = state.get("counterfactual_issues", [])

    summary = []
    details = []

    # -----------------------------
    # POLICY VIOLATIONS
    # -----------------------------
    for v in policy_violations:
        details.append({
            "type": "policy_violation",
            "issue": v.get("issue"),
            "severity": v.get("severity"),
            "claim": v.get("claim")
        })

    # -----------------------------
    # INCONSISTENCIES
    # -----------------------------
    for inc in inconsistencies:
        details.append({
            "type": "inconsistency",
            "issue": inc.get("issue"),
            "severity": inc.get("severity"),
            "claim": inc.get("claim")
        })

    # -----------------------------
    # COUNTERFACTUAL ISSUES
    # -----------------------------
    for cf in counterfactual:
        details.append({
            "type": "counterfactual",
            "issue": cf.get("issue"),
            "severity": cf.get("severity"),
            "claim": cf.get("claim")
        })

    # -----------------------------
    # SUMMARY BUILDING
    # -----------------------------
    if policy_violations:
        summary.append("policy violations detected")

    if inconsistencies:
        summary.append("logical inconsistencies found")

    if counterfactual:
        summary.append("decision is fragile under counterfactual testing")

    if confidence < 0.5:
        summary.append("low confidence score")

    if not summary:
        summary.append("no major issues detected")

    return {
        "verdict": verdict,
        "confidence": round(confidence, 3),
        "risk": risk,
        "summary": summary,
        "details": details
    }