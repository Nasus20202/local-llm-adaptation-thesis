## 1. Project and Tooling Foundation

- [ ] 1.1 Create the Python 3.14 `src/thesis_bench` package, Hatchling `pyproject.toml` with `requires-python = \">=3.14\"`, console entry point, and package version source; verify CPython 3.14.7 is selected from `.python-version`, `uv run thesis-bench --version` succeeds, and `uv build` succeeds.
- [ ] 1.2 Select and declare an exact `[tool.uv] required-version`, add pinned runtime/development dependencies, and commit `uv.lock`; verify `uv lock --check` succeeds from a clean checkout and CI obtains `uv` from the declared requirement.
- [ ] 1.3 Configure Ruff, mypy, pytest, and coverage in `pyproject.toml`; verify empty package checks run through the documented `uv run` commands.
- [ ] 1.4 Verify `renovate.json` extracts the Python pin, the required `uv` version, supported PEP 621 dependencies and lockfiles, and GitHub Actions; verify semantic commits, CI-gated patch/minor automerge, manual major updates, and the configuration with Renovate's config validator. Verify OpenSpec upgrades remain a deliberate manual workflow with skill regeneration and review.
- [ ] 1.5 Add only the package directories required by the design and verify no inference, RAG, fine-tuning, harness, skill, benchmark, database, or plugin implementation is introduced.

## 2. Versioned Configuration and Identity

- [ ] 2.1 Implement strict schema-version-1 models for experiment, references, model, hardware, dataset, and evaluation metadata; verify unit tests cover all required fields, strict scalar types, identifier patterns, hashes, mutable-revision rejection, unknown fields, and unsupported versions.
- [ ] 2.2 Implement the duplicate-key-rejecting safe YAML loader and secret-safe validation errors; verify malformed, duplicate, and non-finite fixtures fail without echoing fixture secrets.
- [ ] 2.3 Implement project-root discovery and repository-contained reference resolution with kind/expected-ID checks; verify tests cover valid relative paths, missing files, URLs, wrong extensions, ID/kind mismatch, `..` traversal, and symlink escape.
- [ ] 2.4 Implement source-byte and canonical semantic SHA-256 identity; verify stable fixtures prove formatting/key-order independence, list-order sensitivity, Unicode stability, and semantic-change sensitivity.
- [ ] 2.5 Add minimal valid example model, hardware, dataset, evaluation, and exploratory experiment YAML under `configs/`; verify the loader accepts the set and the examples do not claim that external artifacts were downloaded or tested.

## 3. Git, Environment, and Manifest Provenance

- [ ] 3.1 Implement Git-root/HEAD/branch/status capture using argument-array subprocess calls; verify integration tests cover attached/detached HEAD, no repository, and no commit.
- [ ] 3.2 Implement deterministic dirty-tree hashing for staged, unstaged, deleted, renamed, symlink, and non-ignored untracked entries; verify identical states hash equally and content/status changes alter the digest without storing file contents.
- [ ] 3.3 Implement formal-clean enforcement and exploratory-dirty recording; verify formal dirty preparation fails before publication while exploratory preparation records the dirty digest.
- [ ] 3.4 Implement safe local runtime environment capture; verify tests record required platform/Python/package facts and prove credential environment variables are absent.
- [ ] 3.5 Implement strict run manifest construction, canonical serialization, validation, and semantic hashing; verify round-trip, unknown-field, portable-path, intended-versus-observed hardware, and trailing-newline tests pass.

## 4. Raw Run Lifecycle

- [ ] 4.1 Implement UTC-plus-UUID run and event ID generation with injectable time/UUID sources; verify format, safety, sortability, and repeated-run uniqueness tests pass.
- [ ] 4.2 Implement same-filesystem staging, exclusive file writes, validation, fsync where supported, and non-replacing atomic publication; verify success, destination collision, injected write failure, and no-partial-publication tests pass.
- [ ] 4.3 Implement immutable manifest enforcement and initial `run_prepared` NDJSON creation; verify overwrite attempts preserve exact manifest bytes and a new run has one valid initial event.
- [ ] 4.4 Implement append-only event persistence and complete-history validation; verify appends preserve the existing byte prefix and reject malformed history, unsupported schema, and mismatched run IDs.
- [ ] 4.5 Implement read-only run integrity inspection; verify valid summaries, missing paths, directory/manifest/event ID mismatch, missing initial event, and corrupt JSON behavior.

## 5. Command-Line Contract

- [ ] 5.1 Implement the `argparse` root command, approved subcommands, help, and version behavior; verify CLI tests show no execution or model-management commands.
- [ ] 5.2 Implement `validate-config` success/error JSON and exit behavior; verify side-effect-free filesystem assertions, stdout/stderr separation, exit `0`, and invalid-input exit `2`.
- [ ] 5.3 Implement `prepare-run`, default/explicit results roots, and JSON response; verify clean success, dirty formal exit `3`, Git failure exit `3`, and collision/integrity exit `4` without model execution.
- [ ] 5.4 Implement `show-run` JSON summaries and safe error mapping; verify intact exit `0`, missing exit `2`, corrupt exit `4`, read-only behavior, and absence of routine tracebacks.
- [ ] 5.5 Add end-to-end CLI integration tests in temporary committed Git repositories; verify validate → prepare → show produces mutually consistent IDs, hashes, Git state, and events.

## 6. Documentation and Continuous Integration

- [ ] 6.1 Update README, `AGENTS.md`, development/testing documentation, and example comments with the implemented commands and schema locations; verify every documented command executes successfully.
- [ ] 6.2 Add a Linux GitHub Actions workflow that reads Python from `.python-version`, installs the exact `uv` version required by `pyproject.toml`, checks the lock, formatting/lint, mypy, pytest/coverage, package build, example validation, Renovate configuration, and strict OpenSpec validation; verify workflow syntax and reproduce every step locally.
- [ ] 6.3 Pin every GitHub Action to a full commit SHA with its release tag in a trailing comment and verify Renovate detects later action releases without replacing the immutable pin policy.
- [ ] 6.4 Ensure routine tests and CI require no credentials, network calls after dependency installation, model downloads, GPU, or writes outside temporary directories; verify with test instrumentation and workflow review.

## 7. Completion Verification

- [ ] 7.1 Verify the repository-pinned Python is active, then run `uv lock --check`, Ruff format check, Ruff lint, mypy, the complete pytest suite with coverage, package build, example validation, Renovate config validation, and `npx --yes @fission-ai/openspec validate foundation-experiment-platform --strict --no-interactive`; record exact outputs in the pull request.
- [ ] 7.2 Review every requirement scenario against an automated test or explicit validation artifact and record the mapping in the pull request; leave no uncovered acceptance criterion.
- [ ] 7.3 Inspect the final Git diff and raw-results tree; verify all tasks are checked, no raw experimental result or model artifact was committed, no substantial feature outside the proposal was implemented, and Git status is accurately reported.
