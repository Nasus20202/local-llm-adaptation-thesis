## 1. Protected contract and custody records

- [x] 1.1 Extend the existing evaluation/pilot typed records with a protected semantic answer-contract schema that supports required claims, accepted alternatives, contract-declared unsupported/contradictory criteria, construct-critical exact rules, deterministic gates, task-specific semantic criteria/anchors, permitted assessor modes/config references, evidence references, class-specific score configuration, and binding to the approved family/input hash.
- [x] 1.2 Validate that protected contracts resolve only under `development-protected-evaluator-v1`, use safe root-relative references and exact SHA-256 identities, and reject unknown/mismatched roots, hashes, scenario bindings, schema versions, or unfrozen source identities.
- [x] 1.3 Integrate governed protected read/write/freeze/supersession/review/judge-assessment/adjudication/audit events with the existing append-only custody evidence abstractions without exposing protected payloads in exceptions or participant-model-facing serialization.
- [x] 1.4 Add explicit validation that human reviewer convenience notes cannot be declared as evaluator evidence or construction truth.

## 2. Deterministic score derivation

- [x] 2.1 Implement Knowledge criterion accounting by stable IDs and atomic-claim F1 as `2TP/(2TP+FP+FN)`, including no duplicate credit from repeated wording and fail-closed handling of unresolved primary semantic criteria.
- [x] 2.2 Implement binary Procedural end-to-end success from predeclared primary-required and prohibited criteria. Use deterministic predicates for mechanical constraints; when a protected semantic criterion is genuinely necessary, accept only a resolved assessment from the approved hierarchy (qualified judge, then human adjudication when required).
- [x] 2.3 Implement Mixed scoring with procedural hard gates first; any failed primary hard gate returns `0`, otherwise apply only the contract's explicit pre-frozen point table and positive normalizer to produce `[0,1]`. Provide no default weights.
- [x] 2.4 Implement a structured assessment/adjudication route that carries safe criterion identities/status and assessor/config identities only, prefers deterministic assessment where applicable, and emits no final primary score until all required primary assessments are resolved.
- [x] 2.5 Ensure the score-kernel API has no lexical-similarity, embedding-similarity, source-overlap, ROUGE/BLEU, edit-distance, n-gram, token-overlap, judge-confidence, or prose-similarity input that can affect score.

## 3. Qualified semantic judge and human adjudication records

- [x] 3.1 Add a model-agnostic semantic-assessment record/interface that can represent structured criterion dispositions from a separately qualified judge configuration without selecting or invoking a concrete judge model in repository tests or this implementation step.
- [x] 3.2 Add immutable judge-configuration records/validation for model/provider or artifact identity, backend/version where relevant, prompt/template hash, response schema, decoding/retry/failure configuration, protected input-contract identity, qualification-fixture identity, predeclared acceptance thresholds, and audit/suspension/requalification policy.
- [x] 3.3 Reject primary judge assessments when the exact judge configuration is unqualified, changed since qualification, outside its approved task/language/criterion scope, malformed, or inconsistent with its frozen protected bindings.
- [x] 3.4 Add judge-qualification records that capture criterion-level human agreement, disposition confusion counts/matrix, an optional agreement statistic such as Cohen's kappa when applicable, unresolved/schema failures, adjudications, fairness invariants, and a final qualified/non-qualified decision derived from predeclared thresholds.
- [x] 3.5 Add calibrated human-adjudication and blinded audit routing for predefined escalation/audit conditions. Validate that audit membership and judge suspension/requalification rules are frozen before participant-model outcomes are inspected.
- [x] 3.6 Keep exact judge selection and judge-model execution out of this implementation PR. A later human-approved freeze must supply the concrete judge configuration, protected human-labelled qualification fixtures, thresholds, and audit policy before judge qualification runs.

## 4. Fairness qualification

- [x] 4.1 Extend evaluator qualification records to represent protected metamorphic fixture groups and the required Knowledge/Mixed × Polish/English coverage without storing real Kubernetes fixture payloads in repository tests.
- [x] 4.2 Enforce equality for correct paraphrase/source-like/synonym-reordering variants, required degradation on affected criteria for technically wrong or missing-claim variants, and the rule that appended irrelevant source text never raises a primary score.
- [x] 4.3 Apply the required semantic relations both to the pure score kernel and to every enabled qualified semantic-judge scope; make any fairness-invariant violation prevent `GO` qualification with structured reason evidence.
- [x] 4.4 Add synthetic non-domain test groups that prove the scoring/qualification implementation itself is copying-neutral; keep actual Kubernetes fairness responses, human labels, and expected outcomes outside the normal checkout.

## 5. Evidence and protected-reference validation

- [x] 5.1 Validate criterion-level evidence mappings against the approved Kubernetes v1.36.4 source registry/inventory identities and immutable website/OpenAPI revisions without requiring source excerpts in public/participant-model-facing records.
- [x] 5.2 Verify safe protected-handle serialization exposes only permitted identity/integrity/assessor status fields and rejects answer-bearing claims, expected values, evidence relationships, rubric/criterion decisions, judge protected-input payloads, fixture expectations, recovery data, and absolute locators.
- [x] 5.3 Add successor/version validation so a protected evaluator or qualified judge correction cannot overwrite a frozen artifact and forces a new identity for derived evaluations.

## 6. Verification and handoff

- [x] 6.1 Add decisive unit tests for every new invariant, including malformed contracts, hash/input mismatch, denied protected access, safe diagnostics, assessor hierarchy, unqualified/changed judge configuration, unresolved semantics, post-hoc audit selection, Knowledge edge cases, Procedural failures, Mixed hard gates, point-table validation, judge qualification decisions, and fairness violations.
- [x] 6.2 Reuse the existing evaluator/pilot modules and abstractions; do not add a database, service, generic annotation framework, embedding/NLI similarity matcher, concrete judge-provider integration, stable end-user CLI integration, or unrelated refactor.
- [x] 6.3 Run the complete relevant repository checks, including formatting, static analysis/tests, and `./node_modules/.bin/openspec validate --all --strict --no-interactive`; record exact verification evidence in the implementation PR.
- [x] 6.4 Confirm the implementation contains no protected Kubernetes answer contracts, source-answer mappings, real human-labelled/judge fairness fixture payloads, participant-model outputs, concrete judge-model execution/configuration selection, training/final-test material, real `kind`/W1 execution, or changes to the approved 24 scenario inputs.
