# ADR-0006: Experiment Provenance and Raw-Run Storage

- **Status:** Accepted
- **Date:** 2026-08-31

## Context

Results without complete input and environment identity cannot support scientific claims. Repeated and failed runs must remain auditable, and derived evaluation may evolve.

## Considered alternatives

1. Mutable result folders named by experiment.
2. A database or experiment-tracking server.
3. File-based unique runs with versioned manifests and append-only events.

## Decision

Use explicit versioned JSON/YAML schemas, SHA-256 identity, unique raw run directories, a manifest created once, and append-only observations/lifecycle events. Never overwrite a run. Write derived results to separately versioned paths. Record Git state, input hashes, model/backend/config identity, environment, timing, and outcome.

## Rationale

Files plus Git are inspectable, portable, and sufficient for the project scale. Append-only raw history prevents post-hoc cleanup from erasing inconvenient outcomes.

## Consequences

Tools must use exclusive/atomic creation and strict validation. Storage cleanup needs explicit retention rules, not silent deletion. Schema evolution must preserve readers or provide migrations for metadata, never rewrite observations.
