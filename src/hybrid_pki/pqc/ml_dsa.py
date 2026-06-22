from __future__ import annotations

from dataclasses import dataclass

from hybrid_pki.pqc.oqs_provider import require_oqs

DEFAULT_ML_DSA_ALGORITHM = "ML-DSA-65"


@dataclass(frozen=True)
class MLDSAKeyPair:
    """
    ML-DSA key pair.

    public_key:
        Public key used for signature verification.

    secret_key:
        Secret key used for signing.
    """

    public_key: bytes
    secret_key: bytes
    algorithm: str


@dataclass(frozen=True)
class MLDSASignature:
    """
    ML-DSA signature result.
    """

    signature: bytes
    algorithm: str


class MLDSA:
    """
    Wrapper around liboqs-python Signature for ML-DSA.

    ML-DSA is a post-quantum digital signature algorithm.

    It is used for:
    - signing messages
    - verifying signatures
    - signing hybrid certificates

    It is not a key encapsulation mechanism.
    """

    def __init__(self, algorithm: str = DEFAULT_ML_DSA_ALGORITHM):
        self.algorithm = algorithm

    def generate_keypair(self) -> MLDSAKeyPair:
        """
        Generate an ML-DSA key pair.
        """
        oqs = require_oqs()

        with oqs.Signature(self.algorithm) as signer:
            public_key = signer.generate_keypair()
            secret_key = signer.export_secret_key()

        return MLDSAKeyPair(
            public_key=public_key,
            secret_key=secret_key,
            algorithm=self.algorithm,
        )

    def sign(self, secret_key: bytes, message: bytes) -> MLDSASignature:
        """
        Sign a message using an ML-DSA secret key.
        """
        oqs = require_oqs()

        with oqs.Signature(self.algorithm, secret_key) as signer:
            signature = signer.sign(message)

        return MLDSASignature(
            signature=signature,
            algorithm=self.algorithm,
        )

    def verify(
        self,
        public_key: bytes,
        message: bytes,
        signature: bytes,
    ) -> bool:
        """
        Verify an ML-DSA signature.
        """
        oqs = require_oqs()

        with oqs.Signature(self.algorithm) as verifier:
            return bool(verifier.verify(message, signature, public_key))


def generate_ml_dsa_keypair(
    algorithm: str = DEFAULT_ML_DSA_ALGORITHM,
) -> MLDSAKeyPair:
    """
    Convenience function to generate an ML-DSA key pair.
    """
    return MLDSA(algorithm).generate_keypair()


def ml_dsa_sign(
    secret_key: bytes,
    message: bytes,
    algorithm: str = DEFAULT_ML_DSA_ALGORITHM,
) -> MLDSASignature:
    """
    Convenience function to sign a message with ML-DSA.
    """
    return MLDSA(algorithm).sign(secret_key, message)


def ml_dsa_verify(
    public_key: bytes,
    message: bytes,
    signature: bytes,
    algorithm: str = DEFAULT_ML_DSA_ALGORITHM,
) -> bool:
    """
    Convenience function to verify an ML-DSA signature.
    """
    return MLDSA(algorithm).verify(public_key, message, signature)
