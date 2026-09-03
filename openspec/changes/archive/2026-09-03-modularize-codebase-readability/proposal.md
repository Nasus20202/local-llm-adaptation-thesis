## Why

The pilot-foundation implementation is scientifically bounded but needs an inspectable package organization before more experiment capabilities depend on it. This change records the initial capability boundaries and compatibility surfaces used to make the implementation easier for one researcher to review safely; it does not claim a behavior-preserving test run against modules that were not present in the baseline.

## What Changes

- Replace oversized production modules with cohesive capability subpackages for pilot data, evaluation, controlled-cluster execution, web-search sensitivity, configuration, and provenance.
- Separate declarative records, pure validation and calculation logic, persistence, adapters, fakes, and opt-in entry points where those responsibilities are currently combined.
- Preserve the existing public import paths and exported names through explicit compatibility facades.
- Reorganize oversized tests by behavior under matching capability packages (`tests/config`, `tests/provenance`, `tests/pilot`, `tests/evaluation`, `tests/cluster`, and `tests/web`) while preserving their scientific assertions and deterministic boundaries.
- Treat 250 physical lines as the default maximum for hand-written Python source and test files, with only explicit cohesion-based exceptions documented during review.
- Preserve compatibility checks for the public import surface while reviewing readability through the implementation diff and normal formatting/lint checks. These checks characterize the organized implementation and are not presented as pre-organization evidence.

## Capabilities

### New Capabilities

None. This change organizes the initial implementation and declares `skip_specs: true` rather than inventing a new externally observable capability.

### Modified Capabilities

None. Existing OpenSpec requirements, public behavior, schemas, and scientific rules remain unchanged; the package boundaries document how that implementation is organized.

## Impact

The change affects the internal organization of `src/thesis_bench/` and corresponding tests, especially `pilot`, `evaluation`, `cluster`, `web`, `config`, and `provenance`. Existing consumers continue to import the same public names from the same top-level module paths. No dependency, CLI, schema, serialization, hash, result, external-service policy, or experiment configuration changes are intended. The compatibility checks validate those intended surfaces after organization; they do not assert that the same package modules existed before this change.
