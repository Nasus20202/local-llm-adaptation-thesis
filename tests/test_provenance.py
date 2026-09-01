from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pytest

from thesis_bench.errors import IntegrityError, PreparationError
from thesis_bench.provenance import (
    build_manifest,
    capture_environment,
    capture_git,
    load_manifest,
    manifest_to_bytes,
)


def init_git(root: Path) -> None:
    (root / ".gitignore").write_text("runs/\nresults/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "tests@example.test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=root, check=True, capture_output=True)


def test_clean_git_provenance_records_root_commit_branch_and_clean_state(project: Path) -> None:
    init_git(project.parent.parent)

    provenance = capture_git(project.parent.parent)

    assert provenance.root == project.parent.parent.resolve()
    assert len(provenance.commit) == 40
    assert provenance.branch == "main"
    assert provenance.clean is True


def test_git_provenance_detects_dirty_and_detached_states(project: Path) -> None:
    init_git(project.parent.parent)
    (project.parent.parent / "untracked.txt").write_text("untracked\n", encoding="utf-8")
    dirty = capture_git(project.parent.parent)
    assert dirty.clean is False

    subprocess.run(["git", "add", "untracked.txt"], cwd=project.parent.parent, check=True)
    assert capture_git(project.parent.parent).clean is False

    subprocess.run(
        ["git", "reset", "--quiet", "HEAD", "untracked.txt"], cwd=project.parent.parent, check=True
    )
    subprocess.run(
        ["git", "checkout", "--detach", "HEAD"],
        cwd=project.parent.parent,
        check=True,
        capture_output=True,
    )
    detached = capture_git(project.parent.parent)
    assert detached.branch is None
    assert detached.commit == dirty.commit


def test_git_provenance_detects_tracked_unstaged_change(project: Path) -> None:
    root = project.parent.parent
    init_git(root)
    tracked = root / "openspec/config.yaml"
    original = tracked.read_bytes()
    tracked.write_bytes(original + b"changed: true\n")

    try:
        assert capture_git(root).clean is False
    finally:
        tracked.write_bytes(original)


def test_git_provenance_rejects_missing_repository_or_commit(tmp_path: Path) -> None:
    with pytest.raises(PreparationError) as no_repository:
        capture_git(tmp_path)
    assert no_repository.value.code == "git_unavailable"

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    with pytest.raises(PreparationError) as no_commit:
        capture_git(tmp_path)
    assert no_commit.value.code == "git_commit_missing"


def test_environment_capture_is_local_and_secret_free(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "secret-token")
    environment = capture_environment()
    serialized = json.dumps(environment.__dict__, sort_keys=True)

    assert environment.platform
    assert environment.machine
    assert environment.python_implementation
    assert environment.python_version
    assert environment.package_version
    assert "OPENAI_API_KEY" not in serialized
    assert "secret-token" not in serialized
    assert str(Path.home()) not in serialized


def test_manifest_round_trip_is_strict_canonical_and_portable(project: Path) -> None:
    init_git(project.parent.parent)
    from thesis_bench.config import load_configuration

    configuration = load_configuration(project)
    manifest = build_manifest(
        configuration,
        run_id="20260901t120000000000z-abcdef123456",
        git=capture_git(project.parent.parent),
        environment=capture_environment(),
        prepared_at=datetime(2026, 9, 1, 12, tzinfo=UTC),
    )
    encoded = manifest_to_bytes(manifest)
    restored = load_manifest(encoded)

    assert encoded.endswith(b"\n")
    assert restored == manifest
    assert str(project.parent.parent) not in encoded.decode("utf-8")
    assert restored.metadata.hardware.id == "rx-5700"
    assert restored.environment.platform
    assert restored.git.clean is True

    altered = json.loads(encoded)
    altered["unexpected"] = "value"
    with pytest.raises(IntegrityError):
        load_manifest((json.dumps(altered) + "\n").encode("utf-8"))
