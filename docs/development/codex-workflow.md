# Codex Workflow

## Before editing

1. Read the root `AGENTS.md`.
2. Read the linked GitHub Issue and every referenced research, architecture, and ADR document.
3. Read the complete approved OpenSpec change: proposal, specifications, design, and tasks.
4. Inspect the existing tree and Git status. Preserve unrelated human changes.
5. Confirm that Human Gate A is approved for a major change.

## During implementation

- Use the repository skill `$openspec-apply-change` for an approved OpenSpec implementation. The generated OpenSpec skills live under `.agents/skills/` and are refreshed deliberately with `openspec update --force`.
- Implement the approved tasks incrementally and keep the change narrow.
- Write or update tests before relying on behavior.
- Keep pure schema, hashing, and evaluation logic independent of model loading.
- Run targeted tests and static checks frequently.
- Do not alter experimental meaning, model revisions, datasets, prompts, or result schemas silently.
- Record any necessary specification deviation and stop for review if it changes scope or scientific validity.
- If the package is ambiguous or contradictory, report the blocker. Do not invent methodology or a general framework.

## Verification and handoff

Run the complete relevant test suite, static checks, configuration validation, all-spec OpenSpec validation (`openspec validate --all --strict --no-interactive`), and inspect the final diff. Map evidence to acceptance criteria. Report commands, results, remaining risks, and any intentionally deferred work. Open a pull request, but do not archive OpenSpec or merge.

The next default step is an independent Chat review. Implementation findings return to Codex; methodology, specification, or consequential architecture findings return to Work. After material fixes, request a focused re-review. The human researcher performs the merge after review passes.

## First approved handoff

After explicit approval of [Issue #1](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/1) and its OpenSpec package, the intended instruction is:

> Implement the approved `foundation-experiment-platform` OpenSpec change. Before editing, read `AGENTS.md`, `docs/project/status.md`, GitHub Issue #1, the complete OpenSpec change, and every document they reference; then inspect the repository state. Implement only the approved scope as the smallest clear research-support implementation. Follow the requirements, design, tasks, and acceptance criteria; write the required tests and run all relevant verification. Do not invent methodology, architecture, abstractions, or infrastructure. If the package is insufficient or contradictory, stop and report the blocker. When complete, summarize the implementation and verification, list deviations or concerns, and provide the pull-request URL. Do not merge.

In Codex, this handoff may invoke `$openspec-apply-change` explicitly after Human Gate A approval.
