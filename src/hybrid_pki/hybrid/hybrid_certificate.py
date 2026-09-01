from __future__ import annotations

import json
import secrets
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from hybrid_pki.pqc.pqc_serialization import base64_to_bytes, bytes_to_base64


@dataclass
class HybridCertificate:
    """
    Experimental hybrid certificate format.

    This is not a production X.509 hybrid certificate.
    It is a pedagogical JSON certificate used by Hybrid-PKI-Lab.
    """

    version: int
    serial_number: str

    subject: str
    issuer: str

    not_before: str
    not_after: str

    classical_algorithm: str
    classical_public_key_pem: str

    pqc_signature_algorithm: str
    pqc_public_key_b64: str

    classical_signature_b64: str | None = None
    pqc_signature_b64: str | None = None

    def to_unsigned_dict(self) -> dict:
        """
        Return the certificate payload without signatures.
        """
        data = asdict(self)
        data["classical_signature_b64"] = None
        data["pqc_signature_b64"] = None
        return data

    def to_unsigned_payload(self) -> bytes:
        """
        Return canonical JSON bytes used for signing.
        """
        return json.dumps(
            self.to_unsigned_dict(),
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def to_dict(self) -> dict:
        """
        Convert certificate to dictionary.
        """
        return asdict(self)

    def to_json(self) -> str:
        """
        Convert certificate to pretty JSON.
        """
        return json.dumps(
            self.to_dict(),
            indent=2,
            sort_keys=True,
        )

    @classmethod
    def from_dict(cls, data: dict) -> HybridCertificate:
        """Create and validate a certificate from an untrusted dictionary."""
        expected_fields = set(cls.__dataclass_fields__)
        provided_fields = set(data)
        if provided_fields != expected_fields:
            missing = sorted(expected_fields - provided_fields)
            unknown = sorted(provided_fields - expected_fields)
            raise ValueError(
                "Invalid hybrid certificate fields: "
                f"missing={missing}, unknown={unknown}"
            )

        certificate = cls(**data)
        if certificate.version != 1:
            raise ValueError("Unsupported hybrid certificate version")
        required_text = (
            certificate.serial_number,
            certificate.subject,
            certificate.issuer,
            certificate.classical_algorithm,
            certificate.classical_public_key_pem,
            certificate.pqc_signature_algorithm,
            certificate.pqc_public_key_b64,
        )
        if not all(isinstance(value, str) and value.strip() for value in required_text):
            raise ValueError(
                "Hybrid certificate contains an empty or invalid text field"
            )

        _ = certificate.pqc_public_key
        _parse_aware_datetime(certificate.not_before)
        _parse_aware_datetime(certificate.not_after)
        return certificate

    @classmethod
    def from_json(cls, data: str) -> HybridCertificate:
        """
        Create certificate from JSON string.
        """
        return cls.from_dict(json.loads(data))

    @property
    def pqc_public_key(self) -> bytes:
        """
        Return decoded PQC public key.
        """
        return base64_to_bytes(self.pqc_public_key_b64)


def _parse_aware_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid ISO-8601 certificate timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Certificate timestamps must include a timezone")
    return parsed.astimezone(UTC)


def generate_hybrid_serial_number(prefix: str = "HYB") -> str:
    """
    Generate a random hybrid certificate serial number.
    """
    return f"{prefix}-{secrets.token_hex(8).upper()}"


def create_unsigned_hybrid_certificate(
    subject: str,
    issuer: str,
    classical_algorithm: str,
    classical_public_key_pem: bytes,
    pqc_signature_algorithm: str,
    pqc_public_key: bytes,
    days_valid: int = 365,
    serial_number: str | None = None,
) -> HybridCertificate:
    """
    Create an unsigned hybrid certificate.
    """
    if not 1 <= days_valid <= 397:
        raise ValueError("days_valid must be between 1 and 397")

    now = datetime.now(UTC)

    return HybridCertificate(
        version=1,
        serial_number=serial_number or generate_hybrid_serial_number(),
        subject=subject,
        issuer=issuer,
        not_before=now.isoformat(),
        not_after=(now + timedelta(days=days_valid)).isoformat(),
        classical_algorithm=classical_algorithm,
        classical_public_key_pem=classical_public_key_pem.decode("utf-8"),
        pqc_signature_algorithm=pqc_signature_algorithm,
        pqc_public_key_b64=bytes_to_base64(pqc_public_key),
    )


def save_hybrid_certificate(
    certificate: HybridCertificate,
    path: str | Path,
) -> None:
    """
    Save hybrid certificate as JSON.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        certificate.to_json(),
        encoding="utf-8",
    )


def load_hybrid_certificate(path: str | Path) -> HybridCertificate:
    """
    Load hybrid certificate from JSON.
    """
    return HybridCertificate.from_json(Path(path).read_text(encoding="utf-8"))


def is_hybrid_certificate_time_valid(certificate: HybridCertificate) -> bool:
    """
    Verify hybrid certificate validity period.
    """
    now = datetime.now(UTC)
    try:
        not_before = _parse_aware_datetime(certificate.not_before)
        not_after = _parse_aware_datetime(certificate.not_after)
    except ValueError:
        return False

    return not_before <= not_after and not_before <= now <= not_after
