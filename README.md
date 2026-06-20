# Hybrid-PKI-Lab

Hybrid-PKI-Lab is an educational and experimental Public Key Infrastructure project written in Python.

It implements:

- Classical PKI with RSA, ECDSA and Ed25519
- Root CA and Intermediate CA
- X.509 certificate generation
- CSR generation and signing
- Certificate chain validation
- CRL-based revocation
- OCSP-like simulation
- Post-Quantum Cryptography using ML-KEM and ML-DSA
- Hybrid certificates combining classical and PQC material
- Hybrid handshake simulation
- Benchmarks for classical vs PQC algorithms

## Why this project?

Quantum computers threaten RSA, finite-field Diffie-Hellman, ECDH and ECDSA. This project shows how a traditional PKI can migrate progressively toward a hybrid PKI model.

## Supported Algorithms

### Classical

| Purpose | Algorithms |
|---|---|
| Signature | RSA-PSS, ECDSA P-256, Ed25519 |
| Key Exchange | ECDH X25519 |
| Hashing | SHA-256, SHA-384 |
| KDF | HKDF |

### Post-Quantum

| Purpose | Algorithms |
|---|---|
| KEM | ML-KEM-512, ML-KEM-768, ML-KEM-1024 |
| Signature | ML-DSA-44, ML-DSA-65, ML-DSA-87 |
| Hash-based Signature | SLH-DSA |

## Installation

```bash
git clone https://github.com/your-username/hybrid-pki-lab.git
cd hybrid-pki-lab
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
