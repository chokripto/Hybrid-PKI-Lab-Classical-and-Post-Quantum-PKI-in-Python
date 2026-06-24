# Hybrid-PKI-Lab

**Hybrid-PKI-Lab** is an educational and experimental Python project for building, testing and comparing classical Public Key Infrastructure, PKI, Post-Quantum Cryptography, PQC, and Hybrid PKI combining classical cryptography and PQC.

The project demonstrates how traditional PKI systems based on RSA, ECDSA, Ed25519 and X.509 certificates can evolve toward hybrid post-quantum architectures using algorithms such as ML-KEM and ML-DSA.

---

## Main Features

### Classical PKI

* Root CA generation
* Intermediate CA generation
* Server certificate issuance
* Client certificate issuance
* X.509 certificate generation
* CSR generation
* Certificate chain validation
* Certificate revocation using CRL
* OCSP-like revocation simulation
* PEM and DER serialization
* RSA, ECDSA and Ed25519 support

### Post-Quantum Cryptography

* ML-KEM key encapsulation
* ML-DSA digital signatures
* PQC key generation
* PQC signing and verification
* PQC key serialization helpers
* Classical vs PQC benchmarks
* Optional `liboqs-python` provider
* Safe fallback when `liboqs` is unavailable

### Hybrid PKI

* Experimental hybrid certificate format
* Classical public key + PQC public key
* Classical signature + PQC signature
* Hybrid certificate validation policies
* Hybrid handshake simulation
* Hybrid shared secret derivation
* Downgrade attack demonstration
* Migration from classical PKI to hybrid PKI

### API

* FastAPI-based REST API
* Classical PKI endpoints
* PQC status endpoint
* Hybrid PKI endpoints
* Benchmark endpoints
* Swagger UI documentation

---

## Project Strategy

This project supports two execution modes:

```text
Standard mode:
Usable without liboqs and without Docker.

Advanced mode:
Full post-quantum functionality with liboqs through Docker.
```

This strategy keeps the project easy to install and test while still supporting real post-quantum cryptography experiments in a controlled Docker environment.

---

## Execution Modes

### Standard Mode

The standard mode works without `liboqs` and without Docker.

It is recommended for:

* Normal development
* GitHub Actions
* Classical PKI features
* Stable and fast tests
* Users who do not want to install native PQC dependencies

In this mode:

* Classical PKI works.
* The FastAPI application works.
* Classical benchmarks work.
* PQC features are safely skipped or reported as unavailable.
* Tests remain fast and stable.

Run:

```powershell
$env:HYBRID_PKI_DISABLE_OQS="1"
pytest -v
```

Expected result:

```text
passed + skipped
```

The skipped tests are the real PQC tests that require `liboqs`.

---

### Docker PQC Mode

The Docker PQC mode enables real post-quantum cryptography through `liboqs`.

It supports:

* ML-KEM
* ML-DSA
* Hybrid X25519 + ML-KEM handshake
* Hybrid certificate experiments
* PQC benchmarks
* Real `liboqs-python` execution inside Docker

Build the PQC image:

```powershell
docker compose --profile pqc build hybrid-pki-pqc
```

Run the PQC API:

```powershell
docker compose --profile pqc up hybrid-pki-pqc
```

Open Swagger UI:

```text
http://127.0.0.1:8001/docs
```

Full Docker PQC setup guide:

```text
docs/07_docker_pqc_setup.md
```

---

## Project Structure

```text
hybrid-pki-lab/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── Dockerfile
├── Dockerfile.pqc
├── docker-compose.yml
├── Makefile
├── docs/
│   ├── 01_pki_classique.md
│   ├── 02_pki_hybride.md
│   ├── 03_pqc_algorithms.md
│   ├── 04_certificate_lifecycle.md
│   ├── 05_security_model.md
│   ├── 06_attack_scenarios.md
│   ├── 07_docker_pqc_setup.md
│   └── diagrams/
├── benchmarks/
│   ├── benchmark_keygen.py
│   ├── benchmark_signatures.py
│   ├── benchmark_handshake.py
│   └── results/
├── tests/
└── src/hybrid_pki/
```

---

## Supported Algorithms

| Category               | Algorithms                               |
| ---------------------- | ---------------------------------------- |
| Classical signatures   | RSA-PSS, ECDSA P-256, Ed25519            |
| Classical key exchange | X25519, ECDH                             |
| Hashing                | SHA-256, SHA-384                         |
| KDF                    | HKDF                                     |
| PQC KEM                | ML-KEM-512, ML-KEM-768, ML-KEM-1024      |
| PQC signatures         | ML-DSA-44, ML-DSA-65, ML-DSA-87, SLH-DSA |

---

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

The `hybrid-strict` policy requires both the classical and the post-quantum cryptographic checks to succeed.

---

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python.git
cd Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### Linux / macOS

```bash
git clone https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python.git
cd Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python

python -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

---

## Run API

### Standard API

```bash
uvicorn hybrid_pki.api.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

Or on Windows PowerShell:

```powershell
python -m uvicorn hybrid_pki.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Docker

### Standard Docker Mode

```powershell
docker compose up --build
```

Open:

```text
http://127.0.0.1:8000/docs
```

### Docker PQC Mode

Build the image with `liboqs`:

```powershell
docker compose --profile pqc build hybrid-pki-pqc
```

Run the PQC API:

```powershell
docker compose --profile pqc up hybrid-pki-pqc
```

Open:

```text
http://127.0.0.1:8001/docs
```

Stop the PQC API:

```powershell
docker compose --profile pqc down
```

---

## API Endpoints

### General

```text
GET /
GET /health
```

### Classical PKI

```text
POST /classical/ca/root/init
POST /classical/ca/intermediate/init
POST /classical/certificates/server/issue
POST /classical/certificates/server/verify
POST /classical/certificates/server/revoke
GET  /classical/certificates/revoked
GET  /classical/status
```

### PQC

```text
GET /pqc/status
```

### Hybrid PKI

```text
GET  /hybrid/status
POST /hybrid/ca/create-demo
POST /hybrid/certificates/create-demo
POST /hybrid/certificates/verify-demo
POST /hybrid/handshake/simulate
```

### Benchmarks

```text
GET  /benchmarks/status
POST /benchmarks/run-keygen
POST /benchmarks/run-signatures
POST /benchmarks/run-handshake
GET  /benchmarks/results
```

---

## Verify PQC Availability

When running in Docker PQC mode, open Swagger and run:

```text
GET /pqc/status
```

Expected result:

```json
{
  "available": true,
  "message": "liboqs-python is available."
}
```

You can also test from PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/pqc/status
```

---

## Hybrid Handshake Example

In Docker PQC mode, run:

```text
POST /hybrid/handshake/simulate
```

Request body:

```json
{
  "pqc_algorithm": "ML-KEM-768"
}
```

Expected result:

```json
{
  "status": "success",
  "algorithm": {
    "classical": "X25519",
    "pqc": "ML-KEM-768",
    "kdf": "HKDF-SHA256"
  },
  "secrets_match": true
}
```

The most important value is:

```json
"secrets_match": true
```

This confirms that the hybrid key exchange works correctly with both classical and post-quantum key exchange material.

---

## Tests

### Standard Tests

Use this mode for normal development and GitHub Actions:

```powershell
$env:HYBRID_PKI_DISABLE_OQS="1"
pytest -v
```

Expected result:

```text
passed + skipped
```

### Docker PQC Tests

Use this mode to run real PQC tests with `liboqs`:

```powershell
docker compose --profile pqc-test up --build hybrid-pki-pqc-tests
```

In this mode, tests that are skipped in standard mode should run with real `liboqs` support.

---

## Benchmarks

Run benchmark scripts locally:

```powershell
python benchmarks/benchmark_keygen.py
python benchmarks/benchmark_signatures.py
python benchmarks/benchmark_handshake.py
```

Run benchmarks in Docker PQC mode:

```powershell
docker compose --profile pqc run --rm hybrid-pki-pqc python benchmarks/benchmark_keygen.py
docker compose --profile pqc run --rm hybrid-pki-pqc python benchmarks/benchmark_signatures.py
docker compose --profile pqc run --rm hybrid-pki-pqc python benchmarks/benchmark_handshake.py
```

Benchmark results are written to:

```text
benchmarks/results/
```

Generated JSON benchmark results should not be committed to GitHub.

---

## Development Commands

Format code:

```powershell
python -m black src tests examples benchmarks
```

Run Ruff:

```powershell
python -m ruff check src tests examples benchmarks --fix
```

Run tests:

```powershell
pytest -v
```

Check Git status:

```powershell
git status
```

---

## Security Notice

This project is for education, research and experimentation.

Do not use it directly in production without:

* Professional cryptographic review
* Secure key management
* Proper CA operational procedures
* Hardened infrastructure
* Audit logging
* Secure revocation handling
* Formal policy and compliance review

Generated keys, certificates, benchmark results and local logs should not be committed to GitHub.

---

## Documentation

Additional documentation is available in the `docs/` directory:

```text
docs/01_pki_classique.md
docs/02_pki_hybride.md
docs/03_pqc_algorithms.md
docs/04_certificate_lifecycle.md
docs/05_security_model.md
docs/06_attack_scenarios.md
docs/07_docker_pqc_setup.md
docs/08_api_usage.md
```

---

## License

MIT License.
