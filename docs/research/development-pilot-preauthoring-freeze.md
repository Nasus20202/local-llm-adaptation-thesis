# Development-pilot Pre-authoring Custody and Metadata Freeze

## Gate status

- **Freeze ID:** `development-pilot-preauthoring-freeze-v1`
- **Policy:** `pilot-policy-v1`
- **Issue:** #35
- **Decision state:** approved and frozen
- **Human approval:** recorded on PR #42 on 2026-09-04 for head `22ba5b6ab1a8b16b78e7eba00f889e27c89233cb`
- **Freeze commit:** `575fc4df4597c6b13ad3535e34474ddc455b4527`
- **Predecessors:** development-pilot authorization (PR #38), source/rights freeze `development-pilot-source-rights-v1` (PR #40), approved-state synchronization (PR #41)
- **Machine-readable ledger:** `development-pilot-preauthoring-freeze-v1.json`
- **Canonical semantic SHA-256:** `ce07a181086f8a1e7264f2b89f1da3fae06679709a5771fadee489f3e56c26a9`
- **Exact JSON-file SHA-256:** `74a3cec3cfdde9e4f78f204ad4880da1c6b8d1188c2587b96e7940a7c4b2a54c`

This package freezes only pre-authoring custody identities, safe evidence rules, empty development-family metadata, and already-approved condition/comparator declarations. It contains no scenario prose, question, prompt, expected answer, golden, answer-bearing hint, protected evaluator payload, final-test identity or payload, training example, or usable benchmark item. The human researcher approved this exact freeze; only the next sequenced development-only scenario-input authoring within the 24 frozen slots is now authorized.

## Basis and change classification

### Verified repository requirements

The accepted protocol and canonical specifications already require:

- exactly 24 independent `development` families: eight knowledge, eight procedural, and eight mixed; each class has four Polish and four English families;
- stable family identity and nested variants; variants never increase the independent-family count;
- one answer contract per family across compared conditions, class-appropriate metric applicability, explicit inapplicability rather than zero scores, and preregistered comparator/target-stratum metadata;
- protected expected results, evidence maps, rubrics, adjudication material, and goldens to remain outside the model-facing boundary and be referenced only by approved identity/hash;
- separate development, protected-evaluator, training, and final-test custody, with final-test material absent from this stage;
- append-only freeze/access/supersession/redaction/disclosure evidence and immutable hashes;
- B0/P1/P2/R1/F1/H1/S1/C1/C2 semantics and comparators from the accepted method-to-task matrix;
- C2 eligibility and comparator selection to be frozen before outcomes using only model-independent metadata and `strongest-constituent-v1`; outcome-informed selection is exploratory and confirmatory reuse requires fresh family-disjoint development families;
- real `kind` and live W1 to remain separate opt-in paths.

The exact source boundary is already frozen by `development-pilot-source-rights-v1`: Kubernetes `v1.36.4`, the approved `kubernetes/website` inventory, and the approved OpenAPI inventory. This package does not change that selection.

### Concrete project decisions frozen here

This gate freezes only the concrete identities needed before authoring: three logical custody roots, six access roles, four append-only evidence streams, 24 stable empty family IDs with coverage/source-role metadata, reusable condition profiles, and the explicit decision to select no optional `kind`, W1, or C2 families yet.

No new methodology, threshold, metric, comparator rule, source, release, condition meaning, or execution capability is introduced.

## Custody-root identities

Logical identities are stable project identifiers. Runtime filesystem, object-store, or secret bindings are deliberately not committed; a binding is later recorded as custody evidence without making a protected locator model-visible.

| Root ID                              | Logical identity                  | Current state                                                              | Model-facing resolution                                    |
| ------------------------------------ | --------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `development-model-facing-v1`        | `development/model-facing`        | metadata only at approval; scenario-input payloads absent before authoring | allowed only when the relevant later process is authorized |
| `development-protected-evaluator-v1` | `development/protected-evaluator` | identity only; no protected payload committed                              | **deny / fail closed**                                     |
| `future-training-v1`                 | `future-training`                 | sealed empty; no training material selected or created                     | **deny / fail closed**                                     |

No final-test root identity, placeholder, relative locator, payload hash, family ID, or resolvable reference is created by this package.

### Separation model

- A model-facing runner, retriever, prompt, harness, skill, or W1 process may resolve only `development-model-facing-v1`, and only after its own execution gate.
- `development-protected-evaluator-v1` is never indexed for RAG or training and is never supplied to prompts, skills, harnesses, W1, model-facing logs, or model-visible validation errors.
- `future-training-v1` is not a staging area for development material. It remains empty until a separate training-data authorization and must remain family-disjoint from development material.
- Runtime bindings for protected or future-training roots are private custody configuration. The repository may retain the logical root ID, root-relative protected reference when one later exists, artifact kind, status/reason code, and SHA-256; it must not retain a machine-specific absolute locator.

## Access roles

| Role                                                       | Development model-facing             | Protected evaluator                                                | Future training                                       |
| ---------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------ | ----------------------------------------------------- |
| `human-researcher-custodian`                               | read/write after this gate           | read/write only when the sequenced protected-authoring step begins | identity only until a separate training authorization |
| `development-author`                                       | read/write after this gate           | deny                                                               | deny                                                  |
| `evaluator-author-reviewer`                                | read                                 | read/write only during the protected-authoring/review step         | deny                                                  |
| `blinded-rater-adjudicator`                                | scoped input export only             | scoped rating/adjudication subset only                             | deny                                                  |
| `model-facing-runner-retriever-prompt-harness-skill-or-w1` | read-only when separately authorized | **deny / fail closed**                                             | **deny / fail closed**                                |
| `future-training-builder-or-trainer`                       | deny                                 | deny                                                               | disabled until separate training authorization        |

Access is least-privilege and purpose-bound. A denied read remains an append-only access event; a process does not fall back to another root or copy protected content into an error.

## Redaction, disclosure, and evidence

### Safe committed/model-facing fields

Only stable identifiers, root-relative protected references, artifact kind, source/provenance identities, status/reason codes, and SHA-256 hashes may cross from protected custody into committed or model-facing metadata.

Expected results, goldens, answer-revealing evidence maps, answer-revealing rubric anchors/decisions, adjudication prose revealing an answer, protected excerpts, redaction-recovery data, absolute protected locators, and any final-test locator/reference are forbidden.

If a review or error record would reveal an answer, the exposed representation uses a non-recoverable protected-redaction marker. The complete record remains only in protected custody. Hashes identify bytes; they are not a substitute channel for content.

### Append-only evidence streams

The following logical ledgers are frozen:

- `development-custody-provenance-v1`: root binding, acquisition, transformation, freeze, supersession;
- `development-custody-access-v1`: read, write, deny, export, disclosure;
- `development-custody-review-v1`: technical, rights, custody, redaction, and decision events;
- `development-custody-hash-v1`: content, manifest, binding, and derived-artifact hashes.

Every event records at minimum `event_id`, `event_type`, UTC timestamp, `root_id`, actor role, status, reason codes, and—when safe/applicable—artifact ID, SHA-256, parent-manifest ID, and superseded-event ID. Frozen events are never edited or deleted; a correction appends a successor/supersession event.

### Hashing

SHA-256 is the content identity. Semantic metadata hashes use the project's canonical JSON rule: UTF-8, sorted keys, no insignificant whitespace. Payload hashes use exact governed bytes before transformation. A transformation later records its input hash, configuration/identity hash, and output hash.

For this approved freeze, the semantic hash above covers the complete machine-readable pre-authoring ledger. The exact-file hash permits byte-for-byte verification of the committed JSON representation. The ledger remains byte-identical to the artifact approved on PR #42; its embedded `decision_state` therefore records the historical pre-approval proposal state of that immutable artifact rather than serving as the mutable post-approval project status.

## Empty 24-slot allocation

Abbreviations:

- **W-E** — `website-v1.36.4-development-pilot-v1` as human construction evidence.
- **W-R** — the same website inventory as a future R1 closed-corpus source; exposure still needs the later execution gate.
- **O-S** — `openapi-v1.36.4-development-pilot-v1` as machine-readable schema/reference evidence; it is not model-facing by default.
- **SR/W**, **SR/O** — provenance references into `development-pilot-source-rights-v1`.

Every row has `split=development`, `counts_as_independent=true`, and `construction_status=empty-preauthoring`. No language, static/interactive, formulation, or repeat variant exists yet.

| Family ID     | Class      | Lang | Coverage/subtype                         | Answer contract | Source roles  | Provenance | Condition profile          |
| ------------- | ---------- | ---- | ---------------------------------------- | --------------- | ------------- | ---------- | -------------------------- |
| `dev-k-pl-01` | knowledge  | pl   | `direct-evidence`                        | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-pl-02` | knowledge  | pl   | `synthesis`                              | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-pl-03` | knowledge  | pl   | `absent-answer-abstention`               | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-pl-04` | knowledge  | pl   | `distractor-heavy-evidence`              | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-en-01` | knowledge  | en   | `direct-evidence`                        | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-en-02` | knowledge  | en   | `synthesis`                              | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-en-03` | knowledge  | en   | `absent-answer-abstention`               | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-k-en-04` | knowledge  | en   | `distractor-heavy-evidence`              | `knowledge`     | W-E, W-R      | SR/W       | `knowledge-standard-v1`    |
| `dev-p-pl-01` | procedural | pl   | `diagnosis`                              | `procedural`    | W-E           | SR/W       | `procedural-structured-v1` |
| `dev-p-pl-02` | procedural | pl   | `constrained-repair`                     | `procedural`    | W-E, O-S      | SR/W, SR/O | `procedural-general-v1`    |
| `dev-p-pl-03` | procedural | pl   | `ordered-action`                         | `procedural`    | W-E           | SR/W       | `procedural-general-v1`    |
| `dev-p-pl-04` | procedural | pl   | `structured-artifact-schema-adherence`   | `procedural`    | W-E, O-S      | SR/W, SR/O | `procedural-structured-v1` |
| `dev-p-en-01` | procedural | en   | `diagnosis`                              | `procedural`    | W-E           | SR/W       | `procedural-structured-v1` |
| `dev-p-en-02` | procedural | en   | `constrained-repair`                     | `procedural`    | W-E, O-S      | SR/W, SR/O | `procedural-general-v1`    |
| `dev-p-en-03` | procedural | en   | `ordered-action`                         | `procedural`    | W-E           | SR/W       | `procedural-general-v1`    |
| `dev-p-en-04` | procedural | en   | `structured-artifact-schema-adherence`   | `procedural`    | W-E, O-S      | SR/W, SR/O | `procedural-structured-v1` |
| `dev-m-pl-01` | mixed      | pl   | `evidence-backed-configuration-decision` | `mixed`         | W-E, W-R, O-S | SR/W, SR/O | `mixed-standard-v1`        |
| `dev-m-pl-02` | mixed      | pl   | `evidence-backed-bounded-procedure`      | `mixed`         | W-E, W-R      | SR/W       | `mixed-standard-v1`        |
| `dev-m-pl-03` | mixed      | pl   | `evidence-backed-artifact-validation`    | `mixed`         | W-E, W-R, O-S | SR/W, SR/O | `mixed-standard-v1`        |
| `dev-m-pl-04` | mixed      | pl   | `evidence-backed-repair-plan`            | `mixed`         | W-E, W-R, O-S | SR/W, SR/O | `mixed-standard-v1`        |
| `dev-m-en-01` | mixed      | en   | `evidence-backed-configuration-decision` | `mixed`         | W-E, W-R, O-S | SR/W, SR/O | `mixed-standard-v1`        |
| `dev-m-en-02` | mixed      | en   | `evidence-backed-bounded-procedure`      | `mixed`         | W-E, W-R      | SR/W       | `mixed-standard-v1`        |
| `dev-m-en-03` | mixed      | en   | `evidence-backed-artifact-validation`    | `mixed`         | W-E, W-R, O-S | SR/W, SR/O | `mixed-standard-v1`        |
| `dev-m-en-04` | mixed      | en   | `evidence-backed-repair-plan`            | `mixed`         | W-E, W-R, O-S | SR/W, SR/O | `mixed-standard-v1`        |

This creates exactly 8/8/8 families and exactly 4 Polish plus 4 English families inside every class. No Polish/English semantic pair is selected.

## Answer and metric applicability

The class contracts are frozen from the accepted evaluation strategy; they do not contain expected answers.

| Class      | Permitted answer-form class                                              | Candidate pilot primary metric                            | Deterministic gate classes                                                                     | Supporting metric classes                              |
| ---------- | ------------------------------------------------------------------------ | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| knowledge  | concise prose or atomic claims with requested evidence references        | atomic-claim F1 on required/unsupported claims            | format; evidence identifier; answerability; exact facts when applicable                        | completeness; evidence correctness; abstention quality |
| procedural | YAML/JSON, patch, bounded action sequence, or structured diagnosis       | binary end-to-end task success                            | parse/schema; prohibited action; required constraint; static/final-state check when applicable | constraint adherence; step errors; schema validity     |
| mixed      | evidence-grounded decision plus verifiable artifact or bounded procedure | normalized task-specific score with procedural hard gates | artifact/state success; evidence/citation checks                                               | knowledge correctness; procedural success; cost        |

Metrics not meaningful for a later concrete family are recorded explicitly as inapplicable with a reason; they are never encoded as zero. Final primary outcomes still freeze only after the approved development-pilot evidence review.

## Condition profiles and target strata

The profiles are pre-outcome metadata only. `applicable` means scientifically valid for a later comparison; it does **not** authorize execution. `deferred` means the accepted mechanism could become applicable only after the named separate gate. All model execution remains closed.

| Profile                    | Applicable conditions | Mechanism-aligned targets | Deferred   | Explicitly outside this profile |
| -------------------------- | --------------------- | ------------------------- | ---------- | ------------------------------- |
| `knowledge-standard-v1`    | B0, P1, R1            | B0, P1, R1                | W1         | P2, F1, H1, S1, C1, C2          |
| `procedural-general-v1`    | B0, P1, F1            | B0, P1, F1                | H1, S1, C2 | P2, R1, C1, W1                  |
| `procedural-structured-v1` | B0, P1, P2, F1        | B0, P1, P2, F1            | H1, S1, C2 | R1, C1, W1                      |
| `mixed-standard-v1`        | B0, P1, R1, C1        | B0, R1, C1                | C2, W1     | P2, F1, H1, S1                  |

For `mixed-standard-v1`, P1 is applicable as the preregistered C1 constituent/comparator but is not promoted to the P1 mechanism-aligned target stratum. The JSON ledger preserves explicit reasons for every deferred or inapplicable condition.

### Frozen comparator/dependency rules

| Condition | Comparator(s) / selector                                                                                              | Dependency retained                                                                                                                                      |
| --------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B0        | B0 self-reference in validation metadata                                                                              | reference condition                                                                                                                                      |
| P1        | B0                                                                                                                    | none beyond later model-execution authorization                                                                                                          |
| P2        | P1 and B0                                                                                                             | only structured-diagnosis/taxonomy/output-schema target families                                                                                         |
| R1        | matched no-retrieval and B0                                                                                           | pinned closed corpus; later execution authorization                                                                                                      |
| F1        | B0 under the same inference contract                                                                                  | `future-training-v1` remains empty; training-data construction/training require separate authorization                                                   |
| H1        | B0-I                                                                                                                  | no family selected; separate `kind` family selection and opt-in required                                                                                 |
| S1        | H1                                                                                                                    | requires H1 applicability plus an approved reusable non-answer-bearing skill and its separate execution gate                                             |
| C1        | design-time strongest constituent under `strongest-constituent-v1`; constituents P1/R1; frozen selector order P1 → R1 | no outcome may select the comparator                                                                                                                     |
| C2        | no comparator instantiated because no C2 family is eligible in this freeze                                            | separate pre-outcome eligibility manifest must freeze the complete declared constituent set and filtered P1 → R1 → H1 → S1 selector before applicability |
| W1        | B0 and R1                                                                                                             | no family selected; separate W1 eligibility and live-access authorization required                                                                       |

The C2 state is deliberately `not-declared-in-this-freeze`, with zero eligible family IDs. This is not a negative C2 result. It preserves the already-approved choice that eligibility must be made from model-independent metadata before outcomes. If later pilot error analysis informs eligibility or comparator selection, that contrast is exploratory; confirmatory C2 then requires fresh family-disjoint development families linked to the exploratory manifest.

## Optional-stratum state

At this freeze:

- selected Polish/English semantic pairs: **0**;
- selected static/interactive `kind` families: **0**;
- W1-eligible families: **0**;
- C2-eligible families: **0**.

Later selection may use only the frozen model-independent metadata and the accepted rules. It may not use model scores, errors, rater disagreement, runtime behavior, or a desired method effect.

## Assumptions and unresolved risks

### Assumptions recorded, not silently promoted to facts

- The approved English source inventory is sufficient construction evidence for both Polish and English slots under the existing human-adaptation rule.
- No development scenario payload, protected evaluator payload, training material, or final-test material exists yet.
- Runtime custody bindings can be supplied later without weakening the logical separation or exposing absolute protected locators.

### Unresolved risks / later decisions

- The exact four optional procedural families, if any, for static/interactive pairing remain unselected.
- W1 family eligibility and allowlist revision remain unselected.
- C2 eligibility/constituents remain unselected; the rule is frozen, not an eligible stratum.
- Token-overlap and semantic contamination-detector implementations/thresholds remain a later calibrated freeze.
- Kubernetes-domain human evaluator calibration remains later.
- Future F1 training material remains absent.
- Repository-wide publication/licensing remains Issue #36 and is not expanded here.

## Authorization boundary

**Human approval is recorded:** PR #42 records explicit approval of this exact freeze at head `22ba5b6ab1a8b16b78e7eba00f889e27c89233cb`, and the approved change was squash-merged into `main` as `575fc4df4597c6b13ad3535e34474ddc455b4527`.

The next sequenced activity may author fresh **development-only scenario inputs** inside these 24 slots, using only the frozen source/rights boundary and `development-model-facing-v1` custody. Rejected inputs must leave append-only reason evidence and replacements remain inside the same predeclared slot.

Approval of this gate still does **not** authorize protected evaluator payload authoring out of sequence, model execution, formal experiments, training-data construction or training, any final-test action, a real `kind` cluster, live W1, outcome-selected C2, or experimental-harness implementation.

## OpenSpec assessment

**No OpenSpec change is necessary.** The synchronized `benchmark-pilot-dataset` specification already governs development-only identity/composition, answer/metric metadata, protected separation, contamination evidence, C2 freeze, and progression. `evaluation-protocol`, `controlled-cluster-tasks`, and `web-search-sensitivity` already govern the later evaluator, optional `kind`, and W1 boundaries. This package only instantiates concrete safe metadata and custody decisions inside those accepted contracts; it changes no observable software behavior.

## Human gate

**Decision: APPROVED.** The human researcher approved `development-pilot-preauthoring-freeze-v1` on 2026-09-04 exactly as committed at PR #42 head `22ba5b6ab1a8b16b78e7eba00f889e27c89233cb`; CI for that head was green, and PR #42 was squash-merged as `575fc4df4597c6b13ad3535e34474ddc455b4527`.

Recorded approval:

> I approve `development-pilot-preauthoring-freeze-v1` exactly as committed. This freezes the three logical custody roots, access/redaction/evidence rules, 24 metadata-only development slots, and existing condition/comparator/dependency declarations, and authorizes only the next sequenced authoring of development-only scenario inputs within those frozen slots; it does not authorize protected evaluator payloads out of sequence, model execution, training data or training, final-test material or access, a real `kind` cluster, live W1, outcome-selected C2, formal experiments, or harness implementation.

## Post-freeze evaluation clarification

On 2026-09-04 the human researcher explicitly approved `development-pilot-evaluation-clarification-v1`. The exact approved `development-pilot-preauthoring-freeze-v1.json` remains byte-identical; its historical wording is not rewritten. The clarification supersedes only the interpretation that a model answer must reproduce an evidence identifier, citation, source path, or URL.

For this development pilot:

- model answers do **not** require or score citations, source paths, evidence IDs, or URLs;
- source and retrieval provenance remain system/evaluator-side evidence;
- open prose is scored by semantic atomic claims and task-specific rubrics, not by lexical overlap with protected reference prose or Kubernetes documentation;
- semantically equivalent paraphrases receive equivalent credit; verbatim documentation receives no bonus;
- exact-string checks remain only where an exact technical literal or output format is itself part of the construct;
- the candidate primary metric families, condition profiles, comparators, source freeze, custody rules, optional-stratum state, and execution gates remain unchanged.

This clarification is recorded machine-readably in `development-pilot-evaluation-clarification-v1.json`.
