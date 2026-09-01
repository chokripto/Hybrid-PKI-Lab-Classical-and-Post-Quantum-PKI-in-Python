from __future__ import annotations

import base64
import binascii
import os
import tempfile
from pathlib import Path


def bytes_to_base64(data: bytes) -> str:
    """Encode bytes to a Base64 string."""
    return base64.b64encode(data).decode("ascii")


def base64_to_bytes(data: str) -> bytes:
    """Strictly decode a Base64 string to bytes."""
    try:
        return base64.b64decode(data.encode("ascii"), validate=True)
    except (UnicodeEncodeError, binascii.Error) as exc:
        raise ValueError("Invalid Base64 data") from exc


def _atomic_write(path: str | Path, data: bytes) -> None:
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


def save_binary_file(path: str | Path, data: bytes) -> None:
    """Atomically save binary key material with owner-only permissions."""
    _atomic_write(path, data)


def load_binary_file(path: str | Path) -> bytes:
    return Path(path).read_bytes()


def save_base64_file(path: str | Path, data: bytes) -> None:
    """Atomically save Base64 key material with owner-only permissions."""
    _atomic_write(path, bytes_to_base64(data).encode("ascii"))


def load_base64_file(path: str | Path) -> bytes:
    return base64_to_bytes(Path(path).read_text(encoding="ascii").strip())


def serialize_pqc_key_to_json_value(data: bytes) -> str:
    return bytes_to_base64(data)


def deserialize_pqc_key_from_json_value(data: str) -> bytes:
    return base64_to_bytes(data)
