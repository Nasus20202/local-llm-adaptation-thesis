# Data Policy

## Data classes

- **Source data:** preserved copies or retrieval instructions for licensed source material.
- **Processed data:** deterministic transformations with code, configuration, and input hashes.
- **Corpus:** documents/chunks available to RAG conditions.
- **Benchmark:** task inputs, metadata, and split manifests.
- **Golden data:** protected references, evidence annotations, and rubrics.
- **Training data:** material visible to the fine-tuning condition only.

## Required controls

- assign stable IDs and cryptographic hashes;
- record source, retrieval date, license/terms, and redistribution status;
- group semantic/near duplicates before splitting;
- maintain train/development/test separation;
- freeze final test and golden manifests;
- restrict golden access from runners, retrieval indexes, prompts, skills, and harnesses;
- retain scripts that reconstruct excluded payloads where legally possible.

## Git policy

Commit small, redistributable manifests and fixtures. Do not commit model weights, credentials, personal data, private university material, or third-party datasets without verified redistribution rights. Large payloads stay outside Git and are referenced by immutable source plus hash.

## Corrections and versions

Never edit a frozen dataset silently. A correction creates a new dataset version, documents the reason and affected IDs, and invalidates or scopes comparisons as needed. Old manifests remain available.

## Raw results

Raw observations are append-only. Invalid runs retain their manifest, raw outputs where safe, objective invalidity reason, and superseding run ID. Derived data can be regenerated under a new evaluation/analysis version.

## Privacy and security

Do not send confidential, non-public, personal, or golden-answer data to external GenAI services. Redact logs before publication and treat prompt/model outputs as potentially sensitive until reviewed.
