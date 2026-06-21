from hybrid_pki.api.main import app
from hybrid_pki.classical.keygen import generate_ecdsa_private_key


def test_smoke():
    assert app.title == "Hybrid PKI Lab API"


def test_generate_ecdsa_private_key():
    private_key = generate_ecdsa_private_key()
    assert private_key is not None
