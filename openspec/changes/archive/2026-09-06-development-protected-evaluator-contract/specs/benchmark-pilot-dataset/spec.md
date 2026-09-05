## Purpose

Define auditable development-only benchmark metadata and progression records without placing protected answers, semantic-judge qualification truth, or final-test payloads in the normal repository or participant-model-facing boundary.

## ADDED Requirements

### Requirement: Protected evaluator binds to approved scenario inputs

Every protected development evaluator contract SHALL identify the approved `family_id`, scenario-input identity, exact scenario-input SHA-256, task class, language, source-rights manifest identity, and pre-authoring/evaluation-clarification identities on which it was constructed.

Validation SHALL reject a protected evaluator contract if its family/input identity or hash does not match the approved development-pilot input manifest. A correction SHALL create a successor contract; it SHALL NOT silently retarget an existing protected contract.

#### Scenario: Contract matches approved input

- **WHEN** a protected contract identifies one approved family and the exact approved scenario-input hash
- **THEN** input-binding validation accepts the contract for further protected evaluation checks

#### Scenario: Scenario input changed

- **WHEN** the protected contract's recorded input hash differs from the approved scenario-input manifest
- **THEN** validation rejects the contract before scoring and requires an explicit successor/review path

### Requirement: Protected evidence maps use only frozen source identities

Every score-affecting required claim, unsupported/contradictory claim criterion, construct-critical exact rule, deterministic gate, and answer-bearing semantic criterion SHALL map to one or more evidence entries from the frozen Kubernetes v1.36.4 source boundary.

Each evidence entry SHALL preserve enough immutable identity to resolve the approved source version, including the source registry/inventory identity and the frozen repository revision plus path/blob or OpenAPI identity/hash as applicable. Source excerpts MAY exist in protected custody when rights permit, but they SHALL NOT be required in participant-model-facing references or diagnostic output.

Reviewer-convenience expected-answer notes, including the `Expected answer — reviewer note` text in the scenario-review documentation, SHALL NOT be accepted as evaluator evidence, evaluator reference content, semantic-judge input truth, human-rubric input, or a construction source for protected answer truth.

#### Scenario: Frozen source evidence accepted

- **WHEN** every score-affecting criterion maps to an approved Kubernetes v1.36.4 source identity present in the frozen source registry
- **THEN** evidence-map validation succeeds without exposing answer-bearing mappings to participant-model-facing output

#### Scenario: Reviewer note used as evidence

- **WHEN** an evidence map, judge input, or construction provenance names a human reviewer convenience note as support for evaluator truth
- **THEN** protected evaluator validation fails

#### Scenario: Unfrozen source revision used

- **WHEN** a score-affecting criterion maps to a Kubernetes source revision outside `development-pilot-source-rights-v1`
- **THEN** validation fails and the source cannot be silently substituted

### Requirement: Semantic-judge qualification truth remains protected and bound

Human-labelled semantic-judge qualification fixtures, calibrated criterion labels, expected dispositions, fairness relations, adjudication material, and answer-bearing judge input payloads SHALL remain under `development-protected-evaluator-v1` and SHALL NOT be committed to the normal repository or exposed to participant-model-facing roles.

Each frozen qualification set SHALL identify the evaluator-contract version and protected criteria/source identities from which it was constructed. A judge qualification record SHALL additionally bind the exact frozen judge-configuration identity and qualification-set identity/hash used to derive the qualification decision.

A change to answer-bearing qualification fixtures or labels SHALL create a successor qualification-set identity. A change to the judge configuration SHALL require a new judge qualification record; prior qualification SHALL NOT be silently reused.

#### Scenario: Qualified judge is reproducibly bound

- **WHEN** a semantic judge is marked qualified for a task/language/criterion scope
- **THEN** the qualification record identifies the exact judge configuration and protected human-labelled qualification-set identities/hashes that produced that decision

#### Scenario: Human labels cross participant-model boundary

- **WHEN** participant-model-facing serialization attempts to include a protected qualification response, calibrated human label, expected disposition, or answer-bearing judge criterion/evidence payload
- **THEN** serialization fails before protected truth is written

#### Scenario: Qualification fixture corrected after freeze

- **WHEN** a protected human-labelled qualification fixture or expected disposition requires correction after freeze
- **THEN** the previous qualification set remains immutable, a successor set is created, and affected judge configurations require qualification against the successor before new primary use

### Requirement: Safe protected references expose no evaluator truth

A committed or participant-model-facing reference to protected development evaluator or semantic-judge qualification material SHALL contain only the approved safe metadata needed for identity and integrity: stable artifact identity, artifact kind, protected root identity, protected-root-relative path, exact SHA-256, status/reason codes, non-answer-bearing assessor/configuration identities, and non-answer-bearing provenance identities already permitted by the custody freeze.

Such a reference SHALL NOT contain required claims, accepted alternatives, prohibited claims, exact expected values, answer-bearing semantic anchors, calibrated human labels, expected judge dispositions, expected fixture outcomes, evidence-map relationships that reveal the answer, protected excerpts, judge protected-input payloads, recovery data, or a machine-specific absolute locator.

#### Scenario: Safe protected handle serialized

- **WHEN** participant-model-facing metadata needs to identify the evaluator artifact used for a family
- **THEN** it may serialize only the safe protected reference and hash, not the protected contract or judge-qualification payload

#### Scenario: Answer-bearing field crosses boundary

- **WHEN** participant-model-facing serialization contains a required claim, expected value, answer-bearing evidence relation, human criterion decision, judge qualification label, or fixture expectation from protected custody
- **THEN** serialization fails before output is written

### Requirement: Protected evaluator lineage is immutable and append-only

Every protected evaluator artifact, protected evaluator manifest, human-labelled judge qualification set, and judge qualification record SHALL have an exact content SHA-256 and immutable version identity. Freeze, access, review, judge assessment, human adjudication/audit, redaction/disclosure, and supersession SHALL be recorded through the approved append-only development custody evidence streams.

A frozen protected artifact SHALL NOT be overwritten. Any scientific correction, source-remapping correction, semantic-anchor change, qualification-label/fixture change, or fairness-fixture change SHALL create a successor identity linked to the superseded artifact and SHALL force a new evaluator or judge-qualification identity for affected derived evaluations.

#### Scenario: Frozen evaluator contract is corrected

- **WHEN** a reviewed protected contract requires a scientific or mapping correction after freeze
- **THEN** the prior artifact remains immutable and a successor contract plus supersession evidence is created

#### Scenario: In-place overwrite attempted

- **WHEN** a writer attempts to replace bytes under an already frozen protected evaluator or judge-qualification artifact identity
- **THEN** the write is rejected and the existing artifact remains unchanged
