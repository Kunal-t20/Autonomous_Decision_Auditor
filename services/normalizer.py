from typing import List
import re


def normalize_decision(decision: str) -> str:

    return decision.strip()


def normalize_reasoning(reasoning: str) -> str:

    cleaned = reasoning.strip()
    cleaned = re.sub(r"\s+", " ", cleaned) #remove whitespaces
    return cleaned


def normalize_evidence(evidence: List[str]) -> List[str]:
    seen = set()
    result: List[str] = []

    for item in evidence:
        cleaned = item.strip()
        if not cleaned:
            continue

        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)

    return result

