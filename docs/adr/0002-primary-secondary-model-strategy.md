# ADR-0002: Primary and Secondary Model Strategy

- **Status:** Proposed
- **Date:** 2026-08-31

## Context

The research variable is adaptation method, not foundation-model ranking. The target is an RX 5700 with 8 GB VRAM, while selected conclusions should be checked across model families.

## Considered alternatives

1. Gemma 4 E4B as primary and Qwen3.5-9B as secondary.
2. Qwen3.5-4B as primary for greater memory margin.
3. Multiple models across the full matrix.
4. A larger Qwen3.8 model with CPU offload.

## Proposed decision

Use the official `google/gemma-4-E4B-it-qat-q4_0-gguf` instruction model as the primary text-only candidate. Use Qwen3.5-9B for preselected replication contrasts. If Qwen3.5-9B fails the declared local feasibility threshold, require human approval before substituting Qwen3.5-4B. Freeze exact repositories, revisions, files, hashes, chat templates, and settings only after M0 smoke tests.

## Rationale

Gemma offers a first-party QAT GGUF with plausible 8 GB feasibility. Qwen supplies a distinct architecture and strong multilingual scope. Limiting replication preserves the adaptation-focused design and compute budget.

## Consequences

The E4B parameter accounting and QAT artifact must be described precisely. Multimodal projectors are excluded. The secondary result will test transfer of direction/effect pattern, not claim equal hardware cost or full model equivalence.
