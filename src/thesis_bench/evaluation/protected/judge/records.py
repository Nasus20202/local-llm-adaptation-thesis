from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import ConfigDict, Field, field_validator, model_validator
from pydantic.types import StrictBool, StrictFloat, StrictInt

from ....pilot.models import Language, TaskClass
from ....records import DecisionStatus, ProtectedRootReference, VersionedRecord
from ....schemas import Identifier, Sha256
from ..contracts.config import ProtectedSemanticContract
from ..scoring.assessment import CriterionAssessment
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path


class DecodingPolicy(VersionedRecord):
    temperature: StrictFloat = Field(ge=0.0)
    top_p: StrictFloat = Field(gt=0.0, le=1.0)
    max_output_tokens: StrictInt = Field(gt=0)
    max_retries: StrictInt = Field(ge=0)
    failure_policy: Literal["route_to_human", "fail_closed"]


class JudgeResponseSchema(VersionedRecord):
    schema_id: Identifier
    schema_version_id: Identifier
    schema_sha256: Sha256


class QualificationThresholds(VersionedRecord):
    threshold_set_id: Identifier
    minimum_criterion_agreement: StrictFloat | None = Field(default=None, ge=0.0, le=1.0)
    minimum_kappa: StrictFloat | None = Field(default=None, ge=-1.0, le=1.0)
    maximum_unresolved_rate: StrictFloat | None = Field(default=None, ge=0.0, le=1.0)

    @property
    def is_frozen(self) -> bool:
        return all(
            value is not None
            for value in (
                self.minimum_criterion_agreement,
                self.maximum_unresolved_rate,
            )
        )


class AuditPolicy(VersionedRecord):
    audit_policy_id: Identifier
    sampling_identity: Identifier
    frozen_before_outcomes: Literal[True]
    blinded: Literal[True]


class JudgeScope(VersionedRecord):
    task_class: TaskClass
    language: Language
    criterion_ids: tuple[Identifier, ...] = Field(min_length=1)

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_unique_scope_criteria(self) -> JudgeScope:
        if len(set(self.criterion_ids)) != len(self.criterion_ids):
            raise ValueError("judge scope criterion identifiers must be unique")
        return self


class JudgeConfiguration(VersionedRecord):
    judge_config_id: Identifier
    revision: Identifier
    model_identity: Identifier
    provider_or_artifact_identity: Identifier
    backend_identity: Identifier
    prompt_template_identity: Identifier
    prompt_template_sha256: Sha256
    response_schema: JudgeResponseSchema
    decoding_policy: DecodingPolicy
    protected_input_contract_id: Identifier
    protected_input_contract_sha256: Sha256
    qualification_set_id: Identifier
    qualification_set_sha256: Sha256
    qualification_thresholds: QualificationThresholds
    audit_policy: AuditPolicy
    scopes: tuple[JudgeScope, ...] = Field(min_length=1)
    state: Literal["draft", "frozen", "superseded"]
    suspension_state: Literal["active", "suspended", "requalification_required"] = "active"
    suspension_reason: Identifier | None = None
    content_sha256: Sha256 | None = None
    supersedes_judge_config_id: Identifier | None = None

    @model_validator(mode="after")
    def require_suspension_reason(self) -> JudgeConfiguration:
        if self.suspension_state == "active" and self.suspension_reason is not None:
            raise ValueError("active judge configurations cannot carry a suspension reason")
        if self.suspension_state != "active" and self.suspension_reason is None:
            raise ValueError("suspended judge configurations require a reason")
        return self


class JudgeQualification(VersionedRecord):
    qualification_id: Identifier
    judge_config_id: Identifier
    judge_config_sha256: Sha256
    qualification_set_id: Identifier
    qualification_set_sha256: Sha256
    protected_input_contract_id: Identifier
    protected_input_contract_sha256: Sha256
    criterion_agreement: dict[Identifier, StrictFloat]
    confusion_matrix: dict[Identifier, dict[str, dict[str, StrictInt]]]
    agreement_statistic: StrictFloat | None = None
    unresolved_count: StrictInt = Field(ge=0)
    schema_failure_count: StrictInt = Field(ge=0)
    fairness_status: DecisionStatus
    fairness_scope_status: dict[Identifier, DecisionStatus] = {}
    thresholds_satisfied: StrictBool
    status: DecisionStatus


class MetamorphicVariantKind(StrEnum):
    CONCISE_CORRECT_PARAPHRASE = "concise_correct_paraphrase"
    CORRECT_SOURCE_LIKE = "correct_source_like"
    ACCEPTED_SYNONYM_REORDERING = "accepted_synonym_reordering"
    LEXICALLY_SIMILAR_WRONG = "lexically_similar_wrong"
    PARTIAL_MISSING_CLAIM = "partial_missing_claim"
    IRRELEVANT_SOURCE_APPENDED = "irrelevant_source_appended"


class MetamorphicVariant(VersionedRecord):
    variant_id: Identifier
    kind: MetamorphicVariantKind

    @field_validator("kind", mode="before")
    @classmethod
    def parse_kind(cls, value: object) -> object:
        return MetamorphicVariantKind(value) if isinstance(value, str) else value


class MetamorphicFixtureGroup(VersionedRecord):
    group_id: Identifier
    task_class: TaskClass
    language: Language
    variant_ids: tuple[Identifier, ...] = Field(min_length=6)
    variants: tuple[MetamorphicVariant, ...] = Field(min_length=6)
    protected_fixture_reference: ProtectedRootReference

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_six_distinct_variants(self) -> MetamorphicFixtureGroup:
        if (
            len(self.variant_ids) != 6
            or len(set(self.variant_ids)) != 6
            or len(self.variants) != 6
            or len({variant.variant_id for variant in self.variants}) != 6
        ):
            raise ValueError("fairness fixture group must contain six distinct variants")
        if set(self.variant_ids) != {variant.variant_id for variant in self.variants}:
            raise ValueError("fairness fixture identifiers must bind their variants")
        if {variant.kind for variant in self.variants} != set(MetamorphicVariantKind):
            raise ValueError("fairness fixture group must cover all approved variant relations")
        if self.protected_fixture_reference.root_id != APPROVED_PROTECTED_ROOT:
            raise ValueError("fairness fixture must use the approved protected root")
        validate_protected_relative_path(self.protected_fixture_reference.relative_path)
        return self


class JudgeFairnessCase(VersionedRecord):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, hide_input_in_errors=True)

    case_id: Identifier
    scope_key: Identifier
    contract: ProtectedSemanticContract
    variants: dict[MetamorphicVariantKind, tuple[CriterionAssessment, ...]]
    affected_criterion_ids: dict[MetamorphicVariantKind, tuple[Identifier, ...]] = {}


class FairnessQualification(VersionedRecord):
    status: DecisionStatus
    violations: tuple[Identifier, ...] = ()


__all__ = [
    "AuditPolicy",
    "DecodingPolicy",
    "FairnessQualification",
    "JudgeConfiguration",
    "JudgeFairnessCase",
    "JudgeQualification",
    "JudgeResponseSchema",
    "JudgeScope",
    "MetamorphicFixtureGroup",
    "MetamorphicVariant",
    "MetamorphicVariantKind",
    "QualificationThresholds",
]
