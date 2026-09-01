# Reproducibility Architecture

## Reproducibility levels

- **Inspectability:** a reviewer can understand the condition and see raw observations.
- **Computational repeatability:** the same environment and artifacts can repeat the run.
- **Analytical reproducibility:** processed results, statistics, tables, and figures can be regenerated from raw runs.
- **Replicability:** a selected conclusion can be tested on the secondary model family.

## Minimum run manifest

Every valid run must eventually include:

- schema version, run ID, experiment ID, and condition ID;
- Git commit, clean/dirty state, and diff hash when dirty;
- model repository, revision, artifact hash, quantization, and chat-template identity;
- backend name/version/build identity and generation configuration;
- prompt, dataset, evaluation, and method-specific identifiers and hashes;
- hardware configuration and observed software environment;
- start/end timestamps, seed where meaningful, and lifecycle outcome;
- hashes of raw request/response artifacts.

The foundation change implements only identities already required for provenance-only run preparation. Later method fields require reviewed schema evolution. A manifest is rejected if unknown fields could be silently ignored.

## Hashing

Use SHA-256. Preserve a byte hash for the source file and a semantic hash of canonical validated JSON for configuration. Canonicalization sorts object keys, uses UTF-8, and uses a stable compact JSON representation; lists remain ordered. Hashes prove identity, not trustworthiness.

## Environment capture

Record the platform, Python and package versions, backend revision, Mesa/RADV/Vulkan facts, CPU, RAM, and GPU where available. Automatic hardware probing is deferred until its interfaces are specified; the foundation records validated hardware metadata and the environment it can determine safely.

## Reproduction bundle

A future release bundle should contain configs, manifests, source revision, dependency lock, evaluator version, derived scripts, and checksums. It must refer to externally hosted weights/datasets when redistribution is prohibited.

## Non-guarantees

Exact token-for-token replication can be impossible across drivers or backend kernels even with a fixed seed. The project therefore records environment and repeated-run distributions instead of claiming determinism that the stack does not provide.
