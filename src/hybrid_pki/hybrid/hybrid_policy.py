from enum import StrEnum


class HybridValidationPolicy(StrEnum):
    """
    Supported hybrid certificate validation policies.
    """

    CLASSICAL_ONLY = "classical-only"
    PQC_ONLY = "pqc-only"
    HYBRID_STRICT = "hybrid-strict"
    HYBRID_FALLBACK = "hybrid-fallback"


def explain_policy(policy: HybridValidationPolicy) -> str:
    """
    Return a human-readable explanation for a hybrid validation policy.
    """
    explanations = {
        HybridValidationPolicy.CLASSICAL_ONLY: (
            "Accept the certificate only if the classical signature is valid."
        ),
        HybridValidationPolicy.PQC_ONLY: (
            "Accept the certificate only if the PQC signature is valid."
        ),
        HybridValidationPolicy.HYBRID_STRICT: (
            "Accept the certificate only if both classical and PQC signatures "
            "are valid."
        ),
        HybridValidationPolicy.HYBRID_FALLBACK: (
            "Accept the certificate if at least one signature is valid."
        ),
    }

    return explanations[policy]


def evaluate_policy(
    policy: HybridValidationPolicy,
    classical_valid: bool,
    pqc_valid: bool,
) -> bool:
    """
    Evaluate a hybrid validation policy.
    """
    if policy == HybridValidationPolicy.CLASSICAL_ONLY:
        return classical_valid

    if policy == HybridValidationPolicy.PQC_ONLY:
        return pqc_valid

    if policy == HybridValidationPolicy.HYBRID_STRICT:
        return classical_valid and pqc_valid

    if policy == HybridValidationPolicy.HYBRID_FALLBACK:
        return classical_valid or pqc_valid

    return False
