# AI-Driven Development Lifecycle

## Roles

- **Human researcher:** final decision-maker; approves major methodology, architecture, experiment, merge, and publication decisions.
- **ChatGPT Work:** research lead, methodology reviewer, architect, product owner, documentation owner, OpenSpec author, GitHub coordinator, scientific reviewer, and thesis integrator.
- **Codex:** implementation, tests, command execution, debugging, experiment execution, raw-result capture, and technical verification.

Git and repository artifacts are the communication boundary. Conversation history is never the durable specification.

## OpenSpec skill routing

- `$openspec-explore`: investigate and clarify without implementing.
- `$openspec-propose`: create a new proposal/specs/design/tasks package.
- `$openspec-update-change`: revise an existing package and reconcile its artifacts.
- `$openspec-apply-change`: implement only after Human Gate A approval.
- `$openspec-sync-specs`: synchronize reviewed delta specifications when the workflow requires it.
- `$openspec-archive-change`: archive only after merge and Human Gate B.

These skills are generated under `.agents/skills/`. Do not edit them manually. Upgrade OpenSpec deliberately, regenerate the skills, inspect their diff, and validate the active packages before accepting the upgrade.

## Lifecycle

1. **Governance:** maintain charter, language, AI policy, conventions, and source-of-truth rules.
2. **Discovery:** inspect repository state and authoritative sources; identify alternatives, uncertainty, and scientific consequences.
3. **Research design:** define purpose, question, variables, benchmark subset, evaluation, controls, and validity risks.
4. **Technical architecture:** define boundaries, interfaces, data flow, persistence, failure behavior, observability, reproducibility, and tests.
5. **Backlog:** create or refine an Issue with motivation, scope, dependencies, validation, and links.
6. **OpenSpec:** use `explore → change → proposal → specs → design → tasks → review → validation` for substantial changes.
7. **Human Gate A:** stop when a major implementation package is ready. Implementation requires explicit approval.
8. **Codex implementation:** Codex reads AGENTS.md, Issue, complete OpenSpec change, references, and current code; then implements incrementally with tests.
9. **Technical verification:** run tests, static checks, config validation, OpenSpec validation, task review, acceptance review, and diff inspection.
10. **Scientific review:** Work checks experimental fidelity, hidden variables, leakage, telemetry, reproducibility, and fairness.
11. **Human Gate B:** obtain merge approval for major changes.
12. **Archive and synchronize:** archive the OpenSpec change with the current workflow and update work state after merge.
13. **Experiment freeze and execution:** freeze revisions and hashes, execute approved software, and append a new immutable run.
14. **Analysis:** separate facts, statistical results, interpretation, and limitations.
15. **Thesis integration:** add only validated Polish narrative traceable to evidence.

## Gate A review package

Every major change must present: repository state, linked Issue, proposal/spec/design/tasks summary, acceptance criteria, verification plan, scientific risks, unresolved questions, and the exact recommended Codex instruction.

## Emergency rule

If implementation discovers that a requirement is scientifically invalid or infeasible, Codex stops, records evidence, and returns to Discovery. It does not silently “make it work” by changing the experimental condition.
