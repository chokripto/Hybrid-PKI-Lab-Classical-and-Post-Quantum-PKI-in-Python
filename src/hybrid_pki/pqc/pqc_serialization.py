from __future__ import annotations

import base64
from pathlib import Path


def bytes_to_base64(data: bytes) -> str:
    """
    Encode bytes to a Base64 string.
    """
    return base64.b64encode(data).decode("utf-8")


def base64_to_bytes(data: str) -> bytes:
    """
    Decode a Base64 string to bytes.
    """
    return base64.b64decode(data.encode("utf-8"))


def save_binary_file(path: str | Path, data: bytes) -> None:
    """
    Save raw binary data to disk.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(data)


def load_binary_file(path: str | Path) -> bytes:
    """
    Load raw binary data from disk.
    """
    return Path(path).read_bytes()


def save_base64_file(path: str | Path, data: bytes) -> None:
    """
    Save binary data as Base64 text.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        bytes_to_base64(data),
        encoding="utf-8",
    )


def load_base64_file(path: str | Path) -> bytes:
    """
    Load Base64 text and decode it to bytes.
    """
    data = Path(path).read_text(encoding="utf-8")
    return base64_to_bytes(data)


def serialize_pqc_key_to_json_value(data: bytes) -> str:
    """
    Serialize a PQC key to a JSON-compatible Base64 string.
    """
    return bytes_to_base64(data)


def deserialize_pqc_key_from_json_value(data: str) -> bytes:
    """
    Deserialize a PQC key from a JSON-compatible Base64 string.
    """
    return base64_to_bytes(data)
