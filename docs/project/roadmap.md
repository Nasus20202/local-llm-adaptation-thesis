# Project Roadmap

The roadmap is evidence-driven. Near-term work is detailed; later milestones remain coarse until preceding experiments justify them.

GitHub milestone and label conventions are defined in [github-management.md](github-management.md).

## Milestones

| ID  | Milestone                                   | Exit condition                                                                                                                         |
| --- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| M0  | Research & Project Foundation               | Governance, feasibility review, architecture, initial ADRs, OpenSpec bootstrap, and first approved implementation package              |
| M1  | Benchmark Dataset and Evaluation Foundation | Task taxonomy, data sources, split protocol, golden process, evaluator versioning, contamination audit, and pilot dataset are approved |
| M2  | Local Model Inference Baseline              | Frozen primary model runs reproducibly through `llama.cpp` on target hardware with telemetry and B0 results                            |
| M3  | Prompt Engineering Experiments              | P1/P2 are frozen and compared without test-set tuning                                                                                  |
| M4  | Retrieval-Augmented Generation              | Retrieval corpus and simple baseline are frozen; retrieval and answer metrics are reported                                             |
| M5  | Fine-Tuning / QLoRA                         | One justified training pipeline produces a locally evaluated adapter or model with adaptation-cost accounting                          |
| M6  | Model Harness                               | H1 is defined as an explicit controlled condition and evaluated on procedural tasks                                                    |
| M7  | Skill-Based Adaptation                      | S1 isolates reusable procedural context from harness-only behavior                                                                     |
| M8  | Stability and Combined Experiments          | Repeated runs, paraphrases, C1, and a metadata-frozen C2 (or exploratory-only C2 followed by fresh confirmatory families) are analyzed |
| M9  | Secondary Model Replication                 | Selected effects are replicated on the frozen second family                                                                            |
| M10 | Statistical Analysis                        | Pre-specified analyses, uncertainty intervals, sensitivity checks, tables, and figures are reproducible                                |
| M11 | Thesis Results and Discussion               | Validated results, limitations, and conclusions are integrated into the Polish thesis                                                  |
| M12 | Reproducibility and Final Audit             | Independent reproduction checklist, artifact audit, citation audit, GenAI declaration, and final build pass                            |

## Completed milestone: M0

The provenance-only foundation for Issue [#1](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/1) was independently reviewed, merged in PR [#18](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/18), and archived. Its canonical software specifications are under `openspec/specs/`.

## Immediate backlog: M1

1. The Issue [#2](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/2) benchmark-domain package was approved, merged in PR [#22](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/22), and closed.
2. The Issue [#4](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/4) pilot/evaluator protocol was approved and merged in [PR #25](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/25).
3. Its bounded synthetic pilot/evaluator, controlled-cluster, and W1 software foundations were implemented, independently reviewed, and merged in [PR #33](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/33). The canonical specifications are synchronized and the completed changes archived.
4. [Issue #35](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/35) is active. Its focused authorization package was merged in PR #38; the exact Kubernetes `v1.36.4` [source/release rights manifest](../research/development-pilot-source-rights-manifest.md) was approved and merged in PR #40; the [pre-authoring custody and metadata freeze](../research/development-pilot-preauthoring-freeze.md) was approved and merged in PR #42; the 24 development-only model-facing scenario inputs were human-approved and squash-merged in PR #44; Human Gate A approved the protected evaluator scientific/OpenSpec contract in PR #47, squash-merged as `028eb9453cfb3ae1c90537104a6dfa6922acd7dc`; and the resulting generic protected-evaluator implementation was independently reviewed and squash-merged in PR #50 as `23e1f559eab24b755402cdb738572c359eeed167`. The completed OpenSpec change is synchronized into the canonical specifications and archived.
5. **Current step:** prepare and review the 24 protected evaluator bundles under `development-protected-evaluator-v1`, preserving the approved scenario bindings, Kubernetes v1.36.4 source-evidence rules, evaluator hierarchy, class-specific metrics, copying-neutral fairness requirements, custody boundaries, and append-only provenance.
6. After the protected bundles are reviewed/frozen as required, prepare a separate semantic-judge freeze: exact model/provider or artifact identity, backend/version, prompt/template hash, response schema, decoding/retry behavior, protected input contract, predeclared human-agreement/fairness thresholds, blinded audit sample/policy, and suspension/requalification rules. Human approval is required before any judge-model execution.
7. Execute judge qualification only after that approval. A judge that fails any required threshold remains ineligible for primary semantic dispositions; unresolved criteria use the calibrated human route or fail closed. Participant-model scoring remains separately gated.
8. Run [target-hardware candidate smoke tests](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/5) only when the M1/M2 sequencing gate authorizes them.
9. Decide the public licensing plan through [Issue #36](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/36) before making the repository public if that decision has not already been completed.

## Next milestone: M1

M1 next prepares and reviews the 24 protected evaluator bundles under `development-protected-evaluator-v1`. A later separate gate freezes and qualifies the semantic judge against protected human labels while preserving calibrated human adjudication/audit for residual cases. Participant-model execution follows only through a later focused authorization. Real `kind`, live W1, training, outcome-selected C2, formal experiments, and final-test construction/freeze remain separate approvals.

- [Benchmark domain and construction decision](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/2)
- [Benchmark pilot and evaluator calibration protocol](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/4)
- [Development-only pilot construction authorization](../research/development-pilot-authorization.md)
- [Development-pilot pre-authoring custody and metadata freeze](../research/development-pilot-preauthoring-freeze.md)
- [Protected development evaluator design](../research/development-pilot-protected-evaluator-design.md)

## Later tracking issues

| Milestone | Tracking issue                                                                                                |
| --------- | ------------------------------------------------------------------------------------------------------------- |
| M2        | [Local inference baseline](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/8)                |
| M3        | [Prompt-engineering experiments](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/11)         |
| M4        | [Retrieval baseline](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/10)                     |
| M5        | [QLoRA adaptation](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/6)                        |
| M6        | [Model harness](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/7)                           |
| M7        | [Reusable skills](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/12)                        |
| M8        | Stability and Combined Experiments                                                                            |
| M9        | [Secondary-model replication](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/13)            |
| M10       | [Statistical analysis](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/14)                   |
| M11       | [Polish thesis results and discussion](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/15)   |
| M12       | [Reproducibility and final thesis audit](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/16) |

## Dependency principles

- M2 depends on M1 interfaces and the M0 runner foundation, not on a complete final dataset.
- Method milestones depend on a frozen baseline and evaluator version.
- Any primary semantic judge is part of the evaluator version and must be frozen/qualified against protected human labels before participant-model scoring.
- Deterministic verification takes precedence over semantic judging whenever the task construct permits it.
- Human audit/adjudication is predeclared and blinded; it is not selected post hoc from surprising condition outcomes.
- Combined experiments start only after individual conditions produce interpretable evidence.
- Secondary replication targets selected findings; it does not repeat every development iteration.
- Thesis results are generated from validated analysis artifacts, never transcribed from ad hoc notebooks.

## Change control

Milestone names are stable planning anchors, not a waterfall commitment. Exit criteria or ordering may change through an ADR and human approval when empirical evidence requires it. The official thesis objective does not change.
