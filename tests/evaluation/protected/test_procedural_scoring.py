from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    AssessmentSource,
    CriterionAssessment,
    CriterionDisposition,
    MixedScoreConfiguration,
    score_mixed,
    score_procedural,
)

from .contracts import mixed_contract, procedural_contract
from .fixtures import assessment


def test_human_assessments_cannot_bypass_deterministic_predicates() -> None:
    with pytest.raises(ValueError):
        score_procedural(
            procedural_contract(),
            (
                assessment(
                    "required-state",
                    CriterionDisposition.SATISFIED,
                    AssessmentSource.HUMAN_ADJUDICATION,
                    review_id="arbitrary-review",
                ),
                assessment(
                    "prohibited-action",
                    CriterionDisposition.NOT_SATISFIED,
                    AssessmentSource.HUMAN_ADJUDICATION,
                    review_id="arbitrary-review",
                ),
            ),
        )


def test_deterministic_assessment_binds_the_executed_predicate() -> None:
    with pytest.raises(ValueError, match="predicate"):
        score_procedural(
            procedural_contract(),
            (
                CriterionAssessment(
                    schema_version=1,
                    assessment_id="missing-predicate-binding",
                    criterion_id="required-state",
                    disposition=CriterionDisposition.SATISFIED,
                    source=AssessmentSource.DETERMINISTIC,
                    assessor_id="deterministic-runner",
                ),
                assessment("prohibited-action", CriterionDisposition.NOT_SATISFIED),
            ),
        )


def test_procedural_score_requires_required_success_and_clear_prohibited_criteria() -> None:
    contract = procedural_contract()
    success = score_procedural(
        contract,
        (
            assessment("required-state", CriterionDisposition.SATISFIED),
            assessment("prohibited-action", CriterionDisposition.NOT_SATISFIED),
        ),
    )
    assert success.success is True
    assert success.score == 1.0
    failure = score_procedural(
        contract,
        (
            assessment("required-state", CriterionDisposition.NOT_SATISFIED),
            assessment("prohibited-action", CriterionDisposition.NOT_SATISFIED),
        ),
    )
    assert failure.success is False
    assert failure.score == 0.0
    with pytest.raises(ValueError, match="unresolved"):
        score_procedural(
            contract,
            (
                assessment("required-state", CriterionDisposition.UNRESOLVED),
                assessment("prohibited-action", CriterionDisposition.NOT_SATISFIED),
            ),
        )


def test_mixed_hard_gate_is_non_compensable_and_points_are_explicit() -> None:
    contract = mixed_contract()
    hard_gate_failure = score_mixed(
        contract,
        (
            assessment("required-state", CriterionDisposition.NOT_SATISFIED),
            assessment("prohibited-action", CriterionDisposition.NOT_SATISFIED),
            assessment("semantic-point", CriterionDisposition.SATISFIED),
        ),
    )
    assert hard_gate_failure.hard_gate_failed is True
    assert hard_gate_failure.score == 0.0
    full = score_mixed(
        contract,
        (
            assessment("required-state", CriterionDisposition.SATISFIED),
            assessment("prohibited-action", CriterionDisposition.NOT_SATISFIED),
            assessment("semantic-point", CriterionDisposition.SATISFIED),
        ),
    )
    assert full.score == 1.0
    with pytest.raises(ValueError):
        MixedScoreConfiguration(
            schema_version=1,
            primary_hard_gate_criterion_ids=("required-state",),
            point_table={},
            positive_maximum=2.0,
        )
