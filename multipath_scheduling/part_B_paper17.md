### 17. A Survey on Multipath Transport Protocols Towards 5G Access Traffic Steering, Switching and Splitting

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Hongjia Wu (SimulaMet/OsloMet), Simone Ferlin (Ericsson), Giuseppe Caso (Karlstad
  University), Özgü Alay (SimulaMet/OsloMet), Anna Brunström (Karlstad University). **2021**,
  **IEEE Access**, vol. 9, DOI `10.1109/ACCESS.2021.3134261` (received November 2021; published
  in the "accepted for future issue" version retrieved, which carries the final DOI).
  **Peer-reviewed journal survey; gold open access (CC BY 4.0).**
  *Note on the genre:* this is a survey, so several of the 21 fields are not applicable in the
  way they are for a primary paper. Where a field has no survey-level answer I say so explicitly
  rather than manufacture one.

- **1. Number and type of paths**
  Survey scope: **3GPP + non-3GPP access**, i.e. heterogeneous by construction — 5G New Radio
  (NR) / LTE on the 3GPP side and **WiFi** on the non-3GPP side. The survey is explicitly based
  on **ATSSS Rel-16** ("We base our work in this survey on ATSSS's Rel-16 [13] [15], which lay
  the foundations for multi-connectivity in 5G. Currently, 3GPP's ATSSS Rel-17 (Phase 2) [16] is
  ongoing work"), with Rel-17 discussed as ongoing. It also discusses **mmWave** dynamicity as
  the coming challenge.

- **2. Network architecture**
  The 5G **ATSSS** architecture: a **Multi-Access PDU (MA-PDU) session** anchored in the 5G core,
  with **AMF, SMF and UPF** network functions, and two integration topologies the survey
  distinguishes — **above-the-core** (end-to-end multipath, flows transparent to the cellular
  core) and **core-centric** (flows from both accesses aggregated into a single flow before
  leaving the cellular core). In the core-centric case "the UE and UPF communicate through the
  **Multipath Transport Function** (in the UE) and the **Multipath Transport Proxy Function**
  (in the UPF)"; for ATSSS-LL "the UE and UPF communicate with each other via the combination of
  ATSSS-LL Function of the UE and UPF. In addition, **UPF supports Performance Measurement
  Functionality (PMF)**". Policy: "delivering the policy rule to the SMF. The policy rule, shared
  by the SMF with the UE (uplink) or the UPF (downlink)". This is the single most important
  architectural fact in this document for the gap analysis: **the standard place where a
  network-side multipath function lives is the UPF, and the control interface is SMF→UE/UPF policy
  rules.**

- **3. Transport protocol**
  Covers **CMT-SCTP, MPTCP, MPQUIC and MP-DCCP**, with MPTCP as ATSSS's primary transport:
  "MPTCP plays a central role in ATSSS while MPQUIC has been discussed as an alternative"; and
  "The above steering modes are all supported by MPTCP." It records that most ATSSS-oriented work
  uses MPTCP "with exception of [36], that presents both MPTCP and Multipath QUIC (MPQUIC)".
  It also notes QUIC's structural limitation for core-centric ATSSS: because "QUIC connections
  are fully encrypted and therefore cannot be intercepted, e.g., terminated at the UPF, a solution
  such as the ATSSS Release 16 with MPTCP is not possible", so without MPQUIC adoption "a
  QUIC-based solution is limited to Switching and Steering" (no Splitting).

- **4. Scheduler location**
  Both, and the survey is explicit that they are different things: a **UE-side** function
  (Multipath Transport Function / ATSSS-LL Function) and a **core-network/UPF-side** function
  (Multipath Transport Proxy Function), configured by **SMF-issued policy rules**. The steering
  mode is part of that policy rule.

- **5. Scheduler inputs** (as the survey characterises the literature, not as its own design)
  The survey summarises the state of the art as using **path capacity and latency** ("When
  assigning packets to paths, the existing works usually take into account the capacity and
  latency of each path"), with per-approach additions: packet **arrival-time prediction** (FPS),
  **RTT ratio between paths** (DAPS), **loss rates** ("tailored for lossy networks and takes loss
  rates into account"), and active path-status/quality sensing to counter "the inaccurate
  estimation of the path latency when assigning the load to each path, caused by the underlying
  wireless networks". It further states that in ATSSS the relevant characteristics span "from
  frequency bands, e.g. mid- or high-bands, to transport layer characteristics, e.g. **RTT, CWND,
  and packet loss rates**", and that PMF exists in the UPF to measure path performance.

- **6. Path metrics used** (survey-level)
  RTT / smallest delay, capacity/bandwidth, packet loss rate, cost ("priority related to financial
  considerations at the user side, e.g., **cost per bit** sent on each path"). The survey notes
  that "Most of the existing multipath research … tackle[s] heterogeneous paths by looking at the
  **mean value** of path delay, loss rate, etc., while few others tackle the dynamicity of
  heterogeneous paths", and that 5G NR "will inevitably bring higher dynamicity to the paths due
  to millimeter Wave (mmWave)" — recommending future work "efficiently utilizing the **statistical
  distribution** of the path delay, loss, etc."

- **7. Scheduling decision**
  The survey's framing is **3GPP steering modes**, which it presents as the action space of
  ATSSS (four modes defined in TS 23.501), covering both per-packet and per-group granularity:
  - **Priority-based** — "Some priority weights are assigned to [accesses]" (conceptually
    containing Smallest Delay and Best-Access);
  - **Smallest Delay** — "The used access network is the one providing the shortest Round Trip
    Time (RTT)";
  - **Load-balancing** — "Each access network receives a per[centage]…"; identified as the one
    mode that is **not** per-packet: "The main difference with the other steering modes is that it
    directly schedules a **group of packets together**, while the other steering modes schedule on
    a **per-packet basis**";
  - **Best-Access** — generalises Smallest Delay with a higher-priority access preference;
  - **Redundant** — "All or some data flows are transmitted on both accesses in order to increase
    reliability."
  The survey also distinguishes **Steering** (choose access per flow/packet), **Switching**
  ("redirect all traffic of an ongoing [flow]…", a hard decision "to abandon one of the access
  networks"), and **Splitting** ("splitting of the traffic of a data [flow]…" across accesses).

- **8. Packet-level or flow-level scheduling**
  The survey keeps this distinction sharp and it is one of its most useful contributions: the
  **Load-balancing** mode is group/flow-level, whereas "the other steering modes schedule on a
  per-packet basis". It also reports an empirical claim about cMPTCP (client-based MPTCP over
  multiple operators' LTE networks) that is entirely flow/path-level: "cMPTCP is shown to
  outperform the default minRTT with up to **18.5%** and the other state-of-the-art multipath
  schedulers such as **ECF** with up to **11.7%** for the download throughput."

- **9. Reordering handling**
  Discussed as a structural property of the transport rather than a tunable penalty: MPTCP's
  data-level sequence numbering versus QUIC's stream-based multiplexing; the survey notes QUIC's
  advantages in "more efficient loss recovery". It reports results that hinge on reordering:
  "Both [97] and [98] present it is possible to maintain the performance metric as the default
  minRTT, while possibly decreasing the **cost ranging from 20% to more than 50%**." No
  receive-buffer sizing discussion of the kind found in papers 2 and 4 is reported.

- **10. Congestion-control interaction**
  A whole survey subsection is devoted to it ("Multipath Congestion Control for 5G"). It notes the
  fairness premise — "flows sharing a bottleneck end-to-end must receive the same resource amount"
  — and then makes a 5G-specific observation that **undercuts** the classic shared-bottleneck
  assumption: because "ATSSS scenarios include in general different technologies, which often
  belong to distinct underlying network infrastructures, e.g., the non-3GPP access does not share
  the same radio base station as the 3GPP access … the strict assumption about shared bottlenecks
  may become here **less relevant** compared to when the focus was on end-to-end Internet
  scenarios." It also notes that the current ATSSS modes are "very coarse-grained" and that
  "extending the current modes to also cover congestion control and reliable transfer aspects
  will be of great importance moving forward".

- **11. Objective**
  The survey's stated purpose is "to ease the link between … multipath transport protocols … and
  the ATSSS steering modes" and to determine which multipath techniques fit "the **eMBB and URLLC**
  service requirements". It identifies latency, throughput, reliability, and **cost** as the
  competing objectives, with Priority mode explicitly framed around cost: "a common approach is
  to set users' priority as the constraint for the optimization problem. The optimization goal can
  be however throughput-specific, which applies to eMBB, but also related to both latency and
  throughput, e.g., in deadline-aware video streaming applications, which thus maps to URLLC."

- **12. Algorithm** (survey-level taxonomy)
  It organises the literature into mathematical-modelling/optimisation approaches, rule-based
  heuristics, and data-driven approaches; it does not propose a new algorithm.

- **13. ML/DRL usage**
  **Yes — as a surveyed category, and this is directly relevant to the review.** The survey
  devotes subsection V-E to "**Data-driven approaches**" and reports:
  - "Recently, machine learning approaches (e.g., reinforcement [learning])…"
  - "**Reles** [63] uses offline reinforcement learning, i.e., a **Deep Q-Network (DQN)**, to train
    a multipath scheduler with **throughput as the reward**, and **delay and packet loss as
    penalties**. A similar approach is applied in [64], where a penalty is given when the number
    of unacknowledged packets exceeds a limit."
  - "Applying **online learning** in MPQUIC, **Peekaboo** [65] proposes a multipath scheduler that
    is aware of the dynamics of the paths and can adapt its scheduling strategy accordingly."
  - "More recently, [95] proposes an enhancement to Peekaboo, i.e., **M-Peekaboo**, capable of
    handling high oscillations in terms of network path characteristics, i.e, delay, bandwidth and
    loss, observed in **5G millimeter wave** network paths."
  - Effectiveness claim: "These scheduling approaches based on machine learning in general
    outperform the selected scheduling approaches that are not based on machine learning. For
    example, M-Peekaboo is shown to outperform BLEST with up to **28.7%** in the emulated 5G
    networks."
  - **Critical caveats the survey itself raises (verbatim):** "The advantage of data-driven
    solutions is that they have the potential to learn over different path conditions and
    accordingly adapt to them. However, they **may lack of explainability**, which might be even
    more severe in **URLLC**, where reliability is difficult to mathematically prove or measure,
    i.e., you have 100% reliability until the first packet loss happens. Therefore, we argue that
    future research in this direction should bear the **explainability** point in mind. Moreover,
    data-driven solutions are normally of **higher computation complexity** compared to the
    rule-based counterpart, but this can be alleviated nowadays by using specialized hardware used
    for data-driven tasks."

- **14. Simulator / testbed**
  `NOT REPORTED` as a primary contribution (it is a survey). It does name the platforms it
  considers necessary for 5G-era research: "experimental open-source 5G platforms such as
  **mmFlex** [159], and open source components such as **openairinterface** [160] that build on
  **software-defined radio** [161] will be crucial." Individual surveyed results it cites use
  emulated 5G networks (e.g. M-Peekaboo "in the emulated 5G networks") — the survey does not
  report their testbed details.

- **15. Traffic model**
  Discussed at the service level: **eMBB** (high throughput) and **URLLC** (low latency, high
  reliability), with examples including "deadline-aware video streaming", "virtual/augmented
  reality (VR/AR)", and video-on-demand. It notes burstiness as a real constraint: "by the
  end-users in case of **bursty video-on-demand traffic**."

- **16. Baselines**
  At the level of the survey's comparisons: **default minRTT**, **ECF**, **BLEST**, **RR**, and
  **FPS/DAPS**; the comparative claim quoted in field 13 uses BLEST as the ML baseline.

- **17. Metrics**
  Download throughput (%), goodput, latency/application delay, cost (%), reliability, and
  service-level eMBB/URLLC requirements.

- **18. Main result**
  As a survey its "result" is the mapping of multipath techniques onto ATSSS modes. The concrete
  quoted findings are: cMPTCP "up to **18.5%**" over default minRTT and "up to **11.7%**" over
  ECF for download throughput; M-Peekaboo "up to **28.7%**" over BLEST in emulated 5G; FPS/DAPS
  and the loss-aware family "[mainly] compare with RR and show the **throughput increase ranging
  from 10% to 40%**"; the packet-preallocation family "maintain the performance metric as the
  default minRTT, while possibly decreasing the **cost ranging from 20% to more than 50%**"; and
  the loss-aware mechanism [103] "can increase the download throughput around **10%** compared
  with FPS". Its overall conclusion: "We have presented what we believe to be the **first survey
  of multipath transport protocols for 5G**, subjecting to the standardized ATSSS architecture."

- **19. Limitation**
  As stated: the survey is scoped to Rel-16 with Rel-17 "ongoing work" and it "heavily rel[ies] on
  them at this stage"; its ATSSS analysis is therefore a snapshot that has since been superseded
  (Rel-17/18 ATSSS phases, and the IETF MP-DCCP/MPQUIC standardisation it flags as in progress).
  It also restricts depth: "In this paper, we [focus on] the MPTCP literature" for scheduling.
  Methodological limitation it surfaces itself: the shared-bottleneck fairness premise underlying
  multipath CC "may become here less relevant" in ATSSS — meaning the surveyed CC results may not
  transfer to the 5G core-centric architecture it advocates. Mine: the numeric claims it quotes
  are inherited from primary papers without independent verification, and no testbed is
  reproduced.

- **20. Research gap this suggests**
  This survey is the single best evidence source for the review's central question, because it is
  written by the multipath-scheduling community *about* 5G integration, and it shows three
  separate unbridged seams:
  (i) **Scheduling vs. orchestration**: the ATSSS control surface is a *coarse* policy rule
  (mode + priority) issued SMF→UE/UPF; the survey complains the modes are "very coarse-grained"
  and should "cover congestion control and reliable transfer aspects". There is no interface by
  which a scheduler's fine-grained state or decision can be exposed to, or driven by, a network
  orchestrator.
  (ii) **AI vs. reliability guarantees**: it explicitly flags **explainability** as a blocker for
  data-driven scheduling under URLLC, and **computational complexity** as the second cost.
  (iii) **Path dynamics**: it says the field studies *mean* path delay/loss while 5G mmWave needs
  *distributional* modelling.
  All three are open problems as of this 2021 survey.

- **21. Best URL retrieved / depth**
  `https://www.diva-portal.org/smash/get/diva2:1625432/FULLTEXT01.pdf` (Karlstad University DiVA
  deposit of the accepted version; publisher version:
  `https://ieeexplore.ieee.org/document/9645537`) — **FULL TEXT** (1,882 extracted lines,
  converted and read).

---
