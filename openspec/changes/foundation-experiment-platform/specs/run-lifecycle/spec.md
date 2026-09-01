## Purpose

Define collision-safe raw run preparation and append-only lifecycle storage so no execution attempt can overwrite or cosmetically repair historical evidence.

## ADDED Requirements

### Requirement: Unique run identity

The system SHALL generate a run ID containing a sortable UTC timestamp and a random UUID-derived suffix. The ID SHALL use only ASCII digits, lowercase letters, `-`, and `t`/`z` timestamp markers and SHALL be safe as a single directory name. Repeated preparations of the same experiment SHALL receive different run IDs.

#### Scenario: Repeated preparation
- **WHEN** the same experiment is prepared twice
- **THEN** two distinct run IDs and raw directories are created

#### Scenario: Run ID format
- **WHEN** a run ID is generated
- **THEN** it contains a UTC timestamp and sufficient random identity without embedding a username or absolute path

### Requirement: Atomic exclusive raw run creation

The system SHALL create a run at `<results-root>/<run-id>/` using an exclusive staging directory in the same parent filesystem, write and validate the manifest and initial lifecycle event, and atomically publish the completed directory. It SHALL never replace, merge with, or delete an existing run directory. Validation or write failure SHALL leave no published run directory.

#### Scenario: Successful preparation
- **WHEN** valid configuration and provenance are available and the generated destination does not exist
- **THEN** one complete raw run directory becomes visible containing `manifest.json` and `events.ndjson`

#### Scenario: Destination collision
- **WHEN** the destination run directory already exists
- **THEN** the system fails without modifying any file in the existing directory

#### Scenario: Write fails before publication
- **WHEN** manifest or event persistence fails in the staging directory
- **THEN** no partially prepared run appears under the final run ID

### Requirement: Immutable manifest and append-only events

The system SHALL create `manifest.json` exactly once and SHALL refuse any operation that would replace or edit it. Lifecycle records SHALL be UTF-8 JSON objects appended one per line to `events.ndjson`; every event SHALL include schema version `1`, the run ID, an event ID, a timezone-aware UTC timestamp, an event type, and structured details. Preparation SHALL append `run_prepared` as the first event. Event appends SHALL preserve all existing bytes and reject malformed existing content or a mismatched run ID.

#### Scenario: Prepared event
- **WHEN** a run directory is published
- **THEN** its first and initially only event is a valid `run_prepared` event for that run ID

#### Scenario: Later event append
- **WHEN** a valid later lifecycle event is appended
- **THEN** all existing event bytes remain unchanged and exactly one valid line is added

#### Scenario: Manifest overwrite attempt
- **WHEN** persistence is asked to write a manifest to a run that already has one
- **THEN** the operation fails and the existing manifest bytes remain unchanged

#### Scenario: Corrupt event history
- **WHEN** the existing event file contains invalid JSON, an unsupported schema, or a different run ID
- **THEN** the system refuses to append an event

### Requirement: Run integrity inspection

The system SHALL inspect a prepared run by validating the manifest, parsing every lifecycle event, verifying consistent run IDs, and confirming that the first event is `run_prepared`. Inspection SHALL be read-only and SHALL report integrity failure distinctly from a missing path.

#### Scenario: Intact prepared run
- **WHEN** a run contains a valid manifest and valid event history
- **THEN** inspection returns its identities, preparation time, Git state, and latest lifecycle event

#### Scenario: Mismatched run identity
- **WHEN** the directory name, manifest run ID, or event run ID do not agree
- **THEN** inspection reports an integrity error without modifying the run
