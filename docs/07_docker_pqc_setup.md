\# Docker PQC Setup



This project supports two execution modes:



1\. Standard mode without liboqs.

2\. Advanced PQC mode with liboqs through Docker.



The standard mode is recommended for normal development and GitHub Actions.

The Docker PQC mode is recommended for real post-quantum cryptography experiments.



\---



\## 1. Standard mode without liboqs



This mode does not require liboqs or Docker.



It supports:



\- Classical PKI

\- FastAPI API

\- Classical benchmarks

\- OQS fallback

\- Stable tests



Run:



```powershell

$env:HYBRID\_PKI\_DISABLE\_OQS="1"

pytest -v

