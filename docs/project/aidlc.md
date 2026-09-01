# AI-Driven Research and Development Lifecycle

## Purpose

This lifecycle supports an MSc scientific study. Research questions, validity, reproducibility, and evidence quality govern the backlog; software is the smallest infrastructure needed to run and audit the experiments. Repository artifacts, not conversation history, are the durable handoff.

## Stable model roles

| Role | Primary environment | Responsibility |
|---|---|---|
| Human researcher | — | Final decisions, specification approval, merge, experiment freeze, and academic responsibility |
| Frontier Planning Model | ChatGPT Work | Literature, methodology, research design, consequential architecture, ADRs, OpenSpec, analysis, and Polish thesis integration |
| Budget Implementation Model | Codex | Approved code, tests, CI, implementation debugging, experiment execution, raw-output capture, and technical verification |
| Frontier Reviewer | ChatGPT Chat | Independent review of correctness, scientific fidelity, reproducibility, scope, tests, fairness, and unnecessary complexity |
| Escalation Implementation Model | Codex | Exceptional implementation-only escalation after the specification is clear and the budget model has failed |

Concrete model names are runtime recommendations, never stable policy.

## Core lifecycle

1. **Work designs:** inspect current state and evidence; define the research purpose, methodology, risks, architecture, Issue, and OpenSpec package.
2. **Human Gate A:** the researcher reviews and explicitly approves the complete implementation package.
3. **Codex implements:** the Budget Implementation Model builds only the approved minimum, writes tests, verifies it, and opens a pull request without merging.
4. **Chat reviews:** the Frontier Reviewer independently compares the pull request with research documents, the Issue, OpenSpec, ADRs, and architecture.
5. **Codex fixes:** implementation defects return to Codex. Specification, architecture, or methodology defects return to Work for an upstream correction. Material fixes are re-reviewed.
6. **Human merges:** the researcher merges only after the review outcome permits it.
7. **Work synchronizes:** inspect the merged state, archive/synchronize OpenSpec with the current workflow, update the Issue, milestone, status, and evidence logs, then prepare the next research step.

## Research-driven change preparation

Before substantial engineering work, identify the scientific capability or research question it supports. For experiment-affecting work, define relevant hypotheses, variables, controls, benchmark subsets, leakage risks, confounders, measurements, and validity threats. Do not force this ceremony onto trivial maintenance.

For substantial software behavior use the current OpenSpec concepts:

`explore → create change → proposal → specs → design → tasks → cross-artifact review → validate → Human Gate A`

The package is ready only if a competent Budget Implementation Model can implement it without making major architectural or methodological decisions. Resolve invariants, errors, edge cases, acceptance criteria, and scientific constraints upstream without overspecifying internals.

Generated OpenSpec skills live under `.agents/skills/`. Do not edit them manually or hard-code an OpenSpec release in stable policy. During an upgrade, inspect the current installation and documentation, regenerate skills, review the diff, and validate active changes.

## Handoffs

### Work to Codex

Stop before implementation and present the scientific goal, implementation goal, scope, non-goals, decisions, requirements, acceptance criteria, tasks, and unresolved risks. After approval, provide one concise prompt that directs Codex to repository sources rather than restating the thesis.

### Codex to Chat

After a substantial pull request, explicitly ask for independent review. The review priority is:

1. scientific requirement compliance;
2. correctness and reproducibility;
3. OpenSpec and scope compliance;
4. tests and experimental integrity;
5. hidden methodology changes or unfair comparisons;
6. unnecessary engineering complexity.

Findings use `BLOCKER`, `IMPORTANT`, `MINOR`, or `OPTIONAL`, and conclude `READY TO MERGE`, `READY AFTER MINOR FIXES`, or `CHANGES REQUIRED`.

### Review triage

- Bugs, missing tests, incomplete tasks, and needless code complexity are implementation defects: send a focused fix prompt to the Budget Implementation Model.
- Ambiguous requirements, invalid research assumptions, leakage, unfair design, or architecture that distorts comparison are planning defects: keep them in Work and amend the authoritative artifacts before implementation continues.
- Re-review significant fixes, concentrating on prior `BLOCKER`/`IMPORTANT` findings and regressions.

## Experiment and results lifecycle

Before a formal run, freeze and verify Git state, model revision and artifact hash, dataset version/hash and split, experiment configuration, prompt/evaluation versions, generation settings, and applicable method configuration. Raw runs are immutable; invalid runs remain preserved with a predeclared reason.

Codex may execute an approved experiment and perform mechanical validation. Work validates completeness, performs scientific/statistical analysis, separates `FACT`, `STATISTICAL RESULT`, `INTERPRETATION`, and `LIMITATION`, and integrates validated evidence into the Polish thesis. Chat may independently challenge major conclusions.

Engineering artifacts remain English. Thesis prose remains Polish and progresses through `DRAFT`, `EVIDENCE-VALIDATED`, `REVIEWED`, and `READY FOR SUPERVISOR REVIEW` as applicable.

## Required next-action contract

At every meaningful stop, Work provides exactly one concrete next action with:

- **What you should do**
- **Where**: ChatGPT Work, Codex, ChatGPT Chat, GitHub, local terminal, Kaggle, or another justified tool
- **Model role**
- **Current recommended model** when useful, explicitly time-dependent
- **Reasoning level**
- **Why**
- **Exact prompt** whenever another AI session is required

Never leave the researcher to infer whether to approve, dispatch Codex, request review, fix, merge, synchronize, or run an experiment.
