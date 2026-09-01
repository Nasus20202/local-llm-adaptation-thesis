# AGENTS.md

## Purpose

This repository supports a theoretical-experimental MSc thesis comparing prompt engineering, RAG, LoRA/QLoRA, model harnesses, skills, and justified combined approaches for models evaluated on local consumer hardware. Optimize for scientific validity, traceability, and clarity—not product-scale architecture.

## Research first

- The thesis, research design, evidence, and reproducible results are the deliverables. Software exists only to make the experiments valid, repeatable, and inspectable.
- Before adding code, identify the research requirement, measurement, source of bias, or reproducibility risk it supports. If none exists, do not add it.
- Prefer the smallest readable implementation that preserves scientific correctness. Avoid speculative abstractions, framework layers, boilerplate, and comments or documentation that merely restate the code or OpenSpec.
- Spend complexity on experimental validity, contamination control, provenance, deterministic evaluation, statistical analysis, and traceability—not on product architecture.
- Keep code modules narrow and tests decisive. A compact implementation with strong scientific tests is preferable to a verbose generalized system.
- When engineering convenience conflicts with the approved methodology, stop and return to scientific review.

## Language

- Write code, tests, configs, Git history, GitHub artifacts, OpenSpec, ADRs, and engineering documentation in English.
- Write thesis prose, chapter titles, and thesis captions in Polish.
- Keep canonical technology names and bibliographic titles unchanged.

## Read before editing

1. Read [`docs/project/status.md`](docs/project/status.md) and the linked GitHub Issue.
2. Read the complete active OpenSpec change and every referenced research, architecture, and ADR document.
3. Inspect existing implementation, tests, and Git state.
4. Confirm that Human Gate A approved substantial implementation work.

## Role boundary

- Work is the Frontier Planning Model: it owns research, methodology, consequential architecture, specifications, and result interpretation.
- Codex is normally the Budget Implementation Model: implement and verify the approved scope without inventing methodology or architecture.
- Chat is the Frontier Reviewer: independently reviews substantial pull requests before merge.
- A stronger implementation model is an exception for a clear implementation problem that the budget model could not solve; it is not a substitute for a complete specification.
- The human researcher approves specifications and merges. Codex never merges its own substantial change.

## AIDLC routing

Use [`docs/project/aidlc.md`](docs/project/aidlc.md) for the complete lifecycle. The durable route is:

1. Research and design the change in repository documents.
2. Create or refine the GitHub Issue.
3. For a substantial change, prepare and strictly validate proposal, specs, design, and tasks with the generated OpenSpec skills under `.agents/skills/`.
4. Stop at Human Gate A. Do not implement until the human researcher approves the package.
5. Implement the approved package with `openspec-apply-change`, tests, and recorded verification evidence.
6. Open a pull request and stop. An independent Chat review checks scientific fidelity, correctness, reproducibility, scope, tests, and unnecessary complexity.
7. Fix implementation defects in Codex. Return methodology, architecture, or specification defects to Work. Re-review material fixes.
8. The human researcher merges only after review passes.
9. After merge, Work archives/synchronizes OpenSpec and updates status, roadmap, Issue, and evidence logs.

Use `$openspec-explore` for investigation, `$openspec-propose` for a new change, `$openspec-update-change` for an existing package, `$openspec-apply-change` only after Gate A, `$openspec-sync-specs` when reviewed delta specifications must be synchronized, and `$openspec-archive-change` only after merge. Do not edit the generated OpenSpec skills manually; regenerate and review them during a deliberate OpenSpec upgrade.

## Sources of truth

- `docs/research/`: scientific purpose and methodology—why the study is designed this way.
- `openspec/specs/`: normative software behavior—what the system must do.
- `docs/adr/`: consequential decisions and alternatives.
- GitHub Issues: work queue and status, not duplicated specifications.
- Source and tests: implementation of approved specifications.
- `results/raw/`: immutable observations.
- `results/processed/`: reproducible derivations.
- `thesis/`: Polish narrative, never the source of raw numbers.

Resolve conflicts using `docs/project/source-of-truth.md`; do not silently choose.

## Change control

- Substantial changes require an approved OpenSpec package.
- Never implement an unapproved major change.
- Do not expand scope or perform unrelated refactoring.
- Do not silently change a model, revision, quantization, prompt, dataset, split, seed, evaluation version, or experiment configuration.
- If the specification is ambiguous, contradictory, or requires an undocumented methodological or architectural decision, stop and report the exact blocker. Do not invent a design.

## Scientific integrity

- Keep train, development, and held-out test partitions separate.
- Do not tune against final test answers or expose golden answers to inference conditions.
- Do not edit frozen references because a model failed.
- Detect verbatim, semantic, and retrieval-time contamination.
- Record invalid and failed runs; never overwrite a run.
- Never fabricate experiments, results, citations, provenance, or verification evidence.
- A run without the required provenance is invalid, even if its output looks plausible.

## Engineering expectations

- Prefer files, Git, explicit typed schemas, and Python over infrastructure platforms.
- Use the CPython version pinned in `.python-version` and the exact `uv` version declared in `pyproject.toml`; do not duplicate toolchain versions in CI.
- Keep `renovate.json` valid. Renovate covers Python, supported package/lockfile managers, GitHub Actions, and the exact `uv` version; patch and minor updates may automerge only after required checks pass. Major updates remain manual. Upgrade OpenSpec deliberately and regenerate its skills; do not add post-upgrade commands to Renovate.
- Keep pure configuration/domain logic separate from external processes and real-model inference.
- Write deterministic unit tests for scientific logic and integration tests for critical file/CLI boundaries.
- Prefer tests that protect scientific invariants and failure behavior over broad tests that merely increase coverage.
- Routine CI must not download or run multi-gigabyte models; real-model tests are explicit and opt-in.
- Treat raw result directories as append-only. Derived artifacts may be regenerated from raw data.
- Do not commit credentials, model weights, generated caches, private data, or license-incompatible content.

## Current commands

Bootstrap planning validation:

```bash
npx --yes --package renovate renovate-config-validator renovate.json
npx --yes @fission-ai/openspec status --change foundation-experiment-platform
npx --yes @fission-ai/openspec validate foundation-experiment-platform --strict --no-interactive
```

Implementation commands will be added by the approved `foundation-experiment-platform` change. Do not invent them before implementation.

## Completion evidence

Before claiming completion, run every relevant test, static check, configuration validation, and OpenSpec validation; inspect `git diff` and verify each acceptance criterion. Report exact commands and outcomes.

## Git history

- Use Conventional Commits in English: `<type>(<optional-scope>): <imperative summary>`.
- Use the narrowest appropriate type, normally `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`, `chore`, or `research`.
- Keep commits focused and do not mix research decisions, generated results, and unrelated implementation changes.
- Renovate commits use `chore(deps):`.
