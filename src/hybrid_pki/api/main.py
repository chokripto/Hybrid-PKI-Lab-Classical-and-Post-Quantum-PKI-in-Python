from fastapi import FastAPI

from hybrid_pki.api.routes_classical import router as classical_router
from hybrid_pki.api.routes_hybrid import router as hybrid_router
from hybrid_pki.api.routes_pqc import router as pqc_router

app = FastAPI(
    title="Hybrid PKI Lab API",
    description="Classical and Post-Quantum Hybrid PKI API",
    version="1.0.0",
)

app.include_router(classical_router)
app.include_router(pqc_router)
app.include_router(hybrid_router)


@app.get("/")
def root():
    return {
        "project": "Hybrid PKI Lab",
        "status": "running",
        "message": "API is working successfully",
        "available_modules": [
            "Classical PKI",
            "Post-Quantum Cryptography",
            "Hybrid PKI",
        ],
        "documentation": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }
