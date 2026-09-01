# Foundation Verification Map

This map connects the approved `foundation-experiment-platform` scenarios and Issue #1 acceptance criteria to deterministic tests or explicit repository checks. It covers the provenance-only foundation; it does not authorize inference, observations, lifecycle events, or benchmark data.

The amended OpenSpec defines a composite frozen identity rather than claiming universal branch detection. Model revisions must be full 40-character lowercase Git commit IDs and are paired with artifact SHA-256. Dataset revision and evaluation version use the repository identifier grammar and reject the reserved moving labels `latest`, `main`, and `master` case-insensitively; dataset contents are bound by manifest SHA-256, while evaluation configuration and code are bound by the document semantic hash and prepared run Git commit. Exhaustive symbolic-reference detection and remote resolution are intentionally out of scope.

## Requirement scenarios

| Area | Evidence |
|---|---|
| Versioned strict metadata, required fields, strict scalar types, identifiers, hashes, stable-label formats and reserved moving labels, whitespace-only identity rejection, unsupported versions, and unknown fields | `tests/test_configuration.py::test_model_revision_requires_full_lowercase_commit_id`, `test_dataset_and_evaluation_versions_require_stable_labels`, `test_dataset_and_evaluation_stable_labels_are_accepted`, plus the existing configuration tests listed here |
| Duplicate and unhashable YAML keys, malformed/non-UTF-8 YAML, non-finite values, and secret-safe errors | `tests/test_configuration.py::test_duplicate_yaml_keys_are_rejected`, `test_unhashable_yaml_mapping_key_is_rejected`, `test_malformed_yaml_is_rejected`, `test_non_utf8_yaml_is_rejected`, `test_non_finite_numeric_values_are_rejected`, `test_unknown_field_is_rejected_without_echoing_value`; `tests/test_cli.py::test_validate_config_rejects_unhashable_yaml_mapping_key` |
| Contained relative references, missing/wrong files, URLs, mismatches, parent traversal, and symlink escape | `tests/test_configuration.py::test_missing_reference_is_rejected`, `test_reference_mismatch_and_escape_are_rejected`, `test_reference_urls_and_non_yaml_paths_are_rejected`, `test_symlink_escape_is_rejected` |
| Exact source and canonical semantic SHA-256 identity, formatting/key-order independence, list order, Unicode, and semantic changes | `tests/test_configuration.py::test_semantic_hash_ignores_yaml_formatting_but_source_hash_does_not`, `test_semantic_hash_preserves_list_order_unicode_and_value_changes` |
| Valid identity-only examples without external artifact claims | `tests/test_examples.py::test_foundation_example_is_valid_identity_only_configuration` |
| Git root, full commit, branch, clean/dirty/staged/tracked-unstaged/untracked/detached/no-commit behavior | `tests/test_provenance.py::test_clean_git_provenance_records_root_commit_branch_and_clean_state`, `test_git_provenance_detects_dirty_and_detached_states`, `test_git_provenance_detects_tracked_unstaged_change`, `test_git_provenance_rejects_missing_repository_or_commit` |
| Local runtime facts, secret exclusion, portable paths, intended versus observed hardware, strict manifest round-trip, unknown fields, and trailing newline | `tests/test_provenance.py::test_environment_capture_is_local_and_secret_free`, `test_manifest_round_trip_is_strict_canonical_and_portable` |
| UTC sortable private IDs and repeated-run uniqueness | `tests/test_lifecycle.py::test_run_id_is_utc_sortable_private_and_unique`, `test_repeated_preparation_creates_two_distinct_runs` |
| Exclusive staging, atomic no-replace publication, collision preservation, injected write failure, immutable manifests, and read-only integrity inspection | `tests/test_lifecycle.py::test_prepare_publishes_one_complete_manifest_and_show_is_read_only`, `test_prepare_collision_preserves_existing_bytes`, `test_race_collision_preserves_existing_directory`, `test_write_failure_leaves_no_published_run`, `test_manifest_overwrite_is_refused_without_changing_bytes`, `test_show_run_distinguishes_missing_corrupt_and_mismatched_runs` |
| CLI command set, JSON streams, exit classes, side-effect-free validation, and validate → prepare → show | `tests/test_cli.py` |

## Issue #1 acceptance checks

| Acceptance criterion | Evidence |
|---|---|
| Tasks 1.1–6.5 complete without scope expansion | `openspec/changes/archive/2026-09-01-foundation-experiment-platform/tasks.md`, final diff inspection |
| Five metadata kinds reject unsafe input and establish the specified composite frozen identities | Configuration tests listed above, including the focused task 2.1 cases; `uv run thesis-bench validate-config examples/foundation/experiment.yaml` |
| Deterministic source and semantic hashes | Configuration hash tests listed above |
| Preparation requires committed clean Git and records approved provenance | Provenance/lifecycle tests listed above; CLI dirty-tree test |
| Atomic, immutable, collision-safe manifests | Lifecycle tests listed above |
| Three JSON CLI commands and exit codes | `tests/test_cli.py` |
| Routine verification is model-, GPU-, credential-, inference-, and post-install-network-free | `.node-version`, `pyproject.toml`, `package-lock.json`, `.github/workflows/ci.yml`, and the exact CI-equivalent command list in `docs/development/testing.md` |
| No events, observations, model artifacts, benchmark content, or speculative framework | Final diff and raw-results tree inspection recorded in the pull request |

## CI-equivalent command set

```bash
uv lock --check
uv run ruff format --check src tests
uv run ruff check src tests
uv run mypy src
uv run coverage run -m pytest -q
uv run coverage report
uv build
uv run thesis-bench validate-config examples/foundation/experiment.yaml
npm ci --ignore-scripts --no-audit --no-fund
./node_modules/.bin/renovate-config-validator renovate.json
./node_modules/.bin/openspec validate --all --strict --no-interactive
```
