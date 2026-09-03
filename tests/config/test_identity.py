from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from thesis_bench.config import load_configuration
from thesis_bench.errors import ConfigurationError


def test_semantic_hash_ignores_yaml_formatting_but_source_hash_does_not(project: Path) -> None:
    first = load_configuration(project)
    first_identity = first.metadata["experiment"]

    project.write_text(
        "kind: experiment\n"
        "schema_version: 1\n"
        "id: experiment-foundation\n"
        "condition_id: baseline\n"
        "run_kind: exploratory\n"
        "random_seed: 7\n"
        "model: {expected_id: model-q4, path: ../metadata/model.yaml}\n"
        "hardware: {path: ../metadata/hardware.yaml, expected_id: rx-5700}\n"
        "dataset: {path: ../metadata/dataset.yaml, expected_id: dataset-v1}\n"
        "evaluation: {path: ../metadata/evaluation.yaml, expected_id: evaluation-v1}\n",
        encoding="utf-8",
    )
    second_identity = load_configuration(project).metadata["experiment"]

    assert first_identity.semantic_sha256 == second_identity.semantic_sha256
    assert first_identity.source_sha256 != second_identity.source_sha256
    assert (
        first_identity.semantic_sha256
        == hashlib.sha256(
            json.dumps(
                first.experiment.model_dump(mode="json"),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
    )


def test_semantic_hash_preserves_list_order_unicode_and_value_changes(
    project: Path, tmp_path: Path
) -> None:
    first = load_configuration(project)
    first_evaluation = first.metadata["evaluation"].semantic_sha256
    evaluation_path = tmp_path / "metadata/evaluation.yaml"
    evaluation_path.write_text(
        "schema_version: 1\nkind: evaluation\nid: evaluation-v1\n"
        'evaluator: "żółw"\nversion: "2026.01"\nmetrics:\n  - exact_match\n  - latency\n',
        encoding="utf-8",
    )
    changed = load_configuration(project)
    changed_evaluation = changed.metadata["evaluation"].semantic_sha256
    assert changed_evaluation != first_evaluation

    evaluation_path.write_text(
        "schema_version: 1\nkind: evaluation\nid: evaluation-v1\n"
        'evaluator: "żółw"\nversion: "2026.01"\nmetrics:\n  - latency\n  - exact_match\n',
        encoding="utf-8",
    )
    reordered = load_configuration(project)
    assert reordered.metadata["evaluation"].semantic_sha256 != changed_evaluation

    assert "żółw" in json.dumps(
        reordered.metadata["evaluation"].document.model_dump(mode="json"), ensure_ascii=False
    )


def test_reference_mismatch_and_escape_are_rejected(project: Path) -> None:
    original = project.read_text(encoding="utf-8")
    project.write_text(original.replace("model-q4", "wrong-id"), encoding="utf-8")
    with pytest.raises(ConfigurationError) as mismatch:
        load_configuration(project)
    assert "wrong-id" in str(mismatch.value)
    assert "model-q4" in str(mismatch.value)

    project.write_text(
        original.replace("../metadata/model.yaml", "../../outside.yaml"), encoding="utf-8"
    )
    with pytest.raises(ConfigurationError):
        load_configuration(project)


def test_symlink_escape_is_rejected(project: Path, tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-model.yaml"
    outside.write_text(
        (tmp_path / "metadata/model.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    link = tmp_path / "metadata/escape.yaml"
    link.symlink_to(outside)
    experiment = project.read_text(encoding="utf-8")
    project.write_text(
        experiment.replace("../metadata/model.yaml", "../metadata/escape.yaml"), encoding="utf-8"
    )

    with pytest.raises(ConfigurationError):
        load_configuration(project)


def test_reference_urls_and_non_yaml_paths_are_rejected(project: Path) -> None:
    original = project.read_text(encoding="utf-8")
    for replacement in ("https://example.test/model.yaml", "../metadata/model.json"):
        project.write_text(
            original.replace("../metadata/model.yaml", replacement), encoding="utf-8"
        )
        with pytest.raises(ConfigurationError):
            load_configuration(project)


def test_missing_reference_is_rejected(project: Path) -> None:
    original = project.read_text(encoding="utf-8")
    project.write_text(
        original.replace("../metadata/model.yaml", "../metadata/missing.yaml"),
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError) as raised:
        load_configuration(project)

    assert raised.value.code == "unsafe_reference"


def test_each_yaml_source_is_read_once(project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original_read_bytes = Path.read_bytes
    read_counts: dict[Path, int] = {}

    def counted_read_bytes(path: Path) -> bytes:
        resolved = path.resolve()
        read_counts[resolved] = read_counts.get(resolved, 0) + 1
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", counted_read_bytes)

    load_configuration(project)

    expected_paths = {
        project.resolve(),
        *(path.resolve() for path in (project.parent.parent / "metadata").glob("*.yaml")),
    }
    assert {path: read_counts[path] for path in expected_paths} == {
        path: 1 for path in expected_paths
    }


def test_experiment_source_hash_matches_the_bytes_that_were_validated(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original_read_bytes = Path.read_bytes
    experiment_path = project.resolve()
    original_source = original_read_bytes(experiment_path)
    altered_source = original_source + b"# changed after validation\n"
    calls = 0

    def changing_read_bytes(path: Path) -> bytes:
        nonlocal calls
        if path.resolve() == experiment_path:
            calls += 1
            return original_source if calls == 1 else altered_source
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", changing_read_bytes)

    configuration = load_configuration(project)

    assert calls == 1
    assert (
        configuration.metadata["experiment"].source_sha256
        == hashlib.sha256(original_source).hexdigest()
    )
