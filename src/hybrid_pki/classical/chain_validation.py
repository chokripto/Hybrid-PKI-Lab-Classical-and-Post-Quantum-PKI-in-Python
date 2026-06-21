from datetime import datetime, timezone

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa


class CertificateValidationError(Exception):
    """
    Raised when certificate validation fails.
    """


def verify_certificate_time(certificate: x509.Certificate) -> bool:
    """
    Verify that the certificate is currently valid.
    """
    now = datetime.now(timezone.utc)

    if now < certificate.not_valid_before_utc:
        raise CertificateValidationError("Certificate is not yet valid")

    if now > certificate.not_valid_after_utc:
        raise CertificateValidationError("Certificate has expired")

    return True


def verify_signature(
    child_certificate: x509.Certificate,
    issuer_certificate: x509.Certificate,
) -> bool:
    """
    Verify that child_certificate was signed by issuer_certificate.
    """
    issuer_public_key = issuer_certificate.public_key()

    try:
        if isinstance(issuer_public_key, rsa.RSAPublicKey):
            issuer_public_key.verify(
                child_certificate.signature,
                child_certificate.tbs_certificate_bytes,
                padding.PKCS1v15(),
                child_certificate.signature_hash_algorithm,
            )

        elif isinstance(issuer_public_key, ec.EllipticCurvePublicKey):
            issuer_public_key.verify(
                child_certificate.signature,
                child_certificate.tbs_certificate_bytes,
                ec.ECDSA(child_certificate.signature_hash_algorithm),
            )

        elif isinstance(issuer_public_key, ed25519.Ed25519PublicKey):
            issuer_public_key.verify(
                child_certificate.signature,
                child_certificate.tbs_certificate_bytes,
            )

        else:
            raise CertificateValidationError("Unsupported issuer public key type")

    except Exception as exc:
        raise CertificateValidationError("Invalid certificate signature") from exc

    return True


def verify_basic_constraints(
    certificate: x509.Certificate,
    expected_ca: bool,
) -> bool:
    """
    Verify the BasicConstraints extension.
    """
    try:
        basic_constraints = certificate.extensions.get_extension_for_class(
            x509.BasicConstraints
        ).value
    except x509.ExtensionNotFound as exc:
        raise CertificateValidationError("Missing BasicConstraints extension") from exc

    if basic_constraints.ca != expected_ca:
        raise CertificateValidationError(
            f"Invalid CA constraint: expected ca={expected_ca}"
        )

    return True


def verify_hostname(certificate: x509.Certificate, hostname: str) -> bool:
    """
    Verify that hostname exists in the certificate SAN extension.
    """
    try:
        san = certificate.extensions.get_extension_for_class(
            x509.SubjectAlternativeName
        ).value
    except x509.ExtensionNotFound as exc:
        raise CertificateValidationError(
            "Missing SubjectAlternativeName extension"
        ) from exc

    dns_names = san.get_values_for_type(x509.DNSName)

    if hostname not in dns_names:
        raise CertificateValidationError(
            f"Hostname mismatch: {hostname} not in {dns_names}"
        )

    return True


def validate_chain(
    leaf_certificate: x509.Certificate,
    intermediate_certificates: list[x509.Certificate],
    root_certificate: x509.Certificate,
    hostname: str | None = None,
) -> bool:
    """
    Validate a certificate chain.

    Chain order:
    leaf -> intermediate(s) -> root
    """
    chain = [leaf_certificate] + intermediate_certificates + [root_certificate]

    for certificate in chain:
        verify_certificate_time(certificate)

    verify_basic_constraints(leaf_certificate, expected_ca=False)

    for ca_certificate in intermediate_certificates:
        verify_basic_constraints(ca_certificate, expected_ca=True)

    verify_basic_constraints(root_certificate, expected_ca=True)

    for index in range(len(chain) - 1):
        child = chain[index]
        issuer = chain[index + 1]
        verify_signature(child, issuer)

    if root_certificate.subject != root_certificate.issuer:
        raise CertificateValidationError("Root certificate is not self-issued")

    verify_signature(root_certificate, root_certificate)

    if hostname:
        verify_hostname(leaf_certificate, hostname)

    return True
