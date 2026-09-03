from __future__ import annotations

from ..records import DecisionStatus, ReasonCode, VersionedRecord


class SourceDriftResult(VersionedRecord):
    status: DecisionStatus
    reason_code: ReasonCode


def source_drift_precheck(
    *, frozen_hash: str, current_hash: str, source_available: bool
) -> SourceDriftResult:
    if not source_available or frozen_hash != current_hash:
        return SourceDriftResult(
            schema_version=1, status=DecisionStatus.STOP_DEFER, reason_code=ReasonCode.SOURCE_DRIFT
        )
    return SourceDriftResult(schema_version=1, status=DecisionStatus.GO, reason_code=ReasonCode.OK)
