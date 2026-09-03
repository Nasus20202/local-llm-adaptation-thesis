# benchmark-pilot-dataset Specification

## Purpose

Define auditable development-only benchmark metadata and progression records without placing protected answers or final-test payloads in the normal repository or model-facing boundary.

## Requirements

### Requirement: Development-only partition boundary
The system SHALL accept pilot records only when their split is `development`, and SHALL reject any pilot operation that declares or resolves final-test content.

#### Scenario: Development family accepted
- **WHEN** a pilot manifest identifies every family and nested variant as development-only
- **THEN** the system accepts the partition boundary for further validation

#### Scenario: Final-test content rejected
- **WHEN** a pilot manifest, referenced payload, or command identifies a final-test split or protected final-test location
- **THEN** the system rejects the operation before reading or emitting that content

### Requirement: Scenario-family identity and nesting
The system SHALL require a stable family identifier for every pilot family and SHALL associate language variants, static/interactive variants, prompt formulations, and repeated generations with that family rather than treating them as independent families.

#### Scenario: Nested variants preserved
- **WHEN** two records describe semantic language variants or static/interactive forms of one scenario
- **THEN** validation requires one shared family identifier and distinct variant identifiers

#### Scenario: Variant counted as independent family
- **WHEN** a manifest counts a nested variant or repeat toward the independent-family total
- **THEN** validation fails with the affected identifiers

### Requirement: Pilot composition validation
The system SHALL validate the approved pilot cap and required task-class/language allocation from versioned policy rather than hard-coded item content.

#### Scenario: Balanced pilot metadata
- **WHEN** a manifest declares 24 independent development families with eight per task class and four per language within class
- **THEN** composition validation succeeds

#### Scenario: Unapproved composition
- **WHEN** the independent-family count, class allocation, or language allocation differs from the approved policy
- **THEN** validation fails and reports every violated allocation

### Requirement: Answer-contract and metric applicability metadata
Each family SHALL identify its task class, answer form, deterministic gates, candidate primary outcome, supporting metrics, applicable conditions, inapplicable conditions, target-stratum tags, and preregistered comparator without containing a model-visible golden answer.

#### Scenario: Applicable condition fully declared
- **WHEN** a family marks a condition applicable
- **THEN** validation requires a target-stratum decision, answer contract, evaluator references, and comparator consistent with the approved matrix

#### Scenario: Inapplicable metric handled
- **WHEN** a metric or condition is scientifically inapplicable to a family
- **THEN** the record preserves an explicit inapplicability reason and does not encode a zero score

### Requirement: Protected-content separation
The model-facing pilot manifest SHALL contain only inputs and permitted context. Protected evidence maps, expected results, rubrics, adjudication notes, and golden material SHALL be referenced by identity and cryptographic hash through a separate evaluator boundary.

#### Scenario: Protected material in model manifest
- **WHEN** validation detects a protected answer, expected validator result, rubric decision, or golden payload in a model-facing manifest
- **THEN** validation fails before the manifest can be used

#### Scenario: Protected reference recorded safely
- **WHEN** an evaluator record references protected material by approved identity and hash
- **THEN** validation succeeds without copying the protected payload into model-facing output

### Requirement: Contamination audit record
The system SHALL record exact, normalized, token-overlap, code/configuration-structure, semantic, and cross-language audit outcomes by artifact pair, method version, threshold, and adjudication status. An aggregate contamination record SHALL prove that every required detector ran before claiming no direct overlap. It SHALL distinguish source/domain, semantic-pattern, and direct-item exposure and SHALL NOT emit a numerical pre-training exposure probability.

#### Scenario: Audit with no detected direct overlap
- **WHEN** all required detectors ran and no direct match passed its threshold
- **THEN** the record states that no direct overlap was detected under the named methods and that parametric exposure remains unknown

#### Scenario: Direct leakage detected
- **WHEN** an audit or custody event identifies train/development/final overlap or golden exposure
- **THEN** progression is `STOP/DEFER`, affected identifiers are recorded, and no automatic deletion or replacement occurs

### Requirement: C2 applicability and comparator freeze
For any C2 record, the system SHALL require an eligibility manifest frozen before pilot outcomes, containing only model-independent family metadata, the complete constituent set, a frozen outcome-independent constituent selector/order, and a versioned design-time comparator rule. Confirmatory C2 validation SHALL reject outcome-derived eligibility or comparator fields. A confirmatory follow-up SHALL bind to the immutable exploratory manifest identity and derive its excluded family set from that linked manifest rather than trusting a self-declared exclusion list.

#### Scenario: Metadata-frozen C2 accepted
- **WHEN** a C2 manifest contains model-independent family metadata, a complete constituent set, a frozen constituent selector/order, a design-time comparator rule, and a pre-outcome freeze identity
- **THEN** validation accepts the C2 target stratum and comparator for confirmatory analysis

#### Scenario: Outcome-selected C2 marked exploratory
- **WHEN** C2 eligibility or comparator selection references pilot scores, error analysis, evaluator disagreement, or another outcome-derived signal
- **THEN** the record is marked exploratory and confirmatory C2 analysis is denied without a fresh family-disjoint manifest

#### Scenario: Fresh C2 confirmation
- **WHEN** a new C2 manifest is frozen before outcomes, is linked to the exploratory manifest whose family IDs are used to derive the exclusion set, contains no family overlap with that manifest, and satisfies the approved metadata rule
- **THEN** validation permits the confirmatory C2 comparison

### Requirement: Pilot progression report
The system SHALL derive separate `GO`, `AMEND`, or `STOP/DEFER` statuses for each approved feasibility criterion from versioned thresholds and SHALL preserve the observations and reasons used. It SHALL NOT use method superiority or final-test outcomes as a progression input.

#### Scenario: Mixed progression outcomes
- **WHEN** at least one non-safety criterion is amber and no criterion is red
- **THEN** the report records `AMEND`, identifies the criteria, and preserves all individual statuses

#### Scenario: Prohibited progression input
- **WHEN** a report attempts to select or replace a family because a method did not improve or references a final-test outcome
- **THEN** the system rejects the report as an invalid progression decision
