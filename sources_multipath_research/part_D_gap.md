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

