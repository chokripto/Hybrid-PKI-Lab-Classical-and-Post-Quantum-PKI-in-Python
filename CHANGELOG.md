# Changelog

All notable changes to Hybrid PKI Lab are documented here.

## Unreleased

### Security

- Disabled state-changing API operations by default and added optional API-key protection.
- Restricted Docker-published ports to localhost and prevented silent Root CA overwrite.
- Restricted certificate paths and added atomic owner-only key storage.
- Added strict Base64 decoding.

### PQC and reproducibility

- Separated the standard image from the native liboqs toolchain.
- Pinned the real-PQC Docker environment and removed masked installation failures.
- Added non-root containers and a real-PQC integration workflow.
- Expanded standard CI to Python 3.11 and 3.12.

### Hybrid protocol

- Bound HKDF derivation to a versioned public handshake transcript.
- Documented the lack of peer authentication.
- Added hybrid-certificate schema, timestamp, validity and expected-issuer checks.
- Added issuer/subject linkage checks to classical chain validation.

### Documentation

- Reframed the project as an educational research prototype.
- Corrected algorithm claims and clarified downgrade and production limitations.
- Added SECURITY.md and improved package metadata.

## 1.0.0

Initial educational laboratory release with classical PKI, optional ML-KEM and ML-DSA integration, experimental hybrid certificates, FastAPI demonstrations, benchmarks, Docker support, tests and technical documentation.
