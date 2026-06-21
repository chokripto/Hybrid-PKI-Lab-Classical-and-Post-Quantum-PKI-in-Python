from fastapi import FastAPI

from hybrid_pki.api.routes_classical import router as classical_router

app = FastAPI(
    title="Hybrid PKI Lab API",
    description="Classical and Post-Quantum Hybrid PKI API",
    version="1.0.0",
)

app.include_router(classical_router)


@app.get("/")
def root():
    return {
        "project": "Hybrid PKI Lab",
        "status": "running",
        "message": "API is working successfully",
        "available_modules": [
            "Classical PKI",
            "Hybrid PKI",
            "Post-Quantum Cryptography",
        ],
        "documentation": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }
