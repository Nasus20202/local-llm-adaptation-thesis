# Public evaluator custody amendment

- **Date:** 2026-09-05
- **Tool/model:** Codex; exact runtime model metadata is not retained in the repository.
- **Task:** Prepare a governance/OpenSpec amendment after the researcher rejected the unnecessary external-private-storage requirement for non-confidential development evaluator answers.
- **Affected artifacts:** `openspec/changes/development-public-evaluator-custody/`, `docs/research/development-pilot-public-evaluator-custody-amendment-v1.md`, and project status/roadmap updates.
- **Protected logical root:** `development-protected-evaluator-v1`, proposed to bind to a dedicated repository-relative evaluator subtree after approval.
- **Contribution:** Public development-evaluator storage is proposed while preserving exclusion from model-facing exports, RAG, training, prompts, harnesses, W1 inputs, participant workspaces, logs, and diagnostics. Final-test custody and semantic-judge gates remain unchanged.
- **Human verification:** Human Gate A review and approval are required before implementation or evaluator-bundle authoring.
- **Related work:** Issue #35; follow-up PR to be opened from this amendment branch.
- **Boundary:** No protected evaluator criteria, answer-bearing evidence maps, fixture payloads, model outputs, judge configuration, or final-test material are reproduced in this log.
