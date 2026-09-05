from __future__ import annotations

from thesis_bench.evaluation import calibration_summary
from thesis_bench.evaluation.protected import (
    AssessmentSource,
    CriterionDisposition,
    HumanReviewRoute,
    validate_human_adjudication,
)
from thesis_bench.evaluation.rubrics import RatingRecord, adjudicate_ratings

from .fixtures import assessment, knowledge_contract


def test_calibrated_human_adjudication_resolves_an_atomic_semantic_criterion() -> None:
    calibration = calibration_summary(
        tuple((f"family-{index}", "criterion-a", 1, 1) for index in range(1, 5)),
        draws=10,
    )
    ratings = tuple(
        RatingRecord(
            schema_version=1,
            rating_id=f"rating-{rater}",
            rater_pseudonym=f"rater-{rater}",
            randomized_response_id="response-1",
            criterion_id="claim-a",
            value=1,
            rubric_version="rubric-v1",
            rated_at="2026-09-05T10:00:00Z",
            independent=True,
            blinded=True,
        )
        for rater in ("a", "b")
    )
    adjudication = adjudicate_ratings(
        ratings,
        criterion_kind="binary",
        rationale=None,
        adjudication_id="adjudication-claim-a",
    )
    resolved = validate_human_adjudication(
        knowledge_contract(),
        assessment(
            "claim-a",
            CriterionDisposition.SATISFIED,
            AssessmentSource.HUMAN_ADJUDICATION,
            review_id=adjudication.adjudication_id,
        ),
        calibration=calibration,
        adjudication=adjudication,
    )
    assert resolved.review_route == HumanReviewRoute.ADJUDICATION
    assert resolved.adjudication_id == adjudication.adjudication_id
