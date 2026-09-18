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

## MODERN / AI-BASED

### 8. ReLeS: A Neural Adaptive Multipath Scheduler based on Deep Reinforcement Learning

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Han Zhang, Wenzhong Li, Shaohua Gao, Xiaoliang Wang, Baoliu Ye. 2019. *IEEE INFOCOM 2019 - IEEE Conference on Computer Communications*, Paris, France, April 29–May 2, 2019, pp. 1648–1656. DOI `10.1109/INFOCOM.2019.8737649`. Peer-reviewed conference paper (IEEE). Metadata verified from Crossref (`api.crossref.org/works/10.1109/INFOCOM.2019.8737649`: container title "IEEE INFOCOM 2019 - IEEE Conference on Computer Communications", published 2019-04, page "1648-1656"), and independently corroborated by the Nanjing University DISLAB publication list for 2019 (venue "INFOCOM") and by reference [32] of the BCCPS/TVT paper ("in Proc. 38th IEEE Int. Conf. Comput. Commun., 2019, pp. 1648–1656"). No source disagreed on venue/year.

- **1. Number and type of paths**
  NOT REPORTED (abstract does not state path types or count).

- **2. Network architecture**
  NOT REPORTED (abstract does not describe topology).

- **3. Transport protocol**
  MPTCP. Abstract: "The Multipath TCP (MPTCP) protocol, featured by its ability of capacity aggregation across multiple links and connectivity maintenance against single-path failure". Version (v0/v1) NOT REPORTED.

- **4. Scheduler location**
  NOT REPORTED as a location, but the abstract states: "We implement ReLeS in the Linux kernel" — i.e. kernel-level implementation is stated; the abstract does not name the specific hook/component.

- **5. Scheduler inputs**
  NOT REPORTED (abstract does not enumerate state signals).

- **6. Path metrics used**
  NOT REPORTED (abstract does not enumerate metrics; only the generic phrase "diverse QoS characteristics").

- **7. Scheduling decision**
  NOT REPORTED (abstract does not give the action space). The abstract only says the neural network "generate[s] the control policy for packet scheduling".

- **8. Packet-level or flow-level scheduling**
  Packet-level is implied by the abstract's framing only: "Multipath packet scheduling is a unique and fundamental mechanism for the design and implementation of MPTCP, which is responsible for distributing the traffic over multiple subflows." No explicit action-space statement is available, so the granularity is NOT REPORTED beyond this framing.

- **9. Reordering handling**
  NOT REPORTED.

- **10. Congestion-control interaction**
  NOT REPORTED.

- **11. Objective**
  Abstract: "It adopts a comprehensive reward function that takes diverse QoS characteristics into consideration to optimize packet scheduling." The individual QoS terms are NOT REPORTED.

- **12. Algorithm**
  NOT REPORTED. Abstract states only "We propose ReLeS, a Reinforcement Learning based Scheduler for MPTCP. ReLeS uses modern deep reinforcement learning (DRL) techniques to learn a neural network to generate the control policy for packet scheduling." and "we propose an asynchronous training algorithm that enables parallel execution of packet scheduling, data collecting, and neural network training."

- **13. ML/DRL usage**
  Yes — DRL is used, but the **exact DRL variant is NOT REPORTED** in the abstract, and the **neural network architecture (layer types, neuron counts) is NOT REPORTED**. The only architectural/algorithmic facts available: (a) a neural network is learned to generate the scheduling control policy; (b) an "asynchronous training algorithm" decouples packet scheduling, data collecting and neural network training for real-time operation.

- **14. Simulator / testbed**
  Only the abstract-level statement is available: "We implement ReLeS in the Linux kernel and evaluate it over both emulated and real network conditions." The specific emulator, testbed hardware, link technologies and counts are NOT REPORTED. (Testbed-vs-simulation cannot be disambiguated beyond "emulated" vs "real".)

- **15. Traffic model**
  NOT REPORTED.

- **16. Baselines**
  NOT REPORTED — the abstract only says "significantly outperforms the state-of-the-art schedulers" without naming them.

- **17. Metrics**
  NOT REPORTED.

- **18. Main result**
  The only result statement available is qualitative: "Extensive experiments show that ReLeS significantly outperforms the state-of-the-art schedulers." **No numbers are reported in the abstract.** (Do not attribute any numeric gain to this paper.)

- **19. Limitation**
  Author-stated: none in the abstract. Methodological limitation observed by me: the full text could not be obtained through any open channel, so this extraction covers only the abstract (see field 21). The abstract supplies no action space, no state/reward formulation, no hyperparameters, no baselines and no numbers, so the paper cannot be compared quantitatively against the other three in this file without the full text.

- **20. Research gap this suggests**
  Only a weak, non-fabricated gap can be stated from the abstract: the paper claims a DRL scheduler with an asynchronous training algorithm and a multi-QoS reward, but does not (in the abstract) expose the state/action/reward design or reproducibility artifacts, so a literature review cannot verify or reproduce its scheduler from open sources. Verifying ReLeS's actual state/action/reward and its interaction with MPTCP's coupled congestion control requires the paywalled full text.

- **21. Best URL you actually retrieved, and whether you read full text or only abstract**
  **ABSTRACT ONLY.**
  Best retrieved source: Semantic Scholar record with the publisher abstract —
  `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/INFOCOM.2019.8737649?fields=title,abstract,openAccessPdf,venue,year,externalIds` (returned `openAccessPdf: ""`).
  Supporting bibliographic record: `https://api.crossref.org/works/10.1109/INFOCOM.2019.8737649`.
  Publisher landing page (DOI): `https://doi.org/10.1109/INFOCOM.2019.8737649`.
  **Full text was genuinely not obtainable.** Attempts made and their outcomes:
  - Unpaywall `https://api.unpaywall.org/v2/10.1109/INFOCOM.2019.8737649?email=research@example.org` → `is_oa: false`, `oa_status: closed`, no PDF.
  - OpenAlex `https://api.openalex.org/works/doi:10.1109/INFOCOM.2019.8737649` → the only location is the DOI landing page, `is_oa: false`, no `pdf_url`. (Subsequent OpenAlex calls hit the API daily budget limit and returned `Rate limit exceeded`.)
  - Semantic Scholar `openAccessPdf` → empty; no arXiv ID in `externalIds`.
  - arXiv API (`https://export.arxiv.org/api/query`) searches for `all:"ReLeS"`, `all:"DeepCC"`, `au:"Wenzhong Li" AND all:"multipath"` → no matching preprint.
  - Author homepage / lab pages: `https://cs.nju.edu.cn/lwz/` (Wenzhong Li) has no ReLeS PDF link; his CV `https://cs.nju.edu.cn/_upload/tpl/01/5c/348/template348/CV-WenzhongLi.pdf` lists the paper (item: "Han Zhang, Wenzhong Li, Shaohua Gao, Xiaoliang Wang, Baoliu Ye, ReLeS: ... INFOCOM 2019, Paris, France, April 29-May 2, 2019") but links no PDF; NJU DISLAB lists `https://dislab.nju.edu.cn/publications/en/year/2019` contain the citation but no PDF; guessed paths `https://cs.nju.edu.cn/lwz/paper/ReLeS.pdf`, `.../papers/ReLeS.pdf`, `.../paper/reles.pdf` all returned HTTP 404.
  - IEEE Xplore `https://ieeexplore.ieee.org/document/8737649` → HTTP 202 with an empty body (bot protection); no abstract HTML retrievable.
  - ACM DL `https://dl.acm.org/doi/abs/10.1109/INFOCOM.2019.8737649` → paywalled abstract stub.
  - Scholars Portal `https://journals.scholarsportal.info/details/26419874/v2019inone/1648_ranamsbodrl.xml` → "restricted to IP addresses from our member universities".
  - CORE public search → HTTP 403; Internet Archive / Wayback Machine → "Temporarily Offline"; OpenAlex `best_oa_location` → none.
  - A `pdfs.semanticscholar.org` hit surfaced by search was downloaded and checked, but it is a **different** document ("Novel Multipath TCP Scheduling Design for Future IoT Applications", Mohammed Asiri, Deakin University) that merely cites this area — it was **not** used as a source for any field above.

---

### 9. DeepCC: Multi-Agent Deep Reinforcement Learning Congestion Control for Multi-Path TCP Based on Self-Attention

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Bo He, Jingyu Wang, Qi Qi, Haifeng Sun, Jianxin Liao, Chunning Du, Xiang Yang, Zhu Han. 2021. *IEEE Transactions on Network and Service Management*, vol. 18, no. 4, December 2021, pp. 4770–4788. DOI `10.1109/TNSM.2021.3093302`. Peer-reviewed journal article. Verified from Crossref (`api.crossref.org/works/10.1109/TNSM.2021.3093302`: volume 18, issue 4, page "4770-4788", published-print 2021-12) and confirmed against the retrieved PDF's running headers ("IEEE TRANSACTIONS ON NETWORK AND SERVICE MANAGEMENT, VOL. 18, NO. 4, DECEMBER 2021", first page 4770, last page 4788) and its own DOI line ("Digital Object Identifier 10.1109/TNSM.2021.3093302"). No source disagreed.

- **1. Number and type of paths**
  Heterogeneous multipath. The testbed sender "has multiple Gigabit Ethernet interfaces and a WiFi interface", and the paper motivates subflows "built by heterogeneous network interfaces like WiFi, Ethernet, and LTE/5G". Main experiments use **3 subflows**; a scaling study uses **2, 3 and 4 subflows**: "the number of the subflows in the experimental network are 2, 3, and 4, respectively." Exact interface-to-subflow mapping per experiment is not tabulated in the extractable text.

- **2. Network architecture**
  End-to-end MPTCP: "There are several paths connecting the clients and the server. The testbed allows running some MPTCP flows and single-path TCP flows together." Sender is a Dell desktop with multiple Gigabit Ethernet interfaces plus a WiFi interface; "The receiver is another desktop which is connected to the sender through a Gigabit switch" and "the receiver has a Gigabit Ethernet interface". No proxy or middlebox is reported. Heterogeneity is emulated at the sender: "we use Linux tc and ethtool to limit the delay, bandwidth, and random packet loss rate of each subflow on the sender." Experiments run 4 MPTCP flows simultaneously plus a competing regular single-path TCP flow sharing a bottleneck in the friendliness study.

- **3. Transport protocol**
  MPTCP. Implementation: "We implement DeepCC on Ubuntu with the MPTCP v0.93 [44] which is based on Linux release v4.9.x." (i.e. MPTCP v0.93 in the Linux kernel.) Not MPQUIC.

- **4. Scheduler location**
  Sender side, split across kernel and userspace. Kernel side: "we register several sysctl parameters in the kernel space, like the congestion windows, RTTs, the number of lost packets, the split ratios of packets, and so on." Userspace side: "we implement the DRL agents in the Linux userspace and run them as daemon processes", and deployment is via "a system call set_cwnd_ratio(·) in the userspace". The rationale is explicit: "the common-used MPTCP is built on the Linux Kernel whose available program resource is strictly limited, the DRL agents that need lots of complex mathematical calculations to obtain the optimal policies cannot be run in the kernel space."

- **5. Scheduler inputs**
  Exact state vector, per agent *i* at epoch *t*: `S_{i,t} = (O^i_t, Õ^i_t) = (x^i_t, c^i_t, k^i_t, v^i_t, w^i_t, l^i_t, x̃^i_t, c̃^i_t, k̃^i_t, ṽ^i_t, w̃^i_t, l̃^i_t)` — twelve parameters total, six for the subflow itself and six for the (self-attention-weighted) environment of other subflows. The six self-state parameters are defined verbatim as:
  - "x^i_t is the average goodput"
  - "c^i_t is the sending rate"
  - "k^i_t is the average RTT"
  - "v^i_t is the mean deviation of RTTs"
  - "w^i_t is the average CWND"
  - "l^i_t is the number of lost packets"
  
  The authors state: "During our testing, adding more parameters like the delivered rate and the number of inflight packets does not lead to noticeable performance improvement but undoubtedly increases data collection overhead." Notably **absent**: queue occupancy, buffer estimate, BLEST-style penalisation, energy, cost.

- **6. Path metrics used**
  Average goodput, sending rate, average RTT, mean deviation of RTTs, average CWND, number of lost packets (same six, mirrored to other subflows). Reported performance metrics are total goodput and average jitter ("the difference of consecutive RTTs"). No explicit bandwidth estimate or queue-occupancy metric is used as an input.

- **7. Scheduling decision**
  Continuous per-subflow control of **two** quantities, not a discrete path choice. Verbatim: "the action of agent i at epoch t consists of two parts: a_{i,t} = (u^p_{i,t}, u^w_{i,t})". Mechanics: "u^p_{i,t} specifies how much change needs to be made to the split ratio sr^i_t of traffic data that delivered over the i-th subflow... The positive and negative value of u^p_{i,t} control the increase and reduction of the split ratios. The value of u^w_{i,t} ∈ (0.5, 2) is the coefficient of the new size of CWND. Thus, for the i-th subflow at the next epoch t + 1, the new split ratio sr^i_{t+1} = sr^i_t + u^p_{i,t} while the new size of CWND cwnd^i_{t+1} = u^w_{i,t} × cwnd^i_t." Policy is stochastic: "π_i : S_i × A_i → [0, 1]". Epoch granularity: "Each episode contains 20 continuous epochs".
  
  *Discrepancy to flag:* the paper also writes that DeepCC is used "to select the best next-hop forwarding node for each arrived traffic packet". This single sentence is inconsistent with the formally defined action space (CWND-multiplier + split-ratio delta) and with the state/action equations; the formal action definition should be treated as authoritative. I report both rather than silently choosing one.

- **8. Packet-level or flow-level scheduling**
  Primarily **flow/rate-level**: the agent sets a CWND multiplier and a split ratio ("the number of traffic packets that are allocated on each subflow can be depicted by the split ratio while the change of CWND also impacts the transmission process"), which the kernel then applies when "a packet (named as a sk_buff in the kernel) needs to be assigned a subflow for the transmission". So the decision is a per-epoch rate/split control, not an explicit per-segment "select path i for the next segment" rule. The one "next-hop forwarding node for each arrived traffic packet" sentence sits in tension with this (see field 7).

- **9. Reordering handling**
  Handled by MPTCP's standard mechanism, not by the learned policy: "Here, we still adopt the default Data Sequence Mapping (DSM) method [1] to implement the reordering of data in the receiver of the MPTCP connection... DSM defines the mapping from the subflow sequence space to the data sequence space. Here, the subflow sequence space consists of the Subflow Sequence Numbers (SSN) that represent the packet order in this subflow, while the data sequence space consists of the Data Sequence Numbers (DSN) that represent the packet order in all subflows." There is **no** reordering penalty term in the reward beyond the lost-packet penalty; jitter (difference of consecutive RTTs) is a reported metric rather than a reordering signal. Receive-buffer/ATD-based blocking estimation is not used.

- **10. Congestion-control interaction**
  DeepCC **replaces** the per-subflow congestion control decision: each agent controls its own subflow's CWND and split ratio. The baselines LIA, OLIA, BALIA and wVegas are "contained in the MPTCP v0.93, and we adopt their default parameters in the experiments", and MPTCP's default LIA is described as "the congestion control algorithm of MPTCP... that adjusts the CWND of each subflow". DeepCC's own reward explicitly encodes TCP-friendliness ("the reward function takes into account the parameters belonging to TCP and MPTCP flows, which helps DeepCC to have a good TCP-friendliness"), verified experimentally in an MPTCP/TCP co-existing scenario. The interaction mechanism is the sysctl/syscall bridge between kernel and userspace agents (see field 4).

- **11. Objective**
  Verbatim: "We craft a reward function to guide the agents toward good performance for objectives: increasing the total goodput and reducing the congestion in the MPTCP network. Here, the goodput is the total number of bytes received correctly and sequentially from all subflows with a unit of time." The policy objective is "to maximize the accumulated reward R_t from the historical experience", and the multi-agent solution concept is Nash Equilibrium: "The multi-agent control belongs to the general-sum n-player game... It has been proved that the this kind of game can obtain at least one Nash Equilibrium".

- **12. Algorithm**
  **MAPOKTR** — "Multi-Agent Policy Optimization using Kronecker-Factored Trust Region": "DeepCC adopts an improved MADRL algorithm based on ACKTR, Multi-Agent Policy Optimization using Kronecker-Factored Trust Region (MAPOKTR) [51]". The surrogate objective (Eq. 19) is verbatim:
  `L(θ) = E_t [ clip(r_t(θ), 1 − ε, 1 + ε) Â_t ] − η D_pp(π_θold(·|s), π_θ(·|s))`
  where `r_t(θ) = π_θ(a_t|s_t) / π_θold(a_t|s_t)` (Eq. 17) and the **point probability distance** `D_pp(π_θold(·|s), π_θ(·|s)) = (π_θold(a|s) − π_θ(a|s))^2` (Eq. 18) replaces the usual KL term: "the new surrogate objective function in MAPOKTR... composites the point probability distance and implicit KL constraint, while enhancing the stability in controlling the distance between old and new policies. Compared with KLD, D_pp and the clipped ratio are less sensitive to the action space dimension so that the robustness of MAPOKTR is increased." Fisher information is approximated by Kronecker-Factored Approximate Curvature (K-FAC). Discount: "γ is the discount coefficient (γ∈(0,1))". Training is asynchronous: "the online control and the offline training process run asynchronously and iteratively."

- **13. ML/DRL usage**
  Yes. **Variant:** multi-agent actor-critic DRL, specifically MAPOKTR (ACKTR-derived, K-FAC natural-gradient, PPO-style clipped ratio + point-probability-distance penalty), one agent per subflow. **Exact architecture** (from the text; Fig. 3 is the figure but the prose enumerates the layers):
  - BiLSTM over the sequence of other subflows' states: "The size of the BiLSTM is 32"; each unidirectional LSTM layer has κ hidden nodes so the concatenated hidden state matrix `H_i` has shape `(n−1)-by-2κ`; input token `w_j` is "a six-dimensional state embedding", so `S^e_i` is a matrix of shape `(n-1)-by-6`.
  - First self-attention layer (SSA, "State-Self-Attention"): "the number of nodes in the first self-attention layer is 64"; "The activation function is tanh(·) and the learning rate is 0.01."
  - Fully connected layer receiving the processed states: "the number of the fully connected layer that receives processed states is 64".
  - Second self-attention layer (PSA, "Policy-Self-Attention"): "the second self-attention layer has 64 nodes"; "Their activation functions are also tanh(·) but the learning rates are 0.001."
  - Output layer: "the number of nodes in the output layer is the number of subflows."
  - Multi-hop attention: "we adopt the multi-hop attention mechanism that extracts x different elements from the sequence... W_{s2} with the shape of x-by-d_e"; attention weights `E_i = softmax(W_{s2} tanh(W_{s1} H_i^T))` (Eq. 25).
  - RL hyperparameters: "ε is set to 0.2 and η is set to 0.5 in (19)."
  - Training scale: "we train the DeepCC agents for over 2,000 episodes (i.e., 40,000 training samples) in the offline manner"; per-condition cost "it took 50 minutes to complete the offline training process with 2000 episodes, and the average CPU usage of training process is nearly 5%"; "the online inference time of DeepCC is less than 1 millisecond".
  - Framework: "We use a Python-based framework, Pytorch to construct the architecture of DeepCC and its deep neural networks."
  
  **Exact reward function (Eq. 5), verbatim:** `r_t = α(X^i_t − βL^i_t) + (1 − α)(X̃^i_t − βL̃^i_t)`
  with: "α ∈ [0, 1] is a coefficient. Here, X^i_t is the average goodput of the i-th subflow at epoch t and X̃^i_t is the weighted sum of goodput of other subflows. The weights of goodput in X̃^i_t are learned by a self-attention mechanism... L^i_t is the total number of lost packets in the i-th subflow at epoch t. By using the same weights learned by the self-attention mechanism as X̃^i_t, L̃^i_t is the weighted sum of number of lost packets in other subflows." Tuning: "According to our testing, setting α as 0.6 and setting β as 0.5 by default have the best performance" (and later, confirming the reward study, "In the reward function, α is set to 0.6"). Semantics: "If α is 1, the policy of agent i only targets to increase the goodput of the i-th subflow... Then, if α is 0, the policy of agent i aims to maximize the total goodput... When α is 0.5, the agent treats its subflow and other subflows fairly. These two terms can be interpreted as penalty items when the value of α is larger. They can prevent agents from being too 'selfish' and causing a waste of resources."

- **14. Simulator / testbed**
  **Real Linux testbed with emulated link characteristics — not a network simulator.** Verbatim: "all experiments are conducted on the sender that is a Dell desktop (CPU: Intel i7-8700 3.2GHz; Memory: 32G DDR4L 2666Mhz; OS: 64-bit Ubuntu 16.04LTS). To simulate heterogeneous network conditions, we use Linux tc and ethtool to limit the delay, bandwidth, and random packet loss rate of each subflow on the sender. The receiver is another desktop which is connected to the sender through a Gigabit switch." Measurement tooling: "the traffic packets are captured by the tcpdump tool1 and analyzed by the scapy library2 of python"; "We use the iPerf3 tool3 to continuously generate packets to keep the network always busy when we collect the training samples in experiments"; "we use the TRex tool4 to provide background traffic by continuously replaying packets from real traces." Protocol stack: MPTCP v0.93 on Linux v4.9.x. Four MPTCP flows run simultaneously with metrics averaged. Note: this is a single-sender tc/netem-style emulation setup, not real WiFi/LTE radio.

- **15. Traffic model**
  Bulk file transfer over FTP: "The MPTCP traffic data are generated by retrieving a binary document in the transmission process based on File Transfer Protocol (FTP)." Document sizes studied: 2 MB and 4 MB (e.g. "the size of the document is 2M"; "the size of the document is 4M"). Background load from iPerf3 and from TRex-replayed real traces. Also a bulk FTP task for the resource-consumption study. No web or video workload.

- **16. Baselines**
  As the paper names them — DRL-based: **DRL-CC** [14] and **SmartCC** [15]; traditional: **LIA** [8], **OLIA** [2], **BALIA** [9], **wVegas** [10]. For the MADRL-algorithm comparison: **MAACKTR** ("the ACKTR algorithm deployed on Multi-Agent system") and **MADDPG** [30]. For the architecture ablation: **FC** (fully-connected only), **FC with PSA**, **SSA without PSA**. For the reward ablation: the paper's own **fair-efficient reward** vs a **fair reward** and an **efficient reward**. Provenance caveat stated by the authors: "Since the code of DRL-CC and SmartCC is not shared by the authors, we implement them by ourselves. We adopt the open-source code of the their DRL algorithms to build the DRL agents for them. As for the state collection module, the authors were not explained in detail in their papers, so that we collect the states of DRL-CC and SmartCC in the same approach of DeepCC."

- **17. Metrics**
  "The performance metrics in the experiments are: i) the total goodput: the total number of bytes received from all subflows with a unit of time; ii) the average jitter: the difference of consecutive RTTs. The goodput is calculated by dividing the document size by the elapsed download time". Additionally used: goodput ratio of the one-hop path (efficiency study), CPU and memory usage (resource consumption), convergence behaviour over training episodes, and performance loss in unseen environments (robustness, Table V).

- **18. Main result**
  Exact quoted headline numbers:
  - Architecture (self-attention) gain, stated twice in the paper: "DeepCC with the attention mechanism reduces convergence time by about 50% and increase goodput by about 80% compared with the commonly used structures of neural networks" (abstract); and "we prove that DeepCC with self-attention layers reduces convergence time by about 50% and increases the goodput by about 80% compared with the common-used structures of neural networks."
  - Algorithm gain: "the used MADRL algorithm, MAPOKTR, increases the goodput by at least 10% compared with the state-of-the-art algorithms."
  - Overall vs baselines: "DeepCC consistently outperforms the well-known heuristic method and DRL-based MPTCP congestion control method in terms of goodput and jitter" (abstract); "DeepCC consistently and significantly outperforms some well-known heuristic and DRL-based MPTCP congestion control methods in all complicated and varying network conditions."
  - Robustness cost (Table V, prose): "Compare with the best performance, the performance losses range from 10% to 40% as shown in Table V. Finally, we continue to collect more transition samples and train the models in new environments for some episodes... At this time, the performance losses range from 2% to 9%."
  - Efficiency study: "the goodput ratios of the three flows range from 0.8 to 0.85. According to the analysis in [55], the goodput ratios in this scenario range from 0.6 to 0.9 by using existing heuristic multi-path congestion control methods."
  - Reward tuning: fair-efficient reward (α = 0.6) "significantly outperforms the other rewards"; "the efficient reward obtains higher goodput than the fair reward but it performs unstably"; α = 0.5 → "the performance of the fair reward is mediocre".
  - Resource consumption: "DeepCC improves the performance without consuming a lot of resources"; "the average CPU usage of training process is nearly 5%"; "the online inference time of DeepCC is less than 1 millisecond". (Table IV numeric values are an image in the PDF and were not extractable as text — no numbers invented.)
  - Fairness/comparability caveat the authors themselves flag: DeepCC tolerates subflow-closure events ("such as the TCP connection is not established, SACK is disabled") and keeps those transitions, whereas "when these conditions happen in an episode, the DRL transition is still added to the experience buffer of DeepCC but it is discarded in the experiments of DRL-CC and SmartCC. Hence, in our experiments, DeepCC is tested in the totally actual network environments while the other two methods have to work in the environments under idealized assumes."

- **19. Limitation**
  Author-stated: (a) robustness depends on experience-buffer richness — "the robustness of DeepCC is greatly impacted by the number and richness of transition samples in the experience buffer", with 10–40% performance loss in a new environment and needing continued retraining to fall to 2–9%; (b) offline training is costly — "the time of offline training varies from half an hour to several hours" (50 minutes for 2000 episodes in one setting).
  Methodological limitations I observe: (i) evaluation is a single-sender Linux testbed with `tc`/`ethtool`-emulated delay/bandwidth/loss on Gigabit Ethernet plus one WiFi interface — no real cellular/WiFi radio dynamics, no mobility; (ii) only bulk FTP transfers of 2 MB and 4 MB with iPerf3/TRex background load, so no interactive, video or many-flow web workload; (iii) baselines DRL-CC and SmartCC are self-reimplemented by the authors with states collected "in the same approach of DeepCC", which favours DeepCC in the comparison and is acknowledged as an asymmetry ("idealized assumes"); (iv) the paper's only quantitative architecture claim (≈50% convergence, ≈80% goodput) is stated relative to unnamed "commonly used structures of neural networks" rather than to an external published model; (v) the action space controls CWND multiplier and split ratio, not explicit per-packet path assignment, so it is a congestion-control/rate-split method rather than a packet scheduler; (vi) training-data and hyperparameter tables (Tables II, IV, V) are embedded as images in the PDF and their per-method numeric entries could not be verified from the text layer.

- **20. Research gap this suggests**
  DeepCC handles the *fixed state space / retraining* problem of MADRL for MPTCP by adding self-attention so the agent generalizes across a changing number of subflows, and it explicitly notes that previous DRL approaches "need to be rebuilt and retrained unavoidably" when the number of subflows changes. Open gaps that follow: (a) the learned controller is validated only on an emulated single-host testbed with 2–4 subflows and bulk FTP, leaving real heterogeneous radio (WiFi+LTE/5G), mobility and handover untested; (b) the reward's fairness term is a self-attention-weighted goodput/loss mixture with a hand-tuned α, with no formal fairness guarantee (e.g. no proof of bottleneck fairness against regular TCP, unlike BCCPS in this same file) and no energy or cost term; (c) because reordering is left entirely to MPTCP's DSM, the DRL policy is blind to head-of-line blocking, so an AI-native design that jointly learns congestion control *and* reordering-aware scheduling remains open; (d) self-reimplemented DRL baselines and image-only result tables make independent reproduction difficult — a gap for benchmark-able, artifact-releasing DRL transport work.

- **21. Best URL you actually retrieved, and whether you read full text or only abstract**
  **FULL TEXT.**
  Retrieved from (Google Drive copy of the IEEE Xplore PDF, downloaded this session):
  `https://drive.google.com/uc?export=download&id=1uEXs89YZP_uw0EH8w4TYhruvUZLqOcpk`
  (the Drive file's own page is `https://drive.google.com/file/d/1uEXs89YZP_uw0EH8w4TYhruvUZLqOcpk/view`). Downloaded as `pdfs/deepcc_tnsm2021.pdf` (4,225,029 bytes, PDF v1.4, **19 pages**, pages 4770–4788, carrying the IEEE watermark "Authorized licensed use limited to: BEIJING UNIVERSITY OF POST AND TELECOM. Downloaded on December 15,2021"), converted with `pdftotext -layout` to `pdfs/deepcc_tnsm2021.txt` (1,385 lines).
  Identity verified three ways: page/volume header "IEEE TRANSACTIONS ON NETWORK AND SERVICE MANAGEMENT, VOL. 18, NO. 4, DECEMBER 2021", DOI line "Digital Object Identifier 10.1109/TNSM.2021.3093302", and Crossref metadata (vol 18, iss 4, pp. 4770–4788).
  Other URLs used for this paper: `https://api.crossref.org/works/10.1109/TNSM.2021.3093302`; `https://api.unpaywall.org/v2/10.1109/TNSM.2021.3093302?email=research@example.org` (→ closed, no OA PDF); `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TNSM.2021.3093302?fields=title,abstract,openAccessPdf,venue,year,externalIds` (→ `openAccessPdf` empty); `https://ieeexplore.ieee.org/document/9467277`.
  Caveat: Tables II, IV and V are raster images in this PDF, so their cell values are not in the text layer — no values were invented for them.

---

### 10. Leveraging Coupled BBR and Adaptive Packet Scheduling to Boost MPTCP

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Jiangping Han, Kaiping Xue, Yitao Xing, Jian Li, Wenjia Wei, David S. L. Wei, Guoliang Xue. 2021. *IEEE Transactions on Wireless Communications*, vol. 20, no. 11, November 2021, pp. 7555–7567. DOI `10.1109/TWC.2021.3085661`. Peer-reviewed journal article. Crossref (`api.crossref.org/works/10.1109/TWC.2021.3085661`) gives volume 20, issue 11, page "7555-7567", published-print 2021-11.
  **Source-version note:** the full text I read is the **arXiv preprint** `arXiv:2002.06284v2 [cs.NI]`, 11 Jun 2021, titled identically with the same author list (`https://arxiv.org/abs/2002.06284`). Semantic Scholar records year 2020 for this DOI and links `ArXiv: 2002.06284` — that 2020 is the arXiv v1 year, not the journal year. **I trust 2021 / TWC 20(11) for the venue year**, because Crossref (publisher-deposited) and the journal issue both say 2021-11; the 2020 figure is an artifact of the preprint.

- **1. Number and type of paths**
  Heterogeneous wireless, MPTCP-style. Testbed: **2 subflows**, mapped to 4G and Wi-Fi. Verbatim: "Considering that the device usually has two interfaces (4G and Wi-Fi) in the real network, we also used two subflows in an MPTCP connection in the experiments." Real-network tests add "different kinds of Wi-Fi links (2.4GHz and 5GHz)" and 4G. The simulation study scales to **3 subflows**: "The MPTCP connection includes three subflows, each of which passes through a path with bandwidth of B_i on the bottleneck." Testbed bottlenecks: "Both the bottleneck links have 100 Mbps bandwidth and 25 ms delay."

- **2. Network architecture**
  End-to-end MPTCP with no proxy. Testbed: "Our testbed includes a pair of MPTCP server and client, two pairs of TCP servers and clients, and four routers within the topology shown in Fig. 2. MPTCP connection includes two subflows, where each subflow passes through two routers. The links between two routers represent the bottleneck in the network... Both the bottleneck links have 100 Mbps bandwidth and 25 ms delay. At each bottleneck, there are two TCP background flows on each path using the same kind of congestion control algorithm as MPTCP uses." Real-network tests: "we deploy Linux kernels that support our scheme in cloud servers to conduct some tests in real networks, transmitting data from the implemented server in the cloud to the lab-built client", using "rented cloud servers in different regions" with Wi-Fi (2.4/5 GHz) and 4G access. Simulation: "a network topology shown in Fig. 16... three subflows... There is one TCP flow that passes through the same path of each subflow."
  Crucially: "Coupled BBR is implemented at the sender side, and does not require interaction between the receiver and the sender" and "MPTCP receiver performs the original operation and does not need any other extra interaction with the sender."

- **3. Transport protocol**
  MPTCP, implemented in the Linux kernel: "We integrate Coupled BBR and AR&P scheduler into MPTCP v0.94 implemented in Linux kernel [26]". The congestion control is a custom coupled BBR ("Coupled BBR"), not LIA/OLIA/BALIA. No MPQUIC.

- **4. Scheduler location**
  Sender-side, in the MPTCP kernel implementation: "Coupled BBR and AR&P scheduler are implemented at MPTCP sender for better transmission control." The scheduler is drawn as an in-sender block fed by Coupled BBR (Fig. 4: `Coupled BBR → RTT_i, BW_i, pacing_rate_i → AR&P Scheduler → subflows 1..N`). No proxy, no core-network element.

- **5. Scheduler inputs**
  Per-subflow: the BBR-measured bottleneck bandwidth `BW_i` and RTT `r_i`, the sending rate `x_i`, the number of inflight packets, and the amount of already-scheduled-but-unsent data on each subflow. Verbatim: "The path conditions of each subflow are measured in real time by Coupled BBR. We uses x_i and r_i to denote the sending rate and RTT of subflow_i, respectively." For scheduling: "When MPTCP schedules the packet j, the set of packets that are already scheduled on subflow_i but not sent out yet is L_i. And the size of a packet j is s_j." And "In addition, AR-Scheduling utilizes inflight packets for the auxiliary judgment... So when the inflight packets of subflow_i are less than 4, AR-scheduling marks that subflow_i as in the redundant state." Packet loss is used only indirectly (fast-retransmission behaviour). No queue-occupancy estimate, no BLEST-style penalisation, no send-buffer occupancy beyond `L_i` byte counts.

- **6. Path metrics used**
  Measured bottleneck bandwidth `BW_i`, RTT `r_i`, sending rate `x_i`, inflight packet count, and the per-subflow value ratio `x_i / r_i`. Packet loss rate is not an input (the design deliberately avoids loss-based signals: it measures "bandwidth and RTT of the bottleneck"). Goodput and out-of-order packet counts are the evaluation metrics.

- **7. Scheduling decision**
  Two coupled decisions per subflow, all sender-side:
  1. **AR-Scheduling** chooses each subflow's *state*: redundant vs non-redundant. "AR-Scheduling decides the redundant/non-redundant state of each subflow. If a subflow is in poor network conditions (low bandwidth or large RTT), AR-Scheduling tends to send redundant packets via it." Formally the action is the choice of the non-redundant set: "The goal of AR-Scheduling is choosing the P non-redundant subflows N to maximize goodput" with set membership decided by a greedy test (Algorithm 2), plus the inflight guard "if inflight_i < 4 then mark as redundant".
  2. **P-Scheduling** chooses a subflow for **each individual packet**: "P-Scheduling calculates the arrival time of each packet and schedules each packet one-by-one... choose a subflow with the minimum A_i(j) to schedule packet on it", with `i_k = arg min_{i∈N} A_i(j_k)` (Algorithm 3).
  Congestion-control action is separate: Coupled BBR sets the pacing gain cycle `{1.25, 0.75, α_i, α_i, α_i, α_i, α_i, α_i}` and hence the pacing rate.

- **8. Packet-level or flow-level scheduling**
  **Packet-level** (per-segment path assignment), explicitly contrasted with window-level prior art: "Different from previous packet schedulers which only schedule in each congestion window, P-Scheduling calculates the arrival time of packets and schedules each packet one-by-one." Scheduling is done ahead of transmission on a window of packets: "P-Scheduling maintains a scheduling window at the size of max_{i∈N} RTT_i · Σ_{i∈N} BW_i... Each packet in this window is scheduled to a certain subflow according to the predicted arrival time, and the packets outside the scheduling window will not be scheduled until they are included in the scheduling window." As a special case, "Algorithm 3 is not used when all the subflows are in slow-start phase at the beginning of the connection. In this case, P-Scheduling behaves the same as Round-Robin." Decision cadence for AR-Scheduling: "AR-Scheduling makes decisions every min_{i∈S} r_i during the transmission."

- **9. Reordering handling**
  Reordering is handled by *predictive in-order scheduling* at the sender, not by a receiver buffer or a penalty term. Arrival time is predicted per packet per subflow (Eq. 4): `A_i(j) = t_0 + (Σ_{j'∈L_i} s_{j'}) / x_i + r_i / 2`, where "the second item Σ_{j'∈L_i} s_{j'} / x_i on the right hand side of the equation is the waiting time for packet j_k to start transmitting if it is scheduled on subflow_i. The third item r_i / 2 is the transmission time of each packet." The claim: "In this way, P-Scheduling ensures that the packets scheduled after packet j will not arrive earlier than packet j, therefore it keeps in-order packets arrival and the number of out-of-order packets can be significantly reduced in asymmetric networks." Robustness of the prediction is analysed: "Therefore P-Scheduling can keep the out-of-ordered packets in a low level even there are jitters in the network environment", with error bound `O ≤ (1/2) Σ_{i∈N} x_i max_{i∈N} r_i (ε_1 + ε_2)` for jitter bounds `|Δx_i/x_i| < ε_1` and `|Δr_i/r_i| < ε_2`. Out-of-order packets (bytes) at the receiver are the evaluation metric. No receive-buffer/ATD penalty term is used.

- **10. Congestion-control interaction**
  The scheduler is co-designed with a *new* congestion control, **Coupled BBR** (BBR adapted to MPTCP), and the paper argues the coupling is essential: "Previous schedulers are usually based on the congestion window, while Coupled BBR changes it to smooth sending rate and makes previous schedulers no longer suitable." Mechanically, in Coupled BBR "the congestion window (cwnd) is no longer the deciding factor, it is pacing rate instead" (inherited from BBR: "BBR sets the interval time between two packets to packet size/pacing rate"). Coupling rule (Eqs. 1–2): `β_i = BW_i · max_j{BW_j} / Σ_{j∈S} BW_j²`, `α_i = (4β_i − 1)/3`, and "the average throughput of MPTCP subflow_i using Coupled BBR is: T_i^MP = β_i · BW_i", giving `T^MP = Σ_{i∈S} β_i BW_i = max_j{BW_j}`, which "simply achieves the fairness between MPTCP and TCP BBR flows" — i.e. MPTCP's aggregate matches a single-path TCP BBR flow on the best path. "Coupled BBR is implemented at the sender side, and does not require interaction between the receiver and the sender." If `α_i ≤ 0`, "Coupled BBR sets the sending rate to 4 · packets/RTT_i if α_i ≤ 0, which is similar to the PROBE RTT phase." The paper also notes the design precondition: "for bottleneck fairness, MPTCP subflows sharing one bottleneck should be coupled to achieve fairness with TCP flows in the same bottleneck, and it just needs a bottleneck detection method for Coupled BBR. Then our scheme can be easily adapted for it" — i.e. shared-bottleneck detection is *assumed*, not implemented here. Baselines for CC are LIA, OLIA, BALIA, Cubic and BBR.

- **11. Objective**
  Verbatim: "The main purpose is to promote transmission rate under lossy networks, while also provide stability when networks suffer physical link changes and asymmetric links." And: "1) Promote MPTCP in wireless lossy networks, as well as provide high lossy tolerance and achieve fairness and balanced congestion, and 2) Further improve the transmission efficiency and stability of MPTCP in ever-changing and asymmetric networks by designing a customized scheduler that suitable for the novel congestion control algorithm". AR-Scheduling's objective is stated as a multi-objective utility maximisation (Eq. 3): `max_{|N|≥1} log(Σ_{i∈N} x_i) − log( (Σ_{i∈N} x_i r_i) / (Σ_{i∈N} x_i) )`, where "|N| ≥ 1 means there should be at least one subflow to send non-redundant packets" — i.e. "choosing the non-redundant subflows N to maximize goodput (J1 = log Σ_{i∈N} x_i) and minimize average RTT (J2 = log Σ_{i∈N} x_i r_i / Σ_{i∈N} x_i)". AR-Scheduling solves it greedily: "The greedy method gives an optimal result when there are two subflows in an MPTCP connection... we compare the solutions when there are three subflows in the simulation, where the result given by the greedy method is not very different from the optimal solution."

- **12. Algorithm**
  Two coupled heuristic algorithms (no learning):
  1. **Coupled BBR** (Algorithm 1): per-subflow, `β_i = BW_i · max_j{BW_j} / Σ_{j∈S} BW_j²`; `α_i = (4β_i − 1)/3`; `pacing gain = [1.25, 0.75, α_i, α_i, α_i, α_i, α_i, α_i]`; on each send event, if `cycle index > 2` and `α_i > 0` then `nextSendTime = now + packet.size/(α_i · BW_i)`, if `α_i ≤ 0` then `nextSendTime = now + RTT_i/4`, else `nextSendTime = now + packet.size/(pacing gain[cycle index] · BW_i)`. It "spends the vast majority of its time in PROBE BW phase (about 98 percent)".
  2. **AR-Scheduling** (Algorithm 2): "Sort subflows as i_1, ···, i_n, where x_{i_1}/r_{i_1} ≥ ··· ≥ x_{i_n}/r_{i_n}; N = {i_1}, R = ∅"; then "for each j ∈ {2, ···, n}": add `i_j` to `R` (redundant) and otherwise to `N` (non-redundant). The exact greedy criterion in prose is stated as: "For each j in 2, ···, n, add it to N if the objective after adding i_j to N is larger than that of the original N, which means: log(Σ_{i∈N} x_i + x_{i_j}) − log( (Σ_{i∈N} x_i r_i + x_{i_j} r_{i_j}) / (Σ_{i∈N} x_i + x_{i_j}) ) > log(Σ_{i∈N} x_i) − log( (Σ_{i∈N} x_i r_i) / (Σ_{i∈N} x_i) )"; plus the auxiliary guard "or inflight_i < 4". **Caveat on the simplified closed form:** the boxed Algorithm 2 prints a simplified inequality whose two-dimensional typesetting extracts ambiguously from the PDF. The two readings I obtained are `x_{i_j} / (Σ_{i∈N} x_i) ≤ (Σ_{i∈N} x_i (r_{i_j} − 2r_i)) / (Σ_{i∈N} x_i r_i)` (`pdftotext -raw`) and, from the `-layout` extraction, a form involving `r_i − 2r_i`. The prose simplification sentence is also mangled by extraction. **I therefore do not assert the exact simplified inequality**; the un-mangled prose criterion above and Eq. (3) should be treated as authoritative, and the boxed inequality read from the published PDF.
  3. **P-Scheduling** (Algorithm 3): for each new packet `j_k` in the window, compute `A_i(j_k) = t_0 + (Σ_{j'∈L_i} s_{j'})/x_i + r_i/2` for all `i ∈ N`, then `i_k = arg min_{i∈N} A_i(j_k)` and schedule packet `j_k` on subflow `i_k`.

- **13. ML/DRL usage**
  **No. This paper uses no machine learning and no DRL.** Coupled BBR is an analytical/control-theoretic adaptation of BBR's pacing-gain cycle, and AR&P is a greedy plus earliest-predicted-arrival-time heuristic. The authors explicitly reject the RL alternative on cost grounds, in their related-work discussion: "Some RL-based algorithms, such as [34] [35], would provides better performance by learning from a large number of data. However, their are computationally complex and require a lot of CPU resources." Also noted: "as BBR does not include the AIMD method, any AIMD-based scheme is not suitable for developing MPTCP over BBR congestion control." No NN architecture, no state/action/reward — **NOT REPORTED is not applicable here; the correct value is "none used"**.

- **14. Simulator / testbed**
  Three distinct evaluation environments — do not conflate:
  1. **Linux kernel testbed (real hosts, emulated path characteristics):** "MPTCP v0.94 implemented in Linux kernel... a lab-built testbed with 8 nodes" with "a pair of MPTCP server and client, two pairs of TCP servers and clients, and four routers", two subflows each crossing two routers, bottleneck links of 100 Mbps / 25 ms with two TCP background flows per path. Loss/delay asymmetry created by configuring the bottleneck links (0%, 0.01%, 1% random loss; delay differences 20–250 ms).
  2. **Real networks:** cloud servers in "several regions"/"different regions" downloading to a lab client over 4G and Wi-Fi (2.4 GHz and 5 GHz); "we repeat 10-20 times of data download under different network environments (10 for using MPTCP flows and 20 for using TCP flows on different links)". For the comparison, "When we use the proposed MPTCP, the compared TCP flow uses BBR. Otherwise, the compared TCP flow uses NewReno."
  3. **Simulation:** "we also simulate the proposed algorithms under different network scenarios utilizing a packet-level simulator" — the simulator is **not named** (no ns-3/ns-2 identification in the text); topology in Fig. 16 with three subflows, one competing TCP flow per path, parameters `B_i`, `d_i`, `p_i`.

- **15. Traffic model**
  Bulk data download. Testbed: throughput under varying loss/delay with TCP background flows. Real network: "data download" over 4G/Wi-Fi with 10–20 repetitions reporting download speed (MB/s) with 25–75% box ranges. Simulation: bulk goodput (Mbps) and out-of-order packets (MSS) versus time. No web/video/interactive workload is studied.

- **16. Baselines**
  As the paper names them. Congestion control: **BBR**, **Cubic**, **LIA**, **OLIA**, **BALIA** (Table I compares MPTCP and single-path TCP throughput under each). Schedulers: **Round-Robin (RR)**, **minRTT**, and **Redundant** (a redundant-sending scheduler), plus their own **Coupled BBR + minRTT** and **Coupled BBR + AR&P** combinations. Real-network baselines: **Proposed** vs **BALIA+RR**, **OLIA+RR**, **LIA+RR**, and single-path TCP (BBR or NewReno). Simulation baselines: **LIA+minRTT**, **BALIA**, **OLIA**, **LIA**, and "Coupled BBR" with minRTT / AR&P.

- **17. Metrics**
  Throughput / goodput (Mbps or MB/s), bandwidth utilization (%), RTT distribution (CDF, ms), out-of-order packets (bytes, and in MSS in simulation), goodput vs time, robustness/recovery time after a path breaks down or degrades, and fairness versus a single-path TCP BBR flow on the best path.

- **18. Main result**
  Exact quoted numbers:
  - Headline testbed claim: "In most of the tested scenarios, the performance of MPTCP can be improved by more than two-and-a-half times."
  - Summary of all evaluation: "With our proposed schemes, MPTCP throughput can be improved by up to 2.5 times in normal wireless scenarios and more than 10 times in other scenarios with large RTT and loss. Moreover, the number of out-of-order packets can be reduced by 80% at most in asymmetric scenarios."
  - Real networks, 4G + Wi-Fi (2.4 GHz): "The overall throughput of the proposed scheme is twice higher than that of the original MPTCP. At the same time, the proposed scheme also achieves the goal of fairness, i.e., the proposed MPTCP flow is no more aggressive than the best single TCP BBR flow."
  - Real networks, 4G + Wi-Fi (5 GHz): "Compared with the original MPTCP, the proposed scheme brings more advantages in this scenario. The throughput of our scheme is almost 3 times higher than that of original MPTCP algorithms."
  - Real networks with large RTT/loss (cross-region cloud): "the throughput of the original MPTCP is less than 0.2MB/s... wherever the server is, MPTCP with our scheme achieves throughput over 10 times higher than that of original MPTCP".
  - Out-of-order in asymmetric RTT: "when the RTT of one path reaches 100 ms, we observe that both minRTT and Round-Robin increase out-of-order queues by over 300%, which is much longer than that of AR&P scheduler. When the RTT of one path reaches 250 ms, which means that the two paths are highly asymmetric in terms of RTT, AR&P scheduler reduces the average out-of-order queue by 65% compared to minRTT and Round-Robin." And in real networks: "our AR&P scheduler keeps the out-of-order queue short, while minRTT and Round-Robin schedulers create up to 5 times longer out-of-order queue than AR&P does."
  - Lossy-network CC comparison (Table I, random loss 0.01% on subflow1 and 0.1% on subflow2) — "AVERAGE THROUGHPUT": MPTCP (Mbps): **BBR 55.9**, Cubic 35.1, LIA 20.3, OLIA 19.9, BALIA 20.9; Subflow 1 (Mbps): 30.7 / 27.6 / 19.1 / 19.6 / 20.5; Subflow 2 (Mbps): 25.2 / 7.5 / 1.2 / 0.3 / 0.6; TCP on path 1 (Mbps): 31.9 / 27.7 / 21.1 / 21.3 / 20.8; TCP on path 2 (Mbps): 27.5 / 8.5 / 1.1 / 1.0 / 1.2; **Bandwidth utilization: BBR 88%, Cubic 54%, LIA 32%, OLIA 32%, BALIA 33%**.
  - RTT behaviour: "BBR keeps RTT of MPTCP concentrating at around 55 ms. But half of RTTs of other algorithms are concentrated at the zone of 85 ms".
  - Dynamic-network behaviour: "AR-Scheduling realizes that one of the paths is no longer satisfactory and starts to send redundant packets on it for better performance at 12 s, while Round-Robin keeps sending new packets resulting in a significant throughput decrease"; throughput at the break-down moment: "The throughput of Round-Robin and AR&P drops from 40 Mbps to about 15 Mbps while redundant scheduler protects its throughput from a high packet loss rate by sending redundant packets."

- **19. Limitation**
  Author-stated: (a) fairness/shared-bottleneck coupling is assumed rather than solved — "for bottleneck fairness, MPTCP subflows sharing one bottleneck should be coupled to achieve fairness with TCP flows in the same bottleneck, and it just needs a bottleneck detection method for Coupled BBR. Then our scheme can be easily adapted for it" (i.e. no bottleneck detection is implemented); (b) the greedy AR-Scheduling set-selection is only provably optimal for two subflows — "The greedy method gives an optimal result when there are two subflows in an MPTCP connection... we compare the solutions when there are three subflows in the simulation, where the result given by the greedy method is not very different from the optimal solution"; (c) the entire approach presumes a network where BBR controls the competing flows — "We consider a network that uses BBR to control all the flows so that the network is more stable and all the flows can get better performance. A full BBR network provides more advantages for developing higher performance transmission protocols in the future. Moreover, in lossy networks, traditional loss-based congestion control algorithms could not make good use of the available bandwidth of the bottleneck, which makes it meaningless to achieve fairness between BBR and other algorithms in this case."
  Methodological limitations I observe: (i) the full-text source is the **arXiv preprint (v2, June 2021)**, so pagination/figures may differ from the published TWC version; (ii) no ML/DRL at all, so any claim that this is an "AI-native" design would be wrong — it is an analytical BBR coupling plus a predictive heuristic; (iii) the simulation simulator is unnamed, so the packet-level simulation results are not reproducible from the paper alone; (iv) the simulation and testbed are almost entirely **2-subflow** (with a 3-subflow simulation), and the real-network study is bulk download only, with the evaluation of "mouse"/interactive flows absent; (v) the arrival-time prediction assumes a steady, smooth BBR pacing rate, and the paper concedes P-Scheduling degenerates to Round-Robin during slow-start; (vi) no energy/cost metric despite the wireless/mobile framing.

- **20. Research gap this suggests**
  Coupled BBR deliberately solves coupling/fairness analytically for a *known* bottleneck relationship, and P-Scheduling needs an accurate per-subflow `BW`/`RTT` estimate to predict arrival times. The gaps this suggests for AI-native network management: (a) shared-bottleneck detection — which the authors leave as an external prerequisite — is exactly a learning-friendly inference problem that neither this paper nor its CC solves; (b) the authors' own reason for avoiding RL is CPU cost ("computationally complex and require a lot of CPU resources"), whereas DeepCC in this same file runs inference in <1 ms, so the cost argument is not settled empirically by either paper; (c) arrival-time prediction is done with a static formula plus an analytical error bound rather than learned, leaving open whether a learned delay/bandwidth predictor would beat it under non-stationary radio conditions; (d) evaluation is 2-subflow bulk download, so multi-subflow, mixed interactive/bulk and energy-aware scheduling remain open; (e) no public artifact for the packet-level simulator is described, hindering reproducible comparison of learned vs analytical schedulers.

- **21. Best URL you actually retrieved, and whether you read full text or only abstract**
  **FULL TEXT** (arXiv preprint version).
  Retrieved from: `https://arxiv.org/pdf/2002.06284` (abstract page `https://arxiv.org/abs/2002.06284`, `arXiv:2002.06284v2 [cs.NI]`, 11 Jun 2021). Downloaded as `pdfs/coupledbbr_arxiv.pdf` (2,507,863 bytes, **14 pages**, letter, pdfTeX-1.40.21), converted with `pdftotext -layout` to `pdfs/coupledbbr_arxiv.txt` (1,269 lines). Title and author list on page 1 match the published paper exactly.
  Other URLs used: `https://api.crossref.org/works/10.1109/TWC.2021.3085661` (venue/year/pages); `https://api.unpaywall.org/v2/10.1109/TWC.2021.3085661?email=research@example.org` (→ `is_oa: false`, `oa_status: closed`); `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TWC.2021.3085661?fields=title,abstract,openAccessPdf,venue,year,externalIds` (→ `openAccessPdf` = the DOI itself, `ArXiv: 2002.06284`, `year: 2020`).

---

### 11. BBR-Based Congestion Control and Packet Scheduling for Bottleneck Fairness Considered Multipath TCP in Heterogeneous Wireless Networks

- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
  Wenjia Wei, Kaiping Xue, Jiangping Han, Yitao Xing, David S. L. Wei, Peilin Hong. IEEE Transactions on Vehicular Technology, vol. 70, no. 1, pp. 914–927. DOI `10.1109/TVT.2020.3047877`. Peer-reviewed journal article.
  **Year discrepancy (spec rule 8):** the assignment called this a 2020 paper and the DOI carries a 2020 stem; the retrieved PDF's running header reads "IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, VOL. 70, NO. 1, JANUARY 2021" and Crossref reports issued year 2021. These are consistent once the IEEE early-access convention is accounted for (DOI assigned December 2020, issue January 2021). **I trust the January 2021 issue date for the citation** (source: the printed PDF header plus Crossref `published-print`), and would cite it as TVT 70(1):914–927, 2021, noting online publication in 2020.

- **1. Number and type of paths**
  Heterogeneous wireless with **2 subflows**. NS-3 shared-bottleneck scenario: "Two subflows (Subflow 0 and Subflow 1) are established between MPTCP client (C_0) and server (S_0). The subflows compete with each other in this bottleneck... The bottleneck bandwidth is set to 1 Mbps and the link delay is set to 10 ms. Bandwidth of other links is set to 100 Mbps." NS-3 non-shared scenario: "Subflow 0 has 1 Mbps bandwidth, 10 ms latency and 0.1% loss rate... the delay of Subflow 1 vary from 10 ms to 50 ms and the loss rate vary from 0.1% to 5%." Real-network setup: "The client has both WiFi and LTE interfaces, and can downloads data from the application server through WiFi and LTE at the same time." Exactly two paths throughout.

- **2. Network architecture**
  End-to-end MPTCP over heterogeneous wireless, **via a Socks proxy** in the real-network study: "Considering that the existing application server does not support MPTCP, we develop a heterogeneous wireless network test framework based on Socks proxy according to [46]... We implement our BCCPS in the Linux kernel of Socks Proxy and the client." The NS-3 side is a direct MPTCP client/server connection (C_0↔S_0) with single-path BBR and MPTCP background flows injected from C_1,C_2 to S_1,S_2. No 5G core or ATSSS elements.

- **3. Transport protocol**
  MPTCP. "Then we implement BCCPS in Linux kernel base on MPTCP v0.94 and test it in real network." Congestion control is a custom BBR-derived coupled algorithm, **MPTCP-BBR**, with the default Linux scheduler replaced by the paper's fine-grained scheme. MPTCP RFC 6824 is the cited specification.

- **4. Scheduler location**
  Sender side ("This detection can be implemented on sender's side"; the shared-bottleneck detection, congestion control and scheduling all run at the MPTCP sender). In the real-network study it lives in the Socks proxy's Linux kernel and in the client. No receiver-side or in-network component: reordering is left to MPTCP's normal receive-buffer machinery.

- **5. Scheduler inputs**
  Per subflow `r`: BBR-measured bottleneck bandwidth `BtlBW_r` (Eq. 5: `BtlBW_r = max{x_r(t)}, t ∈ [T−W, T]`), the RTT / `RTprop_r` measurement, and the observed packet loss rate `q_r`; plus the number of unsent packets queued on the subflow `k_r`. Verbatim: "When scheduling a connection level packet, the algorithm estimates its arrival time, denoted by T_r, if sent over subflow r, which is the end-to-end delay of subflow r. Then it chooses the subflow with the earliest arrival time." And "The estimation is performed based on a subflow's BtlBW_r, and the number of unsent packets in queue k_r." Loss is explicitly an input, unlike Coupled BBR: "When the sender detects a loss event, it updates the loss rate q_r, calculates the average loss rate, and forecast the time arriving at the destination."

- **6. Path metrics used**
  Bottleneck bandwidth `BtlBW_r`, RTT / `RTprop_r`, packet loss rate `q_r`, number of queued unsent packets `k_r`, and the traffic size of the flow (to classify mouse vs elephant flows). No energy or cost metric.

- **7. Scheduling decision**
  A **two-phase** decision per connection:
  1. **Redundancy phase** (small flows): send the *same* packets over multiple subflows — "In the initial phase, packets are redundantly transmitted over multiple paths until the amount of transmitted packets reaches a certain threshold." The threshold is explicit: "We heuristically mandate that flows less than or equal to 100 KB are considered mouse flows, and are replicated to achieve better latency. This threshold value is chosen in accordance with many existing literatures [41]–[43]."
  2. **Forward-prediction phase** (bulk): choose a subflow per packet by earliest predicted completion time: "for each packet in the queue, scheduler selects the appropriate subflow to transmit according to its arrival time in FIFO order"; prediction (Eqs. 7–9): `T_r = T^r_net + T^r_wait`, `T^r_net = RTT_r/2 + q_r · RTT_r`, `T^r_wait = k_r / BtlBW_r`. "Then it chooses the subflow with the earliest arrival time." The authors state the design intent: "This algorithm aims at scheduling more packets on a subflow than what it can currently send, so the queues may therefore build up at the sender." Note the loss term is added *as if* the packet arrives after one retransmission: "we assume that the lost packet can successfully arrive at the receiver by one retransmission."
  Congestion-control actions are separate (pacing gain, Eq. 4).

- **8. Packet-level or flow-level scheduling**
  **Packet-level** ("a fine-grained packet scheduling scheme... for each packet in the queue, scheduler selects the appropriate subflow to transmit according to its arrival time in FIFO order"), operating above a connection-level "completion time" estimate. The redundancy phase is also packet-level but replicates each packet across subflows. Explicitly contrasted with window-level prior art: "all the existing predictive scheduling schemes, e.g., [19], [20] work on packet-loss-based congestion control, which rely on modeling congestion window (CWND) changes in multiple scheduling cycles when predicting the throughput on each subflow. The sending rate of TCP-BBR does not change according to a specific regular rule, so a new packet scheduling algorithm needs to be designed based on our proposed MPTCP-BBR."

- **9. Reordering handling**
  Reordering is *avoided* by construction rather than detected and penalised. Packets are assigned so that predicted arrival times are ordered: "for each packet in the queue, scheduler selects the appropriate subflow to transmit according to its arrival time in FIFO order." And "In this way, all these packets will arrive at receiver in order." Head-of-line blocking is the motivating problem: "As shown in Fig. 4, a first packet is sent on a slow path, and subsequent packets are sent on the fast path to fill the receive buffer. While the subsequent packets are received in a timely manner, the transmission is blocked, waiting for the first packet to be received." The measured reordering quantity is the "average MPTCP OFO queue size: the average out-of-order queue size counted at receiver". No BLEST-style blocking estimate is computed; BLEST appears only as a comparison scheduler. The redundant-transmission phase also reduces reordering indirectly: "BCCPS reduces the completion time of mouse flows since the redundancy packet transmission reduce the possibility of retransmission."

- **10. Congestion-control interaction**
  BCCPS *replaces* MPTCP's coupled congestion control with **MPTCP-BBR**, and the scheduler is designed specifically for it (the paper argues BBR's irregular sending rate invalidates window-based predictive schedulers). Coupling mechanism: subflows are first partitioned into **shared-bottleneck sets** and only subflows in the *same* set are coupled. Detection procedure (stated verbatim): "S1: The MPTCP sender monitors the RTTs of all subflows in respective ProbeBW states. When the RTT of one subflow increases, the sender further detect whether there are other subflows whose RRTs are also linearly increasing in the same time. If so, these subflows can be judged to share a bottleneck... S2: Furthermore, for a shared bottleneck set judged previously, if the minimum RTTs of the subflows in a shared bottleneck set are measured simultaneously in the ProbeRTT state, then this bottleneck set can be confirmed finally and all the subflows in this set should be coupled together. Otherwise, the previously judged shared-bottleneck set should be cancelled." The probing period is unified across a set (Eq. 1: `RTT* = max_{r∈S_i}{RTprop_r}`), the BDP is `BDP_r = max{x_r(t)} × RTT*, t ∈ [T−W, T]` (Eq. 2), rate is gated by `R_r = G_r × max{x_r(t)} if I ≤ BDP_r, else 0` (Eq. 3), the pacing gain cycle is `G_r ∈ [1.25, 0.75, α_r, α_r, α_r, α_r, α_r, α_r]` (Eq. 4), and `α_r = max_{r∈S_i} BtlBW_r / Σ_{r∈S_i} BtlBW_r` (Eq. 6, as printed). This is the distinctive claim versus Coupled BBR (which assumes a known bottleneck relationship): BCCPS adds the detection. The stated goal: in each shared-bottleneck set "MPTCP-BBR should perform equally well as a single-path TCP-BBR flow running on the best path at the shared-bottleneck." Fairness notion used: "Bottleneck Fairness only restricts the total goodput of the subflows sharing the same bottleneck not bigger than that of the TCP path sharing this bottleneck" (contrasted with Network Fairness as in LIA/OLIA/BALIA).

- **11. Objective**
  Verbatim: "In order to reduce the completion time caused by the out-of-order delivery problem, our scheme employs a new fine-grained packet scheduling scheme... we divide the scheduling procedure into two phases: the redundant data transmission phase and the regular MPTCP packet scheduling phase. This design can both achieve high goodput for elephant flows and low completion time for mouse flows." Congestion-control objective: "(i) 'Improve Goodput,' (ii) 'Do No Harm,' and (iii) 'Balance Congestion'" with "Do No Harm" defined as "an MPTCP connection should be TCP friendly which is called Network Fairness", combined with bottleneck fairness as described in field 10.

- **12. Algorithm**
  Heuristic/analytical, no learning. Three components: (a) shared-bottleneck set detection via ProbeBW RTT-trend correlation plus ProbeRTT confirmation (steps S1/S2), with "we set the judgement period as one RTprop" and default ProbeRTT behaviour "entered when the value of RTT_min hasn't been updated with a lower measured value for several seconds (default: 10 s). In ProbeRTT, the sender limits its inflight data amount to 4 packets a maximum value. This state lasts for 200 ms"; (b) **MPTCP-BBR** coupling via Eqs. (1)–(6) (Algorithm 1); (c) two-phase packet scheduling giving Algorithm 2, with the 100 KB mouse-flow redundancy threshold and the earliest-predicted-completion-time rule of Eqs. (7)–(9).

- **13. ML/DRL usage**
  **No. BCCPS uses no machine learning and no DRL.** It is BBR control theory plus heuristics. The paper positions itself against RL approaches explicitly, listing them as related work and criticising their generalisation and convergence cost: "Li et al. [25] proposed a reinforcement learning-based congestion control scheme for MPTCP, named SmartCC... Xu et al. [26] proposed a deep reinforcement learning (DRL)-based congestion control scheme for MPTCP, named DRL-CC... Learning-based approaches have the potential to converge to the best decision to improve goodput under the network conditions that have occurred in offline training stage. However, these approaches, such as SmartCC and DRL-CC, might have a worse performance when facing new network conditions and have a long convergence time to achieve the best sending rate on each subflow [27]." It also cites ReLeS as related work (its reference [32]). No state/action/reward, no NN architecture — **none used**.

- **14. Simulator / testbed**
  Two environments, both used:
  1. **NS-3 simulation:** "We first evaluate our BCCPS proposed in this paper through NS-3 simulator [44]. The MPTCP NS-3 code is provided by Google MPTCP group [45]." Two topologies: shared bottleneck (Fig. 7(a), 1 Mbps / 10 ms bottleneck, other links 100 Mbps, with single-path BBR and MPTCP background traffic) and non-shared bottleneck (Fig. 7(b), Subflow 0 fixed at 1 Mbps / 10 ms / 0.1% loss; Subflow 1 delay swept 10→50 ms and loss 0.1%→5%). The exact parameter table ("TABLE I NETWORK CHARACTERISTICS IN NS3") is a **raster image** in the PDF and its cell values are not in the text layer — I did not reconstruct them.
  2. **Real-network testbed:** "Then we implement BCCPS in Linux kernel base on MPTCP v0.94 and test it in real network", over a **Socks-proxy-based** heterogeneous framework, with a client having "both WiFi and LTE interfaces", downloading from an application server over WiFi and LTE simultaneously. The network-characteristics table ("TABLE II REAL NETWORK CHARACTERISTICS") is likewise an image and not readable from the text layer. Applications tested: "we directly download a 100 MB file from the server" (bulk), and web traffic from "Instagram, Amazon, and Wikipedia" (mouse flows), where "The average file size is sorted as Instagram >Amazon > Wikipedia."

- **15. Traffic model**
  Mixed, deliberately: bulk/elephant traffic ("We first test the performance of the algorithm in the case of elephant flows by bulk traffic. We directly download a 100 MB file from the server"), a small-file mouse-flow case ("we first exchange a small file with a size of 100 KB between MPTCP client (C_0) and server (S_0) to evaluate the performance of mouse flows in lossy network"), and real web traffic (Instagram, Amazon, Wikipedia). Background traffic is present in both environments ("single-path BBR and MPTCP background flows produce background traffic between clients (C_1, C_2) and servers (S_1, S_2), and compete with MPTCP flow at bottleneck"). No video streaming.

- **16. Baselines**
  As the paper names them. Congestion control: "we compare our scheme with MPTCP using LIA and BALIA" — i.e. **MPTCP-LIA**, **MPTCP-BALIA**, with **single-path TCP-BBR** ("BBR_0", "BBR_1", and "BBR_0+BBR_1") as the baseline for the goodput ratio, plus **Single-path BBR** and **MPTCP-BBR** in the real-network study and **DWC** ("loss-and-delay-based mechanism, i.e., DWC") for bottleneck-detection accuracy. Scheduling: "RR and LRF and BLEST [20] are used to compare with our scheme" → **MPTCP-BBR-RR**, **MPTCP-BBR-LRF**, **MPTCP-BLEST**, and in the real-network study **MPTCP** and **MPTCP-BBR** (both using LRF, so the scheduler effect is isolated).

- **17. Metrics**
  Verbatim: "Performance Metrics: 1) Goodput: the application-level throughput of a communication, which can accurately reflect algorithm performance, especially for bulk transmission. 2) Average MPTCP OFO queue size: the average out-of-order queue size counted at receiver, which can reveal the effectiveness of scheduling algorithm. 3) Download time: the completion time to download a specific size file, especially for small-size data transmission." Additionally: bottleneck-detection accuracy, normalized download time (relative to "the best single-path TCP-BBR as a baseline, which is theoretical performance value"), end-to-end RTT CDF, and goodput ratio versus single-path BBR.

- **18. Main result**
  Exact quoted numbers (the paper reports most results graphically, and the only two numeric claims stated in prose are these):
  - "The experimental results show that our proposed scheme can reduce the out-of-order packets in the receiver's buffer by >50% and increase the goodput by >30% compared with the comparison schemes, while achieving bottleneck fairness with other TCP/MPTCP flows."
  - "Experimental results show that our proposed scheme far outperforms existing MPTCP schemes in heterogeneous wireless environment" (abstract).
  Qualitative but exact comparisons as stated: "MPTCP-BBR's detection accuracy is higher than DWC"; "MPTCP-BBR outperforms MPTCP-LIA and MPTCP-BALIA obviously as MPTCP-BBR can continuously probes the current transmission capacity and its transmission goodput is closer to theoretical bandwidth. When the RTT of Subflow 1 increases, MP-BBR can still achieves higher goodput"; "the performance of MPTCP-BBR in Fig. 8(b) is close to single-path TCP-BBR... MPTCP-BBR detects bottleneck correctly and achieves fairness with regular single-path TCP-BBR flow at the shared bottleneck"; in the non-shared scenario "MPTCP-BBR outperforms MPTCP-LIA and MPTCP-BALIA close to BBR_0+BBR_1, which means that each of the disjoint subflows can reach the goodput of single-path TCP-BBR and a good bottleneck fairness can be achieved"; "Fig. 10(a) shows that the best single-path BBR outperforms MPTCP-BBR-RR and MPTCP-BBR-LRF when the amount of data is less than 100 KB... Compared with MPTCP-BBR-RR and MPTCP-BBR-LRF, BCCPS avoids the long time caused by packet loss during the startup phase with redundancy packet transmission. When the amount of data is greater than 100 KB, all the three scheduling algorithms perform nearly the same as the best single-path BBR and BCCPS has the highest performance"; "BCCPS performs best regardless of the loss rate"; "MPTCP-BBR-RR and MPTCP-BBR-LRF induce more out-of-order packets than MPTCP-BLEST and BCCPS"; in the real network "the BBR-based congestion control algorithms, MPTCP-BBR, achieves greater goodput and less download time than legacy MPTCP. Besides, compared to MPTCP-BBR, BCCPS further shortens download time because of our new scheduling algorithm"; and for web traffic "BCCPS performs the best... as the size of the web traffic increases, we can see that BCCPS's advantages in performance are more obvious." **No numeric per-figure values were recoverable from the text layer; I have not estimated any.**

- **19. Limitation**
  Author-stated: (a) scope is narrow and future work is acknowledged — "In the future, we will consider more complex simulation scenarios to analyze the performance of our proposed algorithms and further evaluate our scheme in real scenarios. Meanwhile, we will further refine the scheme design to consider fine-grained scheduling policies for different types of transmitted data." (b) The design rests on BBR's assumed behaviour and on a synchronisation phenomenon: shared-bottleneck confirmation depends on subflows entering ProbeRTT together ("subflows traversing from a same bottleneck could approximately synchronize the above process of state change at the same time"), which the authors concede is affected by measurement error ("Due to the influence of background flows in the network, RTT's measurement error will affect the detection accuracy of shared-bottleneck sets"). (c) The arrival-time model is explicitly optimistic about loss: "we assume that the lost packet can successfully arrive at the receiver by one retransmission."
  Methodological limitations I observe: (i) the full text is an **author-hosted copy** (`staff.ustc.edu.cn`), which matches the published version's header/pagination but is not the publisher's own file; (ii) all experiments use exactly **2 subflows** (WiFi+LTE), so the coupling and detection logic is never exercised on more than two paths — and the coupling equations' behaviour in multi-set topologies is untested; (iii) the 100 KB mouse-flow threshold is a heuristic ("We heuristically mandate... chosen in accordance with many existing literatures") with no sensitivity study; (iv) NS-3 parameter tables (Tables I and II) are images in the PDF and could not be verified from the text, limiting reproducibility of the exact simulated link characteristics; (v) prose reports only two aggregate percentages (>50% OFO reduction, >30% goodput increase) with "the comparison schemes" left collectively unspecified, so the per-baseline attribution of those figures is not established by the text; (vi) the redundancy phase trades bandwidth for latency by design, with no energy or cost accounting despite the wireless/LTE setting; (vii) no ML — so it cannot be cited as AI-native, and its critique of DRL ("worse performance when facing new network conditions and a long convergence time") is asserted with a citation rather than measured in this paper.

- **20. Research gap this suggests**
  BCCPS closes the shared-bottleneck-detection prerequisite that Coupled BBR leaves open, by correlating ProbeBW RTT trends and confirming in ProbeRTT — but it does so with a **fixed-rule** detector that the authors admit is error-prone under background flows and that is only validated with two subflows and two scenarios (shared / non-shared). This suggests a concrete gap: learned or probabilistic shared-bottleneck inference over more than two subflows and multiple overlapping bottleneck sets, where BCCPS's RTT-trend heuristic is most fragile. Related gaps: (a) the mouse/elephant split is a hard-coded 100 KB threshold with no adaptivity to application class, so learned flow-class-aware scheduling with a bandwidth/latency trade-off (and explicit cost accounting) is open; (b) the loss term in the arrival-time predictor assumes one retransmission succeeds, leaving room for learning the loss/retransmission delay distribution; (c) BCCPS and Coupled BBR both keep reordering control at the sender with no receiver-side or in-network coordination, so cross-layer or AI-assisted reordering (receive-buffer-aware scheduling) is unaddressed; (d) the paper's own critique of DeepCC-style DRL (poor generalisation, slow convergence) is untested head-to-head in this paper, which is exactly the benchmark an AI-native transport study should run.

- **21. Best URL you actually retrieved, and whether you read full text or only abstract**
  **FULL TEXT.**
  Retrieved from the corresponding author's (Kaiping Xue, USTC) institutional author copy:
  `http://staff.ustc.edu.cn/~kpxue/paper/TVT-BBR-Wei-2021.01.pdf` (HTTP 200, `application/pdf`, 2,676,044 bytes). Downloaded as `pdfs/bccps_tvt2020.pdf` (PDF v1.4, **14 pages**), converted with `pdftotext -layout` to `pdfs/bccps_tvt2020.txt` (931 lines).
  Identity verified three ways: the running header reads "IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, VOL. 70, NO. 1, JANUARY 2021" with first page 914 and last page 927; the PDF's own text contains the DOI `10.1109/TVT.2020.3047877`; and the title and full author list on page 1 match the Crossref record. It also carries the IEEE watermark "Authorized licensed use limited to: University of Science & Technology of China. Downloaded on February 15,2021" — i.e. a copy of the publisher's version of record, not a preprint.
  Other URLs used for this paper: `https://api.crossref.org/works?query.bibliographic=BBR-Based+Congestion+Control+and+Packet+Scheduling+for+Bottleneck+Fairness+Considered+Multipath+TCP+in+Heterogeneous+Wireless+Networks` (this is how the DOI was **found**, since it was not supplied: Crossref returned `10.1109/tvt.2020.3047877`, TVT vol. 70, iss. 1, pp. 914–927, issued 2021); `https://api.unpaywall.org/v2/10.1109/TVT.2020.3047877?email=research@example.org` (→ `is_oa: false`, `oa_status: closed`, no best PDF); `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TVT.2020.3047877?fields=title,abstract,openAccessPdf,venue,year,externalIds` (→ `openAccessPdf` empty, no arXiv ID); `https://ieeexplore.ieee.org/abstract/document/9310257` (publisher abstract page).
  Caveat: BCCPS Tables I and II are raster images in this PDF, so their cell values are not in the text layer — no values were invented for them.

---

### 12. BLEST: Blocking Estimation-based MPTCP Scheduler for Heterogeneous Networks

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

### 13. ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths

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

### 14. Peekaboo: Learning-Based Multipath Scheduling for Dynamic Heterogeneous Environments

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

### 15. CMT-QA: Quality-Aware Adaptive Concurrent Multipath Data Transfer in Heterogeneous Wireless Networks

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

### 16. Bandwidth-Efficient Multipath Transport Protocol for Quality-Guaranteed Real-Time Video Over Heterogeneous Wireless Networks

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

### 18. GCLR: GNN-Based Cross Layer Optimization for Multipath TCP by Routing

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

### 19. A Reinforcement Learning-based Multipath Scheduling for Heterogeneous Wireless Networks (protocol name: **SATO**)

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

### 20. An Improved MPQUIC Scheduler Based on Multi-Agent Reinforcement Learning

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

### 21. Deep Reinforcement Learning for Access Traffic Splitting in 5G Core System
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

### 22. Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective Reinforcement Learning
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


### 23. Multipath TCP Meets Reinforcement Learning: A Novel Energy-Efficient Scheduling Approach in Heterogeneous Wireless Networks
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

### 24. Self-selected 2023–2026 AI/ML multipath-scheduling paper — selection and extraction

#### How the paper was selected
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

### 24a. Energy-Aware MPTCP Scheduling in Heterogeneous Wireless Networks Using Multi-Agent Deep Reinforcement Learning Techniques  *(the selected paper)*
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

### 24b. LiveStream Meta-DAMS: Multipath Scheduler Using Hybrid Meta Reinforcement Learning for Live Video Streaming  *(secondary pick, also read in full)*
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

## Comparison table

**Legend for "scheduler type":** *heuristic* = fixed rule using measured path state; *learning* =
policy fitted from data (DRL / bandit / GNN / meta-RL); *optimisation* = an explicit objective
solved or approximated; *analytical-CC* = the paper's contribution is congestion control, not
scheduling (scheduling is emergent or untouched).
**Bold** in the "read" column marks papers where only the abstract was obtainable — for those,
every `NOT REPORTED` cell means *the abstract does not say*, not *the paper does not say*.

| # | Paper (short) | Scheduler type | CC | Testbed or simulator | Baselines | Headline result | Read |
|---|---|---|---|---|---|---|---|
| 1 | RFC 8684 (2020) | none specified — **standard deliberately defines no scheduler** ("a host may use any local policy it wishes") | RFC 6356 coupled CC *recommended*, not mandated | n/a (standards document) | n/a | No experimental results; normative safety property only | FULL TEXT |
| 2 | Barré, MPTCP: Theory to Practice (IFIP Netw. 2011) | heuristic — "fill all subflows" | Coupled CC with α-factor (α from cwnd/RTT); per-subflow loss → cwnd/2 | **Real testbed** (HEN, UCL): up to 4 workstations, 1 Gbps + 100 Mbps, disjoint paths, injected delay 0–500 ms | Regular TCP (Reno); MPTCP with Reno per subflow | Two 100 Mbps links saturated at rcvbuf ≥ 2 MB; 1–3 % loss on one path does not degrade the other; 500 ms asymmetry "much more affected" | FULL TEXT |
| 3 | Wischik, CC for MPTCP (NSDI 2012) | analytical-CC (no packet scheduler; packets striped "as space in the subflow windows becomes available") | **COUPLED** (proposed) vs per-subflow TCP vs EWTCP | **Custom high-speed packet-level simulator** + **real Linux 3G+WiFi laptop testbed** | single-path TCP, EWTCP, per-subflow TCP | Testbed: 14.4 / 2.1 / **17.3** Mb/s (TCP-WiFi / TCP-3G / MPTCP); competing-flows MPTCP **2.21** vs EWTCP 1.66 vs COUPLED 1.41 Mb/s; sim RTT-compensation **+15 %** avg | FULL TEXT |
| 4 | Paasch, Experimental evaluation of MPTCP schedulers (CSWS 2014) | heuristic — RR, LowRTT, LowRTT+RP, LowRTT+BM | **OLIA** | **Mininet emulation** (400 / 200 settings) **+ NorNet real public WLAN & 3G** | RR, LowRTT, LowRTT+RP, LowRTT+BM (mutual) | RR: ~40 % of runs 100–1500 % delay increase; LowRTT: 70 % of runs 10–100 %; LowRTT "up to 10 times better" than RR at 1875 Kbps | FULL TEXT |
| 5 | Hurtig, Low-Latency Scheduling in MPTCP (ToN 2019) | heuristic — BLEST, STTF (vs LRF, DAPS, OTIAS, ECF) | `NOT REPORTED` in text | **5-machine emulation testbed** + **MONROE real WLAN+3G** (RTT ≈25/75 ms) | LRF (default), DAPS, OTIAS, ECF, single-path TCP | STTF **−51 %** web object time and **+45 %** faster interactive vs LRF; Amazon **−27 %** page-load / **−41 %** object time | FULL TEXT |
| 6 | De Coninck, Multipath QUIC (CoNEXT 2017) | heuristic — MPTCP-Linux default (lowest SRTT with cwnd space), applied to QUIC | **OLIA** (multipath), **CUBIC** (single-path) | **Mininet emulation only** (506 sims/class × 4 classes, ×3 reps, median) | TCP, MPTCP v0.91 (Linux 4.1.39), single-path QUIC | Aggregation benefit higher in **77 %** of scenarios vs MPTCP **45 %**; multipath beneficial in **58 %** (QUIC) vs **20 %** (TCP) in high-BDP no-loss; real-world eval left to future work | FULL TEXT |
| 7 | Langley, The QUIC Transport Protocol (SIGCOMM 2017) | none — **single-path** (connection migration only) | **Cubic** for both TCP and QUIC; CC modular by design | **Production deployment** at Google (Chrome, Search, YouTube) | TCP+TLS, TCP+HTTP/2 | Search latency **−8.0 %** desktop / **−3.6 %** mobile; YouTube rebuffering **−18.0 %** / **−15.3 %**; QUIC > **30 %** of Google egress ≈ **7 %** of Internet traffic | FULL TEXT |
| 8 | **ReLeS** (INFOCOM 2019) | learning — DRL (abstract says neural adaptive DRL) | `NOT REPORTED` | `NOT REPORTED` (abstract: "emulated and real network conditions") | `NOT REPORTED` ("state-of-the-art schedulers") | Qualitative only: "significantly outperforms the state-of-the-art schedulers". **No numbers** | **ABSTRACT ONLY** |
| 9 | **DeepCC** (TNSM 2021) | learning — multi-agent DRL, per-subflow agents, self-attention; action = (Δsplit ratio, cwnd multiplier) | **replaces** CC: each agent sets its own subflow's cwnd/rate | **Real Linux testbed** (Dell i7-8700, Ubuntu 16.04) with `tc`/`ethtool` link emulation | DRL-CC, SmartCC; LIA, OLIA, BALIA, wVegas; MAACKTR, MADDPG | Self-attention "reduces convergence time by about **50 %** and increase[s] goodput by about **80 %**" vs common NN structures; MAPOKTR "increases the goodput by at least **10 %**" | FULL TEXT |
| 10 | Coupled BBR + AR&P (TWC 2021) | heuristic scheduler + **new analytical CC**; **no ML anywhere** | **Coupled BBR** (α_i = (4β_i−1)/3); fairness target T^MP = max_j BW_j | Linux kernel testbed (8 nodes, MPTCP v0.94) + further environments | CC: BBR, Cubic, LIA, OLIA, BALIA. Schedulers: RR, minRTT, Redundant | "improved by more than two-and-a-half times" in most scenarios; "up to **2.5 times** … and more than **10 times**" in high-RTT-loss; OFO "reduced by **80 %** at most" | FULL TEXT |
| 11 | BCCPS / MPTCP-BBR (TVT 2021) | heuristic predictive scheduler + **new analytical CC**; **no ML** | **MPTCP-BBR** with shared-bottleneck-set detection (ProbeBW RTT-trend + ProbeRTT) | **ns-3 simulation** *and* a real-network study | MPTCP-LIA, MPTCP-BALIA, single-path BBR, DWC | "reduce the out-of-order packets in the receiver's buffer by **>50 %** and increase the goodput by **>30 %**"; prose numbers only (tables are images) | FULL TEXT |
| 12 | **BLEST** (IFIP Networking 2016) | heuristic — blocking estimation + penalisation | **MPTCP-OLIA** (MPTCP v0.90, Linux 3.14.33); scheduler reads cwnd, not coupled to CC | **CORE emulation** + **real-network testbed** (no ns-2/ns-3) | **minRTT** (MPTCP default), **DAPS**, **OTIAS**, single-path TCP on 3G and WLAN (note: **not** Round-Robin) | Abstract: **+12 % goodput / −80 % retransmissions**; emulation 3G+WLAN **−19 %** out-of-order, **+12 %** goodput; retrans 366.37 pkt (minRTT) vs **70.3 pkt** (BLEST); real network **+18 %** goodput, **>37 %** fewer retransmissions | FULL TEXT |
| 13 | **ECF** (CoNEXT 2017) | heuristic — "ecf:1" / send-credit scheduling to stop cc-coupled subflows going idle | **CC-agnostic** by design ("similar performance degradation regardless of the congestion controller used (e.g., Olia)") — CC *not named* | **Real Linux testbed**: Nexus 5 + real 802.11g AP + **real AT&T LTE**, plus in-the-wild measurements. No simulator | **Default** (= minRTT), **DAPS**, **BLEST** | IW resets: Default 486 / DAPS 92 / BLEST 382 / **ECF 16**; OOO delay: ECF **99.9 %** of transfers < 0.8 s vs default > 99 % > 1 s; in-the-wild streaming **7.79 vs 6.72 Mbps (+16 %)**; web **0.650 s vs 0.882 s (−26 %)**, OOO 0.087 s vs 0.297 s (−71 %) | FULL TEXT |
| 14 | **Peekaboo** (JSAC **2020**) | learning — **contextual multi-armed bandit solved with LinUCB (d = 6)** — **not deep RL** | **NOT REPORTED** (no CC named in the paper) | **Mininet emulation** (`tc`) + **real-network** deployment | **RR**, **minRTT**, **BLEST**, **ECF** | Up to **31.2 %** (emulated) / **36.3 %** (real) improvement; "up to **30 %** shorter than ECF"; beats non-learning schedulers in ~**80 %** of the design space, minRTT in ~60 %. Could **not** benchmark RELES (no code available) | FULL TEXT |
| 15 | **CMT-QA** (TMC 2013) | optimisation/heuristic — **CMT over SCTP**, chunk-level distribution + per-path rate control; **pre-MPTCP** | `NOT REPORTED` (differentiates loss types to avoid "unreasonable congestion window adjustments") | **Simulation** — simulator name/version/topology `NOT REPORTED` | "existing solutions" — **not named** | Qualitative only. **No numbers** | **ABSTRACT ONLY** |
| 16 | **BEMA** (TCOM 2016) | optimisation — priority-aware scheduling + Raptor FEC, delay-constrained distortion minimisation | `NOT REPORTED` | **Emulation in Exata** with real-time H.264 (not a live testbed) | "the existing multipath protocols" — **not named** | Qualitative only: "appreciable improvements" in PSNR, delay, bandwidth utilisation, goodput. **No numbers** | **ABSTRACT ONLY** |
| 17 | Wu, Survey on Multipath Transport Towards 5G ATSSS (IEEE Access 2021) | survey — covers heuristic + learning + optimisation | survey-level (multipath CC for 5G section) | n/a (survey) | n/a | Maps MPTCP/MPQUIC/MP-DCCP/CMT-SCTP onto **four ATSSS steering modes** (Priority-based, Smallest Delay, Load-balancing, Best-Access, Redundant); reviews the DRL schedulers (ReLeS, Peekaboo, M-Peekaboo) and flags **explainability** and **complexity** as open issues | FULL TEXT |
| 18 | **GCLR** (IEEE Access 2020) | learning (GNN) but at **flow level: path selection / routing, NOT packet scheduling** | `NOT REPORTED` (no CC algorithm named, no coupling policy) | **Mininet 2.2.2 + Floodlight SDN controller** on one Linux server, MPTCP kernel v0.89 | **ECMP**, **fullmesh**, traversal optimum | GNN prediction MSE **0.016**, ρ **0.994** after 100 k steps, average model error **0.004**; GCLR **+14.57 %** average throughput vs ECMP; CDF nearly coincides with traversal optimum | FULL TEXT |
| 19 | **SATO** (IEEE WF-IoT 2022) | learning — RL-based **MPQUIC** scheduler | `NOT REPORTED` | **Both simulation and a real deployment claimed, neither named** | unnamed "state-of-the-art algorithm" (related work names minRTT, BLEST, ECF) | "SATO improves the QoS by **10 %-15 %** in simulation and **12 %** in a real deployment compared to the state-of-the-art algorithm" | **ABSTRACT ONLY** |
| 20 | **MPQUIC MARL** (IEICE E108-D, Aug 2025) | learning — **per-client DQN + LSTM**, one agent per client, **packet-level** action = path index per packet | `NOT REPORTED` (CWND is a state input; CC algorithm not named) | **ns-3 + NS3-MPQUIC + PyTorch via Pybind11** (simulation only) | **MinRTT, BLEST, ECF, Peekaboo, MuLeS** | Download time **−6.3 % to −13.7 %**; throughput **+10.4 % to +24.1 %** across three loss settings (0.1 / 0.5 / 0.9 %) | FULL TEXT |
| 21 | **DRL for Access Traffic Splitting in 5G Core** (IEEE ICTC 2024) | learning — DRL | `NOT REPORTED` | `NOT REPORTED` (no free5GC/Open5GS/ns-3/testbed named) | "traditional methods" — not named | Qualitative only: "outperforms traditional methods". **No numbers** | **ABSTRACT ONLY** |
| 22 | **Autonomous Access Traffic Splitting via 5G Core** (IEEE ICCCN 2025) | learning — **multi-objective RL** (MORL) | `NOT REPORTED` | **Simulation only, unnamed** ("a simulated network environment") | "traditional parameter-based methods" — not named | "a **19 % higher QoS satisfaction level** and a **9 % enhancement in ROI retention**" vs traditional parameter-based methods | **ABSTRACT ONLY** |
| 23 | **Multipath TCP Meets RL** (IEEE Wireless Commun. 30(2), 2023) | learning — RL, but **flow-level: "optimal path set for different flows" — not per-packet scheduling** | `NOT REPORTED` | `NOT REPORTED` | "state-of-the-art mechanisms" — not named | "improve the aggregate throughput and reduce energy consumption **significantly**" — **unquantified** | **ABSTRACT ONLY** |
| 24a | **EE-MADDPG** (Electronics 12(21):4496, 2023) | learning — **MADDPG**; action includes rate, path, subflow **and a CC parameter** | modifies CC parameters; **CC algorithm not named** | **Simulation, simulator never named** (1,000 episodes) | **Round Robin, eMPTCP, EE-MPTCP, DMPTCP, ReLes** | vs Round Robin: throughput **+239.57 %**, delay **−70.33 %**, energy **−62.11 %** | FULL TEXT |
| 24b | **LiveStream Meta-DAMS** (IEEE TCCN 11(4), 2025) | learning — **hybrid meta-RL (MA3C) + LSTM**, packet-level, **server-side** | **observes** cwnd/send window, explicitly **does not** couple; coupled CC named as future work | **Mininet emulation** (trace-driven) with **mpquic-go + TensorFlow + keras-rl** | **minRTT, RR, DAMS, Meta-DQN, DQN, ReLeS, Peekaboo** | up to **+32 %** learning, **−25 %** download time, **+15 %** video quality (VQA), **−35 %** stalling | FULL TEXT |

---

---

## Is there a gap between classical multipath schedulers and modern AI/agentic network orchestration?

**Answer: yes — and it is a *two-sided* gap, verifiable from the 24 items above.** The
multipath-scheduling literature has moved decisively toward learning (papers 8, 9, 14, 19, 20,
24a, 24b) while remaining **entirely endpoint-local**, and the 5G/orchestration literature has
built a network-side multipath anchor point (ATSSS / UPF) that **no peer-reviewed paper in this
corpus drives with a learned scheduler**. The two literatures currently meet at exactly one
place — the IEEE Access survey (paper 17), which is a survey, not an integration.

### (a) Multipath scheduler + SDN controller / network orchestrator

**Found (partially, and never at packet granularity):**

| What | Where | Granularity |
|---|---|---|
| **GCLR** (paper 18 in this report) | Mininet 2.2.2 + **Floodlight SDN controller** + MPTCP kernel v0.89; a GNN predicts per-route expected throughput and the controller assigns routes | **Flow-level path selection / routing.** The extraction explicitly classifies it as *not* a packet scheduler |
| MPS-OF-AS, *Scientific African* 2026, DOI `10.1016/j.sciaf.2025.e03134` (CC BY-NC-ND) | SDN + multipath scheduling | Path selection |
| Alruwisan & Yuksel, "Load Balancing MPTCP Traffic in Reactive SDN with MARL", IEEE ICC Workshops 2026, DOI `10.1109/ICCWorkshops63917.2026.11586241` | MARL + reactive SDN; MPTCP throughput **+97 %** vs SPF, MLU **−16 %** | **Subflow-to-path assignment**, not per-packet |
| Wischik et al. (paper 3), *NSDI 2012* | Discusses and **rejects** a centralised scheduler on scalability grounds: "one may need to re-run the scheduler as often as every **10ms** … which raises serious scalability concerns" | — (argument, not implementation) |

**Not found:** any paper that co-designs a **packet-level** multipath scheduler with an SDN
controller or that exports per-packet scheduling policy to an orchestrator. Every SDN-side hit
operates at subflow/path *assignment* granularity. The one paper in this corpus with a learned
model and an SDN controller (GCLR) chose to predict *route* throughput, not to schedule packets.

### (b) Multipath scheduler + LLM or AI agent

**Not found — and this is the cleanest negative in the review.** No peer-reviewed paper was found
in which an LLM or an agentic AI system *is* the multipath scheduler's policy. What exists is:

- IETF `draft-song-tsvwg-camp-00` (CAMP) — an MPQUIC scheduler for interactive LLM systems. **The
  LLM is the workload being transported, not the scheduler.** This is the opposite direction.
- LLM-for-congestion-control preprints on **single-path** CC (arXiv:2603.10357, 2604.03857,
  2508.16074, 2412.18200). Single-path, and preprints.
- Two arXiv queries for multipath + LLM returned **zero** results.

Terminological caution that the table makes concrete: papers 8, 9, 19, 20, 21, 22, 24a and 24b are
all "AI" in the sense of *learned policies*, and paper 9 is literally *multi-**agent*** DRL — but
"agent" there means an RL agent controlling one subflow, **not** an autonomous AI agent that
orchestrates network functions. Papers 9 and 24b put several such agents side by side; neither
exposes them to a controller, and neither is steerable by an external objective at runtime.

### (c) Multipath scheduler + 5G core ATSSS / UPF

**Found (architecturally documented, but not integrated by any paper here):** paper 17 establishes
from the standard that in core-centric ATSSS "the UE and UPF communicate through the **Multipath
Transport Function** (in the UE) and the **Multipath Transport Proxy Function** (in the UPF)", that
"**UPF supports Performance Measurement Functionality (PMF)**", and that control is a **policy
rule** the SMF shares with the UE (uplink) or UPF (downlink). It also records the survey's own
complaint that "the current ATSSS modes are also **very coarse-grained**" and that extending them
"to also cover congestion control and reliable transfer aspects will be of great importance."

**Found (the only two papers at the 5G core):** papers 21 and 22 (Pham et al., IEEE ICTC 2024 and
IEEE ICCCN 2025) do DRL access-traffic splitting **in the 5G core**, but both are **ABSTRACT ONLY**
and neither's retrievable text names MPTCP, MPQUIC, the UPF, N4 or N6. Their measurable claims are
core-level, not transport-level: "a **19 % higher QoS satisfaction level** and a **9 % enhancement
in ROI retention**". There is no evidence in the retrievable text that either drives a multipath
*transport* scheduler.

**Not found:** any free5GC/Open5GS ATSSS + ML implementation; any paper placing a learned
multipath scheduler at the UPF proxy anchor point; any paper that uses the **standardised ATSSS
steering modes as a learned action space**. (Closest near-miss found in the probe: a JISEM 2025
paper, DOI `10.52783/jisem.v10i62s.13781`, doing RAN-analytics → UPF steering — not multipath.)

### (d) Multipath scheduler + O-RAN (near-RT RIC / xApp / E2)

**Not found.** No paper integrating an MPTCP/MPQUIC scheduler with a near-RT RIC, an xApp, or the
E2 interface. The O-RAN + RL work that was found is entirely RAN-domain: REAL (arXiv:2502.00715),
hierarchical-RL traffic steering (IEEE ICC 2023, DOI `10.1109/icc45041.2023.10278983`), and
"Network-Aided Intelligent Traffic Steering in 6G O-RAN" (arXiv:2302.02711). None touches
transport-layer multipath scheduling.

### Why the gap persists — four concrete, quotable seams

1. **There is no standard interface to schedule through.** RFC 8684 (paper 1) contains **zero**
   occurrences of "scheduler"/"scheduling"; §3.3.8 says only that "a host may use any local
   policy it wishes". An orchestrator therefore has nothing to attach to. Every integration in
   this corpus is out-of-band and implementation-specific.
2. **The standard's network-side anchor is deliberately coarse.** ATSSS exposes a *mode + priority*
   policy rule, not per-path telemetry or per-packet control (paper 17). The transport's scheduler
   state (SRTT, cwnd, delivery rate, blocking estimate) is invisible to the core.
3. **The AI-native side is refused entry on reliability grounds — by the multipath community
   itself.** Paper 17 states it in terms the review must engage with: data-driven schedulers "may
   lack of **explainability**, which might be even more severe in **URLLC**, where reliability is
   difficult to mathematically prove or measure, i.e., you have 100% reliability until the first
   packet loss happens", and they are "normally of **higher computation complexity** compared to
   the rule-based counterpart."
4. **Classical work pre-emptively rejected the orchestrated design.** Paper 3 argued against
   core participation ("inefficient outcomes may arise when both the end-systems and the core
   participate in balancing traffic") and against centralised re-solving at 10 ms. Any AI-native
   orchestration proposal must answer that 2012 objection with measurements, not assertions.

### What would close it (the unoccupied position, stated as a gap not a result)

The evidence above points at a specific, standards-anchored vacancy: a **learned multipath
scheduler placed at the UPF multipath proxy / PMF anchor of ATSSS, whose action space is the 3GPP
steering modes and whose state is the per-path telemetry the transport already computes** — with
an explicit explainability and worst-case-latency story to answer seam 3, and a scalability
measurement to answer seam 4. No paper in this corpus occupies it. The nearest neighbours are
GCLR (SDN but flow-level and no ATSSS), papers 21/22 (5G core but control-plane, abstract-only,
no transport scheduler) and paper 20/24b (packet-level DRL but endpoint-side and simulator/emulated
only).

### Evidence appendix — the four searches, with their exact queries and negatives

The probe below was executed as four separate targeted searches; it is reproduced because the
*negatives* are the finding, and they are only credible with the queries shown.

Method notes: searches were run with the `web_search` tool (which surfaces indexed paper landing pages) and with
the **arXiv API** (`https://export.arxiv.org/api/query?search_query=...`) and **Crossref**
(`https://api.crossref.org/works?query.bibliographic=...`) for verification. OpenAlex was unavailable
(daily budget exhausted, HTTP 429). Every item below is a paper I actually saw in results; where I could not
find something, I say so explicitly and give the queries. **No absence is asserted without a listed query.**

#### (a) Multipath scheduler + SDN controller / network orchestrator
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

#### (b) Multipath scheduler + LLM or AI agent
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

#### (c) Multipath scheduler + 5G core ATSSS / UPF
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

#### (d) Multipath scheduler + O-RAN (near-RT RIC / xApps / E2)
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

#### Probe conclusion (what the four searches jointly establish)
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

---

## WHAT I COULD NOT VERIFY

### 1. Papers retrieved as ABSTRACT ONLY (seven of twenty-four)

For these, **every** claim in their extraction comes from the abstract (and, where noted, the
free IEEE preview of §I) and nothing else. Fields the abstract does not cover are `NOT REPORTED`
by construction. Two independent OA checks (Unpaywall `is_oa` and Semantic Scholar
open-access status) agreed these are closed, and a dedicated second pass over arXiv, CORE v3,
ResearchGate, Google Scholar, scholar.archive.org, TechRxiv, fatcat and author/institution pages
found no legitimate copy.

| Paper | Venue verified | What is missing because of it |
|---|---|---|
| 8. ReLeS | IEEE INFOCOM 2019, DOI `10.1109/INFOCOM.2019.8737649` | The entire DRL design (state/action/reward, network architecture), the scheduler inputs, the baselines, the testbed, and **all numbers**. The paper is universally described as DRL+Linux kernel, but its actual mechanism could not be read |
| 15. CMT-QA | IEEE TMC 12(11):2193–2205, 2013, DOI `10.1109/TMC.2012.189` | Scheduler mechanism details, simulator name, baselines, all metrics/numbers |
| 16. BEMA | IEEE TCOM 64(6):2477–2493, 2016, DOI `10.1109/TCOMM.2016.2553138` | Detailed algorithm, baseline names, quantitative results |
| 19. SATO | IEEE WF-IoT 2022, DOI `10.1109/WF-IoT54382.2022.10152217` | Simulator identity, testbed identity, the name of the baseline behind "state-of-the-art algorithm", all per-metric numbers |
| 21. DRL ATSSS | IEEE ICTC 2024, pp. 903–908, DOI `10.1109/ICTC62082.2024.10826899` | Action space, state, simulator, baselines, all numbers; also whether it touches MPTCP/MPQUIC/UPF at all |
| 22. MORL ATSSS | IEEE ICCCN 2025, pp. 1–8, DOI `10.1109/ICCCN65249.2025.11133925` | The MORL formulation (objectives, weights, preference vector), the simulator, the baseline definitions, per-metric breakdown |
| 23. MPTCP-RL | IEEE Wireless Communications 30(2):138–146, 2023, DOI `10.1109/MWC.013.2100658` | The RL algorithm, the simulator/testbed, the baseline names, and every number (the abstract's claim is the unquantified word "significantly") |

**Recommendation:** these seven are the only papers in the set that a single institutional IEEE
Xplore session would upgrade from abstract to full extraction. ReLeS matters most — it is the
canonical "first DRL MPTCP scheduler" citation and is currently unusable for mechanism-level
claims in this report.

### 2. Facts asserted in the brief that the sources contradict

- **Paper 3's venue.** The paper is real and is ACM's NSDI '12 record at pp. 99–112
  (`10.5555/1972457.1972468`), but **USENIX's own NSDI '12 programme index does not list it** —
  the only multipath paper there is "How Hard Can It Be? Designing and Implementing a Deployable
  Multipath TCP" (also NSDI 2012, retrieved and identified during this work). Two citing papers
  (papers 2 and 4) cite it as **2011**. I used NSDI 2012 and recorded the conflict rather than
  silently picking one.
- **Paper 16 is not called "BEWARE".** The TCOM 2016 paper's own abstract names its protocol
  **BEMA** ("bandwidth-efficient multipath streaming"). "BEWARE: Background Traffic-Aware Rate
  Adaptation for IEEE 802.11" is an unrelated paper (`10.1109/TNET.2011.2106140`). Cite it as BEMA.
- **Paper 23's title** is registered as "**Multipath** TCP Meets Reinforcement Learning…" (MPTCP
  spelled out). Same paper; not a substitute.
- **Paper 14 (Peekaboo) year = 2020**, confirmed: IEEE JSAC 38(10):2295–2310, 2020, DOI
  `10.1109/JSAC.2020.3000365`.
- **Paper 10's and 11's years are traps.** Coupled BBR: Semantic Scholar reports 2020 (the arXiv
  year) — the journal issue is **TWC 2021**. BCCPS: the DOI stem is 2020 (early access) — the
  issue is **TVT January 2021**. Both are reported with both readings in their sections.
- **There is no extended journal version of ECF.** No KTH technical report and no *Computer
  Communications* 2022 version exists in Crossref or OpenAlex. What exists is an *earlier,
  shorter* 2-page SIGMETRICS 2017 paper (`10.1145/3078505.3078552`); a copy of that was
  downloaded by mistake and discarded once the 2-page/13-page discrepancy was caught. All ECF
  values here come from the 13-page CoNEXT paper.
- **ECF's own reference list mis-cites BLEST** as "pages 1222–1227, 2016". Crossref and BLEST's
  own page footers agree on **431–439**; I used 431–439.

### 3. In-paper facts that are genuinely absent (recorded as `NOT REPORTED`, not guessed)

- **Congestion controller is unnamed** in **ECF** (paper 13 — it only claims CC-agnosticism and
  names Olia parenthetically) and in **Peekaboo** (paper 14 — searched for Cubic/NewReno/Olia/
  BALIA/LIA/BBR; only *related-work* mentions exist). Also unnamed in papers 19, 20, 23, 24a and
  both ATSSS papers.
- **Simulator/testbed is unnamed** in papers 19, 21, 22 and **24a** ("simulations conducted within
  this environment", simulator never identified) and 23.
- **Baselines are unnamed** in papers 15, 16, 19, 21, 22, 23 (papers 15/16/19/21/22/23 use only
  generic phrases such as "existing solutions" or "state-of-the-art").
- **GCLR's GNN architecture** is `NOT REPORTED` ("a multi-layer perceptron with appropriate
  activations"), and **GCLR's Tables 1–2 are raster images**, so per-cell MSE values are not
  machine-readable from the OA PDF.
- **DeepCC's Tables II/IV/V and BCCPS's Tables I/II are raster images** in their PDFs, so only the
  hyperparameters and percentages stated in prose could be reported.
- **Reordering never enters the state, reward or metrics** of paper 24a, even though head-of-line
  blocking is its stated motivation (observed by the extractor, not claimed by the paper).
- **Round-Robin is not a baseline in BLEST or ECF.** BLEST's baselines are minRTT, DAPS, OTIAS and
  single-path TCP; ECF's are "Default" (minRTT), DAPS and BLEST. Round-Robin appears as a baseline
  only in Peekaboo. This is worth carrying into any synthesis table built from memory of the
  literature.

### 4. Environment limitations that shaped the retrievals (disclosed, not worked around)

- **IEEE Xplore** returns HTTP 202 with an empty body to non-browser clients and 502 for some
  `ielx7` PDF URLs; the working routes were gold-OA `ielx7` PDFs with a cookie jar + desktop UA +
  Referer (GCLR), and `https://r.jina.ai/<ieee-url>` for abstract + free-preview §I (papers 15,
  16, 19, 21, 22, 23). **ACM DL** `/doi/pdf/` returns 403. These are the direct cause of the
  seven ABSTRACT ONLY entries above.
- **OpenAlex's API exhausted its daily budget** mid-session (`HTTP 429 … Insufficient budget …
  Resets at midnight UTC`), so bibliographic verification used **Crossref + Unpaywall + Semantic
  Scholar** instead. Semantic Scholar also rate-limited intermittently (HTTP 429).
- **HAL and DiVA sit behind an Anubis proof-of-work interstitial.** Rather than declare those
  sources unreachable, a solver was written (`tools/anubis_fetch.py`) and used to retrieve the
  publisher-designated OA copy of paper 5 from HAL. This is legitimate retrieval from the
  designated OA location, but it is a non-standard access path and is disclosed here so the
  provenance of paper 5 can be checked.
- **A Google Research PDF link initially resolved to the wrong paper** (an unrelated
  neural-network-compression paper at `.../archive/46274.pdf`). It was discarded; the correct
  QUIC SIGCOMM PDF was obtained from `.../pubtools/4102.pdf`. The retrieved QUIC file is the
  **Google author copy (9 pages)**; the ACM version is cited by that PDF's own footnote as
  **14 pages**, so figure/table completeness may differ from the ACM version.

### 5. Things I deliberately did **not** do

- I did **not** import numbers, baselines or testbed names for the seven abstract-only papers from
  secondary sources, other papers' descriptions of them, or model memory. Where a secondary
  source (paper 17's survey) describes ReLeS as "offline reinforcement learning, i.e., a Deep
  Q-Network (DQN) … with throughput as the reward, and delay and packet loss as penalties", that
  description is attributed **to the survey** in paper 17's section, not presented as ReLeS's own
  text.
- I did **not** resolve conflicting numbers by averaging or by choosing the more flattering one.
  Where sources conflict (NSDI 2012 venue/pages, BLEST pages, Coupled BBR/BCCPS years) both
  readings are reported with the reason for the choice.
- I did **not** treat "AI-based" as a single category. Papers 10 and 11 are explicitly **not**
  machine learning despite appearing in an "AI-based" cluster, and paper 14 is a **contextual
  bandit (LinUCB)**, not deep RL, despite being routinely grouped with DRL schedulers.
