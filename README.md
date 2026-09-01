# Local LLM Adaptation Thesis

Research and reproducible software for the MSc thesis **“Comparison of Optimization and Adaptation Methods for Large Language Models in Local Environment.”** The Polish thesis title is *„Porównanie metod optymalizacji i dostosowania dużych modeli językowych pracujących w warunkach lokalnych”*.

The project compares adaptation strategies rather than foundation-model leaderboards. One primary local model will be used across the main matrix; a second model family will replicate selected conclusions. Target inference hardware is an AMD Radeon RX 5700 8 GB, Ryzen 5 3600, 32 GB RAM, Fedora Linux system using `llama.cpp` with Vulkan.

## Current status

The repository is at **M0 — Research & Project Foundation**. The approved [`foundation-experiment-platform`](openspec/changes/foundation-experiment-platform/) change provides the first provenance-only software slice: strict metadata validation, deterministic configuration identity, clean-Git manifests, immutable prepared-run directories, and read-only inspection. It does not execute models or create experimental results. See the concise [project status](docs/project/status.md) for the project gate and current research stage.

The current repository contains the research plan, methodology, architecture, governance, and the first reviewed implementation package. It does not yet contain the experiment platform or experimental results.

## Start here

- [Project charter](docs/project/charter.md)
- [Current project status](docs/project/status.md)
- [Current feasibility review](docs/research/current-feasibility-review.md)
- [Research questions](docs/research/research-questions.md)
- [System overview](docs/architecture/system-overview.md)
- [Roadmap](docs/project/roadmap.md)
- [GitHub project management](docs/project/github-management.md)
- [Bootstrap verification](docs/project/bootstrap-verification.md)
- [Instructions for agents](AGENTS.md)

## Foundation commands

Install the locked environment and validate the identity-only example:

```bash
uv sync --locked
uv run thesis-bench validate-config examples/foundation/experiment.yaml
```

The command boundary is deliberately limited to configuration validation, provenance-only run preparation, and run inspection:

```bash
uv run thesis-bench --version
uv run thesis-bench validate-config <experiment-path>
uv run thesis-bench prepare-run <experiment-path> [--results-root <path>]
uv run thesis-bench show-run <run-directory>
```

Versioned schema examples live under `examples/foundation/`; implementation modules and focused tests live under `src/thesis_bench/` and `tests/`. The example identifies external artifacts only; this change does not download or test them.

## Source-of-truth order

1. Project governance under `docs/project/`
2. Scientific rationale under `docs/research/`
3. Normative software behavior under `openspec/specs/` and active OpenSpec changes
4. Decisions under `docs/adr/`
5. GitHub Issues for work status
6. Source code and tests as implementation
7. Immutable observations under `results/raw/`
8. Polish narrative under `thesis/`

See [source-of-truth.md](docs/project/source-of-truth.md) for conflict resolution.

## Language policy

Engineering artifacts are written in English. The academic thesis and its captions are written in Polish. Canonical technology names and bibliographic titles retain their original form.

## OpenSpec

OpenSpec provides the artifact-guided `spec-driven` workflow. Upgrade it deliberately: review release notes, regenerate the Codex skills, inspect their diff, and validate active changes.

```bash
npx --yes @fission-ai/openspec status --change foundation-experiment-platform
npx --yes @fission-ai/openspec validate foundation-experiment-platform --strict --no-interactive
```

## Repository scope

Model weights, credentials, caches, private or unlicensed datasets, and generated runtime environments are excluded. Licensing of the final public repository remains a human decision; the bootstrap is private and all rights are reserved meanwhile.
