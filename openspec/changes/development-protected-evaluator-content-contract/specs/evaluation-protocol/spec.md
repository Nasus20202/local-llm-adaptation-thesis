## ADDED Requirements

### Requirement: Protected evaluator content is representable and assessable

Every answer-bearing development evaluator contract SHALL encode protected, hashed definitions for the meaning and assessment boundary of each score-affecting criterion. Accepted semantic alternatives SHALL encode equivalent meaning rather than preferred wording. Semantic criteria SHALL encode observable anchors. Unsupported or contradictory criteria SHALL encode the claim boundary that makes the disposition assessable. Deterministic predicates SHALL encode the governed expected result required by their predicate kind.

The definitions SHALL remain part of the existing protected artifact and lineage graph, SHALL map to frozen Kubernetes v1.36.4 source evidence, SHALL reject reviewer-convenience notes, and SHALL never be emitted through model-facing serialization. No parallel unvalidated answer schema is permitted.

#### Scenario: Complete criterion content validates

- **WHEN** a protected contract supplies assessable criterion definitions, semantic anchors, accepted meanings, deterministic governed results, and frozen source evidence for every score-affecting criterion
- **THEN** contract validation accepts the content under the existing artifact hash and lineage

#### Scenario: Criterion meaning is missing

- **WHEN** a score-affecting criterion is represented only by an identifier, role, or evidence ID
- **THEN** validation rejects the contract before scoring or judge input construction

#### Scenario: Answer-bearing content crosses the model boundary

- **WHEN** model-facing serialization attempts to include a protected definition, anchor, accepted meaning, unsupported-claim boundary, or deterministic expected result
- **THEN** serialization fails closed without emitting the protected value

#### Scenario: Reviewer note is used as protected truth

- **WHEN** a protected definition or anchor contains the scenario-review convenience note marker
- **THEN** validation rejects the contract as an invalid evidence source
