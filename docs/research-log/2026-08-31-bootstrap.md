# Bootstrap Research Log — 2026-08-31

## Scope

Reviewed current primary sources for Gemma 4, Qwen3.5 and newer small-model availability, `llama.cpp`, Vulkan/RDNA1, Unsloth AMD support, Kaggle accelerators, OpenSpec, current WETI thesis materials, university GenAI guidance, and the core adaptation/evaluation literature.

## Outcome

- Retained Gemma 4 E4B IT QAT Q4_0 GGUF and Qwen3.5-9B as proposed candidates.
- Required a target-hardware smoke test before freezing either artifact.
- Rejected RX 5700 as the planned QLoRA training device based on current supported-hardware documentation.
- Proposed one pinned Unsloth/Kaggle pipeline with PEFT/TRL as a fallback.
- Initialized the current OpenSpec `spec-driven` Codex workflow.
- Recorded official 2026 WETI template links and GenAI disclosure obligations.

Detailed evidence and unresolved questions are in `docs/research/current-feasibility-review.md` and `docs/literature/evidence-table.md`.
