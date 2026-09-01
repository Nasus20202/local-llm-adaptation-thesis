# Project Charter

## Identity

- **Author:** Krzysztof Nasuta
- **Degree:** Master of Engineering (`mgr inż.`)
- **Programme:** Computer Science, second-cycle full-time studies
- **Faculty:** Faculty of Electronics, Telecommunications and Informatics, Gdańsk University of Technology
- **Supervisor:** dr inż. Krzysztof Manuszewski
- **Thesis language:** Polish
- **Type:** theoretical-experimental
- **Polish title:** „Porównanie metod optymalizacji i dostosowania dużych modeli językowych pracujących w warunkach lokalnych”
- **English title:** “Comparison of Optimization and Adaptation Methods for Large Language Models in Local Environment”

## Immutable objective

The project compares approaches to optimization and adaptation of Large Language Models for specialized tasks when the resulting systems operate locally. The controlled experiment studies fine-tuning, Retrieval-Augmented Generation, prompt engineering, model harnesses, and skill-based mechanisms, and evaluates their effect on answer quality, precision, stability, and computational cost.

Changing this objective requires explicit approval from the author and supervisor.

## Purpose

The repository provides one traceable chain from literature and methodology through specifications, software, raw observations, analysis, figures, and the Polish thesis. It is both a research record and a small reproducible experimental platform.

## Goals

1. Define fair research questions and pre-specified evaluation methods.
2. Build a benchmark with knowledge, procedural, and mixed task classes.
3. Compare only adaptation conditions that answer a research question.
4. Run the main matrix on one primary model in the target local environment.
5. Replicate selected findings on a second model family.
6. Measure quality, reliability, inference cost, and engineering/adaptation cost.
7. Preserve enough provenance to reproduce or invalidate every reported run.
8. Generate thesis tables and figures from validated result data.

## Non-goals

- A broad leaderboard of foundation models.
- Exhaustive pairwise combinations of every method.
- Enterprise-scale serving, distributed orchestration, or a web product.
- Training all models on the target computer.
- Hiding negative, failed, or inconclusive results.
- Treating an LLM judge as the sole ground truth.

## Research philosophy

The unit of comparison is an adaptation strategy within a task class, not a model brand. Conclusions should have the form: “For task class X, strategy Y changed outcome Z at computational and engineering cost C under stated limitations.” Negative findings remain valid.

Evaluation design precedes method optimization. The final test partition and its references are immutable after freeze. Development errors are corrected through versioned datasets and new runs rather than historical rewriting.

## Target environment

- AMD Radeon RX 5700, 8 GB VRAM, RDNA1
- AMD Ryzen 5 3600
- 32 GB RAM
- Fedora Linux
- `llama.cpp` with the Vulkan backend as the default local inference candidate

Local inference is the target condition. External LoRA/QLoRA training is permitted when the exported adapter or model is evaluated on the target computer and adaptation cost is measured separately.

## Adaptation families

- **B0:** unaltered instruction-model baseline
- **P1:** engineered zero-shot prompt
- **P2:** structured or few-shot prompting when justified
- **R1:** RAG
- **F1:** LoRA/QLoRA adaptation
- **H1:** model harness
- **S1:** harness plus reusable skills
- **C1:** one justified simple combination, expected to be prompt plus RAG
- **C2:** best justified complete stack

These identifiers describe candidates, not an obligation to implement all conditions. A condition enters the frozen matrix only with a research question, fairness argument, and human approval.

## Success criteria

- Every reported claim is traceable to literature, a methodological decision, or versioned results.
- The main matrix isolates adaptation effects on one primary model.
- Repeated and paraphrased trials support stability analysis.
- Run manifests capture model, data, prompt, software, hardware, generation, and evaluation provenance.
- Routine tests validate scientific logic without loading a real model.
- Raw results are append-only and derived results are reproducible.
- The thesis satisfies current Gdańsk University of Technology/WETI requirements and transparently declares GenAI use.

## Constraints

- Engineering artifacts are English; thesis prose is Polish.
- Major scientific and architectural decisions require human approval.
- OpenSpec governs substantial software behavior.
- No model weights, credentials, private data, or large caches are committed.
- The system remains understandable and operable by one MSc student.
