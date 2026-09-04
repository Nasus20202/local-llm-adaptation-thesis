# Development-pilot Protected Evaluator Design

## Status and boundary

The 24 development-only scenario inputs were human-approved and squash-merged in PR #44. The next Issue #35 step is to define the evaluator that can later score those scenarios without leaking answer truth or rewarding documentation-like wording.

This document explains the scientific design for review. The normative software behavior is the active OpenSpec change `development-protected-evaluator-contract`. No production evaluator, protected Kubernetes answer payload, participant-model output, training material, final-test material, real `kind` task, or live W1 access is created here.

The approved metric families do not change:

| Task class | Primary outcome                                           |
| ---------- | --------------------------------------------------------- |
| Knowledge  | atomic-claim F1                                           |
| Procedural | binary end-to-end task success                            |
| Mixed      | normalized task-specific score with procedural hard gates |

For reusable definitions of atomic claims, F1, semantic scoring, deterministic evaluators, rubrics, metamorphic fairness fixtures, and calibration statistics, see the [glossary](../glossary.md). The broader method remains in the [evaluation strategy](evaluation.md) and [development-pilot protocol](benchmark-pilot-protocol.md).

## Three layers that must stay separate

### Scientific specification — committed now

The specification defines the shape and invariants of a protected per-scenario contract: atomic criteria, exact construct-critical checks, score derivation, semantic-assessor routing, judge qualification, human adjudication/audit, source evidence identity, anti-copying qualification, custody, hashes, and provenance.

It deliberately does **not** state the correct Kubernetes answer to any of the 24 questions.

### Protected content — instantiated later

Each approved family will later receive a protected bundle under `development-protected-evaluator-v1`. Depending on the task, the bundle contains the required claims, accepted semantic alternatives, unsupported/contradictory criteria, exact values or structures that are genuinely part of the construct, deterministic predicates, task-specific semantic criteria and observable anchors, Mixed point table, evidence map, and protected qualification fixtures.

Those artifacts are authored from only:

- the approved scenario input and its immutable hash; and
- the frozen Kubernetes v1.36.4 website/OpenAPI source registry in `development-pilot-source-rights-v1`.

The one-sentence `Expected answer — reviewer note` text in the human scenario-review page is convenience material only. It is not an evaluator source and cannot be copied into protected contracts, rubrics, fixtures, RAG, prompts, training, or final-test construction.

### Implementation — Codex after Human Gate A

Codex implements the typed schemas, validators, deterministic score calculations, model-agnostic semantic-assessment records/interfaces, protected-root access boundary, safe references/errors, provenance checks, qualification records, and adjudication/audit routing. Repository tests use synthetic non-domain fixtures.

Codex does not select or execute a real LLM judge in this implementation step, and it does not invent or author the protected Kubernetes criteria. Missing protected scientific content or an unqualified semantic assessor is an error, not permission to infer an answer.

## Evaluator resolution hierarchy

The evaluator uses the most objective valid evidence path available. Open semantics are not sent directly to a human by default, and an LLM judge never overrides a criterion that can be decided mechanically.

### 1. Deterministic verification first

Where correctness is mechanically observable, the contract uses a deterministic rule: for example schema structure, an exact API field/value, an explicit command count, an allowed mutation scope, a required action/final state, or another construct-critical requirement.

A semantic judge is not consulted for such a criterion. This follows the same broad preference for objective verification seen in benchmarks such as [IFEval](https://arxiv.org/abs/2311.07911), [LiveBench](https://arxiv.org/abs/2406.19314), and execution-based benchmarks such as [SWE-bench](https://arxiv.org/abs/2310.06770).

### 2. Qualified frozen LLM judge for residual semantic criteria

If an atomic criterion cannot be resolved by a legitimate deterministic rule, it may be assessed by a **qualified frozen semantic judge**. The judge receives the protected task-specific criterion, observable anchors and permitted frozen evidence needed for that criterion rather than one canonical answer paragraph to imitate.

The judge returns a structured criterion disposition such as `satisfied`, `not_satisfied`, `contradicted`, or `unresolved`; it does not directly choose the task score or weighting. The deterministic score kernel converts resolved criterion dispositions into Knowledge F1, Procedural success, or Mixed points.

Before a judge can be used for primary criterion dispositions, its exact evaluation configuration must be frozen and independently identifiable, including at least:

- model/provider or model artifact identity and version sufficient for reproducibility;
- inference backend/version where relevant;
- judge prompt/template hash and response schema;
- decoding and retry configuration;
- protected criterion/evidence input contract;
- qualification fixture-set identity;
- predeclared qualification thresholds and human-audit policy.

The exact judge model and thresholds are **not selected by this PR**. They require a later explicit freeze/approval before any judge-model execution.

LLM-as-a-judge is therefore treated as a calibrated measurement instrument rather than ground truth. This is consistent with the validation approach used by [MT-Bench](https://arxiv.org/abs/2306.05685), while taking seriously judge biases documented there and in [AlpacaEval 2](https://arxiv.org/abs/2404.04475). The criterion-specific checklist/rubric style is also aligned with the direction used by [WildBench](https://arxiv.org/abs/2406.04770).

### 3. Human adjudication and audit

A calibrated human reviewer is the final authority only for predefined escalation and audit paths. Human review is required when, for example:

- no qualified judge is approved for the criterion;
- the judge returns `unresolved` or an invalid/non-conforming assessment;
- qualification or audit detects a dispute that the frozen policy routes to adjudication; or
- the response is part of the predeclared blinded human-audit sample.

Human assessment is criterion-level and uses the same protected observable anchors. The reviewer is not asked to assign an intuitive whole-answer score.

The audit sample and any rule that can suspend/requalify a judge version must be frozen before the evaluated outputs are inspected, so human review cannot become outcome-driven cherry-picking.

## Judge qualification against human labels

A semantic judge cannot become primary merely because it is a strong model. Before use it must pass protected qualification against human-labelled criterion fixtures representing the actual task/language cells in which it will operate.

Qualification records at least:

- criterion-level agreement with the calibrated human labels;
- a disposition confusion matrix;
- an agreement statistic such as Cohen's kappa where the sample/design supports it;
- copying-neutral metamorphic results for paraphrase/source-like/synonym/wrong/partial/irrelevant variants;
- all failures, unresolved outputs, schema errors and adjudications.

The acceptance thresholds are predeclared and human-approved with the exact judge configuration; they are not tuned after seeing candidate-model outcomes. If the judge fails qualification, it cannot issue primary semantic dispositions. The evaluator then fails closed or uses the approved human route.

This structure deliberately separates **semantic assessment** from **score calculation**. Even when an LLM supplies a criterion disposition, the score itself is still deterministically derived from the frozen contract.

## How semantic scoring avoids lexical bias

The score kernel does not decide open meaning from string resemblance. It has no input for token overlap, n-grams, edit distance, ROUGE, BLEU, embeddings, source-prose similarity, or verbatim overlap.

A qualified LLM judge is also not a similarity scorer. It evaluates one protected criterion against the candidate response and frozen evidence/anchors. Correct source-like wording receives no bonus, and a lexically similar technical error must still fail the affected criterion.

A correct paraphrase and a correct source-like sentence are therefore intended to remain equivalent by construction: wording is not a score feature.

## Class-specific score flow

**Knowledge.** Required claims are stable atomic criterion IDs. Each satisfied required criterion counts once as TP; an unsatisfied required criterion is FN. FP comes only from unsupported/contradictory criteria declared by the protected contract and assessed for the response. Repeating a claim creates no extra credit. After primary assessments resolve, F1 is `2TP / (2TP + FP + FN)`.

**Procedural.** The primary result is one binary end-to-end success label. All primary-required constraints must pass and primary prohibited actions must remain absent. Mechanical parts are deterministic. If an essential diagnosis is genuinely semantic, the protected contract may route that binary criterion through the qualified semantic judge and then to human adjudication if necessary; lexical approximation is forbidden.

**Mixed.** Primary procedural hard gates run first. Any failed hard gate makes the primary score `0`, so fluent prose cannot compensate for an invalid artifact or forbidden action. If all hard gates pass, the evaluator applies the contract's pre-frozen criterion point table and divides by its declared positive maximum to obtain `[0,1]`. There are no default weights and no post-output reweighting.

## Evidence and provenance

Every score-affecting criterion maps to one or more frozen Kubernetes v1.36.4 source identities. The protected map records the approved inventory/repository revision and the path/blob or OpenAPI identity/hash needed to audit support. The participant model is not asked to reproduce any source path, evidence ID, URL, or citation.

Every protected bundle is also bound to the approved `family_id`, scenario-input identity/hash, source-rights manifest, evaluator version, and exact protected content hash. Judge assessments additionally bind the exact qualified judge-configuration identity. Corrections create successor identities; frozen artifacts are never overwritten.

This is criterion-level provenance, not a hidden prose golden.

## Fairness qualification

Actual Kubernetes fairness fixture responses and their expected criterion outcomes stay protected. At minimum, each Knowledge/Mixed × Polish/English cell has a fixture group containing:

1. concise correct paraphrase;
2. correct source-like wording;
3. accepted synonym/reordering;
4. lexically similar but technically wrong wording;
5. partially copied wording missing an important required claim;
6. a valid answer with irrelevant source text appended.

The first three must receive the same semantic dispositions and primary score. Wrong or incomplete variants must be worse on the affected criteria. Appending irrelevant text can never improve a score and may reduce it when it introduces a declared unsupported/contradictory claim.

Qualification applies both to the pure score kernel and, when enabled, to the frozen semantic judge. A judge that violates the required equivalence/order relations cannot qualify for primary assessment.

This is a form of [metamorphic testing](https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf): related inputs are constructed with a known relation that the evaluator must preserve. The fixture checks are about evaluator behavior; they are not benchmark families, participant-model training examples, or final-test material.

## Custody flow

Protected evaluator payloads resolve only through logical root `development-protected-evaluator-v1`. The concrete private storage binding is runtime custody configuration, not a model-visible or machine-specific path committed to the repository.

Authorized evaluation can resolve the protected payload only after checking role/purpose, root identity, root-relative reference, scenario binding, and SHA-256. Model-facing runners, retrievers, prompts, harnesses, skills, W1 processes, and future-training roles fail closed on the same reference. A judge role may receive only the protected criterion/evidence material authorized for the judge assessment and must never expose it to the participant model.

Safe public/model-facing metadata may retain only permitted identities, protected-relative handles, hashes, status/reason codes, assessor-type/config identities that do not reveal answers, and non-answer-bearing provenance. Validation errors never echo protected claims, expected values, source excerpts, answer-bearing evidence relationships, judge prompt payloads, or absolute protected locators.

## What approval of this design authorizes

Human approval of the accompanying Work PR authorizes Codex to implement only the generic evaluator contract, deterministic scoring, model-agnostic semantic-assessor/qualification records, protected routing, and synthetic qualification machinery described by the OpenSpec tasks. It does **not** authorize selection or execution of a real LLM judge, participant-model execution, or Codex fabrication of the per-scenario protected truth.

After that implementation is independently reviewed and merged, the 24 protected bundles can be instantiated and reviewed under the protected custody root. A separate human-approved judge freeze then selects the exact semantic judge configuration, human-labelled qualification fixtures/thresholds and audit policy. Only after that gate may judge qualification execute. Participant-model pilot scoring still requires its later execution gate.
