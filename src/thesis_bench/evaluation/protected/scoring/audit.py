from __future__ import annotations

from ....records import content_sha256
from ....schemas import Identifier
from .assessment import AuditSelection, HumanReviewRoute


def audit_selection_identity(
    policy_id: str, manifest_id: str, manifest_sha256: str, response_id: str
) -> str:
    digest = content_sha256(
        {
            "audit_policy_id": policy_id,
            "membership_manifest_id": manifest_id,
            "membership_manifest_sha256": manifest_sha256,
            "response_id": response_id,
        }
    )
    return f"audit-selection-{digest[:24]}"


def validate_audit_selection(
    selection: AuditSelection,
    policy: object | None,
    *,
    response_id: Identifier | None = None,
) -> AuditSelection:
    if selection.route != HumanReviewRoute.BLINDED_AUDIT:
        raise ValueError("audit selection must use the blinded-audit route")
    if selection.selected_before_outcomes is not True or selection.outcome_inspected is not False:
        raise ValueError("audit membership must be predeclared and blinded")
    from ..judge.records import AuditPolicy

    if not isinstance(policy, AuditPolicy):
        raise ValueError("audit policy is required") from None
    try:
        policy = AuditPolicy.model_validate(policy.model_dump(mode="python"))
    except ValueError:
        raise ValueError("audit policy is invalid") from None
    if response_id is None or selection.response_id != response_id:
        raise ValueError("audit selection does not match the response identity")
    if selection.response_id not in policy.selected_response_ids:
        raise ValueError("response is not in the frozen audit membership")
    if (
        policy.audit_policy_id != selection.audit_policy_id
        or policy.membership_manifest_id != selection.membership_manifest_id
        or policy.membership_manifest_sha256 != selection.membership_manifest_sha256
        or policy.membership_manifest_root_reference != selection.membership_manifest_root_reference
    ):
        raise ValueError("audit selection does not match the frozen membership manifest")
    if not policy.frozen_before_outcomes or not policy.blinded:
        raise ValueError("audit policy is not frozen and blinded")
    if selection.selection_id != audit_selection_identity(
        policy.audit_policy_id,
        policy.membership_manifest_id,
        policy.membership_manifest_sha256,
        selection.response_id,
    ):
        raise ValueError("audit selection identity is not reproducible")
    return selection


__all__ = ["audit_selection_identity", "validate_audit_selection"]
