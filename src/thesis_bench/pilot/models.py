from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic.types import StrictBool

from ..records import ProtectedRootReference, VersionedRecord
from ..schemas import Identifier, NonBlankStr

_APPROVED_CONDITIONS = frozenset({"B0", "P1", "P2", "R1", "F1", "H1", "S1", "C1", "C2", "W1"})


class TaskClass(StrEnum):
    KNOWLEDGE = "knowledge"
    PROCEDURAL = "procedural"
    MIXED = "mixed"


class Language(StrEnum):
    PL = "pl"
    EN = "en"


class VariantType(StrEnum):
    LANGUAGE = "language"
    STATIC_INTERACTIVE = "static_interactive"
    PROMPT_FORMULATION = "prompt_formulation"
    REPEAT = "repeat"


class AnswerContract(VersionedRecord):
    form: Identifier
    deterministic_gates: tuple[Identifier, ...] = Field(min_length=1)
    candidate_primary_metric: Identifier


class MetricApplicability(VersionedRecord):
    applicable_metrics: tuple[Identifier, ...] = Field(min_length=1)
    inapplicable_metrics: tuple[Identifier, ...] = ()
    inapplicability_reasons: dict[Identifier, NonBlankStr] = {}

    @model_validator(mode="after")
    def require_reasons_for_inapplicable_metrics(self) -> MetricApplicability:
        missing = set(self.inapplicable_metrics) - set(self.inapplicability_reasons)
        if missing:
            raise ValueError("inapplicable metrics require reasons")
        if set(self.applicable_metrics) & set(self.inapplicable_metrics):
            raise ValueError("metric cannot be both applicable and inapplicable")
        return self


class ProtectedArtifactReference(VersionedRecord):
    artifact_id: Identifier
    artifact_kind: Literal[
        "evidence",
        "expected_result",
        "rubric",
        "golden",
        "adjudication",
        "fixture",
        "evaluator",
    ]
    root_reference: ProtectedRootReference


class TargetStratumRecord(VersionedRecord):
    stratum_id: Identifier
    conditions: tuple[NonBlankStr, ...] = Field(min_length=1)
    selection_rule: NonBlankStr
    policy_version: Literal["pilot-policy-v1"] = "pilot-policy-v1"


class ComparatorRecord(VersionedRecord):
    comparator_id: Identifier
    condition: NonBlankStr
    design_rule: NonBlankStr
    policy_version: Literal["pilot-policy-v1"] = "pilot-policy-v1"


class ConditionAnalysisContract(VersionedRecord):
    condition: NonBlankStr
    target_stratum: TargetStratumRecord
    comparators: tuple[ComparatorRecord, ...] = Field(min_length=1)


class ConditionApplicability(VersionedRecord):
    condition: NonBlankStr
    applicable: StrictBool
    reason: NonBlankStr | None = None

    @model_validator(mode="after")
    def require_explicit_applicability_reason(self) -> ConditionApplicability:
        if self.applicable and self.reason is not None:
            raise ValueError("applicable conditions cannot have an inapplicability reason")
        if not self.applicable and self.reason is None:
            raise ValueError("inapplicable conditions require a reason")
        return self


TargetStratum = TargetStratumRecord

Comparator = ComparatorRecord


class FamilyRecord(VersionedRecord):
    family_id: Identifier
    split: Literal["development"]
    task_class: TaskClass
    language: Language
    answer_contract: AnswerContract
    metric_applicability: MetricApplicability
    target_stratum: TargetStratumRecord
    comparator: ComparatorRecord
    condition_applicability: tuple[ConditionApplicability, ...] = Field(min_length=1)
    analysis_contracts: tuple[ConditionAnalysisContract, ...] = Field(min_length=1)
    evaluator_references: tuple[ProtectedArtifactReference, ...] = Field(min_length=1)

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value

    @property
    def applicable_conditions(self) -> tuple[str, ...]:
        return tuple(
            declaration.condition
            for declaration in self.condition_applicability
            if declaration.applicable
        )

    @model_validator(mode="after")
    def require_frozen_family_contract(self) -> FamilyRecord:
        primary = self.answer_contract.candidate_primary_metric
        if primary not in self.metric_applicability.applicable_metrics:
            raise ValueError("candidate primary metric must be applicable")
        declarations = self.condition_applicability
        condition_ids = tuple(declaration.condition for declaration in declarations)
        if len(set(condition_ids)) != len(condition_ids):
            raise ValueError("condition applicability identifiers must be unique")
        if set(condition_ids) != _APPROVED_CONDITIONS:
            raise ValueError("condition applicability must cover the approved condition matrix")
        applicable = set(self.applicable_conditions)
        if not applicable:
            raise ValueError("family must declare an applicable condition")
        if not set(self.target_stratum.conditions) <= applicable:
            raise ValueError("target stratum must reference applicable conditions")
        contracts_by_condition = {
            contract.condition: contract for contract in self.analysis_contracts
        }
        if len(contracts_by_condition) != len(self.analysis_contracts):
            raise ValueError("condition analysis contracts must be unique")
        if set(contracts_by_condition) != applicable:
            raise ValueError("every applicable condition requires an analysis contract")
        if self.comparator.condition != self.comparator.condition.strip():
            raise ValueError("comparator condition must be canonical")
        for condition, contract in contracts_by_condition.items():
            if contract.target_stratum != self.target_stratum:
                raise ValueError("analysis contract target stratum must be frozen at family level")
            comparator_conditions = {comparator.condition for comparator in contract.comparators}
            if condition == "B0" and comparator_conditions != {"B0"}:
                raise ValueError("B0 comparator must use the frozen self-reference")
            if condition in {"P1", "F1"} and comparator_conditions != {"B0"}:
                raise ValueError("condition comparator must match the approved matrix")
            if condition == "P2" and comparator_conditions != {"P1", "B0"}:
                raise ValueError("P2 requires P1 and B0 comparators")
            if condition == "R1" and comparator_conditions != {"matched-no-retrieval", "B0"}:
                raise ValueError("R1 requires matched no-retrieval and B0 comparators")
            if condition == "H1" and comparator_conditions != {"B0-I"}:
                raise ValueError("H1 requires the B0-I comparator")
            if condition == "S1" and comparator_conditions != {"H1"}:
                raise ValueError("S1 requires the H1 comparator")
            if condition == "W1" and comparator_conditions != {"B0", "R1"}:
                raise ValueError("W1 requires B0 and R1 comparators")
            if condition in {"C1", "C2"}:
                if len(contract.comparators) != 1:
                    raise ValueError("combined conditions require one strongest constituent")
                comparator = contract.comparators[0]
                allowed_constituents = (
                    {"P1", "R1"}
                    if condition == "C1"
                    else {
                        "P1",
                        "R1",
                        "H1",
                        "S1",
                    }
                )
                if comparator.condition not in allowed_constituents:
                    raise ValueError("combined condition comparator must be a constituent")
                if comparator.design_rule != "strongest-constituent-v1":
                    raise ValueError("combined condition comparator must use strongest constituent")
        if not any(
            self.comparator == comparator
            for contract in self.analysis_contracts
            for comparator in contract.comparators
        ):
            raise ValueError("family comparator must be one of its frozen analysis contracts")
        return self


class VariantRecord(VersionedRecord):
    variant_id: Identifier
    family_id: Identifier
    split: Literal["development"]
    variant_type: VariantType
    repeat_index: int = Field(default=0, ge=0)
    counts_as_independent: StrictBool = False

    @field_validator("variant_type", mode="before")
    @classmethod
    def parse_variant_type(cls, value: object) -> object:
        return VariantType(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_nested_counting(self) -> VariantRecord:
        if self.counts_as_independent:
            raise ValueError("nested variants cannot count as independent families")
        return self


class PilotManifest(VersionedRecord):
    manifest_id: Identifier
    policy_version: Identifier
    families: tuple[FamilyRecord, ...] = Field(min_length=1)
    variants: tuple[VariantRecord, ...] = ()

    @model_validator(mode="after")
    def validate_identity_and_nesting(self) -> PilotManifest:
        if self.policy_version != "pilot-policy-v1":
            raise ValueError("unknown pilot policy version")
        family_ids = [family.family_id for family in self.families]
        if len(set(family_ids)) != len(family_ids):
            raise ValueError("family identifiers must be unique")
        variant_ids = [variant.variant_id for variant in self.variants]
        if len(set(variant_ids)) != len(variant_ids):
            raise ValueError("variant identifiers must be unique")
        family_set = set(family_ids)
        if any(variant.family_id not in family_set for variant in self.variants):
            raise ValueError("variant must reference a manifest family")
        return self
