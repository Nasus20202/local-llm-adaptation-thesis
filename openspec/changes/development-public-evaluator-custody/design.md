## Decision

Store development-only protected evaluator bundles in a dedicated tracked repository subtree, for example `data/benchmark/development/protected-evaluator/`. The subtree is public and answer-bearing by design, but it is not model-facing data.

The model-facing export, RAG corpus, training manifest, prompt/harness/skill inputs, W1 inputs, and participant run workspace MUST be generated from explicit allowlists that exclude the evaluator subtree. A model-facing role attempting to resolve an evaluator artifact MUST fail closed before reading it. CI MUST validate the exclusion and MUST reject accidental copies into model-facing paths, logs, artifacts, or generated documentation.

The existing protected artifact schema, exact SHA-256 references, source-evidence validation, lineage, deterministic-first scoring, and append-only event model remain authoritative. The physical binding changes from an external private runtime locator to a repository-relative binding under the dedicated evaluator subtree. Absolute locators remain forbidden.

Public repository storage does not authorize any final-test content. Final-test answers, fixtures, and locators remain forbidden until a separate final-test custody decision.

## Rationale

The relevant protection is process and data-flow separation from participant models, not secrecy from repository readers. Public storage improves reproducibility and removes an unnecessary private-storage dependency for a small thesis artifact set. The cost is that future contamination audits must treat evaluator truth as publicly discoverable and cannot claim that it was secret; this is acceptable because the thesis does not rely on evaluator-answer secrecy as a scientific outcome.

## Migration

1. Approve this amendment at Human Gate A.
2. Implement the repository-relative binding and model-facing exclusion checks.
3. Author and review the 24 bundles in the dedicated subtree.
4. Freeze hashes and provenance, then proceed to the separately gated semantic-judge package.
