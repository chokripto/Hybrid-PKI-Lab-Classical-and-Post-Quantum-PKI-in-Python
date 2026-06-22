from __future__ import annotations

from dataclasses import dataclass

from hybrid_pki.hybrid.hybrid_certificate import (
    HybridCertificate,
    is_hybrid_certificate_time_valid,
)
from hybrid_pki.hybrid.hybrid_policy import (
    HybridValidationPolicy,
    evaluate_policy,
)
from hybrid_pki.hybrid.hybrid_signatures import verify_hybrid_certificate_signatures


@dataclass(frozen=True)
class HybridValidationResult:
    """
    Result of hybrid certificate validation.
    """

    valid: bool
    policy: str
    classical_signature_valid: bool
    pqc_signature_valid: bool
    time_valid: bool
    reason: str


def validate_hybrid_certificate(
    certificate: HybridCertificate,
    classical_ca_public_key,
    pqc_ca_public_key: bytes,
    policy: HybridValidationPolicy = HybridValidationPolicy.HYBRID_STRICT,
) -> HybridValidationResult:
    """
    Validate a hybrid certificate according to a policy.
    """
    time_valid = is_hybrid_certificate_time_valid(certificate)

    if not time_valid:
        return HybridValidationResult(
            valid=False,
            policy=policy.value,
            classical_signature_valid=False,
            pqc_signature_valid=False,
            time_valid=False,
            reason="certificate is outside its validity period",
        )

    classical_valid, pqc_valid = verify_hybrid_certificate_signatures(
        certificate=certificate,
        classical_ca_public_key=classical_ca_public_key,
        pqc_ca_public_key=pqc_ca_public_key,
    )

    accepted = evaluate_policy(
        policy=policy,
        classical_valid=classical_valid,
        pqc_valid=pqc_valid,
    )

    if accepted:
        reason = "hybrid certificate accepted"
    else:
        reason = "hybrid certificate rejected by validation policy"

    return HybridValidationResult(
        valid=accepted,
        policy=policy.value,
        classical_signature_valid=classical_valid,
        pqc_signature_valid=pqc_valid,
        time_valid=time_valid,
        reason=reason,
    )
