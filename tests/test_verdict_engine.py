from rules.verdict_engine import verdict_engine
from core.constants import ACCEPT, ESCALATE, REJECT

def test_verdict_engine():
    state_accept = {"confidence": 0.85}
    result = verdict_engine(state_accept)
    assert result["verdict"] == ACCEPT

    state_escalate = {"confidence": 0.60}
    result = verdict_engine(state_escalate)
    assert result["verdict"] == ESCALATE

    state_reject = {"confidence": 0.30}
    result = verdict_engine(state_reject)
    assert result["verdict"] == REJECT
