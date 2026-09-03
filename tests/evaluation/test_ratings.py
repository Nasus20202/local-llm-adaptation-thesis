from __future__ import annotations

from pathlib import Path

import pytest

from thesis_bench.evaluation import (
    AppendOnlyAdjudicationStore,
    RatingRecord,
    RubricCriterion,
    adjudicate_ratings,
    import_rating,
    validate_rubric,
)


def test_rubric_requires_atomic_three_level_anchors_and_separate_binary_labels() -> None:
    valid = RubricCriterion(
        schema_version=1,
        criterion_id="correctness",
        kind="ordinal",
        anchors={
            0: "no required claim is supported",
            1: "some required claims are supported",
            2: "all required claims are supported",
        },
        critical=False,
        atomic=True,
    )
    assert validate_rubric((valid,)) == (valid,)

    with pytest.raises(ValueError):
        validate_rubric((valid.model_copy(update={"anchors": {0: "vague", 1: "partly"}}),))
    with pytest.raises(ValueError):
        validate_rubric((valid.model_copy(update={"atomic": False}),))
    with pytest.raises(ValueError, match="critical criteria must be binary"):
        validate_rubric((valid.model_copy(update={"critical": True}),))


def test_blinded_ratings_require_independence_and_adjudication_is_append_only(
    tmp_path: Path,
) -> None:
    raw = {
        "schema_version": 1,
        "rating_id": "rating-1",
        "rater_pseudonym": "rater-a",
        "randomized_response_id": "response-1",
        "criterion_id": "correctness",
        "value": 2,
        "rubric_version": "rubric-v1",
        "rated_at": "2026-09-03T10:00:00Z",
        "independent": True,
        "blinded": True,
    }
    rating = import_rating(raw)
    assert isinstance(rating, RatingRecord)
    with pytest.raises(ValueError):
        import_rating(raw | {"rating_id": "rating-bad-time", "rated_at": "not-a-time"})
    with pytest.raises(ValueError, match="rubric"):
        import_rating(
            raw | {"rating_id": "rating-out-of-anchor", "value": 3},
            rubric=(
                RubricCriterion(
                    schema_version=1,
                    criterion_id="correctness",
                    kind="ordinal",
                    anchors={0: "no", 1: "partial", 2: "yes"},
                    critical=False,
                    atomic=True,
                ),
            ),
        )
    with pytest.raises(ValueError):
        import_rating(raw | {"rating_id": "rating-unblinded", "blinded": False})
    with pytest.raises(ValueError):
        import_rating(raw | {"rating_id": "rating-condition", "condition_label": "B0"})

    other = import_rating(raw | {"rating_id": "rating-2", "rater_pseudonym": "rater-b", "value": 0})
    unresolved = adjudicate_ratings(
        (rating, other),
        criterion_kind="ordinal",
        rationale=None,
    )
    assert unresolved.resolved is False
    assert unresolved.labels == (2, 0)
    assert unresolved.sensitivity_flag is True
    with pytest.raises(ValueError, match="distinct"):
        adjudicate_ratings(
            (rating, rating.model_copy(update={"rating_id": "rating-3"})),
            criterion_kind="ordinal",
            rationale=None,
        )

    store = AppendOnlyAdjudicationStore(tmp_path)
    store.append(unresolved)
    with pytest.raises(ValueError, match="collision"):
        store.append(unresolved)
