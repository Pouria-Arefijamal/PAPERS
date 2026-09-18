# 12 — Key Papers, Reading Order and Proposed PhD Architecture

Every entry below was bibliographically verified in this session (Crossref/OpenAlex), and the
evidence level for the content is stated. Where a paper could not be read beyond its abstract,
that is said explicitly rather than glossed over.

---

# Part 1 — The ten foundational papers

### 1. Network Service Orchestration: A survey
- **Authors / Year / Venue / DOI:** N. F. Saraiva de Sousa, D. A. Lachos Perez, R. V. Rosa, M. A. S. Santos, C. E. Rothenberg — 2019 — *Computer Communications* 142–143:69–94 — `10.1016/j.comcom.2019.04.008`
- **Why it matters:** It defines orchestration precisely enough to detect when the word is being misused.
- **What it does:** Surveys standards, projects and platforms; proposes the service / lifecycle / resource orchestration taxonomy.
- **Architecture:** Not a system — a three-scope taxonomy anchored on ETSI NFV MANO, with MEF LSO, TMF, IETF, TOSCA and ONF covered.
- **Algorithm:** None.
- **Experiment:** None (survey).
- **Limitation:** Pre-2020 snapshot; ML/AI-driven orchestration essentially absent.
- **Connection to my PhD:** It is the yardstick that shows most "orchestrators" in my corpus are resource-allocation algorithms (type B), not orchestrators. It also documents that cross-domain information exchange "is not a standard".

### 2. Knowledge-Defined Networking
- **Authors / Year / Venue / DOI:** A. Mestres et al. — 2017 — *ACM SIGCOMM Computer Communication Review* — `10.1145/3138808.3138810`
- **Why it matters:** The conceptual ancestor of every agentic network controller.
- **What it does:** Proposes a knowledge plane above data and control planes that observes, learns and acts.
- **Architecture:** Three planes; ML plus reasoning in the knowledge plane.
- **Algorithm:** Learned network models driving decisions.
- **Experiment:** Prototype on an emulated network (12 overlay nodes, 19 underlay elements, 72 links) using OMNeT++, Open vSwitch and Snort; learned overlay model at ~1% relative error with 3,000 training samples.
- **Limitation:** A vision paper with a small prototype; it never solves safe, verifiable decision-making.
- **Connection to my PhD:** Supplies the framing for my architecture and names the problem my work must actually solve: not "can an intelligent plane exist" but "can its decisions be verified and bounded".

### 3. Multipath TCP: From Theory to Practice
- **Authors / Year / Venue / DOI:** C. Raiciu et al. — 2011 — *IFIP Networking* — `10.1007/978-3-642-20757-0_21`
- **Why it matters:** The founding demonstration that multipath transport works, and the origin of the coupled-scheduling/congestion-control problem.
- **Architecture:** Multiple TCP subflows in one connection with a connection-level sequence space.
- **Algorithm:** Default scheduler plus coupled congestion control.
- **Experiment:** Real multi-homed 3G + Wi-Fi testbed.
- **Limitation:** Early prototype; the naive scheduler later proved harmful on heterogeneous paths.
- **Connection to my PhD:** Establishes that path selection is a control problem, not a routing detail.

### 4. Design, Implementation and Evaluation of Congestion Control for Multipath TCP
- **Authors / Year / Venue / DOI:** D. Wischik, C. Raiciu, A. Greenhalgh, M. Handley — 2012 — *USENIX NSDI* — no DOI
- **Why it matters:** Proves that uncoupled multipath flows starve single-path TCP, and that coupling restores fairness.
- **Algorithm:** Coupled congestion control (LIA family) with a fluid-model derivation.
- **Experiment:** Linux implementation over emulated and real networks.
- **Limitation:** Fairness is solved at the congestion-control layer; the scheduler can undo it.
- **Connection to my PhD:** Any learned scheduler I build must respect this coupling; DeepCC is the paper that finally learns both jointly.

### 5. Experimental evaluation of multipath TCP schedulers
- **Authors / Year / Venue / DOI:** C. Paasch, S. Ferlin, O. Alay, et al. — 2014 — *ACM SIGCOMM Capacity Sharing Workshop* — `10.1145/2630088.2631977`
- **Why it matters:** The canonical evidence that head-of-line blocking is a *scheduler* failure.
- **Algorithm:** Comparison of default lowest-RTT-first against alternatives.
- **Metrics:** Throughput, receiver buffer occupancy, reordering.
- **Limitation:** Two paths; nothing learned.
- **Connection to my PhD:** Defines the failure mode and the metrics my scheduler evaluation must include.

### 6. Low-Latency Scheduling in MPTCP
- **Authors / Year / Venue / DOI:** P. Hurtig, K.-J. Grinnemo, A. Brunstrom — 2019 — *IEEE/ACM Transactions on Networking* — `10.1109/TNET.2018.2884791`
- **Why it matters:** The strongest classical latency baseline; shows that throughput-oriented scheduling is wrong for latency-sensitive traffic.
- **Algorithm:** Latency-optimised scheduling rules derived from decomposing MPTCP delay, with explicit reordering consideration.
- **Limitation:** Rule-based; no learning; no network-level objective.
- **Connection to my PhD:** The baseline to beat, and a reminder that "who sets the objective" is the orchestrator's job.

### 7. AI-Driven Zero Touch Network and Service Management in 5G and Beyond
- **Authors / Year / Venue / DOI:** C. Benzaid, T. Taleb — 2020 — *IEEE Network* 34(2):186–194 — `10.1109/MNET.001.1900252`
- **Why it matters:** Sets the closed-loop, multi-timescale target that agentic management must hit.
- **Architecture:** AI/ML across ETSI ZSM control loops, intent-driven.
- **Algorithm / Experiment:** None — research directions.
- **Limitation:** Agenda paper; no implementation.
- **Connection to my PhD:** Its requirements (multi-scale loops, intent assurance, conflict resolution) are the checklist against which I can show that current LLM work is only partially there.

### 8. Cellular Network Traffic Scheduling With Deep Reinforcement Learning
- **Authors / Year / Venue / DOI:** S. Chinchali et al. — 2018 — *AAAI* — `10.1609/aaai.v32i1.11339`
- **Why it matters:** The methodological model for combining classical optimisation structure with learning.
- **Architecture:** Centralised base-station controller.
- **Algorithm:** A Lyapunov drift-plus-penalty per-slot optimum approximated by a deep RL policy.
- **Experiment:** Simulation with an RF throughput model (11.4% median error) and an LSTM forecast (14.8% median error); learned policy reaches ~80% of the offline DP oracle versus ~62% for stochastic MPC, and serves 2.06× the IoT traffic of the heuristic.
- **Limitation:** Single-cell simulation; no 5G core or slicing; the $661M saving figure is an extrapolation.
- **Connection to my PhD:** "Optimisation-structured RL" is the safest pattern for network control and the direct ancestor of my LLM-proposes/optimiser-disposes design.

### 9. Orchestrating Virtualized Network Functions
- **Authors / Year / Venue / DOI:** M. F. Bari et al. — 2016 — *IEEE Transactions on Network and Service Management* 13(4):725–739 — `10.1109/TNSM.2016.2569020`
- **Why it matters:** The classical placement/chaining baseline, and hard evidence that heuristics can be near-optimal.
- **Algorithm:** Exact and heuristic latency-aware VNF placement and chaining.
- **Experiment:** Simulation on real topologies; CPLEX 34.99 s versus 0.535 s for the heuristic on Internet2; more than 4× OPEX reduction; heuristic within 1.3× of optimal; >90% of middleboxes within 5 hops. (Numbers from the 2015 preprint; the TNSM version of record is paywalled.)
- **Limitation:** One-shot offline placement; no learning; no slices.
- **Connection to my PhD:** Sets the bar for what a learned placement engine must beat — and it is a type-B algorithm, not an orchestrator, which is exactly the distinction my taxonomy enforces.

### 10. TCP Extensions for Multipath Operation with Multiple Addresses (RFC 8684)
- **Authors / Year / Venue / DOI:** A. Ford, C. Raiciu, M. Handley, O. Bonaventure, C. Paasch — 2020 — IETF RFC (Standards Track) — `10.17487/RFC8684`
- **Why it matters:** It fixes the pluggable scheduler interface that every multipath scheduler must live within.
- **Key observation:** The standard exposes a scheduler hook but **no channel for the network to convey objectives**.
- **Connection to my PhD:** That absence is the architectural opening for my objective-passing contribution.

---

# Part 2 — Fifteen important scheduling / orchestration papers

1. **Intelligent Resource Scheduling for 5G Radio Access Network Slicing** — M. Yan, G. Feng, J. Hong Zhou, Y. Sun, Y.-C. Liang — 2019 — *IEEE TVT* — `10.1109/TVT.2019.2922668`. DRL slice-aware RAN scheduling; utilisation beats Q-learning by 16.3–19.8%, classic AC by 8.3–13.7%, HRSA by 30.5–34.7%; LSTM converges at ~18 epochs. *RAN-only, no end-to-end SLA.*
2. **Deep Reinforcement Learning for Dynamic Uplink/Downlink Resource Allocation in High Mobility 5G HetNet** — F. Tang, Y. Zhou, N. Kato — 2020 — *IEEE JSAC* — `10.1109/JSAC.2020.3005495`. Joint UL/DL allocation under mobility. *Abstract-level in this session.*
3. **Learn to Schedule (LEASCH)** — F. Al-Tam, N. Correia, J. Rodriguez — 2020 — *IEEE Access* — `10.1109/ACCESS.2020.3000893`. DRL MAC scheduler; throughput +2.4–3% over proportional fair and +18–19% over round robin; Jain fairness +1–5%; converges in <300 episodes. *Only 4 UEs; no named simulator; no traffic model.*
4. **Reinforcement Learning-Based Particle Swarm Optimization for End-to-End Traffic Scheduling in TSN-5G Networks** — X. Wang, H. Yao, T. Mai, et al. — 2023 — *IEEE/ACM ToN* — `10.1109/TNET.2023.3276363`. RL-guided metaheuristic with a MILP reference. *Abstract-level; the hybrid RL+optimiser pattern matters most.*
5. **DecAge: Decentralized Flow Scheduling for Industrial 5G and TSN Integrated Networks** — M. Li, S. Guo, C. Chen, et al. — 2024 — *IEEE TNSE* — `10.1109/TNSE.2023.3301879`. Distributed cross-domain scheduling; the decentralisation argument that motivates hierarchical agents.
6. **NRflex: Enforcing Network Slicing in 5G New Radio** — K. Boutiba, A. Ksentini, B. Brik, Y. Challal, A. Balla — 2022 — *Computer Communications* 181:284–292 — `10.1016/j.comcom.2021.09.034`. **Full text read.** RIC-side BWP manager plus gNB BWP multiplexer driving the MAC scheduler; deadline failure rate reaches zero at ~50 UEs (numerology 2) versus ~25 UEs for the standard scheme. *Rule-based control law; RAN-only.*
7. **Satisfying Network Slicing Constraints via 5G MAC Scheduling** — M. Mandelli, J. G. Andrews, S. Borst, S. Klein — 2019 — *IEEE INFOCOM* — `10.1109/INFOCOM.2019.8737604`. Slice-constraint-aware MAC scheduling. *Closed access; abstract only.*
8. **On Deep Reinforcement Learning for Traffic Steering Intelligent O-RAN** — F. Kavehmadavani, V.-D. Nguyen, T. X. Vu, S. Chatzinotas — 2023 — *IEEE Globecom Workshops* — `10.1109/GCWkshps58843.2023.10464606`. DDQN at the **non-RT RIC** plus a heuristic/ML/convex-optimisation pipeline — the same tier an LLM planner would occupy.
9. **Federated Meta-Learning for Traffic Steering in O-RAN** — H. Erdol et al. — 2022 — *IEEE VTC2022-Fall* — `10.1109/VTC2022-Fall57202.2022.10012789`. Reptile + DQN across K = 5 federated agents; relevant to multi-domain data governance.
10. **Programmable and Customized Intelligence for Traffic Steering in 5G Networks Using Open RAN Architectures** — 2023 — *IEEE TMC* — `10.1109/TMC.2023.3272948`. The programmable steering control point my agent would attach to. *Read as an author preprint of the TMC version.*
11. **Power Consumption-Aware 5G Edge UPF Selection using DRL** — A. Bellin, N. Di Cicco, D. Munaretto, F. Granelli — 2024 — *IEEE NFV-SDN* — `10.1109/NFV-SDN61811.2024.10807472`. **Full text read.** 1% latency error versus 14.3% for a latency-greedy heuristic; 20% less energy than latency-smart; and a **null ablation** (power-based vs CPU-based PPO show no difference on identical hardware).
12. **Scaling UPF Instances in 5G/6G Core With Deep Reinforcement Learning** — H. T. Nguyen, T. Van Do, C. Rotter — 2021 — *IEEE Access* — `10.1109/ACCESS.2021.3135315`. PPO saves 2.7–3.8% of Pods versus Kubernetes HPA — a **weak baseline** that flatters the learned method.
13. **SFCPlanner: An Online SFC Planning Approach With SRv6 Flow Steering** — 2024 — *IEEE TNSM* — `10.1109/TNSM.2024.3392945`. Online chain planning plus flow steering — the closest transport-layer analogue to orchestrated scheduling.
14. **Using Distributed Reinforcement Learning for Resource Orchestration in a Network Slicing Scenario** — F. Mason, G. Nencioni, A. Zanella — 2023 — *IEEE/ACM ToN* 31(1):88–102 — `10.1109/TNET.2022.3187310`. **The best-specified DRL orchestration study**: distributed A2C controllers, 2–6 flows, 50 Gbps links, 20 ms/1 ms delay targets, an explicit SLA performance function in [0,1]; Ω > 0.45 in ~50% of episodes with a 10% gain over the empirical heuristic; transfers across topologies; **but the heuristic wins in the hardest scenario**.
15. **An Autonomous Network Orchestration Framework Integrating LLMs with Continual RL** — M. Shokrnezhad, T. Taleb — 2025 — *IEEE Communications Magazine* 63(8):78–84 — `10.1109/MCOM.001.2400526`. **Full text read.** ARC: LLaMA 3.1-8B planner + Double Dueling DQN executors + continual RL; 10 nodes, 10 users; **figure-only results with no numbers**; no external baseline. *The single most instructive paper for my proposed architecture.*

---

# Part 3 — Fifteen multipath papers

1. **Multipath TCP: From Theory to Practice** — Raiciu et al. — 2011 — IFIP Networking — `10.1007/978-3-642-20757-0_21`. *Foundational.*
2. **Design, Implementation and Evaluation of Congestion Control for Multipath TCP** — Wischik et al. — 2012 — USENIX NSDI — no DOI. *Foundational; coupled CC.*
3. **CMT-QA: Quality-Aware Adaptive Concurrent Multipath Data Transfer in Heterogeneous Wireless Networks** — C.-M. Huang, C.-H. Tsai — 2013 — *IEEE TMC* — `10.1109/TMC.2012.196`. Earliest quality-aware multipath scheduling; SCTP/CMT lineage.
4. **Experimental evaluation of multipath TCP schedulers** — Paasch et al. — 2014 — ACM SIGCOMM CSWS — `10.1145/2630088.2631977`. *The head-of-line-blocking evidence.*
5. **DAPS: Intelligent Delay-Aware Packet Scheduling for Multipath Transport** — 2014 — IEEE ICC — `10.1109/ICC.2014.6883576`. Earliest delay-aware MPTCP scheduler baseline.
6. **BLEST: Blocking Estimation-Based MPTCP Scheduler for Heterogeneous Networks** — S. Ferlin, Ö. Alay, T. Dreibholz, et al. — 2016 — IFIP Networking — `10.1109/IFIPNetworking.2016.7492955`. *The classical reordering-aware baseline.*
7. **Bandwidth-Efficient Multipath Transport Protocol for Quality-Guaranteed Real-Time Video Over Heterogeneous Wireless Networks** — 2016 — *IEEE TCOM* — `10.1109/TCOMM.2016.2539169`. Application-level objectives inside a multipath scheduler.
8. **Multipath QUIC: Design and Evaluation** — Q. De Coninck, O. Bonaventure — 2017 — *ACM CoNEXT* — `10.1145/3143361.3143370`. Opens the MPQUIC scheduling space.
9. **The QUIC Transport Protocol: Design and Internet-Scale Deployment** — A. Langley et al. — 2017 — *ACM SIGCOMM* — `10.1145/3098822.3098842`. Why QUIC's packet-number space makes MPQUIC scheduling tractable.
10. **ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths** — 2017 — *ACM CoNEXT* — `10.1145/3143361.3143379`. *The second classical baseline; needed a congestion-control patch to estimate rates.*
11. **A Stream-Aware Multipath QUIC Scheduler for Heterogeneous Paths** — 2018 — ACM Workshop on the Evolution of QUIC — `10.1145/3229543.3229550`. Richer (stream-level) context for scheduling.
12. **Low-Latency Scheduling in MPTCP** — Hurtig et al. — 2019 — *IEEE/ACM ToN* — `10.1109/TNET.2018.2884791`. *The latency baseline.*
13. **ReLeS: A Neural Adaptive Multipath Scheduler Based on DRL** — H. Zhang, W. Li, S. Gao, X. Wang, B. Ye — 2019 — *IEEE INFOCOM* — `10.1109/INFOCOM.2019.8737649`. **Abstract only, and the full text is genuinely closed** — no OpenAlex/Unpaywall OA location, no arXiv version, no author PDF. *Its opacity is a reproducibility finding.*
14. **Peekaboo: Learning-Based Multipath Scheduling for Dynamic Heterogeneous Environments** — 2020 — *IEEE JSAC* — `10.1109/JSAC.2020.3000413`. The learning scheduler that still cannot hear the network.
15. **DeepCC: Multi-Agent DRL Congestion Control for Multi-Path TCP Based on Self-Attention** — B. He, J. Wang, Q. Qi, et al. — 2021 — *IEEE TNSM* — `10.1109/TNSM.2021.3093302`. **Full text read. The most rigorous learning-based multipath scheduler found**: 12-dimensional state, two continuous actions per subflow, MAPOKTR (K-FAC actor-critic), BiLSTM-32 + self-attention, real Linux testbed with `tc`/`ethtool`, four subflows; self-attention cuts convergence time ~50% and raises goodput ~80%.

**Also worth reading:** **Multipath QUIC for ATSSS in 5G Advanced** (IEEE ComMag Standards 2023, `10.1109/MCOMSTD.0001.2200069`) — the standards hook; **Deep RL for Access Traffic Splitting in 5G Core** (2024) and **Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective RL** (2025) — the core-side multipath line; **Tokens, Not Packets** (ANRW 2026) — the interface argument my contribution builds on; **A Survey on Multipath Transport Protocols Towards 5G ATSSS** (IEEE Access 2021, `10.1109/ACCESS.2021.3118593`).

---

# Part 4 — Fifteen LLM / agent / network-management papers

1. **NetConfEval: Can LLMs Facilitate Network Configuration?** — C. Wang, M. Scazzariello, A. Farshin, et al. — 2024 — *ACM CoNEXT / PACMNET* — `10.1145/3656296`. The benchmark template; **public code and public dataset**.
2. **NIKA: A Network Arena for Benchmarking AI Agents on Network Troubleshooting** — Z. Wang, A. Cornacchia, A. Sacco, F. Galante, M. Canini, D. Jiang — 2025 — arXiv:2512.16381 (**preprint**) — 640 incidents, 54 issues, 30+ MCP tools, 900+ public reasoning traces. *Shows an executable agent benchmark is feasible — and that no 5G/6G equivalent exists.*
3. **NetArena: Dynamic Benchmarks for AI Agents in Network Automation** — 2026 — **ICLR 2026** — arXiv:2506.03231. Dynamic generation, contamination control, safety decoupled from correctness. *The methodological standard I must meet.*
4. **OperAID: Benchmarking LLM Agents for Autonomous Kubernetes Fault Remediation on a 5G Core** — 2026 — *IEEE NetSoft* — `10.1109/NetSoft70012.2026.11603505`. **The closest existing closed-loop 5G-core benchmark**: Open5GS + UERANSIM on Kubernetes, 900 experiments, **70.7% with tools versus 7.1% without**, best model 93.3%. *Faults are Kubernetes-level, not 3GPP protocol-level, and no SLA is scored.*
5. **TeleCom-Bench** — 2026 — *ACM KDD* — `10.1145/3770855.3817480`. 22,678 samples from live operator trajectories; the measured **execution wall (~90% linguistic versus ~30% procedural)**.
6. **TeleQnA** — A. Maatouk et al. — 2026 — *IEEE Network* 40(2):253–260 — `10.1109/MNET.2025.3576035`. The standard telecom-knowledge benchmark; public code and dataset.
7. **Mobile-LLaMA: Instruction Fine-Tuning an Open-Source LLM for Network Analysis in 5G Networks** — K. B. Kan, H. Mun, G. Cao, Y. Lee — 2024 — *IEEE Network* 38(5):76–83 — `10.1109/MNET.2024.3421306`. 15,111 instruction sets; **247/300 versus GPT-3.5's 209/300**; public code. *Analysis, not control.*
8. **TelecomGPT** — H. Zou, Q. Zhao, Y. Tian, et al. — 2025 — *IEEE TMLCN* 3:948–975 — `10.1109/TMLCN.2025.3593184`. Three-stage domain adaptation; **75.30 versus GPT-4o's 38.94 on 3GPP tdoc classification**; ~1.5 h instruct-tuning on an 8-GPU node.
9. **Tele-LLMs: A Series of Specialized LLMs for Telecommunications** — 2026 — *IEEE Access* 14:86424–86441 — `10.1109/ACCESS.2026.3698683`. ~5,000 GPU-hours on 8×A6000; **LoRA tested and rejected as saturating**; public models and data.
10. **ORANSight-2.0: Foundational LLMs for O-RAN** — 2025 — *IEEE TMLCN* 3:903–920 — `10.1109/TMLCN.2025.3592658`. **QLoRA-4-bit fine-tuning of models up to 70B on 151,500 O-RAN instruction pairs using a single 24 GB RTX 4090** — the hardware-feasibility result for my own experiments.
11. **ORION: Intent-Aware Orchestration in Open RAN for SLA-Driven Network Management** — G. da Silva Machado, G. Z. Bruno, A. Huff, J. M. C. Brito, C. B. Both — 2026 — arXiv:2603.03667 (**preprint**). **Full text read.** LLM agents over MCP inside the O-RAN SMO/RIC hierarchy; 100% policy-generation success for high-capacity models but 17% for one mid-tier model; **156× cost spread**; ~15 s per SMO-stage call.
12. **NetIntent: Leveraging LLMs for End-to-End Intent-Based Networking** — 2025 — *IEEE OJ-COMS* — `10.1109/OJCOMS.2025.3642642`. 33 models from 1.1B to 70B integrated with OpenDaylight/ONOS; **model size does not predict quality**; 20.1–35.1 s per intent on ODL.
13. **Toward Autonomous O-RAN: A Multi-Scale Agentic AI Framework for Real-Time Network Control** — 2026 — arXiv:2602.14117 (**preprint**). The measured tiering result: **0.847 ms on-device, 793 ms near-RT SLM**, with an LLM supervising from non-RT; VIP throughput +6% at preserved 22 ms latency on an srsRAN testbed with four slices. *The single most architecturally decisive measurement in this review.*
14. **An Autonomous Network Orchestration Framework Integrating LLMs with Continual RL** — Shokrnezhad, Taleb — 2025 — *IEEE Communications Magazine* 63(8):78–84 — `10.1109/MCOM.001.2400526`. The LLM-planner + RL-executor pattern, fully instrumented in the paper's description but under-reported in its results.
15. **A Survey on Large Language Models for Communication, Network, and Service Management** — 2026 — *IEEE COMST* — `10.1109/COMST.2025.3548039`. The current consolidated picture; use it to check my related work immediately before writing.

**Also essential:** **Large Language Models for Networking** (IEEE Network 2025, `10.1109/MNET.2024.3435752`); **Semantic Routing for LLM-Assisted Intent-Based 5G Core Management** (GLOBECOM 2024, `10.1109/GLOBECOM52923.2024.10901065`); **TSpec-LLM** (GC Wkshps 2024, `10.1109/GCWkshp64532.2024.11101012`); **Telco-RAG** (`10.1109/GLOBECOM52923.2024.10901155`) and **TelecomRAG** (ACM CCR 2025, `10.1145/3711992.3711996`) — two *different* papers with similar names; **LLM-xApp** (`10.14722/futureg.2025.23057`); **SafeCOMM** (WCNC 2026, `10.1109/WCNC65185.2026.11555432`) — safety degradation after telecom fine-tuning.

---

# Part 5 — Ten model-efficiency / fine-tuning papers

1. **LoRA: Low-Rank Adaptation of Large Language Models** — E. Hu et al. — 2022 — *ICLR* — arXiv:2106.09685. The default adaptation method in network-domain work.
2. **QLoRA: Efficient Finetuning of Quantized LLMs** — T. Dettmers et al. — 2023 — *NeurIPS* — `10.52202/075280-0441`. The technique that makes single-GPU domain specialisation possible.
3. **TinyBERT: Distilling BERT for Natural Language Understanding** — X. Jiao et al. — 2020 — *Findings of EMNLP* — `10.18653/v1/2020.findings-emnlp.119`. The distillation template.
4. **LLM-Pruner: On the Structural Pruning of Large Language Models** — X. Ma, G. Fang, X. Wang — 2023 — *NeurIPS* — `10.52202/075280-0950`. Structural pruning of genuine LLMs — established in NLP, **never evaluated on a network task**.
5. **A Survey on Model Compression for Large Language Models** — 2024 — *TACL* — `10.1162/tacl_a_00704`. The taxonomy I use to keep compression families distinct.
6. **TelecomGPT** — 2025 — *IEEE TMLCN* — `10.1109/TMLCN.2025.3593184`. The best-documented domain-adaptation recipe and its measured cost.
7. **Mobile-LLaMA** — 2024 — *IEEE Network* — `10.1109/MNET.2024.3421306`. The first well-known network-domain instruction fine-tuning result.
8. **ORANSight-2.0** — 2025 — *IEEE TMLCN* — `10.1109/TMLCN.2025.3592658`. **QLoRA-4-bit 70B on one 24 GB RTX 4090** — the practical hardware floor.
9. **MERLOT: A Distilled LLM-Based Mixture-of-Experts Framework for Scalable Encrypted Traffic Classification** — 2025 — *IEEE Globecom Workshops* — `10.1109/GCWkshps68340.2025.1159118`. A **660M student matching a 7B model** on 8 of 10 datasets at 85–90% less inference time and memory. *(Its parameter accounting is internally inconsistent in the paper — report the conflict rather than resolving it.)*
10. **Toward 6G Edge Intelligence: Lightweight LLMs for Intent-Driven Network Management** — 2026 — *IEEE TMC* — `10.1109/TMC.2026.3678546`. Distillation plus a knowledge graph for intent management: **95% accuracy with 60% lower inference latency**.

**Also important:** **Tele-LLMs** (`10.1109/ACCESS.2026.3698683`, LoRA-rejection evidence); **SQLLM** (`10.1109/TCE.2026.3657983`, quantisation for 5G private-network operations — **unreadable behind a paywall, the largest verification gap in Area 5**); **5G INSTRUCT Forge** (`10.1109/TCCN.2024.3516055`, freeze-tuning with an MMLU-collapse ablation); **NetKD** (`10.1109/CSCWD61410.2024.10580837`, 4.61% of parameters at 99.10% of F1); **Distilling LLMs for Network Active Queue Management** (`10.1109/TON.2026.3690076`) — note that **despite the title there is no teacher-student distillation in it**; the mechanism is LoRA plus offline RL.

---

# A) The 20 papers to read first, in learning order

Not a quality ranking — a dependency order, so that each paper supplies the vocabulary for the next.

| # | Paper | Why at this position |
|---|---|---|
| 1 | Network Service Orchestration: A survey (ComCom 2019) | Fixes the meaning of "orchestration" before anything else |
| 2 | Knowledge-Defined Networking (CCR 2017) | The conceptual ancestor of agentic control |
| 3 | AI-Driven Zero Touch Network and Service Management (IEEE Network 2020) | Defines the closed-loop target |
| 4 | Multipath TCP: From Theory to Practice (IFIP Networking 2011) | Why multipath is hard |
| 5 | Coupled Congestion Control for MPTCP (NSDI 2012) | Why control and scheduling are one problem |
| 6 | Experimental evaluation of MPTCP schedulers (SIGCOMM CSWS 2014) | Why scheduling is a research problem |
| 7 | Low-Latency Scheduling in MPTCP (ToN 2019) | The latency baseline |
| 8 | Orchestrating Virtualized Network Functions (TNSM 2016) | The placement/chaining baseline and the "type B vs orchestrator" distinction |
| 9 | Cellular Network Traffic Scheduling with DRL (AAAI 2018) | Optimisation-structured RL — the safest control pattern |
| 10 | An Autonomous Network Orchestration Framework Integrating LLMs with Continual RL (ComMag 2025) | The LLM-planner + RL-executor pattern in full |
| 11 | Using Distributed RL for Resource Orchestration in a Network Slicing Scenario (ToN 2023) | What a complete experimental description looks like; explicit SLA function |
| 12 | DeepCC (TNSM 2021) | What a complete *scheduler* description looks like |
| 13 | TelecomGPT (TMLCN 2025) | Domain adaptation and its cost |
| 14 | Tele-LLMs (IEEE Access 2026) | The LoRA-versus-full-fine-tuning dispute |
| 15 | ORANSight-2.0 (TMLCN 2025) | The hardware feasibility floor (70B on one 24 GB GPU) |
| 16 | TeleCom-Bench (KDD 2026) | The measured execution wall |
| 17 | NIKA (arXiv 2025) | How to build an executable network-agent benchmark |
| 18 | OperAID (NetSoft 2026) | The boundary of what is benchmarked for 5G cores |
| 19 | ORION (arXiv 2026) | LLMs inside the O-RAN hierarchy — and what they cost |
| 20 | Toward Autonomous O-RAN: Multi-Scale Agentic AI (arXiv 2026) | The latency tiering that constrains every design |

# B) The 10 papers most directly connected to my proposed direction

1. **An Autonomous Network Orchestration Framework Integrating LLMs with Continual RL** (ComMag 2025) — the pattern I extend.
2. **OperAID** (NetSoft 2026) — the closed-loop 5G-core benchmark I must surpass in scope (3GPP-level faults, SLA scoring).
3. **ORION** (arXiv 2026) — the closest LLM-in-O-RAN attempt; my work must measure what it does not (SLA outcomes).
4. **Toward Autonomous O-RAN: Multi-Scale Agentic AI** (arXiv 2026) — measured tiering that defines my architecture.
5. **Using Distributed RL for Resource Orchestration in a Network Slicing Scenario** (ToN 2023) — my primary DRL orchestration baseline and SLA-function formulation.
6. **DeepCC** (TNSM 2021) — my primary learned-scheduler baseline, and the demonstration that joint CC+scheduling learning works in a real stack.
7. **BLEST** (IFIP Networking 2016) and **ECF** (CoNEXT 2017) — the classical multipath baselines.
8. **Tokens, Not Packets** (ANRW 2026) — the interface argument underpinning my objective-passing contribution.
9. **TeleCom-Bench** (KDD 2026) — independent evidence that the execution gap is real and large.
10. **ORANSight-2.0** (TMLCN 2025) — proof that the fine-tuning leg of my plan is feasible on one consumer GPU.

# C) The 10 most useful experimental architectures from the literature

1. **ns-3 + ns-O-RAN + a real near-RT RIC** — the only Area-1 architecture found that puts a real control-plane component in the loop while simulating the RAN. The most credible route to a reproducible O-RAN evaluation.
2. **Colosseum / OpenRAN Gym** — large-scale, repeatable O-RAN experimentation with real xApps (used by the ColO-RAN and xApp-design work).
3. **Open5GS + UERANSIM + Kubernetes** — the OperAID architecture: a real 5G core with real signalling, containerised so that an agent's actions (scaling, configuration) are genuine infrastructure changes.
4. **srsRAN live testbed with slices + E2SM-KPM telemetry** — the multi-scale agentic tiering setup; the only architecture found that measures all three control-loop tiers on live hardware.
5. **Mininet + OpenDaylight/ONOS** — the NetIntent architecture: real SDN controllers, fast iteration, good for intent-to-flow work.
6. **Linux kernel/userspace hybrid (DeepCC)** — the MPTCP v0.93 + sysctl + userspace-daemon pattern with `tc`/`ethtool` path emulation; the standard for reproducible multipath scheduler evaluation.
7. **OMNeT++ + Simu5G** — integrated 5G system simulation, good for large sweeps of end-to-end behaviour.
8. **Dynamic task generation with statistical-power control (NetArena)** — not a network testbed but an evaluation architecture: generate tasks at runtime, report confidence intervals, separate safety from correctness.
9. **Curated incident suites with an Agent Access Layer / MCP tool interface (NIKA)** — how to expose a network to an agent safely and reproducibly, with access policies.
10. **SLA-function formulation over a fluid/markov traffic model (ToN 2023)** — the evaluation architecture for scoring service-level satisfaction continuously rather than as pass/fail.

# D) The 10 most common evaluation metrics

1. **End-to-end latency / delay percentiles** (mean, p50, p95, p99) — the dominant metric across all five areas.
2. **Throughput / goodput** — universal; in multipath, *sequential* goodput specifically (reordering-penalised).
3. **Resource utilisation / PRB consumption / spectral efficiency** — the RAN scheduling metric of record.
4. **SLA satisfaction / QoS satisfaction rate** — usually a rate target or a continuous satisfaction function; the metric most often claimed and least often properly measured.
5. **Packet loss / deadline failure rate / SLA-violation rate** — the failure-side metric.
6. **Jitter and packet reordering / receive-buffer occupancy** — the multipath-specific metric pair.
7. **Fairness (Jain index, bottleneck fairness, inter-slice fairness)** — reported widely, optimised rarely.
8. **Energy / power consumption** — increasingly standard for 5G core and RAN decisions.
9. **Convergence time / episodes to convergence** — the DRL-specific metric that almost every DRL paper reports.
10. **Accuracy (task accuracy, F1, decision agreement, policy-generation success rate)** — the LLM/agent-side metric; note that **latency and cost are far less commonly reported**, and SLA-level outcomes almost never.

# E) The 10 most common experimental parameters

Extracted literally into `08_experimental_parameters.csv` (values remain `NA` where not present in a retrievable source).

1. **Number of UEs / users** (4 to 126 in the papers where it was reported)
2. **Number of flows / subflows** (2 to 9 in the DRL orchestration work; 4 simultaneous MPTCP subflows in DeepCC)
3. **Number of gNBs / base stations / nodes** (1 to 8 gNBs; 10 nodes in ARC)
4. **Link bandwidth / capacity** (10 Mbps to 50 Gbps depending on the setting)
5. **Latency targets** (1 ms URLLC, 5 ms, 20 ms eMBB, 22 ms preserved)
6. **Traffic model** (Poisson, CBR, Markov-modulated demand, periodic TSN flows, real traces, or — revealingly — not reported)
7. **Training episodes / simulation time** (3×10⁴ to 5×10⁴ episodes of 50 slots in ToN 2023; 500 test episodes)
8. **Learning rate and RL hyperparameters** (e.g. actor/critic 10⁻⁵, discount 0.9, entropy weight 10⁻⁴ in ToN 2023)
9. **Model and model size** (LLaMA-2 13B, LLaMA 3.1-8B, Qwen 7–8B, GPT-2-base 117M, 1.1B–70B in the model-comparison studies)
10. **GPU / hardware** (single RTX 4090 24 GB, RTX A6000 48 GB, 2×A100-80GB, 7×A6000, 8×A6000, 8×H200, Jetson Xavier NX)

# F) The strongest evidence-supported research gaps

Ranked by strength of the supporting evidence in this review (full detail in `10_gap_report.md` §10).

1. **No SLA-scored, closed-loop agent benchmark for 5G/6G management** — ~30 benchmarks exist, none scores service-level outcomes as the primary result; OperAID's faults are Kubernetes-level.
2. **No model-size / compression versus network-decision-quality curve** — every trade-off found uses an NLP proxy metric; the only billion-parameter pruning work evaluates on Wikitext2.
3. **Multipath scheduling has never been connected to orchestration or O-RAN** — zero hits for multipath + O-RAN; endpoint schedulers are structurally network-blind.
4. **No agentic orchestration across RAN + transport + core + edge** — cross-domain end-to-end management is described as open even by the COMST 2024 survey, which covers DRL only, not LLMs.
5. **"LLM proposes, optimiser disposes" has not been demonstrated inside a standards-compliant management plane** — the hybrid exists in configuration repair and in ARC, never in O-RAN SMO with A1/E2 enforcement and SLA scoring.
6. **Latency-feasible tiering of management functions is unstandardised** — measured LLM/intent latencies (0.8 ms to 35 s) span four orders of magnitude, and only one preprint implements a three-tier design.
7. **Safety, hallucination and the blast radius of wrong actions are unmeasured for 5G/6G agents** — safety work exists off-core (prompt injection, false premises, unsafe-apply rate), none on a core or RAN.
8. **RAN scheduling and 5G core QoS-flow scheduling are disjoint literatures** — no paper found couples them, although end-to-end QoS requires exactly that.
9. **The fine-tuning recipe for network *decision* quality is unknown** — domain adaptation helps text tasks, LoRA's sufficiency is disputed, and one QLoRA-tuned 1B model lost to a Random Forest.
10. **Reproducibility is poor and a reproducibility-first contribution is available** — the canonical DRL MPTCP scheduler (ReLeS) is unreadable and has no code; only 27 of 152 records have an identified public artifact; several studies report no simulator identity at all.

# G) Proposed experimental architecture for the PhD

**This architecture is a composition of published ingredients, not a novel invention.** Each
component exists in the literature — the LLM planner plus RL executors (ARC), the O-RAN
management hierarchy (ORION), the tiering constraint (the multi-scale agentic preprint), the
learned scheduler (DeepCC), the core-side splitting decision (ATSSS DRL work), the
optimiser-as-feasibility-authority pattern (configuration repair and RL-PSO), the benchmark
methodology (NetArena, NIKA), and the SLA function (ToN 2023). **What does not exist is the
composition with SLA-level evaluation, and that — not the components — is the claim.**
Before writing any novelty statement, the three closest 2026 papers must be retrieved and read
(see §10 GAP list and the reading order, Stage 6).

```
                        ┌──────────────────────────────────────────────┐
   operator intent ────►│  TIER 3 — NON-RT / SMO  (> 1 s budget)       │
   (natural language)   │  LLM planner (7–8B, RAG over 3GPP/O-RAN)     │
                        │  · intent → service objectives & constraints │
                        │  · cross-domain conflict arbitration         │
                        │  · explanation + audit log                   │
                        └───────────────┬──────────────────────────────┘
                                        │ objectives, constraints, priorities
                                        │ (A1-style policy objects)
                        ┌───────────────▼──────────────────────────────┐
                        │  FEASIBILITY & OPTIMISATION LAYER            │
                        │  constrained optimiser (MILP / CP) + DRL     │
                        │  · feasibility authority: rejects infeasible │
                        │    or unsafe objectives  ← HALLUCINATION     │
                        │    SHIELD                                    │
                        │  · produces a verifiable plan                │
                        └───────────────┬──────────────────────────────┘
                                        │ verified plan
        ┌───────────────────────────────┼────────────────────────────────┐
        │                               │                                │
┌───────▼────────┐          ┌───────────▼──────────┐        ┌────────────▼─────────┐
│ TIER 2 — NEAR-RT (10 ms–1 s)                                              │
│ · distilled SLM (1–3B, INT8) for adaptation & re-planning                 │
│ · DRL controllers: slice admission, PRB/BWP allocation, UPF selection     │
│ · multipath/ATSSS objective-setting scheduler                             │
└───────┬───────────────────────────────────────────────────────────────────┘
        │ E2-style control
┌───────▼────────────────────────────────────────────────────────────────────┐
│ TIER 1 — REAL-TIME (sub-ms to 10 ms)                                       │
│ · classical scheduler / tiny model (0.847 ms measured precedent)           │
│ · MAC scheduling, per-packet multipath assignment                          │
└───────┬────────────────────────────────────────────────────────────────────┘
        │
┌───────▼────────────────────────────────────────────────────────────────────┐
│ 5G/6G NETWORK UNDER TEST                                                  │
│ · RAN: ns-3 + ns-O-RAN (reproducible)  ▸ escalate to srsRAN live testbed   │
│ · CORE: Open5GS (AMF/SMF/UPF/NRF) on Kubernetes                            │
│ · TRANSPORT: SRv6 / segment-routing traffic engineering                    │
│ · EDGE: MEC placement; ATSSS split between 3GPP and non-3GPP access        │
│ · MULTIPATH: MPQUIC/MPTCP scheduler with an objective-passing interface    │
└───────┬────────────────────────────────────────────────────────────────────┘
        │ telemetry
┌───────▼────────────────────────────────────────────────────────────────────┐
│ TELEMETRY & CLOSED-LOOP ASSURANCE                                          │
│ · Prometheus/Grafana + Open5GS KPIs + E2SM-KPM + multipath path metrics    │
│ · SLA scorer: slice-KPI attainment, per-flow latency/jitter/throughput,    │
│   availability, SLA-violation rate and duration, latency-to-recovery,      │
│   cost and energy per remediated incident                                  │
│ · feedback → memory (state history, reasoning exemplars, retraining)       │
└────────────────────────────────────────────────────────────────────────────┘
```

**Design decisions and their justification**

| Decision | Justification from the literature |
|---|---|
| LLM **only** at the non-RT tier | Measured LLM/intent latencies of 8–35 s versus a >1 s non-RT budget; the near-RT SLM precedent is 793 ms and the real-time precedent 0.847 ms |
| Small distilled/quantised model at near-RT | Distillation is the best-evidenced compression family for network tasks (MERLOT, NetKD, distilled intent model); QLoRA-4-bit makes the training feasible on one 24 GB GPU |
| Constrained optimiser as feasibility authority | The "LLM proposes, optimiser disposes" pattern gives hallucination robustness without a separate validator; heuristics are within 1.3× of optimal in the classical placement literature, so the optimiser is a strong baseline too |
| Multipath scheduler connected by an objective-passing interface | Zero papers connect multipath scheduling to O-RAN; the interface limitation is documented by the *Tokens, Not Packets* argument; ATSSS DRL work shows the core-side decision point exists |
| Both simulated (ns-3/ns-O-RAN) and live (srsRAN) evaluation | Reproducibility requires a simulator; credibility requires at least one live demonstration. This mirrors the field's own split and bridges it |
| SLA-level scoring as the primary result | No benchmark found does this for 5G/6G management; it is the single strongest evidence-supported gap |
| Safety and cost as first-class metrics | Only one benchmark found has a normalised cost pillar; the 156× cost spread across models makes cost decisive; no work measures hallucination consequences on a core |

**What I would build first (minimum viable contribution).** A single-domain slice: RAN
(PRB/BWP allocation) + core (UPF selection) on Open5GS + ns-O-RAN, one LLM planner at non-RT,
one DRL controller at near-RT, an SLA scorer, and three baselines (rule-based, DRL-only,
LLM-only). That is enough to answer RQ1 and RQ5 and to produce a defensible first paper. The
multipath leg (RQ3) and the multi-domain leg (RQ4) follow.

---

# WHAT I SHOULD DO NEXT — first 4 to 8 weeks

## Weeks 1–2: close the verification gaps before writing anything

1. **Retrieve the three unread papers whose titles are closest to this proposal**, via
   institutional access, and read them fully before making any novelty claim:
   - *AgentPN Loop: Benchmarking AI Agents for Private 5G/6G Network Management* (SSRN
     10.2139/ssrn.7411918 — blocked by SSRN's 403 during this review)
   - *LLM-Driven Multi-Agent Framework for Autonomous Network Slice Management* (IEEE Xplore
     doc 11573048)
   - *A Feasibility-Shielded Agentic AI Framework for 6G Self-Healing Core Networks* (IEEE
     Xplore doc 11577510)
2. **Retrieve and read SQLLM** (`10.1109/TCE.2026.3657983`) — the largest evidence gap in
   Area 5, and the closest existing work on quantisation for 5G operations.
3. **Retrieve LDOT** (`10.1109/JSAC.2025.3641905`) — the one benchmark paper in IEEE JSAC, and
   the counter-argument I must pre-empt.
4. **Resolve ORION's peer-review status and OperAID's venue** (repository BibTeX and Crossref
   disagree on the latter).
5. **Run a Scopus/Web of Science forward-citation sweep** on NetConfEval, TeleQnA, NIKA,
   NetArena, TSpec-LLM and ORAN-Bench-13K. This review's citation chaining was truncated by API
   rate limits, so this step will very likely surface 2026 work I have not seen.

## Weeks 3–4: build the smallest credible testbed and baseline set

6. **Stand up Open5GS + UERANSIM on Kubernetes** (following the OperAID architecture) and get
   slice-level telemetry flowing. This is the fastest path to a real 5G core I can act on.
7. **Stand up ns-3 with ns-O-RAN** and connect it to the same telemetry/control plane, so the
   RAN and core are evaluated in one loop. This bridging is itself unusual — the two
   communities currently use non-overlapping platforms.
8. **Implement three reference controllers** — rule-based, DRL (PPO or A2C, following the ToN
   2023 formulation), and a flat LLM agent — and **one SLA scorer**. Without the scorer there is
   no experiment.
9. **Define the state/action/reward and the SLA function explicitly and publish them**, so my
   first result is reproducible by construction (the field's central weakness).

## Weeks 5–6: establish the baselines and the negative controls

10. **Reproduce at least one published DRL result** on my testbed before claiming any
    improvement. If I cannot reproduce a published number, that is itself a finding worth
    reporting.
11. **Run the adversarial and degenerate cases deliberately**: an unshielded LLM agent, an
    ambiguous intent, a distribution shift, and a fault the DRL controller was not trained on.
    The field's negative results (cell-edge throughput, greedy-baseline losses, null ablations)
    show this is where honest contributions are made.
12. **Measure latency and cost from day one** — p50/p95 decision latency, tokens, GPU-seconds,
    energy — not as an afterthought.

## Weeks 7–8: the first paper and the model-efficiency leg

13. **Target the first paper at RQ1 + RQ5** (SLA-scored closed-loop agentic slice management
    with an optimiser shield). Realistic venues: IEEE TNSM, IEEE/IFIP NOMS, IEEE CNSM,
    IEEE NetSoft.
14. **Start the Area-5 leg in parallel** because it needs GPU time, not testbed time:
    fine-tune a 7–8B model on 3GPP/O-RAN data with QLoRA on a single 24 GB GPU (the
    ORANSight-2.0 precedent), then distil to 1–3B and quantise, and evaluate all variants on
    the *same* closed-loop task from step 13. That produces RQ2 and RQ9 as a second paper
    (target IEEE TMLCN or IEEE TMC).
15. **Write the related-work section only after steps 1–5 are complete** — the three unread
    2026 papers are the ones most likely to overlap my claim.

## Standing rules for the whole PhD

- **Never state a negative finding as "no one has done this."** State it as "in the papers
  identified through this search, X exists but does not cover Y" — the IEEE Xplore and
  rate-limit outages during this review make over-claiming easy and dangerous.
- **Report the strongest baseline, not the convenient one.** Two Area-1 papers lost to a
  greedy heuristic or failed on cell-edge throughput; a proposal that only compares against
  Kubernetes HPA or static allocation will not survive review.
- **Publish the artifact.** Only 27 of 152 papers in this review had an identified public
  artifact; the canonical DRL multipath scheduler cannot even be read. An open testbed plus
  reference controllers is a contribution in its own right here.
