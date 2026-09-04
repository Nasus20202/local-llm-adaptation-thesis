# run-provenance Specification

## Purpose

Define a stable, reviewable run manifest that binds a prepared execution attempt to its configuration, repository state, and software environment without exposing secrets.

## Requirements

### Requirement: Versioned run manifest

The system SHALL construct a JSON manifest with schema version `1` containing a unique run ID, experiment ID, condition ID, run kind, optional random seed, UTC preparation timestamp, package version, the project-relative experiment source path, and the source and semantic hashes for the experiment and each referenced metadata document. The manifest SHALL preserve explicit model, hardware, dataset, and evaluation identities.

#### Scenario: Manifest from valid configuration

- **WHEN** a run is prepared from a valid metadata set
- **THEN** the manifest contains every required identity and hash copied from the validated set

#### Scenario: Round-trip validation

- **WHEN** a written version `1` manifest is loaded
- **THEN** it validates to the same data and serializes as canonical JSON with a trailing newline

#### Scenario: Unknown manifest field

- **WHEN** a manifest contains an unknown top-level or nested field
- **THEN** the system rejects it instead of silently discarding the field

### Requirement: Git provenance

Run preparation SHALL require a clean Git worktree with a resolvable `HEAD`. The manifest SHALL record the full commit SHA and branch name when attached. Any staged, unstaged, or non-ignored untracked change SHALL prevent preparation. Side-effect-free configuration validation remains available while the tree is dirty.

#### Scenario: Clean preparation

- **WHEN** a run is prepared from a clean Git worktree with a commit
- **THEN** the manifest records the commit and branch when attached

#### Scenario: Dirty preparation

- **WHEN** preparation is requested while any staged, unstaged, or non-ignored untracked change exists
- **THEN** preparation fails before a run directory is committed

#### Scenario: Missing Git commit

- **WHEN** preparation is requested outside a Git worktree or before its first commit
- **THEN** preparation fails without creating a raw run

### Requirement: Runtime environment provenance

The manifest SHALL record the operating-system/platform description, machine architecture, Python implementation and version, and installed `thesis-bench` package version observed at preparation. Environment capture SHALL be local and SHALL NOT contact external services. Hardware metadata describes the intended benchmark profile and SHALL remain distinct from observed runtime facts.

#### Scenario: Local environment captured

- **WHEN** a run is prepared
- **THEN** the manifest records the available required runtime facts without network access

#### Scenario: Intended and observed environment differ

- **WHEN** the declared hardware profile differs from observable platform facts
- **THEN** the manifest preserves both identities without silently rewriting the declared profile

### Requirement: Secret-safe and portable provenance

The manifest SHALL include project-relative metadata paths only and SHALL NOT include environment-variable values, credentials, home-directory paths, full Git diffs, model outputs, or complete dataset records. Errors SHALL avoid echoing YAML values that could contain secrets.

#### Scenario: Environment contains a token

- **WHEN** run preparation executes in a process with credential-like environment variables
- **THEN** neither the manifest nor normal diagnostic output contains their names and values as provenance data

#### Scenario: Project is moved

- **WHEN** the same committed project tree is located under a different absolute parent directory
- **THEN** source paths stored in the manifest remain identical
