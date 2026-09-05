from __future__ import annotations

from enum import StrEnum

from pydantic import ConfigDict, Field, field_validator, model_validator

from ....pilot.models import Language, TaskClass
from ....records import DecisionStatus, ProtectedRootReference, VersionedRecord
from ....schemas import Identifier
from ..contracts.config import (
    KnowledgeScoreConfiguration,
    MixedScoreConfiguration,
    ProceduralScoreConfiguration,
    ProtectedSemanticContract,
)
from ..scoring.assessment import CriterionAssessment
from ..source import APPROVED_PROTECTED_ROOT, validate_protected_relative_path


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
    contract: ProtectedSemanticContract
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
        if self.contract.task_class != self.task_class or self.contract.language != self.language:
            raise ValueError("fairness fixture contract scope does not match its group")
        return self

    def scoring_rule_ids(self) -> frozenset[str]:
        config = self.contract.score_configuration
        if self.task_class == TaskClass.KNOWLEDGE and isinstance(
            config, KnowledgeScoreConfiguration
        ):
            return frozenset(config.required_criterion_ids) | frozenset(
                config.unsupported_criterion_ids
            )
        if self.task_class == TaskClass.PROCEDURAL and isinstance(
            config, ProceduralScoreConfiguration
        ):
            return frozenset(config.primary_required_criterion_ids) | frozenset(
                config.primary_prohibited_criterion_ids
            )
        if self.task_class == TaskClass.MIXED and isinstance(config, MixedScoreConfiguration):
            return frozenset(config.primary_hard_gate_criterion_ids) | frozenset(config.point_table)
        raise ValueError("fairness fixture has an unsupported score configuration")


class JudgeFairnessCase(VersionedRecord):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True, hide_input_in_errors=True)

    case_id: Identifier
    scope_key: Identifier
    contract: ProtectedSemanticContract
    variants: dict[MetamorphicVariantKind, tuple[CriterionAssessment, ...]]

    @model_validator(mode="after")
    def require_complete_variants(self) -> JudgeFairnessCase:
        if set(self.variants) != set(MetamorphicVariantKind):
            raise ValueError("fairness case must provide every approved variant relation")
        return self

    def exercised_rule_ids(self) -> frozenset[str]:
        return frozenset(
            assessment.criterion_id
            for assessments in self.variants.values()
            for assessment in assessments
        )


class FairnessQualification(VersionedRecord):
    status: DecisionStatus
    violations: tuple[Identifier, ...] = ()


__all__ = [
    "FairnessQualification",
    "JudgeFairnessCase",
    "MetamorphicFixtureGroup",
    "MetamorphicVariant",
    "MetamorphicVariantKind",
]
