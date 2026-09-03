from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator
from pydantic.types import StrictBool, StrictStr

from ..records import VersionedRecord, content_sha256
from ..schemas import Identifier, NonBlankStr, Sha256
from .models import ComparatorRecord, Language, TaskClass


class C2EligibilityMetadata(VersionedRecord):
    task_classes: tuple[TaskClass, ...] = Field(min_length=1)
    languages: tuple[Language, ...] = Field(min_length=1)
    answer_contracts: tuple[Identifier, ...] = Field(min_length=1)
    required_capabilities: tuple[
        Literal[
            "prompt-control",
            "retrieval",
            "orchestration",
            "procedural-context",
            "web-search",
        ],
        ...,
    ] = Field(min_length=2)
    declared_needs: tuple[
        Literal["evidence", "interaction", "answer-contract", "state-validation"], ...
    ] = Field(min_length=1)
    target_stratum: Literal["mixed", "interactive"]


class C2FreezeIdentity(VersionedRecord):
    artifact_id: Identifier
    artifact_revision: Identifier
    content_sha256: Sha256
    stage: Literal["pre_outcome"]


class C2EligibilityManifest(VersionedRecord):
    eligibility_id: Identifier
    family_ids: tuple[Identifier, ...] = Field(min_length=2)
    metadata: C2EligibilityMetadata
    constituent_conditions: tuple[NonBlankStr, ...] = Field(min_length=2)
    comparator: ComparatorRecord
    freeze_identity: C2FreezeIdentity
    analysis_status: Literal["confirmatory", "exploratory"]
    outcome_derived_fields: tuple[StrictStr, ...] = ()
    confirmatory_follow_up: StrictBool = False
    excluded_family_ids: tuple[Identifier, ...] = ()
    exploratory_manifest_id: Identifier | None = None

    @model_validator(mode="after")
    def require_unique_family_and_constituent_ids(self) -> C2EligibilityManifest:
        if len(set(self.family_ids)) != len(self.family_ids):
            raise ValueError("C2 family identifiers must be unique")
        if len(set(self.constituent_conditions)) != len(self.constituent_conditions):
            raise ValueError("C2 constituent conditions must be unique")
        if not set(self.constituent_conditions) <= {"P1", "R1", "H1", "S1"}:
            raise ValueError("C2 constituent set contains an unapproved condition")
        if self.comparator.condition not in self.constituent_conditions:
            raise ValueError("C2 comparator must be one of the frozen constituents")
        if self.comparator.design_rule != "strongest-constituent-v1":
            raise ValueError("C2 comparator must use the approved design-time rule")
        if self.confirmatory_follow_up and not self.excluded_family_ids:
            raise ValueError("confirmatory follow-up requires an exploratory family set")
        if self.confirmatory_follow_up and self.exploratory_manifest_id is None:
            raise ValueError("confirmatory follow-up requires its exploratory manifest identity")
        if set(self.family_ids) & set(self.excluded_family_ids):
            raise ValueError("confirmatory C2 requires fresh family-disjoint families")
        if self.analysis_status == "confirmatory" and self.outcome_derived_fields:
            raise ValueError("confirmatory C2 cannot use outcome-derived eligibility")
        if self.analysis_status == "exploratory" and not self.outcome_derived_fields:
            raise ValueError("exploratory C2 requires an explicit exploratory reason")
        declaration_hash = content_sha256(
            {
                "declaration": self.model_dump(mode="json", exclude={"freeze_identity"}),
                "artifact_id": self.freeze_identity.artifact_id,
                "artifact_revision": self.freeze_identity.artifact_revision,
                "stage": self.freeze_identity.stage,
            }
        )
        if declaration_hash != self.freeze_identity.content_sha256:
            raise ValueError("C2 freeze identity does not bind the frozen declaration")
        return self

    @property
    def comparator_rule(self) -> str:
        return self.comparator.design_rule

    @property
    def freeze_stage(self) -> str:
        return self.freeze_identity.stage


def validate_c2_eligibility(
    manifest: C2EligibilityManifest,
) -> C2EligibilityManifest:
    try:
        parsed = C2EligibilityManifest.model_validate(manifest.model_dump(mode="python"))
    except ValueError as exc:
        raise ValueError("C2 eligibility validation failed") from exc
    if parsed.freeze_identity.stage != "pre_outcome":
        raise ValueError("C2 eligibility must be frozen before outcomes")
    return parsed
