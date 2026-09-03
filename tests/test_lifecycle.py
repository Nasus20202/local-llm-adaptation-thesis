from __future__ import annotations

import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest

from tests.provenance.test_provenance import init_git
from thesis_bench import lifecycle
from thesis_bench.config import load_configuration
from thesis_bench.errors import CollisionError, IntegrityError, PreparationError, ThesisBenchError
from thesis_bench.lifecycle import (
    generate_run_id,
    inspect_run,
    prepare_run,
    write_manifest,
)


def test_run_id_is_utc_sortable_private_and_unique() -> None:
    when = datetime(2026, 9, 1, 12, 30, 4, 123456, tzinfo=UTC)
    first = generate_run_id(now_source=lambda: when, uuid_source=lambda: uuid.UUID(int=1))
    second = generate_run_id(now_source=lambda: when, uuid_source=lambda: uuid.UUID(int=2))

    assert first == "20260901t123004123456z-000000000001"
    assert first < "20260901t123005000000z-000000000000"
    assert first != second
    assert all(
        character.isdigit() or character in "abcdefghijklmnopqrstuvwxyz-" for character in first
    )
    assert "/" not in first
    assert "nasus" not in first


def prepared_configuration(project: Path):
    init_git(project.parent.parent)
    return load_configuration(project)


def test_prepare_publishes_one_complete_manifest_and_show_is_read_only(
    project: Path, tmp_path: Path
) -> None:
    configuration = prepared_configuration(project)
    results_root = tmp_path / "runs"

    prepared = prepare_run(
        configuration,
        results_root=results_root,
        now_source=lambda: datetime(2026, 9, 1, 12, tzinfo=UTC),
        uuid_source=lambda: uuid.UUID(int=3),
    )
    manifest_bytes = (prepared.path / "manifest.json").read_bytes()
    before = sorted(path.name for path in results_root.iterdir())
    summary = inspect_run(prepared.path)
    after = sorted(path.name for path in results_root.iterdir())

    assert prepared.path.is_dir()
    assert manifest_bytes.endswith(b"\n")
    assert before == [prepared.run_id]
    assert after == before
    assert summary["run_id"] == prepared.run_id
    assert summary["experiment_id"] == "experiment-foundation"
    assert summary["git_commit"] == prepared.manifest.git.commit


def test_prepare_collision_preserves_existing_bytes(project: Path, tmp_path: Path) -> None:
    configuration = prepared_configuration(project)
    results_root = tmp_path / "runs"

    def fixed() -> uuid.UUID:
        return uuid.UUID(int=4)

    def now() -> datetime:
        return datetime(2026, 9, 1, 12, tzinfo=UTC)

    first = prepare_run(configuration, results_root=results_root, uuid_source=fixed, now_source=now)
    existing = (first.path / "manifest.json").read_bytes()

    with pytest.raises(CollisionError) as raised:
        prepare_run(configuration, results_root=results_root, uuid_source=fixed, now_source=now)

    assert raised.value.exit_code == 4
    assert (first.path / "manifest.json").read_bytes() == existing


def test_repeated_preparation_creates_two_distinct_runs(project: Path, tmp_path: Path) -> None:
    configuration = prepared_configuration(project)
    results_root = tmp_path / "runs"
    timestamps = datetime(2026, 9, 1, 12, tzinfo=UTC)
    uuids = iter((uuid.UUID(int=5), uuid.UUID(int=6)))

    first = prepare_run(
        configuration,
        results_root=results_root,
        now_source=lambda: timestamps,
        uuid_source=lambda: next(uuids),
    )
    second = prepare_run(
        configuration,
        results_root=results_root,
        now_source=lambda: timestamps,
        uuid_source=lambda: next(uuids),
    )

    assert first.run_id != second.run_id
    assert first.path.is_dir()
    assert second.path.is_dir()
    assert sorted(path.name for path in results_root.iterdir()) == sorted(
        (first.run_id, second.run_id)
    )


def test_race_collision_preserves_existing_directory(
    project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    configuration = prepared_configuration(project)
    results_root = tmp_path / "runs"
    real_noreplace = lifecycle._rename_noreplace

    def create_collision(source: Path, destination: Path) -> None:
        destination.mkdir()
        (destination / "intruder").write_bytes(b"preserve me")
        real_noreplace(source, destination)

    monkeypatch.setattr(lifecycle, "_rename_noreplace", create_collision)

    with pytest.raises(CollisionError):
        prepare_run(configuration, results_root=results_root)

    run_directories = [path for path in results_root.iterdir() if path.is_dir()]
    assert len(run_directories) == 1
    assert (run_directories[0] / "intruder").read_bytes() == b"preserve me"


def test_write_failure_leaves_no_published_run(project: Path, tmp_path: Path, monkeypatch) -> None:
    configuration = prepared_configuration(project)
    results_root = tmp_path / "runs"

    def fail_writer(*args, **kwargs):
        raise OSError("injected failure")

    monkeypatch.setattr("thesis_bench.lifecycle.write_manifest", fail_writer)
    with pytest.raises(PreparationError):
        prepare_run(configuration, results_root=results_root)

    assert not results_root.exists() or list(results_root.iterdir()) == []


def test_manifest_overwrite_is_refused_without_changing_bytes(
    project: Path, tmp_path: Path
) -> None:
    configuration = prepared_configuration(project)
    prepared = prepare_run(configuration, results_root=tmp_path / "runs")
    target = prepared.path / "manifest.json"
    before = target.read_bytes()

    with pytest.raises(CollisionError):
        write_manifest(prepared.path, prepared.manifest)

    assert target.read_bytes() == before


def test_show_run_distinguishes_missing_corrupt_and_mismatched_runs(
    project: Path, tmp_path: Path
) -> None:
    configuration = prepared_configuration(project)
    prepared = prepare_run(configuration, results_root=tmp_path / "runs")

    with pytest.raises(ThesisBenchError) as missing:
        inspect_run(tmp_path / "does-not-exist")
    assert missing.value.code == "run_not_found"
    assert missing.value.exit_code == 2

    corrupt = tmp_path / "corrupt"
    corrupt.mkdir()
    (corrupt / "manifest.json").write_text("{not json}\n", encoding="utf-8")
    with pytest.raises(IntegrityError):
        inspect_run(corrupt)

    mismatch = tmp_path / "different-name"
    prepared.path.rename(mismatch)
    with pytest.raises(IntegrityError):
        inspect_run(mismatch)
