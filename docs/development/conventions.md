# Development Conventions

## Language and naming

All engineering artifacts use English. Python identifiers use `snake_case`, classes use `PascalCase`, and configuration fields use `snake_case`. Stable public field names are changed only through a schema-version decision.

## Python baseline

The approved foundation targets CPython `>=3.14` and pins the current developer/CI interpreter to 3.14.7 in the repository `.python-version`. It uses `uv` for locked environments, Hatchling for packaging, Pydantic v2 for strict typed schemas, PyYAML for configuration input, `argparse` for the small CLI, pytest, Ruff, and mypy. Renovate proposes Python patch and feature-series updates from `.python-version`; a candidate update can merge only when required CI remains green.

`pyproject.toml` must declare an exact `[tool.uv] required-version`. CI reads both the Python pin and the `uv` requirement from repository files rather than duplicating versions in workflow YAML. Renovate covers `.python-version`, supported Python dependency and lockfile managers, the exact `uv` version, and GitHub Actions. Patch and minor updates use semantic commits and automerge after required checks. Major updates remain manual. OpenSpec is upgraded deliberately outside Renovate because its generated skills and command contract must be refreshed and reviewed.

## Repository practices

- Keep modules small and cohesive; avoid speculative plugin systems.
- Prefer explicit files, schemas, and pure functions over framework indirection.
- Use `pathlib` and UTF-8 explicitly.
- Treat timestamps as timezone-aware UTC.
- Log structured lifecycle facts without logging secrets or full restricted data.
- Never commit weights, credentials, virtual environments, caches, or unlicensed datasets.
- Keep raw results append-only; regenerate processed outputs.

## Version control

Use short English branch names, Conventional Commits with imperative summaries, focused pull requests, and links to the GitHub Issue and OpenSpec change. Do not mix unrelated refactoring with experimental changes.
