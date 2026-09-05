from __future__ import annotations

import pytest

from thesis_bench.evaluation.protected import (
    AssessmentSource,
    AuditPolicy,
    AuditSelection,
    CriterionDisposition,
    HumanReviewRoute,
    route_criterion_assessment,
    validate_audit_selection,
)

from .contracts import procedural_contract
from .fixtures import assessment, knowledge_contract


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
        knowledge_contract(),
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
            knowledge_contract(),
            "claim-a",
            judge_assessment=assessment(
                "claim-a",
                CriterionDisposition.UNRESOLVED,
                AssessmentSource.QUALIFIED_SEMANTIC_JUDGE,
                judge_config_id="judge-config-1",
            ),
            review_route=HumanReviewRoute.BLINDED_AUDIT,
        )


def test_human_audit_selection_must_be_predeclared_and_blinded() -> None:
    policy = AuditPolicy(
        schema_version=1,
        audit_policy_id="audit-policy-1",
        sampling_identity="frozen-sample-rule",
        frozen_before_outcomes=True,
        blinded=True,
    )
    selected = validate_audit_selection(
        AuditSelection(
            schema_version=1,
            selection_id="selected",
            response_id="response-1",
            audit_policy_id=policy.audit_policy_id,
            route=HumanReviewRoute.BLINDED_AUDIT,
            selected_before_outcomes=True,
            outcome_inspected=False,
        ),
        policy,
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
        )
