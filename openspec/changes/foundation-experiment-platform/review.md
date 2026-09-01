# Cross-Artifact Review

**Review date:** 2026-09-02
**Review status:** Revision-identity amendment approved at focused Human Gate A; task 2.1 implementation completed on PR #18.

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
- Unknown/duplicate data, revision identity, unsafe references, dirty Git, collisions, corrupt manifests, and CLI errors have explicit behavior and test obligations.
- No task authorizes inference, method implementation, benchmark content, observations, or results.
- Stable project policy does not pin an OpenSpec release or assume old command syntax.
- The package is precise enough for a Budget Implementation Model without requiring it to choose methodology or consequential architecture.

## Revision-identity amendment

- Model revision accepts one unambiguous source format: a full 40-character lowercase Git commit ID. The existing artifact SHA-256 remains the independent byte identity.
- Dataset revision and evaluation version are stable labels, not self-proving immutable locators. Their accepted grammar and three reserved moving labels are exhaustive for schema version 1.
- Dataset identity is completed by split and manifest SHA-256. Evaluation identity is completed by the evaluation document semantic hash and prepared run Git commit.
- Exhaustive branch-name detection, remote resolution, new provider abstractions, and new metadata fields remain out of scope.

## Acceptance coverage

Every requirement has at least one WHEN/THEN scenario, and every scenario maps to a task or explicit verification item. Task 2.1 is reopened only for the amended identity grammar and focused regression tests. No other implementation task is reopened. The implementation must remain smaller than the specification if equally clear code can satisfy it; document any contradiction instead of adding abstractions.

## Decision

The amended package was internally consistent for focused Human Gate A approval. PR #18 remains open and the change remains unarchived. Codex updated only task 2.1 and its evidence; Chat should now perform a focused independent re-review before human merge.
