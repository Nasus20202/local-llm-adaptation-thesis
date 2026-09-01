# Data policy

Tracked files in this directory are documentation, schemas, and deterministic manifests. Large, private, generated, or license-restricted payloads are excluded from Git and must be restored from recorded source instructions and verified hashes.

- `raw/`: source-preserving inputs; never edited in place.
- `processed/`: reproducibly generated transformations.
- `corpus/`: retrieval corpora and their manifests.
- `benchmark/`: benchmark tasks and split manifests.
- `golden/`: protected references unavailable to experiment conditions.

See [`docs/research/data-policy.md`](../docs/research/data-policy.md).
