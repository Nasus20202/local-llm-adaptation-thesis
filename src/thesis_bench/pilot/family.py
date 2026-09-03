from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator, model_validator

from ..records import VersionedRecord
from ..schemas import Identifier
from .models import (
    _APPROVED_CONDITIONS,
    _FROZEN_CONSTITUENT_ORDER,
    AnswerContract,
    ComparatorRecord,
    ConditionAnalysisContract,
    ConditionApplicability,
    Language,
    MetricApplicability,
    ProtectedArtifactReference,
    TargetStratumRecord,
    TaskClass,
)


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
                    {"P1", "R1"} if condition == "C1" else {"P1", "R1", "H1", "S1"}
                )
                if comparator.condition not in allowed_constituents:
                    raise ValueError("combined condition comparator must be a constituent")
                if comparator.design_rule != "strongest-constituent-v1":
                    raise ValueError("combined condition comparator must use strongest constituent")
                if len(comparator.selection_order) < 2:
                    raise ValueError("combined condition selector must include its constituents")
                if set(comparator.selection_order) - allowed_constituents:
                    raise ValueError(
                        "combined condition selector contains an unapproved constituent"
                    )
                expected_order = tuple(
                    candidate
                    for candidate in _FROZEN_CONSTITUENT_ORDER
                    if candidate in comparator.selection_order
                )
                if comparator.selection_order != expected_order:
                    raise ValueError("combined condition selector order is not frozen")
                if comparator.condition != expected_order[0]:
                    raise ValueError("combined condition comparator is not the frozen strongest")
        if not any(
            self.comparator == comparator
            for contract in self.analysis_contracts
            for comparator in contract.comparators
        ):
            raise ValueError("family comparator must be one of its frozen analysis contracts")
        return self
