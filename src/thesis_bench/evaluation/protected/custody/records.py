from __future__ import annotations

from datetime import UTC, datetime

from pydantic import field_validator, model_validator
from pydantic.types import StrictBool

from ....records import AppendOnlyEvent, DecisionStatus, ReasonCode, VersionedRecord
from ....schemas import Identifier, NonBlankStr, Sha256
from ..contracts.records import CustodyPurpose, CustodyRole
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path


class ProtectedCustodyEvent(AppendOnlyEvent):
    artifact_id: Identifier
    artifact_kind: Identifier
    root_id: str
    artifact_revision: Identifier
    artifact_sha256: Sha256
    actor_role: CustodyRole
    purpose: CustodyPurpose
    assessor_configuration_id: Identifier | None = None
    qualification_id: Identifier | None = None
    criterion_id: Identifier | None = None
    supersedes_artifact_id: Identifier | None = None

    @field_validator("status", mode="before")
    @classmethod
    def parse_status(cls, value: object) -> object:
        return DecisionStatus(value) if isinstance(value, str) else value

    @field_validator("actor_role", mode="before")
    @classmethod
    def parse_actor_role(cls, value: object) -> object:
        return CustodyRole(value) if isinstance(value, str) else value

    @field_validator("purpose", mode="before")
    @classmethod
    def parse_purpose(cls, value: object) -> object:
        return CustodyPurpose(value) if isinstance(value, str) else value

    @field_validator("occurred_at")
    @classmethod
    def require_utc_timestamp(cls, value: str) -> str:
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp must be ISO-8601 UTC") from exc
        if timestamp.tzinfo is None or timestamp.utcoffset() != UTC.utcoffset(timestamp):
            raise ValueError("timestamp must be UTC")
        return value

    @field_validator("root_id")
    @classmethod
    def require_approved_root(cls, value: str) -> str:
        if value != APPROVED_PROTECTED_ROOT:
            raise ValueError("protected event root is not approved")
        return value

    @model_validator(mode="after")
    def require_judge_scope(self) -> ProtectedCustodyEvent:
        if self.purpose == CustodyPurpose.JUDGE_ASSESSMENT and any(
            value is None
            for value in (
                self.assessor_configuration_id,
                self.qualification_id,
                self.criterion_id,
            )
        ):
            raise ValueError("judge custody events require exact qualification scope")
        return self


class AccessDecision(VersionedRecord):
    allowed: StrictBool
    root_id: str
    actor_role: CustodyRole
    purpose: CustodyPurpose
    reason_code: ReasonCode


class SafeProtectedHandle(VersionedRecord):
    artifact_id: Identifier
    artifact_kind: Identifier
    root_id: str
    relative_path: NonBlankStr
    content_sha256: Sha256
    status: str
    reason_codes: tuple[ReasonCode, ...] = ()
    assessor_configuration_id: Identifier | None = None
    provenance_id: Identifier | None = None

    @field_validator("root_id")
    @classmethod
    def require_approved_root(cls, value: str) -> str:
        if value != APPROVED_PROTECTED_ROOT:
            raise ValueError("protected handle must use the approved root")
        return value

    @field_validator("status")
    @classmethod
    def require_known_status(cls, value: str) -> str:
        if value not in {"draft", "frozen", "superseded"}:
            raise ValueError("protected handle status is invalid")
        return value

    @field_validator("relative_path")
    @classmethod
    def require_safe_path(cls, value: str) -> str:
        return validate_protected_relative_path(value)


__all__ = ["AccessDecision", "ProtectedCustodyEvent", "SafeProtectedHandle"]
