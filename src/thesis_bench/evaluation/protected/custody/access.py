from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping, Sequence
from typing import TYPE_CHECKING

from ....pilot.models import ProtectedArtifactReference
from ....records import AppendOnlyEventStore, DecisionStatus, ProtectedRootReference, ReasonCode
from ..contracts.records import (
    CustodyPurpose,
    CustodyRole,
    ProtectedArtifact,
)
from ..source import APPROVED_PROTECTED_ROOT, is_repository_protected_path, protected_policy
from .events import append_access_event
from .judge_access import JudgeAccessGrant, validate_judge_access_grant
from .records import AccessDecision, ProtectedCustodyEvent, SafeProtectedHandle

if TYPE_CHECKING:
    from ..judge.records import JudgeConfiguration, JudgeQualification


def _coerce_role(value: CustodyRole | str) -> CustodyRole:
    try:
        return value if isinstance(value, CustodyRole) else CustodyRole(value)
    except ValueError as exc:
        raise ValueError("protected access role is not authorized") from exc


def _coerce_purpose(value: CustodyPurpose | str) -> CustodyPurpose:
    try:
        return value if isinstance(value, CustodyPurpose) else CustodyPurpose(value)
    except ValueError as exc:
        raise ValueError("protected access purpose is not authorized") from exc


def _allowed_purposes(role: CustodyRole) -> set[CustodyPurpose]:
    configured_policy = protected_policy()
    policy = configured_policy.get("access_policy")
    if not isinstance(policy, Mapping):
        raise ValueError("protected access policy is unavailable")
    denied_roles = configured_policy.get("model_facing_denied_roles")
    if not isinstance(denied_roles, (tuple, list)):
        raise ValueError("protected access policy is unavailable")
    if role.value in denied_roles:
        return set()
    configured = policy.get("allowed_purposes")
    if not isinstance(configured, Mapping):
        raise ValueError("protected access policy is unavailable")
    raw_purposes = configured.get(role.value)
    if not isinstance(raw_purposes, (tuple, list)):
        raise ValueError("protected access role is not configured")
    try:
        return {_coerce_purpose(value) for value in raw_purposes}
    except (TypeError, ValueError) as exc:
        raise ValueError("protected access policy is invalid") from exc


def _requires_exact_judge_scope(role: CustodyRole) -> bool:
    policy = protected_policy().get("access_policy")
    if not isinstance(policy, Mapping):
        raise ValueError("protected access policy is unavailable")
    scoped_roles = policy.get("scope_required_roles")
    if not isinstance(scoped_roles, (tuple, list)):
        raise ValueError("protected access policy is unavailable")
    return role.value in scoped_roles


def authorize_protected_access(
    *,
    actor_role: CustodyRole | str,
    purpose: CustodyPurpose | str,
    root_id: str = APPROVED_PROTECTED_ROOT,
) -> AccessDecision:
    role = _coerce_role(actor_role)
    access_purpose = _coerce_purpose(purpose)
    allowed = root_id == APPROVED_PROTECTED_ROOT and access_purpose in _allowed_purposes(role)
    return AccessDecision(
        schema_version=1,
        allowed=allowed,
        root_id=root_id,
        actor_role=role,
        purpose=access_purpose,
        reason_code=ReasonCode.OK if allowed else ReasonCode.DENIED_OPERATION,
    )


def load_protected_payload(
    reference: ProtectedRootReference,
    *,
    artifact: ProtectedArtifact,
    actor_role: CustodyRole | str,
    purpose: CustodyPurpose | str,
    reader: Callable[[str], bytes],
    event_store: AppendOnlyEventStore,
    judge_access: JudgeAccessGrant | None = None,
    judge_configuration: JudgeConfiguration | None = None,
    judge_qualification: JudgeQualification | None = None,
) -> bytes:
    if event_store is None:
        raise ValueError("protected custody evidence store is required")
    try:
        reference = ProtectedRootReference.model_validate(reference.model_dump(mode="python"))
        artifact = ProtectedArtifact.model_validate(artifact.model_dump(mode="python"))
    except ValueError:
        raise ValueError("protected payload access denied") from None
    role = _coerce_role(actor_role)
    access_purpose = _coerce_purpose(purpose)
    if _requires_exact_judge_scope(role):
        if judge_access is None or judge_configuration is None or judge_qualification is None:
            raise ValueError("judge access scope is required")
        validate_judge_access_grant(
            judge_access,
            configuration=judge_configuration,
            qualification=judge_qualification,
            artifact=artifact,
        )
    decision = authorize_protected_access(
        actor_role=role, purpose=access_purpose, root_id=reference.root_id
    )
    if reference != artifact.root_reference:
        decision = decision.model_copy(
            update={"allowed": False, "reason_code": ReasonCode.DENIED_OPERATION}
        )
    if not decision.allowed:
        append_access_event(
            event_store,
            artifact,
            role,
            access_purpose,
            DecisionStatus.AMEND,
            decision.reason_code,
            judge_access=judge_access,
        )
        raise ValueError("protected payload access denied")
    try:
        payload = reader(reference.relative_path)
        if (
            not isinstance(payload, bytes)
            or hashlib.sha256(payload).hexdigest() != reference.content_sha256
        ):
            raise ValueError
    except Exception:
        append_access_event(
            event_store,
            artifact,
            role,
            access_purpose,
            DecisionStatus.AMEND,
            ReasonCode.CAPTURE_HASH_MISMATCH,
            judge_access=judge_access,
        )
        raise ValueError("protected payload integrity validation failed") from None
    append_access_event(
        event_store,
        artifact,
        role,
        access_purpose,
        DecisionStatus.GO,
        ReasonCode.OK,
        judge_access=judge_access,
    )
    return payload


def record_protected_event(
    store: AppendOnlyEventStore, event: ProtectedCustodyEvent, *, artifact: ProtectedArtifact
) -> object:
    try:
        event = ProtectedCustodyEvent.model_validate(event.model_dump(mode="python"))
        artifact = ProtectedArtifact.model_validate(artifact.model_dump(mode="python"))
    except ValueError:
        raise ValueError("protected custody event is invalid") from None
    if event.root_id != artifact.root_reference.root_id:
        raise ValueError("protected event root does not match artifact")
    if (
        event.artifact_id != artifact.artifact_id
        or event.artifact_kind != artifact.artifact_kind
        or event.artifact_revision != artifact.revision
        or event.artifact_sha256 != artifact.content_sha256
    ):
        raise ValueError("protected event artifact identity does not match")
    return store.append(event)


def safe_protected_handle(
    reference: ProtectedArtifactReference,
    *,
    status: str,
    reason_codes: Sequence[ReasonCode] = (),
    assessor_configuration_id: str | None = None,
    provenance_id: str | None = None,
) -> SafeProtectedHandle:
    if reference.root_reference.root_id != APPROVED_PROTECTED_ROOT:
        raise ValueError("protected handle must use the approved root")
    return SafeProtectedHandle(
        schema_version=1,
        artifact_id=reference.artifact_id,
        artifact_kind=reference.artifact_kind,
        root_id=reference.root_reference.root_id,
        relative_path=reference.root_reference.relative_path,
        content_sha256=reference.root_reference.content_sha256,
        status=status,
        reason_codes=tuple(reason_codes),
        assessor_configuration_id=assessor_configuration_id,
        provenance_id=provenance_id,
    )


def model_facing_safe_handle(handle: SafeProtectedHandle) -> dict[str, object]:
    validated = SafeProtectedHandle.model_validate(handle.model_dump(mode="python"))
    if is_repository_protected_path(validated.relative_path):
        raise ValueError("protected evaluator payload is not model-facing")
    return validated.model_dump(mode="json")


__all__ = [
    "authorize_protected_access",
    "load_protected_payload",
    "model_facing_safe_handle",
    "record_protected_event",
    "safe_protected_handle",
]
