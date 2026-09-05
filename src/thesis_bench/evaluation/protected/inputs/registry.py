from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic.types import StrictInt

from ....pilot.models import Language, TaskClass
from ....records import VersionedRecord
from ....schemas import Identifier, Sha256
from ..source import protected_policy


class ApprovedInputBinding(VersionedRecord):
    family_id: Identifier
    scenario_input_id: Identifier
    input_sha256: Sha256
    task_class: TaskClass
    language: Language
    split: Literal["development"] = "development"

    @field_validator("task_class", mode="before")
    @classmethod
    def parse_task_class(cls, value: object) -> object:
        return TaskClass(value) if isinstance(value, str) else value

    @field_validator("language", mode="before")
    @classmethod
    def parse_language(cls, value: object) -> object:
        return Language(value) if isinstance(value, str) else value


class ApprovedInputRegistry(VersionedRecord):
    manifest_id: Identifier
    root_id: Identifier
    manifest_sha256: Sha256
    scenario_count: StrictInt = Field(gt=0)
    entries: tuple[ApprovedInputBinding, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_against_frozen_policy(self) -> ApprovedInputRegistry:
        if len(self.entries) != self.scenario_count:
            raise ValueError("approved input registry count does not match its entries")
        family_ids = [entry.family_id for entry in self.entries]
        input_ids = [entry.scenario_input_id for entry in self.entries]
        if len(set(family_ids)) != len(family_ids) or len(set(input_ids)) != len(input_ids):
            raise ValueError("approved input registry identifiers must be unique")
        configured = protected_policy().get("approved_input_manifest")
        if not isinstance(configured, Mapping):
            raise ValueError("approved input registry is unavailable")
        if any(
            self.model_dump(mode="json")[field] != configured.get(field)
            for field in ("manifest_id", "root_id", "manifest_sha256", "scenario_count")
        ):
            raise ValueError("approved input registry identity is not frozen")
        configured_entries = configured.get("entries")
        if not isinstance(configured_entries, (tuple, list)):
            raise ValueError("approved input registry entries are unavailable")
        expected = {
            entry["family_id"]: entry
            for entry in configured_entries
            if isinstance(entry, Mapping) and "family_id" in entry
        }
        if len(expected) != len(configured_entries) or set(expected) != set(family_ids):
            raise ValueError("approved input registry entries are not frozen")
        for entry in self.entries:
            configured_entry = expected.get(entry.family_id)
            if configured_entry is None or any(
                entry.model_dump(mode="json")[field]
                != configured_entry.get(field, "development" if field == "split" else None)
                for field in (
                    "family_id",
                    "scenario_input_id",
                    "input_sha256",
                    "task_class",
                    "language",
                    "split",
                )
            ):
                raise ValueError("approved input binding is not frozen")
        return self

    def binding_for(self, family_id: str) -> ApprovedInputBinding:
        for entry in self.entries:
            if entry.family_id == family_id:
                return entry
        raise ValueError("approved input registry does not contain the contract family")


def approved_input_registry() -> ApprovedInputRegistry:
    configured = protected_policy().get("approved_input_manifest")
    if not isinstance(configured, Mapping):
        raise ValueError("approved input registry is unavailable")
    entries = configured.get("entries")
    if not isinstance(entries, (tuple, list)):
        raise ValueError("approved input registry entries are unavailable")
    try:
        return ApprovedInputRegistry(
            schema_version=1,
            manifest_id=configured["manifest_id"],
            root_id=configured["root_id"],
            manifest_sha256=configured["manifest_sha256"],
            scenario_count=configured["scenario_count"],
            entries=tuple(
                ApprovedInputBinding(schema_version=1, **dict(entry))
                for entry in entries
                if isinstance(entry, Mapping)
            ),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("approved input registry is invalid") from exc


def validate_approved_input_registry(registry: ApprovedInputRegistry) -> ApprovedInputRegistry:
    try:
        return ApprovedInputRegistry.model_validate(registry.model_dump(mode="python"))
    except ValueError:
        raise ValueError("approved input registry is invalid") from None


__all__ = [
    "ApprovedInputBinding",
    "ApprovedInputRegistry",
    "approved_input_registry",
    "validate_approved_input_registry",
]
