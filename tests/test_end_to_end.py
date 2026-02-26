from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_audit_endpoint():
    response = client.post(
        "/audit",
        json={
            "decision": "APPROVE_LOAN",
            "reasoning": "AI helps automate tasks.",
            "evidence": ["No external evidence provided"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "verdict" in data
    assert "confidence" in data
    assert "explanation" in data