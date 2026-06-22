from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from hybrid_pki.classical.keygen import (
    generate_ecdsa_private_key,
    save_pem_file,
    serialize_private_key,
    serialize_public_key,
)
from hybrid_pki.hybrid.hybrid_certificate import (
    create_unsigned_hybrid_certificate,
    load_hybrid_certificate,
    save_hybrid_certificate,
)
from hybrid_pki.hybrid.hybrid_handshake import (
    client_hybrid_encapsulate,
    generate_server_hybrid_handshake_keys,
    server_hybrid_decapsulate,
)
from hybrid_pki.hybrid.hybrid_policy import HybridValidationPolicy
from hybrid_pki.hybrid.hybrid_signatures import sign_hybrid_certificate
from hybrid_pki.hybrid.hybrid_validation import validate_hybrid_certificate
from hybrid_pki.pqc.ml_dsa import MLDSA
from hybrid_pki.pqc.oqs_provider import OQSUnavailableError, get_oqs_status
from hybrid_pki.pqc.pqc_serialization import (
    load_binary_file,
    save_base64_file,
    save_binary_file,
)

router = APIRouter(
    prefix="/hybrid",
    tags=["Hybrid PKI"],
)

HYBRID_DIR = Path("certs") / "hybrid"

HYBRID_CA_CLASSICAL_PRIVATE_KEY_PATH = (
    HYBRID_DIR / "hybrid_ca_classical_private_key.pem"
)
HYBRID_CA_CLASSICAL_PUBLIC_KEY_PATH = HYBRID_DIR / "hybrid_ca_classical_public_key.pem"
HYBRID_CA_PQC_PRIVATE_KEY_PATH = HYBRID_DIR / "hybrid_ca_pqc_private_key.bin"
HYBRID_CA_PQC_PUBLIC_KEY_PATH = HYBRID_DIR / "hybrid_ca_pqc_public_key.bin"

DEMO_CERTIFICATE_PATH = HYBRID_DIR / "hybrid.example.com_certificate.json"
DEMO_SUBJECT_CLASSICAL_PRIVATE_KEY_PATH = (
    HYBRID_DIR / "hybrid.example.com_classical_private_key.pem"
)
DEMO_SUBJECT_CLASSICAL_PUBLIC_KEY_PATH = (
    HYBRID_DIR / "hybrid.example.com_classical_public_key.pem"
)
DEMO_SUBJECT_PQC_PRIVATE_KEY_PATH = (
    HYBRID_DIR / "hybrid.example.com_pqc_private_key.bin"
)
DEMO_SUBJECT_PQC_PUBLIC_KEY_PATH = HYBRID_DIR / "hybrid.example.com_pqc_public_key.bin"


class HybridCertificateDemoRequest(BaseModel):
    subject: str = Field(
        default="CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA",
    )
    issuer: str = Field(
        default="CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA",
    )
    classical_algorithm: str = Field(default="ECDSA-P256")
    pqc_signature_algorithm: str = Field(default="ML-DSA-65")
    days_valid: int = Field(default=365, ge=1)


class HybridCertificateVerifyRequest(BaseModel):
    certificate_path: str = Field(
        default="certs/hybrid/hybrid.example.com_certificate.json",
    )
    policy: HybridValidationPolicy = Field(
        default=HybridValidationPolicy.HYBRID_STRICT,
    )


class HybridHandshakeRequest(BaseModel):
    pqc_algorithm: str = Field(default="ML-KEM-768")


def ensure_file_exists(path: Path, description: str) -> None:
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{description} not found: {path}",
        )


@router.get("/status")
def hybrid_status():
    """
    Show Hybrid PKI status.
    """
    oqs_status = get_oqs_status()

    return {
        "hybrid_module": "available",
        "pqc_provider": {
            "available": oqs_status.available,
            "message": oqs_status.message,
        },
        "ca_material": {
            "classical_private_key_exists": (
                HYBRID_CA_CLASSICAL_PRIVATE_KEY_PATH.exists()
            ),
            "classical_public_key_exists": HYBRID_CA_CLASSICAL_PUBLIC_KEY_PATH.exists(),
            "pqc_private_key_exists": HYBRID_CA_PQC_PRIVATE_KEY_PATH.exists(),
            "pqc_public_key_exists": HYBRID_CA_PQC_PUBLIC_KEY_PATH.exists(),
        },
        "demo_certificate": {
            "exists": DEMO_CERTIFICATE_PATH.exists(),
            "path": str(DEMO_CERTIFICATE_PATH),
        },
    }


@router.post("/ca/create-demo")
def create_hybrid_demo_ca():
    """
    Create demo Hybrid CA material.

    This creates:
    - Classical ECDSA CA key pair
    - PQC ML-DSA CA key pair

    Requires liboqs-python for the PQC part.
    """
    try:
        HYBRID_DIR.mkdir(parents=True, exist_ok=True)

        classical_ca_private_key = generate_ecdsa_private_key()
        classical_ca_public_key = classical_ca_private_key.public_key()

        pqc_signer = MLDSA("ML-DSA-65")
        pqc_ca_keypair = pqc_signer.generate_keypair()

        save_pem_file(
            HYBRID_CA_CLASSICAL_PRIVATE_KEY_PATH,
            serialize_private_key(classical_ca_private_key),
        )
        save_pem_file(
            HYBRID_CA_CLASSICAL_PUBLIC_KEY_PATH,
            serialize_public_key(classical_ca_public_key),
        )

        save_binary_file(
            HYBRID_CA_PQC_PRIVATE_KEY_PATH,
            pqc_ca_keypair.secret_key,
        )
        save_binary_file(
            HYBRID_CA_PQC_PUBLIC_KEY_PATH,
            pqc_ca_keypair.public_key,
        )

        save_base64_file(
            HYBRID_DIR / "hybrid_ca_pqc_public_key.b64",
            pqc_ca_keypair.public_key,
        )

        return {
            "status": "success",
            "message": "Hybrid demo CA material created successfully",
            "classical_algorithm": "ECDSA-P256",
            "pqc_signature_algorithm": "ML-DSA-65",
            "paths": {
                "classical_private_key": str(HYBRID_CA_CLASSICAL_PRIVATE_KEY_PATH),
                "classical_public_key": str(HYBRID_CA_CLASSICAL_PUBLIC_KEY_PATH),
                "pqc_private_key": str(HYBRID_CA_PQC_PRIVATE_KEY_PATH),
                "pqc_public_key": str(HYBRID_CA_PQC_PUBLIC_KEY_PATH),
            },
        }

    except OQSUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


@router.post("/certificates/create-demo")
def create_hybrid_demo_certificate(request: HybridCertificateDemoRequest):
    """
    Create and sign a demo hybrid certificate.

    Requires:
    - Hybrid demo CA material
    - liboqs-python
    """
    try:
        ensure_file_exists(
            HYBRID_CA_CLASSICAL_PRIVATE_KEY_PATH,
            "Hybrid CA classical private key",
        )
        ensure_file_exists(
            HYBRID_CA_PQC_PRIVATE_KEY_PATH,
            "Hybrid CA PQC private key",
        )

        from hybrid_pki.classical.keygen import load_private_key

        classical_ca_private_key = load_private_key(
            HYBRID_CA_CLASSICAL_PRIVATE_KEY_PATH
        )
        pqc_ca_secret_key = load_binary_file(HYBRID_CA_PQC_PRIVATE_KEY_PATH)

        subject_classical_private_key = generate_ecdsa_private_key()
        subject_classical_public_key_pem = serialize_public_key(
            subject_classical_private_key.public_key()
        )

        pqc_signer = MLDSA(request.pqc_signature_algorithm)
        subject_pqc_keypair = pqc_signer.generate_keypair()

        unsigned_certificate = create_unsigned_hybrid_certificate(
            subject=request.subject,
            issuer=request.issuer,
            classical_algorithm=request.classical_algorithm,
            classical_public_key_pem=subject_classical_public_key_pem,
            pqc_signature_algorithm=request.pqc_signature_algorithm,
            pqc_public_key=subject_pqc_keypair.public_key,
            days_valid=request.days_valid,
        )

        signed_certificate = sign_hybrid_certificate(
            certificate=unsigned_certificate,
            classical_ca_private_key=classical_ca_private_key,
            pqc_ca_secret_key=pqc_ca_secret_key,
            pqc_algorithm=request.pqc_signature_algorithm,
        )

        save_pem_file(
            DEMO_SUBJECT_CLASSICAL_PRIVATE_KEY_PATH,
            serialize_private_key(subject_classical_private_key),
        )
        save_pem_file(
            DEMO_SUBJECT_CLASSICAL_PUBLIC_KEY_PATH,
            subject_classical_public_key_pem,
        )
        save_binary_file(
            DEMO_SUBJECT_PQC_PRIVATE_KEY_PATH,
            subject_pqc_keypair.secret_key,
        )
        save_binary_file(
            DEMO_SUBJECT_PQC_PUBLIC_KEY_PATH,
            subject_pqc_keypair.public_key,
        )
        save_hybrid_certificate(
            signed_certificate,
            DEMO_CERTIFICATE_PATH,
        )

        return {
            "status": "success",
            "message": "Hybrid demo certificate created successfully",
            "certificate_path": str(DEMO_CERTIFICATE_PATH),
            "serial_number": signed_certificate.serial_number,
            "subject": signed_certificate.subject,
            "issuer": signed_certificate.issuer,
            "classical_algorithm": signed_certificate.classical_algorithm,
            "pqc_signature_algorithm": signed_certificate.pqc_signature_algorithm,
            "has_classical_signature": (
                signed_certificate.classical_signature_b64 is not None
            ),
            "has_pqc_signature": signed_certificate.pqc_signature_b64 is not None,
        }

    except OQSUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


@router.post("/certificates/verify-demo")
def verify_hybrid_demo_certificate(request: HybridCertificateVerifyRequest):
    """
    Verify a hybrid demo certificate.

    Requires:
    - Hybrid demo CA public keys
    - liboqs-python
    """
    try:
        certificate_path = Path(request.certificate_path)

        ensure_file_exists(certificate_path, "Hybrid certificate")
        ensure_file_exists(
            HYBRID_CA_CLASSICAL_PUBLIC_KEY_PATH,
            "Hybrid CA classical public key",
        )
        ensure_file_exists(
            HYBRID_CA_PQC_PUBLIC_KEY_PATH,
            "Hybrid CA PQC public key",
        )

        from cryptography.hazmat.primitives import serialization

        classical_ca_public_key = serialization.load_pem_public_key(
            HYBRID_CA_CLASSICAL_PUBLIC_KEY_PATH.read_bytes()
        )
        pqc_ca_public_key = load_binary_file(HYBRID_CA_PQC_PUBLIC_KEY_PATH)

        certificate = load_hybrid_certificate(certificate_path)

        result = validate_hybrid_certificate(
            certificate=certificate,
            classical_ca_public_key=classical_ca_public_key,
            pqc_ca_public_key=pqc_ca_public_key,
            policy=request.policy,
        )

        return {
            "valid": result.valid,
            "policy": result.policy,
            "classical_signature_valid": result.classical_signature_valid,
            "pqc_signature_valid": result.pqc_signature_valid,
            "time_valid": result.time_valid,
            "reason": result.reason,
            "certificate_path": str(certificate_path),
            "serial_number": certificate.serial_number,
            "subject": certificate.subject,
            "issuer": certificate.issuer,
        }

    except OQSUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


@router.post("/handshake/simulate")
def simulate_hybrid_handshake(request: HybridHandshakeRequest):
    """
    Simulate a hybrid handshake using X25519 + ML-KEM.

    Requires liboqs-python.
    """
    try:
        server_keys = generate_server_hybrid_handshake_keys(
            pqc_algorithm=request.pqc_algorithm
        )

        client_result = client_hybrid_encapsulate(
            server_classical_public_key_bytes=server_keys.classical_public_key_bytes,
            server_pqc_public_key=server_keys.pqc_public_key,
            pqc_algorithm=server_keys.pqc_algorithm,
        )

        server_secret = server_hybrid_decapsulate(
            server_classical_private_key=server_keys.classical_private_key,
            client_classical_public_key_bytes=(
                client_result.client_classical_public_key_bytes
            ),
            server_pqc_secret_key=server_keys.pqc_secret_key,
            pqc_ciphertext=client_result.pqc_ciphertext,
            pqc_algorithm=server_keys.pqc_algorithm,
        )

        secrets_match = server_secret == client_result.hybrid_secret

        return {
            "status": "success",
            "algorithm": {
                "classical": "X25519",
                "pqc": request.pqc_algorithm,
                "kdf": "HKDF-SHA256",
            },
            "secrets_match": secrets_match,
            "hybrid_secret_length": len(server_secret),
            "pqc_ciphertext_length": len(client_result.pqc_ciphertext),
            "server_classical_public_key_length": len(
                server_keys.classical_public_key_bytes
            ),
            "client_classical_public_key_length": len(
                client_result.client_classical_public_key_bytes
            ),
        }

    except OQSUnavailableError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
