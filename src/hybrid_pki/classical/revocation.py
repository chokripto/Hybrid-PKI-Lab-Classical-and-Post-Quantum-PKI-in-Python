import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization


class RevocationError(Exception):
    """
    Raised when revocation handling fails.
    """


def load_revoked_database(path: str | Path) -> list[dict]:
    """
    Load revoked certificates database from JSON.
    """
    file_path = Path(path)

    if not file_path.exists():
        return []

    return json.loads(file_path.read_text(encoding="utf-8"))


def save_revoked_database(path: str | Path, revoked_entries: list[dict]) -> None:
    """
    Save revoked certificates database to JSON.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        json.dumps(revoked_entries, indent=2),
        encoding="utf-8",
    )


def revoke_certificate(
    certificate: x509.Certificate,
    database_path: str | Path = "certs/revoked/revoked_certificates.json",
    reason: str = "keyCompromise",
) -> dict:
    """
    Add a certificate to the revoked database.
    """
    revoked_entries = load_revoked_database(database_path)

    serial_number = str(certificate.serial_number)

    for entry in revoked_entries:
        if entry["serial_number"] == serial_number:
            return entry

    revoked_entry = {
        "serial_number": serial_number,
        "subject": certificate.subject.rfc4514_string(),
        "issuer": certificate.issuer.rfc4514_string(),
        "revocation_date": datetime.now(UTC).isoformat(),
        "reason": reason,
    }

    revoked_entries.append(revoked_entry)
    save_revoked_database(database_path, revoked_entries)

    return revoked_entry


def is_certificate_revoked(
    certificate: x509.Certificate,
    database_path: str | Path = "certs/revoked/revoked_certificates.json",
) -> bool:
    """
    Check if a certificate is revoked using the JSON revoked database.
    """
    revoked_entries = load_revoked_database(database_path)
    serial_number = str(certificate.serial_number)

    return any(entry["serial_number"] == serial_number for entry in revoked_entries)


def create_crl(
    issuer_certificate: x509.Certificate,
    issuer_private_key,
    revoked_certificates: list[x509.Certificate],
    days_valid: int = 30,
) -> x509.CertificateRevocationList:
    """
    Create a Certificate Revocation List signed by the issuer CA.
    """
    now = datetime.now(UTC)

    builder = (
        x509.CertificateRevocationListBuilder()
        .issuer_name(issuer_certificate.subject)
        .last_update(now)
        .next_update(now + timedelta(days=days_valid))
    )

    for certificate in revoked_certificates:
        revoked_certificate = (
            x509.RevokedCertificateBuilder()
            .serial_number(certificate.serial_number)
            .revocation_date(now)
            .build()
        )
        builder = builder.add_revoked_certificate(revoked_certificate)

    crl = builder.sign(
        private_key=issuer_private_key,
        algorithm=hashes.SHA256(),
    )

    return crl


def save_crl_pem(crl: x509.CertificateRevocationList, path: str | Path) -> None:
    """
    Save a CRL as PEM.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(crl.public_bytes(serialization.Encoding.PEM))


def save_crl_der(crl: x509.CertificateRevocationList, path: str | Path) -> None:
    """
    Save a CRL as DER.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(crl.public_bytes(serialization.Encoding.DER))
