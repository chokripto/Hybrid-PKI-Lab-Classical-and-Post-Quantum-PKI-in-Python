from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa

from hybrid_pki.hybrid.hybrid_certificate import HybridCertificate
from hybrid_pki.pqc.ml_dsa import MLDSA
from hybrid_pki.pqc.pqc_serialization import base64_to_bytes, bytes_to_base64


class HybridSignatureError(Exception):
    """
    Raised when hybrid signing or verification fails.
    """


def classical_sign(private_key, message: bytes) -> bytes:
    """
    Sign a message with a classical private key.
    """
    if isinstance(private_key, rsa.RSAPrivateKey):
        from cryptography.hazmat.primitives import hashes

        return private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

    if isinstance(private_key, ec.EllipticCurvePrivateKey):
        from cryptography.hazmat.primitives import hashes

        return private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256()),
        )

    if isinstance(private_key, ed25519.Ed25519PrivateKey):
        return private_key.sign(message)

    raise HybridSignatureError("Unsupported classical private key type")


def classical_verify(public_key, message: bytes, signature: bytes) -> bool:
    """
    Verify a classical signature.
    """
    try:
        if isinstance(public_key, rsa.RSAPublicKey):
            from cryptography.hazmat.primitives import hashes

            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True

        if isinstance(public_key, ec.EllipticCurvePublicKey):
            from cryptography.hazmat.primitives import hashes

            public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256()),
            )
            return True

        if isinstance(public_key, ed25519.Ed25519PublicKey):
            public_key.verify(
                signature,
                message,
            )
            return True

        return False

    except Exception:
        return False


def sign_hybrid_certificate(
    certificate: HybridCertificate,
    classical_ca_private_key,
    pqc_ca_secret_key: bytes,
    pqc_algorithm: str = "ML-DSA-65",
) -> HybridCertificate:
    """
    Sign a hybrid certificate with classical and PQC CA keys.
    """
    payload = certificate.to_unsigned_payload()

    classical_signature = classical_sign(
        classical_ca_private_key,
        payload,
    )

    pqc_signer = MLDSA(pqc_algorithm)
    pqc_signature = pqc_signer.sign(
        pqc_ca_secret_key,
        payload,
    )

    certificate.classical_signature_b64 = bytes_to_base64(classical_signature)
    certificate.pqc_signature_b64 = bytes_to_base64(pqc_signature.signature)

    return certificate


def verify_hybrid_certificate_signatures(
    certificate: HybridCertificate,
    classical_ca_public_key,
    pqc_ca_public_key: bytes,
) -> tuple[bool, bool]:
    """
    Verify both classical and PQC signatures of a hybrid certificate.

    Returns:
        tuple[classical_valid, pqc_valid]
    """
    if certificate.classical_signature_b64 is None:
        classical_valid = False
    else:
        classical_valid = classical_verify(
            classical_ca_public_key,
            certificate.to_unsigned_payload(),
            base64_to_bytes(certificate.classical_signature_b64),
        )

    if certificate.pqc_signature_b64 is None:
        pqc_valid = False
    else:
        pqc_signer = MLDSA(certificate.pqc_signature_algorithm)
        pqc_valid = pqc_signer.verify(
            pqc_ca_public_key,
            certificate.to_unsigned_payload(),
            base64_to_bytes(certificate.pqc_signature_b64),
        )

    return classical_valid, pqc_valid
