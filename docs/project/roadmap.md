# Project Roadmap

The roadmap is evidence-driven. Near-term work is detailed; later milestones remain coarse until preceding experiments justify them.

GitHub milestone and label conventions are defined in [github-management.md](github-management.md).

## Milestones

| ID | Milestone | Exit condition |
|---|---|---|
| M0 | Research & Project Foundation | Governance, feasibility review, architecture, initial ADRs, OpenSpec bootstrap, and first approved implementation package |
| M1 | Benchmark Dataset and Evaluation Foundation | Task taxonomy, data sources, split protocol, golden process, evaluator versioning, contamination audit, and pilot dataset are approved |
| M2 | Local Model Inference Baseline | Frozen primary model runs reproducibly through `llama.cpp` on target hardware with telemetry and B0 results |
| M3 | Prompt Engineering Experiments | P1/P2 are frozen and compared without test-set tuning |
| M4 | Retrieval-Augmented Generation | Retrieval corpus and simple baseline are frozen; retrieval and answer metrics are reported |
| M5 | Fine-Tuning / QLoRA | One justified training pipeline produces a locally evaluated adapter or model with adaptation-cost accounting |
| M6 | Model Harness | H1 is defined as an explicit controlled condition and evaluated on procedural tasks |
| M7 | Skill-Based Adaptation | S1 isolates reusable procedural context from harness-only behavior |
| M8 | Stability and Combined Experiments | Repeated runs, paraphrases, C1, and a metadata-frozen C2 (or exploratory-only C2 followed by fresh confirmatory families) are analyzed |
| M9 | Secondary Model Replication | Selected effects are replicated on the frozen second family |
| M10 | Statistical Analysis | Pre-specified analyses, uncertainty intervals, sensitivity checks, tables, and figures are reproducible |
| M11 | Thesis Results and Discussion | Validated results, limitations, and conclusions are integrated into the Polish thesis |
| M12 | Reproducibility and Final Audit | Independent reproduction checklist, artifact audit, citation audit, GenAI declaration, and final build pass |

## Completed milestone: M0

The provenance-only foundation for Issue [#1](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/1) was independently reviewed, merged in PR [#18](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/18), and archived. Its canonical software specifications are under `openspec/specs/`.

## Immediate backlog: M1

1. The Issue [#2](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/2) benchmark-domain package was approved, merged in PR [#22](https://github.com/Nasus20202/local-llm-adaptation-thesis/pull/22), and closed.
2. Review the Issue [#4](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/4) pilot/evaluator methodology and `benchmark-pilot-evaluation-foundation` OpenSpec package at Human Gate A.
3. After approval, implement only the synthetic validation/evaluation/tool-boundary foundation; do not construct pilot payloads or run real clusters, web tools, or models in that implementation cycle.
4. Separately authorize development-only pilot/fixture construction and empirical qualification after the software foundation is reviewed and merged.
5. Run [target-hardware candidate smoke tests](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/5).
6. [Import and verify the official WETI template](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/3).
7. Decide the public licensing plan before making the private repository public.

## Next milestone: M1

M1 next validates task families, metrics, annotation, evaluator calibration, contamination checks, and the separately gated `kind`/W1 strata on development-only material. Final-test construction and freeze remain separate approvals.

- [Benchmark domain and construction decision](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/2)
- [Benchmark pilot and evaluator calibration protocol](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/4)

## Later tracking issues

| Milestone | Tracking issue |
|---|---|
| M2 | [Local inference baseline](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/8) |
| M3 | [Prompt-engineering experiments](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/11) |
| M4 | [Retrieval baseline](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/10) |
| M5 | [QLoRA adaptation](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/6) |
| M6 | [Model harness](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/7) |
| M7 | [Reusable skills](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/12) |
| M8 | Stability and Combined Experiments | Repeated runs, paraphrases, C1, and a metadata-frozen C2 (or exploratory-only C2 followed by fresh confirmatory families) are analyzed |
| M9 | [Secondary-model replication](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/13) |
| M10 | [Statistical analysis](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/14) |
| M11 | [Polish thesis results and discussion](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/15) |
| M12 | [Reproducibility and final audit](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/16) |

## Dependency principles

- M2 depends on M1 interfaces and the M0 runner foundation, not on a complete final dataset.
- Method milestones depend on a frozen baseline and evaluator version.
- Combined experiments start only after individual conditions produce interpretable evidence.
- Secondary replication targets selected findings; it does not repeat every development iteration.
- Thesis results are generated from validated analysis artifacts, never transcribed from ad hoc notebooks.

## Change control

Milestone names are stable planning anchors, not a waterfall commitment. Exit criteria or ordering may change through an ADR and human approval when empirical evidence requires it. The official thesis objective does not change.
