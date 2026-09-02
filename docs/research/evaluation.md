# Evaluation Strategy

## Principles

Use the cheapest valid evaluator first: deterministic validation, then reference-based metrics, then calibrated rubrics and human review, and only then an LLM judge as supporting evidence. No important conclusion rests on one proprietary judge.

Each item freezes one answer contract that is identical for all compared conditions. A malformed or constraint-violating answer may fail a deterministic gate; a well-formed but incorrect answer remains valid evidence.

## Quality layers

1. **Structural validity:** parseability, schema validity, required fields, length, and format constraints.
2. **Deterministic task success:** exact match, API-schema checks, policy assertions, allowed action sequence, or executable outcome.
3. **Reference comparison:** token or semantic F1 only where its assumptions fit the answer form.
4. **Evidence-based rubric:** atomic claim correctness, completeness, relevance, and constraint adherence.
5. **Calibrated judge:** blinded condition labels, fixed prompt and version, repeated calibration against human ratings, and disagreement reporting.

## Task-class answer forms and outcomes

| Class | Permitted primary answer forms | Candidate primary outcome | Supporting outcomes |
|---|---|---|---|
| Knowledge | concise prose or atomic claims with requested evidence references | atomic factual correctness or exact task success | claim precision and recall, completeness, abstention quality |
| Procedural | Kubernetes YAML or JSON, patch, bounded action sequence, or structured diagnosis | end-to-end task success | constraint adherence, step errors, schema validity |
| Mixed | evidence-grounded decision plus verifiable artifact or procedure | end-to-end rubric score with deterministic gates | knowledge correctness, procedural success, cost |

Final primary outcomes remain unresolved until development-only pilot evidence is reviewed.

## Cross-language scoring equivalence

Polish and English items use the same construct definitions, task-class outcome hierarchy, and severity of deterministic gates. Technical identifiers and configuration semantics are unchanged. Language-specific surface quality is not allowed to substitute for technical correctness.

Human-adapted variants receive a semantic-equivalence record covering task intent, constraints, evidence, expected answer form, and difficulty. Reviewers inspect disagreements for translation or adaptation error before attributing them to model language ability. Parallel variants share a family ID and are analyzed as nested observations.

## Stability

- probability of retry-free success per item;
- within-item agreement across samples;
- variance or entropy of discrete outcomes;
- paraphrase sensitivity as paired performance spread;
- selected cross-language paired spread;
- worst-formulation and lower-quantile performance, not only mean score.

## Performance

Capture model load time, TTFT, end-to-end latency, prompt or effective input tokens, generated tokens, decode throughput, peak resident RAM, peak VRAM where reliably measurable, and failures. Define measurement boundaries and sampling frequency before baseline freeze.

## RAG decomposition

- retrieval recall at K against evidence annotations;
- retrieval precision or relevance and ranking metrics where graded relevance exists;
- retrieval latency and context token cost;
- answer correctness and completeness;
- claim-level faithfulness or groundedness;
- citation and evidence correctness;
- explicit no-answer behavior.

A correct answer after retrieval failure and an incorrect answer after successful retrieval are distinct error modes. The primary corpus is the same pinned canonical English source snapshot for Polish and English items; language-related retrieval differences are reported rather than hidden by document substitution.

## Fine-tuning accounting

Record training wall time, GPU type and count, peak memory, examples or tokens, steps or epochs, seed, optimizer and schedule, adapter rank and targets, adapter size, exported model size, and every cloud or session failure. Training cost is separate from local inference cost.

## Evaluator governance

Evaluator code, schemas, checks, and rubrics have versions and hashes. Changes generate a new processed evaluation version; raw model outputs remain unchanged. Human raters are blinded to condition where possible. Inter-rater agreement and adjudication rules are reported.
