from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from hybrid_pki.pqc.ml_kem import MLKEM

PROTOCOL_LABEL = b"Hybrid-PKI-Lab-Hybrid-Handshake-v2"


@dataclass(frozen=True)
class ServerHybridHandshakeKeys:
    """Server-side hybrid handshake key material."""

    classical_private_key: x25519.X25519PrivateKey
    classical_public_key_bytes: bytes
    pqc_public_key: bytes
    pqc_secret_key: bytes
    pqc_algorithm: str


@dataclass(frozen=True)
class ClientHybridHandshakeResult:
    """Client-side result for an unauthenticated educational key exchange."""

    client_classical_public_key_bytes: bytes
    pqc_ciphertext: bytes
    hybrid_secret: bytes
    pqc_algorithm: str
    transcript_hash: bytes


def build_transcript_hash(
    server_classical_public_key_bytes: bytes,
    client_classical_public_key_bytes: bytes,
    server_pqc_public_key: bytes,
    pqc_ciphertext: bytes,
    pqc_algorithm: str,
) -> bytes:
    """Bind the KDF to the public handshake transcript."""
    digest = hashes.Hash(hashes.SHA256())
    for value in (
        PROTOCOL_LABEL,
        pqc_algorithm.encode("ascii"),
        server_classical_public_key_bytes,
        client_classical_public_key_bytes,
        server_pqc_public_key,
        pqc_ciphertext,
    ):
        digest.update(len(value).to_bytes(4, "big"))
        digest.update(value)
    return digest.finalize()


def derive_hybrid_secret(
    classical_secret: bytes,
    pqc_secret: bytes,
    context: bytes = PROTOCOL_LABEL,
    transcript_hash: bytes | None = None,
    length: int = 32,
) -> bytes:
    """Derive a domain-separated hybrid secret using HKDF-SHA256.

    This combines independent classical and PQC contributions. Authentication
    must be supplied by a higher-level signed transcript or authenticated
    transport; this laboratory primitive does not provide peer authentication.
    """
    if not classical_secret or not pqc_secret:
        raise ValueError("Both classical and PQC secrets are required")
    if not 16 <= length <= 64:
        raise ValueError("Derived secret length must be between 16 and 64 bytes")

    salt = transcript_hash or bytes(hashes.SHA256().digest_size)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        info=context,
    )
    return hkdf.derive(classical_secret + pqc_secret)


def generate_server_hybrid_handshake_keys(
    pqc_algorithm: str = "ML-KEM-768",
) -> ServerHybridHandshakeKeys:
    classical_private_key = x25519.X25519PrivateKey.generate()
    classical_public_key_bytes = classical_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    pqc_keypair = MLKEM(pqc_algorithm).generate_keypair()
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
    server_public_key = x25519.X25519PublicKey.from_public_bytes(
        server_classical_public_key_bytes
    )
    client_private_key = x25519.X25519PrivateKey.generate()
    client_public_key_bytes = client_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    classical_secret = client_private_key.exchange(server_public_key)
    encapsulation = MLKEM(pqc_algorithm).encapsulate(server_pqc_public_key)
    transcript_hash = build_transcript_hash(
        server_classical_public_key_bytes,
        client_public_key_bytes,
        server_pqc_public_key,
        encapsulation.ciphertext,
        pqc_algorithm,
    )
    hybrid_secret = derive_hybrid_secret(
        classical_secret,
        encapsulation.shared_secret,
        transcript_hash=transcript_hash,
    )
    return ClientHybridHandshakeResult(
        client_classical_public_key_bytes=client_public_key_bytes,
        pqc_ciphertext=encapsulation.ciphertext,
        hybrid_secret=hybrid_secret,
        pqc_algorithm=pqc_algorithm,
        transcript_hash=transcript_hash,
    )


def server_hybrid_decapsulate(
    server_classical_private_key: x25519.X25519PrivateKey,
    client_classical_public_key_bytes: bytes,
    server_pqc_secret_key: bytes,
    pqc_ciphertext: bytes,
    pqc_algorithm: str = "ML-KEM-768",
    server_pqc_public_key: bytes | None = None,
) -> bytes:
    """Complete the server side of the educational hybrid exchange.

    The server PQC public key is required in protocol v2 so both peers bind the
    same transcript. It is optional only to produce a clear migration error.
    """
    if server_pqc_public_key is None:
        raise ValueError("server_pqc_public_key is required for transcript binding")

    server_public_key_bytes = server_classical_private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    client_public_key = x25519.X25519PublicKey.from_public_bytes(
        client_classical_public_key_bytes
    )
    classical_secret = server_classical_private_key.exchange(client_public_key)
    pqc_secret = MLKEM(pqc_algorithm).decapsulate(
        secret_key=server_pqc_secret_key,
        ciphertext=pqc_ciphertext,
    )
    transcript_hash = build_transcript_hash(
        server_public_key_bytes,
        client_classical_public_key_bytes,
        server_pqc_public_key,
        pqc_ciphertext,
        pqc_algorithm,
    )
    return derive_hybrid_secret(
        classical_secret,
        pqc_secret,
        transcript_hash=transcript_hash,
    )
