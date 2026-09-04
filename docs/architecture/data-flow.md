# Data Flow

## Input classes

| Input                | Durable identity                                  | Storage rule                                          |
| -------------------- | ------------------------------------------------- | ----------------------------------------------------- |
| Model metadata       | Repository, revision, artifact hash, quantization | Metadata in Git; weights outside Git                  |
| Hardware metadata    | Versioned config plus captured runtime facts      | Config in Git; facts in run manifest                  |
| Dataset              | Dataset ID, revision, deterministic manifest/hash | Licensed metadata in Git; restricted data outside Git |
| Prompt               | Prompt ID, revision, content hash                 | Text and metadata in Git                              |
| Method configuration | Versioned RAG/training/harness/skill settings     | Git-tracked configuration                             |
| Evaluation           | Evaluator ID, version, rules/rubric hash          | Code/config in Git; outputs derived                   |

## Transformation rules

1. Configuration loading resolves metadata references relative to the experiment configuration and validates schema versions.
2. Run preparation hashes both source bytes and normalized validated content where relevant.
3. Execution writes the manifest before observations and appends outputs/events only inside a newly created run directory.
4. Evaluation reads raw runs and writes to a versioned processed namespace; it has no write access to raw observations by design.
5. Statistics read processed results and emit regenerable tables, figures, and reports.
6. Thesis sources reference generated artifacts or analysis summaries rather than duplicating editable numeric tables.

## Trust boundaries

- External model artifacts and datasets require license and checksum verification.
- Model output is untrusted data and must not alter configuration or execute tools implicitly.
- Human rubric labels require assessor identity/pseudonym, rubric version, and adjudication status.
- Proprietary LLM judgments, if used, are supplemental and must retain model/version/prompt/output provenance.

## Data minimization

Do not place credentials, private prompts, confidential university material, or personal participant data in run manifests. Record identifiers and hashes sufficient for audit while storing restricted material according to `docs/research/data-policy.md`.
