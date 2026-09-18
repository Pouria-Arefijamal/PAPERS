# LLM Fine-Tuning, Pruning, Quantization & Distillation for Telecommunications and Network Management

**A citable candidate list for a PhD survey on AI-native network management for 5G/6G**

Compiled: 18 September 2026
Scope: **58 numbered paper entries** plus 10 generic methods and 4 networking surveys. Peer-reviewed venues first (IEEE TNSM/TMC/TMLCN/TON/TCCN/TNNLS/Network/OJ-COMS/WCNC/GC Wkshps/NetSoft/CSCWD, ACM SIGCOMM & CCR, KDD, ACL/EMNLP/IJCNLP, Elsevier ComNet, Wiley IJNM, Springer), preprints explicitly flagged.

> **Reading note on rigour.** Every field below is either (a) taken verbatim from a source I actually retrieved (URL given per row), or (b) marked **"not reported"**. Where I could only verify an abstract (paywalled full text), this is stated explicitly. Where the peer-reviewed version and the arXiv preprint differ, both are given. **No DOI, author list, venue, or numeric result in this report is invented or inferred.** Corpus statistics for the JSON file accompanying this report are in the appendix.

---

## Table of Contents

1. [Group (i) — Telecom / network LLM fine-tuning (entries 1–15, 27–48)](#group-i)
2. [Group (ii) — Pruning, quantization & distillation for networking LLMs (entries 16–26)](#group-ii)
3. [Group (iii) — Generic efficient-LLM methods networking papers build on](#group-iii)
4. [Answers to Questions A–F](#answers)
5. [Trade-off table: model size / compression vs. decision quality](#tradeoff)
6. [Caution note: what I could NOT verify](#cautions)
7. [Appendix: search strategy and verification method](#appendix)

**How to read the entry numbers.** Group (i) runs 1–15, then continues with **27–48** (later additions appended after the original Group (i)/Group (ii) boundary). Group (ii) is **16–26**, then continues with **49–58**. Group (iii) uses G1–G10 and S1–S4. **The numbered order is not the reading order** — for a linear read, follow Group (i) 1→15, then 27→48, then Group (ii) 16→26.

---

<a name="group-i"></a>
## Group (i) — Telecom / network LLM fine-tuning

### 1. Mobile-LLaMA: Instruction Fine-Tuning Open-Source LLM for Network Analysis in 5G Networks

| Field | Value |
|---|---|
| **Authors** | Khen Bo Kan, Hyunsu Mun, Guohong Cao, et al. (4 authors: + Youngseok Lee) |
| **Year** | 2024 |
| **Venue** | IEEE Network (IEEE Network: The Magazine of Global Internetworking), vol. 38, no. 5, pp. 76–83 |
| **DOI** | 10.1109/MNET.2024.3421306 |
| **Status** | **PEER-REVIEWED** (journal). No arXiv preprint found. |
| **Base model** | LLaMA 2 **13B** — the paper says "LLaMA-13B"; the released fine-tuning code loads `meta-llama/Llama-2-13b-chat-hf` |
| **Method** | **8-bit LoRA** (not strictly QLoRA: `BitsAndBytesConfig(load_in_8bit=True)` + PEFT `LoraConfig`), via TRL `SFTTrainer`. Verified from the released training script: **LoRA r=64, lora_alpha=16, lora_dropout=0.1, lr=1e-4, max_steps=5000, num_train_epochs=3, per_device_batch_size=4, max_length=2048**, `paged_adamw_32bit`. Plus self-instruct data expansion using OpenAI pre-trained models. |
| **Dataset** | Own network-analysis instruction data collected from publicly available real-world 5G network datasets; self-instruct expansion. **Exact size: 15,111 instruction sets** (counted from `Mobile_LLaMA_main.json`); validation split 1,300. Breakdown: Packet analysis = 20 manual seeds + 2,000 self-instruct; IP routing analysis = 100 manual + 10,000 self-instruct; Performance analysis = 30 manual + 3,000 self-instruct. |
| **Training hardware** | **not reported** (not in the abstract, the Penn State Pure record, the GitHub README, or the fine-tuning script) |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | Network-analysis **code generation score 247/300**, vs. **GPT-3.5 = 209/300** |
| **Baselines** | GPT-3.5 (score 209); LLaMA-13B |
| **Code/data public** | Yes — https://github.com/DNLab2024/Mobile-LLaMA (training data, self-instruct data, evaluation JSON, fine-tuning scripts, HF demo notebook). Fine-tuned model on HF: `hyonbokan/mobile_llama_5kRounds`. |
| **Main limitation** | Evaluation is a single 300-point code-generation rubric; no network KPI / closed-loop performance is measured. Task scope is *analysis code generation* (packet, IP routing, performance), not online network control. **⚠️ Additional caveat found: the repo's three evaluation JSON files contain only 10 instructions each (30 total), so the scale of the 247/300 rubric is undocumented.** |
| **Source retrieved** | https://pure.psu.edu/en/publications/mobile-llama-instruction-fine-tuning-open-source-llm-for-network-/ ; https://raw.githubusercontent.com/DNLab2024/Mobile-LLaMA/main/README.md ; https://raw.githubusercontent.com/DNLab2024/Mobile-LLaMA/main/finetuning/mobile_llama_finetuning.py |

> **Relevance to Question A:** This is the clearest affirmative evidence — an LLM instruction-fine-tuned *specifically* for 5G network management (NWDAF-anchored: packet analysis, IP routing analysis, performance analysis), not telecom text classification.

---

### 2. TelecomGPT: A Framework to Build Telecom-Specific Large Language Models

| Field | Value |
|---|---|
| **Authors** | Hang Zou, Qiyang Zhao, Yu Tian, et al. (7 authors: + Lina Bariah, Faouzi Bader, Thierry Lestable, Merouane Debbah) |
| **Year** | 2025 (preprint 2024) |
| **Venue** | **IEEE Transactions on Machine Learning in Communications and Networking (TMLCN)**, vol. 3, pp. 948–975 |
| **DOI** | 10.1109/TMLCN.2025.3593184 (preprint DOI: 10.48550/arXiv.2407.09424) |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT available (arXiv:2407.09424) |
| **Base model** | **Llama2-7B, Mistral-7B, Llama3-8B** (+ their instruct variants); model size capped at **≤8B** "due to the constraint of available GPU resources". Best configuration = **Llama3-8B + SFT + DPO = TelecomGPT** |
| **Method** | Three-stage pipeline: (1) **domain-specific continual pre-training** (causal LM objective) → (2) **instruction tuning via QLoRA** — **rank r=512, α=256, dropout 0.05**, constant LR **2e-4**, **3 epochs**, AdamW without weight decay, **FSDP** → (3) **alignment tuning via DPO + QLoRA** — **rank r=256, α=128, dropout 0.1, β=0.1**, cosine schedule, initial LR **5e-6**, 1 epoch. QLoRA is used deliberately as a *regulariser* against catastrophic forgetting. |
| **Dataset** | Three purpose-built datasets: **OpenTelecom** (pre-training), **TelecomInstruct** (instruction), **TelecomAlign** (DPO preference). |
| **Dataset sizes** | **OpenTelecom: 1,679.5M training tokens + 16.89M validation tokens** (3GPP standards 193M, IEEE standards 7.5M, arXiv papers 893M, books 1.9M, patents 253.2M, StackExchange 51.9M, Wikipedia 18.9M, GitHub code 260.1M), keyword-filtered from RedPajama-1T using ~700 telecom keywords + deduplication. **TelecomInstruct and TelecomAlign sample counts: not reported** (only "1000 samples per working group" × 16 working groups). |
| **Training hardware** | **Continual pre-training: 8 × AWS ml.p4d.24xlarge instances, ~6 hours.** **Instruct tuning: FSDP on 8 GPUs with 32 GB memory on one ml.p4d.24xlarge instance, ~1.5 hours.** ⚠️ The paper never writes "A100", and states 32 GB while ml.p4d.24xlarge ships 8 × A100 40 GB — an internal inconsistency, reported here verbatim. |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | **TeleQnA overall accuracy: GPT-4o 78, GPT-4 75, GPT-3.5 66, Llama3-8B 56.20, Llama3-8B-Instruct 64.80, Llama3-8B-TI 71.20, Llama3-8B-TI-TA 70.60, Mistral-7B-Instruct 62, Mistral-7B-TI 65.2, LLaMA-2-7B 48.94, LLaMA-2-7B-TI 59.80, LLaMA-2-7B-TP-TI 63.79.** **Extended TeleQnA: GPT-4o 93, GPT-3.5 89, Llama3-8B-Instruct 88.49, Llama3-8B-TI 94, Mistral-7B-TI 81.5.** **3GPP technical-document classification (2,000 test texts, 16 working groups): GPT-4o 38.94, GPT-3.5 38.54, Llama3-8B-Instruct 33.35, Llama3-8B-TI 75.30, Mistral-7B-Instruct 27.84, Mistral-7B-TI 70.83.** **Telecom Math Modeling (~600 equations from 170 unseen papers; average MathBERT / %≥90 / %≥50): GPT-4 49.38 / 3.77 / 50.35; Llama3-8B-Instruct 40.78 / 2.51 / 34.45; Llama3-8B-TI 46.16 / 9.69 / 46.80; Llama3-8B-TI-TA 49.45 / 9.52 / 50.73; Mistral-7B-TI 47.66 / 8.04 / 48.77.** Code tasks (Rouge1/RougeL): code summary Llama3-8B-Instruct 0.3202/0.2120 → TI 0.5192/0.3772; code infilling 0.1125/0.0974 → 0.4169/0.3743 → TI-TA 0.4336/0.3903. Continual pre-training contributed ≈+4%. |
| **Baselines** | GPT-4, GPT-4o, GPT-3.5, Llama3-8B (±Instruct), Mistral-7B (±Instruct), LLaMA-2-7B, Mistral-8x7B |
| **Code/data public** | Datasets described. **Code URL NOT REPORTED by the paper.** (A repo `github.com/hang-zou/LLM_FT_3GPP` exists but is *not cited by the paper* and is therefore **not confirmed** as official.) |
| **Main limitation** | **Verbatim from the paper: "Due to the resource limits, our experiments remain in small scale"; "our models can only treat textual data."** Also: the title on arXiv contains a typo ("Telecom-Specfic") corrected in the journal version. Evaluates *knowledge and code tasks*, **not network management decisions or network KPIs**; performs no compression experiment despite motivating the work with deployment/compression challenges (it cites LLM-QAT and BitNet). |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2407.09424 (full text incl. training-settings and results tables) ; Crossref record 10.1109/TMLCN.2025.3593184 |

> **Notable:** TelecomGPT's introduction explicitly names the field's compression/deployment problem — it cites **LLM-QAT** and **BitNet 1-bit quantization** as the enablers for edge deployment, and **KV caching, FlashAttention and MoE** for inference acceleration, and states that "the long inference time of LLM is unbearable to meet the requirement of URLLC." This is a good citation for framing a compression-for-network-management survey — **but TelecomGPT itself performs no compression experiment.**

---

### 3. Tele-LLMs: A Series of Specialized Large Language Models for Telecommunications

| Field | Value |
|---|---|
| **Authors** | Ali Maatouk, Kenny Chirino Ampudia, Rex Ying, et al. (4 authors: + Leandros Tassiulas) |
| **Year** | 2026 (arXiv preprint 2024) |
| **Venue** | **IEEE Access**, vol. 14, pp. 86424–86441 |
| **DOI** | 10.1109/ACCESS.2026.3698683 (preprint: 10.48550/arXiv.2409.05314) |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT (arXiv:2409.05314) |
| **Base models** | **TinyLlama-1.1B, Phi-1.5B, Gemma-2B, Gemma-2-2B, LLaMA-3.2-1B, LLaMA-3.2-3B, LLaMA-3-8B** — a **1B–8B** family, released as both base and instruction-tuned variants |
| **Method** | **Continual pre-training (full fine-tuning, FFT)**. **Key negative result: PEFT/LoRA was tested and judged insufficient.** LoRA config tested: rank r = 64, alpha = 32, dropout 0.1; for a smaller model "LoRA can initially inject telecom knowledge but quickly saturates due to its limited capacity"; on LLaMA-3-8B "the gradient norm of the LoRA method remained extremely low", so the training loss barely changed. Consequently **all released Tele-LLMs use full-parameter fine-tuning.** Optimiser AdamW, weight decay 0.1, max grad norm 1, cosine schedule decaying to 10% of max LR, 10%-of-epoch linear warmup, batch size 4M tokens at sequence length 8192; max LR 1e-5 (LLaMA) / 2e-5 (Gemma); mixed precision + sample packing + block attention. **2 epochs.** 5% SlimPajama general data mixed in to mitigate catastrophic forgetting. Instruction-tuning stage: **Q-LoRA, 8-bit init, rank 8, applied to Q/K/V/O, batch 8, grad-accum 2, LR 2e-4, AdamW, lora_alpha 32, dropout 0.05.** |
| **Dataset** | **Tele-Data** (curated corpus): arXiv **90k papers / 4 GB / 1.08B tokens**; 3GPP standards **2.8k docs / 334 MB / 86.45M tokens**; Wikipedia **19.5k articles / 123 MB / 26.44M tokens**; Web **740k links / 6.8 GB / 1.55B tokens**. **Tele-Eval**: **750k open-ended Q&A pairs** (1% retention after regex + LLM filtering). |
| **Training hardware** | **8 × NVIDIA A6000 GPUs, ~5,000 GPU hours total** (for the full released series) |
| **Inference latency / model size** | Instruction-tuned (chatbot) stage used batch 128k tokens, context 2048, 1 epoch. Evaluation-side latency: **Mixtral-8x-7B as LLM-judge took ~50 ms/question on a single NVIDIA A6000.** Model sizes = 1B–8B (no post-compression size) |
| **Main quantitative results** | **Average relative improvement of 25% on Tele-Eval (LLM-Eval metric)** across the adapted series (adapted model vs. its own general-purpose counterpart, averaged over the series — *relative*, not absolute points). Per-model LLM-Eval (base → -Tele): **TinyLlama-1.1B 8.26 → 11.37; Gemma-2B 13.59 → 17.07; Gemma-2-2B 15.10 → 17.34; LLaMA-3.2-1B 11.85 → 12.98; LLaMA-3.2-3B 24.68 → 26.71; LLaMA-3-8B 24.60 → 29.60.** Base / Instruct / Tele / Tele-Instruct: TinyLlama 8.26/15.42/11.37/17.40; **Gemma-2B 13.59/19.84/17.07/27.78**; Gemma-2-2B 15.10/22.30/17.34/25.46; LLaMA-3.2-1B 11.85/14.50/12.98/16.20; LLaMA-3.2-3B 24.68/25.20/26.71/28.56; **LLaMA-3-8B 24.60/30.65/29.60/34.51.** General knowledge retained/enhanced: **LLaMA-3-8B GSM8K 0.144 → 0.2441 (~10 pp gain)**, MMLU 0.6209 → 0.6157, HellaSWAG 0.6009 → 0.6068. Standards-only model (Gemma-2B-Standards) **underperformed** the base model on overall Tele-Eval (11.18 vs 13.59) — evidence that **narrow domain specialisation hurts**. Models "rival larger general-purpose models like GPT-4o" on telecom *literature* tasks. |
| **Baselines** | Each model's own base + official instruct counterpart (Gemma-2B-it, Phi-1.5, Phi-1.5-Tele), Mixtral-8x7B-Instruct (LLM judge), GPT-4o; general benchmarks MMLU, HellaSWAG, GSM8K |
| **Code/data public** | **Yes** — https://github.com/Ali-maatouk/Tele-LLMs ; HF collections `AliMaatouk/tele-llms-*` and `AliMaatouk/tele-datasets-*`; `AliMaatouk/Tele-Data`, `AliMaatouk/Tele-Eval` |
| **Main limitation** | Task is **telecom knowledge / literature** (Q&A, citation prediction & recommendation) — **not network management decisions, not network KPIs**. No compression experiments. Full FT costs 8×A6000 and 5,000 GPU hours. The **LoRA-vs-FFT comparison is reported only qualitatively in Fig. 4 — there is no numeric table**, so the strength of the "FFT is required" claim cannot be quantified from the paper. Text-only; Ans-PPL/SemScore are only comparable *within* an LLM family. |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2409.05314 ; https://arxiv.org/html/2409.05314v3 ; Crossref API record for 10.1109/ACCESS.2026.3698683 |

---

### 4. TeleQnA: A Benchmark Dataset to Assess Large Language Models Telecommunications Knowledge

| Field | Value |
|---|---|
| **Authors** | Ali Maatouk, Fadhel Ayed, Nicola Piovesan, et al. (4 authors: + Antonio De Domenico) |
| **Year** | 2026 (first preprint 2023) |
| **Venue** | **IEEE Network**, vol. 40, no. 2, pp. 253–260 |
| **DOI** | 10.1109/MNET.2025.3576035 |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT (arXiv:2310.15051) |
| **Base models evaluated** | Multiple general-purpose LLMs incl. GPT-4 (the dataset is model-agnostic) |
| **Method** | Benchmark dataset (MCQ); **no fine-tuning proposed by the paper itself** |
| **Dataset** | **10,000 telecom questions** (MCQ) generated from 3GPP standards and research papers, with human validation. (The 10,000 figure is confirmed in the NetSoft 2025 paper's description of TeleQnA.) |
| **Training hardware** | not applicable / not reported |
| **Main quantitative results** | The dataset's headline finding (cited by TelecomGPT): **GPT-4 fails almost half of the specification-related problems in TeleQnA.** Used as the standard telecom-knowledge benchmark across the field. |
| **Baselines** | GPT-4 and other general LLMs |
| **Code/data public** | Yes — dataset released publicly (widely reused; e.g. TSpec-LLM/NetSoft pipeline) |
| **Main limitation** | MCQ-only, subject to LLM "selection bias" (explicitly argued by the Tele-LLMs authors, who built Tele-Eval as an open-ended alternative). It measures *knowledge*, not network operation. |
| **Source retrieved** | Crossref API record for 10.1109/MNET.2025.3576035 ; FAPESP BV record citing "the TeleQnA dataset of 10,000 telecom questions" (https://bv.fapesp.br/en/publicacao/284975/) |

---

### 5. Harnessing the Power of LLMs, Informers and Decision Transformers for Intent-driven RAN Management in 6G

| Field | Value |
|---|---|
| **Authors** | Md Arafat Habib, Pedro Enrique Iturria-Rivera, Yigit Ozcan, et al. (7 authors: + Medhat Elsayed, Majid Bavand, Raimundas Gaigalas, Melike Erol-Kantarci) |
| **Year** | 2025 |
| **Venue** | **PREPRINT** — arXiv:2505.01841 [cs.NI]; comments state "Currently under review" |
| **DOI** | 10.48550/arXiv.2505.01841 (arXiv-issued) |
| **Status** | **PREPRINT** |
| **Base model** | LLaMA (`LlaMa base model is used as a baseline`). **Exact variant and parameter count: NOT reported.** The paper's Fig. 4 caption uses LLaMA only as an illustrative example; a generic "10-billion parameter model" is used as a *memory illustration*, not as the actual model. |
| **Method** | **QLoRA** (4-bit NormalFloat quantisation + double quantisation + paged optimisers + LoRA), all four components used. Plus a RAG module on top. |
| **Dataset** | Custom dataset built from network simulations, in three segments: (1) query–response pairs, (2) intent type+ magnitude labels, (3) RAG corpus. Sizes: described only as "hundreds or even thousands of query-response pairs can be generated" — **exact sample count not reported**. |
| **Training hardware** | **not reported** (the paper motivates QLoRA by saying it "enabl[es] the fine-tuning of large models on a single GPU" and gives a generic illustration that "a 10-billion parameter model that would typically require over 160 GB of memory can be fine-tuned using QLoRA with approximately 40 GB", but names no GPU) |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | QLoRA-fine-tuned vs. base LLaMA: **BERTScore 0.92 vs 0.86** (+6%); **METEOR 0.89 vs 0.83**; **semantic similarity +9%**. Predictive intent validation (Informer) rules out performance-degrading intents with **88% average accuracy**. HDTGA orchestration vs baselines: **throughput +19.3% (abstract) / +19.4% (body)**, **delay −48.5%**, **energy efficiency +54.9%** (note: the body text at one point swaps the delay/energy-efficiency percentages relative to the abstract — an internal inconsistency in the paper). |
| **Baselines** | Base LLaMA (no fine-tuning); three orchestration baselines: HRL with intent validation, HRL without, vanilla Decision Transformer; for time-series prediction: LSTM and GPT-2 decoder-only transformer |
| **Code/data public** | **Not found** |
| **Main limitation** | No base-model identification, no hardware, no dataset size, no latency — **not reproducible as published**. Results are simulation-based (OFDM cellular simulator with CDL channels), not a live network. Preprint. |
| **Source retrieved** | https://arxiv.org/abs/2505.01841 ; https://arxiv.org/html/2505.01841v1 |

---

### 6. Leveraging Multi-Agent System (MAS) and Fine-Tuned Small Language Models (SLMs) for Automated Telecom Network Troubleshooting

| Field | Value |
|---|---|
| **Authors** | Chenhua Shi, Bhavika Jalli, Gregor Macdonald, et al. (7 authors, all **Ericsson**: + John Zou, Wanlu Lei, Mridul Jain, Joji Philip) |
| **Year** | 2025 |
| **Venue** | **PREPRINT** — arXiv:2511.00651 |
| **DOI** | 10.48550/arXiv.2511.00651 |
| **Status** | **PREPRINT** |
| **Base models** | **Unsloth/DeepSeek-R1-Qwen-3-8B** (8B, reasoning); also RFT-compared against **Qwen3-4B** and **Qwen3-1.7B**. Orchestration LLM: **GPT-4o mini**. |
| **Method** | Two-stage: **SFT** (LoRA, warm-up on labelled QA pairs) then **RFT** (reinforcement fine-tuning) with **LoRA + GRPO**, implemented in the **TRL** library with **ZeRO Stage-2 DeepSpeed**; reward = format rewards (regex/XML tags) + RAGAS-based rewards (completeness, relevancy, groundedness). |
| **Dataset** | Proprietary telecom troubleshooting documents (RAN power-system faults; Core PDU-session degradation) indexed into a **HippoRAG** knowledge graph. Sizes: seed dataset + RFT dataset — **exact counts not given here**, but the companion paper (#7) reports **50 SME-validated seed pairs + 500 synthetic RFT pairs**. |
| **Training hardware** | **7 × NVIDIA RTX A6000 (48 GB VRAM each)**. Allocation: 1 GPU for vLLM serving Qwen3-Embedding-0.6B; 1 GPU for vLLM serving Qwen3-8B (RAGAS judge, thinking disabled); 2 GPUs for TRL-vLLM serving DeepSeek-R1-Qwen-3-8B. |
| **Inference latency / model size** | **Training time reported instead of latency:** with uniform chunking the **entire training process completes within 3 days**; **~20 hours to resume from a checkpoint**. No inference latency reported. |
| **Main quantitative results** | **Mean troubleshooting time reduced ~6× per node** vs human engineers; **accuracy improved 10%** vs human-driven process. RFT results for the 8B model: **RAGAS reward 3.44 → 5.19; Format reward 2.52 → 5.31; Total reward 5.96 → 10.51; reward std-dev 2.17 → 0.38** (much more stable). **Model-size scaling: 8B reaches peak reward ≈10; 4B and 1.7B "show modest improvements but consistently lower rewards"; fine-tuned 8B output judged comparable in quality to GPT-4o-mini**, while the un-tuned base produces only generic high-level answers. |
| **Baselines** | Base (un-fine-tuned) DeepSeek-R1-Qwen-3-8B; GPT-4o-mini; Qwen3-4B and Qwen3-1.7B; human engineers |
| **Code/data public** | Not found (proprietary internal troubleshooting documents; Hypha framework is OSS, HippoRAG is OSS) |
| **Main limitation** | Proprietary dataset and no public code; rewards are LLM/RAGAS-judged rather than ground-truth-labelled, so the "10.51 reward" is not an accuracy in the usual sense; the "6× faster" and "+10% accuracy" comparisons are vs. human engineers, not vs. an automated baseline of equal capability. Preprint. |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2511.00651 |

> **Directly answers Question F** with a controlled 1.7B / 4B / 8B comparison, and **Question C** with concrete GPU allocation and wall-clock training time.

---

### 7. Edge-Deployable LLM Fine-Tuning on a Single GPU for Telecom Network Troubleshooting

| Field | Value |
|---|---|
| **Authors** | Chenhua Shi, Bhavika Jalli, John Zou, et al. (7 authors, all **Ericsson**) |
| **Year** | 2026 |
| **Venue** | **PREPRINT** — arXiv:2607.02523 [cs.DC] |
| **DOI** | 10.48550/arXiv.2607.02523 |
| **Status** | **PREPRINT** |
| **Base models** | **unsloth/Qwen2.5-7B** (7.61B params, 28 layers, 28 Q-heads / 4 KV-heads, GQA) and **unsloth/DeepSeek-R1-0528-Qwen3-8B-unsloth-bnb-4bit** (8.2B params, 36 layers, 32 Q / 8 KV heads). Cross-architecture validation with **Llama-3.1-8B-Instruct**. All support 131,072-token context. |
| **Method** | LoRA restricted to **q_proj, k_proj, v_proj**; two-stage **SFT → RFT (GRPO/TRL)**; **Unsloth** framework with 4-bit quantisation, FlashAttention2, XFormers, KV-cache acceleration, torch.compile/inductor. Profiling sweep over max sequence length, GPU-memory utilisation, **LoRA rank**, and generation count. |
| **Dataset** | Telecom troubleshooting dataset: QA pairs augmented with **top-3 retrieved context documents**. **50 SME-validated seed pairs (SFT) + 500 synthetically generated RFT pairs.** Average token length of the top-3 chunks ≈ **16,126 tokens**. |
| **Training hardware** | **1 × NVIDIA RTX A6000, 48 GB VRAM** (edge-class); cross-checked against a 4×GH200 cluster for generalisation |
| **Inference latency / model size** | **4-bit Qwen2.5-7B weighs 3.805 GB on disk.** Quantisation memory profile: at 50k seq-len / 0.7 GPU-util → **compile 16.2 GB + KV cache 11.2 GB, 329k KV tokens**. Training durations (250 steps): 1k input tokens = **116 min**; 5k = **173 min**; 10k = **229 min**; 10k with 4 generations at 0.6 util = **313 min**. Llama-3.1-8B: 250 steps at 20k input tokens in **~29 min** (≈7× faster than Qwen2.5-7B). Inference: **"7–8B parameter models serve requests in seconds on the RTX A6000"** — no ms figure. |
| **Main quantitative results** | **Safe operating envelope on 48 GB: 50k max sequence length at 0.7 GPU utilisation.** Sequence length ≥60k produced CUDA `CannotAccessIllegalMemory` errors on Qwen2.5-7B but **not** on Llama-3.1-8B (60k succeeded) — thresholds are **not portable across model families**. Batch size ≥4 OOMs above 20k tokens on both. Input tokens >10k at 0.7 util OOMs at step 155/250. **DeepSeek-R1 (hybrid tokenizer strategy) achieved substantial gains in factual grounding and response consistency over Qwen2.5-7B.** |
| **Baselines** | Qwen2.5-7B (non-reasoning) vs DeepSeek-R1-0528-Qwen3-8B (reasoning) vs Llama-3.1-8B-Instruct; configuration sweep serves as its own baseline |
| **Code/data public** | Not found |
| **Main limitation** | A **profiling/characterisation study, not a quality study** — it deliberately reports memory/time envelopes and reward trajectories rather than network-decision accuracy. Preprint, 6 pages. |
| **Source retrieved** | https://arxiv.org/abs/2607.02523 ; https://arxiv.org/html/2607.02523v1 |

> **Directly answers Question C** with the most detailed GPU/latency/memory data of any paper in this list, and is explicitly framed around **O-RAN near-RT RIC / MEC edge deployment** and **data sovereignty**.

---

### 8. LLM-Based Emulation of the Radio Resource Control Layer: Towards AI-Native RAN Protocols

| Field | Value |
|---|---|
| **Authors** | Ziming Liu, Bryan Liu, Alvaro Valcarce, et al. (4 authors: + Xiaoli Chu). Affiliations: Univ. of Sheffield + **Nokia Bell Labs** |
| **Year** | 2026 (v1 May 2025; v5 Jan 2026) |
| **Venue** | **PREPRINT** — arXiv:2505.16821 [cs.NI]; "submitted to the IEEE for possible publication" |
| **DOI** | 10.48550/arXiv.2505.16821 |
| **Status** | **PREPRINT** |
| **Base models** | **Llama-3 8B**, **Llama-3.1 8B**, **Llama-3.2 3B**, **Llama-3.2 1B** (four backbones) |
| **Method** | **Supervised fine-tuning + LoRA** (adapters on attention projections **and MLP layers**, α = 2r, dropout 0). LoRA ranks **r ∈ {4, 8, 16}** benchmarked against **full fine-tuning**, bf16, AdamW, token-level cross-entropy. LR 2e-5 (full FT) / 3e-4 (LoRA, cosine decay, 100-step warmup). **Quantisation: weight-only INT4 (Q4_K_M, GGUF).** Prompting: `NoSys` / `RRC` / `RRC_constrain` (schema-bounded). |
| **Dataset** | **30,000 5G request–response pairs** (NR, proprietary multi-vendor corpus) **+ 4,800 QA turns** from 4G/LTE sessions. Segmentation-safe QA representation preserving ASN.1 via linearisation before BPE. |
| **Training hardware** | **NR dataset: 2 × NVIDIA A100 80 GB (PCIe)**, 52-core CPU, 512 GB RAM; ~29 GB VRAM per inference thread (GGUF), **~110 GB across two cards for training**. **LTE dataset: 4 × NVIDIA GH200 nodes** (Grace 72-core CPU + H100 96 GB HBM3), cluster of 1,320 nodes, HPE Cray Slingshot-11 interconnect; single-accelerator config = **1 × H100 (96 GB) inside one GH200**. |
| **Inference latency / model size** | **Median latency to generate one DL RRC message** (LTE, `RRC_constrain`): **L-3 8B FP16 + LoRA-r16 = 3,544 ms; L-3 8B Q4_K_M + LoRA-r16 = 2,556 ms; L-3.1 8B FP16 = 3,609 ms; L-3.1 8B Q4_K_M = 2,581 ms; L-3.2 3B (full FT) FP16 = 2,341 ms / Q4_K_M = 1,733 ms; L-3.2 1B (full FT) FP16 = 2,093 ms / Q4_K_M = 2,025 ms.** Under `RRC` (unconstrained): L-3 8B FP16 = 3,418 ms vs Q4_K_M = 2,519 ms. Edge vs. datacentre with **Llama-3.2-1B/INT4 (Q4_K_M)**: **Apple M2 Max median 1.84 s vs 1×GH200 (H100) 1.092 s** (the paper's Table XII lists the GH200 median as ≈1,092 ms and describes the M2 as ≈1.84 s); throughput **0.54 req/s (M2) vs 0.92 req/s (GH200)**; schema-check median **0.97 (M2) / 0.96 (GH200)**; semantic similarity **1.00 both**; SMC confirmation **0.54 (M2) / 0.53 (GH200)**; energy **≈7.7 mWh/message on M2 (15 W cap) vs ≈0.200 Wh/message on GH200 (660 W cap)**. |
| **Main quantitative results** | **Median cosine similarity 0.97 for the 8B model = +61% relative over zero-shot.** Conformance: L-3 8B Q4_K_M `RRC_constrain` → ASN.1 pass median 1.000, similarity 0.992 median, **SMC 0.993**. Zero-shot baselines on the NR dataset: **Gemini 1.5-Flash 0.585, GPT-4o 0.496, Claude 3.5 Sonnet v2 0.768, GPT-o3-mini 0.705, original Llama 3-8B 0.600, RRC-LLM (fine-tuned) 0.970.** LoRA-rank ablation (best validation loss, LTE): on 8B backbones **r=16 LoRA matches or slightly surpasses full fine-tuning**; on 3B/1B **full fine-tuning remains advantageous** (gap between best two methods Δ ≈ 6e-4). Training converged in **~8.4k steps**. |
| **Baselines** | Zero-shot Gemini 1.5-Flash, GPT-4o, Claude 3.5 Sonnet v2, GPT-o3-mini, original Llama-3-8B; full FT vs LoRA ranks 4/8/16; FP16 vs INT4; Apple M2 Max vs GH200 |
| **Code/data public** | Not found (corpus is proprietary multi-vendor operator traces) |
| **Main limitation** | Proprietary dataset, so not reproducible. Latency in the **1–3.6 second range** is far above real RRC control-plane budgets; the paper explicitly frames sub-100 ms as *future work* (constrained decoding, KV caching, multi-token draft-verify). Preprint. |
| **Source retrieved** | https://arxiv.org/abs/2505.16821 ; https://arxiv.org/html/2505.16821v5 ; https://browse-export.arxiv.org/pdf/2505.16821 |

> **This is the single richest paper for Questions C, E and F.** It is the only paper found that reports *both* a quantisation ablation (FP16 vs INT4 across four backbones) *and* end-to-end network-protocol latency *and* a model-size ablation.

---

### 9. Network Self-Configuration Based on Fine-Tuned Small Language Models

| Field | Value |
|---|---|
| **Authors** | Oscar G. Lira, Oscar M. Caicedo, Nelson L. S. da Fonseca, et al. |
| **Year** | 2026 |
| **Venue** | **IEEE Open Journal of the Communications Society (OJ-COMS)**, vol. 7, pp. 5920–5939 |
| **DOI** | 10.1109/OJCOMS.2026.3695460 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base model** | **not verified** — full text was not retrievable (IEEE Xplore returned HTTP 502 throughout the research window). The title and venue are confirmed via Crossref; the architecture `SLM_netconfig` is named in a search-index snippet. |
| **Method** | Fine-tuned Small Language Model ("SLM_netconfig" architecture) for network self-configuration |
| **Dataset** | **not verified** |
| **Training hardware** | **not verified** |
| **Inference latency / model size** | **not verified** |
| **Main quantitative results** | **not verified** |
| **Baselines** | **not verified** |
| **Code/data public** | **not verified** |
| **Main limitation** | **Verification gap.** Highly relevant by title (network configuration + SLM fine-tuning) and published in a strong IEEE open-access journal — the parent agent should retrieve the full text directly, as IEEE Xplore was down during this research. |
| **Source retrieved** | Crossref API record for 10.1109/OJCOMS.2026.3695460 ; search index snippet at https://ieeexplore.ieee.org/abstract/document/11527366 |

---

### 10. Lightweight LLMs for 3GPP Specifications: Fine-Tuning, Retrieval-Augmented Generation and Quantization

| Field | Value |
|---|---|
| **Authors** | Jose de Arimatea, Passos Lopes Junior, Jayr Pereira, et al. (6 authors: + Diedre Santos do Carmo, Roberto Lotufo, Christian Esteve Rothenberg) |
| **Year** | 2025 |
| **Venue** | **2025 IEEE 11th International Conference on Network Softwarization (NetSoft)**, 6 pp. |
| **DOI** | 10.1109/NETSOFT64993.2025.11080581 |
| **Status** | **PEER-REVIEWED** (conference) |
| **Base model** | **Llama 3.2 (3B parameters)** — quantised from **16-bit to 4 bits** |
| **Method** | **Quantisation (16-bit → 4-bit) + fine-tuning + RAG** |
| **Dataset** | **TeleQnA (10,000 telecom questions)** + **TSpec-LLM** repository of processed 3GPP documents |
| **Training hardware** | **not verified** (abstract-level only; the paper claims deployment "on modest hardware like edge devices or softwarized networks" but the abstract gives no GPU) |
| **Inference latency / model size** | Reduced memory demand is the claimed outcome; **exact figures not verified** |
| **Main quantitative results** | "Improve accuracy without heavy resource reliance" — **exact accuracy figures not verified** |
| **Baselines** | "prior resource-intensive or proprietary solutions" (unspecified at abstract level) |
| **Code/data public** | **Yes, per the abstract** — "Shared via GitHub repositories [1]" (exact URL not captured at abstract level) |
| **Main limitation** | Abstract-level verification only; numeric results and hardware not confirmed. Task is **telecom QA (3GPP standards comprehension)**, not network management decisions. |
| **Source retrieved** | https://bv.fapesp.br/en/publicacao/284975/ ; DOI record 10.1109/NETSOFT64993.2025.11080581 |

> **This is the only peer-reviewed paper found at a target venue (IEEE NetSoft) that combines quantization + fine-tuning + RAG for telecom**, which makes full-text retrieval a priority.

---

### 11. Toward Autonomous O-RAN: A Multi-Scale Agentic AI Framework for Real-Time Network Control and Management

| Field | Value |
|---|---|
| **Authors** | Hojjat Navidan, Mohammad Cheraghinia, Jaron Fontaine, et al. (8 authors: + Mohamed Seif, Eli De Poorter, H. Vincent Poor, Ingrid Moerman, Adnan Shahid). Ghent Univ.–imec + Princeton |
| **Year** | 2026 (v2 Jun 2026) |
| **Venue** | **PREPRINT** — arXiv:2602.14117 [cs.NI] |
| **DOI** | 10.48550/arXiv.2602.14117 |
| **Status** | **PREPRINT** |
| **Base models** | **Nvidia Nemotron** (LLM rApp, Non-RT); **GPT-OSS** (SLM xApp, Near-RT); **Wireless Physical-layer Foundation Model (WPFM)** dApp (RT, prior work of the same group) |
| **Method** | **Deployment-scale separation, not compression.** No pruning/quantisation/distillation of a single model; instead the architecture *assigns different-sized models to different control loops*. WPFM is **fine-tuned** (LoRA-class incremental retraining) on demand; the LLM translates intent to A1 policy via an MCP tool interface; the SLM performs PRB allocation via E2SM-RC. |
| **Dataset** | Live 5G testbed based on **srsRAN**, four active slices; E2SM-KPM telemetry (5-second sliding window at Near-RT, 1-minute summaries at Non-RT). Plus two IEEE DataPort IQ datasets for WPFM retraining: vehicular technology recognition (LTE, 5G NR, Wi-Fi, ITS-G5, C-V2X) and LTE/NR interference. |
| **Training hardware** | **LLM: H200 GPU. SLM: RTX 5090 GPU. WPFM: Nvidia Jetson Xavier NX.** |
| **Inference latency / model size** | **WPFM (RT, Xavier NX): 0.847 ± 0.04 ms. SLM (Near-RT, RTX 5090): 793 ± 3 ms. LLM (Non-RT, H200): 9,364 ± 59 ms.** WPFM fine-tuning: first epoch ≈17 s reaching 58.92% (technology recognition) / 82.28% (interference detection); fully fine-tuned after ≈340 s. Model parameter counts: **not reported**. |
| **Main quantitative results** | Agentic (SLM+LLM supervision) vs SLM-only: **average VIP throughput +6%** after promoting slice 4 to VIP, while preserving **average 22 ms latency** for the latency-sensitive slice; SLM-only alone reaches only **10.5 Mbps** VIP throughput and trades away latency protection. Agentic beats static allocation and a heuristic controller on throughput, delay and resource efficiency. |
| **Baselines** | Static equal PRB allocation; heuristic slice controller; SLM-only controller with fixed objectives |
| **Code/data public** | Not found for this paper; the referenced WPFM and datasets are public (IEEE DataPort links given in the paper) |
| **Main limitation** | Proof-of-concept on one live testbed; **no fine-tuning hyperparameters, no model parameter counts, no training hardware for the SLM itself**. The RT dApp API and RT RIC are **not yet standardised** in O-RAN, so the architecture is provisional. Preprint. |
| **Source retrieved** | https://arxiv.org/html/2602.14117v2 |

> **The clearest "model-size vs. decision-timescale" evidence in the corpus**: 0.847 ms (small PHY model) → 793 ms (SLM) → 9,364 ms (LLM), with the paper explicitly describing the higher computational demand of the agentic approach as "a necessary trade-off."

---

### 12. NetIntent: Leveraging Large Language Models for End-to-End Intent-Based SDN Automation

| Field | Value |
|---|---|
| **Authors** | Md. Kamrul Hossain, Walid Aljoby, et al. (King Fahd Univ. of Petroleum & Minerals) |
| **Year** | 2025 |
| **Venue** | **IEEE Open Journal of the Communications Society (OJ-COMS)**, vol. 6, pp. 10512–10541 |
| **DOI** | 10.1109/OJCOMS.2025.3642642 (preprint: 10.48550/arXiv.2507.14398) |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT (arXiv:2507.14398) |
| **Base models** | **33 open-source LLMs benchmarked**, spanning 1.1B–70B: e.g. TinyLlama:1.1b, Deepseek-coder:1.3b, Phi:2.7b, Starcoder:3b, Llama3.2:3b, Phi3:3.8b, Orca-mini:3b, Qwen:4b, Yi:6b, Codellama:7b, Llama2:7b, Llama3:8b, Llama3.1:8b, Qwen2.5:7b, Mistral:7b, Dolphin-Mistral:7b, Wizardlm2:7b, Codegemma:7b, Zephyr:7b, Qwen2:7b, Mistral-nemo:12b, Codestral:22b, Deepseek-coder-v2:16b, QwQ:32b, Gemma2-27b, Codellama:34b, Command-r:35b, Llama2:70b, Llama3.3:70b, Codellama:70b |
| **Method** | **No fine-tuning** — in-context/few-shot learning with dynamic context-example selection (Max Marginal Relevance), temperature 0.6 / top-p 0.3 (translation) and 0.3 / 0.5 (conflict detection), served via Ollama. |
| **Dataset** | **IBNBench** (new): Intent2Flow-ODL (**52 pairs**), Intent2Flow-ONOS (**50 pairs**), FlowConflict-ODL (**60 pairs**, 19 conflicting), FlowConflict-ONOS (**74 pairs**, 27 conflicting). Plus two existing: **Formal Specification (1,500 pairs)** and **NFV Configuration (120 pairs)**. 50/50 context/test split. |
| **Training hardware** | No training. **Inference hardware: AMD Ryzen Threadripper PRO 5995WX (64-core), 500 GB RAM, 1 × NVIDIA RTX A6000 (48 GB VRAM).** |
| **Inference latency / model size** | **Runtime reported per model.** Example: **Codellama-34b required over 10 seconds per inference, whereas Qwen2.5-7B achieved competitive performance in under 2 seconds.** 70B models could not be evaluated at larger context sizes "due to hardware memory constraints." |
| **Main quantitative results** | Accuracy by model size: **QwQ-fusion and Command-r (32–35B) ≥99%** on the Formal Specification dataset; **Codellama:7b and Mistral:7b up to 95% with lower latency**; mid-sized models gained **up to 20% accuracy** from 0→9 context examples (Dolphin-Mistral:7b jumped **0% → 80%**); smaller models (TinyLlama:1.1b, Deepseek-coder:1.3b) "show significantly lower accuracy"; **Llama3.3:70b reached 88% zero-shot on Intent2Flow-ONOS, surpassing Llama2:70b and Codellama:70b**, but **Codellama:22b (Codestral) outperformed Command-r:35b** on flow-rule tasks. Conflict detection (FlowConflict-ONOS): **QwQ:32b perfect (F1 1.0); Llama3.3:70b 94% accuracy, FPR 0.02, F1 0.78; Llama2:70b had perfect recall but 52 false positives**; Codellama:7b, Codegemma-7b, Dolphin-Mistral-7b, Deepseek-coder-1.3b exceeded **87% FPR**. |
| **Baselines** | All 33 LLMs serve as mutual baselines; the paper also benchmarks against prior IBN work (NetConfEval, NFV-configuration) |
| **Code/data public** | **Yes** — datasets and benchmarking results released (GitHub link referenced as [48] in the paper); NetIntent framework implementation released |
| **Main limitation** | **No fine-tuning** — so it does not test whether a *small fine-tuned* model could replace a large prompted one. Results are highly prompt- and schema-sensitive, which the authors acknowledge. |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2507.14398 ; Crossref API record for 10.1109/OJCOMS.2025.3642642 |

> **This is the strongest single piece of evidence for Question F**, because it benchmarks 33 models from 1.1B to 70B on the *same networking decision task* with the same prompts. Verdict: **model size is not a reliable predictor of network-decision quality.**

---

### 13. Telecom Foundation Models: Applications, Challenges, and Future Trends *(survey / framing)*

| Field | Value |
|---|---|
| **Authors** | Tahar Zanouda, Meysam Masoudi, Fitsum Gaim Gebre, et al. (4 authors: + Mischa Dohler) |
| **Year** | 2024 |
| **Venue** | **PREPRINT** — arXiv:2408.03964 [cs.NI] |
| **DOI** | 10.48550/arXiv.2408.03964 |
| **Status** | **PREPRINT** |
| **Base models** | n/a (conceptual paper) |
| **Method** | Conceptual process for developing Telecom Foundation Models (TFMs); discussion of orchestrating specialised TFMs for **network configuration, operation and maintenance** |
| **Dataset** | n/a |
| **Training hardware** | not reported |
| **Inference latency / model size** | not reported |
| **Main quantitative results** | None (position/survey paper) |
| **Baselines** | n/a |
| **Code/data public** | n/a |
| **Main limitation** | No experiments. Useful only for motivation/framing and citation-chaining. |
| **Source retrieved** | https://arxiv.org/abs/2408.03964 |

---

### 14. Think Less, Label Better: Multi-Stage Domain-Grounded Synthetic Data Generation for Fine-Tuning Large Language Models in Telecommunications

| Field | Value |
|---|---|
| **Authors** | Chenhua Shi, Gregor Macdonald, Bhavika Jalli, et al. (7 authors, Ericsson) |
| **Year** | 2026 (v1 Sep 2025, v2 Jan 2026) |
| **Venue** | **IEEE ICC 2026** (per the arXiv comment field) — **PREPRINT** (arXiv:2509.25736) |
| **DOI** | 10.48550/arXiv.2509.25736 |
| **Status** | **PREPRINT** (accepted at ICC 2026, but I verified only the arXiv version) |
| **Base models** | Retriever + base generator + refinement model pipeline (specific checkpoints **not verified**) |
| **Method** | Fully automated retrieval-augmented synthetic QA generation grounded in a domain knowledge graph; RAGAS-based scoring filters low-quality samples, producing a dataset for **reinforcement fine-tuning (RFT)** |
| **Dataset** | Synthetic RAN troubleshooting QA pairs (real-world telecom scenario). **Exact size not verified.** |
| **Training hardware** | **not verified** |
| **Inference latency / model size** | not reported |
| **Main quantitative results** | Produces "complex, context-rich troubleshooting solution plans without human intervention" — quantitative gains **not verified** |
| **Baselines** | not verified |
| **Code/data public** | Not found |
| **Main limitation** | A data-generation paper, not a compression or decision-quality paper. Relevant as the dataset provenance for refs. #6 and #7. Verification is abstract-level only. |
| **Source retrieved** | https://arxiv.org/abs/2509.25736 |

---

### 15. ORION: Intent-Aware Orchestration in Open RAN for SLA-Driven Network Management

| Field | Value |
|---|---|
| **Authors** | Gabriela da Silva Machado, Gustavo Z. Bruno, Alexandre Huff, et al. (5 authors: + Jose Marcos Camara Brito, Cristiano B. Both) |
| **Year** | 2026 |
| **Venue** | **PREPRINT** — arXiv:2603.03667 [cs.NI] |
| **DOI** | 10.48550/arXiv.2603.03667 |
| **Status** | **PREPRINT** |
| **Base models** | **GPT-5, Gemini 3 Pro, Claude Opus 4.5, GPT-5 Nano, Gemini 3 Flash, Claude Sonnet 4.5** (proprietary; **no fine-tuning**) |
| **Method** | Hierarchical agent architecture over the **Model Context Protocol (MCP)**: MCP-based SMO layer for semantic translation + Non-RT RIC rApp + Near-RT RIC xApp for closed-loop enforcement. No weight modification. |
| **Dataset** | 101 natural-language intents: **eMBB 20 samples, URLLC 20 samples, mMTC 60 samples** (mMTC oversampled for IoT heterogeneity) |
| **Training hardware** | No training. Deployment: **Open5GS (Release 16) on Kubernetes, 3 worker nodes × 8 vCPU / 32 GB RAM each** |
| **Inference latency / model size** | Reports latency/resource overhead of the MCP orchestration; **exact values not extracted** |
| **Main quantitative results** | **100% policy-generation success rate for high-capacity models.** 3GPP slice-type classification accuracy across 101 intents: **Claude Opus 4.5 99%, GPT-5 96%, GPT-5 Nano 90%, Gemini 3 Pro 77%, Gemini 3 Flash 66%, Claude Sonnet 4.5 13%.** Key finding: **"the primary bottleneck for intent-to-policy fidelity lies in the MCP tool orchestration layer rather than in the model's semantic understanding"** — among models with ≥97% prediction rate, accuracy spans 90–99%. |
| **Baselines** | Six frontier LLMs compared against each other |
| **Code/data public** | **Yes** — https://github.com/zanattabruno/analysis-orion (scripts, datasets, figures) |
| **Main limitation** | **No open-weight, no small, and no fine-tuned models** — so it says nothing about the compression/size question. The headline 100% figure is a *tool-invocation* success rate, not an end-to-end autonomy result. Preprint. |
| **Source retrieved** | https://arxiv.org/abs/2603.03667 ; https://arxiv.org/html/2603.03667 |

---

### 27. 5G INSTRUCT Forge: An Advanced Data Engineering Pipeline for Making LLMs Learn 5G

| Field | Value |
|---|---|
| **Authors** | Azzedine Idir Ait Said, Abdelkader Mekrache, Karim Boutiba, et al. (6 authors: + Kostas Ramantas, Adlen Ksentini, Moufida Rahmani) |
| **Year** | 2025 |
| **Venue** | **IEEE Transactions on Cognitive Communications and Networking (TCCN)**, vol. 11, no. 2, pp. 974–986 |
| **DOI** | 10.1109/TCCN.2024.3516055 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base models** | **Llama3-8B (16 GB), Solar-10.7B (21 GB), Mistral-7B (14 GB)** |
| **Method** | **"Freeze-tuning" (partial-parameter freezing) in the LLaMA Factory framework — LoRA explicitly REJECTED**: "we opted not to use LoRA due to the significant domain shift." Trainable parameters: **Llama3 9%, Solar 12%, Mistral 11%**; 4 epochs; lr 4e-5; per-device batch size 4. |
| **Dataset** | **OAI Instruct** dataset, generated by the 5G Instruct Forge pipeline from **22 3GPP Technical Specifications** used to develop OpenAirInterface (OAI); ≈80 MB. Evaluation: **>9,000 Q&A pairs** + a **5G exam of ~200 questions** (4 options each). |
| **Training hardware** | **Training: NOT REPORTED.** Deployment/inference: **a single machine with one NVIDIA A100 GPU (80 GB VRAM)**, temperature 0.7 |
| **Inference latency / model size** | **not reported** (base model sizes in GB reported: Llama3-8B 16 GB, Solar-10.7B 21 GB, Mistral-7B 14 GB; no compressed size) |
| **Main quantitative results** | 5G-aware fine-tuned LLMs **outperform OpenAI's GPT-4 on 5G-specific tasks.** ROUGE-L F1: fine-tuned models **0.55 / 0.58 vs GPT-4's 0.35**, while BERTScore F1 was close. **Trainable-parameter ablation for Mistral (MMLU / 5G exam): 6% → 21.99 / 164.0; 9% → 22.45 / 160.0; 11% → 19.84 / 101.0; 17% → MMLU collapses to 14.74.** The paper selects **11%** as the operating point. |
| **Baselines** | GPT-4 (`gpt-4-0125-preview`); Llama3-8B, Solar-10.7B, Mistral-7B in default vs 5G-aware versions |
| **Code/data public** | **NOT REPORTED** in the retrieved full text (the paper references OpenAirInterface, LLaMA Factory, finance-alpaca and lawinstruct as comparators) |
| **Main limitation** | The **MMLU trade-off is severe and implicit**: pushing trainable parameters beyond ~11% causes catastrophic forgetting of general knowledge (MMLU 14.74 at 17%). Hyperparameters had to be tuned per model. No latency, no compression. |
| **Source retrieved** | https://hal.science/hal-05045324v1/file/publi-8009.pdf (full text, HAL deposit) ; Crossref record 10.1109/TCCN.2024.3516055 |

> **Directly relevant to Questions B, D and E.** This is the second paper (with Tele-LLMs) to **explicitly reject LoRA** for domain adaptation — and unlike Tele-LLMs it quantifies the trade-off between trainable-parameter fraction, 5G-task accuracy and general-knowledge retention.

---

### 28. Understanding Telecom Language Through Large Language Models

| Field | Value |
|---|---|
| **Authors** | Lina Bariah, Hang Zou, Qiyang Zhao, et al. (6 authors: + Belkacem Mouhouche, Faouzi Bader, Merouane Debbah). Technology Innovation Institute, Abu Dhabi |
| **Year** | 2023 |
| **Venue** | **IEEE GLOBECOM 2023 (2023 IEEE Global Communications Conference)**, pp. 6542–6547 |
| **DOI** | 10.1109/GLOBECOM54140.2023.10437725 (preprint: arXiv 2306.07933; also TechRxiv 10.36227/techrxiv.23501271) |
| **Status** | **PEER-REVIEWED** (conference) + PREPRINT |
| **Base models** | **BERT-Base (uncased) 110M; DistilBERT 66M; RoBERTa 125M; GPT-2 smallest 124M** |
| **Method** | **Full single-task single-label fine-tuning** with an added linear + SoftMax classification head; cross-entropy loss; batch size 32; lr 2e-5; L2 regularisation 0.01 |
| **Dataset** | 3GPP technical documents (tdocs) from working groups RAN1–5, SA1–6, CT1/3/4/6; **train = tdocs 2009/2010–2019, test = tdocs 2020–April 2023**; text segmented at 200 words per segment |
| **Training hardware** | **not reported** |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | **BERT and RoBERTa 84.6% accuracy; GPT-2 83%**; DistilBERT ≈ equal accuracy with ~50% fewer parameters. Per-working-group-combination BERT accuracy: **RAN1/SA1/CT1 98.05%**; RAN1,2,3 only 88.90%; RAN1,2,3+SA1+CT1 88.26%; **full 15-WG setting 84.35%**. Accuracy increases with text-segment length, with diminishing returns. |
| **Baselines** | BERT vs DistilBERT vs RoBERTa vs GPT-2 cross-model comparison; cites a prior BERT-like telecom QA model trained on 347 documents / 2,021 Q&A pairs |
| **Code/data public** | **NOT REPORTED** (the paper notes the prior 2,021-QA dataset "is not publicly available") |
| **Main limitation** | The identified constraint is that **accuracy depends strongly on the working-group combination** and on **text-segment length** — "significant role of selecting the optimum size for a LLM, in order to strike a balance between performance and computing complexity". **DistilBERT is used as a comparison point, not produced by the authors — the paper applies no compression itself.** |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2306.07933 (full text) ; Crossref record 10.1109/GLOBECOM54140.2023.10437725 |

> **Historical note for the survey:** this is the earliest telecom LLM fine-tuning recipe found (2023, same group as TelecomGPT), and it is the only paper in the corpus that benchmarks a **distilled model (DistilBERT 66M) against its full-size teacher (BERT-Base 110M) on a telecom task** — finding ~equal accuracy at ~50% fewer parameters.

---

### 29. TSpec-LLM: An Open-source Dataset for LLM Understanding of 3GPP Specifications

| Field | Value |
|---|---|
| **Authors** | Rasoul Nikbakht, Mohamed Benzaghta, Giovanni Geraci |
| **Year** | 2024 |
| **Venue** | **2024 IEEE Globecom Workshops (GC Wkshps)**, pp. 1–6 |
| **DOI** | 10.1109/GCWkshp64532.2024.11101012 (preprint: arXiv 2406.01768) |
| **Status** | **PEER-REVIEWED** (workshop) + PREPRINT |
| **Base models** | Not trained by the authors. Evaluates **GPT-3.5, GPT-4, Gemini 1.0 Pro** with naive-RAG. |
| **Method** | Dataset + naive-RAG benchmark. **No fine-tuning, no compression.** |
| **Dataset** | **30,137 documents · 13.5 GB · 535 million words** — all 3GPP documents **Release 8 → Release 19 (1999–2023)**, tables and formulas retained, released as Markdown |
| **Training hardware** | not applicable |
| **Inference latency / model size** | not reported |
| **Main quantitative results** | Naive-RAG over TSpec-LLM: **GPT-3.5 44% → 71%; Gemini 1.0 Pro 46% → 75%; GPT-4 51% → 72%.** Baseline (no RAG): GPT-4 51%, Gemini 46%, GPT-3.5 44%. |
| **Baselines** | GPT-3.5, GPT-4, Gemini 1.0 Pro, each with and without RAG |
| **Code/data public** | Open-source dataset, questionnaire and prompts released (`download3gpp 0.7.0` tooling); specific URLs **not verified** |
| **Main limitation** | RAG retrieval, not model adaptation — so it improves accuracy without changing model size, which makes it a **direct alternative to compression** for edge deployment and should be presented as such. |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2406.01768 ; Crossref record 10.1109/GCWkshp64532.2024.11101012 |

> **Critical link:** TSpec-LLM is the retrieval corpus used by paper #10 (NetSoft 2025). It is the standard 3GPP dataset for this field and belongs in a dataset-provenance section.

---

### 30. SPEC5G: A Dataset for 5G Cellular Network Protocol Analysis

| Field | Value |
|---|---|
| **Authors** | Imtiaz Karim, Kazi Samin Mubasshir, Mirza Masfiqur Rahman, et al. (4 authors: + Elisa Bertino) |
| **Year** | 2023 |
| **Venue** | **Findings of the Association for Computational Linguistics: IJCNLP-AACL 2023 (Findings)**, pp. 20–38 |
| **DOI** | 10.18653/v1/2023.findings-ijcnlp.3 |
| **Status** | **PEER-REVIEWED** (ACL Findings) |
| **Base model / method / hardware / latency / results** | **NOT VERIFIED** — only the Crossref bibliographic record was retrieved. |
| **What it is** | A 3GPP specification-derived dataset (a *subset* of documents, filtered to remove tables/symbols), created for 5G protocol analysis; used as a comparator by TSpec-LLM. |
| **Main limitation** | **Verification gap.** Include as a dataset citation only, with the ACL Findings DOI. |
| **Source retrieved** | Crossref bibliographic query (record 10.18653/v1/2023.findings-ijcnlp.3) |

---

### 31. Telco-RAG: Navigating the Challenges of Retrieval Augmented Language Models for Telecommunications

| Field | Value |
|---|---|
| **Authors** | Andrei-Laurentiu Bornea, Fadhel Ayed, Antonio De Domenico, et al. (5 authors: + Nicola Piovesan, Ali Maatouk) |
| **Year** | 2024 |
| **Venue** | **IEEE GLOBECOM 2024 (2024 IEEE Global Communications Conference)**, pp. 2359–2364 |
| **DOI** | 10.1109/GLOBECOM52923.2024.10901158 (preprint: arXiv 2404.15939) |
| **Status** | **PEER-REVIEWED** (conference) + PREPRINT |
| **Base model / fine-tuning / hardware / latency / compression** | **N/A or not reported** — this is a **RAG pipeline, not a trained model**. Contributes a dual-stage query-enhancement + retrieval process, a **neural-network router that reduces RAM usage**, and hyperparameter optimisation (chunk size, context length, embedding model) over 3GPP documents. |
| **Code public** | **Yes** — https://github.com/netop-team/Telco-RAG (verified; the README reproduces the arXiv citation and DOI) |
| **Main limitation** | No fine-tuning and no compression. Notably, the **neural-network router that reduces RAM usage is a memory-efficiency technique for telecom LLM deployment** and is therefore adjacent evidence for Question C/E. |
| **Source retrieved** | https://arxiv.org/abs/2404.15939 ; https://raw.githubusercontent.com/netop-team/Telco-RAG/main/README.md ; Crossref record 10.1109/GLOBECOM52923.2024.10901158 |

---

### 32. ORANSight-2.0: Foundational LLMs for O-RAN

| Field | Value |
|---|---|
| **Authors** | Pranshav Gajjar, Vijay K. Shah, et al. |
| **Year** | 2025 |
| **Venue** | **IEEE Transactions on Machine Learning in Communications and Networking (TMLCN)**, vol. 3, pp. 903-920 |
| **DOI** | 10.1109/TMLCN.2025.3592658 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base models** | **18 open LLMs spanning 1B-70B** |
| **Method** | **QLoRA 4-bit** fine-tuning, **rank/alpha <= 256**, **1 epoch** |
| **Dataset** | **RANSTRUCT - 151,500 instruction-answer pairs** (58.6% srsRAN code, 41.4% O-RAN specifications) |
| **Training hardware** | **A SINGLE NVIDIA RTX 4090, 24 GB VRAM** |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | **+5.421% over ChatGPT-4o and Gemini on ORANBench; +18.465% on srsRANBench** |
| **Baselines** | ChatGPT-4o, Gemini (and 17 other open LLMs 1B-70B) |
| **Code/data public** | **Yes** - https://github.com/prnshv/ORAN-Bench-13K ; Hugging Face org `NextGLab` |
| **Main limitation** | Benchmarks are domain-QA/code benchmarks, **not network KPIs or closed-loop RAN control**. "Foundational LLMs" in the title means domain-adapted general LLMs, not a new architecture. |
| **Source retrieved** | Crossref record 10.1109/TMLCN.2025.3592658 (title, authors, venue, volume, pages verified) |

> **The most important addition for Question C.** ORANSight-2.0 is a **peer-reviewed IEEE TMLCN paper** showing that **QLoRA 4-bit fine-tuning of up to 70B-parameter models on 151,500 O-RAN instruction pairs is achievable on a single 24 GB consumer GPU (RTX 4090) in one epoch.** This sets the true floor for GPU requirements in this field - substantially lower than the A6000/A100 configurations reported elsewhere. *(Verification note: bibliographic data confirmed via Crossref; technical figures come from a parallel verification pass that read the full text. Treat the numeric results as single-source until the PDF is checked directly.)*

---

### 33. SafeCOMM: A Study on Safety Degradation in Fine-Tuned Telecom Large Language Models

| Field | Value |
|---|---|
| **Authors** | Aladin Djuhera, Swanand Ravindra Kadhe, Farhan Ahmed, et al. (7 authors: + Syed Zawad, Fernando Koch, Walid Saad, Holger Boche) |
| **Year** | 2026 |
| **Venue** | **2026 IEEE Wireless Communications and Networking Conference (WCNC)**, pp. 1-6 |
| **DOI** | 10.1109/WCNC65185.2026.11555432 (preprint: arXiv 2506.00062) |
| **Status** | **PEER-REVIEWED** (conference) + PREPRINT |
| **Base models** | General-purpose LLMs fine-tuned on telecom data; plus the publicly released **Tele-LLMs** |
| **Method** | SFT on three telecom datasets, followed by three **realignment defenses: SafeInstruct, SafeLoRA, SafeMERGE** |
| **Dataset** | **TeleQnA (8k)**, **TeleData (600k)**, **TSpecLLM (80)**; new **TeleHarm** red-teaming benchmark; established **DirectHarm** and **HexPhi** |
| **Training hardware** | **not verified** |
| **Inference latency / model size** | not reported |
| **Main quantitative results** | **Safety degrades even for light telecom domain adaptation.** Notably: **continually-pretrained Tele-LLMs reach ~90% harmfulness**, "primarily due to the omission of safety-focused instruction tuning." SafeInstruct / SafeLoRA / SafeMERGE **restore safety without hurting task utility**. |
| **Baselines** | Pre-fine-tuning (aligned) models; DirectHarm and HexPhi benchmarks |
| **Code/data public** | TeleHarm benchmark introduced; release URL **not verified** |
| **Main limitation** | A safety paper, not a compression paper - but **highly citable for a limitations/risk section**, and it directly implicates the Tele-LLMs recipe (#3) as unsafe. |
| **Source retrieved** | https://arxiv.org/abs/2506.00062 (title, authors, abstract) ; Crossref record 10.1109/WCNC65185.2026.11555432 |

> **Important cross-reference:** this paper is **evidence against** the otherwise rosy picture of domain-adapted telecom LLMs. Any survey section on "deploying a fine-tuned telecom LLM in a network operations centre" should cite it.

---

### 34. TelcoLM: Collecting Data, Adapting, and Benchmarking Language Models for the Telecommunication Domain

| Field | Value |
|---|---|
| **Authors** | Camille Barboule, Viet-Phi Huynh, Adrien Bufort, et al. (6 authors: + Yoan Chabot, Geraldine Damnati, Gwenole Lecorve). **Orange** |
| **Year** | 2024 (achieved March 2024, released December 2024) |
| **Venue** | **PREPRINT** - arXiv:2412.15891 (30 pages: 13 main + 17 appendices, 22 tables) |
| **DOI** | 10.48550/arXiv.2412.15891 |
| **Status** | **PREPRINT** |
| **Base model** | **Llama-2-7b** |
| **Method** | **DAPT** (domain-adaptive pre-training / continual pretraining) + **IAPT** (instruction-adaptive pre-training / instruction tuning). **Key finding: adaptation can be restricted to a single instruction-tuning step, discarding the need for fine-tuning on raw texts beforehand; IAPT alone is approximately equal to DAPT+IAPT. Blended domain + general instructions works best.** |
| **Dataset** | 800M tokens of domain-specific telco data + **80K instructions** |
| **Training hardware** | **2 x A100-80GB (DAPT) and 2 x A100-40GB (IAPT)** - one of the very few papers in this corpus reporting concrete GPU models |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | "Domain-adapted models can challenge the large generalist models" on downstream tasks requiring extensive telecom knowledge |
| **Baselines** | Larger generalist models |
| **Code/data public** | not verified |
| **Main limitation** | Preprint, and exact result tables not verified. The key actionable claim - **DAPT is unnecessary if you do IAPT well** - is a direct cost-saving finding that contradicts the TelecomGPT three-stage recipe and deserves explicit comparison. |
| **Source retrieved** | https://arxiv.org/abs/2412.15891 (title, authors, abstract, comments) |

---

### 35. TelecomGPT-R1: A Unified Open-Source Reasoner for the Telecom Stack

| Field | Value |
|---|---|
| **Authors** | Bohao Wang, Chenwei Wu, Haoyu Li, et al. (11 authors: + Hang Zou, Yu Tian, Lina Bariah, Li Wei, Chongwen Huang, Yongliang Shen, Zhaoyang Zhang, Merouane Debbah) |
| **Year** | 2026 |
| **Venue** | **PREPRINT** - arXiv:2608.26126 |
| **DOI** | 10.48550/arXiv.2608.26126 |
| **Status** | **PREPRINT** |
| **Base model** | **Qwen3.5-9B** |
| **Method** | Two-stage: **LoRA-SFT (r=128)** then **GRPO/DAPO** reinforcement post-training |
| **Dataset** | **67,427-example SFT corpus** organised around four reasoning axes (protocol, knowledge, modeling, fault), built from axis-matched public web sources + axis-specific chain-of-thought generation + prefix-continuation self-validation |
| **Training hardware** | **8 x H200** |
| **Inference latency / model size** | **not reported** |
| **Main quantitative results** | **TelecomGPT-R1-9B "ranks top-performing on the GSMA open telco leaderboard"; 82.1% GSMA seven-axis mean** |
| **Baselines** | GSMA open telco leaderboard entries |
| **Code/data public** | "release" implied (open-source reasoner); URL **not verified** |
| **Main limitation** | Preprint. It is a **direct follow-up to TelecomGPT (#2) by an overlapping author group**, moving from QLoRA-SFT to **RL post-training** - worth its own subsection as the field's trajectory. Evaluated on the GSMA leaderboard (knowledge/reasoning), **not on network KPIs**. |
| **Source retrieved** | https://arxiv.org/abs/2608.26126 (title, authors, abstract) |

---

### Additional telecom LLM works verified via Crossref (peer-reviewed; technical detail not independently retrieved)

| # | Title | Authors (first 3 + et al.) | Year | Venue | DOI | Note |
|---|---|---|---|---|---|---|
| 36 | **TeleCom-Bench** | Xiao, Lin, Qiu et al. (13 authors) | 2026 | **KDD '26**, pp. 10056–10067 | 10.1145/3770855.3817480 *(Crossref lookup returned no record for this DOI — **treat as unverified**)* | **22,678 samples; documents an "Execution Wall": >90% on intent recognition / entity extraction but ~30% on solution generation** — a directly relevant capability-gap result |
| 37 | **AI²MMUM: AI-AI Oriented Multi-Modal Universal Model Leveraging Telecom Domain Large Model** | Tianyu Jiao, Yin Xu, Zhuoran Xiao, et al. | 2025 | **IEEE Wireless Communications Letters**, vol. 14, no. 8, pp. 2651–2655 | 10.1109/LWC.2025.3578370 | Telecom LLM backbone + **LoRA** + frozen radio encoders; SOTA on five physical-layer tasks. **Backbone identity and compression details not verified** |
| 38 | **TelecomRAG: Taming Telecom Standards with Retrieval Augmented Generation and LLMs** | Girma M. Yilma, Jose A. Ayala-Romero, Andres Garcia-Saavedra, et al. (+ Xavier Costa-Perez). NEC Labs Europe | 2024 | **ACM SIGCOMM Computer Communication Review (CCR)**, vol. 54, no. 3, pp. 18–23 | 10.1145/3711992.3711996 | **⚠️ DISTINCT from Telco-RAG (#31) — two unrelated papers with similar names. Do not conflate.** |
| 39 | **TelBench: A Benchmark for Evaluating Telco-Specific Large Language Models** | Sunwoo Lee, Dhammiko Arya, Seung-Mo Cho, et al. (+ Gyoung-eun Han). SK Telecom | 2024 | **EMNLP 2024 Industry Track**, pp. 609–626 | 10.18653/v1/2024.emnlp-industry.45 | Industrial telco LLM benchmark |
| 40 | **ORAN-Bench-13K** | (see IEEE record) | 2025 | **IEEE CCNC 2025**, pp. 1–4 | 10.1109/CCNC54725.2025.10975994 | 13,952 MCQs from 116 O-RAN specifications |
| 41 | **TelcoAI** | (see ACL Anthology) | 2025 | **Findings of IJCNLP-AACL 2025**, pp. 1305–1317 | 10.18653/v1/2025.findings-ijcnlp.80 | Reported 87% recall / 92% faithfulness (numbers **not independently verified**) |
| 42 | **Chat3GPP** | (see IEEE record) | 2025 | **IEEE ICC Workshops 2025**, pp. 492–497 | 10.1109/ICCWorkshops67674.2025.11162262 | 3GPP assistant |
| 43 | **NextG-GPT** | (see IEEE record) | 2025 | **IEEE ICCCN 2025**, pp. 1–9 | 10.1109/ICCCN65249.2025.11133874 | LLaMA-3.1-70B: 86.2% correctness, 90.6% answer relevancy |
| 44 | **TeleMath** | (see IEEE record) | 2026 | **IEEE Network** (early access) | 10.1109/MNET.2026.3658826 | Telecom math benchmark |
| 45 | **TSLAM-Mini** | (see arXiv) | 2025 | **PREPRINT** — arXiv:2505.07877 | 10.48550/arXiv.2505.07877 | Phi-4-Mini-Instruct **4B**; **QLoRA NF4 4-bit, r=16, α=32**; **100,000 samples / 20 telecom use cases**; mean token accuracy 0.9679 |
| 46 | **OTel (Open Telco)** | Tavakkoli, Paulk, Terrazas et al. (AT&T / GSMA) | 2026 | **PREPRINT** — arXiv:2608.15436 | 10.48550/arXiv.2608.15436 | **30 full-parameter post-trained baselines**; ~1.1M raw → **326,767 cleaned examples**; **AMD MI300X/MI325X/MI355X + NVIDIA A100/H100**; LM correctness 88.2% |
| 47 | **TSLAM-8B** | NetoAI | 2025 | **GREY LITERATURE — vendor AWS engineering blog, NOT peer-reviewed** | no DOI | Llama-3.1-8B + LoRA on AWS Trainium `trn1.32xlarge`. **⚠️ The ONLY source in the entire search reporting an inference latency for a telecom LLM: 300–500 ms on AWS Inferentia2.** Also 86.2 vs Llama-3.1-8B's 63.1. **Cite with the non-peer-reviewed caveat** |
| 48 | **Solving AI Foundational Model Latency with Telco Infrastructure** | Barros | 2025 | **PREPRINT** — arXiv:2504.03708 | 10.48550/arXiv.2504.03708 | Best dedicated lead for the **latency** question; detail not verified |

> **Naming caution:** the literature now contains **Telco-RAG** (#31, Bornea et al., GLOBECOM 2024), **TelecomRAG** (#38, Yilma et al., ACM CCR 2024), and **three distinct things called "TrafficLLM"** — (a) a GitHub repo (`ZGC-LLM-Safety/TrafficLLM`) that MERLOT benchmarks against and which has **no DOI or venue**; (b) arXiv:2504.04222 (Cui et al., 10 scenarios / 229 traffic types, F1 0.9875 detection / 0.9483 generation, **PEFT but no compression**); (c) Ginige et al., *Computer Networks* 2026, DOI 10.1016/j.comnet.2025.111847 (open-set encrypted traffic). **Check which one a citation means before reusing it.**

---

### ⚠️ Leads explicitly NOT confirmed as real papers

| Search term | Finding |
|---|---|
| **"Telco-LLM"** (e.g. *"Telco-LLM: Towards a Foundation Model for the Telecommunications Industry"*) | **NOT FOUND.** Crossref bibliographic queries return only unrelated telecom business/industry articles. Web search surfaced only the **GSMA Open-Telco LLM Benchmarks** industry initiative (an MWC Barcelona benchmark programme, **not a peer-reviewed paper**) whose technical details were not verified. **Do NOT cite "Telco-LLM" as a paper without further verification.** |
| **"TelecomLLM"** | **NOT FOUND** as a distinct titled paper in Crossref or arXiv searches performed. |
| **"LLaMA-Telecom"** | **NOT FOUND** as a titled paper. The real works in this space are the **`*-Tele` model family** (Tele-LLMs, #3) and **Mobile-LLaMA** (#1). |
| **"TMF921-Grounded Intent-to-Network-Configuration Dataset for 5G/6G"** | Appeared only as a Hugging Face dataset card referencing `arXiv:2603.03667`; that ID resolves to a **different** paper (ORION, #15). Excluded rather than mis-attributed. |
| Telco-oRAG; Hermes (autonomous networks); AI-native Interconnect Framework for 6G | Surfaced as arXiv leads (`2505.11856`, `2411.06490`, `2311.05842`). **Venue/DOI/authors NOT VERIFIED.** |

---

<a name="group-ii"></a>
## Group (ii) — Pruning, quantization & distillation for networking LLMs
### 16. MERLOT: A Distilled LLM-based Mixture-of-Experts Framework for Scalable Encrypted Traffic Classification

| Field | Value |
|---|---|
| **Authors** | Yuxuan Chen, Rongpeng Li, Xutong Li, et al. (5 authors: + Zhifeng Zhao, Honggang Zhang) |
| **Year** | 2025 (preprint v1 Nov 2024) |
| **Venue** | **2025 IEEE Globecom Workshops (GC Wkshps)**, pp. 98–103 |
| **DOI** | 10.1109/GCWkshps68340.2025.11591188 (preprint: 10.48550/arXiv.2411.13004) |
| **Status** | **PEER-REVIEWED** (workshop paper) + PREPRINT (arXiv:2411.13004). Note the published version adds a 5th author (Xutong Li) vs. 4 on arXiv. |
| **Base model** | **GPT-2-base** — 12 layers, hidden dim 768, **~117M parameters** |
| **Compression method** | **(a) Knowledge distillation** — teacher–student, composite loss `L = (1−α)·CE(student, hard label) + α·KL(student ‖ teacher)`; **verified hyperparameters: α = 0.5, temperature = 2.0** (ablation over α∈{0.4, 0.5, 0.6}, T∈{1.0, 2.0, 3.0}; best F1 0.9953 on USTC TFC 2016). Teacher = GPT-2-base (12 layers, 117M). **Each student expert = 3 transformer layers, hidden 768, ≈85M params**; MoE = **10 experts + 1 gating network**. 5 epochs, 95:5 split. **(b) Pruning** — the MoE gating function is "implemented as a distilled, **pruned** GPT-2-base model." **(c) MoE with hard one-hot gating** — exactly one expert activated per input. **(d) Architectural change** — direct classification from the final decoder token instead of generative/prompt-based classification. |
| **⚠️ Internal inconsistency in the paper** | It states "600-million-parameter MERLOT" **and** "0.66-billion" **and** "the gating network has 935-million parameters" — but 10 × 85M + 935M ≠ 660M. **Reported verbatim; not resolved.** |
| **Dataset** | **10 encrypted-traffic datasets, ~527.6K samples total**: APP-53 2023 (109.8K / 54 labels), CSIC 2010 (34.5K / 2), CSTNET 2023 (97.6K / 20), CW-100 2018 (7.4K / 100), DAPT 2020 (10.0K / 2), DoHBrw 2020 (47.8K / 2), ISCX Botnet 2014 (25.0K / 5), ISCX Tor 2016 (40.0K / 8), ISCX VPN 2016 (64.8K / 14), USTC TFC 2016 (50.7K / 20) |
| **Training hardware** | **NVIDIA A800 GPU** (count not reported). *(From a parallel full-text verification pass; not independently re-verified by me.)* |
| **Inference latency / model size** | **Model sizes: MERLOT 500M / 660M / 1.25B parameters** (the MoE aggregates multiple distilled experts, so it is *not* sub-117M). **"Consumes 85–90% less inference time and memory usage" than 7B TrafficLLM** — but **no absolute ms or MB figure is reported**. |
| **Main quantitative results** | MERLOT (660M) F1 vs. TrafficLLM (7B) vs. ET-BERT: **ISCX Tor 2016 0.9845 / 0.9810 / 0.9368; ISCX VPN 2016 0.9920 / 0.9970 / 0.9539; CSTNET 2023 0.9996 / 0.9599 / 0.9496; ISCX Botnet 2014 0.9992 / 0.9992 / 0.9489; USTC TFC 2016 0.9953 / 0.9950 / 0.9587; CIC-DoHBrw 2020 0.9999 / 0.9939 / 0.8467; DAPT 2020 0.9635 / 0.9810 / 0.9435; CSIC 2010 0.9906 / 0.9845 / 0.8995.** **MERLOT LOSES on APP-53 2023 (0.8601 vs 0.9320) and CW-100 2018 (0.8466 vs 0.9366).** The 1.25B variant recovers to 0.8702 / 0.8892. |
| **Baselines** | TrafficLLM (7B Llama2-based), ET-BERT (110M), and NetGPT (117M) as context |
| **Code/data public** | Not found |
| **Main limitation** | Losses on two of ten datasets (APP-53, CW-100) — the compression is **not uniformly lossless**. No training hardware, no absolute latency, no compressed size in MB. The paper's own framing concedes TrafficLLM's higher F1 on VPN 2016. Workshop paper, 5 pages. |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2411.13004 ; Crossref API record for 10.1109/GCWkshps68340.2025.11591188 |

---

### 17. Distilling Large Language Models for Network Active Queue Management (AQM-LLM)

> **⚠️ TERMINOLOGY CORRECTION — this paper does NOT perform knowledge distillation.** Despite the title, I verified in the full text that there is **no teacher–student KD anywhere in it**. The mechanism is **LoRA (rank r=128) + a data-driven reinforcement-learning adaptation pipeline**. The paper uses "distillation" loosely to mean "transferring knowledge from existing AQM algorithms into an LLM via offline RL". Its "99% parameter reduction" is a **reduction in *trainable* parameters (7B → 70M), which does NOT reduce inference cost** — the 7B weights remain at serving time. The authors themselves state in the conclusion: *"further refinement via pruning, quantization, and distillation toward small-language-model-based AQM can enhance scalability and resource efficiency"* — i.e. they identify real compression as **future work**. **Do not cite this as compression or KD evidence.**

| Field | Value |
|---|---|
| **Authors** | Shiva Raj Pokhrel, Deol Satish, Jonathan Kua, et al. (4 authors: + Anwar Walid) |
| **Year** | 2026 (arXiv v1 Jan 2025, v3 Sep 2025) |
| **Venue** | **IEEE Transactions on Networking (TON)**, vol. 34, pp. 5501–5513 |
| **DOI** | 10.1109/TON.2026.3690076 (preprint: 10.48550/arXiv.2501.16734) |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT (arXiv:2501.16734; **v2 was withdrawn**, only v3 is valid; journal_ref says "IEEE Trans on Networking, 2025") |
| **Base models** | **Llama2-7B** (primary), **OPT-1.3B**, **GPT-2 (125M)**, **T5-LLM (220M)** |
| **Method** | **LoRA (rank r=128)** + offline/data-driven **reinforcement learning**; improved state encoder mapping network metrics to token embeddings (4096-dim for Llama2); extended LLM head giving **single-inference** congestion decisions (enqueue / drop / ECN-mark). **No KD, no pruning, no quantization.** |
| **Task / dataset** | L4S (RFC 9330) active queue management with ECN marking (RFC 9331) + periodic packet dropping; **FreeBSD-14** open-source implementation; DCTCP and UDP Prague protocols. Dataset = pre-collected traces from existing AQM algorithms; **size not reported**. |
| **Training hardware** | **Two NVIDIA A40 (48 GB)** → Llama2 needs **23.91 GB VRAM**; OPT 7 GB; GPT-2 3.6 GB; T5-LLM 2.32 GB. (The paper also mentions RTX 4090 / 128 GB RAM / 13th-gen i9 as generic "high-end hardware" for LLM fine-tuning.) |
| **Training time** | **>20 hours for Llama2-7B**, versus **sub-hour** for OPT / GPT-2 / T5 |
| **Inference latency / model size** | **Un-adapted Llama2-7B: 0.200 s per answer. LoRA-adapted: Llama2 0.0391 s, OPT 0.0395 s, GPT-2 0.0414 s, T5-LLM 0.0411 s — ~80% inference-time reduction, ~5× speedup.** Model size unchanged (7B). LoRA gives **−64% GPU memory and −15.1% training time**. |
| **Main quantitative results** | **Llama2-7B 97.56% accuracy vs 82–83% plateau for OPT, GPT-2 and T5-LLM.** LoRA reduces trainable params from **7B → ~70M (1%)** while maintaining accuracy. Reduced delay variability and enhanced bandwidth utilisation across DCTCP and UDP Prague. |
| **Baselines** | OPT-1.3B, GPT-2, T5-LLM; classical AQM algorithms (RED, CoDel, PIE, CAKE) discussed as complementary |
| **Code/data public** | **Yes** — https://github.com/MPTCP-FreeBSD/L4S-LLM |
| **Main limitation** | **No compression is performed** — "99% parameter reduction" refers to trainable parameters only and does not reduce serving cost; the 7B model still requires 23.91 GB VRAM. Latency of **39 ms** is far above packet-processing budgets (the authors target sub-millisecond as future work). >20 h training for a marginal accuracy gain over much smaller models (97.56% vs 82–83%) is a poor cost/benefit trade that the paper does not analyse. |
| **Source retrieved** | https://arxiv.org/html/2501.16734v3 (full text, verified by me) ; Crossref record 10.1109/TON.2026.3690076 |

> **Value to the survey:** this is a **methodological cautionary case**. It shows that "distillation" is used loosely in the networking-LLM literature to describe PEFT and offline-RL adaptation. A survey that counts papers by title keyword will over-count distillation evidence. **Two such cases are documented in this corpus: AQM-LLM (#17) and Cost-Efficient KD-enabled Student Placement (#23, a placement optimisation problem, not an empirical distillation study).**

---

### 18. Pruned Traffic Trees: Native Semantic Compression with a Protocol-Structured Model Family for Encrypted Traffic Classification

| Field | Value |
|---|---|
| **Authors** | Yuantu Luo, Jun Tao, Xiangyu Xu, et al. (5 authors: + Linxiao Yu, Kangying Li) |
| **Year** | 2026 |
| **Venue** | **PREPRINT** — arXiv:2608.21874; comment: "This paper is submitted to INFOCOM 2027" |
| **DOI** | 10.48550/arXiv.2608.21874 |
| **Status** | **PREPRINT** |
| **Base model** | Not a pretrained LLM — a **protocol-structured model family** built on **Protocol Tree Graphs (PTGs)** with flow-level self-supervised learning. Parameter count: reported only as *relative reductions*. |
| **Compression method** | **(a) Structured pruning at the protocol level** — learned field salience + **TopK + k closure** selects which protocol fields and structural contexts to retain, producing "Distilled PTGs" (PTG-Ds). This treats **native protocol structure as the compression unit** rather than weights/channels/hidden representations. **(b) Width reduction** via structure-aligned transfer. **(c) Flow-level logits distillation.** Three levels: PTT-Full → PTT-Distilled → PTT-Lite. |
| **Dataset** | **CSTNET-TLS1.3** and **CipherSpectrum**, under flow-disjoint and Strong Information (SII)-masked settings. Sample counts **not extracted**. |
| **Training hardware** | **not reported** (CPU inference speedups are reported, implying CPU evaluation) |
| **Inference latency / model size** | **PTT-Lite: 80.3% fewer parameters (CSTNET-TLS1.3) and 61.3% fewer parameters (CipherSpectrum); 98.85% / 98.78% lower effective GFLOPs; 8.75× / 8.46× CPU inference speedups.** |
| **Main quantitative results** | **Macro-F1: PTT-Full 0.9519 (CSTNET-TLS1.3) / 0.9416 (CipherSpectrum); PTT-Lite retains 0.9325 / 0.9136.** So the compression costs **≈1.9 and ≈2.8 Macro-F1 points** for 80.3%/61.3% parameter reduction. |
| **Baselines** | Existing compression methods that "operate on weights, channels, hidden representations, or predictions" |
| **Code/data public** | Not confirmed |
| **Main limitation** | Preprint under review (INFOCOM 2027), not peer-reviewed. The compressed model is a **purpose-built protocol-structured architecture, not an LLM** — so the transferability of the finding to LLM compression is an open question. |
| **Source retrieved** | https://arxiv.org/abs/2608.21874 |

---

### 19. SQLLM: A Secure and Quantized Framework for Large Language Models in 5G Private Network Operations

| Field | Value |
|---|---|
| **Authors** | Jian Ma, Tong Liu, Yimeng Shang, et al. (8 authors: + Nan Hu, Lei Xia, Peizhen Liao, Yitong Shang) |
| **Year** | 2026 (early online 26 Jan 2026) |
| **Venue** | **IEEE Transactions on Consumer Electronics (TCE)**, vol. 72, no. 3, pp. 7552–7564 |
| **DOI** | 10.1109/TCE.2026.3657983 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base model** | **not verified** (paywalled full text) |
| **Compression method** | **LoRA fine-tuning + static quantization** with a **dynamic smoothing factor α** (migrates outlier variance from activations to weights) and **hybrid per-tensor / per-token granularity** |
| **Task / dataset** | Detecting abnormal user query-based network attacks in **5G private network operations**; 1 normal + 3 attack question classes. Dataset name/size **not verified**. |
| **Training hardware** | **not verified** |
| **Inference latency / model size** | The abstract-level claim reports **VRAM consumption** and **inference time** as metrics, but the **exact values could not be retrieved** (full text paywalled) |
| **Main quantitative results** | Reports **accuracy, VRAM consumption, inference time** — **exact values not verified** |
| **Baselines** | **not verified** |
| **Code/data public** | not verified |
| **Main limitation** | **Verification gap — abstract-level only.** Also: the HKUST Pure portal lists this under "Department of Civil and Environmental Engineering", which is likely a portal indexing artifact and should not be cited as an affiliation. Task is **attack/anomaly classification of queries**, not network configuration or closed-loop control. |
| **Source retrieved** | Crossref API record for 10.1109/TCE.2026.3657983 ; https://researchportal.hkust.edu.hk/en/publications/sqllm-a-secure-and-quantized-framework-for-large-language-models-/ |

---

### 20. Toward 6G Edge Intelligence: Lightweight LLMs for Intent-Driven Network Automation (KGLlama-KD)

| Field | Value |
|---|---|
| **Authors** | Bing Wu, Sai Zou, Minghui Liwang, et al. (6 authors: + Wei Ni, Xianbin Wang, Youliang Tian) |
| **Year** | 2026 |
| **Venue** | **IEEE Transactions on Mobile Computing (TMC)**, vol. 25, no. 9, pp. 14352–14365 |
| **DOI** | 10.1109/TMC.2026.3678546 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base model** | **Llama 3** (parameter count **not reported** in the abstract record) |
| **Compression method** | **Knowledge distillation (KD)** combined with a **knowledge graph (KG)**. Two-phase optimisation: (1) fine-tune the LLM with KG guidance **in the cloud**; (2) **compress via KD**, then deploy the distilled student on resource-constrained edge nodes. The KG formally describes relations among application scenarios, functional primitives, performance requirements within APPIs, and APPIs↔NSR correspondences, producing a structured intent training dataset. |
| **Task / dataset** | Intent-driven networking: translating heterogeneous **application intents (APPIs)** into **network service requests (NSRs)**. Dataset is KG-derived and structured (size **not reported**). |
| **Training hardware** | "cloud" fine-tuning then edge deployment — **specific GPU type/count not reported** in the record retrieved |
| **Inference latency / model size** | **"The distilled model reduces inference latency by 60% compared to full-scale LLMs, fulfilling the sub-100 ms requirement for 6G latency-sensitive services."** Post-distillation parameter count: **not reported**. |
| **Main quantitative results** | **95% accuracy for APPI understanding, surpassing DeepSeek and Qwen by an average of 8%.** |
| **Baselines** | DeepSeek and Qwen (general-purpose LLMs) |
| **Code/data public** | not verified |
| **Main limitation** | Only the institutional-repository abstract was retrievable; full experimental detail (hardware, model size, dataset size, latency distributions) is behind IEEE paywall. |
| **Source retrieved** | https://ro.ecu.edu.au/ecuworks2022-2026/8058/ ; https://ieeexplore.ieee.org/abstract/document/11457733 |

> **This is the best available evidence for Question E on distillation**: a 60% inference-latency reduction with 95% task accuracy, in an IEEE TMC paper, on an intent-driven network-automation task.

---

### 21. xApp distillation: AI-based conflict mitigation in B5G O-RAN

| Field | Value |
|---|---|
| **Authors** | Hakan Erdol, Xiaoyang Wang, Robert Piechocki, et al. (4 authors: + George Oikonomou). Univ. of Bristol |
| **Year** | 2026 (SSRN preprint 2025) |
| **Venue** | **Computer Networks (Elsevier)**, vol. 274, art. 111848 |
| **DOI** | 10.1016/j.comnet.2025.111848 (preprint DOI: 10.2139/ssrn.5278781) |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT (SSRN) |
| **Base model** | **not verified** (paywalled full text) — this is xApp (not LLM) distillation |
| **Compression method** | **Knowledge distillation of xApp control policies**: a teacher network's policy is distilled into a student, with **the distillation loss choice examined explicitly** ("When distilling policy from a teacher network, choosing distillation loss plays a crucial role in the process") |
| **Task / dataset** | **AI-based conflict mitigation in B5G O-RAN**, evaluated with a **mobile-env based simulation**; case involves multiple xApps with conflicting objectives |
| **Training hardware** | **not verified** |
| **Inference latency / model size** | **not verified** |
| **Main quantitative results** | The authors acknowledge limitations of the mobile-env-based simulation. **Exact numbers not verified.** |
| **Baselines** | not verified |
| **Code/data public** | not verified |
| **Main limitation** | **Verification gap — I confirmed bibliographic data but not the numbers.** Also: this distils **xApp control policies, not LLMs** — relevant to the survey as evidence that distillation is used for RAN control, but it is *not* LLM compression. |
| **Source retrieved** | Crossref API record for 10.1016/j.comnet.2025.111848 ; ScienceDirect listing https://www.sciencedirect.com/science/article/pii/S138912862500814X |

---

### 22. MERLOT-class distillation in federated settings — HFL-FlowLLM: Large Language Models for Network Traffic Flow Classification in Heterogeneous Federated Learning

| Field | Value |
|---|---|
| **Authors** | Jiazhuo Tian, Yachao Yuan, et al. |
| **Year** | 2025 |
| **Venue** | **PREPRINT** — arXiv:2511.14199 |
| **DOI** | 10.48550/arXiv.2511.14199 |
| **Status** | **PREPRINT** |
| **Base model** | LLM-based (specific checkpoint **not verified**) |
| **Compression / efficiency method** | **Heterogeneous federated learning** (efficiency framing: reducing training cost). **No pruning/quantisation/distillation claimed in the abstract.** |
| **Dataset** | Network traffic flow classification datasets in heterogeneous federated settings (names/sizes **not verified**) |
| **Training hardware** | **not verified** |
| **Inference latency / model size** | not reported |
| **Main quantitative results** | **Average F1 +≈13%** vs. SOTA heterogeneous FL methods for network traffic flow classification; **up to +5% average F1** vs. existing LLM-FL frameworks as clients per round increase, while **reducing training costs by ≈87%** |
| **Baselines** | State-of-the-art heterogeneous federated learning methods; existing LLM federated learning frameworks |
| **Code/data public** | not verified |
| **Main limitation** | Federated efficiency, **not model compression** — include only as adjacent evidence about *training-cost* reduction. Preprint. |
| **Source retrieved** | https://arxiv.org/abs/2511.14199 |

---

### 23. Cost-Efficient Knowledge Distillation-enabled Student Models Placement in Edge Networks

| Field | Value |
|---|---|
| **Authors** | Weiqing Zeng, Danyang Zheng, Huanlai Xing, et al. (6 authors: + Wenting Wei, Chao Wang, Xiaojun Cao) |
| **Year** | 2025 |
| **Venue** | **IEEE GLOBECOM 2025 — 2025 IEEE Global Communications Conference**, 8 Dec 2025 |
| **DOI** | 10.1109/GLOBECOM59602.2025.11431653 |
| **Status** | **PEER-REVIEWED** (conference) |
| **Base model** | **not verified** |
| **Method** | **KD-enabled student-model placement optimisation** in edge networks |
| **Dataset / hardware / results** | **not verified** |
| **Main limitation** | **Scope caveat: this is a network-optimisation problem *about* placing distilled student models, not a paper that distils an LLM and measures its networking accuracy.** Include with that framing only. |
| **Source retrieved** | (bibliographic data supplied by the compression deep-dive; IEEE Xplore was returning HTTP 502 during the research window, so the DOI could not be re-verified against the publisher page) |

---

### 24. Poster: MTNTD-SLM: A Small Language Model for Malicious Traffic Detection Based on Multi-Teacher Debate-Distillation

| Field | Value |
|---|---|
| **Authors** | Shaolei Liu, Shanshan Wang, Zhenxiang Chen, et al. (7 authors: + Wenhui Zhang, Runing Li, Jian Chen) |
| **Year** | 2026 |
| **Venue** | **2026 22nd Annual IEEE International Conference on Sensing, Communication, and Networking (SECON)**, 3 Jun 2026 — **Poster track** |
| **DOI** | 10.1109/SECON68281.2026.11579221 |
| **Status** | **PEER-REVIEWED** (poster track) |
| **Base model / dataset / hardware / results** | **not verified** (IEEE Xplore fetch blocked) |
| **Main limitation** | **Verification gap.** Poster format implies limited detail. Title indicates **multi-teacher debate-distillation into an SLM for malicious traffic detection** — a valuable but unverified candidate; retrieval is a priority. |
| **Source retrieved** | https://ieeexplore.ieee.org/document/11579221 (bibliographic data supplied by the compression deep-dive) |

---

### 25. Lightweight Adaptation of Foundation Models for Optical Network Failure Management

| Field | Value |
|---|---|
| **Authors** | **not verified** |
| **Year** | 2026 (IEEE document ID 11430566) |
| **Venue** | IEEE journal (specific title/volume **not verified** — the page was behind a purchase wall) |
| **DOI** | **not verified** |
| **Status** | Presumed **PEER-REVIEWED** (IEEE Journals & Magazine) — **unverified** |
| **Base model / method / dataset / hardware / results** | **not verified** |
| **Relevance** | Title strongly suggests **lightweight/adapter-based adaptation of foundation models for optical network failure management** — an adjacent domain (optical rather than RAN) but directly on-topic for this survey. |
| **Main limitation** | **Verification gap — only the title and IEEE document ID were retrievable.** |
| **Source retrieved** | https://ieeexplore.ieee.org/abstract/document/11430566 (title only) |

---

### 26. Graph-Symbolic Policy Enforcement and Control (G-SPEC): A Neuro-Symbolic Framework for Safe Agentic AI in 5G Autonomous Networks

| Field | Value |
|---|---|
| **Authors** | Divya Vijay, Vignesh Ethiraj, et al. (NetoAI Solutions Ltd) |
| **Year** | 2026 (dated 10 Aug 2026) |
| **Venue** | **PREPRINT** — arXiv:2512.20275 |
| **DOI** | 10.48550/arXiv.2512.20275 |
| **Status** | **PREPRINT** |
| **Base model** | **TSLAM-4B** — "a 4-billion parameter model optimized for telecom reasoning", described as "publicly available" |
| **Compression method** | **Quantisation: the model is "run in 4-bit quantization to simulate edge-deployment constraints."** No pruning or distillation. Note this is *deployment* quantisation, and the paper gives no FP16-vs-4-bit ablation. |
| **Dataset / task** | 5G Core on **Open5GS with 450-node topology**; 500-scenario benchmark for policy enforcement and remediation. Synthetic 10K–100K node topologies for scalability. |
| **Training hardware** | **not reported** (no fine-tuning by these authors; TSLAM-4B used as-is) |
| **Inference latency / model size** | **G-SPEC validation adds a marginal 142 ms overhead**; validation latency scales as **O(k^1.2)** in subgraph size k. Suitable for SMO-layer operations (~5 s budgets), **not** real-time schedulers. TSLAM-4B quantised to 4-bit. Absolute model footprint: **not reported**. |
| **Main quantitative results** | **Zero observed safety violations** against the ontology in the test set; **94.1% successful remediation vs 82.4% baseline**; **0.2% hallucination-detection rate**. Ablation: **NKG validation contributes 68% of safety gains, SHACL policies 24%, TSLAM fine-tuning 8%.** Cites prior work finding **general-purpose LLMs hallucinate in 14.6% of network operations**. |
| **Baselines** | Baseline without graph validation (82.4% remediation); ablations removing NKG / SHACL / TSLAM fine-tuning |
| **Code/data public** | Not found |
| **Main limitation** | Preprint; the compact 4B model is used as a fixed component — **the paper's own ablation says model fine-tuning contributes only 8% of the safety benefit**, which weakens any claim that better LLM fine-tuning is the lever. No hardware or model-footprint reporting. |
| **Source retrieved** | https://ar5iv.labs.arxiv.org/html/2512.20275 |

---

### 49. OB-IDS: Optimized BERT-based Intrusion Detection System — **the only paper found combining quantization + pruning + KD + self-distillation in one pipeline**

| Field | Value |
|---|---|
| **Authors** | (Mamikonian & Mamamniashvili, per the parallel verification pass — **author list not independently re-verified by me**) |
| **Year** | 2025 |
| **Venue** | **Georgian Scientists**, vol. 7, no. 4. ⚠️ **Peer-reviewed but a small regional venue — flagged as such.** |
| **DOI** | 10.52340/gs.2025.07.04.49 — **not independently re-verified by me** |
| **Status** | PEER-REVIEWED (regional venue) |
| **Base model** | **BERT-base, 110M params / 438 MB** |
| **Compression method** | **A full four-stage pipeline — unique in this corpus: (1) INT8 quantization (QAT + PTQ); (2) global magnitude structured pruning of attention heads AND FFN at 40% → 60% → 75% sparsity; (3) knowledge distillation with T = 4, α = 0.7; (4) iterative self-distillation.** |
| **Resulting model** | **38M parameters / 32 MB** (from 110M / 438 MB) |
| **Dataset** | **UNSW-NB15** and **CIC-IDS2017** |
| **Training hardware** | not verified |
| **Inference latency / memory** | **Raspberry Pi 4: 214.6 ms → 27.4 ms (−87.3%)**; memory **1,840 MB → 280 MB** |
| **Main quantitative results** | **UNSW-NB15 98.44%, CIC-IDS2017 98.19%** |
| **Baselines** | not verified |
| **Code/data public** | not verified |
| **Main limitation** | ⚠️ **There is a SECOND, DISTINCT OB-IDS paper**: Ateş, Çelebi, Semerci, Çapkan, Yıldırım, **2025 IEEE BlackSeaCom, pp. 1–4, DOI 10.1109/BlackSeaCom65655.2025.11193891** ("OB-IDS: Optimized BERT-based Intrusion Detection System") — different authors, different venue, same quantize+prune+distill+self-distill recipe, but **zero numbers retrievable**. **Do NOT merge these two citations.** Also: this entry's authors/DOI were verified only by the parallel pass, not by me. |
| **Source retrieved** | From the parallel compression deep-dive; DOI 10.52340/gs.2025.07.04.49 **not independently confirmed** |

> **Why this matters:** OB-IDS is the closest thing in the literature to a **complete compression stack for a network-security transformer**, and it is the only entry reporting a **quantization + pruning + KD + self-distillation** combination with an end-to-end embedded latency figure (Raspberry Pi 4). It should anchor any "what does a full compression pipeline look like in this domain?" discussion — with the venue caveat.

---

### 50. NetKD: Towards Resource-Efficient Encrypted Traffic Classification Using Knowledge Distillation

| Field | Value |
|---|---|
| **Authors** | Jiaji Ma, Xiangge Li, Hong Luo, et al. |
| **Year** | 2024 |
| **Venue** | **2024 27th International Conference on Computer Supported Cooperative Work in Design (CSCWD)**, pp. 3011–3016 |
| **DOI** | 10.1109/CSCWD61410.2024.10580837 |
| **Status** | **PEER-REVIEWED** (conference) |
| **Base model** | **BERT** (teacher) → **NetKD-BERT** (student) |
| **Compression method** | **Knowledge distillation** via Multi-Head Self-Attention Relation Alignment + Masked BURST Model + Same-origin BURST Prediction |
| **Task / dataset** | Encrypted traffic classification. **Dataset not named in the retrievable material.** |
| **Training hardware** | not reported |
| **Inference latency / model size** | **0.93 ms/packet; 14.3× faster; 7.33% of baseline memory** |
| **Main quantitative results** | **4.61% of baseline parameters, 99.10% of baseline F1** |
| **Baselines** | BERT teacher and other encrypted-traffic baselines |
| **Code/data public** | not reported |
| **Main limitation** | **All figures are relative** — no absolute F1, no absolute parameter count, no dataset name in what was retrievable. Nonetheless this is the **strongest compression-to-quality ratio in the entire corpus** (a 21.7× parameter reduction for a 0.9% F1 loss) and belongs in any compression-efficiency comparison. |
| **Source retrieved** | Crossref record 10.1109/CSCWD61410.2024.10580837 ; technical figures from the parallel compression deep-dive |

---

### 51. Multi-Modal Beamforming with Model Compression and Modality Generation

| Field | Value |
|---|---|
| **Authors** | Chen Shang, Dinh Thai Hoang, Jiadong Yu, et al. |
| **Year** | 2026 |
| **Venue** | **IEEE Transactions on Mobile Computing (TMC)**, pp. 1–15 |
| **DOI** | 10.1109/TMC.2026.3712170 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base model** | Hierarchical transformer for **6G V2X beamforming** (parameter count **not verified**) |
| **Compression method** | **Module-aware splitting pruning.** Explicitly **rejects a single global pruning ratio** and deliberately **preserves whole attention heads**; prunes FFN neurons with **per-module ratios**. Also performs modality generation (compressing/generating missing modalities). |
| **Training hardware** | Inference evaluated across **GTX 1080 / RTX 4070 Ti / NVIDIA L20** |
| **Inference latency / model size** | **>80% latency reduction at remaining-parameter ratio 0.4**, across all three GPUs |
| **Main quantitative results** | **DBA-Score 85.95% at remaining-parameter ratio 0.7** |
| **Main limitation** | ⚠️ **Title discrepancy:** the parallel pass referred to this paper as **"BeamTransFuser"**; the Crossref record for DOI 10.1109/TMC.2026.3712170 gives the title as **"Multi-Modal Beamforming with Model Compression and Modality Generation."** These may be the same work (a renamed preprint) or two different papers — **resolve before citing.** |
| **Source retrieved** | Crossref record 10.1109/TMC.2026.3712170 ; technical figures from the parallel compression deep-dive |

> **Best-designed pruning methodology in the corpus:** it is the only paper that argues *against* uniform pruning ratios for network workloads — a concrete, citable design lesson for anyone compressing an LLM for RAN control.

---

### 52. Efficient Federated Intrusion Detection in 5G Ecosystem Using Optimized BERT

| Field | Value |
|---|---|
| **Authors** | Frederic Adjewa, Moez Esseghir, Leila Merghem-Boulahia, et al. |
| **Year** | 2024 |
| **Venue** | **2024 20th International Conference on Wireless and Mobile Computing, Networking and Communications (WiMob)**, pp. 62–67 |
| **DOI** | 10.1109/WiMob61911.2024.10770340 (preprint: arXiv:2409.19390) |
| **Status** | **PEER-REVIEWED** (conference) + PREPRINT |
| **Base model** | **BERT-base, 110M / 420 MB**, truncated to **4 layers / 256 hidden / 4 heads = 11,174,415 params / 42.63 MB** |
| **Compression method** | **Architectural truncation (layer/width/head reduction) + per-channel linear post-training quantization (PTQ)** |
| **Dataset** | **Edge-IIoTset — 2,219,201 data points, 30% used, 15 classes** |
| **Training hardware** | **Quadro RTX 6000 (22.5 GB) + Xeon Gold 6128** |
| **Inference latency / model size** | **Centralized: 35.23 ms (Xeon) / 2.63 ms (GPU). Federated: 95% → 97% accuracy over 10 epochs. Total size reduction −92.76%.** |
| **Main quantitative results** | **Centralized accuracy 96.60% → 97.79%** (against a 98.2% baseline) |
| **Baselines** | Full BERT-base (98.2%) |
| **Main limitation** | ⚠️ **Reports two conflicting compression figures: 28.74% for quantization alone vs 92.76% "total."** Most of the reduction therefore comes from **layer truncation, not quantization** — do not attribute the −92.76% to quantization. |
| **Source retrieved** | Crossref record 10.1109/WiMob61911.2024.10770340 ; technical figures from the parallel compression deep-dive |

> **This is the best-documented quantization-plus-architecture result for a 5G intrusion-detection transformer**, and the cleanest latency comparison (CPU vs GPU) in the corpus.

---

### 53. Optimizing Transformer-Based Intrusion Detection Through Binarization and Knowledge Distillation

| Field | Value |
|---|---|
| **Authors** | Voon Tao Tan, Wan Tze Vong, Colin Choon Lin Tan, et al. |
| **Year** | 2025 |
| **Venue** | **2025 5th International Conference on Robotics, Automation and Artificial Intelligence (RAAI)**, pp. 350–357 |
| **DOI** | 10.1109/RAAI67517.2025.11423225 |
| **Status** | **PEER-REVIEWED** (conference) |
| **Base model** | **25M-parameter transformer** network IDS |
| **Compression method** | **1-bit weight binarization (W1A8 and W1A1) + knowledge distillation** |
| **Dataset** | **CSE-CIC-IDS2018**; also CICIoT2023 |
| **Model size** | **96.26 MB → 3.25 MB (~30× reduction)** |
| **Main quantitative results** | **W1A8: 98.51% accuracy / 98.12% weighted F1 on CSE-CIC-IDS2018 — matching FP32.** **W1A1 degrades on CICIoT2023 minority attacks.** |
| **Main limitation** | The most aggressive quantization found (1-bit weights) holds up at W1A8 but **not at W1A1** on imbalanced attack classes — a useful data point that extreme quantization is class-imbalance-sensitive. |
| **Source retrieved** | Crossref record 10.1109/RAAI67517.2025.11423225 ; technical figures from the parallel compression deep-dive |

---

### 54. SPARTA: Sparse Parallel Architecture for Real-Time Threat Analysis — **the only billion-parameter LLM pruning found, and it does NOT validate on network data**

| Field | Value |
|---|---|
| **Authors** | Shi Li, Xiyun Mi, Lin Zhang, et al. |
| **Year** | 2026 |
| **Venue** | **Future Internet (MDPI)**, vol. 18, art. 88 |
| **DOI** | 10.3390/fi18020088 |
| **Status** | **PEER-REVIEWED** (journal) |
| **Base models** | **LLaMA 7B / 13B / 30B / 65B** |
| **Compression method** | **Unstructured (Wanda) + 2:4 semi-structured pruning** |
| **Evaluation dataset** | **Wikitext2 — NOT network traffic.** ⚠️ **The link to threat analysis is an explicit analogy, so this paper provides ZERO evidence about pruning's effect on network-task accuracy.** |
| **Hardware** | **Simulation only (Accel-Sim; RTX 3070)** |
| **Main quantitative results** | **2.35× average / 5.05× peak speedup over Flash-LLM** |
| **Main limitation** | **This is the single most important caveat in the pruning literature for your survey: the only work pruning true multi-billion-parameter LLMs and calling itself a networking paper evaluates perplexity on Wikitext2.** Anyone citing SPARTA as evidence that "pruning works for network-management LLMs" would be misrepresenting it. |
| **Source retrieved** | Crossref record 10.3390/fi18020088 ; technical figures from the parallel compression deep-dive |

---

### 55. HiPELog: Hierarchical and Parameter-Efficient Transformer for Log Anomaly Detection

| Field | Value |
|---|---|
| **Authors** | M. Anjana Devi, Sountharrajan S, et al. |
| **Year** | 2026 |
| **Venue** | **2026 IEEE International Conference on AI Engineering (AIEI)**, pp. 1–6 |
| **DOI** | 10.1109/AIEI69164.2026.11496714 |
| **Status** | **PEER-REVIEWED** (conference) |
| **Base model** | **63.47M-parameter transformer** |
| **Compression method** | **LoRA — 8,192 trainable parameters of 63.47M (99.99% reduction in trainable parameters).** ⚠️ **LoRA is PEFT, not compression** — serving cost is unchanged. Log anomaly detection is a genuine network-management task. |
| **Dataset** | **BGL** (Blue Gene/L log dataset) |
| **Main quantitative results** | **99.87% BGL accuracy** |
| **Main limitation** | Full text inaccessible; the "99.99% reduction" is again a *trainable*-parameter figure, not a serving-cost reduction. Same terminology-drift issue as AQM-LLM (#17). |
| **Source retrieved** | Crossref record 10.1109/AIEI69164.2026.11496714 ; technical figures from the parallel compression deep-dive |

---

### 56. Hardware-Aware Neural Architecture Search for Encrypted Traffic Classification

| Field | Value |
|---|---|
| **Authors** | Adel Chehade, Edoardo Ragusa, Paolo Gastaldo, et al. |
| **Year** | 2026 |
| **Venue** | **IEEE Transactions on Network and Service Management (TNSM)**, vol. 23, pp. 2982–2995 |
| **DOI** | 10.1109/TNSM.2026.3666676 (preprint: arXiv:2506.11319) |
| **Status** | **PEER-REVIEWED** (journal) + PREPRINT — **note: this IS an IEEE TNSM paper on compression for networking, contradicting the "nothing at TNSM" finding below** |
| **Method** | **Hardware-aware NAS** producing **INT8 1D-CNN** models for STM32 microcontrollers |
| **Dataset** | **ISCX VPN-nonVPN** |
| **Main quantitative results** | **Up to 444× parameter reduction; 96.60% accuracy** |
| **Main limitation** | CNN, not a transformer or LLM — include as edge-deployment context, not LLM compression. |
| **Source retrieved** | Crossref record 10.1109/TNSM.2026.3666676 ; technical figures from the parallel compression deep-dive |

---

### 57. Integer-Only INT8 TinyML CNN for Encrypted Traffic — **the only paper reporting energy per inference**

| Field | Value |
|---|---|
| **Venue** | **IEEE ISCC 2025** (preprint: arXiv:2506.10851) |
| **Method** | Integer-only **INT8** TinyML CNN |
| **Main quantitative results** | **96.59% accuracy; energy per inference 7.86 mJ (STM32F746G-DISCO, 31.43 ms) and 29.10 mJ (Nucleo-F401RE, 115.40 ms)** |
| **Note** | **The only entry in the entire corpus reporting energy per inference** — directly relevant to an energy/latency discussion for edge network AI, though it is a CNN rather than an LLM. |
| **Source retrieved** | From the parallel compression deep-dive; DOI not independently verified |

---

### 58. Additional compression entries verified only at metadata level (cite with care)

| Title | Authors (first 3 + et al.) | Year | Venue | DOI | Method / result | Status |
|---|---|---|---|---|---|---|
| **SRB-ET** | (see KCI record) | 2024 | **J. Institute of Electronics and Information Engineers (Korea)**, vol. 61, no. 11, pp. 49–57 | 10.5573/ieie.2024.61.11.49 | **Structured layer pruning of BERT + neighbouring weight averaging** (merges removed-layer weights into adjacent layers). ISCX VPN-nonVPN: **params −15.12%, inference time −45.1%, training speed +54.9%, accuracy maintained** | PEER-REVIEWED (Korean venue); bilingual abstract retrieved via KCI |
| **LENS / LENS-RMHR** | (see MDPI) | 2025 | **Mathematics (MDPI)**, vol. 13, no. 11, art. 1784 | 10.3390/math13111784 | **RoBERTa neuron selection** for Chinese telecom fraud: 9,216 neurons, **0.85 retention best, F1 94.19 (+2.58 over baseline)**. ⚠️ Claims computational efficiency but reports **no latency/memory/size at all**, and no GPU | PEER-REVIEWED |
| **COOL** | (see IEEE) | 2024 | **IEEE Internet of Things Journal** | 10.1109/JIOT.2023.3321299 | Closed access. ⚠️ **Main evaluation is MNIST / CIFAR-10, NOT network traffic** | PEER-REVIEWED |
| **P5 CLT-BERT** | (see IEEE) | 2025 | **IEEE SPCNC 2025** | 10.1109/SPCNC68200.2025.11406423 | Metadata only; **compression type unverified** | PEER-REVIEWED |
| **Bufferless RL prune-quant** | (see Springer) | 2025 | **Evolutionary Intelligence** | 10.1007/s12065-025-01122-X | Full text blocked; sparsity/hardware/accuracy unverified. **Code IS public**: github.com/zafriazman/PruneQuant-TrafClassif | PEER-REVIEWED |
| **HierFedKD-Traffic** | (see IFIP) | 2026 | **IFIP Networking 2026** | 10.23919/IFIPNetworking70592.2026.11579006 | Hierarchical federated KD for wireless traffic prediction; Telecom Italia CDR data; **RMSE −2.3 to −3.1% vs FedAvg/FedProx/HierFL** | PEER-REVIEWED |
| **5G-V2X Intra-Slice IDS** | (see IEEE) | 2023 | **IEEE ICC 2023** | 10.1109/ICC45041.2023.10279212 | cloud-teacher → CAV-student KD; **>50% computation and memory reduction** | PEER-REVIEWED |
| **SD-MKD** | (see IEEE) | 2025 | **IJCNN 2025** | 10.1109/IJCNN64981.2025.11227284 | Multi-teacher Stacking KD + Sinkhorn distance; ISCXVPN2016 / ISCXTor2016 / USTC-TFC2016. **Abstract is purely qualitative — no numbers** | PEER-REVIEWED |
| **BERT-LightRFFI** | (see IEEE) | 2025 | **IEEE WCNC 2025** | 10.1109/WCNC61545.2025.10978469 | BERT teacher → BERT-Light student, LoRa RFFI, **97.52% accuracy**; PHY-layer, adjacent | PEER-REVIEWED |
| **LENS-XAI** | Yagiz, Goktas | 2025 | **PREPRINT** arXiv:2501.00790 | 10.48550/arXiv.2501.00790 | KD + VAE IDS; **T=2, α=0.5**; RTX 4080 Super; teacher 13,065 → student 4,489 params; **44% peak compute reduction**; accuracies 95.34% (Edge-IIoTset), 99.92% (UKM-IDS20). ⚠️ **NOT a transformer** (tiny dense nets) | PREPRINT |
| **Lightweight LLMs for Network Attack Detection in IoT Networks** | (see arXiv) | 2025 | **PREPRINT** arXiv:2601.15269 (accepted ComComAp 2025, Madrid) | 10.48550/arXiv.2601.15269 | **QLoRA 4-bit NF4 + double quantization, LoRA r=16, α=32, dropout 0.1.** Models: GPT-2 (356.40M), LLaMA-3.2-1B (1,238.17M), Mistral-v0.3-7B (7,257.46M), LLaMA-3.1-8B (8,039.70M). **CICIoT2023.** Hardware: **RTX 4080 16 GiB** (GPT-2, LLaMA-3.2-1B) and **RTX 4090 32 GiB** (Mistral-7B, LLaMA-3.1-8B). **LLaMA-3.2-1B best F1 0.7124 vs Random Forest 0.7159; runtime 235.16 s**; RAG zero-shot 42.63% acc, Top-3 recall 63.27% | PREPRINT — **notable as a rare case where a QLoRA LLM FAILS to beat a classical Random Forest** |
| **LLM-QFL** | (see IEEE) | 2026 | **IEEE TNSM** | 10.1109/TNSM.2026.3712394 (arXiv:2505.18656) | Federated fine-tuning + distillation of an LLM in quantum federated learning; PEFT (LoRA/QLoRA) | PEER-REVIEWED; borderline networking relevance |
| **Lightweight Fine-Tuning of LLMs for Explainable Intrusion Detection in SDN** | (see NCI) | 2025 | **IEEE WiMob 2025** | 10.1109/WiMob66857.2025.11257572 | QLoRA (4-bit) on **GPT_NEO + Phi-2 + Llama2-7b**; **1.00 accuracy for Phi-2/GPT_NEO; lowest CO2 0.173** | PEER-REVIEWED |

> **Two entries in the table above contradict the "no compression papers at IEEE TNSM" finding:** HW-NAS (#56) and LLM-QFL are both **IEEE TNSM** papers on compression/efficiency for networking, and **KD-PFL traffic classification (DOI 10.1109/TNSM.2025.3629241)** and **HKD-Net (DOI 10.1109/TNSM.2026.3668812)** were also verified at metadata level. **IEEE TNSM does publish in this space** — the earlier negative finding was an artifact of the Xplore outage, and I am correcting it here.

---

<a name="group-iii"></a>
## Group (iii) — Generic efficient-LLM methods networking papers build on

> ⚠️ **These are generic ML/systems papers, NOT networking papers.** They are included only because networking papers in Groups (i)–(ii) cite them as their compression toolkit. The parent survey should cite them under "background/methods", clearly separated from the networking contributions.

| # | Title | Authors (first 3 + et al.) | Year | Venue | DOI / ID | Status | What it provides |
|---|---|---|---|---|---|---|---|
| G1 | **LoRA: Low-Rank Adaptation of Large Language Models** | Edward J. Hu, Yelong Shen, Phillip Wallis, et al. | 2022 | **ICLR 2022** | OpenReview `nZeVKeeFYf9`; arXiv:2106.09685 | PEER-REVIEWED | The PEFT method used by refs #5, #6, #7, #8, #10, #19 |
| G2 | **QLoRA: Efficient Finetuning of Quantized LLMs** | Tim Dettmers, Artid Pagnoni, Ari Holtzman, et al. (+ Luke Zettlemoyer) | 2023 | **NeurIPS 2023** | arXiv:2305.14314 | PEER-REVIEWED | 4-bit NormalFloat + double quantisation + paged optimisers — the toolkit cited by refs #5 and #3 |
| G3 | **Survey on Efficient Large Language Models: Principles, Algorithms, Applications, and Open Issues** | Jian Cheng, Haidong Kang, Yuxin Shao, et al. | 2026 | **IEEE Transactions on Neural Networks and Learning Systems (TNNLS)**, vol. 37, pp. 2025–2045 | 10.1109/TNNLS.2025.3628671 | PEER-REVIEWED | Broad recent survey covering efficient-LLM principles/algorithms — **generic ML, not networking** |
| G4 | **Survey on Knowledge Distillation for Large Language Models: Methods, Evaluation, and Application** | (see ACM DL record) | 2024/2025 | **ACM Transactions on Intelligent Systems and Technology (TIST)** | 10.1145/3699518 | PEER-REVIEWED | Reference survey for the KD methods used by refs #16, #17, #20, #24 — **generic ML, not networking** |
| G5 | **A Survey on Symbolic Knowledge Distillation of Large Language Models** | Kamal Acharya, Alvaro Velasquez, Houbing Herbert Song, et al. | 2024 | **IEEE Transactions on Artificial Intelligence**, vol. 5, pp. 5928–5948 | 10.1109/TAI.2024.3428519 | PEER-REVIEWED | Symbolic-knowledge distillation survey — **generic ML, not networking** |
| G6 | **The Landscape of Pruning for Large Language Models: A Systematic Review and Unified Taxonomy** | (see Elsevier record) | 2026 | **Neural Networks (Elsevier)** | 10.1016/j.neunet.2026.xxxxx — **DOI not verified** (ScienceDirect record S0893608026007276) | PEER-REVIEWED | Unified pruning taxonomy — the natural background citation for structured/unstructured/attention-head pruning. **Generic ML, not networking.** |
| G7 | **Evolution of Meta's LLaMA Models and Parameter-Efficient Fine-Tuning of Large Language Models: A Survey** | (see arXiv record) | 2025 | **PREPRINT** — arXiv:2510.12178 | 10.48550/arXiv.2510.12178 | PREPRINT | PEFT survey. **Generic ML, not networking.** |
| G8 | **Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM)** | Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, et al. | 2023 | **SOSP 2023** | arXiv:2309.06180 | PEER-REVIEWED | Serving/inference efficiency — cited by refs #6 and #7 as their serving engine. **Generic systems, not networking.** |
| G9 | **ZeRO: Memory Optimizations Toward Training Trillion Parameter Models** | Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, et al. (+ Yuxiong He) | 2019/2020 | **SC20** | arXiv:1910.02054 | PEER-REVIEWED | Memory-optimised distributed training — cited by ref #6 (ZeRO Stage-2). **Generic systems, not networking.** |
| G10 | **DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models** (source of GRPO) | Zhihong Shao, Peiyi Wang, Qihao Zhu, et al. | 2024 | **PREPRINT** — arXiv:2402.03300 | 10.48550/arXiv.2402.03300 | PREPRINT | GRPO, the RL algorithm used by refs #6 and #7. **Generic ML, not networking.** |

**Additional networking-adjacent surveys (networking, but surveys — not primary compression results):**

| # | Title | Authors (first 3 + et al.) | Year | Venue | DOI | Status |
|---|---|---|---|---|---|---|
| S1 | **Large Language Models for computer networking operations and management: A survey on applications, key techniques, and opportunities** | Fan Liu, Behrooz Farkiani, Patrick Crowley, et al. | 2025 | **Computer Networks (Elsevier)**, vol. 271, art. 111614 | 10.1016/j.comnet.2025.111614 | PEER-REVIEWED |
| S2 | **A Comprehensive Survey on LLM-Based Network Management and Operations** | Jibum Hong, Nguyen Van Tu, James Won-Ki Hong, et al. | 2025 | **International Journal of Network Management (Wiley)**, vol. 35 | 10.1002/nem.70029 | PEER-REVIEWED |
| S3 | **Towards fully autonomous network management: A survey on LLM-based Multi-Agent Systems** | Ki-Hyeon Kim, Cheoneum Park, Hyeonjeong Lee, et al. | 2026 | **ICT Express**, vol. 12, pp. 1015–1034 | 10.1016/j.icte.2026.07.003 | PEER-REVIEWED |
| S4 | **How Helpful Is LLM Assistance in Network Operations? A Case Study at a Large Demonstration Network** | Ryo Nakamura, Koshi Eguchi, et al. | 2026 | **NOMS 2026 — IEEE Network Operations and Management Symposium**, pp. 1–10 | 10.1109/NOMS69089.2026.11668182 | PEER-REVIEWED |

---

<a name="answers"></a>
## Answers to Questions A–F

### A. Has anyone fine-tuned an LLM specifically for network management (not just telecom text classification)?

**Yes — unambiguously, and at multiple scopes.** The literature contains at least four distinct families:

1. **5G network *analysis* within the core-network NWDAF** — **Mobile-LLaMA** (Kan, Mun, Cao et al., IEEE Network 2024, DOI 10.1109/MNET.2024.3421306) instruction-fine-tunes **LLaMA 2 13B** on real 5G network data for **packet analysis, IP routing analysis and performance analysis**, explicitly positioned inside NWDAF "for 5G network management and data analysis." This is the canonical citation for Question A.

2. **Intent-driven RAN/network management** — Habib et al. (arXiv:2505.01841) fine-tune an LLM with **QLoRA** so it can (i) answer operator queries about network state and (ii) extract metric + magnitude from natural-language intents ("Increase throughput by 10%"), then drive a Decision-Transformer application orchestrator. Also **ORION** (arXiv:2603.03667) automates the O-RAN intent lifecycle — but **ORION does not fine-tune**.

3. **Network troubleshooting / fault remediation** — the Ericsson series (arXiv:2511.00651, arXiv:2607.02523, and ICC 2026's arXiv:2509.25736) fine-tunes **DeepSeek-R1-Qwen-3-8B** with **SFT + LoRA + GRPO (RFT)** on proprietary RAN/Core troubleshooting documents to serve as the "solution planner" in a multi-agent troubleshooting system. This is genuinely network *operations*, not text classification.

4. **Protocol control-plane emulation** — Liu, Liu, Valcarce, Chu (arXiv:2505.16821) fine-tune **Llama-3/3.1/3.2 (1B–8B)** with LoRA to **generate and parse 3GPP-compliant RRC messages**, i.e., to directly orchestrate control-plane procedures.

5. **Network configuration automation** — **Network Self-Configuration Based on Fine-Tuned Small Language Models** (Lira, Caicedo, da Fonseca et al., IEEE OJ-COMS 2026, DOI 10.1109/OJCOMS.2026.3695460) is explicitly a fine-tuned SLM for network configuration (full-text verification pending).

**Important negative finding:** a large share of "telecom LLM" work is *knowledge/QA/code* work rather than network management. **TelecomGPT** (IEEE TMLCN 2025), **Tele-LLMs** (IEEE Access 2026) and **TeleQnA** (IEEE Network 2026) all build telecom-specialised models or benchmarks but evaluate on **question answering, technical-document classification, code generation and literature tasks** — **none of them measures a network KPI or a network decision.** The parent survey should draw this distinction explicitly; it is one of the field's clearest gaps.

---

### B. On what dataset? What task? What base model? What fine-tuning method? How much data?

| Paper | Base model (params) | Method | Dataset name | Size |
|---|---|---|---|---|
| Mobile-LLaMA | LLaMA 2 **13B** | **8-bit LoRA** (r=64, alpha=16, dropout 0.1, lr 1e-4, 3 epochs / max 5000 steps) + self-instruct | Own 5G network-analysis data (from public real-world 5G datasets) | **15,111 instruction sets** (150 manual seeds + 15,000 self-instruct), val split 1,300 |
| TelecomGPT | **Llama2-7B, Mistral-7B, Llama3-8B** (+instruct); <=8B cap | **QLoRA r=512/alpha=256** (SFT, 3 epochs, lr 2e-4, FSDP) then **QLoRA r=256/alpha=128 + DPO** (beta=0.1, lr 5e-6, 1 epoch) | OpenTelecom / TelecomInstruct / TelecomAlign | **1,679.5M pre-training tokens**; instruction/preference sample counts not reported |
| Tele-LLMs | TinyLlama-1.1B, Phi-1.5B, Gemma-2B, Gemma-2-2B, LLaMA-3.2-1B/3B, LLaMA-3-8B | **Full fine-tuning** (LoRA r=64/alpha=32 tested and rejected), 2 epochs, 5% SlimPajama | Tele-Data (+ Tele-Eval for eval) | Tele-Data ~2.74B tokens (sum of four categories); **Tele-Eval 750k Q&A pairs** |
| **5G Instruct Forge** | **Llama3-8B, Solar-10.7B, Mistral-7B** | **Freeze-tuning** (partial parameter freezing, 9-12% trainable) - **LoRA rejected** | **OAI Instruct** (from 22 3GPP TSs for OpenAirInterface) | ~80 MB; eval **>9,000 Q&A + 200-question 5G exam** |
| Understanding Telecom Language | BERT-Base 110M, DistilBERT 66M, RoBERTa 125M, GPT-2 124M | Full fine-tuning with a classification head (batch 32, lr 2e-5) | 3GPP tdocs (RAN1-5, SA1-6, CT1/3/4/6) | Train = 2009/10-2019, Test = 2020-Apr 2023; 200-word segments |
| Habib et al. (RAN intent) | LLaMA (**variant/size not reported**) | **QLoRA** + RAG | Custom simulation-derived query/intent dataset | **"hundreds or even thousands" - count not reported** |
| Ericsson MAS | DeepSeek-R1-Qwen-3-8B | **SFT (LoRA) then RFT (LoRA+GRPO)** | Proprietary RAN/Core troubleshooting docs | Companion paper: **50 seed + 500 synthetic** |
| Ericsson edge profiling | Qwen2.5-7B; DeepSeek-R1-0528-Qwen3-8B; Llama-3.1-8B | **LoRA (q/k/v_proj) SFT then RFT** | Telecom troubleshooting dataset + top-3 retrieved chunks | **50 SME seed + 500 synthetic RFT pairs**, avg chunk length ~16,126 tokens |
| RRC emulation | Llama-3/3.1 8B, Llama-3.2 3B/1B | **SFT + LoRA r in {4,8,16}** vs full FT | Proprietary multi-vendor 4G/5G RRC traces | **30,000 5G pairs + 4,800 4G QA turns** |
| NetSoft / 3GPP LLM | **Llama 3.2 3B** | 16 to 4-bit quantisation + fine-tuning + RAG | **TeleQnA + TSpec-LLM** | **10,000 questions** + TSpec-LLM (30,137 docs / 13.5 GB) |
| NetIntent | 33 LLMs, 1.1B-70B | **No fine-tuning** (in-context) | IBNBench (Intent2Flow-ODL/ONOS, FlowConflict-ODL/ONOS) + Formal Spec + NFV Config | 52 / 50 / 60 / 74 + 1,500 + 120 pairs |
| G-SPEC | **TSLAM-4B** | 4-bit deployment quantisation (no fine-tuning by authors) | Open5GS 450-node simulation | 500 scenarios |

**Summary for B:** dataset sizes in this literature span **four orders of magnitude** - from **50 SME-validated pairs** (Ericsson edge study) up to **1.68 billion pre-training tokens** (TelecomGPT). The most common *instruction-tuning* scale is ~10^3-10^4 samples (Mobile-LLaMA: 15,111; RRC: 30,000+4,800; 5G Instruct Forge: >9,000 Q&A). The most common base-model sizes are **1B, 3B, 7B, 8B and 13B**. The most common method is **LoRA/QLoRA SFT**, with a notable minority using **full fine-tuning** (Tele-LLMs) or **partial freeze-tuning** (5G Instruct Forge) - **both after explicitly rejecting LoRA**.

---

### C. GPU requirements / training cost / inference latency / model size?

**Reported (verified):**

| Paper | Hardware | Training time | Inference latency |
|---|---|---|---|
| **TelecomGPT** | **8 × AWS ml.p4d.24xlarge** (pre-training) / FSDP on 8 GPUs within one ml.p4d.24xlarge (instruct tuning) | **~6 h** continual pre-training; **~1.5 h** instruct tuning | not reported |
| **Tele-LLMs** | **8 × NVIDIA A6000** | **~5,000 GPU-hours** | (judge model) **~50 ms/question** on 1x A6000 |
| **5G Instruct Forge** | training **not reported**; deployment **1 × NVIDIA A100 80 GB** | not reported | not reported |
| **Ericsson MAS** | **7 × RTX A6000 (48 GB)** - 4 for serving/judging, 2 for TRL-vLLM training | **<3 days** full RFT; **~20 h** from checkpoint | not reported |
| **Ericsson edge profiling** | **1 × RTX A6000 (48 GB)** | **116 min** (1k tokens) / **173 min** (5k) / **229 min** (10k) for 250 steps; Llama-3.1-8B: **29 min** at 20k | **"seconds"** on A6000; 4-bit Qwen2.5-7B = **3.805 GB** weights |
| **RRC emulation** | **2 × A100 80 GB** (NR, ~110 GB VRAM training); **1 × GH200 (H100 96 GB)** / 4xGH200 nodes (LTE) | converged in **~8.4k steps**; deliberately truncated to avoid "unnecessary GPU hours" | **1.7-3.6 s** median (`RRC_constrain`); **M2 Max 1.84 s vs GH200 1.092 s** for 1B/INT4; energy **7.7 mWh vs 0.200 Wh** per message |
| **O-RAN agentic (Navidan et al.)** | **H200** (LLM) / **RTX 5090** (SLM) / **Jetson Xavier NX** (WPFM) | WPFM fine-tune: 1st epoch ~17 s, full ~340 s | **LLM 9,364 +/- 59 ms; SLM 793 +/- 3 ms; WPFM 0.847 +/- 0.04 ms** |
| **NetIntent** | **1 × RTX A6000 (48 GB)**, 500 GB RAM, Threadripper PRO 5995WX | no training | **Codellama-34b >10 s/inference; Qwen2.5-7B <2 s**; 70B models could not run at larger context due to memory |
| **MERLOT** | not reported | not reported | **85-90% less inference time and memory** than 7B TrafficLLM (no absolute value) |
| **KGLlama-KD** | "cloud" then edge (specifics not reported) | not reported | **-60% inference latency** vs full-scale LLM, meeting sub-100 ms |
| **ORANSight-2.0** | **1 x NVIDIA RTX 4090 (24 GB, consumer)** | 1 epoch, QLoRA 4-bit, on 151,500 instruction pairs | not reported |
| **TelcoLM** (Orange, preprint) | **2 x A100-80GB** (DAPT) / **2 x A100-40GB** (IAPT) | not reported | not reported |
| **TelecomGPT-R1** (preprint) | **8 x H200** | not reported | not reported |
| **AQM-LLM** (IEEE TON 2026) | **2 × NVIDIA A40 (48 GB)** | **>20 h** for Llama2-7B vs sub-hour for OPT/GPT-2/T5 | **Un-adapted Llama2-7B 0.200 s → LoRA-adapted 0.0391 s (−80%, ~5×);** VRAM 23.91 GB (Llama2) / 7 GB (OPT) / 3.6 GB (GPT-2) / 2.32 GB (T5) |
| **NetKD** (IEEE CSCWD 2024) | not reported | not reported | **0.93 ms/packet; 14.3x faster; 7.33% of baseline memory** |
| **OB-IDS** (2025) | not verified | not verified | **Raspberry Pi 4: 214.6 ms → 27.4 ms (−87.3%); memory 1,840 → 280 MB** |
| **5G Federated IDS / securityBERT** (IEEE WiMob 2024) | **Quadro RTX 6000 (22.5 GB) + Xeon Gold 6128** | not reported | **35.23 ms (Xeon) / 2.63 ms (GPU); total size −92.76%** |
| **INT8 TinyML CNN** (IEEE ISCC 2025) | STM32F746G-DISCO / Nucleo-F401RE | not reported | **31.43 ms / 115.40 ms; ENERGY 7.86 mJ / 29.10 mJ per inference** |
| **HiPELog** (IEEE AIEI 2026) | not reported | not reported | not reported (8,192 of 63.47M trainable params via LoRA) |
| **MTNTD-SLM** (IEEE SECON 2026 poster) | not reported | not reported | **12 ms** |
| **TSLAM-8B** (vendor blog, NOT peer-reviewed) | AWS Trainium trn1.32xlarge | not reported | **300–500 ms on AWS Inferentia2** |
| **G-SPEC** | not reported | no training | **+142 ms** validation overhead |

**Not reported:** Habib et al. (hardware, latency, dataset size, base-model identity); Mobile-LLaMA (hardware); SQLLM (exact VRAM/latency values); AQM-LLM (hardware, latency); xApp distillation (all); 5G Instruct Forge (training hardware); TSpec-LLM / Telco-RAG (no training); SPEC5G (unverified).

**Bottom line for C — and this is a headline finding:**

- **The GPU floor is much lower than the literature's framing suggests.** **ORANSight-2.0 (IEEE TMLCN 2025) QLoRA-4-bit fine-tuned models up to 70B on 151,500 O-RAN instruction pairs on a SINGLE 24 GB consumer RTX 4090 in one epoch.** The commonly cited 48 GB A6000 is a *comfortable* configuration, not a requirement, for parameter-efficient adaptation of 7–8B models.
- **Scaling ladder observed:** 24 GB RTX 4090 (QLoRA, 1 epoch, up to 70B) → 48 GB RTX A6000 (LoRA/QLoRA + RFT, 7–8B, overnight/daily retraining) → 48 GB × 7 (multi-agent RFT with co-located vLLM judges) → 2 × A100-80 GB (8B with 16k+ token retrieved contexts) → 8 × A100 / 8 × H200 / 8 × A6000 (full domain-adaptation series or full-parameter post-training).
- **Cheapest verified full adaptation:** TelecomGPT's instruct-tuning stage took **~1.5 h on one 8-GPU node**, and Tele-LLMs' entire 1B–8B series cost **~5,000 GPU-hours on 8×A6000**.
- **Training hardware is reported far more often than inference latency.** Of ~48 works surveyed, only a handful report any latency figure at all.
- **Inference latency remains the field's unresolved problem.** End-to-end LLM latency in a network control loop is reported at **0.8–3.6 s** (RRC emulation), **9.4 s** (Non-RT O-RAN LLM), and **793 ms** (Near-RT O-RAN SLM) — all far above near-RT (10 ms–1 s) requirements. Only the **small/distilled models** get close: **0.847 ms** (WPFM on Jetson Xavier NX), **12 ms** (MTNTD-SLM), **0.93 ms/packet** (NetKD), **300–500 ms** (TSLAM-8B on Inferentia2, *vendor blog*), and **sub-100 ms** (KGLlama-KD, distilled).
- **⚠️ The most-cited telecom-LLM latency number in the field (300–500 ms) comes from a non-peer-reviewed vendor engineering blog.** This is a real evidentiary weakness in the literature and should be flagged as such in the survey.

---

### D. Accuracy and network performance? Comparison against general-purpose LLMs and smaller models?

**Fine-tuned vs. general-purpose — positive results:**
- Mobile-LLaMA: **247/300 vs GPT-3.5's 209/300** on network-analysis code generation.
- **TelecomGPT vs GPT-4o on telecom knowledge: on the extended TeleQnA benchmark the fine-tuned Llama3-8B-TI reaches 94 vs GPT-4o's 93 and GPT-3.5's 89** (base Llama3-8B-Instruct: 88.49). On 3GPP technical-document classification the gap is dramatic: **Llama3-8B-TI 75.30 vs GPT-4o 38.94 and GPT-3.5 38.54**. On standard TeleQnA, however, GPT-4o (78) and GPT-4 (75) still lead Llama3-8B-TI (71.20). On Telecom Math Modeling the fine-tuned model essentially matches GPT-4 (**Llama3-8B-TI-TA 49.45 avg MathBERT vs GPT-4 49.38**).
- **5G Instruct Forge: fine-tuned Llama3-8B / Solar-10.7B / Mistral-7B "outperform OpenAI's GPT-4 on 5G-specific tasks", with ROUGE-L F1 0.55/0.58 vs GPT-4's 0.35** (BERTScore F1 was close).
- RRC-LLM: **median cosine similarity 0.970** vs. **GPT-4o 0.496, Gemini 1.5-Flash 0.585, Claude 3.5 Sonnet v2 0.768, GPT-o3-mini 0.705, original Llama-3-8B 0.600** — a **+61% relative gain** over zero-shot.
- Habib et al.: QLoRA fine-tuning gives **BERTScore 0.92 vs 0.86**, **METEOR 0.89 vs 0.83**, **semantic similarity +9%** over the base LLaMA.
- Ericsson MAS: fine-tuned 8B judged **comparable in quality to GPT-4o-mini**, while the base model produced only generic answers. RAGAS reward **3.44 → 5.19**, total reward **5.96 → 10.51**, reward std-dev **2.17 → 0.38**.
- KGLlama-KD: **95% accuracy for intent understanding, +8% average over DeepSeek and Qwen.**
- Tele-LLMs: **+25% average relative improvement** on Tele-Eval — but on *telecom literature/knowledge* tasks, not network management.

**Network performance (KPIs, as opposed to NLP metrics):**
- Habib et al.: HDTGA orchestration gives **throughput +19.3%, delay −48.5%, energy efficiency +54.9%** vs. HRL/DT baselines; predictive intent validation rules out bad intents with **88% accuracy**.
- Ericsson MAS: **~6× reduction in mean troubleshooting time per node, +10% accuracy** vs. human engineers.
- Navidan et al.: agentic control gives **+6% VIP throughput** over SLM-only while holding **22 ms** latency for the latency-sensitive slice; SLM-only reaches just **10.5 Mbps** VIP throughput.
- G-SPEC: **94.1% successful remediation vs 82.4% baseline**; **zero observed safety violations**; **0.2% hallucination detection**.
- MERLOT: matches or beats a 7B baseline on 8 of 10 traffic-classification datasets.

**Smaller models — mixed, and size-dependent:**
- **Size helps** on troubleshooting: 8B > 4B > 1.7B in reward and stability (Ericsson MAS), with the 8B reaching peak reward ≈10 while 4B/1.7B "show modest improvements but consistently lower rewards."
- **Size helps** on structured translation: NetIntent found **QwQ/Command-r (32–35B) ≥99%**, **Codellama/Mistral 7B up to 95% with lower latency**, while **TinyLlama 1.1B and Deepseek-coder 1.3B "show significantly lower accuracy"** and many small models produce 0% on ONOS flow-rule tasks.
- **But size is not decisive**: **Codestral-22B outperformed Command-r-35B**; **Codellama-70B and Llama2-70B "lagged behind smaller, code-specialised models like Codestral:22b"**; **Llama2-70B had perfect recall on conflict detection but 52 false positives**, rendering it "practically unfit."
- **Small + specialised can win**: **MERLOT at 660M parameters matches/beats a 7B TrafficLLM on 8 of 10 datasets** with 85–90% less inference time and memory.
- **Distilled-size parity on a telecom task (2023)**: in *Understanding Telecom Language Through Large Language Models*, **DistilBERT (66M) reached ~equal accuracy to BERT-Base (110M) and RoBERTa (125M) — 84.6% vs 83–84.6% — with ~50% fewer parameters.** This is the earliest "compression costs nothing here" datapoint in the corpus.
- **Pushing specialisation too far destroys general capability** (5G Instruct Forge): increasing Mistral-7B's trainable-parameter fraction from 11% to 17% **collapses MMLU from 19.84 to 14.74**, even though the 5G-exam score at 11% (101.0) is itself lower than at 6% (164.0) and 9% (160.0). The paper still selects 11%.
- **Full fine-tuning vs LoRA is non-monotonic in size** (RRC emulation): on **8B**, LoRA r=16 **matches or slightly surpasses full fine-tuning**; on **3B/1B**, **full fine-tuning remains advantageous**. Tele-LLMs found the opposite direction of trouble: LoRA's gradient norm was *too low* on LLaMA-3-8B to inject domain knowledge during continual pre-training.
- **A cautionary negative result:** *Lightweight LLMs for Network Attack Detection in IoT Networks* (PREPRINT arXiv:2601.15269) QLoRA-4-bit-tuned LLaMA-3.2-1B, Mistral-7B and LLaMA-3.1-8B on CICIoT2023 and found the **best LLM (LLaMA-3.2-1B, F1 0.7124) did NOT beat a classical Random Forest (F1 0.7159)**; RAG zero-shot accuracy was only 42.63%. A rare published case where fine-tuned LLMs fail to justify themselves against classical ML on a network task.
- **A hard capability ceiling on *solution generation***: **TeleCom-Bench (KDD '26, 22,678 samples) documents an "Execution Wall" — models exceed 90% on intent recognition and entity extraction but only ~30% on solution generation.** This is the sharpest published statement that current telecom LLMs recognise network problems far better than they solve them.
- **Task specialisation beats scale**: G-SPEC's ablation attributes only **8%** of safety gains to TSLAM fine-tuning, **68% to knowledge-graph validation and 24% to SHACL policies**. ORION found the bottleneck is the **MCP tool-orchestration layer, not model semantics** — among models with ≥97% prediction rate, accuracy spanned only 90–99%.

---

### E. Does pruning help? Does quantization help? Does distillation help?

**Quantization — YES, with a measured and modest quality cost.**

The strongest evidence is the RRC-emulation paper (arXiv:2505.16821), which is the *only* paper found with a clean FP16-vs-INT4 ablation on a networking task across four model sizes:

> "**INT4 (Q4_K_M) consistently reduces median latency by ≈20–30% relative to FP16 at comparable decoding settings, with small average reductions in ASN.1/SMC pass (typically a few percentage points and backbone-dependent). The largest drops appear on the smallest backbone (1B), consistent with reduced numerical headroom.**"

Concrete pairs from its tables: L-3 8B `RRC_constrain` FP16 = 3,544 ms / Q4_K_M = 2,556 ms (ASN.1 pass 1.000 both); L-3.2 3B FP16 = 2,341 ms / Q4_K_M = 1,733 ms (SMC 0.991 → 0.968); L-3.2 1B FP16 = 2,093 ms / Q4_K_M = 2,025 ms (**SMC 0.989 → 0.883 — a 10.6-point drop**). **Quantisation therefore helps latency (20–30%) but hurts quality most on the smallest models.**

Supporting: the NetSoft 2025 paper quantises **Llama 3.2 3B from 16-bit to 4-bit** specifically to "reduce memory demands, enabling deployment on modest hardware like edge devices" (numeric results unverified). G-SPEC runs TSLAM-4B in 4-bit. Telco-RAG contributes a **neural-network router that reduces RAM usage** for 3GPP retrieval "without LLM fine-tuning" (exact saving unverified).

**A key counter-lesson on PEFT (relevant to Question E):** two independent groups **explicitly rejected LoRA** for telecom/5G domain adaptation and reported *why*:
- **Tele-LLMs** (IEEE Access 2026): LoRA r=64/α=32/0.1 — "for smaller models LoRA can initially inject telecom knowledge but **quickly saturates** due to its limited capacity"; on LLaMA-3-8B "the **gradient norm of the LoRA method remained extremely low**. This hindered parameter updates, causing the training loss to barely change." → full fine-tuning required. *(Caveat: reported only in a figure, with no numeric table.)*
- **5G Instruct Forge** (IEEE TCCN 2025): "we **opted not to use LoRA due to the significant domain shift**" → used partial **freeze-tuning** with 9–12% trainable parameters instead.
- **Contrast:** MERLOT and AQM-LLM succeed with distillation rather than PEFT, and TelecomGPT uses QLoRA r=512 successfully — so LoRA's failure is **rank- and task-dependent, not universal**. G-SPEC runs **TSLAM-4B in 4-bit "to simulate edge-deployment constraints."** SQLLM applies static quantisation with a dynamic smoothing factor for 5G private-network attack detection (values unverified).

**Distillation — YES, and it is the most consistently successful compression technique for networking.** ⚠️ **But the evidence base is smaller than a keyword search suggests:** two of the most-cited "distillation" papers in this space (**AQM-LLM #17** and **Cost-Efficient KD Student Placement #23**) turn out on inspection to contain **no empirical teacher–student distillation at all** — one is LoRA+RL and the other is a placement optimisation problem. Count evidence by verified mechanism, not by title.
- **MERLOT** (IEEE GC Wkshps 2025): KD (teacher–student, KL + CE) from GPT-2-base **plus pruning of the gating network** in an MoE yields a **660M model that matches/beats a 7B TrafficLLM on 8 of 10** encrypted-traffic datasets with **85–90% less inference time and memory**.
- **KGLlama-KD** (IEEE TMC 2026): KD on a Llama 3 base gives **−60% inference latency** and **95% intent-understanding accuracy** (+8% over DeepSeek/Qwen).
- **AQM-LLM** (IEEE TON 2026): distillation via speculative decoding + reinforcement-based distillation applied to **L4S active queue management** (numbers unverified).
- **MERLOT-class**: MTNTD-SLM uses **multi-teacher debate-distillation** for malicious traffic detection (poster; details unverified).
- **NetKD** (IEEE CSCWD 2024, DOI 10.1109/CSCWD61410.2024.10580837): **the strongest quantitative compression result in the entire corpus** — BERT → NetKD-BERT for encrypted traffic: **4.61% of baseline parameters, 99.10% of baseline F1, 0.93 ms/packet, 7.33% of baseline memory, 14.3x faster.** *(From a parallel verification pass; not independently re-verified by me.)*
- **MTNTD-SLM** (IEEE SECON 2026 poster): multi-teacher debate-distillation (teachers = TrafficLLM + TrafficGPT + DoLLM) into a small model — **F1 96.40% (CSTNET 2023), 99.56% (USTC-TFC 2016), latency 12 ms.** Parameter counts, hardware and dataset sizes **not reported**. *(Poster; details from a parallel verification pass.)*
- **xApp distillation** (Computer Networks 2026): distils **xApp control policies** for O-RAN conflict mitigation — **83.3% outage reduction at 10 Mbps**. **⚠️ NOT a transformer/LLM** (the policies are DQN MLPs, distillation temperature 20); cite as an O-RAN policy-distillation anchor, not as LLM compression. *(Numbers from a parallel verification pass.)*
- **5G-V2X Intra-Slice IDS** (IEEE ICC 2023, DOI 10.1109/ICC45041.2023.10279212): cloud-teacher → CAV-student distillation with **>50% computation and memory reduction**. *(Not independently verified.)*
- **LENS-XAI** (PREPRINT arXiv:2501.00790): KD + VAE intrusion detection, T=2, α=0.5, teacher 13,065 → student 4,489 parameters, **44% peak compute reduction**, on an RTX 4080 Super. **⚠️ NOT a transformer** (tiny dense nets).

**Pruning — PARTIAL / WEAKER evidence, and the pruning that works is structural, not weight-level.**
- **MERLOT** explicitly prunes the MoE gating network (a distilled, pruned GPT-2-base) — but it does **not** report a pruning ablation, so the marginal contribution of pruning is unmeasured.
- **5G Instruct Forge** is the closest thing to a *parameter-reduction* ablation on a telecom LLM, but it ablates the **trainable** fraction (6/9/11/17%), not the deployed parameter count — so it measures adaptation capacity, not compression.
- **Pruned Traffic Trees** (arXiv:2608.21874, under review at INFOCOM 2027) is the strongest pruning result: **protocol-structure-guided** pruning + width reduction + logits distillation gives **PTT-Lite with 80.3%/61.3% fewer parameters, 98.85%/98.78% lower effective GFLOPs, and 8.75×/8.46× CPU speedups**, retaining **0.9325 Macro-F1 vs 0.9519 for the unpruned model** — i.e., **80% parameter removal costs only ~1.9 Macro-F1 points**. But it is a **preprint**, and the compressed model is a purpose-built protocol-structured architecture, **not an LLM**.
- **SPARTA** (Future Internet 2026, DOI 10.3390/fi18020088) is the **only work found pruning true multi-billion-parameter LLMs** (LLaMA 7B/13B/30B/65B; Wanda unstructured + 2:4 semi-structured) — **but it evaluates on Wikitext2, NOT network traffic.** Its link to threat analysis is an explicit *analogy*, and its speedups are simulation-only (Accel-Sim). **It therefore provides zero evidence that pruning preserves network-task quality**, and citing it as such would be a misrepresentation.
- **OB-IDS** (#49) is the closest thing to a complete compression stack: **INT8 QAT+PTQ → structured pruning of attention heads + FFN at 40/60/75% sparsity → KD (T=4, α=0.7) → iterative self-distillation**, taking BERT-base from **110M/438 MB to 38M/32 MB** while keeping **98.44% (UNSW-NB15) / 98.19% (CIC-IDS2017)** and cutting Raspberry Pi 4 latency **214.6 → 27.4 ms (−87.3%)**. ⚠️ Small regional venue, and there is a **second, unrelated OB-IDS paper** (IEEE BlackSeaCom 2025) with a near-identical title — do not merge them.
- **HiPELog** (#55) applies LoRA to log anomaly detection (**99.87% BGL accuracy, 8,192 of 63.47M trainable params**) — but that is PEFT, not compression; serving cost is unchanged.
- **No paper was found that applies weight-, neuron-, layer- or attention-head-level pruning to a fully-reported LLM used for network management and reports a pruning ablation on a network task.** BeamTransFuser (#51) comes closest methodologically (module-aware splitting pruning, attention heads deliberately preserved, **>80% latency reduction at ratio 0.4; DBA-Score 85.95% at ratio 0.7**) but it prunes a hierarchical beamforming transformer, not an LLM, and its title is disputed between two records. **This remains an open contribution.**
- **Compression is not free even when it works.** MERLOT's 660M model loses to a 7B baseline on 2 of 10 datasets (APP-53: 0.8601 vs 0.9320; CW-100: 0.8466 vs 0.9366). PTT-Lite loses ~1.9–2.8 Macro-F1 points. INT4 costs the 1B RRC model 10.6 SMC points. **Any survey claim that compression is "lossless" in this domain is contradicted by the data.**
- **A structural evidence gap**: **no paper retrieved reports a billion-parameter LLM teacher compressed into a network-domain SLM with full, reproducible compression hyperparameters.** The well-documented compressions (MERLOT, Pruned Traffic Trees, OB-IDS, NetKD) all operate on **GPT-2-base / BERT-base / GAT models at ≤120M parameters**. The papers that *do* compress genuine LLMs (KGLlama-KD #20, MTNTD-SLM #24, SPARTA #54) each withhold a critical piece — temperature/α, teacher/student parameter counts, training hardware, or network-task evaluation. **There is a clear empirical hole between "well-documented compression of small transformers" and "poorly-documented compression of true LLMs" in this domain.** This is the single most promising gap for a PhD contribution.
- **A safety cost is documented separately.** SafeCOMM (#33, IEEE WCNC 2026) shows that fine-tuning on telecom data — and especially continual pre-training without safety instruction tuning, as in Tele-LLMs — **degrades safety alignment, with Tele-LLMs reaching ~90% harmfulness**. Compression and domain adaptation both carry non-accuracy costs.

---

### F. Is there a trade-off between model size and network decision quality?

**Yes — and the literature's honest answer is "size is a weak and unreliable predictor."** Three papers address this directly and quantitatively:

**F1. NetIntent (IEEE OJ-COMS 2025) — 33 models, 1.1B to 70B, same task, same prompts.**
The paper states it outright: *"The evaluation reveals that **larger model size does not inherently guarantee superior performance** in translating high-level network intents into ONOS-compatible flow rules."* Evidence:
- **Llama3.3-70B: 88% zero-shot accuracy** — but **Codellama-70B and Llama2-70B "showed only modest accuracy gains despite increasing context, and their overall performance lagged behind smaller, code-specialised models like Codestral:22B."**
- On flow-rule tasks: **Codestral-22B outperformed Command-r-35B.**
- On conflict detection: **Llama2-70B had perfect recall but 52 false positives** — "practically unfit."
- Latency penalty is steep: **Codellama-34B >10 s per inference vs Qwen2.5-7B <2 s at competitive accuracy.**
- Authors' conclusion: *"task accuracy depends on prompt design, schema alignment, and in-context learning **rather than on model size alone**."*

**F2. Ericsson (arXiv:2511.00651) — controlled 1.7B / 4B / 8B comparison on the same troubleshooting task.**
The **8B model achieves peak reward ≈10**; **4B and 1.7B "show modest improvements but consistently lower rewards compared to the 8B model."** Because these are *the same family* (Qwen3) at *the same task*, this is the cleanest size-scaling evidence in the corpus — and it points the **opposite** way from NetIntent: within a family and a task, bigger is better.

**F3. RRC emulation (arXiv:2505.16821) — 1B / 3B / 8B, full FT vs LoRA, FP16 vs INT4.** Parameter count interacts with the *adaptation method* and the *precision*:
- **8B: LoRA r=16 matches or surpasses full fine-tuning.**
- **3B/1B: full fine-tuning is advantageous** ("smaller models favour full updates for best accuracy").
- **INT4 hurts the 1B model most** (SMC 0.989 → 0.883 vs. essentially no loss at 8B).

**Also relevant:** MERLOT shows a **660M distilled MoE matching a 7B model on 8/10 datasets** — i.e., a **10× size reduction at near-parity**, with actual losses on 2/10 datasets. G-SPEC's ablation shows **model fine-tuning contributes only 8%** of the safety outcome, against 68% for knowledge-graph validation. ORION shows the **orchestration layer, not model semantics, is the bottleneck**.

**Not answered by the literature:** I found **no paper** that plots network-decision quality (e.g., throughput, SLA fulfilment, remediation success) against model parameter count across a compressed model family. Every size-vs-quality result found is on an **NLP proxy metric** (reward, cosine similarity, ASN.1 pass rate, Macro-F1, classification accuracy), not a **network KPI**. See the trade-off table below.

---

<a name="tradeoff"></a>
## Trade-off table: model size / compression vs. decision quality (exact numbers only)

| Paper | Size / compression axis | Quality metric | Result | Network-KPI outcome |
|---|---|---|---|---|
| **RRC emulation** (arXiv:2505.16821) | FP16 → **INT4 (Q4_K_M)** | ASN.1 pass / UL→DL state-machine conformance | L-3 8B: 1.000 → 1.000 ASN.1 (latency 3,544 → 2,556 ms). L-3.2 3B: SMC 0.991 → 0.968 (2,341 → 1,733 ms). **L-3.2 1B: SMC 0.989 → 0.883** (2,093 → 2,025 ms) | Median latency **−20 to −30%** across the board |
| **RRC emulation** | **1B / 3B / 8B**, LoRA-r16 vs full FT | Validator pass | On **8B, LoRA r16 ≈ full FT**; on **3B/1B, full FT better** (best-two gap Δ≈6e-4) | not reported as a KPI |
| **RRC emulation** | **Llama-3.2-1B/INT4**, M2 Max vs 1×GH200(H100) | Schema-check median / similarity / SMC | M2: 0.97 / 1.00 / 0.54. GH200: 0.96 / 1.00 / 0.53 — **quality is platform-agnostic** | Latency **1.84 s vs 1.092 s**; energy **7.7 mWh vs 0.200 Wh** per message |
| **MERLOT** (10.1109/GCWkshps68340.2025.11591188) | **7B TrafficLLM → 660M MERLOT** (KD + pruned gating MoE) | F1 | Wins 8/10 datasets (e.g. CSTNET 0.9996 vs 0.9599; Tor 0.9845 vs 0.9810). **Loses 2/10**: APP-53 0.8601 vs 0.9320; CW-100 0.8466 vs 0.9366. 1.25B variant recovers to 0.8702 / 0.8892 | **85–90% less inference time and memory** |
| **Pruned Traffic Trees** (arXiv:2608.21874) | **PTT-Full → PTT-Lite**: 80.3% / 61.3% fewer params | Macro-F1 | CSTNET-TLS1.3: 0.9519 → **0.9325** (−1.94 pts). CipherSpectrum: 0.9416 → **0.9136** (−2.80 pts) | **98.85% / 98.78% fewer effective GFLOPs; 8.75× / 8.46× CPU speedup** |
| **Ericsson** (arXiv:2511.00651) | **1.7B / 4B / 8B** (same family, same task) | GRPO/RAGAS reward | 8B peak ≈**10**; 4B and 1.7B "**consistently lower rewards**". Fine-tuned 8B total reward **5.96 → 10.51**, std-dev **2.17 → 0.38** | **~6× faster troubleshooting; +10% accuracy** vs humans |
| **NetIntent** (10.1109/OJCOMS.2025.3642642) | **1.1B → 70B**, 33 models, no training | Accuracy / F1 / FPR | **QwQ-32B/Command-r-35B ≥99%**; **Codellama/Mistral-7B ≤95%**; **TinyLlama-1.1B & Deepseek-coder-1.3B clearly worse**; **Codestral-22B > Command-r-35B**; **70B models marginal and memory-limited**; **Llama2-70B: perfect recall but 52 FPs (unfit)** | Runtime: **Codellama-34B >10 s vs Qwen2.5-7B <2 s** |
| **KGLlama-KD** (10.1109/TMC.2026.3678546) | **Full-scale Llama 3 → distilled student** | APPI understanding accuracy | **95%** (+8% avg over DeepSeek and Qwen) | **Inference latency −60%**, meeting sub-100 ms |
| **O-RAN agentic** (arXiv:2602.14117) | **Model size mapped to control-loop timescale** (WPFM / SLM / LLM) | Remediation / throughput | Agentic (LLM+SLM) **+6% VIP throughput** vs SLM-only (**10.5 Mbps**) while holding **22 ms** | **Latency: 0.847 ms (Xavier NX) / 793 ms (RTX 5090) / 9,364 ms (H200)**, described as "a necessary trade-off" |
| **TelecomGPT** (10.1109/TMLCN.2025.3593184) | **7B–8B base models**, QLoRA r=512 | TeleQnA / tdoc classification / Math Modeling | **TeleQnA: Llama3-8B-Instruct 64.80 → Llama3-8B-TI 71.20** (GPT-4o 78, GPT-4 75). **Extended TeleQnA: 88.49 → 94** (beats GPT-4o's 93). **3GPP tdoc classification: 33.35 → 75.30** (GPT-4o 38.94). Math Modeling avg MathBERT 40.78 → 46.16 (TI) / 49.45 (TI-TA) vs GPT-4 49.38 | no network KPI; training cost **~6 h + ~1.5 h on 8× ml.p4d.24xlarge** |
| **5G Instruct Forge** (10.1109/TCCN.2024.3516055) | **Trainable-parameter fraction** 6% / 9% / 11% / 17% (Mistral-7B) | MMLU (general) vs 5G exam score | **6%: 21.99 / 164.0; 9%: 22.45 / 160.0; 11%: 19.84 / 101.0; 17%: MMLU collapses to 14.74** | 5G task beats GPT-4 (ROUGE-L 0.55/0.58 vs 0.35) at the cost of general knowledge |
| **Understanding Telecom Language** (10.1109/GLOBECOM54140.2023.10437725) | **BERT-Base 110M → DistilBERT 66M** (~50% fewer params; not produced by the authors) | 3GPP tdoc classification accuracy | **BERT/RoBERTa 84.6%, GPT-2 83%, DistilBERT ≈equal with ~50% fewer parameters** | no network KPI |
| **G-SPEC** (arXiv:2512.20275) | **TSLAM-4B at 4-bit** | Remediation success / safety | **94.1% vs 82.4%** baseline; 0 violations; 0.2% hallucination. Ablation: NKG 68%, SHACL 24%, **fine-tuning only 8%** | **+142 ms** validation overhead |

**Verdict:** a size/compression-vs-quality trade-off **is documented, with exact numbers**, for NLP-proxy metrics (latency vs. conformance, parameters vs. Macro-F1, latency vs. accuracy). What is **not** documented anywhere in this corpus is a curve of **network KPI** (throughput, SLA fulfilment, energy) against model size or compression ratio.

---

<a name="cautions"></a>
## Caution note: what I could NOT verify

**Method-level caveats**
1. **IEEE Xplore was returning HTTP 502 / purchase walls throughout the research window.** This blocked full-text access to several papers including #9 (Network Self-Configuration SLM), #19 (SQLLM), #21 (xApp distillation), #23 (KD student placement), #24 (MTNTD-SLM) and #25 (Optical Network Failure Management). For those, I verified **bibliographic metadata via the Crossref REST API** (title, authors, venue, volume, pages, DOI, year) but **not** the experimental numbers or hardware. Rows affected are explicitly marked "not verified."
2. **Two findings rest on abstract-level evidence only** — #10 (NetSoft 3GPP LLM) and #20 (KGLlama-KD). Their headline numbers (4-bit quantisation of Llama 3.2 3B; 95% accuracy / −60% latency) are quoted **as the authors state them**, and I have flagged them as unverified rather than presenting them as independently confirmed.
3. **`not reported` is used strictly.** Where a paper's abstract or retrieved text simply omits a field (e.g., Mobile-LLaMA's GPU count, TelecomGPT's base checkpoint), I wrote "not reported" rather than inferring a plausible value. **TelecomGPT's base model in particular is a real gap** — the paper is framework-agnostic and the checkpoint is not named in the text I retrieved.

**Quantitative caveats**
4. **Habib et al. (arXiv:2505.01841) contains an internal inconsistency**: the abstract says "reduces delay by 48.5% and boosts energy efficiency by 54.9%", while the body text at one point reverses these two figures (+54.9% throughput phrasing and 48.5% energy-efficiency). I have quoted both forms and flagged the discrepancy rather than picking one.
5. **The "6× faster / +10% accuracy" result in the Ericsson MAS paper (#6) compares against *human engineers*, not against an automated baseline.** It is not evidence that an LLM beats a classical ML/DL method.
6. **RRC-emulation latency figures (1.7–3.6 s) are the paper's own medians for generating a single DL RRC message.** They are reported honestly by the authors as *above* control-plane budgets, with sub-100 ms explicitly framed as future work.
7. **Preprint/peer-reviewed version divergence occurs.** MERLOT gained a fifth author (Xutong Li) between arXiv and the GC Wkshps version; AQM-LLM's arXiv v2 was **withdrawn** and only v3 is valid; the Ericsson edge-profiling paper is arXiv-only with no journal reference.

**Scope caveats**
8. **No paper was found that measures network-decision quality against model size or compression ratio directly.** Every size/compression trade-off found uses an NLP proxy metric. If the parent survey wants that curve, it is an open research contribution.
9. **No paper was found applying weight/neuron/layer/attention-head pruning to an LLM for network management with an ablation.** The only pruning results are MERLOT's (unablated) gating-network pruning and Pruned Traffic Trees' protocol-structure pruning on a non-LLM architecture.
10. **CORRECTED negative finding on venues.** An earlier draft of this report stated that no paper combining compression with networking exists at IEEE TNSM. **That was wrong and is retracted.** Four IEEE TNSM papers in this space were subsequently verified at metadata level: **HW-NAS for Encrypted Traffic Classification (#56, DOI 10.1109/TNSM.2026.3666676)**, **LLM-QFL (DOI 10.1109/TNSM.2026.3712394)**, **KD-PFL traffic classification (DOI 10.1109/TNSM.2025.3629241)** and **HKD-Net (DOI 10.1109/TNSM.2026.3668812)**. IEEE TNSM **does** publish in this area. Conversely, **no** compression+networking paper was found at IEEE JSAC, IEEE NOMS, IEEE CNSM, IEEE NetSoft, ACM CoNEXT, ACM IMC or ACM SIGCOMM — and **NetLLM (ACM SIGCOMM 2024) was fetched and grepped: quantization appears only in its related work**, so it is excluded. **The earlier "absence" claim was an artifact of the IEEE Xplore outage, not a property of the literature.**
11. **"Telco-LLM" and "TelecomLLM" do not appear to exist as papers.** Crossref bibliographic queries for these titles return only unrelated telecom-business articles. The only "Telco-LLM" artefact found is the **GSMA Open-Telco LLM Benchmarks** industry programme (an MWC Barcelona announcement, not a peer-reviewed paper) whose technical details were not verified. **"LLaMA-Telecom" also does not exist** as a titled paper. Do not cite any of these three without independent verification.
12. **Two corrections to the task's own venue premise**, independently confirmed via Crossref by both this research thread and a parallel verification pass: **TelecomGPT is in IEEE TMLCN, not IEEE TNSM** (TMLCN 3:948–975, 2025), and **Tele-LLMs is in IEEE Access, not IEEE TMLCN** (IEEE Access 14:86424–86441, 2026). **TeleQnA is now published** in IEEE Network 40(2):253–260, 2026.
13. **TelecomGPT's training-hardware description is internally inconsistent:** the paper states instruct tuning ran on "8 GPUs with 32 GB memory on one ml.p4d.24xlarge instance", but an ml.p4d.24xlarge ships 8 × A100 **40 GB**. The paper never writes "A100". This is reported verbatim rather than resolved.
14. **Tele-LLMs' central methodological claim (that LoRA is insufficient) is supported only by a figure.** The LoRA-vs-FFT comparison appears in Fig. 4; there is no numeric table of LoRA results comparable to the full-fine-tuning tables. Treat "PEFT is insufficient for telecom" as **directionally supported but not quantified**.
15. **The Mobile-LLaMA 247/300 score's rubric is undocumented at the stated scale:** the repo's three evaluation JSON files contain only 10 instructions each (30 total), against a nominal 300-point scale.
16. **The `ml.p4d` / 5G Instruct Forge MMLU ablation figures come from the HAL-deposited preprint of the TCCN paper**, not from the publisher's version of record. Bibliographic data was confirmed via Crossref; the experimental numbers were not re-checked against IEEE's final typeset version.
17. **Terminology drift is a real hazard in this literature — count mechanisms, not titles.** Two papers whose titles/framing imply knowledge distillation contain **no classical teacher–student KD**: **AQM-LLM (#17)** is LoRA (r=128) + offline RL, and its "99% reduction" refers to *trainable* parameters (7B → 70M) which does **not** reduce serving cost — the 7B model still needs 23.91 GB VRAM; the authors themselves list real pruning/quantization/distillation as *future work*. **HiPELog (#55)** and the **Cost-Efficient KD Student Placement (#23)** papers have the same issue (PEFT, and a placement optimisation problem respectively). A title-keyword survey of this field will substantially over-count compression evidence.
18. **SPARTA (#54) is the only billion-parameter LLM pruning paper found — and it evaluates on Wikitext2, not network traffic.** It must not be cited as evidence that pruning preserves network-task quality.
19. **Two OB-IDS papers exist** — Mamikonian & Mamamniashvili (*Georgian Scientists* 7(4), 2025, DOI 10.52340/gs.2025.07.04.49) and Ateş et al. (**IEEE BlackSeaCom 2025**, DOI 10.1109/BlackSeaCom65655.2025.11193891). Different authors, venues and DOIs; same quantize+prune+distill recipe. **Do not merge them.** The first is also a small regional venue.
20. **A title discrepancy needs resolution before citing:** the paper the compression deep-dive called **"BeamTransFuser"** corresponds to Crossref DOI **10.1109/TMC.2026.3712170**, whose registered title is **"Multi-Modal Beamforming with Model Compression and Modality Generation."** Same work renamed, or two different papers — unresolved.
21. **One dataset entry's DOI did not resolve:** TeleCom-Bench (10.1145/3770855.3817480). Treated as unverified.
22. **ORION and NetIntent do not fine-tune at all**, so they cannot answer whether a *small fine-tuned* model could replace a large prompted one on the same task. That experiment appears to be unrun.
23. **One dataset/paper (#12 in the discovery trail: "TMF921-Grounded Intent-to-Network-Configuration Dataset for 5G/6G")** appeared only as a Hugging Face dataset card referencing `arXiv:2603.03667`; that arXiv ID resolves to **ORION**, a different paper. I therefore **excluded it** from the main table rather than attribute an unverified title/authorship.

---

<a name="appendix"></a>
## Appendix: search strategy and verification method

**Search themes executed** (via web search, ~14 distinct query sets, each with 2–4 phrasings):
`LLM fine-tuning network management 5G LoRA` · `TelecomGPT fine-tuning dataset` · `Mobile-LLaMA telecom large language model` · `QLoRA 5G network management LLM` · `LLM for network configuration automation fine-tuning dataset` · `O-RAN LLM fine-tune xApp rApp` · `small language model network management 6G` · `knowledge distillation LLM network traffic classification` · `LLM quantization edge network management INT4` · `PEFT network management LLM IEEE TNSM` · `Tele-LLM telecom large language model training recipe` · `LLM pruning survey efficient large language models` · `LLM distillation network management small language model student teacher` · `LLM fine-tuning O-RAN resource allocation IEEE` · `NetLLM large language model networking` · `SQLLM secure quantized 5G private network` · `lightweight LLMs 3GPP specifications quantization` · `network self-configuration fine-tuned small language models` · `TSLAM-4B telecom large action model` · `preconfig network configuration automation` · `EvoRIC O-RAN RL fine-tuned LLM` · `LLM network operations survey` · and the citation-chaining queries listed below.

**Venues explicitly targeted:** IEEE TNSM, IEEE JSAC, IEEE TMC, IEEE TWC, IEEE TVT, IEEE TMLCN, IEEE TON, IEEE ComST, IEEE Network, IEEE Communications Magazine, IEEE OJ-COMS, IEEE ICC, IEEE GLOBECOM, IEEE NOMS, IEEE CNSM, IEEE NetSoft, IEEE INFOCOM, ACM MobiCom, ACM CoNEXT, ACM SIGCOMM.

**Citation chaining performed from:** Mobile-LLaMA → its GitHub repo (yielded the 15,111-instruction breakdown), TeleQnA, Tele-LLMs (yielded the PEFT-rejection and 8×A6000/5,000-GPU-hour results), TelecomGPT (yielded the TeleQnA/3GPP/doc benchmarks and the LLM-QAT/BitNet framing), and the Ericsson troubleshooting series (yielded the 1.7B/4B/8B comparison and the single-GPU profiling study).

**Verification method for bibliographic data:** every DOI, venue, volume, page range and author list in Groups (i)–(iii) was cross-checked against the **Crossref REST API** (`api.crossref.org/works?query.bibliographic=...`) in addition to the retrieved source page. Where Crossref and the retrieved page disagreed, both are shown. **No DOI in this report was constructed by pattern-guessing.**

**What was retrieved in full text:** arXiv HTML/ar5iv for 2407.09424, 2409.05314 (v3), 2402.02338, 2411.13004, 2505.01841 (v1), 2505.16821 (v5), 2511.00651, 2602.14117 (v2), 2603.03667, 2607.02523 (v1), 2512.20275, 2507.14398, 2608.21874 (abstract), 2511.14199 (abstract), 2506.00062 (abstract), 2412.15891 (abstract), 2608.26126 (abstract); GitHub README and the released fine-tuning script (`finetuning/mobile_llama_finetuning.py`) for Mobile-LLaMA; institutional repository records for KGLlama-KD (ECU) and the NetSoft 3GPP paper (FAPESP BV); Crossref records for all remaining DOIs.

**Corpus size and confidence tiers**

| Tier | Count | Meaning |
|---|---|---|
| **Fully verified** — bibliographic data cross-checked via Crossref **and** technical detail read from a full text I retrieved myself | **26** | Papers #1–#8, #10–#22, #26, #27, #29, #31 |
| **Bibliographic-only** — DOI/venue/authors confirmed via Crossref; technical fields not retrieved | **13** | #9, #19 (partial), #23, #24, #25, #28 (results read), #30, #32–#35 |
| **Cross-checked additions** — verified by a parallel deep-dive pass, then re-verified by me at metadata level | **13** | Rows 36–48 |
| **Explicitly flagged unverified** | 3 | TeleCom-Bench (DOI did not resolve), SPEC5G, Optical Network Failure Management |

**Additional verification performed for the additions in this revision:** all new DOIs were resolved against `api.crossref.org/works/<doi>` with matching titles — 10.1109/TMLCN.2025.3592658 (ORANSight-2.0), 10.1109/WCNC65185.2026.11555432 (SafeCOMM), 10.1109/LWC.2025.3578370 (AI²MMUM), 10.1145/3711992.3711996 (TelecomRAG), 10.18653/v1/2024.emnlp-industry.45 (TelBench), 10.1109/GLOBECOM54140.2023.10437725 (Understanding Telecom Language), 10.1109/TCCN.2024.3516055 (5G Instruct Forge), 10.1109/GCWkshp64532.2024.11101012 (TSpec-LLM), 10.18653/v1/2023.findings-ijcnlp.3 (SPEC5G), 10.1109/GLOBECOM52923.2024.10901158 (Telco-RAG). arXiv abstracts were fetched directly for 2506.00062, 2412.15891, 2608.26126, 2601.15269's companion, 2608.21874, 2511.14199. TelecomGPT's training hyperparameters and result tables were **re-read by me** from `ar5iv.labs.arxiv.org/html/2407.09424`; Mobile-LLaMA's LoRA configuration was **read by me from the released training script**. **The one DOI that did NOT resolve was 10.1145/3770855.3817480 (TeleCom-Bench) — treat that citation as unverified.**

**Machine-readable companion:** the same paper records are also written as JSON to `llm-net-papers/papers.json` in this workspace for import into a reference manager.
