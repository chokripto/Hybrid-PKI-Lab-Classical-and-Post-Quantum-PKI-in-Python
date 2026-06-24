from pathlib import Path

from fastapi.testclient import TestClient

from hybrid_pki.api import routes_classical
from hybrid_pki.api.main import app

client = TestClient(app)


def configure_classical_paths(tmp_path: Path, monkeypatch):
    certs_root = tmp_path / "certs"
    root_dir = certs_root / "root"
    intermediate_dir = certs_root / "intermediate"
    issued_dir = certs_root / "issued"
    revoked_dir = certs_root / "revoked"

    monkeypatch.setattr(routes_classical, "CERTS_ROOT", certs_root)
    monkeypatch.setattr(routes_classical, "ROOT_DIR", root_dir)
    monkeypatch.setattr(routes_classical, "INTERMEDIATE_DIR", intermediate_dir)
    monkeypatch.setattr(routes_classical, "ISSUED_DIR", issued_dir)
    monkeypatch.setattr(routes_classical, "REVOKED_DIR", revoked_dir)

    monkeypatch.setattr(
        routes_classical,
        "ROOT_KEY_PATH",
        root_dir / "root_ca_private_key.pem",
    )
    monkeypatch.setattr(
        routes_classical,
        "ROOT_CERT_PATH",
        root_dir / "root_ca_certificate.pem",
    )
    monkeypatch.setattr(
        routes_classical,
        "INTERMEDIATE_KEY_PATH",
        intermediate_dir / "intermediate_ca_private_key.pem",
    )
    monkeypatch.setattr(
        routes_classical,
        "INTERMEDIATE_CERT_PATH",
        intermediate_dir / "intermediate_ca_certificate.pem",
    )
    monkeypatch.setattr(
        routes_classical,
        "REVOKED_DB_PATH",
        revoked_dir / "revoked_certificates.json",
    )

    return {
        "certs_root": certs_root,
        "root_dir": root_dir,
        "intermediate_dir": intermediate_dir,
        "issued_dir": issued_dir,
        "revoked_dir": revoked_dir,
    }


def test_classical_status_uses_configured_paths(tmp_path, monkeypatch):
    paths = configure_classical_paths(tmp_path, monkeypatch)

    response = client.get("/classical/status")

    assert response.status_code == 200

    data = response.json()

    assert data["root_ca"]["private_key_exists"] is False
    assert data["root_ca"]["certificate_exists"] is False
    assert data["intermediate_ca"]["private_key_exists"] is False
    assert data["intermediate_ca"]["certificate_exists"] is False
    assert data["storage"]["certs_root"] == str(paths["certs_root"])
    assert data["storage"]["issued_dir"] == str(paths["issued_dir"])
    assert data["storage"]["revoked_dir"] == str(paths["revoked_dir"])


def test_classical_intermediate_ca_requires_root_ca(tmp_path, monkeypatch):
    configure_classical_paths(tmp_path, monkeypatch)

    payload = {
        "common_name": "Hybrid PKI Lab Intermediate CA",
        "organization": "Hybrid PKI Lab",
        "country": "MA",
        "algorithm": "ecdsa",
        "days_valid": 365,
    }

    response = client.post("/classical/ca/intermediate/init", json=payload)

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data
    assert "Root CA private key not found" in data["detail"]


def test_classical_server_certificate_issue_requires_intermediate_ca(
    tmp_path,
    monkeypatch,
):
    configure_classical_paths(tmp_path, monkeypatch)

    payload = {
        "common_name": "server.example.com",
        "san_dns_names": ["server.example.com"],
        "organization": "Hybrid PKI Lab",
        "country": "MA",
        "algorithm": "ecdsa",
        "days_valid": 365,
    }

    response = client.post("/classical/certificates/server/issue", json=payload)

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data
    assert "Intermediate CA private key not found" in data["detail"]


def test_classical_full_certificate_workflow(tmp_path, monkeypatch):
    paths = configure_classical_paths(tmp_path, monkeypatch)

    root_payload = {
        "common_name": "Hybrid PKI Lab Root CA",
        "organization": "Hybrid PKI Lab",
        "country": "MA",
        "algorithm": "ecdsa",
        "days_valid": 3650,
    }

    root_response = client.post("/classical/ca/root/init", json=root_payload)

    assert root_response.status_code == 200

    root_data = root_response.json()

    assert root_data["status"] == "success"
    assert root_data["message"] == "Root CA generated successfully"
    assert Path(root_data["private_key_path"]).exists()
    assert Path(root_data["certificate_pem_path"]).exists()

    intermediate_payload = {
        "common_name": "Hybrid PKI Lab Intermediate CA",
        "organization": "Hybrid PKI Lab",
        "country": "MA",
        "algorithm": "ecdsa",
        "days_valid": 1825,
    }

    intermediate_response = client.post(
        "/classical/ca/intermediate/init",
        json=intermediate_payload,
    )

    assert intermediate_response.status_code == 200

    intermediate_data = intermediate_response.json()

    assert intermediate_data["status"] == "success"
    assert intermediate_data["message"] == "Intermediate CA generated successfully"
    assert Path(intermediate_data["private_key_path"]).exists()
    assert Path(intermediate_data["certificate_pem_path"]).exists()

    server_payload = {
        "common_name": "server.example.com",
        "san_dns_names": ["server.example.com", "www.server.example.com"],
        "organization": "Hybrid PKI Lab",
        "country": "MA",
        "algorithm": "ecdsa",
        "days_valid": 365,
    }

    server_response = client.post(
        "/classical/certificates/server/issue",
        json=server_payload,
    )

    assert server_response.status_code == 200

    server_data = server_response.json()

    assert server_data["status"] == "success"
    assert server_data["message"] == "Server certificate issued successfully"
    assert server_data["common_name"] == "server.example.com"
    assert Path(server_data["private_key_path"]).exists()
    assert Path(server_data["certificate_pem_path"]).exists()
    assert Path(server_data["fullchain_path"]).exists()

    verify_payload = {
        "certificate_path": server_data["certificate_pem_path"],
        "hostname": "server.example.com",
    }

    verify_response = client.post(
        "/classical/certificates/server/verify",
        json=verify_payload,
    )

    assert verify_response.status_code == 200

    verify_data = verify_response.json()

    assert verify_data["status"] == "accepted"
    assert verify_data["valid"] is True

    revoke_payload = {
        "certificate_path": server_data["certificate_pem_path"],
        "reason": "keyCompromise",
    }

    revoke_response = client.post(
        "/classical/certificates/server/revoke",
        json=revoke_payload,
    )

    assert revoke_response.status_code == 200

    revoke_data = revoke_response.json()

    assert revoke_data["status"] == "success"
    assert revoke_data["message"] == "Certificate revoked successfully"

    revoked_response = client.get("/classical/certificates/revoked")

    assert revoked_response.status_code == 200

    revoked_data = revoked_response.json()

    assert revoked_data["status"] == "success"
    assert revoked_data["count"] == 1
    assert len(revoked_data["revoked_certificates"]) == 1

    verify_after_revoke_response = client.post(
        "/classical/certificates/server/verify",
        json=verify_payload,
    )

    assert verify_after_revoke_response.status_code == 200

    verify_after_revoke_data = verify_after_revoke_response.json()

    assert verify_after_revoke_data["status"] == "rejected"
    assert verify_after_revoke_data["valid"] is False
    assert verify_after_revoke_data["reason"] == "certificate revoked"

    assert paths["certs_root"].exists()
    assert paths["root_dir"].exists()
    assert paths["intermediate_dir"].exists()
    assert paths["issued_dir"].exists()
    assert paths["revoked_dir"].exists()


def test_classical_verify_rejects_wrong_hostname(tmp_path, monkeypatch):
    configure_classical_paths(tmp_path, monkeypatch)

    client.post(
        "/classical/ca/root/init",
        json={
            "common_name": "Hybrid PKI Lab Root CA",
            "organization": "Hybrid PKI Lab",
            "country": "MA",
            "algorithm": "ecdsa",
            "days_valid": 3650,
        },
    )

    client.post(
        "/classical/ca/intermediate/init",
        json={
            "common_name": "Hybrid PKI Lab Intermediate CA",
            "organization": "Hybrid PKI Lab",
            "country": "MA",
            "algorithm": "ecdsa",
            "days_valid": 1825,
        },
    )

    server_response = client.post(
        "/classical/certificates/server/issue",
        json={
            "common_name": "server.example.com",
            "san_dns_names": ["server.example.com"],
            "organization": "Hybrid PKI Lab",
            "country": "MA",
            "algorithm": "ecdsa",
            "days_valid": 365,
        },
    )

    server_data = server_response.json()

    verify_response = client.post(
        "/classical/certificates/server/verify",
        json={
            "certificate_path": server_data["certificate_pem_path"],
            "hostname": "wrong.example.com",
        },
    )

    assert verify_response.status_code == 200

    verify_data = verify_response.json()

    assert verify_data["status"] == "rejected"
    assert verify_data["valid"] is False
