import pytest

from hybrid_pki.pqc.oqs_provider import is_oqs_available
from hybrid_pki.pqc.pqc_serialization import (
    base64_to_bytes,
    bytes_to_base64,
)


def test_pqc_serialization_roundtrip():
    data = b"post-quantum-test-data"
    encoded = bytes_to_base64(data)
    decoded = base64_to_bytes(encoded)

    assert decoded == data


@pytest.mark.skipif(
    not is_oqs_available(),
    reason="liboqs-python is not installed",
)
def test_ml_kem_roundtrip():
    from hybrid_pki.pqc.ml_kem import MLKEM

    kem = MLKEM("ML-KEM-768")

    keypair = kem.generate_keypair()
    encapsulation = kem.encapsulate(keypair.public_key)
    decapsulated_secret = kem.decapsulate(
        keypair.secret_key,
        encapsulation.ciphertext,
    )

    assert decapsulated_secret == encapsulation.shared_secret


@pytest.mark.skipif(
    not is_oqs_available(),
    reason="liboqs-python is not installed",
)
def test_ml_dsa_sign_verify():
    from hybrid_pki.pqc.ml_dsa import MLDSA

    signer = MLDSA("ML-DSA-65")
    keypair = signer.generate_keypair()

    message = b"Hybrid PKI Lab PQC signature test"
    signature = signer.sign(keypair.secret_key, message)

    assert signer.verify(
        keypair.public_key,
        message,
        signature.signature,
    )
