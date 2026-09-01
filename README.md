# Hybrid PKI Lab

[![Tests](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/tests.yml/badge.svg)](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/tests.yml)
[![Real PQC](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/pqc-integration.yml/badge.svg)](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/pqc-integration.yml)
[![Lint](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/lint.yml/badge.svg)](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/lint.yml)
[![Security](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/security.yml/badge.svg)](https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python/actions/workflows/security.yml)

An educational research prototype for exploring migration from classical PKI to hybrid classical/post-quantum architectures in Python.

The laboratory combines X.509, RSA, ECDSA, Ed25519 and X25519 with ML-KEM and ML-DSA through an optional, pinned `liboqs` environment.

> **Scope:** research, teaching, protocol experimentation and portfolio demonstration. This repository is not a production Certificate Authority, TLS implementation or replacement for a validated PKI stack.

## What the laboratory demonstrates

- Classical Root and Intermediate CA workflows
- Server certificates, CSRs, chains and revocation simulation
- ML-KEM key encapsulation and ML-DSA signatures
- Experimental JSON hybrid certificates with dual signatures
- Strict, classical-only, PQC-only and downgrade-demonstration policies
- Transcript-bound X25519 + ML-KEM key establishment
- Classical/PQC benchmarks and a local FastAPI interface
- Standard CI plus real-PQC integration tests inside Docker

## Security model

The recommended validation policy is `hybrid-strict`: both classical and PQC signatures must validate.

The hybrid key establishment combines independent secrets and binds HKDF to the public transcript. It remains **unauthenticated** unless a higher-level protocol signs that transcript or runs it inside an authenticated transport. The `hybrid-fallback` policy exists only to demonstrate migration and downgrade risk.

State-changing API routes are disabled by default. Docker Compose publishes services on localhost only. See [Security model and limitations](docs/10_security_model_and_limitations.md), [attack scenarios](docs/06_attack_scenarios.md), and [SECURITY.md](SECURITY.md).

## Supported algorithms

| Purpose | Implemented algorithms |
|---|---|
| Certificate/signature keys | RSA, ECDSA P-256, Ed25519 |
| Classical key establishment | X25519 |
| Hash/KDF | SHA-256, SHA-384, HKDF-SHA256 |
| PQC KEM | ML-KEM-512, ML-KEM-768, ML-KEM-1024 through liboqs |
| PQC signatures | ML-DSA-44, ML-DSA-65, ML-DSA-87 through liboqs |

Algorithm availability depends on the pinned `liboqs` build. SLH-DSA is not currently wrapped by this project.

## Standard mode

```bash
git clone https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python.git
cd Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
export HYBRID_PKI_DISABLE_OQS=1
pytest
uvicorn hybrid_pki.api.main:app --host 127.0.0.1 --port 8000
```

On PowerShell, activate with `.\.venv\Scripts\Activate.ps1` and set `$env:HYBRID_PKI_DISABLE_OQS="1"`.

## Real-PQC Docker mode

```bash
docker compose --profile pqc build hybrid-pki-pqc
docker compose --profile pqc up hybrid-pki-pqc
docker compose --profile pqc-test up --build hybrid-pki-pqc-tests
```

Swagger UI is available locally at <http://127.0.0.1:8001/docs>.

## Enabling laboratory mutations

CA initialization, certificate issuance/revocation, hybrid demo creation and benchmark execution are disabled by default.

```bash
export HYBRID_PKI_ENABLE_MUTATIONS=1
export HYBRID_PKI_API_KEY="replace-with-a-random-lab-key"
```

Send the key in the `X-Hybrid-PKI-API-Key` header. Never expose this API to an untrusted network. Root CA initialization refuses to overwrite an existing Root CA.

## API overview

Read-only routes include `/health`, `/classical/status`, `/pqc/status`, `/hybrid/status`, `/benchmarks/status` and `/benchmarks/results`. Protected routes cover CA creation, issuance, revocation, hybrid demonstrations and benchmark execution. See [API usage](docs/08_api_usage.md).

## Repository map

```text
src/hybrid_pki/
├── api/          # local FastAPI laboratory interface
├── classical/    # X.509, CA, chain and revocation primitives
├── hybrid/       # experimental certificates, policies and key establishment
└── pqc/          # liboqs provider, ML-KEM, ML-DSA and serialization

tests/            # standard and real-PQC tests
benchmarks/       # performance experiments
docs/             # architecture, threat model and migration notes
```

## Development checks

```bash
pytest
ruff check src tests examples benchmarks
black --check src tests examples benchmarks
bandit -r src -ll
pip-audit
```

GitHub Actions tests Python 3.11 and 3.12. A separate workflow builds the pinned PQC image and executes ML-KEM, ML-DSA and hybrid tests.

## Limitations

- The hybrid certificate is pedagogical JSON, not standardized X.509.
- The hybrid exchange does not authenticate peers by itself.
- Local private-key storage is for demonstrations; real CAs require an HSM or managed KMS.
- Revocation and OCSP behavior are simulations.
- Validation covers a teaching subset of full RFC 5280 path validation.
- Dependencies and containers still require periodic security review.

## Documentation

Start with [architecture](docs/09_project_architecture.md), [classical PKI](docs/01_pki_classique.md), [hybrid PKI](docs/02_pki_hybride.md), [PQC algorithms](docs/03_pqc_algorithms.md), [security limitations](docs/10_security_model_and_limitations.md), [demo scenarios](docs/11_demo_scenarios.md), and the [roadmap](docs/12_roadmap.md).

## Author

**Dr. Chokri NOUAR**  
Cybersecurity · Network Security · Post-Quantum Cryptography  
*Engineering Trust in the Digital and Quantum Era.*

## License

Released under the [MIT License](LICENSE). The license does not make the experimental design suitable for production deployment.
