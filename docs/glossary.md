# Glossary

A compact reference for concepts used in the thesis. Entries are intentionally short: enough to understand the method and reuse the explanation later in the theoretical chapter, with a primary or official source for deeper reading.

## Adaptation and inference

### Large language model (LLM)

A neural language model trained to predict tokens from context and then used to generate text autoregressively. In this thesis the underlying model is kept identifiable and reproducible so changes in adaptation method can be compared rather than silently attributed to a different base model.

### Prompt engineering

Changing instructions, examples, structure, or other prompt content without changing model weights. It works by altering the context from which the model predicts the next tokens; here it is the lightest adaptation family and a comparator for heavier methods. See [Brown et al., 2020](https://arxiv.org/abs/2005.14165) for few-shot prompting and [Wei et al., 2022](https://arxiv.org/abs/2201.11903) for chain-of-thought prompting.

### Retrieval-augmented generation (RAG)

A retriever first selects external passages relevant to the query, then those passages are added to the model context before generation. RAG can add version-specific knowledge without changing model weights, but retrieval quality and answer quality must be measured separately. [Original RAG paper](https://arxiv.org/abs/2005.11401).

### Embedding and retriever

An embedding maps text to a numeric vector intended to preserve useful semantic relationships. A vector retriever compares query and document vectors, ranks candidate passages, and returns the top `K`; retrieval can therefore fail even when the answer generator would have used the right passage correctly. The retrieval-plus-generation split is described in [Lewis et al., 2020](https://arxiv.org/abs/2005.11401).

### LoRA

Low-Rank Adaptation freezes the base model and learns small low-rank update matrices for selected weight layers. It reduces the number of trainable parameters and the storage cost of adaptation compared with full fine-tuning. [LoRA paper](https://arxiv.org/abs/2106.09685).

### QLoRA

QLoRA combines LoRA adapters with a quantized frozen base model during fine-tuning, reducing memory requirements while retaining trainable low-rank adapters. It is relevant here because training must fit limited local or notebook GPU memory. [QLoRA paper](https://arxiv.org/abs/2305.14314).

### Quantization

Representing model weights, and sometimes activations or caches, with fewer bits than the original floating-point representation. It reduces memory use and can improve local inference speed at the cost of approximation error; quantization is therefore part of the reproducible model identity rather than an invisible implementation detail. [llama.cpp](https://github.com/ggml-org/llama.cpp).

### Model harness

The orchestration layer around the model: it can expose tools, collect observations, enforce budgets, decide when to stop, and record provenance. A harness can improve task success without changing model knowledge, so the thesis evaluates it as a separate adaptation mechanism. [ReAct](https://arxiv.org/abs/2210.03629) and [Toolformer](https://arxiv.org/abs/2302.04761) are primary examples of tool-using language-model systems.

### Skill

A reusable, versioned set of procedural instructions or workflow knowledge supplied to the model or harness. A skill should encode general procedure rather than the answer to a benchmark item, otherwise it becomes leakage rather than adaptation. `Skill` is a project-level experimental construct; its exact contract is defined in [Experimental Design](research/experimental-design.md).

### Tool calling

The model emits a structured request for an external operation, the harness executes an allowed tool, and the result is returned to the model as new context. Tool access changes what the system can observe or do, so permissions and action budgets must be matched across compared conditions.

## Evaluation

### Atomic claim

A single independently judgeable proposition in an answer, such as “`Forbid` applies only to Jobs from the same CronJob.” Breaking open answers into claims lets the evaluator score meaning without requiring one canonical sentence. [FActScore](https://arxiv.org/abs/2305.14251) is a primary example of decomposing generated text into atomic facts for fine-grained factual evaluation; this thesis uses its own protected task-specific claim contracts rather than FActScore's automated scorer.

### Precision, recall, and F1

For semantic claim scoring, a true positive is a required claim expressed correctly, a false negative is a required claim that is missing, and a false positive is an unsupported or contradictory claim counted by the contract. Precision is `TP / (TP + FP)`, recall is `TP / (TP + FN)`, and F1 is their harmonic mean `2PR / (P + R)`. The semantic labels are decided before these counts; text overlap does not define a true positive. [scikit-learn F1 reference](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html).

### Deterministic evaluator

A rule-based check whose result is mechanically reproducible, for example JSON parseability, a Kubernetes schema constraint, an exact required field, or a validated final cluster state. It is preferred whenever the construct can be checked without subjective language judgment.

### Semantic scoring

Judging whether the response expresses the required technical meaning rather than matching reference wording. Correct paraphrases and source-like wording receive the same credit; lexical similarity is not a score component in this project. Open semantic criteria are resolved through protected task-specific criteria and calibrated human assessment when exact/value/structure rules cannot decide them. Fine-grained atomic evaluation is exemplified by [FActScore](https://arxiv.org/abs/2305.14251); the project's no-lexical-bonus rule is an explicit methodological control.

### Construct-critical literal

A string, value, identifier, count, enum, key, or structure whose exact identity is itself part of the task construct—for example a required Kubernetes API field or explicitly requested numeric value. Exact comparison is allowed only for such criteria; it is not a shortcut for grading open prose. Kubernetes schema identity is audited against the frozen [OpenAPI specification](https://spec.openapis.org/oas/latest.html) and Kubernetes v1.36.4 source snapshot.

### Rubric

A small set of named criteria with explicit observable anchors. Human raters use it only for aspects that deterministic checks cannot decide reliably, such as whether an explanation is technically complete without requiring canonical prose.

### LLM judge

Another language model used to rate an answer. It is convenient for open text but can introduce model-specific bias and instability, so this thesis treats it as calibrated supporting evidence rather than the sole basis for a primary conclusion. See Zheng et al., [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685).

### Metamorphic fairness fixture

A test pair or set where the technical meaning is deliberately held constant while wording changes, or wording is held similar while correctness changes. A valid semantic evaluator must score correct paraphrases equivalently and must not reward a technically wrong answer merely because it resembles documentation. This adapts the metamorphic-testing idea of checking known relations between related test cases; see Chen, Cheung, and Yiu, [Metamorphic Testing: A New Approach for Generating Next Test Cases](https://www.cse.ust.hk/~scc/publ/CS98-01-metamorphictesting.pdf).

### Krippendorff's alpha

A chance-corrected measure of agreement between raters that can handle different measurement levels and missing ratings. The project uses it to decide whether a human rubric is reliable enough for confirmatory scoring. [Krippendorff, 2011](https://doi.org/10.1080/19312458.2011.568376).

### Bootstrap confidence interval

A bootstrap repeatedly resamples observed units and recomputes a statistic to approximate its sampling uncertainty without assuming a simple parametric distribution. Here family-clustered resampling keeps related observations together when estimating uncertainty. [Efron, 1979](https://doi.org/10.1214/aos/1176344552).

### Groundedness

Whether an answer's factual claims are supported by the context that the RAG or search condition actually supplied. It is evaluated from captured retrieval/search provenance; the model does not need to reproduce file paths or citations to receive credit. See Es et al., [RAGAS](https://arxiv.org/abs/2309.15217) for retrieval, grounding, and answer-evaluation dimensions.

### Retrieval Recall@K

The proportion of queries for which the evidence needed for the answer appears within the top `K` retrieved passages. It isolates retrieval failure from generation failure: a model cannot use evidence that the retriever never returned.

### Abstention

Explicitly declining to invent an answer when the available evidence does not justify one. In the benchmark this is a positive capability for questions whose correct behavior is to reject a false precision or unsupported guarantee.

## Experiment and infrastructure

### Provenance

The recorded identity and history of inputs, model revisions, sources, tools, configuration, and outputs needed to explain and reproduce a result. Missing required provenance makes a run invalid even if the answer looks plausible.

### Contamination

Unintended exposure of benchmark or protected answer information to training, retrieval, prompts, tools, or model selection. Contamination can make an apparent improvement meaningless because the tested system has effectively seen the answer. See Sainz et al., [NLP Evaluation in trouble](https://arxiv.org/abs/2310.18018), and Yang et al. on [rephrased-sample contamination](https://arxiv.org/abs/2311.04850).

### Held-out final test

A family-disjoint test set that remains unavailable during development and method tuning. It is used only after the design is frozen so final performance is not selected around known answers. Protected benchmark custody is also motivated by Rajore et al., [TRUCE](https://arxiv.org/abs/2403.00393).

### Kubernetes

The benchmark domain used in the current experiment: an orchestration system with declarative API objects such as Pods, Deployments, Services, Jobs, and CronJobs. The pilot freezes Kubernetes `v1.36.4` source material so version-specific answers remain reproducible. [Kubernetes documentation](https://kubernetes.io/docs/home/).

### OpenAPI

A machine-readable description of HTTP APIs and schemas. The project keeps a frozen Kubernetes OpenAPI snapshot as schema evidence for artifact-validation tasks. [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).

### kind

Kubernetes IN Docker creates Kubernetes clusters using container nodes and is useful for controlled local integration tests. The planned interactive stratum can use it to test tool-driven diagnosis and repair against a real but disposable cluster. [kind documentation](https://kind.sigs.k8s.io/).

### TTFT and decode throughput

Time to first token (TTFT) measures startup/prefill latency before generation begins; decode throughput measures generated tokens per second after generation starts. Reporting both avoids hiding a slow startup behind a fast steady-state decoder or vice versa.

## Maintenance rule

When a new research-relevant algorithm, metric, tool, or technology appears in the repository, add a concise entry here or link to an existing one. Prefer the original paper for research methods and official documentation for technologies; explain only what the thesis actually needs.
