from __future__ import annotations

import pytest

from thesis_bench.evaluation import calibration_summary
from thesis_bench.evaluation.protected import (
    AssessmentSource,
    AuditSelection,
    CriterionDisposition,
    HumanReviewRoute,
    Language,
    TaskClass,
    audit_selection_identity,
    validate_human_adjudication,
    validate_primary_human_assessment,
)
from thesis_bench.evaluation.rubrics import RatingRecord, adjudicate_ratings
from thesis_bench.records import content_sha256

from .fixtures import assessment, knowledge_contract, semantic_knowledge_contract
from .judge_fixtures import judge_configuration


def test_calibrated_human_adjudication_resolves_an_atomic_semantic_criterion() -> None:
    calibration = calibration_summary(
        tuple((f"family-{index}", "claim-a", 1, 1) for index in range(1, 5)),
        draws=10,
        task_class=TaskClass.KNOWLEDGE,
        language=Language.EN,
        contract_id="evaluator-contract-1",
        contract_sha256="c" * 64,
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
        semantic_knowledge_contract(),
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
    with pytest.raises(ValueError, match="provenance"):
        validate_primary_human_assessment(
            semantic_knowledge_contract(),
            resolved.model_copy(update={"calibration_id": "unrelated-calibration"}),
            calibration=calibration,
            adjudication=adjudication,
        )
    policy = judge_configuration().audit_policy
    selection_fields = {
        "schema_version": 1,
        "selection_id": audit_selection_identity(
            policy.audit_policy_id,
            policy.membership_manifest_id,
            policy.membership_manifest_sha256,
            "response-1",
        ),
        "response_id": "response-1",
        "audit_policy_id": policy.audit_policy_id,
        "route": HumanReviewRoute.BLINDED_AUDIT,
        "selected_before_outcomes": True,
        "outcome_inspected": False,
        "membership_manifest_id": policy.membership_manifest_id,
        "membership_manifest_sha256": policy.membership_manifest_sha256,
        "membership_manifest_root_reference": policy.membership_manifest_root_reference,
    }
    audit_selection = AuditSelection(
        **selection_fields,
        selection_content_sha256=content_sha256(selection_fields),
    )
    with pytest.raises(ValueError, match="frozen selection"):
        validate_human_adjudication(
            semantic_knowledge_contract(),
            assessment(
                "claim-a",
                CriterionDisposition.SATISFIED,
                AssessmentSource.HUMAN_ADJUDICATION,
                review_id=adjudication.adjudication_id,
            ),
            calibration=calibration,
            adjudication=adjudication,
            review_route=HumanReviewRoute.BLINDED_AUDIT,
            audit_selection=audit_selection,
            response_id="response-1",
        )


def test_human_adjudication_cannot_bypass_an_applicable_deterministic_predicate() -> None:
    calibration = calibration_summary(
        tuple((f"family-{index}", "claim-a", 1, 1) for index in range(1, 5)),
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
        adjudication_id="adjudication-deterministic-bypass",
    )
    with pytest.raises(ValueError, match="deterministic"):
        validate_human_adjudication(
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


def test_human_adjudication_rejects_unrelated_calibration_scope() -> None:
    calibration = calibration_summary(
        tuple((f"family-{index}", "unrelated-criterion", 1, 1) for index in range(1, 5)),
        draws=10,
    )
    ratings = tuple(
        RatingRecord(
            schema_version=1,
            rating_id=f"rating-unrelated-{rater}",
            rater_pseudonym=f"rater-{rater}",
            randomized_response_id="response-unrelated",
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
        adjudication_id="adjudication-unrelated-calibration",
    )
    with pytest.raises(ValueError, match="calibration"):
        validate_human_adjudication(
            semantic_knowledge_contract(),
            assessment(
                "claim-a",
                CriterionDisposition.SATISFIED,
                AssessmentSource.HUMAN_ADJUDICATION,
                review_id=adjudication.adjudication_id,
            ),
            calibration=calibration,
            adjudication=adjudication,
        )
