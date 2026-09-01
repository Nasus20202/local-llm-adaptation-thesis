# Result policy

- `raw/` is append-only by convention. Every run receives a new immutable identifier.
- `processed/`, `tables/`, `figures/`, and `statistics/` are generated from raw observations and versioned analysis code.
- Invalid or failed runs remain recorded with an explicit status and reason.
- No thesis number should be maintained manually when it can be generated from validated results.

See [`docs/architecture/reproducibility.md`](../docs/architecture/reproducibility.md).
