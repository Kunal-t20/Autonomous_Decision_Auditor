from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_audit_endpoint():
    response = client.post(
        "/audit",
        json={"reasoning": "AI helps automate tasks."}
    )

    assert response.status_code == 200

    data = response.json()

    assert "verdict" in data
    assert "confidence" in data
    assert "explanation" in data
