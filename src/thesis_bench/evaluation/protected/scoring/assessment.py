from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import field_validator, model_validator

from ....records import VersionedRecord
from ....schemas import Identifier, Sha256
from ...calibration import CalibrationStatus, CalibrationSummary
from ...rubrics import AdjudicationRecord
from ..contracts.config import ProtectedSemanticContract
from ..contracts.records import CriterionRole


class CriterionDisposition(StrEnum):
    SATISFIED = "satisfied"
    NOT_SATISFIED = "not_satisfied"
    CONTRADICTED = "contradicted"
    UNRESOLVED = "unresolved"


class AssessmentSource(StrEnum):
    DETERMINISTIC = "deterministic"
    QUALIFIED_SEMANTIC_JUDGE = "qualified_semantic_judge"
    HUMAN_ADJUDICATION = "human_adjudication"


class HumanReviewRoute(StrEnum):
    NONE = "none"
    ADJUDICATION = "adjudication"
    BLINDED_AUDIT = "blinded_audit"


class AuditSelection(VersionedRecord):
    selection_id: Identifier
    response_id: Identifier
    audit_policy_id: Identifier
    route: Literal[HumanReviewRoute.BLINDED_AUDIT] = HumanReviewRoute.BLINDED_AUDIT
    selected_before_outcomes: Literal[True]
    outcome_inspected: Literal[False]


class CriterionAssessment(VersionedRecord):
    assessment_id: Identifier
    criterion_id: Identifier
    disposition: CriterionDisposition
    source: AssessmentSource
    assessor_id: Identifier
    judge_config_id: Identifier | None = None
    review_id: Identifier | None = None
    predicate_id: Identifier | None = None
    predicate_version: Identifier | None = None

    @field_validator("disposition", mode="before")
    @classmethod
    def parse_disposition(cls, value: object) -> object:
        return CriterionDisposition(value) if isinstance(value, str) else value

    @field_validator("source", mode="before")
    @classmethod
    def parse_source(cls, value: object) -> object:
        return AssessmentSource(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_assessor_binding(self) -> CriterionAssessment:
        if self.source == AssessmentSource.QUALIFIED_SEMANTIC_JUDGE:
            if self.judge_config_id is None:
                raise ValueError("judge assessment requires a judge configuration identity")
            if self.review_id is not None:
                raise ValueError("judge assessment cannot carry a human review identity")
        elif self.source == AssessmentSource.HUMAN_ADJUDICATION:
            if self.review_id is None:
                raise ValueError("human assessment requires an adjudication identity")
            if self.judge_config_id is not None:
                raise ValueError("human assessment cannot carry a judge configuration identity")
        elif self.judge_config_id is not None or self.review_id is not None:
            raise ValueError("deterministic assessment cannot carry judge or review identity")
        if (self.predicate_id is None) != (self.predicate_version is None):
            raise ValueError("deterministic predicate binding must be complete")
        if self.source != AssessmentSource.DETERMINISTIC and (
            self.predicate_id is not None or self.predicate_version is not None
        ):
            raise ValueError("semantic assessments cannot carry deterministic predicate identity")
        return self


class QualifiedCriterionAssessment(CriterionAssessment):
    judge_config_sha256: Sha256
    qualification_id: Identifier

    @model_validator(mode="after")
    def require_qualified_judge_source(self) -> QualifiedCriterionAssessment:
        if self.source != AssessmentSource.QUALIFIED_SEMANTIC_JUDGE:
            raise ValueError("qualified assessment requires a semantic-judge source")
        if self.disposition == CriterionDisposition.UNRESOLVED:
            raise ValueError("qualified assessment cannot remain unresolved")
        return self


class CalibratedHumanCriterionAssessment(CriterionAssessment):
    contract_id: Identifier
    calibration_id: Identifier
    adjudication_id: Identifier
    review_route: HumanReviewRoute
    audit_selection_id: Identifier | None = None

    @model_validator(mode="after")
    def require_calibrated_human_source(self) -> CalibratedHumanCriterionAssessment:
        if self.source != AssessmentSource.HUMAN_ADJUDICATION:
            raise ValueError("calibrated assessment requires a human adjudication source")
        if self.disposition == CriterionDisposition.UNRESOLVED:
            raise ValueError("calibrated human assessment cannot remain unresolved")
        if self.review_id != self.adjudication_id:
            raise ValueError("calibrated human assessment must bind its adjudication")
        if self.review_route == HumanReviewRoute.NONE:
            raise ValueError("calibrated human assessment requires a review route")
        if self.review_route == HumanReviewRoute.BLINDED_AUDIT and self.audit_selection_id is None:
            raise ValueError("blinded human assessment requires an audit selection")
        if (
            self.review_route == HumanReviewRoute.ADJUDICATION
            and self.audit_selection_id is not None
        ):
            raise ValueError("ordinary human adjudication cannot carry an audit selection")
        return self


def validate_human_adjudication(
    contract: ProtectedSemanticContract,
    assessment: CriterionAssessment,
    *,
    calibration: CalibrationSummary,
    adjudication: AdjudicationRecord,
    review_route: HumanReviewRoute = HumanReviewRoute.ADJUDICATION,
    audit_selection: AuditSelection | None = None,
) -> CalibratedHumanCriterionAssessment:
    try:
        review_route = HumanReviewRoute(review_route)
        if audit_selection is not None:
            audit_selection = AuditSelection.model_validate(
                audit_selection.model_dump(mode="python")
            )
    except ValueError:
        raise ValueError("human review route is invalid") from None
    if calibration.status != CalibrationStatus.GO:
        raise ValueError("human assessor calibration is not qualified")
    if assessment.source != AssessmentSource.HUMAN_ADJUDICATION:
        raise ValueError("human adjudication requires a human assessment")
    if assessment.disposition == CriterionDisposition.UNRESOLVED or not adjudication.resolved:
        raise ValueError("human adjudication cannot remain unresolved")
    if adjudication.criterion_id != assessment.criterion_id:
        raise ValueError("human adjudication criterion does not match assessment")
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
    if "human_adjudication" not in semantic.allowed_assessor_modes:
        raise ValueError("human adjudication is not allowed for this criterion")
    if review_route == HumanReviewRoute.BLINDED_AUDIT and audit_selection is None:
        raise ValueError("audit selection is not predeclared")
    if review_route == HumanReviewRoute.ADJUDICATION and audit_selection is not None:
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
        calibration_id=calibration.summary_id,
        adjudication_id=adjudication.adjudication_id,
        review_route=review_route,
        audit_selection_id=audit_selection.selection_id if audit_selection else None,
    )


__all__ = [
    "AssessmentSource",
    "AuditSelection",
    "CalibratedHumanCriterionAssessment",
    "CriterionAssessment",
    "CriterionDisposition",
    "HumanReviewRoute",
    "QualifiedCriterionAssessment",
    "validate_human_adjudication",
]
