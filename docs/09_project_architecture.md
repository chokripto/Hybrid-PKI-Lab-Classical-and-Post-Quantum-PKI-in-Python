\# Project Architecture



This document describes the architecture of \*\*Hybrid-PKI-Lab\*\*, including the Python modules, API layer, execution modes, testing strategy and benchmark design.



\---



\## 1. Overview



Hybrid-PKI-Lab is an educational and experimental Public Key Infrastructure project.



It combines three main areas:



```text id="pnl5ct"

1\. Classical PKI

2\. Post-Quantum Cryptography

3\. Hybrid Classical + Post-Quantum PKI

```



The project is designed to demonstrate how traditional PKI systems can evolve toward hybrid post-quantum architectures.



The main design goal is:



```text id="aymn8t"

Usable by default without liboqs or Docker.

Fully PQC-capable through Docker with liboqs.

```



\---



\## 2. High-Level Architecture



```text id="2xha5w"

User / Developer

&#x20;     |

&#x20;     v

FastAPI REST API

&#x20;     |

&#x20;     +--------------------+

&#x20;     |                    |

&#x20;     v                    v

Classical PKI Modules      PQC Provider Layer

&#x20;     |                    |

&#x20;     v                    v

X.509 / RSA / ECDSA        liboqs-python or fallback

Ed25519 / CRL

&#x20;     |

&#x20;     +--------------------+

&#x20;     |

&#x20;     v

Hybrid PKI Modules

&#x20;     |

&#x20;     v

Hybrid Certificates

Hybrid Signatures

Hybrid Handshake

Hybrid Validation

```



The API layer exposes the internal modules through Swagger UI, while the test and benchmark layers validate and compare the behavior of the implemented components.



\---



\## 3. Execution Modes



The project supports two execution modes.



\---



\### 3.1 Standard Mode



Standard mode works without `liboqs` and without Docker.



It is used for:



\* Normal development

\* GitHub Actions

\* Classical PKI testing

\* Fast and stable CI

\* Users who do not want native PQC dependencies



In this mode:



```text id="lwo0sr"

Classical PKI        available

FastAPI API          available

Benchmarks           partially available

PQC operations       skipped or reported unavailable

Hybrid PQC features  skipped or reported unavailable

```



The environment variable used for this mode is:



```powershell id="rmc60n"

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

```



\---



\### 3.2 Docker PQC Mode



Docker PQC mode builds and installs `liboqs` inside a Linux Docker container.



It is used for:



\* Real ML-KEM operations

\* Real ML-DSA operations

\* Hybrid X25519 + ML-KEM handshake

\* Hybrid certificate experiments

\* PQC benchmarks



In this mode:



```text id="u0qlpn"

Classical PKI        available

FastAPI API          available

ML-KEM               available

ML-DSA               available

Hybrid handshake     available

PQC benchmarks       available

```



Main command:



```powershell id="im0t7r"

docker compose --profile pqc up hybrid-pki-pqc

```



Swagger UI:



```text id="mv4sz2"

http://127.0.0.1:8001/docs

```



\---



\## 4. Source Code Layout



The main source code is located under:



```text id="wigfy1"

src/hybrid\_pki/

```



Recommended module view:



```text id="o0qp2d"

src/hybrid\_pki/

├── api/

├── classical/

├── pqc/

└── hybrid/

```



\---



\## 5. Classical PKI Architecture



The classical PKI layer is responsible for traditional PKI operations.



Typical responsibilities:



```text id="m6hceu"

Key generation

Root CA creation

Intermediate CA creation

CSR creation

Server certificate issuance

Certificate chain validation

Certificate revocation

PEM / DER serialization

```



Typical module layout:



```text id="rnix8p"

src/hybrid\_pki/classical/

├── keygen.py

├── ca.py

├── certificate.py

├── chain\_validation.py

└── revocation.py

```



\---



\### 5.1 Classical PKI Flow



```text id="oxll6v"

Generate Root CA key

&#x20;       |

&#x20;       v

Create Root CA certificate

&#x20;       |

&#x20;       v

Generate Intermediate CA key

&#x20;       |

&#x20;       v

Create Intermediate CA certificate

&#x20;       |

&#x20;       v

Generate server key

&#x20;       |

&#x20;       v

Issue server certificate

&#x20;       |

&#x20;       v

Validate certificate chain

&#x20;       |

&#x20;       v

Optionally revoke certificate

```



\---



\### 5.2 Classical Algorithms



The classical layer supports:



| Purpose      | Algorithms                    |

| ------------ | ----------------------------- |

| Signatures   | RSA-PSS, ECDSA P-256, Ed25519 |

| Key exchange | X25519, ECDH                  |

| Hashing      | SHA-256, SHA-384              |

| KDF          | HKDF                          |



\---



\## 6. PQC Architecture



The PQC layer provides access to post-quantum cryptography operations.



Typical module layout:



```text id="0510f6"

src/hybrid\_pki/pqc/

├── oqs\_provider.py

├── ml\_kem.py

├── ml\_dsa.py

└── pqc\_serialization.py

```



\---



\### 6.1 OQS Provider Layer



The `oqs\_provider.py` module is the compatibility layer between the project and `liboqs-python`.



It has three main goals:



```text id="7nbv9e"

1\. Detect whether liboqs-python is available.

2\. Avoid crashing if liboqs is missing or broken.

3\. Allow OQS to be disabled for standard tests and GitHub Actions.

```



Main behavior:



```text id="ik53ri"

If HYBRID\_PKI\_DISABLE\_OQS=1:

&#x20;   report OQS unavailable quickly



If liboqs-python is installed and working:

&#x20;   enable PQC features



If liboqs-python is missing or broken:

&#x20;   report OQS unavailable cleanly

```



This design avoids making `liboqs` a hard dependency.



\---



\### 6.2 ML-KEM Module



The ML-KEM module provides key encapsulation functionality.



Typical operations:



```text id="z7a9cu"

Generate ML-KEM key pair

Encapsulate shared secret

Decapsulate shared secret

Serialize public and secret keys

```



Default algorithm:



```text id="yqf24k"

ML-KEM-768

```



\---



\### 6.3 ML-DSA Module



The ML-DSA module provides digital signature functionality.



Typical operations:



```text id="eevjf1"

Generate ML-DSA key pair

Sign message

Verify signature

Serialize public and secret keys

```



Default algorithm:



```text id="bd2lgz"

ML-DSA-65

```



\---



\## 7. Hybrid PKI Architecture



The hybrid layer combines classical cryptography with PQC.



Typical module layout:



```text id="6nd9tv"

src/hybrid\_pki/hybrid/

├── hybrid\_policy.py

├── hybrid\_certificate.py

├── hybrid\_signatures.py

├── hybrid\_validation.py

└── hybrid\_handshake.py

```



\---



\## 8. Hybrid Certificate Model



A hybrid certificate contains both classical and post-quantum information.



Conceptual structure:



```text id="o6q4wu"

HybridCertificate:

&#x20;   subject

&#x20;   issuer

&#x20;   classical\_public\_key

&#x20;   pqc\_public\_key

&#x20;   validity\_period

&#x20;   classical\_signature

&#x20;   pqc\_signature

&#x20;   metadata

```



The goal is to demonstrate a migration path from classical certificates to hybrid certificates.



\---



\### 8.1 Hybrid Validation Rule



Recommended policy:



```text id="mthwzf"

hybrid-strict

```



The validation rule is:



$$

valid\_{hybrid} = valid\_{classical} \\land valid\_{PQC}

$$



This means that the hybrid certificate is valid only if both classical and PQC validation succeed.



\---



\### 8.2 Hybrid Shared Secret Derivation



The hybrid handshake combines a classical shared secret and a PQC shared secret.



$$

secret\_{hybrid} = HKDF(secret\_{classical} \\parallel secret\_{PQC})

$$



Where:



```text id="kz6c42"

secret\_classical = X25519 shared secret

secret\_PQC       = ML-KEM shared secret

HKDF             = key derivation function

```



\---



\## 9. Hybrid Handshake Architecture



The hybrid handshake combines:



```text id="xim98j"

Classical key exchange: X25519

PQC key encapsulation:  ML-KEM

KDF:                    HKDF-SHA256

```



Flow:



```text id="adnmge"

Server generates X25519 key pair

Server generates ML-KEM key pair

&#x20;       |

&#x20;       v

Client receives server public keys

&#x20;       |

&#x20;       v

Client performs X25519 exchange

Client encapsulates ML-KEM shared secret

&#x20;       |

&#x20;       v

Client derives hybrid secret with HKDF

&#x20;       |

&#x20;       v

Server decapsulates ML-KEM secret

Server performs X25519 exchange

&#x20;       |

&#x20;       v

Server derives hybrid secret with HKDF

&#x20;       |

&#x20;       v

Both sides compare derived secrets

```



Expected result:



```json id="hz9psu"

{

&#x20; "secrets\_match": true

}

```



\---



\## 10. Hybrid Validation Policies



The project supports multiple validation policies.



| Policy            | Description                                      |

| ----------------- | ------------------------------------------------ |

| `classical-only`  | Accepts classical validation only                |

| `pqc-only`        | Accepts PQC validation only                      |

| `hybrid-strict`   | Requires both classical and PQC validation       |

| `hybrid-fallback` | Allows fallback behavior for migration scenarios |



Recommended policy for security experiments:



```text id="07o9i6"

hybrid-strict

```



\---



\## 11. API Architecture



The API layer is implemented with FastAPI.



Typical module layout:



```text id="4qiino"

src/hybrid\_pki/api/

├── main.py

├── routes\_classical.py

├── routes\_pqc.py

├── routes\_hybrid.py

└── routes\_benchmarks.py

```



\---



\### 11.1 API Responsibilities



The API provides:



```text id="dqmwgg"

Health checks

Classical PKI operations

PQC provider status

Hybrid PKI operations

Benchmark execution

Swagger UI documentation

```



Main Swagger URLs:



```text id="alv69g"

Standard mode:

http://127.0.0.1:8000/docs



Docker PQC mode:

http://127.0.0.1:8001/docs

```



\---



\### 11.2 API Route Groups



| Route Group       | Purpose                        |

| ----------------- | ------------------------------ |

| `/` and `/health` | General API status             |

| `/classical/\*`    | Classical PKI operations       |

| `/pqc/\*`          | PQC provider status            |

| `/hybrid/\*`       | Hybrid PKI operations          |

| `/benchmarks/\*`   | Benchmark status and execution |



\---



\## 12. Benchmark Architecture



Benchmark scripts are located under:



```text id="2ehiyx"

benchmarks/

```



Typical layout:



```text id="g81sxh"

benchmarks/

├── benchmark\_keygen.py

├── benchmark\_signatures.py

├── benchmark\_handshake.py

└── results/

```



\---



\### 12.1 Benchmark Categories



| Benchmark                 | Purpose                                             |

| ------------------------- | --------------------------------------------------- |

| `benchmark\_keygen.py`     | Measures classical and PQC key generation           |

| `benchmark\_signatures.py` | Measures classical and PQC signing and verification |

| `benchmark\_handshake.py`  | Measures classical and hybrid handshake operations  |



Generated results are written to:



```text id="n1fka4"

benchmarks/results/

```



Generated JSON files should not be committed to GitHub.



\---



\## 13. Testing Architecture



Tests are located under:



```text id="jfcn83"

tests/

```



The test strategy is split into two modes.



\---



\### 13.1 Standard Tests



Standard tests run without requiring `liboqs`.



They are used for:



```text id="nrnm6s"

Local development

GitHub Actions

Regression testing

Fast feedback

```



The environment variable is:



```powershell id="md0hw1"

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

```



Expected result:



```text id="spcdlt"

passed + skipped

```



The skipped tests are PQC tests requiring real `liboqs`.



\---



\### 13.2 Docker PQC Tests



Docker PQC tests run with real `liboqs`.



Command:



```powershell id="gde2f2"

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests

```



These tests validate real PQC functionality such as:



```text id="k529xg"

ML-KEM encapsulation / decapsulation

ML-DSA signing / verification

Hybrid certificate signing

Hybrid X25519 + ML-KEM handshake

```



\---



\## 14. CI Architecture



GitHub Actions are used for continuous integration.



Main workflows:



```text id="li34a5"

Tests

Lint

Security

```



The default CI mode disables OQS:



```text id="dybcrz"

HYBRID\_PKI\_DISABLE\_OQS=1

```



This ensures:



```text id="fkf0r3"

Fast CI

Stable tests

No native liboqs requirement

No Docker requirement for basic validation

```



\---



\## 15. Storage Architecture



Generated runtime material is stored under:



```text id="7yoo8j"

certs/

logs/

benchmarks/results/

```



These directories may contain:



```text id="hm1jvq"

Private keys

Public keys

Certificates

Hybrid certificate JSON files

Benchmark JSON files

Runtime logs

```



These files should not be committed to GitHub.



The repository should keep source code, tests and documentation, not generated cryptographic artifacts.



\---



\## 16. Security Considerations



This project is educational and experimental.



It should not be used directly in production.



A production-grade PKI system would require:



```text id="kvc1s7"

Hardware-backed key management

Secure CA ceremony

Formal certificate policies

Auditing and logging

Access control

HSM or KMS integration

Secure revocation infrastructure

Compliance review

Cryptographic review

Threat modeling

```



\---



\## 17. Design Summary



The project follows this design philosophy:



```text id="4af489"

Simple by default.

Advanced when needed.

Safe fallback when PQC is unavailable.

Real PQC support through Docker.

```



The final architecture is:



```text id="h2904h"

Standard mode:

\- No liboqs required

\- No Docker required

\- Fast tests

\- Stable GitHub Actions



Docker PQC mode:

\- liboqs built inside Docker

\- Real ML-KEM

\- Real ML-DSA

\- Real hybrid handshake

\- Real PQC benchmarks

```



