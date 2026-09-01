# Threats to Validity

## Internal validity

- **Hidden configuration differences:** chat templates, thinking mode, context truncation, sampling, or cache types may vary. Mitigation: hash and record all effective inputs; validate rendered prompts.
- **Unequal information access:** RAG, skills, or harnesses may contain answer-like content. Mitigation: contamination scans and explicit permitted-context manifests.
- **Order and thermal effects:** condition order can change performance. Mitigation: randomize/counterbalance, warm up consistently, record clocks and temperatures where available.
- **Evaluator drift:** rubric or judge changes alter derived scores. Mitigation: version evaluators and regenerate processed results without changing raw outputs.
- **Development leakage:** prompt or adapter decisions may overfit development items. Mitigation: immutable final test and decision logs.

## Construct validity

- “Quality,” “precision,” “stability,” and “engineering cost” are broad. Mitigation: task-specific operational definitions and multiple aligned metrics.
- Automated lexical metrics may punish valid paraphrases. Mitigation: deterministic semantic checks/rubrics and human calibration.
- Harness and skill definitions may conflate orchestration with extra knowledge. Mitigation: explicit component contracts and matched-information sensitivity tests.

## External validity

- One domain, one computer, and two model families limit generalization. Mitigation: state the target population narrowly and use selected replication.
- Kaggle training hardware differs from local deployment. Mitigation: separate adaptation cost and evaluate exported artifacts only on target inference hardware.
- Results may not transfer to cloud-scale or proprietary models. This is outside thesis scope.

## Conclusion validity

- Few items, correlated repeats, and many contrasts can create unstable rankings. Mitigation: item-level paired analysis, hierarchical treatment of repeats, pre-registered contrasts, intervals, and multiplicity control.
- Stochastic outputs can invite favorable-run selection. Mitigation: deterministic manifests, full raw output retention, and frozen invalidity rules.
- Timing noise can dominate small differences. Mitigation: isolated runs, warm-up, repeated measurements, and environment telemetry.

## Reproducibility threats

- Mutable model branches, containers, websites, and datasets. Mitigation: commit/digest/hash pinning and source snapshots where licensing permits.
- Driver/backend updates can change kernels. Mitigation: environment manifests and no silent upgrades after freeze.
- Hosted notebook quotas and images change. Mitigation: capture session environment and exported artifacts; do not rely on notebook availability for reproduction.

## AI-specific threats

- LLM judges can exhibit position, verbosity, self-preference, language, and model-family bias.
- Public benchmark or search-time contamination can inflate results.
- AI-generated references or code may be plausible but wrong.

Mitigation combines human verification, primary sources, judge calibration, benchmark provenance, semantic leakage scans, and the GenAI audit log.
