# Experimental Design

## Design overview

Use a blocked, within-family comparison on one primary model. Each benchmark family is evaluated under applicable adaptation conditions; task class and language are predeclared strata, and method is the principal independent variable. The secondary model repeats only pre-registered contrasts.

The proposed [development-only benchmark pilot](benchmark-pilot-protocol.md) establishes feasibility and evaluator calibration before final construction. Pilot data cannot support thesis effectiveness claims or final-item selection based on method performance.

## Analysis unit

The scenario/item family is the principal independent unit. Repeated generations, semantic prompt formulations, Polish/English variants, and static/interactive variants are nested observations and do not increase the independent sample size.

## Variables

### Independent variables

- adaptation condition: B0, P1, P2, R1, F1, H1, S1, C1, or C2 when applicable;
- W1 only as a separately governed official-source web sensitivity condition;
- task class: knowledge, procedural, mixed;
- benchmark language: Polish or English;
- observation form: static or interactive only in the controlled `kind` subset;
- prompt formulation: canonical plus frozen semantic paraphrases for the stability study;
- repeated-generation seed or sample index;
- model family only in the selected replication stage.

### Dependent variables

- correctness and task success;
- task-specific precision, constraint adherence, and schema validity;
- factuality, groundedness, evidence correctness, retrieval success, and abstention where applicable;
- action validity, action count, tool-budget use, and final-state success for interactive tasks;
- repeated-run, paraphrase, selected cross-language, and selected static/interactive stability;
- TTFT, latency, throughput, token counts, peak RAM or VRAM, load time, and tool time;
- training duration, accelerator, peak memory, tokens or examples, and adapter or export size;
- recorded engineering effort and configuration complexity using a pre-defined rubric.

### Controlled variables

- model repository, revision, artifact hash, and quantization;
- inference backend build, container digest, and hardware/software environment;
- chat template, thinking policy, generation parameters, and maximum output;
- benchmark revision, split, evaluator version, and golden hash;
- condition-specific prompt, RAG, skill, harness, cluster, and web-policy revisions;
- source-document identity across language strata in the primary RAG condition;
- answer contract across compared conditions;
- cluster initial state, interface, permissions, action/time budget, and validator across interactive conditions;
- W1 allowlist, search/fetch budget, capture policy, and pre-run source check;
- warm-up policy, timing boundary, concurrency, and background-load policy.

## Preregistered applicability

| Task class/stratum     | Required core contrasts                         | Optional justified contrasts                                                                                                                                        |
| ---------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Knowledge              | B0, P1, R1, F1                                  | P2, C1, W1 sensitivity                                                                                                                                              |
| Static procedural      | B0, P1, S1 with H1 constituent where applicable | P2, F1 when training target matches                                                                                                                                 |
| Interactive procedural | B0-I (B0 with the neutral interface), H1, S1    | F1 only when target matches; explicit combined condition                                                                                                            |
| Mixed                  | B0 and strongest simple conditions              | C1; one C2 only with metadata-frozen eligibility and comparator; error-analysis-selected C2 is exploratory and requires fresh confirmatory families; W1 sensitivity |

The detailed hypothesis matrix defines target strata and comparators. C2 applicability and its comparator are frozen from model-independent metadata and a design-time rule before any pilot outcome; pilot error analysis cannot authorize a confirmatory C2 stratum. An error-analysis-selected C2 pilot is exploratory and requires fresh, family-disjoint development families for confirmation. Inapplicable methods are not scored as failures. Pairwise combinations are not generated automatically.

## Language design

Independent families are allocated equally between Polish and English within each task class. Items are natively authored or human-adapted; unreviewed automatic translations are excluded.

A predeclared paired subset may present the same semantic task in both languages. Both variants remain in one split and are analyzed within family. Primary method effects do not count them as independent examples. Language interactions are reported with uncertainty and are not generalized beyond the selected domain.

## Controlled interactive design

Up to four procedural development families receive paired static and `kind` variants. The interactive environment uses a version-pinned node image and workloads, isolated namespace, dummy credentials, disabled external egress, explicit permissions, deterministic reset, complete action capture, and automatic final-state validation.

Every applicable condition receives the same neutral raw cluster interface and budget. B0-I labels the nested interactive form of B0 rather than a new adaptation family. H1 changes orchestration, observation management, stopping, and verification; it does not grant exclusive tools or knowledge. The interactive stratum enters final confirmatory evidence only after all feasibility checks pass.

## Web-search sensitivity design

W1 is neither the R1 closed corpus nor the H1 harness. It is an official-source-only live-web sensitivity condition with a fixed allowlist, search/fetch/token/time budgets, redirect enforcement, complete query/result/body provenance, and repository/benchmark denial controls. Any harness-plus-web or harness-plus-RAG condition is separately named and approved.

## Run structure

1. Freeze all inputs in an experiment manifest.
2. Execute a small non-test smoke set to validate configuration, access controls, evaluator, and telemetry.
3. Randomize or counterbalance condition execution order within hardware blocks.
4. Warm the model or runtime according to a fixed protocol; exclude warm-up from quality but record it.
5. Reset interactive state and verify the declared initial state before each applicable run.
6. Save every raw request, response, retrieval, tool action, timing event, exit status, and validity flag.
7. Evaluate without exposing golden answers to the generator or external service.
8. Produce a new run for retries; never overwrite.

## Repetition and stability

The pilot uses five stochastic samples and three semantic formulations on a balanced six-family subset. The final default remains five samples and three formulations; seven samples are allowed only under the predeclared Monte Carlo-error and compute-budget rule. Repeats and formulations remain nested within families.

## Fairness and context

Primary comparison uses each method's necessary context and reports its token and cost consequence. A context-budget-matched sensitivity analysis is used where truncation does not destroy the method definition. RAG receives the same source corpus across language variants. Harnesses, skills, web tools, and cluster tools cannot access goldens or evaluator logic.

## Invalid runs

Validity rules freeze before execution. Corrupted capture, missing provenance, hash mismatch, or evaluator/required-telemetry infrastructure failure is invalid. Semantically wrong output, refusal, malformed response, tool-budget exhaustion, evaluated-system timeout, failed remediation, or deployed runtime failure is valid evidence of task failure.

## Pilot and freeze decisions

The pilot uses explicit `GO`, `AMEND`, and `STOP/DEFER` criteria for evaluator reliability, solvability, headroom, invalidity, fairness, contamination, `kind`, W1, and researcher feasibility. Final item count is selected by simulation and capped at 60 independent families. Underpowered contrasts are reported as estimation rather than repaired with repeats or favorable task selection.

No final family, primary outcome, sampling policy, or condition is frozen by this unapproved proposal. Human Gate A must first approve the protocol; later development evidence and a separate freeze decision establish immutable values.
