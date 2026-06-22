from fastapi.testclient import TestClient

from hybrid_pki.api.main import app

client = TestClient(app)


def test_hybrid_status_endpoint():
    response = client.get("/hybrid/status")

    assert response.status_code == 200

    data = response.json()

    assert data["hybrid_module"] == "available"
    assert "pqc_provider" in data
    assert "ca_material" in data
    assert "demo_certificate" in data
