# Experimental Design

## Design overview

Use a blocked, within-item comparison on one primary model. Each benchmark item is evaluated under the applicable adaptation conditions; task class is a block and method is the principal independent variable. The secondary model repeats only pre-registered contrasts.

## Variables

### Independent variables

- adaptation condition: B0, P1, P2, R1, F1, H1, S1, C1, or C2 when applicable;
- task class: knowledge, procedural, mixed;
- prompt formulation: canonical plus frozen semantic paraphrases for the stability study;
- repeated-generation seed/sample index;
- model family only in the selected replication stage.

### Dependent variables

- correctness and task success;
- task-specific precision, constraint adherence, and schema validity;
- factuality/groundedness and citation correctness where applicable;
- repeated-run and paraphrase stability;
- TTFT, latency, throughput, token counts, peak RAM/VRAM, and load time;
- training duration, accelerator, peak memory, tokens/examples, adapter/export size;
- recorded engineering effort and configuration complexity using a pre-defined rubric.

### Controlled variables

- model repository, revision, artifact hash, and quantization;
- inference backend build, container digest, and hardware/software environment;
- chat template, thinking policy, generation parameters, and maximum output;
- benchmark revision, split, evaluator version, and golden hash;
- condition-specific prompt/RAG/skill/harness revisions;
- warm-up policy, timing boundary, concurrency, and background-load policy.

## Applicability matrix

| Task class | Required core contrasts | Optional justified contrasts |
|---|---|---|
| Knowledge | B0, P1, R1, F1 | P2, C1 |
| Procedural | B0, P1, H1, S1 | P2, F1 if the training target is procedural |
| Mixed | B0, strongest simple conditions | C1 and one C2 after component evidence |

Inapplicable methods are not scored as failures. Pairwise combinations are not generated automatically.

## Run structure

1. Freeze all inputs in an experiment manifest.
2. Execute a small non-test smoke set to validate configuration and telemetry.
3. Randomize or counterbalance condition execution order within hardware blocks.
4. Warm the model/runtime according to a fixed protocol; exclude warm-up from quality but record it.
5. Save every raw request, response, timing event, exit status, and validity flag.
6. Evaluate without exposing golden answers to the generator.
7. Produce a new run for retries; never overwrite.

## Repetition and stability

- Temperature-zero repeats do not estimate stochastic stability and are used only where deterministic decoding is scientifically intended.
- A frozen non-zero sampling configuration will be used for repeated-generation reliability.
- Candidate minimum: five samples per item/condition and three semantic formulations per selected item. Final counts require a pilot-based compute and precision analysis before test freeze.
- Repetitions are nested within benchmark items; they are not independent benchmark examples.

## Fairness and context

Primary comparison uses each method's necessary context and reports its token/cost consequence. A context-budget-matched sensitivity analysis should be used where truncation does not destroy the method definition. RAG receives the same source corpus across variants; harness and skills may not access golden answers or evaluator logic.

## Invalid runs

Validity rules are fixed before final execution. Examples include corrupted output capture, backend crash, missing provenance, hash mismatch, or hardware telemetry failure required by the analysis. A semantically wrong model answer is valid evidence, not an invalid run.

## Unresolved before final design

- benchmark domain and item counts;
- primary outcome and smallest effect of interest per task class;
- repetition counts and semantic-paraphrase construction;
- thinking/sampling policy;
- fair context budget and maximum local runtime per item.
