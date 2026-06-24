\# API Usage Guide



This guide explains how to use the Hybrid-PKI-Lab API through Swagger UI.



The project supports two API execution modes:



1\. \*\*Standard API mode\*\* without `liboqs`.

2\. \*\*Docker PQC API mode\*\* with real `liboqs` support.



\---



\## 1. Start the API



\### 1.1 Standard API mode



Use this mode for normal development.



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

python -m uvicorn hybrid\_pki.api.main:app --host 127.0.0.1 --port 8000 --reload

```



Open Swagger UI:



```text

http://127.0.0.1:8000/docs

```



In this mode:



\* Classical PKI endpoints work.

\* API endpoints work.

\* PQC-dependent endpoints return a clean unavailable status or skip PQC operations.

\* No Docker is required.

\* No `liboqs` installation is required.



\---



\### 1.2 Docker PQC API mode



Use this mode for real post-quantum cryptography experiments.



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



In this mode:



\* `liboqs-python` is available.

\* ML-KEM works.

\* ML-DSA works.

\* Hybrid X25519 + ML-KEM handshake works.

\* PQC benchmarks can run.



\---



\## 2. General API checks



\### 2.1 Root endpoint



Endpoint:



```text

GET /

```



Expected result:



```json

{

&#x20; "project": "Hybrid PKI Lab",

&#x20; "status": "running",

&#x20; "message": "API is working successfully"

}

```



\---



\### 2.2 Health endpoint



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



\---



\## 3. Classical PKI workflow



This workflow demonstrates a classical PKI hierarchy:



```text

Root CA -> Intermediate CA -> Server Certificate

```



Use Swagger UI and execute the following endpoints in order.



\---



\### 3.1 Check classical PKI status



Endpoint:



```text

GET /classical/status

```



Expected result before initialization:



```json

{

&#x20; "classical\_module": "available"

}

```



\---



\### 3.2 Create a Root CA



Endpoint:



```text

POST /classical/ca/root/init

```



Example request body:



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



Generated files are stored under:



```text

certs/root/

```



\---



\### 3.3 Create an Intermediate CA



Endpoint:



```text

POST /classical/ca/intermediate/init

```



Example request body:



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



Generated files are stored under:



```text

certs/intermediate/

```



\---



\### 3.4 Issue a server certificate



Endpoint:



```text

POST /classical/certificates/server/issue

```



Example request body:



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



Generated files are stored under:



```text

certs/issued/

```



\---



\### 3.5 Verify a server certificate



Endpoint:



```text

POST /classical/certificates/server/verify

```



Example request body:



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



\### 3.6 Revoke a server certificate



Endpoint:



```text

POST /classical/certificates/server/revoke

```



Example request body:



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



\### 3.7 List revoked certificates



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



The list content depends on the certificates revoked during the demo.



\---



\## 4. PQC status



\### 4.1 Standard mode result



Endpoint:



```text

GET /pqc/status

```



When running without `liboqs`, the result should indicate that PQC is unavailable or disabled.



Example:



```json

{

&#x20; "available": false,

&#x20; "message": "OQS support is disabled by HYBRID\_PKI\_DISABLE\_OQS."

}

```



\---



\### 4.2 Docker PQC mode result



Endpoint:



```text

GET /pqc/status

```



When running through Docker PQC mode, the expected result is:



```json

{

&#x20; "available": true,

&#x20; "message": "liboqs-python is available."

}

```



This confirms that `liboqs-python` is correctly loaded inside Docker.



\---



\## 5. Hybrid PKI workflow



The hybrid workflow requires Docker PQC mode for real post-quantum operations.



\---



\### 5.1 Check hybrid status



Endpoint:



```text

GET /hybrid/status

```



Expected result in Docker PQC mode:



```json

{

&#x20; "hybrid\_module": "available",

&#x20; "pqc\_provider": {

&#x20;   "available": true,

&#x20;   "message": "liboqs-python is available."

&#x20; }

}

```



\---



\### 5.2 Create demo hybrid CA material



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



Generated files are stored under:



```text

certs/hybrid/

```



\---



\### 5.3 Verify hybrid CA material



Run again:



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



\---



\### 5.4 Create a demo hybrid certificate



Endpoint:



```text

POST /hybrid/certificates/create-demo

```



Example request body:



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



\### 5.5 Verify a demo hybrid certificate



Endpoint:



```text

POST /hybrid/certificates/verify-demo

```



Example request body:



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



\---



\### 5.6 Simulate a real hybrid handshake



Endpoint:



```text

POST /hybrid/handshake/simulate

```



Example request body:



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



This confirms that the classical and post-quantum shared secrets were combined correctly.



\---



\## 6. Benchmark API workflow



The benchmark API allows running benchmark scripts from Swagger.



\---



\### 6.1 Check benchmark status



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



\### 6.2 Run key generation benchmarks



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



Results are written to:



```text

benchmarks/results/keygen\_results.json

```



\---



\### 6.3 Run signature benchmarks



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



Results are written to:



```text

benchmarks/results/signature\_results.json

```



\---



\### 6.4 Run handshake benchmarks



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



Results are written to:



```text

benchmarks/results/handshake\_results.json

```



\---



\### 6.5 Read benchmark results



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



The exact values depend on the machine and execution mode.



\---



\## 7. Recommended testing order



For a full API demonstration, use this order:



```text

1\. GET  /health

2\. GET  /classical/status

3\. POST /classical/ca/root/init

4\. POST /classical/ca/intermediate/init

5\. POST /classical/certificates/server/issue

6\. POST /classical/certificates/server/verify

7\. GET  /pqc/status

8\. GET  /hybrid/status

9\. POST /hybrid/ca/create-demo

10\. POST /hybrid/certificates/create-demo

11\. POST /hybrid/certificates/verify-demo

12\. POST /hybrid/handshake/simulate

13\. GET  /benchmarks/status

14\. POST /benchmarks/run-keygen

15\. POST /benchmarks/run-signatures

16\. POST /benchmarks/run-handshake

17\. GET  /benchmarks/results

```



\---



\## 8. Important security note



This API is designed for education, experimentation and research.



Do not expose it directly to the public Internet.



Generated material may include:



\* Private keys

\* Public keys

\* Certificates

\* Hybrid certificate JSON files

\* Benchmark results

\* Logs



Generated files under the following directories should not be committed to GitHub:



```text

certs/

logs/

benchmarks/results/

```



\---



\## 9. Stop the API



\### Standard mode



Use:



```text

CTRL + C

```



\### Docker PQC mode



Use:



```text

CTRL + C

```



or:



```powershell

docker compose --profile pqc down

```



