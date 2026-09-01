from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator
from pydantic.types import StrictInt, StrictStr

Identifier = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[a-z0-9][a-z0-9._-]{0,127}$"),
]
Sha256 = Annotated[str, StringConstraints(strict=True, pattern=r"^[0-9a-f]{64}$")]


class StrictDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    schema_version: Literal[1]
    kind: StrictStr
    id: Identifier


class Reference(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    path: StrictStr = Field(min_length=1)
    expected_id: Identifier


class ModelMetadata(StrictDocument):
    kind: Literal["model"]
    repository: StrictStr = Field(min_length=1)
    revision: StrictStr = Field(min_length=1)
    artifact_filename: StrictStr = Field(min_length=1)
    artifact_sha256: Sha256
    quantization: StrictStr = Field(min_length=1)
    license_id: StrictStr = Field(min_length=1)
    chat_template_id: StrictStr = Field(min_length=1)

    @field_validator("revision")
    @classmethod
    def require_immutable_revision(cls, value: str) -> str:
        if not value.strip() or value.strip().lower() in {"latest", "main", "master"}:
            raise ValueError("revision must be immutable")
        return value


class HardwareMetadata(StrictDocument):
    kind: Literal["hardware"]
    profile: StrictStr = Field(min_length=1)
    operating_system: StrictStr = Field(min_length=1)
    cpu: StrictStr = Field(min_length=1)
    ram_gb: StrictInt = Field(gt=0)
    gpu: StrictStr = Field(min_length=1)
    vram_gb: StrictInt = Field(gt=0)


class DatasetMetadata(StrictDocument):
    kind: Literal["dataset"]
    dataset: StrictStr = Field(min_length=1)
    revision: StrictStr = Field(min_length=1)
    split: StrictStr = Field(min_length=1)
    manifest_sha256: Sha256

    @field_validator("revision")
    @classmethod
    def require_immutable_revision(cls, value: str) -> str:
        if not value.strip() or value.strip().lower() in {"latest", "main", "master"}:
            raise ValueError("revision must be immutable")
        return value


class EvaluationMetadata(StrictDocument):
    kind: Literal["evaluation"]
    evaluator: StrictStr = Field(min_length=1)
    version: StrictStr = Field(min_length=1)
    metrics: list[Identifier] = Field(min_length=1)

    @field_validator("version")
    @classmethod
    def require_immutable_version(cls, value: str) -> str:
        if not value.strip() or value.strip().lower() in {"latest", "main", "master"}:
            raise ValueError("version must be immutable")
        return value

    @field_validator("metrics", mode="before")
    @classmethod
    def require_list(cls, value: object) -> object:
        if not isinstance(value, list):
            raise ValueError("metrics must be a list")
        return value


class ExperimentMetadata(StrictDocument):
    kind: Literal["experiment"]
    condition_id: Identifier
    run_kind: Literal["exploratory", "formal"]
    random_seed: StrictInt | None = None
    model: Reference
    hardware: Reference
    dataset: Reference
    evaluation: Reference


type MetadataDocument = (
    ExperimentMetadata | ModelMetadata | HardwareMetadata | DatasetMetadata | EvaluationMetadata
)
