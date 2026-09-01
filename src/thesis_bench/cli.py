from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import NoReturn, TextIO

from . import __version__
from .config import load_configuration
from .errors import ConfigurationError, ThesisBenchError
from .lifecycle import inspect_run, prepare_run


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ConfigurationError("invalid_arguments", "invalid command arguments")


def _build_parser() -> _ArgumentParser:
    parser = _ArgumentParser(
        prog="thesis-bench",
        description="Validate experiment metadata and prepare provenance-only runs.",
    )
    parser.add_argument(
        "--version", action="store_true", help="print the installed package version"
    )
    commands = parser.add_subparsers(dest="command", metavar="COMMAND")

    validate = commands.add_parser("validate-config", help="validate an experiment configuration")
    validate.add_argument("experiment_path", type=Path)

    prepare = commands.add_parser("prepare-run", help="prepare one provenance-only raw run")
    prepare.add_argument("experiment_path", type=Path)
    prepare.add_argument("--results-root", type=Path)

    show = commands.add_parser("show-run", help="inspect a prepared run manifest")
    show.add_argument("run_directory", type=Path)
    return parser


def _write_json(payload: object, stream: TextIO) -> None:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    print(text, file=stream)


def _relative_path(path: Path, root: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _validate_payload(experiment_path: Path) -> dict[str, object]:
    configuration = load_configuration(experiment_path)
    sources = {
        kind: {
            "path": identity.path,
            "source_sha256": identity.source_sha256,
            "semantic_sha256": identity.semantic_sha256,
        }
        for kind, identity in configuration.metadata.items()
    }
    return {
        "valid": True,
        "experiment_id": configuration.experiment.id,
        "condition_id": configuration.experiment.condition_id,
        "sources": sources,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    try:
        arguments = parser.parse_args(argv)
        if arguments.version:
            print(f"thesis-bench {__version__}")
            return 0
        if arguments.command is None:
            parser.print_help()
            return 0
        if arguments.command == "validate-config":
            _write_json(_validate_payload(arguments.experiment_path), sys.stdout)
            return 0
        if arguments.command == "prepare-run":
            configuration = load_configuration(arguments.experiment_path)
            prepared = prepare_run(configuration, results_root=arguments.results_root)
            _write_json(
                {
                    "run_id": prepared.run_id,
                    "run_path": _relative_path(prepared.path, configuration.project_root),
                    "manifest_semantic_sha256": prepared.manifest_semantic_sha256,
                    "status": "prepared",
                },
                sys.stdout,
            )
            return 0
        if arguments.command == "show-run":
            _write_json(inspect_run(arguments.run_directory), sys.stdout)
            return 0
        raise ConfigurationError("invalid_arguments", "invalid command")
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 1
    except ThesisBenchError as exc:
        _write_json(exc.as_json_object(), sys.stderr)
        return exc.exit_code
    except Exception:
        _write_json(
            {"error": {"code": "internal_error", "message": "unexpected internal error"}},
            sys.stderr,
        )
        return 1
