\# Changelog



All notable changes to \*\*Hybrid-PKI-Lab\*\* will be documented in this file.



This project follows a practical changelog format focused on educational cybersecurity and cryptography development.



\---



\## \[1.0.0] - Initial Stable Lab Version



\### Added



\* Classical PKI core modules.

\* Root CA generation.

\* Intermediate CA generation.

\* Server certificate issuance.

\* Certificate signing request support.

\* Certificate chain validation.

\* Certificate revocation simulation.

\* PEM and DER serialization.

\* RSA, ECDSA and Ed25519 support.



\### Added



\* Post-Quantum Cryptography provider layer.

\* Optional `liboqs-python` integration.

\* Safe fallback when `liboqs` is unavailable.

\* ML-KEM wrapper.

\* ML-DSA wrapper.

\* PQC serialization helpers.



\### Added



\* Hybrid PKI core modules.

\* Experimental hybrid certificate format.

\* Classical and PQC public key binding.

\* Classical and PQC signature support.

\* Hybrid validation policies.

\* Hybrid strict validation mode.

\* Hybrid fallback validation mode.

\* Hybrid X25519 + ML-KEM handshake.

\* Hybrid shared secret derivation with HKDF.



\### Added



\* FastAPI application.

\* Classical PKI API endpoints.

\* PQC status endpoint.

\* Hybrid PKI API endpoints.

\* Benchmark API endpoints.

\* Swagger UI support.



\### Added



\* Benchmark scripts for:



&#x20; \* Key generation

&#x20; \* Signatures

&#x20; \* Handshake operations



\### Added



\* Docker support.

\* Docker PQC mode with `liboqs`.

\* Docker PQC test mode.

\* Standard mode without `liboqs`.

\* GitHub Actions workflows:



&#x20; \* Tests

&#x20; \* Lint

&#x20; \* Security



\### Added



\* Extended test suite:



&#x20; \* Core API tests

&#x20; \* API error handling tests

&#x20; \* Benchmark API tests

&#x20; \* Classical PKI workflow API tests

&#x20; \* Hybrid policy tests

&#x20; \* Hybrid certificate tests

&#x20; \* PQC serialization tests

&#x20; \* Classical key generation tests



\### Added



\* Project documentation:



&#x20; \* Classical PKI

&#x20; \* Hybrid PKI

&#x20; \* PQC algorithms

&#x20; \* Certificate lifecycle

&#x20; \* Security model

&#x20; \* Attack scenarios

&#x20; \* Docker PQC setup

&#x20; \* API usage

&#x20; \* Project architecture

&#x20; \* Security model and limitations

&#x20; \* Demo scenarios

&#x20; \* Roadmap

&#x20; \* Troubleshooting guide



\### Added



\* `CONTRIBUTING.md`

\* `CODE\_OF\_CONDUCT.md`

\* README badges

\* Project status section

\* Quick Start section



\---



\## Project Strategy



The project supports two execution modes:



```text

Standard mode:

Usable without liboqs and without Docker.



Docker PQC mode:

Full post-quantum functionality with liboqs through Docker.

```



\---



\## Security Notice



Hybrid-PKI-Lab is an educational and experimental project.



It is not production-ready and should not be used as a real Certificate Authority without professional cryptographic review, secure key management and operational hardening.



