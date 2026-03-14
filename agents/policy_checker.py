from utils.llm import call_llm

def policy_checker(state):
    policies = state.get("policies", [])
    if not policies:
        state["policy_violations"] = []
        return state

    claims = "\n".join(state.get("claims", []))
    policy_text = "\n".join(policies)
    
    prompt = f"""
    Check if the following claims violate any of these mandatory policies.
    Policies: {policy_text}
    Claims: {claims}
    List any violations briefly. If none, return 'NONE'.
    """
    
    response = call_llm(prompt)
    
    if "NONE" in response.upper():
        state["policy_violations"] = []
    else:
        # Penalize confidence scorer later based on this list
        state["policy_violations"] = [line.strip() for line in response.split("\n") if line.strip()]
        
    return state
