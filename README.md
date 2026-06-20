# Hybrid-PKI-Lab

**Hybrid-PKI-Lab** is an educational and experimental Python project for building, testing and comparing:

- Classical Public Key Infrastructure, PKI
- Post-Quantum Cryptography, PQC
- Hybrid PKI combining classical cryptography and PQC

The project demonstrates how traditional PKI systems based on RSA, ECDSA, Ed25519 and X.509 certificates can evolve toward hybrid post-quantum architectures using algorithms such as ML-KEM and ML-DSA.

> This project is designed for cybersecurity learning, cryptography labs, academic projects, research demonstrations and GitHub portfolio work.

---

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

---

## Project Structure

```text
hybrid-pki-lab/
│
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
│
├── docs/
│   ├── 01_pki_classique.md
│   ├── 02_pki_hybride.md
│   ├── 03_pqc_algorithms.md
│   ├── 04_certificate_lifecycle.md
│   ├── 05_security_model.md
│   ├── 06_attack_scenarios.md
│   └── diagrams/
│
├── src/
│   └── hybrid_pki/
│       ├── classical/
│       ├── pqc/
│       ├── hybrid/
│       ├── crypto/
│       ├── api/
│       ├── cli.py
│       └── config.py
│
├── examples/
├── tests/
├── benchmarks/
├── scripts/
├── certs/
└── .github/
```

---

## Supported Algorithms

### Classical Algorithms

| Use Case | Algorithms |
|---|---|
| Digital Signature | RSA-PSS, ECDSA P-256, Ed25519 |
| Key Exchange | X25519, ECDH |
| Hashing | SHA-256, SHA-384 |
| KDF | HKDF |
| Certificate Format | X.509 |

### Post-Quantum Algorithms

| Use Case | Algorithms |
|---|---|
| Key Encapsulation | ML-KEM-512, ML-KEM-768, ML-KEM-1024 |
| Digital Signature | ML-DSA-44, ML-DSA-65, ML-DSA-87 |
| Hash-Based Signature | SLH-DSA |

---

## Hybrid Security Model

Hybrid-PKI-Lab supports several validation policies:

| Policy | Description |
|---|---|
| `classical-only` | Accept only the classical signature |
| `pqc-only` | Accept only the PQC signature |
| `hybrid-strict` | Accept only if both classical and PQC signatures are valid |
| `hybrid-fallback` | Accept if at least one signature is valid |

Recommended policy:

```text
hybrid-strict
```

The hybrid validation rule is:

$$
valid_{hybrid} = valid_{classical} \land valid_{PQC}
$$

The hybrid shared secret is derived as:

$$
secret_{hybrid} = HKDF(secret_{classical} \parallel secret_{PQC})
$$

---

## Requirements

- Python 3.11+
- OpenSSL
- liboqs
- liboqs-python
- Docker, optional

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hybrid-pki-lab.git
cd hybrid-pki-lab
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install the package locally

```bash
pip install -e .
```

---

## Running the CLI

```bash
hybrid-pki --help
```

Examples:

```bash
hybrid-pki init-classical-pki
hybrid-pki issue-classical-cert --common-name example.com
hybrid-pki init-hybrid-pki
hybrid-pki issue-hybrid-cert --common-name pqc.example.com
hybrid-pki verify-cert certs/hybrid/server.json --policy hybrid-strict
hybrid-pki benchmark
```

---

## Running the API

```bash
uvicorn hybrid_pki.api.main:app --reload
```

Then open:

```text
http://localhost:8000
http://localhost:8000/docs
```

---

## Running with Docker

Build the image:

```bash
docker build -t hybrid-pki-lab .
```

Run the container:

```bash
docker run -p 8000:8000 hybrid-pki-lab
```

Or use Docker Compose:

```bash
docker compose up --build
```

API documentation:

```text
http://localhost:8000/docs
```

---

## Running Tests

```bash
pytest -v
```

With coverage:

```bash
pytest -v --cov=hybrid_pki --cov-report=term-missing
```

---

## Running Benchmarks

```bash
python benchmarks/benchmark_keygen.py
python benchmarks/benchmark_signatures.py
python benchmarks/benchmark_handshake.py
```

Or:

```bash
make benchmark
```

---

## Example Labs

| Lab | Description |
|---|---|
| Lab 1 | Generate a Root CA |
| Lab 2 | Generate an Intermediate CA |
| Lab 3 | Issue a Server Certificate |
| Lab 4 | Validate a Certificate Chain |
| Lab 5 | Revoke a Certificate |
| Lab 6 | Generate ML-KEM Keys |
| Lab 7 | Generate ML-DSA Signatures |
| Lab 8 | Create a Hybrid Certificate |
| Lab 9 | Simulate a Hybrid Handshake |
| Lab 10 | Simulate a Downgrade Attack |

---

## Security Notice

This project is for education, research and experimentation.

Do not use this project directly in production without:

- professional cryptographic review
- secure key management
- hardware security module integration
- proper compliance validation
- secure CA operational procedures

---

## Roadmap

### v1.0 Classical PKI

- [ ] RSA key generation
- [ ] ECDSA key generation
- [ ] Ed25519 key generation
- [ ] Root CA generation
- [ ] Intermediate CA generation
- [ ] Server certificate issuance
- [ ] Client certificate issuance
- [ ] Certificate chain validation
- [ ] CRL revocation

### v2.0 PQC Layer

- [ ] ML-KEM support
- [ ] ML-DSA support
- [ ] PQC key serialization
- [ ] PQC signatures
- [ ] PQC benchmarks

### v3.0 Hybrid PKI

- [ ] Hybrid certificate format
- [ ] Hybrid certificate signing
- [ ] Hybrid certificate validation
- [ ] Hybrid handshake simulation
- [ ] Downgrade attack demo

### v4.0 API and Dashboard

- [ ] FastAPI backend
- [ ] Certificate management API
- [ ] Revocation API
- [ ] Benchmark API
- [ ] Web dashboard

---

## License

This project is licensed under the MIT License.
