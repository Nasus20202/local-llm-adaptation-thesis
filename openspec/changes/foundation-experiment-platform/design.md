## Context

The repository currently contains research and architecture documents but no Python package. The first implementation must create stable configuration/provenance primitives without pulling model runtime concerns into the foundation. See `proposal.md` and the four capability specs for the behavior contract. Architectural constraints are defined in `docs/architecture/` and ADR-0006.

## Goals / Non-Goals

**Goals:**

- Make the smallest useful vertical slice from strict metadata loading through an inspectable prepared run.
- Keep validation, canonicalization, hashing, and persistence deterministic and independently testable.
- Produce portable files that humans can inspect and later components can extend through versioned schemas.
- Establish repeatable developer and CI commands without network or GPU dependencies.

**Non-Goals:**

- Generic plugin or provider abstractions.
- Model artifact verification/download, inference-process integration, GPU probing, live telemetry, scoring, or reporting.
- Backward compatibility with pre-foundation schemas or migration tooling.
- A database, experiment server, notebook API, web application, or experiment scheduler.

## Decisions

### Python 3.14 package and minimal tooling

Use a `src`-layout package named `thesis_bench`, Python `>=3.14`, Hatchling, and a `uv.lock` produced by `uv`. Pin the developer and CI interpreter to [CPython 3.14.7](https://www.python.org/downloads/release/python-3147/) in `.python-version`; this is the latest stable release verified on 2026-09-01. Declare an exact `[tool.uv] required-version` selected at implementation time. Runtime dependencies are Pydantic v2 and PyYAML. Use stdlib `argparse` rather than adding a CLI framework. Development tools are pytest, pytest-cov, Ruff, and mypy, configured in `pyproject.toml`.

Python 3.14 is chosen because the project is new, the foundation dependencies support current CPython, and the user explicitly prefers the newest stable feature series. The lower bound permits Renovate to advance `.python-version` to later stable Python feature series without a contradictory upper constraint; required CI is the compatibility gate. Pydantic provides strict nested validation and JSON schema generation; handwritten dataclasses would require more validation code. PyYAML is kept behind a narrow loader that rejects duplicate keys. `argparse` is sufficient for three commands.

The root `renovate.json` extends Renovate's best-practices preset. Its native managers cover `.python-version`, supported PEP 621 dependencies and lockfiles, and GitHub Actions; one narrow regex manager covers `[tool.uv] required-version`. Renovate uses semantic `chore(deps)` commits and automerges patch/minor updates only after required checks. Major updates remain manual. OpenSpec is upgraded deliberately outside Renovate because its generated skills must be regenerated and reviewed. Formal experiment campaigns freeze their complete environment independently of later maintenance updates.

### Module boundaries

Use cohesive modules rather than a framework:

- `schemas.py`: strict versioned metadata, manifest, and event models;
- `configuration.py`: project-root discovery, safe reference resolution, YAML loading, and cross-document validation;
- `identity.py`: canonical JSON, SHA-256, run/event ID generation;
- `git_provenance.py`: Git command execution and working-tree digest;
- `environment.py`: safe local runtime facts;
- `run_store.py`: atomic preparation, append-only events, and integrity inspection;
- `cli.py`: argument parsing, JSON output, error-to-exit-code mapping;
- `errors.py`: small typed domain error taxonomy.

Avoid repository/service interfaces until a second implementation requires interchangeable behavior. External command interaction is isolated in `git_provenance.py` so tests can use temporary Git repositories and constrained fakes.

### Configuration shape and project root

Each YAML file carries `schema_version: 1`, `kind`, and a kind-specific ID. The experiment contains references shaped as `{path, expected_id}`. Discover the project root by walking upward from the experiment file to the nearest directory containing both `pyproject.toml` and `openspec/config.yaml`. Resolve and canonicalize references, then require `resolved_path.is_relative_to(project_root.resolve())` and a `.yaml`/`.yml` regular file. This supports portable checked-in metadata while leaving large datasets and weights external and identified by revision/hash.

Set Pydantic models to forbid extra fields, use strict scalar validation, and reject mutable revision sentinels with field validators. Install a PyYAML `SafeLoader` subclass whose mapping constructor detects duplicate keys before Pydantic validation. Keep error details to field locations and safe identifiers; do not echo arbitrary scalar values.

### Dual hashes

Compute `source_sha256` directly from file bytes. Convert the validated model with JSON-compatible values, exclude no explicit field, and encode with `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")` for `semantic_sha256`. This makes semantic identity independent of YAML comments/key order while preserving list order. Write manifests with the same canonical JSON plus one newline.

Alternative hashing only source bytes would make harmless formatting a semantic change. Hashing only normalized data would lose exact-source traceability; both are retained.

### Git working-tree digest

Invoke Git with argument arrays and a controlled working directory, never a shell. Require `git rev-parse --show-toplevel` to match the discovered project root and resolve `HEAD^{commit}`. Use NUL-delimited porcelain status to classify staged, unstaged, rename/delete, and non-ignored untracked paths. Build a deterministic sequence of status codes, normalized repository-relative paths, and SHA-256 hashes of current file/symlink bytes where they exist, using deletion markers otherwise; hash that sequence for `working_tree_sha256`.

The digest is evidence, not a reconstructable patch, and the manifest never stores contents. Formal runs reject any dirty status. Exploratory runs retain the digest. Ignored model weights and caches are absent by Git definition; referenced scientific artifacts remain independently hashed in metadata.

### Atomic run layout

The default root is `results/raw`. Generate IDs as `YYYYMMDDtHHMMSSffffffz-<12 lowercase hex characters from UUID4>`. Under the results root, create a same-filesystem hidden staging directory exclusively, write `manifest.json` and `events.ndjson` with exclusive file creation, fsync files and staging directory where supported, validate both by reading them, then rename the staging directory to the final ID without replacement. A collision is an error; do not retry invisibly in tests that inject an ID.

The initial event contains no scientific observation, only `run_prepared`. Future components append events through one function that opens in append mode, locks within the process, validates the existing history first, writes one complete JSON line, flushes, and fsyncs. Cross-process locking is deliberately deferred until parallel execution is introduced; the current runner is single-process. The API refuses manifest replacement.

### JSON CLI and error taxonomy

The console entry point calls pure application functions and serializes exactly one JSON success or error object. Use exit `2` for paths/configuration/user input, `3` for Git or environment preparation failures, `4` for collision/integrity/immutability failures, and `1` only for unexpected internal errors converted to a generic safe message. Help/version retain conventional text output. Tracebacks remain available only to tests/logging, not routine CLI output.

### Tests, examples, and CI

Create minimal valid example files under the existing `configs/` hierarchy and one experiment example under `configs/experiments/`; hashes represent identity metadata and do not claim that artifacts were downloaded. Unit tests cover strict schemas, duplicate keys, canonical hashing, reference escape, secret-safe errors, IDs, and events. Integration tests create temporary Git repositories to cover clean/dirty/formal/exploratory behavior, atomic run creation, collision, corruption, and CLI exit/output streams.

Expose consistent `uv run` commands in README/AGENTS. CI on supported Linux reads Python 3.14.7 from `.python-version`, reads the exact `uv` requirement from `pyproject.toml`, and runs lockfile consistency, Ruff formatting/lint, mypy, pytest with coverage, package build, example validation, Renovate configuration validation, and OpenSpec strict validation. GitHub Actions are pinned to immutable commit SHAs and updated by Renovate. CI performs no network calls after dependency installation and no model operations.

## Risks / Trade-offs

- **[Schema is too rigid for later methods]** → Keep only a versioned `extensions` container in the manifest; add method configuration through later capability specs and schema versions rather than permissive unknown fields.
- **[Working-tree digest is mistaken for full reproducibility]** → Document that it is an integrity signal; formal runs require a clean commit and inputs have independent hashes.
- **[Append can tear on abnormal termination]** → Flush/fsync each complete line and make inspection fail closed; a failed run remains preserved for diagnosis.
- **[Filesystem atomicity differs]** → Stage and rename within one parent filesystem, test on Linux, and report unsupported persistence behavior rather than degrading silently.
- **[Manual hardware metadata differs from the machine]** → Preserve declared and observed facts separately; automated GPU/driver capture belongs to a later telemetry change.
- **[Dependency or runtime pin becomes stale]** → Renovate opens pull requests for Python, `uv`, dependencies, lockfile maintenance, and GitHub Actions. Required CI gates patch/minor automerge; majors remain manual. OpenSpec upgrades follow their separate deliberate workflow.

## Migration Plan

There is no prior software schema to migrate. Implementation lands behind the new CLI, validates the committed examples, and creates no raw run during installation or CI except in temporary test directories. Rollback removes the package/tooling files and CI workflow; any intentionally prepared raw run remains preserved as historical data.
