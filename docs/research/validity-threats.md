# Threats to Validity

## Internal validity

- **Hidden configuration differences:** chat templates, thinking mode, context truncation, sampling, or cache types may vary. Mitigation: hash and record all effective inputs; validate rendered prompts.
- **Unequal information access:** RAG, skills, or harnesses may contain answer-like content. Mitigation: contamination scans and explicit permitted-context manifests.
- **Language-dependent corpus changes:** translated or localized documents could change information access. Mitigation: keep the same pinned canonical English corpus in the primary RAG condition and treat any translated corpus as a separate sensitivity condition.
- **Order and thermal effects:** condition order can change performance. Mitigation: randomize or counterbalance, warm up consistently, and record clocks and temperatures where available.
- **Evaluator drift:** rubric or judge changes alter derived scores. Mitigation: version evaluators and regenerate processed results without changing raw outputs.
- **Development leakage:** prompt or adapter decisions may overfit development items. Mitigation: immutable final test and decision logs.

## Construct validity

- “Quality,” “precision,” “stability,” and “engineering cost” are broad. Mitigation: task-specific operational definitions and multiple aligned metrics.
- Automated lexical metrics may punish valid paraphrases. Mitigation: deterministic semantic checks, rubrics, and human calibration.
- Polish and English variants may differ because of adaptation quality rather than model ability. Mitigation: native authorship or human technical review, semantic-equivalence records, family-level analysis, and explicit translation-error adjudication.
- Harness and skill definitions may conflate orchestration with extra knowledge. Mitigation: explicit component contracts and matched-information sensitivity tests.

## External validity

- One Kubernetes workload domain, one computer, and two model families limit generalization. Mitigation: state the target population narrowly and use selected model-family replication.
- Excluding live clusters improves control but may underrepresent operational state and timing. Mitigation: restrict conclusions to offline-verifiable configuration and diagnosis tasks.
- Kaggle training hardware differs from local deployment. Mitigation: separate adaptation cost and evaluate exported artifacts only on target inference hardware.
- Results may not transfer to cloud-scale, proprietary models, vendor-specific Kubernetes behavior, or other technical domains. This is outside thesis scope.

## Conclusion validity

- Few independent families, correlated language variants and repeats, and many contrasts can create unstable rankings. Mitigation: family-level paired analysis, hierarchical treatment of nested observations, pre-registered contrasts, intervals, and multiplicity control.
- Stochastic outputs can invite favorable-run selection. Mitigation: deterministic manifests, full raw output retention, and frozen invalidity rules.
- Timing noise can dominate small differences. Mitigation: isolated runs, warm-up, repeated measurements, and environment telemetry.

## Reproducibility threats

- Mutable model branches, containers, websites, and datasets. Mitigation: commit, digest, and hash pinning and source snapshots where licensing permits.
- Upstream documentation and localizations can describe different releases. Mitigation: freeze exact source commits, compatible release metadata, included paths, and exclusions.
- Driver or backend updates can change kernels. Mitigation: environment manifests and no silent upgrades after freeze.
- Hosted notebook quotas and images change. Mitigation: capture session environment and exported artifacts; do not rely on notebook availability for reproduction.

## AI-specific threats

- Public Kubernetes documentation may be present in model pretraining; opaque training corpora prevent proof of absence.
- Exact overlap checks miss paraphrases, translations, and semantic duplicates; semantic checks have threshold-dependent false positives and false negatives.
- LLM judges can exhibit position, verbosity, self-preference, language, and model-family bias.
- AI-assisted item generation can reproduce public benchmark patterns or introduce plausible technical errors.

Mitigation combines fresh source-transformed scenarios, version-specific facts, controlled configurations, human technical verification, benchmark provenance, cross-split semantic scans, judge calibration, and the GenAI audit log. Residual contamination is reported as a limitation; the benchmark is not described as contamination-free.
