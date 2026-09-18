# Agent B — Extraction: BLEST, ECF, Peekaboo, GCLR

Scope: the four papers assigned to Agent B. All 21 fields for each paper were filled **only** from
documents actually downloaded and converted in this session (PDFs + `pdftotext` output listed in
§"Retrieved artefacts" below). Bibliographic metadata was verified against Crossref/OpenAlex, not
against search snippets. Where the source does not state something, the field says `NOT REPORTED`.

**All four papers were read as FULL TEXT. None is ABSTRACT ONLY.**

---

### BLEST: Blocking Estimation-based MPTCP Scheduler for Heterogeneous Networks

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors (as printed): Simone Ferlin (†Simula Research Laboratory, Norway; ‡National ICT Australia
    (NICTA), Sydney, Australia), Özgü Alay (Simula Research Laboratory), Olivier Mehani (NICTA),
    Roksana Boreli (NICTA).
  - Year / Venue: 2016, *2016 IFIP Networking Conference (IFIP Networking) and Workshops*, Vienna,
    May 17–19, 2016.
  - DOI: `10.1109/IFIPNetworking.2016.7497206` — verified via Crossref, which returns
    `TITLE: BLEST: Blocking estimation-based MPTCP scheduler for heterogeneous networks`,
    `issued: [2016,5]`, `container-title: 2016 IFIP Networking Conference (IFIP Networking) and
    Workshops`, `page: 431-439`, `publisher: IEEE`.
  - Peer-reviewed conference paper. The retrieved PDF is the **official IFIP Open Digital Library
    version** (PDF metadata Subject: "Jörg Ott, Christos Papadopoulos, Fabio Ricciato: 15th
    International IFIP TC6 Networking Conference, Networking 2016, Vienna, May 17-19, 2016. IFIP
    Open Digital Library, ISBN: 978-3-901882-84-5"), with page footers `431`–`439`.
  - **Venue/page disagreement handled per spec rule 8:** the ECF paper's reference list cites BLEST as
    "In Proc. of IFIP Networking, **pages 1222–1227**, 2016" — those page numbers are wrong (they are
    the page range ECF also assigns to DAPS at IEEE ICC 2014). Crossref *and* the BLEST PDF's own
    page footers agree on **pp. 431–439**, so I trust pp. 431–439.

- **1. Number and type of paths**
  - **Exactly two paths.** Two configurations used throughout: heterogeneous **3G + WLAN**, and
    homogeneous **WLAN + WLAN** (`WLAN0` and `WLAN1`).
  - Emulated link characteristics (Section III): "• WLAN: Capacity=25 Mbit/s, Delay=25 ms, Loss=1%
    • 3G: Capacity=5 Mbit/s, Delay=65 ms, Loss=0%". Queue lengths: "the queue lengths at each router
    interface were set to 100 packets for WLAN and 3750 packets for 3G. The losses applied to the
    WLAN path are random."
  - Heterogeneous (deliberately asymmetric delay/capacity/loss: 25 ms vs 65 ms delay, 25 vs 5 Mbit/s,
    1% vs 0% loss).

- **2. Network architecture**
  - End-to-end MPTCP, **no proxy or middlebox**. Emulation topology (Figure 2, "Emulation experiment
    setup"): an MPTCP Client with two interfaces and an MPTCP Server, with two partially disjoint
    bottleneck paths; "Bottleneck 1 was loaded with background traffic from Server 1 to Client 1, and
    bottleneck 2 with traffic from Server 2 to Client 2."
  - Real-network experiments use the same logical topology "but now constructed over NorNet [20]",
    with background traffic generated from "Virtual Machines (VM) from five commercial cloud service
    providers (2x in Europe, 1x in North America and 2x in Asia) connected via 100 Mbps links", and
    the client is "consumer hardware with a RaspberryPi connected to a home DSL provider via WLAN and
    another interface via 3G/3.5G to a mobile broadband operator."
  - No 5G core, no proxy, no MPTCP-capable middlebox.

- **3. Transport protocol**
  - **MPTCP v0.90.** Footnote 2: "We base our work on MPTCP v0.90 throughout this paper."
  - Kernel: footnote 3: "TCP-Linux kernel 3.14.33 is used throughout our evaluations."

- **4. Scheduler location**
  - **Kernel.** The schedulers are implemented in the Linux MPTCP kernel: "we address this issue by
    re-implementing these schedulers in the Linux kernel"; the contribution is described as
    "state-of-the-art schedulers, all implemented in the Linux kernel". No userspace/proxy component.
  - Code availability (as stated): "BLEST's code is available at http://nicta.info/mptcp-blest."

- **5. Scheduler inputs (exact signals)**
  - BLEST is built on **MPTCP's connection-level send window**, not on RTT alone:
    "To overcome the issues of the PR, we propose a proactive scheduler where we decide at packet
    scheduling time whether to send packets over the slow subflow or not. **The decision is based on
    MPTCP's send window.** MPTCP maintains a send window on its control-plane for each MPTCP
    connection, one level above the subflows."
  - Exact signals, quoted:
    - "BLEST assumes that a segment will occupy space in MPTCP's send window (`MPTCP_SW`) for at least
      `RTT_S` if it is sent now on subflow `S`… We assume that all segments in flight on `S` occupy
      space in the window for the same amount of time."
    - "The remaining send window can be used by the faster subflow (i.e., lower RTT subflow), `F`."
    - "we estimate the amount of data `X` that will be sent on `F` during `RTT_S`, and check whether
      this fits into MPTCP's send window".
    - "To estimate `X`, we assume that for every `RTT_F`, its CWND grows by 1 (as it is done in
      congestion avoidance) and is always filled by the scheduler, as
      `rtts = RTT_S / RTT_F`  →  `X = MSS_F · (CWND + (rtts − 1)/2) · rtts`"
    - Decision inequality: "**If `X × δ > |M| − MSS_S · (inflight_S + 1)`, the next segment will not
      be sent on `S`. Instead, the scheduler waits for the faster subflow to become available.**"
  - So the exact input set is: `RTT_S` (RTT of slow subflow S), `RTT_F` (RTT of fast subflow F),
    `CWND` (congestion window of the faster subflow F), `MSS_F` and `MSS_S`, `inflight_S` (segments in
    flight on S), `|M|` = MPTCP send window `MPTCP_SW` (explicitly "mirror of receive window at the
    sender"), and a correction factor `δ` (denoted `δ_λ` in the sweeps).
  - Correction factor, quoted: "we introduce a correction factor `δ`, to scale `X`. `δ` is adjusted
    as follows. **HoL-blocking during one `RTT_F` is an event that triggers an increase of `δ` by
    `δ_λ`; the absence of HoL-blocking triggers a decrease by `δ_λ`. In the beginning of the
    connection we set `δ=1.0`, i.e., no correction of the estimation.**"
  - Sensitivities swept: "BLEST's parameter influence on bulk traffic with varying `δ_λ`=0.001, 0.003,
    0.005, 0.01, and 0.02; compared against minRTT."

- **6. Path metrics used**
  - Per-subflow **RTT** (`RTT_S`, `RTT_F`), per-subflow **CWND**, **MSS**, **number of in-flight
    segments** (`inflight_S`), and **MPTCP connection-level send-window occupancy** (`MPTCP_SW`, the
    sender-side mirror of the receive window).
  - Loss/buffer estimates are *not* direct inputs: the authors state the model "does not incorporate
    losses", which is why `δ` has to be learned. Quoted: "`δ` is corrected to lower values than its
    initial setting of 1.0, because **the model does not incorporate losses**."
  - No bandwidth, energy or cost metric is used as an input.

- **7. Scheduling decision**
  - Binary, per-segment decision over the *available* subflow: either **transmit the next segment on
    the candidate slow subflow `S`**, or **decline `S` and wait for the faster subflow `F`**.
    Quoted: "If `X × δ > |M| − MSS_S · (inflight_S + 1)`, the next segment will not be sent on `S`.
    Instead, the scheduler waits for the faster subflow to become available. Essentially, while
    minRTT always opts to use an available subflow, our scheduler is able to skip a subflow, waiting
    for a more advantageous subflow which can offer a lower risk of HoL-blocking, and the number of
    retransmissions that would have been consequently triggered."
  - It is not a split-ratio and not a multi-path selection: the action space is {send on S, wait for F}.

- **8. Packet-level or flow-level scheduling**
  - **Packet-level** (per-segment path assignment). BLEST decides "at packet scheduling time"; Figure 6
    illustrates allocation of individual segments ("segments 0…10", "segments 11…12", "13…20",
    "21…23", "24…32") to two subflows. Path selection and routing are out of scope.

- **9. Reordering handling (penalisation and receive-buffer terms)**
  - The problem is framed as **send-window → receive-buffer → HoL blocking**: "This heterogeneity
    results in packet reordering, leading to head-of-line (HoL) blocking, increased out-of-order (OFO)
    buffer use at the receiver and, ultimately, reduced goodput."
  - **MPTCP's own Penalisation-and-Retransmission (PR) mechanism and its penalty term**: "In order to
    address the heterogeneity of the paths, a mechanism of opportunistic retransmission and
    penalisation (PR) has also been proposed in [2]. In order to quickly overcome HoL-blocking,
    opportunistic retransmission immediately reinjects segments causing HoL-blocking onto a subflow
    with an RTT lower than that of the blocking subflow which has space available in its congestion
    window. **The penalisation mechanism also halves the congestion window of the blocking subflow to
    limit its use.**"
  - **Why BLEST rejects the penalty term**: "Penalisation of a long subflow (higher RTT) has a
    long-term detrimental impact on the performance: it will take longer for the subflow to increase
    its CWND, leading to underutilisation of the path and, ultimately, lower capacity aggregation."
    and "the approach is reactive as it depends on blocking to trigger PR at the sender. **The PR
    mechanism itself is detrimental in the long run, since it keeps the CWND of slow subflow
    artificially low.**"
  - **BLEST's replacement**: "Rather than penalising the slow subflows, BLEST estimates whether a path
    will cause HoL-blocking and dynamically adapts scheduling to prevent blocking." The penalty is
    therefore replaced by a *predictive skip/wait* action.
  - **Receive-buffer / receive-window terms**: the receive buffer is explicitly identified as the
    binding constraint — "As a rule-of-thumb, it is also recommended to **increase the receive buffer
    size** to further limit HoL-blocking situations [5]"; the send window BLEST uses is "mirror of
    receive window at the sender"; and the state of the art is critiqued for "trying to overcome
    **receive-window limitation** and, consequently, HoL-blocking". BLEST's own contribution is to
    make the receive-window constraint bind less often without inflating the buffer, by not filling
    the send window with slow-path data.
  - Reordering is **measured** as the MPTCP out-of-order (OFO) queue: "we also sample the maximum
    value of the out-of-order (OFO) queue every 10 ms during the experiments and present the results."
  - Buffer settings used, quoted: "The TCP buffer sizes (send/receive) were set to be equivalent to
    widely known Android settings… • Homogeneous (WLAN): 1024 KiB/2048 KiB. • Heterogeneous
    (3G+WLAN): 1024 KiB/2048 KiB." and "For bulk traffic experiments, we set both send and receive
    buffers to 16 MiB to evaluate MPTCP's aggregation capability."

- **10. Congestion-control interaction**
  - Congestion controller used: **MPTCP-OLIA**. The only explicit statement is: "For single-path TCP
    flows, we used TCP-Reno, therefore, fairly compairing against **MPTCP-OLIA**." (footnote 3). MPTCP
    v0.90 with Linux kernel 3.14.33.
  - Interaction mechanism: BLEST is **not coupled to the CC algorithm** — it reads the CWND and
    send-window state produced by congestion control and *withholds* traffic from the slow subflow, so
    that the sender does not have to rely on PR's CWND-halving. Quoted: "The PR mechanism itself is
    detrimental in the long run, since it keeps the CWND of slow subflow artificially low." BLEST
    avoids triggering that path, i.e. it *protects* the slow subflow's CWND instead of penalising it.
  - The paper also notes the scheduler cannot be replaced by CC alone: "while scheduling is needed to
    complement pure congestion control, path selection and send buffer management are also primordial."

- **11. Objective**
  - Stated objective (abstract): "We then propose a send-window BLocking ESTimation scheduler, BLEST,
    **which aims to minimise HoL-blocking in heterogeneous networks, thereby increasing the potential
    for capacity aggregation by reducing the number of spurious retransmissions.**"
  - Design-stance statement: "we propose a novel BLocking ESTimation-based scheduler, BLEST, **which
    takes a proactive stand towards minimising HoL-blocking. Rather than penalising the slow
    subflows, BLEST estimates whether a path will cause HoL-blocking and dynamically adapts
    scheduling to prevent blocking.**"
  - Secondary design constraint: "Although BLEST is designed for heterogeneous paths, we show in our
    experiments that it works as well as MPTCP's minRTT scheduler in homogeneous scenarios."

- **12. Algorithm**
  - A closed-form, per-segment *blocking-estimation* test (no pseudocode listing is given for BLEST
    itself; the algorithm is the Section V formulation):
    1. Let `S` be the candidate subflow the default scheduler would use, `F` the fastest subflow by RTT.
    2. Set `rtts = RTT_S / RTT_F`.
    3. Estimate the data the fast subflow can carry during one `RTT_S`:
       `X = MSS_F · (CWND + (rtts − 1)/2) · rtts`.
    4. If `X × δ > |M| − MSS_S · (inflight_S + 1)` → do **not** send on `S`; wait for `F`.
       Otherwise send on `S`.
    5. Adapt `δ` online: `+δ_λ` on each HoL-blocking event during one `RTT_F`, `−δ_λ` otherwise;
       initialise `δ = 1.0`.
  - The authors also re-implemented two prior algorithms for comparison (Algorithm 1 DAPS, Algorithm 2
    OTIAS), which are described in the paper but are not part of BLEST.

- **13. ML/DRL usage**
  - **No.** BLEST uses no machine learning, no reinforcement learning, and no neural network. It is an
    analytic closed-form estimator with a hand-tuned online correction factor `δ` (with swept
    `δ_λ = 0.001 … 0.02`). `NOT REPORTED` for any DRL variant, layers, or neurons (not applicable).

- **14. Simulator / testbed**
  - **Emulation + real-network testbed** (explicitly *not* a packet-level simulator such as ns-2/ns-3):
    - Emulation: "We used CORE [16] for the initial evaluation. CORE is a network emulator able to
      emulate a real network stack implementation within Linux containers, making it suitable to avoid
      simulation model simplifications."
    - Real: "we validate the performance of the different schedulers with real-network experiments
      within the same topology as shown in Figure 2 for the emulation experiments, but now constructed
      over **NorNet** [20]", with cloud VMs as background traffic and a RaspberryPi client on
      home DSL/WLAN + 3G/3.5G.
  - Background load generator: D-ITG. "We repeated all experiment settings 50 times, in both emulation
    and real scenarios." Analysis window: "we discarded the initial phase for each experiment and
    analyzed a period of 90 s for bulk and constant bitrate (CBR) traffic."

- **15. Traffic model**
  - Three traffic classes:
    - **Bulk transfer**: "a buk transfer, of 64 MiB" (with 16 MiB send/receive buffers), plus a
      45-second trace used for the `δ` convergence study.
    - **Web traffic**: three real sites — Table I "WEB TRAFFIC GENERATION": `wikipedia.org` 15 objects
      / 72 KiB; `amazon.com` 54 objects / 1024 KiB; `huffingtonpost.com` 138 objects / 3994 KiB.
      "To mimic the behavior of a real browser downloads were performed with 6 concurrent connections."
    - **Video**: "We considered constant bit-rate (CBR) video traffic with a frame size of 5 KiB on the
      application level and a rate of 1 Mbps."
    - Background: "A synthetic mix of TCP and UDP traffic was generated with D-ITG [19] … The TCP
      traffic was composed of saturated sender and rate-limited TCP flows with a exponentially
      distributed mean rate of 157 pps. The UDP traffic was composed of UDP on/off flows with Pareto
      distributed on and exponentially distributed off times. Each flow has an exponentially
      distributed mean rate of 100 kbps in the heterogeneous scenario and 500 kbps in the homogeneous
      scenario. Packet sizes were varied with a mean of 1000 Bytes and RTTs between 20 and 100 ms."

- **16. Baselines (exact names as the paper names them)**
  - **`minRTT`** — "MPTCP's default scheduler, minRTT"; "MPTCP's default minRTT scheduler first sends
    data on the subflow with the lowest RTT estimation". *(This is the "Lowest-RTT-First" baseline
    referred to in my task brief; the paper never calls it "Lowest-RTT-First".)*
  - **`DAPS`** — "Delay-Aware Packet Scheduler (DAPS) [7], [8]" (the original DAPS [7] was
    re-implemented; the ns-2 simplification in [8] was deliberately excluded: "We ignore the
    simplifications presented in [8], as they were only introduced to ease the implementation in the
    ns-2 of CMT-SCTP").
  - **`OTIAS`** — "Out-of-order Transmission for In-order Arrival Scheduler (OTIAS) [9]".
  - **Single-path TCP** — plain TCP on each path: "we compare MPTCP's default scheduler, minRTT, and
    BLEST against single path TCP on 3G and WLAN paths"; for TCP they "used TCP-Reno".
  - **There is NO Round-Robin (RR) baseline in BLEST.** The task brief mentioned Round-Robin; it does
    not appear anywhere in this paper's evaluation. The comparison set is {minRTT, DAPS, OTIAS} for
    multipath and {TCP-on-3G, TCP-on-WLAN} for single-path.

- **17. Metrics**
  - Application **goodput** [kiBps] (bulk); **web completion time** [s]; **application delay** [ms]
    (CBR); **average/maximum MPTCP out-of-order (OFO) queue size** [kiB] ("we also sample the maximum
    value of the out-of-order (OFO) queue every 10 ms"); **retransmission packets / retransmission
    volume** (Table II, Table V); **bytes on each path ratio** (Figures 9(c)/10(c)).

- **18. Main results (exact numbers, quoted)**
  - **Headline (abstract)**: "The resulting scheduler allows an increase by **12% in application
    goodput** with bulk traffic while **reducing unnecessary retransmissions by 80%** as compared to
    default MPTCP and other schedulers."
  - **Bulk, emulation, 3G+WLAN** (vs minRTT): "In 3G+WLAN, we observe that **BLEST reduces OFO buffer
    size by 19%, while it increases application goodput by 12%.**"
  - **Retransmissions, emulation, 3G+WLAN, bulk** (Table II): minRTT `366.37` packets ≈ `0.53 MiB`;
    BLEST `70.3` packets ≈ `0.1 MiB`. Text: "As illustrated in Table II, MPTCP's PR mechanism can send
    up to 0.53 MiB retransmissions, to overcome blocking of the WLAN path. BLEST achieves better
    aggregation with less OFO buffer, **saving up to 80% of retransmissions**."
  - **Bulk, emulation, WLAN+WLAN (homogeneous)**: "In WLAN+WLAN, **BLEST achieves similar application
    goodput with negligible OFO buffer size of 2.5 kiB compared to minRTT.**"
  - **Latency / CBR application delay, emulation (Table IV, 1 Mbps CBR)**:
    - 3G+WLAN: minRTT `68` ms, OTIAS `53.2` ms, DAPS `843.7` ms, **BLEST `62.8` ms**.
    - WLAN+WLAN: minRTT `52.18` ms, OTIAS `53.49` ms, DAPS `54.02` ms, **BLEST `52.24` ms**.
    - Text: "In the 3G+WLAN scenario, **BLEST improved the application delay over minRTT by 8% for CBR
      (1 Mbps)** and a slight improvement in OFO buffer size of 8% is also achieved."
    - Caveat stated by the authors: "BLEST performed worse than OTIAS with CBR, because OTIAS
      completely discarded the 3G path."
  - **Web completion time, emulation (Table III, seconds)**:
    - 3G+WLAN — Wikipedia: minRTT `0.421`, OTIAS `0.392`, DAPS `0.435`, **BLEST `0.337`**;
      Amazon: `1.60` / `1.724` / `1.789` / **`1.503`**;
      Huffington Post: `4.87` / `4.858` / `4.932` / **`4.62`**.
    - WLAN+WLAN — Wikipedia: `0.398` / `0.4107` / `0.333` / **`0.324`**;
      Amazon: `1.461` / `1.621` / `1.598` / **`1.456`**;
      Huffington Post: `4.218` / `4.509` / `4.393` / **`4.114`**.
    - Text (3G+WLAN): "the small contribution of the 3G path for Amazon can cause an impact of **up to
      7% reduction in the completion time for BLEST compared to minRTT**"; "For Huffington Post …
      the completion time for **BLEST is 6% lower than minRTT**."
    - Text (WLAN+WLAN): "In WLAN+WLAN, BLEST provides an **improvement of 3% for Huffington Post and 2%
      for Amazon in completion times compared to minRTT**. Overall, Table III illustrates the benefits
      of BLEST where the lowest completion time is achieved by the proposed BLEST algorithm for both
      heterogeneous and homogeneous scenarios for all the websites evaluated."
  - **Real-network (NorNet) results**:
    - Bulk: "**BLEST achieves on average 18% higher application goodput aggregation, while reducing
      the amount of retransmissions by more than 37%**, see Table V, with a slight improvement in OFO
      buffer size of 3%." Table V (retransmission packets, 3G+WLAN bulk): minRTT `33.42`,
      **BLEST `21.3`** (note: the table values imply ≈36.3%, while the text says "more than 37%" — both
      are quoted as printed).
    - Web: "With larger object sizes, **BLEST reduces the completion time by up to 10%, while reducing
      the OFO size by up to 25%.** Thus, MPTCP's performance with BLEST is closer to the WLAN path,
      **only 3% worse than TCP on the best path (WLAN)**."
    - CBR: "**BLEST improves the application delay by 11% while reducing the OFO size by more than
      20%.**"
  - **Preceding baseline study (DAPS/OTIAS vs minRTT, emulation, 3G+WLAN bulk)**: "OTIAS provides a
    goodput increase of 6% but requires 35% less OFO buffer compared to MPTCP's minRTT. On the other
    hand, DAPS provides a goodput decrease of 27% and requires 65% less OFO buffer compared to MPTCP's
    default scheduler." WLAN+WLAN: "MPTCP's default scheduler has a 3.5% lower goodput compared to
    OTIAS, which on the contrary takes about 87% more OFO buffer. DAPS delivers goodput values of
    about 16% less compared to MPTCP's default scheduler with about 97% more OFO buffer."

- **19. Limitation**
  - **Authors' stated limitations / future work (Section VII)**: "We want to expand our evaluation with
    the method proposed in [5], add other elements of heterogeneity, e.g., other network access
    technologies, evaluate different application performance metrics, e.g., throughput aggregation
    versus delay constraints, **increase the number of subflows and test the approach in mobility
    scenarios**." Also, `δ` is needed because "the model does not incorporate losses", i.e. the
    analytic estimator is loss-blind and must be corrected empirically.
  - **Methodological limitations I observe from the text**:
    - Only **two** subflows are ever evaluated; the BLEST decision rule is formulated pairwise
      (`S` vs `F`), and the paper does not show how it scales to >2 subflows.
    - Evaluation is emulation (CORE) plus one real testbed (NorNet), with 50 repetitions and a 90 s
      window; no ns-3/simulation cross-check and no large-scale measurement study.
    - The `δ_λ` correction factor is hand-swept (0.001–0.02) rather than derived; the paper shows
      performance depends on it (Figure 7).
    - BLEST still underperforms single-path TCP on the best path in some real scenarios by 3%, i.e. the
      MPTCP design goal is approached but not fully met.
    - The comparison against OTIAS on CBR is unfavourable to BLEST (62.8 ms vs 53.2 ms), which the
      authors attribute to OTIAS fully discarding the 3G path — i.e. BLEST trades latency for
      aggregation.
    - CBR delay for DAPS is pathological (843.7 ms) — a sign the comparison set is heterogeneous in
      maturity, but no statistical significance testing is reported.

- **20. Research gap this suggests**
  - BLEST's decision rule is a fixed analytic estimator with a single scalar, loss-blind correction
    factor, tuned by hand and swept offline. It has **no mechanism to learn the path/dynamicity model
    online** and no notion of *how dynamic* a path is — only its current RTT/CWND/window state. This is
    precisely the gap Peekaboo later attacks (field 13 of Peekaboo = online learning; Peekaboo's
    Insight 1 states the gap explicitly, and its Section II-B notes BLEST "fail[s] to be generically
    applicable" and that when dynamicity is high "BLEST and ECF overuse the lossy and delay varying
    Path 2"). Also unaddressed by BLEST: >2 subflows, mobility, and loss-aware estimation.
  - For an AI-native network-management review: BLEST is the canonical **model-based, non-learned**
    baseline whose hand-tuned scalar `δ_λ` is the parameter an AI-native controller would have to
    learn/adapt.

- **21. Best URL actually retrieved, and full text vs abstract**
  - **URL: `https://dl.ifip.org/db/conf/networking/networking2016/1570234725.pdf`** (IFIP Open Digital
    Library, Networking 2016 proceedings index at
    `https://dl.ifip.org/db/conf/networking/networking2016/index.html`). Retrieved HTTP 200,
    `application/pdf`, 1,394,632 bytes, 9 pages; PDF metadata Title = "BLEST: Blocking Estimation-based
    MPTCP Scheduler for Heterogeneous Networks".
  - **FULL TEXT.**
  - Dead ends tried first (for the record): Unpaywall (`is_oa: false`), OpenAlex (`oa_status: closed`),
    Semantic Scholar (`isOpenAccess: false`), HAL (`numFound: 0`), Fatcat/scholar.archive.org (no
    files), `web-backend.simula.no/.../blest.pdf` (HTTP 404), Simula publication page (HTTP 404).

---

### ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors (as printed on the version read): Yeon-sup Lim (IBM T. J. Watson Research Center),
    Erich M. Nahum (IBM T. J. Watson Research Center), Don Towsley (University of Massachusetts
    Amherst), Richard J. Gibbens (University of Cambridge).
  - Year / Venue: 2017, *Proceedings of the 13th International Conference on emerging Networking
    EXperiments and Technologies* (CoNEXT '17), Incheon, Republic of Korea, December 12–15, 2017.
  - DOI: **`10.1145/3143361.3143376`** — verified via Crossref: `TITLE: ECF`, authors
    "Yeon-sup Lim; Erich M. Nahum; Don Towsley; Richard J. Gibbens", `issued: [2017,11,28]`,
    `container-title: Proceedings of the 13th International Conference on emerging Networking
    EXperiments and Technologies`, `page: 147-159`, `publisher: ACM`, event "CoNEXT '17".
  - Peer-reviewed conference paper.
  - **Which version I read (task explicitly asked):** I read the **CoNEXT '17 full paper**, 13 pages,
    obtained from the University of Cambridge Apollo repository (item handle `1810/279112`,
    bitstream `conext17-ecf-draft-cr-rev5.pdf`, author-accepted manuscript; Apollo metadata
    `prism.startingPage=147`, `prism.endingPage=159`, `rioxxterms.versionofrecord=10.1145/3143361.3143376`,
    `rioxxterms.version=AM`, `dc.date.issued=2017-11-28`).
  - **On the "earlier/extended version" claim in my brief — checked and NOT substantiated:**
    - There **is** an earlier, *shorter* version: a 2-page paper at **ACM SIGMETRICS 2017**
      (`10.1145/3078505.3078552`, pp. 33–34, ISBN 9781450350327), also republished in *ACM SIGMETRICS
      Performance Evaluation Review* (`10.1145/3143314.3078552`). I initially downloaded this 2-page
      version by mistake (Cambridge Apollo item `1810/279113`) and then retrieved the 13-page CoNEXT
      version from item `1810/279112`. **All field values below are from the 13-page CoNEXT version.**
    - I found **no** KTH technical report and **no** *Computer Communications* 2022 version. Crossref
      bibliographic and container-title-filtered searches for `ECF` + `Computer Communications` return
      no such article, and Crossref/OpenAlex record exactly three `ECF` entries, all 2017 (the CoNEXT
      paper, the SIGMETRICS paper, and the SIGMETRICS PER republication). Reported as unverified.
  - Reference-list caveat (see BLEST entry above): ECF's reference [6] gives BLEST's pages as
    "1222–1227", which conflicts with Crossref and with the BLEST PDF itself (431–439). I trust
    431–439.

- **1. Number and type of paths**
  - **Two paths in the main evaluation: WiFi + LTE**, heterogeneous. Client is an "Android mobile
    device (Google Nexus 5)"; "The mobile device communicates with the server over the Internet using
    a WiFi access point (IEEE 802.11g) and an LTE cellular interface from AT&T." WiFi is the primary
    subflow (Android default).
  - Paths are made heterogeneous by server-side bandwidth regulation with `tc`: "we set WiFi and LTE
    bandwidths … between [1,10] Mbps" in the download study, and `{0.3, 0.7, 1.1, 1.7, 4.2, 8.6}` Mbps
    in the streaming study. Measured average RTTs at each setting are given in Table 2 (e.g. at 0.3 Mbps
    "WiFi RTT(ms) 969", "LTE RTT(ms) 858"; at 8.6 Mbps "WiFi RTT(ms) 40", "LTE RTT(ms) 105").
  - A **four-subflow** variant is also evaluated: "we compare the performance of the default and ECF
    scheduler for bandwidth pairs of 0.3 Mbps and [0.3-8.6] Mbps **using four subflows (two over WiFi
    and two over LTE)**".

- **2. Network architecture**
  - End-to-end MPTCP, **no proxy or middlebox**. Lab: Android Nexus 5 client (ExoPlayer DASH client;
    wget; Android Web browser with "six parallel (MP)TCP connections to the server (12 subflows for
    MPTCP)") ↔ WiFi AP (IEEE 802.11g) + AT&T LTE ↔ "a desktop running Ubuntu Linux 12.04 with the
    MPTCP 0.89 implementation deployed [19] … connected to the UMass campus network through a single
    Gigabit Ethernet interface. We use Apache 2.2.22 as the HTTP server while enabling HTTP persistent
    connections with the default Keep Alive Timeout (5 sec)."
  - In the wild: "we deploy an MPTCP enabled server in Washington D.C. using a commercial cloud
    provider, which uses the same server configuration for the controlled in-lab experiments".
  - Deployment property claimed: "**ECF, in contrast, is a server-side only modification, improving
    deployability**".

- **3. Transport protocol**
  - **MPTCP** (v0.89 in-kernel), not MPQUIC. Quoted: "with the **MPTCP 0.89** implementation deployed
    [19]". Standards referenced: RFC 6824 (MPTCP) and RFC 6182 (architectural guidelines).

- **4. Scheduler location**
  - **Kernel** — a modification of the Linux MPTCP kernel, on the **server side only**:
    "The implementation details of the ECF scheduler in the Linux Kernel are available at our technical
    report (http://cs.umass.edu/~ylim/mptcp_ecf)." and "ECF … is a server-side only modification,
    improving deployability, and works transparently for multiple workloads, not just streaming video."

- **5. Scheduler inputs (exact signals)**
  - The paper's thesis is that the scheduler must not use RTT alone: "Our results show that ECF
    consistently utilizes all available paths more efficiently than other approaches…" / abstract: "a
    new MPTCP path scheduler, ECF (Earliest Completion First), that utilizes **all relevant information
    about a path, not just RTT**"; "ECF monitors not only RTT estimates, but also the current subflow
    bandwidths (i.e., congestion windows) and the amount of data available to send (i.e., the send
    buffer)."
  - Complete exact input list, quoted from Section 4 ("APPROACH") and Algorithm 1:
    - `RTT_f`, `RTT_s` — RTTs of the fastest subflow `x_f` and second-fastest subflow `x_s`.
    - `CWND_f`, `CWND_s` — congestion windows of `x_f` and `x_s`. ("step 1: Select x_f using MPTCP
      default scheduler"; "n = 1 + CWND_f").
    - `σ_f`, `σ_s` — "the standard deviations of `RTT_f` and `RTT_s`, respectively", used as the margin
      "`δ = max(σ_f , σ_s)`".
    - `k` — "the number of packets in the connection level send buffer, which have not been assigned
      (scheduled) to any subflow". This is the **send-buffer occupancy** input.
    - The MPTCP **connection-level send buffer / send window**: "An MPTCP sender stores packets both in
      its connection-level send buffer and in the subflow level send buffer (if the packet is assigned
      to that subflow)."
    - `β` — the **hysteresis** constant, "The ECF hysteresis value `β` is set to 0.25 throughout our
      experiments".
    - Implicit state: whether the fast subflow has available CWND, and the sticky `waiting` state
      variable ("`waiting = 1 // Wait for x_f`").
    - Also relevant (diagnosis, not a decision input): the CWND-reset-on-idle behaviour —
      "the congestion controller resets the CWND to the initial window value and restarts from the
      slow-start phase if a connection is idle for longer than the retransmission timeout [1]."

- **6. Path metrics used**
  - **RTT** (estimate + its standard deviation `σ`), **CWND** as a proxy for subflow bandwidth
    ("the current subflow bandwidths (i.e., congestion windows)"), **send-buffer occupancy** `k`,
    RTT **variation/difference** between paths, and **out-of-order delay** as an evaluation metric.
    Explicitly **not** used: loss rate, queue occupancy, energy, cost (none appear as scheduler inputs).

- **7. Scheduling decision**
  - Exact action space (Algorithm 1, "ECF Scheduler"): return one of
    - "`return x_f`" — send the packet on the fastest subflow,
    - "`return x_s`" — send the packet on the second-fastest subflow, or
    - "`return no available subflow`" with "`waiting = 1 // Wait for x_f`" — i.e. **decline to schedule
      now and wait** for the fastest subflow.
  - Formally: "If `[1 + k/CWND_f] × RTT_f < RTT_s + δ` then if `CWND_s × RTT_s ≥ 2RTT_f + δ` then
    waiting = 1 // Wait for x_f, return no available subflow; else return x_s; else waiting = 0,
    return x_s." The first inequality decides whether waiting for the fastest subflow can finish the
    transfer earlier; the second "validates if using the second fastest subflow with its CWND (it
    takes `CWND_s × RTT_s` to finish transfer) does not complete earlier than waiting for the fastest
    subflow (at least `2RTT_f` for transfer)".
  - Hysteresis for switching back: "ECF uses a different inequality for switching back to using `x_s`
    after deciding to wait for `x_f`: `[1 + k/CWND_f] × RTT_f < (1 + β)(RTT_s + δ)`. This adds some
    hysteresis to the system and prevents it from switching states (waiting for `x_f` or using `x_s`
    now) too frequently."
  - Not a split ratio and not multi-path routing; it selects one subflow for the next packet, or defers.

- **8. Packet-level or flow-level scheduling**
  - **Packet-level** (per-packet path assignment with a wait option). Quoted: "MP-DASH … does not focus
    per-packet scheduling" (contrast case); "the design of the MPTCP path scheduler … distributes
    traffic across available paths according to a particular scheduling policy"; Algorithm 1 is
    "// This function returns a subflow for packet transmission". Path selection/routing is out of scope.

- **9. Reordering handling**
  - **Root-cause framing is deliberately different from HoL blocking:** "Note that this problem is due
    to the lack of packets to send, and **not** because of head of line blocking or receive window
    limitation problems discussed in [22]." The problem ECF targets is a **fast-subflow idle period**
    followed by a **CWND reset**: "the sender is still transferring data over the slow WiFi subflow
    while the fast LTE subflow is idle… the 8.6 Mbps LTE subflow completes its assigned packet
    transmissions much earlier than the 0.3 Mbps WiFi subflow and stays idle until the next download
    request is received", and "resetting the CWND of a fast subflow because of an idle period can
    result in the fast subflow not being fully utilized for consecutive downloads."
  - **Explicit penalty/reordering machinery inherited unchanged**: "The opportunistic retransmission
    and penalization mechanisms are enabled throughout all experiments." ECF does **not** add a new
    penalty term and does **not** modify the PR mechanism; it prevents the situation PR was designed to
    clean up. (Contrast stated by the authors: "BLEST's decision is based on the space in MPTCP send
    window and minimizing out-of-order delivery, whereas ECF's is based on the amount of data queued in
    the send buffer and with the goal to minimize completion time.")
  - **Robustness term used instead of a penalty**: the margin `δ = max(σ_f, σ_s)` — "To compensate for
    this variability, we add a margin `δ = max(σ_f, σ_s)`, where `σ_f` and `σ_s` are the standard
    deviations of `RTT_f` and `RTT_s`, respectively, in the inequality for the scheduling decision."
    The same `δ` is reused in the second inequality and in the hysteresis inequality.
  - **Reordering is measured, not penalised**, via **out-of-order delay** at the receiver:
    "Figure 13 presents the CCDF of the out-of-order delay that individual packets experience with the
    default scheduler… The median delay is a full second in the case of 0.3 Mbps WiFi and 8.6 Mbps
    LTE." No receive-buffer/ATD term is used as a scheduler input. Buffer/queue effects enter only via
    the connection-level send buffer `k`.
  - **Slow-start assumption disclosed**: "Note that ECF assumes that the subflows are in the congestion
    avoidance phase, which can cause incorrect estimations of the expected number of transfers
    (e.g., `k/CWND_f`) during the slow-start phase."

- **10. Congestion-control interaction**
  - ECF is designed to be **CC-agnostic**: "Note that we observe similar performance degradation
    regardless of the congestion controller used (e.g., Olia [15])."
  - The interaction mechanism is explicit and is the paper's core insight: coupled MPTCP CCs make the
    fast subflow's CWND a function of all subflows' CWNDs, so an idle-period reset of the fast subflow
    throttles the whole connection — "Since MPTCP congestion controllers such as coupled [27] and Olia
    [15] are designed to adapt a subflow CWND as a function of all the CWNDs across all subflows,
    resetting the CWND of a fast subflow because of an idle period can result in the fast subflow not
    being fully utilized for consecutive downloads." ECF therefore *preserves* the fast flow's CWND by
    avoiding idle periods: "ECF better preserves the faster flow's CWND and thus performs better."
  - "As with the default scheduler, ECF does no worse statistically than the default scheduler…"
  - **Which CC was actually configured in the experiments: NOT REPORTED.** The paper names Olia and
    "coupled" only as *examples* of controllers for which the phenomenon holds; no explicit statement
    of the CC used in the testbed runs appears in the text I retrieved.

- **11. Objective**
  - Stated objective (Introduction): "In this work, we propose a novel MPTCP path scheduler to
    **maximize fast path utilization**, called ECF (Earliest Completion First)."
  - Mechanism-goal statement: "By determining whether using a slow path for the injected traffic will
    cause faster paths to become idle, ECF more efficiently utilizes the faster paths, **maximizing
    throughput, minimizing download time, and reducing out-of-order packet delivery**."
  - Problem statement: "we examine whether the default MPTCP path scheduler can provide applications the
    **ideal aggregate bandwidth, i.e., the sum of available bandwidths of every paths**."
  - Secondary constraint: "it performs as well as other schedulers under symmetric path conditions";
    "Our experimental results show that ECF outperforms the existing schedulers across a range of
    workloads when path heterogeneity is significantly large, while providing the same performance
    using homogeneous paths."

- **12. Algorithm**
  - **Algorithm 1 – ECF Scheduler** (given verbatim in the paper):
    ```
    // This function returns a subflow for packet transmission
    Find fastest subflow x_f with smallest RTT
    if x_f is available for packet transfer then
        return x_f
    else
        Select x_s using MPTCP default scheduler
        n = 1 + CWND_f
        δ = max(σ_f , σ_s)
        if n × RTT_f < (1 + waiting × β)(RTT_s + δ) then
            if CWND_s × RTT_s ≥ 2RTT_f + δ then
                waiting = 1        // Wait for x_f
                return no available subflow
            else
                return x_s
            end if
        else
            waiting = 0
            return x_s
        end if
    end if
    ```
  - The two design inequalities, as printed: `(1 + k/CWND_f) × RTT_f < RTT_s + δ` and
    `(k/CWND_s) × RTT_s ≥ 2RTT_f + δ`; hysteresis variant
    `(1 + k/CWND_f) × RTT_f < (1 + β)(RTT_s + δ)`.
  - No learning; purely an analytic, closed-form decision rule with a tuned hysteresis constant and a
    variance-derived margin.

- **13. ML/DRL usage**
  - **No.** ECF uses no ML, no RL, no neural network. `NOT REPORTED` (not applicable) for DRL variant,
    layers, neurons. The only statistical machinery is the RTT standard deviation `σ` used as the
    margin `δ`.

- **14. Simulator / testbed**
  - **Real Linux-kernel testbed with real WiFi + real LTE, plus in-the-wild measurements. No simulator.**
    - Lab: "We use an Android mobile device (Google Nexus 5) as the client. Videos are played on the
      device using ExoPlayer [9]… over a WiFi access point (IEEE 802.11g) and an LTE cellular interface
      from AT&T." Server: Ubuntu Linux 12.04 + MPTCP 0.89 + Apache 2.2.22, on the UMass campus network.
      Path bandwidths are **emulated by traffic shaping on the server side**: video streaming is
      evaluated "while limiting the bandwidth of the WiFi and LTE subflows on the server-side using the
      Linux traffic control utility tc"; the wget study regulates "the WiFi and LTE bandwidths between
      [1,10] Mbps in a manner similar to Section 3.1".
    - In the wild: "we deploy an MPTCP enabled server in Washington D.C. using a commercial cloud
      provider… The mobile device communicates with the server over the Internet using a WiFi access
      point (a local town public WiFi) and an LTE cellular interface from AT&T. Note that in these
      experiments, the device uses each network as-is without any additional bandwidth regulation."
  - So: **bandwidth-limited real testbed with tc** (not netem-emulated paths), plus an unregulated
    wild deployment. Repetitions: streaming "Each experiment consists of five runs, where a run
    consists of the playout of the 20 minute video"; wget "averaged over thirty runs"; web browsing in
    the wild "measured over thirty runs"; wild streaming "nine runs over two days".

- **15. Traffic model**
  - Three workloads: "adaptive streaming video over HTTP, simple download activity using wget, and
    Web-browsing."
    - **DASH streaming**: "we select a video clip from [14] that is 1332 seconds long and encoded at
      50 Mbps by an H.264/MPEG-4 AVC codec. The original resolution of the video is 2160p (3840 by
      2160 pixels). We configure the streaming server to provide six representations of the video with
      resolutions varying from 144p to 1080p (just as Youtube does)… create DASH representations with
      5 second chunks." ABR: "a state-of-art adaptive bit rate selection (ABR) algorithm [6]."
      Bandwidth pairs chosen "slightly larger than those listed in Table 1, i.e.,
      {0.3, 0.7, 1.1, 1.7, 4.2, 8.6} Mbps, to ensure there is sufficient bandwidth for that video
      encoding."
    - **wget downloads**: "several file sizes (64 KB to 2 MB, in powers of two)".
    - **Web browsing**: "We deploy a copy of CNN's home page (as of 9/11/2014) consisting of 107 Web
      objects into our MPTCP server", fetched by the Android browser over "six parallel (MP)TCP
      connections… (12 subflows for MPTCP), using persistent HTTP connections".
    - **Dynamic-bandwidth streaming**: "we change WiFi and LTE bandwidths randomly at exponentially
      distributed intervals of time with an average of 40 seconds. The bandwidth values are selected
      from the set {0.3, 1.1, 1.7, 4.2, 8.6} Mbps, and chosen uniformly at random. Ten scenarios are
      generated, each using a different unique random seed".

- **16. Baselines (exact names as the paper names them)**
  - "We compare ECF to the following schedulers:"
    - **`Default`** — "The default scheduler allocates traffic to a subflow with the smallest RTT and
      available CWND space. If the subflow with the smallest RTT does not have available CWND space, it
      chooses an available subflow with the second smallest RTT." *(This is the "Lowest-RTT-First"
      baseline in my task brief; ECF calls it "the default scheduler" / "Default".)*
    - **`DAPS`** — "Delay-Aware Packet Scheduler (DAPS) [16]: DAPS seeks in-order packet arrivals at the
      receiver by deciding the path over which to send each packet based on the forward delay and CWND
      of each subflow: DAPS assigns traffic to each subflow inversely proportional to RTT."
    - **`BLEST`** — "Blocking Estimation-based Scheduler (BLEST) [6]: BLEST aims to avoid out-of-order
      delivery caused by sender-side blocking when there is insufficient space in the MPTCP
      connection-level send window… BLEST waits for a fast subflow to become available, so that the fast
      subflow can transmit more packets during the slow subflow's RTT, so as to free up space of the
      connection-level send window."
    - Implementations: "For DAPS and BLEST, we use the implementation from
      https://bitbucket.org/blest_mptcp/nicta_mptcp [6]".
  - A baseline they explicitly **exclude**: "we do not examine MP-DASH [10]… since MP-DASH does not
    focus per-packet scheduling".
  - **There is NO Round-Robin baseline in ECF.**
  - In the wild, "We limit our comparison of ECF to just the default scheduler since the other
    schedulers do not exhibit consistent improvement over the default scheduler in the previous
    experiments."

- **17. Metrics**
  - "Ratio of Measured Average Bit Rate vs. Ideal Average Bit Rate" (streaming quality); "Fraction of
    Traffic Allocated to Fast Subflow"; CWND traces over time; **average number of IW (initial window)
    resets**; **out-of-order delay** CCDF; **download completion time** (wget and Web objects);
    **average throughput**; LTE subflow utilization.

- **18. Main results (exact numbers, quoted)**
  - **Headline:** "Our results show that ECF consistently utilizes all available paths more efficiently
    than other approaches under path heterogeneity, particularly for streaming video. At the same time,
    it performs as well as other schedulers under symmetric path conditions." / "In Web browsing
    workloads, ECF also does better in some scenarios and never does worse."
  - **Streaming bit rate (lab, fixed bandwidth, 5 runs × 20 min video)**: "Figure 9(b) shows that ECF
    successfully enables the streaming client to obtain average bit rates closest to the ideal average
    bit rate, and does substantially better than the default when paths are not symmetric." vs DAPS:
    "DAPS does not improve streaming performance; it yields even worse streaming bit rate than the
    default scheduler with some bandwidth configurations, e.g., 4.2Mbps for both of WiFi and LTE."
    vs BLEST: "BLEST slightly improves streaming performance with 1 Mbps WiFi and [1..10] Mbps LTE
    pairs, but does not improve the average bit rate for other configurations."
  - **CWND resets (Table 3, "0.3 Mbps WiFi & 8.6 Mbps LTE", # of IW resets over the whole video
    playback)**: `Default 486`, `DAPS 92`, `BLEST 382`, **`ECF 16`** — "the default, DAPS, and BLEST
    schedulers experience high numbers of IW resets, while ECF incurs such events only 16 times on
    average."
  - **Out-of-order delay (streaming, 0.3 Mbps WiFi / 8.6 Mbps LTE)**: "**Under ECF, almost 99.9% of
    packets experience out-of-order delays less than 0.8 seconds.** In contrast, with the default
    scheduler, **over 99% of the packets suffer from out-of-order delays larger than one second**,
    while DAPS and BLEST have 90% and 96% of packets." Default scheduler median OOO delay: "The median
    delay is a full second in the case of 0.3 Mbps WiFi and 8.6 Mbps LTE." Symmetric case (4.2/8.6):
    "out-of-order delay becomes much smaller… The schedulers mostly yield out-of-order delays of less
    than 0.1 seconds (again, except for DAPS). **DAPS, on the other hand, delivers over 60% of packets
    to the application layer with delays greater than 0.05 sec, which is worse than that even the
    default scheduler.**"
  - **Streaming with random bandwidth changes**: "**ECF obtains up to 2x more throughput than the
    default scheduler in the presence of path heterogeneity (e.g., 200th chunk download).**"
  - **wget simple downloads**: "**when LTE is 10 Mbps and WiFi is 1 Mbps, ECF reduces download time by
    200 ms or 13%**"; "**ECF yields up to 20% smaller download times than the default scheduler in the
    presence of path heterogeneity when downloading files of 256 KB or larger**." For small transfers:
    "for small transfers (128 KB), the default and ECF schedulers both yield the same completion time."
    Caveat: "the relative improvement by ECF decreases as the transfer size increases."
  - **Web browsing (lab, CNN page, 107 objects)**: equal bandwidth (5.0/5.0): "all schedulers yield
    almost the same download completion time: 98% of object downloads are completed in a similar time
    for all schedulers"; (1.0 WiFi / 5.0 LTE): "**ECF completes 99% of object downloads earlier than
    the other schedulers**"; (1.0/10.0): "as paths become more heterogeneous, ECF again explicitly
    exhibits smaller object download completion times than the other schedulers, while **DAPS and BLEST
    do not outperform the default scheduler**."
  - **In the wild — streaming (9 runs, 2 days)**: "**On average, the ECF throughput is 7.79 Mbps while
    the default scheduler 6.72 Mbps, an improvement of 16%.**" Subflow level in run 9: "the default
    scheduler injects 3% of packets through the WiFi subflow in this case… (in terms of LTE throughput,
    the default scheduler yields 7.31 Mbps while ECF does 7.72 Mbps)."
  - **In the wild — Web browsing (30 runs), Table 4 "Average Statistics of Web Browsing in the Wild"**:
    | | Download Completion Time (sec) | Out of Order Delay (sec) |
    |---|---|---|
    | Default | 0.882 | 0.297 |
    | ECF | 0.650 | 0.087 |
    | **ECF Improvement** | **26% shorter** | **71% shorter** |
    Text: "On average, **ECF completes the object downloads in 0.65 seconds, while the default scheduler
    requires 0.88 seconds, an improvement of 26%**. In addition, while **ECF completes 99.9% of object
    downloads in around 17 seconds, the default scheduler requires 30 seconds**." and "**ECF yields an
    average out-of-order delay of 0.087 seconds, while the default scheduler yields an average of 0.297
    seconds, an improvement of 71%.** Only 0.2% of packets downloaded using ECF exhibit slightly larger
    out-of-order delays than the largest one using the default scheduler. We found that 0.2% is from
    twelve instances out of approximately 27000 data points; these twelve packets suffer out-of-order
    delays of approximately 2.5 seconds."
  - **Four-subflow check**: "As shown in Figure 15, ECF mitigates performance degradation in the
    presence of significant path heterogeneity."
  - **Diagnostic (justifying the design)**: "when WiFi and LTE provide 0.3 Mbps and 8.6 Mbps… the
    streaming client retrieves 480p video chunks, which requires only 2 Mbps, even though the ideal
    aggregate bandwidth is larger than 8.47 Mbps. Thus, the value is **only 25% of the ideal
    bandwidth**."

- **19. Limitation**
  - **Authors' stated limitations**:
    - "Note that **ECF assumes that the subflows are in the congestion avoidance phase**, which can
      cause incorrect estimations of the expected number of transfers (e.g., `k/CWND_f`) during the
      slow-start phase."
    - Small transfers are unaffected: "for small transfers (128 KB), the default and ECF schedulers
      both yield the same completion time", and "the relative improvement by ECF decreases as the
      transfer size increases" (the single idle period is amortised over a longer transfer).
    - Evaluation choices disclosed as omissions: "other values for β were examined but found to yield
      similar results, **not shown due to space limitations**"; configurations with WiFi > 1 Mbps in the
      wget study "omit those figures for space limitations".
  - **Methodological limitations I observe from the text**:
    - Only **one real access-technology pair** is evaluated (IEEE 802.11g WiFi + AT&T LTE); the
      heterogeneous conditions in the lab are produced by **server-side `tc` bandwidth shaping**, so
      delay heterogeneity is largely whatever the live networks provide, not a controlled variable.
      RTT values vary widely run to run (Table 2), and in the wild "RTT varies widely over the two
      days".
    - The in-the-wild comparison drops DAPS and BLEST ("We limit our comparison of ECF to just the
      default scheduler"), so the headline 16%/26%/71% wild numbers are ECF-vs-default only.
    - The 4-subflow result is qualitative ("ECF mitigates performance degradation") with no numbers in
      the text.
    - `β = 0.25` is a hand-tuned constant with the sensitivity study withheld from the paper.
    - No comparison against learning-based schedulers (none existed at the time), and no energy/data-
      cost accounting despite a mobile client.

- **20. Research gap this suggests**
  - ECF is a **static, hand-parameterised analytic rule** (`β`, `δ = max(σ)`), built on the assumption
    that subflows are in congestion avoidance. It has no mechanism to (a) detect that its assumptions
    are violated, (b) re-tune itself when path dynamicity changes, or (c) reason about loss — the
    authors show ECF's advantage shrinks or disappears as paths become symmetric or highly dynamic.
    Peekaboo states this gap explicitly for both BLEST and ECF: "Both BLEST and ECF have their merits;
    however, **they fail to be generically applicable**", and "given different dynamicity levels, none
    of the existing solutions consistently outperforms the others", "when the dynamicity level is high,
    minRTT becomes the best choice, since BLEST and ECF overuse the lossy and delay varying Path 2."
  - For an AI-native network-management review, ECF is the strongest **non-learned, heterogeneity-aware**
    baseline: it uses exactly the telemetry an AI-native controller would consume (RTT, RTT variance,
    CWND, send-buffer occupancy) but combines it with fixed thresholds — a natural target for learned
    or adaptive policies.

- **21. Best URL actually retrieved, and full text vs abstract**
  - **CoNEXT '17 full paper (the version I extracted from):**
    `https://api.repository.cam.ac.uk/server/api/core/bitstreams/9f216be1-4124-4f10-bbad-137e912cc7ff/content`
    (University of Cambridge Apollo repository, item `https://www.repository.cam.ac.uk/handle/1810/279112`,
    file `conext17-ecf-draft-cr-rev5.pdf`). HTTP 200, `application/pdf`, 1,480,470 bytes, **13 pages**;
    PDF Title = "ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths".
  - **Also retrieved but NOT used for extraction (2-page SIGMETRICS version, for version disambiguation):**
    `https://api.repository.cam.ac.uk/server/api/core/bitstreams/3ec47f93-4360-4630-bd4a-9e1ed23605fa/content`
    (Apollo item `https://www.repository.cam.ac.uk/handle/1810/279113`, 2 pages, pp. 33–34, DOI
    10.1145/3078505.3078552).
  - **FULL TEXT.**
  - Dead ends tried first (for the record): Unpaywall (`is_oa: false`), OpenAlex (`oa_status: closed`),
    Semantic Scholar (`isOpenAccess: false`), ACM DL `dl.acm.org/doi/...` and `/doi/pdf/...` (HTTP 403,
    Cloudflare "Just a moment…" challenge on both the abstract and PDF endpoints, with and without a
    cookie jar), KTH DiVA (no ECF record; DiVA search subsequently returned an Anubis bot challenge),
    Crossref/OpenAlex searches for a *Computer Communications* 2022 or KTH technical-report version
    (none found).

---

### Peekaboo: Learning-Based Multipath Scheduling for Dynamic Heterogeneous Environments

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors (as printed): Hongjia Wu (SimulaMet and OsloMet), Özgü Alay (University of Oslo and
    SimulaMet), Anna Brunstrom (Karlstad University), Simone Ferlin (Ericsson AB, Stockholm), Giuseppe
    Caso (SimulaMet). (OpenAlex author list confirms: H. Wu, Ö. Alay, A. Brunström, S. Ferlin,
    G. Caso.)
  - Year / Venue: **2020**, *IEEE Journal on Selected Areas in Communications (JSAC)*, vol. 38, no. 10,
    pp. 2295–2310. Verified via Crossref: `issued: [2020,10]`, `container-title: IEEE Journal on
    Selected Areas in Communications`, and OpenAlex: `publication_date: 2020-06-08`,
    `publication_year: 2020`. *(This confirms the "likely 2020" in my brief: the exact year is 2020,
    issue date October 2020, online 8 June 2020.)* The manuscript itself records "Manuscript received
    October 8, 2019; revised February 15, 2020; accepted March 16, 2020."
  - DOI: **`10.1109/JSAC.2020.3000365`** (verified via Crossref).
  - **Peer-reviewed journal article.** The copy I read is the **author-accepted manuscript**
    (NVA/OSLOMET "AcceptedVersion", carrying the IEEE notice "© 2020 IEEE. Personal use of this
    material is permitted… DOI: http://doi.org/10.1109/JSAC.2020.3000365").

- **1. Number and type of paths**
  - **Two paths, heterogeneous, assumed by design**: "For simplicity, in this work we assume two paths
    (i.e., **WiFi and cellular**), which is a common configuration in off-the-shelf devices. However,
    the use of Peekaboo can be straightforwardly extended to the case of more than two paths."
  - Heterogeneity parameters (Table III, "THE RANGE OF PARAMETERS REFLECTING PATH HETEROGENEITY IN
    TERMS OF BANDWIDTH, DELAY AND DIFFERENT DYNAMICITY LEVELS"): **Path 1: 2–10 Mbps, OWD 80–100 ms,
    RTT variation 0–16%, Loss 0–3%**; **Path 2: 40–50 Mbps, OWD 20–30 ms, RTT variation 0–16%,
    Loss 0–3%**.
  - Design-insight experiment: "Path 1 mimics a slower link with 2 Mbps bandwidth and RTT of 200 ms,
    Path 2 mimics a faster link with 50 Mbps bandwidth and RTT of 40 ms."
  - Dynamicity levels defined: "Low dynamicity refers to very stable channel conditions with **0%
    random packet loss and 0% delay variation**, Medium dynamicity refers to low variations in the
    channel with **1, 5% random packet loss and 8% delay variation** and finally High dynamicity refers
    to significant variations in the channel with **3% random packet loss and 16% delay variation**."
  - The design-space exploration varies Path 1 over "2 Mbps-50 Mbps and 20 ms-100 ms" against a fixed
    Path 2 of 50 Mbps / 20 ms, giving 9 dynamicity combinations.

- **2. Network architecture**
  - End-to-end **MPQUIC, no proxy or middlebox**. Emulation topology (Figure 4, "Multipath topology
    used in the experiments"): "MPQUIC Client" with "two network interfaces to the client and one to
    the server over two partially disjoint paths, i.e., Path 1 and Path 2", via a "Router" to an
    "MPQUIC Server". "Each path is characterized by its bandwidth, One-Way Delay (OWD), RTT variation,
    and random loss."
  - Real deployment: "We deploy an MPQUIC server in a European capital, and the MPQUIC client is
    locally on a laptop in the same city. The client communicates with the server over the Internet,
    using both a WiFi access point and an LTE network." Five scenarios (Residence/private WiFi;
    Library 1 and Office 1 at one university via Eduroam; Library 2 and Office 2 at another
    university via Eduroam).

- **3. Transport protocol**
  - **Multipath QUIC (MPQUIC)** — *not* MPTCP. "We implement Peekaboo in Multipath QUIC (MPQUIC) and
    compare it with state-of-the-art multipath schedulers…"; reason for choosing MPQUIC: "(i) QUIC's
    development is currently attracting attention in different communities; (ii) **QUIC's
    implementation is in user space, simplifying extension and adoption**." MPQUIC reference:
    De Coninck & Bonaventure, "Multipath QUIC: Design and evaluation", ACM CoNEXT 2017.

- **4. Scheduler location**
  - **Userspace** — inside the MPQUIC implementation; the paper argues this is a deployability
    advantage ("QUIC's implementation is in user space, simplifying extension and adoption"). The
    scheduler sits between the send buffer and the interfaces: "The data packets from the application
    reside in the send buffer, and the scheduler assigns each packet to a different interface based on
    a particular scheduling policy." Code open-sourced: "The source code of Peekaboo and all the
    scripts to produce results are open source" at `https://mosaic-simulamet.com/peekaboo`.

- **5. Scheduler inputs (exact signals)**
  - **A 6-dimensional feature vector `x_t`**: "We adopt four main parameters to create the features used
    to characterize the paths at the transport layer, these are: **CWND, number of Inflight Packets
    (InP), Send Window (SWND) (the mirror of receive window at the sender) and RTT.**" … "we use the
    selected parameters for three features with a throughput-like unit, **dividing the first three
    parameters by the RTT** experienced on the paths. Thus, the feature vector used by Peekaboo includes
    **CWND/RTT, InP/RTT, and SWND/RTT values, for both Path 1 and Path 2**. Given a time `t`, in which a
    transmit/wait decision has to be taken by Peekaboo, the feature vector is defined as `x_t`, having
    dimension `d × 1`, with **`d = 6`** in our case. Normalizing the CWND, InP and SWND by the RTT
    before embedding them in the feature vector provides a comparable scale and also boosts the
    learning speed [41]."
  - **RTT statistics used to build the reward's reference window**: "`T_ref` is calculated by
    considering the values of RTT and RTT variation on both faster and slower paths, as captured by the
    **`RTT_f`, `RTT_s`, `σ_f`, and `σ_s`** parameters [43], respectively", with
    "`T_ref = max(2(RTT_f + σ_f), RTT_s + σ_s)`".
  - **Reward-derived signals**: instantaneous reward "`r = PS/(T_ACK)`" where PS is the packet size in
    bytes and T_ACK the time from transmission to ACK reception, and the discounted accumulated reward
    `R`; the fit statistic `q̂` and its change threshold `q̂_th`.
  - **Action-set decision inputs**: path availability ("A path is considered available if there is
    space left in its CWND").
  - **NOT inputs**: no loss-rate or queue-occupancy signal is fed to the learner. Dynamicity is
    *experienced* through the reward and through RTT variation, not measured and passed in explicitly —
    "Peekaboo runs without any initial input and assumption of the path dynamicity."

- **6. Path metrics used**
  - **CWND**, **number of in-flight packets (InP)**, **send window (SWND, the sender-side mirror of the
    receive window)**, **RTT**, and **RTT variation `σ`**; all three of CWND/InP/SWND are normalised by
    RTT to give throughput-like units.
  - **Throughput** is the quantity being optimised, via the reward `R` in "bytes per millisecond".
  - Deliberately **no** explicit loss-rate, energy or cost metric as an input; loss and delay variation
    enter only as environmental "dynamicity" that changes the observed reward and the optimal action.
  - Application-level metric: application delay relative to a deadline (real-time streaming).

- **7. Scheduling decision**
  - Action space: for each *available* path, `{transmit, wait}`.
    "**A path is considered available if there is space left in its CWND, and for each available path
    we have two actions: transmit and wait.** For example, if only one path is available, the action
    set includes: (i) transmit on that path and (ii) wait until the other path becomes available again,
    and if both paths are available, each action corresponds to the selection of a path."
  - Which subset of actions is learned — the baseline action set:
    "**we rely on minRTT when two paths are available (same as BLEST and ECF), while optimizing the
    policy when the scheduler has to decide between waiting for the low latency path or transmitting on
    the high latency path.**" Three supersets were tested and rejected ("Addition 1/2/3"), concluding
    "Based on these observations, **we keep the baseline as the action set in Peekaboo**."
  - The action is made stochastic by a two-state Markov-chain adjustment: the deterministic decision is
    taken with probability `p`, and the discarded action with probability `1−p` (e.g. for ECF-A,
    "ECF-A has `P1 = 0.73` probability to wait but also `1−P1 = 0.27` probability to transmit the packet
    on the slower path").
  - Not a split ratio and not routing: it is a per-packet transmit-here-or-wait choice.

- **8. Packet-level or flow-level scheduling**
  - **Packet-level.** "the scheduler assigns each packet to a different interface"; the decision is
    taken per packet ("Given a time `t`, in which a transmit/wait decision has to be taken by
    Peekaboo"); the reward is computed per packet ("the throughput obtained over the currently
    scheduled packet and the following ones"). Path selection/routing is out of scope.

- **9. Reordering handling**
  - **Motivation is head-of-line blocking and the receiver-buffer problem**: "When the paths are
    heterogeneous, especially in terms of delay and loss, sent packets will arrive to the destination
    out of order, leading to head of line (HoL) blocking, ultimately reducing the performance." The
    related-work section notes "To solve the receiver buffer problem [32] in multipath transport, [30]
    proposes the Penalisation and Retransmission (PR) mechanism."
  - **The paper adds no explicit reordering penalty term and no receive-buffer/ATD term.** This is a
    genuine absence, not an omission on my part: the scheduler's only reordering-aware mechanism is
    (a) the `wait` action inherited from BLEST/ECF and (b) the reward's in-order-delivery accounting.
    Quoted: "since each path has its own packet sequence space in MPQUIC, a later scheduled packet from
    the application can be ACK'ed earlier. In this case, **the ACK is not released as a new ACK until
    all the previous packets have been ACK'ed, capturing the in-order-delivery of the packets in the
    calculation of `r` and thus `R`.**"
  - The reward is explicitly designed to internalise the cost of blocking the future:
    "**it utilizes the discounted reward to quantify the impact between different packets. It penalizes
    the case where the current packet may delay the receipt of future packets.** Besides that, we also
    observe that for the packets that missed the deadline, Peekaboo provides shorter delays."
  - RTT **variation `σ`** is used as the uncertainty measure in `T_ref` and is one of the two axes of
    the "dynamicity" definition (the other being loss rate) — so reordering risk is captured
    statistically rather than as a buffer-occupancy penalty.
  - A receive-buffer / reordering term as an explicit scheduler input: **NOT REPORTED.**

- **10. Congestion-control interaction**
  - CC algorithm used in the experiments: **NOT REPORTED.** I searched the retrieved full text for
    Cubic/NewReno/Olia/BALIA/LIA/BBR and for any statement naming the CC configured in the MPQUIC
    client/server; the paper names coupled CC and OLIA only in the *related-work* reference list, and
    mentions congestion control generically ("in multipath transport, three main building blocks are
    often the objects of research: congestion control [17]–[22], path (or connection) management
    [23]–[26] and the scheduler [27], [2], [28], [29], [1]"). No explicit interaction mechanism with a
    named CC is described.
  - What *is* stated about the interaction: Peekaboo consumes **CWND** as a feature and treats "space
    left in its CWND" as the definition of path availability, so it is CWND-driven and CC-agnostic in
    principle; and the scheduler must not hurt the stack — one of the two requirements on the learning
    approach is that it be "computationally lightweight, **so that the operation of the network stack is
    not negatively affected**."

- **11. Objective**
  - Research problem, quoted verbatim: "**How to design a multipath scheduler that learns and adapts to
    heterogeneous paths with dynamically varying channel conditions?**"
  - Optimisation objective behind the stochastic adjustment: "Our goal is to find the probability values
    that maximize the scheduler performance (**i.e. to minimize the median completion time of a file
    download**)."
  - Learning objective: "The goal of the agent is to **maximize a reward function**, which indicates how
    well the agent is adapting to the environment by selecting an action from the available set."
  - Design insights stated as objectives: "**Insight 1:** A multipath scheduler should employ an
    adaptive scheme that takes into account both the current network path characteristics and their
    dynamicity levels." / "**Insight 2:** Without an accurate estimate of the characteristics of the
    available paths, due to variability and incomplete information, a multipath scheduler should employ
    a stochastic adjustment strategy."

- **12. Algorithm**
  - **Peekaboo (Algorithm 4)** = three stages (Figure 3): **Learning stage** (§III-A LinUCB +
    §III-B stochastic adjustment), then **Deployment stage** (§III-C), with re-learning on detected
    dynamicity change.
  - **Deterministic online learning — LinUCB (Algorithm 2 "Online Learning via LinUCB")**:
    initialise `A_a ← I_d` (d-dimensional identity) and `b_a ← 0_{d×1}` for every action `a ∈ A`;
    loop: "`θ_a ← A_a^{-1} b_a`", "`E[R_{t,a}|x_t] ← x_t^T θ_a + α sqrt(x_t^T A_a^{-1} x_t)`",
    "`a_t ← arg max_a E[R_{t,a}|x_t]`", then "`A_{a_t} = A_{a_t} + x_t x_t^T`",
    "`b_{a_t} = b_{a_t} + R_{t,a_t} x_t`"; return `Θ ← {θ_a ∀a ∈ A}`. (Ridge regression + Upper
    Confidence Bound; also "Algorithm 3" tunes `α`; the paper notes "we adopt the LinUCB version
    proposed in [44], which transforms the matrix multiplication in Equation (2), so that only a `d×d`
    dimensional matrix is buffered in the computing unit instead of the original `m×d` matrix.")
  - **Reward (Algorithm 1 "Discounted Reward R")**, exact: "`γ = 1, R = 0`";
    "`T_ref = max(2(RTT_f + σ_f), RTT_s + σ_s)`"; while "`T_elap < 3T_ref` && new ACK":
    "`r = PS/(T_ACK)`", "`R = R + rγ`", with γ updated by "`γ = c1γ`" if `T_elap ≤ T_ref`,
    "`γ = c2γ`" if `T_elap ≤ 2T_ref`, else "`γ = c3γ`". "The constants `c1`, `c2`, and `c3` are
    selected so that `c3 ≤ c2 ≤ c1`. Based on preliminary analysis, we fix these values to **0.9, 0.7,
    and 0.5**, respectively. We note that a different setting results in negligible performance
    changes, as long as the selected values are appropriately spaced and ensure a decreasing γ."
  - **Stochastic adjustment strategy** (§III-B): "we insert a **two-state Markov chain** [38] and
    maintain a nonzero probability of selecting the action that is discarded during the previous
    deterministic decision step." The adjustment probability `p` is obtained from an **indifferent
    point `p_indiff`**, derived via PSO where an exact solution is unavailable: "we use the Particle
    Swarm Optimization (PSO) [39] approach to derive the probability values to be associated to the
    deterministic decisions of the scheduler", "Without loss of generality, we built the stochastic
    adjustment on top of the ECF scheduler as an example and refer to the stochastically adjusted ECF
    as **ECF-A**."
  - **Deployment stage (Algorithm 4 "Peekaboo")**, exact thresholds: "If `q̂` is close to 1 (i.e., `q̂` is
    larger than the boundary `BD1`), we behave almost deterministically by letting **`p = 0.9`**.
    Similarly, if `q̂` is close to 0, we choose **`p = 0.1`**… If `q̂` does fall in between the boundaries
    `BD1` and `BD0`, we use `p = p_indiff`. We set **`BD1` and `BD0` to 70% and 30%**, respectively,
    based on our extensive empirical observations." Re-learning trigger: "if `|q̂_deploy,wt − q̂_wt| >
    q̂_th` … `goto(Learning)`"; "Based on preliminary experiments, we found **`q̂_th = 17.5%`** to be a
    suitable threshold."
  - Learning overhead quantified: "We allocate **4 MB learning overhead** in each learning round, which
    is equivalent to **4-8 seconds in the emulated networks** depending on the path characteristics, and
    **0.5-1.4 seconds in real networks**."

- **13. ML/DRL usage (exact variant)**
  - **Yes.** The variant is a **contextual Multi-Armed Bandit (MAB) solved with LinUCB** — explicitly
    *not* deep RL and *not* a neural network. Quoted: "we tackle this problem using an online learning
    based on **contextual MAB theory** [13]"; "we adopt the **LinUCB algorithm** [44] to derive how
    Peekaboo deterministically selects between transmit and wait actions. **LinUCB adopts a ridge
    regression** [45] to evaluate the expected reward for a particular action `a` at time `t`, given
    the feature vector `x_t`. It then applies an **Upper Confidence Bound (UCB)** [46] to the
    estimation…"
  - Chosen deliberately over heavier RL: "The lightweight approach decreases the algorithm's reaction
    time but sacrifices the accuracy [12]. To mitigate the trade-off, we propose and incorporate a
    stochastic adjustment strategy to improve the algorithm accuracy."
  - **Network architecture (layers, neurons): NOT REPORTED and not applicable** — LinUCB is a linear
    ridge-regression model with an explicit UCB exploration bonus, parameterised by `A_a` (`d×d`) and
    `b_a` (`d×1`) with `d = 6`; there are no hidden layers or neurons to report.
  - One component *is* solved with a metaheuristic: the indifferent probability `p_indiff` is found with
    **Particle Swarm Optimization (PSO)**.
  - For contrast, the paper's nearest ML prior art is **RELES** ("a neural adaptive multipath scheduler
    based on deep reinforcement learning. RELES applies **Deep Q-Network (DQN)**"), which Peekaboo
    explicitly could **not** compare against: "the authors do not provide open source code of their
    implementation and we could not obtain the code from the authors either. Further, the paper does
    not offer sufficient information for us to reproduce the work. It is, therefore, **not possible to
    compare Peekaboo against it**."

- **14. Simulator / testbed**
  - **Both: a container-based emulation *and* a real-network deployment. No ns-3.**
    - Emulation: "We use **Mininet** [51] as the emulation environment, since it can emulate a real
      network stack using Linux containers **avoiding simplifications of simulation models**." Path
      parameters are set with "the Linux traffic control tool **NetEM** [52]". Repetitions: "To ensure
      statistical significant results, for each path configuration, we run **120 repetitions for each
      scheduler**." Design-space exploration uses "the experimental design principle, **WSP (Wooton,
      Sergent, Phan-Tan-Luu) algorithm**, to distribute the design parameters equally across the
      experiments, based on uniform random sampling of the input design parameters [53]… We use WSP to
      generate **100 distinct path configurations**."
    - Adaptivity stress test: "we examine a network where bandwidth, OWD, RTT variation and random loss
      rates change **every 60 seconds for 3000 seconds**."
    - Real: "We deploy an MPQUIC server in a European capital, and the MPQUIC client is locally on a
      laptop in the same city… using both a WiFi access point and an LTE network", five scenarios,
      "repeating the experiment **120 times for each scheduler** at each file size"; reported real
      dynamicity in Table IV (e.g. Residence: WiFi RTT variation 8.8% / loss 0.02%, LTE 9.7% / 0.03%;
      Library 1: WiFi 15.8% / 0.41%, LTE 11.2% / 0.19%).

- **15. Traffic model**
  - **Two applications: file download and real-time streaming.**
    - File download: "Inspired by [36]… we evaluate the download completion times." Emulation learning
      chunk "a 2 MB data chunk"/"2MB file download completion times"; design-space work uses file
      downloads; real-network downloads "of different file sizes, i.e., **256KB, 512KB, 2MB, and 4MB**".
      Preliminary insight experiments "repeats such downloads **100 times**".
    - Real-time streaming: "the application regularly sends equally spaced messages. The application has
      a deadline for the messages, and we evaluate the percentage of messages that arrive before the
      deadline and the delay of these late messages that arrive after the deadline. For example, to
      mimic real-time streaming with a bitrate of **2 Mbps, we regularly send messages composed of 8
      QUIC packets of 1000 bytes. Each message is spaced by 33 milliseconds.** We also assume the
      deadline is equal to the spacing, which is 33 milliseconds [36]." Evaluated at **1 Mbps and
      2 Mbps**; "we stream 20 MB of data for each scheduler".
  - Dynamicity levels as in field 1 (loss 0–3%, RTT variation 0–16%).

- **16. Baselines (exact names as the paper names them)**
  - "we consider **RR, minRTT, BLEST, and ECF** as the closest relevant state-of-the-art schedulers to
    motivate Peekaboo's design and evaluation in the rest of the paper."
    - **`RR`** — "A common baseline for multipath scheduler evaluation is the **Round-Robin (RR)**
      scheduler algorithm, which cyclically transmits packets over each path, as long as there is space
      in the Congestion Window (CWND)."
    - **`minRTT`** — "the minRTT scheduler, the default algorithm in MPTCP [16] and MPQUIC [14],
      prioritizes transmission on the path with the lowest estimated Round Trip Time (RTT) [30], after
      checking for space in the CWND."
    - **`BLEST`** — "the Blocking Estimation-based MPTCP Scheduler (BLEST) algorithm adds such
      estimation, introducing a wait mechanism [1]: If the network path with the highest RTT is the only
      one available, BLEST can decide to wait for the lowest RTT path to become available again, if it
      predicts that sending on the highest RTT path may block the receiver."
    - **`ECF`** — "The Earliest Completion First (ECF) algorithm also applies a similar wait mechanism,
      but the estimation is based on decreasing the idle time of the lowest RTT path [2]."
  - Additional internal/oracle comparators used in the design analysis:
    - **`LinUCB`** — the deterministic-learning-only variant ("the deterministic online learning,
      denoted as LinUCB").
    - **`ECF-A`** — "the stochastically adjusted ECF".
    - **`BSoA`** ("Best State of the Art") — "Given a path dynamicity level, BSoA would select the
      scheduler that provides the best performance, among several state-of-the-art schedulers… we note
      that it is not practical. However, also motivated by the potential gains obtained with BSoA, we
      design Peekaboo…"
  - **`RELES` is deliberately NOT a baseline** (no code available; see field 13).
  - **Peekaboo vs its own components** is also reported: `Peekaboo` (full), `LinUCB`-only, and
    `p = 0 / p = 1 / p = p_indiff` stochastic-factor variants.

- **17. Metrics**
  - **Median (and distribution of) file download completion time**; **percentage of messages arriving
    before the deadline** (real-time streaming) and **application delay** of all messages (ECDF, in ms,
    "if the message arrives before the deadline, the application delay is 0 ms"); **ECDF of the
    percentage performance improvement / "percentage of median gain"** over each baseline; **measured
    vs ideal bit rate ratio**; **percentage of trials**; **CPU and memory utilization** overhead;
    **learning overhead in MB / seconds**; adaptivity (performance under 60-second parameter changes).

- **18. Main results (exact numbers, quoted)**
  - **Headline (abstract)**: "Our results show that **Peekaboo outperforms the other schedulers by up to
    31.2% in emulated networks and up to 36.3% in real network scenarios.**" Conclusion repeats:
    "with the performance improvements of Peekaboo reaching by **up to 31.2% in emulated networks and up
    to 36.3% in real network scenarios**."
  - **File download, emulation, 100 WSP path configurations (Figure 7)**: "We observe that Peekaboo
    outperforms all the state-of-the-art schedulers." … "**compared to ECF, Peekaboo can achieve up to
    30% shorter download completion times for certain path configurations.** And we observe that those
    certain path configurations are mostly of low dynamicity levels, where the deterministic learning
    part of Peekaboo can provide the most benefit. Further, **the gains are over 20% for more than 50%
    of the path configurations.**"
  - **Real-time streaming, emulation (1 Mbps and 2 Mbps)** — "we evaluate the percentage of messages
    that arrive before the deadline": "**Peekaboo in total achieves 10.6% and 16.1% higher percentages
    for the messages that arrive before their deadline, compared with the best state-of-the-art
    scheduler at 1 Mbps and 2 Mbps, respectively.**"
  - **Deterministic learning alone (LinUCB) vs state of the art**: "for the 1.0% random loss case, we
    achieve **up to 28% shorter download completion time**. However, when the random loss rate is in the
    range of 2.0% to 3.0%, the performance benefits are not as significant, **with minRTT outperforming
    LinUCB when the random loss rate is 3.0%**… **minRTT outperforms online learning when the RTT
    variation rate is 16.0%.**"
  - **Stochastic adjustment proof of concept**: "**ECF-A outperforms the best state-of-the-art algorithm
    by providing a 17% median reduced download time**" (medium dynamicity on both paths); "when the
    dynamicity level is low… the stochastic factor of 1 offers the best performance. However, as we
    increase the dynamicity levels, the stochastic factor that offers the best performance varies, and
    the value generally decreases. **When the dynamicity level is the highest, the stochastic factor of
    0 offers the best performance.**"
  - **Adaptivity (parameters changing every 60 s for 3000 s)**: "**we achieve up to 26.4% shorter median
    completion times than ECF.** We can see that the performance gains over the state-of-the-art
    schedulers is slightly less as compared to Figure 7. This is because, with rapid changes in network
    characteristics, Peekaboo needs to adapt regularly resulting in a learning overhead."
  - **Design-space exploration (heterogeneous → homogeneous, 9 dynamicity combinations)**:
    "**Peekaboo performs better than BLEST, ECF, and RR in around 80% of the whole design space, and
    better than minRTT in around 60% of the whole design space with more than 50% performance
    improvement for some path configurations.**" And in the high-dynamicity heterogeneous corner:
    "Peekaboo converges back to the same policy of minRTT in the heterogeneous case due to the high
    dynamicity. As a result, they perform similarly (i.e., the points are in the **0.9-1.1** range)".
    Overall: "Peekaboo performs better than or similar to the best state-of-the-art scheduler across the
    examined design space."
  - **Real networks, file download (120 repetitions per scheduler per size)**: "we observe that
    **Peekaboo can reduce file download completion times, which can reach up to 36.3% in the 4MB file
    download case at the Residence scenario, compared to the best state-of-the-art scheduler.** However,
    we also observe the performance of Peekaboo is only slightly better than minRTT at Library 1 and 2
    when, e.g., downloading the 2MB file. This is because Peekaboo can adapt to the policy of minRTT in
    that scenario when detecting the high dynamicity."
  - **Real networks, real-time streaming (2 Mbps)**: "**Peekaboo achieves up to 15.1% higher percentage
    for messages that arrive before the deadlines compared with the best state-of-the-art scheduler**";
    "Peekaboo can always guarantee more messages arriving before the deadline at different scenarios.
    This is because Peekaboo essentially sets the function of packet delay as its reward and the
    real-time streaming scenario has a higher requirement on packet delay compared to the file
    download."
  - **Overhead**: "**Peekaboo incurs negligible runtime overhead**, as both learning and scheduling
    algorithm phases have low complexity. We profiled Peekaboo's CPU and memory utilization comparing it
    to the other schedulers, without noticing significant penalty in CPU and memory usage."
  - **Motivational measurement (the gap Peekaboo fills)**: on ECF at medium dynamicity, "ECF-A has
    `P1 = 0.73` probability to wait but also `1−P1 = 0.27` probability to transmit the packet on the
    slower path (i.e., Path 1)"; and BLEST/ECF's failure mode: "**when the dynamicity level is high,
    minRTT becomes the best choice, since BLEST and ECF overuse the lossy and delay varying Path 2.**"

- **19. Limitation**
  - **Authors' stated limitations (Section VI, "LIMITATIONS")**, quoted:
    - Online-only learning caps the applicable scenario space: "**in mobility scenarios the speed at
      which the network changes can surpass the learning speed achieved through online learning.** This
      can be even more difficult when there is not enough traffic for Peekaboo to learn the mobility
      scenario." Proposed remedy (future work): "it is possible to incorporate **offline learning**…
      The downside of offline learning is that once the offline traffic used for learning deviates from
      the current online traffic, it will lack a new learning outcome due to the amount of data required
      and the convergence time."
    - Generality of the action set / reward beyond today's apps and links: "we expect there to be a
      significant number of vertical applications in the upcoming 5G era, where **the exploited action
      and reward in this work (i.e., mainly targeting at heterogeneous networks and existing
      applications) will need to be extended** in order to support a wide range of applications, as well
      as link characteristics. For example, when interfacing with **tactile Internet** applications
      [56], the hard real-time performance should be guaranteed. In that case, robustness is more
      important than extra data and battery usage. Thus, the action set can have redundancy
      characteristics, e.g., packet duplication or FEC [57], etc. The reward should also be modified so
      that it can be mathematically proven to have a delay bound."
    - Missing MPQUIC features: "**Peekaboo currently does not explore stream prioritization capabilities
      in MPQUIC**, a feature that has been shown to improve performance [58]. We plan to extend the work
      in this direction and with multi-streaming."
    - Fixed to two paths by assumption: "For simplicity, in this work we assume two paths (i.e., WiFi and
      cellular)… the use of Peekaboo can be straightforwardly extended to the case of more than two
      paths" (asserted, not demonstrated).
  - **Methodological limitations I observe from the text**:
    - **No congestion-control disclosure**: the CC algorithm used in the emulation and real
      experiments is never named, so the results cannot be attributed to the scheduler independently of
      the CC — even though Peekaboo consumes CWND directly (field 10).
    - **The action set excludes the "both paths available" case** — those decisions are delegated to
      minRTT. So the learned component only ever arbitrates the *wait-vs-transmit-on-slow-path* choice;
      the reported gains are attributable to that narrow arbitration plus the stochastic adjustment.
    - **The most convincing ablation is missing**: the paper compares Peekaboo to LinUCB-only and to
      stochastic-factor sweeps, but the `p_indiff` value is derived with PSO *offline beforehand* per
      dynamicity level, and in deployment `p_indiff` is only *estimated*; the paper concedes "although
      the estimation error exists, it does not result in any significant performance penalty" without
      quantifying that error.
    - **Learning overhead is a real cost**: 4 MB per learning round (4–8 s of emulated transfer,
      0.5–1.4 s real), and the adaptivity results are explicitly worse than the static-best results
      ("the performance gains over the state-of-the-art schedulers is slightly less as compared to
      Figure 7… resulting in a learning overhead").
    - **No head-to-head with any deep-RL scheduler**: RELES is excluded for lack of code, so the claim
      that a lightweight contextual bandit beats DRL is untested.
    - The two paths are "partially disjoint" in emulation, so shared-bottleneck effects are not studied.

- **20. Research gap this suggests**
  - Peekaboo itself names the next gap: **online-only learning is too slow for mobility and too
    data-hungry for sparse traffic**, so it proposes **hybrid offline+online learning** as future work
    ("we plan to take the cooperation of both online learning and offline learning into account as our
    future work"). It also leaves open a reward that can be **proven to have a delay bound** and an
    action set with **redundancy (duplication/FEC)** for hard-real-time 5G/tactile applications.
  - Structurally, Peekaboo learns *only* the wait/transmit arbitration and hard-codes minRTT for the
    two-paths-available case, uses a **linear** LinUCB model with a hand-designed 6-feature vector, and
    a **single scalar** dynamicity threshold `q̂_th = 17.5%` for re-learning. An AI-native manager could
    plausibly learn the full action space, the feature representation, and the change-detection
    threshold end-to-end — and would need to do so per-slice across >2 access technologies, which
    Peekaboo only asserts.
  - For the review: Peekaboo is the reference point where multipath scheduling becomes an **online
    learning problem** (contextual bandit) rather than an analytic rule, and it also supplies the
    cleanest statement of *why* static schedulers fail — path **dynamicity level**, not just path
    heterogeneity, determines which policy is optimal.

- **21. Best URL actually retrieved, and full text vs abstract**
  - **URL actually used for extraction:**
    `https://web.archive.org/web/20231119135805id_/https://oda.oslomet.no/oda-xmlui/bitstream/handle/10642/9989/JSAC_Multipath_Scheduler.pdf`
    (Internet Archive Wayback Machine snapshot, 2023-11-19, of the OsloMet ODA repository copy —
    `application/pdf`, 4,305,855 bytes, **15 pages**, PDF `Producer: pdfTeX-1.40.18`,
    `CreationDate: Tue Feb 2 12:40:28 2021 CET`). This byte size matches the NVA/OSLOMET
    `OpenFile` artifact `76859cb8-81cb-40e9-a814-f1328c8fbd05` (`name: JSAC_Multipath_Scheduler.pdf`,
    `size: 4305855`, `publisherVersion: AcceptedVersion`), confirming it is the same accepted version.
  - **FULL TEXT** (author-accepted manuscript; not the IEEE typeset version).
  - Resolution chain (for reproducibility): Unpaywall reported `is_oa: true` with repository copies at
    `https://hdl.handle.net/10642/9989` and `http://hdl.handle.net/10852/83680`; both handles resolve
    (Handle API) to `https://nva.sikt.no/registration/0198cc44c194-6dd6687c-71fa-4145-8e87-0438ce368da6`
    (Norwegian National Vitus Archive); the NVA API returned the two `OpenFile` artifacts but
    `https://api.nva.unit.no/download/public/<fileId>` returns HTTP 403 `{"message":"Forbidden"}` for
    both; the original ODA/Brage bitstream URLs now redirect to the handle proxy; OpenAIRE
    (`https://api.openaire.eu/search/publications?doi=10.1109/JSAC.2020.3000365`) exposed the historical
    ODA bitstream path, and the Wayback CDX API
    (`https://web.archive.org/cdx/search/cdx?url=oda.oslomet.no&matchType=domain&filter=original:.*9989.*`)
    confirmed archived `200 application/pdf` snapshots, from which the file was fetched.
  - Other dead ends tried: arXiv (no Peekaboo preprint), KTH/Karlstad DiVA (record `diva2:1475066` exists
    at `https://kau.diva-portal.org/smash/record.jsf?pid=diva2%3A1475066` but DiVA now serves an
    **Anubis** bot-protection challenge to non-browser clients, and
    `https://kau.diva-portal.org/smash/get/diva2:1475066/FULLTEXT01.pdf` returns HTTP 404).

---

### GCLR: GNN-Based Cross Layer Optimization for Multipath TCP by Routing

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  - Authors: **Ting Zhu, Xiaohui Chen, Li Chen, Weidong Wang, Guo Wei** — "Department of Electronic
    Engineering and Information Science, University of Science and Technology of China, Hefei 230027,
    China" (corresponding author: Xiaohui Chen).
  - Year / Venue: **2020**, *IEEE Access*, vol. 8, pp. 17060–17070. Verified via Crossref:
    `TITLE: GCLR: GNN-Based Cross Layer Optimization for Multipath TCP by Routing`,
    `issued: [2020]`, `container-title: IEEE Access`, `volume: 8`, `page: 17060-17070`.
  - DOI: **`10.1109/ACCESS.2020.2966045`** (verified via Crossref; the PDF itself prints "Digital
    Object Identifier 10.1109/ACCESS.2020.2966045", "Received December 24, 2019, accepted January 8,
    2020, date of publication January 13, 2020, date of current version January 28, 2020").
  - **Peer-reviewed journal article, gold open access (CC-BY)** — Unpaywall reports
    `is_oa: true`, `loc[publisher] https://ieeexplore.ieee.org/ielx7/6287639/8948470/08957071.pdf`,
    `version=publishedVersion, license=cc-by`; OpenAlex reports `oa_status: gold`.

- **1. Number and type of paths**
  - GCLR is **not** a fixed WiFi/LTE-style access-technology scheduler; it targets **multi-hop
    datacenter/WAN topologies** where an MPTCP connection can span many subflows and many physical
    links. Topologies used: "the directly connected network, the National Science Foundation Network
    (**NSFNet**), and the **US Backbone Network** in fig.6", plus a "6-node network topology in fig.1".
  - Subflow counts evaluated: "MPTCP connections with **2 and 3 subflows**" for the model study, and
    "**4-subflow connections** are set as the experimental group" for the *connection-arbitrary*
    generalisation test.
  - Heterogeneity is over **link** properties, not access technologies: "topology parameters `x_l`
    including **bandwidth, delay, and packet loss rate** are randomly set."
  - The motivating problem is subflow asymmetry and overlap: "existing multipath routing algorithms and
    network modeling techniques are facing the challenges of **subflow asymmetry due to network
    heterogeneity**, thus cannot handle routing optimization problems comprehensively"; and "in complex
    topologies such as the NSFNet, there are more links in subflows, and various **overlapped links**
    exist."

- **2. Network architecture**
  - **SDN-controlled network with MPTCP endpoints. No proxy, no middlebox, no 5G core.**
    "the system is composed of the **real network** and the **SDN controller**"; "**SDN is deployed
    among switches in data centers**, it separates control planes and data planes to enable network
    programmability through flexible rules. Moreover, the availability of SDN has been extended to
    routers in WANs. In this paper, SDN is applied to provide a global view of the whole network and the
    further control of connections using the **OpenFlow** protocol [47], [48]." Controller: "Floodlight
    v1.2 is used as the SDN controller in the cross layer optimization."
  - Four SDN-controller modules: "the **topology explorer** module, **routing generator** module, **GNN
    model**, and **decision maker**." Routing instructions are pushed as flow tables: "decision maker
    chooses the optimal one for multipath routing and sends the configurations to the routers and
    switches in the network by **flow table**."
  - MPTCP endpoints run a **modified MPTCP kernel**: "The **MPTCP kernel is modified so that it can
    communicate MPTCP-level information with the Linux userspace through kernel logs.**"

- **3. Transport protocol**
  - **MPTCP**, kernel **v0.89**: "installed with **MPTCP kernel v0.89** as the most widely used MPTCP
    kernel version", on Ubuntu 14.04 LTS. The paper also notes "traditional TCP is a special case of
    MPTCP and can be regarded as an MPTCP connection with only one subflow, so the model in this paper
    also works when routing for traditional TCP connections."
  - Not MPQUIC, not CMT-SCTP, not ATSSS.

- **4. Scheduler location**
  - **Not a transport-layer packet scheduler.** GCLR's control logic lives in the **SDN controller
    (network layer, userspace)**, with a kernel-side telemetry hook:
    "The GNN model is implemented with **Tensorflow in Linux userspace**."
  - The four modules run in the controller; the data-plane switches/routers receive OpenFlow flow-table
    entries. The MPTCP kernel is modified only to export MPTCP-level information to userspace.
  - **This is a cross-layer routing/path-management system, not a per-packet scheduler.** The paper is
    explicit: "we focus on cross layer optimization at the **network layer**", and it criticises
    transport-only approaches: "the MPTCP stack has very limited knowledge of the underlying network to
    adopt efficient routing decisions. However, the advantages of MPTCP cannot be fully utilized by
    relying only on the traditional transport layer information, and useful network information on other
    layers need to be considered."

- **5. Scheduler inputs**
  - Two matrix inputs, quoted: "The input of the model includes **link information `x_l` from network
    topology** and **subflow information matrix `x_s` from the MPTCP connection**."
    - `x_l` — per-link properties: "`x_l = [bw_1 bw_2 … bw_|L| ; de_1 de_2 … de_|L| ; lo_1 lo_2 … lo_|L|]`",
      i.e. "**bandwidth `bw_i`, delay `de_i`, and packet loss rate `lo_i` are considered as link
      properties**", for "`|L|`, the number of links in the network topology".
    - `x_s` — subflow/route information: "since the number of subflows in an MPTCP connection and the
      number of links that a subflow passes are variable, they are set as parameters"; the routing
      generator "provides subflow information `x_s` for the model".
  - Collected by the topology explorer "to collect and update various networking feedback from switches
    and routers in **real-time**".
  - Hidden states are initialised from these matrices: "`h_s^0 = [x_s, 0, …, 0]`" and
    "`h_l^0 = [x_l, 0, …, 0]`".
  - **NOT inputs**: no SRTT/CWND/send-buffer/receive-buffer/queue-occupancy signal is fed to the model.
    The paper asserts what link states *should* contain ("We expect that link state vectors contain link
    information such as delay, packet loss rate, **link utilization**, etc, and path state is expected to
    contain the information of end to end connection parameters like **RTT, throughput, packet loss
    rate**, etc") but the implemented model uses only bandwidth, delay and loss.

- **6. Path metrics used**
  - **Bandwidth, delay, packet-loss rate** (the three link features), aggregated to path level by fixed
    rules, quoted:
    - Delay: "the delay of `s_i` is the sum of each link that `s_i` passes, which can be expressed as
      `de_{p_i} = Σ_{j=1}^{|p_i|} de_{p_i^j}`."
    - Bandwidth: "the bandwidth is determined by the **minimum** value of `bw_i^j`, which is
      `bw_{p_i} = min(bw_{p_i^j})`."
    - Loss: "the packet loss rate follows the **multiplication** rule, which is
      `lo_{p_i} = 1 − Π_{j=1}^{|p_i|} (1 − lo_{p_i^j})`."
  - Connection-level: "the throughput of the MPTCP connection is equal to the **sum of throughput of all
    the subflows** in this connection: `tp_c = Σ_{s_i ∈ c} tp_{s_i}`."
  - The predicted quantity is **expected throughput** `tp_c` for a given (topology, multipath route)
    pair. No energy, cost, jitter or delay-variation metric is used.

- **7. Scheduling decision**
  - Action space = **which set of multipath routes / subflows to install for the MPTCP connection**,
    chosen from a candidate set: "when there comes a transmission request from the network, according to
    the network state updated by the topology explorer, the routing generator generates a **routing
    candidate set** of the two hosts based on classic routing algorithms, greedy algorithms, and random
    algorithms."
  - Selection procedure: "routes in the candidate set will be sent to the GNN model to predict the
    corresponding expected throughput, then the results will be sent to the **decision maker** module";
    "based on the prediction of various routing strategies by the GNN model, decision maker **chooses
    the optimal one for multipath routing** and sends the configurations to the routers and switches in
    the network by flow table."
  - "In the routing generator module, the number of subflows should be a **parameter** to test the
    optimal subflow number of the MPTCP connection."
  - Not a per-packet path assignment, not a split ratio: it is **route/subflow-set selection**, i.e.
    `argmax` predicted throughput over the candidate route set.

- **8. Packet-level or flow-level scheduling**
  - **FLOW-LEVEL / path selection / routing** — explicitly *not* packet-level scheduling. The action is
    a routing configuration (flow-table entries + subflow set) for an MPTCP connection, and the
    optimisation target is `tp_c`, the connection's expected throughput. The paper contrasts itself with
    packet schedulers in its related work ("In [18], a scheduler for MPTCP is proposed based on Deep
    Reinforcement Learning… [19] LSTM and DRL…") and positions its contribution at the network layer.
  - **Important for the review: GCLR must not be counted as a packet scheduler alongside BLEST/ECF/
    Peekaboo.** It is a routing cross-layer optimiser.

- **9. Reordering handling**
  - **NOT REPORTED.** GCLR defines no reordering penalty, no receive-buffer/ATD term, no HoL-blocking
    mitigation, and no retransmission policy. The only mention of reordering is background motivation
    for why multipath reassembly matters: "This is mainly because **MPTCP needs to reassemble the
    out-of-ordered data into a complete and orderly one at the receiver**" (in the context of why extra
    subflows can reduce throughput). No penalty term, buffer term, or window term appears anywhere in
    the model or system design.
  - Note also that the paper's shared-bottleneck discussion ("In a bottleneck link, bandwidth has
    limits both subflows") is about throughput, not reordering.

- **10. Congestion-control interaction**
  - **NOT REPORTED** as an explicit mechanism. The paper names no CC algorithm (LIA/OLIA/BALIA/wVegas/
    Cubic/BBR are absent) and describes no CC interaction policy.
  - The only CC-adjacent statement is that coupling is *why* subflow states are interdependent, and is
    used to justify the graph model rather than to couple with a controller: "due to the data sequence
    number mechanism shared by all MPTCP subflows and **the coupled transmission control algorithms**, we
    can acknowledge that the state of each subflow in an MPTCP connection is determined by the paths that
    each subflow passes."
  - Congestion control is otherwise treated as related work (e.g. its reference [19] "Experience-driven
    congestion control: When multi-path TCP meets deep reinforcement learning").

- **11. Objective**
  - Stated objective (abstract): "**To address these problems, in this paper, firstly, a novel Graph
    Neural Network (GNN) based multipath routing model is proposed to explore the complications among
    links, paths, subflows and the MPTCP connection on various topologies. Leveraging the GNN model,
    expected throughput can be predicted with given network topology and multipath routes, which can
    further be the guidance for optimizing the multipath routing.**"
  - Introduced contribution: "We propose **GCLR, a cross layer multipath routing optimization system**
    [that] can ascertain the potential nonlinear relationships among features…"
  - Method-goal: "it is significant for us to cover the optimal or near-optimal solution with a **small
    routing candidate set**"; "Benefit from GNN's fast single calculation time (**around 1 ms**), the
    number of routes in the candidate set can be large enough to cover potential optimal solutions."
  - Closing claim: "Evaluation results have shown that **GCLR can achieve significant throughput
    enhancement in multipath routing optimization.**"

- **12. Algorithm**
  - **Algorithm 1 — "MPTCP Network Model for Multipath Routing"** (message passing neural network),
    verbatim structure:
    - Input: `x_s`, `x_l`; Output: `h_s^T`, `h_l^T`, `o`.
    - Initial phase: `h_s^0 = [x_s, 0, …, 0]` for each subflow `s ∈ S`; `h_l^0 = [x_l, 0, …, 0]` for
      each link `l ∈ L`.
    - Message passing phase, `T` iterations: for each subflow, for each link,
      `h_s^t = RNN_t(h_s^t, h_l^t)`, `m̃_{s,l}^{t+1} = h_s^t`, `h_s^{t+1} = h_s^t`; then for each link
      `m_l^{t+1} = Σ m̃_{s,l}^{t+1}`, `h_l^{t+1} = U^t(h_l^t, m_l^{t+1})`.
    - Readout phase: `o = O(h_s^T, h_l^T)`.
    - Aggregator choice explained: "Information is aggregated through a **recurrent neural network
      (RNN)** for the iteration of subflows and through **summation** for links. For links, the order of
      subflows does not matter. But for subflows, sequential dependence between links in the same subflow
      caused by losses requires sophisticated message aggregation. So we use RNN here for it can record
      input sequence information."
    - Readout: "`O()` is a **multi-layer perceptron with appropriate activations**, it can finally
      calculate the feature vector of the graph based on the hidden state `h_s^T` and `h_l^T`."
  - **Two-stage operation**: "the GNN model is divided into the **off-line training stage** and the
    **on-line predicting stage**." Off-line: "samples in different topology, by different routing
    algorithms, and with different subflow numbers are collected to cover most application scenarios.
    Then, these samples are divided into a training set and a test set…"; metrics tracked are "the
    **smoothed mean squared error (MSE)** and the **person correlation (ρ)**." Online: "routes in the
    candidate set will be sent to the GNN model to predict the corresponding expected throughput, then
    the results will be sent to the decision maker module."
  - **Candidate-set generation** (part of the system, not learned): "the routing generator generates a
    routing candidate set of the two hosts based on **classic routing algorithms, greedy algorithms, and
    random algorithms**… greedy algorithms are used to search for an optimal route while controlling the
    size of the routing candidate set, random algorithms are applied to **maintain the diversity of the
    candidate set to avoid the algorithm getting trapped in a local optimum**."
  - **Selection**: `argmax` over predicted expected throughput (decision maker).

- **13. ML/DRL usage**
  - **Yes — but not DRL.** The variant is a **Graph Neural Network**, specifically a **Message Passing
    Neural Network (MPNN)**: "**Message Passing Neural Network (MPNN) [45] is a GNN framework, MPNN
    updates node representations by stacking multiple graph convolutional layers using synthesis
    methods. MPNN consists of two phases, which are the message passing phase and the readout phase.
    During the message passing phase, `T` times of spatial graph convolutions are performed, and hidden
    states of nodes are iterated through message [passing]**."
  - Components: `T` spatial graph convolutions; an **RNN** aggregator for subflow updates; **summation**
    aggregator for link updates; an **MLP** readout `O()`; implementation in **TensorFlow** in Linux
    userspace.
  - **Exact network architecture (number of layers, neurons, hidden dimension, learning rate, batch
    size): NOT REPORTED.** The paper says only "a multi-layer perceptron with **appropriate
    activations**" and does not state layer counts, unit counts, hidden-state dimension, or optimiser
    hyperparameters. Training duration is given: "The MPTCP model has been trained for **100k steps**".
  - Motivation for choosing GNN over CNN, quoted: "CNN has to traverse all the input orders of nodes,
    which leads to additinal overhead. As for GNN, it is designed for the structure of graphs, features
    can be propagated separately on each node, so that **the input order of nodes can be ignored**, and
    the inputs in different orders can come to the same output result."; "for GNN, the information of
    edges can be propagated along with the graph structure, that is to say, **the GNN model can learn
    the structural features of a graph**".
  - No DRL, no DQN, no actor-critic, no replay buffer anywhere in GCLR. (DRL appears only as cited
    related work: "[19] LSTM (Long Short Term Memory) and DRL are [used]…".)

- **14. Simulator / testbed**
  - **Container-based network emulation/simulation on a single server — not a real testbed.**
    - "The simulation environment is configured in a **Linux server with Intel i7-4790k with 8 CPU cores,
      16GB memory, and 300GB storage**. In order to support the MPTCP protocol, the operating system is
      **Ubuntu 14.04 LTS** and installed with **MPTCP kernel v0.89** as the most widely used MPTCP kernel
      version. The experimental network topologies are **simulated by Mininet 2.2.2**, and **Floodlight
      v1.2** is used as the SDN controller in the cross layer optimization. The **GNN model is
      implemented with Tensorflow in Linux userspace**."
    - "To ensure topological diversity, the directly connected network, the National Science Foundation
      Network (NSFNet), and the US Backbone Network in fig.6 are **simulated by Mininet**. Then,
      topology parameters `x_l` including bandwidth, delay, and packet loss rate are **randomly set**.
      Finally, we generate MPTCP connections by **Iperf** to collect training samples."
    - The paper calls this "the simulation platform" and "simulation results" throughout, so I record it
      as **Mininet/container emulation with an SDN controller**, explicitly labelled *simulation* by the
      authors — no real wireless links, no real operator network.
    - Repetition/scale: "We transmit data for **10 seconds** by MPTCP and calculate the average
      transmission rate"; training "100k steps"; test-set experiments for topology-arbitrary and
      connection-arbitrary generalisation.

- **15. Traffic model**
  - **Synthetic, generated by Iperf** — no web/video/DASH or real application traffic.
    "we generate MPTCP connections by Iperf to collect training samples. In the MPTCP connections,
    **communication peers, subflow numbers, and the route of each subflow `x_s` are randomly
    configured** to simulate all possible scenarios." For the routing evaluation: "**transmission
    requests are created randomly**" and "We transmit data for 10 seconds by MPTCP and calculate the
    average transmission rate." Subflow counts: 2, 3 (training/validation) and 4 (held-out
    experimental group).

- **16. Baselines (exact names as the paper names them)**
  - **`fullmesh`** — "the traditional MPTCP **fullmesh** algorithm. The fullmesh algorithm will exhaust
    all feasible subflows without considering the impact of subflow asymmetry on throughput."
    Comparison: "we compare the throughput difference among GCLR, fullmesh, and **the optimal solution
    obtained by traversal**" (the traversal-based optimum acts as an oracle).
  - **`ECMP`** — "**Equal-Cost Multi-Path (ECMP)** [12] are commonly applied for network routing in
    MPTCP… it is unrealistic to obtain the optimal solution for multipath routing. Therefore, we only
    compare the performance improvement of the GCLR with the traditional **ECMP** algorithm", evaluated
    on NSFNet.
  - Baselines are therefore **routing-level** (`fullmesh`, `ECMP`, traversal-optimum), not packet
    schedulers (no minRTT / RR / BLEST / ECF / DAPS anywhere in GCLR's evaluation).

- **17. Metrics**
  - **Throughput-prediction accuracy**: "the **smoothed mean squared error (MSE)** and the **person
    correlation (ρ)**"; MSE broken down "in terms of **subflow numbers and topologies**" (Table 1);
    MSE for generalization validation (Table 2); "the **average error** of the GNN model". Note: the
    paper writes "person correlation" for what is normally "Pearson correlation" — I quote as printed.
  - **Routing performance**: "the average transmission rate" / throughput, reported as a **throughput
    CDF** ("The throughput cumulative distribution function of GCLR, fullmesh, and the optimal value")
    and as **average throughput increase (%)** vs ECMP.
  - **Computational**: "GNN's fast single calculation time (**around 1 ms**)".
  - Lists the three quantities a tutorial reviewer will want: MSE, ρ, and % throughput gain.

- **18. Main result (exact numbers, quoted)**
  - **Model convergence and accuracy**: "In fig.7, the smoothed MSE drops rapidly in the first 3k steps
    and turns into a steady state, while the ρ value following the opposite trend. **After 100k steps,
    the smoothed MSE arrives at 0.016 and ρ reaches 0.994**, so we can conclude that the GNN model can
    provide accurate predictions for different MPTCP connections and be the guidance for multipath
    routing optimization."
  - **Subflow-number / topology sensitivity (Table 1, qualitative in the text)**: "in the same topology,
    the performance of the GNN model **slowly decreases as the subflow number increases**… the model has
    a very low MSE in the directly connected network, this is because it is a simple topology and has no
    overlapped subflows… As for complex topologies such as the NSFNet, there are more links in subflows,
    and various overlapped links exist, so **the MSE is a little bit higher but still acceptable** for
    multipath routing optimization." *(Tables 1 and 2 are typeset as figures in the PDF and their
    individual cells did not survive `pdftotext`; I therefore report only the values stated in prose.)*
  - **Generalization (topology-arbitrary and connection-arbitrary, Table 2)**: "Although the results in
    experimental groups are not as good as that in control groups, **they can still maintain MSE at a
    low level**, which is sufficient for throughput prediction in multipath routing decisions. The result
    for **connection arbitrary is not as good as that of topology arbitrary**, this is because the
    increase of subflow number brings the increase in the input dimension, but there is no corresponding
    treatment for that in the GNN model."
  - **GCLR vs MPTCP `fullmesh` (directly connected topology, 10 s transfers)**: "due to the ability of
    GCLR to predict the throughput of different subflow combinations, **the CDF curves of GCLR and the
    optimal value almost completely coincide, which exceed the traditional fullmesh algorithm a lot**…
    the performance of GCLR cannot reach the optimal value only at a few individual points, this is due
    to the prediction error of the GNN model. However, since **the average error of the GNN model is
    small (0.004)**, even though the optimal combination of subflows is not selected, the throughput of
    GCLR will not differ much from the optimal value."
  - **GCLR vs `ECMP` (NSFNet, random link parameters, random transmission requests)** — the headline
    routing number: "**GCLR has significantly improved performance compared with ECMP, with an average
    throughput increase of 14.57%.**"
  - **Speed**: "Benefit from GNN's fast single calculation time (**around 1 ms**), the number of routes in
    the candidate set can be large enough to cover potential optimal solutions."

- **19. Limitation**
  - **Authors' stated limitations**:
    - Connection-arbitrary generalization degrades with more subflows, and the model has no mechanism to
      handle it: "the increase of subflow number brings the increase in the input dimension, but **there
      is no corresponding treatment for that in the GNN model**."
    - No optimal solution is available in realistic topologies, so the comparison is weakened by
      necessity: "In complex topologies, the feasible multipath routes increase exponentially with the
      topology size, **it is unrealistic to obtain the optimal solution for multipath routing. Therefore,
      we only compare the performance improvement of the GCLR with the traditional ECMP algorithm.**"
    - Residual prediction error causes occasional suboptimal selection: "the performance of GCLR cannot
      reach the optimal value only at a few individual points, this is due to the prediction error of the
      GNN model."
    - The GNN is trained **offline and then frozen**: "our off-line learned GNN model can predict the
      expected throughput…", with generalization asserted rather than guaranteed ("a sufficient number of
      training samples can satisfy most scenarios at the on-line predicting stage").
  - **Methodological limitations I observe from the text**:
    - **Everything is Mininet-based simulation on one server with MPTCP kernel v0.89 on Ubuntu 14.04
      (2014-era stack)**; despite the "real network" module language, there is no real deployment, no
      real wireless, and no operator data. The paper itself calls the results "simulation results".
    - **Hyperparameters and architecture are essentially unreported** (MLP size/activations, hidden
      dimension, `T`, optimiser, learning rate), so the model is not reproducible from the paper — the
      paper even notes "appropriate activations" without specifying them.
    - **Tables 1 and 2 are presented as images**, so the per-cell MSE numbers are unavailable to text
      extraction; the per-topology/per-subflow conclusions are only qualitative.
    - **The evaluation compares against routing baselines only** (`ECMP`, `fullmesh`); there is no
      comparison against any MPTCP packet scheduler or against a DRL-based path-management approach,
      even though the paper cites several such works.
    - **Link parameters are "randomly set"** with no stated distribution or seed, and each configuration
      appears to be a single 10-second transfer ("We transmit data for 10 seconds by MPTCP"), with no
      reported repetition count or confidence intervals for the 14.57% figure.
    - **No reordering, buffer, energy, or fairness metric** is measured — only throughput and prediction
      error — so the claim of "cross layer optimization" is one-dimensional.
    - The candidate-set generator is heuristic (greedy + random) and its size is a free parameter; the
      reported accuracy/gain is conditional on that unspecified design.

- **20. Research gap this suggests**
  - GCLR is the **flow-level, routing-side** counterpart to the packet-level schedulers in this set, and
    it leaves a clean gap at the intersection of the two: it optimises *which routes/subflows* an MPTCP
    connection uses using **predicted throughput as the sole objective**, while BLEST/ECF/Peekaboo
    optimise *which path each packet takes* using instantaneous RTT/CWND/send-buffer state. **Neither
    side models the other's decision variable**, so an AI-native, cross-layer controller that jointly
    selects routes/subflow sets *and* per-packet scheduling policy — with reordering/buffer cost and
    delay constraints in the objective — is unaddressed by GCLR and by all three schedulers here.
  - GCLR also stops at **offline-trained, frozen inference** with a hand-designed feature set
    (bandwidth/delay/loss) and a heuristic candidate set. It explicitly names two open problems: no
    treatment of growing subflow count/input dimension, and no optimality oracle in realistic
    topologies. An AI-native manager would additionally need **online adaptation** to topology/state
    change (GCLR's model is static once trained), **generalisation guarantees** across unseen topologies
    (only MSE is reported), and **multi-objective** routing (GCLR reports throughput only).
  - Finally, GCLR's telemetry path — a **modified MPTCP kernel exporting MPTCP-level state to a
    userspace SDN controller via kernel logs** — is exactly the kind of in-band, kernel-log-based
    observability an AI-native network-management review should flag as fragile/non-scalable compared
    with modern streaming telemetry.

- **21. Best URL actually retrieved, and full text vs abstract**
  - **URL: `https://ieeexplore.ieee.org/ielx7/6287639/8948470/08957071.pdf`** (IEEE Xplore, the
    **gold-OA CC-BY published version**; this is also the `best_oa_location.pdf_url` reported by OpenAlex
    and the `openAccessPdf` reported by Semantic Scholar). Retrieved HTTP 200, `application/pdf`,
    1,339,096 bytes, **11 pages**, PDF Title "GCLR: GNN-Based Cross Layer Optimization for Multipath TCP
    by Routing".
  - Note on retrieval: the identical URL returned **HTTP 502** (an IEEE WAF interstitial) when called
    without a browser-like `User-Agent`. It succeeded only after first fetching
    `https://ieeexplore.ieee.org/document/8957071` with a desktop `User-Agent` into a **cookie jar** and
    replaying the PDF request with the same UA, cookie jar and a `Referer` header. Recorded here so the
    retrieval is reproducible.
  - **FULL TEXT** (published version, not a preprint).
  - Other sources checked: Unpaywall (`is_oa: true`, `publishedVersion`, `cc-by`, plus a DOAJ
    `submittedVersion` record at `https://doaj.org/article/ee4a1e5f8df9430fa34339093f30a5b2`); OpenAlex
    (`oa_status: gold`); scholar.archive.org (same IEEE PDF URL); DOAJ API (`doi:10.1109/access.2020.2966045`).

---

## Retrieved artefacts (this session)

All files live in
`/home/pouriaarefi/Documents/phd_network_ai_literature_review/multipath_scheduling/pdfs/`.
`*_layout.txt` is `pdftotext -layout` output; `*_flow.txt` is `pdftotext` reading-order output, which I
used for verbatim quote verification (the two-column `-layout` output interleaves columns and breaks
sentences mid-line).

| Paper | PDF | pages | `pdftotext -layout` | `pdftotext` (flow) |
|---|---|---|---|---|
| BLEST | `blest_ifip2016.pdf` | 9 | `blest_ifip2016.txt` | `blest_ifip2016_flow.txt` |
| ECF | `ecf_conext2017.pdf` | 13 | `ecf_conext2017.txt` | `ecf_conext2017_flow.txt` |
| Peekaboo | `peekaboo_jsac2020.pdf` | 15 | `peekaboo_jsac2020.txt` | `peekaboo_jsac2020_flow.txt` |
| GCLR | `gclr_access2020.pdf` | 11 | `gclr_access2020.txt` | `gclr_access2020_flow.txt` |

### URL list actually used (all four are FULL TEXT, none is ABSTRACT ONLY)

1. **BLEST** — `https://dl.ifip.org/db/conf/networking/networking2016/1570234725.pdf`
   (index: `https://dl.ifip.org/db/conf/networking/networking2016/index.html`)
2. **ECF** — `https://api.repository.cam.ac.uk/server/api/core/bitstreams/9f216be1-4124-4f10-bbad-137e912cc7ff/content`
   (Apollo item: `https://www.repository.cam.ac.uk/handle/1810/279112`)
3. **Peekaboo** — `https://web.archive.org/web/20231119135805id_/https://oda.oslomet.no/oda-xmlui/bitstream/handle/10642/9989/JSAC_Multipath_Scheduler.pdf`
4. **GCLR** — `https://ieeexplore.ieee.org/ielx7/6287639/8948470/08957071.pdf`

### Metadata verification endpoints used

- Crossref: `https://api.crossref.org/works/10.1109/IFIPNetworking.2016.7497206`,
  `https://api.crossref.org/works/10.1145/3143361.3143376`,
  `https://api.crossref.org/works/10.1109/JSAC.2020.3000365`,
  `https://api.crossref.org/works/10.1109/access.2020.2966045`
- OpenAlex: `https://api.openalex.org/works/doi:<doi>?mailto=research@example.org`
- Unpaywall: `https://api.unpaywall.org/v2/<doi>?email=research@example.org`
- Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=title,abstract,openAccessPdf,venue,year,externalIds`
- OpenAIRE (Peekaboo repository path): `https://api.openaire.eu/search/publications?doi=10.1109/JSAC.2020.3000365&format=json`
- Cambridge Apollo API (ECF): `https://api.repository.cam.ac.uk/server/api/discover/search/objects?query=ECF%20MPTCP%20scheduler`
- Wayback CDX (Peekaboo): `https://web.archive.org/cdx/search/cdx?url=oda.oslomet.no&matchType=domain&filter=original:.*9989.*`

## Cross-paper notes for the review (grounded only in the four texts above)

- **Naming caution on the "Lowest-RTT-First / Round-Robin" brief:** BLEST and ECF both benchmark against
  the MPTCP default scheduler, which they call **`minRTT`** (BLEST: "MPTCP's default minRTT scheduler";
  ECF: "Default … allocates traffic to a subflow with the smallest RTT"). **Neither BLEST nor ECF uses a
  Round-Robin baseline.** Round-Robin (**`RR`**) appears only in **Peekaboo**, which benchmarks `RR`,
  `minRTT`, `BLEST`, `ECF`.
- **Shared-baseline chain:** BLEST and ECF appear both as methods and as each other's baselines; Peekaboo
  benchmarks all three plus `RR`. This gives a clean 2016 → 2017 → 2020 progression from analytic
  estimator (BLEST) → analytic idle-time rule (ECF) → online contextual bandit (Peekaboo).
- **GCLR is not in that chain:** it is a **flow-level SDN routing/path-selection** system for MPTCP
  (Mininet + Floodlight + GNN, throughput-prediction-guided routing) whose baselines are `fullmesh`,
  `ECMP` and a traversal optimum. It should be classified separately from the packet schedulers.
- **ML progression:** BLEST = no ML (analytic + hand-tuned scalar `δ_λ`); ECF = no ML (analytic +
  hand-tuned `β` and variance margin `δ`); Peekaboo = contextual MAB / LinUCB with PSO-tuned
  `p_indiff` (linear model, `d = 6` features); GCLR = offline-trained GNN/MPNN with TensorFlow
  (architecture under-specified in the paper).
