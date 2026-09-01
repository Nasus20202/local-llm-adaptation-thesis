# Testing Strategy

## Test layers

- **Unit tests:** deterministic configuration, canonicalization, hashing, manifest validation, path handling, and lifecycle invariants.
- **Integration tests:** CLI boundaries, Git metadata capture in temporary repositories, atomic run creation, manifest immutability, and read-only inspection.
- **Contract tests:** future inference adapters against recorded or fake process responses.
- **Opt-in system tests:** real local models and hardware; never part of routine CI.
- **Scientific validation:** fixture experiments that confirm conditions differ only where specified and evaluators produce expected metrics.

## Required properties

- Tests must not download or load multi-gigabyte models.
- Time and randomness must be injectable or matched structurally rather than asserted as fixed values.
- Tests use temporary result roots and prove that an existing raw run cannot be overwritten.
- Invalid configuration tests cover missing, unknown, malformed, incompatible, and unsupported-version fields.
- Hash tests use stable fixtures and document canonicalization expectations.
- CLI tests assert exit codes and machine-readable error behavior, not incidental terminal formatting.

## CI policy

Routine CI uses the repository-pinned Node.js, Python, and `uv` versions and runs lock consistency, formatting/linting, static typing, unit/integration tests, package build, example-config validation, Renovate configuration validation, and strict OpenSpec validation. Network access after dependency installation and real-model inference are prohibited unless a later workflow is explicitly approved and isolated.

Renovate pull requests must pass the same required workflow as human-authored changes. Patch and minor updates, including a stable Python feature-series update such as 3.14 to 3.15, may automerge when every required check passes. Major updates and every OpenSpec update require manual review.

## Local verification commands

From a locked environment, run the same checks as CI:

```bash
uv sync --locked
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

These checks use metadata fixtures and temporary Git/result roots only. They do not download model weights, load a model, contact an inference backend, or persist observations.
