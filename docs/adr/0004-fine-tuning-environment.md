# ADR-0004: Fine-Tuning Environment

- **Status:** Proposed
- **Date:** 2026-08-31

## Context

The thesis must evaluate a fine-tuning family, but the local RX 5700/RDNA1 is not supported by the current practical QLoRA stack. Training need not occur on the inference computer, while final evaluation must.

## Considered alternatives

1. Local AMD training.
2. One Unsloth QLoRA pipeline on Kaggle NVIDIA GPU.
3. A raw Hugging Face PEFT/TRL pipeline.
4. Multiple equivalent pipelines.

## Proposed decision

Use one pinned Unsloth LoRA/QLoRA notebook on a recorded Kaggle P100 or T4 environment. Export an adapter or merged/quantized artifact that can be evaluated through the approved local backend. Use PEFT/TRL only as a documented fallback if Unsloth is blocked.

## Rationale

Current Unsloth AMD support omits RDNA1, while Kaggle exposes compatible NVIDIA accelerators. One pipeline controls engineering variability and keeps the comparison focused on adaptation rather than framework choice.

## Consequences

Training and inference costs are reported separately. Kaggle availability and quotas are external risks. A pilot must verify target modules, memory, export fidelity, chat template, and local load before this ADR can be accepted.
