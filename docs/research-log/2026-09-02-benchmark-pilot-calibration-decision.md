# Research Log: Benchmark Pilot and Evaluator Calibration

- **Date:** 2026-09-02
- **Issue:** [#4](https://github.com/Nasus20202/local-llm-adaptation-thesis/issues/4)
- **Status:** Proposed for Human Gate A

## Question

What smallest development-only pilot can test benchmark and evaluator feasibility, expose method-aligned signal opportunities, and govern controlled live-cluster and official-web sensitivity conditions without constructing or tuning on final-test material?

## Search and evidence review

The review screened 182 returned candidates across four workstreams: evaluator reliability and human-evaluation reporting; paired NLP statistics and power; pilot progression rules; and contamination, interactive environments, and web provenance. Duplicate, clinical-only, vendor-promotional, broad agent-leaderboard, and unvalidated commentary sources were not used to set thesis claims.

The selected evidence supports four conclusions:

- paired and nested evaluation needs family-level inference, uncertainty intervals, and explicit power limits rather than treating repeats as independent;
- human evaluation needs named constructs, anchored criteria, blinded independent scoring, agreement uncertainty, and a revision path rather than a single arbitrary kappa value;
- pilot success should be judged against preregistered feasibility criteria, not method-effect significance;
- exact matching and private custody reduce different contamination risks but cannot prove absence of semantic, translated, or parametric exposure.

Primary sources are linked in [the protocol](../research/benchmark-pilot-protocol.md#evidence-basis) and mapped in the [literature evidence table](../literature/evidence-table.md).

## Decision synthesis

The proposed design uses 24 development-only families, balanced across three task classes and two languages. It separates evaluator fixtures from benchmark families, makes deterministic checks precede human scoring, and qualifies the human rubric on a disjoint response set. Method targets are preregistered by mechanism, while zero and negative effects remain valid.

The controlled `kind` stratum is deliberately small and paired with static variants. Its inclusion depends on reset, isolation, permission, egress, validator, and runtime checks. W1 is a separate official-source sensitivity condition with an allowlist, fixed budgets, complete capture, and explicit source-drift limits. Neither capability is silently folded into H1 or R1.

## Limitations and unresolved implementation work

Agreement thresholds are progression criteria, not universal definitions of quality. The 24-family pilot cannot estimate small method effects precisely. Public Kubernetes exposure remains unknowable for opaque pre-training corpora. Live search ranking cannot be recreated perfectly, and `kind` isolation must be demonstrated on the eventual host.

The accompanying OpenSpec package resolves the observable validation, custody, evaluator, cluster, and web-boundary behavior needed for implementation while leaving internal class/library choices to Codex. Stable CLI integration with the existing runner remains a later change. No item, fixture payload, golden, model output, or software implementation was produced in this decision step.

## Protocol correction before Human Gate A

The initial draft allowed C2 applicability to be identified from pilot error analysis while comparing C2 with its strongest constituent. That is outcome-informed selection. The protocol now freezes C2 eligibility and comparator identity from model-independent family metadata and a design-time rule before any pilot output. Any error-analysis-selected pilot C2 result is exploratory, and confirmatory C2 requires a fresh, family-disjoint development-family set with a new frozen manifest. No pilot outcome exists, so this correction changes the preregistration safeguard, not an empirical result.
