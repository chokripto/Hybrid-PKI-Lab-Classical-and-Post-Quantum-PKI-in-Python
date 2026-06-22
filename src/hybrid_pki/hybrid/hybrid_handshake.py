from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from hybrid_pki.pqc.ml_kem import MLKEM


@dataclass(frozen=True)
class ServerHybridHandshakeKeys:
    """
    Server-side hybrid handshake key material.
    """

    classical_private_key: x25519.X25519PrivateKey
    classical_public_key_bytes: bytes
    pqc_public_key: bytes
    pqc_secret_key: bytes
    pqc_algorithm: str


@dataclass(frozen=True)
class ClientHybridHandshakeResult:
    """
    Client-side hybrid handshake result.
    """

    client_classical_public_key_bytes: bytes
    pqc_ciphertext: bytes
    hybrid_secret: bytes
    pqc_algorithm: str


def derive_hybrid_secret(
    classical_secret: bytes,
    pqc_secret: bytes,
    context: bytes = b"Hybrid-PKI-Lab-Hybrid-Handshake-v1",
    length: int = 32,
) -> bytes:
    """
    Derive a hybrid shared secret using HKDF.

    secret_hybrid = HKDF(secret_classical || secret_pqc)
    """
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=context,
    )

    return hkdf.derive(classical_secret + pqc_secret)


def generate_server_hybrid_handshake_keys(
    pqc_algorithm: str = "ML-KEM-768",
) -> ServerHybridHandshakeKeys:
    """
    Generate server-side keys for a hybrid handshake.
    """
    classical_private_key = x25519.X25519PrivateKey.generate()
    classical_public_key = classical_private_key.public_key()

    classical_public_key_bytes = classical_public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    kem = MLKEM(pqc_algorithm)
    pqc_keypair = kem.generate_keypair()

    return ServerHybridHandshakeKeys(
        classical_private_key=classical_private_key,
        classical_public_key_bytes=classical_public_key_bytes,
        pqc_public_key=pqc_keypair.public_key,
        pqc_secret_key=pqc_keypair.secret_key,
        pqc_algorithm=pqc_algorithm,
    )


def client_hybrid_encapsulate(
    server_classical_public_key_bytes: bytes,
    server_pqc_public_key: bytes,
    pqc_algorithm: str = "ML-KEM-768",
) -> ClientHybridHandshakeResult:
    """
    Client side of the hybrid handshake.
    """
    server_classical_public_key = x25519.X25519PublicKey.from_public_bytes(
        server_classical_public_key_bytes
    )

    client_private_key = x25519.X25519PrivateKey.generate()
    client_public_key = client_private_key.public_key()

    client_public_key_bytes = client_public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    classical_secret = client_private_key.exchange(server_classical_public_key)

    kem = MLKEM(pqc_algorithm)
    encapsulation = kem.encapsulate(server_pqc_public_key)

    hybrid_secret = derive_hybrid_secret(
        classical_secret=classical_secret,
        pqc_secret=encapsulation.shared_secret,
    )

    return ClientHybridHandshakeResult(
        client_classical_public_key_bytes=client_public_key_bytes,
        pqc_ciphertext=encapsulation.ciphertext,
        hybrid_secret=hybrid_secret,
        pqc_algorithm=pqc_algorithm,
    )


def server_hybrid_decapsulate(
    server_classical_private_key: x25519.X25519PrivateKey,
    client_classical_public_key_bytes: bytes,
    server_pqc_secret_key: bytes,
    pqc_ciphertext: bytes,
    pqc_algorithm: str = "ML-KEM-768",
) -> bytes:
    """
    Server side of the hybrid handshake.
    """
    client_classical_public_key = x25519.X25519PublicKey.from_public_bytes(
        client_classical_public_key_bytes
    )

    classical_secret = server_classical_private_key.exchange(
        client_classical_public_key
    )

    kem = MLKEM(pqc_algorithm)
    pqc_secret = kem.decapsulate(
        secret_key=server_pqc_secret_key,
        ciphertext=pqc_ciphertext,
    )

    return derive_hybrid_secret(
        classical_secret=classical_secret,
        pqc_secret=pqc_secret,
    )
