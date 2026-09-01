# Contributing

This is a research repository with a human approval gate for consequential changes.

## Workflow

1. Select a GitHub Issue in the active milestone.
2. Follow the [AI-driven development lifecycle](docs/project/aidlc.md).
3. For substantial behavior, prepare and validate an OpenSpec change, then stop for Human Gate A.
4. Create a focused branch with an English kebab-case name.
5. Implement the approved package incrementally with tests; avoid unrelated refactoring.
6. Run the relevant verification suite and OpenSpec validation.
7. Open a pull request using the repository template. Ask Chat for an independent review against the Issue, OpenSpec, research constraints, and acceptance criteria.
8. Send implementation defects back to Codex. Return specification, architecture, or methodology defects to Work, then re-review material fixes.
9. The human researcher merges only after review passes.
10. After merge, Work archives/synchronizes OpenSpec and updates the Issue, status, roadmap, and evidence logs.

## Commit and pull-request language

Use English Conventional Commits: `<type>(<optional-scope>): <imperative summary>`. Use the narrowest appropriate type, normally `feat`, `fix`, `docs`, `test`, `refactor`, `build`, `ci`, `chore`, or `research`. Keep each commit focused; Renovate uses `chore(deps):`.

## Research changes

Changes to research questions, benchmark construction, data splits, metrics, statistical analysis, model selection, inference parameters, or validity rules require explicit human review. Explain the scientific consequence, not only the code change.

## Data and results

Do not commit model weights, private data, or third-party material without verified redistribution rights. Raw experiment runs are immutable. Correct an invalid run by recording its status and producing a new run.

## AI-assisted work

Significant generative-AI use must be recorded under `docs/genai-log/` with human verification and a related commit or PR when available. The human author remains responsible for all content.
