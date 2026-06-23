from __future__ import annotations

import json
import statistics
import time
from collections.abc import Callable
from pathlib import Path

from hybrid_pki.classical.keygen import (
    generate_ecdsa_private_key,
    generate_ed25519_private_key,
    generate_rsa_private_key,
)
from hybrid_pki.pqc.oqs_provider import is_oqs_available

RESULTS_DIR = Path("benchmarks/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def benchmark_function(
    name: str,
    function: Callable,
    iterations: int = 20,
) -> dict:
    durations = []

    for _ in range(iterations):
        start = time.perf_counter()
        function()
        end = time.perf_counter()
        durations.append(end - start)

    return {
        "name": name,
        "iterations": iterations,
        "total_seconds": sum(durations),
        "average_seconds": statistics.mean(durations),
        "min_seconds": min(durations),
        "max_seconds": max(durations),
    }


def benchmark_classical_keygen() -> list[dict]:
    return [
        benchmark_function(
            "RSA-3072 key generation",
            lambda: generate_rsa_private_key(3072),
            iterations=5,
        ),
        benchmark_function(
            "ECDSA-P256 key generation",
            generate_ecdsa_private_key,
            iterations=50,
        ),
        benchmark_function(
            "Ed25519 key generation",
            generate_ed25519_private_key,
            iterations=50,
        ),
    ]


def benchmark_pqc_keygen() -> list[dict]:
    if not is_oqs_available():
        return [
            {
                "name": "PQC key generation",
                "status": "skipped",
                "reason": "liboqs-python is not installed",
            }
        ]

    from hybrid_pki.pqc.ml_dsa import MLDSA
    from hybrid_pki.pqc.ml_kem import MLKEM

    return [
        benchmark_function(
            "ML-KEM-768 key generation",
            lambda: MLKEM("ML-KEM-768").generate_keypair(),
            iterations=20,
        ),
        benchmark_function(
            "ML-DSA-65 key generation",
            lambda: MLDSA("ML-DSA-65").generate_keypair(),
            iterations=20,
        ),
    ]


def main() -> None:
    results = {
        "benchmark": "key generation",
        "classical": benchmark_classical_keygen(),
        "pqc": benchmark_pqc_keygen(),
    }

    output_path = RESULTS_DIR / "keygen_results.json"
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(json.dumps(results, indent=2))
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
