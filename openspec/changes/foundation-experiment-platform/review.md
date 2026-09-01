# Cross-Artifact Review

**Review date:** 2026-09-01
**Review status:** Ready for Human Gate A; implementation not authorized.

## Consistency matrix

| Proposal capability | Normative spec | Design coverage | Task coverage |
|---|---|---|---|
| `experiment-configuration` | Strict documents, minimum identities, contained references, dual hashes, side-effect-free validation | Configuration shape, safe YAML, project-root rule, canonical hashing | 2.1–2.5, CLI validation in 5.2 |
| `run-provenance` | Manifest, Git state, runtime facts, secret-safe paths | Schema module, Git digest, environment capture, canonical manifest | 3.1–3.5 |
| `run-lifecycle` | IDs, atomic creation, immutable manifest/events, inspection | Identity module, same-filesystem staging, append and validation policy | 4.1–4.5 |
| `command-line-interface` | Commands, JSON streams, exit codes, read-only inspection | `argparse`, application boundary, error taxonomy | 5.1–5.5 |
| Tooling/CI impact | Non-functional constraints across scenarios | Python 3.14/tooling, Renovate, and CI decisions | 1.1–1.5, 6.1–6.4, 7.1–7.3 |

## Review findings resolved

1. **Raw immutability:** changed the lifecycle from a mutable status manifest to one manifest plus append-only NDJSON events.
2. **Repeated runs:** separated unique run identity from deterministic configuration hashes so repetitions cannot collide.
3. **Dirty Git state:** formal preparation fails closed; exploratory preparation records a deterministic working-tree digest.
4. **Portability and privacy:** metadata paths are project-relative and references cannot escape the project root; manifests exclude environment values and absolute home paths.
5. **Configuration drift:** unknown and duplicate YAML fields, mutable revision sentinels, unsupported schema versions, and reference ID mismatches fail before persistence.
6. **Failure behavior:** CLI exit classes, staging cleanup, collision refusal, corrupt-event refusal, and inspection errors are explicitly specified and tasked.
7. **Unnecessary abstraction:** no provider/plugin layer, database, web service, model adapter, RAG, training, harness, skill, benchmark content, or telemetry sampler is included.
8. **OpenSpec syntax:** strict validation is the executable validation gate; no nonexistent legacy `verify` command is assumed.
9. **Toolchain freshness:** CPython 3.14.7 is pinned as the current stable runtime; Renovate uses semantic commits, covers Python, `uv`, supported PEP 621 dependencies and lockfiles, and GitHub Actions, and automerges patch/minor updates only after required checks. Major updates remain manual. OpenSpec upgrades are deliberate and include skill regeneration and review.

## Acceptance coverage

- Every requirement has at least one WHEN/THEN scenario.
- Every scenario maps to an implementation or verification task.
- The design contains no unresolved question that would alter scope, behavior, or task breakdown.
- Dependencies, security/privacy constraints, deterministic identity, and filesystem error behavior are explicit.
- No task authorizes model inference or experimental result creation.

## Review decision

The proposal, specifications, design, and tasks are internally consistent and strictly validate with the current reviewed OpenSpec CLI. Human approval may accept the package as written or request changes. Codex must not apply it before that approval.
