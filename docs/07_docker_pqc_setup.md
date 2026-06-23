# Docker PQC Setup

This project supports two execution modes:

1. **Standard mode**: works without `liboqs` and without Docker.
2. **Docker PQC mode**: enables real post-quantum cryptography through `liboqs`.

The standard mode is recommended for normal development and GitHub Actions.
The Docker PQC mode is recommended for real ML-KEM, ML-DSA, and hybrid PKI experiments.

---

## 1. Project strategy

The project is designed to be usable by default without requiring a complex post-quantum cryptography installation.

```text
Standard mode:
Usable without liboqs and without Docker.

Advanced mode:
Full post-quantum functionality with liboqs through Docker.
```

This keeps the project simple for most users while still supporting real post-quantum cryptography experiments.

---

## 2. Standard mode without liboqs

This mode is used for normal development and CI.

It supports:

* Classical PKI
* FastAPI API
* Classical benchmarks
* OQS fallback
* Stable tests

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

## 3. Docker PQC mode with liboqs

This mode builds `liboqs` inside a Linux Docker container.

It supports:

* ML-KEM
* ML-DSA
* Hybrid X25519 + ML-KEM handshake
* Hybrid certificate experiments
* PQC benchmarks

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

The API runs inside Docker on port `8000`, but it is exposed on the host machine through port `8001`.

---

## 4. Verify PQC availability

In Swagger, run:

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

You can also test it from PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/pqc/status
```

---

## 5. Verify hybrid module status

In Swagger, run:

```text
GET /hybrid/status
```

Expected result:

```json
{
  "hybrid_module": "available",
  "pqc_provider": {
    "available": true,
    "message": "liboqs-python is available."
  }
}
```

---

## 6. Create demo hybrid CA material

In Swagger, run:

```text
POST /hybrid/ca/create-demo
```

Then run again:

```text
GET /hybrid/status
```

Expected CA material status:

```json
{
  "classical_private_key_exists": true,
  "classical_public_key_exists": true,
  "pqc_private_key_exists": true,
  "pqc_public_key_exists": true
}
```

The generated material is stored under:

```text
certs/hybrid/
```

Generated certificates and keys should not be committed to GitHub.

---

## 7. Simulate a real hybrid handshake

In Swagger, run:

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

## 8. Run real PQC tests in Docker

Run:

```powershell
docker compose --profile pqc-test up --build hybrid-pki-pqc-tests
```

In this mode, tests that are skipped in standard mode should run with real `liboqs` support.

---

## 9. Run PQC benchmarks

Run:

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

## 10. Stop the Docker PQC API

If the API is running in the foreground, stop it with:

```text
CTRL + C
```

You can also stop the container with:

```powershell
docker compose --profile pqc down
```

---

## 11. Summary

```text
Standard mode:
- No liboqs required
- No Docker required
- Fast and stable tests
- Recommended for GitHub Actions

Docker PQC mode:
- liboqs built inside Docker
- Real ML-KEM support
- Real ML-DSA support
- Real hybrid handshake support
- Recommended for post-quantum experiments
```
