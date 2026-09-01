from __future__ import annotations

import json
from pathlib import Path

from test_provenance import init_git

from thesis_bench.cli import main


def test_version_prints_package_version(capsys) -> None:
    assert main(["--version"]) == 0

    captured = capsys.readouterr()
    assert captured.out == "thesis-bench 0.1.0\n"
    assert captured.err == ""


def test_validate_config_prints_identity_json_without_creating_runs(project: Path, capsys) -> None:
    assert main(["validate-config", str(project)]) == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["valid"] is True
    assert payload["experiment_id"] == "experiment-foundation"
    assert payload["condition_id"] == "baseline"
    assert payload["sources"]["experiment"]["path"] == "configs/experiment.yaml"
    assert captured.err == ""
    assert not (project.parent.parent / "results").exists()


def test_validate_config_error_is_json_on_stderr_and_side_effect_free(
    project: Path, capsys
) -> None:
    project.write_text(project.read_text(encoding="utf-8") + "unknown: value\n", encoding="utf-8")

    assert main(["validate-config", str(project)]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"]["code"] == "invalid_configuration"
    assert not (project.parent.parent / "results").exists()


def test_validate_config_rejects_unhashable_yaml_mapping_key(project: Path, capsys) -> None:
    project.write_text(
        project.read_text(encoding="utf-8") + "? [a, b]\n: value\n", encoding="utf-8"
    )

    assert main(["validate-config", str(project)]) == 2

    captured = capsys.readouterr()
    assert captured.out == ""
    error = json.loads(captured.err)["error"]
    assert error["code"] == "invalid_yaml"
    assert "traceback" not in captured.err.lower()


def test_prepare_and_show_form_one_json_stream(project: Path, tmp_path: Path, capsys) -> None:
    init_git(project.parent.parent)
    results_root = tmp_path / "runs"

    assert main(["prepare-run", str(project), "--results-root", str(results_root)]) == 0
    prepared_output = capsys.readouterr()
    prepared_payload = json.loads(prepared_output.out)
    assert prepared_payload["status"] == "prepared"
    run_directory = results_root / prepared_payload["run_id"]
    assert run_directory.is_dir()
    assert prepared_output.err == ""

    assert main(["show-run", str(run_directory)]) == 0
    shown_output = capsys.readouterr()
    shown_payload = json.loads(shown_output.out)
    assert shown_payload["run_id"] == prepared_payload["run_id"]
    assert shown_payload["git_commit"]
    assert shown_output.err == ""


def test_prepare_defaults_to_project_raw_results_root(project: Path, capsys) -> None:
    init_git(project.parent.parent)

    assert main(["prepare-run", str(project)]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["run_path"].startswith("results/raw/")
    assert (project.parent.parent / payload["run_path"]).is_dir()


def test_prepare_collision_returns_integrity_exit_code_and_preserves_run(
    project: Path, tmp_path: Path, monkeypatch, capsys
) -> None:
    init_git(project.parent.parent)
    results_root = tmp_path / "runs"
    run_id = "20260901t120000000000z-abcdef123456"
    monkeypatch.setattr("thesis_bench.lifecycle.generate_run_id", lambda **_: run_id)

    assert main(["prepare-run", str(project), "--results-root", str(results_root)]) == 0
    existing = (results_root / run_id / "manifest.json").read_bytes()
    capsys.readouterr()

    assert main(["prepare-run", str(project), "--results-root", str(results_root)]) == 4

    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"]["code"] == "run_exists"
    assert (results_root / run_id / "manifest.json").read_bytes() == existing


def test_prepare_rejects_dirty_git_without_publishing(
    project: Path, tmp_path: Path, capsys
) -> None:
    init_git(project.parent.parent)
    (project.parent.parent / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    results_root = tmp_path / "runs"

    assert main(["prepare-run", str(project), "--results-root", str(results_root)]) == 3

    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"]["code"] == "git_dirty"
    assert not results_root.exists()


def test_prepare_rejects_missing_git_without_publishing(
    project: Path, tmp_path: Path, capsys
) -> None:
    results_root = tmp_path / "runs"

    assert main(["prepare-run", str(project), "--results-root", str(results_root)]) == 3

    captured = capsys.readouterr()
    assert captured.out == ""
    assert json.loads(captured.err)["error"]["code"] == "git_unavailable"
    assert not results_root.exists()


def test_show_corrupt_and_missing_runs_have_distinct_exit_codes(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing"
    assert main(["show-run", str(missing)]) == 2
    missing_error = json.loads(capsys.readouterr().err)
    assert missing_error["error"]["code"] == "run_not_found"

    corrupt = tmp_path / "corrupt"
    corrupt.mkdir()
    (corrupt / "manifest.json").write_text("{broken}\n", encoding="utf-8")
    assert main(["show-run", str(corrupt)]) == 4
    corrupt_error = json.loads(capsys.readouterr().err)
    assert corrupt_error["error"]["code"] == "invalid_manifest"


def test_help_lists_only_foundation_commands(capsys) -> None:
    assert main(["--help"]) == 0
    output = capsys.readouterr().out
    assert "validate-config" in output
    assert "prepare-run" in output
    assert "show-run" in output
    assert "infer" not in output
    assert "download" not in output
