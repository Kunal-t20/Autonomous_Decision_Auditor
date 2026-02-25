from agents.state import AuditState
from utils.llm import call_llm


def claim_extractor(state: AuditState):

    reasoning = state.get("reasoning", "")

    prompt = f"""
Break the following reasoning into minimal factual claims.

Rules:
1. One claim per line.
2. Claims must be checkable.
3. Do not merge ideas.
4. Do not explain.
5. Return ONLY numbered list.

Reasoning:
{reasoning}
"""

    response = call_llm(prompt)
    raw_output = response.content if hasattr(response, "content") else str(response)

    lines = raw_output.split("\n")
    claims = []

    for line in lines:
        line = line.strip()

        if not line or len(line) < 3:
            continue

        if "." in line[:3]:
            line = line.split(".", 1)[1].strip()

        if line.startswith("-"):
            line = line[1:].strip()

        if line.lower().startswith("explanation"):
            continue

        claims.append(line)

    state["claims"] = claims
    return state