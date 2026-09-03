from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic.types import StrictInt, StrictStr

from ..schemas import (
    DatasetMetadata,
    EvaluationMetadata,
    ExperimentMetadata,
    HardwareMetadata,
    ModelMetadata,
)

_COMMIT = Annotated[str, Field(pattern=r"^[0-9a-f]{40}$", strict=True)]

_RUN_ID = Annotated[
    str,
    Field(pattern=r"^[0-9]{8}t[0-9]{12}z-[0-9a-f]{12}$", strict=True),
]


@dataclass(frozen=True)
class GitProvenance:
    root: Path
    commit: str
    branch: str | None
    clean: bool


@dataclass(frozen=True)
class RuntimeEnvironment:
    platform: str
    machine: str
    python_implementation: str
    python_version: str
    package_version: str


class ManifestSource(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    path: StrictStr = Field(min_length=1)
    source_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$", strict=True)]
    semantic_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$", strict=True)]

    @field_validator("path")
    @classmethod
    def require_portable_path(cls, value: str) -> str:
        if value.startswith("/") or "\\" in value or any(part == ".." for part in value.split("/")):
            raise ValueError("path must be project-relative")
        return value


class ManifestHashes(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    experiment: ManifestSource
    model: ManifestSource
    hardware: ManifestSource
    dataset: ManifestSource
    evaluation: ManifestSource


class ManifestMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    experiment: ExperimentMetadata
    model: ModelMetadata
    hardware: HardwareMetadata
    dataset: DatasetMetadata
    evaluation: EvaluationMetadata


class ManifestGit(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    root: Literal["."]
    commit: _COMMIT
    branch: StrictStr | None = None
    clean: Literal[True]


class ManifestEnvironment(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    platform: StrictStr = Field(min_length=1)
    machine: StrictStr = Field(min_length=1)
    python_implementation: StrictStr = Field(min_length=1)
    python_version: StrictStr = Field(min_length=1)
    package_version: StrictStr = Field(min_length=1)


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    schema_version: Literal[1]
    run_id: _RUN_ID
    experiment_id: StrictStr = Field(min_length=1)
    condition_id: StrictStr = Field(min_length=1)
    run_kind: Literal["exploratory", "formal"]
    random_seed: StrictInt | None = None
    prepared_at: datetime
    package_version: StrictStr = Field(min_length=1)
    experiment_source_path: StrictStr = Field(min_length=1)
    configuration_hashes: ManifestHashes
    metadata: ManifestMetadata
    git: ManifestGit
    environment: ManifestEnvironment

    @field_validator("prepared_at")
    @classmethod
    def require_utc_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
            raise ValueError("prepared_at must be UTC")
        return value

    @field_validator("experiment_source_path")
    @classmethod
    def require_portable_experiment_path(cls, value: str) -> str:
        if value.startswith("/") or "\\" in value or any(part == ".." for part in value.split("/")):
            raise ValueError("path must be project-relative")
        return value

    @model_validator(mode="after")
    def validate_cross_references(self) -> Manifest:
        if self.configuration_hashes.experiment.path != self.experiment_source_path:
            raise ValueError("experiment source path does not match its identity")
        references = self.metadata.experiment
        for kind in ("model", "hardware", "dataset", "evaluation"):
            if getattr(references, kind).expected_id != getattr(self.metadata, kind).id:
                raise ValueError("experiment reference does not match manifest metadata")
        return self
