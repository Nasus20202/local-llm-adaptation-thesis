# Pilot Foundation Implementation Boundary

This document describes the software boundary implemented for the approved
[development-only benchmark pilot protocol](../research/benchmark-pilot-protocol.md)
and its [ADR-0009](../adr/0009-development-pilot-and-calibration-protocol.md)
without restating scientific decision thresholds.

## Roots and custody

Model-facing records contain development-only family metadata, permitted input
references, applicability, and hashes. Protected roots contain evaluator
bundles, expected results, evidence maps, rubrics, adjudications, and other
protected payloads. `ProtectedRootReference` records only a portable relative
path, root identity, and content hash. Model-facing serialization rejects
protected payload markers and validation diagnostics never echo payload values.

Family records use typed applicability declarations with an explicit reason for
each inapplicable approved condition, protected evaluator references, and
versioned target-stratum/comparator records. Each applicable condition also has
a condition-specific analysis contract validated against `pilot-policy-v1`,
including multi-comparator contrasts and the nested `B0-I` reference. C2
records reference a hash bound to the canonical pre-outcome declaration and
typed model-independent metadata; outcome-selected records remain exploratory
and confirmatory follow-ups carry both their linked exploratory-manifest
identity and family-disjoint exclusion set.

## Versioning and reason codes

Every new record carries `schema_version=1`; unknown versions are rejected.
Frozen identities and append-only stores reject mutation, collisions, and
overwrites. Statuses are `GO`, `AMEND`, and `STOP/DEFER`. Shared reason codes
cover record, custody, policy, budget, provenance, evaluator, safety, and
infrastructure decisions; records preserve the specific codes used.

## Opt-in external boundaries

Routine tests use `FakeCluster` and `FakeSearchFetchProvider`. The cluster
adapter requires an injected process/container implementation and the real
`kind` entry point currently returns prerequisite/help metadata only. The W1
boundary requires an explicit W1 or a separately approved combined-condition identity and
an injected provider; its qualification entry point is also prerequisite/help
only. These boundaries do not run from imports, default tests, or the existing
foundation CLI.

W1 providers expose redirect/status metadata through a body-free preparation
operation; the body-read operation consumes the immutable prepared handle only
after the W1 policy and budget checks pass. Denied redirects remain in
protected provenance while model-facing diagnostics are redacted. Cluster
final-state results come from the injected adapter, and budget exhaustion
terminates the append-only attempt as a valid failure.

Progression consumes typed evidence for every approved feasibility criterion.
The records preserve per-stratum headroom, provenance/access gates, critical
calibration disagreement, and qualification-attempt state so a scalar summary
cannot turn an unmeasured or unsafe criterion into `GO`.

## Later integration boundary

This package provides typed records, pure validators, deterministic fakes, and
bounded adapter contracts. Integrating them with model inference, the runner,
retrieval, fine-tuning, harnesses, skills, real clusters, live providers, or
raw experiment results requires a separately approved change. Final-test
material remains outside this implementation boundary.
