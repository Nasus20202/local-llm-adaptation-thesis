## Purpose

Provide versioned deterministic and human-evaluation records whose fixture behavior, calibration, adjudication, and invalidity decisions are reproducible without altering raw observations.

## ADDED Requirements

### Requirement: Immutable evaluator identity
Every evaluation SHALL identify the evaluator schema/version, code or artifact revision, configuration hash, rubric version when applicable, fixture-set hash, input observation identity/hash, and output hash. Re-evaluation with changed inputs SHALL create a new derived record and SHALL NOT modify the raw observation or prior evaluation.

#### Scenario: Same raw output evaluated under a revision
- **WHEN** a new evaluator version scores an existing raw observation
- **THEN** the system creates a distinct derived record linked to both identities and preserves the previous evaluation

#### Scenario: Incomplete evaluator identity
- **WHEN** any required evaluator or input identity is absent or mutable
- **THEN** evaluation fails before a score is emitted

### Requirement: Deterministic fixture classes
Every deterministic evaluator SHALL declare fixture cases for positive, negative, boundary, malformed, and ambiguous behavior. Qualification SHALL require 100% expected outcomes and identical outcome/reason codes on repeated fixture execution.

#### Scenario: Deterministic evaluator qualifies
- **WHEN** every required fixture class is present, every expected outcome matches, and repeated execution is identical
- **THEN** the qualification status is `GO`

#### Scenario: Ambiguous fixture receives arbitrary score
- **WHEN** an ambiguous fixture cannot be resolved by the declared deterministic contract
- **THEN** the evaluator returns a documented rejection or human-review route rather than a substantive score

#### Scenario: Fixture mismatch
- **WHEN** one or more deterministic fixture outcomes or reason codes differ from the expected record
- **THEN** the evaluator qualification is not `GO` and affected fixtures are listed

### Requirement: Atomic task-specific rubric
Human rubrics SHALL consist of named atomic criteria with observable anchors. Ordinal criteria SHALL use the approved three levels, and critical binary labels SHALL remain separately reportable. A universal undifferentiated quality score SHALL NOT replace task-specific outcomes.

#### Scenario: Complete ordinal criterion
- **WHEN** an ordinal criterion defines all three observable anchors and applicability
- **THEN** it is accepted for calibration

#### Scenario: Vague criterion
- **WHEN** a criterion lacks observable anchors, conflates distinct constructs, or permits two incompatible interpretations
- **THEN** rubric validation fails before human qualification

### Requirement: Blinded independent rating records
Rating import SHALL require rater pseudonym, randomized response identity, criterion values, rubric version, timestamp, and independence/blinding declarations. Method, model, prompt, and seed labels SHALL NOT be required or exposed in the rating view.

#### Scenario: Independent ratings imported
- **WHEN** two raters submit complete ratings without access to each other's decisions
- **THEN** both immutable rating records are linked to the response for calibration or adjudication

#### Scenario: Rater sees condition label
- **WHEN** a rating view or import payload includes a model or experimental-condition label not required by the rubric
- **THEN** the system rejects the blinded qualification record or marks the rating explicitly unblinded and ineligible for green qualification

### Requirement: Calibration summary and thresholds
The system SHALL report criterion confusion tables, exact agreement, adjacent-category agreement for ordinal criteria, and nominal or ordinal Krippendorff alpha with a family-clustered 95% interval. It SHALL apply the approved green/amber/red thresholds without substituting a different coefficient silently.

#### Scenario: Green human qualification
- **WHEN** each critical binary label has at least 90% exact agreement, pooled primary-rubric alpha is at least 0.80, and its lower 95% interval bound is at least 0.67
- **THEN** the qualification status is `GO`

#### Scenario: Amber human qualification
- **WHEN** pooled alpha is from 0.67 through 0.79 or the lower interval bound is below 0.67 without systematic critical disagreement
- **THEN** the qualification status is `AMEND` and at most one disjoint requalification is permitted

#### Scenario: Red human qualification
- **WHEN** pooled alpha is below 0.67, a systematic critical disagreement remains, or a second qualification attempt is not green
- **THEN** the affected human metric is `STOP/DEFER` for confirmatory use until narrowed or replaced

### Requirement: Written adjudication
The system SHALL preserve both independent ratings and require a written evidence-based adjudication for critical-label disagreement or ordinal disagreement greater than one level. It SHALL preserve unresolved labels rather than silently selecting one.

#### Scenario: Disagreement resolved
- **WHEN** adjudicators resolve a qualifying disagreement
- **THEN** the derived adjudicated label records the rationale and rater identities while original ratings remain unchanged

#### Scenario: Disagreement unresolved
- **WHEN** no approved adjudicator resolves a critical disagreement
- **THEN** both labels remain available and the record requires a conservative sensitivity-analysis flag

### Requirement: Objective invalidity classification
The evaluator SHALL distinguish measurement-infrastructure invalidity from evaluated-system failure using frozen reason codes. Wrong answers, refusals, malformed model outputs, action-budget exhaustion, evaluated-system timeouts, and failed remediation SHALL remain valid task failures.

#### Scenario: Capture hash mismatch
- **WHEN** an observation fails its required hash or capture-integrity check
- **THEN** evaluation records objective invalidity without deleting the observation

#### Scenario: Malformed model answer
- **WHEN** the captured model response violates the answer contract but capture and provenance are intact
- **THEN** the evaluator records a valid task failure rather than invalidating the run

### Requirement: Optional judge remains supplemental
An LLM judge SHALL be disabled for confirmatory scoring unless its frozen identity and prompt are recorded and it has been calibrated against adjudicated human labels in both languages. No primary outcome SHALL depend solely on it.

#### Scenario: Uncalibrated judge requested as primary
- **WHEN** a configuration assigns primary or sole authority to an unqualified LLM judge
- **THEN** validation fails before evaluation
