import json

from fastapi.testclient import TestClient

from hybrid_pki.api import routes_benchmarks
from hybrid_pki.api.main import app

client = TestClient(app)


def test_benchmark_status_endpoint_structure(tmp_path, monkeypatch):
    monkeypatch.setattr(routes_benchmarks, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(
        routes_benchmarks,
        "KEYGEN_RESULTS_PATH",
        tmp_path / "keygen_results.json",
    )
    monkeypatch.setattr(
        routes_benchmarks,
        "SIGNATURE_RESULTS_PATH",
        tmp_path / "signature_results.json",
    )
    monkeypatch.setattr(
        routes_benchmarks,
        "HANDSHAKE_RESULTS_PATH",
        tmp_path / "handshake_results.json",
    )

    response = client.get("/benchmarks/status")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "available"
    assert data["results_directory"] == str(tmp_path)
    assert "results" in data
    assert "keygen" in data["results"]
    assert "signatures" in data["results"]
    assert "handshake" in data["results"]
    assert "available_benchmarks" in data


def test_run_keygen_benchmark_endpoint_uses_mocked_benchmarks(tmp_path, monkeypatch):
    keygen_path = tmp_path / "keygen_results.json"

    monkeypatch.setattr(routes_benchmarks, "KEYGEN_RESULTS_PATH", keygen_path)
    monkeypatch.setattr(
        routes_benchmarks,
        "benchmark_classical_keygen",
        lambda: {"RSA-3072": {"average_ms": 1.0}},
    )
    monkeypatch.setattr(
        routes_benchmarks,
        "benchmark_pqc_keygen",
        lambda: {"ML-KEM-768": {"status": "skipped"}},
    )

    response = client.post("/benchmarks/run-keygen")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["message"] == "Key generation benchmark completed"
    assert data["results_path"] == str(keygen_path)
    assert data["results"]["benchmark"] == "key generation"
    assert data["results"]["classical"]["RSA-3072"]["average_ms"] == 1.0
    assert data["results"]["pqc"]["ML-KEM-768"]["status"] == "skipped"

    assert keygen_path.exists()

    saved_data = json.loads(keygen_path.read_text(encoding="utf-8"))
    assert saved_data == data["results"]


def test_run_signature_benchmark_endpoint_uses_mocked_benchmarks(
    tmp_path,
    monkeypatch,
):
    signature_path = tmp_path / "signature_results.json"

    monkeypatch.setattr(routes_benchmarks, "SIGNATURE_RESULTS_PATH", signature_path)
    monkeypatch.setattr(
        routes_benchmarks,
        "benchmark_classical_signatures",
        lambda: {"Ed25519": {"sign_average_ms": 1.0}},
    )
    monkeypatch.setattr(
        routes_benchmarks,
        "benchmark_pqc_signatures",
        lambda: {"ML-DSA-65": {"status": "skipped"}},
    )

    response = client.post("/benchmarks/run-signatures")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["message"] == "Signature benchmark completed"
    assert data["results_path"] == str(signature_path)
    assert data["results"]["benchmark"] == "signatures"
    assert data["results"]["classical"]["Ed25519"]["sign_average_ms"] == 1.0
    assert data["results"]["pqc"]["ML-DSA-65"]["status"] == "skipped"

    assert signature_path.exists()

    saved_data = json.loads(signature_path.read_text(encoding="utf-8"))
    assert saved_data == data["results"]


def test_run_handshake_benchmark_endpoint_uses_mocked_benchmark(
    tmp_path,
    monkeypatch,
):
    handshake_path = tmp_path / "handshake_results.json"

    monkeypatch.setattr(routes_benchmarks, "HANDSHAKE_RESULTS_PATH", handshake_path)
    monkeypatch.setattr(
        routes_benchmarks,
        "benchmark_handshakes",
        lambda: {"X25519": {"average_ms": 1.0}},
    )

    response = client.post("/benchmarks/run-handshake")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["message"] == "Handshake benchmark completed"
    assert data["results_path"] == str(handshake_path)
    assert data["results"]["benchmark"] == "handshake"
    assert data["results"]["results"]["X25519"]["average_ms"] == 1.0

    assert handshake_path.exists()

    saved_data = json.loads(handshake_path.read_text(encoding="utf-8"))
    assert saved_data == data["results"]


def test_get_benchmark_results_returns_saved_results(tmp_path, monkeypatch):
    keygen_path = tmp_path / "keygen_results.json"
    signature_path = tmp_path / "signature_results.json"
    handshake_path = tmp_path / "handshake_results.json"

    keygen_data = {
        "benchmark": "key generation",
        "classical": {"RSA-3072": {"average_ms": 1.0}},
    }
    signature_data = {
        "benchmark": "signatures",
        "classical": {"Ed25519": {"average_ms": 1.0}},
    }
    handshake_data = {
        "benchmark": "handshake",
        "results": {"X25519": {"average_ms": 1.0}},
    }

    keygen_path.write_text(json.dumps(keygen_data), encoding="utf-8")
    signature_path.write_text(json.dumps(signature_data), encoding="utf-8")
    handshake_path.write_text(json.dumps(handshake_data), encoding="utf-8")

    monkeypatch.setattr(routes_benchmarks, "KEYGEN_RESULTS_PATH", keygen_path)
    monkeypatch.setattr(routes_benchmarks, "SIGNATURE_RESULTS_PATH", signature_path)
    monkeypatch.setattr(routes_benchmarks, "HANDSHAKE_RESULTS_PATH", handshake_path)

    response = client.get("/benchmarks/results")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["results"]["keygen"] == keygen_data
    assert data["results"]["signatures"] == signature_data
    assert data["results"]["handshake"] == handshake_data


def test_get_benchmark_results_returns_none_when_files_do_not_exist(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        routes_benchmarks,
        "KEYGEN_RESULTS_PATH",
        tmp_path / "missing_keygen_results.json",
    )
    monkeypatch.setattr(
        routes_benchmarks,
        "SIGNATURE_RESULTS_PATH",
        tmp_path / "missing_signature_results.json",
    )
    monkeypatch.setattr(
        routes_benchmarks,
        "HANDSHAKE_RESULTS_PATH",
        tmp_path / "missing_handshake_results.json",
    )

    response = client.get("/benchmarks/results")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["results"]["keygen"] is None
    assert data["results"]["signatures"] is None
    assert data["results"]["handshake"] is None
