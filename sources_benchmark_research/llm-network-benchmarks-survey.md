# Benchmarks for LLM / AI-Agent Performance in Network Management, Network Operations, and Networking Tasks

**A verified candidate list for a PhD survey on AI-native network management for 5G/6G**

Compiled 18 September 2026. Every DOI, venue, year and author list below was read from a live source: the **Crossref REST API**, **arXiv** abstract pages, **Zenodo**, **OpenReview/ICLR**, or a **publisher/institution page**. Fields that could not be confirmed are marked **UNVERIFIED** or "no DOI found" — never guessed.

**Method.** ~90 distinct web queries across the requested phrasings; three parallel discovery sweeps (telecom-domain, agentic-NetOps, venue-targeted); Crossref lookups by title *and* by DOI for authoritative metadata; arXiv abstract pages and the arXiv search UI; OpenAlex; Semantic Scholar; Zenodo; Hugging Face; GitHub. Citation chaining was attempted on NetConfEval (89 citing works) but the OpenAlex citation-expansion endpoint returned HTTP 429 under load, so chaining relied on Semantic Scholar "citing papers" pages plus targeted searches. **IEEE Xplore, ACM DL, Springer, GSMA.com and SSRN all block automated retrieval (HTTP 202/403)**, so IEEE/ACM metadata comes from Crossref (authoritative for bibliographic fields, silent on content) and content claims for those items are marked UNVERIFIED.

---

## 0. Direct answer to the survey question

**Yes — benchmarks for LLM/agent performance in network management now exist, and there are more of them than the initial reading list suggested. But none of them is a 5G/6G core or RAN management benchmark in the strict sense, and almost none evaluates SLA-level network outcomes.**

Concretely:

| Question | Answer |
|---|---|
| Is there a proper benchmark for LLM/agent **network configuration**? | **Yes, several.** NetConfEval (ACM CoNEXT/PACMNET 2024), NetArena (ICLR 2026), NetConfArena (preprint), NetConfBench (IETF draft), Cornetto (preprint), NetLLMBench (NFV-SDN 2024). |
| Is there one for **network troubleshooting / RCA**? | **Yes.** NIKA (preprint + published Zenodo dataset), FaulT-Bench (preprint), plus SADE as an agent evaluated *on* NIKA. |
| Is there one for **telecom / 3GPP knowledge**? | **Yes, the most mature area.** TeleQnA (IEEE Network), LDOT (IEEE JSAC), TSpec-LLM (Globecom Wkshps), ORAN-Bench-13K (CCNC), 6G-Bench (OJ-COMS), GSMA Open-Telco LLM Benchmarks. |
| Is there one for **intent translation**? | **Yes.** IBNBench (in NetIntent, IEEE OJ-COMS 2025). |
| Is there a **closed-loop 5G core** agent benchmark? | **Closest match: OperAID** (IEEE NetSoft 2026) — an open-source testbed evaluating LLM agents as autonomous operators of a **5G Core (Open5GS) on Kubernetes**, with fault injection → agentic diagnosis → remediation → execution-based verification. Note it injects *Kubernetes-level* faults (NetworkPolicy, ConfigMap, pod scaling), not 3GPP protocol-level faults. |
| Is there a **closed-loop 6G** agent benchmark? | **Closest match: 6GAgentGym / 6GAgentBench** (arXiv preprint) — closed-loop 6G management with 42 typed tools and an NS-3-calibrated Experiment Model. |
| Is there one that scores **SLA / latency / throughput outcomes**? | **Essentially no.** See §(b), gap 2. |
| Is there one that measures **cost, latency and safety** for network agents? | **Only α³-Bench** (preprint, UAV-over-6G) has a fully normalised cost/efficiency pillar; NetInjectBench covers safety/injection; NetArena and WirelessOptBench cover execution safety. |

**Recommended phrasing for the survey:** *"No peer-reviewed benchmark was found that evaluates LLM/agent performance on 5G/6G network management with SLA-level outcome metrics in a closed loop. The nearest efforts — OperAID (5G core on Kubernetes, IEEE NetSoft 2026) and 6GAgentGym/6GAgentBench (preprint) — cover infrastructure-level remediation and simulated 6G management respectively, and neither scores service-level guarantees."* Do **not** write "no benchmark exists" — that is false for networking generally, and a reviewer will find NetConfEval, NIKA and NetArena immediately.

---

## (a) Benchmark efforts, by category

### Category 1 — Network configuration: generation, synthesis, repair, validation

---

**1. NetConfEval: Can LLMs Facilitate Network Configuration?**
- **Authors:** Changjie Wang, Mariano Scazzariello, Alireza Farshin, Simone Ferlin, Dejan Kostić, Marco Chiesa
- **Year:** 2024
- **Venue:** *Proceedings of the ACM on Networking* (**PACMNET**), Vol. 2, No. CoNEXT2 — the **ACM CoNEXT 2024** journal track
- **DOI:** 10.1145/3656296 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** The founding benchmark in this space. Evaluates LLMs on network configuration synthesis across several configuration domains, scoring generated configurations against ground truth with semantic (not purely syntactic) equivalence. Tests a spread of open and frontier models and finds success strongly task- and model-dependent. Code: https://github.com/RedHatResearch/conext24-NetConfEval ; dataset: https://huggingface.co/datasets/NetConfEval/NetConfEval
- **Does NOT cover:** closed-loop execution on live devices, multi-turn agent behaviour, latency/token cost, or 5G/6G-specific configuration.
- **Sources retrieved:** https://api.crossref.org/works?query.bibliographic=NetConfEval ; https://marchiesa.bitbucket.io/docs/chiesa/netconfeval-conext-2024.pdf ; https://github.com/RedHatResearch/conext24-NetConfEval

---

**2. NetArena: Dynamic Benchmarks for AI Agents in Network Automation**
- **Authors:** Yajie Zhou, Jiajun Ruan, Eric S. Wang, Sadjad Fouladi, Francis Y. Yan, Kevin Hsieh, Zaoxing Liu
- **Year:** 2025 (v1, 3 Jun) / 2026 (v2, 13 Mar)
- **Venue:** **ICLR 2026** (poster). OpenReview forum id `BPVPOtzoOz`. ICLR proceedings carry no publisher DOI.
- **DOI:** 10.48550/arXiv.2506.03231 (arXiv-issued). **No publisher DOI found.**
- **Status:** Peer-reviewed (ICLR 2026) + arXiv preprint
- **What it does:** A *dynamic* benchmark generator that unifies heterogeneous network-operations tasks as finite state transition systems (state, action, execution function) and generates unlimited queries at runtime instead of a fixed expert-labelled set. Executes agents against **Mininet** and **Kubernetes** emulators and measures **correctness, safety, and latency**. Demonstrated on three applications: datacentre capacity planning, routing, and Kubernetes. Reports agents reach only **13–38 % average performance** (as low as 3 %) on large-scale realistic queries, and that small static benchmarks are statistically unreliable (confidence-interval overlap falls from **85 % to 0** as query count grows). Code: https://github.com/Froot-NetSys/NetArena ; leaderboard: https://github.com/Froot-NetSys/netarena_leaderboard
- **Does NOT cover:** 5G/6G RAN or core; cross-domain routing (conceded in the paper's limitations); defining the state/action space for each new task is manual.
- **Sources retrieved:** https://arxiv.org/abs/2506.03231 ; https://iclr.cc/virtual/2026/poster/10010955

---

**3. NetConfArena: An Executable Benchmark for LLM Agents in Closed-Loop Network Configuration**
- **Authors:** Chang Liu, Xiaohui Xie, Xinyi Chen, Yong Cui
- **Year:** 2026 (submitted 24 Aug 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2608.23179 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2608.23179
- **What it does:** Places LLM agents in emulated multi-device networks, provides a standardised compact action interface, and scores the resulting **network behaviour** with **hidden task-specific executable test cases**. An LLM-assisted, emulation-grounded pipeline converts human-oriented network materials into reusable parameterised templates: **480 task instances from 96 protocol-focused templates → 3,840 execution trajectories**. Finds failures are not limited to command errors: they include **task-specification-adherence gaps** and weak planning/execution.
- **Does NOT cover:** models tested are described only as "representative LLM agents"; no public repository found on the abstract page.
- **⚠ Note for the survey:** **NetConfArena is a different work from NetArena (item 2)** — same broad problem, different authors, different institution, different method. The two are frequently conflated. Do not merge them.
- **Source retrieved:** https://arxiv.org/abs/2608.23179

---

**4. NetConfBench — "A Framework to Evaluate LLM Agents for Network Configuration"**
- **Authors:** Yong Cui, Chang Liu, Xiaohui Xie, Chenguang Du
- **Year:** 2026 (draft-02 last updated 2026-07-06; expires 7 Jan 2027)
- **Venue:** IETF Internet-Draft `draft-cui-nmrg-llm-benchmark-02`, submitted to the IRTF **Network Management Research Group (NMRG)** as an individual submission
- **DOI:** no DOI found (Internet-Drafts receive no DOI)
- **Status:** **NOT peer-reviewed.** The IETF states the document "is not endorsed by the IETF and has no formal standing in the IETF standards process."
- **What it does:** Specifies an evaluation *framework*, not a populated leaderboard, for intent-driven network configuration by LLM agents. Defines an emulator environment (**GNS3** with official vendor images), an Agent–Network Interface (`get-topology`, `get-running-cfg`, `update-cfg`, `execute_validation`) with **MCP** tool definitions, a JSON task schema (intent, topology, initial config, one-or-more validated ground-truth solutions each with a reasoning trace, executable testcases), and two metric layers: **outcome metrics** (functional testcase pass rate — the primary metric) and **agentic process metrics** (command score, reasoning score via ROUGE/cosine similarity against ground truth). **Efficiency metrics (wall-clock time and token consumption) are explicitly optional.** Initial dataset: **40 tasks** across routing, QoS and security. Draft source: https://github.com/nobrowning/draft_llm_conf_benchmark
- **Does NOT cover:** no model comparison results; the contribution process, acceptance criteria and dataset versioning policy are explicitly future work; no 5G/6G content.
- **Source retrieved:** https://datatracker.ietf.org/doc/draft-cui-nmrg-llm-benchmark/

---

**5. Cornetto — "Benchmarking LLM-Driven Network Configuration Repair"**
- **Authors:** Ioannis Protogeros, Rufat Asadli, Benjamin Hoffman, Laurent Vanbever (ETH Zürich, Networked Systems Group)
- **Year:** 2026
- **Venue:** No venue found — **PREPRINT** (ETH NSG lists it as "arXiv")
- **DOI:** 10.48550/arXiv.2604.22513 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2604.22513
- **What it does:** The benchmark is named **Cornetto**; the authors describe it as "the first benchmark to evaluate LLM-driven network configuration repair functionally and at scale." A generation pipeline synthesises representative, plausible misconfiguration scenarios; an evaluation framework uses **formal verification** to assess functional correctness of proposed fixes against ground-truth specifications. Dataset: **231 problems** across topologies of **20–754 nodes** and diverse protocols; **9 state-of-the-art LLMs** evaluated. Key finding: models often introduce **regressions** and degrade at scale, motivating iterative workflows guided by formal verification.
- **Source retrieved:** https://nsg.ethz.ch/publications/2026-05-05-benchmarking-llm-driven-network-configuration-repair-20-500-11850-799709/

---

**6. Evaluating Agentic Configuration Repair for Computer Networks**
- **Authors:** Rufat Asadli, Benjamin Hoffman, Ioannis Protogeros, Laurent Vanbever
- **Year:** 2026
- **Venue:** ETH NSG labels it a **"Workshop Paper"** but does not name the workshop on the retrieved page — **UNVERIFIED venue**
- **DOI:** 10.48550/arXiv.2606.06212 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2606.06212
- **What it does:** Benchmarks open- and closed-source LLMs augmented with **formal network verification and context-retrieval tools** on configuration repair. Agentic architectures outperform base LLMs in repair efficacy (by **12 %** on average) and safety (by **17 %** on average), attributed to dynamic context management and iterative validation. Companion paper to Cornetto (item 5) from the same group.
- **Source retrieved:** https://arxiv.org/abs/2606.06212 ; https://nsg.ethz.ch/publications/2026-05-23-evaluating-agentic-configuration-repair-for-computer-networks/

---

**7. NetLLMBench: A Benchmark Framework for Large Language Models in Network Configuration Tasks**
- **Authors:** Kaan Aykurt, Andreas Blenk, Wolfgang Kellerer (TU Munich)
- **Year:** 2024 (Crossref `issued` 2024-11-05)
- **Venue:** *2024 IEEE Conference on Network Function Virtualization and Software Defined Networks* (**IEEE NFV-SDN 2024**)
- **DOI:** 10.1109/NFV-SDN61811.2024.10807499 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** A benchmark framework for LLMs on network configuration tasks. **Not in any of the venues on your target list** — this is the item that is often mis-attributed to TMLCN or TNSM. Content details (models, metrics, data availability) are **UNVERIFIED**; an accepted manuscript exists at https://mediatum.ub.tum.de/download/1759791/1759791.pdf (PDF not machine-readable by the fetch tool — read manually).
- **Source retrieved:** https://api.crossref.org/works/10.1109/NFV-SDN61811.2024.10807499

---

**8. NetAgentBench: A State-Centric Benchmark for Evaluating Agentic Network Configuration**
- **Authors:** Ahmed Twabi, Yepeng Ding, Tohru Kondo
- **Year:** 2026 (3 Apr 2026, 9 pages)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2604.09678 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2604.09678
- **What it does:** A dynamic benchmark that evaluates agents through a **Finite State Machine (FSM)** formalisation guaranteeing determinism, correctness and bounded execution, explicitly targeting multi-turn operational behaviour rather than static one-shot testing. Evaluates **four state-of-the-art LLM agents** on network configuration tasks and reports "severe exploration meltdowns and coherence collapse" on expert-level configurations.
- **Does NOT cover:** FSM abstraction rather than a live emulated topology; public artefacts **UNVERIFIED**.
- **Source retrieved:** https://arxiv.org/abs/2604.09678

---

**9. PeeringLLM-Bench: Evaluating LLMs for BGP Configuration Tasks**
- **Authors:** John Robert Mendoza, Roel Ocampo
- **Year:** 2025 (Crossref `issued` 2025-11-24)
- **Venue:** *Proceedings of the 20th Asian Internet Engineering Conference* (**AINTEC '25**), ACM
- **DOI:** 10.1145/3763400.3763451 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** A narrowly scoped benchmark for **BGP configuration** specifically — valuable because BGP policy semantics are where generic LLM configuration performance is typically weakest. Full text was behind a Cloudflare challenge, so model coverage, metrics and data availability are **UNVERIFIED**.
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=PeeringLLM-Bench

---

**10. Toward Agentic SysAdmin / NetLLMeval**
- **Authors:** Gianmaria Frigo, Davide Saladino, Alberto Castagnaro, Francesco Marchiori, Denis Donadel, Luca Pajola, Mauro Conti
- **Year:** 2026
- **Venue:** No venue found — **PREPRINT** (comments field: "Under submission")
- **DOI:** 10.48550/arXiv.2606.26960 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2606.26960
- **What it does:** Presents **NetLLMeval**, a framework that derives ground truth automatically from **live network emulation** instead of static reference outputs or manual expert validation — directly answering the annotation-bottleneck critique of NetConfEval-style datasets. Full-factorial study of **24,000 runs** across **10 foundation models, 4 solver architectures, 10 task types, and 6 network topologies** of increasing complexity. Key finding: **solver design dominates model scale** — a 14B open-weight model rose from 0.43 to 0.88 correctness under a better solver architecture, matching trillion-parameter frontier systems. Abstract states it is "released open-source" but **gives no URL — UNVERIFIED**.
- **Source retrieved:** https://arxiv.org/abs/2606.26960

---

**11. dsm2cli / A Reproducible Semantic Benchmark for Multivendor DSM-to-CLI Translation**
- **Authors:** Jerônimo Menezes, Leonardo Bitzki, Diego Kreutz, Gefte Almeida, Marcio Pohlmann, Rodrigo Mansilha
- **Year:** 2026
- **Venue (two related records):** (i) **PREPRINT** arXiv:2606.20564, stated as submitted to the *Workshop on Artificial Intelligence in Networks and Communications* (WIARC at SBRC 2026); (ii) a companion extended abstract with a different title — *"dsm2cli: An Observable Pipeline for Translating Network Intents into Multivendor CLI with Independent Semantic Assessment"* — in *Anais Estendidos do XLIV Simpósio Brasileiro de Redes de Computadores e Sistemas Distribuídos* (**SBRC 2026**), **DOI 10.5753/sbrc_estendido.2026.23256** (Crossref-verified)
- **DOI:** 10.48550/arXiv.2606.20564 (preprint); 10.5753/sbrc_estendido.2026.23256 (extended abstract)
- **Status:** **PREPRINT** for the full paper; extended abstract in a peer-reviewed (lightly reviewed) venue
- **What it does:** A reproducible **semantic** benchmark for translating high-level intents into multivendor CLI (three vendors), on the premise that syntactically valid output can still violate the intended operational state. Covers **5 cloud LLMs, 3 vendors, 5 use cases, 10 repeated runs per experimental cell**, fixed judges, explicit failure taxonomy. Findings: semantic quality and operational reliability are **orthogonal**; vendor effects dominate use-case effects; repeated-run dispersion predicts vote instability; Huawei VRP exposes failure modes hidden by aggregate metrics.
- **Source retrieved:** https://arxiv.org/abs/2606.20564 ; https://api.crossref.org/works?query.bibliographic=A+Reproducible+Semantic+Benchmark+for+Multivendor+DSM-to-CLI+Translation

---

**12. Continual Benchmarking of LLM-Based Systems on Networking Operations**
- **Authors:** Ioannis Protogeros, Laurent Vanbever (ETH Zürich)
- **Year:** 2025 (Crossref `issued` 2025-09-08)
- **Venue:** *Proceedings of the ACM SIGCOMM 2025 Posters and Demos* (**SIGCOMM '25**), pp. 70–72
- **DOI:** 10.1145/3744969.3748425 — **Crossref-verified**
- **Status:** Peer-reviewed (poster/demo)
- **What it does:** Proposes **continual** benchmarking of LLM-based systems on networking operations — i.e. addressing benchmark staleness and model/data contamination as models and networks evolve. Same ETH Zürich NSG group as Cornetto. **This is the most on-point SIGCOMM-venue citation for the "benchmarks go stale" argument in your gap section.**
- **Does NOT cover:** 3-page poster; metrics, models and code/data availability **UNVERIFIED** (Crossref holds no abstract; ACM DL paywalled to fetchers).
- **Source retrieved:** https://api.crossref.org/works/10.1145/3744969.3748425

---

**13. Enhancing Network Management Using Code Generated by Large Language Models** *(the "NeMoEval" line)*
- **Authors:** Sathiya Kumaran Mani, Yajie Zhou, Kevin Hsieh, Santiago Segarra, Trevor Eberl, Eliran Azulai, Ido Frizler, Ranveer Chandra, Srikanth Kandula
- **Year:** 2023 (Crossref `issued` 2023-11-28)
- **Venue:** *Proceedings of the 22nd ACM Workshop on Hot Topics in Networks* (**HotNets '23**), pp. 196–204 — an ACM SIGCOMM-sponsored workshop
- **DOI:** 10.1145/3626111.3628183 — **Crossref-verified**
- **Status:** Peer-reviewed (workshop)
- **What it does:** Natural-language network management via **LLM code generation**: the operator inspects the generated code and no network data is shared with the LLM — an explainability/scalability/privacy play. The prototype is "design[ed] and evaluate[d] … using benchmark applications," showing high accuracy and cost-effectiveness. Note this is also the **direct ancestor of NetArena** (shared authors Zhou, Hsieh).
- **⚠ Caution:** the name **"NeMoEval"** appears in some indexed snippets but does **NOT** appear in the retrieved arXiv abstract (arXiv:2308.06261). The attribution of that name to this paper is **UNVERIFIED** — cite the paper title, not the benchmark name.
- **Source retrieved:** https://api.crossref.org/works/10.1145/3626111.3628183 ; https://arxiv.org/abs/2308.06261

---

### Category 2 — Network troubleshooting, fault diagnosis, RCA, NetOps

---

**14. NIKA / "A Network Arena for Benchmarking AI Agents on Network Troubleshooting"**
- **Authors:** Zhihao Wang, Alessandro Cornacchia, Alessio Sacco, Franco Galante, Marco Canini, Dingde Jiang
- **Year:** 2025 (18 Dec 2025)
- **Venue:** No venue found for the paper — **PREPRINT** (its companion workshop paper, item 15, *is* published)
- **DOI:** paper — 10.48550/arXiv.2512.16381 (arXiv-issued). **Dataset — 10.5281/zenodo.17971675** (Zenodo, Crossref/DataCite-verified)
- **Status:** **PREPRINT** for the paper; the **dataset is a published, citable Zenodo record** (v1, 18 Dec 2025, CC-BY-4.0)
- **What it does:** Described by its authors as "the largest public benchmark to date for LLM-driven network incident diagnosis and troubleshooting." Provides zero-effort **replay of real-world network scenarios** and standardised agent–network interfaces. Comprises **906 reasoning traces over 54 distinct network issues across five network scenarios** (datacentre and campus/ISP), categorised into link failures, end-host failures, network node errors, misconfigurations, resource contention, and network under attack. The released traces were generated with **GPT-5, GPT-5-mini, and GPT-OSS:20B**, and evaluation compares agent submissions against `ground_truth.json`. Finding: larger models detect issues more often but still struggle to **localize faults and identify root causes**. Code: https://github.com/sands-lab/nika
- **Does NOT cover:** closed-loop remediation, SLA outcomes, or token cost as a first-class metric. Diagnosis only.
- **Sources retrieved:** https://arxiv.org/abs/2512.16381 ; https://zenodo.org/records/17971675

---

**15. Towards a Playground to Democratize Experimentation and Benchmarking of AI Agents for Network Troubleshooting**
- **Authors:** Zhihao Wang, Alessandro Cornacchia, Franco Galante, Carlo Centofanti, Alessio Sacco, Dingde Jiang
- **Year:** 2025 (Crossref `issued` 2025-09-08)
- **Venue:** *Proceedings of the 1st Workshop on Next-Generation Network Observability* (**NGNO '25**), co-located with **ACM SIGCOMM 2025** (Crossref `event` field confirms SIGCOMM '25)
- **DOI:** 10.1145/3748496.3748990 — **Crossref-verified**
- **Status:** Peer-reviewed (workshop)
- **What it does:** A short/position paper arguing for a shared, open playground for reproducible benchmarking of LLM/AI agents on network troubleshooting — the direct conceptual precursor to NIKA (item 14). Clickable citation for "network-agent benchmarking" in a SIGCOMM venue. Introduces no dataset and reports no leaderboard.
- **Sources retrieved:** https://api.crossref.org/works/10.1145/3748496.3748990 ; https://conferences.sigcomm.org/sigcomm/2025/workshop/ngno/

---

**16. SADE: Symptom-Aware Diagnostic Escalation for LLM-Based Network Troubleshooting**
- **Authors:** Kuan-Hao Tseng, Niruth Bogahawatta, Yasod Ginige, Kosta Dakic, Arunan Sivanathan, Suranga Seneviratne
  - *Author-name discrepancy: Crossref (IEEE LCN 2026) renders the fifth author "Kosta **Dakic**"; the arXiv v1 listing renders it "Kosta **Dekic**". I report the Crossref spelling and flag the discrepancy rather than silently choosing.*
- **Year:** 2026 (Crossref `issued` 2026-10)
- **Venue:** *2026 IEEE 51st Conference on Local Computer Networks* (**IEEE LCN 2026**)
- **DOI:** 10.1109/LCN67947.2026.11660797 — **Crossref-verified**
- **Status:** Peer-reviewed + arXiv preprint (arXiv:2605.04530)
- **What it does — important framing:** SADE is **an agent, not a benchmark.** It encodes the classical Cisco troubleshooting methodology as an explicit phase-gated policy, separating evidence acquisition from hypothesis commitment, with a routed library of fault-family skills. It is **evaluated on NIKA** (item 14): on a held-out **523-incident set covering eleven unseen NIKA scenarios**, SADE improves root-cause F1 by **37 percentage points** over a ReAct + GPT-5 baseline; a model-controlled comparison against the same Claude Sonnet backend attributes **22 of those points to the diagnostic policy alone**. Cite it as evidence about agent design, not as a benchmark contribution.
- **Sources retrieved:** https://arxiv.org/abs/2605.04530 ; https://api.crossref.org/works?query.bibliographic=SADE+Symptom-Aware+Diagnostic+Escalation

---

**17. FaulT-Bench: Towards Benchmarking Network Troubleshooting LLM Agents under Unreliable User Tickets**
- **Authors:** Kuan-Hao Tseng, Niruth Bogahawatta, Yasod Ginige, Kunjan Patel, Kosta Dakic, Suranga Seneviratne
- **Year:** 2026 (27 Aug 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2608.27021 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2608.27021
- **What it does:** Fills a practically important gap: existing troubleshooting benchmarks assume the ticket is accurate and that a fault is present. FaulT-Bench contains **200 troubleshooting scenarios across eight network topologies** (five reimplemented from public practitioner labs), spanning genuine faults, **false fault reports, incorrect device attribution, and incorrect root-cause claims**. It rewrites **72 false-premise tickets into five reporter personas**, varying confidence and verifiable detail one factor at a time with network state held fixed. The harness deploys each scenario in **Kathará**, agents interact through the **NIKA tool interface**, and an **LLM judge** scores free-text diagnoses on **outcome, fix, and reasoning quality**. Agents evaluated: **SADE, ReAct, and Claude Code**. Findings: all three are near-saturated on accurate tickets and robust to misdirection, but degrade sharply when the network is healthy and the ticket is wrong — agents "probe until a benign condition can be promoted to a root cause" rather than concluding nothing is wrong; ticket *wording* matters more than ticket *claims*; the three agents fail differently and at very different cost.
- **Does NOT cover:** no stated public code/data URL; not peer-reviewed.
- **Source retrieved:** https://arxiv.org/abs/2608.27021

---

**18. A Playground for Benchmarking Agentic AI in Network Management**
- **Authors:** Stefano Salsano, Andrea Mayer, Lorenzo Bracciale, Pierpaolo Loreti, Giuseppe Bianchi
- **Year:** 2026 (Crossref `issued` 2026-07)
- **Venue:** *2026 Mediterranean Artificial Intelligence and Networking Conference* (**IEEE MAIN 2026**)
- **DOI:** 10.1109/MAIN71116.2026.11622333 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** A playground/evaluation environment for agentic AI in network management (Salsano/Bianchi group, University of Rome Tor Vergata). Content details — models, metrics, artefact availability — are **UNVERIFIED** (IEEE Xplore blocks automated access; no open mirror found).
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=A+Playground+for+Benchmarking+Agentic+AI+in+Network+Management

---

**19. From Topology to Troubleshooting: Evaluating Multimodal Large Language Models on Network Management**
- **Authors:** Yongqing Zhu, Yoke Moon Wong, Huaqun Guo, Qi Cao
- **Year:** 2026 (Crossref `issued` 2026-05)
- **Venue:** *NOMS 2026 — 2026 IEEE Network Operations and Management Symposium*, pp. 1–6. Presented in the **AIMLOps 2026** workshop session (Rome, 18 May 2026).
- **DOI:** 10.1109/NOMS69089.2026.11668270 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** An evaluation study of **multimodal** LLMs on network management, spanning topology understanding through troubleshooting — one of very few evaluations testing MLLMs (diagram/topology image inputs) rather than text-only models. **This is the item that answers your explicit IEEE NOMS question.**
- **Does NOT cover:** models tested, metrics, public code/data **UNVERIFIED** (IEEE Xplore blocked; Crossref holds no abstract).
- **Source retrieved:** https://api.crossref.org/works/10.1109/NOMS69089.2026.11668270 ; program: https://aimlops.future-iot.org/

---

**20. DEMO: NetArena Adaptation for Next Waves of Network Benchmarks**
- **Authors:** Yajie Zhou, Francis Y. Yan, Kevin Hsieh, Zaoxing Liu
- **Year:** 2026 (Crossref `issued` 2026-08-11)
- **Venue:** *Proceedings of the ACM SIGCOMM 2026 Conference* (**SIGCOMM '26**), demo track, pp. 2210–2212
- **DOI:** 10.1145/3789240.3830284 — **Crossref-verified**
- **Status:** Peer-reviewed (demo)
- **What it does:** Demo-track extension of NetArena (item 2) showing adaptation to new classes of network benchmarks. Cite as the **ACM SIGCOMM-venue** reference for the NetArena line. A 2-page demo, not a new dataset.
- **Source retrieved:** https://api.crossref.org/works/10.1145/3789240.3830284

---

### Category 3 — Intent-based networking and intent translation

---

**21. IBNBench** — introduced in *"NetIntent: Leveraging Large Language Models for End-to-End Intent-Based SDN Automation"*
- **Authors:** Md. Kamrul Hossain, Walid Aljoby
- **Year:** 2025
- **Venue:** *IEEE Open Journal of the Communications Society* (**IEEE OJ-COMS**), vol. 6, pp. 10512–10541
- **DOI:** 10.1109/OJCOMS.2025.3642642 — **Crossref-verified** (also the "related DOI" on the arXiv record)
- **Status:** Peer-reviewed + arXiv preprint (arXiv:2507.14398)
- **What it does:** Introduces **IBNBench**, "a first-of-its-kind benchmarking suite comprising four novel datasets": **Intent2Flow-ODL, Intent2Flow-ONOS, FlowConflict-ODL, FlowConflict-ONOS**, designed to evaluate LLMs on **intent translation and conflict detection** inside the industry-grade SDN controllers **OpenDaylight** and **ONOS**. Reports the first comprehensive comparison of **33 open-source LLMs** on IBNBench and related datasets. The second contribution, **NetIntent**, automates the full IBN lifecycle (translation, activation, assurance) on both controllers.
- **Does NOT cover:** 5G/6G intent (3GPP intent-driven management, TMF intent APIs), SLA-level outcome scoring, or closed-loop execution against a live core. Public dataset URLs are **UNVERIFIED** (named but not linked in the abstract).
- **Source retrieved:** https://arxiv.org/abs/2507.14398

---

**22. INTA: Intent-Based Translation for Network Configuration with LLM Agents**
- **Authors:** Yunze Wei, Xiaohui Xie, Tianshuo Hu, Yiwei Zuo, Xinyi Chen, Kaiwen Chi, Yong Cui
- **Year:** 2025 (Crossref `issued` 2025-09-22)
- **Venue:** *2025 IEEE 33rd International Conference on Network Protocols* (**IEEE ICNP 2025**)
- **DOI:** 10.1109/ICNP65844.2025.11192391 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** Intent-to-configuration translation using LLM agents, from the same Tsinghua group as NetConfArena (item 3) and the NetConfBench IETF draft (item 4). Content details **UNVERIFIED** (IEEE Xplore blocked).
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=INTA+Intent-Based+Translation+for+Network+Configuration+with+LLM+Agents

---

**23. LLM-Powered Intent-Driven Configuration Generation for Multi-Vendor Networks**
- **Authors:** Jingyu Wang, Bo He, Jinyu Zhao, Yixin Xuan, Haifeng Sun, Qi Qi, Junzhe Liang, Zirui Zhuang, Jianxin Liao
- **Year:** 2026
- **Venue:** *IEEE Transactions on Network and Service Management* (**IEEE TNSM**)
- **DOI:** 10.1109/TNSM.2026.3675409 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** Multi-vendor intent-driven configuration generation. **This is the item that answers your explicit IEEE TNSM question** — but note it is a *method/system* paper with its own multi-vendor evaluation, **not** a reusable public benchmark with a leaderboard. Content details **UNVERIFIED**.
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=LLM-Powered+Intent-Driven+Configuration+Generation+for+Multi-Vendor+Networks

---

**24. ConfAgent: Towards Intelligent Network Configuration Via LLM Agent**
- **Authors:** Shaowei Li, Zhiwen Gan, Jinyao Liu, Chengxi Gao, Fuliang Li, Si Wu, Pengfei Hu, Feng Li
- **Year:** 2025 (Crossref `issued` 2025-07-02)
- **Venue:** *2025 IEEE/ACM 33rd International Symposium on Quality of Service* (**IEEE/ACM IWQoS 2025**)
- **DOI:** 10.1109/IWQoS65803.2025.11143333 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** An LLM-agent system for network configuration — **a system paper with its own evaluation, not a reusable benchmark.** Content details **UNVERIFIED**.
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=ConfAgent+Towards+Intelligent+Network+Configuration+Via+LLM+Agent

---

### Category 4 — Telecom-domain knowledge, standards (3GPP), and code

---

**25. TeleQnA: A Benchmark Dataset to Assess Large Language Models Telecommunications Knowledge**
- **Authors:** Ali Maatouk, Fadhel Ayed, Nicola Piovesan, Antonio De Domenico, Merouane Debbah, Zhi-Quan Luo
- **Year:** 2026 (Crossref `issued` 2026-03; *IEEE Network* vol. 40, no. 2, pp. 253–260). Preprint dates from October 2023.
- **Venue:** *IEEE Network* (magazine)
- **DOI:** 10.1109/MNET.2025.3576035 — **Crossref-verified**
- **Status:** Peer-reviewed + arXiv preprint (arXiv:2310.15051)
- **What it does:** The reference telecom-knowledge benchmark: **10,000 multiple-choice questions** on telecommunications standards, terminology and concepts, generated by an automated question-generation framework with human-in-the-loop quality checks, with subsets spanning 3GPP and other standards bodies. Evaluates GPT-3.5 and GPT-4 plus a human cohort of telecom professionals; finds models struggle on complex standards questions and that adding telecom context substantially improves accuracy. Data: https://github.com/netop-team/TeleQnA and https://huggingface.co/datasets/netop/TeleQnA
- **Does NOT cover:** network operations, configuration, tool use, closed-loop control, or any network-level outcome metric. **Knowledge, not operational capability.**
- **Sources retrieved:** https://api.crossref.org/works?query.bibliographic=TeleQnA ; https://genainet.committees.comsoc.org/four-datasets-released-for-large-generative-ai-in-telecom-research/

---

**26. LDOT — "Go Gentle Into the Final Dance: A Benchmark for Evaluating LLMs in Telecom"**
- **Authors:** Yushen Lin, Zhiguo Ding, Ruichen Zhang, Daniel K. C. So
- **Year:** 2026 (Crossref `issued` [[2026]]; University of Manchester page: published 1 Jan 2026)
- **Venue:** *IEEE Journal on Selected Areas in Communications* (**IEEE JSAC**), vol. 44, pp. 2365–2377
- **DOI:** 10.1109/JSAC.2025.3641905 — **Crossref-verified** (independently confirmed on both the Manchester and Khalifa University publication pages)
- **Status:** Peer-reviewed (accepted author manuscript available CC-BY at Manchester)
- **What it does:** Introduces **Last Dance of Telecommunications (LDOT)**, a benchmark suite spanning **conceptual telecom questions, mathematical and logical reasoning problems, and complex network optimization scenarios**, designed to stress high-level reasoning and domain-specific knowledge rather than recall. Evaluates SOTA closed- and open-source LLMs; finds general-purpose models are strong on basic telecom knowledge but struggle with reasoning-intensive wireless problems, and that **certain multi-step optimization and planning tasks remain unsolved even by the best models** — exposing gaps invisible in saturated benchmarks. Includes a failure analysis separating insufficient domain knowledge from inadequate reasoning. The LDOT dataset is described as available; a public URL was **not confirmed — UNVERIFIED**.
- **Why this matters for you:** **This is the one benchmark paper found in IEEE JSAC** — directly answering your venue question, and it is much more on-topic than the venue sweep initially suggested. It is still a *static reasoning/knowledge* benchmark, not closed-loop network management.
- **Sources retrieved:** https://api.crossref.org/works/10.1109/JSAC.2025.3641905 ; https://research.manchester.ac.uk/en/publications/go-gentle-into-the-final-dance-a-benchmark-for-evaluating-llms-in/ ; https://khazna.ku.ac.ae/en/publications/go-gentle-into-the-final-dance-a-benchmark-for-evaluating-llms-in/

---

**27. TSpec-LLM: An Open-source Dataset for LLM Understanding of 3GPP Specifications**
- **Authors:** Rasoul Nikbakht, Mohamed Benzaghta, Giovanni Geraci
- **Year:** 2024 (Crossref `issued` 2024-12-08)
- **Venue:** *2024 IEEE Globecom Workshops* (**GC Wkshps 2024**)
- **DOI:** 10.1109/GCWkshp64532.2024.11101012 — **Crossref-verified**
- **Status:** Peer-reviewed + arXiv preprint (arXiv:2406.01768)
- **What it does:** A corpus (not a leaderboard) comprising **all 3GPP documents from Release 8 to Release 19**, for pre-training and fine-tuning LLMs on standards text, with associated QA-style evaluation of 3GPP understanding. Data: https://huggingface.co/datasets/rasoul-nikbakht/TSpec-LLM
- **Does NOT cover:** network operations or configuration correctness.
- **Sources retrieved:** https://api.crossref.org/works?query.bibliographic=TSpec-LLM ; https://genainet.committees.comsoc.org/four-datasets-released-for-large-generative-ai-in-telecom-research/

---

**28. ORAN-Bench-13K: An Open Source Benchmark for Assessing LLMs in Open Radio Access Networks**
- **Authors:** Pranshav Gajjar, Vijay K. Shah
- **Year:** 2025 (Crossref `issued` 2025-01-10)
- **Venue:** *2025 IEEE 22nd Consumer Communications & Networking Conference* (**IEEE CCNC 2025**)
- **DOI:** 10.1109/CCNC54725.2025.10975994 — **Crossref-verified**
- **Status:** Peer-reviewed + arXiv preprint (arXiv:2407.06245)
- **What it does:** A ~13K-item benchmark for assessing LLMs on **Open RAN** — the most RAN-proximate domain-knowledge benchmark found. Static knowledge/QA style.
- **Does NOT cover:** closed-loop RAN control, xApp/rApp policy execution, or RAN KPI outcomes.
- **Sources retrieved:** https://api.crossref.org/works?query.bibliographic=ORAN-Bench-13K ; https://arxiv.org/search/?searchtype=all&query=ORAN-Bench-13K

---

**29. Tele-LLMs: A Series of Specialized Large Language Models for Telecommunications**
- **Authors:** Ali Maatouk, Kenny Chirino Ampudia, Rex Ying, Leandros Tassiulas
- **Year:** 2026 (Crossref `issued` per *IEEE Access*; arXiv v1 September 2024, last revised 5 May 2025)
- **Venue:** *IEEE Access*
- **DOI:** 10.1109/ACCESS.2026.3698683 — **Crossref-verified**
- **Status:** Peer-reviewed + arXiv preprint (**arXiv:2409.05314** — note this is the same record that also carries Tele-Data)
- **What it does:** A family of telecom-specialised LLMs (1B–8B) released with **Tele-Data** (~2.5 billion tokens of telecommunications material) and an evaluation suite covering telecom knowledge and reasoning. Primarily a **model + dataset** contribution with an associated evaluation protocol. Data: https://huggingface.co/datasets/AliMaatouk/Tele-Data
- **Does NOT cover:** no network-operations execution benchmark.
- **Sources retrieved:** https://api.crossref.org/works?query.bibliographic=Tele-LLMs ; https://arxiv.org/search/?searchtype=all&query=Tele-LLMs

---

**30. TelecomGPT: A Framework to Build Telecom-Specific Large Language Models**
- **Authors:** Hang Zou, Qiyang Zhao, Yu Tian, Lina Bariah, Faouzi Bader, Thierry Lestable, Merouane Debbah
- **Year:** 2025
- **Venue:** *IEEE Transactions on Machine Learning in Communications and Networking* (**IEEE TMLCN**)
- **DOI:** 10.1109/TMLCN.2025.3593184 — **Crossref-verified**
- **Status:** Peer-reviewed + arXiv preprint (**arXiv id not verified — UNVERIFIED**)
- **What it does:** A framework for building telecom-specific LLMs (continued pre-training, instruction tuning, multi-modal alignment), evaluated on telecom knowledge and standards tasks. A model/framework contribution, **not** an operations benchmark.
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=TelecomGPT+A+Framework+to+Build+Telecom-Specific+Large+Language+Models

---

**31. Mobile-LLaMA: Instruction Fine-Tuning Open-Source LLM for Network Analysis in 5G Networks**
- **Authors:** Khen Bo Kan, Hyunsu Mun, Guohong Cao, Youngseok Lee
- **Year:** 2024 (Crossref `issued` 2024-09)
- **Venue:** *IEEE Network* (magazine)
- **DOI:** 10.1109/MNET.2024.3421306 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** Instruction fine-tuning of an open-source LLM for **5G network analysis**, with an evaluation set drawn from 5G protocol/analysis material. The closest "5G + LLM" peer-reviewed item in IEEE Network, but it is a **fine-tuning + task-evaluation** paper, not a reusable closed-loop benchmark.
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=Mobile-LLaMA+Instruction+Fine-Tuning+Open-Source+LLM+for+Network+Analysis+in+5G+Networks

---

**32. 6G-Bench: An Open Benchmark for Semantic Communication and Network-Level Reasoning With Foundation Models in AI-Native 6G Networks**
- **Authors:** Mohamed Amine Ferrag, Abderrahmane Lakas, Mérouane Debbah
- **Year:** 2026
- **Venue:** *IEEE Open Journal of the Communications Society* (**IEEE OJ-COMS**) — **not a JSAC/TNSM/TMLCN paper**, which is itself notable
- **DOI:** 10.1109/OJCOMS.2026.3680457 — **Crossref-verified** + arXiv preprint (arXiv:2602.08675)
- **Status:** Peer-reviewed + arXiv preprint
- **What it does:** The most 6G-native benchmark found. Defines a taxonomy of **30 decision-making tasks (T1–T30)** extracted from **3GPP, IETF, ETSI, ITU-T, and O-RAN Alliance** standardisation activities, in five standardisation-aligned capability categories, including **AI-native networking and agentic control tasks**. From **113,475 scenarios** it generates a balanced pool of **10,000 very-hard multiple-choice questions** requiring multi-step quantitative reasoning under uncertainty and worst-case regret minimisation over multi-turn horizons; after automated filtering and expert human validation, **3,722 questions** form the high-confidence evaluation set. Evaluates **22 foundation models** (dense and MoE, short- and long-context up to 1M tokens, open-weight and proprietary). Metrics: **pass@1** (0.22–0.82) and **pass@5** robustness (0.20–0.91); intent and policy reasoning accuracy **0.87–0.89** for leading models. Data: https://github.com/maferrag/6G-Bench
- **⚠ Critical caveat:** despite the 6G framing, this is a **static multiple-choice benchmark**. It does **not** execute actions on a network, does **not** measure SLA/latency/throughput outcomes, and does **not** evaluate closed-loop control. Also note the arXiv title ("...with Foundation Models...") differs in capitalisation from the published title — cite the published version.
- **Sources retrieved:** https://arxiv.org/abs/2602.08675 ; https://api.crossref.org/works?query.bibliographic=6G-Bench+An+Open+Benchmark+for+Semantic+Communication+and+Network-Level+Reasoning

---

**33. SWE-Bench 5G: Benchmarking AI Coding Agents on Telecom Network Engineering Tasks**
- **Authors:** Jiao Chen, Jianhua Tang, Xiaotong Yang, Zuohong Lv
- **Year:** 2026 (29 Apr 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2604.26278 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2604.26278
- **What it does:** The first benchmark (per the authors) targeting whether AI coding agents can resolve **real-world bugs in 5G core network software**. Instances are collected from **three open-source 5G projects** and packaged as self-contained Docker environments with automated fail-to-pass tests, plus a dual test strategy for telecom runtime dependencies. For instances whose original issues reference **3GPP specification clauses**, concise specification-context documents enable controlled evaluation of whether domain knowledge improves agent performance. **Four LLMs** evaluated: all diagnose bugs at **>91 %** but resolve rates are only **10–30 %**; 3GPP excerpts improve resolve rates on specification-dependent bugs but gains on generic defensive checks are limited.
- **Does NOT cover:** this is **software engineering, not network management** — it does not measure network state, SLA, or configuration outcomes on a running core. Repository/public-data status **UNVERIFIED**.
- **Source retrieved:** https://arxiv.org/abs/2604.26278

---

**34. GSMA Open-Telco LLM Benchmarks (GSMA Foundry / Open Telco initiative)**
- **Authors:** GSMA Foundry — consortium/industry effort, no individual authors
- **Year:** 2025 (initiative; datasets and tooling actively updated into 2026)
- **Venue:** Industry benchmark initiative — **not a paper, not peer-reviewed**
- **DOI:** no DOI found
- **Status:** **Not peer-reviewed** (industry consortium benchmark)
- **What it does:** A community benchmark suite in which operators submit telecom use cases; it emphasises **domain knowledge, safety, and energy efficiency**. Public artefacts: **https://huggingface.co/datasets/GSMA/ot-lite**, **https://huggingface.co/datasets/GSMA/ot-full** (10K–100K rows; question-answering and text-classification; tagged telecom, 3GPP, 5G, benchmarks, evaluation), a leaderboard at **https://huggingface.co/datasets/GSMA/leaderboard**, and evaluation tooling at **https://github.com/gsma-labs/evals**. Per the NetConfBench IETF draft (item 4), this suite is "largely centered on knowledge- and analysis-oriented tasks," and alignment between the two efforts is stated as future work.
- **Why it matters:** this is the most important non-academic telecom-LLM benchmarking effort and should be cited in the survey even though it is not peer-reviewed. **gsma.com returned HTTP 403 to automated retrieval**, so the current task list and leaderboard composition are **UNVERIFIED** from the primary source.
- **Sources retrieved:** https://github.com/gsma-labs/evals ; https://huggingface.co/datasets/GSMA/ot-full ; https://huggingface.co/datasets/GSMA/ot-lite

---

### Category 5 — Wireless / RAN / optical / 5G–6G operations (agentic, closed-loop, safety)

---

**35. OperAID — "OperAID: Benchmarking LLM Agents for Autonomous Kubernetes Fault Remediation"**
- **Authors:** Ariel Góes de Castro, Konstantinos Vandikas, Simone Ferlin, Marco Chiesa, Christian Esteve Rothenberg
- **Year:** 2026 (Crossref `issued` 2026-06-29)
- **Venue:** *2026 IEEE 12th International Conference on Network Softwarization* (**IEEE NetSoft 2026**), pp. 1–6. *(The GitHub README's BibTeX cites "IEEE NetSoft Trust 6G-N Workshop"; Crossref records the main NetSoft 2026 conference. I report Crossref — verify which you cite.)*
- **DOI:** 10.1109/NetSoft70012.2026.11603505 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does — and why it is the single most important find for your survey question:** OperAID is an **open-source testbed for evaluating LLM agents as autonomous operators of 5G Core networks deployed on Kubernetes**, providing a closed loop: **Fault Injection → Agentic Diagnosis → Remediation → Execution-Based Verification**, using **Open5GS + UERANSIM** via the `openverso-charts` Helm charts on a KinD cluster. Three fault scenarios: **S1** NetworkPolicy blocking AMF→SMF SBI (port 7777); **S2** SMF referencing a non-existent ConfigMap → CrashLoopBackOff; **S3** UPF scaled to 0 replicas (no user plane). Full suite: **5 models × 2 conditions (tools / no-tools) × 3 scenarios × 30 runs = 900 experiments** (April 2026). Reported results: overall success **36.0 %**; with tools **70.7 %** vs without tools **7.1 %**; best model Qwen3.5-35B-A3B at **93.3 %** with tools; per-scenario S1 **16.0 %**, S2 **42.0 %**, S3 **49.3 %**; failure modes 68 % "no_remediation" and 31 % "wrong_diagnosis" when tools are unavailable. Metrics include success rate, cost (pricing.csv → per-run cost figures) and error breakdowns. Code: **https://github.com/EricssonResearch/operaid**
- **Does NOT cover:** the injected faults are **Kubernetes/infrastructure-level** (NetworkPolicy, ConfigMap, replica scaling) rather than 3GPP protocol-level (NAS, NGAP, PFCP, SBI semantics); no RAN; no slice/SLA KPI scoring; the 5G core is used as the *managed workload*, not as the *unit of evaluation*. **This distinction is the crux of your novelty claim.**
- **Sources retrieved:** https://api.crossref.org/works/10.1109/NetSoft70012.2026.11603505 ; https://github.com/EricssonResearch/operaid ; https://raw.githubusercontent.com/EricssonResearch/operaid/main/README.md

---

**36. 6GAgentGym / 6GAgentBench — "6GAgentGym: Tool Use, Data Synthesis, and Agentic Learning for Network Management"**
- **Authors:** Jiao Chen, Jianhua Tang, Xiaotong Yang, Zuohong Lv
- **Year:** 2026 (31 Mar 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2603.29656 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2603.29656
- **What it does:** The most complete **closed-loop 6G network management** agent environment found. It provides an interactive environment with **42 typed tools** whose effect classification distinguishes **read-only observation from state-mutating configuration**, backed by a learned **Experiment Model** calibrated on **NS-3** simulation data. **6G-Forge** bootstraps closed-loop training trajectories from NS-3 seeds via iterative Self-Instruct generation with execution verification against the Experiment Model. Supervised fine-tuning on the resulting corpus followed by RL with online closed-loop interaction lets an **8B open-source model match GPT-5's overall success rate on the accompanying 6GAgentBench**, with stronger long-horizon performance.
- **Does NOT cover:** evaluation is against a **learned Experiment Model calibrated on simulation**, not a live 5G/6G core or testbed; no SLA/KPI outcome scoring is described in the abstract; public artefact URL **UNVERIFIED**. Authors overlap with SWE-Bench 5G (item 33) — same group, two different benchmarks.
- **Source retrieved:** https://arxiv.org/abs/2603.29656

---

**37. NetInjectBench: Benchmarking Indirect Prompt Injection in Tool-Using Large Language Model Agents for Network Operations**
- **Authors:** Ruksat Khan Shayoni, Muhammad Faraz Shoaib, S M Asif Hossain, M. F. Mridha
- **Year:** 2026 (11 Jul 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2607.10490 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2607.10490 (cs.CR)
- **What it does:** A **130-scenario safety benchmark** for **indirect prompt injection in tool-using LLM agents for network operations**, motivated by the fact that tickets, alerts, logs, runbooks and ChatOps messages can carry injections. It separates untrusted artifact text, trusted policy metadata, and evaluation labels. Composition: **40 benign, 40 weak-attack, 40 strong-attack, 10 approved high-impact change** scenarios; each evaluated with **Qwen2.5-7B, Llama3.1-8B, Mistral-7B**. Across **240 attack instances**, naive execution produced an **82.50 % unsafe tool-action rate**. Defences: prompt-only safety **25.63 %**, Self-Reminder **21.67 %**, Spotlighting **18.33 %**, Two-Pass LLM Judge **10.00 %**; static allowlisting reached **5.00 %** but blocked **all** approved changes (**0.00 % usefulness**, 100 % overblocking); a metadata-aware policy gate achieved **0/240 unsafe actions** (95 % Wilson upper bound 1.58 %) while preserving **99.17 %** attack-scenario usefulness and **100 %** approved-change usefulness. Conclusion: network-operation agents need **execution-time authorization boundaries** alongside prompt-level hygiene.
- **Why it matters:** this is the **only benchmark found that directly measures the safety/security failure dimension for network-operations agents** — it fills much of gap 4 below, though it is not peer-reviewed and does not use a 5G/6G network.
- **Source retrieved:** https://arxiv.org/abs/2607.10490

---

**38. WirelessOptBench** — introduced in *"WirelessOpsAgent: A Benchmark and Agent Design for Action Assurance in Wireless Networks"*
- **Authors:** Zijian Lu, Yiping Zuo, Hao Xu, Weicong Chen, Xin He, Jiajia Guo, Shi Jin
- **Year:** 2026 (8 Aug 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2608.08277 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2608.08277
- **What it does:** A benchmark for **action assurance** in wireless operations, built on the insight that "a task answer that is correct at proposal time can still be unsafe at execution time if supporting telemetry is stale or inconsistent." It turns wireless tasks into **execution-state decision episodes with controlled telemetry faults and action constraints**, testing whether an agent verifies that a proposed action is still supported by current evidence. Metrics: **Exact Action Accuracy** and **Unsafe APPLY Rate**. Across three backbone evaluations of **600 episodes each**, the proposed WirelessOpsAgent reaches up to **0.983 Exact Action Accuracy** and cuts the Unsafe APPLY Rate on Claude Sonnet 4.6 from **82.2 % to 10.3 %** versus the safest baseline. Artifact (anonymous during review): https://anonymous.4open.science/r/wirelessopsbench-artifact-D969/
- **Source retrieved:** https://arxiv.org/abs/2608.08277

---

**39. α³-Bench: A Unified Benchmark of Safety, Robustness, and Efficiency for LLM-Based UAV Agents over 6G Networks**
- **Authors:** Mohamed Amine Ferrag, Abderrahmane Lakas, Merouane Debbah
- **Year:** 2026 (1 Jan 2026)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2601.03281 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2601.03281 (eess.SY), 20 pages
- **What it does:** Frames each UAV mission as a language-mediated control loop between an LLM agent and a human operator, where decisions must satisfy strict schema validity, mission policies, speaker alternation and safety constraints while adapting to **fluctuating network slices, latency, jitter, packet loss, throughput, and edge load**. Supports both **tool calls and agent-to-agent coordination**, enabling evaluation of tool-use consistency and multi-agent interaction. Corpus: **113k conversational UAV episodes** grounded in UAVBench scenarios; **17 state-of-the-art LLMs** evaluated on a fixed **50-episode subset per scenario** under deterministic decoding. Proposes a composite **α³ metric unifying six pillars: Task Outcome, Safety Policy, Tool Consistency, Interaction Quality, Network Robustness, and Communication Cost**, with efficiency normalised **per second and per thousand tokens**. Data: https://github.com/maferrag/AlphaBench
- **Why it matters:** **this is the single best existing template for the cost/latency/safety dimensions you want in a 5G/6G benchmark** — but it targets UAV autonomy over 6G links, not 5G/6G network management.
- **Source retrieved:** https://arxiv.org/abs/2601.03281

---

**40. AgentPN Loop: Benchmarking AI Agents for Private 5G/6G Network Management**
- **Authors:** Onur Sahin, Vanlin Sathya, Lyutianyang Zhang, Kalpana Naidu
- **Year:** 2026
- **Venue:** No venue found — SSRN working paper (Elsevier BV), type `posted-content`. **PREPRINT.**
- **DOI:** 10.2139/ssrn.7411918 — **Crossref-verified (metadata only)**
- **Status:** **PREPRINT** — SSRN working paper, **not peer-reviewed**
- **What it does:** **The only item found whose title explicitly targets AI agents for *private 5G/6G network management*.** However: (i) no peer-reviewed venue found; (ii) **ssrn.com returned HTTP 403 "Content Blocked"**, so abstract, task list, models tested, metrics and data availability are **entirely UNVERIFIED**; (iii) no public code or dataset repository was found.
- **⚑ Action for the survey: retrieve the SSRN PDF manually through an institutional login and read it before making any claim about it.** Do not describe its contents in print until you have done so.
- **Sources retrieved:** https://api.crossref.org/works/10.2139/ssrn.7411918 (metadata); full text blocked at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7411918

---

**41. AutoONBench: a benchmark for large language model agents in autonomous optical networks**
- **Authors:** Yihao Zhang, Qizhi Qiu, Jiaping Wu, Xiaomin Liu, Weisheng Hu, Qunbi Zhuge
- **Year:** 2026 (Crossref `issued` 2026-03-27)
- **Venue:** *Journal of Optical Communications and Networking* (**JOCN**), Optica Publishing Group
- **DOI:** 10.1364/JOCN.589201 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** An agent benchmark for **autonomous optical networks** — evidence that the benchmark idea reached the optical transport community before the 5G/6G core community. Content details beyond title/authors/venue/DOI are **UNVERIFIED**.
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=AutoONBench+a+benchmark+for+large+language+model+agents+in+autonomous+optical+networks

---

**42. A YANG-Grounded LLM Agent Supporting Multi-Vendor OpenROADM Optical Transport Networks**
- **Authors:** Linqi Xiao, Aparaajitha Gomathinayakam Latha, Venkateswarlu Gudepu, Andrea Fumagalli
- **Year:** 2026 (Crossref `issued` 2026-08-11)
- **Venue:** *Proceedings of the ACM SIGCOMM 2026 Conference* (**SIGCOMM '26**)
- **DOI:** 10.1145/3789240.3822606 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** A YANG-model-grounded LLM agent for multi-vendor OpenROADM optical transport, evaluated on a simulated network of **5 Lightynode containers** (3 ROADM OpenROADM v2.2.1 and 2 TPDR OpenROADM v7.1). An **agent-system paper with a testbed evaluation**, not a reusable public benchmark — but a notable SIGCOMM 2026 data point for YANG-grounded, emulator-executed agent evaluation. Related: **CORA: a conversational AI-agent for intelligent automation of OpenROADM multi-vendor optical transport networks**, DOI 10.1117/12.3113861, *Applications of Machine Learning 2026* (SPIE).
- **Source retrieved:** https://api.crossref.org/works?query.bibliographic=A+YANG-Grounded+LLM+Agent+Supporting+Multi-Vendor+OpenROADM+Optical+Transport+Networks

---

**43. Small Models, Big Impact: Tool-Augmented AI Agents for Wireless Network Planning**
- **Authors:** Yongqiang Zhang, Mustafa A. Kishk, Mohamed-Slim Alouini
- **Year:** 2026 (Crossref `issued` 2026-04)
- **Venue:** *IEEE Communications Magazine*, vol. 64, no. 4, pp. 26–32
- **DOI:** 10.1109/MCOM.001.2500402 — **Crossref-verified**
- **Status:** Peer-reviewed (magazine)
- **What it does:** Evaluates a **tool-augmented AI agent** built on **small/medium language models** (not frontier LLMs) applied to **wireless network planning**, arguing that small models plus tools beat large models on the cost/performance tradeoff for this task. **This is the item that answers your IEEE Communications Magazine question, and it is the closest thing found to a "network planning + tool-use + cost" evaluation.** It is a system + evaluation article, **not** a released public benchmark/dataset; metrics, baselines and artefact availability are **UNVERIFIED** (no Crossref abstract; IEEE Xplore blocked).
- **Sources retrieved:** https://api.crossref.org/works/10.1109/MCOM.001.2500402 ; https://ui.adsabs.harvard.edu/abs/2026IComM..64d..26Z/abstract

---

**44. Revisiting Multi-Level Network Modeling and Simulation With Domain-Adapted LLMs**
- **Authors:** Dongming Wu, Jiewen Liu, Xingqin Lin, Dongkuan Xu, Peng Gao, Yuchen Liu
- **Year:** 2026
- **Venue:** *IEEE Transactions on Network Science and Engineering* (**IEEE TNSE**), vol. 13, pp. 10408–10424
- **DOI:** 10.1109/TNSE.2026.3708012 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** Uses **domain-adapted LLMs to revisit multi-level network modeling and simulation** — i.e. LLMs as the modelling/simulation engine rather than as management agents. It is **not** an agent benchmark; included as an evaluation-of-LLM-capability paper in a target journal. Metrics, datasets and artefact URLs **UNVERIFIED**.
- **Source retrieved:** https://api.crossref.org/works/10.1109/TNSE.2026.3708012

---

### Category 6 — ADJACENT: IT/cloud/DevOps operations benchmarks

> **Framing note.** These are **not** network-management benchmarks; they target cloud-native/microservice/IT-automation operations. They are included because reviewers will ask, because they are the most methodologically mature executable agent benchmarks in the operations space, and because the network benchmarks above explicitly position against them (NetArena compares to AIOpsLab; NetConfBench compares to operator use cases).

---

**45. ITBench**
- **Authors (DSN-S record):** Jackson Clark, Rohan Arora, Saurabh Jha. The ICML 2025 record lists a larger author set — **UNVERIFIED here**.
- **Year:** 2025
- **Venue:** (i) *2025 55th Annual IEEE/IFIP International Conference on Dependable Systems and Networks — Supplemental Volume* (**IEEE/IFIP DSN-S 2025**), DOI **10.1109/DSN-S65789.2025.00060** (Crossref-verified; title on this record: *"Benchmarking AI Agents for IT Automation Tasks with ITBench"*); (ii) **ICML 2025** oral, listed as *"ITBench: Evaluating AI Agents across Diverse Real-World IT Automation Tasks."*
- **DOI:** 10.1109/DSN-S65789.2025.00060. **No DOI found for the ICML record.**
- **Status:** Peer-reviewed (both venues)
- **What it does:** A benchmark of real-world IT automation tasks for AI agents — the industry-standard reference for "can agents actually run IT operations." Task/scenario counts and metrics **UNVERIFIED** (IEEE Xplore blocked; IBM page lists the paper only).
- **Sources retrieved:** https://api.crossref.org/works/10.1109/DSN-S65789.2025.00060 ; https://icml.cc/virtual/2025/oral/47199 ; https://research.ibm.com/publications/itbench-evaluating-ai-agents-across-diverse-real-world-it-automation-tasks

---

**46. AIOpsLab**
- **Authors (FSE Companion record):** Minghua Ma, Jackson Clark, Shenglin Zhang. The original arXiv paper (arXiv:2501.06706) lists a larger Microsoft Research / academic author set — **UNVERIFIED here**.
- **Year:** 2025 (Crossref `issued` 2025-06-23)
- **Venue:** *Proceedings of the 33rd ACM International Conference on the Foundations of Software Engineering* (**FSE Companion '25**), ACM (record title: *"AIOpsLab in Action: An Open Platform for AIOps Research"*)
- **DOI:** 10.1145/3696630.3728619 — **Crossref-verified**
- **Status:** Peer-reviewed (companion) + arXiv preprint
- **What it does:** An open platform for designing, developing and evaluating **AIOps agents** — fault injection, telemetry and agent orchestration for cloud systems. The de-facto substrate for cloud-operations agent evaluation. **Does not cover L2/L3, RAN or core network management.**
- **Source retrieved:** https://api.crossref.org/works/10.1145/3696630.3728619

---

**47. RCAEval: A Benchmark for Root Cause Analysis of Microservice Systems with Telemetry Data**
- **Authors:** Luan Pham, Hongyu Zhang, Huong Ha, Flora Salim, Xiuzhen Zhang
- **Year:** 2025 (Crossref `issued` 2025-05-08)
- **Venue:** *Companion Proceedings of the ACM on Web Conference 2025* (**WWW '25 Companion**), ACM
- **DOI:** 10.1145/3701716.3715290 — **Crossref-verified**
- **Status:** Peer-reviewed (companion)
- **What it does:** A benchmark for RCA on microservice systems using telemetry data (metrics, traces, logs), with standardised datasets and evaluation for RCA methods including LLM-based ones. Cloud microservices, not network fault diagnosis — but its evaluation methodology (localisation accuracy against injected ground truth) is the closest methodological analogue to NIKA/FaulT-Bench.
- **Source retrieved:** https://api.crossref.org/works/10.1145/3701716.3715290

---

**48. SREGym: A Live Training Ground for AI SRE Agents with High-Fidelity Failure Drills**
- **Authors:** Jackson Clark, Yiming Su, Saad Mohammad Rafid Pial, Lily Gniedziejko, Tianyin Xu
- **Year:** 2026 (Crossref `issued` 2026-05-26)
- **Venue:** *Proceedings of the ACM Conference on AI and Agentic Systems* (**CAIS '26**), pp. 1253–1258
- **DOI:** 10.1145/3786335.3813208 — **Crossref-verified**
- **Status:** Peer-reviewed
- **What it does:** A **live** training/evaluation ground for AI SRE agents with high-fidelity failure drills. Adjacent to network management (SRE/cloud), but methodologically notable because it is a *live* environment rather than a static dataset.
- **Source retrieved:** https://api.crossref.org/works/10.1145/3786335.3813208

---

**49. ORCA-bench: How Ready Are Language Model Agents for Oncall?**
- **Authors:** Albert Gong, Kyuseong Choi, Abhineet Agarwal, Jason Schechner, Ryan Huang, Raj Agrawal, Anish Agarwal, Raaz Dwivedi
- **Year:** 2026 (v1 30 Jul; v2 5 Aug)
- **Venue:** No venue found — **PREPRINT**
- **DOI:** 10.48550/arXiv.2607.28545 (arXiv-issued). **No publisher DOI found.**
- **Status:** **PREPRINT** — arXiv:2607.28545 (cs.CL)
- **What it does:** A **production-fidelity oncall RCA benchmark**. Pairs a **live OpenTelemetry-instrumented microservice system** — exposing **six days** of metrics, logs and traces through real telemetry interfaces (**Prometheus, Jaeger, OpenSearch via Grafana**) plus full source-code access — with **1,079 RCA tasks** that systematically vary **report specificity, time-to-detection, and co-occurring fault scenarios**. Ground-truth symptoms are curated and signed off by expert SREs; the LLM-as-judge is independently re-scored by humans (**Cohen's κ_w = 0.90**). Across **five frontier agents**, best RCA Accuracy is **25.3 %** on Medium and **10.0 %** on Hard. The weakest model **hallucinates an implausible root cause in 40 % of incident reports**; removing source-code access degrades every metric. Public set: https://hub.harborframework.com/datasets/orca-bench/orca-bench
- **Why it matters:** this is the **strongest existing example of (i) a live-telemetry benchmark, (ii) explicit hallucination measurement, and (iii) human-validated LLM-judge reliability** in the operations space — all three are things your 5G/6G benchmark should replicate. It is cloud microservices, not networking.
- **Source retrieved:** https://arxiv.org/abs/2607.28545

---

**50. NetBench: A Large-Scale and Comprehensive Network Traffic Benchmark Dataset for Foundation Models**
- **Authors:** Chen Qian, Xiaochang Li, Qineng Wang, Gang Zhou, Huajie Shao
- **Year:** 2024 (Crossref `issued` 2024-05-13)
- **Venue:** *2024 IEEE International Workshop on Foundation Models for Cyber-Physical Systems & Internet of Things* (**FMSys 2024**), pp. 20–25
- **DOI:** 10.1109/FMSys62467.2024.00008 — **Crossref-verified**
- **Status:** Peer-reviewed (workshop) + arXiv preprint (arXiv:2403.10319)
- **What it does:** A large-scale **network traffic** benchmark dataset for foundation models, aimed at traffic classification rather than LLM/agent network management. Included because it is frequently surfaced by "network benchmark" searches and is sometimes confused with NetConfBench/NetArena. Public dataset: https://huggingface.co/datasets/NetoAISolutions/NetBench (gated).
- **Source retrieved:** https://api.crossref.org/works/10.1109/FMSys62467.2024.00008

---

### Other relevant items found (not benchmarks)

- **LMTE — "Putting the 'Reasoning' into WAN Traffic Engineering with Language Models"** — stated in its own text to be **accepted at IEEE INFOCOM 2026**; **arXiv:2602.00941** (PREPRINT on arXiv). A *method* paper for WAN traffic engineering, not a benchmark. **This is the nearest INFOCOM hit found** — relevant because it is the closest thing to LLM-based traffic engineering, and because your survey's "no INFOCOM benchmark found" claim should be qualified by it. *(Venue claim from the paper's own text via a search snippet — **UNVERIFIED**; confirm on IEEE Xplore.)*
- **NeMoCopilot** (33 tasks) and **AI4OpsLab** (48 tasks) — cited in NetArena's comparison table as prior network-admin/DevOps benchmarks. **Bibliographic details not verified — UNVERIFIED.**
- **TelcoLM**, **Tele-Data**, **MAESTRO** (LLM-driven intent-based 6G automation, DOI 10.1109/LNET.2024.3503292, IEEE Networking Letters) — related telecom-LLM works surfaced during the sweep that are *models/frameworks*, not benchmarks.

---

## (b) Gaps in the benchmark landscape

These are the dimensions **not** jointly covered by any benchmark found. This section is the core of your "no benchmark exists" argument.

**1. No closed-loop execution against a real or emulated 5G core / RAN at the 3GPP protocol level.**
The executable closed-loop benchmarks split into two groups, neither of which is 5G/6G network management:
- *IP/enterprise/datacentre/Kubernetes:* NetArena, NetConfArena, NetConfBench, NetLLMBench, Cornetto, NIKA, FaulT-Bench, OperAID, SREGym, ORCA-bench.
- *5G/6G-adjacent but not protocol-level:* **OperAID** (a 5G core used as a Kubernetes workload, with Kubernetes-level faults), **6GAgentGym** (a learned Experiment Model calibrated on NS-3 simulation, not a live core or testbed), **SWE-Bench 5G** (5G core *source-code* bug repair), **α³-Bench** (UAV agents over 6G links).

**No peer-reviewed benchmark was found that executes an LLM/agent action against 5G core network functions (AMF/SMF/UPF/NRF), a RAN (near-RT/non-RT RIC, xApp/rApp), or a network slice at the protocol level (NAS, NGAP, PFCP, SBI, E2/OTA) and scores the resulting network behaviour.** 6GAgentGym comes closest and is a preprint evaluated against a surrogate model.

**2. No SLA-level outcome metrics anywhere in network management.**
NetArena measures correctness, safety and latency **of the agent's actions**, not of the **service**. WirelessOptBench measures action safety against telemetry. α³-Bench measures network robustness and communication cost, but for UAV missions over 6G links. OperAID measures remediation success and cost, not service KPIs. **No benchmark found scores SLA satisfaction, slice-KPI attainment, per-flow latency/jitter, throughput, availability or QoE as the primary outcome of network-management agent actions.**

**3. Cost, latency and token economics are secondary or absent.**
NetConfBench (IETF draft) makes time and token cost **optional** efficiency metrics; FaulT-Bench notes agents fail "at very different cost" without making cost a first-class axis; NIKA, NetConfEval, Cornetto and 6G-Bench do not report token/cost metrics; OperAID does report per-run cost. **α³-Bench is the only benchmark found with a fully normalised per-second and per-1k-token efficiency pillar.** There is no benchmark reporting **cost-per-remediated-incident** or **latency-to-recovery** at scale for network management.

**4. Safety, robustness and hallucination are only beginning to be measured — and never for 5G/6G.**
- **NetArena** decouples step-wise safety from final correctness.
- **WirelessOptBench** measures Unsafe APPLY Rate under telemetry faults.
- **α³-Bench** has a Safety Policy pillar.
- **NetInjectBench** measures indirect prompt injection and unsafe tool actions in network operations (82.5 % naive unsafe rate).
- **FaulT-Bench** measures false-premise handling — the closest proxy for hallucination under misleading input.
- **ORCA-bench** explicitly measures hallucinated root causes (40 % of reports for the weakest model).

**No benchmark found measures hallucination rate for network-management agents against a network-state ground truth, and none evaluates the consequence of a wrong action on a live/emulated 5G core** (session drops, slice-isolation breach, signalling storms, lawful-intercept or charging corruption).

**5. Multi-domain / cross-domain orchestration is absent.**
NetArena's own limitations concede "coverage of complex scenarios like cross-domain routing remains limited." Nothing found covers orchestration across RAN + transport + core + edge/cloud, nor cross-operator or end-to-end multi-vendor service management. dsm2cli covers multi-vendor CLI translation, but at command level, not orchestration level.

**6. Resource allocation, scheduling and traffic engineering for 5G/6G are not benchmarked as agent tasks.**
NetArena includes a datacentre capacity-planning task. Nothing found covers RAN scheduling decisions, spectrum/resource-block allocation, MEC placement, network-slicing admission, or multipath/QoS-flow scheduling as LLM-agent tasks with measurable network outcomes. LMTE (INFOCOM 2026, method paper) is the nearest traffic-engineering work and is not a benchmark.

**7. Statistical reliability and contamination resistance are recent concerns, not established practice.**
Only NetArena explicitly addresses statistical power and pretraining contamination (dynamic generation; CI overlap 85 % → 0). NetConfArena and NetAgentBench adopt dynamic/FSM-generated tasks; **Continual Benchmarking** (SIGCOMM '25 poster) is the position paper. Most others — TeleQnA, TSpec-LLM, ORAN-Bench-13K, 6G-Bench, LDOT, NetConfEval — are **static and therefore contamination-prone**. Any new 5G/6G benchmark must be dynamically generated to be credible in 2026.

**8. Process-quality and reasoning-trace evaluation is inconsistent and unvalidated.**
NetConfBench uses ROUGE/cosine similarity against ground-truth reasoning traces (a weak proxy and a documented limitation of that draft); FaulT-Bench uses an LLM judge on outcome, fix and reasoning quality; NIKA releases full trajectories; ORCA-bench is the only work found that reports **human re-scoring of its LLM judge (κ_w = 0.90)**. **No benchmark reports inter-judge reliability for network-specific grading at all**, and there is no agreed metric for reasoning quality in network operations.

**9. Industry/academic fragmentation.**
The GSMA Open-Telco LLM Benchmarks (operator-submitted; knowledge/safety/energy-oriented) and the academic executable benchmarks (configuration/troubleshooting-oriented) are explicitly described as complementary in the NetConfBench IETF draft, with alignment listed as **future work**. **No benchmark bridges operator use cases to executable 5G/6G network outcomes.**

**10. The most relevant work is unpublished.**
Of the 50 items above, the following are **PREPRINT only**: NetConfArena, Cornetto, Evaluating Agentic Configuration Repair, NetAgentBench, dsm2cli (full paper), NetLLMeval, NIKA (paper), FaulT-Bench, SWE-Bench 5G, 6GAgentGym, NetInjectBench, WirelessOptBench, α³-Bench, ORCA-bench, AgentPN Loop. **NetConfBench is an IETF Internet-Draft with explicitly "no formal standing."** Several of the most on-topic 5G/6G items (6GAgentGym, AgentPN Loop) are unrefereed. **This is itself a defensible finding** — and it means the peer-reviewed record lags the state of the art by roughly 12–18 months in this subfield.

---

## (c) Public code and public datasets

### Both code and dataset public (URLs verified by retrieval)
| Benchmark | Code | Dataset |
|---|---|---|
| **OperAID** | https://github.com/EricssonResearch/operaid | scenarios + Open5GS/UERANSIM Helm charts inside the repo |
| NetConfEval | https://github.com/RedHatResearch/conext24-NetConfEval | https://huggingface.co/datasets/NetConfEval/NetConfEval |
| NetArena | https://github.com/Froot-NetSys/NetArena ; https://github.com/Froot-NetSys/netarena_leaderboard ; project page http://www.netarena.ai/ | generated at runtime (dynamic by design) |
| **NetConfArena** | **https://github.com/liujona/NetConfArena** | in repo (contents not inspected) |
| NIKA | https://github.com/sands-lab/nika | https://zenodo.org/records/17971675 (DOI 10.5281/zenodo.17971675, CC-BY-4.0, 15.1 MB) |
| 6GAgentGym | not confirmed — **UNVERIFIED** | 6GAgentBench; URL **UNVERIFIED** |
| TeleQnA | https://github.com/netop-team/TeleQnA (+ https://github.com/Ali-maatouk/Tele-LLMs for Tele-LLMs) | https://huggingface.co/datasets/netop/TeleQnA |
| TSpec-LLM | — | https://huggingface.co/datasets/rasoul-nikbakht/TSpec-LLM |
| Tele-LLMs / Tele-Data / Tele-Eval | https://github.com/Ali-maatouk/Tele-LLMs | https://huggingface.co/datasets/AliMaatouk/Tele-Data |
| ORAN-Bench-13K / ORANSight-2.0 | https://github.com/prnshv/ORAN-Bench-13K | https://huggingface.co/datasets/qubol/ORANBench |
| 6G-Bench | https://github.com/maferrag/6G-Bench | same repo |
| α³-Bench | https://github.com/maferrag/AlphaBench | same repo |
| Mobile-LLaMA | https://github.com/DNLab2024/Mobile-LLaMA | in repo |
| GSMA Open-Telco LLM Benchmarks | https://github.com/gsma-labs/evals | https://huggingface.co/datasets/GSMA/ot-lite ; https://huggingface.co/datasets/GSMA/ot-full ; leaderboard https://huggingface.co/datasets/GSMA/leaderboard |
| NetConfBench (IETF draft) | https://github.com/nobrowning/draft_llm_conf_benchmark | 40-task dataset described; publication status **UNVERIFIED** |
| WirelessOptBench | https://anonymous.4open.science/r/wirelessopsbench-artifact-D969/ (anonymous, under review) | same |
| ORCA-bench | — | https://hub.harborframework.com/datasets/orca-bench/orca-bench |
| ITBench | https://github.com/itbench-hub/ITBench | in repo |
| AIOpsLab | https://github.com/microsoft/AIOpsLab | in repo |
| RCAEval | https://github.com/phamquiluan/RCAEval (+ PyPI `RCAEval`) | in repo |
| OpenRCA | https://github.com/microsoft/OpenRCA | in repo |
| SREGym | https://github.com/SREGym/SREGym | in repo |

### Released but no URL confirmed from the retrieved page — treat as UNVERIFIED
- **NetLLMeval / Toward Agentic SysAdmin** — abstract says "released open-source", no URL given.
- **SWE-Bench 5G** — Docker-packaged instances from three open-source 5G projects; repo URL not on the abstract page.
- **IBNBench** — four named datasets (Intent2Flow-ODL/ONOS, FlowConflict-ODL/ONOS); no URL in the abstract.
- **LDOT (JSAC 2026)** — abstract says "The LDOT dataset … aim[s] to facilitate…", no URL confirmed. **Worth an author email.**
- **NetLLMBench** — TUM accepted manuscript exists at https://mediatum.ub.tum.de/download/1759791/1759791.pdf (PDF not machine-readable here).
- **AutoONBench, OperAID's peer-reviewed record, A Playground for Benchmarking Agentic AI (MAIN 2026), INTA, LLM-Powered Intent-Driven Config Generation, ConfAgent** — public release not confirmed; full texts not retrievable.
- **Cornetto / Evaluating Agentic Configuration Repair** — no repo stated; the ETH Research Collection handle https://www.research-collection.ethz.ch/handle/20.500.11850/799709 holds the *paper*, not data.

### Not public / not applicable
- **AgentPN Loop** — no repository found; full text inaccessible.
- **TelecomGPT**, **Mobile-LLaMA** — weights/data release not confirmed.
- **NetBench (FMSys 2024)** — dataset at https://huggingface.co/datasets/NetoAISolutions/NetBench but **gated**.

---

## (d) Caution note — what could NOT be verified

Read this before citing anything above.

1. **IEEE Xplore blocks automated retrieval** (HTTP 202/403), as do ACM DL (Cloudflare), Springer, GSMA.com (403) and SSRN (403 "Content Blocked"). For every IEEE/ACM item, DOI/venue/year/authors/pages come from the **Crossref REST API** — authoritative for bibliographic metadata, silent on content. The following have **UNVERIFIED** model lists, metrics, dataset sizes and code availability: **INTA (ICNP 2025), LLM-Powered Intent-Driven Configuration Generation (TNSM 2026), ConfAgent (IWQoS 2025), A Playground for Benchmarking Agentic AI (MAIN 2026), From Topology to Troubleshooting (NOMS 2026), Small Models Big Impact (ComMag 2026), Revisiting Multi-Level Network Modeling (TNSE 2026), AutoONBench (JOCN), NetLLMBench (NFV-SDN 2024), ITBench (ICML 2025 record), LDOT (JSAC 2026 — abstract retrieved, dataset URL not).** Retrieve these manually through an institutional subscription.

2. **AgentPN Loop is the most on-topic item and the least verified.** SSRN returned HTTP 403. Its abstract, task list, model coverage, metrics and data availability are entirely unknown to me; only its title/authors/year/DOI are Crossref-verified. **Do not describe its contents in print until you have read the PDF.**

3. **Venue for "Evaluating Agentic Configuration Repair for Computer Networks" is unknown.** ETH NSG labels it "Workshop Paper" without naming the workshop; arXiv lists it only under cs.AI.

4. **OperAID's venue has two conflicting statements.** Crossref: *2026 IEEE 12th International Conference on Network Softwarization (NetSoft 2026)*, pp. 1–6. The GitHub README BibTeX: *"IEEE NetSoft Trust 6G-N Workshop."* I report Crossref. **Resolve before citing.**

5. **Author-name discrepancy.** SADE's fifth author is **"Kosta Dakic"** in Crossref (IEEE LCN 2026) and **"Kosta Dekic"** in the arXiv v1 listing.

6. **The "NeMoEval" name is unverified.** It appears in indexed snippets but **not** in the retrieved arXiv abstract of *Enhancing Network Management Using Code Generated by Large Language Models* (arXiv:2308.06261). Cite the paper title, not the benchmark name, unless you confirm it in the full text.

7. **Publication-year ambiguity is widespread and will bite you.** TeleQnA: Crossref year 2026 (*IEEE Network*), arXiv October 2023 — widely cited as 2023/2024. Tele-LLMs: Crossref year 2026 (*IEEE Access*), arXiv v1 September 2024. LDOT: Crossref 2026 (*IEEE JSAC*), DOI string contains "2025". **Cite the published venue/year, but expect reviewers to know the preprint year.**

8. **LDOT (JSAC) was found late and only via a non-obvious query.** It is the single most important item for your venue question. I verified its DOI, authors, journal, volume and pages from Crossref **and** two independent university repositories, but I have not read the full paper, so the LDOT task list and dataset URL remain UNVERIFIED. **Read this paper — it is the strongest "JSAC already published a telecom LLM benchmark" counter-argument you will face.**

9. **Search coverage limits — the negative claims are the weakest part of this report.** Discovery relied on web search plus Crossref. **A claim of the form "no benchmark exists in venue X" is not supported by this method.** Phrase such claims as "**no benchmark was found in our search**, which covered [list the queries and venues]." For a defensible negative claim, additionally search Scopus and Web of Science, and read the proceedings tables of contents directly for: IEEE NOMS/CNSM/IM 2024–2026, IEEE INFOCOM main + workshops 2024–2026, ACM CoNEXT 2023–2026, ACM SIGCOMM 2023–2026, USENIX NSDI 2024–2026, ACM IMC 2024–2026, IEEE TNSM/JSAC/ComMag/Network 2024–2026. One sub-sweep enumerated the **full CNSM 2025 technical program** and found only systems papers (no benchmarks) — that is the level of evidence needed for each negative claim.

10. **Citation chaining is incomplete.** The OpenAlex citation-expansion endpoint returned HTTP 429 when listing NetConfEval's 89 citing works, and the Semantic Scholar API was rate-limited throughout. Only targeted chaining was completed. **A systematic forward-citation sweep of NetConfEval, TeleQnA, NIKA, NetArena, TSpec-LLM and ORAN-Bench-13K in Scopus/Web of Science is still needed** and is likely to surface additional 2026 benchmark papers — this literature is moving faster than indexing.

11. **No field above is inferred.** Every DOI, venue, year and author list was read from Crossref, arXiv, Zenodo, OpenReview/ICLR, Hugging Face, GitHub or a publisher page. Where a field could not be read it is marked "no DOI found" or "UNVERIFIED" rather than guessed.

---

## (e) Additional verified items found in the second-pass sweep

These were confirmed via Crossref by DOI after the main report was drafted, and are grouped separately so you can see exactly what is Crossref-verified.

**Telecom / wireless knowledge and reasoning (additions to Category 4)**
- **TeleMath: A Benchmark for Large Language Models in Telecom Mathematical Problem Solving** — *IEEE Network*, 2026 — **DOI 10.1109/MNET.2026.3658826** (Crossref-verified). Author list **not retrieved — UNVERIFIED**. Telecom mathematical reasoning benchmark; complements LDOT and 6G-Bench in the "quantitative reasoning" niche.
- **TeleCom-Bench: How Far Are Large Language Models from Industrial Telecommunication Applications?** — *Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2* (**KDD '26**), 2026 — **DOI 10.1145/3770855.3817480** (Crossref-verified). Authors **not retrieved — UNVERIFIED**. Industrial-telecom application benchmark; the first KDD-venue item found in this space.
- **WirelessMathBench: A Mathematical Modeling Benchmark for LLMs in Wireless Communications** — *Findings of the Association for Computational Linguistics: ACL 2025*, 2025 — **DOI 10.18653/v1/2025.findings-acl.573** (Crossref-verified). Authors **not retrieved — UNVERIFIED**. An NLP-venue (ACL Findings) wireless benchmark — useful evidence that this topic is crossing into MLSys/NLP venues.
- **ORANSight-2.0: Foundational LLMs for O-RAN** — Pranshav Gajjar, Vijay K. Shah — *IEEE Transactions on Machine Learning in Communications and Networking* (**IEEE TMLCN**), vol. 3, pp. 903–920, 2025 — **DOI 10.1109/TMLCN.2025.3592658** (Crossref-verified). The **TMLCN-venue** successor to ORAN-Bench-13K (item 28). It is a model + evaluation contribution (arXiv:2503.05200 — **ID reported by a discovery pass, not independently verified here**).

**Adjacent IT/AIOps additions (extend Category 6)**
- **OpenRCA: Can Large Language Models Locate the Root Cause of Software Failures?** — Junjielong Xu, Qinan Zhang, Zhiqing Zhong, Shilin He, Chaoyun Zhang, Qingwei Lin, Dan Pei, Pinjia He, Dongmei Zhang, Qi Zhang — 2025 — **ICLR 2025** — **DOI: no DOI found** (ICLR proceedings carry none); no arXiv preprint found. Code: https://github.com/microsoft/OpenRCA. **335 failures** from three enterprise systems with **>68 GB** of logs/metrics/traces; best model (Claude 3.5) solved only **11.34 %**. Static-QA-like: no execution, no remediation, no closed-loop verification.
- **Stalled, Biased, and Confused: Uncovering Reasoning Failures in LLMs for Cloud-Based Root Cause Analysis** — Evelien Riddell, James Riddell, Gengyi Sun, Michał Antkiewicz, Krzysztof Czarnecki — 2026 — *Proceedings of the 2026 IEEE/ACM Third International Conference on AI Foundation Models and Software Engineering* (**FORGE '26**), pp. 172–183 — **DOI 10.1145/3793655.3793732** (Crossref-verified); arXiv:2601.22208. Six LLMs × two agentic workflows (ReAct, Plan-and-Execute) + non-agentic baseline on GAIA and OpenRCA; **48,000 simulated failure scenarios (228 days of execution)**; measures root-cause accuracy **and intermediate reasoning-trace quality**, producing a labelled failure taxonomy (stalled / biased / confused). **This is the best methodological template found for evaluating agent reasoning quality rather than only outcomes** — directly relevant to gap 8.
- **RCAgentBench: An Agent-Oriented Benchmark for Multimodal Root Cause Analysis in Microservices** — Hengyue Jiang, Zexin Wang, Xiaohui Nie, Di Gao, Jingjing Li, Changhua Pei — 2026 — *2026 IEEE/ACM International Symposium on Quality of Service* (**IWQoS 2026**), pp. 1–10 — **DOI 10.1109/IWQoS70441.2026.11661026** (Crossref-verified). Agent-oriented **multimodal** RCA benchmark for microservices.
- **CloudRCA: A Root Cause Analysis Framework for Cloud Computing Platforms** — Yingying Zhang, Zhengxiong Guan, Huajie Qian, Leili Xu, Hengbo Liu, Qingsong Wen, Liang Sun, Junwei Jiang, Lunting Fan, Min Ke — 2021 — *Proceedings of the 30th ACM International Conference on Information & Knowledge Management* (**CIKM '21**), pp. 4373–4382 — **DOI 10.1145/3459637.3481903** (Crossref-verified); arXiv:2111.03753. **Not an agent benchmark and not LLM-based** — cite only as the classical pre-agentic RCA baseline (Knowledge-informed Hierarchical Bayesian Network; deployed in Alibaba Cloud, >20 % SRE resolution-time saving).
- **SREGym: A Live Training Ground for AI SRE Agents with High-Fidelity Failure Drills** — arXiv preprint version is titled *"SREGym: A Live Benchmark for AI SRE Agents with High-Fidelity Failure Scenarios"* (**arXiv:2605.07161**) — additional authors on the arXiv record: Yifang Tian, Hans-Arno Jacobsen, Yinfang Chen. Code: https://github.com/SREGym/SREGym
- **ITBench** — full metadata: **arXiv:2502.05352**; code https://github.com/itbench-hub/ITBench. Three IT-automation domains (**SRE, Compliance & Security Operations, FinOps**) over **94 real-world scenarios**; SOTA agents resolve only **13.8 %** of SRE, **25.2 %** of CISO and **0 %** of FinOps scenarios. The DSN-S record and the ICML record have **different titles and different author subsets** — cite carefully.
- **AIOpsLab** — full metadata: **arXiv:2501.06706** (Yinfang Chen, Manish Shetty, Gagan Somashekar, Minghua Ma, Yogesh Simmhan, Jonathan Mace, Chetan Bansal, Rujia Wang, Saravan Rajmohan); code https://github.com/microsoft/AIOpsLab
- **RCAEval** — code https://github.com/phamquiluan/RCAEval (plus a PyPI package `RCAEval`); **arXiv:2412.17015**; **735 failure cases** across three microservice systems with **15 reproducible RCA baselines**.
- **AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection** — Gou Tan, Zhensu Sun, Jieke Shi, et al. — 2026 — **ASE 2026** (41st IEEE/ACM International Conference on Automated Software Engineering) — **DOI 10.1145/3832783.3837437** — *reported by a discovery pass; my Crossref retry failed (rate limit), so treat this DOI as **UNVERIFIED** and confirm it.* arXiv:2608.06790. Injects crash/omission/value faults into **LLM API responses** at the shared HTTP layer; pass@1 drops by up to 50 pp across 65 fault configurations. Methodological counterpoint: fault injection *into agents*, not network fault remediation.

**Corrections and additions to earlier entries**
- **NetArena (item 2) is confirmed as ICLR 2026**: the official ICLR virtual page (poster, Thu 23 Apr 2026) carries the full abstract and links the OpenReview forum (`BPVPOtzoOz`) and project page http://www.netarena.ai/. A discovery pass also reports the earlier **working title "NetPress: Dynamically Generated LLM Benchmarks for Network Applications"** — if you see "NetPress" cited, it is the same work. *(Working-title claim **UNVERIFIED**.)*
- **NetConfArena (item 3) does have a public repository**: **https://github.com/liujona/NetConfArena** (URL retrieved; repository contents not inspected). A discovery pass additionally reports that the evaluated agents include **DeepSeek settings and Qwen3-8B**, and that stronger DeepSeek settings spend **52–59 % of actions on validation** whereas Qwen3-8B spends more on configuration updates. *(Content claims from a secondary pass — **UNVERIFIED**; the arXiv abstract I retrieved names no models.)*
- **OperAID (item 35)**: a discovery pass confirms **no arXiv preprint exists** for it.

---

## (f) Telecom-domain benchmark expansion — 16 further verified entries

A third sweep resolved several leads that §(f) had listed as unverified, and added substantial new telecom coverage. **These are important because they show the telecom-LLM benchmark space is far more crowded than the network-management space** — which strengthens the novelty claim of your 5G/6G *management* benchmark by contrast.

**Now-VERIFIED items that were previously listed as unverified leads in §(f):**

- **NetEval** *(paper title: "An Empirical Study of NetOps Capability of Pre-Trained Large Language Models")* — Yukai Miao, Yu Bai, Li Chen, Dan Li, Haifeng Sun, Xizheng Wang, Ziqiu Luo, Yanyu Ren, Dapeng Sun, Xiuting Xu, Qi Zhang, Chao Xiang, Xinchi Li — 2023 (arXiv v1 2023-09-11); **PREPRINT**, no DOI found — **arXiv:2309.05557**. Dataset: https://huggingface.co/datasets/NASP/neteval-exam (retrieved). **A 5,732-question multi-lingual NetOps evaluation set covering five NetOps sub-domains**, targeting commonsense knowledge and inference; evaluates **26 publicly available LLMs**; only GPT-4 reaches human-competitive performance. **This is the earliest dedicated NetOps benchmark found and should be cited as prior art** — it is static QA, with no agentic tool use, code generation, or multimodal inputs, and no 5G/6G protocol detail.
- **TelAgentBench: A Multi-faceted Benchmark for Evaluating LLM-based Agents in Telecommunications** — Sunwoo Lee, Daseong Jang, Dhammiko Arya, Gyoung-eun Han, Injee Song, SaeRom Kim, Sangjin Kim, Seojin Lee, et al. (15 authors) — 2025 — *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track* (**EMNLP 2025 Industry Track**), pp. 1173–1211, ACL — **DOI 10.18653/v1/2025.emnlp-industry.83**. A **Korean-language** telecom benchmark evaluating five core **agentic** capabilities: Reasoning, Planning, Action (tool-use), RAG, and Instruction Following; per-capability scoring with no single scalar. **This is the strongest agentic telecom benchmark found and the only non-English one** — cite it when arguing that agentic telecom evaluation has begun but is language- and knowledge-scoped, not network-actuation-scoped.
- **PSMBench** *(dataset: RFC2PSM)* — Zilin Shen, Xinyu Luo, Imtiaz Karim, Elisa Bertino — 2025 — *Advances in Neural Information Processing Systems 38* (**NeurIPS 2025, Datasets and Benchmarks Track**), pp. 63176–63210 — **DOI 10.52202/085713-1899**. RFC2PSM pairs **1,580 pages of cleaned RFC text** with **108 manually validated states and 297 transitions across 14 deployed protocols**. LLMs must emit a machine-readable protocol state machine from chunked RFC text; scored with structure-aware semantic fuzzy-matching. Nine SOTA models show a persistent **state–transition gap** (up to 0.82 F1 on individual states but ≤0.38 F1 on coherent transition graphs). **A NeurIPS D&B-track benchmark for protocol reasoning** — directly citable as evidence that standards-comprehension evaluation now reaches top MLSys venues.
- **TeleMath** — full authors: Vincenzo Colle, Mohamed Sana, Nicola Piovesan, Antonio De Domenico, Fadhel Ayed, Merouane Debbah — *IEEE Network*, 2026 — **DOI 10.1109/MNET.2026.3658826** (Crossref-verified); **arXiv:2506.10674**; dataset https://huggingface.co/datasets/netop/TeleMath. **500 expert-seeded Q&A pairs with numerical answers** covering signal processing, network optimization and performance analysis; reasoning-specialised models win while large general-purpose models struggle. No open-ended answers, no standards-clause retrieval, no agentic workflows.
- **TeleCom-Bench** — full authors: Jieting Xiao, Yun Lin, Huizhen Qiu, Rui Ma, Chen Zhong, Dongyang Xu, Xiao Long, Qiaobo Hao, Ding Zou, Zhiguo Yang, Yanqin Gao, Fang Tan — *KDD '26*, pp. 10056–10067 — **DOI 10.1145/3770855.3817480** (Crossref-verified); **arXiv:2605.18025**; code https://github.com/ZTE-AICloud/TeleCom-Bench. **12 evaluation sets / 22,678 samples** in two tiers: multi-dimensional knowledge comprehension (telecom fundamentals, 3GPP protocols, 5G architecture, plus proprietary product knowledge) and **end-to-end knowledge application formalising six tasks on authentic live-network agent trajectories: intent recognition, entity extraction, event verification, tool invocation, root cause analysis, solution generation.** Eight SOTA LLMs show a **"universal Execution Wall": ~90 % on linguistic interface tasks but ~30 % on procedural execution.** **This is one of the most directly relevant items for your survey** — it is the only benchmark found that scores tool invocation and RCA on *real operator agent trajectories*, and its Execution Wall finding is a citable, independent confirmation of your gap thesis. Caveats: Chinese-language/industrial deployment focus; not open-loop-executed (it scores trajectories, not live actuation).
- **WirelessMathBench** — full authors: Xin Li, Mengbing Liu, Li Wei, Jiancheng An, Merouane Abdelkader Debbah, Chau Yuen — *Findings of the Association for Computational Linguistics: ACL 2025*, pp. 10984–11009 — **DOI 10.18653/v1/2025.findings-acl.573** (Crossref-verified). **587 questions from 40 state-of-the-art wireless papers**, spanning MCQ to partial and full equation completion under physical and dimensional constraints; even DeepSeek-R1 averages only **38.05 %** overall and **7.83 %** on full equation completion. Dataset/toolkit URL not present on the retrieved page — **UNVERIFIED**.
- **ORANSight-2.0** *(introduces the **srsRANBench** benchmark)* — Pranshav Gajjar, Vijay K. Shah — *IEEE TMLCN*, vol. 3, pp. 903–920, 2025 — **DOI 10.1109/TMLCN.2025.3592658** (Crossref-verified); **arXiv:2503.05200**. Fine-tunes **18 open-source LLMs (1B–70B)** across five frameworks using **RANSTRUCT**, a RAG-based instruction-tuning framework with two LLM agents; introduces **srsRANBench** for **code generation and codebase understanding over srsRAN**, a widely used 5G O-RAN stack. Dataset: https://huggingface.co/datasets/prnshv/srsRANBench.

**New PREPRINT-only telecom benchmarks (no DOI found):**

- **TelcoLM: collecting data, adapting, and benchmarking language models for the telecommunication domain** — Camille Barboule, Viet-Phi Huynh, Adrien Bufort, Yoan Chabot, Géraldine Damnati, Gwénolé Lecorvé — 2024 — **PREPRINT**, **arXiv:2412.15891**. 800M tokens / 80K instructions of telco data; shows domain adaptation can be limited to a single instruction-tuning step without raw-text fine-tuning. No 3GPP-specific QA, no agentic evaluation, no code generation.
- **TeleTables: A Benchmark for Large Language Models in Telecom Table Interpretation** — Anas Ezzakri, Nicola Piovesan, Mohamed Sana, Antonio De Domenico, Fadhel Ayed, Haozhe Zhang — 2025/2026 — **PREPRINT**, **arXiv:2601.04202**; dataset https://huggingface.co/datasets/netop/TeleTables. **2,220 tables from 13 3GPP specifications in four formats plus 500 human-verified MCQs**, spanning direct retrieval to multi-step reasoning; evaluates **20 open-weight LLMs**. Closed-book, no general model exceeds **41 %**; with the table as context the best exceed **90 %** but degrade with reasoning depth/evidence scope/structural complexity (32.2 pp spread). **The only 3GPP table-understanding benchmark found** — directly relevant because 3GPP tables are where network management semantics live.
- **TeleSWEBench: A Commit-Driven Benchmark for Evaluating LLM-Powered Software Engineering in Telecommunications** — Pranshav Gajjar, Ali Mamaghani, Dinesh Bharadia, Vijay K. Shah — 2026 — **PREPRINT**, **arXiv:2606.05001**. Mines real developer commits from the **srsRAN 5G repository** into **734 questions with executable unit tests** across three difficulty tiers; evaluates AIDER, OpenHands and ClaudeCode over Qwen3, GPT OSS, Gemma 4, Kimi and Qwencoder 2.5, plus a hierarchical LLM-as-a-Judge ("TeleJudge"). Best tools reach only **~25 % of shippable changes**. Code-repair, not network operations.
- **MM-Telco: Benchmarks and Multimodal Large Language Models for Telecom Applications** — Anshul Kumar, Gagan Raj Gupta, Manish Rai, Apu Chakraborty, Ashutosh Modi, Abdelaali Chaoub, Soumajit Pramanik, Moyank Giri, Yashwanth Holla, Sunny Kumar, M. V. Kiran Sooraj — 2025/2026 — **PREPRINT**, **arXiv:2511.13131**; code https://github.com/gagan-iitb/MM-TelcoBench/. A suite of **multimodal (text + image)** telecom benchmarks covering **network operations, network management, documentation-quality improvement, and retrieval of relevant text and images**, plus fine-tuned baselines. **The only multimodal network-management benchmark found** — and it explicitly includes network management as a task category.
- **Telco-GAIA: Bilingual Benchmark for Agents in Telecom Domain** — Khizbullin, Alyafeai, Eldesokey, AlSultan, Alshalan, Ghanem, Pugh — 2026 — **PREPRINT**, **arXiv:2607.20510**. **100 human-verified English/Arabic multi-hop (avg 4.2 hops) tool-use tasks** over a website snapshot + SQL DB + web archives, in a Docker sandbox, scored by normalised exact string match with **no LLM judge**. Best model **71 %**. Notable for the no-LLM-judge scoring discipline.
- **TelecomGPT-R1: A Unified Open-Source Reasoner for the Telecom Stack** — Wang, Wu, Li, Zou, Tian, Bariah, Wei, Huang, Shen, Zhang, Debbah — 2026 — **PREPRINT**, **arXiv:2608.26126**. 67,427-example SFT corpus on four axes (protocol/knowledge/modelling/fault), two-stage LoRA-SFT + GRPO/DAPO; evaluated across **seven public telecom benchmarks and the GSMA open telco leaderboard**.
- **DeepSpecs: Expert-Level Question Answering in 5G** — Manvattira, Xu, Dang, Lu — *Findings of ACL 2026*, pp. 26935–26953 — **DOI 10.18653/v1/2026.findings-acl.1343**. Standard-native RAG with SpecDB/ChangeDB/TDocDB indices; curates **573 expert-annotated + 350 evolution-focused** 5G QA items from approved Change Requests. Source: https://aclanthology.org/2026.findings-acl.1343/
- **Free-Text Evaluation of LLMs for 5G Domain Knowledge and Fault Analysis using LLM-as-Judge** — Sengupta, Chatzimiltis, Shojafar, Zhu — accepted at **IEEE CSCN** (per the arXiv comment) — **arXiv:2608.21021**. Introduces free-text variants **TeleQNA-ORAN-FT, 5G-Faults-FT, TeleInter-FT** with multi-judge scoring. **A direct critique of MCQ-only telecom benchmarks** — all models show <60 % zero-shot recall of 3GPP/O-RAN specs. **Cite this in your gap section as independent evidence that static MCQ telecom benchmarks overstate capability.**

**Also confirmed:** the **GSMA open telco leaderboard** dataset is at https://huggingface.co/datasets/GSMA/leaderboard — the industry aggregate leaderboard that TelecomGPT-R1 reports against, and a useful cross-benchmark evaluation framework to cite alongside the GSMA ot-lite/ot-full datasets (item 34).

**Two arXiv-ID corrections worth propagating** (both wrong IDs resolve to unrelated papers, so a mis-citation is likely if copied from a secondary source): **Tele-LLMs = arXiv:2409.05314** (not 2409.07452); **ORAN-Bench-13K = arXiv:2407.06245** (not 2406.12398). Also: **Mobile-LLaMA has no arXiv version** — cite the IEEE Network DOI only.

**Revised gap picture after this expansion.** The telecom-LLM benchmark landscape is now demonstrably dense (knowledge, math, tables, multimodal, protocol state machines, code generation, bilingual agent tool-use). What remains absent is narrower and sharper than before: **(i) closed-loop LLM-agent network management with real actuation; (ii) telecom-agent safety/security evaluation in deployment; (iii) 3GPP table/figure understanding is only beginning (TeleTables); and (iv) multilingual telecom-agent evaluation has only TelAgentBench (Korean) and Telco-GAIA (Arabic).** Use this contrast explicitly: *the survey's contribution is not "benchmarking telecom LLMs" — that is crowded — but "benchmarking LLM agents that manage the network."*

---

## (g) Leads reported by discovery passes that I could NOT verify — do not cite without checking

These were surfaced by parallel discovery but **could not be confirmed** by me from a primary source (Crossref returned no match, or the venue record was not retrievable). Treat every field as unverified.

| Item | Reported venue | Why unverified |
|---|---|---|
| **SRE-skills-bench** (Rootly AI Labs) | year/venue unknown; README mentions NeurIPS/ICML/ACL workshops | No citable record found; code: https://github.com/Rootly-AI-Labs/SRE-skills-bench |
| **A Multi-Dataset Benchmark for Evaluating LLM Agents in Microservice Failure Diagnosis** | arXiv:2606.29193 (reported) | arXiv ID not independently confirmed; described as AIOps2025 + RCA100, 500+ expert-labelled cases, reasoning-**process** scoring (Localization / Identification / Reason) — **methodologically relevant to gap 8 if it checks out** |
| **NeMoCopilot** (33 tasks), **AI4OpsLab** (48 tasks) | cited in NetArena's comparison table | Bibliographic data not found |
| **LMTE — "Putting the 'Reasoning' into WAN Traffic Engineering with Language Models"** | stated in its own text to be accepted at **IEEE INFOCOM 2026**; arXiv:2602.00941 | Venue claim read from a search snippet, not from the paper or IEEE Xplore. **If true, it is the nearest INFOCOM item — worth one manual check.** |
| **Telco-GAIA / TelecomGPT-R1 / DeepSpecs / Free-Text 5G evaluation** | see §(f) | Metadata reported by a discovery pass from arXiv/ACL pages; **arXiv IDs and the ACL Findings DOI were not independently re-checked by me**. Verify before citing. |

---

## Appendix — one-line index

| # | Benchmark | Category | Status |
|---|---|---|---|
| 1 | NetConfEval | Config | Peer-reviewed (CoNEXT/PACMNET 2024) |
| 2 | NetArena | Config / dynamic | Peer-reviewed (ICLR 2026) |
| 3 | NetConfArena | Config / closed-loop | PREPRINT |
| 4 | NetConfBench | Config framework | IETF draft (not peer-reviewed) |
| 5 | Cornetto | Config repair | PREPRINT |
| 6 | Agentic Config Repair | Config repair | PREPRINT |
| 7 | NetLLMBench | Config | Peer-reviewed (NFV-SDN 2024) |
| 8 | NetAgentBench | Config / FSM | PREPRINT |
| 9 | PeeringLLM-Bench | BGP config | Peer-reviewed (AINTEC '25) |
| 10 | NetLLMeval | Config / live emulation | PREPRINT |
| 11 | dsm2cli | Intent→multivendor CLI | PREPRINT (+ SBRC 2026 ext. abstract) |
| 12 | Continual Benchmarking | Methodology | Peer-reviewed (SIGCOMM '25 poster) |
| 13 | NeMoEval line | Config via code-gen | Peer-reviewed (HotNets '23) |
| 14 | NIKA | Troubleshooting | PREPRINT + published dataset |
| 15 | NGNO Playground | Troubleshooting (position) | Peer-reviewed (SIGCOMM '25 wkshp) |
| 16 | SADE | Agent (evaluated on NIKA) | Peer-reviewed (LCN 2026) |
| 17 | FaulT-Bench | Troubleshooting / robustness | PREPRINT |
| 18 | MAIN Playground | Agentic network mgmt | Peer-reviewed (MAIN 2026) |
| 19 | Topology→Troubleshooting | Multimodal NetOps | Peer-reviewed (NOMS 2026) |
| 20 | NetArena DEMO | Config / demo | Peer-reviewed (SIGCOMM '26 demo) |
| 21 | IBNBench | Intent | Peer-reviewed (OJ-COMS 2025) |
| 22 | INTA | Intent | Peer-reviewed (ICNP 2025) |
| 23 | Intent-Driven Multi-Vendor | Intent | Peer-reviewed (TNSM 2026) |
| 24 | ConfAgent | Config (system) | Peer-reviewed (IWQoS 2025) |
| 25 | TeleQnA | Telecom knowledge | Peer-reviewed (IEEE Network 2026) |
| 26 | LDOT | Telecom reasoning | Peer-reviewed (IEEE JSAC 2026) |
| 27 | TSpec-LLM | 3GPP corpus | Peer-reviewed (GC Wkshps 2024) |
| 28 | ORAN-Bench-13K | Open RAN knowledge | Peer-reviewed (CCNC 2025) |
| 29 | Tele-LLMs | Telecom models+eval | Peer-reviewed (IEEE Access 2026) |
| 30 | TelecomGPT | Telecom LLM framework | Peer-reviewed (TMLCN 2025) |
| 31 | Mobile-LLaMA | 5G analysis fine-tune | Peer-reviewed (IEEE Network 2024) |
| 32 | 6G-Bench | 6G reasoning (static) | Peer-reviewed (OJ-COMS 2026) |
| 33 | SWE-Bench 5G | 5G core code repair | PREPRINT |
| 34 | GSMA Open-Telco | Telecom knowledge/safety | Industry, not peer-reviewed |
| 35 | **OperAID** | **5G core on K8s, closed loop** | **Peer-reviewed (NetSoft 2026)** |
| 36 | **6GAgentGym / 6GAgentBench** | **Closed-loop 6G mgmt, 42 tools** | **PREPRINT** |
| 37 | NetInjectBench | Safety / prompt injection | PREPRINT |
| 38 | WirelessOptBench | Action assurance | PREPRINT |
| 39 | α³-Bench | Safety/robustness/cost (UAV-6G) | PREPRINT |
| 40 | AgentPN Loop | Private 5G/6G mgmt | PREPRINT (content unverified) |
| 41 | AutoONBench | Optical agents | Peer-reviewed (JOCN 2026) |
| 42 | YANG-Grounded OpenROADM Agent | Optical multi-vendor | Peer-reviewed (SIGCOMM '26) |
| 43 | Small Models, Big Impact | Wireless planning, tool use | Peer-reviewed (ComMag 2026) |
| 44 | Multi-Level Network Modeling w/ LLMs | Simulation | Peer-reviewed (TNSE 2026) |
| 45 | ITBench | IT automation (adjacent) | Peer-reviewed (DSN-S 2025 / ICML 2025) |
| 46 | AIOpsLab | AIOps (adjacent) | Peer-reviewed (FSE '25 companion) |
| 47 | RCAEval | Microservice RCA (adjacent) | Peer-reviewed (WWW '25 companion) |
| 48 | SREGym | SRE live drills (adjacent) | Peer-reviewed (CAIS '26) |
| 49 | ORCA-bench | Oncall RCA (adjacent) | PREPRINT |
| 50 | NetBench | Traffic classification | Peer-reviewed (FMSys 2024) |
| 51 | TeleMath | Telecom math reasoning | Peer-reviewed (IEEE Network 2026) |
| 52 | TeleCom-Bench | Industrial telecom applications | Peer-reviewed (KDD '26) |
| 53 | WirelessMathBench | Wireless math modeling | Peer-reviewed (ACL Findings 2025) |
| 54 | ORANSight-2.0 | O-RAN foundation LLMs | Peer-reviewed (TMLCN 2025) |
| 55 | OpenRCA | Software RCA (adjacent) | Peer-reviewed (ICLR 2025) |
| 56 | Stalled, Biased, and Confused | Reasoning-failure analysis (adjacent) | Peer-reviewed (FORGE '26) |
| 57 | RCAgentBench | Multimodal microservice RCA (adjacent) | Peer-reviewed (IWQoS 2026) |
| 58 | CloudRCA | Pre-agentic RCA baseline (adjacent) | Peer-reviewed (CIKM '21) |
| 59 | AgentChaos | Fault injection into agents | Reported ASE 2026 — **DOI UNVERIFIED** |
