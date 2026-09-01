# ADR-0007: Evaluation Architecture

- **Status:** Proposed
- **Date:** 2026-08-31

## Context

Knowledge, procedural, and mixed tasks need different success criteria. An opaque proprietary LLM judge cannot be the only evaluator, and the final test must remain untouched during method development.

## Considered alternatives

1. One aggregate score for every task.
2. Proprietary LLM judge as the primary evaluator.
3. Task-specific deterministic metrics plus blinded human rubrics and optional supplemental judges.

## Proposed decision

Define metric applicability per benchmark item. Prefer deterministic exact/schema/constraint/task checks; use versioned human rubrics for qualities that cannot be automated; permit LLM judges only as supplemental sensitivity analyses with complete provenance. Store evaluation outputs as derived artifacts keyed by raw run and evaluator version.

## Rationale

This respects task heterogeneity, reduces evaluator bias, and allows corrected evaluation logic without altering raw outputs.

## Consequences

Benchmark construction must include evaluator fixtures and adjudication rules. Inter-rater reliability and multiplicity handling must be predeclared. Final acceptance awaits the benchmark domain and pilot evidence.
