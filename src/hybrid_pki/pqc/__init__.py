"""
Post-Quantum Cryptography modules for Hybrid-PKI-Lab.

This package provides wrappers for PQC algorithms such as:

- ML-KEM for key encapsulation
- ML-DSA for digital signatures

The implementation uses liboqs-python when available.
"""

from hybrid_pki.pqc.oqs_provider import is_oqs_available

__all__ = [
    "is_oqs_available",
]
