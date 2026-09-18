# 10 — Gap Report: AI-Native Network Management and Orchestration for 5G/6G

**Scope of evidence:** 152 papers, bibliographically verified against Crossref/OpenAlex,
across five areas. Evidence levels are marked per record (`BIB` / `ABS` / `FULL` / `SUB` —
see `11_search_log.md` §2). Combination counts below are computed from
`07_research_matrix.csv` over the 25 capability flags.

**A caution that applies to every negative statement in this report.** IEEE Xplore returned
HTTP 202 to scripted retrieval throughout, and OpenAlex rate-limited the final discovery
wave. Negative findings therefore mean **"not found in this search"**. They do **not** mean
"does not exist". Where a gap is claimed, the report gives the positive evidence that the
adjacent work exists, so a reader can judge how narrow the remaining hole is.

---

# 1. Executive Summary

**The five areas are largely disjoint, and the intersections are where the contributions
are.**

1. **Flow/packet scheduling in 5G/6G is a mature, DRL-saturated field — and it is
   network-blind.** Dozens of papers learn schedulers for RAN slices, TSN-5G bridges, O-RAN
   traffic steering and UPF selection. Almost all of them optimise a *local* objective
   (PRB efficiency, slice rate, deadline satisfaction, power) and almost none receives an
   objective from, or reports outcomes to, an orchestrator. Only **1** paper in the corpus
   combines flow scheduling + an agent construct + a closed loop.

2. **"Orchestration" is over-claimed.** Applying the A–G classification, the corpus contains
   **no type-(A) true orchestrator implementation**. It splits into framework designs that
   were never deployed, resource-allocation algorithms an orchestrator could call (type B),
   one RAN controller suite (type C), and partially implemented LLM systems (type F). Papers
   routinely labelled "orchestration" contain no service lifecycle management, no descriptor
   onboarding and no management-plane integration.

3. **Multipath scheduling and network orchestration do not meet.** Multipath schedulers are
   endpoint-transport artefacts (MPTCP/MPQUIC kernel or userspace) that learn their own
   objectives. **Zero papers in this corpus combine a multipath scheduler with O-RAN**, and
   the ATSSS/5G-core work that does exist treats splitting as a core-local decision with no
   orchestrator above it. The one paper explicitly arguing that the MPQUIC scheduling
   interface is too narrow to express flow-level intent is a 2026 workshop paper — i.e. the
   field has only just noticed the interface problem.

4. **LLM/agentic network management is real but shallow, and its centre of gravity is
   advisory.** Benchmarks have proliferated (configuration, troubleshooting, telecom
   knowledge, protocol state machines). But **no peer-reviewed benchmark was found that
   evaluates LLM/agent performance on 5G/6G network management with SLA-level outcome metrics
   in a closed loop.** The nearest effort (OperAID, IEEE NetSoft 2026) operates a real 5G
   core but injects Kubernetes-level faults and scores remediation success, not service
   quality. Independent evidence that this matters: TeleCom-Bench (KDD 2026) measures a
   **"universal Execution Wall"** — about 90% on linguistic tasks versus about 30% on
   procedural execution.

5. **Fine-tuning works; compression is barely tested; and nobody measures the thing that
   matters.** Fine-tuned domain models beat general-purpose LLMs on telecom tasks
   (Mobile-LLaMA 247/300 vs GPT-3.5 209/300; TelecomGPT 75.30 vs GPT-4o 38.94 on tdoc
   classification). Distillation is the most consistently successful compression family
   (MERLOT: 660M matches a 7B model at 85–90% less inference time; NetKD: 4.61% of parameters
   at 99.10% of F1). **Pruning evidence is weakest and in one important case misleading** —
   the only work pruning true multi-billion-parameter LLMs evaluates on Wikitext2, not on a
   network task. And **no paper found reports a billion-parameter network-domain LLM
   compressed to a small model with full, reproducible hyperparameters and network-task
   evaluation.** Every model-size-versus-quality trade-off found uses an NLP proxy metric.

6. **Latency is the unaddressed blocker for LLM-in-the-loop network control.** Measured
   values found in this review: NetIntent 20.1–35.1 s per intent; ORION's SMO LLM stage about
   15 s; a chat-driven configuration agent about 8.2–8.6 s per turn; a near-RT O-RAN SLM 793
   ms; an on-device real-time model 0.847 ms. Near-RT RIC budgets are 10 ms–1 s and non-RT is
   >1 s. **The tiering is therefore forced: LLM at the non-RT/SMO tier, distilled small
   models below it, classical/DRL controllers at the fast tier.** Only one paper found
   implements that tiering on a live testbed (a 2026 preprint on srsRAN with four slices).

7. **The single clearest open slot.** An agentic orchestrator that (i) sits in a standard
   management plane (O-RAN SMO / ETSI ZSM), (ii) plans with an LLM but delegates feasibility
   to a constrained optimiser or DRL controller, (iii) drives *both* flow scheduling and
   multipath/ATSSS decisions, and (iv) is evaluated on **SLA-level outcomes** against
   classical optimisation and DRL baselines on a reproducible 5G/6G testbed. Each ingredient
   exists somewhere in the corpus; the composition does not, and — importantly — the
   *evaluation methodology* for it does not either.

---

# 2. Flow Scheduling Landscape

## 2.1 What the field actually contributes

24 papers in `01_flow_schedulers.csv`. Scheduling is a genuine central contribution in about
20 of them; the rest are surveys, architecture papers or placement problems.

| Sub-area | Representative papers | What is decided | Objective |
|---|---|---|---|
| RAN radio-resource scheduling | *Intelligent Resource Scheduling for 5G RAN Slicing* (TVT 2019); *LEASCH* (Access 2020); *DRL for Dynamic UL/DL Resource Allocation* (JSAC 2020); *NRflex* (ComCom 2022) | Resource blocks / bandwidth parts per slice or UE per TTI | Slice rate/QoS satisfaction, spectral efficiency |
| O-RAN traffic steering | *Intelligent O-RAN Traffic Steering for URLLC* (ICC 2023); *Empowering Traffic Steering in 6G Open RAN* (TWC 2024); *Programmable and Customized Intelligence for Traffic Steering* (TMC 2023) | Which access node/interface carries each flow | URLLC latency/reliability, throughput |
| Deterministic / TSN-5G scheduling | *RL-PSO for End-to-End Traffic Scheduling in TSN-5G* (ToN 2023); *DecAge* (TNSE 2024) | Gate-control lists / transmission offsets per flow per link | Deadline satisfaction, schedulable flow count |
| 5G core / user plane | *Power Consumption-Aware 5G Edge UPF Selection using DRL* (NFV-SDN 2024); *Scaling UPF Instances in 5G/6G Core with DRL* (Access 2021); *Dynamic Energy-Efficient UPF Selection* (IFIP Networking 2025) | Which UPF serves each PDU session; how many UPFs to run | Energy subject to latency/bandwidth QoS |
| Traffic engineering in SDN/transport | *Experience-driven Networking* (INFOCOM 2018); DRL-based TE in hybrid IP/SR and SRv6; *SFCPlanner* (TNSM 2024) | Routing / segment lists per flow aggregate | Max link utilisation, delay |
| Service function chaining | *Joint Optimization of SFC and Resource Allocation* (Access 2016); *Latency-Aware SFC Placement* (NetSoft 2019); *Adaptive SFC Scheduling in MEC via DRL* (Access 2020) | VNF placement, chain composition, resources | Latency, resource cost |

## 2.2 What is methodologically solid

- **DRL is the default** (33 of 152 records are DRL-based), with a standard toolkit: DQN
  variants, DDPG, PPO/A2C, and multi-agent variants (MADDPG, MAPPO-class).
- **A minority use hybrid structure wisely.** *Cellular Network Traffic Scheduling with DRL*
  (AAAI 2018) approximates a Lyapunov drift-plus-penalty solution with a learned policy;
  *RL-PSO for TSN-5G* uses RL to guide a metaheuristic. These are the methodological models
  worth imitating, because they inherit feasibility guarantees from the classical structure.
- **A few papers actually specify their setups fully.** *Using Distributed RL for Resource
  Orchestration in a Network Slicing Scenario* (ToN 2023) reports 2–6 flows, 50 Gbps links,
  60 Gbps/60 Gb core nodes, 20 ms/1 ms delay targets, 3–5×10⁴ training episodes, 500 test
  episodes, and per-resource utility metrics. *DeepCC* (TNSM 2021) specifies its 12-dimensional
  state, two-part continuous action, MAPOKTR algorithm, BiLSTM-32 encoder, real Linux testbed
  and `tc`/`ethtool` emulation. These two records carry most of the weights in
  `08_experimental_parameters.csv` for a good reason.

## 2.3 What is weak

- **Objectives are local proxies.** Slice rate, PRB efficiency and deadline satisfaction are
  used instead of end-to-end SLA outcomes. Only the ToN 2023 orchestration paper formalises
  an SLA performance function as a continuous satisfaction score, and even there it is a
  soft score rather than a contract.
- **Simulators are frequently unnamed or bespoke.** Where a simulator is named, the recurring
  choices are ns-3 (+ ns-O-RAN, 5G-LENA), OMNeT++/Simu5G, and Mininet/Containernet for
  control-plane work. A large fraction of Area 1 reports "simulations" with no named platform
  and no artifact, which makes cross-paper comparison impossible.
- **Baselines are weak.** Common baselines are static allocation, an "empirical" heuristic, or
  a re-implementation of a competitor whose state collection the authors admit is undocumented
  (DeepCC's caveat about DRL-CC/SmartCC). Comparisons against a strong classical optimiser
  (MILP/CPLEX or a well-tuned heuristic) are rare — and where they exist (VNF orchestration,
  where the heuristic is within 1.3× of optimal) they set a high bar that learned methods
  often do not clear.
- **No shared testbed, no shared traffic model, no shared scale.** Reported scales range from
  2 flows to hundreds of UEs, and traffic models from Poisson to 3GPP-style to Markov-modulated
  demand. Numbers are therefore not comparable across papers.
- **The network-blindness problem.** A scheduler that cannot be told "this flow is URLLC in
  slice A" cannot serve an SLA. Integration with the orchestrator is exactly what is missing.

## 2.4 Evidence from a dedicated extraction pass over Area-1 candidates

A separate full-text extraction pass over the Area-1 candidate set produced findings that
sharpen the picture above:

- **No paper in that set couples RAN scheduling with 5G Core / QoS-flow scheduling.** The
  RAN-side and core-side scheduling literatures are disjoint. Since end-to-end QoS is enforced
  by a QoS Flow (QFI) that must be honoured across RAN, transport and core, this is the
  clearest structural gap in Area 1.
- **Experimental practice is weak.** Only **one** paper placed a real control-plane component
  in the loop (a production-grade near-RT RIC), and even there the RAN was simulated in ns-3
  via ns-O-RAN. Only **two** papers used any real hardware measurement, and in both it was an
  input to a simulator rather than a live evaluation. **Four papers report no simulator
  identity at all**, and one reports no traffic model at all.
- **Negative results exist and matter.** One traffic-steering study explicitly reports that its
  solution *"does not improve the cell-edge throughput"* relative to a contextual-bandit
  baseline, and triggers more handovers at 42 UEs. One UPF-selection study concedes it **fails
  to beat the strongest greedy baseline** (Overhead-aware Greedy Average) despite beating a
  weaker one, and reports a **null ablation** (power-based versus CPU-based PPO show no
  significant difference because the hosts are identical hardware). One UPF-scaling study
  compares only against Kubernetes HPA, a weak baseline that flatters the learned method.
  These are exactly the results a new proposal must engage with rather than cite selectively.
- **The 5G-TSN sub-field occupies four disjoint niches** (RL-tuned PSO; RL plus analytical
  allocation for wired DetNet; age-of-information-aware multi-agent actor-critic; cooperative
  multi-agent PPO for 5G uplink injection) with **no head-to-head benchmarking across them**,
  so the sub-field's progress cannot be aggregated.

Two candidate titles that circulate in early reading lists were found **not to exist** and were
replaced with verified substitutes: "Toward a Flexible and Reconfigurable 5G Network Slicing
Scheduler" (replaced by *NRflex*) and "Traffic Steering in O-RAN: A Reinforcement Learning
Approach" (replaced by the Globecom Workshops 2023 DDQN steering paper and the VTC2022-Fall
federated meta-learning paper).

## 2.5 The scheduling/orchestration boundary is the interesting place

The only papers in this corpus that connect a scheduler to a higher layer are: *SFCPlanner*
(SRv6 flow steering driven by an online planner), *NRflex* (RIC-driven BWP/numerology control
feeding the MAC scheduler), and the O-RAN traffic-steering xApps. In each case the higher layer
is a **fixed rule or a single-purpose optimiser**, not a learning or agentic policy with a
service-level objective. **No paper found implements a scheduler that receives its objective
from an orchestrator and is evaluated on whether that objective was met.**

---

# 3. Network Orchestration Landscape

## 3.1 The A–G classification applied

Every orchestration paper was classified as: **(A)** true orchestrator implementation,
**(B)** optimisation/learning algorithm an orchestrator could use, **(C)** controller,
**(D)** orchestration architecture/framework design, **(E)** AI agent, **(F)** LLM-based
orchestrator, **(G)** survey/tutorial.

| Type | Count | Papers |
|---|---|---|
| **A — true orchestrator** | **0** | — |
| B — allocation/optimisation engine | 7 | VNF orchestration (TNSM 2016); distributed RL slice resource orchestration (ToN 2023); MARL slice orchestration (MedComNet 2021); intelligent & collaborative slice orchestration (2022); ML-based multi-domain actuation orchestration (2022); SafeSCHEMA (2022); service placement variants |
| C — controller | 1 | RAN slice controller suite (Sensors 2021) |
| D — architecture/framework | 5 | Multi-domain slice orchestration (IEEE Network 2019); zero-touch management & orchestration for 6G (WCM 2022); cloud-native 5G slicing (ComMag 2017); knowledge-defined networking (CCR 2017); AI-driven ZSM (IEEE Network 2020) |
| E — AI agent (non-LLM) | 0 | — |
| F — LLM-based orchestrator | 6 | ARC (ComMag 2025); ORION (preprint 2026); LLM-driven multi-agent slice management (2026); feasibility-shielded self-healing core (2026); LLM intent orchestration for NFV (2026); cross-domain multi-agent LLM orchestration (2025) |
| G — survey/tutorial | 6 | Network service orchestration survey (ComCom 2019); 5G slicing SDN/NFV survey (ComNet 2020); VNF placement survey (COMST 2019); XAI in 6G O-RAN (COMST 2025); resource management 5G→6G (COMST 2024); LLM for communication/network/service management (COMST 2026) |

**The headline: there is no type-(A) true orchestrator implementation in the corpus.** What
the literature calls orchestration is mostly resource allocation (B) or architecture (D). This
is not a quibble: it means the *service lifecycle* functions that define orchestration —
descriptor onboarding, service composition, scaling workflows, SLA assurance — are the parts
that are least implemented and least evaluated.

## 3.2 The six LLM-based orchestrators, and what they actually do

- **ARC** (IEEE ComMag 2025) — **the clearest published LLM-planner + RL-executor design.**
  LLaMA 3.1-8B (not fine-tuned) sequences users and tracks the active objective via RAG with
  chain-of-thought exemplars; Double Dueling DQN agents execute per-action allocations;
  continual RL with gradient-based sample selection prevents forgetting. Evaluated on **10
  nodes and 10 users** in a bespoke simulator with **figure-only results and no numbers**, and
  no external baseline.
- **ORION** (preprint 2026) — the only one placed inside a **standard O-RAN hierarchy**
  (SMO/non-RT RIC/near-RT RIC, A1 and E2, CAMARA slice-booking schema, MCP tools). 100%
  policy-generation success for high-capacity models, but **17% for one mid-tier model**, a
  **156× cost spread**, and about **15 s per SMO-stage call**. Its evaluation stops at valid
  A1 policy generation; it does not measure whether the SLA was met, and the authors rate the
  assurance stage only partially implemented.
- Four further 2025–2026 papers (multi-agent LLM slice management; feasibility-shielded
  6G self-healing core; LLM intent orchestration for NFV; cross-domain multi-agent LLM
  orchestration) were verified bibliographically; three could not be read beyond the abstract
  from open sources.

## 3.3 What is consistently missing

1. **SLA fulfilment is not measured.** Every LLM orchestration paper measures whether the
   intent was *understood* and the policy *generated*. None measures whether the SLA was *met*.
   This is not a small omission — it is the difference between a language task and a control
   task.
2. **Latency is unaddressed.** 8–35 s per decision (ORION, NetIntent, chat-driven configuration)
   versus millisecond-to-second service cadences. The mitigation that the 6G O-RAN tiering
   preprint demonstrates — LLM in non-RT, SLM in near-RT, tiny model in real time — is not yet
   a standard design.
3. **Reliability, not capability, is the frontier.** ORION's dominant error mode was tool
   invocation failure even when intent understanding succeeded. NetIntent found that
   **parameter count does not predict quality** across 33 models. The field is optimising the
   wrong axis when it reports capability only.
4. **The strongest transferable idea is "LLM proposes, optimiser disposes".** Letting a
   constrained optimiser be the feasibility authority gives hallucination robustness without
   a separate validator module — an idea demonstrated for configuration repair but **not yet
   demonstrated inside a standards-compliant O-RAN/ZSM plane**.
5. **Two disjoint communities.** Optimisation-first work (ToN/COMST-style DRL orchestration)
   has no standards mapping, unnamed simulators and no artifacts. LLM-first work has intent
   metrics and no network KPIs. The COMST 2024 resource-management survey states that
   single-domain resource management "reveals its limits", that multi-agent DRL enables
   cross-domain resource allocation "without needing centralized control", and that ETSI ZSM
   "is still not fully supported across all technological domains" — but it covers DRL only,
   **not LLMs**. That adjacency is the open slot.

---

# 4. Multipath Scheduling Landscape

## 4.1 What the field does

29 papers in `03_multipath_schedulers.csv`: four foundational transport papers, the classical
scheduler line (BLEST, ECF, DAPS, low-latency scheduling), the learning-based line (ReLeS,
DeepCC, Peekaboo, RL-based heterogeneous scheduling, multi-agent MPQUIC), the ATSSS/5G-core
line, and interface work.

**The classical baseline set is stable and well-defined**: round-robin / lowest-RTT-first
(default MPTCP), BLEST (blocking estimation), ECF (receive-buffer aware), DAPS (delay-aware).
Any new scheduler is judged against these, on goodput, completion time, jitter/reordering and
buffer occupancy. **This is a genuine methodological strength** compared with Area 1.

**The learning-based line has produced one rigorous, transparent result**: DeepCC
(TNSM 2021) learns congestion control *and* split ratio jointly with multi-agent MAPOKTR in a
real Linux stack, specifying its state (12 dimensions), action (two continuous values per
subflow), reward, architecture (BiLSTM-32 + self-attention) and testbed (`tc`/`ethtool`).
Reported gains: self-attention cuts convergence time ~50% and raises goodput ~80%; four
simultaneous subflows. **Its own limitation is the gap**: the reward is goodput and jitter —
the scheduler has no idea what the network wants.

## 4.2 The measured intersection counts

| Combination | Papers found |
|---|---|
| Multipath + orchestration (loose keyword match) | 15 — **inspection shows these are transport papers that merely mention orchestration concepts; none integrates with an orchestrator** |
| Multipath + LLM | 7 — again keyword-level; no multipath scheduler in this corpus is driven by an LLM |
| Multipath + agent | 7 — all are **RL agents**, not agentic AI |
| Multipath + 5G core (ATSSS) | 5 |
| **Multipath + O-RAN (RIC/xApp)** | **0** |
| Distillation + closed loop | **0** |

## 4.3 Evidence from a dedicated extraction pass over 24 multipath items

A separate full-text extraction pass (19 items read in full, 7 abstract-only) established the
following, with sources:

- **RFC 8684 contains zero occurrences of "scheduler" or "scheduling"** — §3.3.8 leaves packet
  distribution to "any local policy". The standard that defines multipath transport does not
  even name the component the research community spends its effort on. That is the cleanest
  possible statement of why a scheduling interface is missing.
- **No peer-reviewed paper uses an LLM or agent as the multipath scheduler's policy.** The only
  hit found is an IETF draft in which the LLM is the *workload* carried over MPQUIC, not the
  scheduler. "Multi-agent DRL" in this literature (e.g. DeepCC) means one RL agent per subflow,
  **not** agentic orchestration — an important terminological distinction for my write-up.
- **No paper integrates an MPTCP/MPQUIC scheduler with an O-RAN near-RT RIC, xApp or E2.**
  All O-RAN + RL work found is RAN-domain.
- **SDN integration exists but at the wrong granularity.** The only SDN-controller paper (GCLR,
  Floodlight) does flow-level *routing*, not packet scheduling; two 2026 SDN + MARL papers
  operate at subflow/path-assignment granularity. No packet-level scheduler exports policy to
  an orchestrator.
- **The 5G-core multipath anchor is real but coarse.** ATSSS defines a Multipath Transport Proxy
  and a Performance Measurement Function in the UPF, controlled by an SMF policy rule — and
  **no peer-reviewed paper drives it with a learned scheduler**. No free5GC/Open5GS ATSSS + ML
  implementation was found. No paper uses the four standardised ATSSS steering modes as a
  learned action space.
- **Four reasons the gap persists, quotable from the sources.** (i) The RFC never names the
  scheduler. (ii) ATSSS control is deliberately coarse. (iii) Part of the multipath community
  resists ML on explainability grounds for URLLC ("you have 100% reliability until the first
  packet loss happens") and on complexity grounds. (iv) NSDI 2012 pre-emptively rejected
  centralised scheduling at 10 ms granularity on scalability grounds — **an objection any
  AI-native orchestration proposal must answer with measurements, not assertions.**

**Corrections to how these papers are usually cited** (verified in this pass):
- *Peekaboo* (IEEE JSAC 2020) is a **contextual bandit solved with LinUCB (d = 6), not deep RL**.
- *Coupled BBR* (TWC 2021) and *BCCPS* (TVT 2020) **contain no machine learning at all** — they
  are BBR-derived analytical congestion control plus heuristics, and both argue *against* RL.
  They must not be described as AI-native.
- Round-Robin is **not** a baseline in BLEST or ECF (BLEST uses minRTT/DAPS/OTIAS/single-path
  TCP; ECF uses default-minRTT/DAPS/BLEST). It appears only in Peekaboo. This matters if a
  synthesis table is built from memory.
- The energy-efficient MPTCP-RL paper (IEEE Wireless Communications 30(2), 2023) has a
  **flow-level path-set action space**, not per-packet scheduling.
- The protocol commonly mis-cited as "BEWARE" is named **BEMA** in its own abstract; BEWARE is
  an unrelated IEEE ToN paper.

## 4.4 The gap, stated precisely

1. **Endpoint schedulers are network-blind.** They optimise a transport-local objective and
   cannot be told about slices, SLAs, tenants or operator intent. This is not an oversight in
   individual papers; it is a structural consequence of where the scheduler lives (kernel
   socket layer or userspace daemon).
2. **The scheduling interface is too narrow.** The 2026 workshop paper *Tokens, Not Packets*
   argues explicitly that MPQUIC's packet-based interface prevents schedulers from expressing
   flow-level decisions. That is the interface an orchestrator would need to use.
3. **The ATSSS line is the network-side exception, and it stops short.** DRL for access
   traffic splitting in the 5G core and multi-objective RL balancing QoS against ROI show that
   multipath decisions *can* live in the core. Neither connects to an orchestrator, neither
   involves a slice or SLA object, and neither involves an LLM.
4. **Nobody has combined a multipath scheduler with O-RAN.** Zero hits. Given that O-RAN is
   where multi-connectivity policy naturally lives, and that the near-RT RIC is the natural
   home for a multi-path steering control loop, this is the most concrete unexplored
   intersection found in the entire review.

---

# 5. LLM / Agentic Network Management Landscape

36 papers in `04_llm_network_agents.csv` (17 characterised in depth, plus the efficiency
overlap).

## 5.1 What exists, by task

| Task | Maturity | Representative work |
|---|---|---|
| Telecom knowledge / QA | **Mature** | TeleQnA (10,000 MCQs, IEEE Network 2026); LDOT (IEEE JSAC 2026); 6G-Bench; TSpec-LLM (30,137 3GPP docs) |
| 3GPP standards comprehension (RAG) | Maturing | TSpec-LLM; Telco-RAG (GLOBECOM 2024); TelecomRAG (CCR 2025) |
| Network configuration synthesis / repair | Maturing, benchmarked | NetConfEval (CoNEXT 2024, public data); Cornetto; NetConfBench (IETF draft) |
| Intent translation | Maturing, benchmarked | NetIntent / IBNBench (33 models, 1.1B–70B); semantic routing for 5G-core intents (GLOBECOM 2024) |
| Network troubleshooting / RCA | Emerging, benchmarked | NIKA (640 incidents, 54 issues, 30+ MCP tools); FaulT-Bench; SADE |
| Closed-loop 5G-core operation | **Embryonic** | OperAID (NetSoft 2026): Open5GS + UERANSIM on Kubernetes, 900 runs, 70.7% with tools vs 7.1% without |
| Closed-loop 6G management | Preprint only | 6GAgentGym / 6GAgentBench (42 typed tools, NS-3-calibrated surrogate) |
| O-RAN with LLM in the control loop | Preprint / early | ORION (preprint); LLM-xApp (FutureG 2025); 6G O-RAN multi-scale agentic tiering (preprint) |

## 5.2 What the field has actually established

- **Tool access dominates model choice.** OperAID: 70.7% with tools versus 7.1% without;
  best model 93.3%. This is the single most actionable empirical finding in Area 4.
- **Bigger is not reliably better for network decisions.** NetIntent's 33-model study found
  model size does not predict intent-translation quality (a 22B model beat a 35B; 70B models
  were marginal and memory-limited), and one 70B model had perfect recall but 52 false
  positives. A separate study found an 8B model outperforming larger ones within a family. A
  third found a QLoRA-tuned 1B model **failing to beat a Random Forest** on an IoT intrusion
  task (F1 0.7124 vs 0.7159). The relationship between scale and network-decision quality is
  **unresolved and non-monotonic**.
- **An execution wall exists and is measured.** TeleCom-Bench (KDD 2026), built from real
  operator agent trajectories (22,678 samples, six tasks): ~90% on linguistic tasks, ~30% on
  procedural execution. This is third-party confirmation that "understands the intent" and
  "performs the action" are different problems.
- **Safety and robustness are only starting to be measured.** Tele-LLMs reach ~90%
  harmfulness after telecom fine-tuning (SafeCOMM, WCNC 2026); indirect prompt injection
  achieves an 82.5% unsafe tool-action rate in one network-ops benchmark; agents
  over-diagnose on healthy networks (FaulT-Bench); hallucinated root causes occur in up to 40%
  of reports for the weakest model in one RCA benchmark.
- **Cost is rarely first-class.** Only one benchmark found has a fully normalised cost pillar;
  ORION reports a 156× cost spread across models, which is the kind of number that decides
  deployability.

## 5.3 The question that was asked directly: is there a proper benchmark?

**Answer: yes for networking and telecom in general; no for 5G/6G network management with
SLA-level outcomes in a closed loop.**

Based on the papers identified through this search, I found **~30 benchmark efforts**
(NetConfEval, NetArena, NetConfArena, NIKA, FaulT-Bench, NetEval, TeleQnA, LDOT, TSpec-LLM,
TeleCom-Bench, TelAgentBench, TeleMath, TeleTables, 6G-Bench, ORAN-Bench-13K, ORANSight-2.0,
PSMBench, OperAID, 6GAgentGym, α³-Bench, NetInjectBench, WirelessOptBench, ORCA-bench,
Cornetto, NetLLMBench, ITBench, AIOpsLab, RCAEval, OpenRCA, SREGym, GSMA Open-Telco), of which
they evaluate:

- **configuration correctness** (NetConfEval, NetConfArena, Cornetto, NetConfBench) — against
  reference configurations, without deployment;
- **troubleshooting/diagnosis accuracy** (NIKA, FaulT-Bench, ORCA-bench) — on IP/data-centre
  networks, scoring detection/localisation/root-cause, not service quality;
- **telecom knowledge** (TeleQnA, LDOT, 6G-Bench, TSpec-LLM) — static MCQ or QA;
- **agent task correctness and safety** (NetArena, OperAID, α³-Bench, NetInjectBench) — on
  IP/K8s/UAV scenarios;
- **protocol reasoning** (PSMBench) — state-machine reasoning over RFCs.

and they do **not** cover:

1. **Closed-loop execution at the 3GPP protocol level** against 5G core NFs (AMF/SMF/UPF/NRF),
   a RAN (near-RT/non-RT RIC, xApp/rApp) or a slice, exercising NAS/NGAP/PFCP/SBI or E2.
   OperAID is the nearest and its faults are Kubernetes-level.
2. **SLA-level outcome metrics as the primary score** — slice-KPI attainment, per-flow
   latency/jitter, throughput, availability, QoE, or SLA-violation rate. **No benchmark found
   scores these as the primary outcome of agent actions.**
3. **Cost per remediated incident / latency-to-recovery at scale** (only one benchmark has a
   normalised cost pillar; NetConfBench makes cost optional).
4. **Hallucination measured against network-state ground truth**, and the *consequence* of a
   wrong action on a live/emulated core (session drops, slice-isolation breach, signalling
   storms).
5. **Multi-domain / cross-domain orchestration** (RAN + transport + core + edge).
6. **RAN scheduling, spectrum allocation, MEC placement, slice admission and multipath/QoS-flow
   scheduling as agent tasks** with measurable network outcomes.
7. **Dynamic generation for contamination resistance** — only two of the executable benchmarks
   do this; most are static and therefore contamination-prone.

**Do not write "no benchmark exists."** A reviewer will cite NetConfEval, NIKA and NetArena
within a sentence. The defensible statement is the narrow one above, and it is strong enough.

---

# 6. LLM Fine-Tuning and Model Efficiency

36 papers in `05_llm_efficiency_networking.csv`. Answers to the questions asked:

**A. Has anyone fine-tuned an LLM specifically for network management?**
**Yes, in four distinct families**, but the target task is usually analysis or text, not
control: (i) **Mobile-LLaMA** (IEEE Network 2024) — LLaMA-2 13B instruction-tuned on 15,111
instruction sets for 5G network *analysis*; (ii) intent-driven RAN management (QLoRA);
(iii) telecom **troubleshooting** (Ericsson-line work: SFT + LoRA + GRPO on
DeepSeek-R1-Qwen-3-8B); (iv) protocol/control-plane emulation (RRC message generation,
Llama-3/3.2 1B–8B with LoRA).

**B–E. Datasets, tasks, base models, methods.** Sizes span four orders of magnitude: from
**50 SME-validated seed pairs** (edge troubleshooting) to **1,679.5M pre-training tokens**
(TelecomGPT). The dominant method is LoRA/QLoRA SFT. **Two groups explicitly rejected LoRA**:
Tele-LLMs report LoRA "quickly saturates" with extremely low gradient norms on LLaMA-3-8B and
therefore used full fine-tuning; a 5G instruction-pipeline paper "opted not to use LoRA due to
the significant domain shift". This contradiction with the network-domain default is
unresolved.

**F–H. Hardware and cost.** The hardware floor is **much lower than the field implies**:
ORANSight-2.0 QLoRA-4-bit fine-tuned models up to 70B on **151,500 O-RAN instruction pairs on a
single 24 GB RTX 4090** (one epoch). Others: 48 GB A6000 for 7–8B with RFT; 7×A6000; 2×A100-80GB;
8×A100/H200. TelecomGPT instruct-tuning took about **1.5 h on one 8-GPU node**; the Tele-LLMs
series consumed about **5,000 GPU-hours on 8×A6000**.

**I. Inference latency — the unresolved problem.** Measured values: 0.8–3.6 s (RRC message
generation); ~9.4 s (non-RT O-RAN LLM); 793 ms (near-RT SLM); 0.847 ms (on-device real-time
model); 12 ms (a distilled SLM); 0.93 ms per packet (NetKD); sub-100 ms (a distilled optical
model). **Only small or distilled models reach near-RT budgets.**

**J–N. Accuracy and comparisons.** Fine-tuned domain models beat general models on domain
tasks (TelecomGPT 75.30 vs GPT-4o 38.94 on tdoc classification; RRC generation 0.970 vs 0.496
cosine; ROUGE-L 0.55/0.58 vs GPT-4 0.35; Mobile-LLaMA 247/300 vs GPT-3.5 209/300) — **but not
uniformly** (GPT-4o still leads on standard TeleQnA). Reported **network** KPIs do exist in a
few troubleshooting papers: throughput +19.3%, delay −48.5%, energy +54.9%; ~6× faster
troubleshooting; 94.1% vs 82.4% remediation.

**O. Does pruning help?** **Weakest evidence; do not overstate.** Only one work found prunes
true multi-billion-parameter LLMs (LLaMA 7B–65B, Wanda unstructured + 2:4 semi-structured) —
and it evaluates on **Wikitext2, not a network task**, with simulation-only speedups. Citing
it as evidence that pruning preserves network-task quality would be misrepresentation. One
paper combines all four techniques in one pipeline (INT8 QAT+PTQ → structured pruning of
attention heads/FFN at 40/60/75% sparsity → KD → self-distillation): BERT-base 110M/438 MB →
38M/32 MB, Raspberry Pi 4 latency 214.6 → 27.4 ms (−87.3%), but at a small regional venue and
for intrusion detection rather than management.

**P. Does quantization help?** Yes, with a measured cost. The only clean FP16-versus-INT4
ablation on a networking task shows **INT4 reduces median latency 20–30% at a few points of
pass-rate cost, worst on the smallest model** (1B model: 0.989 → 0.883).

**Q. Does distillation help?** **Most consistently successful family.** MERLOT (660M) matches
or beats a 7B model on 8/10 datasets at 85–90% less inference time and memory; a distilled
intent model retains 95% accuracy with 60% lower inference latency; NetKD retains **99.10% of
F1 at 4.61% of parameters with 0.93 ms per packet**.

**R. Does fine-tuning actually improve network-management performance?** On *text and analysis*
tasks, clearly yes. On *network management decisions*, **the question is essentially
unanswered** — the benchmarks used are code-generation rubrics, QA accuracy and
classification F1. A rare negative result: a QLoRA-tuned 1B model on an IoT intrusion dataset
scored F1 0.7124 versus a Random Forest's 0.7159.

**S. Is there a model-size versus network-decision-quality trade-off curve?** **No.** Every
trade-off found uses an NLP proxy metric. **No paper retrieved reports a billion-parameter
network-domain LLM compressed into a small model with full, reproducible compression
hyperparameters and a network-task evaluation.** The well-documented compressions (MERLOT,
Pruned Traffic Trees, NetKD, the four-technique pipeline) all operate on ≤120M-parameter
models; the papers that compress genuine LLMs each withhold a critical piece (temperature/α,
teacher/student sizes, hardware, or network-task evaluation). **This is the cleanest empirical
hole in Area 5.**

---

# 7. Benchmark Landscape

See §5.3 for the full answer. Summary table of what is covered where:

| Dimension | Covered by | Missing from |
|---|---|---|
| Configuration correctness | NetConfEval, NetConfArena, Cornetto, NetConfBench | Deployment and outcome measurement |
| Troubleshooting accuracy | NIKA, FaulT-Bench, ORCA-bench | 5G/6G core and RAN; service-level scoring |
| Telecom knowledge | TeleQnA, LDOT, 6G-Bench, TSpec-LLM, TeleMath, TeleTables | Everything operational |
| Agent tool use / procedure | NetArena, OperAID, TeleCom-Bench | 3GPP protocol-level actions; SLA outcomes |
| Safety / injection / hallucination | NetArena, NetInjectBench, FaulT-Bench, α³-Bench, WirelessOptBench | 5G core consequences; hallucination vs network ground truth |
| Cost / latency | α³-Bench (normalised), ORION (per-intent cost), OperAID (per-run cost) | Cost-per-remediated-incident; SLA-per-dollar |
| Closed-loop 5G core | OperAID (K8s-level faults) | 3GPP protocol-level faults; SLA scoring |
| Closed-loop 5G/6G with SLA score | **nothing found** | — |

**Terminology warning for the write-up:** NIKA ≠ NetArena ≠ NetConfArena (three distinct
works); SADE is an *agent evaluated on* NIKA, not a benchmark; two widely-circulated arXiv IDs
are wrong (Tele-LLMs is 2409.05314, not 2409.07452; ORAN-Bench-13K is 2407.06245, not
2406.12398). One frequently cited "Telco-LLM"/"TelecomLLM"/"LLaMA-Telecom" paper **does not
exist** as a publication.

---

# 8. Experimental Platforms

What each platform is actually used for in the papers found, and what that implies for my
experimental plan.

| Platform | Used in this corpus for | Strengths | Limits for my work |
|---|---|---|---|
| **ns-3** | Flow/packet-level simulation; RAN scheduling and traffic steering studies. **ns-O-RAN** extends ns-3 to model O-RAN (E2, near-RT RIC, xApps); **5G-LENA** provides NR PHY/MAC. | Open, scriptable, well-validated for packet-level behaviour; the standard for reproducible 5G RAN simulation. | No real 5G core; O-RAN support is a research extension; no container/cloud-native semantics. |
| **OMNeT++ / Simu5G** | End-to-end 5G system simulation (Simu5G is an OMNeT++ library for 5G NR and core-ish functionality); used for flow-scheduling and multipath evaluations. | Mature discrete-event framework; Simu5G gives an integrated 5G stack; good for large parameter sweeps. | Less common in recent AI-native work; integrating an agent loop is bespoke work. |
| **Mininet / Containernet** | SDN and control-plane experiments; NetIntent used Mininet with OpenDaylight/ONOS; several orchestration papers use it for slice/controller prototypes. | Fast, lightweight, realistic control-plane APIs (real OpenFlow controllers). | No real 5G core or RAN; data-plane fidelity is limited. |
| **Open5GS** | Real 5G core in closed-loop and testbed work — OperAID runs Open5GS + UERANSIM on Kubernetes; ORION deploys Open5GS on Kubernetes. | Open-source, 3GPP-aligned 5G core (AMF/SMF/UPF/NRF…); runs in containers so it composes with cloud-native tooling. | Not a RAN; performance limits under load; needs Kubernetes plumbing. |
| **UERANSIM** | The UE/gNB simulator paired with Open5GS to create a complete signalling path. | Completes the core testbed cheaply; supports real NAS/NGAP signalling. | Simulated RAN — no real radio, limited PHY realism. |
| **srsRAN** | Live RAN testbeds: the multi-scale O-RAN agentic preprint runs a live testbed "based on srsRAN with four active slices"; srsRANBench evaluates LLM code generation on the srsRAN codebase. | Open-source, runs on SDR hardware, gives a real RAN with real slicing. | Requires SDR/USRP hardware and RF isolation; steep operational learning curve. |
| **OpenAirInterface (OAI)** | Full open-source 4G/5G RAN+core implementations used across the O-RAN research community (referenced broadly; less prominent in this specific corpus). | Most complete open stack; widely used with O-RAN Software Community components. | Heavy; real-time requirements; hardware-dependent. |
| **O-RAN Software Community (OSC) / O-RAN SC** | Reference near-RT RIC, xApps, SMO implementations used for O-RAN prototypes; ORION-style work and xApp studies build on O-RAN interfaces (A1/E2/O1). | Standards-aligned interfaces; enables genuine xApp/rApp development. | Integration effort is high; documentation and release quality vary. |
| **Kubernetes** | Cloud-native 5G core deployment and orchestration: OperAID and ORION both deploy Open5GS on Kubernetes; cloud-native slicing architectures assume it. | Realistic cloud-native substrate; enables fault injection at the infrastructure level; supports scaling and lifecycle actions an agent can actually take. | Not 3GPP-aware by itself — an agent acting on Kubernetes is not (yet) doing 3GPP management, which is exactly the OperAID limitation. |
| **Real private-5G testbeds** | Live evaluation with real UEs, real radio and real slices — the multi-scale O-RAN tiering preprint (srsRAN, four slices, E2SM-KPM telemetry); Colosseum/OpenRAN Gym-class platforms for xApp studies. | Highest fidelity; the only way to measure genuine SLA outcomes under real radio variability. | Cost, access, and reproducibility constraints; results are hard for others to reproduce. |

**Cross-cutting observation.** The Area 4 work clusters on **Kubernetes + Open5GS + UERANSIM**
(cheap, cloud-native, weak on radio and on 3GPP protocol semantics), while the Area 1 work
clusters on **ns-3 / OMNeT++/Simu5G** (good packet-level fidelity, no real core, no agent
interface). **The two communities use non-overlapping platforms — which is a mechanical reason
why closed-loop, SLA-scored, cross-layer agent evaluation does not yet exist.** A testbed that
bridges them (e.g. ns-3 or srsRAN for the RAN + Open5GS for the core + a controller/orchestrator
above both) is itself a contribution.

---

# 9. Cross-Area Matrix

Combination counts over the 152 verified records (from `07_research_matrix.csv`). Because the
matrix flags are computed by keyword and structured-field matching, small counts are inspected
individually and annotated.

| Combination | Count | Inspection |
|---|---|---|
| Flow scheduling (any) | 52 | broad keyword match; 24 are genuine Area-1 contributions |
| Orchestration (any) | 57 | broad match; 26 are genuine Area-2 contributions |
| Multipath | 30 | 29 genuine Area-3 contributions |
| DRL | 39 | the dominant AI method in the corpus |
| LLM | 83 | includes all knowledge/benchmark work |
| Agent (any) | 42 | includes RL-agent usages |
| Multi-agent | 9 | mostly multi-agent DRL, a few multi-agent LLM |
| RAG | 8 | telecom standards RAG + ARC + ORION |
| Tool calling | 4 | NetConfEval-adjacent, NIKA, OperAID, ORION, 6GAgentGym-class |
| Fine-tuning | 28 | telecom domain adaptation |
| LoRA / QLoRA | 11 / 4 | the default PEFT methods |
| Pruning | 4 | **and only one prunes a true billion-parameter LLM, on a non-network task** |
| Quantization | 8 | one clean ablation on a networking task |
| Distillation | 10 | the best-evidenced compression family in this domain |
| O-RAN | 14 | RAN-side work |
| 5G core | 14 | UPF/AMF/SMF/ATSSS-focused work |
| 6G | 24 | mostly vision/architecture, few implementations |
| Network slicing | 31 | slicing is the common framing across all areas |
| Closed loop | 25 | mostly conceptual or RL loops |
| Testbed | 17 | real-hardware work |
| Simulator | 18 | named simulators only; many papers report unnamed simulation |
| Benchmark | 29 | Area-4 benchmark efforts |
| Open code | 27 | public repositories identified |

## The intersection table that matters

| Intersection | Count | What it means |
|---|---|---|
| **Multipath + O-RAN** | **0** | Multi-connectivity policy has never been coupled to the RIC/xApp ecosystem in this corpus. |
| **Distillation + closed loop** | **0** | Compression is studied for classification and QA; never for a model that closes a control loop. |
| **Flow scheduling + agent + closed loop** | **1** | Essentially one point of contact between Area 1 and Area 4. |
| **LLM + 5G core + closed loop** | **2** | Both are OperAID (conference + repository records of the same work), with Kubernetes-level faults. |
| **Benchmark + 5G core + closed loop** | **2** | Same work. |
| **RAN scheduling + 5G core QoS-flow scheduling (in one system)** | **0** | The RAN-side and core-side scheduling literatures never meet, although end-to-end QoS requires exactly that coupling. |
| **Multipath + 5G core** | 5 | The ATSSS line — core-local splitting, no orchestrator. |
| **LLM + orchestration + closed loop** | 5 | ARC, ORION and three abstract-level 2026 papers. |
| **Fine-tuning + closed loop + LLM** | 6 | Domain-adapted models used, but the loops are mostly non-RT. |
| **Slicing + LLM + closed loop** | 2 | ORION and one abstract-level paper. |

**Reading of the table.** Every pairwise intersection that a reviewer would consider
"obviously related" is either empty or contains one or two papers, and those papers are
typically preprints or abstract-level records. The composition proposed in §11 is therefore
not a crowded space — but neither is it unexplored territory: the *ingredients* are all
published, so the contribution must be the composition, the interface, and above all the
**evaluation methodology**, not the claim that "no one has used an LLM for networks".

---

# 10. Research Gaps

Each gap below states the **existing evidence** (what exists), what those papers **do not**
do, why it matters, and how it could be attacked. Gaps are ordered by how strongly the
evidence supports them, not by ambition.

---

## GAP-1 — No SLA-scored, closed-loop agent benchmark for 5G/6G network management

**Existing evidence.** ~30 benchmark efforts were found: NetConfEval (configuration,
CoNEXT 2024), NIKA (troubleshooting, 640 incidents, public dataset), NetArena (dynamic
generation, ICLR 2026), OperAID (real 5G core on Kubernetes, NetSoft 2026), TeleQnA/LDOT/6G-Bench
(telecom knowledge), TeleCom-Bench (live operator trajectories, KDD 2026), PSMBench (protocol
state machines, NeurIPS D&B 2025). Executable closed-loop evaluation exists.

**What they do NOT do.** None scores **SLA-level network outcomes** — slice-KPI attainment,
per-flow latency/jitter, throughput, availability, QoE, SLA-violation rate — as the primary
result of agent actions. None executes against 5G core NFs or a RAN at the 3GPP protocol
level (NAS/NGAP/PFCP/SBI, E2). OperAID comes closest and its faults are Kubernetes-level.

**Why it matters.** Without SLA scoring, the field cannot answer whether agents *manage* the
network or merely *describe* it. TeleCom-Bench's measured ~90%/-30% execution wall shows the
distinction is real and large.

**Potential research question.** *Can an agentic controller achieve and maintain SLA targets
on an emulated 5G core + RAN under dynamic load, and how does its SLA-violation rate compare
with a DRL controller and a classical optimiser?*

**Possible experiment.** Build a benchmark of dynamically generated service incidents and load
scenarios over Open5GS (core) plus a RAN (ns-3/ns-O-RAN or srsRAN), with an SLA-scoring harness
that reads real telemetry and computes slice-KPI attainment, SLA-violation rate,
latency-to-recovery and cost-per-remediation.

**Baselines.** Static/rule-based policy; DRL slice controller (published, e.g. distributed
A2C or PPO variants); classical optimisation (MILP/heuristic as in the VNF-orchestration line);
LLM-only agent; LLM-planner + optimiser hybrid.

**Metrics.** SLA satisfaction ratio; SLA-violation rate and duration; latency-to-recovery;
action cost (tokens and currency) per remediated incident; safety violations; statistical power
across repeated runs.

**Venue.** IEEE TNSM; IEEE/IFIP NOMS or CNSM; IEEE NetSoft; IEEE INFOCOM; ACM CoNEXT.

---

## GAP-2 — No model-size / compression versus network-decision-quality trade-off

**Existing evidence.** Distillation is shown to work for network tasks (MERLOT 660M ≈ 7B at
85–90% less cost; NetKD 4.61% of parameters at 99.10% of F1; a distilled intent model at 95%
accuracy and −60% latency). Quantization has one clean networking ablation (INT4: −20–30%
latency at a few points of pass-rate cost). Pruning has none on a network task.

**What they do NOT do.** No paper reports compressing a billion-parameter network-domain LLM
into a small model with full, reproducible compression hyperparameters **and** evaluating the
network task. Every size-versus-quality curve found uses an NLP proxy metric.

**Why it matters.** Latency is the binding constraint for placing models in network control
loops (ORION ~15 s; NetIntent 20–35 s; near-RT budget 10 ms–1 s). Quantifying the accuracy cost
of the compression needed to hit those budgets is a prerequisite for deployment.

**Potential research question.** *What is the accuracy-versus-latency Pareto frontier for
network-management LLMs under distillation, quantization and structured pruning, measured on
network-decision quality rather than text similarity?*

**Possible experiment.** Take an open network-management LLM (fine-tuned on 3GPP/O-RAN data);
apply distillation to 1B–3B students, INT8/INT4 quantization, and structured pruning at
several sparsity levels; evaluate each variant on the same closed-loop management task from
GAP-1, reporting SLA outcomes, decision accuracy, latency and memory.

**Baselines.** Uncompressed teacher; the same task solved by a DRL controller and by a
classical optimiser; a general-purpose model of equal size.

**Metrics.** SLA satisfaction; decision accuracy against expert/optimiser references;
p50/p95 inference latency; VRAM; cost per decision.

**Venue.** IEEE TMLCN; IEEE TNSM; IEEE TMC; IEEE JSAC; MLSys/NeurIPS D&B for the benchmark
artefact.

---

## GAP-3 — Multipath scheduling has never been connected to network orchestration or O-RAN

**Existing evidence.** 29 multipath papers: classical schedulers (BLEST, ECF, DAPS, low-latency
MPTCP), learning schedulers (ReLeS, DeepCC, Peekaboo, RL/MPQUIC variants), ATSSS/core-side
splitting (DRL access traffic splitting; multi-objective RL for QoS vs ROI), and one 2026 paper
arguing the MPQUIC scheduling interface is too narrow to express flow-level intent.

**What they do NOT do.** No paper found integrates a multipath scheduler with an orchestrator,
a slice object, an SLA, or **O-RAN** (zero hits). Endpoint schedulers cannot receive a
network-level objective; core-side splitters do not consult one.

**Why it matters.** Multi-connectivity is a first-class 5G/6G capability. If path selection is
made without service-level context, then URLLC and eMBB traffic compete identically, and slice
isolation cannot be enforced at the path layer.

**Potential research question.** *If an orchestrator supplies per-flow objectives to a multipath
scheduler (weight, deadline, slice identity), does SLA attainment improve over
objective-blind scheduling, and what interface is required to carry that objective?*

**Possible experiment.** Extend an open MPTCP/MPQUIC scheduler with an objective-passing
interface (a token/weight API informed by the *Tokens, Not Packets* argument); drive it from a
slice-aware controller and an agentic planner; evaluate on a testbed with emulated
heterogeneous paths, plus an in-core ATSSS variant.

**Baselines.** Round-robin and lowest-RTT-first; BLEST; ECF; DeepCC; objective-blind DRL
scheduler.

**Metrics.** Per-flow/slice latency percentiles; SLA-violation rate; goodput; reordering and
buffer occupancy; fairness across slices; objective-passing overhead.

**Venue.** IEEE/ACM ToN; IEEE TNSM; IEEE INFOCOM; ACM CoNEXT; ACM SIGCOMM (if the interface
contribution is strong).

---

## GAP-4 — No agentic orchestration across RAN + transport + core + edge

**Existing evidence.** Single-domain orchestration is well covered (slicing, VNF placement,
RAN control). Multi-domain work exists architecturally (multi-domain slice orchestration,
COMST surveys, ML-based multi-domain actuation orchestration) and the COMST 2024 survey states
that end-to-end multi-domain resource management remains open and that ETSI ZSM "is still not
fully supported across all technological domains". ORION covers a single RAN domain; ARC covers
space/air/ground but evaluates at 10 nodes/10 users.

**What they do NOT do.** No paper found demonstrates a closed-loop agent orchestrating across
RAN, transport, core and edge **simultaneously** with a single service-level objective, nor
benchmarks cross-domain orchestration with SLA scoring.

**Why it matters.** End-to-end SLAs are inherently cross-domain; a violation can originate in
any segment, and per-domain optimisers can cancel each other out.

**Potential research question.** *Does a hierarchical agentic orchestrator (LLM planner over
per-domain DRL controllers) achieve higher end-to-end SLA attainment across RAN+transport+core
than per-domain optimisation alone, and how much inter-domain signalling does it require?*

**Possible experiment.** Instantiate per-domain controllers (RAN slice controller on ns-3 or
srsRAN; SRv6/segment-routing TE controller; UPF selection/scaling controller in Open5GS; MEC
placement) with an LLM planner above them that composes end-to-end policies and resolves
cross-domain conflicts; inject cross-domain faults and load shifts.

**Baselines.** Per-domain independent optimisation; a single centralised optimiser with full
information (upper bound); a flat single-agent LLM controller; a MARL controller.

**Metrics.** End-to-end SLA attainment; cross-domain conflict count and resolution time;
inter-domain message overhead; convergence/stability under churn; fairness across tenants.

**Venue.** IEEE TNSM; IEEE JSAC; IEEE COMST (if framed as a systematic study); IEEE NOMS/CNSM.

---

## GAP-5 — "LLM proposes, optimiser disposes" has not been demonstrated inside a standards-compliant management plane

**Existing evidence.** Hybrids exist individually: ARC (LLM sequencer + D3QL executors),
RL-PSO for TSN-5G (RL guiding a metaheuristic), DRL for UPF selection with QoS constraints,
SafeRL for multi-domain slices, a feasibility-shielded agentic 6G self-healing framework
(abstract-level), and LLM-based optimisation-algorithm selection. Configuration-repair work
uses an ILP as the feasibility authority.

**What they do NOT do.** No paper demonstrates the hybrid **inside O-RAN SMO/non-RT RIC with
A1/E2 enforcement** (ORION puts the LLM there but keeps the optimiser out), and no paper
reports SLA outcomes for the hybrid versus the optimiser alone.

**Why it matters.** This is the most credible route to safe LLM control: the LLM contributes
generality and intent understanding; the optimiser guarantees feasibility, so hallucination
cannot produce an infeasible action. It converts "is the LLM reliable?" into "is the LLM a
better *objective formulator* than a fixed rule?", which is a tractable research question.

**Potential research question.** *Does LLM-based objective and constraint formulation, with a
constrained optimiser as the feasibility authority, outperform both the optimiser alone and a
flat LLM controller on SLA attainment and feasibility violations?*

**Possible experiment.** Implement three controllers on the same testbed: (a) optimiser alone
with hand-tuned objectives; (b) flat LLM agent issuing actions; (c) LLM producing objectives
and constraints for the optimiser, which returns a feasible plan. Evaluate under distribution
shift and adversarial/ambiguous intents.

**Baselines.** (a) and (b) above; SafeRL controller; rule-based O-RAN policy.

**Metrics.** SLA attainment; infeasibility rate; safety/shield activation rate; decision
latency; cost; recovery time after distribution shift.

**Venue.** IEEE TNSM; IEEE JSAC; IEEE INFOCOM; IEEE NetSoft; IEEE CNSM.

---

## GAP-6 — Latency-feasible tiering of LLM agents across RAN control loops is unstandardised

**Existing evidence.** Measured latencies: 0.847 ms on-device, 12 ms distilled SLM, 793 ms
near-RT SLM, ~9.4 s non-RT LLM, ~15 s ORION SMO stage, 20–35 s NetIntent. One 2026 preprint
implements a three-tier deployment on an srsRAN testbed with four slices (LLM in non-RT, SLM in
near-RT, tiny model in real time) and reports VIP throughput +6% at preserved 22 ms latency.

**What they do NOT do.** There is no systematic study of *which* management functions can be
delegated to which tier, no standard interface between tiers, and no quantified accuracy loss
from moving a function down a tier.

**Why it matters.** It determines what agentic network management can actually be deployed for,
and it is the practical answer to the "LLMs are too slow" objection.

**Potential research question.** *For each 5G/6G management function, what is the highest
control-loop tier at which it can be executed while meeting the loop's latency budget, and what
is the SLA cost of the required model compression or delegation?*

**Possible experiment.** Build a latency-budget matrix of management functions (slice
admission, PRB allocation, traffic steering, UPF selection, fault remediation) × tiers (real
time, near-RT, non-RT) and measure, for each cell, achieved latency and decision quality with
progressively compressed models, on a live or emulated testbed.

**Baselines.** A single-tier deployment; a classical controller at each tier.

**Metrics.** Per-tier p50/p99 latency versus budget; decision-quality loss versus the
non-compressed model; SLA outcomes; cost per decision.

**Venue.** IEEE TMC; IEEE TNSM; IEEE INFOCOM; IEEE ICC/GLOBECOM.

---

## GAP-7 — Safety, hallucination and the *consequences* of wrong actions are unmeasured for 5G/6G agents

**Existing evidence.** Safety work exists off-core: NetInjectBench (indirect prompt injection;
82.5% naive unsafe tool-action rate), NetArena (step-wise safety decoupled from correctness),
FaulT-Bench (agents over-diagnose on healthy networks), α³-Bench (safety policy pillar),
WirelessOptBench (unsafe-apply rate), ORCA-bench (hallucinated root causes in up to 40% of
reports); SafeCOMM (safety degrades to ~90% harmfulness after telecom fine-tuning); Tele-LLMs.

**What they do NOT do.** None measures hallucination against network-state ground truth on a
5G core or RAN, and none measures what a wrong action *does* — dropped sessions, slice-isolation
breach, signalling storms, charging corruption.

**Why it matters.** An operator will not deploy an agent whose worst case is unbounded, however
good its average case is.

**Potential research question.** *What is the blast radius of an incorrect agent action on a
5G core, and can a feasibility shield plus a verified action set reduce it to zero while
preserving most of the agent's benefit?*

**Possible experiment.** Define a taxonomy of incorrect actions (wrong NF, wrong slice, wrong
parameter magnitude, unsafe scale-down), inject each on an emulated core, measure the service
impact, then evaluate a shielded agent (optimiser-verified actions only) against an unshielded
one.

**Baselines.** Unshielded agent; rule-based controller; DRL controller.

**Metrics.** Service-impact severity per incorrect action class; number of prevented unsafe
actions; false-block rate; residual SLA attainment.

**Venue.** IEEE TNSM; IEEE CNSM; IEEE NetSoft; IEEE INFOCOM; ACM CoNEXT.

---

## GAP-8 — Reproducibility in this subfield is poor, and a reproducibility-first contribution is available

**Existing evidence.** ReLeS — the canonical DRL MPTCP scheduler — is closed access with no
arXiv version, no author PDF and no code, so its state/action/reward cannot be verified or
compared. DeepCC's baseline comparison is weakened because the baseline code was unavailable
and had to be re-implemented. Several Area-1 papers report "simulation" with no named platform
and no artifact. Only 27 of 152 records have an identified public artifact. ARC reports results
as two figures with no numbers.

**What they do NOT do.** There is no open, reproducible DRL/LLM network-control baseline suite
that other researchers can extend.

**Why it matters.** Without shared baselines and published state/action/reward definitions,
results cannot be compared, and the field cannot accumulate.

**Potential research question.** *Can a fully open, documented and reproducible
agentic-network-control testbed with published state/action/reward definitions and reference
trajectories become the comparison point for future work?*

**Possible experiment.** Release: a containerised testbed (Open5GS + RAN emulation +
controller), a scenario generator, an SLA-scoring harness, several reference controllers
(rule-based, DRL, LLM-planner-hybrid) and full telemetry traces.

**Baselines.** Not applicable — this *provides* baselines.

**Metrics.** Artefact reuse by third parties (citations, forks); reproduction error versus
published numbers.

**Venue.** IEEE TNSM; ACM CoNEXT/IMC (artefact tracks); IEEE NetSoft; ACM SIGCOMM CCR.

---

## GAP-9 — The fine-tuning recipe for network *decision* quality is unknown

**Existing evidence.** Domain adaptation clearly helps on text/analysis tasks
(Mobile-LLaMA 247/300 vs GPT-3.5 209/300; TelecomGPT 75.30 vs GPT-4o 38.94; RRC generation
0.970 vs 0.496). QLoRA makes 70B specialisation feasible on a single 24 GB GPU (ORANSight-2.0,
151,500 instruction pairs). But Tele-LLMs rejected LoRA as saturating; another group rejected
it for domain shift; and a QLoRA-tuned 1B model lost to a Random Forest on an intrusion task.

**What they do NOT do.** No paper measures whether fine-tuning improves **network-management
decisions** (SLA attainment, decision optimality) as opposed to text/analysis quality, and none
compares LoRA versus full fine-tuning on that axis.

**Why it matters.** If fine-tuning does not improve control decisions, a large part of the
current research agenda is misdirected — and conversely, if it does, the recipe matters a great
deal.

**Potential research question.** *Does domain fine-tuning improve the quality of network
management decisions, and under what adaptation method and data scale?*

**Possible experiment.** Train a 7–8B model under four regimes (no adaptation, LoRA, QLoRA,
full SFT) on identical network-management instruction data at three data scales (50, 5k, 50k
examples); evaluate each on the same closed-loop task against a DRL controller.

**Baselines.** Unadapted model; DRL controller; classical optimiser; Random Forest/tree
baselines on any classification sub-task (to guard against the reported negative result).

**Metrics.** SLA attainment; decision optimality gap versus the optimiser; p95 latency; GPU
hours; cost per decision.

**Venue.** IEEE TMLCN; IEEE TNSM; IEEE TMC; IEEE ICC/GLOBECOM.

---

## GAP-10 — Cost and energy of agentic control are not first-class metrics

**Existing evidence.** ORION reports a **156× cost spread** across models (0.19¢ to 29.68¢ per
intent, equivalent to $694–$108,332/year at 10,000 intents/day); OperAID reports per-run cost;
α³-Bench is the only benchmark found with a fully normalised cost pillar; energy-aware
decisions exist in the network domain (UPF selection for power, energy-efficient MPTCP
scheduling, multi-objective RL balancing QoS against ROI).

**What they do NOT do.** No benchmark reports **cost per remediated incident** or
**SLA-attainment-per-dollar**, and no work measures the **energy footprint of the AI control
plane itself** alongside the energy it saves in the network.

**Why it matters.** 6G has explicit energy-efficiency targets, and an agentic control plane
that saves 10% of network energy while consuming more than that in inference is a net loss.
The 156× cost spread shows the design choice is economically decisive.

**Potential research question.** *What is the net energy and monetary cost of agentic 5G/6G
management (including inference) per unit of SLA improvement, and how does it compare with
classical and DRL control?*

**Possible experiment.** Instrument the GAP-1 testbed to measure inference energy and cost
(model, tokens, GPU-seconds) alongside network energy and SLA outcomes; compare controllers on
net cost per SLA point.

**Baselines.** Rule-based control (near-zero inference cost); DRL control (small-model
inference); LLM-only; hybrid.

**Metrics.** Net energy (J) and monetary cost per SLA point; cost per remediated incident;
energy overhead ratio (control plane versus network savings).

**Venue.** IEEE TNSM; IEEE TMC; IEEE TMLCN; IEEE ICC/GLOBECOM (green communications tracks).

---

# 11. Candidate PhD Research Questions

Ten questions, each with the full apparatus needed to execute it. The three marked ★ are the
ones I would defend first.

---

### RQ1 ★ — SLA-scored closed-loop agentic management of a 5G/6G network

- **Motivation.** No peer-reviewed benchmark found evaluates LLM/agent performance on 5G/6G
  management with SLA-level outcomes in a closed loop (§5.3, §10 GAP-1).
- **Literature evidence.** NetConfEval, NIKA, NetArena, OperAID, TeleCom-Bench exist;
  TeleCom-Bench's execution wall quantifies the gap.
- **Hypothesis.** An agentic controller, constrained by a feasibility authority, achieves a
  materially lower SLA-violation rate than a flat LLM controller and approaches a DRL
  controller, while generalising to unseen incident types where the DRL controller does not.
- **System architecture.** Telemetry (Prometheus/Open5GS KPIs + RAN KPIs) → state builder →
  LLM planner (non-RT tier) → objective/constraint formulation → constrained optimiser or DRL
  controller (near-RT tier) → actuation via Kubernetes/Open5GS APIs and RIC E2 → SLA scorer →
  feedback to memory.
- **Experiment.** Dynamic scenario generator (load shifts, slice-demand changes, injected
  faults); hundreds of episodes across several SLA profiles; repeated runs for statistical
  power.
- **Baselines.** Rule-based; DRL slice controller; classical MILP/heuristic; flat LLM agent.
- **Metrics.** SLA satisfaction ratio; violation rate and duration; latency-to-recovery;
  cost per incident; safety violations.
- **Required tools.** Open5GS, UERANSIM, Kubernetes, ns-3/ns-O-RAN or srsRAN, Prometheus/Grafana,
  an open 7–8B LLM, vLLM for serving.

### RQ2 ★ — Model-size versus network-decision-quality trade-off under compression

- **Motivation.** Latency blocks LLM-in-the-loop control; no size-versus-quality curve exists
  for network decisions (§6, §10 GAP-2).
- **Literature evidence.** MERLOT, NetKD, distilled intent model, INT4 ablation, ORANSight-2.0
  (single-GPU 70B QLoRA), the three-tier O-RAN deployment preprint.
- **Hypothesis.** Distillation to 1–3B plus INT8 quantization preserves network-decision quality
  within a small margin while meeting near-RT latency budgets; structured pruning degrades
  decision quality faster than distillation at equal compression.
- **Architecture.** Teacher (fine-tuned 7–8B network model) → distillation/quantization/pruning
  variants → identical closed-loop evaluation harness.
- **Experiment.** Four compression families at matched compression ratios, evaluated on the
  RQ1 task plus an offline decision-quality set with optimiser-generated references.
- **Baselines.** Uncompressed teacher; general-purpose model of equal size; DRL controller.
- **Metrics.** Decision-agreement with optimiser/optimal; SLA attainment; p50/p95 latency; VRAM;
  cost per decision.
- **Tools.** PyTorch, HuggingFace PEFT/bitsandbytes, Wanda/SparseGPT/LLM-Pruner, vLLM, the RQ1
  testbed.

### RQ3 ★ — Objective-aware multipath scheduling driven by an orchestrator

- **Motivation.** Zero papers combine multipath scheduling with O-RAN; endpoint schedulers are
  network-blind (§4, §10 GAP-3).
- **Literature evidence.** BLEST, ECF, DAPS, DeepCC, Peekaboo, ATSSS/5G-core splitting, and the
  *Tokens, Not Packets* interface argument.
- **Hypothesis.** Passing per-flow objectives (weight, deadline, slice identity) from a
  slice-aware controller to a multipath scheduler reduces slice SLA violations relative to
  objective-blind scheduling, without degrading aggregate goodput.
- **Architecture.** Slice controller/orchestrator → objective API → MPQUIC/MPTCP scheduler
  (userspace) and/or an in-core ATSSS splitter → path emulation → SLA measurement.
- **Experiment.** Heterogeneous path profiles (LTE-like, Wi-Fi-like, satellite-like); URLLC
  and eMBB flows co-scheduled; with and without objective passing.
- **Baselines.** Round-robin, lowest-RTT-first, BLEST, ECF, DeepCC, objective-blind DRL.
- **Metrics.** Per-slice latency percentiles; SLA-violation rate; goodput; reordering and
  buffer occupancy; interface overhead.
- **Tools.** MPQUIC/MPTCP implementations, `tc`/`netem`, Mininet or a multi-interface testbed,
  Open5GS with ATSSS-capable UPF if feasible.

### RQ4 — Cross-domain agentic orchestration (RAN + transport + core + edge)

- **Motivation.** End-to-end SLAs are cross-domain; per-domain optimisers can cancel (§3, §10
  GAP-4).
- **Hypothesis.** A hierarchical orchestrator with an LLM planner above per-domain DRL
  controllers achieves higher end-to-end SLA attainment than independent per-domain
  optimisation, at acceptable inter-domain signalling cost.
- **Experiment.** Four domain controllers; cross-domain fault and load injection; compare
  independent, centralised-optimal, flat-LLM and hierarchical.
- **Baselines.** Independent per-domain; centralised with full information (upper bound);
  flat LLM; MARL.
- **Metrics.** End-to-end SLA attainment; conflict count/resolution time; signalling overhead;
  stability under churn.
- **Tools.** ns-3/ns-O-RAN, SRv6 or segment-routing emulation, Open5GS, Kubernetes, MEC
  emulation.

### RQ5 — LLM proposes, optimiser disposes: hybrid control inside O-RAN

- **Motivation.** The hybrid is the most credible safe-LLM design and has not been demonstrated
  inside a standards-compliant plane (§3.3, §10 GAP-5).
- **Hypothesis.** LLM-formulated objectives with optimiser-guaranteed feasibility outperform
  both the optimiser alone and a flat LLM controller, and eliminate infeasible actions.
- **Experiment.** Three controllers on one testbed; adversarial and ambiguous intents;
  distribution shift.
- **Baselines.** Optimiser alone; flat LLM; SafeRL; rule-based O-RAN policy.
- **Metrics.** SLA attainment; infeasibility rate; shield activations; latency; cost; recovery
  after shift.
- **Tools.** O-RAN SC near-RT RIC + xApps, A1/E2, an open LLM, a MILP/CP solver (OR-Tools).

### RQ6 — Latency-feasible tiering of management functions

- **Motivation.** Measured LLM latencies are 2–4 orders of magnitude above fast-loop budgets
  (§6, §10 GAP-6).
- **Hypothesis.** Each management function has a maximum feasible tier, and pushing a function
  one tier lower costs a measurable amount of decision quality that is smaller for
  optimisation-style functions than for reasoning-heavy ones.
- **Experiment.** Latency-budget matrix (functions × tiers) with progressively compressed
  models on a live/emulated testbed.
- **Baselines.** Single-tier deployments; classical controllers per tier.
- **Metrics.** p50/p99 latency versus budget; quality loss; SLA outcome; cost.
- **Tools.** srsRAN or ns-O-RAN (RAN), Open5GS (core), Jetson-class edge device for the
  real-time tier.

### RQ7 — Safety and blast radius of incorrect agent actions on a 5G core

- **Motivation.** No work measures the consequence of a wrong action on a live/emulated core
  (§5.2, §10 GAP-7).
- **Hypothesis.** A verified-action shield (optimiser-checked feasible set) reduces
  service-impacting incorrect actions to zero while retaining most of the agent's benefit, at a
  measurable false-block cost.
- **Experiment.** Taxonomy of incorrect actions; injected on an emulated core; shielded versus
  unshielded agents.
- **Baselines.** Unshielded agent; rule-based controller; DRL controller.
- **Metrics.** Impact severity per action class; prevented unsafe actions; false-block rate;
  residual SLA attainment.
- **Tools.** Open5GS + UERANSIM + Kubernetes, chaos-injection tooling, the RQ1 harness.

### RQ8 — Reproducible open testbed and baseline suite for agentic network control

- **Motivation.** Canonical results are unreproducible; only 27 of 152 records have an
  identified public artifact (§10 GAP-8).
- **Hypothesis.** A containerised, documented testbed with published state/action/reward
  definitions and reference controllers enables third-party reproduction of published results.
- **Experiment.** Release and validate by reproducing at least one published DRL result and one
  published LLM-agent result.
- **Baselines.** Provides them.
- **Metrics.** Reproduction error versus published numbers; third-party reuse.
- **Tools.** Docker/Kubernetes, Open5GS, ns-3/ns-O-RAN, Prometheus, MLflow/DVC for trace
  management.

### RQ9 — Does fine-tuning improve network *decisions*?

- **Motivation.** Fine-tuning demonstrably helps text tasks; its effect on control decisions is
  unmeasured; LoRA's adequacy is disputed (§6, §10 GAP-9).
- **Hypothesis.** Domain fine-tuning improves decision quality, with diminishing returns beyond
  5k examples, and LoRA matches full fine-tuning at 7–8B scale on this task (contrary to the
  Tele-LLMs finding on knowledge tasks).
- **Experiment.** Four adaptation regimes × three data scales, evaluated on one decision task.
- **Baselines.** Unadapted model; DRL controller; classical optimiser; tree-based models.
- **Metrics.** SLA attainment; optimality gap; latency; GPU-hours; cost.
- **Tools.** HuggingFace PEFT/TRL, Unsloth, one to two A100/A6000-class GPUs or rented compute.

### RQ10 — Net energy and monetary cost of agentic control

- **Motivation.** No benchmark reports SLA-attainment-per-dollar or the control plane's own
  energy footprint (§10 GAP-10), despite the measured 156× cost spread.
- **Hypothesis.** There is a model-size and tier at which agentic control's net energy and cost
  per SLA point beats both rule-based and DRL control; above that size the control plane costs
  more than it saves.
- **Experiment.** Instrument inference energy/cost and network energy alongside SLA outcomes for
  every controller in RQ1/RQ2.
- **Baselines.** Rule-based; DRL; LLM-only; hybrid.
- **Metrics.** Net joules and currency per SLA point; cost per incident; overhead ratio.
- **Tools.** GPU energy telemetry (NVML), network energy models or measurement, the RQ1 harness.

---

# 12. Recommended Reading Order

Ordered by **learning sequence and research relevance**, not by quality. The goal is that each
step supplies the vocabulary needed for the next.

## Stage 1 — Foundations: what the problems are (read first, in this order)

1. **Network Service Orchestration: A survey** (ComCom 2019) — gives the service/lifecycle/
   resource vocabulary that keeps "orchestration" claims honest.
2. **Knowledge-Defined Networking** (CCR 2017) — the conceptual ancestor of every agentic
   orchestrator, and the origin of the "verifiable autonomous decision" problem.
3. **Multipath TCP: From Theory to Practice** (IFIP Networking 2011) + **Coupled Congestion
   Control for MPTCP** (NSDI 2012) — why multipath scheduling and congestion control are one
   problem.
4. **Experimental evaluation of multipath TCP schedulers** (SIGCOMM CSWS 2014) — why head-of-line
   blocking makes scheduling a research problem.
5. **AI-Driven Zero Touch Network and Service Management in 5G and Beyond** (IEEE Network 2020) —
   the closed-loop, multi-timescale target that everything else is measured against.

## Stage 2 — The method toolkit

6. **An Autonomous Network Orchestration Framework Integrating LLMs with Continual RL** (IEEE
   ComMag 2025) — the LLM-planner + RL-executor pattern in full detail. Read this before any
   other LLM-orchestration paper.
7. **Using Distributed RL for Resource Orchestration in a Network Slicing Scenario** (IEEE/ACM
   ToN 2023) — the best-specified DRL orchestration study; learn what a complete experimental
   description looks like.
8. **DeepCC** (IEEE TNSM 2021) — the best-specified learning-based multipath scheduler; a model
   for documenting state/action/reward.
9. **TelecomGPT** (IEEE TMLCN 2025) — the domain-adaptation recipe and its cost.
10. **A Survey on Model Compression for LLMs** (TACL 2024) — the compression taxonomy.

## Stage 3 — The classical baselines I must beat

11. **BLEST** (IFIP Networking 2016) and ECF (ACM CoNEXT 2017) — the multipath baselines.
12. **Low-Latency Scheduling in MPTCP** (IEEE/ACM ToN 2019) — the latency baseline.
13. **Orchestrating Virtualized Network Functions** (IEEE TNSM 2016) — the placement/chaining
    baseline, and proof that a heuristic can be within 1.3× of optimal.
14. **RL-PSO for End-to-End Traffic Scheduling in TSN-5G** (IEEE/ACM ToN 2023) — the
    RL-plus-optimiser hybrid baseline for scheduling.
15. **LEASCH** (IEEE Access 2020) and **Intelligent Resource Scheduling for 5G RAN Slicing**
    (IEEE TVT 2019) — the RAN-scheduling baselines.

## Stage 4 — Recent work: what the state of the art actually is

16. **TeleCom-Bench** (ACM KDD 2026) — the measured execution wall; the single most useful
    recent number in this literature.
17. **OperAID** (IEEE NetSoft 2026) — the closest existing closed-loop 5G-core benchmark, and
    the precise boundary of what is unbenchmarked.
18. **NIKA** (arXiv 2025) — how to build an executable network-agent benchmark properly.
19. **NetArena** (ICLR 2026) — dynamic generation, contamination control, safety separated from
    correctness.
20. **ORION** (arXiv 2026) — the closest LLM-in-O-RAN attempt, with measured latency and cost.
21. **Toward Autonomous O-RAN: A Multi-Scale Agentic AI Framework** (arXiv 2026) — the measured
    tiering result (0.847 ms / 793 ms) that constrains every architecture I design.
22. **ORANSight-2.0** (IEEE TMLCN 2025) — proof that a single 24 GB GPU can specialise a 70B
    model for O-RAN.

## Stage 5 — Directly relevant to my thesis

23. **NetConfEval** (ACM CoNEXT/PACMNET 2024) — the benchmark template, and the public-data
    standard I should match.
24. **Peekaboo** (IEEE JSAC 2020) — the learning scheduler that still cannot hear the network.
25. **Tokens, Not Packets** (ANRW 2026) — the interface argument that underpins my
    objective-passing contribution.
26. **Autonomous Access Traffic Splitting via 5G Core** (IEEE 2025) — business objectives
    entering a network decision; the closest existing analogue to SLA-aware multipath.
27. **NRflex** (Computer Communications 2022) — the concrete RIC-driven slice-control point my
    agent would occupy.

## Stage 6 — The gap

28. **The three 2026 abstract-level papers I could not read** — *LLM-Driven Multi-Agent
    Framework for Autonomous Network Slice Management*, *A Feasibility-Shielded Agentic AI
    Framework for 6G Self-Healing Core Networks*, and *AgentPN Loop: Benchmarking AI Agents for
    Private 5G/6G Network Management* — must be retrieved through institutional access and read
    **before** I write a novelty claim, because their titles are closest to my proposal.
29. **IEEE COMST 2026 — LLMs for communication, network and service management** — to confirm
    the current state of the art immediately before writing my related-work section.
