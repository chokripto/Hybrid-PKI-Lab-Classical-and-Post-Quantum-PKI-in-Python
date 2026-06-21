# Hybrid-PKI-Lab

**Hybrid-PKI-Lab** is an educational and experimental Python project for building, testing and comparing classical Public Key Infrastructure, PKI, Post-Quantum Cryptography, PQC, and Hybrid PKI combining classical cryptography and PQC.

The project demonstrates how traditional PKI systems based on RSA, ECDSA, Ed25519 and X.509 certificates can evolve toward hybrid post-quantum architectures using algorithms such as ML-KEM and ML-DSA.

## Main Features

### Classical PKI

- Root CA generation
- Intermediate CA generation
- Server certificate issuance
- Client certificate issuance
- X.509 certificate generation
- CSR generation
- Certificate chain validation
- Certificate revocation using CRL
- OCSP-like revocation simulation
- PEM and DER serialization
- RSA, ECDSA and Ed25519 support

### Post-Quantum Cryptography

- ML-KEM key encapsulation
- ML-DSA digital signatures
- PQC key generation
- PQC signing and verification
- PQC key serialization helpers
- Classical vs PQC benchmarks

### Hybrid PKI

- Experimental hybrid certificate format
- Classical public key + PQC public key
- Classical signature + PQC signature
- Hybrid certificate validation policies
- Hybrid handshake simulation
- Hybrid shared secret derivation
- Downgrade attack demonstration
- Migration from classical PKI to hybrid PKI

## Project Structure

```text
hybrid-pki-lab/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── docs/
│   ├── 01_pki_classique.md
│   ├── 02_pki_hybride.md
│   ├── 03_pqc_algorithms.md
│   ├── 04_certificate_lifecycle.md
│   ├── 05_security_model.md
│   ├── 06_attack_scenarios.md
│   └── diagrams/
└── src/hybrid_pki/
```

## Supported Algorithms

| Category | Algorithms |
|---|---|
| Classical signatures | RSA-PSS, ECDSA P-256, Ed25519 |
| Classical key exchange | X25519, ECDH |
| Hashing | SHA-256, SHA-384 |
| KDF | HKDF |
| PQC KEM | ML-KEM-512, ML-KEM-768, ML-KEM-1024 |
| PQC signatures | ML-DSA-44, ML-DSA-65, ML-DSA-87, SLH-DSA |

## Hybrid Security Model

Recommended policy:

```text
hybrid-strict
```

Hybrid validation rule:

$$
valid_{hybrid} = valid_{classical} \land valid_{PQC}
$$

Hybrid shared secret derivation:

$$
secret_{hybrid} = HKDF(secret_{classical} \parallel secret_{PQC})
$$

## Installation

```bash
git clone https://github.com/your-username/hybrid-pki-lab.git
cd hybrid-pki-lab
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Run API

```bash
uvicorn hybrid_pki.api.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest -v
```

## Security Notice

This project is for education, research and experimentation. Do not use it directly in production without a professional cryptographic review, secure key management and proper CA operational procedures.

## License

MIT License.
