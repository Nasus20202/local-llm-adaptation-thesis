# Research Questions

## Scope

The questions concern adaptation methods for specialized task classes under local inference constraints. Foundation-model comparison is limited to transfer of selected findings.

## Proposed questions

### RQ1 — Task performance

How does each justified adaptation strategy change task-level correctness relative to the unaltered instruction-model baseline when model, local backend, generation policy, and benchmark item are controlled?

### RQ2 — Precision and reliability

How does each strategy change task-specific precision, factual correctness, constraint adherence, schema validity, and retry-free task success?

“Precision” is not a single universal metric: it must be operationalized per benchmark task before dataset freeze.

### RQ3 — Stability

How stable is each strategy across repeated stochastic generations and semantically equivalent prompt formulations, and does an average improvement conceal increased worst-case or run-to-run variability?

### RQ4 — Cost-effectiveness

What inference, adaptation, and engineering cost is required for each improvement, and which strategies lie on the quality–cost Pareto frontier?

### RQ5 — Task-class interaction

How does strategy effectiveness interact with knowledge, procedural, and mixed task classes?

### RQ6 — Combination value

Do pre-selected combined approaches deliver meaningful incremental gains over their strongest simpler constituent after accounting for context, latency, and implementation cost?

### RQ7 — Transfer

For selected high-value contrasts, do the direction and practical significance of findings transfer from the primary model to a second model family?

## Proposed hypotheses

- **H1:** RAG will improve correctness and groundedness most on knowledge tasks whose answers are present in the indexed corpus; retrieval failure will bound the gain.
- **H2:** harness and skill conditions will improve procedural constraint adherence and task completion more than factual knowledge accuracy.
- **H3:** combined systems will outperform simple systems only when their components address complementary, observed error modes; otherwise added context and orchestration cost will erase the benefit.
- **H4:** effect direction will transfer more consistently than effect magnitude across model families.

H2–H4 remain directional hypotheses. Exact primary outcomes and smallest effect sizes of interest must be defined after the benchmark domain and pilot variability are known, but before final test execution.

## Required decisions before freeze

1. Select the specialized domain and Polish/English language composition.
2. Define “precision” for each task type.
3. Select one primary outcome per task class.
4. Define the smallest practically meaningful improvement and cost increase.
5. Pre-select the contrasts replicated on the secondary model.
