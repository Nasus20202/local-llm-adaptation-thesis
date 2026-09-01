# Experiment Lifecycle

## Lifecycle states

1. **Designed:** the research question, comparison, metrics, controls, and validity risks are documented.
2. **Specified:** the corresponding software behavior is approved through OpenSpec.
3. **Frozen:** model, data, prompt, software, evaluation, and condition configuration identifiers are recorded.
4. **Prepared:** validation succeeds and a unique raw run directory plus immutable manifest are created.
5. **Running:** observations and lifecycle events are appended; external-process output is captured verbatim.
6. **Completed or failed:** a terminal event is appended. Failed runs remain in history.
7. **Evaluated:** a versioned evaluator produces derived data without editing the raw run.
8. **Analyzed:** predeclared statistics produce traceable tables, figures, and analysis artifacts.
9. **Integrated:** validated claims are incorporated into the Polish thesis with artifact references.

## Freeze contract

Before a formal run, record at minimum the Git SHA and dirty state, model repository/revision/artifact hash/quantization, backend version, generation settings, prompt hash, dataset manifest hash, evaluation version, applicable method configuration, hardware/software environment, and timestamps. Formal runs should normally require a clean repository; an exploratory run may be dirty only if its diff hash is recorded and the run is clearly classified.

## Run identity and immutability

A run ID identifies one execution attempt, not a condition. Repeated runs of the same experiment get distinct run IDs. Raw files are created exclusively and never replaced. Later lifecycle facts are appended as events. Corrections to evaluation create a new evaluation version and derived output.

## Valid and invalid runs

Run validity is determined only by predeclared rules such as missing output, parser failure, backend crash, timeout, or provenance failure. A low score is not grounds for invalidation. Invalid and failed attempts remain discoverable and are excluded only with a machine-readable reason.

## Gate ownership

- Work prepares research design, architecture, issue, and OpenSpec artifacts.
- The human researcher approves major specifications before implementation and reviews before merge.
- Codex implements and technically verifies approved behavior.
- Work performs scientific review before an experimental condition is accepted.
