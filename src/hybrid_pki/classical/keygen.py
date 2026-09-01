from __future__ import annotations

import os
import tempfile
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa


def generate_rsa_private_key(key_size: int = 3072):
    """Generate an RSA private key."""
    if key_size < 2048:
        raise ValueError("RSA key size must be at least 2048 bits")
    return rsa.generate_private_key(public_exponent=65537, key_size=key_size)


def generate_ecdsa_private_key():
    """Generate an ECDSA private key using curve P-256."""
    return ec.generate_private_key(ec.SECP256R1())


def generate_ed25519_private_key():
    """Generate an Ed25519 private key."""
    return ed25519.Ed25519PrivateKey.generate()


def serialize_private_key(private_key, password: bytes | None = None) -> bytes:
    """Serialize a private key to encrypted or unencrypted PKCS#8 PEM."""
    encryption_algorithm = (
        serialization.BestAvailableEncryption(password)
        if password
        else serialization.NoEncryption()
    )
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm,
    )


def serialize_public_key(public_key) -> bytes:
    """Serialize a public key to SubjectPublicKeyInfo PEM."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def save_pem_file(path: str | Path, data: bytes) -> None:
    """Atomically save PEM data with owner-only permissions."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{file_path.name}.",
        dir=file_path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, file_path)
        try:
            file_path.chmod(0o600)
        except OSError:
            pass
    except Exception:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary_path.unlink(missing_ok=True)
        raise


def load_private_key(path: str | Path, password: bytes | None = None):
    """Load a private key from a PEM file."""
    return serialization.load_pem_private_key(
        Path(path).read_bytes(), password=password
    )


def load_public_key(path: str | Path):
    """Load a public key from a PEM file."""
    return serialization.load_pem_public_key(Path(path).read_bytes())
