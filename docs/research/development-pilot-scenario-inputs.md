# Development-pilot Scenario Input Authoring

## Review status

- **Package ID:** `development-pilot-scenario-inputs-v1`
- **Issue:** #35
- **State:** candidate-authored; explicit human technical, language, rights, custody, freshness, and answerability review is still required
- **Custody root:** `development-model-facing-v1` (`development/model-facing`)
- **Pre-authoring freeze:** `development-pilot-preauthoring-freeze-v1`
- **Source/rights freeze:** `development-pilot-source-rights-v1`
- **Kubernetes release:** `v1.36.4`
- **Top-level manifest SHA-256:** `c23af39a049e992692865aa6e7a3ab5cab0d17e01db812e58e9daf15143ca3ad`
- **Construction-event log SHA-256:** `b85180089f1e1758e4ae05d219fc5dc69338dd9a76655e7bf51d61f1de7e0864`

This package performs only the authorized development-input authoring step. It does not perform protected evaluator construction, contamination-detector calibration/audit, evaluator qualification, model execution, real `kind`, live W1, C2 selection, training, harness implementation, or final-test work.

GenAI assisted candidate drafting, so these are **not yet human-approved benchmark items**. The human researcher must independently review all 24 inputs without consulting model responses.

## Where to review the questions

The primary human-review artifact is **[Development-pilot Scenario Human Review Catalog](development-pilot-scenario-review.md)**. It contains all 24 complete candidate questions in readable Markdown, grouped by class, with their exact `input_text` and a short explanation of what each item is intended to test. Human review should use that document rather than reading the JSON payloads directly.

## Pilot scope: not the final benchmark

These 24 independent families are the **development-only pilot / feasibility sample**, not the final benchmark sample size and not the final-test set. The pilot exists to validate solvability, evaluator quality, headroom, method applicability, runtime/storage budgets, and the study design. Later work may construct additional family-disjoint development material where scientifically required, separate F1 training families, and eventually a protected final-test set under its own freeze and custody gate. No final-test family is authored or reserved here.

## Model-input exposure contract

`development/model-facing` is a custody boundary, not a declaration that every field stored there is prompt-visible. For the base scenario export, the canonical scenario content supplied to the model is **only the `input_text` field**.

The base model does not receive family/authoring metadata, source or provenance metadata, source-evidence identifiers, OpenAPI schema identities, hashes, condition-profile metadata, review metadata, evaluator metadata, or the top-level source registry. Those fields remain repository governance/provenance data for reproducibility. A later experimental condition may add only context or tools explicitly authorized by that condition's frozen contract.

The per-scenario `source_evidence_ids` and `openapi_schema_identities` fields were removed from the three scenario payloads after human review identified their unnecessary leakage risk. Their provenance relationship remains preserved in the append-only construction ledger and source registry.

A subsequent human review also removed citation/source-path requests from every scenario and removed the one residual phrase that told a procedural item to rely on an approved source. Seventeen `input_text` values therefore receive new SHA-256 identities; seven unaffected procedural inputs retain their prior hashes. The prior hashes remain preserved in append-only provenance and Git history.

### Source-reference and semantic-scoring clarification

`development-pilot-evaluation-clarification-v1` records the human-approved rule that citations, source paths, evidence identifiers, and URLs are not required or scored model outputs. RAG/W1 provenance is captured by the harness/evaluator, while answer groundedness is assessed against the context actually supplied or fetched.

Open prose is evaluated by required/unsupported semantic claims and calibrated task-specific rubrics. Lexical overlap with reference prose or Kubernetes documentation contributes no score, and copying documentation verbatim receives no bonus. Exact matching is reserved for construct-critical literals and explicit output constraints.

## Model-facing artifacts

All candidate inputs are under `development-model-facing-v1`:

- `data/benchmark/development/model-facing/development-pilot-scenario-inputs-v1.json` — package index, exact source registry, frozen identities, boundary assertions, and payload hashes;
- `data/benchmark/development/model-facing/development-pilot-knowledge-scenarios-v1.json` — 8 knowledge inputs, SHA-256 `24ac49211c10c986bd37730e2afefa04b262ba951e097d06528fd6f2c78111db`;
- `data/benchmark/development/model-facing/development-pilot-procedural-scenarios-v1.json` — 8 procedural inputs, SHA-256 `3dc0bd56c79b07dabe3e343e7598b9b01a328764063109b662d6f33e37779066`;
- `data/benchmark/development/model-facing/development-pilot-mixed-scenarios-v1.json` — 8 mixed inputs, SHA-256 `e4d64c75fa9204651a85163926cf80c84ea56badb8da87581544823386c9cab6`;
- `data/benchmark/development/model-facing/development-pilot-construction-events-v1.jsonl` — append-only construction/provenance/hash evidence.

The split payloads are an implementation detail for reviewability. The package remains one logical manifest, `development-pilot-scenario-inputs-v1`.

## Frozen-slot satisfaction

| Family ID     | Class      | Lang | Frozen coverage/subtype                  | Candidate scenario focus                                |
| ------------- | ---------- | ---- | ---------------------------------------- | ------------------------------------------------------- |
| `dev-k-pl-01` | knowledge  | pl   | `direct-evidence`                        | ConfigMap-backed environment variable propagation       |
| `dev-k-pl-02` | knowledge  | pl   | `synthesis`                              | startup/readiness/liveness probe role synthesis         |
| `dev-k-pl-03` | knowledge  | pl   | `absent-answer-abstention`               | StatefulSet DNS delay absent-guarantee case             |
| `dev-k-pl-04` | knowledge  | pl   | `distractor-heavy-evidence`              | non-preempting PriorityClass with distractors           |
| `dev-k-en-01` | knowledge  | en   | `direct-evidence`                        | CronJob Forbid concurrency semantics                    |
| `dev-k-en-02` | knowledge  | en   | `synthesis`                              | CronJob-to-Job and Job restart policy synthesis         |
| `dev-k-en-03` | knowledge  | en   | `absent-answer-abstention`               | Service EndpointSlice update absent-SLA case            |
| `dev-k-en-04` | knowledge  | en   | `distractor-heavy-evidence`              | ConfigMap subPath update with distractors               |
| `dev-p-pl-01` | procedural | pl   | `diagnosis`                              | structured Init Container diagnosis                     |
| `dev-p-pl-02` | procedural | pl   | `constrained-repair`                     | constrained Deployment selector/template repair         |
| `dev-p-pl-03` | procedural | pl   | `ordered-action`                         | ordered Deployment image rollout and rollback procedure |
| `dev-p-pl-04` | procedural | pl   | `structured-artifact-schema-adherence`   | schema-constrained CronJob authoring                    |
| `dev-p-en-01` | procedural | en   | `diagnosis`                              | structured readiness/Service diagnosis                  |
| `dev-p-en-02` | procedural | en   | `constrained-repair`                     | constrained ConfigMap reference repair                  |
| `dev-p-en-03` | procedural | en   | `ordered-action`                         | ordered manual Deployment scaling                       |
| `dev-p-en-04` | procedural | en   | `structured-artifact-schema-adherence`   | schema-constrained indexed Job authoring                |
| `dev-m-pl-01` | mixed      | pl   | `evidence-backed-configuration-decision` | evidence-backed probe configuration decision            |
| `dev-m-pl-02` | mixed      | pl   | `evidence-backed-bounded-procedure`      | evidence-backed Service diagnosis procedure             |
| `dev-m-pl-03` | mixed      | pl   | `evidence-backed-artifact-validation`    | CronJob artifact validation and correction              |
| `dev-m-pl-04` | mixed      | pl   | `evidence-backed-repair-plan`            | ConfigMap environment refresh repair plan               |
| `dev-m-en-01` | mixed      | en   | `evidence-backed-configuration-decision` | topology-spread configuration decision                  |
| `dev-m-en-02` | mixed      | en   | `evidence-backed-bounded-procedure`      | bounded Deployment rollout investigation                |
| `dev-m-en-03` | mixed      | en   | `evidence-backed-artifact-validation`    | resource-quantity artifact validation                   |
| `dev-m-en-04` | mixed      | en   | `evidence-backed-repair-plan`            | taint/toleration repair plan                            |

Composition remains exactly 8 knowledge, 8 procedural, and 8 mixed inputs; each class contains 4 Polish and 4 English inputs. Every payload repeats the frozen `family_id`, `split=development`, independent-family flag, task class, language, coverage/subtype, answer-contract class, source roles, provenance references, and condition profile without alteration.

No Polish/English semantic pair, `kind`, W1, or C2 family is selected.

## Source and provenance controls

Construction facts are limited to the approved inventories:

- `website-v1.36.4-development-pilot-v1`: `kubernetes/website@1de955ebabe7e17da1ebb4f582635491227f4157`, content-index SHA-256 `ff6e098274f45cf35dd669d0de61e566129e891baad8e0e49d7fe6922c432127`;
- `openapi-v1.36.4-development-pilot-v1`: `kubernetes/kubernetes@bb826b1d48562f110659e64e8ec444327433db95`, `api/openapi-spec/swagger.json`, SHA-256 `dcede2063da1d7ad62ecb5af8adb6d7fabd0b52385a7fa0048afb491dac90450`.

The top-level source registry records every exact allowlisted website path and Git blob identity used. Slots whose frozen roles require OpenAPI also carry the frozen OpenAPI provenance reference and a schema identity. No moving current page, localization, external link, linked example, third-party source, or unapproved Kubernetes path was used as construction evidence.

The wording is fresh and source-transformed. No public question or answer was copied. Raw upstream source content is not committed.

Required attribution:

> Based on Kubernetes documentation by the Kubernetes Contributors, frozen at `kubernetes/website@1de955ebabe7e17da1ebb4f582635491227f4157`, licensed under CC BY 4.0. Changes and selection were made for this research benchmark. No endorsement is implied.

## Construction and contamination evidence

One append-only provenance event exists for each authored family and includes the scenario-input hash, source evidence IDs, root, status, and family identity. Hash events freeze the current candidate manifest and three payload files for review.

There were **no formally admitted candidate rejections or replacements** in this batch. No rejection record is fabricated. If human review rejects an item for leakage, ambiguity, unsolvability, missing evidence, or construct mismatch, append a rejection event and author a replacement in the same frozen family slot. Model performance may never justify replacement.

No calibrated contamination audit is claimed here. `semantic_pair_id` remains null for all 24 inputs, and the set was intentionally diversified across languages rather than authored as translations. The formal detector-calibration and contamination-audit steps remain later in the approved sequence.

## Boundary audit

This package contains no protected expected answer/result, evidence map, golden, answer-revealing rubric, adjudication material, protected evaluator payload/locator, training material, final-test identity/reference/placeholder/hash/payload/root, model output, experimental observation, real-cluster execution, live W1 material, C2 eligibility selection, or harness implementation.

OpenAPI references and public website source paths are provenance identities permitted in the model-facing root; they are not protected evaluator references.

## Human review checklist

Review every family without consulting model output and confirm:

1. class, language, coverage/subtype, answer-contract class, source roles, provenance references, and condition profile match the frozen slot;
2. each factual premise is supported by the recorded exact `v1.36.4` source evidence;
3. Polish and English prose is technically natural and no undeclared semantic pair has been created;
4. the input is answerable, except where the frozen abstention subtype intentionally tests absence;
5. response-form constraints are neutral and do not favor an adaptation method;
6. transformation and attribution are acceptable under `development-pilot-source-rights-v1`;
7. no protected, training, final-test, optional-stratum, or execution boundary was crossed.

Only after explicit human approval and merge of this candidate-input package may the workflow advance to protected evaluator construction.
