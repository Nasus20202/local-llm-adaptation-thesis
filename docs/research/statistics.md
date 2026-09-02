# Statistical Analysis Plan

## Analysis unit

The scenario/item family is the principal independent unit. Repeated generations, prompt formulations, language variants, and static/interactive variants are nested observations, not extra independent items.

## Primary estimand and comparisons

For each method, the primary estimand is the paired difference from its preregistered comparator in family-level mean primary outcome within the mechanism-aligned target stratum. Every applicable method is also compared with B0 across the complete applicable benchmark. S1 is compared with H1; C1 uses its frozen strongest constituent; C2 uses only a metadata-frozen eligibility manifest and design-time comparator for confirmatory inference; W1 remains sensitivity evidence.

The full target-stratum and comparator matrix is in the proposed [development-only pilot protocol](benchmark-pilot-protocol.md#preregistered-method-to-task-hypothesis-matrix).

C2 eligibility and comparator identity are frozen before any pilot output using model-independent family metadata and a design-time rule. If pilot error analysis is used to select complementary failures, the resulting pilot C2 contrast is exploratory; confirmatory C2 requires a fresh, family-disjoint family set and a new frozen manifest.

## Estimation and inference

- report paired absolute differences with 95% confidence intervals;
- use a task/language-stratified cluster bootstrap with 10,000 draws, resampling scenario families rather than nested observations;
- use paired randomization tests for the small confirmatory contrast family and Holm adjustment within task class;
- use outcome-appropriate mixed-effects logistic, ordinal, or linear models with family effects as sensitivity analyses for nested observations;
- report failed or singular models rather than substituting a favorable analysis;
- report quality–cost Pareto fronts rather than collapsing all outcomes into one arbitrary score.

## Smallest effects of interest

Pilot candidates are +0.10 atomic-claim F1 for knowledge, +0.15 end-to-end success probability for procedural tasks, and +0.10 normalized mixed-task score. The pilot may raise a threshold or reject a metric if measurement error makes it indefensible. It may not lower a threshold based on observed method deltas. Final values freeze before final-family construction.

Interpretation uses predeclared categories: clear practical benefit, promising but uncertain, detectable but below the practical threshold, inconclusive, and clear regression. The exact interval rules are defined in the [protocol](benchmark-pilot-protocol.md#interpretation-categories). Zero and negative effects remain valid results.

## Stability analysis

Estimate retry-free item success, within-family variance/agreement, paraphrase range, and lower-quantile outcomes. The pilot uses five stochastic generations and three semantic formulations on one balanced family per task-class/language cell. The final default is five generations and three formulations; increase generations to seven only under the protocol's Monte Carlo-error and compute-budget rule.

## Multiple comparisons

Define a small primary contrast family per task class. Control family-wise error using Holm adjustment for confirmatory tests. Label method interactions, most subgroup analyses, and all unplanned analyses exploratory; emphasize estimates and intervals over thresholded significance.

## Missing and invalid observations

- preserve all run records;
- exclude only runs meeting frozen objective invalidity rules;
- report invalidity rates by condition;
- count refusals, malformed outputs, tool-budget exhaustion, evaluated-system timeouts, and runtime failures as task failures when they are part of deployed behavior;
- treat capture, hash, required-provenance, or evaluator-infrastructure failure as invalid;
- report complete-case and all-fail bounds when exclusions could change a conclusion.

## Pilot and final sample size

The development-only pilot contains 24 independent families and estimates feasibility parameters, not method superiority. Final family counts are selected through simulation using pilot nuisance estimates, candidate smallest effects, 80% power, two-sided alpha 0.05, and Holm adjustment. The cap is 60 final families, balanced as 20 per task class and 10 per language within class.

If that cap cannot power the target contrast, the study reduces confirmatory claims and reports estimation honestly. It does not inflate the independent sample with repeats, inspect final outcomes for power tuning, or lower the target effect to manufacture a positive result.

## Evaluator reliability

Report exact and adjacent-category agreement plus nominal or ordinal Krippendorff alpha with a family-clustered 95% bootstrap interval. Reliability thresholds are pilot progression rules and are interpreted with their uncertainty, confusion pattern, and task/language cells rather than as context-free labels.

## Reporting

Every result separates:

- **FACT:** observed values;
- **STATISTICAL RESULT:** derived estimate, interval, or test;
- **INTERPRETATION:** plausible meaning;
- **LIMITATION:** unsupported inference or uncertainty.

## Freeze boundary

The Issue #4 package proposes these rules for Human Gate A. No method result, pilot observation, or final-test outcome has been generated. Final metric details and sample counts become immutable only in an approved freeze manifest after development-only pilot review.
