from datetime import UTC, datetime, timedelta

from hybrid_pki.hybrid.hybrid_certificate import (
    HybridCertificate,
    create_unsigned_hybrid_certificate,
    generate_hybrid_serial_number,
    is_hybrid_certificate_time_valid,
    load_hybrid_certificate,
    save_hybrid_certificate,
)


def test_generate_hybrid_serial_number_default_prefix():
    serial_number = generate_hybrid_serial_number()

    assert serial_number.startswith("HYB-")
    assert len(serial_number) == len("HYB-") + 16


def test_generate_hybrid_serial_number_custom_prefix():
    serial_number = generate_hybrid_serial_number(prefix="TEST")

    assert serial_number.startswith("TEST-")
    assert len(serial_number) == len("TEST-") + 16


def test_create_unsigned_hybrid_certificate_fields():
    public_key_pem = (
        b"-----BEGIN PUBLIC KEY-----\n" b"TEST\n" b"-----END PUBLIC KEY-----\n"
    )

    certificate = create_unsigned_hybrid_certificate(
        subject="CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA",
        issuer="CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=public_key_pem,
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"pqc-public-key",
        days_valid=365,
        serial_number="HYB-TESTSERIAL",
    )

    assert certificate.version == 1
    assert certificate.serial_number == "HYB-TESTSERIAL"
    assert certificate.subject == "CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA"
    assert certificate.issuer == "CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA"
    assert certificate.classical_algorithm == "ECDSA-P256"
    assert "BEGIN PUBLIC KEY" in certificate.classical_public_key_pem
    assert certificate.pqc_signature_algorithm == "ML-DSA-65"
    assert certificate.classical_signature_b64 is None
    assert certificate.pqc_signature_b64 is None
    assert certificate.pqc_public_key == b"pqc-public-key"


def test_hybrid_certificate_to_unsigned_dict_removes_signatures():
    certificate = HybridCertificate(
        version=1,
        serial_number="HYB-123",
        subject="CN=subject",
        issuer="CN=issuer",
        not_before=datetime.now(UTC).isoformat(),
        not_after=(datetime.now(UTC) + timedelta(days=1)).isoformat(),
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem="public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key_b64="cHFj",
        classical_signature_b64="classical-signature",
        pqc_signature_b64="pqc-signature",
    )

    unsigned_dict = certificate.to_unsigned_dict()

    assert unsigned_dict["classical_signature_b64"] is None
    assert unsigned_dict["pqc_signature_b64"] is None
    assert unsigned_dict["serial_number"] == "HYB-123"
    assert unsigned_dict["subject"] == "CN=subject"


def test_hybrid_certificate_unsigned_payload_is_stable_bytes():
    certificate = create_unsigned_hybrid_certificate(
        subject="CN=subject",
        issuer="CN=issuer",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=b"public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"pqc-public-key",
        days_valid=1,
        serial_number="HYB-STABLE",
    )

    payload_1 = certificate.to_unsigned_payload()
    payload_2 = certificate.to_unsigned_payload()

    assert isinstance(payload_1, bytes)
    assert payload_1 == payload_2
    assert b"HYB-STABLE" in payload_1
    assert b"classical_signature_b64" in payload_1
    assert b"pqc_signature_b64" in payload_1


def test_hybrid_certificate_to_dict_and_from_dict_roundtrip():
    certificate = create_unsigned_hybrid_certificate(
        subject="CN=subject",
        issuer="CN=issuer",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=b"public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"pqc-public-key",
        days_valid=1,
        serial_number="HYB-DICT",
    )

    data = certificate.to_dict()
    loaded_certificate = HybridCertificate.from_dict(data)

    assert loaded_certificate == certificate
    assert loaded_certificate.pqc_public_key == b"pqc-public-key"


def test_hybrid_certificate_to_json_and_from_json_roundtrip():
    certificate = create_unsigned_hybrid_certificate(
        subject="CN=subject",
        issuer="CN=issuer",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=b"public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"pqc-public-key",
        days_valid=1,
        serial_number="HYB-JSON",
    )

    json_data = certificate.to_json()
    loaded_certificate = HybridCertificate.from_json(json_data)

    assert loaded_certificate == certificate
    assert '"serial_number": "HYB-JSON"' in json_data


def test_save_and_load_hybrid_certificate(tmp_path):
    certificate_path = tmp_path / "hybrid_certificate.json"

    certificate = create_unsigned_hybrid_certificate(
        subject="CN=subject",
        issuer="CN=issuer",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=b"public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"pqc-public-key",
        days_valid=1,
        serial_number="HYB-FILE",
    )

    save_hybrid_certificate(certificate, certificate_path)

    assert certificate_path.exists()

    loaded_certificate = load_hybrid_certificate(certificate_path)

    assert loaded_certificate == certificate
    assert loaded_certificate.pqc_public_key == b"pqc-public-key"


def test_hybrid_certificate_time_valid_for_current_certificate():
    certificate = create_unsigned_hybrid_certificate(
        subject="CN=subject",
        issuer="CN=issuer",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=b"public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"pqc-public-key",
        days_valid=1,
        serial_number="HYB-TIME-VALID",
    )

    assert is_hybrid_certificate_time_valid(certificate) is True


def test_hybrid_certificate_time_invalid_when_expired():
    now = datetime.now(UTC)

    certificate = HybridCertificate(
        version=1,
        serial_number="HYB-EXPIRED",
        subject="CN=subject",
        issuer="CN=issuer",
        not_before=(now - timedelta(days=10)).isoformat(),
        not_after=(now - timedelta(days=1)).isoformat(),
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem="public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key_b64="cHFj",
    )

    assert is_hybrid_certificate_time_valid(certificate) is False


def test_hybrid_certificate_time_invalid_when_not_yet_valid():
    now = datetime.now(UTC)

    certificate = HybridCertificate(
        version=1,
        serial_number="HYB-FUTURE",
        subject="CN=subject",
        issuer="CN=issuer",
        not_before=(now + timedelta(days=1)).isoformat(),
        not_after=(now + timedelta(days=10)).isoformat(),
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem="public-key",
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key_b64="cHFj",
    )

    assert is_hybrid_certificate_time_valid(certificate) is False
