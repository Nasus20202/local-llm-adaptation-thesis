# Cross-Artifact Review

**Review date:** 2026-09-01
**Review status:** Ready for Human Gate A; implementation not authorized.

## Scientific purpose

The change protects later evidence from ambiguous configuration, mutable external identity, dirty source state, and overwritten provenance. Every included capability supports traceability or repeatable verification; none executes an experiment.

## Consistency matrix

| Proposal capability | Normative behavior | Design | Tasks |
|---|---|---|---|
| `experiment-configuration` | Strict documents, contained references, dual hashes, side-effect-free validation | Strict configuration and identity | 2.1–2.5; CLI in 5.2 |
| `run-provenance` | Manifest, clean Git commit, minimal runtime facts, safe portable paths | Clean Git provenance and manifest | 3.1–3.4 |
| `run-lifecycle` | Unique IDs, atomic creation, immutable manifest, read-only inspection | Immutable prepared run | 4.1–4.4 |
| `command-line-interface` | Three commands, JSON streams, stable error classes | Minimal CLI | 5.1–5.4 |
| Tooling and CI | Deterministic network/model-free verification | Minimal tooling and CI | 1.1–1.4; 6.1–6.5 |

## Scope reduction completed

The alignment review removed behavior that had no current experimental consumer:

1. append-only lifecycle events, locking, and event validation;
2. the custom dirty-working-tree content digest and dirty prepared runs;
3. a speculative manifest extension container;
4. per-concept module mandates and repository/service abstractions;
5. `fsync` durability machinery beyond exclusive staging and atomic publication.

These concerns may return only when an approved experiment or runner provides concrete requirements. Strict metadata, source/semantic hashes, clean-Git provenance, immutable manifest creation, inspection, focused tests, and CI remain because they directly protect scientific traceability.

## Cross-artifact findings resolved

- Proposal, four capability specs, design, tasks, Issue #1, architecture boundary, and status describe the same provenance-only slice.
- Unknown/duplicate data, mutable revisions, unsafe references, dirty Git, collisions, corrupt manifests, and CLI errors have explicit behavior and tests.
- No task authorizes inference, method implementation, benchmark content, observations, or results.
- Stable project policy does not pin an OpenSpec release or assume old command syntax.
- The package is precise enough for a Budget Implementation Model without requiring it to choose methodology or consequential architecture.

## Acceptance coverage

Every requirement has at least one WHEN/THEN scenario, and every scenario maps to a task or explicit verification item. No unresolved question changes approved scope or behavior. The implementation must remain smaller than the specification if equally clear code can satisfy it; document any contradiction instead of adding abstractions.

## Decision

The package is internally consistent and ready for Human Gate A. It remains unapplied and unarchived. After human approval, Codex may implement it; after the pull request, Chat performs an independent review before human merge.
