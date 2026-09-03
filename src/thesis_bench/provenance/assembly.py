from __future__ import annotations

from datetime import UTC, datetime

from ..config import ValidatedConfiguration
from ..errors import PreparationError
from ..schemas import DatasetMetadata, EvaluationMetadata, HardwareMetadata, ModelMetadata
from .models import (
    GitProvenance,
    Manifest,
    ManifestEnvironment,
    ManifestGit,
    ManifestHashes,
    ManifestMetadata,
    ManifestSource,
    RuntimeEnvironment,
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
