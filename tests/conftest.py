from __future__ import annotations

from pathlib import Path

import pytest
import yaml


def metadata_documents() -> dict[str, dict[str, object]]:
    return {
        "metadata/model.yaml": {
            "schema_version": 1,
            "kind": "model",
            "id": "model-q4",
            "repository": "org/model",
            "revision": "0123456789abcdef0123456789abcdef01234567",
            "artifact_filename": "model.gguf",
            "artifact_sha256": "a" * 64,
            "quantization": "Q4_K_M",
            "license_id": "apache-2.0",
            "chat_template_id": "chat-template-v1",
        },
        "metadata/hardware.yaml": {
            "schema_version": 1,
            "kind": "hardware",
            "id": "rx-5700",
            "profile": "primary-local-machine",
            "operating_system": "Fedora Linux",
            "cpu": "AMD Ryzen 5 3600",
            "ram_gb": 32,
            "gpu": "AMD Radeon RX 5700",
            "vram_gb": 8,
        },
        "metadata/dataset.yaml": {
            "schema_version": 1,
            "kind": "dataset",
            "id": "dataset-v1",
            "dataset": "example-dataset",
            "revision": "dataset-2026-01-01",
            "split": "development",
            "manifest_sha256": "b" * 64,
        },
        "metadata/evaluation.yaml": {
            "schema_version": 1,
            "kind": "evaluation",
            "id": "evaluation-v1",
            "evaluator": "deterministic-evaluator",
            "version": "2026.01",
            "metrics": ["exact_match"],
        },
    }


def experiment_document() -> dict[str, object]:
    return {
        "schema_version": 1,
        "kind": "experiment",
        "id": "experiment-foundation",
        "condition_id": "baseline",
        "run_kind": "exploratory",
        "random_seed": 7,
        "model": {"path": "../metadata/model.yaml", "expected_id": "model-q4"},
        "hardware": {"path": "../metadata/hardware.yaml", "expected_id": "rx-5700"},
        "dataset": {"path": "../metadata/dataset.yaml", "expected_id": "dataset-v1"},
        "evaluation": {
            "path": "../metadata/evaluation.yaml",
            "expected_id": "evaluation-v1",
        },
    }


def create_project(root: Path) -> Path:
    (root / "openspec").mkdir()
    (root / "openspec/config.yaml").write_text("schema: spec-driven\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname = 'fixture'\n", encoding="utf-8")
    for relative_path, document in metadata_documents().items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    experiment_path = root / "configs/experiment.yaml"
    experiment_path.parent.mkdir()
    experiment_path.write_text(
        yaml.safe_dump(experiment_document(), sort_keys=False),
        encoding="utf-8",
    )
    return experiment_path


@pytest.fixture
def project(tmp_path: Path) -> Path:
    return create_project(tmp_path)
