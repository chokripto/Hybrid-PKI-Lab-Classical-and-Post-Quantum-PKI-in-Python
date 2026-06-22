from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class OQSUnavailableError(RuntimeError):
    """
    Raised when liboqs-python is required but not installed.
    """


@dataclass(frozen=True)
class OQSStatus:
    """
    Represents liboqs-python availability status.
    """

    available: bool
    message: str


def import_oqs() -> Any:
    """
    Import oqs dynamically.

    This avoids breaking the whole project when liboqs-python is not installed.
    """
    try:
        import oqs  # type: ignore[import-not-found]

        return oqs

    except ImportError as exc:
        raise OQSUnavailableError(
            "liboqs-python is not installed or liboqs is not available. "
            "Install liboqs and liboqs-python to use PQC features."
        ) from exc


def is_oqs_available() -> bool:
    """
    Return True if liboqs-python can be imported.
    """
    try:
        import_oqs()
        return True
    except OQSUnavailableError:
        return False


def get_oqs_status() -> OQSStatus:
    """
    Return detailed status about liboqs-python availability.
    """
    try:
        import_oqs()
        return OQSStatus(
            available=True,
            message="liboqs-python is available.",
        )
    except OQSUnavailableError as exc:
        return OQSStatus(
            available=False,
            message=str(exc),
        )


def require_oqs() -> Any:
    """
    Return oqs module or raise a clear error.
    """
    return import_oqs()
