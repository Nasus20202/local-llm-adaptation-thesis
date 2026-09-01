# GitHub Project Management

## Milestones

GitHub milestones mirror M0–M12 in `roadmap.md`. They are planning containers, not normative requirements. Milestone descriptions use the roadmap exit conditions; no artificial due dates are assigned during bootstrap.

## Label taxonomy

Use a small orthogonal taxonomy when labels are available:

- Type: `type:research`, `type:implementation`, `type:documentation`, `type:governance`
- Area: `area:benchmark`, `area:inference`, `area:prompting`, `area:rag`, `area:fine-tuning`, `area:harness`, `area:skills`, `area:evaluation`, `area:thesis`
- Workflow: `status:blocked`, `needs:human-decision`, `needs:scientific-review`
- Priority: `priority:near-term` only when it materially distinguishes the active backlog

Avoid labels that duplicate milestone names or task completion state.

## Bootstrap issue policy

M0/M1 issues are detailed enough to execute or decide. M2–M12 initially use one coarse tracking issue per milestone and must be refined only after preceding evidence is available. Substantial implementation issues link an authoritative OpenSpec change and do not copy its full design.
