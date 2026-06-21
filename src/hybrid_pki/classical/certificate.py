from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import NameOID


def create_csr(
    private_key,
    common_name: str,
    san_dns_names: list[str] | None = None,
    organization: str = "Hybrid PKI Lab",
    country: str = "MA",
) -> x509.CertificateSigningRequest:
    """
    Create a Certificate Signing Request.
    """
    san_dns_names = san_dns_names or [common_name]

    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ]
    )

    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName(dns_name) for dns_name in san_dns_names]
            ),
            critical=False,
        )
        .sign(
            private_key,
            hashes.SHA256(),
        )
    )

    return csr


def save_csr_pem(csr: x509.CertificateSigningRequest, path: str | Path) -> None:
    """
    Save a CSR as PEM.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(csr.public_bytes(serialization.Encoding.PEM))


def load_csr_pem(path: str | Path) -> x509.CertificateSigningRequest:
    """
    Load a CSR from a PEM file.
    """
    return x509.load_pem_x509_csr(Path(path).read_bytes())


def save_certificate_chain(
    leaf_certificate: x509.Certificate,
    chain_certificates: list[x509.Certificate],
    path: str | Path,
) -> None:
    """
    Save a full certificate chain as PEM.

    Order:
    1. leaf certificate
    2. intermediate certificate
    3. root certificate
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    data = leaf_certificate.public_bytes(serialization.Encoding.PEM)

    for certificate in chain_certificates:
        data += certificate.public_bytes(serialization.Encoding.PEM)

    file_path.write_bytes(data)


def certificate_to_pem(certificate: x509.Certificate) -> bytes:
    """
    Convert a certificate to PEM bytes.
    """
    return certificate.public_bytes(serialization.Encoding.PEM)


def certificate_to_der(certificate: x509.Certificate) -> bytes:
    """
    Convert a certificate to DER bytes.
    """
    return certificate.public_bytes(serialization.Encoding.DER)


def get_certificate_subject_common_name(certificate: x509.Certificate) -> str | None:
    """
    Extract the Common Name from a certificate subject.
    """
    attributes = certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)

    if not attributes:
        return None

    return attributes[0].value


def get_certificate_issuer_common_name(certificate: x509.Certificate) -> str | None:
    """
    Extract the Common Name from a certificate issuer.
    """
    attributes = certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)

    if not attributes:
        return None

    return attributes[0].value
