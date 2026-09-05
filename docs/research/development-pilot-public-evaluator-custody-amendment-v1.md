# Development-pilot Public Evaluator Custody Amendment v1

## Status

Proposed for Human Gate A. This amendment supersedes only the physical-storage and disclosure rule for **development-only evaluator material**. It does not rewrite the approved pre-authoring freeze JSON or change final-test custody.

## Decision requested

Allow the 24 development-only evaluator bundles, protected review report, and their answer-bearing evidence/fixture material to be committed under a dedicated repository subtree. The answers are not confidential thesis data, and the tested models will receive only the model-facing scenario export and permitted runtime inputs.

The repository must nevertheless enforce a separate data-flow boundary: evaluator files are excluded from model-facing exports, RAG/training manifests, prompts, skills, harness inputs, W1 inputs, participant run workspaces, ordinary logs, and diagnostics. The existing deterministic-first hierarchy, hashes, lineage, source binding, semantic-judge gate, and human review remain unchanged.

## Consequences

The project will no longer claim that development evaluator answers are secret or inaccessible to repository readers. This is acceptable because evaluator-answer secrecy is not a thesis outcome. Public availability must be recorded in contamination reports, and reproducibility improves because reviewers can inspect the exact contracts and source mappings.

Final-test material remains prohibited and must not be placed in this subtree. A later final-test custody decision remains required.

## Proposed approval

> I approve `development-pilot-public-evaluator-custody-amendment-v1`. Development-only evaluator bundles and review artifacts may be committed under the dedicated repository subtree. They remain excluded from model-facing exports, RAG, training, prompts, harnesses, W1 inputs, participant run workspaces, and ordinary logs. This does not authorize semantic-judge selection or execution, participant-model execution, training, final-test work, real `kind`, live W1, semantic-pair selection, or C2 selection.
