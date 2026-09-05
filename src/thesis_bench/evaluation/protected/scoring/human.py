from __future__ import annotations

from typing import TYPE_CHECKING

from ....records import content_sha256
from ...calibration import CalibrationStatus, CalibrationSummary, calibration_digest
from ...rubrics import AdjudicationRecord
from ..contracts.config import ProtectedSemanticContract
from ..contracts.records import CriterionRole
from .assessment import (
    AssessmentSource,
    AuditSelection,
    CalibratedHumanCriterionAssessment,
    CriterionAssessment,
    CriterionDisposition,
    HumanReviewRoute,
)

if TYPE_CHECKING:
    from ..judge.records import AuditPolicy


def _validate_calibration_scope(
    contract: ProtectedSemanticContract,
    criterion_id: str,
    calibration: CalibrationSummary,
) -> None:
    if calibration.status != CalibrationStatus.GO:
        raise ValueError("human assessor calibration is not qualified")
    if calibration.content_sha256 is None or calibration.content_sha256 != calibration_digest(
        calibration
    ):
        raise ValueError("human assessor calibration provenance is invalid")
    if (
        calibration.task_class != contract.task_class
        or calibration.language != contract.language
        or calibration.contract_id != contract.evaluator_identity.identity_id
        or calibration.contract_sha256 != contract.evaluator_identity.content_sha256
        or criterion_id not in calibration.exact_by_criterion
    ):
        raise ValueError("human assessor calibration does not cover this contract criterion")


def _validate_adjudication(adjudication: AdjudicationRecord) -> AdjudicationRecord:
    try:
        return AdjudicationRecord.model_validate(adjudication.model_dump(mode="python"))
    except ValueError:
        raise ValueError("human adjudication record is invalid") from None


def validate_human_adjudication(
    contract: ProtectedSemanticContract,
    assessment: CriterionAssessment,
    *,
    calibration: CalibrationSummary,
    adjudication: AdjudicationRecord,
    review_route: HumanReviewRoute = HumanReviewRoute.ADJUDICATION,
    audit_selection: AuditSelection | None = None,
    audit_policy: AuditPolicy | None = None,
    response_id: str | None = None,
) -> CalibratedHumanCriterionAssessment:
    try:
        review_route = HumanReviewRoute(review_route)
        if audit_selection is not None:
            audit_selection = AuditSelection.model_validate(
                audit_selection.model_dump(mode="python")
            )
    except ValueError:
        raise ValueError("human review route is invalid") from None
    if assessment.source != AssessmentSource.HUMAN_ADJUDICATION:
        raise ValueError("human adjudication requires a human assessment")
    if assessment.disposition == CriterionDisposition.UNRESOLVED:
        raise ValueError("human adjudication cannot remain unresolved")
    criterion = next(
        (item for item in contract.criteria if item.criterion_id == assessment.criterion_id), None
    )
    semantic = next(
        (
            item
            for item in contract.semantic_criteria
            if item.criterion_id == assessment.criterion_id
        ),
        None,
    )
    if criterion is None or CriterionRole.SEMANTIC not in criterion.roles or semantic is None:
        raise ValueError("human adjudication requires a declared semantic criterion")
    if CriterionRole.DETERMINISTIC in criterion.roles:
        raise ValueError("human adjudication cannot bypass a deterministic criterion")
    if "human_adjudication" not in semantic.allowed_assessor_modes:
        raise ValueError("human adjudication is not allowed for this criterion")
    _validate_calibration_scope(contract, assessment.criterion_id, calibration)
    adjudication = _validate_adjudication(adjudication)
    if not adjudication.resolved:
        raise ValueError("human adjudication cannot remain unresolved")
    if adjudication.criterion_id != assessment.criterion_id:
        raise ValueError("human adjudication criterion does not match assessment")
    if review_route == HumanReviewRoute.BLINDED_AUDIT:
        if audit_selection is None or audit_policy is None or response_id is None:
            raise ValueError("audit adjudication requires a frozen selection and response")
        from .routing import validate_audit_selection

        validate_audit_selection(audit_selection, audit_policy, response_id=response_id)
    elif audit_selection is not None or audit_policy is not None:
        raise ValueError("ordinary adjudication cannot carry an audit selection")
    return CalibratedHumanCriterionAssessment(
        schema_version=1,
        assessment_id=assessment.assessment_id,
        criterion_id=assessment.criterion_id,
        disposition=assessment.disposition,
        source=assessment.source,
        assessor_id=assessment.assessor_id,
        review_id=adjudication.adjudication_id,
        contract_id=contract.evaluator_identity.identity_id,
        contract_sha256=contract.evaluator_identity.content_sha256,
        calibration_id=calibration.summary_id,
        calibration_content_sha256=calibration.content_sha256 or "",
        adjudication_id=adjudication.adjudication_id,
        adjudication_content_sha256=content_sha256(adjudication.model_dump(mode="json")),
        review_route=review_route,
        audit_selection_id=audit_selection.selection_id if audit_selection else None,
    )


def validate_primary_human_assessment(
    contract: ProtectedSemanticContract,
    assessment: CriterionAssessment,
    *,
    calibration: CalibrationSummary,
    adjudication: AdjudicationRecord,
    audit_selection: AuditSelection | None = None,
    audit_policy: AuditPolicy | None = None,
    response_id: str | None = None,
) -> CalibratedHumanCriterionAssessment:
    if type(assessment) is not CalibratedHumanCriterionAssessment:
        raise ValueError("primary human assessment must be an issued calibrated envelope")
    try:
        assessment = CalibratedHumanCriterionAssessment.model_validate(
            assessment.model_dump(mode="python")
        )
    except ValueError:
        raise ValueError("primary human assessment is invalid") from None
    base = CriterionAssessment(
        schema_version=1,
        assessment_id=assessment.assessment_id,
        criterion_id=assessment.criterion_id,
        disposition=assessment.disposition,
        source=assessment.source,
        assessor_id=assessment.assessor_id,
        review_id=assessment.adjudication_id,
    )
    expected = validate_human_adjudication(
        contract,
        base,
        calibration=calibration,
        adjudication=adjudication,
        review_route=assessment.review_route,
        audit_selection=audit_selection,
        audit_policy=audit_policy,
        response_id=response_id,
    )
    if expected.model_dump(mode="python") != assessment.model_dump(mode="python"):
        raise ValueError("primary human assessment provenance does not match evidence")
    return assessment


__all__ = ["validate_human_adjudication", "validate_primary_human_assessment"]
