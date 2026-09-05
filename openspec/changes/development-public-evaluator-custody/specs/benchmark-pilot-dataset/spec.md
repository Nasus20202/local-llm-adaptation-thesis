## ADDED Requirements

### Requirement: Development evaluator storage binding

The system SHALL permit answer-bearing development evaluator contracts, evidence maps, review artifacts, and qualification fixtures to be committed under the dedicated repository-relative development evaluator subtree. The binding SHALL retain exact artifact identity, SHA-256, lineage, source registry, and review/freeze state.

Final-test payloads and locators SHALL remain outside this permission and SHALL continue to fail closed.

#### Scenario: Tracked development evaluator artifact

- **WHEN** a development evaluator artifact is loaded from the approved repository-relative subtree with a matching identity and SHA-256
- **THEN** validation accepts it for protected evaluation and records the applicable provenance event

#### Scenario: Absolute evaluator locator

- **WHEN** an evaluator reference uses an absolute or parent-traversing path
- **THEN** validation rejects it without exposing payload content

### Requirement: Public evaluator content remains non-model-facing

Tracked evaluator payloads SHALL NOT be included in model-facing exports, RAG corpora, training manifests, prompts, skills, harness inputs, W1 inputs, participant run workspaces, ordinary logs, or diagnostics. A model-facing role attempting to resolve them SHALL fail closed before reading the payload.

#### Scenario: Model-facing evaluator access

- **WHEN** a participant-model-facing process requests a tracked evaluator reference
- **THEN** access is denied and only safe identifiers and reason codes are returned
