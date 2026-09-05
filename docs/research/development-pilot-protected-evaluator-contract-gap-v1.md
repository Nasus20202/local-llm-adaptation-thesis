# Development-pilot protected evaluator contract gap v1

## Status

Human Gate A blocker identified during implementation review on 2026-09-05. No 24-bundle authoring has been performed.

## Exact gap

The approved generic protected-evaluator implementation validates the structure of a contract, but its current records do not carry the protected scientific content required to assess an answer. `ProtectedCriterion` contains only an identifier, roles, alternative identifiers, predicate binding, and evidence IDs. `AcceptedSemanticAlternative` contains only an identifier, criterion identifier, and relation. `SemanticCriterion` contains only an identifier, anchor identifier, and assessor modes. The deterministic predicate record does not provide a governed expected result for predicate kinds that need one.

Therefore a contract can be structurally valid while failing to state what a criterion means, what counts as an equivalent alternative, what an observable semantic anchor is, what unsupported or contradictory content means, or which deterministic result is required. Authoring those fields in an adjacent unvalidated JSON document would bypass the approved contract hash, lineage, validation, and model-facing exclusion boundary.

## Required decision

Human approval is required for the smallest schema amendment that adds these answer-bearing protected definitions to the existing contract graph. The amendment must preserve the frozen 24 scenario inputs, Kubernetes `v1.36.4` source boundary, deterministic-first evaluator hierarchy, class-specific primary metrics, copying-neutral rules, and later semantic-judge gate.

Until that amendment is approved and implemented, the 24 bundles cannot honestly be reported as complete. No semantic judge, participant model, final-test material, training data, real `kind`, live W1, semantic-pair selection, or C2 selection was used to identify this gap.
