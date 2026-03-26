from agents.state import AuditState
from utils.llm import call_llm


def normalize_severity(s):
    s = str(s).upper()
    if "HIGH" in s:
        return "HIGH"
    if "LOW" in s:
        return "LOW"
    return "MEDIUM"


def policy_checker(state: AuditState):

    policies = state.get("policies", [])
    claims = state.get("claims", [])

    if not policies or not claims:
        state["policy_violations"] = []
        return state

    violations = []

    # -----------------------------
    # STEP 1: improved deterministic rules
    # -----------------------------
    for claim in claims:
        text = claim.lower()

        # age detection (better)
        if any(x in text for x in ["under 18", "minor", "teen", "17", "16"]):
            violations.append({
                "claim": claim,
                "policy": "Age restriction",
                "issue": "Underage subject detected",
                "severity": "HIGH",
                "type": "DETERMINISTIC",
                "confidence": 1.0
            })

        # weak evidence
        if any(x in text for x in ["no evidence", "no proof", "unsupported"]):
            violations.append({
                "claim": claim,
                "policy": "Evidence requirement",
                "issue": "Claim lacks supporting basis",
                "severity": "MEDIUM",
                "type": "DETERMINISTIC",
                "confidence": 0.9
            })

    # -----------------------------
    # STEP 2: batch LLM check
    # -----------------------------
    claims_text = "\n".join([f"{i+1}. {c}" for i, c in enumerate(claims)])
    policy_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(policies)])

    prompt = f"""
You are a strict policy auditor.

Policies:
{policy_text}

Claims:
{claims_text}

Return ONLY JSON.

Format:
{{
  "violations": [
    {{
      "claim_index": 1,
      "policy": "policy text",
      "reason": "short reason",
      "severity": "HIGH/MEDIUM/LOW",
      "confidence": 0.0-1.0
    }}
  ]
}}

If none:
{{"violations": []}}
"""

    try:
        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)

        import json
        parsed = json.loads(raw_output)

        for v in parsed.get("violations", []):
            idx = v.get("claim_index")

            if isinstance(idx, int) and 1 <= idx <= len(claims):
                violations.append({
                    "claim": claims[idx - 1],
                    "policy": v.get("policy", "Unknown"),
                    "issue": v.get("reason", "Violation"),
                    "severity": normalize_severity(v.get("severity")),
                    "type": "LLM",
                    "confidence": float(v.get("confidence", 0.7))
                })

    except Exception:
        pass

    # -----------------------------
    # STEP 3: deduplicate
    # -----------------------------
    unique = []
    seen = set()

    for v in violations:
        key = (v["claim"], v["policy"], v["issue"])
        if key not in seen:
            seen.add(key)
            unique.append(v)

    state["policy_violations"] = unique
    return state