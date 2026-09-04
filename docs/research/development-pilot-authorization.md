# Development-only Pilot Construction and Qualification Authorization

## Decision purpose

This package is the dedicated authorization gate for the first development-only benchmark pilot under Issue #35. It translates the accepted [benchmark design](benchmark-design.md), [pilot protocol](benchmark-pilot-protocol.md), canonical OpenSpec specifications, and merged pilot foundation into a bounded construction and qualification sequence.

Approval of this package authorizes only the core work listed under [Authorized after this gate](#authorized-after-this-gate). It does not authorize model execution, formal experiments, real `kind`, live W1 access, training-data construction, or any final-test action. Pilot evidence remains feasibility evidence and cannot support a claim that an adaptation method improves over B0.

## Decision register

### Already approved and unchanged

- The independent unit is the scenario family; variants and repeats remain nested.
- The pilot contains exactly 24 development families: eight knowledge, eight procedural, and eight mixed; every class contains four Polish and four English families.
- At most one Polish/English semantic pair per task class may be added without increasing the independent-family count.
- Up to four procedural families may later receive paired static/interactive variants through the separate `kind` path.
- Five stochastic generations and three frozen formulations apply only to the balanced six-family stability subset when model execution is separately authorized.
- The answer contract, condition applicability, target stratum, comparator, metric applicability, custody, evaluator identity, invalidity, calibration, contamination, C2, `kind`, W1, and progression rules remain those in the accepted protocol and canonical specifications.
- C2 constituent selection order remains `P1`, `R1`, `H1`, `S1`, filtered to the declared constituents. The first remaining constituent is the design-time comparator under `strongest-constituent-v1`; no outcome may change that order.
- Final-test inputs, final goldens, and final-test access do not exist within this package and remain outside the normal checkout and every AI-accessible workspace.

### Proposed operational details for this gate

- Construction proceeds through the frozen sequence below and uses the merged `pilot-policy-v1` records as validation evidence.
- The repository receives only redistributable model-facing metadata and hashes. Development inputs may be committed only after rights review; protected evaluator material stays in a separately identified protected root.
- Calibration at this stage uses synthetic non-domain fixtures and responses only. It qualifies evaluator mechanics, rubric clarity, blinding, rating import, adjudication, and agreement computation; it does not qualify a Kubernetes-domain human metric for confirmatory scoring.
- The core authorization ends with a model-free readiness report. Criteria requiring model, real-cluster, or live-web observations remain explicitly `not measured — separate authorization required`; they are not filled with synthetic success values and do not enter an overall empirical `GO` report prematurely.
- Optional `kind` and W1 strata default to `DEFER` until each receives its separate opt-in authorization.

### Remaining choices not resolved by this gate

- The exact compatible Kubernetes release, `kubernetes/website` commit, `kubernetes/kubernetes` commit, included paths, and redistribution decisions are frozen in the [development-pilot source and rights manifest](development-pilot-source-rights-manifest.md). The human researcher approved it on 2026-09-04 and it was squash-merged in [PR #40](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/40). Any source-boundary change requires a successor manifest and human review. Selection used no model outcomes.
- The four optional procedural families for static/interactive pairing are not selected here. If proposed later, selection uses frozen coverage metadata and must cover diagnosis and remediation before any interactive outcome.
- The W1-eligible subset and allowlist revision are not selected here. They require a pre-outcome eligibility manifest and a separate live-access authorization.
- Detector implementations and numerical thresholds for token-overlap and semantic detectors are not invented here. They are calibrated on seeded synthetic positives and hard negatives, frozen with detector identity, and approved before scanning pilot artifacts.
- Domain-specific evaluator calibration and any development-only B0/headroom execution wait for a separately approved execution package after the required runner boundary exists.

## Construction and custody boundary

### Composition and identity

The construction ledger SHALL create 24 family slots before scenario prose is authored. Slot allocation is fixed as follows:

| Task class | Polish | English | Independent total |
| ---------- | -----: | ------: | ----------------: |
| Knowledge  |      4 |       4 |                 8 |
| Procedural |      4 |       4 |                 8 |
| Mixed      |      4 |       4 |                 8 |
| **Total**  | **12** |  **12** |            **24** |

Each family receives a stable `family_id`, `split=development`, class, language, planned subtype, source-role references, answer-form class, and construction status. Every language, static/interactive, formulation, and repeat record receives its own `variant_id`, refers to exactly one `family_id`, preserves `split=development`, and sets `counts_as_independent=false`. The pilot manifest receives its own immutable `manifest_id`, `policy_version=pilot-policy-v1`, canonical serialization, and SHA-256 identity.

Changes before freeze create a new manifest revision. After freeze, corrections create a successor manifest linked to the prior identity; neither family records nor prior manifests are overwritten.

### Model-facing material

The model-facing root may contain only:

- development input and permitted-context references whose rights allow storage;
- family and variant identities, task class, language, answer form, deterministic-gate identities, metric applicability, condition applicability, target-stratum tags, and comparators;
- source/provenance identities and hashes;
- protected-root references consisting only of approved identity, relative path, artifact kind, and SHA-256 hash.

It SHALL NOT contain expected results, protected evidence maps, scoring anchors tied to an answer, rubric decisions, adjudication notes, goldens, evaluator implementation details that reveal answers, final-test locations, or redacted payload recovery data.

### Protected evaluator material

The protected evaluator root may contain development-only expected results, evidence maps, evaluator fixtures, rubrics, and adjudication records. It has a distinct root identity, access ledger, canonical manifest, and content hashes. It is never indexed for RAG or training, passed to prompts, skills, harnesses, W1, or model-facing logs, or copied into validation errors.

Access, freeze, supersession, redaction, and disclosure events are append-only. Published or model-facing reports use stable IDs, status/reason codes, and hashes; any excerpt capable of revealing an answer is replaced with a redaction marker and retained only in the protected evidence record.

### Explicit exclusions

- No final-test family is created, reserved, sampled, inspected, hashed from content, or accessed.
- No final-test golden, evidence map, rubric payload, or expected answer is created or referenced by a resolvable path.
- No training family is constructed in this authorization. A future F1 training set must use a separate root and manifest and be family-disjoint from development and final material.
- No external GenAI service receives development payloads or protected evaluator material.

## Preregistered construction sequence

The sequence is order-sensitive. A failed gate stops downstream work; it does not permit a later step to repair earlier records after seeing outcomes.

1. **Freeze source-selection rules.** Record the supported release window, permitted upstream repositories, inclusion/exclusion rules, license review fields, authoring rules, and family-slot allocation. Then select and hash compatible upstream revisions. No family prose is authored before human source and rights review.
2. **Freeze custody.** Create distinct model-facing, protected-evaluator, and future training root identities; record access roles, redaction rules, append-only locations, and final-test prohibition. Verify that protected markers and final-test declarations fail closed.
3. **Freeze construction metadata.** Assign all 24 family slots to class, language, planned subtype, and model-independent coverage tags. Record family eligibility and target strata from the accepted matrix without using model scores, errors, rater disagreement, or runtime behavior.
4. **Freeze condition and C2 declarations.** For every family, record all approved condition applicability decisions with reasons, answer-contract/metric applicability, target stratum, and comparator. If C2 is declared, freeze the complete constituent set, filtered selector order `P1 → R1 → H1 → S1`, comparator rule, eligibility manifest, and pre-outcome hash before any output exists.
5. **Construct development inputs.** Author fresh source-transformed scenarios within the fixed slots. Human-review technical correctness, language quality, answerability, provenance, licensing, and realism without consulting a model response. A rejected scenario leaves an append-only exclusion/reason record; replacement occupies the same predeclared cell and cannot be selected for favorable performance.
6. **Construct protected evaluator material.** Independently create evidence maps, answer contracts, deterministic checks, and atomic rubrics in the protected root. Reviewers verify each mapping against the pinned source and family input. Model-facing serialization is regenerated only from permitted fields.
7. **Calibrate contamination detectors.** Use synthetic seeded positives and hard negatives to select token-overlap and semantic thresholds and validate all six detector methods. Freeze method version, configuration, threshold expression, normalization/tokenization rules, and calibration evidence before scanning pilot artifacts.
8. **Run the contamination audit.** Audit every required available artifact-pair class, retain candidates and adjudication evidence, and produce a complete six-method aggregate. Direct leakage stops qualification; unresolved semantic candidates require amendment.
9. **Qualify deterministic evaluators and rating mechanics.** Use only synthetic non-domain positive, negative, boundary, malformed, and ambiguous fixtures. Freeze fixture-set and evaluator identities, require repeated identical outcomes/reason codes, then run the blinded human calibration sequence below.
10. **Perform independent solvability review.** Two technically competent reviewers inspect each development family against its protected evidence/validator mapping without model outputs. Record family-level decisions and reasons; do not rewrite a family because of an adaptation hypothesis.
11. **Issue the model-free readiness report.** Report custody/integrity, composition, source/rights review, deterministic qualification, synthetic calibration, contamination, and independent solvability separately. Keep headroom, run invalidity, condition fidelity, real `kind`, and live W1 unmeasured pending their own prerequisites and authorizations.
12. **Request the next gate.** Any later model execution requires a focused execution package and an approved runner boundary. Real `kind` and live W1 additionally require their separate opt-in releases below.

Training, development, and evaluation custody are therefore separated by root identity, manifest, access role, and data flow. Construction decisions precede model outcomes. No outcome is available in steps 1–11.

### Confirmatory C2 follow-up

If later pilot error analysis motivates C2 eligibility or changes its comparator, that pilot C2 is labeled exploratory. Confirmatory use then requires a new development-family manifest that:

- is frozen before its outcomes;
- links the immutable exploratory-manifest identity and hash;
- derives the excluded family set from that linked manifest rather than a self-declared list;
- contains no overlapping family ID or semantic family;
- repeats the model-independent eligibility and frozen comparator validation.

The exploratory record and all exclusions remain append-only.

## Contamination audit plan

### Audit inputs and artifact-pair identity

Each input artifact unit records `artifact_id`, root/role, split where applicable, family/variant membership, language, media type, canonical content hash, parent-manifest identity, and detector-readable representation hash. An `artifact_pair_id` is derived from the ordered pair of immutable artifact identities plus detector version and configuration hash.

Required pair classes for material that exists at this stage are:

- development input ↔ every other development input, to detect undeclared families/near-duplicates;
- development input ↔ source chunks and public examples, to characterize source transformation rather than treat expected source grounding as hidden;
- development input ↔ prompts, examples, skills, harness text, tool fixtures, and captured tool outputs available to model-facing conditions;
- development input ↔ any pre-existing training material; if none exists, the training manifest identity and empty-state evidence are recorded;
- protected evaluator material ↔ every model-facing, corpus, prompt, skill, harness, tool-fixture, and training artifact, to detect answer leakage;
- Polish ↔ English artifacts, including declared translations and independent families, to identify intended and unintended semantic-family relationships.

Future training and final-test manifests trigger a complete rerun. The current audit does not inspect or imply the existence of final-test content.

### Required detectors and threshold governance

| Audit                        | Input representation                                                                             | Match decision before human adjudication                                                                     |
| ---------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Exact                        | Original bytes/text with encoding identity                                                       | Identical content hash or exact declared representation equality                                             |
| Normalized                   | Frozen whitespace, line-ending, Unicode, comment, and safe formatting normalization              | Equality of the frozen normalized representation                                                             |
| Token-overlap                | Frozen tokenizer and n-gram/shingle configuration                                                | Score meets the threshold calibrated and frozen on seeded positives and hard negatives before pilot scanning |
| Code/configuration structure | Parsed or normalized Kubernetes/code structure with non-semantic values handled by a frozen rule | Structural signature match under the frozen detector rule                                                    |
| Semantic                     | Frozen embedding/model or other semantic representation and distance function                    | Score meets the pre-pilot calibrated threshold; detector/model identity and artifact hash are mandatory      |
| Cross-language               | Frozen multilingual or translate-then-compare representation plus declared family relationships  | Score meets the pre-pilot calibrated threshold or a declared translation/family relation requires review     |

No new numerical token or semantic threshold is asserted by this package. Calibration evidence, selected threshold, detector identity, configuration, false-positive/false-negative observations on synthetic controls, and rationale must be frozen before actual pairs are scanned. Family and declared translation relationships override an automated non-match.

### Adjudication and evidence retention

Every detector candidate receives one of `pending`, `confirmed`, or `rejected`, a written rationale, reviewer identity, UTC timestamp, artifact-pair identity, detector output/hash, and protected evidence reference. Automated non-matches retain summary/count evidence and the aggregate six-detector completeness record. Reports distinguish:

- `public-domain exposure expected`;
- `semantic overlap detected/not detected under method`;
- `direct overlap detected/not detected under method`;
- `parametric exposure unknown`.

No numerical probability of pre-training exposure and no contamination-free claim is permitted.

### STOP/DEFER and amendment handling

- Confirmed direct train/development overlap, final/development overlap if a future final manifest exists, or any golden/evaluator leakage is `STOP/DEFER`. Preserve the event and affected identities; do not silently delete or auto-replace them.
- An unresolved semantic, structural, token, or cross-language candidate is `AMEND` until human adjudication.
- A missing required detector, detector failure, missing artifact identity, or incomplete aggregate prevents a no-overlap claim and is `STOP/DEFER` for qualification until complete evidence is produced.
- Expected source/domain exposure is recorded as a limitation, not an automatic exclusion.
- Replacement of affected non-final material is allowed only for leakage, ambiguity, unsolvability, missing evidence, or construct mismatch, with a successor manifest and reason record—not because a method performed poorly.

## Evaluator calibration plan

### Synthetic non-domain material only

At this gate, fixtures and responses are synthetic, non-Kubernetes, non-benchmark material designed to exercise evaluator contracts without carrying a benchmark answer. They span Polish and English, knowledge-like, procedural-like, and mixed-like answer forms, but they cannot be reused as pilot families, training examples, goldens, prompts, or few-shot demonstrations.

Each deterministic evaluator component must include positive, negative, boundary, malformed, and ambiguous fixtures. Expected results remain protected. Qualification requires 100% expected outcomes and identical outcome and reason codes on repeated execution. An unresolved ambiguous fixture is rejected or routed to a named human criterion; it never receives an arbitrary substantive score.

### Rubrics and labels

Every human rubric is task-specific and decomposed into named atomic criteria with observable applicability and anchors. Ordinal criteria use exactly `0`, `1`, and `2`. Critical safety, answerability, and task-success decisions remain separate binary labels. A universal overall-quality score is prohibited.

The candidate rubric, fixture set, rating schema, randomized response-ID map, and permitted evidence bundle are frozen before qualification ratings. Raters see no method, model, prompt, seed, condition, or each other's ratings. Each immutable rating records rater pseudonym, randomized response identity, criterion values, rubric version, timestamp, and declarations of independence and blinding.

### Calibration sequence and decision rules

1. Two technically competent raters independently score 12 synthetic training responses covering both languages, the three form classes, and correct, incorrect, boundary, and malformed behavior.
2. They discuss disagreements, revise observable anchors, and freeze the candidate rubric. These 12 responses are excluded from reliability estimation.
3. They independently score a disjoint 24-response synthetic qualification set balanced across class-like form and language.
4. Report per-criterion confusion tables, exact agreement, adjacent-category agreement for ordinal criteria, and nominal or ordinal Krippendorff alpha with a family-clustered 95% interval.
5. `GO` requires at least 90% exact agreement for every critical binary label, pooled primary-rubric alpha at least 0.80, and lower 95% interval bound at least 0.67.
6. `AMEND` applies when pooled alpha is 0.67–0.79 or the lower bound is below 0.67 without systematic critical disagreement. Revise anchors and permit at most one new disjoint qualification set.
7. `STOP/DEFER` applies when pooled alpha is below 0.67, systematic critical disagreement remains, or the second qualification attempt is not green. The affected human metric must be narrowed, replaced, or kept exploratory before final freeze.

Synthetic green status qualifies the workflow and schema only. Domain-specific human scoring remains disabled until a later Kubernetes-domain calibration is approved and green.

### Adjudication and invalidity

Preserve both independent ratings. Critical-label disagreement or ordinal disagreement greater than one level requires written evidence-based adjudication containing the adjudicated value, frozen-rubric validation, rationale, adjudicator identity, and source-rating identities. If unresolved, preserve both labels and set the conservative sensitivity-analysis flag.

Corrupted capture, missing required provenance, hash mismatch, evaluator-infrastructure failure, or required measurement failure is invalid and remains append-only. Wrong answers, refusals, malformed evaluated outputs, action-budget exhaustion, evaluated-system timeouts, failed remediation, and failures belonging to the deployed condition are valid task failures. Later exclusion-sensitive conclusions require both complete-case and all-fail sensitivity bounds.

An LLM judge remains supplemental, disabled for confirmatory scoring at this stage, and receives no protected material.

## Optional controlled strata

### Paired static/interactive `kind`

**Offline readiness, allowed by the core gate:** propose up to four procedural family IDs using only frozen coverage metadata; define paired static/interactive variant identities; prepare versioned validator fixtures and neutral-policy metadata using deterministic fakes; verify pinned-identity, reset, permission, matched-access, budget, final-state, and append-only capture requirements without starting a cluster. This preparation does not select families from model outcomes.

**Separate authorization required:** an exact opt-in must name the approved family manifest, `kind` revision, node/workload digests, cluster-policy hash, host/container identity, namespace policy, reset policy, action/output/time budgets, validator version, and evidence location. Only then may a disposable real cluster be created.

**Qualification:** ten consecutive resets must reproduce the declared initial-state hash and validator result; ten independent DNS and outbound HTTP(S) probes must be denied; allowed permissions must succeed and all prohibited permissions fail; validator fixtures must be deterministic across all five fixture classes; applicable conditions must have identical neutral policies; all four variants must be semantically paired; median reset plus validation must be at most three minutes and no attempt may exceed five minutes. Any isolation or privilege failure is `STOP/DEFER`. Timing/reset instability is `AMEND` with one bounded redesign; a repeated non-green result defers interactive confirmatory evidence while static families remain eligible.

### Official-source W1

**Offline readiness, allowed by the core gate:** propose a model-independent eligible family subset, versioned official-source allowlist/deny policy, redirect cases, budget manifest, provenance schema, and synthetic provider fixtures. All default checks use deterministic fakes and cannot contact a service.

**Separate authorization required:** an exact opt-in must name the eligible manifest, W1/combined-condition identity, provider/tool identity, allowlist/policy hash, frozen budgets, deny fixtures, source-drift reviewer, protected-storage boundary, and append-only capture location. W1 remains separate from R1 and H1; any combined condition has its own preapproved identity.

**Qualification:** allow only approved official Kubernetes paths and revalidate every redirect; deny the thesis repository, benchmark/golden storage, user files, local addresses, and non-allowlisted domains. Enforce per response at most three searches, five results per search, two fetches, five total tool calls, 4,000 extracted context tokens, and 120 seconds of measured tool wall time. Persist complete provenance before body text is exposed. A human source-drift precheck records reviewer, rationale, frozen/current hashes, and semantic compatibility. `GO` requires complete provenance, safe access and redirects, and at least 90% within-budget completion across eligible attempts. Prohibited access or missing provenance is `STOP/DEFER`; availability/reproducibility limitations are `AMEND` and may leave W1 exploratory.

Both optional strata may be deferred independently without invalidating the static development benchmark.

## Pilot acceptance and stopping rules

The accepted protocol remains authoritative. The following table restates it for execution planning; it does not alter a threshold.

| Criterion                           | GO                                                                                          | AMEND                                                                                                              | STOP/DEFER                                                                            |
| ----------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| Deterministic evaluation            | 100% fixture agreement and idempotence                                                      | Correctable non-critical specification ambiguity before outputs                                                    | Any unexplained or post-output evaluator change                                       |
| Human calibration                   | Every critical binary label ≥90% exact agreement; pooled alpha ≥0.80; lower 95% bound ≥0.67 | Pooled alpha 0.67–0.79 or lower bound <0.67 without systematic critical disagreement; one disjoint requalification | Alpha <0.67, unresolved systematic critical disagreement, or second non-green attempt |
| Solvability/evidence                | ≥90% of families independently judged solvable with complete evidence/validator mapping     | 80–89% or localized ambiguity                                                                                      | <80% or construct mismatch                                                            |
| Headroom                            | B0 success 20–80% overall and success plus failure in every target stratum                  | One stratum outside range while controls discriminate                                                              | Ceiling/floor cannot be repaired without changing the construct                       |
| Infrastructure/evaluator invalidity | ≤5%                                                                                         | >5% and ≤10% with an identified fix                                                                                | >10% or condition-dependent invalidation                                              |
| Condition fidelity/fairness         | 100% required provenance and matched declared controls                                      | Non-outcome-informed implementation correction                                                                     | Hidden information, unequal permission, or uncaptured mutation                        |
| Contamination                       | No direct leakage; semantic candidates adjudicated                                          | Unresolved semantic candidates                                                                                     | Direct item/golden exposure or an incomplete required audit preventing qualification  |
| `kind`                              | Every approved feasibility check green                                                      | One bounded redesign for timing/reset instability                                                                  | Isolation/privilege failure or repeated non-green result                              |
| W1                                  | All provenance/access checks and ≥90% completion                                            | Availability/reproducibility limitation                                                                            | Prohibited access or missing provenance                                               |
| Researcher feasibility              | Final work fits the pre-freeze time/compute cap with 20% contingency                        | Scope reduction preserving primary strata                                                                          | Work exceeds the cap or needs unavailable raters/hardware                             |

The worst safety, leakage, or evaluator-validity outcome governs progression. Missing measurements are reported as missing and cannot be converted to success. Infrastructure failure that breaks capture, identity, provenance, evaluator operation, or required measurement is invalid; it is retained and counted in the invalidity rule. Evaluated-system failure with intact capture remains a valid failure.

At the present model-free gate, only criteria with genuine observations receive a status. Headroom, model-run invalidity, condition fidelity under execution, real `kind`, and live W1 remain pending separate authorization rather than being populated with synthetic evidence. A full pilot progression report is produced only when all approved criteria have legitimate evidence.

## MSc feasibility envelope

These are workload estimates and scope controls, not scientific acceptance thresholds.

| Work                     | Fixed limit or realistic envelope                                                                                                                                        | Deferral rule                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Core families            | Exactly 24 independent families; no expansion during pilot qualification                                                                                                 | Reduce subtype ambition within the approved cells rather than add families                                        |
| Nested language variants | At most three pairs, one per task class                                                                                                                                  | Defer any or all without changing class/language family counts                                                    |
| Stability observations   | Six families × three frozen formulations × five generations when model execution is later authorized                                                                     | Do not increase repeats to compensate for too few families; seven belongs only to the approved final-study rule   |
| Human calibration        | 24 training ratings plus 48 first qualification ratings across two raters; at most 48 more ratings for one disjoint requalification                                      | A second non-green attempt defers/narrows the metric                                                              |
| Pilot human scoring      | Double-rate only responses whose primary outcome genuinely requires human judgment; deterministic outcomes remain primary where valid                                    | Stage by class and stop when a criterion is red rather than rate unusable downstream material                     |
| Contamination            | Six detectors over batched immutable pair classes; human review only for flagged or relationship-mandated pairs                                                          | A detector may be replaced before pilot scanning; a missing required detector blocks qualification                |
| Core calendar            | Approximately 3–4 part-time weeks for source freeze, 24-family authoring/review, protected evaluators, audit, calibration, and readiness reporting, plus 20% contingency | Stop and reduce optional subtypes if the envelope is exceeded                                                     |
| Core storage/compute     | Text/manifests/evaluator evidence should remain below roughly 1 GB; semantic detection is a bounded one-off CPU/GPU job over the pilot corpus                            | Keep large caches outside Git and retain only identities, lawful evidence, and required reproducibility artifacts |
| Optional `kind`          | Up to four paired families; approximately one additional week plus external image storage and repeated reset/probe time                                                  | Independently defer; static procedural families remain valid                                                      |
| Optional W1              | One predeclared subset; approximately 2–4 additional researcher days plus live-service qualification time                                                                | Independently defer or report exploratory                                                                         |

The dominant human burden is careful family/evidence review and double rating, not software architecture. Construction should stop at the fixed family count, reuse atomic evaluator components only where constructs truly match, and avoid product-scale orchestration.

## OpenSpec assessment

No OpenSpec change is created by this package. The canonical `benchmark-pilot-dataset`, `evaluation-protocol`, `controlled-cluster-tasks`, and `web-search-sensitivity` specifications already define the observable custody, identity, C2, evaluator, invalidity, cluster, W1, and progression behavior needed for this authorization. The merged implementation provides typed records, validators, deterministic fakes, and fail-closed opt-in boundaries.

This gate intentionally excludes model execution and real external integration, which the merged foundation also excludes. A later request to integrate actual model inference, execute real `kind`, contact a live provider, or automate detector algorithms beyond the existing record contract must be assessed as a separate narrow OpenSpec change before implementation.

## Authorized after this gate

After explicit human approval, the researcher and Codex may:

- freeze the source/custody/construction manifests;
- construct and human-review the 24 development-only family inputs and protected evaluator material;
- calibrate and execute all six contamination audits on development material;
- construct only synthetic non-domain evaluator fixtures and calibration responses;
- run deterministic evaluator qualification, blinded human workflow calibration, and independent model-free solvability review;
- prepare offline `kind` and W1 readiness metadata and deterministic-fake fixtures;
- record append-only evidence and a model-free readiness decision.

They may not run a model, create or access final-test material, construct training data, create a real cluster, access a live web service, perform formal experiments, or claim method improvement. Those actions require their later explicit gates.

## Exact approval sentence

> I approve the Issue #35 development-only pilot construction and model-free qualification package. This authorizes the 24-family development pilot, protected evaluator materials, six-detector contamination audit, synthetic non-domain evaluator calibration, independent solvability review, and offline `kind`/W1 readiness preparation exactly as specified; it does not authorize model execution, training data, final-test material or access, a real `kind` cluster, live web access, formal experiments, or method-effect claims.
