\# Security Model and Limitations



This document describes the security model, assumptions, limitations and risks of \*\*Hybrid-PKI-Lab\*\*.



Hybrid-PKI-Lab is an educational and experimental project. It demonstrates classical PKI, post-quantum cryptography and hybrid PKI concepts, but it is not intended for production use.



\---



\## 1. Purpose of the Project



The main purpose of this project is to demonstrate:



```text

Classical PKI concepts

Post-quantum cryptography integration

Hybrid certificate models

Hybrid X25519 + ML-KEM handshakes

Classical and PQC benchmark comparisons

Migration ideas from classical PKI to hybrid PKI

```



The project is designed for:



\* Learning

\* Research

\* Experimentation

\* Demonstrations

\* Security engineering practice

\* GitHub portfolio presentation



It is not designed to operate as a real certificate authority.



\---



\## 2. Security Scope



The project focuses on cryptographic and PKI concepts such as:



```text

Key generation

Certificate issuance

Certificate validation

Certificate revocation simulation

PQC provider detection

Hybrid signatures

Hybrid handshake simulation

Hybrid validation policies

Benchmarking

```



The project does not fully implement a production PKI operational environment.



\---



\## 3. Main Security Assumptions



The project assumes:



```text

The local machine is trusted.

Generated keys are used only for testing.

The API is not exposed directly to the public Internet.

Users understand that generated certificates are not production certificates.

Docker PQC mode is used only for experiments.

```



If these assumptions are false, the security properties of the lab do not hold.



\---



\## 4. What the Project Protects



The project demonstrates how to protect against some cryptographic transition risks.



Examples:



\* Classical-only PKI dependence

\* Lack of PQC migration strategy

\* Downgrade risks in hybrid validation

\* Missing PQC capability detection

\* Unsafe hard dependency on native PQC libraries

\* Lack of separation between standard and PQC execution modes



The recommended hybrid validation rule is:



$$

valid\_{hybrid} = valid\_{classical} \\land valid\_{PQC}

$$



This means that in strict hybrid mode, both the classical and post-quantum checks must succeed.



\---



\## 5. What the Project Does Not Protect



This project does not protect against all real-world PKI threats.



It does not provide:



```text

Hardware Security Module integration

Secure CA ceremony

Production key lifecycle management

Multi-person approval workflows

Certificate transparency

Real OCSP responder

Enterprise-grade CRL distribution

Secure audit logging

Access control

Authentication for API endpoints

Authorization model

Network hardening

Tamper-resistant storage

Compliance controls

Formal verification

Side-channel resistance guarantees

```



It should not be used as a production CA.



\---



\## 6. Classical PKI Risks



Classical PKI systems can be affected by several risks.



\### 6.1 Private Key Compromise



If a CA private key is compromised, an attacker may issue fraudulent certificates.



In a production PKI, CA private keys should be protected using:



```text

HSM

KMS

Offline root CA

Strict access control

Audit logs

Key ceremony procedures

```



This lab stores generated material locally for educational purposes only.



\---



\### 6.2 Weak Operational Security



Even if the cryptographic algorithms are strong, PKI security can fail because of weak operations.



Examples:



```text

Poor private key storage

No access control

No audit trail

Weak certificate policies

Missing revocation process

Improper CA hierarchy

```



This project demonstrates PKI logic, not production PKI operations.



\---



\### 6.3 Revocation Limitations



The project includes CRL-style revocation logic and OCSP-like simulation.



However, it does not implement a complete production revocation system.



Missing production features include:



```text

Public CRL distribution point

Real OCSP responder

Signed revocation service

High availability revocation infrastructure

Revocation freshness guarantees

```



\---



\## 7. Post-Quantum Cryptography Risks



Post-quantum cryptography is still an evolving area.



This project uses PQC algorithms through `liboqs-python` when Docker PQC mode is enabled.



\### 7.1 Implementation Dependency



The PQC features depend on:



```text

liboqs

liboqs-python

Docker PQC environment

Supported ML-KEM and ML-DSA implementations

```



If `liboqs` is unavailable, broken or disabled, the project reports PQC as unavailable instead of crashing.



This behavior is intentional.



\---



\### 7.2 Algorithm Agility



PQC standards and implementations may evolve.



The project is designed to be algorithm-agile by using configurable algorithm names such as:



```text

ML-KEM-768

ML-DSA-65

```



In a production system, algorithm choices should follow current standards, security levels and regulatory guidance.



\---



\### 7.3 Side-Channel Considerations



This project does not make side-channel resistance claims.



It does not evaluate:



```text

Timing attacks

Cache attacks

Power analysis

Fault injection

Memory disclosure

Microarchitectural leakage

```



The cryptographic backend may include countermeasures, but this project itself does not validate them.



\---



\## 8. Hybrid PKI Risks



Hybrid PKI combines classical cryptography and PQC. This can improve migration resilience, but it also introduces design complexity.



\---



\### 8.1 Downgrade Risk



A major hybrid PKI risk is downgrade.



A downgrade attack happens when an attacker causes a system to accept a weaker mode, for example:



```text

Accepting classical-only validation when hybrid validation was expected

Ignoring the PQC signature

Ignoring the classical signature

Treating missing PQC material as valid

```



For this reason, the recommended policy is:



```text

hybrid-strict

```



The strict policy requires both classical and PQC validation.



\---



\### 8.2 Policy Confusion



Hybrid systems need clear validation rules.



Possible policies include:



| Policy            | Risk                                                |

| ----------------- | --------------------------------------------------- |

| `classical-only`  | No PQC protection                                   |

| `pqc-only`        | No classical fallback                               |

| `hybrid-fallback` | May allow downgrade if misused                      |

| `hybrid-strict`   | Stronger, but less tolerant of missing PQC material |



Recommended policy for security-sensitive experiments:



```text

hybrid-strict

```



\---



\### 8.3 Hybrid Secret Composition



The hybrid handshake derives a combined secret:



$$

secret\_{hybrid} = HKDF(secret\_{classical} \\parallel secret\_{PQC})

$$



This construction is intended to combine the classical X25519 shared secret and the PQC ML-KEM shared secret.



A production design would require additional review of:



```text

Key separation

Transcript binding

Authentication

Downgrade protection

Protocol negotiation

Replay protection

Context binding

```



\---



\## 9. API Security Limitations



The FastAPI layer is designed for local experimentation.



It does not currently implement:



```text

Authentication

Authorization

Rate limiting

Request signing

TLS termination

Tenant isolation

Secure audit logging

Input abuse protection

Network-level access control

```



Do not expose the API directly to the public Internet.



Recommended usage:



```text

Localhost only

Private lab network only

Docker local environment only

```



\---



\## 10. Docker Security Limitations



Docker PQC mode is used to provide a reproducible Linux environment for `liboqs`.



Docker improves reproducibility, but it does not automatically make the system production-secure.



Limitations:



```text

The container runs a lab API.

Generated certificates are mounted to local folders.

Benchmark results are written to local folders.

Secrets may exist inside mounted volumes.

The Docker image is not hardened for production.

```



For production-grade containers, additional controls are required:



```text

Non-root user

Read-only filesystem

Secrets management

Minimal runtime image

Image signing

Vulnerability scanning

Network restrictions

Runtime sandboxing

```



\---



\## 11. Generated Files and Secrets



The project may generate sensitive artifacts under:



```text

certs/

logs/

benchmarks/results/

```



These files may include:



```text

Private keys

Public keys

Certificates

CSRs

CRLs

Hybrid certificate JSON files

Benchmark output

Runtime logs

```



These files should not be committed to GitHub.



The `.gitignore` should exclude generated artifacts.



\---



\## 12. GitHub Safety Rules



The repository should include:



```text

Source code

Tests

Documentation

Dockerfiles

Configuration templates

```



The repository should not include:



```text

Private keys

Generated certificates

Generated CRLs

Generated benchmark JSON files

Local logs

Virtual environments

Python cache files

.env files

```



Before committing, always run:



```powershell

git status

```



And verify that no generated secret material is staged.



\---



\## 13. Testing Security Model



The project uses two testing modes.



\### 13.1 Standard CI Tests



Standard tests run with:



```text

HYBRID\_PKI\_DISABLE\_OQS=1

```



This ensures:



```text

No native liboqs requirement

Fast tests

Stable GitHub Actions

PQC tests skipped safely

```



\### 13.2 Docker PQC Tests



Docker PQC tests run with real `liboqs`.



Command:



```powershell

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests

```



This validates real PQC operations such as:



```text

ML-KEM encapsulation and decapsulation

ML-DSA signing and verification

Hybrid handshake simulation

Hybrid certificate signing and validation

```



\---



\## 14. Recommended Safe Usage



Recommended usage pattern:



```text

Use standard mode for development.

Use Docker PQC mode for PQC experiments.

Keep generated keys out of Git.

Do not expose the API publicly.

Do not use generated certificates in production.

Review cryptographic changes carefully.

```



\---



\## 15. Production Readiness Statement



This project is not production-ready.



A production PKI or hybrid PKI system would require:



```text

Formal threat model

Professional cryptographic review

Secure CA hierarchy

Offline root CA

HSM-backed private keys

Strong access control

Certificate policy documents

Audit logging

Secure revocation infrastructure

Compliance validation

Secure deployment architecture

Incident response procedures

```



Hybrid-PKI-Lab is a learning and experimentation environment.



\---



\## 16. Summary



The security model can be summarized as:



```text

Safe for education and experimentation.

Not safe for production deployment.

Classical PKI works in standard mode.

Real PQC works in Docker PQC mode.

Hybrid validation should prefer hybrid-strict.

Generated cryptographic artifacts must stay out of GitHub.

```



The project intentionally prioritizes:



```text

Clarity

Reproducibility

Fallback safety

Educational value

PQC experimentation

```



