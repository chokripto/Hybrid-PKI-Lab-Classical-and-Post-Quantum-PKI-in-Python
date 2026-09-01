from __future__ import annotations

import hmac
import os

from fastapi import Header, HTTPException, status


def require_mutation_access(
    x_hybrid_pki_api_key: str | None = Header(default=None),
) -> None:
    """Protect state-changing laboratory endpoints.

    Mutations are disabled by default. To enable them, set
    HYBRID_PKI_ENABLE_MUTATIONS=1. When HYBRID_PKI_API_KEY is configured,
    clients must also send it in the X-Hybrid-PKI-API-Key header.
    """
    enabled = os.getenv("HYBRID_PKI_ENABLE_MUTATIONS", "0").strip() == "1"
    if not enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "State-changing lab endpoints are disabled. "
                "Set HYBRID_PKI_ENABLE_MUTATIONS=1 only in a controlled environment."
            ),
        )

    expected_key = os.getenv("HYBRID_PKI_API_KEY")
    if expected_key and (
        x_hybrid_pki_api_key is None
        or not hmac.compare_digest(x_hybrid_pki_api_key, expected_key)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid laboratory API key.",
        )
