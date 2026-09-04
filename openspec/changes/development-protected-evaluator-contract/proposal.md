## Why

PR #44 froze and human-approved the 24 development-only model-facing scenario inputs, but the canonical evaluator specifications still stop at generic evaluator identity, fixture classes, rubric calibration, and protected-content separation. A later implementation would otherwise have to invent how semantic claims, exact technical constraints, mixed-task hard gates, source evidence, semantic-assessor qualification, and anti-copying qualification fit together.

The protected evaluator must therefore be specified before Codex implementation so that scoring remains semantically fair, source-bound to Kubernetes v1.36.4, reproducible, and isolated from every participant-model-facing or future-training path.

## What Changes

- Define the protected per-family semantic answer-contract interface: required atomic claims, accepted semantic alternatives, unsupported/contradictory claims, construct-critical exact requirements, deterministic gates, task-specific semantic criteria, evidence mappings, and immutable identities.
- Define a strict assessment hierarchy: deterministic verification whenever the construct is mechanically decidable; a separately frozen and human-qualified LLM judge only for residual semantic criteria; calibrated human adjudication for unresolved/disputed cases plus a predeclared blinded audit sample.
- Keep the score kernel deterministic and independent of lexical similarity, embeddings, judge confidence, or prose resemblance. The judge may produce structured criterion dispositions only; it does not choose metric weights or task scores.
- Require any primary semantic judge to freeze its exact model/backend identity, prompt/template hash, response schema, decoding/retry configuration, qualification fixture identity, acceptance thresholds, and audit policy before judge execution.
- Require judge qualification against protected human-labelled criterion fixtures, including criterion-level agreement/confusion evidence and copying-neutral metamorphic tests. An unqualified judge cannot issue primary dispositions.
- Add metamorphic fairness invariants that make source-like wording, paraphrase, synonyms, and reordering score equivalently while technically wrong or incomplete copied answers score worse on affected criteria.
- Bind protected evaluator artifacts to the approved scenario-input hashes and frozen Kubernetes v1.36.4 source identities, with fail-closed custody and safe public references.
- Keep all answer-bearing per-scenario evaluator payloads outside the normal repository/model-facing checkout. This change defines how those payloads must later be instantiated; it does not author them.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `evaluation-protocol`: protected semantic contracts, hierarchical criterion assessment, qualified semantic-judge records, class-specific score derivation, human adjudication/audit routing, and semantic-fairness qualification.
- `benchmark-pilot-dataset`: approved-input/source binding, protected evidence-map provenance, safe protected references, and immutable protected-artifact lineage.

## Impact

After Human Gate A, Codex may extend the existing `thesis_bench.evaluation` and `thesis_bench.pilot` foundations with the minimum typed schemas, deterministic scoring, model-agnostic semantic-assessment/qualification records, protected-root loading boundary, provenance validation, adjudication routing, and synthetic tests required by this change.

This Gate A does not select or run a real LLM judge. Exact judge selection/configuration, human-labelled qualification thresholds, audit policy, and any judge-model execution require a later explicit freeze/approval. This planning change also does not author Kubernetes answer contracts or fixture payloads, run participant models, construct training/final-test material, enable `kind`, W1, C2, or semantic-pair strata, or change any approved scenario input, source, condition, comparator, metric family, or calibration threshold.
