## 1. Minimal Project Foundation

- [x] 1.1 Create the `src/thesis_bench` package, `pyproject.toml`, console entry point, and package version source using the repository Python pin; verify `uv run thesis-bench --version` and `uv build` succeed.
- [x] 1.2 Select the exact `uv` requirement, declare only approved runtime/development dependencies, and commit `uv.lock`; verify `uv lock --check` from a clean checkout.
- [x] 1.3 Configure Ruff, mypy, pytest, and coverage in `pyproject.toml`; expose compact documented commands.
- [x] 1.4 Verify Renovate covers the runtime pin, `uv`, supported dependencies/lockfile, and GitHub Actions with semantic commits, CI-gated patch/minor automerge, manual major updates, and deliberate OpenSpec upgrades.

## 2. Configuration and Identity

- [ ] 2.1 Implement strict schema-version-1 models for experiment, reference, model, hardware, dataset, and evaluation metadata; test required fields, strict types, identifiers, hashes, exact full-commit model revisions, stable dataset/evaluation labels with the three reserved moving labels, unknown fields, and unsupported versions.
- [x] 2.2 Implement duplicate-key-rejecting safe YAML loading and secret-safe validation errors; test malformed, duplicate, non-finite, and secret-bearing fixtures.
- [x] 2.3 Implement project-root discovery and contained reference resolution with kind/expected-ID checks; test valid paths, missing files, URLs, wrong extensions, mismatches, traversal, and symlink escape.
- [x] 2.4 Implement exact-byte and canonical semantic SHA-256 identity; test formatting/key-order independence, list-order sensitivity, Unicode stability, and semantic changes.
- [x] 2.5 Add the smallest valid example metadata set; verify it loads and makes no claim that external artifacts were downloaded or tested.

## 3. Provenance Manifest

- [x] 3.1 Capture Git root, full commit, attached branch when present, and cleanliness using argument-array subprocess calls; test detached HEAD, dirty states, no repository, and no commit.
- [x] 3.2 Reject preparation for any staged, unstaged, or non-ignored untracked change; verify configuration validation remains side-effect-free and usable while dirty.
- [x] 3.3 Capture only the approved local runtime facts; test that credentials, environment values, absolute home paths, diffs, and scientific payloads are absent.
- [x] 3.4 Implement strict manifest construction, canonical serialization, validation, and hashing; test round-trip, unknown fields, portable paths, intended-versus-observed hardware, and trailing newline.

## 4. Immutable Prepared Run

- [x] 4.1 Implement UTC-plus-UUID run IDs with injectable time/UUID sources; test format, privacy, sortability, and uniqueness.
- [x] 4.2 Implement same-parent staging, exclusive writes, manifest validation, and non-replacing atomic publication; test success, collision, injected write failure, and no partial published run.
- [x] 4.3 Enforce manifest immutability; test that overwrite attempts preserve exact existing bytes.
- [x] 4.4 Implement read-only integrity inspection; test valid summaries, missing paths, directory/manifest ID mismatch, and corrupt JSON.

## 5. Minimal CLI

- [x] 5.1 Implement `validate-config`, `prepare-run`, `show-run`, help, and version behavior; expose no execution or model-management commands.
- [x] 5.2 Test `validate-config` success/error JSON, streams, exit codes, and absence of side effects.
- [x] 5.3 Test `prepare-run` with default/explicit roots, clean success, dirty or missing Git, collisions, and no model execution.
- [x] 5.4 Test `show-run` intact/missing/corrupt behavior, JSON streams, exit codes, and read-only operation; add one validate → prepare → show integration test.

## 6. Documentation, CI, and Completion

- [x] 6.1 Update README, `AGENTS.md`, testing documentation, and example comments with only implemented commands and schema locations; execute every documented command.
- [x] 6.2 Add Linux CI for lock consistency, Ruff, mypy, pytest/coverage, build, example validation, Renovate validation, and strict OpenSpec validation; pin Actions to commit SHAs and reproduce the steps locally.
- [x] 6.3 Verify routine tests/CI need no credentials, post-install network calls, model download, GPU, inference, or writes outside temporary directories.
- [x] 6.4 Map every requirement scenario and acceptance criterion to a test or explicit verification artifact; record exact command results in the pull request.
- [x] 6.5 Inspect the final diff, task list, and raw-results tree; confirm there is no event system, inference, benchmark, RAG, fine-tuning, harness, skill, plugin framework, database, model artifact, experimental result, or unrelated refactor.
