# ADR-0003: Local Inference Backend

- **Status:** Proposed
- **Date:** 2026-08-31

## Context

Formal evaluation must run locally on Fedora, RX 5700, Ryzen 5 3600, and 32 GB RAM. The selected backend must support GGUF, Vulkan, both candidate architectures, deterministic configuration capture, and measurable timing.

## Considered alternatives

1. `llama.cpp` with Vulkan.
2. Ollama as a higher-level service.
3. Transformers/PyTorch with ROCm.
4. CPU-only `llama.cpp`.

## Proposed decision

Use a pinned `llama.cpp` build with Vulkan as the formal local inference backend. Record its Git revision/build flags and the Mesa/RADV/Vulkan environment. Preserve CPU-only execution as a diagnostic reference, not a competing main condition.

## Rationale

`llama.cpp` directly supports GGUF, the official Gemma artifact, Qwen3.5 upstream, and AMD Vulkan without imposing an opaque service layer. RX 5700 is not a currently attractive ROCm training target.

## Consequences

A target-hardware correctness and memory smoke test is mandatory before acceptance. Backend upgrades after freeze require a new experiment configuration and ADR review; context and cache types cannot change silently.
