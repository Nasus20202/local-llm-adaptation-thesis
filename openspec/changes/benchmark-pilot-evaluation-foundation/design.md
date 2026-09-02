## Context

See [proposal.md](proposal.md) for motivation. The repository currently provides strict experiment-configuration identity and immutable prepared-run provenance but intentionally has no observation, dataset, evaluator, inference, retrieval, tool, or reporting pipeline. Issue #4 must add only the reusable pilot-validation foundations needed before any model run.

The research protocol requires protected-content separation, nested family semantics, calibrated human ratings, opt-in external systems, and deterministic routine tests. The implementation must remain readable by one MSc researcher and must not become a generic agent framework.

## Goals / Non-Goals

**Goals:**

- represent and validate development-only pilot metadata without storing item/golden payloads in examples or tests;
- produce immutable, explainable evaluator qualification, calibration, contamination, and progression records;
- isolate real cluster and web effects behind narrow opt-in boundaries whose routine tests use fakes;
- make unfair condition access, missing provenance, and protected-content routing fail before execution;
- keep derived evaluation/version behavior compatible with the existing immutable-run philosophy.

**Non-Goals:**

- model inference, prompt materialization, RAG indexing, QLoRA, harness reasoning, skills, or combined-condition execution;
- benchmark item, fixture payload, source snapshot, training record, model output, or final-test storage;
- an annotation UI, workflow server, database, Kubernetes operator, browser automation framework, or generic tool protocol;
- real `kind` or web execution in routine CI;
- deciding scientific thresholds dynamically from method wins.

## Decisions

### 1. Four narrow domain modules, no framework layer

Implement one focused module per capability: pilot metadata/custody, evaluation/calibration, controlled cluster execution, and W1 capture/access control. Shared code is limited to immutable identifiers, hashes, bounded append-only records, and explicit reason/status enums already justified across at least two capabilities.

Alternative: one generic workflow/agent engine. Rejected because it hides scientific distinctions, adds abstractions before inference exists, and makes H1/W1/R1 separation harder to audit.

### 2. Public manifests and protected evaluator bundles are separate roots

The pilot manifest contains family metadata, inputs only when later authorized, applicability, policy references, and protected artifact identities/hashes. Expected outcomes, evidence maps, rubrics, adjudication notes, and goldens live under a separately supplied evaluator root. Validation takes both roots explicitly when protected evaluation is needed and never copies protected payloads into model-facing artifacts or diagnostic output.

Tests use synthetic non-domain strings and hashes. Repository examples demonstrate schemas without answer-bearing content.

Alternative: one convenient dataset file containing inputs and answers. Rejected because it weakens custody, makes accidental prompt exposure likely, and cannot model the final execution boundary.

### 3. Typed canonical documents plus append-only event records

Use small typed YAML/JSON documents for versioned policy and manifests, following existing project validation and canonical hashing patterns. Use JSON Lines for ordered action, rating, adjudication, retrieval, and progression events. Every persisted document has a schema version; hash identity is calculated from canonical content excluding its own hash field.

Writers create a new versioned output path or use exclusive creation. They never replace prior evaluation or event files. Readers fail on unknown schema versions and return structured reason codes without printing protected content.

Alternative: SQLite. Rejected because the pilot volume is small, file review is useful, and a database adds migration and export work without scientific benefit.

### 4. Pure validation and statistics are separated from adapters

Composition, nesting, applicability, contamination-record, fixture, rubric, rating, calibration, invalidity, and progression logic are pure functions over typed data. Agreement and bootstrap routines accept a frozen seed and resample family IDs. External cluster/web adapters only return bounded normalized events; they do not decide scores or progression.

Alternative: calculate decisions inside CLI/process callbacks. Rejected because it couples scientific logic to unavailable external systems and weakens deterministic unit testing.

### 5. Neutral cluster executor is not H1

The cluster component is a minimal experimental instrument: validate a pinned environment; reset; check initial state; expose a fixed allowlist; enforce namespace/permission/action/output/time limits; append events; run the final validator; and destroy or quarantine the attempt. It does not plan, compress observations, select actions, maintain agent memory, or inject procedural advice. Those later behaviors define H1/S1.

Use an adapter protocol for process/container operations. The first implementation may target the approved local `kind` environment, but tests use a state-machine fake. External egress enforcement must be selected in the implementation design from a mechanism that works on the target host and verified by deny probes; passing an unenforced Kubernetes `NetworkPolicy` object is insufficient.

Alternative: give only H1 a cluster tool. Rejected because tool access would be confounded with orchestration. Alternative: allow arbitrary shell commands inside the node. Rejected for safety and reproducibility.

### 6. W1 uses a policy-enforcing proxy boundary

All search/fetch requests pass through one W1 boundary that validates the condition ID, destination/redirect, protected-context marker, and remaining budgets. It persists required provenance before returning text. The provider adapter exposes search and fetch only; it cannot read local files or benchmark stores. A deterministic fake supplies redirects, failures, ranking changes, budget exhaustion, and malicious destinations in tests.

Unknown provider versions are stored explicitly as `not_exposed`. Content is stored only where licensing permits; otherwise store an immutable URL/reference plus hash and the bounded text actually shown to the model.

Alternative: permit the harness to call a general browser. Rejected because it couples H1 to web access, broadens the attack surface, and cannot enforce reproducible budgets.

### 7. Calibration and progression are derived, never hand-edited

Raw independent ratings and adjudications are append-only. A calibration command or callable computes confusion tables, exact/adjacent agreement, Krippendorff alpha, a family-clustered interval with frozen seed, and the threshold status. A progression report consumes only approved feasibility summaries and records every criterion status. It rejects method-effect fields and final-test references.

The first implementation exposes these operations as callable domain services and versioned file outputs. Adding stable end-user CLI commands or integrating them with experiment execution requires a later delta to the existing command-line-interface/run capabilities.

Alternative: spreadsheet-only calibration. Rejected as the authoritative calculation because formula/version drift is difficult to audit; a generated CSV summary may still be provided later.

### 8. Scope the first implementation to validation and synthetic qualification

The OpenSpec tasks end when schemas, pure logic, fakes, safe adapters, and opt-in qualification entry points are tested. They do not construct the 24 families or run qualification against real `kind`, web, raters, or models. Those are later approved research operations using this foundation.

This separates software correctness from empirical feasibility and prevents simulated checks from being reported as observations.

## Risks / Trade-offs

- **[Four capabilities still create a sizeable change]** → Keep each module independent, prohibit inference/framework work, and split implementation commits/tasks by capability while preserving one reviewed scientific contract.
- **[Protected data could leak through validation errors]** → Errors contain identifiers, paths relative to approved roots, and reason codes only; never echo payload values.
- **[Agreement estimates are unstable on 24 qualification responses]** → Report clustered intervals and confusion patterns; thresholds drive revision, not a claim of universal reliability.
- **[Semantic contamination scanning can be nondeterministic]** → Record detector identity, threshold, seed/settings, candidate pairs, and human adjudication; never convert non-detection into proof.
- **[NetworkPolicy may not be enforced by the selected local network]** → Require demonstrated deny probes and treat any success as `STOP/DEFER`; the implementation may select a host/container boundary instead.
- **[Live search cannot be perfectly replayed]** → Capture every exposed result and explicitly label ranking/provider drift as a limitation.
- **[Opt-in adapters may require host privileges]** → Validate prerequisites, use least privilege, never run by default, and fail closed without modifying unrelated host state.
- **[A file-based design may later need indexing]** → Pilot scale does not justify a database; derived indexes can be added after measured need without changing canonical files.

## Migration Plan

1. Add schemas, validators, pure evaluators, and synthetic fixtures without changing existing experiment commands.
2. Add append-only writers/readers and verify collision, immutability, unknown-version, and protected-output behavior.
3. Add fake-backed cluster and W1 boundaries, then opt-in real adapter qualification entry points.
4. Validate the complete active change and run routine project checks without models, network, or a real cluster.
5. After independent review and merge, archive/synchronize the new capabilities. Constructing pilot payloads or executing empirical qualification requires the next explicit research authorization.

Rollback removes the new independent modules and artifacts; no existing manifest or run needs migration because no existing capability is modified.
