# Agent D — ATSSS / 5G-core multipath scheduling + modern (2023+) AI multipath scheduler + gap-evidence probe

Scope of this file: 4 assigned papers (2 ATSSS/5G-core, 1 MPTCP+RL, 1 self-selected 2023–2026 peer-reviewed
AI/ML/DRL multipath-scheduling paper). Extraction follows `EXTRACTION_SPEC.md` exactly: every field is taken
only from a document actually fetched in this session; unstated fields are literally `NOT REPORTED`; quoted
text is in quotation marks; testbed vs simulation is never blurred.

### Retrieval environment notes (affects the "full text vs abstract" verdicts)
- **OpenAlex API was unusable this session**: `HTTP 429` with body
  `{"error":"Rate limit exceeded","message":"Insufficient budget. This request costs $0.001 but you only have $0 remaining. Resets at midnight UTC."}`
  (verified 2026-09-18). Verification was therefore done with **Crossref** (+ DBLP/Semantic Scholar IDs,
  Unpaywall, IEEE Xplore metadata pages, arXiv API).
- **IEEE Xplore direct fetch is bot-blocked**: `curl` to `https://ieeexplore.ieee.org/document/<id>` returned
  `HTTP 202` with `size:0` for every document. The readable route was the plain-text proxy
  `https://r.jina.ai/https://ieeexplore.ieee.org/document/<id>`, which returns the metadata page, the
  **full abstract**, and **only the free-preview "I. Introduction" section** for paywalled papers, followed by
  "Sign in to Continue Reading". Sections II–V (system model, DRL approach, experiments) are **not** retrievable.
- **Unpaywall confirms no OA copy exists** for the two ATSSS papers or for the MPTCP-RL paper:
  `"is_oa": false, "best_oa_location": null` for all three DOIs.

---

## Assigned paper 1

### Deep Reinforcement Learning for Access Traffic Splitting in 5G Core System
- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors: Thanh Son Pham, Phi Hung Nguyen, Quan Huan Vu, Cong Dan Pham, Duc Hai Nguyen.
  - Year: 2024 (conference dates 16–18 October 2024; added to IEEE Xplore 14 January 2025).
  - Venue: **2024 15th International Conference on Information and Communication Technology Convergence (ICTC)**,
    Jeju Island, Korea (Republic of). Pages 903–908.
  - DOI: **10.1109/ICTC62082.2024.10826899** (Crossref-verified; IEEE Xplore document id 10826899).
  - **Peer-reviewed** conference paper (Crossref `type: proceedings-article`; DBLP key `conf/ictc/PhamNVP024`).
  - Note: Semantic Scholar classifies it as `["JournalArticle","Conference"]`; Crossref — the authoritative
    registration agency record — says `proceedings-article` in a conference proceeding. I trust Crossref.
- **1. Number and type of paths** — `NOT REPORTED` (the abstract states only that two access technologies are
  involved). The abstract names "3GPP Radio Access Technology (RAT) (LTE, 5G New Radio (NR))" and "non-3GPP RAT
  (WiFi)". An exact count of simultaneous paths is not stated in the retrieved text.
- **2. Network architecture** — `NOT REPORTED` in detail. The abstract places the agent inside the 5G core:
  "we have developed a deep reinforcement learning-based agent to integrate into the Policy Control Function
  (PCF) of the 5G Core System". No proxy/middlebox/topology detail is given in the retrieved text.
- **3. Transport protocol** — **ATSSS** (3GPP Access Traffic Steering, Switching, and Splitting). The abstract
  says the work is "[b]ased on the standards provided by 3GPP regarding Access Traffic Steering, Switching, and
  Splitting (ATSSS)". MPTCP/MPQUIC are **not mentioned** in the retrieved text.
- **4. Scheduler location** — **5G core control plane, in the PCF** (Policy Control Function). This is the key
  architectural claim: "a deep reinforcement learning-based agent to integrate into the Policy Control Function
  (PCF) of the 5G Core System". UPF/SMF/N4/N6 are **not mentioned** in the retrieved text. It is a *control-plane
  policy* placement, not a UPF data-plane placement.
- **5. Scheduler inputs** — Only one input is named in the retrieved text: **NR congestion**. The abstract states
  the agent is "capable of making guidance for offloading NR traffic to WiFi in case of NR network congestion".
  The exact signal set (PRB utilisation, load, RSRP, latency, throughput…) is `NOT REPORTED`.
- **6. Path metrics used** — Latency is the only metric named: the agent ensures "the latency requirements for
  end-users"; revenue/"revenue for the network operator" is the second objective. No RTT/bandwidth/loss metric
  definitions are given in the retrieved text.
- **7. Scheduling decision (exact action space)** — `NOT REPORTED` as a formal action space. Qualitatively the
  action is **offloading guidance from NR to WiFi**: "making guidance for offloading NR traffic to WiFi in case
  of NR network congestion". No steering percentages, no "steer X% to 3GPP access" formulation, and no discrete
  action set is stated in the retrieved text. **Important:** the intro's free preview frames the problem as
  *partial or full* offload ("devices will offload part or all of the traffic to WiFi either based on rules
  preset on them or based on guidance from the core network system"), which implies a split ratio, but the paper
  never states the action parameterisation in the retrievable text.
- **8. Packet-level or flow-level scheduling** — `NOT REPORTED`. The retrieved text describes policy/guidance
  ("traffic-splitting mechanism", "offloading decisions"), i.e. a *flow/UE-level steering policy* rather than a
  per-segment packet scheduler, but the paper does not state the granularity explicitly, so this is not asserted.
- **9. Reordering handling** — `NOT REPORTED`.
- **10. Congestion-control interaction** — `NOT REPORTED`.
- **11. Objective** — Two objectives, both stated in the abstract: "[t]he agent outperforms traditional methods
  by ensuring the latency requirements for end-users while maximizing the revenue for the network operator."
  The introduction's free preview states the tension explicitly: "network operators need a sensible
  traffic-splitting mechanism, ensuring service quality for users while avoiding too much revenue loss."
- **12. Algorithm** — `NOT REPORTED` (only "deep reinforcement learning" is named; no DQN/DDPG/PPO naming).
- **13. ML/DRL usage** — **Yes**, deep reinforcement learning. Exact variant: `NOT REPORTED`. Network
  architecture (layers/neurons): `NOT REPORTED`.
- **14. Simulator / testbed** — `NOT REPORTED`. No simulator (free5GC/Open5GS/ns-3) and no testbed is named
  anywhere in the retrieved text. The word "experiment" does not appear in the abstract.
- **15. Traffic model** — `NOT REPORTED`.
- **16. Baselines** — `NOT REPORTED` by name. Only the generic phrase "traditional methods" is used.
- **17. Metrics** — Latency (of end-users) and revenue (of the network operator) are named qualitatively.
  Exact metric definitions and units: `NOT REPORTED`.
- **18. Main result** — `NOT REPORTED`. **No numbers appear in the abstract or the retrievable intro.** The
  only claimed result is qualitative: the agent "outperforms traditional methods".
- **19. Limitation** — As stated by the authors: `NOT REPORTED`. Methodological limitations I observe from the
  retrievable text: (a) no quantitative result is disclosed at abstract level, so the claim cannot be checked;
  (b) the only system signal named is "NR network congestion", with no stated observation vector; (c) action
  granularity (partial vs binary offload) is not defined; (d) no simulator/testbed is named, so reproducibility
  cannot be assessed; (e) it is a 6-page conference paper (pp. 903–908), which bounds how much system detail can
  exist at all.
- **20. Research gap this suggests** — ATSSS splitting decisions placed in the **PCF** are evaluated only at the
  level of "latency vs revenue"; there is no reported data-plane coupling (UPF/N4/N6), no reported simulator or
  open-source 5G core, no reported action-space formalisation, and no reported numbers. A PhD-level gap is the
  absence of a **reproducible, data-plane-anchored ATSSS scheduler** with an explicit split-ratio action space
  and a stated measurement methodology.
- **21. Best URL actually retrieved, and whether full text or abstract** —
  `https://r.jina.ai/https://ieeexplore.ieee.org/document/10826899` (proxy for
  `https://ieeexplore.ieee.org/document/10826899`) — **ABSTRACT ONLY** (metadata + abstract + free-preview
  §I. Introduction; the page then shows "Sign in to Continue Reading"). Metadata cross-verified at
  `https://api.crossref.org/works/10.1109/ictc62082.2024.10826899` and
  `https://api.unpaywall.org/v2/10.1109/ictc62082.2024.10826899?email=research@example.org` (`is_oa: false`).
  All other fields above are `NOT REPORTED` because they are not in the abstract — not because they were
  uninteresting.

---

## Assigned paper 2

### Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective Reinforcement Learning
- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors: Thanh Son Pham, Phi Hung Nguyen, Quan Huan Vu, Duc Hai Nguyen (4 authors — note this paper has
    **no** Cong Dan Pham, unlike paper 1; Crossref author list and DBLP key `conf/icccn/PhamNVN25` agree).
  - Year: 2025 (conference dates 04–07 August 2025, Tokyo, Japan; added to IEEE Xplore 29 August 2025).
  - Venue: **2025 34th International Conference on Computer Communications and Networks (ICCCN)**, pages 1–8.
  - DOI: **10.1109/ICCCN65249.2025.11133925** (Crossref-verified; IEEE Xplore document id 11133925).
  - **Peer-reviewed** conference paper (Crossref `type: proceedings-article`).
  - Semantic Scholar again lists `["JournalArticle","Conference"]`; Crossref says `proceedings-article`.
    I trust Crossref.
- **1. Number and type of paths** — Two access paths, heterogeneous: "particularly between two prevalent Radio
  Access Technologies (RATs): 5G New Radio (NR) and WiFi". Heterogeneous (3GPP + non-3GPP).
- **2. Network architecture** — 5G System with a **Multi-Access PDU session**-style ATSSS arrangement between a
  3GPP access (5G NR) and a non-3GPP access (WiFi), with the intelligence **in the 5G core control plane**:
  the solution is "deployed within the 5GS control plane to enable dynamic traffic-splitting decisions at the
  access layer". The intro adds: "ATSSS ... is a framework designed to manage traffic across multiple access
  networks, including 3GPP (5G, LTE) and non-3GPP (WiFi, LiFi) accesses. It enables features like traffic
  steering, switching, and splitting at a finer granularity than previous standards, such as Multi Access PDU
  sessions, allowing concurrent use of multiple access networks for data traffic."
- **3. Transport protocol** — **ATSSS** ("built upon the 3GPP-standardized Access Traffic Steering, Switching,
  and Splitting (ATSSS) framework"). MPTCP/MPQUIC are **not** named in the retrieved text. Note the intro
  clarifies the framework wording: "Multi Access PDU sessions".
- **4. Scheduler location** — **5G core control plane** ("deployed within the 5GS control plane", "empowers the
  5G Core (5GC) with greater intelligence and autonomy"). The specific NF (PCF vs SMF vs a new ATSSS control
  function) is **not named in the retrievable abstract/intro** — the companion ICTC 2024 paper places its agent
  in the PCF, but I do **not** transfer that here. UPF/N4/N6: `NOT REPORTED`.
- **5. Scheduler inputs** — `NOT REPORTED`. The intro only motivates the problem ("Offloading traffic to WiFi
  may reduce operator revenue, because WiFi services are provided by Internet Service Providers other than the
  mobile network operators. In this case, the network operators can only charge their subscribers for 5G NR
  data."). No state vector is given in the retrievable text.
- **6. Path metrics used** — QoS (as a satisfaction level) and ROI (as a retention/return measure) are the two
  metric families. Their exact definitions are `NOT REPORTED`.
- **7. Scheduling decision (exact action space)** — `NOT REPORTED` as a formal action space. Qualitatively:
  "dynamic traffic-splitting decisions at the access layer" between 5G NR and WiFi. The abstract does not state
  whether the action is a continuous split ratio/percentage or a discrete steering choice.
- **8. Packet-level or flow-level scheduling** — `NOT REPORTED`; the language used is control-plane
  "traffic-splitting decisions at the access layer", i.e. policy-level, not per-segment packet scheduling.
- **9. Reordering handling** — `NOT REPORTED`.
- **10. Congestion-control interaction** — `NOT REPORTED`.
- **11. Objective** — Explicitly multi-objective, quoted from the abstract: "efficiently managing massive data
  traffic to ensure seamless Quality of Service (QoS) for users while retaining Return on Investment (ROI) for
  network operators." The intro sharpens it: "the problem is to dynamically manage traffic splitting to balance
  the operator's ROI with services' QoS (and thus the customer satisfaction)."
- **12. Algorithm** — **Multi-Objective Reinforcement Learning (MORL)**: "By integrating an enhanced
  Multi-Objective Reinforcement Learning (MORL) framework". The specific MORL variant (e.g. Pareto Q-Learning,
  envelope Q-learning, weight-vector decomposition) is `NOT REPORTED`.
- **13. ML/DRL usage** — **Yes** — an "enhanced Multi-Objective Reinforcement Learning (MORL) framework".
  Whether the MORL implementation is deep (neural function approximation) is `NOT REPORTED`; the abstract says
  "Multi-Objective Reinforcement Learning" without the "deep" qualifier. Layers/neurons: `NOT REPORTED`.
- **14. Simulator / testbed** — **Simulation only**, and unnamed: "Experiments conducted in a simulated network
  environment demonstrate significant performance improvements". No free5GC / Open5GS / ns-3 / testbed name is
  given in the retrievable text. (The ICTC 2024 companion also names no simulator.) This is a *simulation*, not
  an emulation or a real testbed — do not blur.
- **15. Traffic model** — `NOT REPORTED` (abstract says only "massive data traffic" / "5G-enabled services").
- **16. Baselines** — Named generically only: "compared to traditional parameter-based methods". No named
  baseline scheduler (e.g. a specific 3GPP ATSSS steering mode) appears in the retrievable text.
- **17. Metrics** — "QoS satisfaction level" and "ROI retention". Units/definitions `NOT REPORTED`.
- **18. Main result** — Exact figures from the abstract, quoted: "a **19% higher QoS satisfaction level** and a
  **9% enhancement in ROI retention** compared to traditional parameter-based methods." These are the only
  numbers available (no tables/figures are retrievable).
- **19. Limitation** — As stated by the authors: `NOT REPORTED`. Methodological limitations I observe:
  (a) no named simulator or testbed, so results are not independently reproducible; (b) the baseline is a
  generic "traditional parameter-based methods" family rather than a specified 3GPP ATSSS steering mode;
  (c) QoS and ROI are reported as single aggregate percentages without dispersion, confidence intervals or
  per-scenario breakdown; (d) the RL observation/action space is entirely absent from the retrievable text;
  (e) 8 pages (pp. 1–8) bounds the system detail available.
- **20. Research gap this suggests** — There is (to the extent this retrievable text shows) **no published
  action-space formalisation, no state definition, and no released simulator configuration** for MORL-based
  ATSSS splitting in the 5G core. A concrete gap: an open, reproducible ATSSS control-plane environment
  (e.g. free5GC/Open5GS + a documented MORL interface) with an explicit split-ratio action space, so that QoS
  vs ROI trade-off curves can be compared across papers.
- **21. Best URL actually retrieved, and whether full text or abstract** —
  `https://r.jina.ai/https://ieeexplore.ieee.org/document/11133925` (proxy for
  `https://ieeexplore.ieee.org/document/11133925`) — **ABSTRACT ONLY** (metadata + full abstract + free-preview
  §I. Introduction up to the ATSSS background paragraph; then the page ends). Metadata cross-verified at
  `https://api.crossref.org/works/10.1109/icccn65249.2025.11133925` and
  `https://api.unpaywall.org/v2/10.1109/icccn65249.2025.11133925?email=research@example.org` (`is_oa: false`,
  `best_oa_location: null`).

---

## OA-availability audit (independent second pass; evidence for every "ABSTRACT ONLY" verdict)

*(Cross-cutting note placed here for readability; it covers **all four** assigned papers plus the paper-4
alternatives, including items whose full extraction appears below.)*

A dedicated second retrieval pass re-checked every DOI through routes beyond the ones used above. Result:
**only the Meta-DAMS author copy is freely readable; the other four papers are confirmed closed access.**
No PDF was fabricated and no file was created for a paper that could not be read.

| DOI | Unpaywall | Semantic Scholar `openAccessPdf` | Other routes tried (all failed) |
|---|---|---|---|
| 10.1109/ICTC62082.2024.10826899 (paper 1) | `is_oa: false`, `oa_status: closed`, **0 OA locations** | `url: ""`, `status: CLOSED` | arXiv API (`all:"Access Traffic Splitting"`) 0 entries; CORE v3 0 hits; ResearchGate HTTP 403 (CAPTCHA via proxy); Google Scholar HTTP 403; DuckDuckGo HTTP 202 challenge; Mojeek HTTP 403; Bing JS-only; TechRxiv HTTP 403; scholar.archive.org bot-blocked; `api.fatcat.wiki` HTTP 000. Authors are industry (Viettel) — no institutional repository exists. |
| 10.1109/ICCCN65249.2025.11133925 (paper 2) | `is_oa: false`, `oa_status: closed` | `isOpenAccess: false`, `url: ""` | arXiv 0 entries; CORE v3 0 records; ResearchGate 403/CAPTCHA; Google Scholar 403; aggregators unusable (as above). |
| 10.1109/MWC.013.2100658 (paper 3) | `is_oa: false`, `oa_status: closed`, `oa_locations: []` | `isOpenAccess: false`, `url: ""` (paperId `12222fc2ca938a60f72d6b0169f2cd2cf15e08cf`) | CORE v3 0 records; arXiv 0 (incl. author queries `au:Alay`, `au:Saxena`); the UVic angle was checked specifically because co-author Wenjun Yang is at UVic — Lin Cai's full publication list `https://www.ece.uvic.ca/~cai/public.html` does **not** host this paper; Wenjun Yang homepage probes all failed (`/~wenjuny/` 404, `/~wyang/` 404, `wenjunyang.ca` 000, `csc.uvic.ca/~wyang/` 403); Hunan Normal University has no OA copy; Chinese aggregators (kczg.org.cn, x-mol) are profile pages only. |
| 10.1016/j.iot.2025.101616 (paper 4 alternative) | `is_oa: false`, **0 OA locations** | `status: CLOSED` | No arXiv preprint; **Karlstad DiVA record exists but is metadata-only** — `https://kau.diva-portal.org/smash/record.jsf?pid=diva2:1965074` (HTTP 200, URN `urn:nbn:se:kau:diva-104815`) states the full text is in the original publication, and `/smash/get/diva2:1965074/FULLTEXT01.pdf` returns HTTP 000 (no file); CORE returned only the *related* DEAR paper (CORE id 633909916) with empty `downloadUrl`/`fullText`; BITS Pilani DSpace API unreachable (HTTP 000); Cristin (Norwegian CRIS) returned empty `[]`; ScienceDirect beyond the Introduction is paywalled. |
| 10.1109/TCCN.2024.3502512 (paper 4B) | publisher version `is_oa: false` | — | **FOUND**: author's accepted manuscript at `https://www.ece.uvic.ca/~cai/tccn24-meta-dams.pdf` (HTTP 200, `application/pdf`, 3,976,091 bytes, PDF v1.5, 15 pages), located via Lin Cai's UVic publication list. Verified by its own first page: "accepted for publication in IEEE Transactions on Cognitive Communications and Networking. This is the author's version" with DOI 10.1109/TCCN.2024.3502512, and title/authors match exactly. |

Environment blockers recorded for reproducibility of this audit: `api.fatcat.wiki` and
`dspace.bits-pilani.ac.in` are network-unreachable (HTTP 000) from this sandbox, and ResearchGate, TechRxiv,
Google Scholar, Bing, DuckDuckGo, Mojeek and scholar.archive.org are all bot-blocked. **OpenAlex was
unavailable for the entire session** (HTTP 429, daily budget exhausted — see the note at the top of this file),
so this audit rests on Unpaywall + Semantic Scholar + CORE + arXiv + author/institutional pages rather than
OpenAlex `best_oa_location`.

---

## Assigned paper 3

### Multipath TCP Meets Reinforcement Learning: A Novel Energy-Efficient Scheduling Approach in Heterogeneous Wireless Networks
- **TITLE VERIFICATION (requested explicitly):** the assigned title was "MPTCP Meets Reinforcement Learning:
  A Novel Energy-Efficient Scheduling Approach in Heterogeneous Wireless Networks". **The paper exists, and the
  only difference is the protocol spelled out in full.** The registered title is
  **"Multipath TCP Meets Reinforcement Learning: A Novel Energy-Efficient Scheduling Approach in Heterogeneous
  Wireless Networks"** — i.e. "Multipath TCP" where the request said "MPTCP". This is not a substitute; it is
  the same paper (confirmed by DOI, authors, venue and the exact remainder of the title string).
- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors: Pingping Dong, Rongcheng Shen, Qian Wang, Yuning Zuo, Yajing Li, Dian Zhang, Lianming Zhang,
    Wenjun Yang.
  - Year: 2023 (Crossref `issued: [[2023, 4]]`; April 2023 issue).
  - Venue: **IEEE Wireless Communications**, vol. 30, no. 2, pp. 138–146.
  - DOI: **10.1109/MWC.013.2100658** (Crossref-verified; IEEE Xplore document id 9826510; DBLP key
    `journals/wc/DongSWZLZZY23`).
  - **Peer-reviewed** journal article (Crossref `type: journal-article`, publisher IEEE).
  - Source-disagreement check (spec rule 8): Crossref, DBLP and Semantic Scholar all agree on venue
    (IEEE Wireless Communications) and year (2023); Semantic Scholar's author ordering differs slightly
    (it lists Yuning Zuo before Yajing Li, and normalises "Dian Zhang" to "Dianxu Zhang"). I trust the
    **Crossref** author order and the IEEE Xplore page, and note the S2 ordering discrepancy here rather than
    silently choosing.
- **1. Number and type of paths** — Multiple heterogeneous wireless paths; the exact count is `NOT REPORTED`.
  The abstract speaks of "heterogeneous wireless networks", "multiple paths", "multiple interfaces" and
  "subflows"; the evaluation is described only as "a variety of network scenarios".
- **2. Network architecture** — `NOT REPORTED` in the abstract. The scheme is named **MPTCP-RL** and is
  described as managing "path usage among multiple connections" with a sender-side perspective ("the sender can
  adaptively select the optimal path set for a certain application according to the current network
  environment"). No proxy/middlebox/MPTCP-capable-server or 5G-core involvement is stated.
- **3. Transport protocol** — **MPTCP v1-family multipath TCP**; the abstract says "[m]ultipath TCP (MPTCP) has
  been standardized by the IETF as an extension of conventional TCP". The specific version (v0 vs v1) is
  `NOT REPORTED`. MPQUIC is not used.
- **4. Scheduler location** — **Sender-side path management** ("the sender can adaptively select the optimal
  path set"). It is an *asynchronous RL framework* that "separates the processes of offline training and online
  decision" — i.e. the online decision component sits with the sender, while training is offline. Kernel vs
  userspace implementation is `NOT REPORTED`.
- **5. Scheduler inputs** — `NOT REPORTED` in the abstract. The abstract refers to "the MPTCP transmission
  model" and "the current network environment" as inputs but names no concrete signal (no SRTT, cwnd, delivery
  rate, queue occupancy, loss rate, or BLEST-style penalisation is mentioned in the retrievable text).
- **6. Path metrics used** — Two are named: **delay** and **energy cost** — "existing scheduling systems, and
  selecting paths based on the path's delay or energy cost, may suffer from performance degradation" — plus
  **packet losses** ("random packet losses in wireless networks") and **throughput** (aggregate throughput as an
  outcome metric). Precise definitions/units `NOT REPORTED`.
- **7. Scheduling decision (exact action space)** — The decision is **selection of a path set for a flow**:
  "we propose a reinforcement learning-based multipath scheduler called MPTCP-RL to determine the optimal path
  set for different flows" and it will "adaptively select the optimal path set for a certain application". So
  the action space is **subset-of-paths selection per flow** (a combinatorial action), *not* a per-packet
  "send segment on path i" action and *not* a numeric split ratio. Exact enumeration of the action set is
  `NOT REPORTED`.
- **8. Packet-level or flow-level scheduling** — **Flow-level path selection / path-set selection.** The
  abstract's own words are "determine the optimal path set for different flows" and "manage path usage among
  multiple connections". It is *not* described as per-segment packet scheduling. The paper's title says
  "scheduling", but the abstract's mechanism is path-set selection — this distinction matters and is reported
  as stated rather than assumed.
- **9. Reordering handling** — `NOT REPORTED`. The abstract mentions "path heterogeneity and random packet
  losses" as the reason existing schedulers degrade, but no reordering detection mechanism, penalty term,
  receive-buffer or ATD handling is stated in the retrieved text.
- **10. Congestion-control interaction** — `NOT REPORTED`. The abstract does not name LIA, OLIA, wVegas, BALIA,
  BBR or Cubic, nor any coupling mechanism. It only notes that MPTCP "allows the system to utilize multiple
  paths simultaneously, which can aggregate bandwidth to improve network throughput".
- **11. Objective** — Stated in the abstract: "how to manage subflows with the MPTCP's scheduling system to
  determine which paths should be used for data transmission is of critical importance **to reduce energy
  consumption and ensure network throughput**"; and the results "improve the aggregate throughput and reduce
  energy consumption significantly compared to the state-of-the-art mechanisms". So: **energy minimisation
  subject to throughput.**
- **12. Algorithm** — "a reinforcement learning-based multipath scheduler called **MPTCP-RL**". It "adopts deep
  reinforcement learning as well as MPTCP transmission model to manage path usage" and is "an **asynchronous
  reinforcement learning framework**, which separates the processes of offline training and online decision to
  ensure that the learning process will not introduce extra delay and overhead on the decision making process
  in MPTCP path management." The specific DRL algorithm (DQN/DDPG/A3C/DDPG-variant) is `NOT REPORTED` in the
  retrievable text.
- **13. ML/DRL usage** — **Yes** — "deep reinforcement learning", asynchronous, with separated offline training
  and online decision. Exact DRL variant: `NOT REPORTED`. Network architecture (layers, neurons): `NOT REPORTED`.
- **14. Simulator / testbed** — `NOT REPORTED`. The abstract says only "[t]he extensive experimental results
  show that MPTCP-RL can improve the aggregate throughput and reduce energy consumption significantly ...
  in a variety of network scenarios." Whether this was an ns-3 simulation, an emulation, or a Linux testbed is
  **not stated in the retrievable text** — I explicitly do not guess.
- **15. Traffic model** — `NOT REPORTED` (only "a certain application" and "different flows").
- **16. Baselines** — `NOT REPORTED` by name. Only "the state-of-the-art mechanisms" generically.
- **17. Metrics** — **Aggregate throughput** and **energy consumption**, both explicitly named. Exact units and
  measurement method: `NOT REPORTED`.
- **18. Main result** — No numbers are available. The exact claim is: "MPTCP-RL can improve the aggregate
  throughput and reduce energy consumption **significantly** compared to the state-of-the-art mechanisms in a
  variety of network scenarios." Because this is an abstract-only retrieval, I report the claim as unquantified
  rather than importing any figure.
- **19. Limitation** — As stated by the authors: `NOT REPORTED`. Methodological limitations I observe from the
  retrievable text: (a) the action space is path-set selection, so the paper does not solve per-packet
  scheduling — a substantially coarser control granularity; (b) no congestion-control interaction is described,
  although MPTCP throughput/energy outcomes are strongly CC-dependent; (c) no simulator/testbed is named, so
  the energy model behind the "energy consumption" metric is unverifiable from the abstract; (d) it is an
  **IEEE Wireless Communications magazine-style article** (8 pages, pp. 138–146), which limits methodological
  depth relative to a full journal paper; (e) the asynchronous offline-training/online-decision split is
  claimed to add no decision-time overhead, but no overhead measurement is reported in the retrievable text.
- **20. Research gap this suggests** — MPTCP energy-aware scheduling via DRL is demonstrated at *path-set*
  granularity with an unstated energy model and unstated simulator. The gap: **no reproducible, packet-level,
  energy-aware MPTCP scheduler with a published energy model and a stated CC coupling**, and no cross-over
  study of when path-set selection is sufficient versus when per-segment scheduling is required.
- **21. Best URL actually retrieved, and whether full text or abstract** —
  `https://r.jina.ai/https://ieeexplore.ieee.org/document/9826510` (proxy for
  `https://ieeexplore.ieee.org/document/9826510`) plus the Semantic Scholar abstract record
  `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/MWC.013.2100658?fields=title,abstract,openAccessPdf,venue,year,externalIds`
  — **ABSTRACT ONLY**. Unpaywall: `https://api.unpaywall.org/v2/10.1109/mwc.013.2100658?email=research@example.org`
  → `is_oa: false`, `best_oa_location: null`; Semantic Scholar `openAccessPdf.status: null` with an empty URL.
  No OA PDF, arXiv preprint, or repository copy could be located.

---

## Assigned paper 4 — self-selected 2023–2026 peer-reviewed AI/ML/DRL multipath-scheduling paper

### How I selected it (required justification)
I searched Crossref, the arXiv API, Semantic Scholar and web search for 2023–2026 multipath-scheduling /
multipath-transport work using AI/ML/DRL. **Candidates considered and why they were not the pick:**

| Candidate | DOI / id | Venue, year | Why not picked |
|---|---|---|---|
| Next-generation DRL empowered actor-critic schedulers for multipath QUIC in 5G vehicular IoT | `10.1016/j.iot.2025.101616` | Internet of Things (Elsevier), 2025, vol. 32, art. 101616 | **Excellent topical fit** (MPQUIC + DRL + 5G) but **not open access**: Unpaywall `is_oa: false`, `best_oa_location: null`; no arXiv preprint found. Could not read it, so I could not extract it honestly. **Recommended for a follow-up if institutional access exists.** |
| DEAR: DRL Empowered Actor-Critic ScheduleR for Multipath QUIC Under 5G/B5G Hybrid Networks | `10.1007/978-3-031-57840-3_10` | AINA 2024, Springer LNCS | Conference version of the above; also paywalled (Springer), no OA copy found. |
| Reinforcement Learning Based Multipath QUIC Scheduler for Multimedia Streaming | `10.3390/s22176333` | Sensors (MDPI), 2022 | OA and readable, but **published 2022 — outside the requested 2023–2026 window.** |
| LiveStream Meta-DAMS | `10.1109/TCCN.2024.3502512` | IEEE TCCN 11(4):2739–2754, 2025 | **Selected as a second, secondary pick** — see Paper 4B. Kept as secondary because the author copy is a pre-publication accepted version and the primary focus is live video rather than 5G/6G access. |
| Learning to Harness Bandwidth with Multipath Congestion Control and Scheduling | arXiv 2105.14271 | arXiv preprint | Out of window (2021) and a preprint, not the target profile. |
| Transformer-Based Multipath Congestion Control: A Decoupled Approach for Wireless Uplinks | arXiv 2603.04550 | arXiv preprint, 2026 | Very relevant and recent, but **preprint only** (no peer-reviewed venue found); also framed as congestion control rather than scheduling. |
| Edge-Served Congestion Control for Wireless Multipath Transmission with a Transformer Agent | arXiv 2512.20186 | arXiv preprint, 2025 | Same reason — preprint, single author, CC-focused. |

**Chosen primary pick: Arain et al., "Energy-Aware MPTCP Scheduling in Heterogeneous Wireless Networks Using
Multi-Agent Deep Reinforcement Learning Techniques", *Electronics* 12(21):4496, 2023, DOI
`10.3390/electronics12214496`.** Reasons, in order of weight:
1. **Verified peer-reviewed** journal article (Crossref `type: journal-article`, MDPI), dated 1 Nov 2023 —
   squarely inside 2023–2026.
2. **Genuinely open access** under CC BY 4.0 (`license: https://creativecommons.org/licenses/by/4.0/`), and the
   full PDF was actually downloaded and read in this session (10 pages of PDF, 17 pages of journal pagination).
3. **Directly on-topic and technically detailed**: it is *multipath transport* (MPTCP) + *AI/ML/DRL*
   (multi-agent deep deterministic policy gradient) + *scheduling*, i.e. it hits all four elements requested.
4. It reports the apparatus a literature review needs: explicit MDP state/action/reward formulation, full
   hyperparameter table, an explicit baseline list (Round Robin, eMPTCP, EE-MPTCP, DMPTCP, ReLes), and a
   percentage-improvement comparison table — so extraction can be concrete instead of `NOT REPORTED`.
5. **Heterogeneous wireless access** (4G + WiFi with differing RTT/loss/bandwidth) is directly relevant to the
   5G/6G multi-access context, even though the paper is not 5G-core-specific (I state this limitation below
   rather than overclaiming).

### 4A. Energy-Aware MPTCP Scheduling in Heterogeneous Wireless Networks Using Multi-Agent Deep Reinforcement Learning Techniques
- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors: Zulfiqar Ali Arain, Xuesong Qiu, Changqiao Xu, Mu Wang, Mussadiq Abdul Rahim.
  - Year: 2023 (received 13 September 2023; revised 16 October 2023; accepted 23 October 2023;
    published 1 November 2023).
  - Venue: **Electronics** (MDPI), vol. 12, no. 21, article 4496, 17 pages.
  - DOI: **10.3390/electronics12214496** (Crossref-verified; `type: journal-article`; publisher MDPI AG;
    CC BY 4.0).
  - **Peer-reviewed** journal article, **open access (gold)**.
- **1. Number and type of paths** — **Two heterogeneous wireless paths**, one 4G and one WiFi, modelled with
  different characteristics. From Table 1 ("MPTCP environment class parameters"): 4G RTT 100–200 ms, 4G loss
  rate 0–0.5, 4G bandwidth 15–20 Mbps; WiFi RTT 40–60 ms, WiFi loss rate 0–1, WiFi bandwidth 5–10 Mbps.
  Number of agents is stated as 2 in Table 2 and "an agent is designed for every MPTCP sub-flow".
  Heterogeneous (cellular + WLAN), not homogeneous.
- **2. Network architecture** — End-to-end multipath between a sender and a receiver spanning heterogeneous
  wireless links: "[t]his environment, as shown in Table 1, comprises multiple wireless links, each with
  distinct characteristics such as bandwidth, delay, and packet loss rate." Each agent "represents a sender or
  receiver" in the formal model. **No proxy, no middlebox, no MPTCP-capable server, and no 5G core** is
  described — this is a plain end-to-end MPTCP deployment. The MPTCP environment "accurately models the
  heterogeneous wireless network" and a dataset for training is "collected through simulations conducted within
  this environment".
- **3. Transport protocol** — **MPTCP** ("Multi-path TCP (MPTCP) [8], a backward-compatible extension to TCP").
  Version (v0/v1) is not stated. It is MPTCP, **not** MPQUIC and **not** ATSSS. The paper notes MPTCP's
  coupling: "in the realm of heterogeneous networks ..., where packets are multiplexed across multiple paths
  with noticeable delay variations, such as WiFi and LTE, improper scheduling decisions can lead to significant
  performance degradation."
- **4. Scheduler location** — **End-host (sender) side, per-subflow, with a multi-agent controller.** "An agent
  is designed for every MPTCP sub-flow to manage its scheduling and resource allocation." Training is
  centralised and execution decentralised: "The agents undergo a centralized training process utilizing a
  specific dataset. Throughout this training phase, the agents foster cooperation by exchanging information via
  their critic networks. This interaction facilitates the learning of decentralized policies ... Each agent
  then makes scheduling decisions grounded solely on its unique policy and local observations." No core-network,
  RAN, proxy or userspace-vs-kernel placement is stated beyond this.
- **5. Scheduler inputs** — The MDP state is explicit: `s_i = [u_i, c_i, d_i, b_i]` "where u_i is the link
  utilization, c_i is the congestion status, d_i is the delay, and b_i is the buffer occupancy for agent i."
  The prose form is: "[t]he state space represents the network parameters relevant to MPTCP operations, such as
  link utilization, congestion status, delay, and buffer occupancy." So the input vector is
  **link utilisation, congestion status, delay, buffer occupancy**. (No SRTT/cwnd/delivery-rate/BLEST-style
  penalisation vocabulary is used.)
- **6. Path metrics used** — **Link utilisation, congestion status, delay, buffer occupancy** (state); and the
  reward aggregates **energy efficiency E(s,a), QoS Q(s,a), and network performance P(s,a)**. Packet loss rate
  and RTT are used as environment parameters (Table 1). The energy metric is expressed in "Joules per second"
  in the results section.
- **7. Scheduling decision (exact action space)** — Explicitly a **continuous vector per agent**:
  `a_i = [r_i, p_i, f_i, α_i]` — "where r_i is the sending rate, p_i is the path selection, f_i is the sub-flow
  management, and α_i is the congestion control parameter." The prose: "The action space (A): It consists of
  actions that each agent can perform to influence the MPTCP operations. These actions may include adjusting
  the sending rate, selecting paths, managing sub-flows, and modifying congestion control parameters."
  Note this is a **composite/continuous control action** (rate + path + subflow + CC parameter), not a discrete
  per-segment path index and not a simple steering percentage.
- **8. Packet-level or flow-level scheduling** — **Neither a per-segment packet scheduler nor a pure flow-level
  path selector.** The action is a per-subflow *rate/path/subflow/CC-parameter* control vector
  (`a_i = [r_i, p_i, f_i, α_i]`), i.e. **subflow-level resource-allocation control**. The paper deliberately
  frames MPTCP scheduling as "a decision-making problem" and as "path coordination" rather than packet
  assignment: "MADDPG ... for the MPTCP path coordination problem". I report this explicitly because it is
  *not* packet-level scheduling in the Peekaboo/BLEST/ECF sense.
- **9. Reordering handling** — Reordering is treated as an **indirect, motivation-level** concern, not a signal
  in the state or a penalty term in the reward. The mechanism described is head-of-line blocking: "One prominent
  issue is the head-of-line (HOL) [11] blocking phenomenon, where packets scheduled on low-latency paths are
  forced to wait for those on high-latency paths to ensure in-order delivery. Additionally, accommodating
  out-of-order packets requires receivers to maintain a large queue for reorganizing packets." The energy
  argument follows from it: "[t]he extended waiting times and packet reordering lead to increased energy
  consumption due to protracted device usage and processing times." **There is no stated penalty term, no
  ATD/receive-buffer estimate, and no explicit reordering metric** — the reward is a weighted sum of energy,
  QoS and performance only. This is a genuine methodological gap.
- **10. Congestion-control interaction** — The scheduler **modifies congestion-control parameters directly**
  (`α_i` is one of the four action components), and the congestion window is an environment parameter
  (Table 1: "Congestion Window" with range [0, 10] for both 4G and WiFi) and is described among what the agent
  adapts ("as the agent adjusts network parameters such as congestion window size, delay, and packet loss").
  **However, no named CC algorithm is used or evaluated** — LIA, OLIA, wVegas, BALIA, BBR and Cubic are
  **never mentioned** in the paper. So the interaction mechanism is "the agent sets the CC parameter α_i as
  part of its action", with the coupled-CC algorithm itself unidentified. Related work does cite SmartCC
  (RL for MPTCP CC) and DeepCC (MARL CC) as prior art.
- **11. Objective** — Stated in the abstract: "aiming to **minimize energy consumption while ensuring low
  latency and high throughput**." The paper also states the study's objective as "developing an
  energy-minimizing scheduling scheme for MPTCP using multi-agent DRL in heterogeneous wireless networks", and
  the reward formalisation is a weighted sum: `R_i(s_i, a_i) = w_E * E(s_i, a_i) + w_Q * Q(s_i, a_i) + w_P * P(s_i, a_i)`
  "where w_E, w_Q, and w_P are weights representing the importance of energy efficiency, QoS, and network
  performance objectives." The weights' numeric values are **not reported** (the reward is described as
  "[t]he formulation could be a weighted sum of energy consumption, delay, throughput, and packet loss metrics").
  Objective function: `J(π) = E[ Σ_{t=0}^{T} Σ_{i=1}^{N} γ^t * R(s_i^t, a_i^t) | π ]`.
- **12. Algorithm** — **MADDPG (Multi-Agent Deep Deterministic Policy Gradient)**, with the scheme named
  **EE-MADDPG**. Full training loop given as Algorithm 1: initialise actor `µ_i(s_i|θ^µ_i)` and critic
  `Q_i(s_i, a_1, …, a_N | θ^Q_i)` per agent plus target networks; replay buffer `B`; per time step each agent
  acts with exploration noise `a_i(t) = µ_i(s_i(t)|θ^µ_i) + N(t)`; critic updated by minimising
  `L(θ^Q_i) = (1/B) Σ_j (y_j − Q_i(s_j, a_j; θ^Q_i))^2` with `y_j = r_j + γ Q'_i(s_{j+1}, π'_i(s_{j+1}|θ'^π_i); θ'^Q_i)`;
  actor updated by the deterministic policy gradient
  `∇_{θ^π_i} J = (1/B) Σ_j ∇_a Q_i(s_j, a; θ^Q_i)|_{a=π_i(s_j)} ∇_{θ^π_i} π_i(a|s_j; θ^π_i)`;
  target networks soft-updated with `θ' = τθ + (1−τ)θ'`. The paper justifies MADDPG over alternatives on five
  grounds (scalability, continuous action spaces, policy-based method, stability/convergence, multi-agent
  coordination) and adapts it "to specifically address the unique challenges and requirements of MPTCP".
- **13. ML/DRL usage** — **Yes, and fully specified.** Variant: **MADDPG** (actor–critic, deterministic policy
  gradient, centralised training with decentralised execution). Network architecture, from Table 2
  ("MADDPG agent implementation hyper-parameters (sample)"): **Number of agents 2; Actor learning rate 0.001;
  Critic learning rate 0.01; Discount factor 0.99; Target network update rate 0.001; Replay buffer size
  100,000; Batch size 128; Number of hidden layers 2; Hidden layer size 128.** (Note: the actor and critic
  learning rates and the target update rate are given, but an activation function, optimiser, or per-layer
  topology is not stated.)
- **14. Simulator / testbed** — **Simulation.** The paper says: "A dataset is subsequently collected through
  simulations conducted within this environment" and "[t]he proposed energy-efficient Multi-Agent Deep
  Deterministic Policy Gradient (EE-MADDPG) scheme was subjected to a series of evaluations through
  simulations." Results are reported over "1000 episodes" / "1000 training steps". **Crucially, the paper never
  names the simulator** (no ns-3, no Mininet, no OMNeT++, no Linux kernel testbed, no real WiFi+LTE hardware).
  It refers to "an MPTCP environment that accurately models the heterogeneous wireless network" and to an
  "MPTCP environment class" with parameters in Table 1. This is **simulation, not a testbed, and not an
  emulation** — and the simulator identity is `NOT REPORTED`. Reward/loss curves are plotted vs. training steps
  (Figures 1, 2, 3, 4, 5).
- **15. Traffic model** — `NOT REPORTED` explicitly. The paper speaks of "data transmission", "packets",
  "traffic load" (as a parameter whose impact is to be examined) and "network size", but names no application
  traffic class (no bulk transfer, web, or video workload is specified). The data is described as a dataset
  collected from simulations. Baseline descriptions imply bulk/aggregate transfer (throughput, delay, energy
  measured over 1000 episodes).
- **16. Baselines** — Named exactly as the paper names them: **"Default Round Robin (RR)"**, **"eMPTCP"**,
  **"EE-MPTCP"**, **"DMPTCP"**, and **"ReLes"**. Their descriptions in the paper: RR "distributes data evenly
  across all sub-flows"; eMPTCP "selects the path (WiFi or LTE) with superior energy efficiency for data
  transmission"; EE-MPTCP "optimizes the utilization of available network interfaces in wireless sensors and
  robots to maximize throughput while minimizing energy consumption"; DMPTCP "estimates the available
  bandwidths of paths and prioritizes data transmission on the path with more available bandwidth"; ReLes
  "employs an LSTM neural network model to determine the split ratio for each sub-flow based on historical
  observations."
- **17. Metrics** — **Throughput** (Mbps), **delay** (ms), **energy consumption** (Joules per second), plus
  **loss function** convergence for each agent. Scalability is also named as an evaluated aspect
  ("energy efficiency, network throughput, latency, and scalability").
- **18. Main result** — Exact figures, quoted from Table 3 ("Comparison of algorithms: throughput, delay, and
  energy consumption improvements", all relative to Round Robin, which is the 0.000000 row):
  - **EE-MADDPG: Throughput +239.571282%, Delay −70.327133%, Energy Consumption −62.109398%** (negative = reduction).
  - EE-MPTCP: +198.793723%, −63.679567%, −49.735080%.
  - RELES: +146.105111%, −48.632261%, −37.386715%.
  - DMPTCP: +93.496327%, −40.201063%, −24.852117%.
  - EMTCP: +52.672159%, −19.297768%, −12.515934%.
  The paper's own summary, quoted: "EE-MADDPG has the highest throughput improvements compared to Round Robin
  (239.57%)"; "EE-MADDPG has the lowest delay percentage (best improvement) compared to Round Robin
  (−70.33%)"; "EE-MADDPG has the lowest energy consumption percentage (best improvement) compared to Round
  Robin (−62.11%)." (These three in-text figures are the paper's own rounded restatements of the Table 3 values
  above; the unrounded Table 3 values are 239.571282 / −70.327133 / −62.109398.) Also: "[t]he simulation results clearly illustrate that the proposed EE-MADDPG scheduling
  scheme achieves substantially lower energy consumption compared to other baseline schemes, while maintaining
  comparable throughput and delay performance." Figures 2–4 report the per-episode curves over **1000 episodes**,
  with EE-MADDPG "consistently" highest throughput, lowest delay and lowest energy.
- **19. Limitation** — As stated by the authors, only a forward-looking one: "For future work, we could refine
  the algorithm to learn policies that are more resilient to dynamic network conditions, including time-varying
  link capacities, delays, and packet loss rates. This would make the scheduling policies more suitable for
  real-world wireless networks." The authors also concede on algorithm choice: "they acknowledge that other
  multi-agent reinforcement learning methods could also be applicable and may be explored in future work."
  Methodological limitations I observe directly in the text:
  (a) **The simulator is never named** — "simulations conducted within this environment" — which makes the
  energy model and the 239%/70%/62% numbers non-reproducible as published.
  (b) **The reward weights w_E, w_Q, w_P are never given numeric values**, and the reward is presented as a
  candidate formulation ("A possible formulation could be a weighted sum"), so the objective actually optimised
  cannot be pinned down.
  (c) **The action space is a continuous 4-tuple including "modifying congestion control parameters α_i", but no
  CC algorithm is named**, leaving the most safety-critical part of the action unspecified.
  (d) **Table 1's parameter values are ranges, not distributions**, and the "Loss Rate" rows are given as
  "[0, 0.5]" and "[0, 1]" — consistent with probabilities but never labelled with units.
  (e) **Only two agents / two paths are configured** (Table 2, "Number of agents 2") while "scalability" is
  claimed as an evaluated property; no larger-agent-count result appears in the text I retrieved.
  (f) **Reordering/HOL blocking is the paper's motivating problem but never enters the state, the reward, or
  the metrics** — the reported metrics are throughput, delay and energy only.
  (g) **No statistical treatment** (no confidence intervals, no repeats/variance) accompanies the single
  Table 3 percentage set.
  (h) It is a modelling study with no 5G core, no real hardware, and no traffic-class definition.
- **20. Research gap this suggests** — For an AI-native network-management review, this paper is a good
  illustration of three gaps: (i) **reproducibility** — a DRL scheduler reporting large triple-digit gains
  without naming its simulator or publishing its environment; (ii) **reordering-blind optimisation** — HOL
  blocking motivates the work but is absent from state/reward/metrics, so "energy-efficient" is asserted
  without an explicit delay-penalty mechanism; (iii) **no management-plane integration** — the agents are
  per-subflow end-host controllers with no northbound interface to an SDN controller, orchestrator, or 5G core,
  which is exactly the integration this literature review is probing (see the gap-evidence probe below).
- **21. Best URL actually retrieved, and whether full text or abstract** —
  `https://mdpi-res.com/d_attachment/electronics/electronics-12-04496/article_deploy/electronics-12-04496.pdf`
  (the MDPI PDF asset host; `https://www.mdpi.com/2079-9292/12/21/4496/pdf` returned an HTML interstitial of
  6,198 bytes to `curl`, so the `mdpi-res.com` asset URL is what actually served the PDF) — **FULL TEXT**
  (627,982-byte PDF, 10 PDF pages / 17 journal pages, converted with `pdftotext -layout` to
  `pdfs/modern_2023plus.txt`, 941 lines). Landing page: `https://www.mdpi.com/2079-9292/12/21/4496`.
  Metadata verified at `https://api.crossref.org/works/10.3390/electronics12214496`.

### 4B. (Secondary pick, also read in full) LiveStream Meta-DAMS: Multipath Scheduler Using Hybrid Meta Reinforcement Learning for Live Video Streaming
I extracted this second paper because it is a 2025 peer-reviewed journal article whose full text I could
actually read, and it covers the **packet-level scheduling + MPQUIC + 5G/4G/WLAN heterogeneity** axis that the
Arain paper does not. It is reported as a **secondary** pick rather than the primary one because the author copy
is the pre-publication accepted version and the application is live video rather than 5G/6G access management.

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors: Amir Sepahi, Lin Cai, Wenjun Yang, Jianping Pan.
  - Year: Crossref `issued: [[2025, 8]]`; the retrieved author copy is watermark-dated "© 2024 IEEE" and
    "Downloaded on November 23, 2024" and is headed "This article has been accepted for publication in IEEE
    Transactions on Cognitive Communications and Networking. This is the author's version which has not been
    fully edited and content may change prior to final publication."
  - Venue: **IEEE Transactions on Cognitive Communications and Networking (TCCN)**, vol. 11, no. 4,
    pp. 2739–2754.
  - DOI: **10.1109/TCCN.2024.3502512** (the DOI itself is the 2024 acceptance DOI; Crossref issued date 2025).
  - **Peer-reviewed** journal article. **Source-disagreement disclosure (spec rule 8):** Crossref says
    `issued: [[2025, 8]]` with vol. 11 no. 4 pp. 2739–2754, while the PDF I read is the **accepted author
    version dated 2024**. I report both and trust the Crossref issue record (2025, TCCN 11(4)) for citation
    purposes, while noting that all quantitative content below comes from the 2024 accepted manuscript.
- **1. Number and type of paths** — **Two heterogeneous access paths** in the emulated topology (Fig. 10,
  "Simulation Topology"): "the client and server are connected using two access links, i.e., WiFi and 4G/5G".
  Table I ("Simulation Parameters", Path Parameters) gives three path profiles: **5G** BW 1100 Mbps, RTT 27 ms,
  jitter ±7 ms, loss 0.1%; **4G** BW 140 Mbps, RTT 30 ms, jitter ±5 ms, loss 0.1%; **WLAN** BW 30 Mbps,
  RTT 20 ms, jitter ±10 ms, loss 0.7%. Evaluated combinations are WLAN/4G and WLAN/5G.
- **2. Network architecture** — **Client–server multipath over MPQUIC via a CDN/origin server**: "IPB frames
  from the requested video ... are stored on an origin server. In order to stream the video, the client device
  sends an HTTP request to a Content Delivery Network (CDN), which responds by sending the appropriate video
  chunks." "The streaming server uses an MPQUIC scheduler to determine [the distribution of packets across
  diverse network paths]." No proxy, middlebox, or 5G core element is used. End-to-end MPQUIC.
- **3. Transport protocol** — **MPQUIC (multipath QUIC)**, explicitly chosen over MPTCP: "We use MPQUIC instead
  of MPTCP because it provides superior multipath performance over UDP, resulting in smoother video delivery,
  lower latency, and higher throughput ... Moreover, MPQUIC's flexibility in scheduler implementation allows
  fine-tuning for optimal video content delivery." Implementation: "The MPQUIC implementation in this study is
  based on the QUIC implementation within **mpquic-go**."
- **4. Scheduler location** — **Sender (streaming server) side, in the MPQUIC scheduler**, implemented in Go
  via `mpquic-go`: "The streaming server uses an MPQUIC scheduler"; "we implement LSMeta-DAMS using mpquic-go".
  The scheduler "updates its scheduling policy" per scheduling interval. No kernel/userspace split is stated
  beyond the mpquic-go userspace implementation. No core-network or RAN placement.
- **5. Scheduler inputs** — The state is a **per-subflow tuple vector** `s_t = (s_{t,1}, …, s_{t,n})` with
  `s_{t,i} = (T_{t,i}, swnd_{t,i}, Inf_{t,i}, w_{t,i}, τ_{t,i}, l_{t,i})`, where the paper defines: "T_{t,i} is
  the subflow throughput measurement; swnd_{t,i} is the maximum amount of unacknowledged data that a sender can
  have in-flight; Inf_{t,i} is the number of unacked packets; w_{t,i} is the average congestion window sizes;
  τ_{t,i} is the subflow mean RTT; l_{t,i} is the packet loss of the subflow." The paper also lists these in
  prose: "T_{t,i} is the subflow throughput measurement; swnd_{t,i} ...; l_{t,i} is the packet loss of the
  subflow." So: **throughput, send window (unacked in-flight data), number of unacked packets, average cwnd,
  mean RTT, loss rate** — six signals per subflow. This is the richest input set among the papers in this file.
  Application-layer signals are also used: frame type (I/P/B), GOP, SVC layers, and MPEG-DASH chunk state.
- **6. Path metrics used** — Throughput `T_{t,i}`, mean RTT `τ_{t,i}`, packet loss `l_{t,i}`, send window
  `swnd_{t,i}`, unacked-packet count `Inf_{t,i}`, average cwnd `w_{t,i}`; plus jitter and RTT in the emulation
  configuration (Table I), and delay as the quantity whose guarantee is targeted. Video metrics used for
  evaluation (not as scheduler inputs): download/completion time, stalling time, PSNR, SSIM, VMAF.
- **7. Scheduling decision (exact action space)** — **Discrete path selection, one action per scheduling
  policy deployment:** "The action space in our scenario is discrete and its size is determined by the
  available paths (A = {a_0, …, a_i, …, a_P}). Each time LSMeta-DAMS deploys a scheduling policy, it can choose
  from this set of actions, and for each action it receives a reward. Each scheduling policy is executed for a
  specific amount of time (T), where T = min{τ_0, …, τ_i, …, τ_P}." So the action is a **per-subflow /
  per-interval path choice**, and the policy is held for one min-RTT interval (not per-packet re-decision).
  Frame-type prioritisation is layered on top: the scheduler "prioritize[s] I-frame packets over P- and B-frame
  packets", and the reward drives "the path that ensures the [timely delivery of frames]".
- **8. Packet-level or flow-level scheduling** — **Packet-level scheduling, with a frame/chunk-aware twist.**
  The scheduler is described as a "multipath **packet** scheduler" and "the MP scheduler is responsible for
  distributing packets across diverse network paths"; the reward contains a frame-level term `R_f` where
  "the action chosen for the n-th packet and ts_n is its sending time" and a chunk-level term `R_c`. So it
  operates at packet/subflow granularity with prioritisation by video frame type — genuinely packet-level, in
  contrast to the Arain paper's subflow-level control vector.
- **9. Reordering handling** — Out-of-order arrival is the paper's central motivation and is handled through an
  explicit delay-aware reward plus a reordering-cost mechanism. Verbatim: "One of the main reasons for this
  problem is out-of-order (OFO) packets. Specifically, if data packets arrive in a different order than
  intended, packets with higher sequence numbers must remain unprocessed in the receiver's buffer until lower
  sequence number packets arrive." The contribution bullet reads verbatim: "[To schedule packets] to different
  frame types on the path that ensures the earliest delivery to the client. **This minimizes the packet
  reordering cost.** We also implement a mechanism to prioritize I-frame packets over P- and B-frame packets.
  We incorporate a video chunk manager and a video frame manager into LSMeta-DAMS's framework to ensure it can
  determine the reception of each frame and each chunk." So reordering is addressed **indirectly** — by picking
  the path that yields earliest delivery, which "minimizes the packet reordering cost" — rather than via an
  explicit closed-form reordering penalty in the state or reward. The reward is frame-level and chunk-level
  (`R_f` with `Pf_I` defined as "the penalty for delayed or lost I-frames", and `R_c = C_max / C_download`), and
  the design is "Delay Aware" (DAMS = Delay Aware Multipath Scheduler), with the policy interval bounded by
  `T = min{τ_0, …, τ_P}`. A specific reordering-penalty formula is not recoverable from the two-column text.
- **10. Congestion-control interaction** — The scheduler **observes** CC state (`w_{t,i}` average cwnd,
  `swnd_{t,i}` send window) but does **not** control it; there is no coupling or joint optimisation. This is
  stated as an explicit future direction: "Firstly, we propose developing a coupled congestion control algorithm
  tailored for the multipath scheduler, aiming to synchronize congestion control mechanisms and optimize MP
  video streaming performance." No named CC algorithm (LIA/OLIA/Cubic/BBR) is given for the mpquic-go runs.
- **11. Objective** — Stated in the abstract: "a novel learning-based multipath scheduler explicitly designed
  for live streaming applications", with "Delay Aware" in the name and the index terms "Meta reinforcement
  learning, multipath scheduler, live video streaming, delay guarantee". The evaluation objectives are stated
  as: "our framework, which aim to minimize stalling time, optimize video quality, and maintain smooth
  playback." Frame-type priority is an explicit sub-objective: "the scheduler's primary [goal] ... to
  prioritize I-frame packets over P- and B-frame packets" (contribution bullet: "To ... prioritize I-frame
  packets over P- and B-frame packets").
- **12. Algorithm** — **Hybrid meta-reinforcement learning** combining online and offline phases, with the
  online learner named **MA3C** ("an enhanced asynchronous training algorithm based on A3C"): "LSMeta-DAMS
  employs a hybrid meta-reinforcement learning architecture, incorporating both online and offline phases to
  enhance speed and accuracy for training and decision making", and "we introduce a training algorithm built on
  top of the asynchronous advantage actor-critic (A3C) [14], which is faster and more accurate than Deep
  Q-Networks (DQN) widely used in other MP-schedulers." MA3C differs from A3C in two ways: "the proposed MA3C
  changes the optimization method used in A3C and incorporates a Long Short-Term Memory (LSTM) model into the
  design" — specifically "While RMSProp [38] is employed in the original A3C design, MA3C utilizes the Adam
  optimizer [39] instead of RMSProp." Offline phase: "Pretrained meta-models in the offline phase enhance both
  the learning process speed and the accuracy of the online learning phase."
- **13. ML/DRL usage** — **Yes, and specified.** Variant: **MA3C = A3C + Adam + LSTM**, wrapped in a **hybrid
  meta-RL** architecture with offline meta-model pretraining and online adaptation. Architecture elements:
  LSTM units process sequences of input states ("Fig. 9: LSTM integration in MA3C algorithm"; "LSTM excels in
  capturing temporal dependencies, facilitating sequential decision-making by the MA3C agent"); multiple
  parallel workers ("we consider LSMeta-DAMS with four workers in these comparisons"). Hyperparameters
  (Table II): **Discounted Factor γ = 0.99; Learning Rate α = 0.001; ϵ_max = 1; ϵ_min = 0.01; ϵ_decay = 0.98.**
  Hidden-layer sizes and neuron counts are not given in Table II.
- **14. Simulator / testbed** — **Emulation (trace-driven), not a simulation and not a real testbed, and it is
  named.** Quoted: "In our emulated experiments, we use network traces ... **Mininet** is utilized to emulate
  the environment". Implementation stack: "Practical implementation and trace-driven emulations using
  **mpquic-go, TensorFlow, and keras-rl** validate LSMeta-DAMS's effectiveness". Path characteristics come from
  Table I (5G/4G/WLAN BW, RTT, jitter, loss). Topology from Fig. 10: client — {4G, 5G, WLAN} — server. This is
  an **emulation with Mininet + mpquic-go**, which is distinct both from ns-3-style simulation and from a
  hardware testbed.
- **15. Traffic model** — **Live video streaming over MPEG-DASH**, with **scalable video coding (SVC)** and a
  GOP structure: "Prioritizing packet scheduling based on frame types and considering the video coding features
  like group of pictures (GOP), scalable video coding (SVC), and Dynamic Adaptive Streaming over HTTP
  (MPEG-DASH)". Traffic is chunk/segment-based HTTP streaming; frame types I, P, B; multiple bitrates/layers.
  A synthetic trace envelope is also described for evaluation: "loss rates can range between [0, 0.5)%,
  [0.5, 0.75)%, and [0.75, 1)%; the mean RTT can be between [0, 50) ms, [50, 100) ms, and [100, 200] ms; and
  the ratio between deviations and mean RTTs can be [0, 10)%, [10, 30)%, and [30, 50]%."
- **16. Baselines** — Named exactly as the paper names them, split into non-learning and learning groups:
  "minRTT and RR are the non-learning or model-based algorithms, while LSMeta-DAMS, DAMS, Meta-DQN, DQN, ReLes,
  and Peekaboo are the learning-based schedulers for comparison." Also in the related work: "minRTT prioritizes
  subflows with minimum RTTs, while RR cyclically distributes packets among available paths"; "BLEST and ECF
  implement sophisticated algorithms based [on blocking estimation / earliest completion first]"; and the
  paper develops its own ablations — "we develop DAMS and DQN to analyze the behavior of the scheduler" and
  "Meta-DQN based on our hybrid meta-RL architecture to observe how our MP scheduler performs when using DQN
  instead of MA3C in our design." Implementation note: "minRTT, RR, ReLes, and Peekaboo are algorithms proposed
  based on MPTCP. We modified them for our application, specifically adapting them to the MPQUIC framework."
- **17. Metrics** — **Learning/convergence score** (Fig. 13), **download (completion) time**, normalised
  against minRTT ("we use a regularized or normalized completion time, defined as the ratio of the actual
  completion time to the baseline completion time of a reference scheduler (minRTT in this case)"),
  **total stalling time** (CDF over "100 experiments" per scheduler), and **video quality assessment** via
  **PSNR, SSIM and VMAF** (PSNR acceptable range "from 30 dB to 50 dB"; SSIM "values exceeding 0.9 are often
  considered acceptable"; VMAF "scores on a 0 to 100 scale").
- **18. Main result** — Exact figures quoted from the abstract: "up to **32% improvement in learning**, up to
  **25% reduction in download time**, up to **15% enhancement in video quality assessment**, and up to **35%
  reduction in stalling time** compared to the state-of-the-art multipath schedulers." Body text adds, on
  download time: "In Fig. 14a, where WLAN and 4G are used as network paths, LSMeta-DAMS demonstrates an
  approximate **30% increase in download speeds compared to minRTT**. Furthermore, when considering WLAN and 5G
  as network paths, LSMeta-DAMS exhibits a **38% improvement in download performance compared to minRTT**."
  And: "LSMeta-DAMS exhibits the least stalling time compared to other MP schedulers in both scenarios." On
  learning speed, the paper states as a **property of A3C cited from reference [14], not as a measured result
  of this work**: "A3C can be trained two times faster than DQN, even if a multi-core CPU is used rather than a
  GPU [14]." I flag this explicitly: **the "2× faster than DQN" figure is a cited claim, not a number LSMeta-DAMS
  measured.** The abstract's "up to 32% improvement in learning" is the authors' own reported figure.
  Worker scaling: "an increase in the number of workers in LSMeta-DAMS's learning algorithm MA3C corresponds to
  a reduction in completion time."
- **19. Limitation** — As stated by the authors, two future directions: "Firstly, we propose developing a coupled
  congestion control algorithm tailored for the multipath scheduler, aiming to synchronize congestion control
  mechanisms and optimize MP video streaming performance. Secondly, we envision creating a dedicated multipath
  dynamic adaptive streaming over HTTP [mechanism]". The paper also concedes on metrics: "widely employed
  metrics such as PSNR and SSIM, despite their ease of calculation, fall short in capturing the subjective
  perceptions of the human eye. As a result, they offer limited practical value in real-world applications."
  Methodological limitations I observe: (a) **evaluation is Mininet emulation with synthetic/trace-driven paths**,
  not a real 4G/5G network — the 5G path (1100 Mbps, 27 ms) is a configured profile, not a measurement;
  (b) **no congestion-control coupling**, which the authors themselves flag as future work, so scheduler gains
  are entangled with an unspecified CC; (c) **two-path configurations only** (WLAN+LTE, WLAN+5G), so
  multi-path (>2) scaling is untested; (d) the evidence for the "38%" and "30%" download gains is read from
  normalised CDFs in figures rather than reported as a table with dispersion; (e) the copy I read is the
  **accepted author version** (2024) rather than the final 2025 TCCN typeset article, so figure/table numbering
  may differ from the published version; (f) it is **video-streaming-specific** — the frame/chunk reward design
  does not transfer to bulk or transactional traffic.
- **20. Research gap this suggests** — This is the strongest packet-level scheduling design in this file, and
  its gaps are precisely the ones relevant to AI-native network management: the agent lives entirely at the
  **endpoint** (streaming server, mpquic-go userspace), consumes only per-subflow transport signals, has **no
  network-side observability** (no RAN/core telemetry), and takes no input from any orchestrator. It observes
  cwnd but does not co-design congestion control. So even the best-in-class learning scheduler here is an
  **isolated endpoint agent** — which is the gap the probe below confirms.
- **21. Best URL actually retrieved, and whether full text or abstract** —
  `https://www.ece.uvic.ca/~cai/tccn24-meta-dams.pdf` (University of Victoria author copy;
  `HTTP 200`, `application/pdf`, 3,976,091 bytes, 15 PDF pages) — **FULL TEXT** (converted to
  `pdfs/metadams_tccn.txt`, 1,099 lines). Landing/metadata verified at
  `https://api.crossref.org/works/10.1109/TCCN.2024.3502512`; Unpaywall
  `https://api.unpaywall.org/v2/10.1109/tccn.2024.3502512?email=research@example.org` reports
  `is_oa: false` for the publisher version, i.e. the full text came from the authors' own repository copy,
  which is the accepted manuscript.

---

## Summary table of the four assigned deliverables

| # | Paper (verified title) | Venue / Year | DOI | Retrieved |
|---|---|---|---|---|
| 1 | Deep Reinforcement Learning for Access Traffic Splitting in 5G Core System | IEEE ICTC 2024, pp. 903–908 | 10.1109/ICTC62082.2024.10826899 | **ABSTRACT ONLY** |
| 2 | Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective Reinforcement Learning | IEEE ICCCN 2025, pp. 1–8 | 10.1109/ICCCN65249.2025.11133925 | **ABSTRACT ONLY** |
| 3 | **Multipath** TCP Meets Reinforcement Learning: A Novel Energy-Efficient Scheduling Approach in Heterogeneous Wireless Networks *(assigned as "MPTCP Meets…"; same paper)* | IEEE Wireless Communications 30(2):138–146, 2023 | 10.1109/MWC.013.2100658 | **ABSTRACT ONLY** |
| 4A | Energy-Aware MPTCP Scheduling in Heterogeneous Wireless Networks Using Multi-Agent Deep Reinforcement Learning Techniques | Electronics (MDPI) 12(21):4496, 2023 | 10.3390/electronics12214496 | **FULL TEXT** |
| 4B | LiveStream Meta-DAMS: Multipath Scheduler Using Hybrid Meta Reinforcement Learning for Live Video Streaming *(secondary pick, also read)* | IEEE TCCN 11(4):2739–2754, 2025 (accepted author version dated 2024) | 10.1109/TCCN.2024.3502512 | **FULL TEXT** (author copy) |
| — | A Survey on Multipath Transport Protocols Towards 5G Access Traffic Steering, Switching and Splitting *(probe reference, §c)* | IEEE Access 9:164417–164439, 2021 | 10.1109/ACCESS.2021.3134261 | **FULL TEXT** (CC BY 4.0) |

### Every URL used for retrieval in this session
Metadata / verification APIs:
`https://api.crossref.org/works/10.1109/ictc62082.2024.10826899` ·
`https://api.crossref.org/works/10.1109/icccn65249.2025.11133925` ·
`https://api.crossref.org/works/10.1109/MWC.013.2100658` ·
`https://api.crossref.org/works/10.3390/electronics12214496` ·
`https://api.crossref.org/works/10.1016/j.iot.2025.101616` ·
`https://api.crossref.org/works/10.1109/TCCN.2024.3502512` ·
`https://api.crossref.org/works/10.1016/j.sciaf.2025.e03134` ·
`https://api.crossref.org/works/10.1109/ACCESS.2021.3134261` ·
`https://api.crossref.org/works/10.1109/iccworkshops63917.2026.11586241` ·
`https://api.crossref.org/works/10.1109/icc45041.2023.10278983` ·
`https://api.crossref.org/works/10.1109/ccnc51644.2023.10060026` ·
`https://api.crossref.org/works/10.52783/jisem.v10i62s.13781` ·
`https://api.crossref.org/works?query.bibliographic=<title>&rows=5` (repeatedly for the searches above) ·
`https://api.unpaywall.org/v2/10.1109/ictc62082.2024.10826899?email=research@example.org` ·
`https://api.unpaywall.org/v2/10.1109/icccn65249.2025.11133925?email=research@example.org` ·
`https://api.unpaywall.org/v2/10.1109/mwc.013.2100658?email=research@example.org` ·
`https://api.unpaywall.org/v2/10.1016/j.iot.2025.101616?email=research@example.org` ·
`https://api.unpaywall.org/v2/10.1109/tccn.2024.3502512?email=research@example.org` ·
`https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/MWC.013.2100658?fields=title,abstract,openAccessPdf,venue,year,externalIds` ·
`https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.sciaf.2025.e03134?fields=title,venue,year,externalIds,openAccessPdf` ·
`https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICTC62082.2024.10826899?fields=title,abstract,venue,year,publicationVenue,externalIds` ·
`https://api.openalex.org/works?search=...` — **FAILED, HTTP 429 out of daily budget**.

Document retrieval:
`https://r.jina.ai/https://ieeexplore.ieee.org/document/10826899` ·
`https://r.jina.ai/https://ieeexplore.ieee.org/document/11133925` ·
`https://r.jina.ai/https://ieeexplore.ieee.org/abstract/document/11133925` ·
`https://r.jina.ai/https://ieeexplore.ieee.org/document/9826510` ·
`https://r.jina.ai/https://ieeexplore.ieee.org/document/11586241` ·
`https://mdpi-res.com/d_attachment/electronics/electronics-12-04496/article_deploy/electronics-12-04496.pdf` ·
`https://www.mdpi.com/2079-9292/12/21/4496` ·
`https://www.ece.uvic.ca/~cai/tccn24-meta-dams.pdf` ·
`https://www.ietf.org/archive/id/draft-song-tsvwg-camp-00.html` ·
`https://datatracker.ietf.org/doc/html/draft-xing-quic-sdn-controller-aware-mptcp-mpquic-00` ·
`https://www.ietf.org/archive/id/draft-xing-nmop-sdn-controller-aware-mptcp-mpquic-03.html` ·
arXiv API: `http://export.arxiv.org/api/query?search_query=...` and `https://export.arxiv.org/api/query?id_list=2603.10357,2509.02124,2512.20186,2603.04550`
(with `https://export.arxiv.org/api/query?search_query=all:%22MPTCP%22+AND+all:%22reinforcement+learning%22`,
`all:"MPTCP" OR all:"multipath QUIC" OR all:"multipath transport"`,
`all:"LLM" AND all:"congestion control"`,
`all:"multipath" AND (all:"LLM" OR all:"large language model")`).
Standards: `https://www.etsi.org/deliver/etsi_ts/123500_123599/123501/18.07.00_60/ts_123501v180700p.pdf` ·
`https://www.3gpp.org/FTP/tsg_sa/WG2_Arch/TSGS2_163_Jeju_2024-05/INBOX/DRAFTS/R19%20FS_MASSS/draft_23700-54-040_rm.docx`.

Local artefacts written (assigned pdf dir): `pdfs/modern_2023plus.pdf` + `pdfs/modern_2023plus.txt`,
`pdfs/metadams_tccn.pdf` + `pdfs/metadams_tccn.txt`.

---

## Gap-evidence probe

Method notes: searches were run with the `web_search` tool (which surfaces indexed paper landing pages) and with
the **arXiv API** (`https://export.arxiv.org/api/query?search_query=...`) and **Crossref**
(`https://api.crossref.org/works?query.bibliographic=...`) for verification. OpenAlex was unavailable
(daily budget exhausted, HTTP 429). Every item below is a paper I actually saw in results; where I could not
find something, I say so explicitly and give the queries. **No absence is asserted without a listed query.**

### (a) Multipath scheduler + SDN controller / network orchestrator
**Searches run (exact queries):**
1. `multipath TCP SDN controller scheduling optimization MPTCP OpenFlow paper`
2. `SDN-based multipath QUIC scheduler network orchestrator`
3. `MPTCP SDN controller path selection reinforcement learning 2024`
4. Crossref: `MPS-OF-AS SDN-based MPQUIC scheduler software-defined cloud services`;
   `Load Balancing MPTCP Traffic Reactive SDN Multi-Agent Reinforcement Learning Alruwisan Yuksel`
5. arXiv: `all:"MPTCP" OR all:"multipath QUIC" OR all:"multipath transport"` (30 results scanned)

**What I FOUND (actual titles + venues + URLs):**
- **MPS-OF-AS: An SDN-based MPQUIC Scheduler for Software-Defined Cloud Services** — John S. Wejin,
  Adeyinka A. Adewale, Kennedy O. Okopkujie (author names exactly as registered in Crossref) —
  *Scientific African*, Elsevier; Crossref `issued: [[2026, 3]]` (also `published-print: [[2026, 3]]`),
  DOI **10.1016/j.sciaf.2025.e03134**, licence **CC BY-NC-ND 4.0** (so it is free to read; I verified the
  Crossref licence field but did not download the full text in this session). This is the closest match found:
  an **MPQUIC scheduler whose logic is placed in an SDN controller/OpenFlow context**. URL:
  https://www.sciencedirect.com/science/article/pii/S2468227625006039
- **Load Balancing MPTCP Traffic in Reactive SDN with Multi-Agent Reinforcement Learning** — Meshal Alruwisan,
  Murat Yuksel — **2026 IEEE International Conference on Communications Workshops (ICC Workshops)**, Glasgow,
  24–28 May 2026, DOI **10.1109/ICCWorkshops63917.2026.11586241**. This is **directly the (a) intersection plus
  RL**: two RL agents ("a FlowSatisfier that provides rapid responses to packet_in events to minimize the time
  needed to assign MPTCP subflows to existing paths, and a GHOST-MAPPO agent that dynamically reroutes
  congested subflows"), reporting "decreasing MLU by 16% and increasing MPTCP throughput by 97% even under
  light-load regimes" compared with "reactive SDN with shortest path first (SPF)". Retrieved as **abstract only**
  via `https://r.jina.ai/https://ieeexplore.ieee.org/document/11586241` (IEEE is paywalled; abstract fully
  readable, rest is free preview). URLs: https://ieeexplore.ieee.org/document/11586241 ·
  https://par.nsf.gov/biblio/10673132-load-balancing-mptcp-traffic-reactive-sdn-multi-agent-reinforcement-learning
- **Exploiting Path Diversity in Datacenters using MPTCP-aware SDN** — arXiv preprint **arXiv:1511.09295v2**
  (30 Nov 2015). Older and a preprint, but a genuine MPTCP × SDN datapath-control paper. URL:
  https://arxiv.org/abs/1511.09295
- **Mobility-Aware Seamless Handover with MPTCP in Software-Defined HetNets** — arXiv preprint
  **arXiv:2101.00678v1** (3 Jan 2021). "Using an SDN controller, HetNets have [programmability]" — an SDN
  controller driving MPTCP handover. URL: https://arxiv.org/abs/2101.00678
- **scMPTCP: SDN Cooperated Multipath Transfer for Satellite Network With Load Awareness** — IEEE Access
  (IEEE Xplore document 8327821), surfaced via search. SDN-cooperated MPTCP for satellite networks. URL:
  https://ieeexplore.ieee.org/document/8327821
- **The SDN-based MPTCP-aware and MPQUIC-aware Transmission Control Model** — IETF Internet-Draft,
  `draft-xing-nmop-sdn-controller-aware-mptcp-mpquic` (versions -00 through -04 seen). **Not peer-reviewed**;
  included because it is a standards-track artefact that names the exact integration. URLs:
  https://datatracker.ietf.org/doc/html/draft-xing-quic-sdn-controller-aware-mptcp-mpquic-00 ·
  https://www.ietf.org/archive/id/draft-xing-nmop-sdn-controller-aware-mptcp-mpquic-03.html

**What I did NOT find:** I did **not** find any paper in which a *packet-level* multipath scheduler (BLEST/ECF/
Peekaboo-class, per-segment path assignment) is **co-designed with, or whose policy is exported to, an SDN
controller or a network orchestrator**. All SDN-adjacent hits operate at **flow/subflow-to-path assignment or
routing** granularity (MPS-OF-AS, the ICC Workshops MARL paper, scMPTCP, MPTCP-aware SDN), or are IETF drafts.
I also did **not** find any work where an SDN controller's global view (topology, link utilisation, TE
objectives from an orchestrator) is an **input to a multipath scheduler's policy** — the SDN papers push
subflows onto paths; they do not feed network-wide state into a scheduler's decision function.

### (b) Multipath scheduler + LLM or AI agent
**Searches run (exact queries):**
1. `LLM large language model network scheduling multipath transport agent`
2. `LLM agent network management MPTCP scheduler`
3. `large language model 5G core network optimization agent paper 2025`
4. `LLM large language model multipath QUIC MPTCP scheduling transport layer agent 2026`
5. `LLM agent congestion control network research paper 2025 multipath`
6. arXiv: `all:"LLM" AND all:"congestion control"` (12 results scanned);
   `all:"multipath" AND (all:"LLM" OR all:"large language model")` (12 results scanned);
   `ti:"consistency-aware multipath"`

**What I FOUND (actual titles + venues + URLs):**
- **Consistency-Aware Multipath Transport (CAMP) toward Interactive Multimodal LLM-Based Systems** — IETF
  Internet-Draft `draft-song-tsvwg-camp-00` (TSVWG), March 2026. **Not peer-reviewed (IETF draft).** This is
  the single closest artefact to "multipath scheduler × LLM": it "specifies CAMP, a consistency-aware multipath
  transport design over the Multipath QUIC (MPQUIC) protocol" with "a transport-layer consistency-aware
  multipath scheduler to reduce inter-modal arrival time deviation across network paths", motivated by
  "interactive LLM-based services, such as digital humans". **The LLM here is the *application* being served,
  not the scheduler's decision-maker.** URL: https://www.ietf.org/archive/id/draft-song-tsvwg-camp-00.html
- **Utility Function is All You Need: LLM-based Congestion Control** — Neta Rozen-Schiff, Liron Schiff, Stefan
  Schmid — **arXiv preprint arXiv:2603.10357v1** (11 March 2026). **Preprint; no peer-reviewed venue found in
  Crossref.** LLM used to *generate/derive congestion-control logic* from a utility function — the
  "LLM as the CC agent" pattern, but for **single-path CC, not multipath scheduling**. URL:
  https://arxiv.org/abs/2603.10357
- **CCA Reimagined: An Exploratory Study of Large Language Models for Congestion Control** — **arXiv preprint
  arXiv:2604.03857v1** (4 April 2026). An "emulation-guided study" of "the feasibility of Large language model
  (LLM)-driven congestion control". **Preprint; no Crossref venue record found.** URL: https://arxiv.org/abs/2604.03857
- **Congestion Control System Optimization with Large Language Models** — **arXiv preprint arXiv:2508.16074v1**
  (22 August 2025). LLM-driven CC algorithm *design*. URL: https://arxiv.org/abs/2508.16074
- **Adapting Large Language Models for Improving TCP Fairness over WiFi** — **arXiv preprint arXiv:2412.18200v1**
  (24 December 2024). LLM → TCP (single path) CC. URL: https://arxiv.org/abs/2412.18200
- **FlexNGIA 2.0: Redesigning the Internet with Agentic AI — Protocols, Services, and Traffic Engineering
  Designed, Deployed, and Managed by AI** — Mohamed Faten Zhani, Younes Korbi, Yamen Mkadem —
  **arXiv:2509.02124v2** (2 September 2025). A vision paper on agentic AI managing protocols and traffic
  engineering; **not a multipath scheduler.** URL: https://arxiv.org/abs/2509.02124
- **Grounding Large Language Models as Generalizable Policies in Network Control** — **arXiv:2512.11839v2**
  (3 December 2025). LLM as a generalizable network-control policy — relevant to AI-native management but not
  multipath scheduling. URL: https://arxiv.org/abs/2512.11839
- **Large Language Model-driven 5G Network Optimization Assistant: A Practical Perspective** — 2025 IEEE
  International Conference on Big Data and Cloud Computing (BDCloud) — surfaced via search; LLM assistant for
  5G optimisation generally, not multipath scheduling. URL:
  https://www.computer.org/csdl/proceedings-article/bdcloud/2025/668200a069/2iPXNdlUJj2

**What I did NOT find:** **I found no peer-reviewed paper that integrates an LLM or an AI agent as the decision
policy of a multipath scheduler (MPTCP or MPQUIC), or with a 5G core ATSSS/UPF.** Concretely:
- No result where an LLM/agent is *the scheduler* or *the scheduler's policy generator*; every LLM hit is either
  (i) about **single-path congestion control** (LLM-based CC), (ii) a **vision/architecture paper** (FlexNGIA 2.0,
  Grounding LLMs), or (iii) a **non-peer-reviewed IETF draft** (CAMP) where the LLM is the *workload* being
  transported over multipath, not the controller. Query 4 and the two arXiv queries returned **zero** papers
  combining multipath scheduling with an LLM.
- No result integrating an "AI agent" (tool-using / orchestrating agent, as opposed to a DRL policy network)
  with an MPTCP/MPQUIC scheduler. The DRL schedulers found (papers 3, 4A, 4B above) are policy networks, not
  agents in the LLM/agentic sense.
- I could not verify any peer-reviewed venue for the LLM-CC papers: Crossref `query.bibliographic` for
  "Utility Function is All You Need LLM-based Congestion Control" returned only unrelated SSRN records, and for
  "CCA Reimagined…" returned only unrelated papers. They are therefore listed as **preprints**, not as
  peer-reviewed literature.

### (c) Multipath scheduler + 5G core ATSSS / UPF
**Searches run (exact queries):**
1. `ATSSS UPF 5G core machine learning traffic splitting implementation paper`
2. `5G ATSSS UPF machine learning traffic steering implementation open5gs free5gc scheduling paper`
3. `ATSSS multi-access PDU session UPF implementation testbed free5GC open5GS measurement study`
4. `5G core UPF traffic steering machine learning QoS scheduling research paper 2025`
5. `ATSSS UPF open source implementation Metis Linux eBPF multipath proxy 2024 2025`
6. `3GPP ATSSS PCF SMF N4 UPF steering mode implementation research testbed`

**What I FOUND (actual titles + venues + URLs):**
- **Deep Reinforcement Learning for Access Traffic Splitting in 5G Core System** — Pham et al. — IEEE ICTC 2024,
  DOI 10.1109/ICTC62082.2024.10826899. ATSSS + DRL **in the PCF**. URL:
  https://ieeexplore.ieee.org/document/10826899
- **Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective Reinforcement
  Learning** — Pham et al. — IEEE ICCCN 2025, DOI 10.1109/ICCCN65249.2025.11133925. ATSSS + MORL **in the 5GS
  control plane**. URL: https://ieeexplore.ieee.org/document/11133925
- **AI-Powered Dynamic Flow Steering in 5G Networks: RAN Analytics Integration with UPF for Enhanced QoS
  Management** — Binu Kiliamkavunkal Govindan — *Journal of Information Systems Engineering and Management*,
  Crossref `issued: [[2025, 11, 18]]`, DOI **10.52783/jisem.v10i62s.13781**. **AI + UPF steering** — but RAN
  analytics → UPF flow steering, *not* a multipath transport scheduler. URL:
  https://jisem-journal.com/index.php/journal/article/download/13781/6519/24898
- **Managing 5G Converged Core With Access Traffic Steering, Switching, and Splitting** — Toktam Mahmoodi et al.
  — book chapter, DOI 10.4018/978-1-7998-7708-0.ch025 (in *Research Anthology on Developing and Optimizing 5G
  Networks and the Impact on Society*, 2021). ATSSS architecture/management, not AI-driven scheduling. (Found via
  the first Crossref query for assigned paper 1; no AI/ML component.)
- **Hierarchical Reinforcement Learning Based Traffic Steering in Multi-RAT 5G Deployments** — Md Arafat Habib,
  Hao Zhou, Pedro Enrique Iturria-Rivera, Medhat Elsayed, Majid Bavand, Raimundas Gaigalas, Yigit Ozcan,
  Melike Erol-Kantarci — **ICC 2023 – IEEE International Conference on Communications**, DOI
  **10.1109/icc45041.2023.10278983**. RAN-level (not transport-level) traffic steering with HRL; the companion
  **Traffic Steering for 5G Multi-RAT Deployments using Deep Reinforcement Learning**, IEEE CCNC 2023,
  DOI **10.1109/ccnc51644.2023.10060026**, same group. URLs: https://arxiv.org/abs/2301.07818 (preprint
  **verified** to be the same paper via the arXiv API title lookup; also readable at
  https://ar5iv.labs.arxiv.org/html/2301.07818) · https://ieeexplore.ieee.org/document/10278983
- A paper surfaced as an ACM DL PDF that discusses UE connectivity "through non-3GPP access network" with TCP
  subflow measurements in a traffic-switching scenario (DOI prefix `10.1145/3609382`). I saw only fragments of
  this via search; **I did not retrieve or verify it, so I do not report it as a finding.**

**KEY ARCHITECTURE REFERENCE I DID FIND (and read in full — this reframes the gap):**
- **A Survey on Multipath Transport Protocols Towards 5G Access Traffic Steering, Switching and Splitting** —
  Hongjia Wu, Simone Ferlin, Giuseppe Caso, Özgü Alay, Anna Brunström — **IEEE Access**, vol. 9,
  pp. 164417–164439, 2021, DOI **10.1109/ACCESS.2021.3134261**, **CC BY 4.0 (gold OA)**. Retrieved and read as
  full text from `pdfs/atsss_survey_access2021.pdf` (a copy already present in the shared assignment `pdfs/`
  directory; Crossref-verified). This survey establishes the *standardised* architecture that the gap sits
  inside, quoted verbatim:
  - "As shown in Figure 5, the PCF controls ATSSS by delivering the policy rule to the SMF. The policy rule,
    shared by the SMF with the UE (uplink) or the UPF (downlink), contains the indication on which ATSSS
    steering function and steering mode to adopt."
  - "TS 23.501 defines two ways of implementing steering functionalities: a) the use of a multipath transport
    protocol, above the IP layer, and b) the use of a so-called ATSSS Lower Layer (ATSSS-LL), below the IP
    layer. In the case of multipath transport, as shown in Figure 5, **the UE and UPF communicate through the
    Multipath Transport Function (in the UE) and the Multipath Transport Proxy Function (in the UPF)**. In the
    case of ATSSS-LL, the UE and UPF communicate with each other via the combination of ATSSS-LL Function of
    the UE and UPF. In addition, **UPF supports Performance Measurement Functionality (PMF)**, that may be used
    by the MA PDU session to obtain access [performance measurements]."
  - The four standardised steering modes, quoted: "**Active-Standby**", "**Priority-based**", "**Smallest
    Delay**: The used access network is the one providing the shortest Round Trip Time (RTT)", and
    "**Load-balancing**: Each access network receives a percentage of the data of the MA-PDU session, depending
    on the assigned weight factor. If one access becomes unavailable, all traffic is sent to the other." Plus
    two TR 23.793 candidates: "**Best-Access**" and "**Redundant**". And: "**The above steering modes are all
    supported by MPTCP.**"
  - On ML/DRL in this space, quoted: "More recently, machine learning approaches (e.g., reinforcement or
    supervised learning, etc.) are used as ways to enable latency and/or throughput optimization in the same
    algorithm. Here, machine learning features can be derived from transport layer information such as RTT,
    CWND, inflight packets [63] [64] [65], etc." — and, as an open issue: "The advantage of data-driven
    solutions is that they have the potential to learn over different path conditions and accordingly adapt to
    them. **However, they may lack of explainability**, which might be even more severe in URLLC".
  This is a **survey**, not an ML-scheduler contribution: it *documents that the UPF/PMF anchor point exists and
  that the four steering modes are MPTCP-supported*, but it does **not** itself propose or evaluate an AI/ML
  scheduler in the UPF. That distinction is exactly the gap.

**Standards evidence (not peer-reviewed papers, but authoritative and found in this search):** the 3GPP
specification set confirms the UPF anchoring and shows that multipath **QUIC** in ATSSS is now an active
Release-19 study item: 3GPP **TS 23.501** defines MPTCP/MPQUIC/ATSSS-LL steering-mode configuration at the DNN
level and "the UPF performing translation on traffic associated with the 'MPTCP link-specific multipath'
addresses" (ETSI TS 123 501 V18.7.0, https://www.etsi.org/deliver/etsi_ts/123500_123599/123501/18.07.00_60/ts_123501v180700p.pdf),
and the Release-19 **FS_MASSS** study drafts state "After the MA PDU Session establishment, the UE creates one
or more multipath QUIC connections with the UPF"
(https://www.3gpp.org/FTP/tsg_sa/WG2_Arch/TSGS2_163_Jeju_2024-05/INBOX/DRAFTS/R19%20FS_MASSS/draft_23700-54-040_rm.docx).
I list these as **standards documents, not as peer-reviewed papers** — they tell us the interface exists in the
spec, not that a research contribution has exploited it.

**What I did NOT find:** **No paper that connects a multipath scheduler (MPTCP/MPQUIC packet scheduler) to a 5G
core ATSSS function or to the UPF data plane, other than the two Pham et al. ATSSS papers above — and those are
control-plane policy papers that never mention MPTCP, MPQUIC, the UPF, N4 or N6 in the retrievable text.**
Specifically:
- I found **no** paper reporting an ATSSS implementation on **free5GC or Open5GS** with a documented ML/DRL
  scheduler. Both assigned ATSSS papers say only "a simulated network environment" / no simulator at all.
- I found **no** paper placing a multipath scheduler inside the **UPF** or using the **N4/N6** interfaces for
  scheduling feedback, in any of the searches above. This is notable given that the 2021 IEEE Access survey
  (above) documents that the standardised MPTCP Proxy Function and PMF *already live in the UPF* — so the
  standardised anchor point exists while the ML-scheduling research has not used it.
- I found **no** study measuring ATSSS steering in a real multi-access testbed with ML. The closest UPF-side hit
  (JISEM 2025) is RAN-analytics-driven flow steering, not multipath transport scheduling, and is in a
  lower-visibility venue.
- I found **no** paper that treats the standardised ATSSS steering modes (Active-Standby / Priority-based /
  Smallest Delay / Load-balancing) as the **action space** of a learned scheduler and compares against them —
  which is a directly actionable gap, since §2 of this file shows the two Pham et al. papers compare only
  against "traditional parameter-based methods".

### (d) Multipath scheduler + O-RAN (near-RT RIC / xApps / E2)
**Searches run (exact queries):**
1. `O-RAN near-RT RIC xApp multipath transport MPTCP scheduling`
2. `O-RAN xApp traffic steering reinforcement learning E2 interface 2025`
3. `MPTCP near-RT RIC xApp O-RAN multipath scheduling`
4. `"near-RT RIC" xApp "traffic steering" 5G dual connectivity paper open access`
5. `O-RAN E2 interface xApp AI/ML scheduling 6G survey 2025 IEEE Access`

**What I FOUND (actual titles + venues + URLs):**
- **REAL: Reinforcement Learning-Enabled xApps for Experimental Closed-Loop Optimization in O-RAN with OSC RIC
  and srsRAN** — arXiv:2502.00715 (2025); also published at IEEE (IEEE Xplore document 11162144). A real
  near-RT RIC + xApp closed-loop RL testbed (OSC RIC, srsRAN) — **RAN optimisation, not multipath transport
  scheduling.** URLs: https://arxiv.org/abs/2502.00715 · https://ieeexplore.ieee.org/document/11162144
- **Hierarchical Reinforcement Learning Based Traffic Steering in Multi-RAT 5G Deployments** — ICC 2023,
  DOI 10.1109/icc45041.2023.10278983 (details in section (c) above). RAN-level traffic steering in the
  AI/ML-for-RAN family; **not** a transport-layer multipath scheduler. URL: https://arxiv.org/abs/2301.07818
- **Network-Aided Intelligent Traffic Steering in 6G O-RAN: A Multi-Layer Optimization Framework** —
  arXiv:2302.02711; "the three-step RL procedure for solving L-SP is carried out at Non-RT RIC based on the
  collected RAN data in SMO". O-RAN traffic steering with RL at the Non-RT RIC — again **RAN-level, not
  multipath transport.** URL: https://ar5iv.labs.arxiv.org/html/2302.02711
- **A Comprehensive Tutorial and Survey of O-RAN: Exploring Slicing-Aware Architecture, Deployment Options, Use
  Cases, and Challenges** — IEEE (Xplore document 11124199). Survey of O-RAN; **no multipath transport
  scheduling content implied by the title**, included only as evidence that the O-RAN literature is surveyed
  broadly. URL: https://ieeexplore.ieee.org/document/11124199
- **AI, ML, and LLM Integration in 5G/6G Networks: A Comprehensive Survey of Architectures, Challenges, and
  Future Directions** — IEEE (Xplore document 11159193), 2025. Survey covering AI/ML **and LLM** integration in
  5G/6G including O-RAN; surfaced by the O-RAN queries. URL: https://ieeexplore.ieee.org/document/11159193

**What I did NOT find:** **No paper integrating an MPTCP/MPQUIC multipath scheduler with an O-RAN near-RT RIC,
an xApp, or the E2 interface.** Across all five queries (including the explicit `MPTCP near-RT RIC xApp O-RAN
multipath scheduling` query), the only O-RAN + RL/xApp results are **RAN-domain** functions (scheduling,
traffic steering between RATs/cells, slice reconfiguration) — none of them touch a multipath **transport**
scheduler, and none read or write MPTCP/MPQUIC subflow state. I also found **no** xApp that exposes a
transport-layer scheduling control action over E2, and **no** paper proposing an E2 information element for
multipath/subflow state.

### Probe conclusion (what the four searches jointly establish)
The evidence pattern is consistent across all four themes: **multipath transport scheduling research and
network-management/AI-native-control research are two largely disjoint literatures.**
- Endpoint multipath schedulers (papers 3, 4A, 4B; Peekaboo, ReLes, DeepCC in their related work) are
  **closed-loop at the endpoint**, consuming per-subflow transport signals (RTT, cwnd, loss, throughput,
  send-window) and taking path/split actions — with **no northbound interface** to an SDN controller,
  orchestrator, RIC, or 5G core.
- Network-side AI control (O-RAN xApps, Non-RT RIC traffic steering, UPF flow steering, ATSSS PCF/MORL) operates
  at **flow/RAT/slice granularity**, with **no per-segment scheduling action** and, in the ATSSS case, no
  MPTCP/MPQUIC involvement at all in the retrievable text.
- The one place the two meet is a **2026 ICC Workshops paper** (Alruwisan & Yuksel) that puts MARL agents in a
  reactive SDN controller to assign/reroute MPTCP **subflows**, and one **2026 Scientific African** paper
  (MPS-OF-AS) that puts an MPQUIC scheduler in an SDN context — both at **flow/subflow assignment granularity**,
  and both very recent, which suggests the integration is only now beginning.
- **LLM/agentic control of multipath scheduling appears to be an open gap**: the only LLM × multipath artefacts
  found are (i) an IETF draft where the LLM is the *traffic being transported* (CAMP), and (ii) LLM-for-single-path-
  congestion-control preprints. I found **zero** peer-reviewed papers with an LLM or agentic AI as the multipath
  scheduler's policy.
- **The sharpest single gap found in this probe** is the mismatch documented in section (c): the standardised
  ATSSS architecture *already* places the Multipath Transport Proxy Function and the Performance Measurement
  Function in the **UPF** (IEEE Access 2021 survey, §II-D/E), and 3GPP Rel-19 FS_MASSS is standardising
  **multipath QUIC toward the UPF** — yet I found **no peer-reviewed paper that puts a learned multipath
  scheduler at that standardised anchor point, and no paper that uses the four standardised ATSSS steering modes
  as the action space of a learned scheduler**. That is a concrete, standards-anchored, unoccupied position for
  an AI-native network-management contribution.
