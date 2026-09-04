## Purpose

Define portable, strict, and hashable experiment metadata so later runs are based on explicit identities rather than implicit filenames or conversational context.

## ADDED Requirements

### Requirement: Versioned strict metadata documents

The system SHALL load UTF-8 YAML documents for experiment, model, hardware, dataset, and evaluation metadata. Every document SHALL declare schema version `1`, its expected document kind, and a non-empty stable identifier. The system SHALL reject duplicate keys, unknown fields, invalid types, non-finite numeric values, unsupported schema versions, and identifiers outside the pattern `[a-z0-9][a-z0-9._-]{0,127}`.

#### Scenario: Valid metadata set

- **WHEN** every metadata document uses schema version `1`, the correct kind, valid required fields, and no unknown fields
- **THEN** the system accepts and returns a typed validated metadata set

#### Scenario: Unknown or duplicate field

- **WHEN** a metadata document contains an unknown field or repeats a YAML mapping key
- **THEN** the system rejects the document with the source path and field location without creating a run

#### Scenario: Unsupported schema version

- **WHEN** any document declares a schema version other than `1`
- **THEN** the system rejects the complete configuration and identifies the unsupported document and version

### Requirement: Minimal metadata identities

Model metadata SHALL identify the model repository, a full 40-character lowercase hexadecimal Git commit revision, artifact filename, artifact SHA-256, quantization, license identifier, and chat-template identifier. Hardware metadata SHALL identify the intended machine profile, operating system, CPU, RAM, GPU, and VRAM. Dataset metadata SHALL identify the dataset, a stable revision label, split, and deterministic manifest SHA-256. Evaluation metadata SHALL identify the evaluator and a stable version label and SHALL list at least one metric identifier. Dataset revision and evaluation version labels SHALL match `[a-z0-9][a-z0-9._-]{0,127}` and SHALL NOT equal `latest`, `main`, or `master` case-insensitively. The experiment document SHALL identify the experiment, condition, run kind (`exploratory` or `formal`), optional integer random seed, and one reference to each metadata kind.

Validation SHALL NOT claim to prove that an arbitrary dataset or evaluation label is immutable. The frozen dataset identity is the dataset identifier, accepted revision label, split, and `manifest_sha256` together. The frozen evaluation identity is the evaluator identifier, accepted version label, evaluation document semantic SHA-256, and prepared run Git commit together. The frozen model identity additionally includes `artifact_sha256`, so the repository commit and artifact bytes are independently traceable.

#### Scenario: Complete minimum metadata

- **WHEN** all required identity fields are present and valid
- **THEN** the system exposes them without deriving missing scientific identity from directory or file names

#### Scenario: Model revision is not a full commit identity

- **WHEN** a model revision is not exactly 40 lowercase hexadecimal characters
- **THEN** the system rejects the model metadata as insufficiently pinned

#### Scenario: Dataset or evaluation label is not stable

- **WHEN** a dataset revision or evaluation version is outside the stable identifier pattern or equals `latest`, `main`, or `master` case-insensitively
- **THEN** the system rejects the metadata as insufficiently labelled for a frozen composite identity

#### Scenario: Invalid hash

- **WHEN** a required SHA-256 value is not exactly 64 lowercase hexadecimal characters
- **THEN** the system rejects the affected document

### Requirement: Portable reference resolution

Each experiment reference SHALL contain a repository-relative YAML path and an expected metadata identifier. The system SHALL resolve references relative to the experiment document, require the resolved regular file to remain inside the discovered project root after symlink resolution, and reject URLs, missing files, non-YAML paths, and path escapes. The resolved document kind and identifier SHALL match the reference.

#### Scenario: Relative reference resolves

- **WHEN** a reference points to a matching metadata document inside the project root
- **THEN** the system loads it and records its normalized project-relative path

#### Scenario: Reference identifier mismatch

- **WHEN** the referenced document's identifier differs from the reference's expected identifier
- **THEN** the system rejects the configuration and reports both identifiers

#### Scenario: Symlink or parent traversal escapes the project

- **WHEN** reference resolution would leave the project root
- **THEN** the system rejects the reference before reading the external target

### Requirement: Deterministic configuration identity

For the experiment file and every referenced metadata file, the system SHALL calculate a SHA-256 hash of the exact source bytes and a semantic SHA-256 hash of the validated document encoded as canonical UTF-8 JSON. Canonical JSON SHALL sort mapping keys, use compact separators, preserve list order, and represent no non-finite numbers. Repeated loading of semantically identical YAML SHALL produce the same semantic hash even if harmless YAML formatting differs.

#### Scenario: Formatting-only YAML change

- **WHEN** two source documents differ only in comments, whitespace, or mapping key order and validate to the same data
- **THEN** their source hashes differ when the bytes differ and their semantic hashes are equal

#### Scenario: Semantic value change

- **WHEN** a validated value changes
- **THEN** the semantic hash changes

### Requirement: Side-effect-free validation

Loading and validating configuration SHALL NOT create result directories, modify source files, access the network, download artifacts, inspect model weights, or execute external inference processes.

#### Scenario: Configuration validation succeeds

- **WHEN** a user validates a complete metadata set
- **THEN** the system returns validation and identity information without changing the filesystem outside ordinary read access
