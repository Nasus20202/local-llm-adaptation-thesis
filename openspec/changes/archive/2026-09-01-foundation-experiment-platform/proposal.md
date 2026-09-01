## Why

Future adaptation experiments need a small, testable foundation that rejects ambiguous inputs and records enough provenance to make every execution attempt auditable. Establishing this contract before inference work prevents incompatible configurations, mutable raw results, and undocumented environment changes from undermining the thesis.

## What Changes

- Establish the small Python project and locked tooling needed to test research-support logic in routine CI.
- Introduce strict, versioned YAML representations for experiment, model, hardware, dataset, and evaluation metadata.
- Resolve referenced metadata relative to the experiment file, validate cross-references, and compute source-byte and canonical semantic SHA-256 hashes.
- Introduce a versioned JSON run manifest containing experiment identity, referenced metadata identity, clean Git state, environment facts, and configuration hashes.
- Introduce exclusive creation of unique raw run directories and immutable manifest creation.
- Provide a minimal CLI to validate configuration, prepare a run without executing a model, and inspect a prepared run.
- Add focused deterministic tests, example metadata, developer commands, CI validation, and dependency maintenance.
- Explicitly exclude inference, benchmark content, RAG, fine-tuning, harnesses, skills, telemetry sampling, evaluation execution, and reporting.

## Capabilities

### New Capabilities

- `experiment-configuration`: Strict loading, reference resolution, validation, and hashing of versioned experiment metadata.
- `run-provenance`: Construction and validation of a stable, secret-safe run manifest with Git and environment provenance.
- `run-lifecycle`: Collision-safe raw run preparation and immutable manifest persistence.
- `command-line-interface`: Human- and automation-usable commands for configuration validation, run preparation, and run inspection.

### Modified Capabilities

None. This repository has no implemented software capabilities yet.

## Impact

The change will create the initial `src/thesis_bench/` package, focused tests, example configurations, project metadata and lockfile, developer commands, and routine CI. It introduces only the dependencies justified by strict metadata validation and testing. It creates no model, data, network, database, GPU, event-log, plugin, or experiment-execution dependency and produces no experimental result.
