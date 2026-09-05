## Why

The approved custody contract treats development evaluator answers as protected payloads that must remain outside the normal repository. That separation is disproportionate for this thesis: the Kubernetes answers are not confidential, and participant-model access can be prevented by keeping evaluator paths out of model-facing workspaces, prompts, retrieval corpora, training inputs, and serialization. The current rule created an operational blocker without adding meaningful secrecy value.

## What Changes

- Permit the development-only evaluator bundles and their protected review artifacts to be committed to this public repository under a dedicated non-model-facing path.
- Preserve immutable identities, hashes, lineage, source-evidence binding, review/freeze states, and append-only provenance records.
- Preserve fail-closed model-facing access: participant runners, retrievers, prompts, harnesses, skills, W1, and future-training processes must not resolve or receive evaluator paths or contents.
- Keep final-test material outside the repository and under a separate future final-test custody decision.
- Treat public repository storage as disclosure of evaluator truth, not as participant-model input; contamination and execution checks must verify that the evaluator subtree is excluded from model-facing artifacts and run workspaces.

## Scope

This amendment changes storage/disclosure policy only. It does not change the 24 scenarios, source release, metric families, evaluator hierarchy, judge gate, participant execution gate, training rules, final-test boundary, or C2/W1/kind decisions.

## Gate

Human Gate A is required before implementing the amended storage binding or authoring the 24 bundles.
