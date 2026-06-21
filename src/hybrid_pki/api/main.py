from fastapi import FastAPI

app = FastAPI(
    title="Hybrid PKI Lab API",
    description="Classical and Post-Quantum Hybrid PKI API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "project": "Hybrid PKI Lab",
        "status": "running",
        "message": "API is working successfully",
        "features": [
            "Classical PKI",
            "Hybrid PKI",
            "Post-Quantum Cryptography",
            "ML-KEM",
            "ML-DSA",
        ],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
