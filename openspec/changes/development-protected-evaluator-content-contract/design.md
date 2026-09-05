## Decision

Add the missing protected semantic content to the existing `ProtectedSemanticContract` graph. The implementation must keep answer-bearing definitions inside the hashed protected artifact and must continue to expose only safe identity/integrity metadata through model-facing records.

The amendment should introduce the smallest cohesive records needed for:

- criterion meaning and assessment boundary;
- accepted semantic alternative meaning and relation to one criterion;
- observable semantic anchor and its allowed assessor modes;
- unsupported/contradictory claim meaning;
- construct-critical exactness where exact values, structures, or relationships are part of the task;
- the expected governed result for deterministic predicates whose current fields do not already encode it.

The existing `ProtectedCriterion`, `AcceptedSemanticAlternative`, `SemanticCriterion`, and `DeterministicPredicate` identities remain the binding points. Existing score configuration IDs and weights remain authoritative; no new default weighting or lexical feature is introduced. The score kernels remain unchanged unless validation of the completed contract proves that a field cannot be represented without a narrow, approved kernel change.

## Required validation

Contract validation must fail closed when:

1. a score-affecting criterion has no protected semantic definition or exactness boundary;
2. a semantic criterion has no observable anchor;
3. an accepted alternative has no semantic meaning or is represented only by preferred wording;
4. an unsupported/contradictory criterion has no declared claim boundary;
5. a deterministic predicate lacks the expected governed result required by its predicate kind;
6. any new answer-bearing field contains the reviewer-convenience note marker;
7. a definition is not reachable through the contract's hashed artifact and lineage;
8. a model-facing serialization attempts to include any new answer-bearing field.

The amendment must preserve validation against the approved 24-input registry and the frozen Kubernetes v1.36.4 source inventories. Every score-affecting definition remains mapped to one or more `SourceEvidenceReference` identities. No source text, reviewer note, model output, or judge result is accepted as a substitute for the frozen source registry.

## Non-goals

This amendment does not select or execute a semantic judge, create human-labelled qualification responses, create concrete fairness response pairs, set judge thresholds, run participant models, create training data, access final-test material, run real `kind`, run live W1, select semantic pairs, or select C2 families.
