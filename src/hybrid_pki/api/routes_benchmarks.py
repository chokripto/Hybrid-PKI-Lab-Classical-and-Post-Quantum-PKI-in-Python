from __future__ import annotations

import json
from pathlib import Path

from benchmarks.benchmark_handshake import benchmark_handshakes
from benchmarks.benchmark_keygen import benchmark_classical_keygen, benchmark_pqc_keygen
from benchmarks.benchmark_signatures import (
    benchmark_classical_signatures,
    benchmark_pqc_signatures,
)
from fastapi import APIRouter

router = APIRouter(
    prefix="/benchmarks",
    tags=["Benchmarks"],
)

RESULTS_DIR = Path("benchmarks") / "results"
KEYGEN_RESULTS_PATH = RESULTS_DIR / "keygen_results.json"
SIGNATURE_RESULTS_PATH = RESULTS_DIR / "signature_results.json"
HANDSHAKE_RESULTS_PATH = RESULTS_DIR / "handshake_results.json"


def save_json_result(path: Path, data: dict) -> None:
    """
    Save benchmark result as JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def load_json_result(path: Path) -> dict | None:
    """
    Load benchmark result if it exists.
    """
    if not path.exists():
        return None

    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/status")
def benchmark_status():
    """
    Show benchmark subsystem status.
    """
    return {
        "status": "available",
        "results_directory": str(RESULTS_DIR),
        "results": {
            "keygen": {
                "exists": KEYGEN_RESULTS_PATH.exists(),
                "path": str(KEYGEN_RESULTS_PATH),
            },
            "signatures": {
                "exists": SIGNATURE_RESULTS_PATH.exists(),
                "path": str(SIGNATURE_RESULTS_PATH),
            },
            "handshake": {
                "exists": HANDSHAKE_RESULTS_PATH.exists(),
                "path": str(HANDSHAKE_RESULTS_PATH),
            },
        },
        "available_benchmarks": [
            "key generation",
            "signatures",
            "handshake",
        ],
    }


@router.post("/run-keygen")
def run_keygen_benchmark():
    """
    Run classical and PQC key generation benchmarks.

    PQC benchmarks are skipped automatically if liboqs is unavailable.
    """
    results = {
        "benchmark": "key generation",
        "classical": benchmark_classical_keygen(),
        "pqc": benchmark_pqc_keygen(),
    }

    save_json_result(KEYGEN_RESULTS_PATH, results)

    return {
        "status": "success",
        "message": "Key generation benchmark completed",
        "results_path": str(KEYGEN_RESULTS_PATH),
        "results": results,
    }


@router.post("/run-signatures")
def run_signature_benchmark():
    """
    Run classical and PQC signature benchmarks.

    PQC benchmarks are skipped automatically if liboqs is unavailable.
    """
    results = {
        "benchmark": "signatures",
        "classical": benchmark_classical_signatures(),
        "pqc": benchmark_pqc_signatures(),
    }

    save_json_result(SIGNATURE_RESULTS_PATH, results)

    return {
        "status": "success",
        "message": "Signature benchmark completed",
        "results_path": str(SIGNATURE_RESULTS_PATH),
        "results": results,
    }


@router.post("/run-handshake")
def run_handshake_benchmark():
    """
    Run classical and hybrid handshake benchmarks.

    Hybrid PQC benchmark is skipped automatically if liboqs is unavailable.
    """
    results = {
        "benchmark": "handshake",
        "results": benchmark_handshakes(),
    }

    save_json_result(HANDSHAKE_RESULTS_PATH, results)

    return {
        "status": "success",
        "message": "Handshake benchmark completed",
        "results_path": str(HANDSHAKE_RESULTS_PATH),
        "results": results,
    }


@router.get("/results")
def get_benchmark_results():
    """
    Return saved benchmark results.
    """
    return {
        "status": "success",
        "results": {
            "keygen": load_json_result(KEYGEN_RESULTS_PATH),
            "signatures": load_json_result(SIGNATURE_RESULTS_PATH),
            "handshake": load_json_result(HANDSHAKE_RESULTS_PATH),
        },
    }
