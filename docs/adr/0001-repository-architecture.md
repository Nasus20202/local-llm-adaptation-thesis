# ADR-0001: Repository Architecture

- **Status:** Accepted
- **Date:** 2026-08-31

## Context

The thesis requires research rationale, normative software behavior, implementation, raw observations, regenerated analysis, and Polish thesis prose to coexist without becoming conflicting sources of truth.

## Considered alternatives

1. Separate repositories for software, data, and thesis.
2. One repository organized by artifact role.
3. A notebook-centric repository with informal folders.

## Decision

Use one private Git repository organized by source-of-truth role: `docs/`, `openspec/`, future `src/` and `tests/`, configuration/data/result areas, and `thesis/`. Create directories only when they contain a useful artifact. Keep weights, caches, secrets, restricted datasets, and large generated outputs outside Git.

## Rationale

A single history makes requirement-to-result-to-thesis traceability practical for one researcher. Explicit artifact roles prevent a notebook or thesis paragraph from silently becoming the normative experiment definition.

## Consequences

Repository size must be monitored, external artifacts need checksums and retrieval instructions, and generated results require a deliberate publication policy. The structure is documented in `docs/project/source-of-truth.md`.
