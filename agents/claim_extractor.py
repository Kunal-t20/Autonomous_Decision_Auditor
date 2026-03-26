from agents.state import AuditState
from utils.llm import call_llm


def claim_extractor(state: AuditState):
    reasoning = state.get("reasoning", "").strip()

    if not reasoning:
        state["claims"] = []
        return state

    prompt = f"""
Break the following reasoning into minimal factual claims.

Rules:
1. One claim per line.
2. Claims must be checkable and specific.
3. Do not merge ideas.
4. Do not explain.
5. No headings, no extra text.
6. Return ONLY numbered list.

Reasoning:
{reasoning}
"""

    try:
        response = call_llm(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)
    except Exception:
        # fallback if LLM fails
        state["claims"] = [reasoning]
        return state

    lines = raw_output.split("\n")
    claims = []

    for line in lines:
        line = line.strip()

        # skip empty / junk
        if not line or len(line) < 5:
            continue

        # remove numbering (1. 2. etc)
        if "." in line[:4]:
            parts = line.split(".", 1)
            if parts[0].isdigit():
                line = parts[1].strip()

        # remove bullets
        if line.startswith("-"):
            line = line[1:].strip()

        # skip unwanted text
        if line.lower().startswith(("explanation", "note", "here")):
            continue

        # basic validation
        if len(line.split()) < 3:
            continue

        claims.append(line)

    # remove duplicates while preserving order
    seen = set()
    unique_claims = []
    for c in claims:
        if c not in seen:
            seen.add(c)
            unique_claims.append(c)

    # limit (LLM kabhi 50 lines de deta hai)
    MAX_CLAIMS = 10
    unique_claims = unique_claims[:MAX_CLAIMS]

    # fallback if nothing extracted
    if not unique_claims:
        unique_claims = [reasoning]

    state["claims"] = unique_claims
    return state