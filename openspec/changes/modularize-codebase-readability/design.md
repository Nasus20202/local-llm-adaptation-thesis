## Context

See [proposal.md](proposal.md) for motivation. Six production modules currently combine several distinct responsibilities: `pilot.py` (893 lines), `web.py` (733), `cluster.py` (661), `evaluation.py` (629), `provenance.py` (290), and `config.py` (282). Four corresponding test modules are also above 250 lines. These modules implement approved scientific and safety boundaries, so this refactor must make them easier to inspect without changing their behavior.

The existing import paths are already used by the CLI, lifecycle code, examples, and tests. The current schemas, canonical serialization and hashing, redacted errors, append-only stores, deterministic statistics, and opt-in external boundaries are implementation evidence for the active pilot-foundation requirements. They are compatibility constraints for this change.

## Goals / Non-Goals

**Goals:**

- give each implementation module one clear responsibility and a dependency direction that can be understood locally;
- keep hand-written Python source and test files at or below 250 physical lines by default;
- retain cohesive groups of small declarative records while placing a substantial behavior-owning class in its own module when that improves comprehension;
- preserve current public imports, exports, data validation, serialization, hashes, errors, side-effect boundaries, and scientific outcomes;
- organize tests by behavior under the matching capability package (`tests/config`,
  `tests/provenance`, `tests/pilot`, `tests/evaluation`, `tests/cluster`, and `tests/web`)
  so production and test navigation use the same boundaries.

**Non-Goals:**

- changing any OpenSpec requirement, research method, threshold, schema field, CLI contract, or experiment configuration;
- introducing a framework, dependency-injection layer, generic repository/service pattern, or external dependency;
- optimizing runtime performance or redesigning algorithms while moving them;
- adding model inference, benchmark content, real external execution, or new end-user commands;
- forcing every small enum or declarative record into a separate file.

## Decisions

### 1. Convert oversized capability modules into compatibility packages

Replace each oversized module with a same-named package whose `__init__.py` explicitly re-exports the existing public API. Existing imports such as `from thesis_bench.pilot import PilotManifest` therefore remain valid. Internal callers may use direct submodule imports only when doing so makes the dependency clearer; external consumers are not required to adopt new paths.

The target responsibility groups are:

- `pilot`: manifest records and validation; contamination records; progression evidence and derivation; C2 eligibility; model-facing serialization and composition;
- `evaluation`: identities and fixtures; rubrics, ratings, and adjudication; agreement/calibration statistics; invalidity and sensitivity; judge policy;
- `cluster`: environment and policy records; adapter protocol and deterministic fake; attempt capture/execution; final-state evaluation; qualification and opt-in entry point;
- `web`: policy and URL controls; provider protocol and deterministic fake; retrieval records and persistence; budgeted attempt execution; drift/qualification and opt-in entry point;
- `config`: YAML parsing; document validation and hashing; path/reference resolution; configuration assembly;
- `provenance`: manifest records; Git/environment capture; manifest construction and serialization.

Compatibility facades use explicit imports and `__all__`; wildcard imports and dynamic export discovery are prohibited. Import-compatibility tests enumerate the pre-refactor public names. The refactor does not promise compatibility for private underscore-prefixed names or new direct imports from internal submodules.

Alternative: strict class-per-file organization. Rejected because the code contains many small Pydantic records that form readable domain vocabularies; separating all of them would multiply files and cross-imports without isolating behavior. Alternative: split only into broad `models.py` and `services.py` files. Rejected because the largest domains would remain oversized and mix unrelated model groups.

### 2. Use cohesion, not line count alone, to choose boundaries

A module should answer one domain question, expose a small intentional surface, and depend only on lower-level modules. Closely related enums and declarative record classes may remain together. A class that owns a substantial workflow or mutable state—such as an attempt executor—belongs in its own focused module unless splitting it would separate invariants that must be reviewed together.

The 250-line threshold counts physical lines as reported by `wc -l` for hand-written Python under `src/` and `tests/`. The implementation review records a manual line-count check; no permanent structure-enforcement test is retained. If implementation shows that a cohesive unit cannot be kept within the threshold without harming clarity, the exception must be narrow, documented in the implementation handoff, and explicitly approved by the human researcher; the implementer may not silently add one.

Ruff formatting remains authoritative. Dense formatting, multiple logical statements per line, generated forwarding modules, or abstractions whose only purpose is reducing the count do not satisfy this design.

Alternative: make 250 lines an unconditional limit. Rejected because a mechanical limit can incentivize arbitrary boundaries. Alternative: use the threshold only as non-verified guidance. Rejected because the current concentration would easily recur without a visible check.

### 3. Enforce a one-way internal dependency structure

Within each capability package, dependencies flow from shared primitives to domain records, then pure validation/calculation logic, then persistence or external adapters, and finally orchestration and the compatibility facade. Pure modules must not import adapters or opt-in entry points. Shared code remains in the existing `records`, `schemas`, and `errors` modules unless at least two capabilities already require the same invariant; this refactor does not create a new generic utilities layer.

Type-only imports and small local protocols may break legitimate annotation cycles. Runtime import cycles, service locators, and import-time registration are prohibited. Importing any facade must remain side-effect free and must not contact a model, network service, Git process, or cluster.

Alternative: centralize all records in one global models package. Rejected because it would erase capability ownership and recreate the original navigation problem at a larger scale.

### 4. Preserve behavior with characterization and compatibility tests

Before moving each responsibility group, retain or add focused characterization tests for its public surface. Tests must cover representative model validation, canonical bytes and hashes, redacted failures, append-only collisions, deterministic seeded calculations, policy denials, and import-time external-effect isolation as applicable. The move is complete only when the same assertions pass against the compatibility facade.

Large tests are split by behavior rather than by arbitrary line ranges and live under the
matching capability test package. Shared fixtures move to the narrowest relevant
`conftest.py` or helper module; helpers must not hide the assertion or scientific condition
being tested. Test names continue to describe the invariant. No expected value may be
weakened merely to accommodate the refactor.

The final verification compares the facade exports with the captured public-name inventory, runs every existing project check, and inspects the diff for accidental schema, constant, default, threshold, error-message, or execution-boundary changes.

Alternative: rely only on the current full test suite. Rejected because moving symbols can accidentally narrow exports or alter representative serialization even while internal call sites are updated together.

### 5. Migrate one capability at a time

Each capability is converted and verified independently, starting with the smaller `config` and `provenance` modules, followed by `pilot`, `evaluation`, `cluster`, and `web`. Corresponding tests move with each capability. This limits review scope and exposes circular dependencies before several domains are in flight.

No compatibility shim is scheduled for later removal: the same-named package facade becomes the stable public boundary. Rollback for any stage restores that capability's original module and tests; because persistence formats and behavior do not change, no data migration is required.

## Risks / Trade-offs

- **[Re-exported classes have different defining submodules]** → Treat the documented top-level import path, public name, validation, and serialized representation as the compatibility contract; add facade-level tests and avoid depending on private module identity.
- **[Splitting records can create circular imports]** → Define dependency direction before moves, keep related record families together, and reject runtime cycles during per-capability type and import checks.
- **[A large move can hide behavior changes]** → Use characterization tests, small capability-scoped stages, and diff review for constants, defaults, validators, hashes, and errors.
- **[Many tiny modules can make navigation worse]** → Split by cohesive responsibility, not automatically per class, and require each module name and public surface to express its purpose.
- **[Test helpers can obscure scientific assertions]** → Share only setup data and keep invariant-specific expectations in the test module.
- **[The line threshold can be gamed]** → Combine automated counting with Ruff formatting and explicit human review of cohesion and any exception rationale.

## Migration Plan

1. Capture the current public export inventory and add structural/compatibility characterization tests without changing implementation behavior.
2. Convert `config` and `provenance` to packages, split their tests, and run focused plus configuration/lifecycle integration checks.
3. Convert `pilot` and `evaluation`, split their tests by scientific responsibility, and run the pilot/evaluation integration path.
4. Convert `cluster` and `web`, split their tests, and verify routine imports and tests remain fake-backed and side-effect free.
5. Run formatting, linting, typing, coverage, build, example validation, dependency configuration validation, and strict OpenSpec validation; inspect exports, line counts, and the complete diff.

Rollback is capability-local and requires no persisted-data migration. Implementation must stop and return to planning if preserving an existing public contract would require a behavioral, schema, methodological, or dependency change.
