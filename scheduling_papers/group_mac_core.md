# Group: 5G MAC-layer scheduling, network slicing & 5G-core/user-plane scheduling — detailed technical extraction

Prepared for a PhD literature review. Every quantitative claim below is traceable to a retrieved source; anything not present in the retrieved source is marked **NOT REPORTED**. Where the retrieved artefact was a preprint or an accepted manuscript rather than the publisher's version of record, this is stated explicitly.

**Retrieval tooling used:** `web_search`, `web_fetch`, `curl` (including the `r.jina.ai` text-extraction proxy for publisher pages that block plain `curl`), `pdftotext -layout`, Crossref REST API (`api.crossref.org`), Semantic Scholar Graph API (`api.semanticscholar.org/graph/v1`), Unpaywall (`api.unpaywall.org`), DOAJ (`doaj.org/api`), DuckDuckGo Lite (`lite.duckduckgo.com` via the proxy).
**APIs that failed / were unavailable in this session:** OpenAlex (`api.openalex.org`) returned HTTP 429 `"Rate limit exceeded ... you only have $0 remaining"` for every query — **no OpenAlex data was used**. DBLP's API returned an Anubis anti-bot challenge page. `scholar.archive.org`, `mojeek.com`, `searx.be`, `search.inetol.net`, `baresearch.org` and Google Scholar all returned bot-protection/403 responses. IEEE Xplore and `iris.unitn.it` block plain `curl` (HTTP 502/403); their content was retrieved through the `r.jina.ai` text proxy instead.

---

## Paper 1

### Learn to Schedule (LEASCH): A Deep Reinforcement Learning Approach for Radio Resource Scheduling in the 5G MAC Layer

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Faroq Al-Tam, Noélia Correia, Jonathan Rodriguez.
  **2020** (received 14 May 2020; accepted 30 May 2020; date of publication 8 June 2020).
  **Venue:** *IEEE Access*, Vol. 8, pp. 108088–108101. **Peer-reviewed journal** (IEEE Access), **open access, CC-BY 4.0** ("This work is licensed under a Creative Commons Attribution 4.0 License").
  **DOI: 10.1109/ACCESS.2020.3000893** (verified via the publisher PDF page 1 and via Crossref, which returns `title = "Learn to Schedule (LEASCH): A Deep Reinforcement Learning Approach for Radio Resource Scheduling in the 5G MAC Layer"`, `container-title = "IEEE Access"`, `issued = 2020`, `volume = 8`, `page = 108088-108101`, `type = journal-article`, `publisher = Institute of Electrical and Electronics Engineers (IEEE)`).
  An author preprint exists as **arXiv:2003.11003v1 [cs.NI], 24 Mar 2020** (6 pages, titled "Learn to Schedule (LEASCH): A Deep reinforcement learning approach for radio resource scheduling in the 5G MAC layer."). Both the published version and the preprint were retrieved and read; **discrepancies between them are flagged below**.

- **A. Exact problem solved:**
  The **radio resource scheduling (RRS) problem in the 5G MAC layer**: filling the time–frequency resource grid by deciding, for every resource block group (RBG) in every slot, **which single eligible UE wins that RBG**, so as to jointly optimise throughput and fairness. Verbatim: *"the current article presents LEASCH, a deep reinforcement learning model able to solve the radio resource scheduling problem in the MAC layer of 5G networks."* And: *"the problem boils down to filling the resource grid by deciding which UE will win the current RBG in the current slot. However, not all users can be considered for scheduling at the current RBGs. Only those that are eligible (active) will be considered and allowed to compete for the RBGs under consideration. A UE is eligible if it has data in the buffer and is not retransmitting in the current slot, i.e., if it is not associated with a HARQ process in progress."* The stated design goal is a **numerology-agnostic** agent: *"The proposed model works under different numerologies with no modification to its architecture or retraining."*
  **Scheduling is the central contribution of this paper** (the agent *is* the scheduler; it is plugged in "like any other conventional scheduling algorithm").

- **B. Network architecture:**
  Single-cell **5G NR** radio access network. The available bandwidth is divided into **resource blocks (RBs)**, each RB = 12 subcarriers; a set of RBs is aggregated into a **resource block group (RBG)**, which is *"the smallest scheduling unit."* The time domain is divided into frames, each frame into 10 subframes; the number of slots per subframe, slot duration and RB bandwidth depend on the numerology index (their Table 1). *"The radio resource scheduler runs at the gNB at every (or kth) slot and uses this information to share the available RBGs between active UEs."* The gNB collects *"channel feedback information, buffer, HARQs, and allocation log"* from the UEs. **Centralized** scheduling at the gNB (the paper explicitly classifies its own work as a *"fine-grained centralized"* DRL approach).

- **C. Network layer/domain:**
  **MAC layer of the 5G NR radio access network** (radio resource management / RRS). Not a core-network or transport paper.

- **D. Network entities involved:**
  **gNB** (hosts the scheduler/agent; centralized network view), **UEs** (the scheduling candidates; 4 UEs in the main experiments, 8 UEs in the scalability experiment), **HARQ processes** (used to determine eligibility), **UE buffers** (data availability), and **CQI / MCS** feedback (channel quality).

- **E. Input/state parameters (exact observation vector as reported):**
  The state is deliberately split into three parts — **eligibility**, **data rate**, and **fairness** — and then combined:
  1. **Eligibility vector `g`** (Eq. 18): a binary indicator per UE, `g_u = 1` if UE `u` is eligible, `0` otherwise, `∀u ∈ U`. The paper states they do *not* feed raw buffer/HARQ status: *"instead of feeding the buffer and the HARQ status of each UE to the LEASCH, and ask the agent to learn 'eligibility', we simplify the task for the agent by calculating a binary vector g to act as an eligibility indicator."*
  2. **Data-rate vector `d`**: derived from *"the valid entries of modulation and coding schemes (MCSs) in Table 5.1.3.1-2 in the 5G physical layer specification TS 38.214"* — i.e. the MCS/bit-per-symbol information rather than a raw bit rate.
  3. **Fairness vector `f`** (Eq. 19): an allocation log initialised to all zeros at the start of each episode and updated per scheduled RBG:
     `f_u = max(f_u − 1, 0)` if `u` is selected; `f_u = f_u + 1` if `u`'s buffer is not empty. *"Therefore, f represents the allocation-log of the resources."* and *"f also represents the delay, because if a UE did not access the resources for too long, its corresponding value in f will be large."*
  **Fusion:** `d̂ = d ∘ g` (Hadamard product, Eq. 20), giving the final state vector `s = [d̂  f]ᵀ`. *"For a better learning stability we normalize d̂ and f to the range [0, 1]."* **Input layer size = 2 × |U|** (confirmed in the experimental setup).

- **F. Decision variables (exact action space as reported):**
  *"The action is to select one of the UEs in the system. It is encoded in hot-one encoding."* (one-hot; `|U|` actions). **Output layer is a layer of size |U|.** At deployment, the action is taken as `u = arg max_{a∈A} Q(s, a; θ)`, and if `u ∈ Û` the current RBG is assigned to `u`.

- **G. Objective function (exact reward/cost):**
  Eq. (21), verbatim:
  `r(s, u; K) = −K` if `u` is none-eligible; otherwise `r(s, u; K) = d̂_u × (min_u f_u / max_u f_u)`.
  (The PDF renders this as a stacked fraction with `min_u f_u` as numerator and `max_u f_u` as denominator; confirmed in both the `pdftotext -layout` and `pdftotext -raw` extractions of arXiv:2003.11003, and referred to in the published version as *"the throughput-fairness reward, i.e., { d̂u × min_u f_u / max_u f_u } in (21)"*.)
  Interpretation given by the authors: *"where K is a threshold to represent the negative penalization signal for scheduling an inactive UE, and f is updated using (19). We can easily see that, our reward is a variant of a discounted bestCQI function, where the data rate is discounted by the resource sharing fairness."*
  The stated intent: *"From our state design the goal is to encourage the agent to transmit at the RBGs with the highest MCS, i.e., highest bit-per-symbol, to increase the throughput in the system. At the same time, we would like the agent not to compromise the resource sharing between the users."* The agent maximises expected discounted return `G_t = E[Σ_k γ^k r(s_{t+k}, a_{t+k}) | s_0 = s_t]` (Eq. 1). **The numerical value of K is NOT REPORTED** (it is absent from the published DRL hyper-parameter table as extracted; the hyper-parameter tables list α, optimizer, gradient threshold, ε, min ε, δ_ε, |R|, M, T, β, episode length and number of episodes only).

- **H. Constraints:**
  - **Eligibility constraint:** only UEs with data in the buffer **and** not associated with an in-progress HARQ process may be scheduled; this is enforced structurally by the eligibility vector `g` and `Û`, and penalised through the `−K` reward term.
  - **One UE per RBG:** the scheduler assigns the current RBG to exactly one selected UE (*"select an active (eligible) UE from a set of candidate UEs and assign that RBG to the selected UE"*).
  - **Numerology/frame constraints:** RBG size and RB counts are determined by the numerology configuration (their Table 1 / Table 3); the model must remain valid across numerologies without retraining.
  - **Explicit optimisation constraints (maximise/minimise subject to…): NOT REPORTED** — the paper formulates the problem as an MDP solved by DRL rather than as a constrained optimisation program.

- **I. Scheduling algorithm + optimization method:**
  **LEASCH = a Double Deep Q-Network (DDQN) agent**, critic-only, trained as an episodic DRL problem and then deployed as a drop-in scheduler. Learning machinery reported: **ε-greedy** action selection with `ε` annealed as `max{ε − δ_ε, min_ε}`; **experience replay memory R** (cyclic queue) from which mini-batches are sampled; a separate **target critic network** whose weights are updated from the on-line network **every T steps using smoothing** `θ̂ = βθ + (1−β)θ̂`; loss = squared Bellman error (MSBE) updated by SGD with learning rate α; DDQN target `Q_target = r_{t+1}(s,a) + γ Q(s_{t+1}, arg max_a Q(s_{t+1}, a, θ); θ̂)`. Training is **off-simulator** ("in a sand-box"), then deployment uses a single forward pass with no retraining. Hyper-parameters (published Table 2 as extracted / arXiv Table I): DNN learning rate α = 1e−4, optimizer = **Adam**, gradient threshold = 1, ε = 0.99, min ε = 0.01, ε decaying factor δ_ε = 1e−4, experience replay memory |R| = 1e6, mini-batch M = 64, smoothing frequency T = 20, smoothing threshold β = 1e−3, episode length = 150 RBG. **Number of training episodes: the arXiv table states "500 Training episodes" while the text and Figure 2 caption state convergence "in less than 300 episodes" and show a curve "for 2000 episodes" — this inconsistency exists in the retrieved sources and is reported verbatim rather than resolved.**
  DNN architecture: **two fully connected hidden layers of 128 neurons each, ReLU activation**; *"The number of layers and neurons are selected empirically."*

- **J. ML/DRL used? yes/no and which:**
  **Yes — Deep Reinforcement Learning, specifically Double Deep Q-Network (DDQN)** (value-based, critic-only, off-policy; DQN/Double-DQN theory is developed at length in Section II). The authors state: *"LEASCH is a breed of DDQN critic-only agents that learns discrete actions from a sequence of states."* Implementation uses MATLAB's `rlDQNAgent` object (visible as *"Episode Reward for SEFair Small v2 with rlDQNAgent"* in the arXiv Figure 2 caption — quoted verbatim from the retrieved figure label).

- **K. Simulator / testbed / dataset (exact names + versions):**
  - **Simulation only — no testbed.** Deployment and testing use *"a 5G system level simulator"*; the text never names it. **The simulator's product name is NOT REPORTED** in either the published version or the arXiv preprint. It is described as *"a 5G system level simulator that uses all recent components and configurations of a 5G network."*
  - **Implementation environment:** *"All methods and algorithms presented/discussed here are implemented in Matlab 2019b in a PC running Linux with i7 2.6GHz, 32GB RAM, and GPU Nvidia RTX 2080Ti with 11 GB."* Training runs *"in a pool of parallel threads in the GPU."*
  - **Training environment ≠ deployment environment:** training happens in an off-simulator sand-box; testing happens in the 5G system-level simulator. The arXiv figure label suggests a scenario/setup named **"SEFair Small v2"** (verbatim figure caption text; the paper does not otherwise define this name).
  - **Dataset:** **NOT REPORTED** (no external dataset is used).

- **L. Traffic model:**
  **NOT REPORTED.** No arrival process, packet-size distribution, offered-load model or full-buffer assumption is specified anywhere in the retrieved published version or the arXiv preprint (searches for "traffic model", "arrival", "full buffer", "FTP", "Poisson", "packet size", "offered load" return no such specification). The only traffic-related mechanism described is per-UE buffer occupancy entering the eligibility test.

- **M. Network scale:**
  From the arXiv Table II ("Adopted parameters for LEASCH testing on 5G network"), quoted verbatim: *Radio access tech.* = **3GPP 5G NR**; *Test time* = **250 frames**; *Simulation runs* = **100 runs with different deployment scenarios**; *Numerology index µ* = **{0, 1, 2}**; *Bandwidth* = **{5 MHz, 10 MHz, 20 MHz}**; *UEs* = **4**; *SCS* = **{15 kHz, 30 kHz, 60 kHz}**; *No. of RBs* = **{25, 24, 24} "see [2]"**; *Scheduling period* = **1 RGB** [sic — RBG]; *RBG size* = **2 RBs according to configuration 1 in [3]**; *Total tested RBGs* = **250 × 100 × {130, 240, 480} RBGs**; *Channel development* = **"Randomly changes each 41 second"** [sic, verbatim]; *HARQ* = **True**. The published text additionally reports a **larger-scale experiment with 8 UEs** (its Figure 7: *"KPIs for 8 UEs simulated for 250 frames using 30kHz SCS under 10MHz BW for 100 runs"*). **Single cell / single gNB; no multi-cell, multi-slice or core-network scale is evaluated.**

- **N. Baselines (exact names):**
  **Proportional Fairness (PF)** and **Round Robin (RR)**. Quoted: *"a comparison with two baseline algorithms, proportional fairness (PF) and round robin (RR). These are widely used algorithms in literature and in practice."* (BestCQI is mentioned as a conventional scheme in the introduction but is **not** used as an experimental baseline.)

- **O. Metrics:**
  *"Throughput, goodput, and fairness are the main key performance indicators (KPIs) used for evaluation. For throughput, the sum of achievable data rate in the cell is reported. For goodput, the delivered data rate is measured at the receiver. For fairness, the popular Jain's fairness index (JFI) is used."* Training diagnostics: episode reward / average reward / theoretical long-term reward, plus a decomposed reward analysis (probability of scheduling active-only UEs vs. throughput–fairness reward).

- **P. Main quantitative results (EXACT numbers with the comparison, quoted):**
  - **5 MHz BW / 15 kHz SCS:** *"LEASCH has improved the throughput by ≈ 2.4% and 18% compared to PF, and RR, respectively. In terms of goodput, LEASCH is better by ≈ 3% and 20 % compared to PF and RR, respectively… For the JFI, LEASCH is ≈ 1% and 4.3% better than PF and RR, respectively."*
  - **10 MHz BW / 30 kHz SCS:** *"LEASCH has improved the throughput by ≈ 3% and 19% compared to PF and RR, respectively. In terms of goodput, LEASCH is ≈ 3.3% and 21% better than PF and RR, respectively. Regarding JFI, LEASCH is ≈ 2% and 5% better than PF and RR, respectively."*
  - **20 MHz BW / 60 kHz SCS:** *"LEASCH has improved the throughput by ≈ 3% and 18% compared to PF and RR, respectively. For goodput, LEASCH outperformed PF and RR by ≈ 4% and 20%, respectively. Regarding JFI, LEASCH improved the fairness compared to PF and RR by ≈ 2% and 5%, respectively."*
  - **8-UE scalability experiment (30 kHz SCS, 10 MHz BW, 250 frames, 100 runs):** *"In terms of throughput it is 5% and 13% better than PF and RR, respectively. Regarding goodput it is 7% and 14% better than PF and RR. For JFI, it has shown similar results as PF and is 2% better than RR."*
  - **Learning/convergence:** *"LEASCH was able to converge in less than 300 episodes."* and *"around episode 300, LEASCH was able to converge for both objectives."*
  - Qualitative claim: *"One nice property of LEASCH is that it is able to push all the KPIs without compromising any of them."* and *"LEASCH outperforms PF and RR since it reaches higher throughput-goodput, especially from the period 5 to 8 time units where major changes have occurred in the channel."*

- **Q. Main limitation:**
  The evaluation is small-scale and simulation-only: **4 UEs** in the main experiments (8 UEs in a single scalability run), a **single cell/gNB**, a **MATLAB system-level simulator that the paper does not even name**, and **no traffic model**; **no real testbed or over-the-air validation** is performed. The authors' own stated limitation/future work: *"As a future work, a more advanced version of LEASCH will be developed to serve larger set of users. It will be developed and deployed under larger 5G network with a mixture of numerologies and more complex rewarding systems that include different type of services."* Also acknowledged: the policy analysis is only *"visual inspection"* and *"our discussion here lacks analytical bases, due to the complexity of the problem."* The agent is **not slice-aware and not QoS-flow-aware** — it optimises a single cell-wide throughput/fairness trade-off.

- **R. Research gap this suggests:**
  (i) Scaling DRL MAC schedulers beyond ~4–8 UEs and beyond a single cell/gNB remains open — the paper's own future work. (ii) **No slice/QoS-flow/5QI awareness:** LEASCH has no notion of network slices, 5QI, GBR/non-GBR or per-flow latency budgets, so it cannot serve the RAN-slicing or QoS-flow scheduling problems studied elsewhere in this review — a natural bridge to Papers 2 and 3 below. (iii) **No cross-layer or core-network coupling:** the agent never interacts with the 5G Core, UPF or PDU-session/QoS-flow establishment, so RAN-side decisions and core-side user-plane decisions are optimised in isolation. (iv) Reproducibility is hampered by the **unnamed simulator** and the absent traffic model; a PhD-level replication would need a named open simulator (e.g. ns-3/5G-LENA, Simu5G, OpenAirInterface). (v) Off-simulator training gives generality but no demonstrated online adaptation or safety guarantees.

- **S. Best URL actually retrieved + whether read FULL TEXT or ONLY ABSTRACT:**
  - **Published version of record (full text retrieved via text proxy, 14 pages):** `https://ieeexplore.ieee.org/ielx7/6287639/8948470/09110842.pdf` — **FULL TEXT READ.**
  - **Open-access author preprint (PDF downloaded and converted locally, 6 pages):** `https://arxiv.org/pdf/2003.11003` — **FULL TEXT READ.**
  - **FULL TEXT READ (both).** Local artefacts: `pdfs/leasch_arxiv.pdf`, `pdfs/leasch_arxiv.txt`, `pdfs/leasch_ieee_published.txt`.
  - Note: direct `curl` of the IEEE PDF returns HTTP 502 (bot protection); the publisher PDF text was obtained through `r.jina.ai`. Unpaywall independently confirms `is_oa: True` with `publishedVersion` at the IEEE URL (CC-BY) and `submittedVersion` at `https://arxiv.org/pdf/2003.11003`.

---

## Paper 2

### "Toward a Flexible and Reconfigurable 5G Network Slicing Scheduler" — **THIS PUBLICATION COULD NOT BE FOUND TO EXIST**

**Finding (stated up front, as required by the rigor rules): after searching the exact title with at least six distinct phrasings across four independent bibliographic/search systems, I could not verify that any paper with this title exists. No authors, year, venue or DOI can be reported, because none was found. I therefore report the negative result with its evidence, and then fully extract the closest *real, verified* publications.**

**Search evidence (all queries executed):**
1. **DuckDuckGo Lite, exact phrase** `"Toward a Flexible and Reconfigurable 5G Network Slicing Scheduler"` → **"No results found"**.
2. DuckDuckGo Lite, exact phrase `"Towards a Flexible and Reconfigurable 5G Network Slicing Scheduler"` → **"No results found"**.
3. DuckDuckGo Lite, exact phrase `"A Flexible and Reconfigurable 5G Network Slicing Scheduler"` → **"No results found"**.
4. DuckDuckGo Lite, exact phrase `"5G Network Slicing Scheduler"` → **"No results found"**.
5. **Crossref** `query.bibliographic` and `query.title` for the title → the only returned items are unrelated (e.g. *"Flexibly Controlled 5G Network Slicing"*, ICCSPA 2022; *"Flexible Function Split Over Ethernet Enabling RAN Slicing"*; *"Autonomic reconfigurable 5G network slicing…"*, Computer Networks 2026). **No title match.**
6. **Semantic Scholar Graph API** `paper/search?query=Flexible and Reconfigurable 5G Network Slicing Scheduler` (succeeded on the 7th retry, `total: 112`) → the nearest titles returned are *"Designing the 5G network infrastructure: a flexible and reconfigurable architecture based on context and content information"* (EURASIP JWCN 2018), *"Intelligent Resource Allocation via Hybrid Reinforcement Learning in 5G Network Slicing"* (IEEE Access 2025), *"MADDPG-Based Deployment Algorithm for 5G Network Slicing"* (Electronics 2024), *"Flexible Network Slicing Assisted 5G for Video Streaming with Effective and Efficient Isolation"* (ITC 2020). **No title match.**
7. **OpenAlex** → unusable this session (HTTP 429, "Insufficient budget… $0 remaining"), so OpenAlex could not corroborate.
8. The Bing results page for the exact phrase returned only unrelated AI-generated filler (semiconductor-market articles), i.e. **no indexed document contains the phrase**.
9. A sanity check confirmed the search channel works: the same DuckDuckGo Lite route returns correct results for `Learn to Schedule LEASCH` and for `"network slicing" scheduler 5G`.

**Interpretation:** the requested title appears to be a **misremembered or conflated title**. The most likely real papers behind it are the two verified works extracted below, plus (documented, abstract-level only) a third. **Recommendation to the parent agent: replace Paper 2 with one of these verified papers, or re-confirm the intended title with the requester before citing anything under the original title.**

---

### Paper 2 — CLOSEST VERIFIED MATCH A (recommended substitute; full text available)

### NRflex: Enforcing network slicing in 5G New Radio

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Karim Boutiba, Adlen Ksentini, Bouziane Brik, Yacine Challal, Amar Balla.
  **2022** (issue January 2022). **Venue: *Computer Communications* (Elsevier), Vol. 181, pp. 284–292.** **Peer-reviewed journal.**
  **DOI: 10.1016/j.comcom.2021.09.034** (verified via Crossref: `title = "NRflex: Enforcing network slicing in 5G New Radio"`, `container-title = "Computer Communications"`, `volume = 181`, `page = 284-292`, `issued = 2022-01`, `publisher = Elsevier BV`, `type = journal-article`).
  **Version read:** the accepted author manuscript distributed by EURECOM (affiliations: EURECOM Sophia Antipolis; DRIVE EA1859, University of Bourgogne Franche-Comté; LMCS, Ecole nationale Supérieure d'Informatique, Algiers). Unpaywall confirms `is_oa: True` with the accepted version at the DOI. **This is an accepted manuscript, not the publisher's typeset version of record — page numbers and figure numbering may differ from the published article.**

- **A. Exact problem solved:**
  RAN slicing in 5G NR: how to *dynamically* assign **Bandwidth Parts (BWPs) with the appropriate physical numerology** to running network slices and their UEs so that each slice's QoS requirement (uRLLC max latency; eMBB desired throughput) is met while minimising the PRBs consumed. Verbatim: *"we introduce a new framework, namely New Radio flexibility (NRflex), which addresses the challenge of slicing the RAN in 5G. NRflex provides a solution that dynamically assigns BWP to the running slices and their associated User Equipment (UE), aiming to fulfill the slices' required QoS."* And: *"NRflex's main idea is to jointly allocate numerology and radio resources for each slice, aiming that UEs can use multiple slices with different requirements."*
  **How central is scheduling?** The framework's *central contribution is the slice-level BWP/numerology reconfiguration loop* (RIC-side) plus the MAC-level BWP multiplexing; PRB allocation to logical channels is the *allocation* step carried out by the (pre-existing) **MAC Scheduler**, which NRflex feeds. So scheduling is **central to the framework but the paper is not a new MAC scheduling algorithm** — it is a slicing/BWP-orchestration framework that *drives* the MAC scheduler and adds two pre-processors and a multiplexer.

- **B. Network architecture:**
  **O-RAN-aligned 5G NR RAN.** NRflex components are distributed between the **RIC** and the **gNB**:
  - **Slice Orchestrator (SO)** — *"not defined by the O-RAN architecture"*; provides the end-to-end slice template and manages end-to-end slice LCM (only the RAN part is in scope).
  - **RIC Non-RT** — launches slice creation/deletion and gathers general performance KPIs from the RAN *"via the O-RAN O1 interface."*
  - **RIC Near-RT** — hosts two NRflex control applications: the **Network slicing master** (manages slices across many gNBs; checks UE–slice association; collects gNB statistics) and the **BWP manager** (Algorithm 1; re-adapts BWP size per slice using O-RAN **E2** feedback) plus a **Network slicing agent**.
  - **gNB** — hosts per-slice **Pre-processors** (eMBB pre-processor Algorithm 2; uRLLC pre-processor Algorithm 3), the **BWP Multiplexer** (Algorithm 4) and the **MAC Scheduler**. The BWP multiplexer *"generates DCI (Downlink Control Indicator) [23] to be sent to the concerned UEs indicating the decision."*
  - Slice definition is three-levelled: **Application level** (type uRLLC/eMBB/mMTC, requirements, duration, associated UEs, region), **MAC level** (*"a slice is a set of Logical Channels (LC) belonging to different UEs"*), **Physical level** (*"a slice is considered as a BWP associated with numerology according to the slice type"*).

- **C. Network layer/domain:**
  **RAN / MAC layer (and NR physical-layer numerology/BWP configuration)**, with a slice-management control plane mapped onto O-RAN (Non-RT RIC / Near-RT RIC / E2 / O1). Not a core-network paper (the paper explicitly scopes out the core: *"Although the end-to-end slice includes other components to deploy, such as the Core Network, the applications, and the transport network, we focus only on the RAN part in this work."*).

- **D. Network entities involved:**
  Slice Orchestrator; Service Management and Orchestration (SMO) framework; Non-RT RIC; Near-RT RIC (Network Slicing Master, Network Slicing Agent, BWP Manager); gNB(s) (Pre-Processor, BWP Multiplexer, MAC Scheduler); UEs (each associated with two slices in the evaluation); Logical Channels (LCs); PDUs; Non-RT and Near-RT databases.

- **E. Input/state parameters (exact observation vector if reported):**
  **No RL state vector — this is not a learning paper.** The controller inputs are explicitly enumerated pieces of standard telemetry:
  - From gNBs to Near-RT RIC: *"gNB statistics"* and *"KPIs + Consumed PRBs"* — the paper names *"CQI, RSRP, RSRQ…"* as gNB statistics.
  - Two computed KPIs drive re-adaptation (Monitoring step): `throughput_success_rate` (*"best value 1, worst value 0"*; *"takes into account the actual throughput, the desired throughput, and the queue size. Its value reaches 1, if the actual throughput reaches the desired throughput or the data queue is empty"*) and `deadline_failure_rate` (*"best value 0, worst value 1"*; *"monitors the PDUs that exceed their deadline"*).
  - Per-UE/per-LC inputs to the pre-processors: **buffer/queue size**, **UE CQI**, **head-PDU remaining time (`remaining_time(pdu_j)`)**, **PDU size**, LC requirements, and the BWP manager's max PRB allocation.
  - Per-UE weight **α_UE** (*"a weight associated with a UE indicating how many eMBB slices of this UE were discriminated in the Multiplexing stage"*), used to control how much throughput to achieve in the current slot.

- **F. Decision variables (exact action space if reported):**
  **No RL action space.** The decision variables are:
  - **BWP size per slice** — `NewPRB_j`, the number of PRBs to allocate for slice `j` (i.e. the BWP size of slice `j`) in the next time interval, computed by the BWP manager.
  - **Active numerology/BWP per UE per slot** — selected by the BWP Multiplexer (Algorithm 4): among numerology 2 / 1 / 0, activating numerology 2 if `µ_LC = 2` and `sched_LC > 0` and `α_UE < α_max1`, else numerology 1 if `µ_LC = 1` and `sched_LC > 0` and `α_UE < α_max2`, else numerology 0 if `sched_LC > 0`. *"α_max1 and α_max2 are thresholds to avoid starvation of eMBB traffic."*
  - **PRB pre-allocation per LC** — `prealloc_res_LC = min(R, N)` for eMBB (R = PRBs for `α_UE * req_LC`, N = PRBs for `queue_size_LC`); for uRLLC, PRBs for the bytes of PDUs with `remaining_time(pdu_j) <= 2 TTI_µ`.
  - **Final PRB allocation per LC in the slot** — performed by the MAC Scheduler: *"it allocates PRBs for each UE based on how many PRBs it needs and how many are available for each slice."*

- **G. Objective function (quote exact reward/cost):**
  **No reward function (not RL).** The stated objective is QoS enforcement with resource minimisation — e.g. *"we minimize the number of PRBs allocated for eMBB slices while respecting their throughput requirements"*, and *"NRflex (algorithm 3) considers PDUs' deadline to allocate only the needed PRBs to schedule PDUs that will exceed their deadline shortly."* The BWP manager's control law is a simple additive-increase rule (Algorithm 1): if `throughput_success_rate_j < 1` then `NewPRB_j = consumedPRB_j + 2`; if `deadline_failure_rate_i > 0` then `NewPRB_i = consumedPRB_i + 2`.

- **H. Constraints:**
  - **One numerology per UE per slot:** *"a UE can use only one numerology at a given time (for example, a UE belonging to both an uRLLC slice and an eMBB slice can not use both of them at the same slot)"* — a 5G NR physical-layer constraint; the paper also states this in slot granularity: *"UEs cannot serve two slices at the same time (i.e. same slot in ms granularity) when the slices use different numerology (5G NR physical layer constraint)."*
  - **PRB budget per numerology:** the number of PRBs per numerology is bounded by the system bandwidth (their Table 1: numerology 0 → 20 MHz/106 PRBs; numerology 1 → 40 MHz/106 PRBs; numerology 2 → 80 MHz/107 PRBs).
  - **Deadline constraints:** uRLLC PDUs must respect slice max latency (urllc1 = 5 ms, urllc2 = 1 ms).
  - **Throughput constraints:** eMBB slices have a desired throughput per UE (embb1 = 0.9 Mbps, embb2 = 1.5 Mbps).
  - **Anti-starvation constraints:** thresholds `α_max1`, `α_max2` bound how many consecutive slots uRLLC numerology can be preferred, *"to avoid starvation of eMBB traffic."*

- **I. Scheduling algorithm + optimization method:**
  **Rule-based / algorithmic framework, not an optimisation or learning method.** Four algorithms: **Algorithm 1 (BWP manager)** — additive-increase BWP resize per slice from KPIs and consumed PRBs; **Algorithm 2 (eMBB pre-processor)** — sort LCs by weight `α_UE`, compute `R = bytes_to_RBs(CQI_UE, α_UE * req_LC)` and `N = bytes_to_RBs(CQI_UE, queue_size_LC)`, set `prealloc_res_LC = min(R, N)`; **Algorithm 3 (uRLLC pre-processor)** — sort LCs by remaining time of the first PDU, accumulate the sizes of PDUs with `remaining_time(pdu_j) <= 2 TTI_µ`, convert to PRBs; **Algorithm 4 (BWP multiplexer)** — per-UE numerology (BWP) activation with uRLLC prioritisation and eMBB anti-starvation thresholds. The run-time slice lifecycle NRflex defines is: **Pre-processing → Multiplexing → Allocation → Monitoring → Pre-adaptation**, *"executed in an infinite loop until the slice deletion."*

- **J. ML/DRL used? yes/no and which:**
  **No.** No machine learning or reinforcement learning is used anywhere in NRflex; the framework is deterministic/rule-based. (The paper does use ML/DRL only in its *related-work* discussion of other slicing approaches.)

- **K. Simulator / testbed / dataset (exact names + versions):**
  - **Simulation only — no testbed.** Verbatim: *"we used a reliable 5G simulator based on Matlab that supports different numerology (table 1) and BWPs with dynamic scheduling. Note that this simulator is an improved version of the one used in [3]; it includes 5G NR features. We validated the simulator using the 3GPP 5G NR simulator [1]. Both of them gave the same throughput with different configurations (Bandwidth, numerology, etc.)."*
    - Reference **[3]** = Bakri, S., Frangoudis, P., Ksentini, A., 2019, *"Dynamic slicing of RAN resources for heterogeneous coexisting 5G services"*, GLOBECOM 2019 — i.e. the MATLAB simulator is an in-house, extended version of the GLOBECOM 2019 simulator. **The simulator has no product name/version.**
    - Reference **[1]** = *"3GPP 5G tools, 2021. 5g nr throughput calculator. https://5g-tools.com/5g-nr-throughput-calculator/"* — i.e. validation was against the **3GPP 5G NR throughput calculator**, not a full 3GPP simulator.
  - **Real deployment:** none. Future work only: *"we intend to implement NRflex in OpenAirInterface (OAI) 5G [15] to test it in the real deployment."*
  - **Dataset: NOT REPORTED** (traffic is generated by the simulator parameters in their Table 3).
  - **Reproducibility:** *"we have run the simulation for 100 iterations. Each value presented in the figures represents the average."*

- **L. Traffic model:**
  Per-slice synthetic traffic defined by inter-arrival time and packet size (their Table 3), quoted verbatim:
  | Slice | Inter-arrival time | Packet size |
  |---|---|---|
  | urllc1 | 4 ms | 800 Bytes |
  | urllc2 | 2 ms | 400 Bytes |
  | embb1 | 70 ms | 4596 Bytes |
  | embb2 | 70 ms | 6516 Bytes |
  Characterisation: *"uRLLC slice traffic is characterized by small data chunks with high frequency, while data chunks' sizes are big with low frequency sending for eMBB slice traffic."* For the uRLLC load sweep, a five-point load table is used (their Table 4): index 1 = 5 ms / 200 Bytes, 2 = 4 ms / 280 Bytes, 3 = 3 ms / 360 Bytes, 4 = 2 ms / 440 Bytes, 5 = 1 ms / 520 Bytes. Channel: *"a random CQI which takes values in [12-15] interval for each UE, indicating a medium to a good channel condition."*

- **M. Network scale:**
  **One gNB region / one cell** (the framework is described for multi-gNB but evaluated in a single simulated cell). **Four slices** with the requirements of their Table 2: `embb1` desired throughput 0.9 Mbps per UE; `embb2` 1.5 Mbps per UE; `urllc1` max latency 5 ms; `urllc2` max latency 1 ms. **UEs:** *"At t=0s, the system includes 10 UEs among them 5 UEs are connected to each slice tuple ((urllc1,urllc2,embb1), (urllc1,urllc2,embb2)). At t=5s and t=11s, 2 more UEs connect to each slice tuple; i.e., at t=6s, the system includes 14 UEs, and at t=12s, 18 UEs."* Each UE is associated with **two slices**. Scenario 2 sweeps **up to 60 UEs**. System bandwidths per numerology: 20/40/80 MHz (106/106/107 PRBs). Slot duration = 2^−n ms for numerology n.

- **N. Baselines (exact names):**
  - For **eMBB slices**: *"the one introduced in [3] (called **standard solution for eMBB slices** in the rest of the paper), which shares the same idea with other eMBB resource allocation algorithms (as [7; 6]); i.e., they use the slice throughput constraint to compute the required amount of PRBs."* (ref [3] = Bakri/Frangoudis/Ksentini, GLOBECOM 2019; ref [6] = Foukas et al., **Orion**, MobiCom 2017; ref [7] = Foukas et al., **FlexRAN**, CoNEXT 2016.)
  - For **uRLLC slices**: *"the **Fair Proportional Scheduling** algorithm combined with a resource allocation strategy that allocates the amount of PRBs needed to schedule all uRLLC traffic first (called **standard solution for uRLLC slices** in the rest of the paper)."*

- **O. Metrics:**
  `deadline_failure_rate` (uRLLC; lower better, target 0), `throughput_success_rate` / slice throughput in Kbps (eMBB), **PRB allocation / "Bandwidth usage ratio"** per slice, **numerology selection rate**, and **number of UEs sustainable at a given failure rate**. Overhead is discussed qualitatively (message count × message size between RIC and gNBs each 1 s interval).

- **P. Main quantitative results (EXACT numbers with the comparison, quoted):**
  - **Scenario 1 (UEs growing 10 → 18 over time):** *"For the first slice, which requires a latency of 5 ms, NRflex ensures a lower deadline_failure_rate (Figure 6a) than the standard solution. Moreover, NRflex adapts itself quickly to the new cell load by adding more PRBs to the slice. We also observe that NRflex meets the slices' required latency deadline with a smaller number of PRBs (Figure 6b). For the second slice, which requires a latency of 1 ms, we remark that, at t=17s (Figure 6b), the standard solution can not reduce the deadline_failure_rate (Figure 6a) as it consumed all the bandwidth dedicated for numerology 2 (table 1). In comparison, **NRflex is able to reduce the deadline_failure_rate to zero after 5s of adaptation with the same bandwidth size.**"*
  - **eMBB:** *"We remark that both approaches achieve the same throughput, which is different from the desired throughput… In figure 7b, we see that NRflex consumes lesser PRBs to meet the same throughput, compared to the standard solution. As the number of UEs increases, the difference between the two approaches increases in terms of used PRBs."*
  - **Scenario 2, medium uRLLC traffic load:** *"NRflex can handle up to **50 UEs in numerology 2** and up to **60 UEs in numerology 1** with a deadline_failure_rate=0 (no packet is lost due to deadline exceeded). In contrast, the standard solution can handle up to **25 UEs in numerology 2** and **40 UEs in numerology 1** before the deadline_failure_rate increases."*
  - **Scenario 2, high uRLLC traffic load:** *"NRflex can handle up to **50 UEs that require a 5 ms latency** and **20 UEs that require a 1ms latency**, while the other approach can handle only **20 UEs** and **10 UEs**, respectively. At the same time, NRflex ensures that the eMBB throughput is respected for both medium and high uRLLC traffic loads."*
  - **Scenario 3 (uRLLC load sweep, their Table 4 indices):** *"from index = 3 (see table 4), uRLLC traffic starts impacting eMBB traffic. However, the results show that even with the higher loads, eMBB slices are still getting served (eMBB numerology is selected)."*
  - **Overhead:** *"Each 1s interval, gNB sends a message containing a list of slices with the average of used PRBs and calculated KPIs … and receives a message containing a list of slices with their new BWP configuration. However, these messages' impact is very low in terms of needed bandwidth, as their size is very small."*

- **Q. Main limitation:**
  **Simulation-only, in a nameless MATLAB simulator**, validated only against an online **throughput calculator**, with **no real testbed** (OAI implementation is left as future work). A single cell/gNB is evaluated (multi-gNB slice management is described but not measured). **No core-network/end-to-end slice evaluation** (explicitly out of scope). **No machine learning** — the control laws are fixed additive-increase rules with hard-coded thresholds (`+2` PRBs, `α_max1`, `α_max2`) whose tuning is not analysed. Traffic is synthetic and stationary per slice (fixed inter-arrival/packet size), and results are reported as averages of 100 iterations with **no confidence intervals** (*"We did not include the minimum and maximum values as they are as very close to the average"*).

- **R. Research gap this suggests:**
  (i) There is **no learning-based or predictive slice/BWP controller** here — replacing the fixed `+2 PRB` additive-increase rule and the static `α_max` thresholds with a DRL/learning controller is an obvious open problem (and is exactly what the DRL slicing literature attempts). (ii) **RAN-only**: no interaction with the 5G Core, PDU sessions, QoS flows or UPF, so end-to-end slice QoS (RAN + core + transport) is unaddressed — bridging directly to Paper 3. (iii) The framework is **validated only in simulation with an unnamed simulator**; a reproducible open-source implementation (OAI/ns-3/SimuRAN) and a real testbed remain open. (iv) **No multi-cell/multi-gNB evaluation** despite the architecture claiming multi-gNB slice management. (v) No treatment of **inter-slice PRB fairness or isolation guarantees** beyond anti-starvation thresholds, and no formal optimality/feasibility analysis of the PRB pre-allocation.

- **S. Best URL actually retrieved + whether read FULL TEXT or ONLY ABSTRACT:**
  `https://www.eurecom.fr/publication/6720/download/comsys-publi-6720.pdf` — downloaded with `curl` and converted with `pdftotext -layout` (1,130 lines). **FULL TEXT READ** (accepted manuscript). Local artefacts: `pdfs/nrflex_comcom2022.pdf`, `pdfs/nrflex_comcom2022.txt`. A mirror of the same work is indexed at `https://5gdrones.eu/wp-content/uploads/2021/10/Enforcing-Network-Slicing-in-5G-New-Radio.pdf` and the publisher landing page is `https://doi.org/10.1016/j.comcom.2021.09.034`.

---

### Paper 2 — CLOSEST VERIFIED MATCH B (thematically closest MAC-scheduling + slicing paper; **NOT open access — abstract-level only**)

### Satisfying Network Slicing Constraints via 5G MAC Scheduling

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Silvio Mandelli, Matthew Andrews, Sem Borst, Siegfried Klein (Nokia Bell Labs).
  **2019** (April 2019). **Venue: IEEE INFOCOM 2019 – IEEE Conference on Computer Communications, pp. 2332–2340.** **Peer-reviewed conference paper.**
  **DOI: 10.1109/INFOCOM.2019.8737604** (verified via Crossref: `container-title = "IEEE INFOCOM 2019 - IEEE Conference on Computer Communications"`, `page = 2332-2340`, `issued = 2019-04`, `publisher = IEEE`, `type = proceedings-article`; authors confirmed as Silvio Mandelli, Matthew Andrews, Sem Borst, Siegfried Klein).
  **Unpaywall reports `is_oa: False` with zero OA locations** — no legal open-access full text was found (no arXiv version; ResearchGate and Semantic Scholar hosts are paywalled/restricted). **Therefore only abstract-level information is reported here, and I explicitly did NOT read the full text.**

- **A. Exact problem solved (from the abstract only):**
  *"Network slicing provides a key functionality in emerging 5G networks, and offers flexibility in creating customized virtual networks and supporting diversified services over a common physical infrastructure."* The paper addresses **inter-slice radio resource allocation (IS-RRA) implemented inside the 5G MAC scheduler.**
- **B. Network architecture:** **NOT REPORTED at a level I can verify** (full text not retrieved; only abstract-level claims available).
- **C. Network layer/domain (from search-result metadata and abstract):** **5G MAC layer / RAN**, specifically *"Inter-slice radio resource allocation (IS-RRA) is a new layer of radio resource management introduced by network slicing in 5G."*
- **D. Network entities involved:** **NOT REPORTED** (abstract only).
- **E–H. Input/state, decision variables, objective, constraints:** **NOT REPORTED** (full text not retrieved). The abstract-level description indicates the mechanism uses **token counters** and **smoothed/instantaneous slice rates** (inferred solely from indexed figure captions: *"Evolution in time of instantaneous and smoothed rates and token counters for two particular cell slices"* and *"Throughput CDF of SM users for an aggregate rate target of 4 Mbps per slice"*) — these are quoted from retrieved index metadata, not from the paper body.
- **I. Scheduling algorithm + optimization method:** **NOT REPORTED** (full text not retrieved).
- **J. ML/DRL used?:** **NOT REPORTED** — nothing in the retrieved metadata indicates machine learning; the work appears to be a scheduling-mechanism design (token-bucket/rate-based), but I cannot verify this from the full text.
- **K. Simulator / testbed / dataset:** **NOT REPORTED** (full text not retrieved).
- **L. Traffic model:** **NOT REPORTED** (full text not retrieved).
- **M. Network scale:** **NOT REPORTED**; the only retrievable number is an *"aggregate rate target of 4 Mbps per slice"* from a figure caption.
- **N. Baselines:** **NOT REPORTED.**
- **O. Metrics:** **NOT REPORTED**; figure captions reference throughput CDFs and slice rates.
- **P. Main quantitative results:** **NOT REPORTED** (no full text; no numbers verifiable).
- **Q. Main limitation:** Cannot be assessed without the full text. Externally visible limitation: **the paper is paywalled and has no open-access version**, which is itself a practical limitation for a literature review.
- **R. Research gap this suggests:** Given that this is the canonical *"network slicing constraints enforced by the 5G MAC scheduler"* paper and it is **closed access with no open artifact**, there is a clear gap for an **open, reproducible, learning-based inter-slice MAC scheduler** that (a) enforces per-slice rate/latency constraints with published code, (b) is validated on a named open simulator, and (c) couples the RAN slice scheduler to the 5G Core/QoS-flow layer.
- **S. Best URL actually retrieved + whether read FULL TEXT or ONLY ABSTRACT:**
  Metadata and abstract obtained from Crossref (`https://api.crossref.org/works/10.1109/INFOCOM.2019.8737604`), Unpaywall (which confirms **no OA copy exists**), and the publisher landing page `https://ieeexplore.ieee.org/document/8737604` (abstract only; the PDF is paywalled and IEEE blocks automated retrieval). **ONLY ABSTRACT/METADATA READ — NOT the full text.** Per the rigor rules, no technical fields have been invented to fill the gaps; everything unobtainable is marked NOT REPORTED.

---

## Paper 3

### Power Consumption-Aware 5G Edge UPF Selection using Deep Reinforcement Learning

**Why this paper was selected:** it is a 2024 peer-reviewed IEEE conference paper whose *central contribution* is a **DRL policy for the UPF selection procedure at PDU-session establishment in a 5G Core deployment** — i.e. it matches the requested "5G QoS Flow / PDU session scheduling in the 5G Core or UPF … UPF selection … DRL-based 5G core user-plane scheduling" brief directly, it uses **5QI/QoS** requirements, and an **open-access full text** is retrievable from the authors' institutional repository. Verification of existence: Crossref returns the record below; IEEE Xplore document 10807472 exists; an author copy is hosted at the University of Trento IRIS repository.

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Arturo Bellin, Nicola Di Cicco, Daniele Munaretto, Fabrizio Granelli.
  **2024** (published 5 November 2024). **Venue: 2024 IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN), pp. 1–6.** **Peer-reviewed IEEE conference paper.**
  **DOI: 10.1109/NFV-SDN61811.2024.10807472** (verified via Crossref: `title = "Power Consumption-Aware 5G Edge UPF Selection using Deep Reinforcement Learning"`, `container-title = "2024 IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN)"`, `page = 1-6`, `issued = 2024-11-05`, `publisher = IEEE`, `type = proceedings-article`).
  Affiliations: Department of Information Engineering and Computer Science (DISI), University of Trento, Italy; Research and Innovation Department, Athonet (an HPE acquisition), Bolzano Vicentino, Italy; Department of Electronics, Information, and Bioengineering (DEIB), Politecnico di Milano, Italy. Funding: Horizon Europe GA 101096342 (HORSE), GA 101096925 (6Green), and the Italian NRRP "RESTART" partnership (PE00000001).
  **Version read:** the author accepted manuscript PDF hosted by the University of Trento IRIS repository (`iris.unitn.it`). **This is not the publisher's typeset version**; section/figure numbering may differ.

- **A. Exact problem solved:**
  **UPF selection (user-plane function placement/allocation) in an edge–cloud 5G Core network at PDU-session establishment**, minimising system power consumption subject to latency/QoS requirements. Verbatim: *"we propose a Deep Reinforcement Learning (DRL) algorithm for the orchestration of an edge-cloud 5G core network deployment with multiple distributed User Plane Function (UPF) instances. More specifically, our DRL agent provides a policy for the UPF selection procedure when a new connection from a user to the data network is established. The choice of UPF is based on the real-time power consumption metrics gathered from the edge and cloud hosts in addition to the latency and bandwidth requirements of the users."* Objective restated: *"The overall objective is to minimize the system power consumption while satisfying the desired quality of service."*
  **Scheduling/placement is the central contribution** — the DRL agent *is* the UPF selector/orchestrator; the paper formulates *"the PDU session allocation problem."*

- **B. Network architecture:**
  A **5G Core (5GC) deployment split between edge hosts and a single cloud host**. Verbatim: *"The edge-cloud environment is modeled as a set E of edge hosts and a single cloud host. Each host node is a different location capable of running one or more instances of a 5G UPF and is characterized by a power consumption model, CPU usage model, maximum available bandwidth, and offered latency. In addition, an edge host can be in an on or off state and switch freely between the two. The cloud host is characterized by a power consumption coefficient, a CPU usage coefficient, and offered latency. Contrary to the edge hosts, it does not have a maximum bandwidth since, for the scale of our experiment, we consider the cloud to be infinitely scalable… we model the cloud power consumption and CPU usage as a simple linear function of the provided throughput."* Users are modelled **per PDU session**; *"The PDU sessions are characterized by the following elements: start time, total duration, required bandwidth, and 5QI value which maps to a required latency budget and priority level."* Standardisation hooks: *"it is compatible with standardized UPF selection procedures and 5G QoS Indicators (5QIs)"*; the 5G procedures reference is 3GPP **TS 23.502 version 18.5.0 (2024)**.

- **C. Network layer/domain:**
  **5G Core network / user plane (UPF), NFV/MANO orchestration, edge–cloud infrastructure.** Not a RAN/MAC paper. (It is the core-side counterpart to Papers 1–2.)

- **D. Network entities involved:**
  **Edge hosts (set E)** each able to run one or more **UPF** instances, in **on/off** states; **one cloud host** (infinitely scalable, no bandwidth cap); **UPF instances**; **PDU sessions** (the arriving "jobs", characterised by start time, duration, required bandwidth and **5QI**); the **DRL agent / orchestrator**; **power meters** (*"hardware or software-based power meters"* on hosts); a **Gymnasium-based simulated environment**; a **network digital twin** concept for training; the **5G Core** deployment underlying the power models (virtual machines, containers, bare metal).

- **E. Input/state parameters (exact observation vector if reported):**
  Verbatim: *"The state space has dimension (|E| + 1) × (h + r + 1), where h is the number of metrics observed on hosts in the environment and r is the number of features of the incoming PDU session."*
  - **From each edge node:** *"current throughput, maximum throughput available at the host, current host power consumption, and latency."*
  - **From the cloud node:** *"the current throughput, host power consumption and latency."*
  - **PDU session request metrics:** *"the QoS Identifier and desired throughput."*
  - **Plus:** *"∆t, the time interval elapsed from the previous request, is also included in the observations to capture the time-dependent dynamics of the system."*
  - *"Finally, the observation space is normalized using a moving average."*
  - **Explicit non-observation:** *"the PDU session request provides no information about its duration, as we assume that it is generally not known in advance by the UE. This is a disadvantage for the DRL agent…"*

- **F. Decision variables (exact action space if reported):**
  *"We use a discrete action space of size |E|+1 in which the selected action represents the host selected to serve the current PDU session request between the E edge hosts and the cloud host. By using the Maskable PPO algorithm, we can dynamically remove from the action space the actions corresponding to the hosts that are full and not capable of accepting any other PDU sessions. Action 0, which corresponds to the cloud host, will always be available since we consider the cloud to be infinitely scalable and, therefore, always able to accept new traffic."*

- **G. Objective function (quote exact reward/cost):**
  Verbatim reward (their Eq. 1):
  `R = 1 − k × ((Σ_{e∈E} P_e + P_c) / (Σ_{e∈E} T_e + T_c))` **when `l_h ≤ l_r`** (the latency offered by the selected host `l_h` is lower or equal to the latency required by the current session `l_r`); and `R = −1` **otherwise**.
  Explanation quoted: *"the first case is selected when the latency requirements are met… In this case, the reward has a positive value lower than 1 and decreases with the power consumed by the system per unit of traffic. This decreasing behavior is controlled by the factor k that is specific to the environment and the desired trade-off level between energy efficiency and latency errors. In the event that the required latency is not satisfied, the reward is set to a constant value of −1."* **k is set to 10** (*"we experimentally found it to be good for the dimensions of the environment"*). MDP tuple: `⟨S, A, P, R, γ⟩`.

- **H. Constraints:**
  - **Latency constraint (soft, penalised):** the selected host must offer latency `l_h ≤ l_r` where `l_r` derives from the PDU session's **5QI**; violations are penalised with reward −1 but are *not* structurally forbidden — the authors state explicitly: *"Note that our approach cannot guarantee any level of latency error rate, even though a different trade-off with energy efficiency can be achieved by tuning the reward function."*
  - **Host capacity constraint:** *"By using the Maskable PPO algorithm, we can dynamically remove from the action space the actions corresponding to the hosts that are full and not capable of accepting any other PDU sessions."*
  - **Bandwidth/throughput constraint:** each edge host has a *"maximum available bandwidth"*; each PDU session has a *"required bandwidth"* and a *"desired throughput"*.
  - **Cloud unconstrained assumption:** the cloud is treated as infinitely scalable with no bandwidth cap — an explicit modelling assumption, not a physical constraint.
  - **No formal optimisation constraints (maximise/minimise subject to…):** the paper notes the problem is NP-hard (*"The problem of finding the optimal distribution of VNFs in a data center network to minimize energy consumption has been shown to be NP-hard [10]. Also, the general task scheduling problem on more than one server is NP-hard [11]. It is, therefore, reasonable to assume that our formulation of the PDU session allocation problem is also similarly complex."*) and consequently solves it with RL rather than constrained optimisation.

- **I. Scheduling algorithm + optimization method:**
  **Maskable Proximal Policy Optimization (Maskable PPO)** — a policy-gradient DRL method with action masking to enforce host-capacity feasibility. Training: **PPO trained for a total of 6M steps with 1000 steps per episode**; the value of k = 10. The agent selects a host for **each incoming PDU session request**; the paper compares **two copies of the same PPO algorithm** — one observing/optimising **power consumption**, the other substituting **CPU utilisation** in both observations and reward.

- **J. ML/DRL used? yes/no and which:**
  **Yes — Deep Reinforcement Learning: Proximal Policy Optimization (PPO), specifically the Maskable PPO variant** from **Stable-Baselines3**. The paper frames the problem as an MDP and notes that *"Model-free DRL algorithms, such as Deep Q-Networks and PPO, do not require knowledge of the transition probability matrix."* A second PPO agent using CPU-utilisation observations/reward is trained as an ablation.

- **K. Simulator / testbed / dataset (exact names + versions):**
  - **Simulation for training and testing, with models empirically derived from a real testbed.** Verbatim: *"For the evaluation of our methodology, we decided to implement a simulated environment using the framework provided by the **Gymnasium** library [12] and the **Stable-Baselines3** algorithms [13]."* And: *"both training and testing environments are simulated using power consumption and CPU models empirically derived from a real-world small-scale testbed described in our previous study [1]. Each experimental model describes the power consumption and CPU usage of a specific host based on the traffic load as a percentage of the maximum throughput available at that host. The power consumption is measured with a **smartplug** connected to the hardware hosting the 5GC, therefore it shows the aggregate power consumption of the system."*
    - **[1] = A. Bellin, F. Granelli, D. Munaretto, "A measurement-based approach to analyze the power consumption of the softwarized 5G core," *Computer Networks*, vol. 244, p. 110312, 2024.**
    - The **measured testbed power/CPU models** (their Table I, "EXPERIMENTAL POWER MODELS") are reported verbatim for three virtualisation options — **virtual machine**: Power [W] 9.47, 10.67, 12.44, 14.77, 17.88, 20.99, 24.05, 27.03, 28.72, 29.83, 30.47 and CPU [%] 5.3, 27.2, 38.8, 42.4, 43.2, 52.3, 62.4, 67.0, 70.9, 74.3, 77.2; **bare metal**: Power [W] 8.20, 8.94, 9.71, 10.49, 11.47, 13.08, 14.18, 15.24, 16.18, 16.92, 17.33 and CPU [%] 0, 8.5, 11.5, 12.3, 12.4, 13.1, 12.2, 14.4, 16.1, 16.6, 17.7; **containers**: Power [W] 7.90, 9.62, 10.92, 12.40, 14.21, 16.06, 17.83, 19.10, 20.08, 20.88, 21.55 and CPU [%] 1.0, 10.5, 13.4, 14.3, 14.9, 14.0, 16.7, 18.2, 20.7, 24.1, 26.1 (traffic load 0%→100% in 10% steps).
  - **No live 5GC testbed was used for the DRL evaluation** — *"For the scope of this study, both training and testing environments are simulated."* Real-world testbed data enters only through the power/CPU models.
  - **Dataset:** **NOT REPORTED** as a named public dataset; traffic is generated by the simulator (see L).

- **L. Traffic model:**
  Verbatim: *"The simulated traffic in the environment is composed of a series of PDU session establishment requests with **exponentially distributed inter-arrival times**, **continuous uniform distributed throughput between values of 10 Mbps and 100 Mbps**, and **normally distributed duration with an average of 40 s and standard deviation of 5 s**."* On 5QI selection: *"Between all 5QIs specified by the standard, we selected three of them to represent a diverse spectrum of requests, namely: **V2X messages (value 3), IMS Signalling (value 5), and Video Buffered Streaming TCP-based (value 9)**. The distribution of the 5QIs in this evaluation are: **30% value 3, 40% value 5, and 30% value 9**."* Two load regimes are tested: *"a low-medium traffic scenario (**inter-arrival time of 1.5**)"* and *"a high traffic scenario (**inter-arrival time of 0.8**)".* A generalisation test uses *"a different distribution of 5QI levels compared to the one used during training."*

- **M. Network scale:**
  An **edge–cloud 5GC with multiple distributed UPF instances**; the numbered host discussion implies hosts **0, 1, 2, 3** (*"host 2, which is the most energy-efficient"*, *"sessions with 5QI of 9 are mostly assigned to host 0 (the cloud)"*, *"host 1 is never selected in this scenario, while host 3 is selected only occasionally"*) — i.e. **|E| + 1 = 4 hosts** in the main scenario (3 edge hosts + 1 cloud). The ablation uses *"a simple simulated environment with only **two edge hosts**."* Figure 5 is described as reporting allocation choices *"from a total of **1000 requests**."* **Number of PDU sessions, number of UEs, number of gNBs, and geographic scale: NOT REPORTED.**

- **N. Baselines (exact names):**
  Four heuristics, quoted verbatim:
  - **Random action** — *"a random host is selected between all the available with equal probability, regardless of the current power consumption metrics and latency requirements."*
  - **Energy greedy** — *"always select the cloud host as in our simulated environment, it is always the one with the lowest power consumption per unit of traffic."*
  - **Latency greedy** — *"select among the available hosts the one with the lowest offered latency."*
  - **Latency smart** — *"select among the available hosts that satisfy the latency requirements the one with the highest latency. If there are no hosts that can satisfy the latency requirement select the one with the lowest latency."*
  Plus an internal ablation baseline: **the same PPO agent using CPU-utilisation instead of power consumption** in observations and reward.

- **O. Metrics:**
  **Latency error probability (latency requirement violation rate)**, **power consumption per Mbit (W/Mbit)**, **episode reward**, **total power consumption**, and allocation-choice distributions per 5QI/host. Also discussed: behaviour under heterogeneous hardware.

- **P. Main quantitative results (EXACT numbers with the comparison, quoted):**
  - **Energy greedy:** *"the energy greedy policy has the best power consumption, equal to the one offered by the cloud host (**0.01 W/Mbit** in our evaluation scenario), but fails to meet the latency requirements most of the time."*
  - **Low–medium traffic:** *"both versions of the DRL algorithm manage to allocate the incoming sessions without incurring any violation of the latency requirements, same as the latency greedy and latency smart algorithms but with significantly lower power consumption."*
  - **High traffic (the headline result):** *"the DRL algorithm presents around **1% latency error rate** compared to the **14.3%** of the standard latency greedy and **0%** of the latency smart algorithm. This scenario highlights the strength of our DRL orchestrator, which is to sacrifice only a percentage point of the latency error rate to get a big return in terms of energy efficiency (**20% less energy used compared to the latency smart heuristic**)."*
  - **Policy interpretation:** *"the sessions with more stringent 5QIs values (3 and 5) are always assigned to edge hosts and, in particular, to host 2, which is the most energy-efficient. Conversely, PDU sessions with 5QI of 9 are mostly assigned to host 0 (the cloud) since they allow for a higher latency. The few sessions of this type assigned to node 2 represent a suboptimal choice of our algorithm that can probably be corrected with a better tuning of the training hyperparameters."*
  - **Generalisation:** *"We also tested the policy using a different distribution of 5QI levels compared to the one used during training and confirmed that our approach can correctly behave even when the traffic levels and latency requirements are somewhat different compared to the one experienced during training."*
  - **Power-vs-CPU ablation (negative result, reported honestly):** *"When comparing the two versions of the PPO algorithm, the one using the power consumption data and the other using the CPU metrics, we do not see any significant variation. This is a limitation of the considered environment since the power models used are gathered from our experimental testbed which uses identical hardware for all hosts."* In the specially constructed **two-host heterogeneous** environment (second host with *"a power consumption that is 5W higher"*), *"The distinction in this case is much clearer"* — motivating power-based over CPU-based orchestration.

- **Q. Main limitation:**
  **Fully simulated evaluation** — *"For the scope of this study, both training and testing environments are simulated"* — with the real testbed contributing only empirical power/CPU models from **identical hardware**, which the authors themselves identify as the reason the power-vs-CPU comparison shows no benefit: *"This is a limitation of the considered environment since the power models used are gathered from our experimental testbed which uses identical hardware for all hosts."* The approach **cannot guarantee any latency-error level** (*"our approach cannot guarantee any level of latency error rate"*). Retraining is required for environmental change: *"bigger environment changes, such as the addition of a new edge host or a complete change in traffic characteristics, will require the retraining of the DRL model."* The cloud is assumed **infinitely scalable with no bandwidth cap**, which removes a key constraint from the problem. Only **three 5QI values** are used and **priority levels are not exploited** (*"We also want to evaluate the algorithm using more 5QI values and include their priority level in the reward function"* — future work). **Only 4 hosts and 1000 requests** in the main scenario; no number of UEs/PDU sessions/geographic scale is given.

- **R. Research gap this suggests:**
  (i) **Real-deployment validation is missing:** the authors' own next step is *"testing the orchestrator in a real-world deployment with a more complex architecture and a wider selection of hardware."* A PhD contribution could be a **live 5GC (e.g. Open5GS/free5GC + real UPFs) with heterogeneous hosts**, closing the sim-to-real gap. (ii) **Heterogeneous hardware and renewable energy awareness** — *"It allows the integration and modeling of renewable energy sources. This aspect is not explored in our work"* — an explicit open problem (carbon-aware UPF selection). (iii) **Only 5QI → latency mapping is used; 5QI priority, GBR/non-GBR and QoS-flow-level (not just PDU-session-level) granularity are unexploited** — i.e. **QoS-flow-level scheduling inside/between UPFs is not addressed**. (iv) **No guarantee mechanism**: the latency constraint is only softly penalised; a safe/constrained-RL formulation with hard SLA guarantees is open. (v) **No coupling with the RAN slice scheduler** (Papers 1–2) — end-to-end, cross-domain (RAN + core) slice/QoS orchestration remains unaddressed. (vi) **No PDU-session-duration observability**: the agent is disadvantaged by not knowing session duration, which a predictive/forecasting extension could address.

- **S. Best URL actually retrieved + whether read FULL TEXT or ONLY ABSTRACT:**
  `https://iris.unitn.it/retrieve/7af18493-ee88-44c0-bbc6-ed38e29e4891/Bellin_Power-Consumption-Aware_2024.pdf` (University of Trento IRIS open-access author copy; plain `curl` returns HTTP 403, retrieved via the `r.jina.ai` text proxy). **FULL TEXT READ** (6 pages). Local artefact: `pdfs/upf_nfvsdn2024_fulltext.txt`. Publisher landing page: `https://ieeexplore.ieee.org/abstract/document/10807472`.

---

## Paper 3 (secondary / alternative candidate, also verified and fully extracted)

### User Plane Function (UPF) Allocation for C-V2X Network Using Deep Reinforcement Learning

**Why included:** this is an alternative 2025 peer-reviewed, fully open-access (CC-BY, DOAJ-indexed) answer to the same brief from Paper 3. It differs from the primary pick in that its UPF decision is a **placement/allocation decision per time slot** (not per PDU-session establishment) and its QoS driver is **latency for vehicular users** rather than 5QI-driven PDU sessions. Reported separately so the parent agent can choose.

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Pruk Sasithong, Tachporn Sanguanpuak, Pisit Vanichchanunt, Lunchakorn Wuttisittikulkij.
  **2025** (received 21 November 2024; accepted 30 December 2024; date of publication 31 December 2024; date of current version 8 January 2025; journal issue **IEEE Access, Volume 13, 2025**, **pages 4547–4561**).
  **Venue: IEEE Access.** **Peer-reviewed journal; open access, CC-BY 4.0** (*"2024 The Authors. This work is licensed under a Creative Commons Attribution 4.0 License."*). Indexed in **DOAJ** (DOAJ record confirms title, journal "IEEE Access" vol. 13, year 2025, and full-text link to IEEE Xplore).
  **DOI: 10.1109/ACCESS.2024.3524886** (verified via Crossref: `container-title = "IEEE Access"`, `volume = 13`, `page = 4547-4561`, `issued = 2025`, `type = journal-article`; Semantic Scholar returns `venue: "IEEE Access", year: 2025, openAccessPdf: {status: "GOLD", license: "CCBY"}`, DBLP key `journals/access/SasithongSVW25`). Unpaywall: `is_oa: True`, publisher PDF CC-BY, published version.
  Affiliations: Chulalongkorn University, Bangkok; **Nokia, Oulu, Finland**; King Mongkut's University of Technology North Bangkok.

- **A. Exact problem solved:**
  **Dynamic UPF placement/allocation in a MEC-integrated C-V2X (cellular vehicle-to-everything) 5G network**, driven by real-time vehicle positions and speeds, to minimise communication latency. Verbatim: *"we proposed an online learning method for predicting an allocation of User Plane Function (UPF) in Cellular Vehicle-to-Everything (C-V2X) networks integrated with Multi-Access Edge Computing (MEC). Our study employed Deep Reinforcement Learning (DRL) techniques, specifically Deep Q-Network (DQN) and Actor-Critic (AC) algorithms. The DQN and AC algorithms were implemented to decide the optimal location of UPFs subject to vehicle positions and speed data of the vehicles. Our objective was to reduce the latency of communications between UPF and vehicles by placing the UPF(s) in optimal way."*
  **UPF allocation is the central contribution.** The paper positions itself as *"the first study to apply DRL techniques for dynamic UPF allocation in C-V2X networks"* with a **multi-actor** extension for multiple UPFs.

- **B. Network architecture:**
  **5G Core user plane with MEC integration.** *"UPF instances have the potential to be established on distributed MEC hosts, enabling efficient traffic routing to MEC applications."* Control chain: *"the data traffic of every user is directed to the UPFs, whose location is determined by the **SDN controller**. The UPF allocation algorithm is responsible for making decisions regarding the locations of UPFs. The decision is transmitted to the **NFV Management and Orchestration (MANO)** platform of the operator, leading the instantiating of the UPFs at the designated MEC host. Subsequently the SDN controller receives a notification to reconfigure the network and redirect the traffic of each user equipment (UE) to the UPF."* Network modelled as a **weighted graph `G = (N, L)`** where nodes are **base stations co-located with MEC** and link weights are propagation delays (*"the distance between the nodes divided by the approximated speed of light in an optical fiber, which is 2 × 10^8 m/s"*). UE–BS association is by **minimum path loss** with an NLOS urban model `PL[dB] = α + 10·β·log(d) + X_σ`, `α = 46.61`, `β = 3.63`, `σ = 9.83 dB`. Session continuity across UPF changes follows **SSC mode 3** (*"These steps follow the procedures of Session and Service Continuity (SSC) mode 3, as specified in 3GPP TS 23.501 [32]"*).

- **C. Network layer/domain:**
  **5G Core network — user plane (UPF) placement / MEC / NFV-MANO orchestration**; applications layer for C-V2X. Not RAN/MAC.

- **D. Network entities involved:**
  **UPF instances** (deployed at MEC hosts); **MEC hosts**; **base stations** (|N| = 247 real BS locations); **vehicles (V)** grouped into **C speed classes**; **SDN controller**; **NFV MANO**; the **DRL agent** (base station viewed as agent); **DQN** and **multi-actor AC** networks; the **Köln Vehicular Mobility Dataset**; **Github repository** for reproducibility.

- **E. Input/state parameters (exact observation vector if reported):**
  Verbatim: *"The state s_t includes a range of factors that effectively capture the current status of the system, including: The number of connected vehicles `v_cj` determined using equation (4) for each node j in speed class c, and then **normalized by dividing by the total number of all vehicles |V|**. The current UPF deployment status `y_j` for each node j."*
  Exact state vector (their Eq. 9): `s_t = [v_11, …, v_C1, y_1, …, v_1|N|, …, v_C|N|, y_|N|]`, with **state size = |N|(C + 1)**.
  Also stated in prose: *"The state in our DRL model represents the current network conditions, including the number of vehicles connected to each base station, the vehicle speed, and the status of UPF deployment across the nodes."* Vehicle speeds enter as discrete **speed classes** (speed data ranges 0–100 km/hr, *"we evenly partition speed range for each class"*).

- **F. Decision variables (exact action space if reported):**
  *"In our scenario, the action `a_t` performed by the agent involves deploying a UPF instance as a node at the next time step in order to set `y_{a_t}` to 1."* Prose: *"The action chosen by the DRL agent involves selecting the node where a new UPF should be deployed for the next time step… In scenarios with multiple UPFs, the agent selects which UPF to allocate to each vehicle."* (The abstract of the published version summarises the space as "the optimal location of UPFs"; no explicit cardinality is stated beyond one node choice per decision.) Constraints on deployment: `Σ_{i∈N} y_i ≤ N_UPF` (Eq. 5), `Σ_{j∈N} z_ij = 1, i ∈ V` (Eq. 6), `z_ij ≤ y_j` (Eq. 7).

- **G. Objective function (quote exact reward/cost):**
  Verbatim: *"The reward function is designed to encourage actions that minimize communication latency. Specifically, the reward is defined as the negative of the overall latency experienced by the vehicles in the network."* Their **Eq. 10: `r_t = − f_latency`**, where the average latency objective (Eq. 8) is
  `f_latency = (1/|V|) Σ_{i∈V} Σ_{j,k∈N} x_ij · z_ik · l_jk`,
  with `l_ij` the shortest-path latency between nodes (Eq. 1), `x_ij` the vehicle-to-BS attachment indicator and `z_ij` the UPF-assignment indicator. Return: `R = Σ_{k=0}^{∞} γ^k r_{t+k}` (Eq. 11).

- **H. Constraints:**
  - **Single-BS attachment per vehicle:** `Σ_{j∈N} x_ij = 1, ∀i ∈ V` (Eq. 3).
  - **Bounded number of deployed UPFs:** `Σ_{i∈N} y_i ≤ N_UPF` (Eq. 5).
  - **Single UPF anchor per vehicle:** `Σ_{j∈N} z_ij = 1, i ∈ V` (Eq. 6).
  - **Deployment–assignment consistency:** `z_ij ≤ y_j` (Eq. 7).
  - **Association rule:** *"Each vehicle is assigned the UPF which provides the lowest communication latency."*
  - **Connectivity of the BS graph:** *"we connect all base station pairs within a certain distance threshold of 500 meters. Subsequently, we identify the two largest connected components… until a single connected graph is achieved."*
  - **Physical-layer constraint of 5G NR (from the companion literature, not this paper's own constraint set): none.**

- **I. Scheduling algorithm + optimization method:**
  Two DRL methods compared: **(i) Deep Q-Network (DQN)** — evaluated Q-network `Q(s_t, a_t | θ_q)` with a periodically synced target network, MSE loss (Eq. 15), gradient update (Eq. 16), **experience replay memory D** storing `(s_t, a_t, r_t, s_{t+1})`, and **ε-greedy** exploration with uniform-random initialisation and exponential ε decay; and **(ii) Actor–Critic (AC)** with **temporal-difference** actor updates using `δ_t = r_t + γV(s_{t+1}; θ_c) − V(s_t; θ_c)` (Eq. 17) and a **centralised critic** with **decentralised actors** — extended to a **multi-actor** formulation (*"a multi-actor approach in order to predicting the allocation of multiple UPFs"*), with per-UPF policy parameters `θ_{a_i}` updated in the loop `for i = 1 to N_UPF`.

- **J. ML/DRL used? yes/no and which:**
  **Yes — Deep Reinforcement Learning: DQN and Actor–Critic (multi-actor AC).** Hyper-parameters quoted:
  - **DQN:** batch size **25**; optimizer **Adam** with learning rate **0.0005**; ε initialised to **1**, *"decayed exponentially by a decay factor of **0.99** per iteration"*; Q-network *"constructed with fully connected neural networks, featuring **two hidden layers, each containing 1024 nodes**, and utilizing **ReLU** activation."*
  - **AC:** Critic learning rate **0.0005**; **Actor learning rate 0.00005** (*"the Actor network requires slower adjustments"*); *"The Actor and Critic networks are constructed using fully connected neural networks, featuring **two hidden layers with 1024 and 512 nodes**, respectively. The output layer of the Actor employs **softmax** activation… whereas the remaining layers utilize ReLU."*

- **K. Simulator / testbed / dataset (exact names + versions):**
  **Simulation only — no testbed.** Verbatim: *"The simulation environment was implemented using **Python 3.10** and **TensorFlow 2.8.0**"*, on *"a machine running **Windows 10**, equipped with an **Intel Core i7-10870H processor (2.2–5 GHz, 8 cores) and 64 GB of RAM**."*
  **Dataset:** the **Köln Vehicular Mobility Dataset** — *"which provides realistic mobility traces for **over 700,000 vehicles across a 24-hour period within a 400 square kilometer area of Cologne, Germany**… This dataset, approximately **20 GB** in size, captures vehicular dynamics at a high resolution with a **1-second sampling interval**, including data on vehicle coordinates, speeds, and timestamps."* Real infrastructure: *"The simulation setup incorporated real-world base station locations, using a dataset of **247 base stations** obtained from public German databases."*
  **Code availability:** *"The source code and configuration files used for the simulation, along with data processing scripts, are publicly available in the project' GitHub repository at https://github.com/albizialebbeck/drl_upf allocation"* (URL as printed in the retrieved text; note the space in "drl_upf allocation" is an artefact of the extraction).

- **L. Traffic model:**
  Not a synthetic traffic generator: **real mobility traces**. Verbatim: *"We have chosen a timeslot duration of **15 seconds**. During each timeslot, we capture position and speed of vehicles based on their timestamps within the corresponding period from the datasets of vehicle trips."* Train/test split: *"During the training phase, we initialize and train the proposed DRL agent using the dataset during the time period from **9 AM to 12 PM**. During the evaluation phase, we evaluate the trained agent with different vehicle trips from the dataset during the time period from **12 PM to 3 PM**. Each phase consists of a simulation period of **3 hours or 720 timeslots**."* Speed range **0–100 km/h**, evenly partitioned into C classes.

- **M. Network scale:**
  **|N| = 247 base stations** (real locations, linked within a 500 m threshold into a single connected graph); Köln dataset covering **>700,000 vehicles over 400 km²**; **720 timeslots of 15 s** per phase; number of UPFs **N_UPF swept from 1 to 12**; **C speed classes swept** (the three-speed-class configuration performs best). Number of simultaneously connected vehicles per slot: **NOT REPORTED** as a single figure (derived from the Köln traces).

- **N. Baselines (exact names):**
  **K-mean Greedy Average** [ref 24 = Fondo-Ferreiro, Candal-Ventureira, González-Castaño, Gil-Castiñeira, *"Latency reduction in vehicular sensing applications by dynamic 5G user plane function allocation with session continuity"*] and **Overhead-aware Greedy Average** [ref 28]. (The abstract loosely says *"K-mean Greedy Average and Greedy Average algorithms"*; the body names the second one precisely as *"Overhead-aware Greedy Average"* — **this inconsistency exists in the retrieved source**.)

- **O. Metrics:**
  **Average communication latency (µs)**, **95% confidence intervals of latency** (latency deviation/reliability), **UPF relocation percentage**, **algorithm computation time**, and **complexity order** (proposed AC: `O(|N| · N_UPF)`; K-mean Greedy Average: *"comparable overall complexity of O(|N| · N_UPF)"*; Overhead-aware Greedy Average: `O(|N|² · N²_UPF)`), plus DQN MSE loss and critic loss convergence curves.

- **P. Main quantitative results (EXACT numbers with the comparison, quoted):**
  - **Abstract (headline):** *"The proposed AC algorithm achieved **up to 40% reduction of average latency** compared with the baseline methods when the placement of multiple UPFs are considered."*
  - **Convergence:** *"The MSE loss shows a clear trend towards convergence after around **400 iterations**"* (DQN). *"It shows significant decrease followed by convergence after **300 iterations**"* (AC). *"the AC algorithm achieves faster convergence with fewer iterations compared to the DQN algorithm."*
  - **Latency levels:** *"The average latency values are within the range of **43–46 μs**."* After AC convergence, latency *"reaching similar values of approximately **40–50 μs** for all scenarios."*
  - **Multi-UPF scaling (1 → 12 UPFs):** *"The result shows a trend of decreasing average latency as more UPFs are deployed"*; *"our proposed AC algorithm with the multi-actor approach… outperforms the K-mean Greedy Average, achieving **up to 40% in latency reduction**. Although the proposed AC algorithm **fails to beat the Overhead-aware Greedy Average** in performance, it is capable of achieving comparable latency levels."*
  - **Reliability:** *"the confidence intervals for the proposed AC algorithm and the Overhead-aware Greedy Average are notably small… In contrast, the K-mean Greedy Average shows significantly larger confidence intervals, especially as the number of UPFs increases."*
  - **Relocation overhead:** *"The proposed AC algorithm shows consistently low UPF relocation percentages for all UPF configurations… the K-mean Greedy Average requires the percentages of UPF relocation greater than those of other algorithms… The Overhead-aware Greedy Average algorithm provides the lowest percentages of UPF relocation and the lowest latency at the expense of the largest computational time."*
  - **Computation time:** *"The proposed AC algorithm demonstrates superior performance in terms of computational efficiency"* with complexity `O(|N| · N_UPF)` versus `O(|N|² · N²_UPF)` for Overhead-aware Greedy Average.

- **Q. Main limitation:**
  **Simulation-only** (no testbed/over-the-air validation), with a dataset covering **one city** — the authors state: *"Limited Generalizability of Dataset: The vehicular dataset used in the simulation represents traffic patterns specific to a particular urban environment. While the dataset provides realistic mobility traces, its generalizability to other environments, such as rural areas or different traffic conditions, remains a challenge."* Other stated challenges: *"High Variance in Training: During the early stages of training the AC algorithm, we observe significant fluctuations in performance due to high variance in the reward function"*; *"Complexity of Multi-Actor Learning: Implementing a multi-actor approach for UPF allocation adds complexity to the model. Coordination between multiple actors increases the computational overhead, particularly in large-scale vehicular networks, which poses challenges in ensuring real-time performance."* The paper also concedes *"the proposed AC algorithm does not achieve the lowest percentages of UPF relocation"*, and the quality/venue profile is weaker than the primary pick (very large reference list with many loosely related citations; inconsistent baseline naming between abstract and body).

- **R. Research gap this suggests:**
  (i) **No QoS-flow / 5QI / GBR awareness at all** — the reward is pure latency minimisation for vehicles; there is no notion of 5QI, QoS flow, GBR/non-GBR, per-flow priority or slice SLA, so **QoS-flow-level scheduling in the 5G core remains completely open**. (ii) **No energy/carbon dimension** (explicitly listed as future work: *"Integrating additional performance metrics, such as energy efficiency and computational overhead"*). (iii) **UPF relocation cost is measured but not optimised jointly** — a multi-objective (latency + migration overhead) constrained formulation is open; note the authors' own admission that the Overhead-aware greedy beats them on latency. (iv) **No real-testbed validation** and no cross-domain coupling with the RAN scheduler (Papers 1–2). (v) Online/continual learning and federated approaches are named as future directions (*"Real-time adaptability of the DRL model could be explored through online learning techniques… Collaborative learning approaches, such as federated learning, could enhance privacy and security"*).

- **S. Best URL actually retrieved + whether read FULL TEXT or ONLY ABSTRACT:**
  `https://ieeexplore.ieee.org/ielx8/6287639/10820123/10819391.pdf` (publisher's open-access CC-BY PDF, 15 pages, obtained via the `r.jina.ai` text proxy because direct `curl` returns HTTP 502). Also verified through DOAJ (`https://doaj.org/article/699dd153f4364a0c9dc5875dec0086e6`) and Semantic Scholar. **FULL TEXT READ** (15 pages). Local artefact: `pdfs/upf_cv2x_fulltext.txt`.

---

## Appendix: retrieval and verification log (auditability)

| Item | DOI | Venue (Crossref-verified) | Year | OA status | Retrieved? |
|---|---|---|---|---|---|
| Learn to Schedule (LEASCH) | 10.1109/ACCESS.2020.3000893 | IEEE Access, 8:108088–108101 | 2020 | Gold OA, CC-BY (+ arXiv:2003.11003) | **Full text** (publisher PDF via proxy + arXiv PDF) |
| NRflex: Enforcing network slicing in 5G New Radio | 10.1016/j.comcom.2021.09.034 | Computer Communications, 181:284–292 | 2022 | OA accepted manuscript | **Full text** (EURECOM accepted MS) |
| Satisfying Network Slicing Constraints via 5G MAC Scheduling | 10.1109/INFOCOM.2019.8737604 | IEEE INFOCOM 2019, pp. 2332–2340 | 2019 | **Closed — no OA copy (Unpaywall `is_oa: False`)** | **Abstract/metadata only** |
| Power Consumption-Aware 5G Edge UPF Selection using DRL | 10.1109/NFV-SDN61811.2024.10807472 | 2024 IEEE NFV-SDN, pp. 1–6 | 2024 | Author copy in IRIS repository | **Full text** (UNITN IRIS PDF) |
| UPF Allocation for C-V2X Network Using DRL | 10.1109/ACCESS.2024.3524886 | IEEE Access, 13 | 2025 | Gold OA, CC-BY, DOAJ-indexed | **Full text** (publisher PDF via proxy) |
| "Toward a Flexible and Reconfigurable 5G Network Slicing Scheduler" | — | — | — | — | **DOES NOT RESOLVE — no such publication found** |

**Not pursued further (candidates surfaced but not extracted), for the parent agent's awareness:** *Scaling UPF Instances in 5G/6G Core With Deep Reinforcement Learning* (Nguyen, Van Do, Rotter, **IEEE Access 2021**, DOI 10.1109/ACCESS.2021.3135315 — DRL for UPF scaling, but **outside the requested 2023–2026 window**); *Dynamic Energy-Efficient User Plane Function Selection in 5G Networks* (Afshar Borji, Bruschi, Costa, Lombardo, **IFIP Networking 2025**, open PDF at `networking.ifip.org`, retrieved locally as `pdfs/upf_ifip2025.pdf` — UPF selection using an **LSTM** traffic predictor with a utility function, **not DRL**, and its energy-saving result is *"approximately 10.46% compared to the best static UPF deployment"*); *Dynamic Deployment and Traffic Scheduling of User-Plane Functions in 5G Networks: A Hybrid Benders-Reinforcement Learning Approach* (DOI 10.1109/ICEI65890.2026.11447627, IEEE ICEI 2026 — real record but a weaker venue and single-author conference paper); *Intelligent Resource Allocation via Hybrid Reinforcement Learning in 5G Network Slicing* (DOI 10.1109/ACCESS.2025.3550518, IEEE Access 2025 — slicing resource allocation, RAN-side).

**Rigor notes:** (1) No number, baseline, simulator or result in this document was inferred, interpolated or invented; every quoted figure is reproduced verbatim from the retrieved artefact named in the corresponding section. (2) Where the published version and the arXiv preprint of LEASCH disagree (number of training episodes) or where an abstract and body disagree (C-V2X baseline naming), the disagreement is reported rather than silently resolved. (3) Simulation-only studies (all five papers) are explicitly distinguished from testbed work; only the NFV-SDN 2024 paper uses *any* real-hardware measurements, and those are used as *models inside a simulator*, not as a live evaluation. (4) Paper 2 as titled could not be verified to exist; the two substitutes are clearly labelled as substitutes, and one of them (Mandelli et al.) is flagged as abstract-only.
