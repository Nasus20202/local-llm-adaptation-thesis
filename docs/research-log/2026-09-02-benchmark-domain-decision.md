# Research Log: Benchmark Domain Decision

- **Date:** 2026-09-02
- **Issue:** [#2](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/2)
- **Status:** Accepted at Human Gate A on 2026-09-02

## Question

Which bounded domain, language policy, source strategy, construction method, and custody rules permit a fair comparison of adaptation families on local models?

## Alternatives reviewed

A single Kubernetes workload domain, two technical domains, and a synthetic controlled world were compared against internal validity, ecological validity, task-class coverage, licensing, contamination risk, deterministic evaluation, and one-researcher feasibility.

## Evidence

Primary project and source evidence:

- Kubernetes website content is version-controlled and licensed under [CC BY 4.0](https://github.com/kubernetes/website/blob/main/LICENSE).
- Kubernetes source and API artifacts use [Apache-2.0](https://github.com/kubernetes/kubernetes/blob/master/LICENSE).
- Upstream documentation explicitly separates [concepts, tasks, and references](https://kubernetes.io/docs/home/), and task pages describe short operational procedures in the [Tasks section](https://kubernetes.io/docs/tasks/).
- Kubernetes exposes version-specific [OpenAPI schemas](https://kubernetes.io/docs/concepts/overview/kubernetes-api/) suitable for deterministic structural checks, while also warning that schemas are not complete substitutes for server validation.
- Localization is maintained from specific English sources and requires human review; machine translation alone is insufficient under the [localization policy](https://kubernetes.io/docs/contribute/localization/).
- Supported documentation and behavior change across releases, requiring an exact snapshot and compatible release metadata under the [version-skew policy](https://kubernetes.io/releases/version-skew-policy/).

Methodological evidence:

- Yang et al., [Rethinking Benchmark and Contamination for Language Models with Rephrased Samples](https://arxiv.org/abs/2311.04850), show that n-gram checks miss paraphrased and translated overlap and recommend fresher evaluations.
- Yao et al., [Data Contamination Can Cross Language Barriers](https://arxiv.org/abs/2406.13236), show that cross-language exposure can inflate results while evading common detection methods.
- Plaza et al., [Spanish and LLM Benchmarks: is MMLU Lost in Translation?](https://arxiv.org/abs/2406.17789), show that automatic translation errors can distort multilingual benchmark outcomes and argue for expert review or language adaptation.

## Interpretation

Kubernetes workload configuration and troubleshooting is the smallest coherent domain found that supports all required task classes with lawful, versioned sources and deterministic checks. The canonical English corpus should remain constant across language strata to avoid hidden information-access changes. Equal Polish/English family allocation supports planned language analysis without treating translations as independent evidence.

## Limitations

Public documentation may exist in model pretraining, exact snapshot licensing still requires path-level review, and offline tasks do not reproduce all live-cluster behavior. The pilot must determine whether the selected scope produces sufficient difficulty, evaluator agreement, and corpus coverage.
