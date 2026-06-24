import base64
import binascii

import pytest

from hybrid_pki.pqc.pqc_serialization import (
    base64_to_bytes,
    bytes_to_base64,
    deserialize_pqc_key_from_json_value,
    load_base64_file,
    load_binary_file,
    save_base64_file,
    save_binary_file,
    serialize_pqc_key_to_json_value,
)


def test_bytes_to_base64_returns_string():
    data = b"pqc-key-material"

    encoded = bytes_to_base64(data)

    assert isinstance(encoded, str)
    assert encoded == base64.b64encode(data).decode("utf-8")


def test_base64_to_bytes_returns_original_bytes():
    data = b"pqc-key-material"
    encoded = base64.b64encode(data).decode("utf-8")

    decoded = base64_to_bytes(encoded)

    assert decoded == data


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"short",
        b"binary\x00data",
        bytes(range(256)),
    ],
)
def test_base64_roundtrip_for_multiple_inputs(data):
    encoded = bytes_to_base64(data)
    decoded = base64_to_bytes(encoded)

    assert decoded == data


def test_base64_to_bytes_raises_for_invalid_base64():
    invalid_base64 = "not-valid-base64@@@"

    with pytest.raises(binascii.Error):
        base64_to_bytes(invalid_base64)


def test_save_and_load_binary_file(tmp_path):
    file_path = tmp_path / "keys" / "pqc_key.bin"
    data = b"raw-pqc-key-material"

    save_binary_file(file_path, data)

    assert file_path.exists()
    assert file_path.read_bytes() == data

    loaded_data = load_binary_file(file_path)

    assert loaded_data == data


def test_save_and_load_binary_file_with_string_path(tmp_path):
    file_path = tmp_path / "keys" / "pqc_key_string_path.bin"
    data = b"raw-pqc-key-material"

    save_binary_file(str(file_path), data)

    loaded_data = load_binary_file(str(file_path))

    assert loaded_data == data


def test_save_and_load_base64_file(tmp_path):
    file_path = tmp_path / "keys" / "pqc_key.b64"
    data = b"base64-pqc-key-material"

    save_base64_file(file_path, data)

    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == bytes_to_base64(data)

    loaded_data = load_base64_file(file_path)

    assert loaded_data == data


def test_save_and_load_base64_file_with_string_path(tmp_path):
    file_path = tmp_path / "keys" / "pqc_key_string_path.b64"
    data = b"base64-pqc-key-material"

    save_base64_file(str(file_path), data)

    loaded_data = load_base64_file(str(file_path))

    assert loaded_data == data


def test_serialize_pqc_key_to_json_value_returns_base64_string():
    data = b"json-pqc-key"

    serialized = serialize_pqc_key_to_json_value(data)

    assert isinstance(serialized, str)
    assert serialized == bytes_to_base64(data)


def test_deserialize_pqc_key_from_json_value_returns_original_bytes():
    data = b"json-pqc-key"
    serialized = serialize_pqc_key_to_json_value(data)

    deserialized = deserialize_pqc_key_from_json_value(serialized)

    assert deserialized == data


def test_json_value_serialization_roundtrip():
    data = b"json-pqc-key-material\x00with-binary"

    serialized = serialize_pqc_key_to_json_value(data)
    deserialized = deserialize_pqc_key_from_json_value(serialized)

    assert deserialized == data


def test_load_binary_file_raises_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.bin"

    with pytest.raises(FileNotFoundError):
        load_binary_file(missing_file)


def test_load_base64_file_raises_for_missing_file(tmp_path):
    missing_file = tmp_path / "missing.b64"

    with pytest.raises(FileNotFoundError):
        load_base64_file(missing_file)
