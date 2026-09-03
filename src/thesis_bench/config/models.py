from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..schemas import ExperimentMetadata, MetadataDocument


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
