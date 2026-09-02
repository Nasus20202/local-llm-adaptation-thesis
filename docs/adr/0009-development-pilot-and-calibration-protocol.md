# ADR-0009: Development Pilot and Evaluator Calibration Protocol

- **Status:** Proposed for Human Gate A
- **Date:** 2026-09-02
- **Decision owner:** Human researcher

## Context

The accepted benchmark domain supports several adaptation mechanisms, but a final benchmark cannot be frozen until development evidence establishes task headroom, evaluator reliability, contamination controls, and operational feasibility. Issue #4 also asks whether controlled live-cluster tasks and official-source web access can be studied without confounding harness behavior or closed-corpus RAG.

## Considered alternatives

1. Freeze a static offline benchmark directly from the Issue #2 policy.
2. Run a bounded development-only feasibility pilot with preregistered target strata, calibrated evaluators, and separately gated `kind` and W1 conditions.
3. Build a broad live-agent and open-web benchmark before the core static study.

## Proposed decision

Select alternative 2 and use [the development-only protocol](../research/benchmark-pilot-protocol.md) as the authoritative methodology.

The pilot contains 24 independent development families, balanced by task class and language. It preregisters mechanism-aligned target strata, keeps repeats and variants nested, qualifies human ratings with independent calibration, and uses explicit `GO`/`AMEND`/`STOP` progression criteria. A small resettable `kind` stratum and an official-source W1 web-search sensitivity condition are admitted only through their own feasibility gates.

R1 remains retrieval from the pinned closed corpus. H1 remains orchestration with no implicit web access. Every applicable interactive condition receives the same neutral cluster interface and permissions. Combined conditions are explicitly named and compared with their strongest constituent.

C2 eligibility and comparator identity are frozen from model-independent family metadata and a design-time rule before any pilot output. If pilot error analysis is used to identify complementary failures, the pilot C2 contrast is exploratory and confirmatory C2 requires fresh, family-disjoint development families.

Contamination reports distinguish public source/domain exposure, semantic-pattern exposure, and direct-item exposure. No unsupported numerical probability or contamination-free claim is permitted.

## Rationale

Alternative 1 risks freezing ambiguous tasks, insensitive metrics, and unreliable rubrics. Alternative 3 would add live-service and agent complexity before core constructs are validated. The selected design creates mechanism-sensitive opportunities without selecting tasks for positive method results and preserves a feasible workload for one MSc researcher.

## Consequences

- Pilot results are feasibility evidence, not thesis effectiveness results.
- Final-test content remains unconstructed and inaccessible throughout this change.
- A second technically competent rater is required for bounded calibration and a stratified reliability subset, not for every final rating.
- Interactive and web conditions may be deferred without invalidating the static benchmark if their gates fail.
- Negative and inconclusive method effects remain reportable outcomes.
- The accompanying OpenSpec package must be approved before Codex implements dataset, evaluator, tool-capture, or cluster-execution behavior.

## OpenSpec decision

Create the narrow `benchmark-pilot-evaluation-foundation` change because protected-content boundaries, evaluator qualification, invalidity reason codes, matched cluster permissions, reset/egress checks, W1 budgets, and write-before-expose provenance are observable software behavior. The change explicitly excludes model execution and benchmark payloads and leaves integration with existing runner/CLI capabilities for a later approved change.

## Approval record

Pending explicit Human Gate A approval. Approval will authorize Codex implementation of the accompanying software package only. It will not authorize pilot/final item or fixture-payload construction, real cluster/web/model execution, or final-test access.
