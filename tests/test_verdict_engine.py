from rules.verdict_engine import verdict_engine

state_accept = {"confidence": 85}
result = verdict_engine(state_accept)
print("TEST:", result["verdict"])

state_escalate = {"confidence": 60}
result = verdict_engine(state_escalate)
print("TEST:", result["verdict"])

state_reject = {"confidence": 30}
result = verdict_engine(state_reject)
print("TEST:", result["verdict"])
