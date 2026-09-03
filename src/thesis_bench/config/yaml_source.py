from __future__ import annotations

from pathlib import Path

import yaml  # type: ignore[import-untyped]

from ..errors import ConfigurationError
from ..schemas import (
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
