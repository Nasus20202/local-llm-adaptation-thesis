# Evaluation Strategy

## Principles

Use the cheapest valid evaluator first: deterministic validation, then reference-based metrics, then calibrated rubrics and human review, and only then an LLM judge as supporting evidence. No important conclusion rests on one proprietary judge.

Each item freezes one answer contract that is identical for all compared conditions. A malformed or constraint-violating answer may fail a deterministic gate; a well-formed but incorrect answer remains valid evidence. The proposed qualification procedure and thresholds are defined in the [development-only pilot protocol](benchmark-pilot-protocol.md).

## Quality layers

1. **Structural validity:** parseability, schema validity, required fields, length, and format constraints.
2. **Deterministic task success:** construct-critical exact literals, API-schema checks, policy assertions, allowed action sequence, or executable outcome.
3. **Reference comparison:** concept-level atomic-claim or semantic equivalence; lexical overlap with reference prose is not scored.
4. **Evidence-based rubric:** technical correctness, completeness, relevance, unsupported-claim control, and constraint adherence.
5. **Calibrated judge:** optional, blinded condition labels, fixed prompt/version, calibration against adjudicated human ratings, and disagreement reporting.

## Task-class answer forms and pilot outcomes

| Class      | Permitted primary answer forms                                                   | Candidate pilot primary outcome                           | Supporting outcomes                                    |
| ---------- | -------------------------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------ |
| Knowledge  | concise prose or atomic claims                                                   | atomic-claim F1 for required and unsupported claims       | semantic correctness, completeness, abstention quality |
| Procedural | Kubernetes YAML or JSON, patch, bounded action sequence, or structured diagnosis | binary end-to-end task success                            | constraint adherence, step errors, schema validity     |
| Mixed      | technically justified decision plus verifiable artifact or procedure             | normalized task-specific score with procedural hard gates | knowledge correctness, procedural success, cost        |

Final primary outcomes freeze only after development-only pilot evidence is reviewed under the predeclared rules. Lexical similarity is never a primary outcome.

## Semantic-scoring fairness

The protected reference for an open answer is a **semantic scoring contract**, not canonical prose that the model is expected to reproduce. It records required concepts, acceptable alternatives, unsupported or contradictory claims, task constraints, and only those exact technical literals whose identity is part of the construct.

- Semantically equivalent paraphrases, synonyms, different sentence order, and concise versus expanded correct explanations receive the same credit.
- Token overlap, n-gram overlap, edit distance, ROUGE/BLEU-like similarity, or verbatim overlap with Kubernetes documentation **must not add score**. Copying documentation word-for-word receives no bonus.
- Exact matching is allowed only for construct-critical literals such as required API/schema keys, enum values, numeric constraints, explicitly requested identifiers, exact output keys, or other literals whose spelling/value is itself being tested.
- Extra copied text can reduce relevance or unsupported-claim precision when it introduces irrelevant, incorrect, contradictory, or unsupported claims.
- If deterministic logic cannot decide whether an open statement is semantically equivalent, the case routes to the calibrated atomic human rubric rather than receiving an arbitrary string-similarity score.
- The same semantic criteria apply across B0, prompting, fine-tuning, RAG, and combined conditions. No condition receives credit merely because it had access to text that resembles the protected reference.

The development pilot does not require the model to emit citations, file paths, evidence IDs, or URLs. Source provenance and evidence support are evaluator/harness-side records.

## Evaluator fixtures

Every deterministic component has versioned positive, negative, boundary, malformed, and ambiguous fixtures. Deterministic checks must match 100% of expected outcomes, be idempotent, and return reason codes. Ambiguous cases are rejected or routed to a named human criterion.

Open-answer scoring additionally uses **metamorphic fairness fixtures** in every applicable Knowledge/Mixed × Polish/English cell. For the same underlying semantic contract:

- a concise correct paraphrase and a correct answer using wording close to the source must receive the same atomic correctness/completeness result;
- reordering correct claims or using accepted synonyms must not change the score;
- a lexically similar or partially copied answer containing a technical contradiction or missing required concept must score worse on the affected atomic criteria;
- adding irrelevant or unsupported copied material must never raise the score and may reduce relevance or unsupported-claim precision.

A semantic evaluator that violates any required invariance or ordering above does not qualify. These fixtures test the scoring implementation directly, rather than assuming that a declared semantic metric is sufficient.

Fixture payloads and expected results are development evaluator material, not benchmark families or final-test goldens. They are constructed only after Human Gate A and protected from model-facing contexts.

## Human rubric and calibration

Rubrics use atomic task-specific criteria with observable three-level anchors where ordinal judgment is necessary. Two technically competent raters complete a 12-response training round and then a disjoint, blinded 24-response qualification set balanced by task class and language.

Report confusion tables, exact agreement, adjacent-category agreement, and nominal/ordinal Krippendorff alpha with a family-clustered 95% bootstrap interval. Green qualification requires at least 90% exact agreement for every critical binary label, pooled alpha at least 0.80, and lower interval bound at least 0.67. Amber permits one rubric revision and disjoint requalification; red or a second non-green attempt narrows or demotes the affected metric before final freeze.

All pilot responses receiving a human primary score are double-rated. After green qualification, a stratified 25% of the larger final study is double-rated. Critical-label or greater-than-one-level disagreements require written adjudication; unresolved cases retain both labels and a conservative sensitivity analysis.

## Cross-language scoring equivalence

Polish and English items use the same construct definitions, task-class outcome hierarchy, and severity of deterministic gates. Technical identifiers and configuration semantics are unchanged. Language-specific surface quality is not allowed to substitute for technical correctness.

Human-adapted variants receive a semantic-equivalence record covering task intent, constraints, evidence, expected answer form, and difficulty. Reviewers inspect disagreements for translation or adaptation error before attributing them to model language ability. Parallel variants share a family ID and are analyzed as nested observations.

## Interactive task evaluation

Static and `kind` variants share the same underlying fault and success criterion. Interactive success is determined by the automatic final-state validator, prohibited-action gates, and action-budget record. Diagnosis prose is secondary when the final state is mechanically decidable. All applicable conditions receive the same neutral execution interface and permissions.

## Stability

- probability of retry-free success per family;
- within-family agreement across samples;
- variance or entropy of discrete outcomes;
- paraphrase sensitivity as paired performance spread;
- selected cross-language and static/interactive paired spread;
- worst-formulation and lower-quantile performance, not only mean score.

## Performance

Capture model load time, TTFT, end-to-end latency, prompt or effective input tokens, generated tokens, decode throughput, peak resident RAM, peak VRAM where reliably measurable, and failures. For tool-enabled conditions, also capture tool wall time, calls, actions, returned context, and budget exhaustion. Define measurement boundaries and sampling frequency before baseline freeze.

## RAG and web decomposition

For R1, separately measure retrieval recall at K, ranking/relevance where supported, retrieval latency/context cost, answer correctness, evaluator-side groundedness, and no-answer behavior. Retrieval and answer failure remain distinct. Retrieval provenance identifies what context was supplied; the model is not required or rewarded for reproducing source paths or citations.

W1 uses the same answer contract but is reported as an official-source live-web sensitivity condition. Query, rank, URL, redirect, timestamp, body/hash, tool version where available, token budget, rejection, and error provenance are required. W1 is not silently substituted for R1 or H1.

## Fine-tuning accounting

Record training wall time, GPU type and count, peak memory, examples or tokens, steps or epochs, seed, optimizer and schedule, adapter rank and targets, adapter size, exported model size, and every cloud or session failure. Training cost is separate from local inference cost.

## Evaluator governance

Evaluator code, schemas, checks, rubrics, and calibration sets have versions and hashes. Changes generate a new processed evaluation version; raw model outputs remain unchanged. Raters are blinded to condition where possible. Inter-rater agreement, adjudication, recalibration, and limitations are reported.
