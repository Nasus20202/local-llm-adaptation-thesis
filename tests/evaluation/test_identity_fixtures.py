from __future__ import annotations

import pytest

from tests.evaluation.fixtures import evaluate, fixtures, identities
from thesis_bench.evaluation import (
    DeterministicFixture,
    FixtureCategory,
    FixtureResult,
    build_evaluation_record,
    qualify_deterministic_evaluator,
)
from thesis_bench.records import DecisionStatus


def test_changed_evaluator_input_has_a_distinct_immutable_identity() -> None:
    first = identities()
    changed = identities(input_hash="f" * 64)
    assert first[2] != changed[2]
    first_evaluation = build_evaluation_record(*first)
    changed_evaluation = build_evaluation_record(
        *changed, derived_from=first_evaluation.evaluation_id
    )
    assert first_evaluation.evaluation_id != changed_evaluation.evaluation_id
    assert changed_evaluation.derived_from == first_evaluation.evaluation_id
    with pytest.raises(ValueError):
        first[2].content_sha256 = "f" * 64  # type: ignore[misc]


def test_deterministic_fixture_qualification_requires_all_classes_and_idempotence() -> None:
    qualification = qualify_deterministic_evaluator(fixtures(), evaluate, repeats=2)

    assert qualification.status == DecisionStatus.GO
    assert qualification.mismatches == ()
    assert qualification.rejected_ambiguous == ("fixture-ambiguous",)


def test_fixture_mismatch_blocks_qualification() -> None:
    def mismatching_evaluator(fixture: DeterministicFixture) -> FixtureResult:
        result = evaluate(fixture)
        if fixture.category == FixtureCategory.BOUNDARY:
            return result.__class__(
                schema_version=1, outcome="unexpected", reason="unexpected", substantive=True
            )
        return result

    qualification = qualify_deterministic_evaluator(fixtures(), mismatching_evaluator)
    assert qualification.status == DecisionStatus.AMEND
    assert "fixture-boundary" in qualification.mismatches
