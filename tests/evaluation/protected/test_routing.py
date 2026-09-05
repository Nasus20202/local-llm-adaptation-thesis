from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    AssessmentSource,
    AuditPolicy,
    AuditSelection,
    CriterionDisposition,
    HumanReviewRoute,
    audit_selection_identity,
    route_criterion_assessment,
    validate_audit_selection,
)
from thesis_bench.records import ProtectedRootReference, content_sha256

from .contracts import procedural_contract
from .fixtures import assessment, semantic_knowledge_contract
from .judge_fixtures import qualified_judge


def test_route_prefers_deterministic_and_routes_unresolved_semantics_to_human() -> None:
    contract = procedural_contract()
    deterministic = assessment("required-state", CriterionDisposition.SATISFIED)
    routed = route_criterion_assessment(
        contract,
        "required-state",
        deterministic_assessment=deterministic,
        judge_assessment=assessment(
            "required-state",
            CriterionDisposition.NOT_SATISFIED,
            AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
            judge_config_id="untrusted",
        ),
    )
    assert routed.assessment == deterministic
    assert routed.route == HumanReviewRoute.NONE

    unresolved = route_criterion_assessment(
        semantic_knowledge_contract(),
        "claim-a",
        judge_assessment=assessment(
            "claim-a",
            CriterionDisposition.UNRESOLVED,
            AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
            judge_config_id="judge-config-1",
        ),
    )
    assert unresolved.assessment is None
    assert unresolved.route == HumanReviewRoute.ADJUDICATION
    assert unresolved.request is not None
    with pytest.raises(ValueError, match="audit selection"):
        route_criterion_assessment(
            semantic_knowledge_contract(),
            "claim-a",
            judge_assessment=assessment(
                "claim-a",
                CriterionDisposition.UNRESOLVED,
                AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
                judge_config_id="judge-config-1",
            ),
            review_route=HumanReviewRoute.BLINDED_AUDIT,
        )


def test_audit_identity_cannot_bypass_membership_validation() -> None:
    configuration, qualification = qualified_judge()
    with pytest.raises(ValueError, match="frozen selection"):
        route_criterion_assessment(
            semantic_knowledge_contract(),
            "claim-a",
            judge_assessment=assessment(
                "claim-a",
                CriterionDisposition.SATISFIED,
                AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
                judge_config_id=configuration.judge_config_id,
            ),
            audit_selection_id="fabricated-selection",
            judge_configuration=configuration,
            judge_qualification=qualification,
        )


def test_human_audit_selection_must_be_predeclared_and_blinded() -> None:
    policy = AuditPolicy(
        schema_version=1,
        audit_policy_id="audit-policy-1",
        sampling_identity="frozen-sample-rule",
        frozen_before_outcomes=True,
        blinded=True,
        membership_manifest_id="audit-membership-manifest-1",
        membership_manifest_sha256="6" * 64,
        membership_manifest_root_reference=ProtectedRootReference(
            schema_version=1,
            root_id="development-protected-evaluator-v1",
            relative_path="audit/membership-manifest-1.json",
            content_sha256="6" * 64,
        ),
        selected_response_ids=("response-1",),
    )
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
    selected = validate_audit_selection(
        AuditSelection(
            **selection_fields,
            selection_content_sha256=content_sha256(selection_fields),
        ),
        policy,
        response_id="response-1",
    )
    assert selected.route == HumanReviewRoute.BLINDED_AUDIT
    with pytest.raises(ValueError):
        validate_audit_selection(
            selected.model_copy(
                update={
                    "selection_id": "post-hoc",
                    "response_id": "response-2",
                    "outcome_inspected": True,
                }
            ),
            policy,
            response_id="response-1",
        )
    fabricated = dict(selection_fields, selection_id="fabricated-selection")
    with pytest.raises(ValueError, match="identity"):
        validate_audit_selection(
            AuditSelection(
                **fabricated,
                selection_content_sha256=content_sha256(fabricated),
            ),
            policy,
            response_id="response-1",
        )


def test_predeclared_audit_routes_to_human_even_without_judge_escalation_reason() -> None:
    configuration, qualification = qualified_judge()
    contract = semantic_knowledge_contract()
    policy = configuration.audit_policy
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
    selection = AuditSelection(
        **selection_fields,
        selection_content_sha256=content_sha256(selection_fields),
    )
    routed = route_criterion_assessment(
        contract,
        "claim-a",
        judge_assessment=assessment(
            "claim-a",
            CriterionDisposition.SATISFIED,
            AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
            judge_config_id=configuration.judge_config_id,
        ),
        human_assessment=assessment(
            "claim-a",
            CriterionDisposition.SATISFIED,
            AssessmentSource.HUMAN_ADJUDICATION,
            review_id="audit-adjudication-1",
        ),
        review_route=HumanReviewRoute.BLINDED_AUDIT,
        audit_selection=selection,
        audit_policy=policy,
        response_id="response-1",
        judge_configuration=configuration,
        judge_qualification=qualification,
    )
    assert routed.route == HumanReviewRoute.BLINDED_AUDIT
    assert routed.assessment is not None
    assert routed.audit_selection_id == selection.selection_id
