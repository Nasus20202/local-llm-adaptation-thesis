# Foundation Verification Map

This map connects the approved `foundation-experiment-platform` scenarios and Issue #1 acceptance criteria to deterministic tests or explicit repository checks. It covers the provenance-only foundation; it does not authorize inference, observations, lifecycle events, or benchmark data.

## Requirement scenarios

| Area | Evidence |
|---|---|
| Versioned strict metadata, required fields, strict scalar types, identifiers, hashes, mutable revisions, unsupported versions, and unknown fields | `tests/test_configuration.py::test_valid_metadata_set_is_typed_and_hashed`, `test_invalid_model_metadata_is_rejected`, `test_unknown_metadata_field_and_missing_required_field_are_rejected` |
| Duplicate YAML keys, malformed/non-UTF-8 YAML, non-finite values, and secret-safe errors | `tests/test_configuration.py::test_duplicate_yaml_keys_are_rejected`, `test_non_finite_numeric_values_are_rejected`, `test_unknown_field_is_rejected_without_echoing_value` |
| Contained relative references, missing/wrong files, URLs, mismatches, parent traversal, and symlink escape | `tests/test_configuration.py::test_reference_mismatch_and_escape_are_rejected`, `test_reference_urls_and_non_yaml_paths_are_rejected`, `test_symlink_escape_is_rejected` |
| Exact source and canonical semantic SHA-256 identity, formatting/key-order independence, list order, Unicode, and semantic changes | `tests/test_configuration.py::test_semantic_hash_ignores_yaml_formatting_but_source_hash_does_not`, `test_semantic_hash_preserves_list_order_unicode_and_value_changes` |
| Valid identity-only examples without external artifact claims | `tests/test_examples.py::test_foundation_example_is_valid_identity_only_configuration` |
| Git root, full commit, branch, clean/dirty/staged/untracked/detached/no-commit behavior | `tests/test_provenance.py::test_clean_git_provenance_records_root_commit_branch_and_clean_state`, `test_git_provenance_detects_dirty_and_detached_states`, `test_git_provenance_rejects_missing_repository_or_commit` |
| Local runtime facts, secret exclusion, portable paths, intended versus observed hardware, strict manifest round-trip, unknown fields, and trailing newline | `tests/test_provenance.py::test_environment_capture_is_local_and_secret_free`, `test_manifest_round_trip_is_strict_canonical_and_portable` |
| UTC sortable private IDs and repeated-run uniqueness | `tests/test_lifecycle.py::test_run_id_is_utc_sortable_private_and_unique` |
| Exclusive staging, atomic publication, collision preservation, injected write failure, immutable manifests, and read-only integrity inspection | `tests/test_lifecycle.py::test_prepare_publishes_one_complete_manifest_and_show_is_read_only`, `test_prepare_collision_preserves_existing_bytes`, `test_write_failure_leaves_no_published_run`, `test_manifest_overwrite_is_refused_without_changing_bytes`, `test_show_run_distinguishes_missing_corrupt_and_mismatched_runs` |
| CLI command set, JSON streams, exit classes, side-effect-free validation, and validate → prepare → show | `tests/test_cli.py` |

## Issue #1 acceptance checks

| Acceptance criterion | Evidence |
|---|---|
| Tasks 1.1–6.5 complete without scope expansion | `openspec/changes/foundation-experiment-platform/tasks.md`, final diff inspection |
| Five metadata kinds reject unsafe or unfrozen input | Configuration tests listed above; `uv run thesis-bench validate-config examples/foundation/experiment.yaml` |
| Deterministic source and semantic hashes | Configuration hash tests listed above |
| Preparation requires committed clean Git and records approved provenance | Provenance/lifecycle tests listed above; CLI dirty-tree test |
| Atomic, immutable, collision-safe manifests | Lifecycle tests listed above |
| Three JSON CLI commands and exit codes | `tests/test_cli.py` |
| Routine verification is model-, GPU-, credential-, and inference-free | `pyproject.toml`, `.github/workflows/ci.yml`, and the exact CI-equivalent command list in `docs/development/testing.md` |
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
npx --yes --package renovate renovate-config-validator renovate.json
npx --yes @fission-ai/openspec validate foundation-experiment-platform --strict --no-interactive
```
