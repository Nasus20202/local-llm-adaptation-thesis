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

## Verification and handoff

Run the complete relevant test suite, static checks, configuration validation, OpenSpec validation, and inspect the final diff. Map evidence to acceptance criteria. Report commands, results, remaining risks, and any intentionally deferred work. Do not archive the OpenSpec change or merge a major change before review.

## First approved handoff

After explicit approval of [Issue #1](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/1) and its OpenSpec package, the intended instruction is:

> Implement the approved `foundation-experiment-platform` OpenSpec change. Read `AGENTS.md`, the linked GitHub Issue, all referenced architecture/ADR documents, and the complete OpenSpec change before editing. Follow the tasks, use tests, run verification, and do not expand scope.

In Codex, this handoff may invoke `$openspec-apply-change` explicitly after Human Gate A approval.
