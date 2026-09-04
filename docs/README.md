# Documentation

This folder is the human-readable explanation of the thesis project. OpenSpec is the normative software contract; `docs/` should explain the research, decisions, terminology, and current state without making the reader reconstruct them from specifications or logs.

## Start here

1. [Project status](project/status.md) — what stage the thesis is in and what happens next.
2. [Research questions](research/research-questions.md) — what the study is trying to answer.
3. [Experimental design](research/experimental-design.md) — conditions and comparisons.
4. [Evaluation strategy](research/evaluation.md) — how answers and runs are scored.
5. [Glossary](glossary.md) — algorithms, metrics, tools, and project terminology.
6. [Approved development-pilot questions](research/development-pilot-scenario-review.md) — the 24 model-facing questions approved in PR #44; reviewer notes on that page are not evaluator truth.
7. [Protected development evaluator design](research/development-pilot-protected-evaluator-design.md) — the current scientific design and custody boundary before Codex implementation.

## What the folders are for

| Path                                             | Use                                                                                  |
| ------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `research/`                                      | Scientific methodology and the reasoning behind the study. Read this for the thesis. |
| `project/`                                       | Current status, roadmap, governance, and workflow.                                   |
| `adr/`                                           | Consequential decisions and rejected alternatives.                                   |
| `architecture/`                                  | How the research software is structured.                                             |
| `development/`                                   | Developer-facing implementation guidance.                                            |
| `literature/`                                    | Literature-review notes and evidence tables.                                         |
| `research-log/`, `genai-log/`, `experiment-log/` | Audit trail. Useful for provenance; not intended to be read front-to-back.           |

## Documentation rule

When the project introduces an algorithm, metric, tool, or technology that matters to the research, the human-facing documentation should explain four things briefly: **what it is, how it works, why it is used here, and where to find a primary or official source**. Add or update the [glossary](glossary.md) instead of repeating the same explanation across many files.

Keep explanatory docs short and linked. Do not restate OpenSpec requirements in prose, and do not turn audit history into tutorial text.
