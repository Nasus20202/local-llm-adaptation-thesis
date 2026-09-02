# ADR-0008: Benchmark Domain and Language Policy

- **Status:** Accepted
- **Date:** 2026-09-02
- **Decision owner:** Human researcher

## Context

Issue #2 must select a domain, language balance, source strategy, construction policy, and independent unit before any benchmark item is created. The domain must support knowledge, procedural, and mixed tasks without giving one adaptation family privileged access to answers.

## Considered alternatives

1. One coherent Kubernetes workload domain.
2. Two smaller technical domains.
3. A fully synthetic technical world.

Language alternatives were Polish-only, uncontrolled bilingual composition, Polish-majority composition, and an equal Polish/English allocation.

## Proposed decision

Use one version-pinned domain: Kubernetes application-workload configuration and troubleshooting for an intermediate application or platform engineer.

Allocate independent scenario families equally between Polish and English within each task class. Polish items are natively authored or human-adapted; unreviewed machine translations are prohibited. Semantically parallel language variants share one family and split and are not independent samples.

Use official Kubernetes documentation and matching API artifacts under their upstream licenses. Keep the same canonical English source snapshot as the primary RAG corpus for both benchmark languages. Treat a translated corpus as a separately approved sensitivity condition.

Construct fresh source-transformed scenarios and controlled configurations with human technical verification. Use the scenario/item family as the independent unit. Keep final-test inputs and goldens sealed from all development conditions and AI-accessible workspaces.

## Rationale

A single domain maximizes internal validity, reuses terminology across task classes, and is feasible for one MSc researcher. Kubernetes provides lawful version-controlled factual documentation, explicit procedures, and machine-checkable configuration semantics. Equal language allocation makes language a planned stratum rather than an incidental imbalance while preserving relevance to Polish practitioners and canonical English technical material.

A second domain would materially increase curation and confound task-class effects with domain. A fully synthetic world would reduce ecological validity and weaken claims about real technical adaptation. Controlled synthetic configurations inside the real domain provide a narrower compromise.

## Consequences

- Conclusions are limited to the selected Kubernetes workload scope and local execution setting.
- Public-source pretraining exposure cannot be ruled out and must be reported.
- Translation and language variants require human equivalence review and clustered analysis.
- Source snapshots need license, attribution, commit, release, path, and hash manifests.
- Issue #4 must determine item counts, detailed metrics, annotation thresholds, evaluator calibration, and pilot acceptance rules.
- No OpenSpec change is created by this ADR because it defines research methodology, not software behavior. Dataset or evaluator software receives a separate OpenSpec package after this decision is approved.

## Approval record

Human Gate A was approved by the human researcher on 2026-09-02. The approval authorizes preparation of the Issue #4 pilot and evaluator-calibration protocol only. It does not authorize benchmark-item construction, dataset or evaluator implementation, model execution, or final-test access.
