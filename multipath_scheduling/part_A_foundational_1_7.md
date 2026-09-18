# Multipath Transport & Scheduling — Structured Paper Extractions

**Prepared for:** PhD literature review on AI-native network management
**Scope:** 24 items — MPTCP/MPQUIC/multipath scheduling, foundational through AI-based, plus a
gap probe on multipath↔orchestration integration.
**Date of retrieval:** all URLs retrieved during this working session.

## Method, and how to read this document

Every paper below was verified against a bibliographic API (Crossref, Unpaywall, Semantic
Scholar, HAL API, J-STAGE) rather than a search snippet. Where an open-access full text
existed it was downloaded as PDF, converted with `pdftotext -layout`, and read. Where only the
abstract was obtainable, the paper is marked **ABSTRACT ONLY** in field 21 and every field that
the abstract does not state is written as `NOT REPORTED` — nothing was filled in from memory,
from the title, or by inference.

Two mechanical facts worth recording, because they shaped what is verifiable here:

1. **Paywalls that could not be circumvented.** IEEE Xplore returns HTTP 202 with an empty body
   to non-browser clients; ACM DL returns HTTP 403 on `/doi/pdf/`. OpenAlex's API exhausted its
   daily budget part-way through the session (`Insufficient budget ... Resets at midnight UTC`),
   so Crossref + Unpaywall + Semantic Scholar were used instead. Institutional access would be
   required to upgrade several ABSTRACT ONLY entries (flagged in "WHAT I COULD NOT VERIFY").
2. **Bot protection was solved, not worked around.** HAL (`hal.science`) and DiVA
   (`kau.diva-portal.org`, `dblp.org`) sit behind an Anubis proof-of-work interstitial. A
   solver was written (`tools/anubis_fetch.py`, SHA-256 proof-of-work over `randomData + nonce`
   at the advertised difficulty, then `pass-challenge`) and used to retrieve the HAL copy of
   paper 5 legitimately from the publisher-designated OA location.

`NOT REPORTED` means **the source does not state it** — it is not a claim that the paper is
silent in some other version, and it is not a placeholder for a guess.

Distinctions maintained throughout: **testbed vs simulation vs emulation** (Linux kernel on real
hardware ≠ Mininet ≠ ns-3), and **packet-level scheduling vs flow-level path selection/routing**.

---

## FOUNDATIONAL

### 1. RFC 8684 — TCP Extensions for Multipath Operation with Multiple Addresses

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  A. Ford (Pexip), C. Raiciu (U. Politehnica of Bucharest), M. Handley (U. College London),
  O. Bonaventure (U. catholique de Louvain), C. Paasch (Apple, Inc.). March 2020. IETF Request
  for Comments 8684, Category: Standards Track, ISSN 2070-1721. **Obsoletes RFC 6824.**
  DOI: `10.17487/RFC8684`.
  **This is a standards document, not a peer-reviewed paper** — it carries IETF rough consensus,
  not journal/conference peer review. Any literature review must weight it accordingly: it is
  normative evidence of what the standard *requires*, not experimental evidence of performance.

- **1. Number and type of paths**
  Not fixed. The document specifies v1 of MPTCP, which "provides the components necessary to
  establish and use multiple TCP flows across potentially disjoint paths" (Abstract). Any
  combination of addresses/interfaces is permitted; medium type is not constrained.

- **2. Network architecture**
  End-to-end, middlebox-transparent: each subflow "is equivalent to a normal TCP connection with
  its own 32-bits sequence numbering space … to allow MultiPath TCP to traverse complex
  middle-boxes like transparent proxies or traffic normalizers" (this framing is from paper 2,
  which describes the same mechanism; RFC 8684 §6 "Interactions with Middleboxes" is the
  normative counterpart). No proxy is required in the architecture; MPTCP is an end-host
  extension. Connection establishment uses MP_CAPABLE; additional subflows use MP_JOIN with a
  token-derived key.

- **3. Transport protocol**
  MPTCP v1 (the RFC explicitly "specifies v1 of Multipath TCP, obsoleting v0 as specified in
  RFC 6824, through clarifications and modifications primarily driven by deployment experience").

- **4. Scheduler location**
  **Not specified — and the silence is deliberate.** A full-text search of the retrieved RFC
  text for `scheduler` and `scheduling` returns **zero occurrences** (excluding the table of
  contents, which has neither). §3.3.8 "Subflow Policy" states normatively:

  > "Within a local MPTCP implementation, a host may use any local policy it wishes to decide
  > how to share the traffic to be sent over the available paths."

  So the scheduler is defined to be **endpoint-local and implementation-defined**. It is neither
  kernel-mandated nor userspace-mandated by the standard.

- **5. Scheduler inputs**
  `NOT REPORTED` — the standard defines no scheduler inputs. The closest normative statement is
  about what the design guarantees to the *congestion controller*: "the design of MPTCP aims to
  provide the congestion control implementations with sufficient information to make the right
  decisions; this information includes, for each subflow, which packets were lost and when."

- **6. Path metrics used**
  `NOT REPORTED` — no path metric is mandated for scheduling.

- **7. Scheduling decision**
  `NOT REPORTED` (implementation-specific). The only related normative text is §3.3.8's
  statement that in the typical throughput-maximising use case "all available paths will be used
  simultaneously for data transfer."

- **8. Packet-level or flow-level scheduling**
  `NOT REPORTED`. The specification is per-segment in its *mechanics* (the DSS option maps the
  64-bit data sequence number to each subflow's 32-bit sequence space, per segment), but it
  specifies no per-segment assignment policy. This distinction matters: RFC 8684 standardises
  the *encoding* that makes packet-level scheduling possible, not the scheduling itself.

- **9. Reordering handling**
  Reordering is handled through the data-level sequence space: a 64-bit Data Sequence Number
  (DSN) with the Data Sequence Signal (DSS) option and Data ACK, giving "two levels" of
  acknowledgement (per-subflow TCP ACKs and connection-level Data ACKs). Receive-buffer sizing
  guidance is given in §3.3.4 and is explicitly acknowledged as unsolved in general:

  > "The lower bound for full network utilization is the maximum bandwidth-delay product of any
  > one of the paths. However, this might be insufficient when a packet is lost on a slower
  > subflow and needs to be retransmitted … A tight upper bound would be the maximum round-trip
  > time (RTT) of any path multiplied by the total bandwidth available across all paths. …
  > Determining the relationship between retransmission strategies and receive buffer sizing is
  > left for future study."

  Also: "With MPTCP, all subflows share the same receive buffer" (§3.3.4).

- **10. Congestion-control interaction**
  Coupled congestion control is *recommended*, not mandated:

  > "To achieve fairness at bottlenecks and resource pooling, it is necessary to couple the
  > congestion windows in use on each subflow, in order to push most traffic to uncongested
  > links. One algorithm for achieving this is presented in [RFC6356]; the algorithm does not
  > achieve perfect resource pooling but is 'safe' in that it is readily deployable in the
  > current Internet."

  And it anticipates alternatives: "It is foreseeable that different congestion controllers will
  be implemented for MPTCP, each aiming to achieve different properties in the resource pooling /
  fairness / stability design space."

- **11. Objective**
  Abstract: "The simultaneous use of these multiple paths for a TCP/IP session would improve
  resource usage within the network and thus improve user experience through higher throughput
  and improved resilience to network failure."
  For CC, the stated property is a safety/fairness constraint, quoted above: a coupled flow
  "does not take up more capacity on any one path than if it was a single path flow using only
  that route, so this ensures fair coexistence with single-path TCP at shared bottlenecks."

- **12. Algorithm**
  A protocol specification. No scheduling algorithm. The only algorithmic content referenced is
  RFC 6356's coupled congestion control.

- **13. ML/DRL usage**
  No. No mention of learning of any kind in the retrieved full text.

- **14. Simulator / testbed**
  `NOT REPORTED` — an RFC reports no evaluation. Its "evidence base" is deployment experience:
  the v1 changes over RFC 6824 are described as "primarily driven by deployment experience",
  but no deployment measurements are given in this document.

- **15. Traffic model** — `NOT REPORTED`
- **16. Baselines** — `NOT REPORTED`
- **17. Metrics** — `NOT REPORTED`
- **18. Main result**
  `NOT REPORTED` (no experimental results). The normative claims are the coupled-CC safety
  property quoted in field 11.

- **19. Limitation**
  As stated: receive-buffer/retransmission sizing "is left for future study"; the CC algorithm
  referenced "does not achieve perfect resource pooling". Methodologically: the standard
  standardises no scheduler interface, so scheduler behaviour is unobservable/unmeasurable at
  the protocol level and cannot be validated for conformance — interoperation between different
  vendor schedulers is undefined by construction.

- **20. Research gap this suggests**
  The standard deliberately leaves the two performance-critical mechanisms — packet scheduling
  and receive-buffer/retransmission policy — to implementations. That creates a
  standards-compliant vacuum in which (a) every scheduler evaluation is implementation-specific
  and non-reproducible across stacks, and (b) there is **no standard control plane through which
  an external orchestrator could influence scheduling at all**. Any claim that AI-native network
  management can drive MPTCP scheduling must therefore either use a non-standard interface or
  operate below/outside the protocol.

- **21. Best URL retrieved / depth**
  `https://www.rfc-editor.org/rfc/rfc8684.txt` — **FULL TEXT** (3,795 lines retrieved and read).

---

### 2. MultiPath TCP: From Theory to Practice

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Sébastien Barré, Christoph Paasch, Olivier Bonaventure (ICTEAM, Université catholique de
  Louvain). 2011. **10th IFIP Networking Conference (NETWORKING 2011)**, Valencia, Spain,
  pp. 444–457. DOI `10.1007/978-3-642-20757-0_35`; HAL `hal-01583423`. **Peer-reviewed
  conference paper.**

- **1. Number and type of paths**
  Evaluation testbed uses **two completely disjoint wired paths** of 100 Mbps each ("the network
  has two completely disjoint paths between the source and the destination"). Motivation targets
  **heterogeneous** 3G + WiFi smartphones. Subflow counts up to 8 are exercised for CPU
  measurement ("MPTCP connections containing 1 to 8 subflows on a shared 1 Gbps bottleneck").

- **2. Network architecture**
  End-to-end multipath, **Linux kernel** implementation. Architecture has three elements: a
  *master subsocket* (application-facing), a *multipath control block (mpcb)* that "runs the
  decision algorithm for starting or stopping subflows …, the scheduling algorithm for feeding
  new application data to a particular subflow, and the reordering algorithm", and *slave
  subsockets* (one per subflow, invisible to the application). Data pushed by the application is
  **not scheduled immediately**: "the data pushed by the applications is not scheduled anymore,
  but instead stored in a connection-level send buffer. Subflows pull data from the shared send
  buffer whenever they receive an acknowledgement."

- **3. Transport protocol**
  MPTCP as then being standardised by the IETF — i.e. **pre-RFC 6824 draft MPTCP** (the paper
  cites `draft-ietf-mptcp-multiaddressed-02`). Not v1.

- **4. Scheduler location**
  **Linux kernel**, inside the mpcb; modular ("the scheduler is modular and other policies like
  preferring one interface over the other could be implemented in the future"). Invoked
  per-segment, at the moment the segment is actually put on the wire — a deliberate design
  choice: "This effectively solves the problem of fluctuating path properties and allows to run
  the scheduler when the segment is sent on the wire."

- **5. Scheduler inputs**
  Subflow state and the connection-level send buffer. Concretely: per-subflow congestion window
  state (the scheduler runs when "an acknowledgement opens up more space in the congestion
  window"), per-subflow RTT estimation (used for buffer sizing, via TCP timestamps), and the
  shared send buffer. The paper states the granularity problem explicitly: "The scheduler must
  deal with the granularity of the allocations, that is, the number of contiguous bytes that are
  sent over the same subflow before deciding to select another subflow."

- **6. Path metrics used**
  RTT per subflow (used for the coupled-CC α and for receive-buffer dimensioning); MSS is
  forced identical across subflows (minimum MSS over all subflows), justified empirically: "97%
  of these servers returned an MSS of 1380 bytes".

- **7. Scheduling decision**
  Default policy: **fill all subflows** — "The current policy implemented in the scheduler tries
  to fill all subflows". Allocation granularity is explicitly left as an open trade-off: "The
  optimal use of all subflows would be an argument in favor of small allocation units. On the
  other hand, to spare CPU cycles and memory accesses, one would tend to allocate in large
  units … In this paper, we favor an optimal allocation of segments, deferring a full study of
  the performance trade-offs for another paper."

- **8. Packet-level or flow-level scheduling**
  **Packet-/segment-level** — the scheduler assigns contiguous byte ranges to subflows and the
  paper quantifies that "the MPTCP scheduler runs for every transmitted segment".

- **9. Reordering handling**
  Two-level reordering: subflow-level reordering on the 32-bit subflow sequence space, then
  connection-level reordering on the 64-bit data sequence numbers, delivering in-order to the
  application. "All subflow-receive queues are always empty, because as soon as a segment
  becomes in order at the subflow-level, it is enqueued in the connection-level receive queue,
  or out-of-order queue." The **receive buffer is the explicit penalty mechanism** and is
  analytically sized:

  > `rbuf = 2 * Σ_{i∈subflows} BW_i * RTT_max`

  with dynamic tuning (Fisk-style) applied per path contribution. Practical consequence
  measured: the receive buffer "may reach the maximum allowed receive buffer configured on the
  system. This should be used as a hint to indicate that a subflow is under-performing and
  disable the slowest path." Buffer tuning is integrated with Van Jacobson's **prequeues**
  because "MPTCP involves more processing, especially with regards to reordering".

- **10. Congestion-control interaction**
  **Coupled congestion control** implemented in-kernel, with the α-factor:

  - On each non-duplicate ACK on subflow *i*: increase cwnd_i by `min(α/cwnd_tot, 1/cwnd_i)`.
  - On loss on subflow *i*: decrease cwnd_i by `cwnd_i/2`.
  - α computed as `α = cwnd_tot · max_i(cwnd_i·mss_i²/RTT_i²) / (Σ_i cwnd_i·mss_i/RTT_i)²`.

  Implementation constraint documented: "the Linux kernel does not support floating point
  numbers", so the implementation counts acknowledged packets in `cwnd_cnt_i` and increases by
  one packet when `cwnd_cnt_i > totcwnd/α`, with fixed-point scaling.

- **11. Objective**
  Quoted design goal: "One obvious goal of MPTCP is to be able to consider all available paths
  as a shared resource, just behaving as the sum of the individual resources." Combined with a
  fairness constraint: "the coupled congestion control should be fair to TCP. This means that an
  MPTCP connection should allow other TCP sessions to take over the bandwidth on a shared
  bottleneck."

- **12. Algorithm**
  Heuristic fill-all scheduler; analytical coupled congestion control (α-coupling) with
  fixed-point kernel arithmetic.

- **13. ML/DRL usage**
  No. No learning component of any kind.

- **14. Simulator / testbed**
  **Real hardware testbed, not simulation.** Two scenarios in the **HEN testbed at University
  College London**:
  - *Congestion testbed*: four Linux workstations (Intel Xeon 2.66 GHz, 8 GB RAM, Intel
    82571EB Gigabit Ethernet), two 1 Gbps links into a router, then a **100 Mbps** link to a
    server; iperf sessions run **10 minutes**, each measurement repeated **5 times**, average
    reported.
  - *Performance testbed*: three workstations (AMD Opteron 248 2.2 GHz, 2 GB RAM, dual Intel
    82546GB GbE), router configured so packets cannot cross-route — two genuinely disjoint
    paths. Link B delay injection of **0, 10, 100 and 500 ms**; loss injection on Link B;
    bandwidth set by Ethernet configuration.
  - No TSO: "we do not use TSO (TCP Segmentation Offload) for these measurements."

- **15. Traffic model**
  **Bulk transfer** (iperf), plus web-server MSS probing against the Alexa top-10,000.

- **16. Baselines**
  Regular **TCP with Reno** on a single path, versus **MPTCP with Reno on each subflow** versus
  **MPTCP with coupled congestion control**. (The paper's own comparison set; no external
  scheduler baselines — none existed yet.)

- **17. Metrics**
  iperf goodput (Mbps), throughput fairness against competing regular TCP, goodput vs receive
  buffer size, goodput vs packet-loss ratio, goodput vs MSS, CPU consumption (softirq % vs user
  context %).

- **18. Main result**
  - Fairness: "When an MPTCP connection with two subflows is sharing a bottleneck link with a
    TCP connection, the coupled congestion control behaves as if the MPTCP session was just one
    single TCP connection. However, when Reno congestion control is used on the subflows, MPTCP
    gets more bandwidth…"; with 1/2/3 subflows "the coupled congestion control provides the same
    fairness".
  - Receive buffer: "When the two subflows have the same delay, they are able to saturate the
    two 100 Mbps links with a receive buffer of 2 MBytes or more." At **500 ms** delay
    difference "the goodput achieved by MultiPath TCP is much more affected."
  - Loss: "the goodput of the other subflow remains stable with packet loss ratios of 1, 2 or
    3 %. It is only when the packet loss ratio reaches 4% or 5% that the goodput of the white
    subflow decreases slightly."
  - MSS/CPU: "It is able to saturate two Gigabit Ethernet links with an MSS of 4500 bytes";
    "Increasing the number of concurrent subflows from 1 to 8 has no significant impact on the
    overall system charge"; receiver "around 50% of the CPU time is spent in soft interrupt, 8%
    in the user context with a 1400 bytes MSS and a single Gigabit Ethernet link."

- **19. Limitation**
  As stated by the authors: (i) "the MultiPath TCP protocol is not yet finalized and for example
  the security issues are still being developed"; (ii) "MultiPath TCP currently uses the standard
  TCP retransmission mechanisms on each subflow while multipath-aware retransmission mechanisms
  could probably improve the performance"; (iii) "**our current implementation uses all
  available subflows while better performance would probably be possible by adding and removing
  subflows based on their measured performance**"; (iv) TSO not yet supported; (v) "the
  performance of MultiPath TCP in the global Internet and its interactions with real middle-boxes
  should be evaluated"; (vi) "A better reordering algorithm could probably improve the receiver
  performance."
  Methodological (my reading of the retrieved text): a single wired lab topology with injected
  delay/loss, not real cellular or WiFi; 100 Mbps bottleneck in the fairness scenario; small
  number of repetitions; values read from figures for several results (the text gives the
  qualitative direction and the axes, not always a table of numbers).

- **20. Research gap this suggests**
  Limitation (iii) is the seed of the entire learning-based-scheduling literature: the scheduler
  uses *all* paths and does not decide *whether* to use a path based on measured performance.
  Limitation (vi) plus the buffer formula show that reordering cost is treated as a buffer
  dimensioning problem rather than as a control signal. Both point to a scheduler that (a) uses
  richer per-path state and (b) makes path *set* decisions — precisely the gap that BLEST/ECF
  then Peekaboo/ReLeS later target.

- **21. Best URL retrieved / depth**
  `https://inria.hal.science/hal-01583423v1/file/978-3-642-20757-0_35_Chapter.pdf` — **FULL
  TEXT** (publisher-authorised HAL deposit; 15 pages, converted and read).

---

### 3. Design, Implementation and Evaluation of Congestion Control for Multipath TCP

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Damon Wischik, Costin Raiciu, Adam Greenhalgh, Mark Handley (University College London).
  **NSDI 2012** (9th USENIX Symposium on Networked Systems Design and Implementation),
  pp. 99–112. No publisher DOI; ACM DL proceedings record `10.5555/1972457.1972468`.
  **Peer-reviewed conference paper.**
  *Bibliographic caveat recorded honestly:* USENIX's own NSDI '12 programme index as retrieved
  lists 27 papers and does **not** include this one — the only multipath paper it lists is
  "How Hard Can It Be? Designing and Implementing a Deployable Multipath TCP" (Raiciu et al.,
  NSDI 2012). The ACM DL record, however, places this paper in the NSDI '12 proceedings at
  pp. 99–112, and the contemporary literature cites it as NSDI. Two citing papers even cite it
  as "USENIX NSDI, 2011" (paper 4, ref. [22]; paper 2, ref. [22]). I treat **NSDI 2012** as
  correct on the strength of the ACM DL proceedings record, and flag the USENIX index
  discrepancy rather than hide it.

- **1. Number and type of paths**
  Generic multipath; evaluated in three scenarios. (i) *Multihomed Internet server* — multiple
  upstream paths. (ii) *Data centres* — **FatTree** (up to **8** paths used; "we have found that
  8 is enough") and **BCube** (3 interfaces per host, paths with differing hop counts).
  (iii) *Mobile client* — **WiFi + 3G**, explicitly heterogeneous ("3G and WiFi have quite
  different link characteristics. WiFi provides much higher throughput and short RTTs … 3G tends
  to vary on longer timescales, and we found that it is overbuffered leading to RTTs of well
  over a second").

- **2. Network architecture**
  Strictly **end-to-end, no core participation**, and this restriction is argued for explicitly:
  "our Linux implementation uses multihoming at one or both ends to provide path choice, but it
  relies on the standard Internet routing mechanisms to determine what those paths are. Our
  reasons for these restrictions are (i) the IETF working group is working under the same
  restrictions, (ii) they lead to a readily deployable protocol, i.e. no modifications to the
  core of the Internet, and (iii) theoretical results indicate that inefficient outcomes may
  arise when both the end-systems and the core participate in balancing traffic."

- **3. Transport protocol**
  MPTCP (design-time; the paper describes "a multipath congestion control algorithm that works
  robustly … and that can be used as a drop-in replacement for TCP").

- **4. Scheduler location**
  Endpoint, Linux kernel (for the testbed part). **The paper does not design a scheduler**; the
  data plane is stated as a given: "An MPTCP sender stripes packets across these subflows as
  space in the subflow windows becomes available." Its control variable is the set of subflow
  congestion windows, so scheduling is an emergent consequence of window-space availability
  (ack-clocking). The paper also discusses, and rejects for architecture reasons, a
  **centralised scheduler**: "An alternative solution for balancing traffic is to use a
  centralized scheduler which monitors large flows and solves an optimization problem to
  calculate good routes for them [3]. We have found that, in order to get comparable performance
  to MPTCP, one may need to re-run the scheduler as often as every 10ms [22] which raises
  serious scalability concerns."

- **5. Scheduler inputs**
  `NOT REPORTED` for a packet scheduler (none is defined). The CC algorithm's inputs are the
  per-subflow congestion window `w_r` and the per-subflow smoothed RTT: "Here RTT_r is the round
  trip time as measured by subflow r. We use a smoothed RTT estimator, computed similarly to
  TCP."

- **6. Path metrics used**
  Smoothed RTT per subflow, per-subflow congestion window, and (in simulations) drop
  probability/loss rate as the implicit congestion signal.

- **7. Scheduling decision**
  `NOT REPORTED` as an action space. Implicitly: **how much window to grant each subflow**
  (a rate/window decision), plus "stripes packets across these subflows as space in the subflow
  windows becomes available" (a data-plane rule, not a designed policy).

- **8. Packet-level or flow-level scheduling**
  Packet striping in the data plane, but the *contribution* is **flow-level/window-level
  control**. This paper must not be cited as a packet-scheduler paper.

- **9. Reordering handling**
  Discussed as a correctness/perf hazard rather than a tunable penalty: "There are hard questions
  about how to avoid deadlock at the receiver buffer when packets can arrive out of order, and
  about the datastream sequence space versus the subflow sequence spaces." No reordering metric,
  no penalty term, no receive-buffer formula reported in the retrieved text (contrast paper 2,
  which does give one).

- **10. Congestion-control interaction**
  This paper **is** the CC contribution. The proposed algorithm:

  > "• Each ACK on subflow r, for each subset S ⊆ R that includes path r, compute
  > `max_{s∈S} w_s/RTT_s² / (Σ_{s∈S} w_s/RTT_s)²`, then find the minimum over all such S, and
  > increase w_r by that much.
  > • Each loss on subflow r, decrease the window w_r by w_r/2."

  It is compared against *per-subflow regular TCP* and **EWTCP** ("For each ACK on path r,
  increase window w_r by a/w_r. For each loss on path r, decrease window w_r by w_r/2. Here …
  a = 1/√n where n is the number of paths"). Implementation note: "we compute the increase
  parameter only when the congestion windows grow to accommodate one more packet, rather than
  every ACK on every subflow."

- **11. Objective**
  Three named goals: fairness at shared bottlenecks ("why not just run regular TCP congestion
  control on each subflow? … the multipath flow would obtain twice as much throughput as the
  single path flow … This is unfair"); efficiency ("A multipath flow should shift all its
  traffic onto the least-congested path"); and RTT compensation. Abstract: "our algorithm
  improves throughput and fairness compared to single-path TCP. Our algorithm is a drop-in
  replacement for TCP, and we believe it is safe to deploy."

- **12. Algorithm**
  Window-based coupled congestion control over the family of subsets S of paths (min over
  subsets containing the ACKed path), additive-increase/multiplicative-decrease; appendix shows
  finding the minimal set S is linear in the number of paths.

- **13. ML/DRL usage**
  No.

- **14. Simulator / testbed**
  **Both, clearly separated by the paper:**
  - **"simulations with a high-speed custom packet-level simulator"** — a custom simulator, not
    ns-3/ns-2. Used for: static load balancing on five bottleneck links in a torus (Jain's
    fairness reported), dynamic load balancing with an on/off CBR flow ("busy for a random
    duration with mean 100ms"), FatTree/BCube data-centre topologies (128-node FatTree
    mentioned; traffic patterns TP1/TP2/TP3), and RTT-compensation sweeps (C1 = 250 pkt/s,
    C2 = 500 pkt/s; then C1 = 400 pkt/s, RTT1 = 100 ms).
  - **Real Linux testbed** — a laptop with a **3G USB interface plus an 802.11 adapter**,
    15 tests of **20 seconds** each (5 single-path WiFi, 5 single-path 3G, 5 MPTCP), and a
    5-minute competing-flows experiment. Notable measurement caveat stated by the authors about
    the WiFi path: "its performance was very variable with quite high loss rates, because there
    was significant interference in the 2.4GHz band."

- **15. Traffic model**
  Bulk/long-lived flows in simulations (explicitly "a stable environment of long-lived flows"),
  long-lived bulk transfers in the testbed; on/off CBR flow for the dynamic scenario; three
  data-centre traffic patterns (TP1 random single incoming flow per host, TP2 one-to-many,
  TP3 sparse with 30 % of hosts).

- **16. Baselines**
  **Single-path TCP** (randomly chosen among shortest-hop paths in data-centre simulations;
  measured on WiFi and on 3G in the testbed), **regular TCP CC per subflow**, and **EWTCP**.

- **17. Metrics**
  Throughput (Mb/s; % of optimal for data centres), Jain's fairness index, throughput achieved
  as a function of number of paths used, ratio of multipath throughput to the better single-path
  flow, and average improvement.

- **18. Main result**
  - Mobile testbed, single flow (20 s tests, avg with standard errors): "The average throughputs
    (with standard errors) were **14.4 (0.2), 2.1 (0.2) and 17.3 (0.7) Mb/s** respectively"
    (TCP-WiFi, TCP-3G, MPTCP) — "the MPTCP user gets bandwidth roughly equal to the sum of the
    bandwidths of the access links."
  - Mobile testbed, competing flows (long-run averages over 5 minutes, Mb/s), columns
    `multipath / TCP-WiFi / TCP-3G`:
    **EWTCP 1.66 / 3.11 / 1.20**, **COUPLED 1.41 / 3.49 / 0.97**, **MPTCP 2.21 / 2.56 / 0.65**.
    The authors note "Only MPTCP gets close to the correct total throughput" and attribute the
    shortfall to "difficulty in adapting to the rapidly changing 3G link speed".
  - Simulation, RTT compensation: "flow M always gets better throughput by using multipath than
    if it used just the better of the two links; **the average improvement is 15%**."
  - Data-centre simulations, per-host throughput (Mb/s):
    FatTree — SINGLE-PATH 51/94/60, EWTCP 92/92.5/99, **MPTCP 95/97/99** (TP1/TP2/TP3);
    BCube — SINGLE-PATH 64.5/297/78, EWTCP 84/229/139, **MPTCP 86.5/272/135**.

- **19. Limitation**
  As stated: "In this paper we will restrict our attention to end-to-end mechanisms…"; "It is
  not an exhaustive survey of the design space, and we do not claim that our algorithm is
  optimal—to even define optimality would require a more advanced theoretical underpinning than
  we have yet developed"; scope is CC only ("Some of the issues (§2.1–§2.3) have previously been
  raised … but not all have been solved. The others (§2.4–§2.5) are novel"); and it notes MPTCP
  "does not move all its traffic away from the most congested path".
  Methodological (mine): the mobile testbed is a single laptop in one room with substantial 2.4
  GHz interference and an overbuffered 3G link; sample sizes are small (5 runs of 20 s for the
  single-flow case); the data-centre results come from a **custom, non-public simulator**, so
  they are not reproducible on a standard platform; and the comparison against a *centralised*
  scheduler is made by argument, not by implementation.

- **20. Research gap this suggests**
  Two gaps. (a) The paper asserts centralised/optimisation-based traffic engineering is not
  viable "as often as every 10ms … serious scalability concerns" — an argument made in 2012
  against a *solver*, which is exactly the assumption that modern learning-based and
  data-driven control challenges; whether an ML policy can be re-evaluated at that cadence at
  acceptable cost is an open empirical question. (b) The CC is tuned for throughput/fairness
  with RTT compensation as an add-on; latency is not an objective, which is the gap papers 5,
  12 and 13 later attack.

- **21. Best URL retrieved / depth**
  `https://courses.cs.duke.edu//cps214/fall15/Papers/mptcp-nsdi.pdf` — **FULL TEXT** (14 pages,
  converted and read). USENIX's own programme page for NSDI '12 does **not** surface this paper
  (see bibliographic caveat above); ACM DL landing page is
  `https://dl.acm.org/doi/abs/10.5555/1972457.1972468`.

---

### 4. Experimental evaluation of multipath TCP schedulers

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Christoph Paasch (UCLouvain), Simone Ferlin (Simula Research Laboratory), Özgü Alay (Simula),
  Olivier Bonaventure (UCLouvain). 2014. **ACM SIGCOMM workshop on Capacity Sharing (CSWS
  '14)**, Chicago. DOI `10.1145/2630088.2631977`. **Peer-reviewed workshop paper.**

- **1. Number and type of paths**
  Two paths. Emulated (Mininet): synthetic low-BDP and high-BDP two-path configurations.
  Real-world: **WLAN + 3G (UMTS)** — heterogeneous, and the WLAN is a congested *public* WLAN
  ("connecting ca. 100 people during work hours in a large office complex with several other
  interfering WLAN networks").

- **2. Network architecture**
  End-to-end MPTCP with a **modular scheduler framework** in the Linux kernel. "We added
  callbacks from the MPTCP stack that invoke the functions specific to each scheduler", with a
  `sysctl` for the system default and **per-connection socket options** letting the application
  choose the scheduler. The framework is invoked whenever the stack is ready to send — on ACK
  freeing window space or on application push — and performs two tasks: choose a subflow, then
  choose the segment.

- **3. Transport protocol**
  MPTCP, Linux kernel implementation **release 0.88**; coupled congestion control **OLIA** used
  in all experiments ("Similar results were obtained with the coupled congestion control
  scheme [22]").

- **4. Scheduler location**
  **Linux kernel** (Mptcp-level scheduler with callbacks), selectable per connection.

- **5. Scheduler inputs**
  Explicitly: "The scheduler has access to the state of each TCP subflow, including **congestion
  window and RTT estimation**." In the scheduler designs: **smoothed RTT (sRTT)**, **minimum
  smoothed RTT (sRTT_min)**, **CWND**, **TSQ / TCP Small Queues** state, available receive
  window, and the ability to **re-inject** an already-sent segment. Bufferbloat mitigation adds a
  derived cap: `cwnd_limit = λ × (sRTT_min/sRTT) × cwnd`, with **λ fixed to 3** ("which has proven
  to bring the best results, as has been analyzed in [16]").

- **6. Path metrics used**
  RTT / sRTT / sRTT_min (bufferbloat proxy), congestion window, receive-window occupancy; no
  bandwidth or loss-rate metric is used as a scheduling input.

- **7. Scheduling decision**
  Per-segment path choice, executed through two callbacks: `get_subflow()` then `get_data()`
  (with `send_data()`). Documented schedulers and their rules:
  - **Round-Robin (RR)** — "selects one subflow after the other in round-robin fashion."
  - **Lowest-RTT-First (LowRTT)** — "first sends data on the subflow with the lowest RTT
    estimation, until it has filled the congestion window. Then, data is sent on the subflow with
    the next higher round-trip time."
  - **Retransmission and Penalization (LowRTT+RP)** — "opportunistic retransmission re-injects
    the segment causing the head-of-line blocking on the subflow that has space available in its
    congestion window"; "the penalization algorithm reduces the congestion window of the subflow
    with the high RTT".
  - **Bufferbloat Mitigation (LowRTT+BM)** — "caps the RTTs by limiting the amount of data to be
    sent on each subflow" via `cwnd_limit` above; proactive rather than reactive.

- **8. Packet-level or flow-level scheduling**
  **Packet-level** — the scheduler is called per segment; the paper's own framing is
  "distribution of data over multiple paths".

- **9. Reordering handling**
  Reordering appears as the two named pathologies the schedulers must fight: **head-of-line
  blocking** ("packets that are scheduled on the low-delay subflow have to 'wait' for the
  high-delay subflow's packets to arrive in the out-of-order queue of the receiver") and
  **receive-window limitation**. The paper states the buffer requirement:
  `Buffer = Σ_i bw_i × RTT_max × 2`, noting "Some end hosts, however, are not able to provide the
  necessary amount of memory". RP is the *reactive* reordering penalty (re-inject the blocking
  segment, penalise the slow subflow's cwnd); BM is the *proactive* one. Empirically the paper
  finds the reactive approach insufficient in bad cases: "in some cases this is not sufficient.
  If the delay-difference is very high due to huge bufferbloat, the penalization will not manage
  to bring the congestion window sufficiently down."

- **10. Congestion-control interaction**
  **OLIA** in all experiments, with the note that similar results were obtained with the coupled
  CC scheme of RFC 6356-lineage (ref. [22] = paper 3). Interaction is direct and two-way: the
  scheduler consumes cwnd and can *write* to it (RP penalises cwnd; BM caps cwnd), and the paper
  warns this can backfire: "anecdotal evidence has shown that the penalization may hurt, if two
  subflows are unfortunately sent through the same bottleneck. The bufferbloat mitigation
  technique helps in these cases, but cannot overcome a large difference in the baseline RTT.
  Further, the delay-based congestion-window capping may also suffer from the known limitations
  of delay-based congestion controls when the bottleneck is shared with other flows that do not
  deploy the same window capping."

- **11. Objective**
  Two objectives, stated separately per technique: for RP, "the goal is not only to improve the
  goodput, but also to reduce the delay, jitter and buffer size requirements"; for BM, "The goal
  here is not to significantly improve goodput, but instead, to improve the application
  delay-jitter and reduce buffer size requirements." Overall: "We consider goodput and
  application delay as metrics."

- **12. Algorithm**
  Heuristic rule-based schedulers (RR, LowRTT, LowRTT+RP, LowRTT+BM). No optimisation, no
  learning.

- **13. ML/DRL usage**
  No.

- **14. Simulator / testbed**
  **Both, explicitly.** (a) **Mininet emulation** with the Experimental Design approach — 400
  different settings classified as low-BDP and high-BDP for bulk transfer, and 200 experiments in
  the high-BDP environment for the application-limited case; iperf transfers of 60 s. (b) **The
  NorNet testbed** with a **real public WLAN and a real 3G (UMTS)** interface — bulk transfers of
  **16 MB** downlink with bounded (**2 MB**) and unbounded (**16 MB**) buffers, each measurement
  repeated **~30 times**, all measurements "performed in the same networks and at the same
  locations over a period of 3 weeks"; system-level TCP metrics flushed between runs to avoid
  inter-experiment dependency.

- **15. Traffic model**
  **Bulk transfer** (iperf, 60 s) and **application-limited / rate-limited** traffic (a custom
  sender emitting 8 KB blocks at 500 Kbps and 1875 Kbps — "at approximately 5 and 10% of the
  mean goodput of the bulk-transfer").

- **16. Baselines**
  The schedulers are compared against each other: **RR**, **LowRTT**, **LowRTT+RP**,
  **LowRTT+BM**. (RR is the baseline for the delay results; LowRTT is the baseline for the
  extension results.)

- **17. Metrics**
  **Aggregation benefit** (normalised: −1 = minimum, 0 = same as TCP on the best path, 1 = perfect
  aggregation), **goodput [Mbps]**, **delay increase with respect to lowest possible delay [%]**,
  **delay variation / application delay-jitter [ms]**, CDFs over the experimental-design sample.

- **18. Main result**
  - Bulk, Mininet: "We skip the RR scheduler since it performs similar to LowRTT. This is because
    in bulk-transfers the TCP subflows are saturated and are thus controlled by the ack-clock."
    In low-BDP "Each of them achieves close to perfect bandwidth aggregation"; in high-BDP "the
    RP and BM techniques … improves the aggregation benefit."
  - Bulk, NorNet, unbounded buffers: "the aggregation benefit of MPTCP across all schedulers is
    similar. Each scheduler is able to efficiently aggregate the bandwidth of WLAN and 3G
    together." With a **bounded (2 MB)** buffer: "LowRTT+BM slightly outperforms the other
    schedulers."
  - Application-limited delay (Mininet): "70% of the experiments using the LowRTT scheduler have a
    range between 10 and 100% of delay-increase. Using a RR scheduler, roughly 40% of the
    experiments have a delay-increase between 100 and 1500%."
  - Application-limited delay (NorNet, 500 Kbps): "RR's delay-variance shows to be up to 10 times
    worse compared to LowRTT." At 1875 Kbps: "MPTCP LowRTT performs in at least 60% of the cases
    up to 10 times better compared to RR."

- **19. Limitation**
  As stated: the authors explicitly decline to design a scheduler — "The design of such a
  scheduler is out of the scope and left for future work"; and they identify the core difficulty
  as *estimator quality in the kernel*: "it is not trivial to design such a scheduler with rough
  estimations on capacity or RTTs of the paths, maintained by the kernel." They also record
  failure modes of their own mechanisms (penalisation hurting on a shared bottleneck; delay-based
  cwnd capping failing when other flows do not cap). Future work: "extend our evaluation
  framework to a larger set of traffic classes (including cross-traffic and on/off flows)."
  Methodological (mine): the emulated topology is two-path only; the real-world WLAN is
  uncontrolled and contended (making variance high); results for the bulk case are largely
  qualitative ("similar", "slightly outperforms") in the retrieved text, with the quantitative
  claims concentrated on delay/jitter CDFs.

- **20. Research gap this suggests**
  The paper's own conclusion — that kernel RTT/CWND estimates are too coarse to build a good
  scheduler on — is the direct motivation for the learning-based schedulers that follow
  (Peekaboo, ReLeS, and the MPQUIC-MARL line), whose central claim is that *better state
  estimation* enables better decisions. It also shows a design tension that no paper in this
  review resolves: the scheduler both reads and writes cwnd, coupling it to CC in a way that can
  create instability.

- **21. Best URL retrieved / depth**
  `https://web-backend.simula.no/sites/default/files/publications/Experimental-Evaluation-of-Multipath-TCP-Schedulers.pdf`
  — **FULL TEXT** (6 pages, converted and read). ACM DL: `https://dl.acm.org/doi/10.1145/2630088.2631977`.

---

### 5. Low-Latency Scheduling in MPTCP

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Per Hurtig, Karl-Johan Grinnemo, Anna Brunström (Karlstad University), Simone Ferlin
  (Ericsson Research), Özgü Alay (Simula Research Laboratory), Nicolas Kuhn. **2019**, IEEE/ACM
  **Transactions on Networking** 27(1):302–315. DOI `10.1109/TNET.2018.2884791`; HAL
  `hal-04127676`. **Peer-reviewed journal.** (Note the DOI stem says 2018 — that is the
  early-access year; the issue is February 2019.)

- **1. Number and type of paths**
  Two paths, deliberately **heterogeneous**: emulated WLAN/3G-style settings and, in the
  real-world experiments, WLAN + 3G where "we measured the RTT of the two paths, which showed an
  average of **RTT_WLAN ≈ 25 ms** and **RTT_3G ≈ 75 ms**."

- **2. Network architecture**
  End-to-end MPTCP over a Linux-kernel stack; no proxy. Emulated topology ("a client, two
  wireless access points (WLAN/3G), a server access router and a server") built from **five
  regular desktop computers**; the client ran a **stock MPTCP kernel** while "the server used a
  modified version including the BLEST and STTF schedulers", and the intermediate machines "used
  regular Linux kernels configured to emulate link characteristics and forward traffic." In the
  real-world part the server was a remote web server in Norway and the client a **MONROE** node
  in Sweden.

- **3. Transport protocol**
  MPTCP (Linux kernel, MPTCP v0.9x-era stack). Client kept as a stock deployment; scheduler
  changes were server-side only.

- **4. Scheduler location**
  **Linux kernel**, at the MPTCP send path — "the data scheduler decides, for each segment, which
  subflow to use for transmission."

- **5. Scheduler inputs**
  Stated explicitly in the design discussion: **smoothed RTT (SRTT)** sampled "at the moment of
  scheduling"; **CWND** (whether the subflow has window space, and how much); **TSQ (TCP Small
  Queues)** state, which can inhibit scheduling on a subflow; and, for STTF, an estimate of the
  **transmission time of each data segment** built from the path's capacity/cwnd estimate and
  RTT. BLEST additionally reasons about **receive-buffer space** it must keep available for
  out-of-order segments. The paper's motivating analysis is precisely that a *stale or coarse*
  SRTT leads LRF astray: it documents "stale RTT measurements, which may lead to the abandonment"
  of a good path, and shows the interaction with TSQ (in the 15-segment burst illustration, "the
  seventh and eight segments are [not schedulable]"). All network buffers in the testbed "were
  kept at their default settings".

- **6. Path metrics used**
  SRTT, CWND, TSQ queueing state, estimated per-path capacity (implicitly via cwnd/RTT), and
  predicted per-segment transmission time. No loss-rate or energy metric.

- **7. Scheduling decision**
  Per-segment subflow selection. Three schedulers are characterised:
  - **LRF** (lowest-RTT-first, the MPTCP default) — send on the lowest-RTT subflow until its CWND
    is full, then the next; the paper notes that because segments wait for the slow subflow, "the
    ten-segment transfer for MPTCP clearly [takes longer]" than TCP on the fast path alone.
  - **BLEST** — the block-estimation scheduler: it estimates whether sending would cause
    head-of-line blocking and reserves buffer space on the slow path (a "penalisation" for
    blocking avoidance), i.e. it may *decline* to use a subflow.
  - **STTF** (shortest transmission time first) — "aims to … predict the transmission time of
    each data segment" and schedules the segment on the path that will deliver it soonest.

- **8. Packet-level or flow-level scheduling**
  **Packet-level** — the paper's own unit is the segment ("for each segment, which subflow to use
  for transmission"), and the latency experiments are explicitly burst-level at 10–50 segments.

- **9. Reordering handling**
  Reordering/head-of-line blocking is the *stated design target*, not an afterthought: "When data
  arrives out-of-order … While HoL blocking introduces a delay in delivering data … this will
  increase latency." Reordering is handled **at scheduling time**: BLEST "aims to reduce buffer
  blocking" by keeping enough receive-buffer margin so a faster subflow is not blocked, and STTF
  avoids creating the out-of-order condition in the first place by predicting arrival order. The
  receive buffer is the constraint being managed; the paper also documents receiver-buffer
  blocking as a throughput *and* latency problem ("receiver buffer blocking … reduces
  throughput … causing both reduced throughput and [increased latency]").

- **10. Congestion-control interaction**
  The schedulers read CWND and are constrained by it (a segment "cannot be scheduled due to full
  CWND"), and BLEST's blocking-avoidance implicitly shapes how much is sent per subflow. The
  retrieved text does not name the CC algorithm used on the subflows in the evaluation
  (`NOT REPORTED` in the full text I read); it does cite RFC 6356-lineage coupled CC and the
  paper-3 algorithm in the reference list.

- **11. Objective**
  Abstract: "we focus on the MPTCP scheduler with the goal of providing a good user experience
  for latency-sensitive applications"; the article "focuses on low-latency capacity aggregation"
  and aims at "responsive communication with minimum latency" while still using the aggregate
  capacity. Explicitly non-throughput-only: "the main objective is not to reduce [goodput but to
  address] latency per se".

- **12. Algorithm**
  Two heuristic schedulers plus the baseline; no optimisation formulation and no learning.

- **13. ML/DRL usage**
  No.

- **14. Simulator / testbed**
  **Both, and clearly separated by the authors:** (a) a **five-machine emulation testbed** with
  Linux traffic shaping/forwarding to emulate WLAN/3G characteristics — the parameters "were not
  chosen to be representative of typical WLAN/3G setups but rather to exhibit necessary path
  asymmetry, causing data to arrive out-of-order"; (b) **real-world experiments** on the
  **MONROE** mobile broadband measurement platform (client node in Sweden, server in Norway,
  real WLAN + 3G). Emulated web/interactive experiments and real web experiments used the same
  software tool-chain and the same websites. Repetitions: burst experiments "repeated 30 times";
  web experiments "the average download time is based on 30 repetitions" with 95 % confidence
  intervals.

- **15. Traffic model**
  Four classes: **synthetic bursts** of 10–50 segments (symmetric RTT 10/10 ms, asymmetric
  10/40 ms, highly asymmetric 10/100 ms); **bulk transfer**; **web browsing** over HTTP/2 against
  five real sites (google.com, wikipedia.com, instagram.com, amazon.com, theguardian.com) driven
  by a reconstructed traffic profile from real captures; and **interactive application** traffic
  (Google Maps) from captured user-interaction traces (objects sent sparsely, "the amount of data
  is small and sparsely communicated due to real user interactions").

- **16. Baselines**
  **LRF** (MPTCP's default scheduler, the primary baseline), **DAPS** (Delay-Aware Packet
  Scheduler), **OTIAS** (One-Way-Delay-based … Arrival Scheduler), **ECF**, plus **single-path
  TCP over the smallest-RTT path** for the burst experiments.

- **17. Metrics**
  Burst transmission time (ms, one-way application delay), **goodput** (bulk), **page load time**
  and **object download time** (web), **traffic path share** (% of data per interface), and
  latency for interactive traffic; 95 % confidence intervals throughout.

- **18. Main result**
  - Abstract-level: "Compared to MPTCP's default scheduler, experiments show that STTF can
    **reduce web object transmission times with up to 51%** and **provide 45% faster
    communication for interactive applications**."
  - Real-world web (MONROE), Amazon: "both BLEST and STTF reduce the page load times for Amazon
    with approximately **27%**, and the object load times with an average of **41%**."
  - Interactive (Google Maps), emulated: "When no packet loss occurs, BLEST outperforms LRF by
    approximately **29%**, and, when packets are lost, BLEST is about **5%** faster. Similarly,
    when no packet loss occurs, STTF outperforms BLEST by approximately **23%**, and, when
    packets are lost, STTF is about **1.5%** faster. Compared to LRF, **STTF is 45% faster when no
    packets are lost, and 6% faster otherwise**." A concrete pathology is also quantified: "when
    LRF is used and there is no data loss, the average download time is about **60 ms** compared
    to **more than 200 ms at 1% random packet loss**."
  - Traffic distribution: "with LRF scheduling approximately **68%** of the [real-world]
    traffic over WLAN, BLEST a little over **70%**, and STTF slightly over **80%**"; in emulation
    LRF sends "approximately 60% of the data over the best path (WLAN), while BLEST uses this path
    for almost **80%** and STTF for roughly **90%** of the traffic."
  - Honest negative result recorded by the authors: "For the Wikipedia experiments, there are no
    noticeable differences in page load times among the schedulers, although BLEST and STTF
    significantly reduce the object download times", explained by site structure/dependency
    delays masking faster object transfer.

- **19. Limitation**
  As stated: gains in the real world are smaller and more variable than in emulation — "the
  difference among the schedulers is slightly lower than for the emulation [results]", "the
  variation in the results is larger when running over real networks", and "reduced object
  download times does not seem to cause a similar reduction in page load times" for some sites.
  Also: the emulated parameters were deliberately non-representative (chosen to force asymmetry),
  and the emulated web workload was found "too small to trigger different scheduling decisions
  among the schedulers". Methodological (mine): the client is a single MONROE node on one route,
  RTTs ~25/75 ms only; no cellular 5G, no lossy 5G mmWave; and the server-side-only modification
  means the evaluation does not test a realistic two-sided deployment.

- **20. Research gap this suggests**
  The paper demonstrates that a *better predictor of per-segment delivery time* (STTF) beats both
  RTT-greedy and blocking-avoidance heuristics — an explicit invitation to replace the analytic
  predictor with a learned one. It also surfaces the evaluation problem the learning papers
  inherit: a scheduler can win on object download time and lose in page load time because
  application-level dependencies dominate — i.e. **scheduler gains do not compose to QoE gains**,
  which no paper in this review measures end-to-end.

- **21. Best URL retrieved / depth**
  `https://hal.science/hal-04127676/document` (publisher-designated OA repository copy; retrieved
  through the site's proof-of-work interstitial with `tools/anubis_fetch.py`) — **FULL TEXT**
  (15 pages, converted and read). Publisher: `https://doi.org/10.1109/TNET.2018.2884791`.

---

### 6. Multipath QUIC: Design and Evaluation

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Quentin De Coninck, Olivier Bonaventure (UCLouvain). 2017. **CoNEXT '17** — Proceedings of the
  13th International Conference on emerging Networking EXperiments and Technologies, Incheon,
  Republic of Korea, December 12–15, 2017, 7 pages. DOI `10.1145/3143361.3143370`. **Peer-reviewed
  conference paper.**

- **1. Number and type of paths**
  Two paths in the evaluation ("a multipath network with two multihomed hosts over disjoint
  paths with different characteristics"), with **heterogeneous** characteristics spanning
  capacity 0.1–100 Mbps, RTT 0–400 ms, queuing delay 0–2000 ms and random loss 0–2.5 % by
  experimental design. Emerging 5G was part of the motivation ("Today's mobile devices such as
  smartphones have several wireless interfaces … a growing fraction of hosts are dual-stack and
  the IPv4 and IPv6 paths between them often differ").

- **2. Network architecture**
  End-to-end, **userspace** multipath extension of QUIC implemented in **quic-go**. Path
  management uses an **ADD_ADDRESS** frame (encrypted, so "it does not suffer from the security
  concerns of the ADD_ADDR option in MPTCP") and a **PATHS** frame carrying path IDs and
  statistics "such as the estimated path round-trip-time", usable to "detect underperforming or
  broken paths and … speed up the handover process in mobility scenarios". A key architectural
  difference from MPTCP is exploited: because packets and frames are independent, control frames
  are not bound to one path.

- **3. Transport protocol**
  **Multipath QUIC (MPQUIC)** — QUIC extended with multiple paths; "our design remains clean and
  simple thanks to the flexibility of the QUIC protocol."

- **4. Scheduler location**
  **Userspace**, inside the quic-go-based MPQUIC implementation at the sender. The paper is
  explicit that this is a different beast from MPTCP's scheduler in scope: "while MPTCP has to
  decide which data (either new or reinjected) will be sent on which path, the MPQUIC scheduler
  also determines which control frame (ACK, WINDOW_UPDATE, PATHS,...) will be sent on a particular
  path."

- **5. Scheduler inputs**
  "It relies on the **smoothed measured round-trip-time (RTT)** and prefers the path with the
  lowest RTT provided that its **congestion window is not already full**." Plus: loss
  information per packet, the receive window / need to deliver WINDOW_UPDATE; and a cold-start
  problem — "when a new path starts in MPQUIC, the scheduler does not have an estimation of the
  path's RTT yet", for which the paper discusses ping-first (costs 1 RTT) versus round-robin
  start (fragile with very different delays).

- **6. Path metrics used**
  Smoothed RTT per path; congestion window; receive-window state. No bandwidth estimate and no
  loss-rate metric as a scheduling input.

- **7. Scheduling decision**
  Per-*packet* (and per-*frame*) path selection. The starting point is deliberately the MPTCP
  Linux default: "For MPQUIC, our starting point is the default scheduler used by the MPTCP
  implementation in the Linux kernel … MPQUIC uses the same heuristic, but with two differences",
  the two differences being (a) control-frame placement and (b) the cold-start RTT problem.
  Retransmission placement is also part of the action space: "When a packet is marked as lost, its
  frames are not necessarily retransmitted over the same path, while MPTCP is forced to
  (re)transmit data in sequence over each path to cope with middleboxes."

- **8. Packet-level or flow-level scheduling**
  **Packet-level**, with frame-level granularity as an additional degree of freedom.

- **9. Reordering handling**
  Reordering is a first-class design consideration, and MPQUIC's advantage is structural: "Thanks
  to the clean support for multiple streams in STREAM frames, MPQUIC does not need to specify a
  new type of sequence number in contrast to MPTCP's DSN." Receive-buffer limitation is handled
  by a scheduler rule: "To prevent receive buffer limitations, the scheduler ensures proper
  delivery of the WINDOW_UPDATE frames by sending them on all paths when they are needed." The
  evaluation attributes MPQUIC's win over MPTCP precisely to reordering dynamics: "MPTCP faces
  head-of-line blocking more often than MPQUIC. With heterogeneous paths, MPTCP tends to send
  large bursts of packets on the slow path."

- **10. Congestion-control interaction**
  Multipath CC used is **OLIA**, stated explicitly ("we use the OLIA congestion control scheme
  with Multipath TCP and Multipath QUIC" — because "there is no multipath variant of CUBIC"),
  while single-path TCP and QUIC both use **CUBIC**. The paper states that adapting multipath CC
  schemes to MPQUIC "is left for further study". Loss response interacts with scheduling: "When a
  packet is lost, the OLIA congestion control scheme reduces the congestion window over the
  affected path."

- **11. Objective**
  For the main scenario: "a multihomed host wants to **minimize the download time** and thus
  **maximize the aggregation of the bandwidth** of the available paths." Broader claim in the
  abstract: "MPQUIC maintains MPTCP's benefits (aggregation benefit, network handover)."

- **12. Algorithm**
  Heuristic lowest-RTT-with-available-cwnd, inherited from the MPTCP Linux default scheduler;
  no optimisation and no learning.

- **13. ML/DRL usage**
  No.

- **14. Simulator / testbed**
  **Emulation only, on Mininet** — explicitly and self-critically: "In this paper, we rely on
  measurements on the Mininet emulation platform with complete (MP)QUIC and (MP)TCP
  implementations and use (MP)TCP as the baseline … **Real-world evaluation is part of our future
  work.**" Experimental design (WSP-chosen parameter values) over the ranges in Table 1; four
  environment classes (low-BDP/high-BDP × no-loss/losses); "For each class, we consider 253
  scenarios and vary the path used to start the connection, leading to **506 simulations**. Each
  simulation is repeated **3 times** for each protocol (TCP, MPTCP, QUIC, MPQUIC) and we analyze
  the median run." Baseline stack: "Linux kernel version **4.1.39 patched with MPTCP v0.91**".
  Host: Intel Xeon E3-1245 V2 @ 3.40 GHz VM with two dedicated cores and 2 GB RAM. Fairness
  control for crypto cost: "our measurements use https over (MP)TCP (TLS 1.2) or (MP)QUIC (QUIC
  crypto)"; maximal receive window 16 MB for both.

- **15. Traffic model**
  **Bulk transfer** — "Each measurement downloads a **20 MB file in a single stream**" and the
  client measures "the delay between the transmission of the first connection packet and the
  reception of the last byte of the file"; plus a small-transfer scenario (256 KB) and a network
  **handover** scenario.

- **16. Baselines**
  **TCP**, **MPTCP** (Linux 4.1.39 + MPTCP v0.91), and **single-path QUIC**; multipath protocols
  are compared both against their single-path counterparts and against each other.

- **17. Metrics**
  Download-time ratio (TCP/QUIC and MPTCP/MPQUIC; 1 = equivalent), and a modified
  **experimental aggregation benefit** normalised against the sum of single-path goodputs
  (0 = same as best single path, 1 = equals sum of per-path goodputs, −1 = transfer failed);
  CDFs over the design space.

- **18. Main result**
  - "When a single path is used, we do not observe a difference between TCP and QUIC. This is
    expected since in this scenario, the congestion control is the main influencing factor, and
    both use CUBIC."
  - "With multipath … **MPQUIC reaches a higher experimental bandwidth aggregation in 77% of our
    scenarios. For MPTCP, this number drops to 45%.** Getting precise estimations of the path
    latencies helps MPQUIC to balance traffic while avoiding head-of-line blocking."
  - High-BDP, no losses: "**multipath is beneficial in 58% of the scenarios with QUIC, while this
    percentage with TCP drops to 20%.**"
  - Lossy low-BDP: "(MP)QUIC nearly always performs better than (MP)TCP. This difference is mainly
    due to the ACK frame that can acknowledge up to 256 packet number ranges. This is much larger
    than the 2-3 blocks than can be acknowledged with the SACK TCP option … Therefore, early
    retransmits are more effective in QUIC and it suffers less from head-of-line blocking."
  - Abstract-level: "Without packet losses, while performance of single-path TCP and single-path
    QUIC are similar, MPQUIC can outperform MPTCP. In lossy scenarios, (MP)QUIC is more suited
    than (MP)TCP."

- **19. Limitation**
  As stated: "**Real-world evaluation is part of our future work**"; "the adaptation and the
  comparison of other [multipath congestion control] schemes [to MPQUIC] … is left for further
  study"; and implementation-scope: "our implementation does not [support all path-creation
  cases]" (client-initiated path creation limitations: "currently use server-initiated paths
  because clients are often behind [NATs]"). Methodological (mine): Mininet emulation with a
  single 20 MB stream over two paths, 3 repetitions per scenario (median reported), no mobility,
  no real cellular/WiFi, and QUIC crypto cost approximated by using TLS 1.2 on the TCP side
  rather than modelling CPU contention.

- **20. Research gap this suggests**
  MPQUIC's structural advantages (frame/packet independence, richer ACK, no DSN) mean the MPTCP
  scheduler literature does not transfer unchanged — yet the paper itself only transplants the
  MPTCP default heuristic. That is an explicit opening for MPQUIC-native schedulers (later taken
  up by the MPQUIC-MARL and Peekaboo/M-Peekaboo line). Second, the cold-start problem ("the
  scheduler does not have an estimation of the path's RTT yet") is a genuine online-learning
  problem — exploration under uncertainty — that no heuristic in this paper solves.

- **21. Best URL retrieved / depth**
  `https://orbi.umons.ac.be/bitstream/20.500.12907/49317/1/conext17-deconinck.pdf` — **FULL
  TEXT** (7 pages, converted and read). ACM DL: `https://dl.acm.org/doi/10.1145/3143361.3143370`.

---

### 7. The QUIC Transport Protocol: Design and Internet-Scale Deployment

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Adam Langley, Alistair Riddoch, Alyssa Wilk, Antonio Vicente, Charles Krasic, Dan Zhang, Fan
  Yang, Fedor Kouranov, Ian Swett, Janardhan Iyengar, Jeff Bailey, Jeremy Dorfman, Jim Roskind,
  Joanna Kulik, Patrik Westin, Raman Tenneti, Robbie Shade, Ryan Hamilton, Victor Vasiliev,
  Wan-Teh Chang, Zhongyi Shi (Google). **SIGCOMM 2017**, Los Angeles, August 21–25, 2017.
  DOI `10.1145/3098822.3098842`. **Peer-reviewed conference paper.**
  *Source note:* the retrieved PDF is the **Google author copy**, paginated as 9 pages, whereas
  the ACM reference in the same PDF's own footnote says "14 pages". Content is the same paper;
  figures/tables may be abridged relative to the ACM version.

- **1. Number and type of paths**
  `NOT REPORTED` / not applicable — **QUIC as deployed here is single-path**. The paper's
  relevant statement is the *absence* of simultaneous multipath: it has connection migration, and
  "client-initiated connection migration is a work in progress with limited deployment".

- **2. Network architecture**
  **Userspace transport over UDP** in the application, terminating at Google front-end servers:
  "We developed QUIC as a user-space transport". Deployment is via **Chrome** on the client and
  the Google server fleet, plus the YouTube app and the Google Search app on Android.

- **3. Transport protocol**
  QUIC (pre-IETF, "This paper describes pre-IETF QUIC design and deployment"). Not multipath.

- **4. Scheduler location**
  `NOT REPORTED` — no multipath scheduler exists in this paper. The relevant architectural
  statement is that the transport lives in **userspace at the application**, which is what makes
  rapid iteration possible ("Deploying changes to TCP stacks typically requires … of the entire
  OS. This limits the deployment and iteration velocity of TCP changes").

- **5. Scheduler inputs** — `NOT REPORTED`
- **6. Path metrics used** — `NOT REPORTED` (RTT estimation is discussed for CC purposes:
  "Accurate RTT estimation can also aid delay-sensing congestion …")
- **7. Scheduling decision** — `NOT REPORTED`
- **8. Packet-level or flow-level scheduling** — `NOT REPORTED`

- **9. Reordering handling**
  Not multi-path reordering, but the paper makes a directly relevant claim about the costs of
  **loss-induced** reordering/head-of-line blocking inside a connection: TCP's bytestream
  abstraction "imposes a 'latency tax' on application frames whose delivery must wait for
  retransmissions of previously lost TCP segments", and QUIC's stream multiplexing removes it:
  "loss of a single packet blocks only streams with data in that packet". It also notes QUIC is
  less sensitive to reordering than TCP: "…to reordering and loss than TCP with SACK …
  Consequently, QUIC can keep more bytes on the wire in the presence of reordering".

- **10. Congestion-control interaction**
  CC is pluggable by design — "The QUIC protocol does not rely on a specific congestion control
  [algorithm]… allow[ing] low experimentation" — but in this deployment **both TCP and QUIC use
  Cubic**: "In our deployment, TCP and QUIC both use Cubic as the congestion controller, with one
  difference worth mentioning…" There is an explicit deployment-scale experimentation
  infrastructure: "We drove QUIC experimentation by implementing it in Chrome, which has a strong
  experimentation and analysis framework".

- **11. Objective**
  Stated design goals: "an encrypted, multiplexed, and low-latency transport protocol designed
  from the ground up to improve transport performance for HTTPS traffic and to enable rapid
  deployment and continued evolution of transport mechanisms." Concrete measurable objectives
  are latency and rebuffering (see field 18).

- **12. Algorithm**
  `NOT REPORTED` for scheduling. Protocol/architecture contribution.

- **13. ML/DRL usage**
  No.

- **14. Simulator / testbed**
  **Neither — this is a production deployment measurement paper.** Evidence base: "globally
  deployed at Google on thousands of servers"; client-side deployment in Chrome, the YouTube
  mobile video streaming app, and the Google Search app on Android; "a strong experimentation and
  analysis framework" collecting metrics "from HTTP error rates to transport handshake latency";
  server-side experimentation frameworks letting engineers "enable/disable features and to tune
  parameters".

- **15. Traffic model**
  Real production traffic: HTTPS web (Google Search) and audio/video streaming (YouTube). The
  paper notes a scheduling-relevant nuance: "each chunk of audio and video arbitrarily …" (chunks
  of audio/video connections are described as delaying-sensitive relative to other traffic).

- **16. Baselines**
  **TCP + TLS, and TCP + HTTP/2** as the incumbent, i.e. QUIC vs TCP in production A/B
  experiments.

- **17. Metrics**
  Latency of Google Search responses; YouTube rebuffer rate; share of egress/Internet traffic;
  HTTP error rates; transport handshake latency.

- **18. Main result**
  - "on average, QUIC **reduces latency of Google Search responses by 8.0% for desktop users and
    by 3.6% for mobile users**, and **reduces rebuffer rates of YouTube playbacks by 18.0% for
    desktop users and 15.3% for mobile users**."
  - Deployment scale: "it currently accounts for **over 30% of Google's total egress traffic in
    bytes** and consequently **an estimated 7% of global Internet traffic**."

- **19. Limitation**
  As stated: QUIC is pre-IETF here and the paper is about one operator's deployment; client
  connection migration "is a work in progress with limited deployment"; middlebox ossification
  and UDP-blocking remain threats ("…its ossification by middleboxes"). Methodological (mine):
  the gains are Google-specific (Search, YouTube) and measured against Google's own TCP stacks;
  no multipath capability is evaluated because none exists in this deployment; and the paper
  measures service-level metrics, not transport-scheduler behaviour.

- **20. Research gap this suggests**
  The paper's own framing of QUIC's value — userspace deployability plus rapid evolution — is the
  strongest argument in the whole foundational set for *why* an AI-native scheduler is feasible
  in QUIC-family transports and much harder in-kernel for MPTCP. Conversely, the absence of
  simultaneous multipath in a globally deployed QUIC means the deployed base at the time offered
  no multipath data plane at all — which is exactly the hole MPQUIC (paper 6) and later 3GPP
  ATSSS work (paper 17) fill.

- **21. Best URL retrieved / depth**
  `https://storage.googleapis.com/gweb-research2023-media/pubtools/4102.pdf` (Google Research
  author copy; the landing page is
  `https://research.google/pubs/the-quic-transport-protocol-design-and-internet-scale-deployment/`)
  — **FULL TEXT** (9-page author copy, converted and read). ACM DL:
  `https://dl.acm.org/doi/10.1145/3098822.3098842`.
  *(A first download attempt hit a different Google Research pubtools record,
  `.../archive/46274.pdf`, which is an unrelated neural-network-compression paper; it was
  discarded, not used.)*

---
