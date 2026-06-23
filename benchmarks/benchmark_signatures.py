from __future__ import annotations

import json
import statistics
import time
from collections.abc import Callable
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding

from hybrid_pki.classical.keygen import (
    generate_ecdsa_private_key,
    generate_ed25519_private_key,
    generate_rsa_private_key,
)
from hybrid_pki.pqc.oqs_provider import is_oqs_available

RESULTS_DIR = Path("benchmarks/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MESSAGE = b"Hybrid PKI Lab signature benchmark message"


def benchmark_function(
    name: str,
    function: Callable,
    iterations: int = 100,
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


def benchmark_classical_signatures() -> list[dict]:
    rsa_key = generate_rsa_private_key(3072)
    ecdsa_key = generate_ecdsa_private_key()
    ed25519_key = generate_ed25519_private_key()

    rsa_signature = rsa_key.sign(
        MESSAGE,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    ecdsa_signature = ecdsa_key.sign(
        MESSAGE,
        ec.ECDSA(hashes.SHA256()),
    )

    ed25519_signature = ed25519_key.sign(MESSAGE)

    return [
        benchmark_function(
            "RSA-3072 PSS signing",
            lambda: rsa_key.sign(
                MESSAGE,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            ),
            iterations=50,
        ),
        benchmark_function(
            "RSA-3072 PSS verification",
            lambda: rsa_key.public_key().verify(
                rsa_signature,
                MESSAGE,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            ),
            iterations=100,
        ),
        benchmark_function(
            "ECDSA-P256 signing",
            lambda: ecdsa_key.sign(
                MESSAGE,
                ec.ECDSA(hashes.SHA256()),
            ),
            iterations=100,
        ),
        benchmark_function(
            "ECDSA-P256 verification",
            lambda: ecdsa_key.public_key().verify(
                ecdsa_signature,
                MESSAGE,
                ec.ECDSA(hashes.SHA256()),
            ),
            iterations=100,
        ),
        benchmark_function(
            "Ed25519 signing",
            lambda: ed25519_key.sign(MESSAGE),
            iterations=100,
        ),
        benchmark_function(
            "Ed25519 verification",
            lambda: ed25519_key.public_key().verify(
                ed25519_signature,
                MESSAGE,
            ),
            iterations=100,
        ),
    ]


def benchmark_pqc_signatures() -> list[dict]:
    if not is_oqs_available():
        return [
            {
                "name": "PQC signatures",
                "status": "skipped",
                "reason": "liboqs-python is not installed",
            }
        ]

    from hybrid_pki.pqc.ml_dsa import MLDSA

    signer = MLDSA("ML-DSA-65")
    keypair = signer.generate_keypair()
    signature = signer.sign(keypair.secret_key, MESSAGE)

    return [
        benchmark_function(
            "ML-DSA-65 signing",
            lambda: signer.sign(keypair.secret_key, MESSAGE),
            iterations=50,
        ),
        benchmark_function(
            "ML-DSA-65 verification",
            lambda: signer.verify(
                keypair.public_key,
                MESSAGE,
                signature.signature,
            ),
            iterations=50,
        ),
    ]


def main() -> None:
    results = {
        "benchmark": "signatures",
        "classical": benchmark_classical_signatures(),
        "pqc": benchmark_pqc_signatures(),
    }

    output_path = RESULTS_DIR / "signature_results.json"
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(json.dumps(results, indent=2))
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
