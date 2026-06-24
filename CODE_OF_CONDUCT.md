\# Code of Conduct



\## 1. Purpose



Hybrid-PKI-Lab is an educational and experimental cybersecurity project focused on classical PKI, post-quantum cryptography and hybrid PKI migration.



The goal of this Code of Conduct is to keep the project respectful, constructive and safe for contributors, learners and researchers.



\---



\## 2. Expected Behavior



Participants are expected to:



\* Be respectful and professional.

\* Use welcoming and inclusive language.

\* Give constructive feedback.

\* Respect different levels of experience.

\* Focus discussions on technical quality, security and learning.

\* Report bugs and security concerns responsibly.

\* Avoid sharing real secrets, private keys, credentials or sensitive information.



\---



\## 3. Unacceptable Behavior



Unacceptable behavior includes:



\* Harassment, insults or personal attacks.

\* Discriminatory language or behavior.

\* Publishing private information without permission.

\* Sharing real private keys, credentials, tokens or secrets.

\* Encouraging unsafe production use of experimental code.

\* Deliberately submitting malicious code.

\* Disruptive or disrespectful communication.

\* Misrepresenting the project as production-ready.



\---



\## 4. Security-Specific Rules



Because this is a cybersecurity and cryptography project, contributors must follow additional safety rules.



Do not submit or publish:



```text

Private keys

Generated production certificates

Real credentials

API tokens

.env files

Sensitive logs

Personal data

Exploit code unrelated to the educational scope of the project

```



Generated lab artifacts should remain local and should not be committed to GitHub.



Examples of generated files that should not be committed:



```text

certs/

logs/

benchmarks/results/\*.json

venv/

\_\_pycache\_\_/

\*.egg-info/

```



\---



\## 5. Responsible Security Reporting



If you find a security issue, report it responsibly.



A good security report should include:



```text

Clear description

Affected component

Steps to reproduce

Expected behavior

Actual behavior

Potential impact

Suggested fix if available

```



Do not include real secrets or sensitive third-party data in public issues.



\---



\## 6. Project Scope Reminder



Hybrid-PKI-Lab is for:



\* Education

\* Research

\* Experimentation

\* Portfolio demonstration

\* Security engineering practice



Hybrid-PKI-Lab is not a production Certificate Authority and should not be used directly in production environments.



Production PKI systems require:



```text

Professional cryptographic review

Secure key management

HSM or KMS integration

Formal certificate policies

Audit logging

Access control

Secure revocation infrastructure

Operational procedures

Compliance review

```



\---



\## 7. Enforcement



Project maintainers may remove content, reject contributions or block participation if behavior violates this Code of Conduct.



The goal of enforcement is to protect the learning environment, the security of the project and the safety of contributors.



\---



\## 8. Good Contribution Culture



Good contributions include:



\* Clear bug reports

\* Reproducible test cases

\* Documentation improvements

\* Security-focused reviews

\* Better error handling

\* Safer defaults

\* More tests

\* Clear explanations of limitations



Contributors should preserve the project strategy:



```text

Simple by default.

PQC optional.

Docker for real liboqs execution.

Safe fallback when PQC is unavailable.

Clear documentation for learning and demos.

```



\---



\## 9. Summary



Be respectful.

Be constructive.

Do not share secrets.

Do not claim production readiness.

Keep the project useful for education, experimentation and responsible cybersecurity learning.



