from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from thesis_bench.config import load_configuration, load_yaml_document
from thesis_bench.errors import ConfigurationError


def test_valid_metadata_set_is_typed_and_hashed(project: Path) -> None:
    configuration = load_configuration(project)

    assert configuration.experiment.id == "experiment-foundation"
    assert configuration.experiment.model.expected_id == "model-q4"
    assert configuration.metadata["model"].document.id == "model-q4"
    assert configuration.metadata["model"].path == "metadata/model.yaml"
    assert len(configuration.metadata["model"].source_sha256) == 64
    assert len(configuration.metadata["model"].semantic_sha256) == 64


def test_unknown_field_is_rejected_without_echoing_value(project: Path) -> None:
    experiment = project.read_text(encoding="utf-8")
    project.write_text(experiment + "secret_token: do-not-echo\n", encoding="utf-8")

    with pytest.raises(ConfigurationError) as raised:
        load_configuration(project)

    assert raised.value.code == "invalid_configuration"
    assert "do-not-echo" not in str(raised.value)
    assert "secret_token" in str(raised.value)


@pytest.mark.parametrize(
    ("relative_path", "field", "value"),
    [
        ("metadata/model.yaml", "schema_version", 2),
        ("metadata/model.yaml", "id", "Not Allowed"),
        ("metadata/model.yaml", "revision", "latest"),
        ("metadata/model.yaml", "artifact_sha256", "not-a-hash"),
        ("metadata/hardware.yaml", "ram_gb", "32"),
        ("metadata/dataset.yaml", "revision", "main"),
        ("metadata/evaluation.yaml", "version", "latest"),
    ],
)
def test_invalid_model_metadata_is_rejected(
    tmp_path: Path, project: Path, relative_path: str, field: str, value: object
) -> None:
    target = tmp_path / relative_path
    document = load_yaml_document(target)
    document[field] = value
    target.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_configuration(project)


def test_unknown_metadata_field_and_missing_required_field_are_rejected(
    project: Path, tmp_path: Path
) -> None:
    target = tmp_path / "metadata/model.yaml"
    document = load_yaml_document(target)
    document["secret_token"] = "not echoed"
    target.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ConfigurationError) as unknown:
        load_configuration(project)
    assert "not echoed" not in str(unknown.value)

    target.write_text(
        json.dumps({key: value for key, value in document.items() if key != "artifact_filename"}),
        encoding="utf-8",
    )
    with pytest.raises(ConfigurationError):
        load_configuration(project)


def test_duplicate_yaml_keys_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.yaml"
    path.write_text("schema_version: 1\nschema_version: 1\n", encoding="utf-8")

    with pytest.raises(ConfigurationError) as raised:
        load_yaml_document(path)

    assert raised.value.code == "invalid_yaml"
    assert "duplicate" in str(raised.value).lower()


def test_non_finite_numeric_values_are_rejected(project: Path, tmp_path: Path) -> None:
    target = tmp_path / "metadata/hardware.yaml"
    target.write_text(
        "schema_version: 1\nkind: hardware\nid: rx-5700\nprofile: p\n"
        "operating_system: os\ncpu: cpu\nram_gb: .nan\ngpu: gpu\nvram_gb: 8\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError):
        load_configuration(project)


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
