# ADR-0005: OpenSpec Workflow

- **Status:** Accepted
- **Date:** 2026-08-31

## Context

Substantial implementation changes need repository-native contracts that a fresh Codex session can follow and that Work and the researcher can review before code exists.

## Considered alternatives

1. GitHub Issues only.
2. Free-form design documents.
3. OpenSpec's current expanded `spec-driven` workflow.

## Decision

Use the current reviewed OpenSpec workflow initialized for Codex. Track its generated workflow skills under `.agents/skills/openspec-*/SKILL.md`; Codex uses skills rather than generated slash commands. Major changes follow exploration, change creation, proposal, capability specs, design, tasks, cross-artifact review, validation, Human Gate A, implementation, verification, independent review, human merge, then archive/synchronization. Inspect current commands and regenerate skills before accepting an OpenSpec upgrade.

## Rationale

Issues remain concise work trackers while specifications define normative behavior and tasks preserve traceability. Stable policy describes workflow concepts rather than freezing release-specific command syntax.

## Consequences

Small documentation fixes do not require OpenSpec. Research rationale remains in `docs/research/` and is referenced rather than duplicated. No major TODO/TBD may remain at approval. OpenSpec upgrades are performed deliberately outside Renovate because the generated skills and command contract require regeneration, diff review, and validation.
