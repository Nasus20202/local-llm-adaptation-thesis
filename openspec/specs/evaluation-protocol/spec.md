# evaluation-protocol Specification

## Purpose

Provide versioned deterministic and human-evaluation records whose fixture behavior, calibration, adjudication, and invalidity decisions are reproducible without altering raw observations.

## Requirements

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

The system SHALL report criterion confusion tables, exact agreement, adjacent-category agreement for ordinal criteria, and nominal or ordinal Krippendorff alpha with a family-clustered 95% interval. Systematic critical disagreement SHALL be an explicit reviewed calibration finding with supporting evidence, not an inference from an agreement percentage. It SHALL apply the approved green/amber/red thresholds without substituting a different coefficient silently.

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

The system SHALL preserve both independent ratings and require a written evidence-based adjudication for critical-label disagreement or ordinal disagreement greater than one level. A resolved disagreement SHALL record the adjudicated value, frozen-rubric validation, rationale, and adjudicator identity or identities. It SHALL preserve unresolved labels rather than silently selecting one.

#### Scenario: Disagreement resolved

- **WHEN** adjudicators resolve a qualifying disagreement with a value supported by the frozen rubric
- **THEN** the derived adjudicated label records that value, rationale, adjudicator identity, and source rater identities while original ratings remain unchanged

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

### Requirement: Protected semantic answer contract

For every development family that can be scored, the evaluator SHALL consume a protected, versioned semantic answer contract bound to exactly one approved family and scenario-input identity/hash. The contract SHALL represent score-affecting meaning as stable criterion identifiers rather than canonical answer prose.

A protected contract SHALL support, as applicable to the task:

- required atomic claims;
- accepted semantic alternatives that satisfy the same criterion without creating additional credit;
- unsupported or contradictory claim criteria that can contribute false-positive or task-failure evidence;
- construct-critical exact literals, values, structures, and comparison rules only where exact identity is part of the construct;
- deterministic structural, schema, action, constraint, and final-state predicates;
- task-specific semantic criteria with observable anchors and allowed assessor modes for judgments that are not mechanically decidable;
- an explicit mapping from each score-affecting criterion to protected frozen-source evidence.

The score calculation interface SHALL NOT accept token overlap, n-gram overlap, edit distance, ROUGE, BLEU, embedding similarity, source-prose similarity, judge verbosity, or verbatim-overlap features.

#### Scenario: Canonical prose used as evaluator truth

- **WHEN** a protected contract supplies one reference paragraph whose wording itself determines open-answer correctness
- **THEN** contract validation fails because open semantic correctness must be represented by atomic criteria and accepted meaning rather than canonical prose

#### Scenario: Accepted paraphrase maps to one claim

- **WHEN** two semantically equivalent response statements satisfy the same required atomic-claim criterion
- **THEN** each response receives the same claim disposition and neither can receive extra credit from wording or repetition

#### Scenario: Lexical feature requested

- **WHEN** evaluator configuration attempts to supply a lexical- or embedding-similarity feature to a semantic score
- **THEN** validation fails before a score is emitted

### Requirement: Hierarchical criterion assessment

Each score-bearing criterion SHALL use the most objective approved assessment path available in this order:

1. an explicit deterministic predicate when the criterion construct is mechanically decidable;
2. a frozen semantic judge only when the criterion remains genuinely semantic and the exact judge configuration is qualified for that criterion/task-language scope;
3. calibrated human adjudication when no qualified judge is available, the judge returns an unresolved/invalid assessment, or the frozen dispute/audit policy requires human review.

A criterion that has an applicable deterministic predicate SHALL NOT be routed to a semantic judge merely for convenience. A semantic judge SHALL return a structured criterion disposition and SHALL NOT assign metric weights or the final task score.

A final primary score SHALL NOT be emitted while any required primary criterion remains unresolved after its allowed assessment route.

#### Scenario: Deterministic rule is available

- **WHEN** a criterion has a valid construct-critical exact/value/structure/action/final-state predicate
- **THEN** the evaluator resolves that criterion deterministically and does not invoke a semantic judge

#### Scenario: Residual open criterion has qualified judge

- **WHEN** an open semantic criterion has no legitimate deterministic rule and references a qualified frozen judge configuration for its task/language scope
- **THEN** the evaluator may accept the judge's structured criterion disposition as assessment input to the deterministic score kernel

#### Scenario: Judge cannot resolve criterion

- **WHEN** the qualified judge returns `unresolved`, malformed output, or another frozen escalation condition
- **THEN** the criterion is routed to calibrated human adjudication and no final primary score is emitted until the required disposition is resolved

### Requirement: Semantic judge configuration is frozen before use

A semantic judge configuration SHALL NOT issue primary criterion dispositions until a separately approved immutable configuration records at least:

- model/provider or model-artifact identity sufficient for reproducibility;
- inference backend/version where relevant;
- judge prompt/template identity and cryptographic hash;
- structured response schema;
- decoding, retry, and failure behavior;
- protected criterion/evidence input contract;
- qualification fixture-set identity;
- predeclared qualification acceptance thresholds;
- predeclared blinded human-audit sampling and judge suspension/requalification policy.

The evaluator implementation SHALL treat a changed model identity, backend identity, prompt/template hash, response schema, or score-affecting inference configuration as a new judge configuration that requires qualification before primary use.

#### Scenario: Unfrozen judge configuration requested

- **WHEN** semantic assessment requests a judge whose required configuration identity or qualification policy is absent
- **THEN** the judge is ineligible for primary assessment and the criterion follows the approved human/fail-closed route

#### Scenario: Judge prompt changes after qualification

- **WHEN** the prompt/template hash differs from the qualified judge configuration
- **THEN** the prior qualification is invalid for that invocation and the judge cannot issue a primary criterion disposition

### Requirement: Semantic judge qualification uses protected human labels

Before a semantic judge configuration can issue primary dispositions, it SHALL pass protected qualification against calibrated human-labelled criterion fixtures covering every task/language/criterion scope for which primary judge assessment is enabled.

Qualification evidence SHALL record, at minimum:

- criterion-level agreement with the frozen human labels;
- disposition confusion counts or matrix;
- an agreement statistic such as Cohen's kappa when the sample/design supports it;
- unresolved, malformed, and schema-failure counts;
- adjudication events generated during qualification;
- the copying-neutral metamorphic invariants required by this specification.

The acceptance thresholds SHALL be frozen and human-approved before judge qualification and SHALL NOT be tuned from participant-model outcomes. Qualification failure SHALL make that exact judge configuration ineligible for primary semantic assessment.

#### Scenario: Judge misses qualification threshold

- **WHEN** the exact frozen judge configuration does not satisfy any predeclared required human-agreement or fairness threshold
- **THEN** qualification is non-green and the judge cannot issue primary criterion dispositions

#### Scenario: Judge qualifies only for one scope

- **WHEN** a judge configuration is qualified for `knowledge/en` but not for another task/language scope
- **THEN** the evaluator accepts primary judge dispositions only within the qualified scope and routes other semantic criteria through their approved fallback

### Requirement: Human adjudication and audit are predeclared

Human review SHALL operate on stable protected criterion identifiers and observable anchors rather than intuitive whole-answer scoring.

The evaluator SHALL route to calibrated human adjudication only through predeclared conditions, including unqualified/unavailable judge paths, unresolved or invalid judge assessments, frozen dispute rules, or a predeclared blinded audit sample.

Audit membership and any rule that can suspend or require requalification of a judge version SHALL be fixed before evaluated participant outputs are inspected. Human audit SHALL NOT be selectively added after seeing condition labels or scores.

#### Scenario: Audited answer selected after score inspection

- **WHEN** an operator attempts to add a participant response to the audit sample because its score is surprising after outcomes are known
- **THEN** the audit-policy validation rejects that post-hoc selection as non-predeclared

#### Scenario: Human adjudication resolves judge uncertainty

- **WHEN** a primary semantic criterion reaches a valid frozen human-adjudication route
- **THEN** the adjudicated criterion disposition becomes the assessment input to the deterministic score kernel and the adjudication event is preserved in provenance

### Requirement: Deterministic score derivation by approved task class

The evaluator SHALL preserve the approved primary metric families and SHALL derive scores only from frozen contract criteria and resolved criterion assessments, regardless of whether an assessment came from a deterministic predicate, qualified semantic judge, or calibrated human adjudication.

For Knowledge families:

- every protected contract SHALL contain at least one required atomic claim;
- each required claim SHALL resolve to exactly one of `satisfied`, `not_satisfied`, or `unresolved` before final scoring;
- false-positive counts SHALL come only from unsupported/contradictory claim criteria declared by the protected contract and resolved for the response;
- `TP`, `FP`, and `FN` SHALL be counted by criterion identity, never by phrase occurrence;
- atomic-claim F1 SHALL be calculated as `2*TP / (2*TP + FP + FN)` after all primary criterion assessments are resolved.

For Procedural families:

- the primary result SHALL remain binary end-to-end task success;
- success SHALL require every contract criterion marked primary-required to pass and every primary prohibited-action/constraint criterion to remain clear;
- parse/schema validity, exact values/structures, command/action bounds, mutation scope, and other mechanically decidable constraints SHALL use deterministic predicates;
- an essential semantic predicate that cannot be decided mechanically MAY use a qualified semantic judge and SHALL route to calibrated human adjudication when the judge is not qualified or cannot resolve it;
- supporting diagnosis or explanation criteria SHALL NOT alter the binary primary result unless the protected contract explicitly marks them primary-required before any participant-model output exists.

For Mixed families:

- every primary procedural hard gate SHALL be evaluated before the compensable score;
- failure of any primary hard gate SHALL set the mixed primary score to `0`;
- when all hard gates pass, the evaluator SHALL calculate the protected contract's pre-frozen task-specific criterion points and divide by its declared positive maximum, yielding a score in `[0,1]`;
- the contract SHALL declare every criterion's point mapping and maximum before participant-model outputs exist; the implementation SHALL provide no default weights or post-outcome tuning.

#### Scenario: Knowledge F1 ignores repetition

- **WHEN** a response repeats one satisfied required claim several times
- **THEN** that claim contributes exactly one true positive

#### Scenario: Procedural required constraint fails

- **WHEN** a Procedural response violates one primary-required constraint while satisfying all other criteria
- **THEN** binary end-to-end task success is `0`

#### Scenario: Mixed hard gate fails

- **WHEN** a Mixed response has a correct explanation but fails one primary procedural hard gate
- **THEN** its mixed primary score is `0` and the explanation cannot compensate for the failed gate

#### Scenario: Mixed contract lacks its point table

- **WHEN** all hard gates are declared but a score-bearing Mixed criterion lacks a pre-frozen point mapping or the positive maximum is absent
- **THEN** evaluation fails before a primary score is emitted

### Requirement: Copying-neutral semantic fairness qualification

Before a protected evaluator version can qualify for the approved development pilot, protected metamorphic fairness fixtures SHALL cover every applicable Knowledge/Mixed task-class × language cell (`knowledge/pl`, `knowledge/en`, `mixed/pl`, `mixed/en`). Every distinct semantic scoring rule used in those cells SHALL be represented by at least one fixture group.

Each applicable fixture group SHALL contain, at minimum:

1. a concise correct paraphrase;
2. correct source-like wording;
3. a correct accepted synonym/reordering variant;
4. a lexically similar but technically wrong response;
5. a partially copied response missing an important required claim;
6. an otherwise valid response with irrelevant source text appended.

The first three variants SHALL receive identical primary semantic criterion dispositions and identical primary scores. The technically wrong and missing-claim variants SHALL score worse on the affected atomic criteria. Appended irrelevant text SHALL never increase the score; when it introduces a declared unsupported or contradictory claim, the affected precision/relevance criterion SHALL worsen.

The pure score kernel SHALL satisfy these relations for equivalent resolved dispositions. Every enabled semantic judge configuration SHALL also satisfy them for the protected semantic fixtures within its qualified scope. Qualification SHALL fail if any required equality or ordering invariant is violated. Verbatim source wording SHALL never receive a bonus.

#### Scenario: Source-like wording beats a paraphrase

- **WHEN** a correct source-like fixture receives a higher score or more favorable semantic disposition than its semantically equivalent concise paraphrase
- **THEN** semantic-fairness qualification fails

#### Scenario: Synonym or claim order changes credit

- **WHEN** an accepted synonym/reordering fixture receives a different primary semantic disposition or primary score from the equivalent correct fixture
- **THEN** semantic-fairness qualification fails

#### Scenario: Lexically similar technical error is rewarded

- **WHEN** a lexically source-like but technically wrong fixture is not worse on the affected criterion than the equivalent correct fixture
- **THEN** semantic-fairness qualification fails

#### Scenario: Irrelevant copied text raises score

- **WHEN** appending irrelevant source text to an otherwise valid answer increases any primary score
- **THEN** semantic-fairness qualification fails

### Requirement: Protected evaluator and judge payloads remain fail-closed

Answer-bearing contracts, evidence mappings, fairness fixtures, human-labelled qualification fixtures, expected fixture results, criterion anchors tied to scenario answers, judge input payloads containing protected criterion/evidence content, and adjudication material SHALL resolve only through the approved protected development evaluator root. Evaluator loading SHALL verify the protected root identity and exact content hash before exposing payload bytes to an authorized evaluator or qualified-judge role.

Participant-model-facing runners, retrievers, prompts, harnesses, skills, W1 processes, future-training roles, and ordinary model-facing serialization SHALL NOT be able to resolve protected evaluator or judge payloads. Denied access SHALL fail closed and SHALL NOT echo protected values, source excerpts, judge prompt payloads, absolute protected locators, or answer-bearing diagnostics.

Judge assessment provenance SHALL bind the exact qualified judge-configuration identity used for the criterion disposition.

#### Scenario: Authorized evaluator loads protected contract

- **WHEN** an evaluator-authorized role supplies a protected reference under `development-protected-evaluator-v1` whose content hash matches
- **THEN** the evaluator may load the protected payload and records the governed access/provenance event

#### Scenario: Qualified judge receives scoped protected input

- **WHEN** a qualified-judge role is authorized for one protected criterion assessment under the exact qualified configuration
- **THEN** it receives only the protected criterion/evidence payload required for that assessment and the governed judge-assessment event records the configuration identity

#### Scenario: Participant-model-facing role attempts protected read

- **WHEN** a participant-model-facing role attempts to resolve a protected evaluator reference
- **THEN** access is denied before content is read and diagnostics contain only safe identifiers and reason codes

#### Scenario: Protected hash mismatch

- **WHEN** protected bytes do not match the frozen reference hash
- **THEN** evaluation fails before any score is emitted and the payload is not copied into diagnostics

### Requirement: Public development evaluator custody

Development-only evaluator contracts, evidence mappings, review artifacts, and evaluator fixtures MAY be stored in the public repository under the dedicated repository-relative subtree configured for `development-protected-evaluator-v1`. Public storage is intentional disclosure of development evaluator truth and SHALL NOT be treated as evaluator-answer secrecy. It SHALL NOT change the evaluator hierarchy, deterministic score derivation, source-evidence binding, semantic-judge freeze gate, human-review gate, class-specific metrics, or final-test custody.

The evaluator subtree SHALL remain excluded from participant-model-facing exports, RAG corpora, training manifests, prompts, skills, harness inputs, W1 inputs, participant workspaces, ordinary logs, and diagnostics. A model-facing role attempting to resolve an evaluator artifact SHALL fail closed before reading it.

#### Scenario: Public evaluator storage does not grant model access

- **WHEN** a participant-model run is prepared from the approved model-facing manifest
- **THEN** evaluator payloads are absent from the run workspace and cannot be resolved through model-facing serialization

#### Scenario: Public evaluator content is disclosed

- **WHEN** a public repository reader inspects a development evaluator artifact
- **THEN** the artifact is treated as intentionally disclosed development material, and contamination reporting does not claim evaluator-answer secrecy
