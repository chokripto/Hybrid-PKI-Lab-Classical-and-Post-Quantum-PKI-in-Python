import pytest

from hybrid_pki.hybrid.hybrid_policy import (
    HybridValidationPolicy,
    evaluate_policy,
    explain_policy,
)


@pytest.mark.parametrize(
    ("policy", "classical_valid", "pqc_valid", "expected"),
    [
        (HybridValidationPolicy.CLASSICAL_ONLY, True, True, True),
        (HybridValidationPolicy.CLASSICAL_ONLY, True, False, True),
        (HybridValidationPolicy.CLASSICAL_ONLY, False, True, False),
        (HybridValidationPolicy.CLASSICAL_ONLY, False, False, False),
        (HybridValidationPolicy.PQC_ONLY, True, True, True),
        (HybridValidationPolicy.PQC_ONLY, False, True, True),
        (HybridValidationPolicy.PQC_ONLY, True, False, False),
        (HybridValidationPolicy.PQC_ONLY, False, False, False),
        (HybridValidationPolicy.HYBRID_STRICT, True, True, True),
        (HybridValidationPolicy.HYBRID_STRICT, True, False, False),
        (HybridValidationPolicy.HYBRID_STRICT, False, True, False),
        (HybridValidationPolicy.HYBRID_STRICT, False, False, False),
        (HybridValidationPolicy.HYBRID_FALLBACK, True, True, True),
        (HybridValidationPolicy.HYBRID_FALLBACK, True, False, True),
        (HybridValidationPolicy.HYBRID_FALLBACK, False, True, True),
        (HybridValidationPolicy.HYBRID_FALLBACK, False, False, False),
    ],
)
def test_evaluate_policy_combinations(
    policy,
    classical_valid,
    pqc_valid,
    expected,
):
    result = evaluate_policy(
        policy=policy,
        classical_valid=classical_valid,
        pqc_valid=pqc_valid,
    )

    assert result is expected


@pytest.mark.parametrize(
    "policy",
    [
        HybridValidationPolicy.CLASSICAL_ONLY,
        HybridValidationPolicy.PQC_ONLY,
        HybridValidationPolicy.HYBRID_STRICT,
        HybridValidationPolicy.HYBRID_FALLBACK,
    ],
)
def test_explain_policy_returns_non_empty_text(policy):
    explanation = explain_policy(policy)

    assert isinstance(explanation, str)
    assert len(explanation) > 0


def test_hybrid_strict_requires_both_classical_and_pqc():
    assert (
        evaluate_policy(
            policy=HybridValidationPolicy.HYBRID_STRICT,
            classical_valid=True,
            pqc_valid=True,
        )
        is True
    )

    assert (
        evaluate_policy(
            policy=HybridValidationPolicy.HYBRID_STRICT,
            classical_valid=True,
            pqc_valid=False,
        )
        is False
    )

    assert (
        evaluate_policy(
            policy=HybridValidationPolicy.HYBRID_STRICT,
            classical_valid=False,
            pqc_valid=True,
        )
        is False
    )


def test_hybrid_fallback_accepts_at_least_one_valid_branch():
    assert (
        evaluate_policy(
            policy=HybridValidationPolicy.HYBRID_FALLBACK,
            classical_valid=True,
            pqc_valid=False,
        )
        is True
    )

    assert (
        evaluate_policy(
            policy=HybridValidationPolicy.HYBRID_FALLBACK,
            classical_valid=False,
            pqc_valid=True,
        )
        is True
    )

    assert (
        evaluate_policy(
            policy=HybridValidationPolicy.HYBRID_FALLBACK,
            classical_valid=False,
            pqc_valid=False,
        )
        is False
    )
