\# Contributing to Hybrid-PKI-Lab



Thank you for your interest in contributing to \*\*Hybrid-PKI-Lab\*\*.



This project is an educational and experimental lab for classical PKI, post-quantum cryptography and hybrid PKI migration.



The project follows this strategy:



```text

Standard mode:

Usable without liboqs and without Docker.



Docker PQC mode:

Full post-quantum functionality with liboqs through Docker.

```



\---



\## 1. Project Goals



Hybrid-PKI-Lab aims to demonstrate:



\* Classical PKI concepts

\* Post-quantum cryptography integration

\* Hybrid certificate models

\* Hybrid validation policies

\* Hybrid X25519 + ML-KEM handshakes

\* Classical and PQC benchmarks

\* Safe fallback when PQC dependencies are unavailable



The project is for education, research and experimentation.



It is not intended to be used as a production CA.



\---



\## 2. Development Setup



\### 2.1 Clone the repository



```bash

git clone https://github.com/chokripto/Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python.git

cd Hybrid-PKI-Lab-Classical-and-Post-Quantum-PKI-in-Python

```



\---



\### 2.2 Create a virtual environment



On Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



On Linux or macOS:



```bash

python -m venv venv

source venv/bin/activate

```



\---



\### 2.3 Install dependencies



```bash

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -e .

```



For development tools:



```bash

pip install black ruff pytest pytest-cov

```



\---



\## 3. Standard Development Mode



Standard mode disables OQS and does not require `liboqs`.



On Windows PowerShell:



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

```



Run tests:



```powershell

pytest -v

```



Expected result:



```text

passed + skipped

```



The skipped tests are the real PQC tests that require `liboqs`.



\---



\## 4. Docker PQC Mode



Use Docker PQC mode to run real post-quantum cryptography features.



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



Run real PQC tests:



```powershell

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests

```



\---



\## 5. Code Quality



Before opening a pull request or pushing changes, run:



```powershell

python -m black src tests examples benchmarks

python -m ruff check src tests examples benchmarks --fix

pytest -v

```



Recommended full local workflow:



```powershell

.\\venv\\Scripts\\Activate.ps1

$env:HYBRID\_PKI\_DISABLE\_OQS="1"



python -m black src tests examples benchmarks

python -m ruff check src tests examples benchmarks --fix

pytest -v

git status

```



\---



\## 6. Testing Strategy



The project uses two testing modes.



\### Standard tests



Used for:



\* Local development

\* GitHub Actions

\* Fast feedback

\* Regression testing



Standard tests run with:



```text

HYBRID\_PKI\_DISABLE\_OQS=1

```



\### Docker PQC tests



Used for:



\* Real ML-KEM validation

\* Real ML-DSA validation

\* Hybrid certificate signing tests

\* Hybrid X25519 + ML-KEM handshake tests



Command:



```powershell

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests

```



\---



\## 7. What Not to Commit



Do not commit generated files or secrets.



Never commit:



```text

certs/

logs/

benchmarks/results/\*.json

venv/

\_\_pycache\_\_/

\*.pyc

\*.egg-info/

.env

```



Generated files may include:



\* Private keys

\* Public keys

\* Certificates

\* CSRs

\* CRLs

\* Hybrid certificate JSON files

\* Benchmark output

\* Runtime logs



Before committing, always run:



```powershell

git status

```



Verify that no generated cryptographic artifacts are staged.



\---



\## 8. Commit Message Style



Use clear commit messages.



Examples:



```text

Add hybrid handshake tests

Fix OQS fallback handling

Add Docker PQC documentation

Improve benchmark output format

Update API usage documentation

```



Avoid vague messages such as:



```text

fix

update

changes

final

```



\---



\## 9. Pull Request Checklist



Before submitting a pull request, verify:



```text

Code is formatted with Black.

Ruff passes.

Tests pass in standard mode.

Generated files are not committed.

Documentation is updated if behavior changed.

Docker PQC mode is tested if PQC behavior changed.

```



Recommended commands:



```powershell

python -m black src tests examples benchmarks

python -m ruff check src tests examples benchmarks --fix

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

pytest -v

git status

```



\---



\## 10. Documentation Contributions



Documentation improvements are welcome.



Useful documentation areas:



```text

API usage examples

Docker PQC setup

Troubleshooting

Architecture diagrams

Security limitations

Demo scenarios

Benchmark explanations

```



Documentation files are located under:



```text

docs/

```



\---



\## 11. Security Contributions



Security-related contributions are welcome, especially:



```text

Better validation checks

Improved revocation handling

Threat model documentation

Downgrade attack demonstrations

Secure key storage abstractions

Additional tests for failure cases

```



However, this project remains educational and experimental.



Do not submit production claims unless the system has received appropriate cryptographic and operational review.



\---



\## 12. Reporting Security Issues



If you find a security issue, do not expose private keys, generated certificates or sensitive local artifacts in public issues.



Provide:



```text

Clear description

Steps to reproduce

Expected behavior

Actual behavior

Affected module

Suggested fix if available

```



Do not include real secrets.



\---



\## 13. Development Philosophy



The project follows this design philosophy:



```text

Simple by default.

PQC optional.

Docker for real liboqs execution.

Safe fallback when PQC is unavailable.

Clear documentation for learning and demos.

```



Contributions should preserve this strategy.



