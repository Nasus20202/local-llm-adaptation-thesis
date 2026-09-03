from __future__ import annotations

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


@pytest.mark.parametrize(
    "revision",
    [
        "0123456789abcdef0123456789abcdef0123456",
        "0123456789ABCDEF0123456789abcdef01234567",
        "HEAD",
        "refs/heads/main",
    ],
)
def test_model_revision_requires_full_lowercase_commit_id(
    project: Path, tmp_path: Path, revision: str
) -> None:
    target = tmp_path / "metadata/model.yaml"
    document = load_yaml_document(target)
    document["revision"] = revision
    target.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_configuration(project)


@pytest.mark.parametrize(
    ("relative_path", "field", "value"),
    [
        ("metadata/dataset.yaml", "revision", "refs/heads/main"),
        ("metadata/dataset.yaml", "revision", "Release-2026"),
        ("metadata/dataset.yaml", "revision", "latest"),
        ("metadata/dataset.yaml", "revision", "main"),
        ("metadata/dataset.yaml", "revision", "master"),
        ("metadata/evaluation.yaml", "version", "refs/heads/main"),
        ("metadata/evaluation.yaml", "version", "Release-2026"),
        ("metadata/evaluation.yaml", "version", "latest"),
        ("metadata/evaluation.yaml", "version", "main"),
        ("metadata/evaluation.yaml", "version", "master"),
    ],
)
def test_dataset_and_evaluation_versions_require_stable_labels(
    project: Path,
    tmp_path: Path,
    relative_path: str,
    field: str,
    value: str,
) -> None:
    target = tmp_path / relative_path
    document = load_yaml_document(target)
    document[field] = value
    target.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_configuration(project)


def test_dataset_and_evaluation_stable_labels_are_accepted(project: Path, tmp_path: Path) -> None:
    for relative_path, field, value in (
        ("metadata/dataset.yaml", "revision", "release-2026.01"),
        ("metadata/evaluation.yaml", "version", "v1.2.3"),
    ):
        target = tmp_path / relative_path
        document = load_yaml_document(target)
        document[field] = value
        target.write_text(json.dumps(document), encoding="utf-8")

    configuration = load_configuration(project)

    assert configuration.metadata["dataset"].document.revision == "release-2026.01"
    assert configuration.metadata["evaluation"].document.version == "v1.2.3"


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


def test_unhashable_yaml_mapping_key_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "unhashable-key.yaml"
    path.write_text("? [a, b]\n: value\n", encoding="utf-8")

    with pytest.raises(ConfigurationError) as raised:
        load_yaml_document(path)

    assert raised.value.code == "invalid_yaml"
    assert "mapping key" in str(raised.value).lower()


def test_malformed_yaml_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "malformed.yaml"
    path.write_text("schema_version: [1\n", encoding="utf-8")

    with pytest.raises(ConfigurationError) as raised:
        load_yaml_document(path)

    assert raised.value.code == "invalid_yaml"
    assert "malformed" in str(raised.value).lower()


def test_non_utf8_yaml_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "non-utf8.yaml"
    path.write_bytes(b"schema_version: 1\nvalue: \xff\n")

    with pytest.raises(ConfigurationError) as raised:
        load_yaml_document(path)

    assert raised.value.code == "invalid_yaml"
    assert "utf-8" in str(raised.value).lower()


def test_non_finite_numeric_values_are_rejected(project: Path, tmp_path: Path) -> None:
    target = tmp_path / "metadata/hardware.yaml"
    target.write_text(
        "schema_version: 1\nkind: hardware\nid: rx-5700\nprofile: p\n"
        "operating_system: os\ncpu: cpu\nram_gb: .nan\ngpu: gpu\nvram_gb: 8\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigurationError):
        load_configuration(project)


@pytest.mark.parametrize(
    ("relative_path", "field"),
    [
        ("metadata/model.yaml", "repository"),
        ("metadata/model.yaml", "revision"),
        ("metadata/model.yaml", "artifact_filename"),
        ("metadata/model.yaml", "quantization"),
        ("metadata/model.yaml", "license_id"),
        ("metadata/model.yaml", "chat_template_id"),
        ("metadata/hardware.yaml", "profile"),
        ("metadata/hardware.yaml", "operating_system"),
        ("metadata/hardware.yaml", "cpu"),
        ("metadata/hardware.yaml", "gpu"),
        ("metadata/dataset.yaml", "dataset"),
        ("metadata/dataset.yaml", "revision"),
        ("metadata/dataset.yaml", "split"),
        ("metadata/evaluation.yaml", "evaluator"),
        ("metadata/evaluation.yaml", "version"),
    ],
)
def test_whitespace_only_identity_fields_are_rejected(
    project: Path, tmp_path: Path, relative_path: str, field: str
) -> None:
    target = tmp_path / relative_path
    document = load_yaml_document(target)
    document[field] = "   "
    target.write_text(json.dumps(document), encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_configuration(project)
