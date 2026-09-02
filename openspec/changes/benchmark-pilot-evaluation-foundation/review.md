# Cross-artifact Review

- **Issue:** [#4](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/4)
- **Date:** 2026-09-02
- **Gate:** Human Gate A pending
- **Strict OpenSpec validation:** passed locally for `benchmark-pilot-evaluation-foundation`

## Scientific traceability

| Issue #4 requirement | Authoritative research decision | Normative capability |
|---|---|---|
| Development pilot and task coverage | `docs/research/benchmark-pilot-protocol.md` — Units, partitions, and pilot size | `benchmark-pilot-dataset` |
| Method-to-task hypotheses and visible unbiased effects | Protocol — Preregistered matrix and Statistical decision rules | Dataset applicability/comparator and progression requirements |
| Deterministic fixtures, human rubric, blinding, agreement, adjudication | Protocol — Evaluator fixture and calibration design | `evaluation-protocol` |
| Repetition, paraphrase, invalidity, and sample-size rules | Protocol — Repetition and statistics; `docs/research/statistics.md` | Evaluation invalidity and dataset progression requirements |
| Controlled paired `kind` stratum | Protocol — Controlled interactive stratum | `controlled-cluster-tasks` |
| Official-source web-search sensitivity | Protocol — W1 condition | `web-search-sensitivity` |
| Contamination and custody | Protocol — Contamination controls; accepted data policy | Dataset audits plus protected boundaries in all capabilities |
| One-researcher feasibility and progression | Protocol — Pilot progression rules | Derived progression and opt-in external qualification |

## Boundary review

- R1 remains closed-corpus retrieval; W1 is separate.
- H1 has no implicit web access and no exclusive cluster permission.
- Static/interactive, language, paraphrase, and repeat observations remain nested by family.
- F1 targets recurring learnable behavior and is not treated as retrieval or live-state observation.
- C1/C2 require strongest-constituent comparisons and are not generated exhaustively.
- C2 eligibility and comparator identity are frozen from model-independent metadata before outcomes; an error-analysis-selected pilot C2 is exploratory and confirmatory C2 requires fresh family-disjoint families.
- Zero, negative, and inconclusive effects remain valid; no progression rule demands method improvement.
- Pilot decisions have no final-test input and cannot use final outcomes.
- Protected content is referenced by identity/hash and never copied into model-facing manifests, errors, examples, or W1.

## Scope review

The OpenSpec package adds only validation/evaluation records and neutral external-system boundaries. It explicitly excludes item/fixture payloads, goldens, source snapshots, models, inference, RAG, training, harness reasoning, skill content, real external execution in routine CI, and final-test access. Existing runner/CLI capabilities are not modified.

## Feasibility review

The research pilot is capped at 24 independent development families and 60 final families. A second rater is needed for bounded calibration and a 25% final reliability subset rather than every final response. Stability work is limited to a balanced subset. `kind` and W1 can be deferred independently if their safety/reproducibility gates fail. These limits preserve the core static benchmark for one MSc researcher.

## Consistency findings

No unresolved methodological or architectural contradiction remains within the package. Implementation details that can vary without changing behavior—module names, exact file paths, provider choice, host egress mechanism, and stable CLI integration—remain appropriately outside the specs. The host egress mechanism must be selected during implementation but cannot weaken the observable deny-probe requirements.

## Human Gate A decision requested

Approve, amend, or reject the research protocol, ADR-0009, and complete OpenSpec package as one decision. Approval authorizes only the tasks in `tasks.md`; it does not authorize benchmark payload construction or any real cluster, web, or model execution.
