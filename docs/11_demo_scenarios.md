\# Demo Scenarios



This document provides practical demo scenarios for \*\*Hybrid-PKI-Lab\*\*.



The goal is to help users demonstrate the project step by step through Swagger UI, Docker PQC mode and benchmark scripts.



The project supports two modes:



```text

Standard mode:

Usable without liboqs and without Docker.



Docker PQC mode:

Full post-quantum functionality with liboqs through Docker.

```



\---



\## 1. Demo Overview



Hybrid-PKI-Lab can be demonstrated through the following scenarios:



```text

1\. Classical PKI demo

2\. PQC provider status demo

3\. Hybrid CA material demo

4\. Hybrid certificate demo

5\. Hybrid handshake demo

6\. Benchmark demo

7\. Security limitations demo

```



Recommended demo order:



```text

1\. Start the API

2\. Verify health status

3\. Run the Classical PKI workflow

4\. Check PQC provider status

5\. Run the Hybrid PKI workflow

6\. Simulate the hybrid handshake

7\. Run benchmarks

8\. Explain security limitations

```



\---



\## 2. Demo Environment



\### 2.1 Standard Mode



Use this mode for classical PKI demonstrations.



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

python -m uvicorn hybrid\_pki.api.main:app --host 127.0.0.1 --port 8000 --reload

```



Open Swagger UI:



```text

http://127.0.0.1:8000/docs

```



\---



\### 2.2 Docker PQC Mode



Use this mode for real post-quantum cryptography demonstrations.



```powershell

docker compose --profile pqc build hybrid-pki-pqc

docker compose --profile pqc up hybrid-pki-pqc

```



Open Swagger UI:



```text

http://127.0.0.1:8001/docs

```



\---



\## 3. Demo 1: API Health Check



Purpose:



```text

Show that the API is running correctly.

```



Endpoint:



```text

GET /health

```



Expected result:



```json

{

&#x20; "status": "ok"

}

```



This is the first endpoint to test during any demo.



\---



\## 4. Demo 2: Classical PKI Workflow



Purpose:



```text

Demonstrate a traditional PKI hierarchy:

Root CA -> Intermediate CA -> Server Certificate

```



Execution mode:



```text

Standard mode or Docker PQC mode

```



\---



\### 4.1 Check Classical Module Status



Endpoint:



```text

GET /classical/status

```



Expected result:



```json

{

&#x20; "classical\_module": "available"

}

```



\---



\### 4.2 Create Root CA



Endpoint:



```text

POST /classical/ca/root/init

```



Example body:



```json

{

&#x20; "common\_name": "Hybrid PKI Lab Root CA",

&#x20; "organization": "Hybrid PKI Lab",

&#x20; "country": "MA",

&#x20; "algorithm": "RSA",

&#x20; "days\_valid": 3650

}

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Root CA created successfully"

}

```



Generated files:



```text

certs/root/

```



\---



\### 4.3 Create Intermediate CA



Endpoint:



```text

POST /classical/ca/intermediate/init

```



Example body:



```json

{

&#x20; "common\_name": "Hybrid PKI Lab Intermediate CA",

&#x20; "organization": "Hybrid PKI Lab",

&#x20; "country": "MA",

&#x20; "algorithm": "ECDSA",

&#x20; "days\_valid": 1825

}

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Intermediate CA created successfully"

}

```



Generated files:



```text

certs/intermediate/

```



\---



\### 4.4 Issue Server Certificate



Endpoint:



```text

POST /classical/certificates/server/issue

```



Example body:



```json

{

&#x20; "common\_name": "server.example.com",

&#x20; "organization": "Hybrid PKI Lab",

&#x20; "country": "MA",

&#x20; "dns\_names": \[

&#x20;   "server.example.com",

&#x20;   "www.server.example.com"

&#x20; ],

&#x20; "algorithm": "ECDSA",

&#x20; "days\_valid": 365

}

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Server certificate issued successfully"

}

```



Generated files:



```text

certs/issued/

```



\---



\### 4.5 Verify Server Certificate



Endpoint:



```text

POST /classical/certificates/server/verify

```



Example body:



```json

{

&#x20; "hostname": "server.example.com"

}

```



Expected result:



```json

{

&#x20; "valid": true

}

```



\---



\### 4.6 Revoke Server Certificate



Endpoint:



```text

POST /classical/certificates/server/revoke

```



Example body:



```json

{

&#x20; "reason": "keyCompromise"

}

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Certificate revoked successfully"

}

```



\---



\### 4.7 List Revoked Certificates



Endpoint:



```text

GET /classical/certificates/revoked

```



Expected result:



```json

{

&#x20; "revoked\_certificates": \[]

}

```



The exact result depends on certificates revoked during the demo.



\---



\## 5. Demo 3: PQC Provider Status



Purpose:



```text

Show the difference between standard mode and Docker PQC mode.

```



Endpoint:



```text

GET /pqc/status

```



\---



\### 5.1 Standard Mode Result



When `HYBRID\_PKI\_DISABLE\_OQS=1`, expected result:



```json

{

&#x20; "available": false,

&#x20; "message": "OQS support is disabled by HYBRID\_PKI\_DISABLE\_OQS."

}

```



This demonstrates that the project can run safely without `liboqs`.



\---



\### 5.2 Docker PQC Mode Result



In Docker PQC mode, expected result:



```json

{

&#x20; "available": true,

&#x20; "message": "liboqs-python is available."

}

```



This demonstrates that real PQC support is available through Docker.



\---



\## 6. Demo 4: Hybrid CA Material



Purpose:



```text

Generate classical and PQC material for the hybrid CA demo.

```



Execution mode:



```text

Docker PQC mode recommended

```



Endpoint:



```text

POST /hybrid/ca/create-demo

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Hybrid demo CA material created successfully"

}

```



Then run:



```text

GET /hybrid/status

```



Expected CA material status:



```json

{

&#x20; "ca\_material": {

&#x20;   "classical\_private\_key\_exists": true,

&#x20;   "classical\_public\_key\_exists": true,

&#x20;   "pqc\_private\_key\_exists": true,

&#x20;   "pqc\_public\_key\_exists": true

&#x20; }

}

```



Generated files:



```text

certs/hybrid/

```



Generated material should not be committed to GitHub.



\---



\## 7. Demo 5: Hybrid Certificate



Purpose:



```text

Demonstrate a certificate containing both classical and post-quantum material.

```



Execution mode:



```text

Docker PQC mode

```



\---



\### 7.1 Create Hybrid Certificate



Endpoint:



```text

POST /hybrid/certificates/create-demo

```



Example body:



```json

{

&#x20; "subject": "CN=hybrid.example.com,O=Hybrid PKI Lab,C=MA",

&#x20; "issuer": "CN=Hybrid Root CA,O=Hybrid PKI Lab,C=MA",

&#x20; "classical\_algorithm": "ECDSA-P256",

&#x20; "pqc\_signature\_algorithm": "ML-DSA-65",

&#x20; "days\_valid": 365

}

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Hybrid demo certificate created successfully",

&#x20; "has\_classical\_signature": true,

&#x20; "has\_pqc\_signature": true

}

```



\---



\### 7.2 Verify Hybrid Certificate



Endpoint:



```text

POST /hybrid/certificates/verify-demo

```



Example body:



```json

{

&#x20; "certificate\_path": "certs/hybrid/hybrid.example.com\_certificate.json",

&#x20; "policy": "hybrid-strict"

}

```



Expected result:



```json

{

&#x20; "valid": true,

&#x20; "policy": "hybrid-strict",

&#x20; "classical\_signature\_valid": true,

&#x20; "pqc\_signature\_valid": true,

&#x20; "time\_valid": true

}

```



Important policy:



```text

hybrid-strict

```



Hybrid validation rule:



$$

valid\_{hybrid} = valid\_{classical} \\land valid\_{PQC}

$$



\---



\## 8. Demo 6: Hybrid Handshake



Purpose:



```text

Demonstrate a real hybrid key exchange using X25519 and ML-KEM.

```



Execution mode:



```text

Docker PQC mode

```



Endpoint:



```text

POST /hybrid/handshake/simulate

```



Example body:



```json

{

&#x20; "pqc\_algorithm": "ML-KEM-768"

}

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "algorithm": {

&#x20;   "classical": "X25519",

&#x20;   "pqc": "ML-KEM-768",

&#x20;   "kdf": "HKDF-SHA256"

&#x20; },

&#x20; "secrets\_match": true

}

```



The most important field is:



```json

{

&#x20; "secrets\_match": true

}

```



This confirms that the client and server derived the same hybrid shared secret.



Hybrid secret derivation:



$$

secret\_{hybrid} = HKDF(secret\_{classical} \\parallel secret\_{PQC})

$$



\---



\## 9. Demo 7: Benchmarks



Purpose:



```text

Compare classical and post-quantum operations.

```



Execution mode:



```text

Standard mode for classical benchmarks.

Docker PQC mode for real PQC benchmarks.

```



\---



\### 9.1 Benchmark Status



Endpoint:



```text

GET /benchmarks/status

```



Expected result:



```json

{

&#x20; "status": "available"

}

```



\---



\### 9.2 Run Key Generation Benchmark



Endpoint:



```text

POST /benchmarks/run-keygen

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Key generation benchmark completed"

}

```



Output file:



```text

benchmarks/results/keygen\_results.json

```



\---



\### 9.3 Run Signature Benchmark



Endpoint:



```text

POST /benchmarks/run-signatures

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Signature benchmark completed"

}

```



Output file:



```text

benchmarks/results/signature\_results.json

```



\---



\### 9.4 Run Handshake Benchmark



Endpoint:



```text

POST /benchmarks/run-handshake

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "message": "Handshake benchmark completed"

}

```



Output file:



```text

benchmarks/results/handshake\_results.json

```



\---



\### 9.5 Read Benchmark Results



Endpoint:



```text

GET /benchmarks/results

```



Expected result:



```json

{

&#x20; "status": "success",

&#x20; "results": {

&#x20;   "keygen": {},

&#x20;   "signatures": {},

&#x20;   "handshake": {}

&#x20; }

}

```



The exact values depend on the machine and the execution mode.



Generated benchmark JSON files should not be committed to GitHub.



\---



\## 10. Demo 8: Security Limitations



Purpose:



```text

Explain that this project is educational and not production-ready.

```



Important points to mention:



```text

The API is for local experiments.

Generated private keys are stored locally.

No HSM is used.

No authentication or authorization is implemented.

No production OCSP service is implemented.

No production CA ceremony is implemented.

Docker mode is for reproducible PQC experiments, not production deployment.

```



Recommended reference:



```text

docs/10\_security\_model\_and\_limitations.md

```



\---



\## 11. Full Recommended Demo Script



For a complete live demo, use the following order:



```text

1\. Open README.md and explain the two execution modes.

2\. Start Standard API mode.

3\. Open http://127.0.0.1:8000/docs.

4\. Run GET /health.

5\. Run GET /classical/status.

6\. Create Root CA.

7\. Create Intermediate CA.

8\. Issue server certificate.

9\. Verify server certificate.

10\. Stop the Standard API.

11\. Start Docker PQC mode.

12\. Open http://127.0.0.1:8001/docs.

13\. Run GET /pqc/status.

14\. Run GET /hybrid/status.

15\. Run POST /hybrid/ca/create-demo.

16\. Run POST /hybrid/certificates/create-demo.

17\. Run POST /hybrid/certificates/verify-demo.

18\. Run POST /hybrid/handshake/simulate.

19\. Run benchmark endpoints.

20\. Explain security limitations.

```



\---



\## 12. Cleanup After Demo



Stop the API:



```text

CTRL + C

```



Stop Docker PQC services:



```powershell

docker compose --profile pqc down

```



Check Git status:



```powershell

git status

```



Do not commit generated files from:



```text

certs/

logs/

benchmarks/results/

```



\---



\## 13. Demo Summary



This project can be demonstrated as:



```text

A classical PKI lab.

A PQC integration lab.

A hybrid PKI migration lab.

A Docker-based liboqs environment.

A benchmark and experimentation platform.

```



The most important successful demo outputs are:



```text

GET /health -> status ok

GET /pqc/status -> available true in Docker PQC mode

POST /hybrid/handshake/simulate -> secrets\_match true

pytest -v -> passed + skipped in standard mode

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests -> real PQC tests pass

```



