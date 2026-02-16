def build_explanation(state: dict) -> str:
    reasons = []

    evidence = state.get("evidence", [])
    inconsistency = state.get("inconsistency_score", 0)
    confidence = state.get("confidence", 0)
    verdict = state.get("verdict", "UNKNOWN")

    if len(evidence) == 0:
        reasons.append("no supporting evidence found")

    if inconsistency > 0.6:
        reasons.append("logical inconsistencies detected")

    if confidence < 0.5:
        reasons.append("low overall confidence")

    if not reasons:
        reasons.append("strong supporting evidence and consistent logic")

    reason_text = ", ".join(reasons).capitalize()

    return f"Verdict: {verdict}. Reason: {reason_text}."
