## Why

Future adaptation experiments need a small, testable foundation that rejects ambiguous inputs and records enough provenance to make every execution attempt auditable. Establishing this contract before inference work prevents incompatible configurations, mutable raw results, and undocumented environment changes from undermining the thesis.

## What Changes

- Establish a Python 3.14 project, pinned initially to CPython 3.14.7, with locked developer tooling, static checks, tests, package build, and network-free routine CI.
- Introduce strict, versioned YAML representations for experiment, model, hardware, dataset, and evaluation metadata.
- Resolve referenced metadata relative to the experiment file, validate cross-references, and compute source-byte and canonical semantic SHA-256 hashes.
- Introduce a versioned JSON run manifest containing experiment identity, referenced metadata identity, Git state, environment facts, configuration hashes, and extension points for later approved methods.
- Introduce exclusive creation of unique raw run directories, immutable manifest creation, and append-only lifecycle events.
- Provide a minimal CLI to validate configuration, prepare a run without executing a model, and inspect a prepared run.
- Add deterministic unit/integration tests, example metadata, developer commands, CI validation, and reviewed Renovate updates for the runtime, toolchain, dependencies, lockfile, and GitHub Actions.
- Explicitly exclude inference, benchmark content, RAG, fine-tuning, harnesses, skills, telemetry sampling, evaluation execution, and reporting.

## Capabilities

### New Capabilities

- `experiment-configuration`: Strict loading, reference resolution, validation, and hashing of versioned experiment metadata.
- `run-provenance`: Construction and validation of a stable, secret-safe run manifest with Git and environment provenance.
- `run-lifecycle`: Collision-safe raw run preparation, immutable manifest persistence, and append-only lifecycle events.
- `command-line-interface`: Human- and automation-usable commands for configuration validation, run preparation, and run inspection.

### Modified Capabilities

None. This repository has no implemented software capabilities yet.

## Impact

The change will create the initial `src/thesis_bench/` package, tests, example configurations, Python project metadata and lockfile, developer task commands, and a routine GitHub Actions workflow. It introduces Pydantic v2 and PyYAML as runtime dependencies and pytest, Ruff, mypy, Hatchling, and `uv`-managed development tooling. The repository-level Python pin and Renovate policy are established during bootstrap; implementation must wire CI and `pyproject.toml` to those sources without duplicating versions. It creates no model, data, network, database, or GPU dependency and does not produce experimental results.
