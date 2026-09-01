## Context

The repository has research and architecture documents but no software. The first code must establish trustworthy configuration identity and provenance before inference begins. It is not a generic experiment platform: every included behavior directly protects later evidence from ambiguous inputs, mutable revisions, dirty source state, or overwritten manifests.

## Goals / Non-Goals

**Goals:**

- validate the minimum model, hardware, dataset, evaluation, and experiment identities needed by later runs;
- bind a prepared run to exact configuration hashes and a clean Git commit;
- create one immutable, inspectable manifest without executing a model;
- keep scientific logic deterministic and testable without GPU, model downloads, or network calls;
- establish only the packaging, CI, and dependency maintenance needed to verify this behavior.

**Non-goals:**

- inference, benchmark content, prompt conditions, retrieval, fine-tuning, harnesses, skills, telemetry, scoring, reporting, or experimental results;
- event logs or observation persistence before execution exists;
- generic providers, repositories, plugins, extension containers, databases, services, schedulers, or migration frameworks.

## Decisions

### Minimal project tooling

Use a `src`-layout `thesis_bench` package, the repository Python pin, Hatchling, and a `uv` lockfile. Runtime dependencies are Pydantic v2 and PyYAML; the CLI uses stdlib `argparse`. Development uses pytest, coverage, Ruff, and mypy. `pyproject.toml` owns package and tool configuration, and CI consumes repository pins instead of duplicating them.

The root Renovate configuration covers the runtime pin, `uv`, supported project dependencies and lockfiles, and GitHub Actions. Patch/minor updates may automerge after required checks; major updates require review. OpenSpec upgrades remain deliberate because generated skills must be regenerated and reviewed.

### Small code boundary

Use cohesive modules for schemas, configuration loading/hashing, provenance, run storage, and CLI behavior. A small error module is acceptable if it makes stable CLI errors clearer. Do not create interfaces, service/repository layers, or one file per type unless the implemented code demonstrates a real need.

Git is invoked with argument arrays and a controlled working directory, never through a shell. Tests use temporary repositories rather than a Git abstraction framework.

### Strict configuration and portable references

Each UTF-8 YAML document has `schema_version: 1`, `kind`, and a stable kind-specific ID. Experiment references use `{path, expected_id}`. Discover the project root by walking upward to the nearest directory containing `pyproject.toml` and `openspec/config.yaml`. Resolve references relative to the experiment file and require their real paths to remain under the project root.

Pydantic forbids unknown fields and enforces strict scalar types. A narrow `SafeLoader` subclass rejects duplicate mapping keys. Validation errors identify safe paths and field locations without echoing arbitrary values.

The model repository revision is provider-narrow by design: the current candidates are Git-backed model repositories, so schema version 1 accepts only a full 40-character lowercase commit ID. The artifact SHA-256 independently binds the selected weight file. Dataset revisions and evaluation versions are stable labels using the repository identifier grammar, with `latest`, `main`, and `master` reserved as moving labels. The validator does not attempt to recognize every possible branch name. Dataset contents are bound by the deterministic manifest SHA-256; evaluation configuration and code are bound by the document semantic hash and prepared run Git commit. This composite contract is scientifically explicit without inventing a general external-version resolver.

### Configuration identity

For each source, calculate SHA-256 over exact bytes and over the validated value encoded as canonical UTF-8 JSON with sorted object keys, compact separators, preserved list order, and no non-finite values. Byte hashes preserve exact-source traceability; semantic hashes identify equivalent validated configuration despite harmless YAML formatting.

### Clean Git provenance

Require the discovered project root to be a Git worktree with a resolvable commit. Any staged, unstaged, or non-ignored untracked change prevents run preparation. This fail-closed rule avoids implementing and explaining a custom dirty-tree digest before formal execution exists. Users may still validate configuration in a dirty tree.

The manifest records the full commit, attached branch when present, local platform, machine architecture, Python implementation/version, and installed package version. It stores project-relative source paths and never stores credentials, environment values, home paths, diffs, model output, or dataset records.

### Immutable prepared run

Generate a unique directory-safe ID from a UTC timestamp and UUID-derived suffix. Under `results/raw` (or an explicit test root), create a hidden staging directory exclusively, write and validate canonical `manifest.json`, then atomically rename the directory to its final ID without replacement. Failure leaves no published run. Existing runs and manifests are never replaced.

`show-run` validates the manifest and directory identity without writing. Lifecycle events and observations are intentionally deferred to the inference-runner change, where their actual requirements can be specified.

### CLI and failures

Provide only `validate-config`, `prepare-run`, `show-run`, and `--version`. Successful payloads and expected errors are one JSON object with a trailing newline. Use exit `2` for invalid input/path/configuration, `3` for Git/environment preparation failures, `4` for collision or stored-run integrity failures, and `1` for a generic unexpected internal error. Routine output contains no traceback.

### Tests and CI

Commit minimal example metadata that identifies artifacts without claiming they were downloaded or tested. Unit tests cover strict schemas, duplicate keys, reference containment, canonical hashes, safe errors, IDs, and manifests. Integration tests use temporary Git repositories for clean/dirty preparation, atomic publication, collisions, corruption, and CLI streams/exit codes.

CI runs lockfile consistency, formatting/lint, typing, tests with coverage, package build, example validation, Renovate validation, and strict OpenSpec validation. It requires no GPU, credentials, model download, inference, or writes outside temporary directories. GitHub Actions use immutable commit SHAs and remain Renovate-managed.

## Risks / Trade-offs

- **Strict schemas need later additions:** add fields through reviewed schema evolution when an experiment requires them; do not prebuild an extension mechanism.
- **Dirty exploratory preparation is unavailable:** configuration can still be validated while dirty; provenance-bearing preparation waits for a commit.
- **No event history yet:** the first change records preparation identity only. Execution and failure events will be specified with the runner that produces them.
- **Manual hardware metadata may differ from the host:** preserve declared hardware separately from minimal observed runtime facts; hardware probing belongs to a later measurement change.
- **Tooling becomes stale:** Renovate proposes maintenance changes while experiment campaigns freeze their complete environments independently.

## Migration Plan

There is no software schema to migrate. Implementation validates committed examples and creates no raw run during installation or CI except under temporary test directories. Rollback removes the package, tooling, examples, and CI; any intentionally prepared raw run remains historical evidence.
