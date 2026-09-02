# Threats to Validity

## Internal validity

- **Hidden configuration differences:** chat templates, thinking mode, context truncation, sampling, or cache types may vary. Mitigation: hash and record all effective inputs; validate rendered prompts.
- **Unequal information access:** RAG, skills, harnesses, tools, or web access may contain answer-like content. Mitigation: explicit permitted-context manifests, matched raw tool permissions, contamination scans, and separately named combined conditions.
- **Harness/tool confounding:** a harness may appear better only because it has exclusive cluster access or a larger action budget. Mitigation: give all applicable conditions the same neutral raw interface, permissions, initial state, and budget; define H1 as orchestration/observation/verification behavior.
- **RAG/web confounding:** live web access can be mistaken for closed-corpus retrieval. Mitigation: keep R1 pinned and closed; label W1 sensitivity evidence and capture its allowlist, queries, ranks, pages, timestamps, and failures.
- **Language-dependent corpus changes:** translated or localized documents could change information access. Mitigation: keep the same pinned canonical English corpus in primary R1 and treat any translated corpus as a separate sensitivity condition.
- **Order and thermal effects:** condition order can change performance. Mitigation: randomize or counterbalance, warm consistently, and record clocks and temperatures where available.
- **Evaluator drift:** rubric or judge changes alter derived scores. Mitigation: freeze versions, qualify raters on disjoint fixtures, and regenerate processed results without changing raw outputs.
- **Development leakage:** prompt, adapter, skill, or harness decisions may overfit development families. Mitigation: immutable final test, family-disjoint training, decision logs, and no final-outcome access during pilot decisions.

## Construct validity

- “Quality,” “precision,” “stability,” and “engineering cost” are broad. Mitigation: task-specific operational definitions and multiple aligned metrics.
- Automated lexical metrics may punish valid paraphrases. Mitigation: deterministic semantic checks, atomic claim scoring, rubrics, and human calibration.
- Polish and English variants may differ because of adaptation quality rather than model ability. Mitigation: native authorship or human technical review, semantic-equivalence records, family-level analysis, and explicit translation-error adjudication.
- A successful static manifest edit may not imply live diagnostic ability. Mitigation: treat static and interactive variants as nested observation forms and restrict claims to the form actually tested.
- Cluster-final-state success may hide unsafe or wasteful actions. Mitigation: combine final-state validation with prohibited-action gates, action counts, and budget adherence.
- Search success may reflect ranking-provider behavior rather than adaptation. Mitigation: report W1 separately with full provenance and no generalization to other providers or dates.
- Harness and skill definitions may conflate orchestration with extra knowledge. Mitigation: component contracts, answer-leakage scans, matched information, and design-time-frozen strongest-constituent comparisons.

## External validity

- One Kubernetes workload domain, one computer, and two model families limit generalization. Mitigation: state the target population narrowly and use selected model-family replication.
- A small isolated `kind` cluster omits production scale, distribution-specific behavior, cloud services, and real incident pressure. Mitigation: limit claims to bounded workload diagnosis/remediation and keep operational generalization explicit.
- The official-source W1 allowlist omits community sources and general search. Mitigation: describe W1 as source-channel sensitivity, not a universal web-agent benchmark.
- Kaggle training hardware differs from local deployment. Mitigation: separate adaptation cost and evaluate exported artifacts only on target inference hardware.
- Results may not transfer to cloud-scale, proprietary models, vendor-specific Kubernetes behavior, or other technical domains. This is outside thesis scope.

## Conclusion validity

- Few independent families, correlated variants/repeats, and many contrasts can create unstable rankings. Mitigation: family-level paired analysis, cluster bootstrap, small preregistered contrast families, intervals, and Holm adjustment.
- **Post-outcome C2 selection:** choosing C2 eligibility or its comparator from pilot error analysis or scores biases the combined-condition contrast. Mitigation: freeze metadata-only eligibility and the comparator rule before outcomes; treat any outcome-selected pilot C2 as exploratory and require fresh family-disjoint families for confirmation.
- The 24-family pilot cannot establish method superiority. Mitigation: use it only for feasibility parameters and progression decisions.
- Stochastic outputs can invite favorable-run selection. Mitigation: deterministic manifests, frozen repetition rules, full raw retention, and frozen invalidity rules.
- Generic agreement thresholds can hide criterion-specific disagreement. Mitigation: report confusion tables, exact/adjacent agreement, Krippendorff alpha with uncertainty, and task/language cells.
- Timing noise can dominate small differences. Mitigation: isolated runs, warm-up, repeated measurements, and environment telemetry.
- A 60-family cap may leave small effects underpowered. Mitigation: freeze practically meaningful effects, simulate power, and reduce confirmatory claims rather than manufacture sample size with repeats.

## Reproducibility threats

- Mutable model branches, containers, websites, datasets, and search indexes. Mitigation: commit/digest/hash pinning, snapshots where lawful, UTC retrieval metadata, and explicit unknown provider versions.
- Upstream documentation and localizations can describe different releases. Mitigation: freeze exact source commits, compatible release metadata, included paths, and exclusions.
- `kind` reset or network behavior may depend on host runtime and firewall state. Mitigation: record the host/container environment and require repeated reset, validator, permission, and egress probes before admission.
- Live search rankings cannot be perfectly replayed. Mitigation: capture queries, ranks, pages/hashes, timestamps, budgets, errors, and treat provider variability as residual limitation.
- Driver or backend updates can change kernels. Mitigation: environment manifests and no silent upgrades after freeze.
- Hosted notebook quotas and images change. Mitigation: capture session environment and exported artifacts; do not rely on notebook availability for reproduction.

## AI-specific and contamination threats

- Public Kubernetes documentation is likely represented in some pre-training corpora, but opaque corpora prevent a defensible probability estimate.
- Exact overlap checks miss paraphrases, translations, semantically equivalent faults, and code/configuration structure; semantic checks have threshold-dependent false positives and negatives.
- Fresh private items reduce direct-item exposure but cannot prove absence of underlying concept or pattern exposure.
- W1 can retrieve benchmark-like or answer-bearing text if access controls fail.
- LLM judges can exhibit position, verbosity, self-preference, language, and model-family bias.
- AI-assisted item generation can reproduce public benchmark patterns or introduce plausible technical errors.

Mitigation distinguishes source/domain, semantic-pattern, and direct-item exposure; combines fresh source-transformed scenarios, private custody, exact/normalized/code/semantic/cross-language scans, human adjudication, web deny controls, calibrated evaluators, and the GenAI log; and never describes the benchmark as contamination-free.
