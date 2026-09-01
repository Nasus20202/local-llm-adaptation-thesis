from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml  # type: ignore[import-untyped]
from pydantic import ValidationError

from .errors import ConfigurationError
from .schemas import (
    DatasetMetadata,
    EvaluationMetadata,
    ExperimentMetadata,
    HardwareMetadata,
    MetadataDocument,
    ModelMetadata,
)

_MODELS: dict[str, type[MetadataDocument]] = {
    "experiment": ExperimentMetadata,
    "model": ModelMetadata,
    "hardware": HardwareMetadata,
    "dataset": DatasetMetadata,
    "evaluation": EvaluationMetadata,
}
_REFERENCE_KINDS = ("model", "hardware", "dataset", "evaluation")
_WINDOWS_PATH = re.compile(r"^[A-Za-z]:[\\/]|^\\\\")


class _DuplicateKeyError(yaml.YAMLError):  # type: ignore[misc]
    pass


class _InvalidMappingKeyError(yaml.YAMLError):  # type: ignore[misc]
    pass


class _UniqueKeyLoader(yaml.SafeLoader):  # type: ignore[misc]
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            is_duplicate = key in mapping
        except TypeError as exc:
            raise _InvalidMappingKeyError("YAML mapping keys must be hashable") from exc
        if is_duplicate:
            raise _DuplicateKeyError("duplicate YAML mapping key")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _load_yaml_source(path: Path) -> tuple[bytes, dict[str, object]]:
    try:
        source = path.read_bytes()
    except (FileNotFoundError, IsADirectoryError, PermissionError) as exc:
        raise ConfigurationError(
            "invalid_yaml", "metadata file cannot be read", location=str(path)
        ) from exc
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ConfigurationError(
            "invalid_yaml", "metadata file is not UTF-8", location=str(path)
        ) from exc
    try:
        document = yaml.load(text, Loader=_UniqueKeyLoader)
    except _DuplicateKeyError as exc:
        raise ConfigurationError(
            "invalid_yaml", "duplicate YAML mapping key", location=str(path)
        ) from exc
    except _InvalidMappingKeyError as exc:
        raise ConfigurationError(
            "invalid_yaml", "YAML mapping key must be hashable", location=str(path)
        ) from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(
            "invalid_yaml", "malformed YAML document", location=str(path)
        ) from exc
    if not isinstance(document, dict) or not all(isinstance(key, str) for key in document):
        raise ConfigurationError(
            "invalid_yaml", "metadata document must be a mapping", location=str(path)
        )
    return source, document


def load_yaml_document(path: Path) -> dict[str, object]:
    return _load_yaml_source(path)[1]


def canonical_json_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(
            "invalid_configuration", "metadata cannot be canonicalized"
        ) from exc


def source_sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def semantic_sha256(document: MetadataDocument) -> str:
    return hashlib.sha256(canonical_json_bytes(document.model_dump(mode="json"))).hexdigest()


def _safe_validation_error(path: Path, error: ValidationError) -> ConfigurationError:
    first = error.errors()[0]
    location = ".".join(str(part) for part in first.get("loc", ())) or str(path)
    error_type = first.get("type")
    if error_type == "extra_forbidden":
        message = "unknown field"
    elif error_type == "missing":
        message = "required field is missing"
    elif error_type == "literal_error" and location == "schema_version":
        message = "unsupported schema version"
    else:
        message = "invalid field"
    return ConfigurationError("invalid_configuration", message, location=f"{path}:{location}")


def validate_document(
    raw: dict[str, object], path: Path, expected_kind: str | None = None
) -> MetadataDocument:
    kind = raw.get("kind")
    if not isinstance(kind, str) or kind not in _MODELS:
        raise ConfigurationError(
            "invalid_configuration", "unknown metadata kind", location=str(path)
        )
    if expected_kind is not None and kind != expected_kind:
        raise ConfigurationError(
            "invalid_configuration",
            "metadata kind does not match reference",
            location=f"{path}:kind",
        )
    model = _MODELS[kind]
    try:
        return model.model_validate(raw)
    except ValidationError as exc:
        raise _safe_validation_error(path, exc) from exc


@dataclass(frozen=True)
class SourceIdentity:
    path: str
    document: MetadataDocument
    source_sha256: str
    semantic_sha256: str


@dataclass(frozen=True)
class ValidatedConfiguration:
    project_root: Path
    experiment_path: Path
    experiment: ExperimentMetadata
    metadata: dict[str, SourceIdentity]

    @property
    def experiment_source_path(self) -> str:
        return self.metadata["experiment"].path


def discover_project_root(start: Path) -> Path:
    start = start.resolve()
    directory = start if start.is_dir() else start.parent
    for candidate in (directory, *directory.parents):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "openspec/config.yaml"
        ).is_file():
            return candidate
    raise ConfigurationError("project_root_not_found", "project root markers were not found")


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError as exc:
        raise ConfigurationError(
            "unsafe_reference", "path is outside the project root", location=str(path)
        ) from exc


def _resolve_reference(reference_path: str, *, experiment_path: Path, project_root: Path) -> Path:
    if (
        not reference_path
        or Path(reference_path).is_absolute()
        or _WINDOWS_PATH.match(reference_path)
        or "://" in reference_path
    ):
        raise ConfigurationError(
            "unsafe_reference", "reference path is not a contained relative path"
        )
    if Path(reference_path).suffix.lower() not in {".yaml", ".yml"}:
        raise ConfigurationError("unsafe_reference", "reference path must be a YAML file")
    candidate = experiment_path.parent / reference_path
    try:
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        raise ConfigurationError(
            "unsafe_reference", "referenced metadata file cannot be resolved"
        ) from exc
    _relative_to_root(resolved, project_root)
    if not resolved.is_file():
        raise ConfigurationError(
            "unsafe_reference", "referenced metadata path is not a regular file"
        )
    return resolved


def load_configuration(experiment_path: Path) -> ValidatedConfiguration:
    try:
        resolved_experiment = experiment_path.resolve(strict=True)
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        raise ConfigurationError(
            "invalid_configuration",
            "experiment file cannot be resolved",
            location=str(experiment_path),
        ) from exc
    if not resolved_experiment.is_file():
        raise ConfigurationError("invalid_configuration", "experiment path is not a file")
    project_root = discover_project_root(resolved_experiment)
    experiment_relative_path = _relative_to_root(resolved_experiment, project_root)
    experiment_source, raw_experiment = _load_yaml_source(resolved_experiment)
    experiment = validate_document(raw_experiment, resolved_experiment, expected_kind="experiment")
    assert isinstance(experiment, ExperimentMetadata)
    identities: dict[str, SourceIdentity] = {
        "experiment": SourceIdentity(
            path=experiment_relative_path,
            document=experiment,
            source_sha256=source_sha256(experiment_source),
            semantic_sha256=semantic_sha256(experiment),
        )
    }
    for kind in _REFERENCE_KINDS:
        reference = getattr(experiment, kind)
        resolved_reference = _resolve_reference(
            reference.path,
            experiment_path=resolved_experiment,
            project_root=project_root,
        )
        source, raw_document = _load_yaml_source(resolved_reference)
        document = validate_document(raw_document, resolved_reference, expected_kind=kind)
        if document.id != reference.expected_id:
            raise ConfigurationError(
                "invalid_configuration",
                "referenced metadata identifier mismatch: "
                f"expected {reference.expected_id}, found {document.id}",
                location=f"{resolved_reference}:id",
            )
        identities[kind] = SourceIdentity(
            path=_relative_to_root(resolved_reference, project_root),
            document=document,
            source_sha256=source_sha256(source),
            semantic_sha256=semantic_sha256(document),
        )
    return ValidatedConfiguration(
        project_root=project_root,
        experiment_path=resolved_experiment,
        experiment=experiment,
        metadata=identities,
    )
