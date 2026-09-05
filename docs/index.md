# Local LLM Adaptation Thesis

This site is the human-readable documentation for the MSc thesis project comparing local LLM optimization and adaptation methods. The documentation explains the research design, project state, architecture, decisions, and implementation guidance; OpenSpec remains the normative software contract.

## Start here

1. [Project status](project/status.md) — the current stage and next authorized work.
2. [Research questions](research/research-questions.md) — what the study is trying to answer.
3. [Experimental design](research/experimental-design.md) — conditions and comparisons.
4. [Evaluation strategy](research/evaluation.md) — how model outputs and runs are evaluated.
5. [System overview](architecture/system-overview.md) — how the research software is structured.
6. [Glossary](glossary.md) — algorithms, metrics, tools, and project terminology.

## Current development pilot

The development-only pilot package is documented in the [pilot protocol](research/benchmark-pilot-protocol.md), [authorization](research/development-pilot-authorization.md), [approved scenario inputs](research/development-pilot-scenario-inputs.md), [human review record](research/development-pilot-scenario-review.md), and approved [protected evaluator design](research/development-pilot-protected-evaluator-design.md). Human Gate A for the evaluator contract passed in PR #47, and the resulting generic protected-evaluator implementation was independently reviewed and squash-merged in PR #50. The next research step is preparation and review of the 24 protected evaluator bundles under `development-protected-evaluator-v1`. Concrete semantic-judge selection/execution, participant-model execution, training, and final-test material remain closed behind later gates.

## Documentation areas

- **Research** — scientific methodology and the reasoning behind the study.
- **Project** — status, roadmap, governance, and workflow.
- **Architecture** — research-software structure, lifecycle, data flow, and reproducibility.
- **Decisions** — consequential ADRs and rejected alternatives.
- **Development** — concise implementation and verification guidance.
- **Audit material** — research, GenAI, and experiment logs remain in the repository for provenance but are intentionally excluded from the rendered site.

Use the navigation and search to browse the site. Source pages remain version-controlled under `docs/` and can be edited directly from each rendered page.
