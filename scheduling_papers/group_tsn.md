# Group: TSN / 5G Flow Scheduling — Detailed Technical Extraction

**Extraction date:** 2026-09-18
**Retrieval working directory:** `/home/pouriaarefi/Documents/phd_network_ai_literature_review/scheduling_papers/pdfs`

## ⚠️ ACCESS-DISCLOSURE SUMMARY (READ FIRST)

| # | Paper | Access achieved | Evidence |
|---|-------|-----------------|----------|
| 1 | DQHPSO (IEEE/ACM ToN 2023) | **ONLY ABSTRACT** | Unpaywall `is_oa: false`, `oa_status: "closed"`; Semantic Scholar `openAccessPdf.url: ""`; IEEE `isOpenAccess: false`; no arXiv version exists; OpenAIRE returned zero web resources; ResearchGate/ACM DL/CORE all bot-blocked (HTTP 403) |
| 2 | LEARNET (IEEE ICC 2020) | **FULL TEXT READ** (7 pp., "Peer reviewed version" / accepted manuscript) | Aalto University repository, via Unpaywall `best_oa_location` |
| 3 | Joint Flow Scheduling Uplink 5G-TSN (IEEE TCCN) | **ONLY ABSTRACT** | Unpaywall `is_oa: false`, `oa_status: "closed"`; IEEE `isOpenAccess: false`; Semantic Scholar abstract elided by publisher; OpenAIRE returned zero web resources |

Papers 1 and 3 are **closed access**. Every field below for those two papers that is not derivable from the published abstract is marked `NOT REPORTED`. **No numbers, baselines, simulators, or results have been inferred, estimated, or reconstructed from general knowledge.** Where a datum comes from a *secondary* source rather than the paper itself, it is explicitly labelled as such.

---

### 1. Reinforcement Learning-Based Particle Swarm Optimization for End-to-End Traffic Scheduling in TSN-5G Networks

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - **Authors:** Xiaolong Wang; Haipeng Yao; Tianle Mai; Song Guo; Yunjie (Yun-jie) Liu
  - **Year:** 2023 (issue publication date **1 December 2023**)
  - **Venue:** *IEEE/ACM Transactions on Networking*, **Vol. 31, No. 6, pp. 3254–3268** (15 pages)
  - **DOI:** `10.1109/TNET.2023.3276363`
  - **Type:** **Peer-reviewed journal article** (verified via Crossref `type: journal-article`, publisher: Institute of Electrical and Electronics Engineers (IEEE); DBLP key `journals/ton/WangYMGL23`). Not a preprint.
  - **Author affiliations (secondary, from repository records):** Beijing University of Posts and Telecommunications (BUPT); The Hong Kong University of Science and Technology (HKUST, Song Guo); The Hong Kong Polytechnic University (PolyU, Song Guo).
  - **Author keywords (secondary, from HKUST + PolyU research portals):** 5G; 5G mobile communication; deterministic communications; hybrid TSN; Job shop scheduling; Optimal scheduling; Schedules; Synchronization; Time-sensitive networking (TSN); Ultra reliable low latency communication (uRLLC); Wireless communication.
  - **Reference count:** 39 (IEEE Xplore metadata) / 35 (Semantic Scholar). *Not used analytically.*
  - **Availability note:** `isOpenAccess: false`. No legal open-access full text located.

- **A. Exact problem solved**
  - From the abstract (verbatim): *"the potential barriers between the TSN and 5G systems, such as clock synchronization and end-to-end traffic scheduling, are inevitable. Time synchronization has been studied in many works, so this paper focuses on the end-to-end traffic scheduling problem in TSN-5G networks."*
  - Framed by the abstract's motivating context (verbatim): *"industrial networks pose new requirements on communications, such as strict latency boundaries, ultra-reliable transmission"* and the goal that TSN+5G integration provides *"increased flexibility, lower commissioning costs, and seamless interoperability of various devices, regardless of whether they use a wired or wireless interface."*
  - **Exact formal problem statement, objective function, decision variables: NOT REPORTED** (beyond the above — full text not retrieved).

- **B. Network architecture**
  - Abstract (verbatim): *"We propose a novel integrated TSN and 5G industrial network architecture, where the 5G system acts as a logical TSN-capable bridge."*
  - **Topology, node counts, link capacities, topology figures: NOT REPORTED.**

- **C. Network layer/domain**
  - Domain: **industrial networking**, spanning the **wired TSN (Layer 2 / data-link) domain** and the **5G wireless (uRLLC) domain**, with the 5G system functioning as a *logical TSN bridge*. This is a **cross-domain / end-to-end** (wired + wireless) scheduling problem.
  - Precise layer-by-layer decomposition (which scheduler sits at which layer, whether TAS/CQF/ATS is assumed): **NOT REPORTED.**

- **D. Network entities involved**
  - Named/implied in the abstract: **IIoT devices** (massive numbers, connecting *"via wired and wireless"*), the **TSN domain**, the **5G system** acting as a *"logical TSN-capable bridge"*, and **uRLLC** wireless links.
  - Explicit list of talkers/listeners, bridges, UEs, gNBs, UPF, DS-TT/NW-TT translation functions, CUC/CNC: **NOT REPORTED.**

- **E. Input/state parameters** (exact observation vector if reported)
  - **NOT REPORTED.** The abstract does not describe the observation/state vector. Full text not retrieved.

- **F. Decision variables** (exact action space if reported)
  - **NOT REPORTED.** The abstract states only that DQHPSO *"search[es] for the optimal scheduling solution"* and that the *"Double Q-learning [is used] to adjust the number of levels in the population"* — i.e., the RL action is applied to **population structure (number of levels)**, but the *scheduling* decision variables (gate control lists, transmission offsets, queue/priority assignment, etc.) are **NOT REPORTED.**

- **G. Objective function** (quote exact reward/cost)
  - **NOT REPORTED.** The abstract gives no reward/cost function and no explicit objective expression. The reported performance orientation is *"increase the scheduling success ratio of time-triggered flows"* (abstract, verbatim).

- **H. Constraints**
  - **NOT REPORTED.** The only constraint-adjacent statement is the abstract's framing of *"strict latency boundaries, ultra-reliable transmission"* as industrial requirements. No formal constraint set is disclosed.

- **I. Scheduling algorithm + optimization method**
  - Abstract (verbatim): *"we design a Double Q-learning based hierarchical particle swarm optimization algorithm (DQHPSO) to search for the optimal scheduling solution. The DQHPSO algorithm adopts a level-based population structure and introduces Double Q-learning to adjust the number of levels in the population, which evades the local optimum to further improve the search efficiency."*
  - **Interpretation (careful, abstract-only):** the metaheuristic is a **hierarchical / level-based PSO**, and **Double Q-learning is used as the outer adaptive controller of the hierarchy depth (number of levels in the population)** — not as the direct scheduler. This is a **hybrid RL + swarm-intelligence metaheuristic**.
  - **Swarm size, level count, iteration budget, Q-table/state-space definition, convergence criterion, fitness function: NOT REPORTED.**

- **J. ML/DRL used?** yes/no and which
  - **YES — Reinforcement Learning.** Specifically **Double Q-learning** (tabular RL family), used to adapt the PSO population's level count. It is **not** deep RL (no DQN/PPO/actor-critic named in the abstract).
  - Full RL formulation (states, actions, reward, discount, ε-greedy schedule): **NOT REPORTED.**

- **K. Simulator / testbed / dataset** (exact names + versions)
  - Abstract (verbatim): *"Extensive simulations demonstrate…"* → **SIMULATION** (not a real testbed).
  - **Exact simulator name, version, custom-vs-commercial status, topology file, and configuration parameters: NOT REPORTED.**

- **L. Traffic model**
  - Abstract references **"time-triggered flows"** as the traffic class whose scheduling success ratio is improved.
  - Arrival process (periodic/Poisson), period distributions, frame sizes, priority classes, 3GPP 5QI mapping, jitter/latency deadlines: **NOT REPORTED.**

- **M. Network scale**
  - **NOT REPORTED.** (Abstract mentions *"massive IIoT devices"* qualitatively only.)

- **N. Baselines** (exact names)
  - **NOT REPORTED.** The abstract states only the comparison target generically: *"compared to other algorithms."* **No baseline is named in the abstract.**

- **O. Metrics**
  - **Scheduling success ratio of time-triggered flows** (abstract, verbatim: *"increase the scheduling success ratio of time-triggered flows"*).
  - Any additional metrics (end-to-end latency, jitter, resource utilization, convergence speed, computational cost): **NOT REPORTED.**

- **P. Main quantitative results** (EXACT numbers with the comparison, quoted)
  - **NO NUMERIC RESULTS ARE GIVEN IN THE ABSTRACT.** The only performance claim available is qualitative, quoted verbatim:
    > *"Extensive simulations demonstrate that the DQHPSO algorithm can increase the scheduling success ratio of time-triggered flows compared to other algorithms."*
  - **Exact percentages, absolute values, and figure/table results: NOT REPORTED** (full text inaccessible). **No numbers have been fabricated.**

- **Q. Main limitation**
  - **NOT REPORTED** by the source retrieved (no limitations section accessible). *Unverified inference is deliberately withheld.*

- **R. Research gap this suggests**
  - *Inferred from the abstract only, and stated as a reviewer observation rather than a claim by the authors:* the abstract reports no quantified comparison, no named baselines, no simulator identification, and no reproducible parameter set — meaning the paper as publicly visible **cannot be benchmarked** without paywalled access. For a systematic review this is itself a reproducibility gap.
  - Additionally, the RL component is confined to **tuning the metaheuristic's population structure** rather than learning the scheduling policy end-to-end; the abstract does not indicate any comparison against a **direct DRL scheduler** (e.g., DQN/PPO over the scheduling action space). Whether such a comparison exists in the full text is **unknown**.

- **S. Best URL you actually retrieved + whether you read FULL TEXT or ONLY ABSTRACT**
  - **Read level: ONLY ABSTRACT** (abstract text verified identically across three independent sources).
  - **Best URLs actually retrieved (all returned HTTP 200 to this session):**
    - PolyU Scholars Hub record (abstract + keywords + pagination): https://research.polyu.edu.hk/en/publications/reinforcement-learning-based-particle-swarm-optimization-for-end-
    - HKUST Research Portal record (abstract + pagination + publication status): https://researchportal.hkust.edu.hk/en/publications/reinforcement-learning-based-particle-swarm-optimization-for-end-/
    - IEEE Xplore metadata endpoint (confirmed `isOpenAccess: false`, vol. 31, pp. 3254–3268, 39 refs): https://xplorestaging.ieee.org/document/10136614
    - Semantic Scholar record (abstract, authors, journal metadata): https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TNET.2023.3276363
    - Unpaywall verification (closed): https://api.unpaywall.org/v2/10.1109/TNET.2023.3276363
    - Publisher landing page (paywalled): https://ieeexplore.ieee.org/document/10136614
  - **Full-text PDF:** NOT OBTAINED. Paywalled at IEEE Xplore and ACM DL.

---

### 2. LEARNET: Reinforcement Learning Based Flow Scheduling for Asynchronous Deterministic Networks

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - **Authors:** Jonathan Prados-Garzon; Tarik Taleb; Miloud Bagaa
  - **Affiliations (from the retrieved full text, p. 1):** ∗ Aalto University, Espoo, Finland; § University of Oulu, 90570 Oulu, Finland.
  - **Year:** 2020 (published 01/06/2020)
  - **Venue:** **ICC 2020 – 2020 IEEE International Conference on Communications (ICC)**, Dublin, Ireland; pp. 1–6; IEEE International Conference on Communications series
  - **DOI:** `10.1109/ICC40277.2020.9149092`
  - **Type:** **Peer-reviewed conference paper.** The retrieved file is explicitly the *"electronic reprint of the original article"*, **"Document Version: Peer reviewed version"** (accepted manuscript deposited at Aalto University). Verified via Crossref (`type: proceedings-article`, venue *ICC 2020 - 2020 IEEE International Conference on Communications (ICC)*, pages 1-6).
  - **Funding acknowledged in the paper:** Business Finland **5G-FORCE** project; Academy of Finland **6Genesis** (grant No. 318927) and **CSN** (grant No. 311654) projects.

- **A. Exact problem solved**
  - The paper addresses the **Online Flow Allocation Problem (OFAP) in DetNet asynchronous networks** (verbatim): *"This work addresses the online flow allocation problem (OFAP) in DetNet asynchronous networks. The OFAP consists of finding the optimal configuration for allocating each incoming flow to the network, given an optimization objective."*
  - Formal restatement (verbatim): *"The OFAP in an ATS-based FP considered here is defined as the process of choosing the allocation configuration for every incoming flow at every hop all along the predefined path from its source to its destination in order to maximize the network operator's revenue. The flow allocation configuration at every ATS implies to decide the flow to shaping buffer, priority level, and delay budget assignments."*
  - **Stated novelty (verbatim):** *"To the best of the authors' knowledge, this is the first paper proposing a RL-based solution for optimizing the operation of a TSN asynchronous forwarding plane."*
  - **Prior-art gap identified (verbatim):** *"the flow allocation problem for ATS-based networks is only tackled in [8] by Specht and Samii"* — who used i) a pure **SMT solver** and ii) a heuristic **Topology Rank Solver (TRS)**, optimizing **maximization of the delay slack**, with the path between every source–destination pair **predefined**.
  - **Scheduling is the CENTRAL contribution of this paper** — not a side detail. The RL agent *is* the flow scheduler.

- **B. Network architecture**
  - **SDN-like DetNet architecture with fully separated Control Plane (CP) and Forwarding Plane (FP)** (verbatim: *"Let us consider a DetNet network with a Software-Defined Networking (SDN)-like architecture [14] where the Control Plane (CP) and Forwarding Plane (FP) are fully separated, see Fig. 1."*)
  - **Forwarding plane:** a set of **V IEEE 802.1 TSN network devices**, each implementing an **IEEE 802.1Qcr Asynchronous Traffic Shaper (ATS)** at **each of their interfaces/egress ports**. The FP is modelled as a directed graph **G = (V, E)**, V = {v1,…,v_V} nodes, E = {e1,…,e_E} edges representing *"the ATSs or simplex links"*. There are **E/2 full-duplex point-to-point links** interconnecting the asynchronous TSN nodes.
  - **Two FP node types:**
    - **DEN — DetNet Edge Node:** may be the starting or termination point of deterministic flows; performs *"the addition or the removal of packet sequencing, and packet replication and combination."*
    - **DTN — DetNet Transit Node:** *"will only implement the DetNet forwarding sub-layer, and are responsible for routing the packets from the DEN source to the DEN destination."*
  - **Control plane:** a **logically centralized SDN controller** controlling/monitoring devices via the southbound interface and exposing an abstraction to the upper application layer via the northbound interface.
  - **Three applications run on top of the controller:**
    1. **Monitoring Engine (ME)** — collects network statistics: flow characteristics (delay constraint, rate demand, holding time), flow arrival process to each DEN (as source and destination), link times-to-failure, etc.
    2. **Data Analytics Engine (DAE)** — consumes and analyses ME data for prediction (e.g., estimation of the temporal workload profile).
    3. **Flow Scheduling Application (FSA)** — leverages the analysed data to optimize flow scheduling; **this is where LEARNET's ML lives.**
  - **ATS / UBS internals (two-level queuing hierarchy, Fig. 2):**
    - **Level 1:** a set of **shaped queues** for interleaved shaping.
    - **Level 2:** **one pseudo-queue per priority level** in the scheduler; each pseudo-queue merges the output of all shaped queues of the same priority level. *"The combining form pseudo points out that it is not required to implement them physically when there are few shaped queues."*
    - All queues follow **First Come, First Served (FCFS)** discipline.
    - **Shaped-queue assignment rules (QAR rules) — verbatim:** *"each shaped queue is associated with only one ingress port (QAR1 rule), one priority level in the previous ATS (QAR2 rule), and one internal priority level (QAR3 rule) at a given time. QAR2 and QAR3 rules are required to provide deterministic QoS, whereas QAR1 isolates the flows from different nodes, avoiding the propagation of non-conformant traffic overloads. These rules also determine the required number of shaped queues to realize P priority levels."*
    - **Shaping algorithm assumed: Length Rate Quotient (LRQ)** — *"Here we will assume the Length Rate Quotient (LRQ) algorithm which enforces an upper bound on the flows of the form A_f(t) ≤ r_f·t + b_f"*, where *"LRQ algorithm computes the eligibility time t_f for the next packet of a given flow f as t_f = l_f/r_f, where l_f is the length of the head-of-line (HOL) packet of the flow. Then, the HOL packet of the flow f will be eligible for transmission after t_f time units have elapsed."*
    - **Packet selection:** *"The decision on which packet to transmit relies on strict priority levels and the interleaved shaping algorithm considered."*
  - **Routing assumption (verbatim):** *"as in [8], suppose that explicit routes between every pair of DENs source and destination in the network is predefined."* → **LEARNET does NOT solve routing; it schedules onto pre-computed paths.**
  - **Architectural contrast stated (verbatim):** *"In contrast to synchronous queuing algorithms such as Cyclic Queuing and Forwarding (CQF) and Time-Aware Shaper (TAS), asynchronous ones do not depend on network-wide coordinated time (higher scalability) and utilize network bandwidth more efficiently by leveraging statistical multiplexing."*

- **C. Network layer/domain**
  - **Layer 2 / data-link layer**, IEEE 802.1 TSN, specifically the **IEEE 802.1Qcr ATS forwarding plane** (egress-port queuing and shaping), operating within an **IETF DetNet** network layer.
  - The evaluated scenario is a **5G DetNet Backhaul Network (BN)** — i.e., the **transport/backhaul network domain**, not the radio access or core application domain.
  - The paper notes TSN/DetNet *"are appealing technologies for supporting network slicing at the transport network domain."*
  - Control plane operates at the **application/control layer** (SDN applications: ME, DAE, FSA).
  - The scheduling decision granularity is **per-flow per-hop, per-ATS** (flow → shaping buffer, priority level, per-hop delay budget).

- **D. Network entities involved**
  - **DEN (DetNet Edge Node)** — source and destination of deterministic flows.
  - **DTN (DetNet Transit Node)** — DetNet forwarding sub-layer only.
  - **ATS (Asynchronous Traffic Shaper)** — instantiated **at every interface at every FP node**; contains **N_SBs^(e) shaping buffers** and therefore at most **P_max^(e) = N_SBs^(e) priority levels**.
  - **Shaped queues (shaping buffers)** — interleaved shaping stage; each characterized by size **B_s** and state (idle/busy).
  - **Pseudo-queues** — one per priority level, second queuing stage.
  - **SDN controller** (logically centralized) — CP.
  - **ME, DAE, FSA** — the three control-plane applications.
  - **RL agent / Flow Scheduling Agent (FSA)**.
  - **Flow Admission Control block** — *"responsible for accepting or rejecting the flow given the action provided by the agent"*; evaluates constraints C1–C5.
  - **Flow Information Base** — *"a kind of flow information base is required to keep track of the allocation configuration and characteristics of every ongoing flow in order to properly update the network FP state when the flow leaves the network."*
  - **foi (flow of interest)** — the incoming flow being scheduled.

- **E. Input/state parameters** (exact observation vector if reported)
  - **Flow request parsing (verbatim):** *"LEARNET needs to know the sustainable rate r^(foi), burstiness b^(foi), maximum packet size l^(foi), and E2E delay budget of the foi."*
  - **Observations fed to the agent (verbatim):** *"The flow scheduling agent is fed with this information along with predictive analytics, related to flow arrival and holding time processes, and the current FP network state."*
  - **Predictive data analytics required (verbatim):** *"i) the expected foi lifetime duration τ^(foi), ii) the foreseen arrival rate λ during the next temporal interval of length τ^(foi), and iii) the predicted mean and standard deviation for the different features of the future incoming flows (r, σ_r, b, σ_b, D_max, and σ_Dmax)."*
  - **Network information required (verbatim):** *"i) link capacities C_{e_l} ∀ e_l ∈ P; ii) current state of the shaping buffers at the different ATSs P in the foi path; and iii) the allocated rate r_p^(e_l), allocated burstiness b_p^(e_l), minimum delay budget D_{p,max}^(e_l), and maximum packet length l_p^(e_l) at each priority level of every ATS in the foi path."*
  - **Stated modelling assumptions behind the analytics (verbatim):** *"i) the flow lifetime duration obeys an exponential distribution, ii) the flow arrival process is Poissonian, and iii) the flow arrival process and the features of the future incoming flows to the system are stationary."*
  - **Per-ATS aggregated state variables (Table I):** `r_p^(e_l)`, `b_p^(e_l)`, `l_p^(e_l)`, `D_{p,max}^(e_l)` = aggregated rate, aggregated burstiness, maximum packet length, and the lowest delay budget to be met in priority level p at ATS e_l. Plus `C_{e_l}` (link capacity at the ATS e_l), `B_s` (size of shaping buffer s), `I_{foi}^(e_l)` (ingress port of the foi at the node containing ATS e_l), `p_a^(e_l)` (chosen priority level for the foi at ATS e_l).

- **F. Decision variables** (exact action space if reported)
  - **Action representation (verbatim):** *"Let us suppose the predefined path for the foi has N_H hops. Then, the action generated by the agent is an N_H dimensional vector of real numbers u, where each component includes two data: i) the chosen priority level p_a^(e_l) for the foi at the respective hop (ATS) e_l, ii) the percentage of the total foi E2E delay budget η^(e_l) = D_{p,max}^(e_l)/D_max^(foi) to be spent at the respective hop. Deciding the maximum delay budget to be spent at every ATS makes scalable the actions feasibility checking… The former is included in the integer part of the component, whereas the latter is contained in the decimal part."*
  - **Component domain (verbatim):** *"each component of u takes values from a finite set of real values in the interval [1, P_max^(e_l) + 1]. The P_max^(e_l) is set to the number of shaping queues in the ATS e_l. The decimal part is discretized according to a given granularity. For instance, a granularity of 0.1 means the percentage of the foi E2E delay budget assigned to each hop is 10% or a multiple of it."*
  - **Action-space filtering (verbatim):** *"the set of actions is filtered in order to reduce its size. Specifically, we only consider the actions that meet the following constraints: c.1) the sum of the decimal parts of all components of u has to equal one, and c.2) the decimal part of every component of u has to be greater than zero. Constraint c.1 enforces that the foi E2E delay budget is fully consumed along the path. This constraint helps to improve the flow acceptance ratio and, hence, the operator's revenue."*
  - **Worked example given in the paper (verbatim):** *"let us assume a path with three hops and P_max^(e_l) = 3 for every ATS. The action vectors u = (1.5, 3.5, 1.0) and u = (1.2, 3.5, 1.2) would be removed from the action set, whereas u = (2.2, 3.5, 1.3) would be valid."*
  - **Net decision variables per flow:** for each hop e_l in path **P**: (a) **priority level** p_a^(e_l), (b) **shaping buffer** assignment s_{e_l}^c (chosen by the admission-control/allocation procedure), (c) **per-hop E2E delay-budget fraction** η^(e_l).

- **G. Objective function** (quote exact reward/cost)
  - **Global objective (verbatim):** *"maximize the network operator's revenue"* / *"to maximize the long-term network operator's revenue"* / *"the goal is to maximize the long-term operator benefit, which will mainly depend on the flow arrival process, the flow characteristics, pricing, and network setup."*
  - **Exact reward function (verbatim):** *"If the flow is accepted, the agent will receive an award 1/τ^(foi) times the income α^(foi) that the operator will obtain for allocating the foi. If the flow is rejected, the agent will be penalized with a reward of −1/τ^(foi) · α^(foi)."*
    - i.e. **R = +α^(foi) / τ^(foi)** on acceptance, **R = −α^(foi) / τ^(foi)** on rejection.
    - The **1/τ^(foi) normalisation** converts a per-flow lump income into a rate, reflecting flow duration.
  - **Special case stated (verbatim):** *"Observe that, if we set α^(foi) = 1 for all the incoming flows, we will maximize the flow acceptance ratio (flow rejection ratio minimization)."*
  - **Income parameterisation (verbatim):** *"the allocation of each incoming flow f, hereinafter referred as to flow of interest (foi), has an associated income α_f for the network operator. That income might be different for each flow depending on the type of flow or the flow characteristics, e.g., mean sustainable rate r_f, burstiness b_f, maximum packet length l_f, and maximum end-to-end (E2E) delay budget D_{f,max}."*

- **H. Constraints**
  - **OFAP feasibility constraints C1–C5 (verbatim, Section III):**
    - **C1** — *"The E2E delay D experienced by the foi has to be lower than its E2E delay budget D_{f,max}."*
    - **C2** — *"The ongoing flows must keep experiencing an E2E delay lower than their respective E2E delay budgets."*
    - **C3** — *"The aggregated rate allocated to any link must be lower than its capacity."*
    - **C4** — *"The aggregated burstiness allocated to any shaping buffer has to be lower than its size."*
    - **C5** — *"The QAR1, QAR2, and QAR3 rules have to be met, i.e., every shaping queue must be either idle or assigned to an only one priority level, only one priority level in the previous hop, and an input port at a given instant."*
  - **Action-space constraints:** c.1 (Σ decimal parts = 1) and c.2 (every decimal part > 0), as quoted in section F.
  - **Scalability remark (verbatim):** *"thanks to deciding and recording the maximum delay budget spent at every ATS for every incoming flow, the checking of the constraints C1-C3 is scalable. Otherwise, we will have to check that the network will keep guaranteeing the performance requirements for all the affected ongoing flows after the potential foi allocation."*
  - **Analytical delay bound used for admission control — Eq. (1) (verbatim form):**
    > D_{f,p}^(e_l) ≤ [ Σ_{z=1}^{p} b_z + ∨_{z=p+1}^{P_max^(e_l)} l_z ] / [ C_{e_l} − Σ_{z=1}^{p−1} r_z ] + l_f / C_{e_l}
    - where (verbatim) *"b_z, l_z, and r_z are the aggregated burstiness, maximum packet size, and aggregated data rate at priority level z, respectively. And C_{e_l} denotes the link capacity."* Per Table I, the `∨`/`W` operator denotes *"the greatest value of the set of elements"* (max). **Note:** this formula is transcribed from the PDF; the `∨` symbol renders as `W` in text extraction and the upper limit is `P_max^(e_l)`.
  - **Concrete admission-control inequalities Eqs. (2)–(5)** are given in the paper for three cases — `p_{e_l} = p_a` (Eq. 2), `p_{e_l} > p_a` (Eq. 3), `p_{e_l} < p_a` (Eq. 4) — and the link-capacity check **Eq. (5):** `Σ_{z=1}^{P_max^(e_l)} r_z^(e_l) + r^(foi) ≤ C_{e_l}; ∀ e_l ∈ P`.
  - **Priority-indexing convention (verbatim):** *"in the constraints listed above, we are considering that lower indexes correspond to higher priority levels."*
  - **Algorithm 1 (verbatim specification):** *"Shaping buffers related constraints verification and allocation process for the foi."*
    - **Input:** `I_{foi}^(e_l)` and `p_a^(e_l) ∀ p, i ∈ [1,…,P_h], j ∈ [1,…,P_{h−1}], & h ∈ P`
    - **Output:** `s_{e_l}^c` and `d ∈ [ACCEPTED, REJECTED]`
    - **Logic:** *"The algorithm looks for a busy shaping buffer with enough capacity and a valid state. In other words, the shaping buffer is assigned to the same input port, internal priority level p_a^(e_l), and priority level p_a^(e_{l−1}) in the previous hop e_{l−1} as the foi allocation configuration commanded by the action. If not, the algorithm checks whether there is any idle shaping buffer to allocate the flow."*
    - Step 1: `if there is any busy s ∈ S_{e_l} such that its input port equals I_{foi}^(e_l), its priority level equals p_a^(e_l), its previous priority level equals p_a^(e_{l−1}), and B_s is enough to accommodate b^(foi)` → Step 2 `d = ACCEPTED`; Step 3 `s_{e_l}^c = ChooseBusyBuffer()`; Step 4 `else`; Step 5 `if there is any idle s ∈ S_{e_l}` → Step 6 `d = ACCEPTED`; Step 7 `s_{e_l}^c = ChooseIdleBuffer()`; Step 8 `else`; Step 9 `d = REJECTED`.
  - **Fallback (verbatim):** *"If any of the constraints C1-C5 is not met, the admission control block will decline the flow allocation request and will penalize the agent with a negative reward."*

- **I. Scheduling algorithm + optimization method**
  - **LEARNET = Reinforcement Learning (RL) + predictive data analytics + ATS analytical performance models**, combined with a **rule-based flow admission control** that filters infeasible agent actions.
  - **Stated design philosophy (verbatim):** *"Some authors have reported and highlighted a drastic reduction in the amount of data required to train the ML-based models by using approaches that combine data-driven techniques and analytical models [10]. Our solution includes a flow admission control process, which relies on the ATS performance models, to check the feasibility of the actions issued by the agent. The flow admission control rejects the invalid actions… In this way, the information of the analytical models is transferred to the agent, and, most importantly, the flow allocation process becomes fully reliable."*
  - **Summary verbatim from conclusion:** *"The solution combines data-driven and analytical model-based approaches to maximize the network operator's revenue."*
  - **Operation flow (Fig. 4, as described in text):** step 1 flow allocation request arrives; request parsed to identify foi characteristics; step 3 agent fed with parsed info + predictive analytics + current FP network state; step 4 agent produces action (allocation configuration for every ATS in the foi path); action + foi characteristics forwarded to flow admission control (constraints C1–C5); step 6 on acceptance, the allocation setup takes place and the network FP state is updated.
  - **Network state update rule (verbatim):** *"∀ e_l ∈ P & p = p_a^(e_l), r_p^(e_l) ← r_p^(e_l) + r^(foi); b_p^(e_l) ← b_p^(e_l) + b^(foi); D_{p,max}^(e_l) ← D_{p,max}^(e_l) ∧ η^(e_l) · D_max^(foi); and l_p^(e_l) ← l_p^(e_l) ∨ l^(foi). Besides, the state of the chosen shaping buffers whose state were idle when the foi arrived will be modified from idle to busy, and the buffer will be associated with the respective input port, internal priority level, and priority level in the previous hop."*
  - **Conventional optimization method compared against:** the only prior OFAP solution for ATS networks is Specht & Samii's — **pure SMT solver** and **Topology Rank Solver (TRS) heuristic** optimizing **delay slack maximization**. LEARNET is positioned against the general scarcity of OFAP work rather than benchmarked head-to-head against these in the retrieved text.

- **J. ML/DRL used?** yes/no and which
  - **YES — Reinforcement Learning.** The paper repeatedly states "Reinforcement Learning (RL)-based solution", "RL agent", "the flow scheduling agent".
  - **⚠️ IMPORTANT NEGATIVE FINDING:** the retrieved full text **does NOT name a specific RL algorithm**. A full-text search for `Q-learning`, `DQN`, `deep Q`, `SARSA`, `actor`, `critic`, `policy gradient`, `neural network`, `epsilon`, `epsilon-greedy`, `tabular`, `value function`, and `convergence` returned **no matches** in the paper body. The paper specifies the **MDP ingredients** (observations, actions, reward, state update) but **not the learning algorithm, function approximator, exploration policy, discount factor, or training procedure**. It is therefore **NOT deep RL** as far as the retrieved text discloses — but the exact algorithm is **NOT REPORTED**.
  - The paper does mention ML generally at the FSA: *"here, we consider the use of Machine Learning (ML) at the FSA to exploit the high degree of flexibility potentially offered by an ATS-based FP."*
  - **No RL hyperparameters, no convergence curves, and no training-episode counts are reported** in the retrieved text.

- **K. Simulator / testbed / dataset** (exact names + versions)
  - **SIMULATION — custom, unnamed event-driven simulator** (verbatim): *"The performance evaluation of LEARNET was carried out by using an event-driven simulator of a 5G DetNet Backhaul Network (BN) with three hops (ATSs) between the source DEN and the destination DENs (see Fig. 5)."*
  - **⚠️ No named simulator (no ns-3, OMNeT++, Simu5G, etc.), no version, no public artifact/dataset, no code release is reported.** The simulator is bespoke and not released in the retrieved text.
  - **No real testbed.** Everything is simulation.

- **L. Traffic model**
  - **Flow classes = the four critical 5G QoS Identifiers (5QIs)** defined in **3GPP TS 23.501 V16.1.0**, referenced as [11]. Verbatim: *"incoming flows have characteristics similar to the four critical 5G QoS Identifiers (5QIs) defined in Third Generation Partnership Project (3GPP) TS 23.501 V16.1.0."*
  - **Data rate (verbatim):** *"The actual data rate demanded by each simulated incoming flow follows a Gaussian distribution. The mean of that distribution for each 5QI is included in the third column of Table II, and the standard deviation was set to 15% of the respective mean."*
  - **Timing processes (verbatim):** *"The flow lifetime and flows inter-arrival times obey an exponential distribution."*
  - **5QI class generation (verbatim):** *"We considered that the aggregated demanded data rate for each 5QI is the same on average as a simple criterion to generate the 5QI of each simulated flow."*
  - **Destination selection (verbatim):** *"we used a discrete uniform distribution to choose the destination DEN for each simulated flow in the scenario depicted in Fig. 5."*
  - **Table II — Flow types characteristics** (verbatim; *"Most of the data included in this table were extracted from [11]"* = 3GPP TS 23.501 V16.1.0):

    | 5QI | Prio | Rate (Mbps) | Burstiness (bits) | D_max (ms) | Income | Avg. Dur. (s) | L_max (bits) | Ex. service |
    |-----|------|-------------|-------------------|------------|--------|---------------|--------------|-------------|
    | 82 | 19 | 0.1 | 2040 | 10 | 2.5 | 1200 | 2040 | Discrete Automation |
    | 83 | 22 | 0.2 | 10832 | 10 | 2.5 | 1200 | 10832 | Discrete Automation |
    | 84 | 24 | 0.3 | 10832 | 30 | 4 | 1200 | 10832 | Intelligent transport systems |
    | 85 | 21 | 0.3 | 2040 | 5 | 3 | 1200 | 2040 | Electricity distribution HV |

- **M. Network scale**
  - **Path length:** *"three hops (ATSs) between the source DEN and the destination DENs"* (Fig. 5).
  - **Per-ATS queues:** *"every ATS in the FP includes four shaping buffers and, then, four potential priority levels."*
  - **Link capacities (verbatim):** *"The link capacities were set to 100 Gbps, 10 Gbps, and 1 Gbps for the first, second, and third hop, respectively."* (i.e., a deliberately **heterogeneous / capacity-decreasing** 3-hop path.)
  - **Graph model:** general G = (V, E) with V nodes and E/2 full-duplex links; the evaluated instance is the 3-hop topology of Fig. 5. **Exact node count of Fig. 5 is not recoverable from the text layer** (Fig. 5 is a raster image in the PDF).
  - **Simulation volume (verbatim):** *"In every simulation (every point represented in Fig. 6), we simulated the arrival and departure of one million of flows."* → **1,000,000 flows per data point.**
  - **Load range:** x-axis of Fig. 6 spans **0 to 150** "Demanded destination DEN link utilization" (%), i.e., the network is driven into **overload (>100%)**.

- **N. Baselines** (exact names)
  - **One baseline, explicitly described (verbatim):** *"We compared the performance achieved by LEARNET with a baseline solution that respects at every ATS the 5QIs priorities defined by 3GPP in [11]. Then, the fois of 5QIs 82, 85, 83, and 84 will be assigned at every ATS to priority level 1, 2, 3, and 4, respectively. Besides, the baseline solution allocates 33% of the E2E delay budget to each hop in the path."*
  - **Baseline label in figures:** `baseline`.
  - **⚠️ No other baselines.** In particular, **no comparison against the SMT solver or TRS of Specht & Samii [8]** is reported in the retrieved text, despite those being the prior-art OFAP solutions.

- **O. Metrics**
  - **Primary metric (verbatim, Fig. 6 y-axis):** *"Perc. of the maximum operator benefit attained"* — reported as *"the percentage of the maximum attainable profit achieved for each solution as a function of the demanded link utilization at the edge."*
  - **Independent variable (verbatim, Fig. 6 x-axis):** *"Demanded destination DEN link utilization"* (range 0–150).
  - **Secondary/qualitative check (verbatim):** *"we checked out that LEARNET met all the time the delay constraints of all the flows."*
  - **Not reported as separate metrics:** flow acceptance ratio (only referenced as the α=1 special case of the reward), jitter, packet loss, computational runtime, convergence speed, control-plane overhead.

- **P. Main quantitative results** (EXACT numbers with the comparison, quoted)
  - **Headline result, quoted verbatim (appears in abstract, Section V-B, and conclusion):**
    > *"the obtained results show that, for the scenario considered, LEARNET achieves a gain in the revenue of up to 45% compared to the baseline solution."*
    > *"Specifically, it achieves a gain in operator benefit up to 45% compared to the baseline solution (see Fig. 6)."*
    > *"LEARNET achieves a gain in the revenue of up to 45% compared to the baseline solution."*
  - **Directional result, verbatim:** *"As observed, LEARNET outperforms the baseline solution for every destination DEN link utilization considered."*
  - **Delay-constraint satisfaction, verbatim:** *"It shall be noted that we checked out that LEARNET met all the time the delay constraints of all the flows. The flow admission control of LEARNET enforces the fulfillment of the flow performance requirements (see Fig. 4). This block enhances the reliability of the LEARNET, which is crucial for supporting critical flows."*
  - **Scale of evidence:** 1,000,000 flows simulated per plotted point; x-axis swept 0→150% demanded destination-DEN link utilization.
  - **⚠️ The only exact quantitative figure stated in prose is "up to 45%".** Per-point values are only in Fig. 6 (raster image; not machine-readable from the retrieved PDF), so **no further numbers are reported here**. No percentages have been estimated from the figure.

- **Q. Main limitation**
  - **Author-acknowledged limitations (verbatim, Section IV-A):** *"the employed predictive analytics reveal three main assumptions taken into account for designing LEARNET: i) the flow lifetime duration obeys an exponential distribution, ii) the flow arrival process is Poissonian, and iii) the flow arrival process and the features of the future incoming flows to the system are stationary."* The authors then state: *"We might consider high-order statistics for the involved stochastic processes as well as their temporal dependence. In this way, we could remove the previous assumptions and improve the generality of the solution."*
  - **Structural limitations evident from the retrieved text (reviewer observation, not author claim):**
    - **Routing is assumed given** — *"explicit routes between every pair of DENs source and destination in the network is predefined"* — so LEARNET optimises only the per-hop queue/priority/delay-budget assignment, not the route.
    - **The RL algorithm itself is unspecified** — no algorithm name, no hyperparameters, no exploration policy, no convergence evidence. This is a serious reproducibility gap for a paper whose central contribution is *"a RL-based solution"*.
    - **Evaluation is a single 3-hop topology** with no topology-sensitivity/ablation study reported.
    - **No released simulator, code, or dataset.**
    - **Only one baseline**, and it is a static 3GPP-priority rule — not the SMT/TRS prior art in the same problem class.
    - **Delay budget fractions must sum to exactly 1** (constraint c.1), which is a hard structural restriction of the action space; the paper justifies it as improving acceptance ratio, but this forecloses partial-budget allocations.

- **R. Research gap this suggests**
  - **RL algorithm under-specification.** LEARNET frames the OFAP as an RL problem and defines the MDP (state, action, reward) carefully, yet never names the learning algorithm. A rigorous follow-up would need to instantiate and compare concrete learners (tabular Q-learning, DQN, PPO, actor-critic) on this exact MDP and report convergence/training cost.
  - **Asynchronous TSN (ATS/UBS) is under-studied relative to TAS/CQF.** The authors state the ATS OFAP is *"only tackled in [8] by Specht and Samii"*. This is a wide-open niche: RL for ATS-based asynchronous deterministic forwarding is essentially a one-paper field.
  - **Routing and scheduling are decoupled.** Joint route + ATS-allocation optimisation under the QAR1–QAR3 coupling rules is not addressed. The QAR2 constraint (a shaped queue binds to *one priority level in the previous hop*) creates an inter-hop coupling that a joint formulation could exploit.
  - **No head-to-head against exact/heuristic prior art.** The SMT solver and TRS of Specht & Samii are the natural optimality/heuristic reference points; a comparison of RL vs. exact optimisation on identical instances (including runtime and optimality gap) is missing.
  - **No comparison against 5G-TSN cross-domain schedulers.** LEARNET lives purely in the wired DetNet backhaul; the 5G radio segment (and hence the TSN-5G bridge problem addressed by papers 1 and 3 in this group) is out of scope. A gap exists for RL that spans the **wired ATS hop chain and the 5G uRLLC air interface jointly**.
  - **Generalisation beyond i.i.d./stationary/Poisson traffic** — explicitly flagged by the authors as future work (high-order statistics and temporal dependence).
  - **Scalability evidence missing** — the graph model is general (V, E) but only a 3-hop path is evaluated; behaviour on large topologies, many DEN pairs, and higher P_max is unexplored.

- **S. Best URL you actually retrieved + whether you read FULL TEXT or ONLY ABSTRACT**
  - **Read level: FULL TEXT READ** (complete 7-page peer-reviewed manuscript, converted with `pdftotext -layout` and `pdftotext -raw`; 486 lines of extracted text; all sections I–VI plus Tables I–II, Algorithm 1, Eqs. (1)–(5), and Figs. 1–6 captions inspected).
  - **Best URL actually retrieved (HTTP 200, `application/pdf`, 1,346,387 bytes):**
    - **https://aaltodoc.aalto.fi/bitstreams/5a2dd81e-1ad2-4bf5-83c3-270ed9383191/download** — Aalto University research repository (AaltoDoc), *"Peer reviewed version"* reprint.
  - **Supporting URLs:**
    - Unpaywall record establishing the OA location (green OA, repository, submittedVersion): https://api.unpaywall.org/v2/10.1109/ICC40277.2020.9149092
    - AaltoDoc item landing page: https://aaltodoc.aalto.fi/items/6092dc7a-d91f-4d0a-82de-1986d21cb70f/full
    - 6G Flagship publication page (abstract + official full citation + URN): https://www.6gflagship.com/publications/learnet/
    - Publisher DOI landing page (paywalled): https://ieeexplore.ieee.org/abstract/document/9149092
  - **Note on a failed route:** the Unpaywall-listed direct file URL `https://research.aalto.fi/files/45129042/Prados_Garzon_Learnet_IEEECC.pdf` returns **HTTP 403** (Cloudflare); the AaltoDoc bitstream link above is the working mirror of the same deposited manuscript.

---

### 3. A Joint Flow Scheduling Scheme for the Uplink of 5G-TSN in Industrial Internet of Things Systems

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - **Authors:** Jian Zhao; Tao Wang; Haonan Tong; Nuocheng Yang; Changchuan Yin; Dusit Niyato
  - **Affiliations (Crossref):** Jian Zhao, Tao Wang, Haonan Tong, Nuocheng Yang, Changchuan Yin — *Beijing Laboratory of Advanced Information Network, and the Beijing Key Laboratory of Network System Architecture and Convergence, Beijing University of Posts and Telecommunications (BUPT), Beijing, China*; Dusit Niyato — *College of Computing and Data Science, Nanyang Technological University (NTU), Nanyang Ave, Singapore*.
  - **Year / Venue:** **IEEE Transactions on Cognitive Communications and Networking**, **Vol. 12, pp. 2339–2354**.
    - **Year reporting is inconsistent across authoritative sources and is flagged here rather than resolved:** the **DOI is `10.1109/TCCN.2025.3583193` (2025)**; **Crossref `issued`/`published` = 2026**; **IEEE Xplore `publicationYear` = "2026"**; Semantic Scholar `year` = 2026. → Earliest-access year **2025**, issue year **2026**.
  - **DOI:** `10.1109/TCCN.2025.3583193`
  - **Type:** **Peer-reviewed journal article** (Crossref `type: journal-article`; DBLP key `journals/tccn/ZhaoWTYYN26`). Not a preprint.
  - **Reference count:** 41 (IEEE Xplore metadata).
  - **Availability note:** IEEE metadata explicitly reports `isOpenAccess: false`, `isFreeDocument: false`, `denialReason: "LICENSE"`.
  - **Funding acknowledged (IEEE metadata):** National Natural Science Foundation of China (grant 62471056); National Key Research and Development Program of China (grant 2024YFE0200300); Beijing Natural Science Foundation (grant L223027); Higher Education Discipline Innovation Project (grant B17007); National Research Foundation, Singapore and Infocomm Media Development Authority under its Future Communications… [truncated in metadata].
  - **Author keywords (from IEEE metadata):** **5G-TSN; multiple configure grants; age of synchronization; cooperative multi-agent proximal policy optimization.**
  - **IEEE Keywords (from IEEE metadata):** 5G mobile communication; Industrial Internet of Things; Wireless communication; Uplink; Symbols; 3GPP; Low latency communication; Job shop scheduling; Reliability; Quality of service.
  - **IEEE Index Terms (from IEEE metadata, full list):** Scheduling Scheme; Industrial Internet Of Things; Flow Scheduling; Wireless Networks; Flow Data; Mass Flow; Quality Of Service Requirements; Spectrum Resources; Proximal Policy Optimization; Decoding; Poisson Distribution; Time Slot; Flow Time; Beta Distribution; Orthogonal Frequency Division Multiplexing; Flow Injection; 5G Networks; Signal-to-interference-plus-noise Ratio; Non-orthogonal Multiple Access; Round-trip Time; Resource Block; Multi-agent Reinforcement Learning; Transmission Time Interval; Transmission Latency; Successive Interference Cancellation; Pilot Sequences; Guard Band; Control Scenario; Collision.

- **A. Exact problem solved**
  - Verbatim from the abstract: *"we focus on the design of a joint flow scheduling scheme for the uplink of 5G-TSN."*
  - Stated problem formulation (verbatim): *"to support massive device access, we formulate an optimization problem to maximize the number of successfully transmitted flows while satisfying the quality of service requirements. To solve the non-stationary and non-convex problem, we propose a cooperative multi-agent proximal policy optimization (CMA-PPO) based flow scheduling scheme to determine the MCG configuration with cognitive information of flows."*
  - Scope (verbatim): the work targets 5G-TSN as *"a crucial enabler for the wireless upgrade of the industrial Internet of Things (IIoT)"* expected *"to support the deterministic transmission of massive data flows in IIoT systems."*

- **B. Network architecture**
  - **Two coupled domains, uplink direction:**
    1. **5G part** — abstract (verbatim): *"in the 5G part, we propose a novel multiple configured grant (MCG) subframe structure to efficiently exploit the available spectrum resources."*
    2. **TSN part** — abstract (verbatim): *"in the TSN part, the age of synchronization (AoS) indicator, which measures the freshness of each flow arriving at the transparent bridge connecting 5G and TSN, determines which flow should be injected into the TSN."*
  - **Interconnection entity (verbatim):** a **"transparent bridge connecting 5G and TSN"** — the standard 5G-TSN logical-bridge integration point, at which flow arrival freshness is measured via the AoS indicator.
  - Direction of study: **uplink** (device → network), explicitly, unlike paper 1 which is end-to-end bidirectional.
  - **Physical topology, node counts, bridge counts, DS-TT/NW-TT placement, gNB count, TSN bridge hop count: NOT REPORTED** in the abstract (full text not retrieved).
  - **Index terms indicate the 5G air-interface mechanisms involved** (secondary, from IEEE metadata, not from the narrative): **OFDM** (Orthogonal Frequency Division Multiplexing), **NOMA** (Non-orthogonal Multiple Access), **SIC** (Successive Interference Cancellation), **pilot sequences**, **guard band**, **resource block**, **transmission time interval**, **SINR**. These imply a **grant-free / configured-grant NOMA uplink** with pilots and SIC-based decoding.

- **C. Network layer/domain**
  - **Cross-domain: 5G radio access (PHY/MAC — uplink grant scheduling and spectrum/resource-block allocation) + TSN (Layer 2 deterministic forwarding/queueing at the 5G-TSN transparent bridge).**
  - The joint scheme therefore couples a **wireless MAC/PHY scheduling decision** (MCG configuration) with a **wired TSN admission/injection decision** (which flow to inject into TSN, driven by AoS).
  - **Time scale relationship between the 5G subframe/TTI and the TSN scheduling cycle: NOT REPORTED** in the abstract.
  - Note: IEEE Index Terms include `Time Slot`, `Transmission Time Interval`, `Round-trip Time`, `Time Slot` — consistent with a **slot/subframe-level** formulation, but the abstract does not state this.

- **D. Network entities involved**
  - Derivable from the abstract: **IIoT devices / massive access devices** (uplink transmitters); the **5G network** (base station / gNB implied by uplink grant scheduling, though not named in the abstract); the **transparent bridge connecting 5G and TSN**; the **TSN domain**; **multiple RL agents** (the "cooperative multi-agent" PPO scheme).
  - Entities implied by the IEEE Index Terms list (secondary metadata, not narrative): gNB/scheduler, NOMA users, SIC receiver, resource blocks, pilots.
  - **Explicit named entity list (talkers, listeners, DS-TT, NW-TT, CNC, CUC, UPF): NOT REPORTED.**

- **E. Input/state parameters** (exact observation vector if reported)
  - **NOT REPORTED.** The abstract describes the *decision* as *"determine the MCG configuration with cognitive information of flows"* but does **not** enumerate the observation vector. Full text not retrieved.
  - Partial signal from the abstract: the **age of synchronization (AoS)** is an input/indicator — *"the age of synchronization (AoS) indicator, which measures the freshness of each flow arriving at the transparent bridge connecting 5G and TSN."*
  - Partial signal from IEEE Index Terms (secondary metadata): *Poisson Distribution*, *Beta Distribution*, *Flow Time*, *Signal-to-interference-plus-noise Ratio*, *Round-trip Time* — indicating that traffic arrivals and/or flow parameters are modelled stochastically and that SINR is an observable. **These are index-term hints, not a reported state vector.**

- **F. Decision variables** (exact action space if reported)
  - **NOT REPORTED** in explicit form. The abstract states that the scheme *"determine[s] the MCG configuration"* — i.e., the **action space is the configuration of the multiple configured grant (MCG) subframe structure** — and, on the TSN side, **"which flow should be injected into the TSN"** (a binary/selection decision per flow per interval, gated by AoS).
  - **Exact action vector, dimensionality, discretisation: NOT REPORTED.**

- **G. Objective function** (quote exact reward/cost)
  - **Optimisation objective (verbatim):** *"we formulate an optimization problem to maximize the number of successfully transmitted flows while satisfying the quality of service requirements."*
  - **Exact PPO reward function, penalty terms, discount factor: NOT REPORTED.**

- **H. Constraints**
  - Abstract (verbatim): *"while satisfying the quality of service requirements"* and *"The scheme can improve the number of successfully transmitted flows within the deadline constraints."* → **QoS requirements and per-flow deadline constraints** are the stated constraint class.
  - **Formal constraint list (spectrum, power, NOMA/SIC decoding order, resource-block budget, deadline equations): NOT REPORTED.**

- **I. Scheduling algorithm + optimization method**
  - Abstract (verbatim): *"we propose a cooperative multi-agent proximal policy optimization (CMA-PPO) based flow scheduling scheme to determine the MCG configuration with cognitive information of flows."*
  - **Optimisation method: deep multi-agent reinforcement learning (cooperative multi-agent PPO)** applied to a **non-stationary and non-convex** problem — the paper explicitly characterises the problem as *"the non-stationary and non-convex problem"*.
  - **Classical optimisation rejected** because of non-convexity/non-stationarity; **no convex relaxation, matching, or heuristic component is reported** in the abstract.
  - **Mechanism components named in the abstract:** (i) **MCG (multiple configured grant) subframe structure** on the 5G side; (ii) **AoS (age of synchronization) indicator** on the TSN side; (iii) **CMA-PPO** as the learning engine.
  - **PPO hyperparameters, network architecture, agent count, cooperation mechanism (shared critic / parameter sharing / centralised training decentralised execution), training schedule: NOT REPORTED.**

- **J. ML/DRL used?** yes/no and which
  - **YES — Deep Reinforcement Learning.** Specifically **Proximal Policy Optimization (PPO)** in a **cooperative multi-agent** formulation (**CMA-PPO**). This is explicitly a *policy-gradient / actor-critic* deep RL method, unlike DQHPSO (paper 1, tabular Double Q-learning wrapping a metaheuristic) and unlike LEARNET (paper 2, unspecified RL).
  - The IEEE Index Terms independently confirm both `Proximal Policy Optimization` and `Multi-agent Reinforcement Learning` as indexing concepts.

- **K. Simulator / testbed / dataset** (exact names + versions)
  - Abstract (verbatim): *"Extensive numerical simulations demonstrate that…"* → **NUMERICAL SIMULATION** (not a real testbed; no over-the-air or industrial pilot reported in the abstract).
  - **Exact simulator name, version, and configuration: NOT REPORTED.**
  - **Training dataset: NOT REPORTED** (the index term `Poisson Distribution` suggests synthetically generated traffic, but this is metadata inference, not a reported dataset).
  - **No code/artifact release reported.**

- **L. Traffic model**
  - **NOT REPORTED in the abstract.** Only the phrase *"deterministic transmission of massive data flows"* and *"massive device access"*.
  - **Index-term hints only (secondary, IEEE metadata):** `Poisson Distribution` (arrival process), `Beta Distribution` (possibly for flow/deadline or AoS distribution), `Flow Time`, `Time Slot`, `Transmission Time Interval`. **These are indexing concepts, not a reported traffic model — treat as unverified.**

- **M. Network scale**
  - **NOT REPORTED.** Abstract says only *"massive device access"* and *"massive data flows"* qualitatively. No device counts, cell counts, bandwidths, subcarrier counts, TSN hop counts, or number of agents are given.

- **N. Baselines** (exact names)
  - **NOT REPORTED.** The abstract refers only generically to *"benchmarks"* — verbatim: *"compared with benchmarks"* and *"about two times compared with the benchmarks"*. **No baseline is named in the abstract.**

- **O. Metrics**
  - **Primary metric (verbatim):** *"the number of successfully transmitted flows"* — reported as an improvement percentage and as a multiplicative factor.
  - **Deadline/QoS satisfaction** is used as a constraint: *"within the deadline constraints"*; the formulation *"maximize[s] the number of successfully transmitted flows while satisfying the quality of service requirements."*
  - Any other metrics (latency distribution, jitter, spectrum efficiency, AoS values, convergence speed, training cost, collision rate): **NOT REPORTED** in the abstract.

- **P. Main quantitative results** (EXACT numbers with the comparison, quoted)
  - **The one exact quantitative claim available, quoted verbatim:**
    > *"Extensive numerical simulations demonstrate that, compared with benchmarks, the proposed scheme improves the number of successfully transmitted flows by up to 24.02% and about two times compared with the benchmarks in the 5G-TSN network."*
  - Note the abstract's wording is ambiguous (it states *"by up to 24.02% and about two times compared with the benchmarks"*), i.e. **two distinct reported gains: up to 24.02% and approximately 2×**, over unnamed benchmarks. **Reported exactly as written; not smoothed or reinterpreted.**
  - **No other numbers, no per-figure values, and no baseline names are available** (abstract-only access). **No numbers have been fabricated.**

- **Q. Main limitation**
  - **NOT REPORTED** by the source retrieved (no limitations section accessible).
  - *Contextual observation from the abstract alone:* the reported gain is expressed against **unnamed "benchmarks"**, and the exact meaning of the paired figures ("up to 24.02%" **and** "about two times") is not disambiguated in the abstract.

- **R. Research gap this suggests**
  - *Inferred from the abstract only; labelled as reviewer observation.*
  - **Uplink asymmetry is under-addressed.** This paper targets the **uplink** specifically — the direction where 5G-TSN integration is hardest (grant acquisition, configured-grant collisions under massive access). Papers 1 and 2 in this group do not treat the uplink/radio-grant problem at all. A gap exists for unified **uplink grant scheduling + TSN injection** treated jointly, which is exactly what this paper claims.
  - **AoS as a cross-domain scheduling signal is novel and under-explored.** Using *age of synchronization* (freshness at the transparent bridge) as the TSN injection criterion is a distinctive contribution; there is no evidence in the abstract of comparison against alternative freshness/staleness metrics (e.g., age of information, deadline slack, or pure FIFO/EDF).
  - **Multi-agent cooperation for TSN-5G is essentially unexplored.** CMA-PPO here is one of very few multi-agent DRL applications to the 5G-TSN bridge; gaps remain in **agent-count scalability, non-stationarity handling guarantees, and CTDE (centralised-training-decentralised-execution) assumptions** — none of which are disclosed in the abstract.
  - **Reproducibility gap:** no simulator, dataset, hyperparameters, or baseline names are available in the public abstract.
  - **Cross-paper gap for this group:** the three papers in this group occupy three disjoint niches — (1) DQHPSO = *end-to-end TSN-5G scheduling via RL-tuned PSO*; (2) LEARNET = *asynchronous wired DetNet/ATS flow allocation via RL + analytical models*; (3) CMA-PPO = *5G uplink + TSN injection via cooperative multi-agent PPO*. **No paper in this set addresses (a) joint routing + scheduling, (b) ATS-style asynchronous shaping in the converged 5G-TSN setting, or (c) head-to-head benchmarking across these three paradigms.** That is the evident gap this group exposes.

- **S. Best URL you actually retrieved + whether you read FULL TEXT or ONLY ABSTRACT**
  - **Read level: ONLY ABSTRACT** (plus complete IEEE metadata: venue, volume, pages, author list, affiliations, funding, full keyword/index-term lists).
  - **Best URL actually retrieved (HTTP 200; abstract extracted from the embedded IEEE metadata JSON):**
    - **https://xplorestaging.ieee.org/document/11050959**
  - **Supporting URLs:**
    - Crossref record (venue, volume 12, pp. 2339–2354, full author affiliations): https://api.crossref.org/works/10.1109/TCCN.2025.3583193
    - Semantic Scholar record (confirms publisher-elided abstract, DBLP key): https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TCCN.2025.3583193
    - Unpaywall verification (closed): https://api.unpaywall.org/v2/10.1109/TCCN.2025.3583193
    - Publisher landing page (paywalled, `isOpenAccess: false`): https://ieeexplore.ieee.org/document/11050959
  - **Full-text PDF:** NOT OBTAINED. Paywalled at IEEE Xplore (`denialReason: "LICENSE"`).

---

## Appendix — Retrieval Log (method compliance and failures)

**Per-paper search phrasings used (≥3 each, as mandated):**

| Paper | Phrasings issued |
|---|---|
| 1 (DQHPSO) | `"<title> pdf"`; `"<title> arXiv"`; `"<title> IEEE ACM Transactions on Networking 2023"`; `"DQHPSO" TSN-5G traffic scheduling Double Q-learning hierarchical particle swarm`; `"level-based population structure" DQHPSO …`; `TSN-5G end-to-end traffic scheduling DQHPSO scheduling success ratio time-triggered flows comparison algorithms`; `Haipeng Yao BUPT publications TSN-5G scheduling pdf repository`; `"Reinforcement Learning-Based Particle Swarm Optimization for End-to-End Traffic Scheduling" filetype:pdf` |
| 2 (LEARNET) | `"<title> ICC"`; `"<title> IEEE"`; `"LEARNET" Prados-Garzon Taleb Bagaa pdf flow scheduling deterministic`; `Prados-Garzon LEARNET flow scheduling filetype:pdf` |
| 3 (CMA-PPO) | `"<title>"`; `"<title> abstract …"`; `Joint Flow Scheduling Uplink 5G-TSN IIoT Nanyang repository DR-NTU`; `Tao Wang BUPT 5G-TSN joint flow scheduling multiple configured grant arXiv preprint`; `"5G-TSN" uplink joint flow scheduling CMA-PPO cooperative multi-agent proximal policy optimization` |

**APIs and routes actually queried:**

| Route | Paper 1 | Paper 2 | Paper 3 |
|---|---|---|---|
| Semantic Scholar Graph API | ✅ metadata + abstract | ✅ metadata | ⚠️ metadata, abstract **elided by publisher** |
| Crossref REST API | ✅ venue/DOI/year/type | ✅ venue/DOI/pages/authors | ✅ venue/vol/pages/authors/affiliations |
| Unpaywall v2 API | ❌ `closed` | ✅ **green OA located** | ❌ `closed` |
| OpenAlex API | ❌ HTTP 403 — *"Insufficient budget… Add funds at openalex.org/pricing"* (account-level quota exhausted; retry-after 30313 s) | ❌ same | ❌ same |
| arXiv API (HTTPS) | ✅ no version exists | ✅ no version exists | ✅ no version exists |
| OpenAIRE API | ✅ 0 web resources | ✅ records exist, 0 direct web resources | ✅ 0 web resources |
| DBLP API | ❌ HTTP 429 rate-limited (key still confirmed via Semantic Scholar `externalIds.DBLP`) | ❌ same | ❌ same |
| IEEE Xplore `xplorestaging` metadata endpoint | ✅ (abstract **not** exposed; `isOpenAccess:false` confirmed) | — | ✅ **abstract recovered here** |
| fatcat / scholar.archive.org / BASE / CORE | ❌ timeout / Anubis bot-wall / HTTP 403 | — | — |
| Google-Scholar-style routes (ResearchGate, ACM DL) | ❌ HTTP 403 Cloudflare | — | — |

**Explicit failure disclosure:** For **papers 1 and 3** no open-access full text exists on any legitimate route checked (`Unpaywall` = closed; `Semantic Scholar` `openAccessPdf.url` empty; `arXiv` = no version; `OpenAIRE` = zero web resources; publisher = `isOpenAccess:false`). Their entries above therefore contain **only** what the published abstracts and verified bibliographic metadata state, with every non-derivable field marked `NOT REPORTED`. **No field has been filled from memory, inference, or analogy to the other papers.**

**Downloaded artifacts in this working directory:**
- `learnet_icc2020.pdf` — LEARNET accepted manuscript (1,346,387 bytes, 7 pages) ✅ verified correct paper (title on p. 1 matches)
- `learnet_icc2020.txt` / `learnet_raw.txt` — `pdftotext -layout` and `-raw` conversions (486 / 821 lines)
- `ieee_p3.html` — IEEE Xplore staging metadata page containing the verbatim P3 abstract
- `polyu_p1.html`, `hkust_p1.html` — repository records containing the verbatim P1 abstract
- `flag_learnet.html` — 6G Flagship record (official citation + URN + abstract)
