from __future__ import annotations

from pathlib import Path

from ..errors import ConfigurationError
from ..schemas import ExperimentMetadata
from .identity import semantic_sha256, source_sha256
from .models import SourceIdentity, ValidatedConfiguration
from .paths import _relative_to_root, _resolve_reference, discover_project_root
from .validation import validate_document
from .yaml_source import _REFERENCE_KINDS, _load_yaml_source


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
