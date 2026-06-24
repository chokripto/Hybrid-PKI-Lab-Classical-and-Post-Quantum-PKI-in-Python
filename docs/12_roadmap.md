\# Project Roadmap



This document describes the current status and future roadmap of \*\*Hybrid-PKI-Lab\*\*.



Hybrid-PKI-Lab is an educational and experimental project for classical PKI, post-quantum cryptography and hybrid PKI migration.



\---



\## 1. Current Status



The project currently supports two execution modes:



```text

Standard mode:

Usable without liboqs and without Docker.



Docker PQC mode:

Full post-quantum functionality with liboqs through Docker.

```



Current project status:



| Area                             | Status      |

| -------------------------------- | ----------- |

| Classical PKI modules            | Completed   |

| Classical PKI API                | Completed   |

| PQC provider fallback            | Completed   |

| ML-KEM wrapper                   | Completed   |

| ML-DSA wrapper                   | Completed   |

| Hybrid certificate model         | Completed   |

| Hybrid validation policies       | Completed   |

| Hybrid X25519 + ML-KEM handshake | Completed   |

| Docker PQC environment           | Completed   |

| Benchmark scripts                | Completed   |

| Benchmark API endpoints          | Completed   |

| GitHub Actions tests             | Completed   |

| Lint workflow                    | Completed   |

| Security workflow                | Completed   |

| Documentation                    | In progress |



\---



\## 2. Completed Features



\### 2.1 Classical PKI



Implemented features:



```text

Root CA generation

Intermediate CA generation

Server certificate issuance

Certificate signing request support

Certificate chain validation

Certificate revocation simulation

PEM and DER serialization

RSA support

ECDSA support

Ed25519 support

```



\---



\### 2.2 Post-Quantum Cryptography



Implemented features:



```text

Optional liboqs-python provider

Safe OQS fallback

ML-KEM key generation

ML-KEM encapsulation and decapsulation

ML-DSA key generation

ML-DSA signing and verification

PQC serialization helpers

Docker-based liboqs environment

```



\---



\### 2.3 Hybrid PKI



Implemented features:



```text

Hybrid certificate data model

Classical + PQC public key binding

Classical + PQC signature support

Hybrid validation policies

Hybrid strict validation mode

Hybrid fallback validation mode

Hybrid X25519 + ML-KEM handshake

Hybrid shared secret derivation with HKDF

```



Hybrid strict validation rule:



$$

valid\_{hybrid} = valid\_{classical} \\land valid\_{PQC}

$$



Hybrid shared secret derivation:



$$

secret\_{hybrid} = HKDF(secret\_{classical} \\parallel secret\_{PQC})

$$



\---



\### 2.4 API



Implemented API areas:



```text

General health endpoints

Classical PKI endpoints

PQC status endpoint

Hybrid PKI endpoints

Benchmark endpoints

Swagger UI integration

```



\---



\### 2.5 Docker



Implemented Docker support:



```text

Standard Docker mode

Docker PQC mode

Docker PQC test mode

liboqs build inside Docker

liboqs-python validation inside Docker

Port mapping for standard and PQC API modes

```



\---



\### 2.6 CI/CD



Implemented GitHub Actions workflows:



```text

Tests

Lint

Security

```



The default CI mode disables OQS:



```text

HYBRID\_PKI\_DISABLE\_OQS=1

```



This keeps CI fast, stable and independent from native PQC dependencies.



\---



\## 3. Short-Term Roadmap



The following improvements are planned as short-term enhancements.



\---



\### 3.1 Improve Documentation



Planned documentation improvements:



```text

Add screenshots of Swagger UI

Add diagrams for API workflows

Add command examples for Windows and Linux

Add troubleshooting guide

Add FAQ section

```



Priority:



```text

High

```



Reason:



```text

Good documentation makes the project easier to understand and easier to demonstrate.

```



\---



\### 3.2 Add More API Tests



Planned API tests:



```text

Test /health

Test /classical/status

Test /pqc/status in disabled mode

Test /hybrid/status

Test /benchmarks/status

Test benchmark result reading

```



Priority:



```text

High

```



Reason:



```text

API tests improve confidence and protect against regressions.

```



\---



\### 3.3 Add More Classical PKI Tests



Planned classical tests:



```text

Test RSA root CA creation

Test ECDSA intermediate CA creation

Test Ed25519 key generation

Test certificate chain validation failure

Test expired certificate rejection

Test hostname mismatch rejection

Test revoked certificate rejection

```



Priority:



```text

Medium

```



\---



\### 3.4 Improve Benchmark Output



Planned benchmark improvements:



```text

Add average duration

Add minimum duration

Add maximum duration

Add standard deviation

Add operation count

Add machine metadata

Add JSON schema for results

```



Priority:



```text

Medium

```



\---



\## 4. Medium-Term Roadmap



The following items can be added after the core project is stable.



\---



\### 4.1 Add CLI Interface



A command-line interface could expose common operations without Swagger UI.



Possible commands:



```text

hybrid-pki classical init-root

hybrid-pki classical init-intermediate

hybrid-pki classical issue-server

hybrid-pki classical verify-server

hybrid-pki pqc status

hybrid-pki hybrid handshake

hybrid-pki benchmarks run

```



Priority:



```text

Medium

```



Benefits:



```text

Better automation

Better scripting

Better GitHub demo experience

```



\---



\### 4.2 Add Configuration File Support



Possible configuration files:



```text

config/default.yml

config/development.yml

config/pqc.yml

```



Configurable values:



```text

Certificate paths

Default algorithms

Default validity periods

Hybrid validation policy

Benchmark iterations

API host and port

```



Priority:



```text

Medium

```



\---



\### 4.3 Add More Hybrid Policies



Possible future policies:



```text

hybrid-strict

hybrid-fallback

classical-transition

pqc-preferred

pqc-required

```



Priority:



```text

Low

```



\---



\### 4.4 Add Threat Model Documentation



Possible threat model topics:



```text

CA key compromise

Certificate forgery

Downgrade attacks

PQC provider failure

API exposure

Generated secrets leakage

Benchmark data leakage

```



Priority:



```text

Medium

```



\---



\## 5. Long-Term Roadmap



These features are more advanced and would require deeper design work.



\---



\### 5.1 Certificate Transparency Simulation



Possible features:



```text

Append-only certificate log

Signed certificate timestamps

Log verification

Merkle tree simulation

Mis-issued certificate detection

```



Priority:



```text

Low

```



\---



\### 5.2 OCSP Responder Simulation



Possible features:



```text

OCSP-like API endpoint

Certificate status responses

Signed status response

Revocation freshness simulation

```



Priority:



```text

Low

```



\---



\### 5.3 HSM or KMS Integration Simulation



Possible features:



```text

Abstract key storage interface

Local file key store

Mock HSM key store

Cloud KMS-style key store simulation

```



Priority:



```text

Low

```



\---



\### 5.4 Web Dashboard



Possible dashboard features:



```text

CA status

Issued certificate list

Revoked certificate list

PQC provider status

Hybrid certificate status

Benchmark charts

```



Priority:



```text

Low

```



\---



\### 5.5 Real TLS Integration Experiment



Possible experimental features:



```text

Generate TLS-compatible classical certificates

Compare classical TLS and hybrid handshake simulation

Explore hybrid TLS design concepts

Document migration considerations

```



Priority:



```text

Research

```



\---



\## 6. Research Directions



Potential research-oriented extensions:



```text

Hybrid certificate encoding formats

Hybrid trust anchor models

Downgrade-resistant negotiation

Algorithm agility in PKI

Classical-to-PQC migration strategies

Benchmarking PQC overhead

Operational impact of hybrid PKI

```



These topics can be explored through documentation, experiments and prototype modules.



\---



\## 7. Non-Goals



The following are not current goals of the project:



```text

Production CA deployment

Public Internet certificate authority

Production TLS stack replacement

Commercial HSM integration

Compliance certification

Formal verification

Side-channel analysis

```



The project remains an educational and experimental lab.



\---



\## 8. Contribution Ideas



Possible contributions:



```text

Add more tests

Improve documentation

Add diagrams

Improve benchmark output

Add CLI commands

Add new examples

Improve Docker build performance

Add troubleshooting documentation

```



Before contributing, contributors should understand that generated cryptographic artifacts should not be committed.



\---



\## 9. Roadmap Summary



Current design philosophy:



```text

Simple by default.

Optional PQC support.

Docker for real liboqs execution.

Safe fallback when PQC is unavailable.

Clear documentation for learning and demos.

```



Main next priorities:



```text

1\. Improve documentation and examples.

2\. Add more API and PKI tests.

3\. Improve benchmark reporting.

4\. Add CLI support.

5\. Expand security and threat model documentation.

```



