# Data Policy

## Data classes

- **Source data:** preserved copies or retrieval instructions for licensed source material.
- **Processed data:** deterministic transformations with code, configuration, and input hashes.
- **Corpus:** documents or chunks available to RAG conditions.
- **Benchmark:** task inputs, metadata, and split manifests.
- **Golden data:** protected references, evidence annotations, checks, and rubrics.
- **Training data:** material visible to the fine-tuning condition only.

## Approved source strategy

The Issue #2 benchmark uses a pinned subset of official Kubernetes upstream material:

| Source                  | Intended use                                                       | License basis                                           |
| ----------------------- | ------------------------------------------------------------------ | ------------------------------------------------------- |
| `kubernetes/website`    | Concepts, tasks, and references                                    | CC BY 4.0, subject to path-level review and attribution |
| `kubernetes/kubernetes` | Matching API schemas and source-controlled fixtures where required | Apache-2.0, subject to NOTICE and path-level review     |

The source manifest records repository, full commit ID, compatible Kubernetes release, path, retrieval date, SHA-256 hash, license, attribution, modification status, redistribution status, and role. Third-party pages linked from upstream are excluded unless their rights are reviewed independently.

Canonical English documentation is the primary source and RAG corpus for both Polish and English benchmark strata. Polish benchmark prose may be human-adapted from that source under the attribution and modification requirements. A translated corpus is not silently mixed into the primary condition.

## Required controls

- assign stable IDs and cryptographic hashes;
- record source, retrieval date, license or terms, attribution, modification status, and redistribution status;
- group semantic families, translations, paraphrases, and near-duplicates before splitting;
- maintain train, development, and final-test separation;
- freeze final-test input and golden manifests independently;
- restrict golden access from runners, retrieval indexes, prompts, skills, harnesses, training data, external services, and model-facing logs;
- retain scripts that reconstruct excluded payloads where legally possible.

## Split ownership and custody

The human researcher owns split assignment and is the final-test custodian. Split assignment occurs at scenario-family level before language variants or repeated observations are generated.

Before formal execution, final-test inputs and goldens remain outside the normal checkout and AI-accessible workspaces. Repository manifests may contain IDs, strata, hashes, and retrieval instructions without protected payloads. The formal runner receives test inputs without goldens; evaluation receives goldens through a separate read boundary. Access and freeze events are recorded.

A reviewer who sees protected material receives only the subset needed for annotation or adjudication and remains blinded to experimental condition. The same protected subset is not used for method development.

## Item and golden governance

Each item has one versioned answer contract, evidence mapping, deterministic checks where applicable, and a rubric only for qualities that cannot be checked mechanically. The contract is identical across compared methods.

Final items, translations, goldens, evidence mappings, and rubrics require human technical review. GenAI output may be a draft but is never accepted as the sole source or sole verification. Corrections create a new dataset version and preserve the prior manifest.

## Leakage and contamination review

Exact, normalized, and semantic-family scans cover train, development, final-test, corpus, prompt, skill, harness, tool-output, and fine-tuning inputs. Translation variants remain in one family and one split. Public-source pretraining exposure cannot be excluded for opaque models; this detection limit is reported rather than converted into a claim of cleanliness.

## Git policy

Commit small, redistributable manifests and fixtures. Do not commit model weights, credentials, personal data, final-test goldens, private university material, or third-party datasets without verified redistribution rights. Large or embargoed payloads stay outside Git and are referenced by immutable source plus hash.

## Corrections and versions

Never edit a frozen dataset silently. A correction creates a new dataset version, documents the reason and affected IDs, and invalidates or scopes comparisons as needed. Old manifests remain available.

## Raw results

Raw observations are append-only. Invalid runs retain their manifest, raw outputs where safe, objective invalidity reason, and superseding run ID. Derived data can be regenerated under a new evaluation or analysis version.

## Privacy and security

Do not send confidential, non-public, personal, embargoed test, or golden-answer data to external GenAI services. Redact logs before publication and treat prompt and model outputs as potentially sensitive until reviewed.
