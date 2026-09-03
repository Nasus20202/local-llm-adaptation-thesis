from __future__ import annotations

from enum import StrEnum
from typing import Literal

from ..records import DecisionStatus, VersionedRecord
from ..schemas import Identifier, NonBlankStr


class AuditMethod(StrEnum):
    EXACT = "exact"
    NORMALIZED = "normalized"
    TOKEN = "token"
    CODE_CONFIGURATION = "code/configuration"
    SEMANTIC = "semantic"
    CROSS_LANGUAGE = "cross-language"


class AuditOutcome(StrEnum):
    NO_MATCH = "no_match"
    MATCH = "match"
    UNRESOLVED = "unresolved"


class ContaminationAudit(VersionedRecord):
    audit_id: Identifier
    method: AuditMethod
    detector_version: Identifier
    artifact_pair: tuple[Identifier, Identifier]
    threshold: NonBlankStr
    outcome: AuditOutcome
    exposure_layer: Literal["source-domain", "semantic-pattern", "direct-item"]
    adjudication: Literal["not_applicable", "pending", "confirmed", "rejected"]
    parametric_exposure: Literal["unknown"] = "unknown"

    def progression_status(self) -> DecisionStatus:
        if self.exposure_layer == "direct-item" and self.outcome == AuditOutcome.MATCH:
            return DecisionStatus.STOP_DEFER
        if (
            self.exposure_layer == "semantic-pattern"
            and self.outcome == AuditOutcome.MATCH
            and self.adjudication == "pending"
        ):
            return DecisionStatus.AMEND
        if self.outcome == AuditOutcome.UNRESOLVED and self.exposure_layer == "semantic-pattern":
            return DecisionStatus.AMEND
        return DecisionStatus.GO
