from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from ....records import AppendOnlyEventStore, DecisionStatus, ReasonCode
from ..contracts.records import CustodyPurpose, CustodyRole, ProtectedArtifact
from ..source import APPROVED_PROTECTED_ROOT
from .judge_access import JudgeAccessGrant
from .records import ProtectedCustodyEvent


def append_access_event(
    event_store: AppendOnlyEventStore,
    artifact: ProtectedArtifact,
    role: CustodyRole,
    purpose: CustodyPurpose,
    status: DecisionStatus,
    reason: ReasonCode,
    *,
    judge_access: JudgeAccessGrant | None = None,
) -> None:
    event = ProtectedCustodyEvent(
        schema_version=1,
        event_id=f"protected-access-{uuid4().hex}",
        event_type="protected-access",
        occurred_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        status=status,
        reason_codes=(reason,),
        artifact_id=artifact.artifact_id,
        artifact_kind=artifact.artifact_kind,
        root_id=APPROVED_PROTECTED_ROOT,
        artifact_revision=artifact.revision,
        artifact_sha256=artifact.content_sha256,
        actor_role=role,
        purpose=purpose,
        assessor_configuration_id=judge_access.judge_config_id if judge_access else None,
        qualification_id=judge_access.qualification_id if judge_access else None,
        criterion_id=judge_access.criterion_id if judge_access else None,
    )
    try:
        event_store.append(event)
    except Exception:
        raise ValueError("protected custody evidence persistence failed") from None


__all__ = ["append_access_event"]
