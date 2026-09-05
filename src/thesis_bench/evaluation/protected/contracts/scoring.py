from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic.types import StrictFloat

from ....pilot.models import TaskClass
from ....schemas import Identifier
from .records import _ProtectedRecord


class KnowledgeScoreConfiguration(_ProtectedRecord):
    task_class: Literal[TaskClass.KNOWLEDGE] = TaskClass.KNOWLEDGE
    required_criterion_ids: tuple[Identifier, ...] = Field(min_length=1)
    unsupported_criterion_ids: tuple[Identifier, ...] = ()

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_unique_knowledge_criteria(self) -> KnowledgeScoreConfiguration:
        identifiers = (*self.required_criterion_ids, *self.unsupported_criterion_ids)
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("knowledge score criterion identifiers must be unique")
        return self


class ProceduralScoreConfiguration(_ProtectedRecord):
    task_class: Literal[TaskClass.PROCEDURAL] = TaskClass.PROCEDURAL
    primary_required_criterion_ids: tuple[Identifier, ...] = Field(min_length=1)
    primary_prohibited_criterion_ids: tuple[Identifier, ...] = ()

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_unique_procedural_criteria(self) -> ProceduralScoreConfiguration:
        identifiers = (
            *self.primary_required_criterion_ids,
            *self.primary_prohibited_criterion_ids,
        )
        if len(set(identifiers)) != len(identifiers):
            raise ValueError("procedural score criterion identifiers must be unique")
        return self


class MixedScoreConfiguration(_ProtectedRecord):
    task_class: Literal[TaskClass.MIXED] = TaskClass.MIXED
    primary_hard_gate_criterion_ids: tuple[Identifier, ...] = Field(min_length=1)
    point_table: dict[Identifier, StrictFloat] = Field(min_length=1)
    positive_maximum: StrictFloat = Field(gt=0.0)

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @model_validator(mode="after")
    def validate_point_table(self) -> MixedScoreConfiguration:
        if any(value <= 0 for value in self.point_table.values()):
            raise ValueError("mixed point table values must be positive")
        if len(set(self.primary_hard_gate_criterion_ids)) != len(
            self.primary_hard_gate_criterion_ids
        ):
            raise ValueError("mixed hard-gate criterion identifiers must be unique")
        if self.positive_maximum < sum(self.point_table.values()):
            raise ValueError("mixed positive maximum cannot be below its point table")
        return self


__all__ = [
    "KnowledgeScoreConfiguration",
    "MixedScoreConfiguration",
    "ProceduralScoreConfiguration",
]
