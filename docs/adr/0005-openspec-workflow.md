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

Use the current reviewed OpenSpec workflow initialized for Codex. Track its six generated workflow skills under `.agents/skills/openspec-*/SKILL.md`; Codex uses skills rather than generated slash commands. Major changes follow proposal, capability specs, design, tasks, cross-artifact review, strict validation, Human Gate A, implementation, technical/scientific review, Human Gate B, then archive/synchronization. Verify commands and regenerate skills with `openspec update --force` before accepting an OpenSpec upgrade.

## Rationale

Issues remain concise work trackers while specifications define normative behavior and tasks preserve traceability. Version pinning avoids relying on stale command names.

## Consequences

Small documentation fixes do not require OpenSpec. Research rationale remains in `docs/research/` and is referenced rather than duplicated. No major TODO/TBD may remain at approval. OpenSpec upgrades are performed deliberately outside Renovate because the generated skills and command contract require regeneration, diff review, and validation.
