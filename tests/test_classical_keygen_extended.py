import pytest
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, rsa

from hybrid_pki.classical.keygen import (
    generate_ecdsa_private_key,
    generate_ed25519_private_key,
    generate_rsa_private_key,
    load_private_key,
    load_public_key,
    save_pem_file,
    serialize_private_key,
    serialize_public_key,
)


def test_generate_rsa_private_key_default_size():
    private_key = generate_rsa_private_key()

    assert isinstance(private_key, rsa.RSAPrivateKey)
    assert private_key.key_size == 3072
    assert private_key.public_key().key_size == 3072


def test_generate_rsa_private_key_custom_size():
    private_key = generate_rsa_private_key(key_size=2048)

    assert isinstance(private_key, rsa.RSAPrivateKey)
    assert private_key.key_size == 2048


def test_generate_ecdsa_private_key_uses_p256():
    private_key = generate_ecdsa_private_key()

    assert isinstance(private_key, ec.EllipticCurvePrivateKey)
    assert isinstance(private_key.curve, ec.SECP256R1)


def test_generate_ed25519_private_key():
    private_key = generate_ed25519_private_key()

    assert isinstance(private_key, ed25519.Ed25519PrivateKey)


@pytest.mark.parametrize(
    "private_key",
    [
        generate_rsa_private_key(key_size=2048),
        generate_ecdsa_private_key(),
        generate_ed25519_private_key(),
    ],
)
def test_serialize_private_key_without_password(private_key):
    pem_data = serialize_private_key(private_key)

    assert isinstance(pem_data, bytes)
    assert pem_data.startswith(b"-----BEGIN PRIVATE KEY-----")
    assert pem_data.endswith(b"-----END PRIVATE KEY-----\n")


@pytest.mark.parametrize(
    "private_key",
    [
        generate_rsa_private_key(key_size=2048),
        generate_ecdsa_private_key(),
        generate_ed25519_private_key(),
    ],
)
def test_serialize_private_key_with_password(private_key):
    pem_data = serialize_private_key(private_key, password=b"strong-password")

    assert isinstance(pem_data, bytes)
    assert pem_data.startswith(b"-----BEGIN ENCRYPTED PRIVATE KEY-----")
    assert pem_data.endswith(b"-----END ENCRYPTED PRIVATE KEY-----\n")


@pytest.mark.parametrize(
    "private_key",
    [
        generate_rsa_private_key(key_size=2048),
        generate_ecdsa_private_key(),
        generate_ed25519_private_key(),
    ],
)
def test_serialize_public_key(private_key):
    public_key = private_key.public_key()

    pem_data = serialize_public_key(public_key)

    assert isinstance(pem_data, bytes)
    assert pem_data.startswith(b"-----BEGIN PUBLIC KEY-----")
    assert pem_data.endswith(b"-----END PUBLIC KEY-----\n")


def test_save_pem_file_creates_parent_directories(tmp_path):
    file_path = tmp_path / "nested" / "keys" / "test_key.pem"
    data = b"test-pem-data"

    save_pem_file(file_path, data)

    assert file_path.exists()
    assert file_path.read_bytes() == data


def test_save_pem_file_accepts_string_path(tmp_path):
    file_path = tmp_path / "key.pem"
    data = b"test-pem-data"

    save_pem_file(str(file_path), data)

    assert file_path.exists()
    assert file_path.read_bytes() == data


@pytest.mark.parametrize(
    "private_key",
    [
        generate_rsa_private_key(key_size=2048),
        generate_ecdsa_private_key(),
        generate_ed25519_private_key(),
    ],
)
def test_save_and_load_private_key_without_password(tmp_path, private_key):
    file_path = tmp_path / "private_key.pem"

    pem_data = serialize_private_key(private_key)
    save_pem_file(file_path, pem_data)

    loaded_private_key = load_private_key(file_path)

    assert type(loaded_private_key) is type(private_key)


@pytest.mark.parametrize(
    "private_key",
    [
        generate_rsa_private_key(key_size=2048),
        generate_ecdsa_private_key(),
        generate_ed25519_private_key(),
    ],
)
def test_save_and_load_private_key_with_password(tmp_path, private_key):
    file_path = tmp_path / "encrypted_private_key.pem"
    password = b"strong-password"

    pem_data = serialize_private_key(private_key, password=password)
    save_pem_file(file_path, pem_data)

    loaded_private_key = load_private_key(file_path, password=password)

    assert type(loaded_private_key) is type(private_key)


def test_load_encrypted_private_key_without_password_fails(tmp_path):
    file_path = tmp_path / "encrypted_private_key.pem"

    private_key = generate_ecdsa_private_key()
    pem_data = serialize_private_key(private_key, password=b"strong-password")
    save_pem_file(file_path, pem_data)

    with pytest.raises(TypeError):
        load_private_key(file_path)


def test_load_encrypted_private_key_with_wrong_password_fails(tmp_path):
    file_path = tmp_path / "encrypted_private_key.pem"

    private_key = generate_ecdsa_private_key()
    pem_data = serialize_private_key(private_key, password=b"strong-password")
    save_pem_file(file_path, pem_data)

    with pytest.raises(ValueError):
        load_private_key(file_path, password=b"wrong-password")


@pytest.mark.parametrize(
    "private_key",
    [
        generate_rsa_private_key(key_size=2048),
        generate_ecdsa_private_key(),
        generate_ed25519_private_key(),
    ],
)
def test_save_and_load_public_key(tmp_path, private_key):
    file_path = tmp_path / "public_key.pem"

    public_key = private_key.public_key()
    pem_data = serialize_public_key(public_key)
    save_pem_file(file_path, pem_data)

    loaded_public_key = load_public_key(file_path)

    assert type(loaded_public_key) is type(public_key)


def test_load_private_key_raises_for_invalid_pem(tmp_path):
    file_path = tmp_path / "invalid_private_key.pem"
    file_path.write_text("not a valid private key", encoding="utf-8")

    with pytest.raises(ValueError):
        load_private_key(file_path)


def test_load_public_key_raises_for_invalid_pem(tmp_path):
    file_path = tmp_path / "invalid_public_key.pem"
    file_path.write_text("not a valid public key", encoding="utf-8")

    with pytest.raises(ValueError):
        load_public_key(file_path)


def test_load_private_key_raises_for_missing_file(tmp_path):
    file_path = tmp_path / "missing_private_key.pem"

    with pytest.raises(FileNotFoundError):
        load_private_key(file_path)


def test_load_public_key_raises_for_missing_file(tmp_path):
    file_path = tmp_path / "missing_public_key.pem"

    with pytest.raises(FileNotFoundError):
        load_public_key(file_path)


def test_rsa_key_generation_rejects_invalid_key_size():
    with pytest.raises(ValueError):
        generate_rsa_private_key(key_size=512)


def test_rsa_key_generation_rejects_unsupported_public_exponent_indirectly():
    with pytest.raises(ValueError):
        rsa.generate_private_key(
            public_exponent=17,
            key_size=2048,
        )
