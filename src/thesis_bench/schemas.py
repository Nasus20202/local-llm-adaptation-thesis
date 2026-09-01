from __future__ import annotations

from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
)
from pydantic.types import StrictInt, StrictStr

Identifier = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[a-z0-9][a-z0-9._-]{0,127}$"),
]
Sha256 = Annotated[str, StringConstraints(strict=True, pattern=r"^[0-9a-f]{64}$")]


def _require_non_blank(value: str) -> str:
    if not value.strip():
        raise ValueError("value must not be blank")
    return value


NonBlankStr = Annotated[
    str,
    StringConstraints(strict=True, min_length=1),
    AfterValidator(_require_non_blank),
]


class StrictDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    schema_version: Literal[1]
    kind: StrictStr
    id: Identifier


class Reference(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    path: NonBlankStr
    expected_id: Identifier


class ModelMetadata(StrictDocument):
    kind: Literal["model"]
    repository: NonBlankStr
    revision: NonBlankStr
    artifact_filename: NonBlankStr
    artifact_sha256: Sha256
    quantization: NonBlankStr
    license_id: NonBlankStr
    chat_template_id: NonBlankStr

    @field_validator("revision")
    @classmethod
    def require_immutable_revision(cls, value: str) -> str:
        if not value.strip() or value.strip().lower() in {"latest", "main", "master"}:
            raise ValueError("revision must be immutable")
        return value


class HardwareMetadata(StrictDocument):
    kind: Literal["hardware"]
    profile: NonBlankStr
    operating_system: NonBlankStr
    cpu: NonBlankStr
    ram_gb: StrictInt = Field(gt=0)
    gpu: NonBlankStr
    vram_gb: StrictInt = Field(gt=0)


class DatasetMetadata(StrictDocument):
    kind: Literal["dataset"]
    dataset: NonBlankStr
    revision: NonBlankStr
    split: NonBlankStr
    manifest_sha256: Sha256

    @field_validator("revision")
    @classmethod
    def require_immutable_revision(cls, value: str) -> str:
        if not value.strip() or value.strip().lower() in {"latest", "main", "master"}:
            raise ValueError("revision must be immutable")
        return value


class EvaluationMetadata(StrictDocument):
    kind: Literal["evaluation"]
    evaluator: NonBlankStr
    version: NonBlankStr
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
