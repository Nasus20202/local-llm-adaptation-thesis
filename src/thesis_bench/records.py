from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from pydantic.types import StrictStr

from .schemas import Identifier, Sha256


class DecisionStatus(StrEnum):
    GO = "GO"
    AMEND = "AMEND"
    STOP_DEFER = "STOP/DEFER"


class ReasonCode(StrEnum):
    OK = "ok"
    UNKNOWN_VERSION = "unknown_version"
    INVALID_RECORD = "invalid_record"
    MUTABLE_IDENTITY = "mutable_identity"
    COLLISION = "collision"
    OVERWRITE_ATTEMPT = "overwrite_attempt"
    PROTECTED_PAYLOAD = "protected_payload"
    UNSAFE_PATH = "unsafe_path"
    POLICY_VIOLATION = "policy_violation"
    BUDGET_EXHAUSTED = "budget_exhausted"
    INFRASTRUCTURE_FAILURE = "infrastructure_failure"
    EVALUATED_SYSTEM_FAILURE = "evaluated_system_failure"
    DENIED_OPERATION = "denied_operation"
    OUTCOME_SELECTED = "outcome_selected"
    FAMILY_OVERLAP = "family_overlap"
    SOURCE_DRIFT = "source_drift"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    FINAL_TEST_FORBIDDEN = "final_test_forbidden"
    FIXTURE_MISMATCH = "fixture_mismatch"
    AMBIGUOUS = "ambiguous"
    UNBLINDED = "unblinded"
    MISSING_INDEPENDENCE = "missing_independence"
    NON_DETERMINISTIC = "non_deterministic"
    SAFETY_FAILURE = "safety_failure"
    PERMISSION_FAILURE = "permission_failure"
    EGRESS_FAILURE = "egress_failure"
    TIMEOUT = "timeout"
    MALFORMED = "malformed"
    INVALID_CONFIGURATION = "invalid_configuration"
    WRONG_ANSWER = "wrong_answer"
    REFUSAL = "refusal"
    MALFORMED_ANSWER = "malformed_answer"
    REMEDIATION_FAILED = "remediation_failed"
    RUNTIME_FAILURE = "runtime_failure"
    EVALUATED_SYSTEM_TIMEOUT = "evaluated_system_timeout"
    CAPTURE_HASH_MISMATCH = "capture_hash_mismatch"
    MISSING_PROVENANCE = "missing_provenance"
    EVALUATOR_INFRASTRUCTURE_FAILURE = "evaluator_infrastructure_failure"
    HARDWARE_MEASUREMENT_FAILURE = "hardware_measurement_failure"


class VersionedRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    schema_version: Annotated[int, Field(strict=True)]

    @field_validator("schema_version")
    @classmethod
    def require_supported_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("unsupported schema version")
        return value


class Identity(VersionedRecord):
    kind: Identifier
    identity_id: Identifier
    revision: Identifier
    content_sha256: Sha256


_UTC_TIMESTAMP = Annotated[str, Field(strict=True, min_length=1)]


class AppendOnlyEvent(VersionedRecord):
    event_id: Identifier
    event_type: Identifier
    occurred_at: _UTC_TIMESTAMP
    status: DecisionStatus
    reason_codes: tuple[ReasonCode, ...] = ()

    @field_validator("occurred_at")
    @classmethod
    def require_utc_timestamp(cls, value: str) -> str:
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp must be ISO-8601") from exc
        if timestamp.tzinfo is None or timestamp.utcoffset() != UTC.utcoffset(timestamp):
            raise ValueError("timestamp must be UTC")
        return value


class ProtectedRootReference(VersionedRecord):
    root_id: Identifier
    relative_path: StrictStr = Field(min_length=1)
    content_sha256: Sha256

    @field_validator("relative_path")
    @classmethod
    def require_relative_path(cls, value: str) -> str:
        if value.startswith("/") or "\\" in value or any(part == ".." for part in value.split("/")):
            raise ValueError("path must be project-relative")
        return value


class RecordValidationError(ValueError):
    def __init__(self, reason_code: ReasonCode, message: str = "record validation failed") -> None:
        self.reason_code = reason_code
        super().__init__(message)


def _json_ready(value: object) -> object:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    return value


def canonical_json_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            _json_ready(value),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise RecordValidationError(ReasonCode.INVALID_RECORD) from exc


def content_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def model_facing_json(value: object, *, protected_values: tuple[str, ...] = ()) -> str:
    encoded = canonical_json_bytes(value).decode("utf-8")
    if any(secret and secret in encoded for secret in protected_values):
        raise RecordValidationError(
            ReasonCode.PROTECTED_PAYLOAD, "protected content cannot be model-facing"
        )
    return encoded


def load_record[T: BaseModel](path: Path, record_type: type[T]) -> T:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict) and raw.get("schema_version") != 1:
            raise RecordValidationError(ReasonCode.UNKNOWN_VERSION)
        return record_type.model_validate(raw)
    except RecordValidationError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValidationError, TypeError) as exc:
        raise RecordValidationError(ReasonCode.INVALID_RECORD) from exc


class AppendOnlyEventStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def append(self, event: AppendOnlyEvent) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        destination = self.root / f"{event.event_id}.json"
        try:
            with destination.open("xb") as stream:
                stream.write(canonical_json_bytes(event))
                stream.write(b"\n")
        except FileExistsError as exc:
            raise ValueError("append collision") from exc
        return destination

    def overwrite(self, event: AppendOnlyEvent) -> None:
        del event
        raise ValueError("overwrite attempt")


__all__ = [
    "AppendOnlyEvent",
    "AppendOnlyEventStore",
    "DecisionStatus",
    "Identity",
    "ProtectedRootReference",
    "ReasonCode",
    "RecordValidationError",
    "VersionedRecord",
    "canonical_json_bytes",
    "content_sha256",
    "load_record",
    "model_facing_json",
]
