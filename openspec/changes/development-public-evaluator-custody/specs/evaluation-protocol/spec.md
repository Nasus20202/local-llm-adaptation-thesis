## ADDED Requirements

### Requirement: Public development evaluator custody

The development evaluator MAY be stored in the public repository because its answers are not treated as confidential. Public storage SHALL NOT change the evaluator hierarchy, deterministic score derivation, source-evidence binding, semantic-judge freeze gate, or class-specific metrics. The evaluator subtree SHALL remain excluded from all participant-model-facing inputs and execution workspaces.

#### Scenario: Public storage does not grant model access

- **WHEN** a participant-model run is prepared from the approved model-facing manifest
- **THEN** evaluator payloads are absent from the run workspace and cannot be resolved through model-facing serialization

#### Scenario: Public evaluator content is disclosed

- **WHEN** a public reader inspects a development evaluator artifact
- **THEN** the artifact is considered intentionally disclosed development material, and contamination reporting does not claim evaluator-answer secrecy
