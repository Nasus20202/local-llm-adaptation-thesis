from __future__ import annotations

from pydantic import model_validator
from pydantic.types import StrictBool

from ..records import DecisionStatus, ReasonCode, VersionedRecord
from ..schemas import Identifier, NonBlankStr, Sha256


class SourceDriftResult(VersionedRecord):
    frozen_hash: Sha256
    current_hash: Sha256
    source_available: StrictBool
    reviewer_id: Identifier
    semantic_compatible: StrictBool
    rationale: NonBlankStr
    status: DecisionStatus
    reason_code: ReasonCode

    @model_validator(mode="after")
    def require_semantic_status_consistency(self) -> SourceDriftResult:
        expected_status = self.source_available and self.semantic_compatible
        if (self.status == DecisionStatus.GO) != expected_status:
            raise ValueError("source drift status must reflect reviewed semantic compatibility")
        return self


def source_drift_precheck(
    *,
    frozen_hash: str,
    current_hash: str,
    source_available: bool,
    reviewer_id: str,
    semantic_compatible: bool,
    rationale: str,
) -> SourceDriftResult:
    if not reviewer_id or not rationale:
        raise ValueError("source drift requires reviewed evidence")
    compatible = source_available and semantic_compatible
    return SourceDriftResult(
        schema_version=1,
        frozen_hash=frozen_hash,
        current_hash=current_hash,
        source_available=source_available,
        reviewer_id=reviewer_id,
        semantic_compatible=semantic_compatible,
        rationale=rationale,
        status=DecisionStatus.GO if compatible else DecisionStatus.STOP_DEFER,
        reason_code=ReasonCode.OK if compatible else ReasonCode.SOURCE_DRIFT,
    )
