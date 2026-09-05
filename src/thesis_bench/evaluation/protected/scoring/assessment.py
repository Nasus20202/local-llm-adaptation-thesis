from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import field_validator, model_validator

from ....records import ProtectedRootReference, VersionedRecord, content_sha256
from ....schemas import Identifier, Sha256
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path


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


class DeterministicPredicateResult(VersionedRecord):
    result_id: Identifier
    criterion_id: Identifier
    predicate_id: Identifier
    predicate_version: Identifier
    disposition: CriterionDisposition
    contract_id: Identifier
    contract_sha256: Sha256
    observation_sha256: Sha256
    result_sha256: Sha256

    @field_validator("disposition", mode="before")
    @classmethod
    def parse_disposition(cls, value: object) -> object:
        return CriterionDisposition(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_result_hash(self) -> DeterministicPredicateResult:
        expected = content_sha256(self.model_dump(mode="json", exclude={"result_sha256"}))
        if self.result_sha256 != expected:
            raise ValueError("deterministic predicate result hash is invalid")
        return self


class AuditSelection(VersionedRecord):
    selection_id: Identifier
    response_id: Identifier
    audit_policy_id: Identifier
    route: Literal[HumanReviewRoute.BLINDED_AUDIT] = HumanReviewRoute.BLINDED_AUDIT
    selected_before_outcomes: Literal[True]
    outcome_inspected: Literal[False]
    membership_manifest_id: Identifier
    membership_manifest_sha256: Sha256
    membership_manifest_root_reference: ProtectedRootReference
    selection_content_sha256: Sha256

    @model_validator(mode="after")
    def validate_membership_artifact(self) -> AuditSelection:
        if self.membership_manifest_root_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("audit membership must use the approved protected root")
        validate_protected_relative_path(self.membership_manifest_root_reference.relative_path)
        if self.membership_manifest_root_reference.content_sha256 != (
            self.membership_manifest_sha256
        ):
            raise ValueError("audit membership manifest hash does not match its root reference")
        expected = content_sha256(
            self.model_dump(mode="json", exclude={"selection_content_sha256"})
        )
        if self.selection_content_sha256 != expected:
            raise ValueError("audit selection hash does not cover its record")
        return self


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
    deterministic_result: DeterministicPredicateResult | None = None

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
        if self.source == AssessmentSource.DETERMINISTIC and self.deterministic_result is None:
            raise ValueError("deterministic assessment requires an executed predicate result")
        if self.source != AssessmentSource.DETERMINISTIC and self.deterministic_result is not None:
            raise ValueError("semantic assessments cannot carry a deterministic result")
        if self.deterministic_result is not None and (
            self.deterministic_result.criterion_id != self.criterion_id
            or self.deterministic_result.predicate_id != self.predicate_id
            or self.deterministic_result.predicate_version != self.predicate_version
            or self.deterministic_result.disposition != self.disposition
        ):
            raise ValueError("deterministic result does not match its assessment")
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
    contract_sha256: Sha256
    calibration_content_sha256: Sha256
    adjudication_content_sha256: Sha256

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


def validate_human_adjudication(*args: Any, **kwargs: Any) -> Any:
    """Compatibility facade for the human-adjudication validator."""
    from .human import validate_human_adjudication as implementation

    return implementation(*args, **kwargs)


__all__ = [
    "AssessmentSource",
    "AuditSelection",
    "CalibratedHumanCriterionAssessment",
    "CriterionAssessment",
    "CriterionDisposition",
    "DeterministicPredicateResult",
    "HumanReviewRoute",
    "QualifiedCriterionAssessment",
    "validate_human_adjudication",
]
