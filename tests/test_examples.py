from __future__ import annotations

from pathlib import Path

from thesis_bench.config import load_configuration


def test_foundation_example_is_valid_identity_only_configuration() -> None:
    path = Path("examples/foundation/experiment.yaml")

    configuration = load_configuration(path)

    assert configuration.experiment.id == "foundation-example"
    assert configuration.metadata["model"].document.artifact_filename == "example-model.gguf"
    assert "does not download" in path.read_text(encoding="utf-8").lower()
    assert (
        "not part of this repository"
        in (path.parent / "metadata/model.yaml").read_text(encoding="utf-8").lower()
    )
