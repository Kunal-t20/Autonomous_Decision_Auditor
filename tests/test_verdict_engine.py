from rules.verdict_engine import verdict_engine
from core.constants import ACCEPT, ESCALATE, REJECT

def test_verdict_engine():

    # ACCEPT case
    state_accept = {
        "confidence": 0.85,
        "claims": ["AI reduces cost"],
        "evidence": ["Study A"]
    }
    result = verdict_engine(state_accept)
    assert result["verdict"] == ACCEPT

    # ESCALATE case
    state_escalate = {
        "confidence": 0.60,
        "claims": ["AI improves efficiency"],
        "evidence": ["Report B"]
    }
    result = verdict_engine(state_escalate)
    assert result["verdict"] == ESCALATE

    # REJECT case
    state_reject = {
        "confidence": 0.30,
        "claims": ["AI replaces all jobs"],
        "evidence": ["Weak blog"]
    }
    result = verdict_engine(state_reject)
    assert result["verdict"] == REJECT

    # INSUFFICIENT DATA case (NEW BEHAVIOR)
    state_insufficient = {
        "confidence": 0.9
    }
    result = verdict_engine(state_insufficient)
    assert result["verdict"] == "INSUFFICIENT_DATA"