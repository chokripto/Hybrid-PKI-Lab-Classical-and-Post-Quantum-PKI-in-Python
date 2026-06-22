import pytest

from hybrid_pki.classical.keygen import generate_ecdsa_private_key, serialize_public_key
from hybrid_pki.hybrid.hybrid_certificate import create_unsigned_hybrid_certificate
from hybrid_pki.hybrid.hybrid_policy import HybridValidationPolicy, evaluate_policy
from hybrid_pki.pqc.oqs_provider import is_oqs_available


def test_hybrid_policy_strict_accepts_only_both_valid():
    assert evaluate_policy(
        HybridValidationPolicy.HYBRID_STRICT,
        classical_valid=True,
        pqc_valid=True,
    )

    assert not evaluate_policy(
        HybridValidationPolicy.HYBRID_STRICT,
        classical_valid=True,
        pqc_valid=False,
    )


def test_create_unsigned_hybrid_certificate():
    classical_key = generate_ecdsa_private_key()
    classical_public_key_pem = serialize_public_key(classical_key.public_key())

    certificate = create_unsigned_hybrid_certificate(
        subject="CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA",
        issuer="CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=classical_public_key_pem,
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=b"fake-pqc-public-key",
    )

    assert certificate.version == 1
    assert certificate.subject.startswith("CN=hybrid.example.com")
    assert certificate.classical_signature_b64 is None
    assert certificate.pqc_signature_b64 is None


@pytest.mark.skipif(
    not is_oqs_available(),
    reason="liboqs-python is not installed",
)
def test_hybrid_certificate_sign_verify_with_oqs():
    from hybrid_pki.hybrid.hybrid_signatures import sign_hybrid_certificate
    from hybrid_pki.hybrid.hybrid_validation import validate_hybrid_certificate
    from hybrid_pki.pqc.ml_dsa import MLDSA

    classical_ca_key = generate_ecdsa_private_key()

    pqc = MLDSA("ML-DSA-65")
    pqc_ca_keypair = pqc.generate_keypair()
    subject_pqc_keypair = pqc.generate_keypair()

    subject_classical_key = generate_ecdsa_private_key()
    subject_classical_public_pem = serialize_public_key(
        subject_classical_key.public_key()
    )

    certificate = create_unsigned_hybrid_certificate(
        subject="CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA",
        issuer="CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA",
        classical_algorithm="ECDSA-P256",
        classical_public_key_pem=subject_classical_public_pem,
        pqc_signature_algorithm="ML-DSA-65",
        pqc_public_key=subject_pqc_keypair.public_key,
    )

    signed_certificate = sign_hybrid_certificate(
        certificate=certificate,
        classical_ca_private_key=classical_ca_key,
        pqc_ca_secret_key=pqc_ca_keypair.secret_key,
        pqc_algorithm="ML-DSA-65",
    )

    result = validate_hybrid_certificate(
        certificate=signed_certificate,
        classical_ca_public_key=classical_ca_key.public_key(),
        pqc_ca_public_key=pqc_ca_keypair.public_key,
        policy=HybridValidationPolicy.HYBRID_STRICT,
    )

    assert result.valid


@pytest.mark.skipif(
    not is_oqs_available(),
    reason="liboqs-python is not installed",
)
def test_hybrid_handshake_with_oqs():
    from hybrid_pki.hybrid.hybrid_handshake import (
        client_hybrid_encapsulate,
        generate_server_hybrid_handshake_keys,
        server_hybrid_decapsulate,
    )

    server_keys = generate_server_hybrid_handshake_keys("ML-KEM-768")

    client_result = client_hybrid_encapsulate(
        server_classical_public_key_bytes=server_keys.classical_public_key_bytes,
        server_pqc_public_key=server_keys.pqc_public_key,
        pqc_algorithm=server_keys.pqc_algorithm,
    )

    server_secret = server_hybrid_decapsulate(
        server_classical_private_key=server_keys.classical_private_key,
        client_classical_public_key_bytes=client_result.client_classical_public_key_bytes,
        server_pqc_secret_key=server_keys.pqc_secret_key,
        pqc_ciphertext=client_result.pqc_ciphertext,
        pqc_algorithm=server_keys.pqc_algorithm,
    )

    assert server_secret == client_result.hybrid_secret
