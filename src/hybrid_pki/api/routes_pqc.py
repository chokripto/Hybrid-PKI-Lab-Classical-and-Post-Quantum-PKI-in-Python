from fastapi import APIRouter

from hybrid_pki.pqc.oqs_provider import get_oqs_status

router = APIRouter(
    prefix="/pqc",
    tags=["Post-Quantum Cryptography"],
)


@router.get("/status")
def pqc_status():
    """
    Show post-quantum cryptography provider status.
    """
    status = get_oqs_status()

    return {
        "available": status.available,
        "message": status.message,
        "supported_modules": [
            "ML-KEM",
            "ML-DSA",
        ],
    }
