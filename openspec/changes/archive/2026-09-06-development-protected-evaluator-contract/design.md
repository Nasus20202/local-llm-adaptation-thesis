## Context

PR #44 approved and merged exactly 24 development-only scenario inputs under `development-model-facing-v1`. The next Issue #35 sequence step is protected evaluator construction, but implementation must not begin until the scientific contract is complete.

The existing foundation already provides evaluator identity, deterministic fixture classes, rubric calibration, adjudication, invalidity, protected references, and pilot custody validation. It intentionally does not define the answer-bearing contract for these concrete development families. The approved evaluation clarification also prohibits model-answer citation scoring and makes semantic, not lexical, correctness authoritative.

Review of established benchmark patterns supports a hierarchy rather than one universal scorer: IFEval, LiveBench, and SWE-bench prefer objective/verifiable checks where available, while MT-Bench, AlpacaEval, and WildBench demonstrate both the usefulness and the calibration/bias risks of LLM judges for open semantic evaluation. This change adopts that hierarchy without changing the approved metric families.

This change therefore extends the existing evaluator/pilot capabilities only. It does not create a second evaluator architecture and it does not place protected Kubernetes answer content in the repository.

## Goals / Non-Goals

**Goals:**

- make a protected per-family evaluator contract precise enough that Codex can implement schemas and score logic without choosing scientific criteria;
- preserve atomic-claim F1, binary Procedural task success, and normalized Mixed scoring with non-compensable procedural hard gates;
- use deterministic verification whenever the task construct is mechanically decidable;
- allow residual open semantic criteria to use only a separately frozen, human-qualified semantic judge, with calibrated human adjudication for unresolved/disputed cases and a predeclared audit sample;
- keep score calculation deterministic after criterion dispositions are resolved;
- make semantic fairness structural: the score kernel has no lexical-similarity or embedding input;
- bind every protected criterion to the approved scenario hash and frozen Kubernetes v1.36.4 evidence;
- qualify anti-copying behavior with protected metamorphic fixtures in Polish and English;
- reuse the frozen protected-root/access/provenance boundaries and fail closed on leakage.

**Non-Goals:**

- authoring the 24 protected answer contracts, answer-bearing evidence maps, Kubernetes fixture responses, expected fixture results, or adjudication content;
- implementing production evaluator code in this planning PR;
- selecting or executing a real LLM judge in this planning/Gate-A implementation package;
- semantic scoring by embeddings, NLI similarity, ROUGE/BLEU, edit distance, token overlap, or another similarity metric;
- participant-model execution, RAG execution, training, final-test construction/access, real `kind`, live W1, C2, or semantic-pair selection;
- changing the approved questions, source release, condition/comparator rules, metric families, existing calibration thresholds, or pilot progression rules.

## Decisions

### 1. Extend the existing evaluator foundation

Codex shall extend `thesis_bench.evaluation` and the existing pilot protected-reference/custody types rather than add a standalone scoring service, database, annotation product, or generic evaluator framework.

The scientific unit is a protected contract plus immutable identities. Public/model-facing records retain only safe references and hashes.

Alternative: a new “semantic evaluator” subsystem. Rejected because it duplicates identity/custody behavior and would make cross-condition consistency harder to audit.

### 2. The protected truth is a criterion contract, not answer prose

Each family later receives one protected contract bound to its approved `family_id` and exact input hash. The contract can include:

- required atomic-claim criterion IDs;
- accepted semantic alternatives that map to the same criterion;
- contract-declared unsupported/contradictory criteria;
- construct-critical exact literals/values/structures and explicit comparison rules;
- deterministic gates;
- task-specific semantic criteria and observable anchors where open judgment is necessary;
- permitted assessor mode/configuration references for semantic criteria;
- evidence links for every score-affecting criterion;
- class-specific score configuration.

A contract may retain short protected examples if needed to make an assessor anchor observable, but no canonical paragraph is used as a similarity target.

The 24 concrete criterion payloads are intentionally not committed by this change. They are scientific protected content to be authored later from the approved input plus frozen upstream evidence.

### 3. Criterion assessment is hierarchical; score calculation stays deterministic

For a score-bearing criterion, the evaluator follows this order:

1. **Deterministic predicate** when exact value, structure, schema, count, action, final state, or another objective property is genuinely part of the construct.
2. **Qualified frozen semantic judge** only when the criterion remains genuinely semantic and an exact approved judge configuration has passed human-labelled qualification for that criterion/task-language scope.
3. **Calibrated human adjudication** when no qualified judge is available, the judge returns `unresolved`/invalid output, or the frozen dispute/audit policy requires human review.

A deterministic criterion is never sent to the judge merely for convenience. An LLM judge returns a structured criterion disposition; it does not directly assign TP/FP/FN weights, Procedural task success, Mixed weights, or final task score. The scorer deterministically converts resolved criterion assessments into the approved metric family.

The score kernel accepts no token overlap, n-grams, edit distance, ROUGE/BLEU, embedding similarity, source-prose similarity, judge verbosity, or verbatim-overlap feature.

Alternative: human review for every open criterion. Rejected as the default because it increases manual effort and avoidable rater variability.

Alternative: an LLM judge as an unqualified default semantic matcher. Rejected because judge/model/prompt versions can introduce systematic bias and non-reproducible drift. A judge is a measurement instrument that must be frozen and qualified, not answer truth.

### 4. Judge identity and qualification are separately frozen

A judge cannot issue primary semantic dispositions until a later explicit freeze records, at minimum:

- exact model/provider or model-artifact identity sufficient for reproduction;
- inference backend/version where relevant;
- prompt/template identity and hash;
- structured response schema;
- decoding, retry, and failure configuration;
- protected criterion/evidence input contract;
- qualification fixture-set identity;
- predeclared acceptance thresholds;
- blinded human-audit sampling and requalification/suspension policy.

The exact judge model and thresholds are not chosen in this PR. Judge-model execution requires a later human gate after generic machinery and protected criterion bundles exist.

Judge qualification uses protected human-labelled criterion fixtures covering the actual task/language scope. Qualification evidence records criterion-level agreement, disposition confusion counts/matrix, an agreement statistic such as Cohen's kappa where methodologically appropriate, schema/unresolved failures, adjudications, and the copying-neutral metamorphic invariants. Thresholds cannot be tuned after candidate-model outcomes are observed.

If qualification fails, that judge configuration cannot issue primary dispositions. The evaluator fails closed or uses the approved human route.

### 5. Human review is adjudication and audit, not the default scorer

Human assessment operates on the same atomic protected criterion and observable anchors as the semantic judge. It is not an intuitive whole-answer rating.

Human review is required for predefined escalation paths and a predeclared blinded audit sample. Audit membership and any rule that can suspend or requalify a judge version are frozen before evaluated outputs are inspected. This prevents selective post-hoc review of inconvenient results.

An unresolved primary criterion still blocks the final primary score until the approved adjudication path resolves it.

### 6. Class-specific score rules are narrow and fail closed

**Knowledge.** Required claims are unique criterion IDs. Satisfied required claims contribute TP; unsatisfied required claims contribute FN; only protected contract-declared unsupported/contradictory criteria can contribute FP. Repetition does not multiply counts. Once primary assessments are resolved, use `2TP/(2TP+FP+FN)`. Every Knowledge contract has at least one required claim.

**Procedural.** Primary task success is binary. All primary-required predicates must pass and all primary prohibited constraints must remain clear. Deterministic rules cover parse/schema, construct-critical values/structures, command/action bounds, mutation scope, and comparable mechanical checks. If an essential semantic diagnosis cannot be decided mechanically, the criterion may use the qualified semantic judge and then human adjudication if necessary; there is no lexical fallback.

**Mixed.** Evaluate primary procedural hard gates first. Any failed hard gate makes the primary score `0`. Otherwise, sum the contract's pre-frozen criterion points and divide by its declared positive maximum. Each protected contract must explicitly freeze its point table. No default point weights or post-output revisions are permitted.

### 7. Fairness qualification uses metamorphic relations, not overlap metrics

Actual Kubernetes fairness fixture payloads remain protected. At least one fixture group exists for each Knowledge/Mixed × Polish/English cell, and every distinct semantic scoring rule used in those cells is covered.

Within each group:

- concise correct paraphrase, correct source-like wording, and accepted synonym/reordering have identical semantic dispositions and primary scores;
- lexical similarity cannot rescue a technical error;
- missing a required claim worsens the affected atomic criterion;
- appended irrelevant source text never increases score and can reduce a declared unsupported/relevance criterion.

Qualification has three separable checks:

1. pure score-kernel tests confirm that equivalent resolved criterion assessments remain equivalent and no lexical feature can alter the result;
2. protected semantic-judge qualification, when a judge is enabled, confirms the frozen judge preserves the required semantic relations and meets the human-labelled agreement thresholds;
3. protected human calibration/adjudication confirms the human anchor path remains usable for unresolved/disputed cases and audit.

A violated required invariant makes that evaluator/judge version non-green.

### 8. Source evidence is frozen and criterion-level

A protected evidence map links each score-affecting criterion to one or more entries from the approved Kubernetes v1.36.4 source registry. The evidence identity carries the frozen inventory/repository revision and path/blob or OpenAPI hash/selector needed for audit.

The participant model does not need to reproduce this source identity. Evidence relationships are protected because they reveal what facts determine the score.

The reviewer catalog may help the human inspect PR #44, but its `Expected answer — reviewer note` text is explicitly excluded from evaluator construction inputs. Protected contract construction provenance may reference only the approved scenario identity and the frozen source registry/source snapshots as answer-truth inputs.

### 9. Reuse the frozen custody root and safe-handle boundary

Protected answer-bearing bytes resolve only under logical root `development-protected-evaluator-v1`. Runtime binding to a concrete private filesystem/object location is supplied outside committed model-facing configuration.

A protected load validates:

- actor/purpose authorization;
- root identity;
- protected-root-relative reference;
- exact content hash;
- contract-to-approved-input binding;
- exact qualified judge-configuration identity for judge-derived assessments.

Every governed read/write/freeze/supersession/review/judge-assessment/adjudication/audit/disclosure event is recorded through the already-approved append-only development custody evidence streams.

Public/model-facing serialization can carry only safe artifact handles, hashes, non-answer-bearing assessor/config identities, and reason/status codes. Errors never echo protected values, source excerpts, answer-bearing criterion names/descriptions when those reveal the answer, judge prompt payloads, or absolute protected locators.

### 10. Protected content, generic implementation, judge freeze, and execution stay separate

This work deliberately separates:

1. **Scientific specification committed now:** contract shape, assessment hierarchy, score invariants, semantic fairness, judge qualification requirements, human adjudication/audit, source/custody/provenance requirements.
2. **Generic implementation after Gate A:** typed records, validators, deterministic score derivation, model-agnostic semantic-assessment/qualification records, protected-root loader boundary, safe diagnostics, append-only integration, and synthetic non-answer-bearing tests. No real judge is selected or run.
3. **Protected content instantiated later:** the 24 per-family criteria, alternatives, prohibited claims, exact values/structures, deterministic predicates, Mixed point tables, answer-bearing anchors/evidence maps, human-labelled qualification fixtures, and Kubernetes fairness fixture payloads/expected results.
4. **Judge freeze and qualification later:** exact judge model/backend/prompt/configuration, predeclared thresholds and audit policy receive explicit approval, then judge qualification may execute against the protected human-labelled fixtures.
5. **Participant-model scoring later still:** only a later focused execution authorization may evaluate participant-model outputs.

Codex is not authorized by this PR to invent protected layer-3 content or to choose/run the layer-4 judge.

## Risks / Trade-offs

- **[LLM judge adds model/version bias.]** Freeze the exact configuration, qualify against protected human labels, audit a predeclared sample, and fail closed on qualification drift or unresolved assessment.
- **[Human adjudication still introduces rater variability.]** Restrict it to atomic anchored criteria, use the existing calibration/adjudication protocol, and record agreement/audit evidence.
- **[A judge can be less reproducible when backed by a mutable hosted API.]** Prefer an immutable/model-artifact identity where feasible; otherwise freeze all provider-visible version/configuration evidence and treat unrecoverable drift as a new judge version requiring requalification.
- **[Protected per-family contracts require substantial expert authoring.]** Keep them atomic and source-mapped; do not replace this work with generic prose goldens.
- **[Mixed point tables could hide weighting choices.]** Require every point mapping and maximum to be explicit, frozen before outputs, and reviewed as protected scientific content; the implementation supplies no default.
- **[Protected diagnostics or judge prompts could leak answers.]** Return safe IDs/reason codes only and test error paths with synthetic secrets.
- **[A source locator can drift if it is not hash-bound.]** Require the exact approved inventory/repository revision and path/blob or OpenAPI hash identity.
- **[Fairness/qualification fixtures could become training examples.]** Keep payloads in protected evaluator custody and exclude them from RAG, participant prompts, skills, future training, participant-model logs, and reviewer convenience exports.

## Migration Plan

1. Human-review and approve this planning PR at Gate A.
2. Codex implements only the generic tasks in `tasks.md`, using synthetic non-domain/non-answer-bearing fixtures and no real judge-model execution.
3. Independent Chat review verifies implementation against this change; the human merges only after review passes.
4. Work synchronizes/archives the OpenSpec change after merge.
5. Under a separately controlled protected-authoring step, instantiate and human-review the 24 protected contracts/evidence maps/fairness and judge-qualification fixture payloads; freeze their hashes and custody evidence.
6. Prepare a separate judge freeze: exact model/backend/prompt/decoding/schema identity, human-labelled qualification set, predeclared acceptance thresholds, audit sample/policy, and custody boundary. Human approval is required before any judge-model run.
7. Execute judge qualification only after that approval. A failing judge remains ineligible for primary semantic assessment; unresolved criteria retain the calibrated human route.
8. Only a later focused participant-execution authorization may score participant-model-derived pilot outputs using the qualified evaluator version.

Rollback before implementation is deletion of this active planning change and its explanatory documentation. After implementation, rollback creates a new evaluator version; it never rewrites protected or derived historical records.
