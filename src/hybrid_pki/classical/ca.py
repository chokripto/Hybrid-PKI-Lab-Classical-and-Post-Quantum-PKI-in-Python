from datetime import UTC, datetime, timedelta
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def build_name(
    common_name: str,
    organization: str = "Hybrid PKI Lab",
    country: str = "MA",
) -> x509.Name:
    """
    Build an X.509 subject or issuer name.
    """
    return x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ]
    )


def create_root_ca_certificate(
    private_key,
    common_name: str = "Hybrid PKI Lab Root CA",
    organization: str = "Hybrid PKI Lab",
    country: str = "MA",
    days_valid: int = 3650,
) -> x509.Certificate:
    """
    Create a self-signed Root CA certificate.
    """
    subject = issuer = build_name(
        common_name=common_name,
        organization=organization,
        country=country,
    )

    now = datetime.now(UTC)

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=days_valid))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=1),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
            critical=False,
        )
        .sign(
            private_key=private_key,
            algorithm=hashes.SHA256(),
        )
    )

    return certificate


def create_intermediate_ca_certificate(
    intermediate_public_key,
    root_private_key,
    root_certificate: x509.Certificate,
    common_name: str = "Hybrid PKI Lab Intermediate CA",
    organization: str = "Hybrid PKI Lab",
    country: str = "MA",
    days_valid: int = 1825,
) -> x509.Certificate:
    """
    Create an Intermediate CA certificate signed by the Root CA.
    """
    subject = build_name(
        common_name=common_name,
        organization=organization,
        country=country,
    )

    now = datetime.now(UTC)

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(root_certificate.subject)
        .public_key(intermediate_public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=days_valid))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=0),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(intermediate_public_key),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(
                root_private_key.public_key()
            ),
            critical=False,
        )
        .sign(
            private_key=root_private_key,
            algorithm=hashes.SHA256(),
        )
    )

    return certificate


def issue_server_certificate(
    subject_public_key,
    issuer_private_key,
    issuer_certificate: x509.Certificate,
    common_name: str,
    san_dns_names: list[str],
    organization: str = "Hybrid PKI Lab",
    country: str = "MA",
    days_valid: int = 365,
) -> x509.Certificate:
    """
    Issue a server certificate signed by an issuer CA.
    """
    subject = build_name(
        common_name=common_name,
        organization=organization,
        country=country,
    )

    now = datetime.now(UTC)

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer_certificate.subject)
        .public_key(subject_public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + timedelta(days=days_valid))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName(dns_name) for dns_name in san_dns_names]
            ),
            critical=False,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
        .add_extension(
            x509.SubjectKeyIdentifier.from_public_key(subject_public_key),
            critical=False,
        )
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(
                issuer_private_key.public_key()
            ),
            critical=False,
        )
        .sign(
            private_key=issuer_private_key,
            algorithm=hashes.SHA256(),
        )
    )

    return certificate


def save_certificate_pem(certificate: x509.Certificate, path: str | Path) -> None:
    """
    Save a certificate as PEM.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))


def save_certificate_der(certificate: x509.Certificate, path: str | Path) -> None:
    """
    Save a certificate as DER.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(certificate.public_bytes(serialization.Encoding.DER))


def load_certificate_pem(path: str | Path) -> x509.Certificate:
    """
    Load a PEM certificate from disk.
    """
    return x509.load_pem_x509_certificate(Path(path).read_bytes())
