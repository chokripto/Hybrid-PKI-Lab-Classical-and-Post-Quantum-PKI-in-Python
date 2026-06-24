\# Troubleshooting Guide



This document lists common issues and fixes for \*\*Hybrid-PKI-Lab\*\*.



The project supports two execution modes:



```text

Standard mode:

Usable without liboqs and without Docker.



Docker PQC mode:

Full post-quantum functionality with liboqs through Docker.

```



\---



\## 1. Virtual environment is not activated



\### Problem



Commands such as:



```powershell

python -m black src tests examples benchmarks

python -m ruff check src tests examples benchmarks --fix

pytest -v

```



fail with errors like:



```text

No module named black

No module named ruff

No module named pytest

```



\### Cause



The Python virtual environment is not activated.



\### Fix



From the project root:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



Then verify:



```powershell

python -c "import sys; print(sys.executable)"

```



Expected path:



```text

C:\\Users\\pc\\Desktop\\hybrid-pki-lab\\venv\\Scripts\\python.exe

```



\---



\## 2. PowerShell blocks venv activation



\### Problem



PowerShell refuses to run:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### Cause



PowerShell execution policy blocks scripts.



\### Fix



Run:



```powershell

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```



Then retry:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\---



\## 3. Dependencies are missing



\### Problem



The project fails because packages are missing.



\### Fix



With the virtual environment activated:



```powershell

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -e .

```



For development tools:



```powershell

pip install black ruff pytest pytest-cov

```



\---



\## 4. pytest is slow after installing liboqs-python



\### Problem



After installing `liboqs-python`, running tests becomes very slow.



\### Cause



`liboqs-python` may try to find or build native `liboqs` shared libraries during import.



\### Fix



Use standard mode for normal testing:



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

pytest -v

```



This disables OQS checks and makes tests fast.



Real PQC tests should be run through Docker PQC mode:



```powershell

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests

```



\---



\## 5. liboqs-python is unavailable



\### Problem



The API returns:



```json

{

&#x20; "available": false,

&#x20; "message": "liboqs-python is not installed correctly..."

}

```



\### Cause



`liboqs-python` is missing, broken, or unable to load the native `liboqs` shared library.



\### Fix



For normal development, use standard mode:



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

pytest -v

```



For real PQC features, use Docker PQC mode:



```powershell

docker compose --profile pqc build hybrid-pki-pqc

docker compose --profile pqc up hybrid-pki-pqc

```



Then open:



```text

http://127.0.0.1:8001/docs

```



And test:



```text

GET /pqc/status

```



Expected result:



```json

{

&#x20; "available": true,

&#x20; "message": "liboqs-python is available."

}

```



\---



\## 6. Docker daemon is not running



\### Problem



Docker commands fail with:



```text

failed to connect to the docker API

check if the daemon is running

```



\### Cause



Docker Desktop is not running.



\### Fix



1\. Open Docker Desktop.

2\. Wait until Docker Engine is running.

3\. Verify:



```powershell

docker version

docker info

```



Then retry:



```powershell

docker compose --profile pqc build hybrid-pki-pqc

```



\---



\## 7. Docker is using Windows containers



\### Problem



Docker build fails with Linux image or package errors.



\### Cause



Docker Desktop may be using Windows containers instead of Linux containers.



\### Fix



Switch Docker Desktop to Linux containers.



The project uses:



```dockerfile

FROM python:3.12-slim

```



This requires Linux containers.



\---



\## 8. docker-compose.yml YAML error



\### Problem



Docker Compose reports an error such as:



```text

mapping key "build" already defined

```



\### Cause



A service block was pasted with incorrect indentation.



\### Fix



All services must be aligned under `services:` like this:



```yaml

services:

&#x20; hybrid-pki-api:

&#x20;   build:

&#x20;     context: .

&#x20;     dockerfile: Dockerfile



&#x20; hybrid-pki-pqc:

&#x20;   build:

&#x20;     context: .

&#x20;     dockerfile: Dockerfile.pqc

```



Validate the file with:



```powershell

docker compose config

```



If the command prints the configuration without errors, the YAML file is valid.



\---



\## 9. Port already in use



\### Problem



The API does not start because the port is already used.



\### Common ports



```text

Standard API: 8000

Docker PQC API: 8001

```



\### Fix



Stop the existing API with:



```text

CTRL + C

```



Or stop Docker services:



```powershell

docker compose down

docker compose --profile pqc down

```



Then restart the desired mode.



\---



\## 10. Swagger UI is not reachable



\### Problem



The browser cannot open Swagger UI.



\### Standard mode URL



```text

http://127.0.0.1:8000/docs

```



\### Docker PQC mode URL



```text

http://127.0.0.1:8001/docs

```



\### Fix



Verify the API is running.



For standard mode:



```powershell

python -m uvicorn hybrid\_pki.api.main:app --host 127.0.0.1 --port 8000 --reload

```



For Docker PQC mode:



```powershell

docker compose --profile pqc up hybrid-pki-pqc

```



\---



\## 11. Git status shows certs/



\### Problem



`git status` shows:



```text

certs/

```



\### Cause



The API or tests generated certificates and keys.



\### Fix



Generated certificates and keys should not be committed.



The `.gitignore` should include:



```gitignore

certs/

```



Then check:



```powershell

git status

```



Expected result:



```text

nothing to commit, working tree clean

```



\---



\## 12. Git status shows benchmark result JSON files



\### Problem



`git status` shows files such as:



```text

benchmarks/results/keygen\_results.json

benchmarks/results/signature\_results.json

benchmarks/results/handshake\_results.json

```



\### Cause



Benchmarks generated local result files.



\### Fix



Generated benchmark results should not be committed.



The `.gitignore` should include:



```gitignore

benchmarks/results/\*.json

!benchmarks/results/.gitkeep

```



\---



\## 13. Git status shows \*\*pycache\*\* or .egg-info



\### Problem



`git status` shows generated Python files:



```text

\_\_pycache\_\_/

\*.pyc

\*.egg-info/

```



\### Fix



The `.gitignore` should include:



```gitignore

\_\_pycache\_\_/

\*.py\[cod]

\*.egg-info/

.pytest\_cache/

.ruff\_cache/

.mypy\_cache/

```



If files were already tracked, remove them from Git tracking:



```powershell

git rm --cached -r src/hybrid\_pki\_lab.egg-info

git rm --cached -r src/hybrid\_pki/api/\_\_pycache\_\_

```



Then commit the cleanup.



\---



\## 14. GitHub Actions fail but local tests pass



\### Problem



Local tests pass, but GitHub Actions fail.



\### Fix checklist



Run locally:



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

python -m black src tests examples benchmarks

python -m ruff check src tests examples benchmarks --fix

pytest -v

```



Then check:



```powershell

git status

```



Commit and push any corrections:



```powershell

git add .

git commit -m "Fix CI issues"

git push

```



If GitHub Actions still fail, open the failed workflow and inspect the red error lines.



\---



\## 15. Docker PQC build is slow



\### Problem



Building Docker PQC takes several minutes.



\### Cause



The Docker image compiles `liboqs` from source.



\### Fix



This is expected.



Use Docker layer caching by avoiding unnecessary changes to:



```text

Dockerfile.pqc

requirements.txt

pyproject.toml

```



Rebuild only when needed:



```powershell

docker compose --profile pqc build hybrid-pki-pqc

```



\---



\## 16. Recommended clean workflow



For normal development:



```powershell

.\\venv\\Scripts\\Activate.ps1

$env:HYBRID\_PKI\_DISABLE\_OQS="1"



python -m black src tests examples benchmarks

python -m ruff check src tests examples benchmarks --fix

pytest -v



git status

git add .

git commit -m "Your commit message"

git push

```



For real PQC validation:



```powershell

docker compose --profile pqc build hybrid-pki-pqc

docker compose --profile pqc up hybrid-pki-pqc

docker compose --profile pqc-test up --build hybrid-pki-pqc-tests

```



\---



\## 17. Summary



Most issues fall into one of these categories:



```text

Virtual environment not activated

Dependencies missing

OQS disabled or unavailable

Docker Desktop not running

YAML indentation error

Generated files showing in Git status

Wrong API port

```



Recommended default mode:



```text

Use standard mode for development and GitHub Actions.

Use Docker PQC mode for real post-quantum experiments.

```



