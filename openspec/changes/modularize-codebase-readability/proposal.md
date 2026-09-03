## Why

The pilot-foundation implementation is scientifically bounded but concentrated in production and test modules that are difficult for one researcher to review safely. Refactoring now, before more experiment capabilities depend on these modules, reduces review and change risk without altering approved methodology or observable behavior.

## What Changes

- Replace oversized production modules with cohesive capability subpackages for pilot data, evaluation, controlled-cluster execution, web-search sensitivity, configuration, and provenance.
- Separate declarative records, pure validation and calculation logic, persistence, adapters, fakes, and opt-in entry points where those responsibilities are currently combined.
- Preserve the existing public import paths and exported names through explicit compatibility facades.
- Reorganize oversized tests by behavior under matching capability packages (`tests/config`, `tests/provenance`, `tests/pilot`, `tests/evaluation`, `tests/cluster`, and `tests/web`) while preserving their scientific assertions and deterministic boundaries.
- Treat 250 physical lines as the default maximum for hand-written Python source and test files, with only explicit cohesion-based exceptions documented during review.
- Preserve compatibility checks for the public import surface while reviewing readability through the implementation diff and normal formatting/lint checks.

## Capabilities

### New Capabilities

None. This change is a behavior-preserving refactor and declares `skip_specs: true` rather than inventing a new externally observable capability.

### Modified Capabilities

None. Existing OpenSpec requirements, public behavior, schemas, and scientific rules remain unchanged.

## Impact

The change affects the internal organization of `src/thesis_bench/` and corresponding tests, especially `pilot`, `evaluation`, `cluster`, `web`, `config`, and `provenance`. Existing consumers continue to import the same public names from the same top-level module paths. No dependency, CLI, schema, serialization, hash, result, external-service policy, or experiment configuration changes are intended.
