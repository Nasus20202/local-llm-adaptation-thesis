# run-lifecycle Specification

## Purpose

Define collision-safe raw run preparation so no execution attempt can overwrite historical evidence. Observation and lifecycle-event storage are deferred until experiment execution exists.

## Requirements

### Requirement: Unique run identity

The system SHALL generate a run ID containing a sortable UTC timestamp and a random UUID-derived suffix. The ID SHALL use only ASCII digits, lowercase letters, `-`, and `t`/`z` timestamp markers and SHALL be safe as one directory name. Repeated preparations of the same experiment SHALL receive different run IDs.

#### Scenario: Repeated preparation
- **WHEN** the same experiment is prepared twice
- **THEN** two distinct run IDs and raw directories are created

#### Scenario: Run ID privacy
- **WHEN** a run ID is generated
- **THEN** it contains no username or absolute path

### Requirement: Atomic exclusive raw run creation

The system SHALL create a run at `<results-root>/<run-id>/` through an exclusive staging directory in the same parent filesystem, write and validate `manifest.json`, and atomically publish the completed directory. It SHALL never replace, merge with, or delete an existing run directory. Validation or write failure SHALL leave no published run directory.

#### Scenario: Successful preparation
- **WHEN** valid configuration and provenance are available and the generated destination does not exist
- **THEN** one complete raw run directory becomes visible containing one valid `manifest.json`

#### Scenario: Destination collision
- **WHEN** the destination run directory already exists
- **THEN** the system fails without modifying any file in the existing directory

#### Scenario: Write fails before publication
- **WHEN** manifest persistence fails in the staging directory
- **THEN** no partially prepared run appears under the final run ID

### Requirement: Immutable manifest

The system SHALL create `manifest.json` exactly once and SHALL refuse any operation that would replace or edit it. The manifest SHALL be canonical UTF-8 JSON with a trailing newline.

#### Scenario: Manifest overwrite attempt
- **WHEN** persistence is asked to write a manifest to a run that already has one
- **THEN** the operation fails and the existing manifest bytes remain unchanged

### Requirement: Run integrity inspection

The system SHALL inspect a prepared run by validating the manifest and confirming that its run ID matches the directory name. Inspection SHALL be read-only and SHALL report integrity failure distinctly from a missing path.

#### Scenario: Intact prepared run
- **WHEN** a run contains a valid manifest with a matching run ID
- **THEN** inspection returns its identities, preparation time, and Git commit

#### Scenario: Mismatched run identity
- **WHEN** the directory name and manifest run ID do not agree
- **THEN** inspection reports an integrity error without modifying the run
