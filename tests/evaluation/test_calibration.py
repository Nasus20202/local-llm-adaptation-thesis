from __future__ import annotations

import pytest

from thesis_bench.evaluation import (
    CalibrationStatus,
    adjacent_agreement,
    calibration_summary,
    exact_agreement,
    family_clustered_interval,
    krippendorff_alpha,
)


def test_agreement_statistics_and_seeded_family_interval_are_deterministic() -> None:
    pairs = ((0, 0), (1, 1), (2, 1), (2, 2))
    assert exact_agreement(pairs) == 0.75
    assert adjacent_agreement(pairs) == 1.0
    assert krippendorff_alpha(((0, 0), (1, 1), (2, 1), (2, 2)), level="ordinal") > 0.0

    observations = (("family-a", 0, 0), ("family-b", 1, 1), ("family-c", 2, 1))
    first = family_clustered_interval(
        observations,
        lambda rows: exact_agreement(tuple((a, b) for _, a, b in rows)),
        seed=7,
        draws=200,
    )
    second = family_clustered_interval(
        observations,
        lambda rows: exact_agreement(tuple((a, b) for _, a, b in rows)),
        seed=7,
        draws=200,
    )
    assert first == second
    assert 0.0 <= first[0] <= first[1] <= 1.0


def test_krippendorff_alpha_matches_nominal_and_ordinal_reference_values() -> None:
    units = ((0, 2), (0, 1), (0, 0), (1, 1))

    assert krippendorff_alpha(units, level="nominal") == pytest.approx(5 / 19)
    assert krippendorff_alpha(units, level="ordinal") == pytest.approx(-1 / 16)


def test_calibration_summary_reports_pooled_alpha_and_green_thresholds() -> None:
    observations = tuple(
        (f"family-{index}", criterion, value, value)
        for index, value in enumerate((0, 1, 2, 1), start=1)
        for criterion in ("correctness", "safety")
    )

    summary = calibration_summary(
        observations,
        critical_criteria=("safety",),
        seed=9,
        draws=100,
    )

    assert summary.status == CalibrationStatus.GO
    assert summary.alpha == 1.0
    assert summary.interval == (1.0, 1.0)
    assert summary.qualification_attempt == 1


def test_calibration_summary_pools_all_criteria_for_alpha() -> None:
    summary = calibration_summary(
        (
            ("family-1", "criterion-a", 0, 0),
            ("family-2", "criterion-a", 1, 1),
            ("family-1", "criterion-b", 0, 1),
            ("family-2", "criterion-b", 1, 0),
        ),
        seed=2,
        draws=100,
    )

    assert summary.alpha < 1.0


def test_calibration_requires_declared_critical_criteria_and_separates_primary_alpha() -> None:
    observations = (
        ("family-1", "primary", 0, 0),
        ("family-2", "primary", 1, 1),
        ("family-1", "critical", 0, 1),
        ("family-2", "critical", 1, 0),
    )

    summary = calibration_summary(observations, critical_criteria=("critical",), draws=100)

    assert summary.alpha == 1.0
    assert summary.critical_exact == {"critical": 0.0}
    assert summary.systematic_critical_disagreement is False
    assert summary.status == CalibrationStatus.AMEND
    with pytest.raises(ValueError, match="critical"):
        calibration_summary(observations[:2], critical_criteria=("critical",))


def test_systematic_critical_disagreement_requires_explicit_review_evidence() -> None:
    observations = (
        ("family-1", "primary", 0, 0),
        ("family-2", "primary", 1, 1),
        ("family-1", "critical", 0, 1),
        ("family-2", "critical", 1, 0),
        ("family-3", "critical", 0, 0),
        ("family-4", "critical", 1, 1),
    )

    summary = calibration_summary(
        observations,
        critical_criteria=("critical",),
        systematic_critical_disagreement=True,
        systematic_disagreement_reason="reviewed technical label conflict",
        draws=100,
    )

    assert summary.status == CalibrationStatus.STOP_DEFER
    assert summary.critical_exact == {"critical": 0.5}
    assert summary.systematic_disagreement_reason == "reviewed technical label conflict"


def test_critical_binary_exact_agreement_includes_the_ninety_percent_boundary() -> None:
    observations = tuple(
        [(f"family-{index}", "primary", 0, 0) for index in range(2)]
        + [(f"family-{index}", "critical", 1, 1 if index < 9 else 0) for index in range(10)]
    )

    summary = calibration_summary(
        observations,
        critical_criteria=("critical",),
        draws=100,
    )

    assert summary.critical_exact["critical"] == pytest.approx(0.9)


def test_second_non_green_calibration_attempt_is_red() -> None:
    observations = (
        ("family-1", "primary", 0, 1),
        ("family-2", "primary", 1, 0),
    )

    summary = calibration_summary(
        observations,
        qualification_attempt=2,
        draws=100,
    )

    assert summary.status == CalibrationStatus.STOP_DEFER


def test_calibration_boundary_decisions_are_explicit(monkeypatch: pytest.MonkeyPatch) -> None:
    observations = (
        ("family-1", "primary", 0, 0),
        ("family-2", "primary", 1, 1),
    )

    monkeypatch.setattr(
        "thesis_bench.evaluation.krippendorff_alpha", lambda *_args, **_kwargs: 0.80
    )
    monkeypatch.setattr(
        "thesis_bench.evaluation.family_clustered_interval",
        lambda *_args, **_kwargs: (0.67, 0.80),
    )
    assert calibration_summary(observations, draws=1).status == CalibrationStatus.GO

    monkeypatch.setattr(
        "thesis_bench.evaluation.krippendorff_alpha", lambda *_args, **_kwargs: 0.79
    )
    assert calibration_summary(observations, draws=1).status == CalibrationStatus.AMEND

    monkeypatch.setattr(
        "thesis_bench.evaluation.krippendorff_alpha", lambda *_args, **_kwargs: 0.67
    )
    assert calibration_summary(observations, draws=1).status == CalibrationStatus.AMEND

    monkeypatch.setattr(
        "thesis_bench.evaluation.krippendorff_alpha", lambda *_args, **_kwargs: 0.66
    )
    assert calibration_summary(observations, draws=1).status == CalibrationStatus.STOP_DEFER
