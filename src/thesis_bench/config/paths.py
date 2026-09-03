from __future__ import annotations

import re
from pathlib import Path

from ..errors import ConfigurationError

_WINDOWS_PATH = re.compile(r"^[A-Za-z]:[\\/]|^\\\\")


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
