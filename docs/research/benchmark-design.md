# Benchmark Design

## Purpose

The benchmark must reveal which adaptation mechanisms help which task types without giving any condition privileged access to answers. It is not a general foundation-model leaderboard.

## Task classes

### Knowledge tasks

Questions require facts from a bounded, versioned domain corpus. Subtypes should include direct facts, evidence synthesis, negative/absent-answer cases, and distractor-heavy cases. RAG evaluation separates retrieval success from answer generation.

### Procedural tasks

Tasks require following a multi-step, explicit procedure, respecting constraints, selecting permitted tools/actions, and producing a verifiable result. They should not depend primarily on obscure factual recall.

### Mixed tasks

Tasks combine corpus knowledge with ordered procedure or structured output. They are reserved for justified combined-condition tests after individual components are understood.

## Domain options requiring human selection

1. **One coherent technical domain (recommended):** a bounded, licensable domain with factual documents and procedures. It maximizes internal validity and permits all three task classes.
2. **Two smaller domains:** improves external validity but doubles curation and risks confounding domain with task class.
3. **Synthetic controlled world:** maximizes leakage control and deterministic grading but weakens ecological validity.

Dataset construction must not begin until the domain, intended user, language balance, and licensing constraints are approved.

## Item contract

Every item eventually records:

- stable item ID and task class;
- source and license/provenance;
- train/development/test split;
- input and permitted context/tools;
- expected output contract;
- deterministic checks and rubric;
- reference evidence and answer, protected where needed;
- difficulty and failure-mode tags;
- paraphrase family ID when applicable;
- contamination review status.

## Split policy

- Training data supports F1 only.
- Development data supports prompt, retrieval, adapter, harness, skill, and evaluator decisions.
- The held-out test manifest and goldens are immutable after freeze.
- Near-duplicate and semantic-family grouping occurs before splitting.
- Sources used as RAG corpus are distinguished from labeled answers; retrieval of a source is allowed, retrieval of benchmark answer keys is not.

## Leakage controls

- search exact and semantic near-duplicates across splits;
- maintain source URLs, snapshots, timestamps, and hashes;
- avoid public benchmark answers where a new domain set is feasible;
- keep final goldens inaccessible to inference components;
- scan RAG chunks, skills, prompts, training data, and tool outputs for item/answer overlap;
- evaluate search-time contamination if any condition can use external search.

## Pilot before freeze

The pilot uses development-only items to estimate ambiguity, evaluator agreement, ceiling/floor effects, runtime, and variance. Pilot failures may change the draft benchmark; final-test failures may not.

## Open questions

- Which specialized domain and intended user scenario?
- Polish-only, bilingual, or controlled Polish-majority composition?
- Human-authored, transformed-source, synthetic, or mixed item creation?
- Required human annotation count and adjudication procedure?
- Minimum corpus coverage needed to classify RAG retrieval failures fairly?
