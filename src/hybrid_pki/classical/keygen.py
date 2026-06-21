from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa


def generate_rsa_private_key(key_size: int = 3072):
    """
    Generate an RSA private key.

    Recommended sizes:
    - 3072 bits for modern security
    - 4096 bits for stronger security
    """
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )


def generate_ecdsa_private_key():
    """
    Generate an ECDSA private key using curve P-256.
    """
    return ec.generate_private_key(ec.SECP256R1())


def generate_ed25519_private_key():
    """
    Generate an Ed25519 private key.
    """
    return ed25519.Ed25519PrivateKey.generate()


def serialize_private_key(private_key, password: bytes | None = None) -> bytes:
    """
    Serialize a private key to PEM format.

    If password is provided, the private key is encrypted.
    """
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
    """
    Serialize a public key to PEM format.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def save_pem_file(path: str | Path, data: bytes) -> None:
    """
    Save PEM data to a file.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(data)


def load_private_key(path: str | Path, password: bytes | None = None):
    """
    Load a private key from a PEM file.
    """
    data = Path(path).read_bytes()

    return serialization.load_pem_private_key(
        data,
        password=password,
    )


def load_public_key(path: str | Path):
    """
    Load a public key from a PEM file.
    """
    data = Path(path).read_bytes()

    return serialization.load_pem_public_key(data)
