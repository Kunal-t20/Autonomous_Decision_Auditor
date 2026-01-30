from agents.state  import AuditState
from utils.llm import call_llm


def claim_extractor(state:AuditState):
    reasoning = state["reasoning"]

    prompt=f"""
    break the following resoning into the minimal factual claims.

    Rules:
    1. Each line must contain one claim only.
    2. Claim must be readable and checkavle.
    3. Do not merge multiple idea in it.
    4. Do not expain anything.
    5. Return only a numbered list.

    Resoning:
    {reasoning}

"""
    #llm call
    response=call_llm(prompt)
    #retrieve the content from object created by llm
    raw_output=response.content if hasattr(response, "content") else str(response)


    #clean and splite raw output 
    lines=raw_output.split("\n")

    claims=[]
    for line in lines:
        line=line.strip()

        if not line:
            continue

        if "." in line[:3]:
            line = line.split(".", 1)[1].strip()
        if line.startswith("-"):
            line = line[1:].strip()

        claims.append(line)

    
    state["claims"]=claims

    return state



