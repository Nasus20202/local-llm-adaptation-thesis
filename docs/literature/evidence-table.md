# Literature Evidence Table

**Review date:** 2026-08-31
**Status:** initial evidence map, not a complete systematic review.

| Area | Primary or authoritative source | Evidence used in this project | Important limitation / follow-up |
|---|---|---|---|
| In-context learning | Brown et al., *Language Models are Few-Shot Learners* ([arXiv:2005.14165](https://arxiv.org/abs/2005.14165)) | Establishes zero-/one-/few-shot prompting as adaptation without weight updates | GPT-3 scale/API setting differs from small local models |
| Instruction tuning | Ouyang et al., *Training language models to follow instructions with human feedback* ([arXiv:2203.02155](https://arxiv.org/abs/2203.02155)) | Background for instruction-following baselines and alignment | Not a study of local inference or LoRA |
| Chain-of-thought prompting | Wei et al., *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* ([arXiv:2201.11903](https://arxiv.org/abs/2201.11903)) | Motivation for structured/few-shot prompting on suitable procedural tasks | Benefits are model/task dependent; do not assume transfer |
| Prompt robustness | Sclar et al., *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design* ([arXiv:2310.11324](https://arxiv.org/abs/2310.11324)) | Supports testing semantically equivalent prompt formulations | Operational paraphrase set still requires a pilot |
| RAG | Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* ([arXiv:2005.11401](https://arxiv.org/abs/2005.11401)) | Canonical retrieval-plus-generation architecture and knowledge-task motivation | Original architecture is not the exact local retrieval implementation |
| RAG evaluation | Es et al., *RAGAS: Automated Evaluation of Retrieval Augmented Generation* ([arXiv:2309.15217](https://arxiv.org/abs/2309.15217)) | Separates retrieval/grounding/answer dimensions | LLM-based metrics require validation and cannot be sole evidence |
| LoRA | Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* ([arXiv:2106.09685](https://arxiv.org/abs/2106.09685)) | Defines low-rank weight adaptation and efficiency rationale | Target-module choice for Gemma 4 PLE remains empirical |
| QLoRA | Dettmers et al., *QLoRA: Efficient Finetuning of Quantized LLMs* ([arXiv:2305.14314](https://arxiv.org/abs/2305.14314)) | Basis for training adapters through a frozen 4-bit base | Reported hardware/models do not establish RX 5700 support |
| Post-training quantization | Frantar et al., *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers* ([arXiv:2210.17323](https://arxiv.org/abs/2210.17323)); Lin et al., *AWQ* ([arXiv:2306.00978](https://arxiv.org/abs/2306.00978)) | Explains why quantization method is a controlled model artifact property | GGUF Q4_0/QAT is not equivalent to GPTQ or AWQ |
| Quantization-aware training | Liu et al., *LLM-QAT* ([arXiv:2305.17888](https://arxiv.org/abs/2305.17888)) | Background for QAT as distinct from post-training quantization | Does not independently validate Gemma 4 vendor claims |
| Tool use / harness | Yao et al., *ReAct* ([arXiv:2210.03629](https://arxiv.org/abs/2210.03629)); Schick et al., *Toolformer* ([arXiv:2302.04761](https://arxiv.org/abs/2302.04761)) | Motivates separating procedural control/tool interaction from static prompting | Thesis harness is a controlled system, not an unrestricted agent |
| Evaluation breadth | Liang et al., *Holistic Evaluation of Language Models* ([arXiv:2211.09110](https://arxiv.org/abs/2211.09110)) | Supports multidimensional accuracy, robustness, efficiency, and transparency | HELM is broader than the thesis and does not define its benchmark |
| LLM judges | Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) | Provides background and known judge-bias concerns | Proprietary judges remain supplemental in this project |
| Contamination | Sainz et al., *NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark* ([arXiv:2310.18018](https://arxiv.org/abs/2310.18018)) | Supports explicit leakage review and held-out benchmark handling | Training corpora are incompletely disclosed; absence cannot be proven |
| Primary model | Google, *Gemma 4 model card* ([official](https://ai.google.dev/gemma/docs/core/model_card_4)); official E4B QAT GGUF ([Hugging Face](https://huggingface.co/google/gemma-4-E4B-it-qat-q4_0-gguf)) | Architecture, license, context, languages, memory estimate, and first-party artifact | Target-hardware behavior must be measured |
| Secondary model | Qwen, *Qwen3.5-9B model card* ([official](https://huggingface.co/Qwen/Qwen3.5-9B)); `llama.cpp` support ([PR #19468](https://github.com/ggml-org/llama.cpp/pull/19468)) | Architecture, language coverage, license, context, and backend support | Community GGUF provenance and 8 GB feasibility unresolved |
| Training implementation | Unsloth, *AMD support* ([documentation](https://unsloth.ai/docs/basics/amd)) | Current supported AMD families; justifies excluding RDNA1 from main local QLoRA plan | Vendor documentation; recheck before training freeze |
| Local backend | `llama.cpp` ([upstream](https://github.com/ggml-org/llama.cpp)) | GGUF/Vulkan implementation candidate | Pin and test an exact revision; do not cite moving `master` as a fixed artifact |
| Thesis rules | Gdańsk University of Technology, Rector's Order 45/2024 ([PDF](https://cdn.files.pg.edu.pl/eti/Dziekanat/regulaminy/ZR%2045-2024.pdf)); [WETI diploma page](https://eti.pg.edu.pl/studenci/dyplomy) | Current format requirements and official 2026 template location | Recheck immediately before submission |
| GenAI governance | Gdańsk University of Technology, Rector's Circular 29/2024 ([PDF](https://files.pg.edu.pl/api/v1/file/preview?path=eia%2F03-studia%2F03-proces-dyplomowania%2F09+-+Wytyczne+dotycz%C4%85ce+stosowania+narz%C4%99dzi+GenAI+na+Politechnice+Gda%C5%84skiej.pdf&response-content-disposition=attachment)) | Disclosure, verification, privacy, authorship, and citation duties | Confirm any faculty/supervisor additions |

## Literature gaps before methodology freeze

- Define a reproducible search protocol and screening log rather than treating this bootstrap map as a systematic review.
- Add current primary work on skill/procedural-context systems and distinguish product terminology from a stable research construct.
- Review local-inference energy measurement and AMD telemetry validity.
- Select contamination-detection procedures suitable for newly authored and source-grounded items.
- Verify Polish-language benchmark and evaluator literature relevant to the chosen domain.
