from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator
from pydantic.types import StrictInt, StrictStr

from . import __version__
from .config import ValidatedConfiguration
from .errors import IntegrityError, PreparationError
from .schemas import (
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


def _run_git(arguments: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PreparationError(
            "git_unavailable", "required Git information is unavailable"
        ) from exc


def capture_git(project_root: Path) -> GitProvenance:
    try:
        root_result = _run_git(["rev-parse", "--show-toplevel"], project_root)
    except PreparationError:
        raise
    discovered_root = Path(root_result.stdout.strip()).resolve()
    expected_root = project_root.resolve()
    if discovered_root != expected_root:
        raise PreparationError("git_root_mismatch", "Git root does not match the project root")
    try:
        commit_result = _run_git(["rev-parse", "--verify", "HEAD^{commit}"], project_root)
    except PreparationError as exc:
        raise PreparationError(
            "git_commit_missing", "Git HEAD does not resolve to a commit"
        ) from exc
    commit = commit_result.stdout.strip()
    if len(commit) != 40 or any(character not in "0123456789abcdef" for character in commit):
        raise PreparationError("git_commit_missing", "Git HEAD does not resolve to a full commit")
    branch_result = _run_git(["branch", "--show-current"], project_root)
    status_result = _run_git(["status", "--porcelain=v1", "--untracked-files=all"], project_root)
    branch = branch_result.stdout.strip() or None
    return GitProvenance(
        root=expected_root,
        commit=commit,
        branch=branch,
        clean=status_result.stdout == "",
    )


def capture_environment() -> RuntimeEnvironment:
    return RuntimeEnvironment(
        platform=platform.platform(),
        machine=platform.machine(),
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        package_version=__version__,
    )


def _source(configuration: ValidatedConfiguration, kind: str) -> ManifestSource:
    identity = configuration.metadata[kind]
    return ManifestSource(
        path=identity.path,
        source_sha256=identity.source_sha256,
        semantic_sha256=identity.semantic_sha256,
    )


def build_manifest(
    configuration: ValidatedConfiguration,
    *,
    run_id: str,
    git: GitProvenance,
    environment: RuntimeEnvironment,
    prepared_at: datetime | None = None,
) -> Manifest:
    if not git.clean:
        raise PreparationError("git_dirty", "run preparation requires a clean Git worktree")
    timestamp = prepared_at or datetime.now(UTC)
    model_document = configuration.metadata["model"].document
    hardware_document = configuration.metadata["hardware"].document
    dataset_document = configuration.metadata["dataset"].document
    evaluation_document = configuration.metadata["evaluation"].document
    assert isinstance(model_document, ModelMetadata)
    assert isinstance(hardware_document, HardwareMetadata)
    assert isinstance(dataset_document, DatasetMetadata)
    assert isinstance(evaluation_document, EvaluationMetadata)
    return Manifest(
        schema_version=1,
        run_id=run_id,
        experiment_id=configuration.experiment.id,
        condition_id=configuration.experiment.condition_id,
        run_kind=configuration.experiment.run_kind,
        random_seed=configuration.experiment.random_seed,
        prepared_at=timestamp,
        package_version=environment.package_version,
        experiment_source_path=configuration.experiment_source_path,
        configuration_hashes=ManifestHashes(
            experiment=_source(configuration, "experiment"),
            model=_source(configuration, "model"),
            hardware=_source(configuration, "hardware"),
            dataset=_source(configuration, "dataset"),
            evaluation=_source(configuration, "evaluation"),
        ),
        metadata=ManifestMetadata(
            experiment=configuration.experiment,
            model=model_document,
            hardware=hardware_document,
            dataset=dataset_document,
            evaluation=evaluation_document,
        ),
        git=ManifestGit(root=".", commit=git.commit, branch=git.branch, clean=True),
        environment=ManifestEnvironment(
            platform=environment.platform,
            machine=environment.machine,
            python_implementation=environment.python_implementation,
            python_version=environment.python_version,
            package_version=environment.package_version,
        ),
    )


def _canonical_manifest_bytes(manifest: Manifest) -> bytes:
    try:
        text = json.dumps(
            manifest.model_dump(mode="json"),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise IntegrityError("invalid_manifest", "manifest cannot be canonicalized") from exc
    return text.encode("utf-8") + b"\n"


def manifest_to_bytes(manifest: Manifest) -> bytes:
    return _canonical_manifest_bytes(manifest)


def manifest_semantic_sha256(manifest: Manifest) -> str:
    return hashlib.sha256(_canonical_manifest_bytes(manifest)[:-1]).hexdigest()


def load_manifest(source: bytes) -> Manifest:
    try:
        manifest = Manifest.model_validate_json(source)
    except (ValueError, ValidationError) as exc:
        raise IntegrityError("invalid_manifest", "stored manifest is invalid") from exc
    return manifest
