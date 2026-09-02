## 1. Shared pilot records and safety boundaries

- [ ] 1.1 Add versioned status, reason-code, immutable-identity, and append-only event models; verify unit tests reject unknown versions, mutable identities, collisions, and overwrite attempts.
- [ ] 1.2 Add protected-root references and redacted validation errors; verify tests prove model-facing serialization and error output never contain synthetic protected payload values.
- [ ] 1.3 Add deterministic canonical serialization/hashing for all new documents; verify repeated and key-order-varied inputs produce the expected stable hashes.

## 2. Development-only pilot dataset capability

- [ ] 2.1 Write failing tests and implement pilot manifest models for family/variant identity, development split, task class, language, answer contract, metric applicability, target stratum, and comparator; verify final-test declarations and nested-unit miscounts fail.
- [ ] 2.2 Implement the 24-family class/language composition validator from versioned policy; verify balanced metadata passes and every count/allocation deviation reports the affected rule without requiring item content.
- [ ] 2.3 Implement model-facing/protected evaluator bundle separation; verify golden/rubric/expected-result fixture markers are rejected from model-facing manifests while identity/hash references pass.
- [ ] 2.4 Implement contamination audit records for exact, normalized, token, code/configuration, semantic, and cross-language checks; verify direct leakage forces `STOP/DEFER`, unresolved semantic matches force `AMEND`, and numerical pre-training probabilities are rejected.
- [ ] 2.5 Implement derived pilot progression reports; verify individual criterion statuses are preserved, safety/leakage red governs overall progression, and method-win/final-test fields are rejected.
- [ ] 2.6 Implement C2 eligibility/comparator freeze validation; verify confirmatory C2 accepts only pre-outcome model-independent metadata and a design-time comparator, outcome-selected pilot C2 is marked exploratory, and confirmation requires a fresh family-disjoint manifest.

## 3. Evaluator and calibration capability

- [ ] 3.1 Write failing tests and implement immutable evaluator/fixture/input/output identity records; verify changed evaluator inputs create a new derived identity and never mutate raw or prior records.
- [ ] 3.2 Implement deterministic fixture qualification for positive, negative, boundary, malformed, and ambiguous classes; verify 100% idempotent outcomes produce `GO`, mismatches block qualification, and unresolved ambiguity routes to rejection/human review.
- [ ] 3.3 Implement task-specific atomic rubric validation with three-level ordinal anchors and separate critical binary labels; verify vague, conflated, or incomplete criteria fail before rating.
- [ ] 3.4 Implement blinded independent rating import and append-only adjudication; verify unblinded qualification records, missing independence declarations, and overwritten ratings fail while unresolved labels remain available.
- [ ] 3.5 Implement exact/adjacent agreement, nominal/ordinal Krippendorff alpha, family-clustered seeded intervals, and green/amber/red decisions; verify calculations against fixed non-domain fixtures and boundary-threshold cases.
- [ ] 3.6 Implement frozen invalidity classification and all-fail/complete-case sensitivity inputs; verify malformed answers, refusals, budget exhaustion, evaluated-system timeouts, and remediation failures remain valid failures while capture/hash/infrastructure failures are invalid.
- [ ] 3.7 Implement supplemental-judge policy validation; verify an uncalibrated or sole-primary judge configuration is rejected and a frozen qualified supporting judge is accepted.

## 4. Controlled cluster-task capability

- [ ] 4.1 Define the narrow process/container adapter and deterministic fake state machine; verify routine tests exercise reset, actions, denials, timeouts, and validator outcomes without creating a real cluster.
- [ ] 4.2 Implement pinned environment and prerequisite validation; verify mutable node/workload tags, missing digests, and unresolved host/runtime identity fail before external execution.
- [ ] 4.3 Implement reset plus initial-state verification and append-only attempt directories; verify mismatched state/hash invalidates an attempt before actions and a retry receives a new identity.
- [ ] 4.4 Implement namespace, command, privilege, permission, egress, action/output/time budget enforcement in the adapter boundary; verify positive and deny fixtures fail closed and capture every requested action.
- [ ] 4.5 Implement matched neutral-policy comparison across applicable conditions; verify any extra permission, action, observation, context, output, or time budget fails comparison before execution.
- [ ] 4.6 Implement final-state validator records and feasibility qualification; verify fixture classes, ten-reset/ten-deny summaries, duration thresholds, and mandatory `STOP/DEFER` on isolation or privilege failure.
- [ ] 4.7 Add an explicit opt-in real-`kind` qualification entry point with prerequisite/help output only; verify the default test and import paths cannot start a cluster, pull images, or modify host networking.

## 5. Official-source W1 capability

- [ ] 5.1 Define search/fetch provider interfaces and a deterministic fake; verify routine tests simulate ranking, redirects, errors, unavailable versions, and malicious targets without network access.
- [ ] 5.2 Implement explicit W1/combined-condition validation and R1/H1 web denial; verify implicit web access fails with a policy reason.
- [ ] 5.3 Implement path-aware allowlist, redirect revalidation, local/private-address denial, and thesis/benchmark/golden denial; verify bypass forms and redirect chains fail before protected content is read.
- [ ] 5.4 Implement per-response search/result/fetch/tool/token/time budgets; verify exact boundaries pass, the next over-budget request is denied, and exhaustion remains a captured valid W1 failure.
- [ ] 5.5 Implement write-before-expose retrieval provenance and lawful body/reference handling; verify missing capture prevents context exposure and unavailable provider version is recorded as `not_exposed`.
- [ ] 5.6 Implement source-drift precheck and W1 feasibility report; verify changed/unavailable source defers execution, complete safe attempts calculate availability, and any provenance/access failure forces `STOP/DEFER`.
- [ ] 5.7 Add an explicit opt-in provider qualification entry point; verify default tests and imports cannot contact an external service.

## 6. Cross-capability verification and handoff

- [ ] 6.1 Add synthetic schema examples that contain no Kubernetes benchmark scenario, evaluator expected answer, golden, credential, or external endpoint; verify example validation succeeds and content scans enforce the exclusion.
- [ ] 6.2 Add focused integration tests from pilot manifest through fixture/calibration/progression records using only synthetic fakes; verify no model, real cluster, network, or final-test path is invoked.
- [ ] 6.3 Document the protected/model-facing roots, opt-in boundaries, reason codes, versioning, and later runner-integration boundary; verify documentation links to the approved research protocol and does not duplicate or alter scientific thresholds.
- [ ] 6.4 Run formatting, linting, typing, full unit/integration tests, build, example validation, Renovate validation, and strict all-change OpenSpec validation; record exact commands and outcomes in the implementation PR.
- [ ] 6.5 Inspect the final diff against every Issue #4/OpenSpec scenario and verify that no benchmark/fixture payload, golden answer, model inference, RAG, QLoRA, harness/skill reasoning, real external run, or raw result was added.
