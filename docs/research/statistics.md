# Statistical Analysis Plan

## Analysis unit

The benchmark item is the principal independent unit. Repeated generations and paraphrases are nested observations, not extra independent items.

## Primary comparisons

For each task class, compare each pre-registered applicable condition with B0 and the strongest simpler constituent for combined systems. Secondary-model analysis tests transfer of selected contrast direction and effect, not a new leaderboard.

## Estimation

- report paired item-level differences with 95% confidence intervals;
- use stratified paired bootstrap intervals for aggregate bounded scores when appropriate;
- use mixed-effects logistic/ordinal/linear models for repeated binary, ordinal, or continuous outcomes, with item effects and pre-specified task strata;
- report absolute effect, relative effect where meaningful, and a practical effect-size interpretation;
- report quality–cost Pareto fronts rather than collapsing all outcomes into one arbitrary score.

## Stability analysis

Estimate retry-free item success, within-item variance/agreement, paraphrase range, and lower-quantile outcomes. Use hierarchical models or cluster bootstrap at item level so repeats do not inflate sample size.

## Multiple comparisons

Define a small primary contrast family per task class. Control family-wise error using Holm adjustment for confirmatory tests. Label all other analyses exploratory and emphasize intervals over thresholded significance.

## Missing and invalid observations

- preserve all run records;
- exclude only runs meeting frozen objective invalidity rules;
- report invalidity rates by condition;
- count model/runtime failures as task failures when they are part of the deployed system behavior, unless the run is invalid because measurement infrastructure failed;
- perform sensitivity analysis when exclusions could change conclusions.

## Pilot and sample size

Development-only pilot data estimates item difficulty, variance, correlation across conditions, annotation reliability, and runtime. Use it to set item and repeat counts against a pre-declared smallest effect of interest and compute budget. Do not use test outcomes for power tuning.

## Reporting

Every result separates:

- **FACT:** observed values;
- **STATISTICAL RESULT:** derived estimate, interval, or test;
- **INTERPRETATION:** plausible meaning;
- **LIMITATION:** unsupported inference or uncertainty.

## Unresolved decisions

- primary metric and smallest effect of interest per task class;
- final item and repeat counts;
- exact mixed-model distribution/link for each metric;
- engineering-effort rubric and whether it is descriptive or analyzed quantitatively.
