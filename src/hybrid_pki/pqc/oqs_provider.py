from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any


class OQSUnavailableError(RuntimeError):
    """
    Raised when liboqs-python is required but not correctly available.
    """


@dataclass(frozen=True)
class OQSStatus:
    """
    Represents liboqs-python availability status.
    """

    available: bool
    message: str


@lru_cache(maxsize=1)
def import_oqs() -> Any:
    """
    Import oqs dynamically and cache the result.

    This prevents repeated slow import attempts when liboqs-python is broken,
    missing, or disabled.
    """
    if os.getenv("HYBRID_PKI_DISABLE_OQS", "").lower() in {"1", "true", "yes"}:
        raise OQSUnavailableError("OQS support is disabled by HYBRID_PKI_DISABLE_OQS.")

    try:
        import oqs  # type: ignore[import-not-found]

        return oqs

    except (ImportError, RuntimeError, OSError, SystemExit) as exc:
        raise OQSUnavailableError(
            "liboqs-python is not installed correctly, or liboqs shared "
            "libraries are not available. Use Docker PQC mode for real "
            "post-quantum cryptography features."
        ) from exc


@lru_cache(maxsize=1)
def is_oqs_available() -> bool:
    """
    Return True if liboqs-python can be imported and loaded.
    """
    try:
        import_oqs()
        return True
    except OQSUnavailableError:
        return False


@lru_cache(maxsize=1)
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


def clear_oqs_cache() -> None:
    """
    Clear cached OQS availability checks.

    Useful for tests.
    """
    import_oqs.cache_clear()
    is_oqs_available.cache_clear()
    get_oqs_status.cache_clear()
