from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic.types import StrictBool

from ..records import ProtectedRootReference, VersionedRecord
from ..schemas import Identifier, NonBlankStr

_APPROVED_CONDITIONS = frozenset({"B0", "P1", "P2", "R1", "F1", "H1", "S1", "C1", "C2", "W1"})
_FROZEN_CONSTITUENT_ORDER = ("P1", "R1", "H1", "S1")


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
    selection_order: tuple[NonBlankStr, ...] = ()
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
