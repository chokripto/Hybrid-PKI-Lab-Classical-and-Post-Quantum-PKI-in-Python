from fastapi.testclient import TestClient

from hybrid_pki.api.main import app

client = TestClient(app)


def test_benchmark_status_endpoint():
    response = client.get("/benchmarks/status")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "available"
    assert "results_directory" in data
    assert "available_benchmarks" in data
    assert "key generation" in data["available_benchmarks"]
