from fastapi.testclient import TestClient

from hybrid_pki.api.main import app

client = TestClient(app)


def test_pqc_status_returns_unavailable_when_oqs_disabled():
    response = client.get("/pqc/status")

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is False
    assert "message" in data
    assert isinstance(data["message"], str)


def test_hybrid_status_reports_pqc_unavailable_when_oqs_disabled():
    response = client.get("/hybrid/status")

    assert response.status_code == 200

    data = response.json()

    assert data["hybrid_module"] == "available"
    assert "pqc_provider" in data
    assert data["pqc_provider"]["available"] is False
    assert "message" in data["pqc_provider"]


def test_hybrid_ca_create_demo_returns_service_unavailable_without_oqs():
    response = client.post("/hybrid/ca/create-demo")

    assert response.status_code == 503

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], str)


def test_hybrid_certificate_create_demo_returns_service_unavailable_without_oqs():
    payload = {
        "subject": "CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA",
        "issuer": "CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA",
        "classical_algorithm": "ECDSA-P256",
        "pqc_signature_algorithm": "ML-DSA-65",
        "days_valid": 365,
    }

    response = client.post("/hybrid/certificates/create-demo", json=payload)

    assert response.status_code == 503

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], str)


def test_hybrid_certificate_verify_demo_returns_error_without_oqs():
    payload = {
        "certificate_path": "certs/hybrid/hybrid.example.com_certificate.json",
        "policy": "hybrid-strict",
    }

    response = client.post("/hybrid/certificates/verify-demo", json=payload)

    assert response.status_code in {404, 503}

    data = response.json()

    assert "detail" in data


def test_hybrid_handshake_returns_service_unavailable_without_oqs():
    payload = {
        "pqc_algorithm": "ML-KEM-768",
    }

    response = client.post("/hybrid/handshake/simulate", json=payload)

    assert response.status_code == 503

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], str)
