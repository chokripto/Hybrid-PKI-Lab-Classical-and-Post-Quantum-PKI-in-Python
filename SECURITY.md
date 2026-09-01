# Security Policy

## Scope

Hybrid PKI Lab is an educational research prototype, not a production CA, TLS stack, HSM integration or formally validated cryptographic product.

## Supported version

Security fixes are applied to the latest commit on `main`.

## Reporting a vulnerability

Do not publish an exploitable vulnerability in a public issue. Use GitHub private vulnerability reporting when available. Include the affected component, impact, preconditions, minimal reproduction and suggested mitigation. Never include real keys, credentials, personal data or third-party systems.

## Safety defaults

- Docker services bind to localhost.
- State-changing routes require `HYBRID_PKI_ENABLE_MUTATIONS=1`.
- `HYBRID_PKI_API_KEY` can protect enabled mutations.
- Generated key files use owner-only permissions where supported.
- Root CA initialization refuses silent overwrite.
- Real PQC integration uses pinned versions in Docker.

These controls reduce accidental exposure; they do not make the API suitable for an untrusted network.

## Out of scope

Documented limitations—pedagogical JSON certificates, unauthenticated key establishment and partial RFC 5280 validation—are not vulnerabilities unless a defect creates impact beyond the stated model.
