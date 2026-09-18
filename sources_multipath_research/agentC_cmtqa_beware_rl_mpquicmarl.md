# Agent C extraction — CMT-QA, BEMA ("BEWARE"), SATO, MPQUIC-MARL

Extraction performed per `EXTRACTION_SPEC.md` (hard anti-fabrication rules). Every statement below
comes from a document actually fetched in this session; anything not stated in the retrieved
document is written as `NOT REPORTED`. Retrieval date: this session.

**Retrieval-status summary**

| # | Paper | Status | Source actually read |
|---|-------|--------|----------------------|
| 1 | CMT-QA (IEEE TMC 2013) | **ABSTRACT ONLY** | IEEE Xplore landing page abstract (paywalled full text) |
| 2 | BEMA / "BEWARE" (IEEE TCOM 2016) | **ABSTRACT ONLY** | IEEE Xplore landing page abstract (paywalled full text) |
| 3 | SATO / RL-based Multipath Scheduling (IEEE WF-IoT 2022) | **ABSTRACT ONLY** (+ full Section I visible on the Xplore landing page) | IEEE Xplore landing page + author lab abstract page |
| 4 | Improved MPQUIC Scheduler based on MARL (IEICE E108.D, 2025) | **FULL TEXT** (5 pp., J-STAGE gold OA) | J-STAGE PDF |

**Full-text search effort for the three paywalled IEEE papers (all unsuccessful):** Crossref, Unpaywall
(`is_oa: false`, 0 OA locations for both DOIs), Semantic Scholar (`openAccessPdf.status = "CLOSED"`),
arXiv API (no preprints), OpenAIRE (`total: 1` record each, no fulltext instances), CORE (bot-blocked),
BASE (bot-blocked), scholar.archive.org / fatcat (blocked), DCU DORAS institutional repository
(0 results for CMT-QA), BUPT author page for Changqiao Xu (citation only, no PDF), Chiba University
lab publication list (`abst.php?paper=734` abstract page exists; the "pdf" entry next to this paper is
plain text with **no** href — the authors posted no PDF), HUST AI4LIFE lab page (no PDF for this paper),
researchmap (DOI only), ResearchGate (CAPTCHA), Google Scholar (403). No OA copy of these three exists
that I could obtain legitimately.

---

## 1. CMT-QA: Quality-Aware Adaptive Concurrent Multipath Data Transfer in Heterogeneous Wireless Networks

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Changqiao Xu, Tianjiao Liu, Jianfeng Guan, Hongke Zhang, Gabriel-Miro Muntean.
  **2013** (issue date November 2013; IEEE "Date of Publication: 30 August 2012").
  **IEEE Transactions on Mobile Computing**, vol. 12, no. 11, pp. 2193–2205.
  **DOI: 10.1109/TMC.2012.189**. Peer-reviewed journal article (Crossref `type: journal-article`);
  not a preprint. Verified from Crossref `https://api.crossref.org/works/10.1109/TMC.2012.189`.

- **1. Number and type of paths:** Heterogeneous wireless. The abstract states that mobile devices with
  multiple interfaces "can increase their throughput by making use of parallel transmissions over
  multiple paths and bandwidth aggregation", and motivates the work by "the different bandwidth and
  delay of the multiple paths". **Exact path count: NOT REPORTED** (abstract does not state how many
  paths, nor which radio technologies by name).

- **2. Network architecture:** Described only as "wireless heterogeneous networks" / delivery "in
  wireless heterogeneous networks" to multi-interface mobile devices. Whether there is a proxy,
  middlebox, or a multipath-capable server: **NOT REPORTED**.

- **3. Transport protocol:** **SCTP** — explicitly "enabled by the stream control transport protocol
  (SCTP)" and the solution "utilizes SCTP for FTP-like data transmission and real-time video delivery".
  This is **pre-MPTCP-standard Concurrent Multipath Transfer over SCTP (CMT-SCTP)**, not MPTCP; the
  abstract never mentions MPTCP. Exact CMT variant/flavour: **NOT REPORTED**.

- **4. Scheduler location:** **NOT REPORTED** (the abstract does not say kernel, userspace, proxy or
  server-side; no statement about where the decision logic runs).

- **5. Scheduler inputs:** Stated qualitatively only: "CMT-QA monitors and analyses regularly each
  path's data handling capability and makes data delivery adaptation decisions to select the qualified
  paths for concurrent data transfer." The exact signals (SRTT, cwnd, delivery rate, queue occupancy,
  loss rate, buffer estimates, BLEST-style penalisation, send buffer) are **NOT REPORTED**.

- **6. Path metrics used:** The abstract names, as motivation only, "the different bandwidth and delay
  of the multiple paths". The metrics the scheduler itself computes and compares are **NOT REPORTED**.
  (Per-path "data handling capability" is the only characterization given.)

- **7. Scheduling decision:** Two stated actions: (i) "select the qualified paths for concurrent data
  transfer", and (ii) "distribute data chunks over multiple paths intelligently and control the data
  traffic rate of each path independently". A formal action space (e.g. "path *i* for next segment",
  split ratio) is **NOT REPORTED**.

- **8. Packet-level or flow-level scheduling:** Described at **data-chunk level** — "distribute data
  chunks over multiple paths" (SCTP "chunks" are the protocol's transmission units), i.e. a
  packet/segment-level distribution mechanism plus per-path **rate control**, not a flow-level path
  selection scheme. The abstract states no segment-level formalism, so the precise granularity beyond
  "data chunks" is **NOT REPORTED**.

- **9. Reordering handling:** Yes, explicitly and centrally: "CMT-QA's goal is to mitigate the
  out-of-order data reception by reducing the reordering delay and unnecessary fast retransmissions",
  motivated by "the different bandwidth and delay of the multiple paths will determine data to be
  received out of order and in the absence of related mechanisms to correct this, serious
  application-level performance degradations will occur". It also "can effectively differentiate
  between different types of packet loss to avoid unreasonable congestion window adjustments for
  retransmissions". Whether a BLEST-style penalty term, receive-buffer limit, or ATD estimate is used
  is **NOT REPORTED**.

- **10. Congestion-control interaction:** The only stated interaction is loss-type differentiation to
  avoid "unreasonable congestion window adjustments for retransmissions" (i.e. the scheduler/CMT logic
  feeds back into cwnd behaviour). The specific congestion-control algorithm (this is pre-MPTCP, so
  LIA/OLIA/BALIA do not apply; standard SCTP AIMD is the presumption but is not stated): **NOT
  REPORTED**.

- **11. Objective:** Quoted verbatim: "CMT-QA's goal is to mitigate the out-of-order data reception by
  reducing the reordering delay and unnecessary fast retransmissions." The broader framing is
  "quality-aware adaptive" path qualification for "FTP-like data transmission and real-time video
  delivery".

- **12. Algorithm:** **NOT REPORTED** as a named algorithm. The abstract says only that CMT-QA
  "includes a series of mechanisms to distribute data chunks over multiple paths intelligently and
  control the data traffic rate of each path independently" and that it "monitors and analyses
  regularly each path's data handling capability".

- **13. ML/DRL usage:** **No ML/DRL is mentioned anywhere in the retrieved abstract.** (The retrieved
  text contains no reference to learning, reinforcement learning, or neural networks; the mechanism is
  described as monitoring/analysis-based. Because only the abstract was retrieved, this is an absence
  in the retrieved text, not a verified claim about the full paper.)

- **14. Simulator / testbed:** **Simulation** — "Simulations show how CMT-QA outperforms existing
  solutions in terms of performance and quality of service." The simulator's name, version, and
  topology, and whether any real testbed was used, are **NOT REPORTED**.

- **15. Traffic model:** Two application classes are named: "FTP-like data transmission and real-time
  video delivery". Traffic-generation parameters (file sizes, video codec/bitrate, duration) are
  **NOT REPORTED**.

- **16. Baselines:** Referred to only as "existing solutions" — **exact baseline names: NOT REPORTED**.

- **17. Metrics:** Referred to only as "performance and quality of service" (plus the qualitative
  reordering delay / fast-retransmission counts implied by the objective) — **exact metric list: NOT
  REPORTED**.

- **18. Main result:** No numbers are given in the abstract. Only the qualitative claim: "Simulations
  show how CMT-QA outperforms existing solutions in terms of performance and quality of service."
  **Exact figures: NOT REPORTED.**

- **19. Limitation:** No limitation is stated in the retrieved abstract. Methodological limitation I
  observe: the full text is paywalled and no OA copy exists, so the mechanism, baseline set, simulator
  and all quantitative results could not be verified; the abstract alone does not permit any
  comparison with modern learning-based schedulers.

- **20. Research gap this suggests (my analysis, not the paper's claim):** CMT-QA is a hand-tuned,
  heuristic, monitor-and-adapt scheme for CMT-SCTP: it defines *what* to adapt (path qualification,
  chunk distribution, per-path rate) but the retrieved text exposes no predictive or learning
  component, no formal objective function, and no quantified evaluation. This points to the gap that
  a DRL-based scheduler could learn the path-qualification/distribution policy from per-path signals
  instead of relying on fixed monitoring thresholds — a gap the AI-native network-management
  literature later fills. Confirming this requires the paywalled full text.

- **21. Best URL actually retrieved, and whether full text or abstract:** IEEE Xplore landing page
  **`https://ieeexplore.ieee.org/document/6291719`** (resolved from the DOI; retrieved through the
  text-extraction reader `https://r.jina.ai/https://ieeexplore.ieee.org/document/6291719`).
  **ABSTRACT ONLY.** The IEEE page additionally exposed only the **first paragraph of Section 1**
  (Introduction) before a "Sign in to Continue Reading" wall; that paragraph is used below only where
  explicitly labelled. An alternative abstract source (author lab page) does not exist for this paper;
  the BUPT author page `https://teacher.bupt.edu.cn/cqxu/en/lwcg/61175/content/3029.htm` lists the
  citation with no PDF.
  *From the visible first Introduction paragraph only:* "The stream control transmission protocol
  (SCTP) [5], [6], [7], with its multihoming feature [8] and SCTP's dynamic reconfiguration extension
  (mSCTP) [9] are very promising protocols to support efficient data transmission, including seamless
  handover in heterogeneous wireless networks."

---

## 2. Bandwidth-Efficient Multipath Transport Protocol for Quality-Guaranteed Real-Time Video Over Heterogeneous Wireless Networks

> **NAMING DISCREPANCY — read this first.** My brief called this paper **"BEWARE"** (suggested PDF name
> `beware_tcom2016.pdf`). The **retrieved publisher abstract names the proposed protocol "BEMA"
> ("bandwidth-efficient multipath streaming")** — quoted: "this paper proposes a bandwidth-efficient
> multipath streaming (BEMA) protocol". **"BEWARE" is a different, unrelated paper**: "BEWARE:
> Background Traffic-Aware Rate Adaptation for IEEE 802.11" (IEEE/ACM Transactions on Networking,
> DOI 10.1109/TNET.2011.2106140). Both names are recorded here per anti-fabrication rule 8; **I trust
> the IEEE TCOM landing-page abstract**, because it is the publisher record for DOI
> 10.1109/TCOMM.2016.2553138 and matches the title, venue, volume, issue, pages and author list
> exactly. **Do not cite this work as "BEWARE".**

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Jiyan Wu, Chau Yuen, Bo Cheng, Yuan Yang, Ming Wang, Junliang Chen.
  **2016** (issue date June 2016; IEEE "Date of Publication: 12 April 2016").
  **IEEE Transactions on Communications**, vol. 64, no. 6, pp. 2477–2493.
  **DOI: 10.1109/TCOMM.2016.2553138**. Peer-reviewed journal article (Crossref `type:
  journal-article`); not a preprint. Verified from
  `https://api.crossref.org/works/10.1109/TCOMM.2016.2553138`.

- **1. Number and type of paths:** Heterogeneous wireless access networks with "different radio
  interfaces (e.g., cellular and Wi-Fi)"; the problem is "concurrent video transmission over multiple
  wireless access networks" to multihomed terminals. **Exact path count: NOT REPORTED.**

- **2. Network architecture:** Multi-homed mobile terminals "concurrently receive multimedia contents
  with different radio interfaces"; the target is "streaming high-quality real-time video to
  multihomed terminals in heterogeneous wireless networks". Whether a proxy, middlebox, or
  multipath-capable server is involved: **NOT REPORTED**.

- **3. Transport protocol:** Described only as multipath video transport: "conventional multipath
  protocols are throughput-oriented" and the paper's proposal is "a bandwidth-efficient multipath
  streaming (BEMA) protocol". **The abstract does not name SCTP/CMT or MPTCP — the specific transport
  protocol is NOT REPORTED from the retrieved abstract.** (The visible first Introduction paragraph
  likewise names no transport protocol; it only lists "wireless local area networks (802.11 family),
  cellular networks (UMTS, HSDPA, LTE), and broadband wireless networks (LTE and WiMAX)" and says
  state-of-the-art terminals "are equipped with multiple radio interfaces to concurrently receive data
  through parallel wireless access networks".)

- **4. Scheduler location:** **NOT REPORTED.**

- **5. Scheduler inputs:** No network-state signal list is given. The scheduler is characterized as
  content-aware: "priority-aware data scheduling and forward error correction-based reliable
  transmission", with a "joint Raptor coding and data distribution framework". The per-path signals
  consumed (SRTT/RTT, cwnd, delivery rate, loss, buffer estimate, penalty) are **NOT REPORTED**.

- **6. Path metrics used:** Only "path asymmetry" is referenced, and only as something BEMA mitigates:
  "The proposed BEMA is able to effectively mitigate packet reordering and path asymmetry to improve
  network utilization." No explicit metric set (RTT, bandwidth, loss, energy, cost) is stated:
  **NOT REPORTED**.

- **7. Scheduling decision:** The stated mechanisms are "priority-aware data scheduling" and a "joint
  Raptor coding and data distribution framework" aimed "to achieve target video quality with minimum
  bandwidth consumption". A formal action space (path index per segment, split ratio, redundancy
  allocation) is **NOT REPORTED**.

- **8. Packet-level or flow-level scheduling:** The scheme operates on video **data** units — "video
  data are scheduled in a content-agnostic fashion" is the criticised status quo, and BEMA performs
  "priority-aware data scheduling" plus a "data distribution framework", which indicates data-unit
  (packet-level) scheduling rather than flow-level path selection. The abstract does not state the
  exact granularity: **exact mechanism NOT REPORTED**.

- **9. Reordering handling:** Stated as an outcome, not a mechanism: "The proposed BEMA is able to
  effectively mitigate packet reordering and path asymmetry to improve network utilization."
  Reordering detection method, penalty term, receive-buffer limit, or ATD estimate: **NOT REPORTED**.

- **10. Congestion-control interaction:** **NOT REPORTED** — the abstract names no congestion-control
  algorithm and no interaction mechanism (it only says "conventional multipath protocols are
  throughput-oriented" as a criticism).

- **11. Objective:** Two quoted objectives: (i) "we present a mathematical framework to formulate the
  delay-constrained distortion minimization problem for concurrent video transmission over multiple
  wireless access networks"; and (ii) "we develop a joint Raptor coding and data distribution framework
  to achieve target video quality with minimum bandwidth consumption".

- **12. Algorithm:** The two named components are (a) a **mathematical framework for the
  delay-constrained distortion minimization problem**, and (b) a **joint Raptor coding and data
  distribution framework**, plus forward error correction-based reliable transmission. No named
  solver/optimisation algorithm, no pseudo-code level detail: **exact algorithm NOT REPORTED**.

- **13. ML/DRL usage:** **No ML/DRL is mentioned anywhere in the retrieved abstract** (no learning,
  RL, or neural-network terms appear; the method is optimisation- and coding-theoretic). Because only
  the abstract was retrieved, this is an absence in the retrieved text, not a verified claim about the
  full paper.

- **14. Simulator / testbed:** **Emulation, not a real testbed** — quoted: "We conduct performance
  evaluation through extensive emulations in Exata involving real-time H.264 video streaming."
  I.e. the **Exata** network emulator with real H.264 video. No live WiFi/LTE testbed is claimed. Node
  counts, topology and emulation parameters are **NOT REPORTED**.

- **15. Traffic model:** **Real-time H.264 video streaming** ("quality-guaranteed real-time video",
  "extensive emulations in Exata involving real-time H.264 video streaming"). Video bitrate, resolution,
  duration, and number of streams are **NOT REPORTED**.

- **16. Baselines:** Referred to only as "the existing multipath protocols" — **exact baseline names:
  NOT REPORTED**.

- **17. Metrics:** Quoted exactly: "video peak signal-to-noise ratio, end-to-end delay, bandwidth
  utilization, and goodput".

- **18. Main result:** No numbers appear in the abstract. Only: "Compared with the existing multipath
  protocols, BEMA achieves appreciable improvements in terms of video peak signal-to-noise ratio,
  end-to-end delay, bandwidth utilization, and goodput." **Exact figures: NOT REPORTED** (the word
  "appreciable" is not quantified in the retrieved abstract).

- **19. Limitation:** No limitation is stated in the retrieved abstract. Methodological limitation I
  observe: the evaluation is **emulation in Exata**, not a real heterogeneous wireless deployment, and
  the abstract reports only directional improvements without any numeric comparison; the full text is
  paywalled with no OA copy, so distortion model, Raptor parameters, baseline set and all figures could
  not be verified.

- **20. Research gap this suggests (my analysis, not the paper's claim):** BEMA attacks multipath video
  quality with a *static, model-based* optimisation (delay-constrained distortion minimisation + Raptor
  FEC) whose parameters are derived offline from a mathematical framework; the retrieved text shows no
  runtime learning or adaptation to changing path conditions, and the evaluation is emulation-only.
  This suggests the gap of an online, learning-based per-packet scheduler that adapts redundancy and
  path assignment to measured path state, and of evaluation on real heterogeneous wireless testbeds
  rather than an emulator. Confirming this requires the paywalled full text.

- **21. Best URL actually retrieved, and whether full text or abstract:** IEEE Xplore landing page
  **`https://ieeexplore.ieee.org/document/7451207`** (resolved from the DOI; retrieved through
  `https://r.jina.ai/https://ieeexplore.ieee.org/document/7451207`). **ABSTRACT ONLY.** The IEEE page
  exposed only the abstract plus the **first paragraph of Section I (Introduction)** before a "Sign in
  to Continue Reading" wall. Alternative records consulted that contain no full text:
  `https://www.semanticscholar.org/paper/9b5c1a0386af543d5c267aa72c34b0632b69e72e` (S2 reports
  `"status": "CLOSED"`), `https://api.unpaywall.org/v2/10.1109/TCOMM.2016.2553138` (`is_oa: false`).

---

## 3. A Reinforcement Learning-based Multipath Scheduling for Heterogeneous Wireless Networks (protocol name: **SATO**)

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Thanh Trung Nguyen, Minh Hai Vu, Phi Le Nguyen, Phan Thuan Do, Kien Nguyen.
  **2022** (conference dates 26 October – 11 November 2022; "Date Added to IEEE Xplore: 22 June 2023").
  **2022 IEEE 8th World Forum on Internet of Things (WF-IoT)**, Yokohama, Japan — conference paper
  (Crossref `type: proceedings-article`; researchmap records it as 研究論文（国際会議プロシーディングス）
  / peer-reviewed international conference proceedings).
  **DOI: 10.1109/WF-IoT54382.2022.10152217** — matches the IEEE Xplore document id **10152217** given
  in my brief. **Author list confirmed to include Kien Nguyen.** Verified from
  `https://api.crossref.org/works/10.1109/WF-IoT54382.2022.10152217`, from the IEEE Xplore landing
  page, and from the author's researchmap record `https://researchmap.jp/kien/published_papers/46413583`
  (which independently gives the same venue, year, DOI and ISBN 9781665491532). Not a preprint.
  **Venue/year/DOI are consistent across all three sources — no disagreement to report.**

- **1. Number and type of paths:** Heterogeneous wireless networks. The abstract speaks of "multipath
  transport protocols such as MPTCP and MPQUIC" and "heterogeneous wireless networks". **Exact path
  count and the radio technologies used are NOT REPORTED** in the retrieved abstract (and are not
  stated in the visible Section I).

- **2. Network architecture:** Stated only at the node level: "a node equipped with SATO can capture
  the environmental changes and select transmission paths". Whether there is a proxy, middlebox,
  5G core element or multipath-capable server: **NOT REPORTED**.

- **3. Transport protocol:** **MPQUIC** — from the visible Section I: "this paper proposes a
  Reinforcement Learning-based Scheduling Algorithm for Transport Optimization (SATO) that considers
  many different network characteristics in MPQUIC." The abstract situates the work in the wider class
  of "multipath transport protocols such as MPTCP and MPQUIC"; the protocol SATO itself is presented
  as "a novel Reinforcement learning-based multipath transport protocol named SATO". No MPTCP-v0/v1 or
  MPQUIC version number is given: **version NOT REPORTED**.

- **4. Scheduler location:** **NOT REPORTED** (kernel, userspace, server, client, or proxy is not
  stated in the retrieved abstract or visible Section I).

- **5. Scheduler inputs:** Only the qualitative statement that SATO "considers many different network
  characteristics in MPQUIC". The exact signal list (SRTT/RTT, cwnd, delivery rate, queue occupancy,
  loss rate, buffer estimate, penalisation) is **NOT REPORTED**. Note (baseline, **not** SATO):
  the visible Section I says of Peekaboo that it "learns at runtime the decision to make when this path
  has no congestion window (CWND) availability".

- **6. Path metrics used:** **NOT REPORTED.**

- **7. Scheduling decision:** "select transmission paths based on an appropriate policy to optimize
  QoS" — i.e. a **path-selection** action. The formal action space (e.g. path *i* for the next segment,
  or a split ratio) is **NOT REPORTED**.

- **8. Packet-level or flow-level scheduling:** The retrieved text describes **path selection** for
  multipath communication ("select transmission paths based on an appropriate policy"). Whether the
  decision is applied per packet/segment or per flow is **NOT REPORTED** in the retrieved abstract and
  visible Section I.

- **9. Reordering handling:** **NOT REPORTED for SATO.** The visible Section I mentions head-of-line
  blocking only when describing **baselines**: "Based on minRTT, BLEST [3] and ECF [4] are non-learning
  schedulers that have been designed to address the Head-of-line blocking problem, but they cannot
  adapt to heterogeneous networks." No reordering mechanism, penalty term, receive-buffer limit or ATD
  estimate is stated for SATO.

- **10. Congestion-control interaction:** **NOT REPORTED for SATO.** The only CC-related statement in
  the visible Section I concerns the baseline Peekaboo (CWND availability, quoted in field 5 above).

- **11. Objective:** Quoted verbatim: "By leveraging the self-learning ability of reinforcement
  learning, a node equipped with SATO can capture the environmental changes and select transmission
  paths based on an appropriate policy to optimize QoS." Framing motivation quoted: "One of the most
  critical issues in dealing with the multipath transmission is appropriately scheduling the pathways
  in order to guarantee QoS."

- **12. Algorithm:** Named as "a novel Reinforcement learning-based multipath transport protocol named
  SATO" ("Reinforcement Learning-based Scheduling Algorithm for Transport Optimization"). **The
  specific RL algorithm (Q-learning, DQN, bandit, policy gradient, …), its state/reward formulation and
  hyper-parameters are NOT REPORTED** in the retrieved abstract or visible Section I.

- **13. ML/DRL usage:** **Yes — reinforcement learning is central** ("By leveraging the self-learning
  ability of reinforcement learning…"). The **exact DRL variant is NOT REPORTED** in the retrieved
  text; no network architecture (layers, neurons) is stated. The visible Section I notes the design was
  "Motivated by the learning effectiveness of Peekaboo" (a multi-armed-bandit baseline), but does not
  state which RL algorithm SATO itself uses — I do **not** infer one.

- **14. Simulator / testbed:** **Both simulation and a real deployment are claimed**, but neither is
  specified: "Our evaluation results show that SATO improves the QoS by 10%-15% in simulation and 12%
  in a real deployment compared to the state-of-the-art algorithm." **The simulator name/version and
  the testbed hardware/radio configuration are NOT REPORTED** in the retrieved abstract.

- **15. Traffic model:** **NOT REPORTED** (no application, file size, video, or synthetic traffic
  model is stated in the retrieved abstract).

- **16. Baselines:** The quantitative comparison is against "the state-of-the-art algorithm" — **that
  phrase is all the abstract says; it is not named.** The visible Section I names the related
  schedulers it positions against: **minRTT** ("the default scheduler" for MPQUIC), **BLEST** and
  **ECF** ("non-learning schedulers"), and **Peekaboo** ("a state-of-the-art learning-based algorithm
  based on multi-armed bandit"). Section I also explains the motivation gap: "However, as the available
  paths get more homogeneous in terms of RTT, its performance converges to the performance provided by
  minRTT, BLEST, and ECF." **I do not infer that the unnamed "state-of-the-art algorithm" in the
  result sentence is Peekaboo** — the retrieved text does not say so.

- **17. Metrics:** Stated only as **QoS** ("improves the QoS by 10%-15%…"). The constituent metrics
  (latency, throughput, loss, etc.) are **NOT REPORTED** in the retrieved abstract.

- **18. Main result:** The only quantitative claim in the retrieved text, quoted exactly: "Our
  evaluation results show that SATO improves the QoS by 10%-15% in simulation and 12% in a real
  deployment compared to the state-of-the-art algorithm." No per-metric figures, no absolute values,
  no confidence intervals: **further numbers NOT REPORTED**.

- **19. Limitation:** No limitation is stated by the authors in the retrieved abstract. Methodological
  limitations I observe: (i) the headline result is a single aggregate "QoS" improvement of 10–15%
  (simulation) / 12% (deployment) against an **unnamed** "state-of-the-art algorithm", so the
  comparison is not independently checkable; (ii) no metric decomposition is given; (iii) no simulator,
  testbed, traffic model or path count is specified in the retrievable text; (iv) the full text is
  paywalled with no OA copy, so the RL algorithm, state/reward design and evaluation methodology could
  not be verified at all.

- **20. Research gap this suggests (my analysis, not the paper's claim):** This paper is itself an
  early RL-based multipath scheduler, and the extractable evidence shows the classic weaknesses of that
  generation: an RL scheduler whose algorithm, state and reward are not visible in the accessible
  record, evaluated against an unnamed state-of-the-art baseline, with results reported as a single
  aggregate QoS percentage. The suggested gap is the need for **reproducible, fully specified DRL
  schedulers with named baselines, decomposed metrics (per-path latency/throughput/loss), and
  openly available evaluation environments** — and, since Peekaboo-style single-agent bandit learners
  converge to minRTT/BLEST/ECF when paths become homogeneous (as the paper's own Section I argues), for
  scheduling policies that retain an advantage under both heterogeneous *and* homogeneous path
  conditions. Confirming this requires the paywalled full text.

- **21. Best URLs actually retrieved, and whether full text or abstract:**
  1. IEEE Xplore landing page **`https://ieeexplore.ieee.org/document/10152217`** (retrieved through
     `https://r.jina.ai/https://ieeexplore.ieee.org/document/10152217`) — **ABSTRACT + the complete
     Section I (Introduction)**; the remainder of the article is behind the paywall ("You do not have
     access to this PDF").
  2. Author lab abstract page **`https://www.s-lab.nd.chiba-u.jp/achievements/abst.php?paper=734&lang=jp`**
     (Kien Nguyen lab, Chiba University) — same abstract text, independently confirming it.
  **Overall: ABSTRACT ONLY** (plus Section I of the introduction). The paper's own lab publication list
  (`https://www.s-lab.nd.chiba-u.jp/achievements/paper_list.php?area=COM&lang=jp`) shows "[ Abstract |
  pdf]" for this entry where **"pdf" carries no hyperlink** — the authors posted no PDF, consistent
  with IEEE copyright.

---

## 4. An Improved MPQUIC Scheduler Based on Multi-Agent Reinforcement Learning

- **Authors / Year / Venue / DOI / peer-reviewed or preprint:**
  Chenchi Liu, Ao Zhan, Chengyu Wu (corresponding author, jerry916@zstu.edu.cn), Zhengqiang Wang.
  Affiliations: School of Computer Science and Technology, Zhejiang Sci-Tech University; School of
  Information Science and Engineering, Zhejiang Sci-Tech University; School of Communications and
  Information Engineering, Chongqing University of Posts and Telecommunication.
  **2025** (issue August 2025; "Manuscript received October 28, 2024", "Manuscript revised January 22,
  2025", "Manuscript publicized February 13, 2025").
  **IEICE Transactions on Information and Systems**, Vol. **E108–D**, No. **8**, pp. **1011–1015**,
  August 2025, published as a **LETTER** in the **Regular Section**.
  **DOI: 10.1587/transinf.2024EDL8090**. Peer-reviewed journal letter (Crossref `type:
  journal-article`), **not** a preprint. Verified from
  `https://api.crossref.org/works/10.1587/transinf.2024EDL8090` (which returns year 2025-08-01,
  vol E108.D, issue 8, pages 1011-1015) and from the J-STAGE landing page. Funding: "National Key
  Laboratory of Science and Technology on Space Microwave, No. HTKJ2022KL504016".

- **1. Number and type of paths:** **Heterogeneous**, 2 paths per client: quoted — "Each client is
  equipped with two network interfaces (WiFi and LTE), allowing for concurrent communication with
  the server through both interfaces" and
  "three clients are connected to the server through two distinct paths". So the evaluated topology is
  **3 clients × 2 paths (WiFi + LTE)**; the scheduler design supports *i* paths per client
  (state includes `CWND_1, SRTT_1, …, CWND_i, SRTT_i`, and "the size of the action space A is equal to
  the number of paths").

- **2. Network architecture:** Server-centric, no proxy: "multiple clients are connected to an MPQUIC
  server"; "The server simulates access points and base stations linked via wired connections."
  "The scheduler in the server plays a pivotal role in determining the optimal path for the transmission
  of each client's packets." Each client reaches the server over its two interfaces ("nication with the
  server through both interfaces").

- **3. Transport protocol:** **Multipath QUIC (MPQUIC)** — an "extension of Google's Quick UDP Internet
  Connections (QUIC) protocol". Implemented using the ns-3 MPQUIC extension: "we implemented the
  proposed scheduler on the NS-3 platform, leveraging the NS3-MPQUIC codebase introduced in [11]"
  (ref. [11] = S. Shu, W. Yang, J. Pan, and L. Cai, "A multipath extension to the QUIC module for
  ns-3", Proc. 2023 Workshop on ns-3, pp.86–93, 2023). No MPQUIC version number given.

- **4. Scheduler location:** **Server side, in userspace/simulation** — "The proposed scheduler is
  implemented on the server side with a Deep Q-Network (DQN) agent for each client"; "The scheduler in
  the server plays a pivotal role in determining the optimal path for the transmission of each client's
  packets."

- **5. Scheduler inputs:** Explicit state vector, quoted:
  `s_t^j = (a_{t−1}^j, r_{t−1}^j, CWND_1,t, SRTT_1,t, · · · , CWND_i,t, SRTT_i,t)` — i.e. **the
  agent's previous action, the previous reward, and per-path congestion window (CWND) and smoothed RTT
  (SRTT)**. "These parameters are monitored every 50 milliseconds" (the letter continues: "and the
  state s_t^j is defined as follows"). SRTT is computed as a weighted
  moving average, `SRTT = (1 − λ) × SRTT + λ × R′`, with λ "conventionally set to 1/8", where R′ is the
  most recently measured RTT. Throughput and SRTT are log-normalised into
  `th_norm` and `SRTT_norm` for the state/reward (Eqs. 3–4, with small constant σ to avoid invalid log
  input).

- **6. Path metrics used:** **CWND, RTT/SRTT, throughput** (normalised, in the reward), and **packet
  loss** (via the ACK-success constraint and via the three loss-rate scenarios: 0.1%, 0.5%, 0.9%).
  No energy or monetary cost metric is used. Bandwidth appears as a constraint (`C1`: "the sum of
  bandwidths allocated to each client must not exceed the total available bandwidth B_max"
  [typeset in the letter as "Bmax", i.e. B with subscript "max"]).

- **7. Scheduling decision:** **Per-packet path index.** Quoted: "Every 50 milliseconds, the agent
  selects the action to choose the transmission path for the data packet. The action of Agent j at time
  t is represented as a_t^j, and the size of the action space A is equal to the number of paths."
  Exploration: "a random path is selected with a probability of ε for each packet". So the action space
  is exactly {path 1, …, path i} per client agent; no split-ratio action.

- **8. Packet-level or flow-level scheduling:** **PACKET-LEVEL** (per-segment path assignment) — the
  agent picks the transmission path for the data packet, with a decision cadence of 50 ms and ε-greedy
  random path selection per packet. Not flow-level and not merely path selection.

- **9. Reordering handling:** **NOT REPORTED** — the letter does not describe a reordering-detection
  mechanism, penalty term, receive-buffer limit or ATD estimate for its own scheduler. Reordering
  appears only implicitly via the reward's SRTT term and via the baselines it compares against (BLEST
  is the blocking-estimation-based MPTCP scheduler in ref. [4]; the letter's own Introduction notes
  that "other existing schedulers, such as ECF [3], which operates on the estimated earliest completion
  time, and BLEST [4], which relies on congestion estimation, also have limitations").

- **10. Congestion-control interaction:** The scheduler **observes** the per-path congestion window
  (CWND is a state input, and CWND is defined as "the amount of data which the sender can send into the
  network before receiving the corresponding acknowledgment (ACK) frames"), but the **congestion-control
  algorithm name (Cubic, BBR, etc.) and any explicit CC interaction mechanism (e.g. waiting for CWND
  availability, as in BLEST/Peekaboo) are NOT REPORTED**. The reward imposes a penalty of −1 when the
  per-client ACK/bandwidth constraints are unmet, which indirectly couples scheduling to congestion
  behaviour, but no CC algorithm is named.

- **11. Objective:** Quoted verbatim: "The primary objective of the proposed scheduler is to elevate
  the QoS indicators for each client." Also: "our objective is to address the following issue: how to
  design a multi-agent MPQUIC scheduler for optimizing multi-path transmission and enhancing the QoS
  for each client?" The reward operationalises this: "we define the reward function as follows: …
  r_j = th_norm_j − SRTT_norm_j, if C1 and C2 are met, −1 otherwise", designed "to incentivize the agent
  to enhance throughput while reducing latency and packet loss".

- **12. Algorithm:** **Multi-agent DQN (one DQN agent per client) with an LSTM front-end.** Details from
  the letter: "we establish a DQN agent for each client, providing scheduling strategies for packet
  transmission at 50 milliseconds"; "each agent … extracts key state inputs from the network
  environment, encompassing prior actions, received rewards, and critical paths' metrics. This
  information is conveyed to a Long Short-Term Memory (LSTM) network, which captures the temporal
  nuances before feeding into the online network to determine Q-values for potential actions. The action
  with the highest Q-value is selected…"; "To ensure training stability, a target network is
  implemented"; "The sequence of states, actions, and rewards is archived in the Replay Buffer";
  ε-greedy action selection (arg max Q_θ(s_t^j, a_t^j) with probability 1 − ε, random path with
  probability ε); target Q-value computed "by summing the immediate reward with the discounted maximum
  Q-value"; parameters updated by a loss function; ε updated at the end of each training episode based
  on step number and a predefined decay rate (ε "initially set as 1"). Constraints in the reward:
  "C1: Σ_{j=1}^{n} B_j ≤ B_max, C2: received ACK". Hyper-parameters: discount factor **γ = 0.6**,
  decay rate **0.996**, learning factor **μ = 0.001**, batch size **32** ("the number of episodes
  randomly drawn from the replay buffer each time learning occurs"), "Step indicates the step size for
  updating the policy network, set to 50", state-monitoring and decision interval **50 ms**, initial
  ε = 1. **Network layer/neuron counts are NOT REPORTED.**

- **13. ML/DRL usage:** **Yes — Multi-Agent Reinforcement Learning (MARL) with Deep Q-Networks.** Exact
  variant: **DQN per client (independent agents), with an LSTM for temporal feature extraction, an
  online network and a target network, and experience replay.** Network architecture (number of layers,
  neurons per layer, LSTM size) is **NOT REPORTED**. The letter cites ref. [8] (Gronauer & Diepold,
  "Multi-agent deep reinforcement learning: A survey") for MARL.

- **14. Simulator / testbed:** **SIMULATION only — no real testbed.** Quoted: "We implemented the
  proposed scheduler on the NS-3 platform, leveraging the NS3-MPQUIC codebase introduced in [11]. To
  facilitate a reinforcement learning-based scheduling strategy, we integrated PyTorch into NS-3 using
  Pybind11 [12]". Test environment: "We conducted 200 trials for each scenario on an Ubuntu 22.04 system
  equipped with a 4-core CPU and 16 GB of RAM." Topology: "The simulation environment, depicted in
  Fig. 1, consists of a multi-path network connected to an MPQUIC server. The server simulates access
  points and base stations linked via wired connections. Additionally, three clients are connected to
  the server through two distinct paths." Path parameters are listed in Table 1 (bandwidth/latency per
  path); **note: the numeric contents of Table 1 are not present in the PDF text layer** (the table is
  vector graphics, not extractable text), so the per-path bandwidth/delay values could not be read; the
  body text states the envelope: "the bandwidth range of 5M to 11 Mbps".

- **15. Traffic model:** **Bulk file download (synthetic), multi-client.** Quoted: "In each trial,
  three clients simultaneously downloaded a 5 MB file from the server." Network conditions: "we conduct
  two main experiments under different network conditions: low packet loss rate of 0.1%, medium packet
  loss rate of 0.5%, and high packet loss rate of 0.9%, to evaluate (1) the time required to complete
  the file download; (2) the instantaneous throughput during the download process". No web/video/real
  application traffic model is used.

- **16. Baselines:** Named exactly: **"MinRTT, BLEST, ECF, Peekaboo, and MuLeS"** — quoted: "we
  compared it against existing algorithms—MinRTT, BLEST, ECF, Peekaboo, and MuLeS within a simulated
  multi-client environment." (Per the letter's references: MinRTT is "the current default scheduler for
  MPQUIC"; ECF = "An MPTCP path scheduler to manage heterogeneous paths" [3]; BLEST = "Blocking
  estimation-based MPTCP scheduler for heterogeneous networks" [4]; Peekaboo = "Learning-based multipath
  scheduling for dynamic heterogeneous environments" [5]; MuLeS = "A multi-client learning-based MPQUIC
  scheduler" [7]. ReLeS [6] is cited as related work but is not listed among the compared baselines.)

- **17. Metrics:** **Download/complete time** (seconds) and **throughput** (Mbps; instantaneous and
  average). Quoted: "We first focus on evaluating the time required for clients to download a 5 MB file
  as a performance metric" and "we conducted an analysis of the instantaneous throughput during the
  download process"; "the average download time and average throughput" are analysed in the parameter
  study.

- **18. Main result (exact numbers, quoted):**
  - Download time reduction vs the other schedulers: "When the packet loss rate is 0.1%, our scheduler
    reduces the average download time for clients by 8–9.6% compared to other schedulers. At a packet
    loss rate of 0.5%, the reduction is 8.8–13.7%, and at a packet loss rate of 0.9%, it is 6.3–12.6%."
  - Throughput increase: "when the packet loss rate was 0.1%, the average throughput for clients
    increased by 10.4–21%. At a packet loss rate of 0.5%, it increased by 13.5–19.5%, and at a packet
    loss rate of 0.9%, it increased by 12.8–24.1%."
  - Parameter study / ablation: at 0.1% loss, "the combination of a discount factor of 0.4 and a decay
    rate of 0.994 can achieve the best performance in terms of download time and throughput, with an
    average download time of 8.82 s and an average throughput of 4.86 Mbps"; at 0.5% loss, "a discount
    factor of 0.6 combined with a decay rate of 0.996 allows the scheduler to achieve optimal
    performance, with an average download time of 14.16 s and an average throughput of 4.33 Mbps",
    whereas "the combination of a discount factor of 0.4 and a decay rate of 0.994 shows a significant
    decline in performance, with the average download time increasing to 14.52 s and the average
    throughput decreasing to 3.96 Mbps"; at 0.9% loss, "the combination of a discount factor of 0.6 and
    a decay rate of 0.996 still performs the best, with an average download time of 15.32 s and an
    average throughput of 3.91 Mbps". Overall conclusion: "we have determined that a discount factor of
    0.6 with a decay rate of 0.996 is the optimal parameter combination."
  (No confidence intervals, p-values, or variance statistics are reported.)

- **19. Limitation:** As stated by the authors: (i) the bandwidth envelope is narrow and deliberately
  conservative — "Although the bandwidth range of 5M to 11 Mbps may appear conservative in the context
  of current network capabilities, this selection is deliberately made to align with the parameters
  utilized in [11]"; (ii) scope of future work — "our future work will extend to broader bandwidth and
  latency ranges to study the scheduler's behavior under more advanced network environments."
  Methodological limitations I observe: (i) **simulation only** (ns-3), with no real WiFi/LTE testbed,
  despite the paper's framing around real multi-interface devices; (ii) a very small scenario — 3
  clients, 2 paths each, one 5 MB bulk download, with a hard-coded upper bound on clients
  (`Σ B_j ≤ B_max` is defined over n clients but n is not explored); (iii) results are presented as
  ranges across figures with **no statistical dispersion** (no CIs/std-dev) even though "200 trials"
  were run, so the reported 8–9.6% / 10.4–21% ranges cannot be tested for significance; (iv) the
  comparison with the learning baselines (Peekaboo, MuLeS) is shown only graphically, with no
  per-baseline numbers in the text; (v) **no reordering / head-of-line-blocking assessment** even though
  the schedulers it compares against (BLEST, ECF) were designed specifically for that problem, and a
  per-packet multi-path scheduler on heterogeneous WiFi/LTE paths is exactly where reordering matters;
  (vi) the state uses only CWND and SRTT per path — no loss-rate, delivery-rate, queue-occupancy, cost
  or energy signal — so the agent cannot directly observe the packet-loss condition that differentiates
  its three scenarios; (vii) as a 5-page letter there is no complexity/scalability analysis for the
  claimed multi-client scaling, and the per-client agent count grows linearly with clients; (viii) the
  numeric path-parameter table (Table 1) is not machine-readable in the PDF, limiting reproducibility.

- **20. Research gap this suggests (my analysis, not the paper's claim):** The letter establishes that
  per-client multi-agent DQN scheduling beats MinRTT/BLEST/ECF/Peekaboo/MuLeS on bulk-download time and
  throughput in a 3-client ns-3 scenario, but it leaves measurable gaps: (a) evaluation on **real
  heterogeneous testbeds** rather than ns-3 with a Pybind11/PyTorch bridge; (b) **reordering- and
  HoL-blocking-aware** scheduling objectives for per-packet MPQUIC scheduling across WiFi/LTE — this
  work optimises throughput-minus-SRTT and never measures reordering; (c) **richer state** (delivery
  rate, loss rate, queue occupancy, per-path available bandwidth) instead of CWND+SRTT only; (d)
  **scalability** with many concurrent clients and the multi-agent non-stationarity that comes with
  independent per-client learners sharing `B_max`; (e) **statistical rigour** (CIs, significance tests,
  per-baseline numbers) and reproducibility artefacts (path parameters, code) — this letter's Table 1
  is not even text-extractable; (f) **energy/cost-aware** multipath scheduling objectives, absent here;
  and (g) extending the scheduler beyond bulk download to **real-time video / interactive traffic**,
  where latency and jitter rather than mean throughput dominate QoS.

- **21. Best URL actually retrieved, and whether full text or abstract:** J-STAGE open-access PDF
  **`https://www.jstage.jst.go.jp/article/transinf/E108.D/8/E108.D_2024EDL8090/_pdf`** (HTTP 200,
  1,058,860 bytes, 5 pages) — **FULL TEXT**. Landing page
  `https://www.jstage.jst.go.jp/article/transinf/E108.D/8/E108.D_2024EDL8090/_article/-char/en`
  (Regular Section, IEICE Transactions on Information and Systems, Online ISSN 1745-1361, Print ISSN
  0916-8532). Bibliographic record verified at
  `https://api.crossref.org/works/10.1587/transinf.2024EDL8090`. Local copies: `pdfs/mpquic_marl_ieice2025.pdf`
  and `pdfs/mpquic_marl_ieice2025.txt` (produced with `pdftotext -layout`).

---

## Cross-paper notes for the review

1. **Protocol generations differ sharply across these four papers.** CMT-QA (#1) is **pre-MPTCP
   CMT-SCTP**; BEMA (#2) is a multipath video transport whose abstract does not name its transport at
   all; SATO (#3) targets **MPQUIC** (with MPTCP named as the wider class); the IEICE letter (#4) is
   **MPQUIC**. Any synthesis table must not present these as one "MPTCP family".
2. **Scheduling granularity is only verifiable for paper #4** (per-packet path index, 50 ms cadence).
   For #1 the abstract supports data-chunk-level distribution; for #2 and #3 the granularity is not
   stated in the retrieved text. Do not assert packet-level scheduling for #2/#3 from these sources.
3. **Only paper #4 is currently verifiable end-to-end** (full text, named baselines, exact numbers,
   named simulator). Papers #1–#3 are **ABSTRACT ONLY**: their mechanisms, baselines, simulators and
   figures are unverified, and any field marked `NOT REPORTED` above should be re-extracted if
   institutional access to IEEE Xplore becomes available.
4. **Naming risk:** the assigned label "BEWARE" for the IEEE TCOM 2016 paper is **wrong** — see the
   discrepancy box in section 2. The correct protocol name in the publisher abstract is **BEMA**.
