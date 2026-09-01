from __future__ import annotations

import os
import shutil
import tempfile
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from .config import ValidatedConfiguration
from .errors import (
    CollisionError,
    ConfigurationError,
    IntegrityError,
    PreparationError,
    ThesisBenchError,
)
from .provenance import (
    GitProvenance,
    Manifest,
    RuntimeEnvironment,
    build_manifest,
    capture_environment,
    capture_git,
    load_manifest,
    manifest_semantic_sha256,
    manifest_to_bytes,
)


def generate_run_id(
    *,
    now_source: Callable[[], datetime] | None = None,
    uuid_source: Callable[[], uuid.UUID] | None = None,
) -> str:
    now = (now_source or (lambda: datetime.now(UTC)))()
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    timestamp = now.astimezone(UTC).strftime("%Y%m%dt%H%M%S%fZ").lower()
    identifier = (uuid_source or uuid.uuid4)().hex[-12:]
    return f"{timestamp}-{identifier}"


def write_manifest(run_directory: Path, manifest: Manifest) -> None:
    target = run_directory / "manifest.json"
    if target.exists():
        raise CollisionError("manifest_exists", "manifest already exists", location="manifest.json")
    try:
        with target.open("xb") as stream:
            stream.write(manifest_to_bytes(manifest))
    except CollisionError:
        raise
    except OSError as exc:
        try:
            target.unlink(missing_ok=True)
        except OSError:
            pass
        raise PreparationError("manifest_write_failed", "manifest could not be written") from exc


def _publish(
    manifest: Manifest,
    results_root: Path,
    *,
    writer: Callable[[Path, Manifest], None] | None = None,
) -> Path:
    try:
        results_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise PreparationError(
            "results_root_unavailable", "results root could not be created"
        ) from exc
    final_directory = results_root / manifest.run_id
    if os.path.lexists(final_directory):
        raise CollisionError("run_exists", "run directory already exists", location=manifest.run_id)
    try:
        staging_directory = Path(
            tempfile.mkdtemp(prefix=f".{manifest.run_id}.staging-", dir=results_root)
        )
    except OSError as exc:
        raise PreparationError(
            "staging_failed", "run staging directory could not be created"
        ) from exc
    try:
        (writer or write_manifest)(staging_directory, manifest)
        if load_manifest((staging_directory / "manifest.json").read_bytes()) != manifest:
            raise PreparationError(
                "manifest_validation_failed", "written manifest failed validation"
            )
        if os.path.lexists(final_directory):
            raise CollisionError(
                "run_exists", "run directory already exists", location=manifest.run_id
            )
        os.rename(staging_directory, final_directory)
    except ThesisBenchError:
        shutil.rmtree(staging_directory, ignore_errors=True)
        raise
    except FileExistsError as exc:
        shutil.rmtree(staging_directory, ignore_errors=True)
        raise CollisionError(
            "run_exists", "run directory already exists", location=manifest.run_id
        ) from exc
    except OSError as exc:
        shutil.rmtree(staging_directory, ignore_errors=True)
        raise PreparationError("run_publish_failed", "run could not be published") from exc
    return final_directory


class PreparedRun:
    def __init__(self, path: Path, manifest: Manifest) -> None:
        self.path = path
        self.manifest = manifest
        self.run_id = manifest.run_id
        self.manifest_semantic_sha256 = manifest_semantic_sha256(manifest)


def prepare_run(
    configuration: ValidatedConfiguration,
    *,
    results_root: Path | None = None,
    now_source: Callable[[], datetime] | None = None,
    uuid_source: Callable[[], uuid.UUID] | None = None,
    git: GitProvenance | None = None,
    environment: RuntimeEnvironment | None = None,
) -> PreparedRun:
    git_provenance = capture_git(configuration.project_root) if git is None else git
    if not getattr(git_provenance, "clean", False):
        raise PreparationError("git_dirty", "run preparation requires a clean Git worktree")
    environment_provenance = environment or capture_environment()
    manifest = build_manifest(
        configuration,
        run_id=generate_run_id(now_source=now_source, uuid_source=uuid_source),
        git=git_provenance,
        environment=environment_provenance,
    )
    root = results_root or configuration.project_root / "results/raw"
    path = _publish(manifest, root)
    return PreparedRun(path, manifest)


def inspect_run(run_directory: Path) -> dict[str, str]:
    if not run_directory.exists():
        raise ConfigurationError("run_not_found", "run directory does not exist")
    if not run_directory.is_dir():
        raise IntegrityError("invalid_run", "run path is not a directory")
    manifest_path = run_directory / "manifest.json"
    if not manifest_path.is_file():
        raise IntegrityError("invalid_run", "run manifest is missing")
    try:
        source = manifest_path.read_bytes()
    except OSError as exc:
        raise IntegrityError("invalid_run", "run manifest cannot be read") from exc
    manifest = load_manifest(source)
    if source != manifest_to_bytes(manifest):
        raise IntegrityError("invalid_manifest", "stored manifest is not canonical")
    if manifest.run_id != run_directory.name:
        raise IntegrityError("run_id_mismatch", "run ID does not match its directory")
    return {
        "run_id": manifest.run_id,
        "experiment_id": manifest.experiment_id,
        "condition_id": manifest.condition_id,
        "run_kind": manifest.run_kind,
        "prepared_at": manifest.prepared_at.isoformat(),
        "git_commit": manifest.git.commit,
    }
