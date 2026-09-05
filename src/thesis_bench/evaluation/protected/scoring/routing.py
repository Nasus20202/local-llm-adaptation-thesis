from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from ....records import ReasonCode, VersionedRecord
from ....schemas import Identifier
from ..contracts.config import ProtectedSemanticContract
from ..contracts.records import CriterionRole
from .assessment import (
    AssessmentSource,
    AuditSelection,
    CriterionAssessment,
    CriterionDisposition,
    HumanReviewRoute,
    QualifiedCriterionAssessment,
)


class SemanticReviewRequest(VersionedRecord):
    request_id: Identifier
    contract_id: Identifier
    criterion_id: Identifier
    route: HumanReviewRoute
    reason_code: ReasonCode
    status: Literal["required"]
    assessor_configuration_id: Identifier | None = None
    audit_selection_id: Identifier | None = None

    @model_validator(mode="after")
    def validate_status(self) -> SemanticReviewRequest:
        if self.route == HumanReviewRoute.NONE:
            raise ValueError("review requests require a human route")
        if self.route == HumanReviewRoute.BLINDED_AUDIT and self.audit_selection_id is None:
            raise ValueError("blinded audit requests require a predeclared selection")
        if self.route == HumanReviewRoute.ADJUDICATION and self.audit_selection_id is not None:
            raise ValueError("ordinary adjudication cannot carry an audit selection")
        return self


class AssessmentRoute(VersionedRecord):
    criterion_id: Identifier
    assessment: CriterionAssessment | None = None
    route: HumanReviewRoute
    audit_selection_id: Identifier | None = None
    request: SemanticReviewRequest | None = None

    @model_validator(mode="after")
    def validate_route(self) -> AssessmentRoute:
        if self.assessment is not None and self.assessment.criterion_id != self.criterion_id:
            raise ValueError("assessment route criterion mismatch")
        if self.assessment is None and self.request is None:
            raise ValueError("unresolved assessment requires a review request")
        if self.assessment is not None and self.request is not None:
            raise ValueError("resolved assessment cannot carry a pending review request")
        if self.route == HumanReviewRoute.NONE and self.assessment is None:
            raise ValueError("no review route requires an assessment")
        if self.route == HumanReviewRoute.BLINDED_AUDIT and self.audit_selection_id is None:
            raise ValueError("blinded audit routes require an audit selection")
        if self.route != HumanReviewRoute.BLINDED_AUDIT and self.audit_selection_id is not None:
            raise ValueError("ordinary routes cannot carry an audit selection")
        if self.assessment is not None and self.route != HumanReviewRoute.NONE:
            if self.assessment.source != AssessmentSource.HUMAN_ADJUDICATION:
                raise ValueError("only human assessments can carry a review route")
        if self.request is not None and self.request.criterion_id != self.criterion_id:
            raise ValueError("assessment route does not match its review request")
        return self


def validate_audit_selection(selection: AuditSelection, policy: object | None) -> AuditSelection:
    if selection.route != HumanReviewRoute.BLINDED_AUDIT:
        raise ValueError("audit selection must use the blinded-audit route")
    if selection.selected_before_outcomes is not True or selection.outcome_inspected is not False:
        raise ValueError("audit membership must be predeclared and blinded")
    if policy is not None:
        if getattr(policy, "audit_policy_id", None) != selection.audit_policy_id:
            raise ValueError("audit selection does not match the frozen policy")
        if not getattr(policy, "frozen_before_outcomes", False) or not getattr(
            policy, "blinded", False
        ):
            raise ValueError("audit policy is not frozen and blinded")
    return selection


def route_criterion_assessment(
    contract: ProtectedSemanticContract,
    criterion_id: str,
    *,
    deterministic_assessment: CriterionAssessment | None = None,
    judge_assessment: CriterionAssessment | None = None,
    human_assessment: CriterionAssessment | None = None,
    review_route: HumanReviewRoute = HumanReviewRoute.ADJUDICATION,
    audit_selection_id: str | None = None,
    audit_selection: AuditSelection | None = None,
) -> AssessmentRoute:
    try:
        review_route = HumanReviewRoute(review_route)
    except ValueError:
        raise ValueError("human review route is invalid") from None
    criterion = next(
        (item for item in contract.criteria if item.criterion_id == criterion_id), None
    )
    if criterion is None:
        raise ValueError("assessment references an unknown criterion")
    semantic = next(
        (item for item in contract.semantic_criteria if item.criterion_id == criterion_id), None
    )
    if deterministic_assessment is not None:
        if deterministic_assessment.source != AssessmentSource.DETERMINISTIC:
            raise ValueError("deterministic route requires a deterministic assessment")
        if CriterionRole.DETERMINISTIC not in criterion.roles:
            raise ValueError("criterion does not declare a deterministic route")
        return AssessmentRoute(
            schema_version=1,
            criterion_id=criterion_id,
            assessment=deterministic_assessment,
            route=HumanReviewRoute.NONE,
        )
    if CriterionRole.DETERMINISTIC in criterion.roles:
        raise ValueError("deterministic criteria require deterministic resolution")
    if CriterionRole.SEMANTIC not in criterion.roles or semantic is None:
        raise ValueError("semantic routes require a declared semantic criterion")
    if human_assessment is not None:
        if human_assessment.source != AssessmentSource.HUMAN_ADJUDICATION:
            raise ValueError("human route requires a human assessment")
        if "human_adjudication" not in semantic.allowed_assessor_modes:
            raise ValueError("human adjudication is not allowed for this criterion")
        if review_route == HumanReviewRoute.NONE:
            raise ValueError("human assessment requires a review route")
        if human_assessment.disposition == CriterionDisposition.UNRESOLVED:
            raise ValueError("human assessment cannot remain unresolved")
        if review_route == HumanReviewRoute.BLINDED_AUDIT:
            if audit_selection is None:
                raise ValueError("audit selection is required")
            audit_selection_id = validate_audit_selection(audit_selection, None).selection_id
        elif audit_selection is not None:
            raise ValueError("ordinary adjudication cannot carry an audit selection")
        return AssessmentRoute(
            schema_version=1,
            criterion_id=criterion_id,
            assessment=human_assessment,
            route=review_route,
            audit_selection_id=audit_selection_id,
        )
    if (
        isinstance(judge_assessment, QualifiedCriterionAssessment)
        and judge_assessment.disposition != CriterionDisposition.UNRESOLVED
    ):
        if "qualified_semantic_judge" not in semantic.allowed_assessor_modes:
            raise ValueError("qualified semantic judge is not allowed for this criterion")
        return AssessmentRoute(
            schema_version=1,
            criterion_id=criterion_id,
            assessment=judge_assessment,
            route=HumanReviewRoute.NONE,
            audit_selection_id=None,
        )
    if review_route == HumanReviewRoute.BLINDED_AUDIT:
        if audit_selection is None:
            raise ValueError("audit selection is required")
        audit_selection_id = validate_audit_selection(audit_selection, None).selection_id
    elif audit_selection is not None:
        raise ValueError("ordinary adjudication cannot carry an audit selection")
    return AssessmentRoute(
        schema_version=1,
        criterion_id=criterion_id,
        route=review_route,
        request=SemanticReviewRequest(
            schema_version=1,
            request_id=f"review-{contract.evaluator_identity.identity_id}-{criterion_id}",
            contract_id=contract.evaluator_identity.identity_id,
            criterion_id=criterion_id,
            route=review_route,
            reason_code=ReasonCode.UNRESOLVED_CRITERION,
            status="required",
            assessor_configuration_id=judge_assessment.judge_config_id
            if judge_assessment
            else None,
            audit_selection_id=audit_selection_id,
        ),
        audit_selection_id=audit_selection_id,
    )


__all__ = [
    "AssessmentRoute",
    "SemanticReviewRequest",
    "route_criterion_assessment",
    "validate_audit_selection",
]
