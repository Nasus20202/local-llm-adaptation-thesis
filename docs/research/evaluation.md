# Evaluation Strategy

## Principles

Use the cheapest valid evaluator first: deterministic validation, then reference-based metrics, then calibrated rubrics/human review, and only then an LLM judge as supporting evidence. No important conclusion rests on one proprietary judge.

## Quality layers

1. **Structural validity:** parseability, schema validity, required fields, length/format constraints.
2. **Deterministic task success:** exact match, unit-style checks, allowed action sequence, or executable outcome.
3. **Reference comparison:** token/semantic F1 only where its assumptions fit the answer form.
4. **Evidence-based rubric:** atomic claim correctness, completeness, relevance, and constraint adherence.
5. **Calibrated judge:** blinded condition labels, fixed prompt/version, repeated calibration against human ratings, and disagreement reporting.

## Task-class primary candidates

| Class | Candidate primary outcome | Supporting outcomes |
|---|---|---|
| Knowledge | atomic factual correctness or exact task success | precision/recall of claims, completeness, abstention quality |
| Procedural | end-to-end task success | constraint adherence, step errors, schema validity |
| Mixed | end-to-end rubric score with deterministic gates | knowledge correctness, procedural success, cost |

Final primary outcomes remain unresolved until the domain is selected.

## Stability

- probability of retry-free success per item;
- within-item agreement across samples;
- variance or entropy of discrete outcomes;
- paraphrase sensitivity as paired performance spread;
- worst-formulation and lower-quantile performance, not only mean score.

## Performance

Capture model load time, TTFT, end-to-end latency, prompt/effective input tokens, generated tokens, decode throughput, peak resident RAM, peak VRAM where reliably measurable, and failures. Define measurement boundaries and sampling frequency before baseline freeze.

## RAG decomposition

- retrieval recall at K against evidence annotations;
- retrieval precision/relevance and ranking metrics where graded relevance exists;
- retrieval latency and context token cost;
- answer correctness and completeness;
- claim-level faithfulness/groundedness;
- citation/evidence correctness;
- explicit no-answer behavior.

A correct answer after retrieval failure and an incorrect answer after successful retrieval are distinct error modes.

## Fine-tuning accounting

Record training wall time, GPU type/count, peak memory, examples/tokens, steps/epochs, seed, optimizer and schedule, adapter rank/targets, adapter size, exported model size, and every cloud/session failure. Training cost is separate from local inference cost.

## Evaluator governance

Evaluator code and rubrics have versions and hashes. Changes generate a new processed evaluation version; raw model outputs remain unchanged. Human raters are blinded to condition where possible. Inter-rater agreement and adjudication rules are reported.
