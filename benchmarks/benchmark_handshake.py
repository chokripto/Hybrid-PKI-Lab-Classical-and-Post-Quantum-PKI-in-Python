from __future__ import annotations

import json
import statistics
import time
from collections.abc import Callable
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric import x25519

from hybrid_pki.hybrid.hybrid_handshake import (
    client_hybrid_encapsulate,
    generate_server_hybrid_handshake_keys,
    server_hybrid_decapsulate,
)
from hybrid_pki.pqc.oqs_provider import is_oqs_available

RESULTS_DIR = Path("benchmarks/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def benchmark_function(
    name: str,
    function: Callable,
    iterations: int = 50,
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


def classical_x25519_handshake() -> bytes:
    server_private_key = x25519.X25519PrivateKey.generate()
    client_private_key = x25519.X25519PrivateKey.generate()

    server_public_key = server_private_key.public_key()
    client_public_key = client_private_key.public_key()

    client_secret = client_private_key.exchange(server_public_key)
    server_secret = server_private_key.exchange(client_public_key)

    if client_secret != server_secret:
        raise RuntimeError("X25519 shared secrets do not match")

    return client_secret


def hybrid_x25519_mlkem_handshake() -> bytes:
    server_keys = generate_server_hybrid_handshake_keys("ML-KEM-768")

    client_result = client_hybrid_encapsulate(
        server_classical_public_key_bytes=server_keys.classical_public_key_bytes,
        server_pqc_public_key=server_keys.pqc_public_key,
        pqc_algorithm=server_keys.pqc_algorithm,
    )

    server_secret = server_hybrid_decapsulate(
        server_classical_private_key=server_keys.classical_private_key,
        client_classical_public_key_bytes=client_result.client_classical_public_key_bytes,
        server_pqc_secret_key=server_keys.pqc_secret_key,
        pqc_ciphertext=client_result.pqc_ciphertext,
        pqc_algorithm=server_keys.pqc_algorithm,
    )

    if server_secret != client_result.hybrid_secret:
        raise RuntimeError("Hybrid shared secrets do not match")

    return server_secret


def benchmark_handshakes() -> list[dict]:
    results = [
        benchmark_function(
            "Classical X25519 handshake",
            classical_x25519_handshake,
            iterations=100,
        )
    ]

    if is_oqs_available():
        results.append(
            benchmark_function(
                "Hybrid X25519 + ML-KEM-768 handshake",
                hybrid_x25519_mlkem_handshake,
                iterations=30,
            )
        )
    else:
        results.append(
            {
                "name": "Hybrid X25519 + ML-KEM-768 handshake",
                "status": "skipped",
                "reason": "liboqs-python is not installed",
            }
        )

    return results


def main() -> None:
    results = {
        "benchmark": "handshake",
        "results": benchmark_handshakes(),
    }

    output_path = RESULTS_DIR / "handshake_results.json"
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(json.dumps(results, indent=2))
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
