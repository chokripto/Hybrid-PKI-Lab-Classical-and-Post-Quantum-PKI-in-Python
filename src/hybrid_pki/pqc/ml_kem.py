from __future__ import annotations

from dataclasses import dataclass

from hybrid_pki.pqc.oqs_provider import require_oqs

DEFAULT_ML_KEM_ALGORITHM = "ML-KEM-768"


@dataclass(frozen=True)
class MLKEMKeyPair:
    """
    ML-KEM key pair.

    public_key:
        Public key used for encapsulation.

    secret_key:
        Secret key used for decapsulation.
    """

    public_key: bytes
    secret_key: bytes
    algorithm: str


@dataclass(frozen=True)
class MLKEMEncapsulationResult:
    """
    ML-KEM encapsulation result.

    ciphertext:
        Encapsulated secret sent to the holder of the secret key.

    shared_secret:
        Shared secret derived during encapsulation.
    """

    ciphertext: bytes
    shared_secret: bytes
    algorithm: str


class MLKEM:
    """
    Wrapper around liboqs-python KeyEncapsulation for ML-KEM.

    ML-KEM is a Key Encapsulation Mechanism.
    It is used to establish a shared secret.

    It is not a signature algorithm.
    """

    def __init__(self, algorithm: str = DEFAULT_ML_KEM_ALGORITHM):
        self.algorithm = algorithm

    def generate_keypair(self) -> MLKEMKeyPair:
        """
        Generate an ML-KEM key pair.
        """
        oqs = require_oqs()

        with oqs.KeyEncapsulation(self.algorithm) as kem:
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()

        return MLKEMKeyPair(
            public_key=public_key,
            secret_key=secret_key,
            algorithm=self.algorithm,
        )

    def encapsulate(self, public_key: bytes) -> MLKEMEncapsulationResult:
        """
        Encapsulate a shared secret using the recipient public key.
        """
        oqs = require_oqs()

        with oqs.KeyEncapsulation(self.algorithm) as kem:
            ciphertext, shared_secret = kem.encap_secret(public_key)

        return MLKEMEncapsulationResult(
            ciphertext=ciphertext,
            shared_secret=shared_secret,
            algorithm=self.algorithm,
        )

    def decapsulate(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        """
        Decapsulate a shared secret using the recipient secret key.
        """
        oqs = require_oqs()

        with oqs.KeyEncapsulation(self.algorithm, secret_key) as kem:
            shared_secret = kem.decap_secret(ciphertext)

        return shared_secret


def generate_ml_kem_keypair(
    algorithm: str = DEFAULT_ML_KEM_ALGORITHM,
) -> MLKEMKeyPair:
    """
    Convenience function to generate an ML-KEM key pair.
    """
    return MLKEM(algorithm).generate_keypair()


def ml_kem_encapsulate(
    public_key: bytes,
    algorithm: str = DEFAULT_ML_KEM_ALGORITHM,
) -> MLKEMEncapsulationResult:
    """
    Convenience function to encapsulate a shared secret.
    """
    return MLKEM(algorithm).encapsulate(public_key)


def ml_kem_decapsulate(
    secret_key: bytes,
    ciphertext: bytes,
    algorithm: str = DEFAULT_ML_KEM_ALGORITHM,
) -> bytes:
    """
    Convenience function to decapsulate a shared secret.
    """
    return MLKEM(algorithm).decapsulate(secret_key, ciphertext)
