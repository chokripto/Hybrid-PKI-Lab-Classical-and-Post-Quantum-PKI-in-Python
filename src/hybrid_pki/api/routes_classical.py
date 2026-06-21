from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from hybrid_pki.classical.ca import (
    create_intermediate_ca_certificate,
    create_root_ca_certificate,
    issue_server_certificate,
    load_certificate_pem,
    save_certificate_der,
    save_certificate_pem,
)
from hybrid_pki.classical.certificate import (
    create_csr,
    save_certificate_chain,
    save_csr_pem,
)
from hybrid_pki.classical.chain_validation import (
    CertificateValidationError,
    validate_chain,
)
from hybrid_pki.classical.keygen import (
    generate_ecdsa_private_key,
    generate_ed25519_private_key,
    generate_rsa_private_key,
    load_private_key,
    save_pem_file,
    serialize_private_key,
    serialize_public_key,
)
from hybrid_pki.classical.revocation import (
    is_certificate_revoked,
    load_revoked_database,
    revoke_certificate,
)

router = APIRouter(
    prefix="/classical",
    tags=["Classical PKI"],
)


CERTS_ROOT = Path("certs")
ROOT_DIR = CERTS_ROOT / "root"
INTERMEDIATE_DIR = CERTS_ROOT / "intermediate"
ISSUED_DIR = CERTS_ROOT / "issued"
REVOKED_DIR = CERTS_ROOT / "revoked"

ROOT_KEY_PATH = ROOT_DIR / "root_ca_private_key.pem"
ROOT_CERT_PATH = ROOT_DIR / "root_ca_certificate.pem"

INTERMEDIATE_KEY_PATH = INTERMEDIATE_DIR / "intermediate_ca_private_key.pem"
INTERMEDIATE_CERT_PATH = INTERMEDIATE_DIR / "intermediate_ca_certificate.pem"

REVOKED_DB_PATH = REVOKED_DIR / "revoked_certificates.json"


class RootCARequest(BaseModel):
    common_name: str = Field(default="Hybrid PKI Lab Root CA")
    organization: str = Field(default="Hybrid PKI Lab")
    country: str = Field(default="MA")
    algorithm: str = Field(default="ecdsa", examples=["rsa", "ecdsa", "ed25519"])
    days_valid: int = Field(default=3650, ge=1)


class IntermediateCARequest(BaseModel):
    common_name: str = Field(default="Hybrid PKI Lab Intermediate CA")
    organization: str = Field(default="Hybrid PKI Lab")
    country: str = Field(default="MA")
    algorithm: str = Field(default="ecdsa", examples=["rsa", "ecdsa", "ed25519"])
    days_valid: int = Field(default=1825, ge=1)


class ServerCertificateRequest(BaseModel):
    common_name: str = Field(default="example.com")
    san_dns_names: list[str] = Field(default=["example.com", "www.example.com"])
    organization: str = Field(default="Hybrid PKI Lab")
    country: str = Field(default="MA")
    algorithm: str = Field(default="ecdsa", examples=["rsa", "ecdsa", "ed25519"])
    days_valid: int = Field(default=365, ge=1)


class VerifyCertificateRequest(BaseModel):
    certificate_path: str = Field(default="certs/issued/example.com_certificate.pem")
    hostname: str | None = Field(default="example.com")


class RevokeCertificateRequest(BaseModel):
    certificate_path: str = Field(default="certs/issued/example.com_certificate.pem")
    reason: str = Field(default="keyCompromise")


def generate_private_key(algorithm: str):
    normalized_algorithm = algorithm.lower()

    if normalized_algorithm == "rsa":
        return generate_rsa_private_key()

    if normalized_algorithm == "ecdsa":
        return generate_ecdsa_private_key()

    if normalized_algorithm == "ed25519":
        return generate_ed25519_private_key()

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported algorithm: {algorithm}",
    )


def ensure_file_exists(path: Path, description: str) -> None:
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{description} not found: {path}",
        )


@router.post("/ca/root/init")
def init_root_ca(request: RootCARequest):
    """
    Generate a classical Root CA.

    This creates:
    - Root CA private key
    - Root CA public key
    - Root CA certificate PEM
    - Root CA certificate DER
    """
    ROOT_DIR.mkdir(parents=True, exist_ok=True)

    private_key = generate_private_key(request.algorithm)

    certificate = create_root_ca_certificate(
        private_key=private_key,
        common_name=request.common_name,
        organization=request.organization,
        country=request.country,
        days_valid=request.days_valid,
    )

    save_pem_file(
        ROOT_KEY_PATH,
        serialize_private_key(private_key),
    )

    save_pem_file(
        ROOT_DIR / "root_ca_public_key.pem",
        serialize_public_key(private_key.public_key()),
    )

    save_certificate_pem(
        certificate,
        ROOT_CERT_PATH,
    )

    save_certificate_der(
        certificate,
        ROOT_DIR / "root_ca_certificate.der",
    )

    return {
        "status": "success",
        "message": "Root CA generated successfully",
        "algorithm": request.algorithm,
        "private_key_path": str(ROOT_KEY_PATH),
        "public_key_path": str(ROOT_DIR / "root_ca_public_key.pem"),
        "certificate_pem_path": str(ROOT_CERT_PATH),
        "certificate_der_path": str(ROOT_DIR / "root_ca_certificate.der"),
        "serial_number": str(certificate.serial_number),
        "subject": certificate.subject.rfc4514_string(),
        "issuer": certificate.issuer.rfc4514_string(),
    }


@router.post("/ca/intermediate/init")
def init_intermediate_ca(request: IntermediateCARequest):
    """
    Generate an Intermediate CA signed by the Root CA.
    """
    ensure_file_exists(ROOT_KEY_PATH, "Root CA private key")
    ensure_file_exists(ROOT_CERT_PATH, "Root CA certificate")

    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

    root_private_key = load_private_key(ROOT_KEY_PATH)
    root_certificate = load_certificate_pem(ROOT_CERT_PATH)

    intermediate_private_key = generate_private_key(request.algorithm)

    intermediate_certificate = create_intermediate_ca_certificate(
        intermediate_public_key=intermediate_private_key.public_key(),
        root_private_key=root_private_key,
        root_certificate=root_certificate,
        common_name=request.common_name,
        organization=request.organization,
        country=request.country,
        days_valid=request.days_valid,
    )

    save_pem_file(
        INTERMEDIATE_KEY_PATH,
        serialize_private_key(intermediate_private_key),
    )

    save_pem_file(
        INTERMEDIATE_DIR / "intermediate_ca_public_key.pem",
        serialize_public_key(intermediate_private_key.public_key()),
    )

    save_certificate_pem(
        intermediate_certificate,
        INTERMEDIATE_CERT_PATH,
    )

    save_certificate_der(
        intermediate_certificate,
        INTERMEDIATE_DIR / "intermediate_ca_certificate.der",
    )

    return {
        "status": "success",
        "message": "Intermediate CA generated successfully",
        "algorithm": request.algorithm,
        "private_key_path": str(INTERMEDIATE_KEY_PATH),
        "public_key_path": str(INTERMEDIATE_DIR / "intermediate_ca_public_key.pem"),
        "certificate_pem_path": str(INTERMEDIATE_CERT_PATH),
        "certificate_der_path": str(
            INTERMEDIATE_DIR / "intermediate_ca_certificate.der"
        ),
        "serial_number": str(intermediate_certificate.serial_number),
        "subject": intermediate_certificate.subject.rfc4514_string(),
        "issuer": intermediate_certificate.issuer.rfc4514_string(),
    }


@router.post("/certificates/server/issue")
def issue_classical_server_certificate(request: ServerCertificateRequest):
    """
    Issue a classical server certificate signed by the Intermediate CA.
    """
    ensure_file_exists(INTERMEDIATE_KEY_PATH, "Intermediate CA private key")
    ensure_file_exists(INTERMEDIATE_CERT_PATH, "Intermediate CA certificate")
    ensure_file_exists(ROOT_CERT_PATH, "Root CA certificate")

    ISSUED_DIR.mkdir(parents=True, exist_ok=True)

    intermediate_private_key = load_private_key(INTERMEDIATE_KEY_PATH)
    intermediate_certificate = load_certificate_pem(INTERMEDIATE_CERT_PATH)
    root_certificate = load_certificate_pem(ROOT_CERT_PATH)

    server_private_key = generate_private_key(request.algorithm)

    server_certificate = issue_server_certificate(
        subject_public_key=server_private_key.public_key(),
        issuer_private_key=intermediate_private_key,
        issuer_certificate=intermediate_certificate,
        common_name=request.common_name,
        san_dns_names=request.san_dns_names,
        organization=request.organization,
        country=request.country,
        days_valid=request.days_valid,
    )

    safe_name = request.common_name.replace("*", "wildcard").replace("/", "_")

    private_key_path = ISSUED_DIR / f"{safe_name}_private_key.pem"
    public_key_path = ISSUED_DIR / f"{safe_name}_public_key.pem"
    csr_path = ISSUED_DIR / f"{safe_name}_csr.pem"
    cert_pem_path = ISSUED_DIR / f"{safe_name}_certificate.pem"
    cert_der_path = ISSUED_DIR / f"{safe_name}_certificate.der"
    fullchain_path = ISSUED_DIR / f"{safe_name}_fullchain.pem"

    csr = create_csr(
        private_key=server_private_key,
        common_name=request.common_name,
        san_dns_names=request.san_dns_names,
        organization=request.organization,
        country=request.country,
    )

    save_pem_file(
        private_key_path,
        serialize_private_key(server_private_key),
    )

    save_pem_file(
        public_key_path,
        serialize_public_key(server_private_key.public_key()),
    )

    save_csr_pem(csr, csr_path)
    save_certificate_pem(server_certificate, cert_pem_path)
    save_certificate_der(server_certificate, cert_der_path)

    save_certificate_chain(
        leaf_certificate=server_certificate,
        chain_certificates=[intermediate_certificate, root_certificate],
        path=fullchain_path,
    )

    return {
        "status": "success",
        "message": "Server certificate issued successfully",
        "algorithm": request.algorithm,
        "common_name": request.common_name,
        "san_dns_names": request.san_dns_names,
        "private_key_path": str(private_key_path),
        "public_key_path": str(public_key_path),
        "csr_path": str(csr_path),
        "certificate_pem_path": str(cert_pem_path),
        "certificate_der_path": str(cert_der_path),
        "fullchain_path": str(fullchain_path),
        "serial_number": str(server_certificate.serial_number),
        "subject": server_certificate.subject.rfc4514_string(),
        "issuer": server_certificate.issuer.rfc4514_string(),
    }


@router.post("/certificates/server/verify")
def verify_classical_server_certificate(request: VerifyCertificateRequest):
    """
    Verify a classical server certificate against the Intermediate CA and Root CA.
    """
    certificate_path = Path(request.certificate_path)

    ensure_file_exists(certificate_path, "Server certificate")
    ensure_file_exists(INTERMEDIATE_CERT_PATH, "Intermediate CA certificate")
    ensure_file_exists(ROOT_CERT_PATH, "Root CA certificate")

    server_certificate = load_certificate_pem(certificate_path)
    intermediate_certificate = load_certificate_pem(INTERMEDIATE_CERT_PATH)
    root_certificate = load_certificate_pem(ROOT_CERT_PATH)

    if is_certificate_revoked(server_certificate, REVOKED_DB_PATH):
        return {
            "status": "rejected",
            "valid": False,
            "reason": "certificate revoked",
            "serial_number": str(server_certificate.serial_number),
        }

    try:
        validate_chain(
            leaf_certificate=server_certificate,
            intermediate_certificates=[intermediate_certificate],
            root_certificate=root_certificate,
            hostname=request.hostname,
        )

    except CertificateValidationError as exc:
        return {
            "status": "rejected",
            "valid": False,
            "reason": str(exc),
            "serial_number": str(server_certificate.serial_number),
        }

    return {
        "status": "accepted",
        "valid": True,
        "reason": "certificate is valid",
        "serial_number": str(server_certificate.serial_number),
        "subject": server_certificate.subject.rfc4514_string(),
        "issuer": server_certificate.issuer.rfc4514_string(),
    }


@router.post("/certificates/server/revoke")
def revoke_classical_server_certificate(request: RevokeCertificateRequest):
    """
    Revoke a classical server certificate.
    """
    certificate_path = Path(request.certificate_path)

    ensure_file_exists(certificate_path, "Server certificate")

    REVOKED_DIR.mkdir(parents=True, exist_ok=True)

    certificate = load_certificate_pem(certificate_path)

    revoked_entry = revoke_certificate(
        certificate=certificate,
        database_path=REVOKED_DB_PATH,
        reason=request.reason,
    )

    return {
        "status": "success",
        "message": "Certificate revoked successfully",
        "revoked": revoked_entry,
    }


@router.get("/certificates/revoked")
def list_revoked_certificates():
    """
    List revoked classical certificates.
    """
    revoked_entries = load_revoked_database(REVOKED_DB_PATH)

    return {
        "status": "success",
        "count": len(revoked_entries),
        "revoked_certificates": revoked_entries,
    }


@router.get("/status")
def classical_pki_status():
    """
    Show status of the classical PKI files.
    """
    return {
        "root_ca": {
            "private_key_exists": ROOT_KEY_PATH.exists(),
            "certificate_exists": ROOT_CERT_PATH.exists(),
            "private_key_path": str(ROOT_KEY_PATH),
            "certificate_path": str(ROOT_CERT_PATH),
        },
        "intermediate_ca": {
            "private_key_exists": INTERMEDIATE_KEY_PATH.exists(),
            "certificate_exists": INTERMEDIATE_CERT_PATH.exists(),
            "private_key_path": str(INTERMEDIATE_KEY_PATH),
            "certificate_path": str(INTERMEDIATE_CERT_PATH),
        },
        "storage": {
            "certs_root": str(CERTS_ROOT),
            "issued_dir": str(ISSUED_DIR),
            "revoked_dir": str(REVOKED_DIR),
        },
    }
