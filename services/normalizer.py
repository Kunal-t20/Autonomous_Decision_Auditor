from typing import List
import re


# -----------------------------
# DECISION NORMALIZATION
# -----------------------------
def normalize_decision(decision: str) -> str:

    if not decision:
        return "UNKNOWN"

    d = decision.strip().lower()

    mapping = {
        "accept": "ACCEPT",
        "approved": "ACCEPT",
        "approve": "ACCEPT",

        "reject": "REJECT",
        "denied": "REJECT",
        "deny": "REJECT",

        "escalate": "ESCALATE",
        "review": "ESCALATE",
        "needs review": "ESCALATE",
    }

    return mapping.get(d, d.upper())


# -----------------------------
# REASONING NORMALIZATION
# -----------------------------
def normalize_reasoning(reasoning: str) -> str:

    if not reasoning:
        return ""

    cleaned = reasoning.strip()

    # collapse whitespace
    cleaned = re.sub(r"\s+", " ", cleaned)

    # remove repeated punctuation
    cleaned = re.sub(r"[.]{2,}", ".", cleaned)
    cleaned = re.sub(r"[!]{2,}", "!", cleaned)

    # optional: lowercase first letter consistency
    cleaned = cleaned[0].upper() + cleaned[1:] if cleaned else cleaned

    return cleaned


# -----------------------------
# EVIDENCE NORMALIZATION
# -----------------------------
def normalize_evidence(evidence: List[str]) -> List[str]:

    seen = set()
    result: List[str] = []

    for item in evidence:
        if not item:
            continue

        cleaned = item.strip()

        # remove extra whitespace
        cleaned = re.sub(r"\s+", " ", cleaned)

        # remove trailing punctuation noise
        cleaned = cleaned.rstrip(" .,!")

        if len(cleaned) < 3:
            continue

        key = cleaned.lower()

        if key not in seen:
            seen.add(key)
            result.append(cleaned)

    return result