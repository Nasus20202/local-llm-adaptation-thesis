# Current Research and Feasibility Review

**Review date:** 2026-08-31
**Decision horizon:** bootstrap only; model and training choices remain unfrozen until target-hardware smoke tests and human approval.

Labels in this report have strict meanings:

- **FACT:** supported by the linked primary or authoritative source.
- **ASSUMPTION:** plausible project-specific inference requiring measurement.
- **RECOMMENDATION:** proposed project action.
- **UNRESOLVED QUESTION:** decision or fact that must be closed before the affected freeze.

## Executive recommendation

- **RECOMMENDATION:** retain **Gemma 4 E4B Instruction-Tuned QAT Q4_0 GGUF** as the primary candidate because Google publishes a first-party `llama.cpp`-ready artifact that fits the 8 GB target at modest context lengths.
- **RECOMMENDATION:** retain **Qwen3.5-9B** as the selected secondary candidate for a limited replication. Newer Qwen3.8 is currently available at 27B rather than a comparable small size, and 27B is unsuitable for an 8 GB replication target.
- **RECOMMENDATION:** use `llama.cpp` Vulkan for local evaluation, pinned to a tested commit/container digest. Treat the advertised 128K/262K model contexts as capabilities, not feasible target settings.
- **RECOMMENDATION:** do not use the RX 5700 for the main QLoRA pipeline. Use one pinned Unsloth pipeline on an NVIDIA Kaggle P100 or dual-T4 session, export the adapter/model, and evaluate it locally. Keep Hugging Face PEFT/TRL as the fallback, not a second experimental pipeline.
- **RECOMMENDATION:** freeze none of these choices until the M0 hardware smoke-test issue records load success, maximum safe context, RAM/VRAM, throughput, output sanity, and exact hashes.

## 1. Primary model candidate: Gemma 4 E4B

### Facts

- **FACT:** Google released Gemma 4 in E2B, E4B, 12B, 26B A4B, and 31B sizes. E4B is a dense model with **4.5B effective parameters and 8B parameters including embeddings**, 42 layers, 262K vocabulary, 512-token sliding attention windows, and 128K advertised context. It uses Per-Layer Embeddings, so memory tracks total embeddings rather than the effective count alone. [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)
- **FACT:** the E4B model supports text, image, and audio inputs and generates text. It is pretrained on more than 140 languages and explicitly supports multilingual use. The experiment is currently text-only; multimodal support is not a reason to select it. [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)
- **FACT:** the official model card identifies the license as Apache-2.0. The exact license file and model revision must still be archived with the freeze manifest. [Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)
- **FACT:** Google estimates E4B inference memory for static weights plus 20% loading overhead at approximately 4.5 GB for Q4_0, excluding context KV cache and other runtime allocations. [Gemma 4 overview](https://ai.google.dev/gemma/docs/core)
- **FACT:** Google publishes `google/gemma-4-E4B-it-qat-q4_0-gguf`; the current Q4_0 GGUF is 5.15 GB and the optional multimodal projector is approximately 992 MB. The artifact is explicitly routed to `llama.cpp`/LM Studio. [Official GGUF repository](https://huggingface.co/google/gemma-4-E4B-it-qat-q4_0-gguf)
- **FACT:** Quantization-Aware Training checkpoints are intended to preserve quality better than ordinary post-training quantization at the target precision, but this is a vendor claim that the thesis must not treat as an experimental result. [Gemma 4 overview](https://ai.google.dev/gemma/docs/core#qat)

### Feasibility interpretation

- **ASSUMPTION:** text-only Q4_0 inference should fit into 8 GB VRAM at a modest context length if the multimodal projector is omitted. The 5.15 GB file size, allocator overhead, KV cache, Vulkan buffers, and Fedora desktop usage leave limited headroom.
- **ASSUMPTION:** 128K context is infeasible on the target and irrelevant to the planned benchmark. Context limits of 4K, 8K, and possibly 16K must be measured rather than inferred.
- **UNRESOLVED QUESTION:** does the official QAT Q4_0 artifact produce correct, stable text on the selected `llama.cpp` Vulkan build and RX 5700 driver stack?
- **UNRESOLVED QUESTION:** should thinking mode be disabled for all primary comparisons or treated as a fixed model-level control? It must not vary silently by condition.

## 2. Secondary model candidate: Qwen3.5-9B

### Facts

- **FACT:** `Qwen/Qwen3.5-9B` is an Apache-2.0 post-trained causal language model with a vision encoder, 9B language-model parameters, 32 layers, a hybrid Gated DeltaNet/attention layout, 262,144 native context, and claimed extensibility beyond one million tokens. [Official model card](https://huggingface.co/Qwen/Qwen3.5-9B)
- **FACT:** Qwen reports support for 201 languages and dialects, making it a reasonable cross-family Polish-capable replication candidate. [Official model card](https://huggingface.co/Qwen/Qwen3.5-9B)
- **FACT:** `llama.cpp` merged Qwen3.5 dense and MoE support on 2026-02-10 in PR [#19468](https://github.com/ggml-org/llama.cpp/pull/19468), merge commit `fc0fe4004985d6749a7a05e250d161f9dbe41d65`.
- **FACT:** the official Qwen repository does not currently provide a first-party GGUF surfaced in the model search. Community GGUFs exist, including Unsloth, so provenance and conversion quality require explicit verification.
- **FACT:** Qwen3.8 currently exposes a 27B dense model and a Flash-Next line; no official 4B/9B Qwen3.8 variant was found. [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B)

### Feasibility interpretation

- **ASSUMPTION:** a 4-bit 9B GGUF is likely to fit only with tight context and possibly partial CPU offload; theoretical 4-bit weights alone are 4.5 GB before scales, metadata, embeddings, cache, and runtime buffers.
- **RECOMMENDATION:** use the secondary model only for pre-selected replication contrasts, not the full development matrix.
- **UNRESOLVED QUESTION:** which exact GGUF repository, quantization, file hash, and conversion path passes local quality and memory checks?
- **UNRESOLVED QUESTION:** if 9B cannot meet a pre-declared minimum usable context without excessive offload, should Qwen3.5-4B replace it? This fallback requires a human decision before model freeze.

## 3. `llama.cpp`, Vulkan, and RX 5700

- **FACT:** Google lists the Gemma 4 QAT GGUF as a drop-in local format for `llama.cpp`. Qwen3.5 support is merged upstream. Gemma 4 Multi-Token Prediction support was merged in `llama.cpp` PR [#23398](https://github.com/ggml-org/llama.cpp/pull/23398) on 2026-06-07, but speculative decoding is not required for the baseline.
- **FACT:** `llama.cpp` provides a Vulkan backend used on AMD Linux systems. Current upstream guidance notes that RDNA1 lacks native BF16 support; the experiment should use quantized weights and supported cache types rather than assuming BF16 kernels. [RADV discussion](https://github.com/ggml-org/llama.cpp/discussions/23295)
- **FACT:** historical RDNA1/MoltenVK regressions exist, demonstrating why a build pin and correctness smoke test are necessary. The reported issue was specific to MoltenVK/macOS, not proof of a current Fedora RADV failure. [Issue #15846](https://github.com/ggml-org/llama.cpp/issues/15846)
- **RECOMMENDATION:** pin a known-good `llama.cpp` Git commit and container digest only after testing; record Mesa/RADV, kernel, firmware, and Vulkan device information.
- **RECOMMENDATION:** measure CPU-only and Vulkan runs during environment validation, but use the approved Vulkan condition for the experiment unless an ADR records a failure.
- **UNRESOLVED QUESTION:** which weight and KV-cache quantizations are supported and quality-safe on the chosen build?

## 4. Fine-tuning feasibility

- **FACT:** current Unsloth AMD training support targets RDNA3+, selected RDNA2 (`gfx1030`), and supported Instinct GPUs. RX 5700/RDNA1 (`gfx1010`) is absent, and Unsloth states that older GPUs lack required hardware support. [Unsloth AMD guide](https://unsloth.ai/docs/basics/amd)
- **FACT:** Unsloth advertises Gemma 4 fine-tuning in 8 GB VRAM and Qwen3.5 in lower VRAM on supported hardware. This does not establish support for RX 5700 and must be validated on the chosen Kaggle accelerator. [Unsloth AMD guide](https://unsloth.ai/docs/basics/amd)
- **FACT:** QLoRA trains LoRA adapters through a frozen 4-bit base model and was introduced as a memory-efficient alternative to full fine-tuning. [QLoRA paper](https://arxiv.org/abs/2305.14314)
- **RECOMMENDATION:** use Unsloth on NVIDIA Kaggle as the single main training pipeline because it offers a maintained path for Gemma 4 and QLoRA. Pin Unsloth, Transformers, PEFT, TRL, bitsandbytes, CUDA, notebook source, dataset manifest, seeds, and exported artifact hashes.
- **RECOMMENDATION:** use raw Hugging Face PEFT/TRL only if a documented incompatibility blocks Unsloth. Such a switch is an ADR change, not an extra experimental condition.
- **UNRESOLVED QUESTION:** can the E4B adapter be exported or merged into a `llama.cpp`-compatible artifact without changing chat template or quantization semantics?
- **UNRESOLVED QUESTION:** which target modules and adapter rank are supported by the PLE architecture? Resolve through official examples and a pilot, never by tuning on the final test split.

## 5. Kaggle

- **FACT:** current Kaggle notebook documentation offers either one NVIDIA Tesla P100 or two NVIDIA Tesla T4 GPUs. Availability is capacity-dependent. [Kaggle notebooks documentation](https://www.kaggle.com/docs/notebooks)
- **FACT:** Kaggle enforces a weekly GPU budget and may change quotas; a historical fixed number must not be encoded as a guarantee. [Kaggle GPU policy discussion](https://www.kaggle.com/discussions/general/108481)
- **RECOMMENDATION:** record accelerator model/count, observed quota, session limits, image/package versions, start/end timestamps, and failure/restart events for every training run.
- **ASSUMPTION:** a 16 GB P100 or one/two 16 GB T4 devices should be sufficient for the planned QLoRA pilot with conservative sequence length and micro-batch size; the actual peak memory must be captured.

## 6. OpenSpec

- **FACT:** the OpenSpec release observed during bootstrap requires Node.js 20.19 or later; the environment uses Node.js 24.19.0.
- **FACT:** OpenSpec's current `spec-driven` schema is `proposal → specs → design → tasks`. Repository commands include `new`, `status`, `instructions`, `validate`, and `archive`; exploration, continuation, application, and verification are exposed to agents through the current skill/instruction workflow rather than assumed legacy CLI commands. [OpenSpec repository](https://github.com/Fission-AI/OpenSpec)
- **FACT:** the repository was initialized non-interactively for Codex in English with a `spec-driven` change.
- **RECOMMENDATION:** pin the bootstrap version in documentation and CI validation. Upgrade only in a dedicated maintenance change after reviewing generated files and workflow behavior.

## 7. Current WETI thesis template and requirements

- **FACT:** the WETI diploma page currently provides **`Thesis_Template_PL_26.zip`** and **`WytPracDyp_2026_v3.docx`**, alongside Gdańsk University of Technology Rector's Order 45/2024 effective 2024-12-02. [WETI diploma page](https://eti.pg.edu.pl/studenci/dyplomy)
- **FACT:** current university guidance describes a typical MSc thesis as approximately 60–80 pages but states there is no formal page-count requirement. It requires Polish and English abstracts, a title page from Moja PG, contents, abbreviations where useful, introduction/objective, substantive chapters, summary, bibliography, and appendices as applicable. [Rector's Order 45/2024](https://cdn.files.pg.edu.pl/eti/Dziekanat/regulaminy/ZR%2045-2024.pdf)
- **FACT:** tables are captioned above and figures below; each must be cited in text. Citations must be consistent with PN-ISO 690:2012 guidance. [Rector's Order 45/2024](https://cdn.files.pg.edu.pl/eti/Dziekanat/regulaminy/ZR%2045-2024.pdf)
- **RECOMMENDATION:** import the official Polish 2026 LaTeX template verbatim in a dedicated issue, preserve upstream provenance, then place chapter content around it. The bootstrap records the official link but does not reconstruct the template manually.
- **UNRESOLVED QUESTION:** supervisor-specific structural or citation preferences and the final Moja PG title-page export.

## 8. University GenAI rules

- **FACT:** Rector's Circular 29/2024, effective 2024-10-01, permits GenAI subject to instructor scope, personal responsibility, critical verification, privacy protection, and transparent documentation. [Official GenAI guidelines](https://files.pg.edu.pl/api/v1/file/preview?path=eia%2F03-studia%2F03-proces-dyplomowania%2F09+-+Wytyczne+dotycz%C4%85ce+stosowania+narz%C4%99dzi+GenAI+na+Politechnice+Gda%C5%84skiej.pdf&response-content-disposition=attachment)
- **FACT:** low-intervention uses such as language correction, translation, transcription, and search do not require granular documentation, though a critical-verification declaration applies.
- **FACT:** generation of content, code, or images is high-intervention. Inclusion requires informed, transparent, ethical use; the declaration must identify the area/range and tool. Generated content must be cited at the end of the thesis, and an LLM cannot be an author.
- **FACT:** users must not submit confidential/non-public data to generally available GenAI tools.
- **RECOMMENDATION:** maintain a lightweight repository log for significant Work/Codex contributions, then generate the final Polish declaration table from verified entries. Log decisions and material generation, not trivial completion.
- **UNRESOLVED QUESTION:** confirm with the supervisor whether repository-native AI logs plus the university declaration table satisfy any faculty-specific expectation.

## Decision gate before M1/M2

The human researcher must approve:

1. the specialized benchmark domain and language balance;
2. the primary/secondary candidate and fallback rule;
3. thinking and sampling controls;
4. text-only scope;
5. QLoRA training environment and export route;
6. minimum usable context and performance thresholds from target-hardware smoke tests.
