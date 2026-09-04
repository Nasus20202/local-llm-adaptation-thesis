# Development-only Benchmark Pilot and Evaluator Calibration Protocol

## Decision status and boundary

This is the proposed Issue #4 protocol for Human Gate A. It operationalizes the accepted benchmark-domain policy without constructing an item, fixture payload, golden answer, evaluator, cluster environment, or model run. The accompanying OpenSpec change defines the minimum software behavior required to validate a later development-only pilot. Approval authorizes only that bounded implementation package; it does not authorize pilot/final item construction, real cluster/web/model execution, or final-test access.

The pilot asks whether the planned study can be executed and interpreted. It does not test the thesis hypotheses and must not be used to claim that one adaptation method is superior.

## Pilot objectives

The development-only pilot must establish:

1. task solvability, source coverage, answer-contract clarity, and useful baseline headroom;
2. deterministic evaluator correctness and human-rubric reliability;
3. method applicability and mechanism-aligned target strata without requiring a positive result;
4. feasible repetition, paraphrase, item-family, rating, runtime, and storage budgets;
5. whether a controlled interactive `kind` stratum can be fair, isolated, resettable, and automatically verified;
6. whether an official-source web-search sensitivity condition can be reproduced and kept separate from closed-corpus RAG and harness orchestration;
7. whether contamination controls detect direct, semantic, configuration, and cross-language overlap while honestly reporting unobservable pre-training exposure.

## Units, partitions, and pilot size

The scenario family remains the independent unit. Static/interactive forms, Polish/English semantic variants, prompt formulations, and repeated generations are nested observations.

The first pilot construction is capped at **24 development-only families**: eight knowledge, eight procedural, and eight mixed. Each task class contains four Polish and four English independent families. This is a feasibility sample, not the final sample size. It is large enough to exercise every planned class-language cell while keeping construction and review feasible for one researcher.

Planned coverage, not item content:

| Task class | Development families | Required coverage                                                                       |
| ---------- | -------------------: | --------------------------------------------------------------------------------------- |
| Knowledge  |                    8 | direct evidence, synthesis, absent-answer/abstention, and distractor-heavy evidence     |
| Procedural |                    8 | diagnosis, constrained repair, ordered action, and structured artifact/schema adherence |
| Mixed      |                    8 | source-grounded decision plus verifiable artifact or bounded procedure                  |

At most one paired Polish/English semantic variant per task class may be added for equivalence checks. Such variants retain one family ID and do not change the independent-family count. Four procedural families may additionally receive paired static and interactive `kind` variants under the controlled stratum below.

No final-test family is authored, sampled, inspected, or reserved during this pilot. Training families for F1 are separately authored and family-disjoint from development and future final-test material.

## Preregistered method-to-task hypothesis matrix

The matrix identifies where each mechanism should have an opportunity to help. It is not a promise of improvement, a task-selection target, or permission to tune against final outcomes.

| Condition | Mechanism-aligned target stratum                                                                                                                                                                                                    | Preregistered directional hypothesis                                                                                                                            | Primary comparator                                                   | Important non-target or regression check                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| B0        | All applicable families                                                                                                                                                                                                             | Reference condition; no positive direction assumed                                                                                                              | —                                                                    | Failure mode and headroom profile                                                                           |
| P1        | Constraint-dense knowledge and procedural families with explicit answer contracts                                                                                                                                                   | Engineered zero-shot instructions improve constraint adherence and retry-free valid output                                                                      | B0                                                                   | Token/latency cost, verbosity, factual regressions                                                          |
| P2        | Recurring structured diagnosis, taxonomy, and output-schema families                                                                                                                                                                | Structured or few-shot examples improve schema adherence and classification consistency beyond P1                                                               | P1 and B0                                                            | Anchoring, copied errors, context cost                                                                      |
| R1        | Knowledge and mixed families whose required evidence is present in the pinned corpus, including absent-answer cases                                                                                                                 | Closed-corpus retrieval improves evidence recall, grounded correctness, and calibrated abstention                                                               | Matched no-retrieval prompt and B0                                   | Retrieval failure, distractor sensitivity, unsupported claims                                               |
| F1        | Recurring learnable behavior: diagnosis structure, manifest repair pattern, controlled terminology/taxonomy, Polish technical phrasing, concision, and schema adherence                                                             | LoRA/QLoRA improves recurring behavior and format reliability                                                                                                   | B0 under the same inference contract                                 | Rare/version-specific facts, live-state observation, knowledge regressions, training cost                   |
| H1        | Multi-step interactive diagnosis/remediation in the controlled `kind` stratum                                                                                                                                                       | Orchestration, observation management, stopping, and verification improve end-to-end success under matched tools and budgets                                    | B0-I: B0 under the interactive observation form and neutral executor | Excess actions, unsafe actions, hidden information, latency                                                 |
| S1        | Procedural families whose reusable, non-answer-bearing skill matches the required workflow                                                                                                                                          | Versioned procedural context improves constraint adherence and reduces avoidable action errors beyond H1                                                        | H1                                                                   | Skill leakage, irrelevant-skill interference, context cost                                                  |
| C1        | Mixed families requiring both source evidence and structured response control                                                                                                                                                       | P1 plus R1 improves the complementary prompt-plus-retrieval failure profile                                                                                     | Stronger of P1 and R1                                                | Redundant context and cost without incremental gain                                                         |
| C2        | A mixed or interactive stratum frozen from model-independent family metadata before any pilot outcome: both constituent capabilities are required by the answer contract and distinct failure opportunities are declared in advance | The complete stack may improve over its strongest constituent when components address distinct preregistered failure opportunities; direction remains empirical | Predeclared strongest constituent under the frozen comparator rule   | Complexity, instability, cost, untraceable interactions; outcome-selected applicability is exploratory only |
| W1        | Official-source-searchable knowledge/mixed sensitivity subset                                                                                                                                                                       | Live official-source search changes performance or evidence behavior relative to B0/R1; no positive direction is required                                       | B0 and R1                                                            | Source drift, service variability, provenance failure, latency                                              |

Any combined harness-plus-web or harness-plus-RAG condition receives its own identifier, factor declaration, comparator, and approval. It is never reported as H1, R1, or W1 alone. A C2 stratum is admitted only from a pre-outcome metadata manifest and a design-time comparator rule; exhaustive combinations remain out of scope.

C2 eligibility and its comparator are frozen before any pilot output or error analysis. The eligibility manifest may use only model-independent family metadata (task class, language, answer contract, required constituent capabilities, declared evidence or interaction needs, and other design-time tags), plus a versioned design-time comparator rule. It may not use model scores, error counts, evaluator disagreement, or other outcome-derived evidence. If complementary failures are discovered through pilot error analysis and used to select a C2 stratum or comparator, that pilot C2 result is exploratory; a confirmatory C2 comparison requires a fresh, family-disjoint set of development families and a new frozen eligibility manifest.

## Metric and evaluator applicability

Each family freezes one answer contract across conditions. The pilot evaluates candidate outcomes but does not change a contract because a particular method failed.

| Task class | Candidate primary outcome for pilot                                     | Required deterministic layer                                                                   | Human layer when required                                    |
| ---------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Knowledge  | atomic-claim F1 on required and unsupported claims, normalized to [0,1] | format, citation/evidence identifier, answerability, and exact facts where applicable          | claim correctness/completeness and abstention quality        |
| Procedural | binary end-to-end task success                                          | parse/schema, prohibited action, required constraint, and static or cluster final-state checks | diagnosis quality only when success checks do not capture it |
| Mixed      | normalized task-specific score with procedural hard gates               | artifact/state success and evidence/citation checks                                            | atomic evidence-grounded decision rubric                     |

Lexical similarity is never a primary outcome. A malformed or prohibited output can fail a deterministic gate; a well-formed but wrong answer is a valid observation. Metrics that are not meaningful for a family are marked inapplicable rather than zero.

## Evaluator fixture and calibration design

### Fixture classes

Before model-derived pilot outputs are scored, each evaluator component receives versioned development fixtures covering **positive, negative, boundary, malformed, and ambiguous** cases. Fixture payloads are not benchmark families or final goldens. The repository package specifies their classes only; later construction keeps expected results in the development evaluator boundary.

Deterministic checks must achieve 100% expected outcomes, be idempotent across repeated execution, and emit an explicit reason code. An ambiguous fixture must be rejected for deterministic grading or routed to the named human criterion; it must not receive an arbitrary automated label.

### Human rubric

Rubrics are task-specific and use atomic criteria. Shared definitions may cover technical correctness, completeness, evidence support, constraint adherence, and relevance, but a universal overall-quality score is prohibited. Ordinal criteria use three anchored levels (`0`, `1`, `2`) with observable examples. Critical safety, answerability, and task-success decisions remain separate binary labels.

Raters see randomized response IDs, item inputs, permitted evidence, and the rubric, but not method, model, seed, prompt version, or other responses from the same condition. Identifying style can make blinding imperfect; suspected unblinding is recorded.

### Calibration sequence

1. Two technically competent raters independently score 12 calibration-training responses spanning task class, language, correct, incorrect, boundary, and malformed behavior.
2. They discuss disagreements, revise anchors, and freeze a candidate rubric version. Training responses are excluded from the reliability estimate.
3. They independently score a disjoint 24-response qualification set, balanced across task class and language.
4. Report per-criterion confusion tables, exact agreement, adjacent-category agreement for ordinal scales, and ordinal or nominal Krippendorff alpha with a family-clustered 95% bootstrap interval.
5. Qualification is green when every critical binary criterion has at least 90% exact agreement, the pooled primary rubric has alpha at least 0.80, and its lower 95% interval bound is at least 0.67. It is amber when the point estimate is 0.67–0.79 or a lower bound is below 0.67 without a critical systematic disagreement. It is red below 0.67 or after any unresolved systematic technical disagreement.
6. Amber triggers anchor revision and one new disjoint qualification set. Red triggers construct/rubric redesign. If a second qualification attempt is not green, the affected human metric becomes exploratory or is replaced by a narrower deterministic/atomic outcome before final freeze.

The numeric thresholds are conservative progression rules, not universal truths. Both point estimates and uncertainty are reported because agreement cut-offs without context can be misleading.

After qualification, all pilot responses receiving human primary scores are double-rated. For the larger final study, a stratified random 25% is double-rated and the remainder may be single-rated only after green calibration; the human researcher remains the primary rater. Any critical-label disagreement or ordinal disagreement larger than one level is adjudicated using written evidence. If two raters cannot resolve a critical case, a third technically competent adjudicator is requested; if unavailable, both labels and a conservative sensitivity analysis are retained.

An LLM judge is optional supporting evidence. It may be retained only with a frozen model/prompt/version, complete provenance, and comparison with adjudicated human labels in both languages. Failure to calibrate excludes it from confirmatory evidence and does not block deterministic or human evaluation.

## Controlled interactive `kind` stratum

### Scientific factor

The `kind` pilot tests whether bounded live observation and remediation add a valid procedural stratum. It does not turn the study into a general autonomous-agent benchmark.

Four of the eight procedural development families may receive static and interactive variants. Candidate fault classes are selector/service-port, probe, ConfigMap reference, scheduling, label/rollout, and Job configuration. The four selected families must cover both diagnosis and remediation; their content is not selected by observed method performance.

### Fair access

All applicable conditions receive the same neutral raw cluster-execution interface, command/action allowlist, namespace, initial state, action budget, timeout, and validator. `B0-I` denotes B0 under this interactive observation form; it is a nested observation label, not a new adaptation family. H1 differs from B0-I through orchestration, observation management, bounded working state, stopping, and verification—not exclusive access to the cluster or additional facts. S1 adds only its approved reusable procedural context.

The cluster protocol requires a version-pinned `kind` binary and node-image digest, preloaded pinned workload images, one isolated namespace per run, dummy credentials, no host mounts or privileged workloads, disabled external egress, deterministic recreate/reset, complete command/action capture, and automatic final-state validation. Read-only observation and namespaced remediation permissions are explicit; cluster-scoped mutation, secret exfiltration, arbitrary host/process access, and destructive commands are denied.

Static and interactive variants share a family ID. They preserve the same underlying fault and success criterion but differ in the observation channel. They are analyzed as nested variants, not independent evidence.

### Feasibility gate

The stratum is green only if:

- ten consecutive resets reproduce the declared initial-state hash and validator result;
- ten independent deny probes demonstrate that DNS and outbound HTTP(S) are unavailable from task workloads;
- allowed operations succeed and every denied operation fails in permission fixtures;
- the final-state validator is deterministic on positive, negative, boundary, malformed, and ambiguous fixtures;
- no condition has additional command permissions, action budget, or hidden observations;
- median reset plus validation time is at most three minutes on the target host, and no single attempt exceeds five minutes;
- all four families can be reviewed as semantically paired static/interactive variants.

Any isolation or privilege failure is red and blocks the stratum. Timing or reset instability is amber and permits one bounded redesign. If it is still not green, interactive tasks are excluded from confirmatory final evidence and the feasibility failure is reported; the static procedural families remain eligible.

## Official-source web-search sensitivity condition

W1 is separate from R1 and H1. R1 remains closed-corpus retrieval over the pinned canonical snapshot. H1 remains orchestration without open-web access. W1 tests the sensitivity of conclusions to a live official-source retrieval channel.

W1 is limited to allowlisted official Kubernetes documentation pages and matching `kubernetes/website` or `kubernetes/kubernetes` content. It cannot access this thesis repository, benchmark storage, item/golden endpoints, general web domains, cached benchmark text, or user-provided files. Redirects are rechecked against the allowlist.

Per response, W1 has at most three search calls, five returned results per search, two page fetches, five total tool calls, 4,000 extracted context tokens, and 120 seconds of tool wall time. Every query, result rank, URL, redirect, retrieval timestamp in UTC, response status, visible body snapshot or lawful hash/reference, content hash, tool/provider version where available, token count, rejection, and error is captured. The benchmark answer contract and evaluator remain unchanged.

Before a W1 run, a human source check confirms that the current official pages have not changed the answer contract relative to the pinned benchmark snapshot. A changed or unavailable page is a recorded sensitivity limitation, not permission to rewrite the item after seeing outputs.

W1 is green only when all attempted accesses have complete provenance, all redirects stay in the allowlist, no prohibited endpoint can be reached in deny fixtures, and at least 90% of eligible pilot attempts complete within the frozen budget. Provenance or access-control failure is red. Availability below 90% is amber and may lead to reporting W1 as exploratory. Search-service ranking remains a reproducibility limitation even with captured pages.

## Contamination controls and reporting

Contamination is reported in three distinct layers:

1. **Source/domain exposure:** public Kubernetes concepts or official source material may be present in pre-training. This risk is high in principle but unquantifiable for opaque corpora.
2. **Semantic-pattern exposure:** a model may have seen equivalent troubleshooting patterns, translated material, public questions, or code shapes even when text differs.
3. **Direct-item exposure:** newly authored private item inputs, evidence maps, and goldens are kept under controlled custody. Direct exposure should be low, but absence cannot be proven.

Before each freeze, exact, whitespace/comment-normalized, token n-gram, code/configuration-structure, embedding/semantic, and cross-language checks cover development, training, future final-test manifests, source chunks, prompts, examples, skills, harness text, tool fixtures, and captured tool outputs. Threshold candidates are calibrated on seeded positives and hard negatives; matches are human-adjudicated. Family and translation relationships override automated non-match decisions.

Fresh scenarios are authored after model/revision selection from the pinned source snapshot and use private custody, version-specific constraints, controlled counterfactuals, and negative/absent-answer cases. No numerical probability of pre-training contamination is assigned. Reports use factual labels such as `public-domain exposure expected`, `semantic overlap detected/not detected under method`, `direct overlap detected/not detected under method`, and `parametric exposure unknown`.

Any direct train/development/final overlap or golden leakage is red. The affected non-final material is replaced and the event logged without consulting final outcomes. Semantic matches are amber until adjudicated. Public-source exposure is a limitation, not an automatic exclusion.

## Pilot execution stages after approval

1. Freeze the source snapshot, pilot schema, evaluator version, budgets, and custody plan.
2. Construct evaluator fixtures and the 24 development families; perform human technical and licensing review.
3. Validate deterministic evaluators and qualify human raters without model output.
4. Implement only behavior approved by the `benchmark-pilot-evaluation-foundation` OpenSpec package and implementation gate.
5. Run B0 plus development-only positive/negative controls to measure solvability, headroom, evaluator sensitivity, runtime, and failure modes.
6. Admit each method only after its implementation-fidelity checks pass; exercise its preregistered target stratum and comparator without altering items to obtain a positive delta. For C2, validate the frozen metadata-only eligibility manifest and design-time comparator before reading outcomes; an outcome-selected pilot C2 is exploratory and cannot be confirmatory without fresh family-disjoint families.
7. Run the `kind` and W1 feasibility gates separately.
8. Produce a pilot decision report. Only then may Work propose final construction/freeze and the required software package.

## Pilot progression rules

Pilot decisions use `GO`, `AMEND`, or `STOP/DEFER`. Each criterion is judged separately and the worst safety, leakage, or evaluator-validity outcome governs progression.

| Criterion                   | GO                                                                                                           | AMEND                                                                           | STOP/DEFER                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Deterministic evaluation    | 100% fixture agreement and idempotence                                                                       | Correctable non-critical specification ambiguity before outputs                 | Any unexplained or post-output evaluator change                 |
| Human calibration           | Green thresholds above                                                                                       | One amber recalibration                                                         | Red or second non-green qualification                           |
| Solvability/evidence        | At least 90% of families independently judged solvable with complete evidence/validator mapping              | 80–89% or localized ambiguity                                                   | Below 80% or construct mismatch                                 |
| Headroom                    | B0 family success lies between 20% and 80% overall and each target stratum contains both success and failure | One stratum outside range but evaluator positive/negative controls discriminate | Ceiling/floor cannot be repaired without changing the construct |
| Invalid output rate         | At most 5% infrastructure/evaluator invalidity                                                               | Above 5% and at most 10% with identified fix                                    | Above 10% or condition-dependent invalidation                   |
| Condition fidelity/fairness | 100% required provenance and matched declared controls                                                       | Non-outcome-informed implementation correction                                  | Hidden information, unequal permissions, or uncaptured mutation |
| Contamination               | No direct leakage; semantic matches adjudicated                                                              | Unresolved semantic matches                                                     | Direct item/golden exposure                                     |
| `kind`                      | All feasibility checks green                                                                                 | One bounded redesign                                                            | Isolation/privilege failure or repeated non-green result        |
| W1                          | All provenance/access checks and at least 90% completion                                                     | Availability/reproducibility limitation                                         | Prohibited access or missing provenance                         |
| Researcher feasibility      | Projected final construction, rating, and compute fit the pre-freeze time/compute cap with 20% contingency   | Scope reduction that preserves all primary strata                               | Required work exceeds cap or needs unavailable raters/hardware  |

The pilot cannot replace or select final tasks based on which method wins. Changes must trace to ambiguity, unsolvability, missing evidence, evaluator failure, ceiling/floor, implementation infidelity, contamination, or infeasibility. Every excluded family and reason remains in the decision log.

## Repetition, paraphrase, and final-size selection

The pilot uses five stochastic generations on a balanced six-family stability subset (one family per task-class/language cell) and three frozen semantic formulations per selected family. Formulations preserve intent, constraints, evidence, and answer form and are human-reviewed before execution.

The final stability study uses five generations and three formulations by default. Increase generations to seven only when the pilot estimates a Monte Carlo standard error above 0.05 on the normalized primary score in more than 20% of applicable family-condition cells and the predeclared compute cap still fits. Repeats never substitute for independent families.

Final independent-family counts are selected by simulation using pilot nuisance estimates (baseline rate/variance, paired correlation, family heterogeneity, missingness) and the smallest effects of interest below. Target power is 80% for the small primary contrast family at two-sided alpha 0.05 after Holm adjustment. The construction cap is 60 final families: 20 per task class and 10 per language within class. If the target is underpowered at that cap, the study reports estimation with reduced confirmatory claims; it does not add repeats, inspect final outcomes, or lower the effect threshold to manufacture power.

## Statistical decision rules

### Estimands and smallest effects of interest

The primary estimand is the paired difference between a condition and its preregistered comparator in the mean family-level primary outcome within the method's target stratum. Pilot candidate smallest effects of interest (SESOI) are:

- knowledge: +0.10 absolute atomic-claim F1;
- procedural: +0.15 absolute end-to-end success probability;
- mixed: +0.10 absolute normalized task score.

These values represent changes worth discussing for a small local system. The pilot may raise a threshold or reject a metric when measurement error makes it indefensible; it may not lower a threshold based on observed method deltas. Final SESOIs are frozen before final-family construction.

### Primary analysis

- Aggregate repeats, formulations, language variants, and static/interactive variants within family before treating families as independent.
- Report paired absolute differences and 95% confidence intervals from a task/language-stratified cluster bootstrap resampling families with 10,000 draws.
- For the small confirmatory contrast family, report paired randomization-test p-values with Holm correction within task class. Intervals and effect sizes remain primary; p-values do not determine scientific value alone.
- Fit outcome-appropriate mixed-effects models with family random intercepts as sensitivity analyses for nested observations. A failed or singular fit is reported and does not replace the family-level analysis.
- Report target-stratum and complete-applicable-benchmark deltas from B0, plus language/task interactions, invalidity, cost, latency, stability, and regressions. Interaction estimates are exploratory unless separately powered.
- Compare C1 with the strongest frozen constituent. For C2, use only the metadata-frozen eligibility manifest and design-time comparator for confirmatory inference; any error-analysis-selected pilot C2 is exploratory and requires fresh family-disjoint families for confirmation. Compare S1 with H1. Decompose R1 retrieval and answer errors. Keep W1 labeled sensitivity evidence.

### Interpretation categories

| Result                                   | Rule                                                                   |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| Clear practical benefit                  | Estimate reaches the positive SESOI and the 95% interval excludes zero |
| Promising but uncertain                  | Estimate reaches the SESOI but the interval includes zero              |
| Detectable but below practical threshold | Interval excludes zero but estimate does not reach the SESOI           |
| Inconclusive                             | Interval includes both zero and the positive SESOI                     |
| Clear regression                         | Upper 95% interval bound is below zero                                 |

Zero, negative, or inconclusive effects remain valid results. No task is replaced, no metric is reweighted, and no condition is repeatedly tuned because it failed to improve.

## Invalid and missing observations

Corrupted capture, missing required provenance, hash mismatch, evaluator infrastructure failure, or declared hardware-measurement failure makes a run invalid. Model refusal, malformed model output, tool-budget exhaustion, timeout caused by the evaluated system, failed remediation, and backend failure that is part of the deployed condition are valid failures. Invalid records remain append-only and are reported by condition. Exclusion-sensitive conclusions receive an all-fail and complete-case sensitivity bound.

## Decision-package outcome

This proposal selects a 24-family development pilot, mechanism-aligned target strata, separate controlled `kind` and W1 sensitivity gates, explicit contamination layers, calibrated evaluator rules, progression thresholds, repetition selection, a 60-family final construction cap, and estimation-first statistical decisions.

The accompanying `benchmark-pilot-evaluation-foundation` OpenSpec change specifies four bounded capabilities: pilot metadata/custody, evaluation/calibration, controlled cluster instrumentation, and W1 access/capture. It deliberately excludes model inference, benchmark/fixture payloads, final-test content, and real external execution in routine tests. Human Gate A approval is required before Codex implementation.

## Evidence basis

- Dror et al., [The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing](https://aclanthology.org/P18-1128/), motivate test selection that respects paired NLP evaluation structure.
- Card et al., [With Little Power Comes Great Responsibility](https://aclanthology.org/2020.emnlp-main.745/), show that NLP comparisons and human-rating studies are commonly underpowered and support explicit power analysis.
- Zapf et al., [Measuring inter-rater reliability for nominal data](https://doi.org/10.1186/s12874-016-0200-9), support Krippendorff alpha and bootstrap uncertainty, especially beyond complete nominal ratings.
- Beckler et al., [Reliability in evaluator-based tests](https://doi.org/10.1186/s12874-018-0606-7), caution that generic agreement thresholds are context-dependent.
- Howcroft et al., [Twenty Years of Confusion in Human Evaluation](https://aclanthology.org/2020.inlg-1.23/), support explicit construct definitions and complete human-evaluation reporting.
- Lewis et al., [Determining sample size for progression criteria for pragmatic pilot RCTs](https://doi.org/10.1186/s40814-021-00770-x), provide the transferable stop/amend/go principle for feasibility criteria; this protocol does not import clinical-effect testing.
- Yang et al., [Rethinking Benchmark and Contamination for Language Models with Rephrased Samples](https://arxiv.org/abs/2311.04850), and Yao et al., [Data Contamination Can Cross Language Barriers](https://arxiv.org/abs/2406.13236), show why exact matching cannot rule out paraphrased or translated exposure.
- Rajore et al., [TRUCE](https://arxiv.org/abs/2403.00393), motivate private test custody while acknowledging that privacy does not itself establish benchmark quality.
- Official [`kind` documentation](https://kind.sigs.k8s.io/docs/user/quick-start/) and the Kubernetes [NetworkPolicy documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/) ground the proposed versioning and egress-feasibility checks; implementation may choose the smallest host/container mechanism that demonstrably satisfies the OpenSpec deny probes.
