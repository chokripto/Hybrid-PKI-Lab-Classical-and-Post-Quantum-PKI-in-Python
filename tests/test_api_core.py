from fastapi.testclient import TestClient

from hybrid_pki.api.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "Hybrid PKI Lab"
    assert data["status"] == "running"
    assert "documentation" in data
    assert data["documentation"] == "/docs"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data == {"status": "ok"}


def test_pqc_status_endpoint_with_oqs_disabled():
    response = client.get("/pqc/status")

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is False
    assert "message" in data
    assert "OQS support is disabled" in data["message"]


def test_hybrid_status_endpoint():
    response = client.get("/hybrid/status")

    assert response.status_code == 200

    data = response.json()

    assert data["hybrid_module"] == "available"
    assert "pqc_provider" in data
    assert data["pqc_provider"]["available"] is False


def test_benchmarks_status_endpoint():
    response = client.get("/benchmarks/status")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "available"
    assert "results_directory" in data
    assert "available_benchmarks" in data

    assert "key generation" in data["available_benchmarks"]
    assert "signatures" in data["available_benchmarks"]
    assert "handshake" in data["available_benchmarks"]


def test_classical_status_endpoint():
    response = client.get("/classical/status")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert len(data) > 0
