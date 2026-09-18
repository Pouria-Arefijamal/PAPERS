# 09 — Paper-by-Paper Summaries

Each entry follows the requested structure. Fields that could not be verified from a
source actually retrieved in this session are marked **Not verified from the free
record** — they are not guesses. Where a paper was read in full, the version read is
stated (several are author preprints or accepted manuscripts, which may differ from the
version of record).

Contents:
- **A. Foundational papers** (§1–§6)
- **B. Flow / packet / traffic scheduling** (§7–§15)
- **C. Network and service orchestration** (§16–§23)
- **D. Multipath transport and scheduling** (§24–§32)
- **E. LLM / agentic network management and benchmarks** (§33–§41)
- **F. Model efficiency: fine-tuning, distillation, compression** (§42–§49)

---

# A. FOUNDATIONAL PAPERS

# PAPER 1 — Multipath TCP: From Theory to Practice

## 1. Problem
Whether multipath TCP can be built and deployed such that it delivers resource pooling
(aggregating multiple access links) and resilience, without becoming unfair to ordinary
single-path TCP.

## 2. Architecture
Multiple TCP subflows — one per available interface/address — bound into a single MPTCP
connection with a connection-level sequence space and a receive-side reassembly buffer.

## 3. Network
4G/3G-era access networks plus Wi-Fi; endpoint transport, not a network function.

## 4. Inputs
Per-subflow congestion state and RTT; available interfaces.

## 5. Decision
Which subflow carries each packet (scheduling) and how each subflow's congestion window
evolves (coupled congestion control).

## 6. Algorithm
First full MPTCP implementation with a simple default scheduler and coupled congestion
control; the contribution is the working system and its experimental evaluation.

## 7. Objective
Deliver real throughput aggregation and failover benefit in practice.

## 8. Constraints
Fairness towards competing single-path TCP; receive-buffer limits.

## 9. Experimental Setup
Real multi-homed testbed using 3G and Wi-Fi interfaces. Exact hardware and traffic
parameters: not verified from the free record.

## 10. Baselines
Single-path TCP.

## 11. Metrics
Throughput, completion time, resilience to path failure.

## 12. Results
Demonstrates measurable aggregation and failover benefit versus single-path TCP. Exact
figures: not verified from the free record.

## 13. Limitations
Early prototype; the simple scheduler later proved problematic on paths with very
different characteristics.

## 14. Reproducibility
Moderate — the implementation lineage is open (Linux MPTCP), but this early prototype's
exact experimental configuration is not readily reproducible today.

## 15. Relevance to my PhD
This paper, with the coupled-congestion-control work that followed, established that
**scheduling and congestion control must be co-designed** and that naive schedulers
misbehave on heterogeneous paths. That is the founding problem statement for every
learning-based multipath scheduler, and it is the reason "multipath scheduling" is a
distinct research area rather than a routing sub-problem.

---

# PAPER 2 — Design, Implementation and Evaluation of Congestion Control for Multipath TCP (NSDI 2012)

## 1. Problem
How to couple congestion control across subflows so that a multipath flow shifts traffic
away from congested paths while remaining fair to single-path TCP.

## 2. Architecture
Sender-side coupled congestion controller inside the MPTCP stack.

## 3. Network
Heterogeneous access networks; endpoint transport.

## 4. Inputs
Per-subflow congestion window, RTT and loss.

## 5. Decision
Per-subflow congestion-window increase/decrease derived from a coupled fluid model.

## 6. Algorithm
Coupled congestion control (the LIA family): a flow-level aggregated increase rule with a
per-subflow decrease rule, provably fair against single-path TCP at equilibrium.

## 7. Objective
Resource pooling with fairness and congestion balancing across paths.

## 8. Constraints
Fairness to single-path TCP; non-negative windows.

## 9. Experimental Setup
Real Linux implementation evaluated over emulated and real networks. Exact topology and
traffic parameters: not verified from the free record.

## 10. Baselines
Single-path TCP; uncoupled multipath congestion control.

## 11. Metrics
Throughput, fairness, congestion balance, responsiveness.

## 12. Results
Shows that uncoupled multipath flows starve single-path TCP and that coupling restores
fairness while retaining pooling. Exact figures: not verified from the free record.

## 13. Limitations
Solving fairness at the congestion-control layer leaves the scheduler able to undo the
benefit — the two are optimised separately.

## 14. Reproducibility
Moderate — the algorithm is specified precisely and implemented in Linux MPTCP.

## 15. Relevance to my PhD
Establishes the **interaction constraint** that any AI/DRL multipath scheduler must
respect: changing split ratios interacts with the coupled controller. DeepCC (PAPER 29)
later attacks exactly this coupling by learning both jointly.

---

# PAPER 3 — Experimental evaluation of multipath TCP schedulers (ACM SIGCOMM CSWS 2014)

## 1. Problem
How much does the choice of MPTCP scheduler matter on heterogeneous paths, and what goes
wrong with the default scheduler?

## 2. Architecture
Sender-side MPTCP schedulers compared under a controlled heterogeneous-path setup.

## 3. Network
Wi-Fi plus cellular; endpoint transport.

## 4. Inputs
Per-subflow RTT, congestion window and send-buffer occupancy.

## 5. Decision
Packet-to-subflow assignment.

## 6. Algorithm
Systematic comparison of the default (lowest-RTT-first) scheduler against alternatives.

## 7. Objective
Quantify the scheduler's contribution to end-to-end performance.

## 8. Constraints
Receive-buffer size (the binding constraint in the asymmetric case).

## 9. Experimental Setup
Real testbed with emulated asymmetric path characteristics. Exact parameters: not
verified from the free record.

## 10. Baselines
Default MPTCP scheduler and variants.

## 11. Metrics
Throughput, receiver buffer occupancy, reordering.

## 12. Results
Demonstrates that the default scheduler can cause severe receive-buffer blocking on
asymmetric paths. Exact figures: not verified from the free record.

## 13. Limitations
Two-path testbed; predates learning-based schedulers.

## 14. Reproducibility
Moderate — the comparison is well specified but the testbed is not publicly packaged.

## 15. Relevance to my PhD
This is the canonical evidence that **head-of-line blocking is a scheduler problem, not a
protocol problem**. Any AI scheduler must be evaluated against this failure mode, and the
paper's metrics (buffer occupancy, reordering) should be in my evaluation suite.

---

# PAPER 4 — Low-Latency Scheduling in MPTCP (IEEE/ACM ToN 2019)

## 1. Problem
Throughput-oriented schedulers are wrong for latency-sensitive traffic: MPTCP's default
scheduler can increase, not decrease, completion time.

## 2. Architecture
Sender-side MPTCP scheduler designed around an analysis of where delay comes from.

## 3. Network
Heterogeneous access; endpoint transport.

## 4. Inputs
Per-subflow RTT and congestion state.

## 5. Decision
Packet-to-subflow assignment chosen to minimise expected delivery time.

## 6. Algorithm
Latency-optimised scheduling rules derived from decomposing the delay components of
MPTCP (queueing, reordering and transmission delay).

## 7. Objective
Minimise end-to-end latency rather than maximise throughput.

## 8. Constraints
Correctness of in-order delivery; congestion-control compatibility.

## 9. Experimental Setup
Linux MPTCP implementation evaluated in emulated and real networks. Exact parameters: not
verified from the free record.

## 10. Baselines
Default lowest-RTT-first MPTCP scheduler.

## 11. Metrics
End-to-end latency, throughput, reordering.

## 12. Results
Shows latency-optimised scheduling reduces completion time for short flows relative to
the default scheduler. Exact figures: not verified from the free record.

## 13. Limitations
Rule-based; depends on RTT estimation accuracy; no learning and no awareness of
network-level objectives.

## 14. Reproducibility
Moderate — rule-based and implemented in an open MPTCP stack, but the evaluation setup is
not packaged.

## 15. Relevance to my PhD
The strongest **classical latency baseline** for a DRL/LLM scheduler to beat. It also
demonstrates the objective-function question at the heart of my proposal: latency,
throughput and fairness trade off, and *who sets the objective* is exactly the
orchestrator's job.

---

# PAPER 5 — Multipath QUIC: Design and Evaluation (ACM CoNEXT 2017)

## 1. Problem
Can multipath operation be added to QUIC, and what does it buy over single-path QUIC and
MPTCP?

## 2. Architecture
A single QUIC connection spanning multiple paths, with a pluggable scheduler and path
management.

## 3. Network
Fixed and wireless; endpoint transport (userspace).

## 4. Inputs
Per-path RTT, congestion window, loss, path state.

## 5. Decision
Packet-to-path assignment plus path addition/removal.

## 6. Algorithm
Multipath QUIC design with a lowest-RTT style scheduler; the contribution is the protocol
extension and its measurement.

## 7. Objective
Aggregate bandwidth and survive path failure while keeping QUIC's security and handshake
properties.

## 8. Constraints
QUIC's connection-level packet-number space and loss-recovery interaction.

## 9. Experimental Setup
Real userspace implementation evaluated over emulated networks. Exact parameters: not
verified from the free record.

## 10. Baselines
Single-path QUIC; MPTCP.

## 11. Metrics
Throughput, completion time, handover behaviour.

## 12. Results
Demonstrates bandwidth aggregation and path-failure resilience, and identifies scheduling
and reordering as the key implementation challenges. Exact figures: not verified from the
free record.

## 13. Limitations
Early design with a simple scheduler; the interaction with QUIC loss recovery is delicate.

## 14. Reproducibility
Moderate–strong — the implementation lineage (picoquic/quant) is open.

## 15. Relevance to my PhD
Opens the MPQUIC scheduler design space that later RL-based MPQUIC schedulers inhabit
(PAPERS 30, 31, 32), and shows that the **scheduling interface** — not just the policy —
is a research object. PAPER 33 argues that interface should be token-based, which is
precisely the interface an orchestrator or agent would need.

---

# PAPER 6 — Knowledge-Defined Networking (ACM SIGCOMM CCR 2017)

## 1. Problem
Network operation is manual and reactive; how should a *knowledge plane* be architected
above the data and control planes to automate it?

## 2. Architecture
Three planes: data plane, control plane, and a new **knowledge plane** that observes,
learns, reasons and issues decisions.

## 3. Network
Generic (SDN-based); the paper's prototype is a small emulated network with NFV elements.

## 4. Inputs
Network telemetry and state; the knowledge plane's learned models.

## 5. Decision
Policies and control actions derived from learned knowledge (e.g. overlay routing
decisions from a learned performance model).

## 6. Algorithm
Machine learning (learned models of network behaviour) combined with reasoning over those
models.

## 7. Objective
Close the loop autonomously, replacing human-in-the-loop operation.

## 8. Constraints
Not formalised in the paper — this is one of its acknowledged open problems.

## 9. Experimental Setup
Prototype on an emulated network: about 12 overlay nodes, 19 underlay elements, 72 links,
using OMNeT++ with Open vSwitch and Snort on an ESXi host.

## 10. Baselines
Not clearly reported in the retrieved source.

## 11. Metrics
Model accuracy (relative error of the learned overlay model) and NFV CPU model behaviour.

## 12. Results
The learned overlay model reaches a relative error of roughly **1% with 3,000 training
samples**; the NFV CPU model is presented only as a CDF figure.

## 13. Limitations
A vision paper with a small prototype. It does not solve how the knowledge plane makes
**safe or verifiable** decisions, nor how it is governed, audited or rolled back.

## 14. Reproducibility
Weak–moderate — prototype described, artifacts not public.

## 15. Relevance to my PhD
KDN is the **direct conceptual ancestor of LLM/agentic orchestration**: an intelligent
plane above control. Its unsolved problem — verifiable, safe autonomous decision-making —
is precisely the problem that agentic network management still has not solved in 2026.
Any PhD proposal in this space should position itself explicitly relative to KDN.

---

# B. FLOW / PACKET / TRAFFIC SCHEDULING

# PAPER 7 — Cellular Network Traffic Scheduling With Deep Reinforcement Learning (AAAI 2018)

## 1. Problem
Schedule delay-tolerant IoT traffic (software updates, backups) alongside real-time
cellular traffic (voice, video) **without violating the real-time service guarantees**.

## 2. Architecture
A centralised cellular base-station controller that decides which device to serve and at
what rate each time slot.

## 3. Network
4G/LTE RAN; single base station serving many devices.

## 4. Inputs
Per-device queue/backlog state and channel state; each application's delay tolerance.

## 5. Decision
Which device to schedule in each slot and the transmission rate allocated to it.

## 6. Algorithm
A per-slot optimisation derived from **Lyapunov drift-plus-penalty** is approximated by a
deep RL policy (policy-gradient/actor-critic style), so the scheduler learns rather than
solving the optimisation online each slot.

## 7. Objective
Minimise time-averaged queue backlog (delay) of delay-tolerant traffic while respecting
real-time service guarantees.

## 8. Constraints
Real-time applications must receive fixed minimum rates; delay-tolerant queues must remain
stable.

## 9. Experimental Setup
Custom simulation of a base station with IoT devices. Exact UE counts and traffic
parameters: not verified from the abstract.

## 10. Baselines
Not verified from the abstract.

## 11. Metrics
Delay/backlog of delay-tolerant traffic; real-time service satisfaction.

## 12. Results
The abstract reports that the learned scheduler approaches the performance of the
Lyapunov-optimal policy while being practical to run; exact numbers are not in the
abstract retrieved.

## 13. Limitations
Single-cell simulation; the technical core is Lyapunov optimisation with learned
approximation rather than an end-to-end learned scheduler; no 5G core, slicing or QoS-flow
concepts.

## 14. Reproducibility
Weak — no public artifact identified.

## 15. Relevance to my PhD
Important methodological template: **combine classical optimisation structure (Lyapunov)
with learning**, rather than learning from scratch. This "optimisation-structured RL"
pattern is one of the most promising hybrids for safe network control and is directly
transferable to the LLM-planner + optimiser-executor architecture I propose.

---

# PAPER 8 — Intelligent Resource Scheduling for 5G Radio Access Network Slicing (IEEE TVT 2019)

## 1. Problem
Allocate radio resource blocks across 5G RAN slices so that each tenant receives its
contracted share while spectral efficiency is preserved.

## 2. Architecture
RAN slicing with an infrastructure provider and multiple tenants; a slice-aware scheduler
at the MAC layer.

## 3. Network
5G RAN (radio access network slicing).

## 4. Inputs
Slice-level demand and QoS requirements, channel quality, queue states.

## 5. Decision
Radio resource-block assignment per slice (and per user inside slices) each scheduling
interval.

## 6. Algorithm
Deep reinforcement learning scheduler operating over the slicing substrate.

## 7. Objective
Satisfy per-slice rate/QoS requirements while maximising resource utilisation.

## 8. Constraints
Per-slice minimum/maximum rates; total resource-block budget.

## 9. Experimental Setup
Not verified from the free record (system-level simulation per the paper).

## 10. Baselines
Not verified from the free record.

## 11. Metrics
Slice-level rate satisfaction; resource utilisation.

## 12. Results
Not verified from the free record.

## 13. Limitations
RAN-only; per-slice rate targets are a proxy for end-to-end SLA; no core or transport
coordination.

## 14. Reproducibility
Weak — no public artifact identified.

## 15. Relevance to my PhD
One of the earliest DRL RAN-slice schedulers and a standard citation for "learning-based
slice scheduling". The gap it leaves — **no end-to-end SLA scoring, no cross-domain
coordination** — is exactly where an orchestrator-integrated scheduler would contribute.

---

# PAPER 9 — Learn to Schedule (LEASCH): DRL for Radio Resource Scheduling in the 5G MAC Layer (IEEE Access 2020)

## 1. Problem
Radio resource scheduling in the 5G MAC layer for users with heterogeneous QoS
requirements.

## 2. Architecture
A simulated gNB whose MAC scheduler is replaced by a DRL agent.

## 3. Network
5G RAN, MAC layer.

## 4. Inputs
Buffer status reports, channel quality indicators, per-bearer QoS class.

## 5. Decision
Resource-block allocation per user per TTI.

## 6. Algorithm
Deep reinforcement learning (DQN family) trained against the 5G MAC environment; the
paper's contribution is the LEASCH environment plus the learned scheduler.

## 7. Objective
Satisfy QoS requirements (throughput/delay) while maximising resource utilisation.

## 8. Constraints
Total available resource blocks; per-bearer QoS targets.

## 9. Experimental Setup
A 5G MAC-layer system-level simulator (the LEASCH environment). Exact parameters: not
verified from the free record.

## 10. Baselines
Classical MAC schedulers (e.g. proportional fair and QoS-aware rules) per the paper.

## 11. Metrics
Throughput, delay, QoS satisfaction, resource utilisation.

## 12. Results
Not verified from the free record beyond the abstract's claim of competitive performance.

## 13. Limitations
MAC-layer scope; no slicing, core or end-to-end view.

## 14. Reproducibility
Moderate — LEASCH is described as a defined environment, but no public repository was
identified in this session.

## 15. Relevance to my PhD
Represents the "replace the scheduler with a learned policy" approach at the lowest layer.
A useful contrast case for my proposal: it shows that a learned scheduler can work, and
also that it is invisible to higher-layer objectives unless an interface is designed.

---

# PAPER 10 — Reinforcement Learning-Based Particle Swarm Optimization for End-to-End Traffic Scheduling in TSN-5G Networks (IEEE/ACM ToN 2023)

## 1. Problem
Compute end-to-end transmission schedules for time-sensitive flows across a network that
spans TSN bridges and a 5G system, so that per-flow deadlines are met.

## 2. Architecture
A centralised scheduling entity (CNC-like) computing gate-control schedules across the
TSN and 5G segments.

## 3. Network
Transport: deterministic networking (TSN) integrated with 5G.

## 4. Inputs
Flow sets (period, deadline, size), topology and link capacities, 5G bridge delay
characteristics.

## 5. Decision
Transmission offsets / gate-control lists (time slots) for each flow on each link/queue.

## 6. Algorithm
**Reinforcement learning used to guide a particle swarm optimisation** search, rather than
as a direct policy.

## 7. Objective
Feasible end-to-end schedule satisfying determinism and deadline bounds (typically
maximising the number of schedulable flows or minimising end-to-end delay).

## 8. Constraints
Per-flow periods and deadlines, link capacity, TSN queue constraints, 5G bridge delay
bounds.

## 9. Experimental Setup
Not verified from the free record; the paper formulates an exact MILP as a reference.

## 10. Baselines
MILP/optimal and pure-PSO baselines per the paper.

## 11. Metrics
Schedulability, end-to-end delay, computation time.

## 12. Results
Not verified from the free record.

## 13. Limitations
Deterministic traffic assumption; the learned component only accelerates the search.

## 14. Reproducibility
Weak — no public artifact identified.

## 15. Relevance to my PhD
A clean instance of **RL + classical optimisation (here a metaheuristic)** for scheduling.
This hybrid pattern is one of the strongest candidates for a safe LLM/agent architecture:
the LLM proposes, the optimiser guarantees feasibility.

---

# PAPER 11 — DecAge: Decentralized Flow Scheduling for Industrial 5G and TSN Integrated Networks (IEEE TNSE 2024)

## 1. Problem
Centralised scheduling across a joint 5G–TSN industrial network does not scale; how can
scheduling be decentralised while still meeting end-to-end deadlines?

## 2. Architecture
Distributed scheduling entities in each domain that coordinate, instead of one centralised
CNC.

## 3. Network
Industrial 5G integrated with TSN.

## 4. Inputs
Flow requirements (period, deadline, size), topology, per-domain capabilities, per-domain
schedule state.

## 5. Decision
Per-flow transmission schedules in each domain.

## 6. Algorithm
Decentralised, deadline/age-aware scheduling with inter-domain coordination.

## 7. Objective
Maximise the number of schedulable time-critical flows / satisfy end-to-end deadlines.

## 8. Constraints
Deadlines, periods, link capacity, per-domain resource limits.

## 9. Experimental Setup
Not verified from the free record.

## 10. Baselines
Not verified from the free record.

## 11. Metrics
Schedulability ratio, deadline satisfaction.

## 12. Results
Not verified from the free record.

## 13. Limitations
Deterministic/industrial traffic model; no learning.

## 14. Reproducibility
Weak — no public artifact identified.

## 15. Relevance to my PhD
Shows the **decentralisation** axis that any orchestrator design must confront: centralised
scheduling does not scale, so a distributed or hierarchical agent architecture is needed.
This directly motivates hierarchical agent designs (LLM planner above DRL executors).

---

# PAPER 12 — NRflex: Enforcing Network Slicing in 5G New Radio (Computer Communications 2022)

## 1. Problem
Dynamically assign bandwidth parts (BWPs) and numerologies to running 5G NR slices so each
slice's QoS requirement is met while minimising the PRBs consumed.

## 2. Architecture
O-RAN-aligned: a Slice Orchestrator, a Non-RT RIC (slice creation via O1), a Near-RT RIC
hosting a Network Slicing Master and a BWP Manager, and the gNB hosting per-slice
pre-processors (eMBB, uRLLC), a BWP multiplexer and the MAC scheduler.

## 3. Network
5G RAN (MAC and NR physical layers) with an O-RAN control plane; core and transport
explicitly out of scope.

## 4. Inputs
Per-slice throughput success rate, per-slice PDU deadline-failure rate, E2 KPI feedback,
UE–slice association.

## 5. Decision
BWP size and numerology per slice; PRB allocation to logical channels.

## 6. Algorithm
An additive-increase control law for BWP size plus deadline-aware pre-processors and a BWP
multiplexer. **The paper explicitly states there is no reward function — this is not RL.**

## 7. Objective
Enforce slice QoS (uRLLC deadline, eMBB throughput) while minimising PRBs allocated to
eMBB slices.

## 8. Constraints
uRLLC maximum latency, eMBB desired throughput, NR numerology/BWP limits.

## 9. Experimental Setup
5G NR system-level simulation; the version read was the EURECOM accepted manuscript.
Exact parameters: not verified from the free record.

## 10. Baselines
Slice-agnostic BWP allocation per the paper.

## 11. Metrics
PRB consumption, throughput satisfaction, deadline-failure rate.

## 12. Results
Reports QoS enforcement at reduced PRB consumption relative to slice-agnostic allocation.

## 13. Limitations
Rule-based control law rather than an optimiser; RAN-only; accepted-manuscript version
read (page/figure numbering may differ from the version of record).

## 14. Reproducibility
Moderate — the algorithm is specified in the paper, but no public artifact was identified.

## 15. Relevance to my PhD
The clearest published example of **RIC-driven slice resource control inside O-RAN**, and
therefore the natural integration point for a learned or LLM-planned slice policy. Its
additive control law is exactly the kind of hand-tuned rule that a DRL/LLM layer could
replace — with the caveat that any replacement must beat it on slice SLA outcomes, not on
proxies.

---

# PAPER 13 — Power Consumption-Aware 5G Edge UPF Selection using DRL (IEEE NFV-SDN 2024)

## 1. Problem
Select the UPF for each new PDU session in an edge–cloud 5G core to minimise system power
consumption while meeting user latency and bandwidth requirements.

## 2. Architecture
Edge–cloud 5G core deployment with multiple distributed UPF instances; a DRL agent makes
the UPF selection at PDU-session establishment.

## 3. Network
5G core, user plane (UPF), deployed across edge and cloud hosts.

## 4. Inputs
Real-time power-consumption metrics from edge and cloud hosts, plus per-user latency and
bandwidth requirements (5QI/QoS).

## 5. Decision
Which UPF instance serves the new PDU session.

## 6. Algorithm
Deep reinforcement learning policy for the PDU-session allocation problem.

## 7. Objective
Minimise total system power consumption subject to QoS satisfaction.

## 8. Constraints
Per-user latency and bandwidth requirements; host capacity.

## 9. Experimental Setup
Simulation of an edge–cloud 5G core deployment; the version read was the University of
Trento accepted manuscript. Exact parameters: not verified from the free record.

## 10. Baselines
Baseline UPF-selection strategies per the paper.

## 11. Metrics
System power consumption; latency and bandwidth satisfaction.

## 12. Results
The DRL policy reduces power consumption relative to the baselines while satisfying latency
and bandwidth requirements (figures per the paper).

## 13. Limitations
Selection only (no UPF scaling, no traffic scheduling inside the UPF); simulation-based;
accepted-manuscript version read.

## 14. Reproducibility
Weak–moderate — no public artifact identified in this session.

## 15. Relevance to my PhD
A concrete **5G-core, DRL-driven, energy-aware placement decision with a QoS constraint** —
one of the closest existing analogues to the job I want an agent to do. The gap it leaves
is the one I intend to fill: it optimises a single decision type in isolation, with no
orchestrator above it and no SLA-level scoring.

---

# PAPER 14 — Joint Routing and Packet Scheduling for URLLC and eMBB Traffic in 5G O-RAN (IEEE ICC Workshops 2022)

## 1. Problem
Schedule coexisting URLLC and eMBB traffic in O-RAN, where URLLC flows have hard latency
budgets and eMBB flows need throughput, and where routing and packet scheduling interact.

## 2. Architecture
O-RAN with a near-real-time RIC controlling joint routing and packet scheduling.

## 3. Network
5G RAN (O-RAN) with transport routing decisions.

## 4. Inputs
Per-flow latency budgets, queue states, radio link quality, traffic class.

## 5. Decision
Route selection and per-TTI packet scheduling for URLLC versus eMBB flows.

## 6. Algorithm
Optimisation/heuristic joint routing–scheduling with O-RAN control-loop integration.

## 7. Objective
Minimise URLLC latency while preserving eMBB throughput.

## 8. Constraints
URLLC latency budget, radio resource limits, route feasibility.

## 9. Experimental Setup
Not verified from the free record.

## 10–12. Baselines, metrics, results
Not verified from the free record.

## 13. Limitations
Workshop paper; evaluation depth not verifiable from the free record.

## 14. Reproducibility
Weak.

## 15. Relevance to my PhD
Represents the **joint scheduling-and-routing** formulation inside O-RAN — the closest
Area 1 work to the "scheduler as a component inside an orchestrated RAN" idea.

---

# PAPER 15 — Programmable and Customized Intelligence for Traffic Steering in 5G Networks Using Open RAN Architectures (IEEE TMC 2023)

## 1. Problem
Traffic steering in Open RAN is typically hard-coded and vendor-specific; how can it be
made programmable and customisable by the operator?

## 2. Architecture
Open RAN with a RAN controller hosting customisable intelligence modules for steering.

## 3. Network
5G RAN (Open RAN).

## 4. Inputs
RAN telemetry (per-UE radio conditions), flow requirements, operator policy configuration.

## 5. Decision
Steering policy parameters and per-flow access selection.

## 6. Algorithm
A programmable control framework with pluggable intelligence modules (not a single learned
policy).

## 7. Objective
Improve throughput and QoS satisfaction relative to static steering.

## 8. Constraints
RAN resource limits; operator policy constraints.

## 9. Experimental Setup
An Open RAN experimental platform. Exact scale: not verified from the free record.

## 10–12. Baselines, metrics, results
Not verified from the free record.

## 13. Limitations
Programmability-focused; does not itself provide a learning or agent-based decision engine.

## 14. Reproducibility
Moderate — built on open Open RAN platforms.

## 15. Relevance to my PhD
Directly relevant as the **integration surface**: a programmable steering control point in
Open RAN is where an agentic or DRL controller would attach. Its limitation is my
opportunity — programmability without intelligence.

---

# C. NETWORK AND SERVICE ORCHESTRATION

# PAPER 16 — Network Service Orchestration: A survey (Computer Communications 2019)

## 1. Problem
Define and organise the field of network service orchestration: what orchestration is,
which standards govern it, which platforms implement it, and what remains open.

## 2. Architecture
Not a system. Defines three orchestrator functional scopes: **Service Orchestration**
(composition, marketplace/OSS-BSS interface), **Lifecycle Orchestration** (workflows and
dependencies, maintaining services per the contracted SLA) and **Resource Orchestration**
(mapping service requests onto virtual/physical resources across NFVO, EMS and SDN
controllers).

## 3. Network
End-to-end and multi-domain, spanning 5G, transport, data-centre and IoT scenarios.

## 4. Inputs
Service requests and descriptors, customer demands, resource availability, SLA contracts.

## 5. Decision (as a taxonomy)
Composition/decomposition, resource mapping, and lifecycle workflows (scaling, topology,
performance management, automation).

## 6. Algorithm
Not applicable — taxonomy and platform survey.

## 7. Objective
Not applicable.

## 8. Constraints
Not applicable.

## 9. Experimental Setup
None (survey of standards, projects and open-source platforms).

## 10. Baselines
Not applicable.

## 11. Metrics
Not applicable.

## 12. Results
None of its own. Notable finding: cross-domain information exchange **"is not a standard"**,
and orchestrators are typically logically centralised over softwarised infrastructure.

## 13. Limitations
Qualitative taxonomy; pre-2020 snapshot; ML/AI-driven orchestration essentially absent from
its coverage.

## 14. Reproducibility
Not applicable (survey).

## 15. Relevance to my PhD
**This is the paper that gives me the vocabulary to keep my own claims honest.** Its
separation of service / lifecycle / resource orchestration is the standard against which I
must classify every "orchestrator" I read — and, as `02_orchestrators.csv` shows, most
papers that call themselves orchestrators actually contribute resource allocation (type B),
not orchestration.

---

# PAPER 17 — Orchestrating Virtualized Network Functions (IEEE TNSM 2016)

## 1. Problem
Where should VNFs be placed and how should they be chained so that end-to-end service
latency is minimised?

## 2. Architecture
A centralised VNF orchestrator over a distributed cloud, mapping service chains onto nodes.

## 3. Network
Core/cloud (NFV), single administrative domain.

## 4. Inputs
Service requests (VNF chains) with latency budgets; node and link capacities; measured
node/link delays.

## 5. Decision
VNF placement and chaining.

## 6. Algorithm
Exact and heuristic optimisation with a latency-aware objective.

## 7. Objective
Minimise end-to-end service latency and orchestration cost.

## 8. Constraints
Node and link capacity, chain ordering, latency budgets.

## 9. Experimental Setup
Simulation over real network topologies; the numbers reported in the accessible preprint
include **CPLEX 34.99 s versus 0.535 s for the heuristic on Internet2** and **more than a
4× OPEX reduction**, with the heuristic **within 1.3× of optimal** and **more than 90% of
middleboxes placed within 5 hops**.

## 10. Baselines
CPLEX optimal solution; latency-agnostic placement.

## 11. Metrics
End-to-end latency, orchestration cost/OPEX, solver runtime, placement distance.

## 12. Results
The heuristic is within 1.3× of optimal while being 65–3,500× faster than exact solving,
and reduces OPEX by more than 4×.

## 13. Limitations
One-shot offline placement; no learning; no continuous re-optimisation; no slice
abstraction; the numbers come from the 2015 preprint, since the TNSM version of record is
paywalled.

## 14. Reproducibility
Moderate — formulations and topologies are described; no public artifact identified.

## 15. Relevance to my PhD
This is a **type-B optimisation algorithm that an orchestrator calls**, not an orchestrator
— a distinction the literature routinely blurs. It is also the classical baseline any
learned placement engine should be compared against, and it shows that heuristics can be
within 1.3× of optimal, which sets a high bar for DRL placement claims.

---

# PAPER 18 — 5G Network Slicing Using SDN and NFV: A Survey (Computer Networks 2020)

## 1. Problem
Organise the 5G network-slicing landscape: enablers, architectures, standardisation and
open challenges.

## 2. Architecture
Review-level: ETSI NFV MANO reference architecture with the dual SDN controller split —
**Infrastructure SDN Controller (ISDNC)** providing the underlay for VNF connectivity, and
**Tenant SDN Controller (TSDNC)** providing the tenant overlay.

## 3–8. Inputs / decisions / algorithm / objective / constraints
Not applicable (survey/tutorial).

## 9. Experimental Setup
None.

## 10–12. Baselines / metrics / results
None of its own (it consolidates others' results).

## 13. Limitations
Survey; predates cloud-native and LLM-era orchestration.

## 14. Reproducibility
Not applicable.

## 15. Relevance to my PhD
Supplies the **layered architecture** (infrastructure vs tenant control, per-domain vs
multi-domain orchestration) that my proposed orchestrator must fit into, and documents that
multi-domain slice management is an open problem rather than a solved one.

---

# PAPER 19 — AI-Driven Zero Touch Network and Service Management in 5G and Beyond (IEEE Network 2020)

## 1. Problem
How should AI be embedded in network and service management to achieve zero-touch (fully
automated) operation?

## 2. Architecture
Closed-loop automation with AI/ML at multiple time scales, mapped onto the ETSI ZSM
reference architecture, from intent down to management actions.

## 3. Network
End-to-end (management plane), 5G and beyond.

## 4. Inputs
Telemetry and KPIs; operator intents.

## 5. Decision
Management actions and policy changes.

## 6. Algorithm
AI/ML across control loops (proposed, not implemented).

## 7. Objective
Zero-touch operation with intent-driven, assured service management.

## 8. Constraints
Multi-scale latency constraints of the loops; conflict resolution between loops.

## 9. Experimental Setup
None — research-directions article.

## 10–12. Baselines / metrics / results
None.

## 13. Limitations
Agenda paper with no implementation or measurements; predates LLM-based agents.

## 14. Reproducibility
Not applicable.

## 15. Relevance to my PhD
**Defines the target that agentic network management must hit** — closed loops at multiple
time scales, intent assurance, conflict resolution — and it is the reference against which
I can argue that today's LLM work is only partially there. Note that the later ORION paper
(PAPER 22) explicitly leaves the assurance loop uninstrumented, which is exactly the ZSM
requirement this paper set out.

---

# PAPER 20 — An Autonomous Network Orchestration Framework Integrating LLMs with Continual Reinforcement Learning (IEEE Communications Magazine 2025)

## 1. Problem
Resource allocation in a complex, non-stationary multi-domain infrastructure (space–air–
ground) where the objective changes over time and transition dynamics are unknown.

## 2. Architecture
**ARC** — a two-tier orchestrator. Tier 1 is a retrieval-augmented LLM (LLaMA 3.1-8B, not
fine-tuned) that sequences users and tracks which system objective is active. Tier 2 is a
set of specialised RL agents (one per action type, Mixture-of-Experts style). Static and
Dynamic Knowledge Bases hold service specifications, objective profiles, action profiles,
state history and `[input, chain-of-thought, output]` reasoning exemplars.

## 3. Network
Multi-domain: terrestrial, airborne (HAPS/UAV) and space (GEO/LEO/MEO/HEO) layers, each
hosting compute — a distributed cloud.

## 4. Inputs
Strategist commands (to switch objective), user service requests, semantic QoE feedback,
monitored per-(user, service, resource) state, service specifications, action profiles.

## 5. Decision
An ordered sequence of users, and per user: the hosting node for each functional block, the
compute and storage capacity to allocate, and the routing path.

## 6. Algorithm
Hybrid: LLM reasoning with chain-of-thought few-shot prompting for sequencing; **Double
Dueling Deep Q-Learning** agents for per-action allocation; **mathematical solvers offline**
to bootstrap the reasoning exemplars; continual RL with gradient-based sample selection to
avoid catastrophic forgetting.

## 7. Objective
Minimise a normalised allocation cost (energy and monetary price) while maximising the
number of supported users; alternatively maximise quality or balance load (exactly one
objective active at a time).

## 8. Constraints
Compute capacity per node (10–100 MIPS), storage, link bandwidth and latency, radio channel
assignment and transmit power (for the non-terrestrial layers), and the semantic QoE
threshold (if unmet, resources are discarded, the user is re-queued and the reward is 0).

## 9. Experimental Setup
Bespoke numerical simulation. **10 nodes (half non-terrestrial), 10 users**, one functional
block per service (2–5 MIPS), node capacity 10–100 MIPS, link latency 1–10 ms, link
capacity 10–100 Mbps, with a deliberate topology change at iteration 30,000.

## 10. Baselines
The solver-optimal allocation; **RU-ARC** (reward-unaware); **NR-ARC** (no RL agents — the
LLM performs low-level allocation directly).

## 11. Metrics
Normalised allocation cost; reward (average resource cost divided by allocated cost);
number of supported users.

## 12. Results
Presented as two figures with **no numerical values in the text**. The paper states that
ARC achieves near-optimal cost, **recovers after the iteration-30,000 topology change where
RU-ARC fails**, and that NR-ARC performs worse with greater fluctuation "due to LLM
instability".

## 13. Limitations
A single small-scale simulation (10 nodes, 10 users); results are figure-only, which blocks
reproduction and meta-analysis; no comparison against any external published orchestrator or
standard DRL/optimisation baseline; exemplar bootstrapping requires an exact solver, which
the authors admit is not generally available; no SLA object, no slicing, no mapping onto a
standard management plane, no testbed.

## 14. Reproducibility
Weak — no public artifact identified; results are not numerically reported.

## 15. Relevance to my PhD
**This is the single most important paper for my proposed architecture.** It is the clearest
published instantiation of the pattern I want to build on — *LLM as planner, RL as executor,
closed loop with continual learning* — and its limitations map one-to-one onto my
opportunities: quantitative benchmarking against external baselines, grounding in a standard
management plane (O-RAN SMO / ETSI ZSM), hallucination verification of planner decisions,
and scoring on SLA outcomes rather than allocation cost proxies.

---

# PAPER 21 — Using Distributed Reinforcement Learning for Resource Orchestration in a Network Slicing Scenario (IEEE/ACM ToN 2023)

## 1. Problem
Allocate bandwidth, compute and memory across eMBB and URLLC slice flows in a shared
infrastructure under Markov-modulated, time-varying demand, maximising an SLA-shaped system
utility.

## 2. Architecture
Distributed DRL: link controllers and node controllers, each holding actor–critic pairs per
slice class and resource type (bandwidth, compute, memory), with a **central training
manager** that collects observations offline and broadcasts updated policies.

## 3. Network
Transport plus attached compute (core and access nodes); a single infrastructure domain
shared by multiple slice tenants, with hierarchical slices.

## 4. Inputs
Per-flow demand vectors `[throughput, compute, memory, delay]` with 10-state Markov demand;
flow endpoints and performance functions; local observations at each network element.

## 5. Decision
Per-flow, per-timeslot allocated resource vector (bandwidth per link, compute and memory per
node).

## 6. Algorithm
**Advantage Actor-Critic (A2C)** with continuous actions, chosen explicitly because
Q-learning cannot handle continuous action spaces; transfer learning across topologies;
genetic algorithms are discussed and rejected because they cannot run at every timeslot.

## 7. Objective
Maximise expected system utility Ω, a weighted aggregate of per-slice performances.

## 8. Constraints
Link rate (50 Gbps), node compute and memory capacities (60 Gbps/60 Gb core, 20 Gbps/20 Gb
access); URLLC delay requirement 1 ms; eMBB 20 ms; **each flow carries a performance
function F ∈ [0,1] where 1 means the SLA is fully met**.

## 9. Experimental Setup
Authors' own custom simulation over three topologies (Dumbbell, Triangle, Pyramid) plus a
harder "Pyramid+" variant. **2–6 flows** (scalability studied to 9); training 3–5×10⁴
episodes of 50 slots at T = 0.1 s; 500 test episodes. Read from the pre-review 2021 preprint.

## 10. Baselines
Static allocation; an empirical heuristic; cross-topology transfer variants (DRL-D, DRL-T,
DRL-DP, DRL-TP).

## 11. Metrics
Expected system utility E[Ω]; per-resource utility; probability that Ω exceeds a threshold.

## 12. Results
DRL keeps **Ω > 0.45 in almost 50% of test episodes, a 10% gain over the empirical
algorithm**; the empirical algorithm reaches Ω > 0.5 in 50% of episodes versus **0.65–0.7**
for the DRL strategies; DRL trained on one topology **generalises to the Pyramid topology
without retraining**; transfer learning raises E[Ω_c] by more than 5%; **in the harder
Pyramid+ scenario the empirical heuristic slightly beats DRL** on throughput and delay.

## 13. Limitations
Routes are static (assigned at episode start, never optimised); simulation only with 2–6
flows and hand-set parameters; **no admission control** (listed as future work); the central
observation database for training is a scalability and single-point-of-failure concern; all
numbers are from the 2021 preprint, so the published ToN version may differ; in the hardest
scenario the simple heuristic wins.

## 14. Reproducibility
Moderate — the model, topologies and hyperparameters are fully specified in the paper, which
is better than most work in this area, but no code repository was identified.

## 15. Relevance to my PhD
This is the **best-specified DRL orchestration study I found**, and its SLA-performance
function formulation (a continuous satisfaction score in [0,1]) is directly reusable as a
reward shaping device. Its gaps are my opportunity: joint routing and allocation instead of
fixed routes, admission control, decentralised training, hard SLA contracts instead of soft
scores, and cross-domain (RAN/transport/core) closed loops.

---

# PAPER 22 — ORION: Intent-Aware Orchestration in Open RAN for SLA-Driven Network Management (arXiv preprint 2026)

## 1. Problem
O-RAN orchestration relies on fragmented manual policies with no end-to-end intent
assurance from high-level requirements down to low-level configurations.

## 2. Architecture
An O-RAN-compliant intent orchestration pipeline: an **MCP-based SMO layer** performs
semantic translation of natural-language intents into slice/QoS policies, grounded in the
**CAMARA NetworkSliceBooking** schema; a **non-RT RIC rApp** and a **near-RT RIC xApp**
enforce them via **A1** and **E2**; validation and composition flows span SMO app, rApp and
xApp.

## 3. Network
O-RAN (SMO, non-RT RIC, near-RT RIC, gNB), single RAN domain.

## 4. Inputs
Natural-language intents; CAMARA slice-booking schema; KPI telemetry.

## 5. Decision
A1 policies and E2-level enforcement actions for slices.

## 6. Algorithm
Hierarchical LLM agents over Model Context Protocol tools with schema validation; no
numerical optimiser.

## 7. Objective
Translate operator intents into enforceable policies without compromising SLA compliance.

## 8. Constraints
CAMARA schema constraints; O-RAN interface constraints; KPI targets carried in the intent.

## 9. Experimental Setup
Prototype combining MCP services with O-RAN-compliant control functions; **101 natural
language intents** (20 eMBB, 20 URLLC, 60 mMTC); deployment of Open5GS on Kubernetes.
Resource overhead and end-to-end latency measured.

## 10. Baselines
Six commercial LLMs compared against each other rather than against a non-LLM orchestrator.

## 11. Metrics
Policy-creation success rate; 3GPP slice-type classification accuracy across the 101
intents; tool-use reliability; SMO-stage latency; per-intent token cost; resource overhead.

## 12. Results
**100% policy-generation success for high-capacity models** (Claude Opus 4.5, GPT-5, Gemini 3
Pro), 97% for GPT-5 Nano, 85.7% for Gemini 3 Flash, but only **17% for Claude Sonnet 4.5**;
**a 156× cost spread** across models (0.19¢ to 29.68¢ per intent); the SMO LLM stage takes
about **15 s**; the system uses about **141 millicores and 8.5 GiB RAM**. Tool-invocation
failures were the dominant error mode even when intent understanding succeeded.

## 13. Limitations
**Preprint with no peer-reviewed version located.** The evaluation is provisioning- and
policy-generation-centric: it stops at valid A1 policy generation and does **not** measure
whether the enforced policies delivered the intended SLA. The authors themselves rate the
lifecycle/assurance stage only partially implemented. Single RAN domain; no comparison to a
classical optimisation baseline.

## 14. Reproducibility
Moderate — the 101-intent dataset is released; the prototype is described; no code
repository confirmed.

## 15. Relevance to my PhD
**The closest published attempt to place an LLM agent inside a standard O-RAN management
hierarchy**, which makes it both the strongest prior art and the clearest statement of what
is missing. Its measured 15 s SMO-stage latency versus a millisecond-scale service cadence
is the concrete evidence for the "latency is the unaddressed blocker" finding, and its
combined success/cost/latency reporting is a model for how I should evaluate my own system.

---

# PAPER 23 — Open RAN xApps Design and Evaluation: Lessons Learnt and Identified Challenges (IEEE JSAC 2024)

## 1. Problem
How are xApps actually designed, controlled and evaluated on programmable O-RAN platforms,
and what practical obstacles remain?

## 2. Architecture
O-RAN with a near-RT RIC hosting multiple xApps that consume E2 telemetry and issue E2
control actions, under the non-RT RIC/SMO.

## 3. Network
RAN (O-RAN), single domain.

## 4. Inputs
E2 KPI telemetry; xApp policies.

## 5. Decision
Radio control actions per xApp.

## 6. Algorithm
xApp-specific (several ML-based xApps are studied).

## 7. Objective
Improve RAN KPIs (throughput, resource allocation, mobility) as defined per xApp.

## 8. Constraints
E2 interface semantics and timing; xApp coexistence.

## 9. Experimental Setup
Open RAN programmable experimental platforms (Colosseum / OpenRAN Gym class).

## 10–12. Baselines, metrics, results
Per-xApp; not consolidated in the free record.

## 13. Limitations
Studies design practice rather than proposing a single orchestrator; cross-xApp conflict
resolution at scale remains open.

## 14. Reproducibility
Moderate — built on open O-RAN platforms.

## 15. Relevance to my PhD
Establishes the **xApp ecosystem** my agent would have to live in, and identifies xApp
conflict as a first-class problem — which is precisely what an orchestrating agent above the
RICs should arbitrate.

---

# D. MULTIPATH TRANSPORT AND SCHEDULING

# PAPER 24 — TCP Extensions for Multipath Operation with Multiple Addresses (RFC 8684, IETF 2020)

## 1. Problem
Standardise how a single transport connection can use multiple IP addresses/interfaces.

## 2. Architecture
Multiple TCP subflows bound into one MPTCP connection, with a connection-level data
sequence space and DSS mapping for reassembly.

## 3. Network
Any IP network; endpoint transport.

## 4. Inputs
Subflow state (RTT, congestion window, send-buffer space).

## 5. Decision
Packet-to-subflow assignment (left deliberately loose), plus path management.

## 6. Algorithm
Normative specification. **The default scheduler is a simple policy and is explicitly
replaceable.**

## 7. Objective
Resource pooling and resilience while remaining fair to single-path TCP (coupled congestion
control is required).

## 8. Constraints
Coupled congestion control; receive-buffer and reordering semantics.

## 9. Experimental Setup
Not applicable (standard).

## 10–12. Baselines / metrics / results
Not applicable.

## 13. Limitations
Provides no optimal scheduler, no delivery-mode semantics beyond what is specified, and no
mechanism for the network to signal objectives into the scheduler.

## 14. Reproducibility
Not applicable — but it is precisely what makes implementations interoperable.

## 15. Relevance to my PhD
The standard **fixes the interface that every scheduler — classical, DRL or agent-driven —
must work within**. The important observation for my proposal is that the standard exposes a
pluggable scheduler point but **no channel for network-level objectives**; supplying one
(from an orchestrator or agent) is an architectural contribution waiting to be made.

---

# PAPER 25 — BLEST: Blocking Estimation-Based MPTCP Scheduler (IFIP Networking 2016)

## 1. Problem
On paths with very different characteristics, MPTCP's in-order delivery requirement causes
head-of-line blocking that destroys goodput.

## 2. Architecture
Sender-side MPTCP scheduler that predicts, for each subflow, the delay it would impose on
the next in-order segment.

## 3. Network
Heterogeneous wireless access; endpoint transport.

## 4. Inputs
Estimated blocking delay per subflow, derived from RTT and send-rate estimates.

## 5. Decision
Packet-to-subflow assignment, penalising subflows predicted to cause blocking.

## 6. Algorithm
Blocking-estimation heuristic.

## 7. Objective
Minimise head-of-line blocking and improve goodput on asymmetric paths.

## 8. Constraints
In-order delivery semantics; receive buffer.

## 9. Experimental Setup
Linux MPTCP implementation evaluated in emulated and real heterogeneous networks. Exact
parameters: not verified from the free record.

## 10. Baselines
Default lowest-RTT-first MPTCP scheduler.

## 11. Metrics
Goodput, head-of-line blocking delay, completion time.

## 12. Results
Substantially reduces blocking and improves goodput on asymmetric paths. Exact figures: not
verified from the free record.

## 13. Limitations
Heuristic; depends on send-rate estimation accuracy; no learning; no network-level objective.

## 14. Reproducibility
Moderate — implemented in an open MPTCP stack; evaluation setup not packaged.

## 15. Relevance to my PhD
With ECF (PAPER 26), **the classical baseline that any learned scheduler must beat**, and
also the clearest demonstration that the scheduler's objective (avoid blocking) is a
*network-observable* trade-off. If my agent sets objectives for a scheduler, BLEST-style
blocking estimation is a natural feasibility check the agent must respect.

---

# PAPER 26 — ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths (ACM CoNEXT 2017)

## 1. Problem
Schedulers that ignore the receive buffer overload the fastest path and stall on the
slowest; how should in-flight data be balanced across heterogeneous paths?

## 2. Architecture
Sender-side MPTCP scheduler that tracks per-path in-flight bytes and the receive buffer.

## 3. Network
Heterogeneous access; endpoint transport.

## 4. Inputs
Per-subflow RTT, congestion window, slow-start state, receive-buffer size, in-flight bytes.

## 5. Decision
Packet-to-subflow assignment with an explicit penalty on the best path.

## 6. Algorithm
ECF heuristic: penalise the fastest path by the RTT difference and cap in-flight data on
slower paths using a rate-estimation hook in the congestion-control module.

## 7. Objective
Improve goodput on heterogeneous paths by balancing receive-buffer occupancy.

## 8. Constraints
Receive-buffer size; in-order delivery.

## 9. Experimental Setup
Linux MPTCP implementation over emulated heterogeneous networks. Exact parameters: not
verified from the free record.

## 10. Baselines
Default MPTCP scheduler; BLEST and other reordering-aware schedulers.

## 11. Metrics
Goodput, completion time, buffer occupancy.

## 12. Results
Reports higher goodput than the default and competing schedulers on heterogeneous paths.
Exact figures: not verified from the free record.

## 13. Limitations
Rule-based; tuned to the receive-buffer regime; no learning; no network-level objective.

## 14. Reproducibility
Moderate.

## 15. Relevance to my PhD
The second half of the classical baseline pair. Also instructive methodologically: ECF
needed a small patch to the congestion-control module to estimate send rates, illustrating
that **scheduler design is constrained by what the transport stack exposes** — the same
observation that motivates the token-based scheduling interface proposed in PAPER 33.

---

# PAPER 27 — DeepCC: Multi-Agent DRL Congestion Control for MPTCP Based on Self-Attention (IEEE TNSM 2021)

## 1. Problem
MPTCP congestion control and traffic splitting are coupled and hand-tuned; can they be
learned jointly, per subflow, in a way that is practical to run in a real kernel?

## 2. Architecture
Agents run in Linux userspace as daemons and write kernel sysctl parameters; the kernel
exposes the state (cwnd, RTTs, loss, split ratios). One DRL agent per subflow; the agents
form a general-sum game.

## 3. Network
Heterogeneous wireless paths emulated on a real Linux testbed.

## 4. Inputs
A 12-dimensional state per agent: six self-state parameters (average goodput, cwnd, RTT,
jitter, and two more) plus a self-attention-weighted embedding of the other subflows' states
(BiLSTM of size 32 over six-dimensional tokens).

## 5. Decision
Two continuous quantities per subflow: the change to the traffic split ratio and the
multiplicative coefficient for the congestion window (`sr_{t+1} = sr_t + u^p`, `cwnd_{t+1} =
u^w · cwnd_t`).

## 6. Algorithm
**MAPOKTR** — Multi-Agent Policy Optimization using Kronecker-Factored Trust Region
(ACKTR-derived: K-FAC natural gradient with a PPO-style clipped ratio and a
point-probability-distance penalty).

## 7. Objective
Increase total goodput (bytes received correctly *and sequentially* per unit time) and
reduce congestion; multi-agent general-sum game solved toward Nash equilibrium.

## 8. Constraints
Split ratios must remain valid; cwnd coefficients bounded in (0.5, 2); paths emulated with
fixed delay/bandwidth/loss.

## 9. Experimental Setup
**A real Linux testbed, not a simulator**: Dell i7-8700, 32 GB RAM, Ubuntu 16.04, MPTCP
v0.93 on Linux 4.9.x; per-subflow delay/bandwidth/loss limited with `tc` and `ethtool`;
receiver on a separate desktop over a Gigabit switch; `tcpdump` + `scapy` for measurement;
iPerf3 for load and TRex replaying real traces for background traffic. Four MPTCP subflows
run simultaneously.

## 10. Baselines
DRL-CC and SmartCC (re-implemented by the authors, with the caveat that the original state
collection was undocumented); LIA, OLIA, BALIA, wVegas; algorithm comparison against MAACKTR
and MADDPG; architecture ablations (FC, FC+PSA, SSA without PSA); reward ablations (fair,
efficient, fair-efficient).

## 11. Metrics
Total goodput; average jitter (difference of consecutive RTTs); per-path goodput ratio; CPU
and memory usage; convergence time; robustness in unseen environments.

## 12. Results
Self-attention **reduces convergence time by about 50% and increases goodput by about 80%**
compared with common neural-network structures; the fair-efficient reward outperforms
single-objective rewards. Baseline implementation caveat: because DRL-CC and SmartCC code
was not shared, the authors re-implemented them, which weakens that particular comparison.

## 13. Limitations
All paths are emulated on one host with `tc`/`ethtool` rather than real radio; bulk FTP
traffic only (2 MB and 4 MB documents), no video or web workloads; evaluated per connection,
with **no slice, SLA or orchestrator objective anywhere in the loop**.

## 14. Reproducibility
Moderate–strong for method transparency (state, action, algorithm, hyperparameters all
specified) but weakened by the unavailability of the baseline implementations.

## 15. Relevance to my PhD
The most rigorous learning-based multipath scheduler I found, and the best evidence that
**joint congestion-control and scheduling learning works in a real stack**. Its decisive
limitation is my opening: the scheduler is *network-blind* — it optimises its own goodput
objective and cannot be told "this flow is URLLC in slice A, prioritise it". Building the
channel from an orchestrator into this kind of scheduler, and measuring the SLA consequence,
is a concrete, well-founded PhD contribution.

---

# PAPER 28 — ReLeS: A Neural Adaptive Multipath Scheduler Based on DRL (IEEE INFOCOM 2019)

## 1. Problem
Learn a multipath packet-scheduling policy rather than hand-tuning heuristics, while keeping
scheduling fast enough for real time.

## 2. Architecture
A DRL scheduler implemented **in the Linux kernel**, with an **asynchronous training
algorithm** that decouples packet scheduling, data collection and neural-network training.

## 3. Network
Multipath wireless, evaluated over emulated and real network conditions.

## 4. Inputs
**Not reported in the abstract** (the full text is paywalled and no open-access version
exists — confirmed via Unpaywall).

## 5. Decision
A packet-scheduling control policy generated by a learned neural network.

## 6. Algorithm
Deep reinforcement learning plus asynchronous training so that scheduling can run in real
time while learning continues off the critical path.

## 7. Objective
A "comprehensive reward function that takes diverse QoS characteristics into consideration"
— the individual terms are not stated in the abstract.

## 8. Constraints
Not reported in the abstract.

## 9. Experimental Setup
"Emulated and real network conditions"; Linux kernel implementation. Specific emulator,
hardware and link configurations: not reported in the abstract, and the full text was not
obtainable.

## 10. Baselines
Not named in the abstract (it claims to outperform "the state-of-the-art schedulers").

## 11. Metrics
Not reported in the abstract.

## 12. Results
**Qualitative only**: "ReLeS significantly outperforms the state-of-the-art schedulers." No
numbers are available from any retrievable source.

## 13. Limitations
Beyond the paywall: the asynchronous-training design raises an unaddressed question (how
does a policy trained on stale experience behave when path characteristics change?), and
there is no network-level objective.

## 14. Reproducibility
**Weak — and this is itself a finding.** Unpaywall reports closed access; no arXiv preprint
exists; author and lab pages list the citation without a PDF; IEEE Xplore blocked retrieval.
The most-cited "DRL scheduler for MPTCP" cannot be reproduced or quantitatively compared
from open sources.

## 15. Relevance to my PhD
ReLeS is the canonical citation for learning-based multipath scheduling, which makes its
opacity a **reproducibility gap I can exploit**: a fully open, reproducible DRL/LLM
scheduler with published state/action/reward, code and traces would be a genuine
contribution independent of any performance claim.

---

# PAPER 29 — Peekaboo: Learning-Based Multipath Scheduling for Dynamic Heterogeneous Environments (IEEE JSAC 2020)

## 1. Problem
Path characteristics change over time (mobility, congestion, interference); a scheduler
tuned offline for one environment degrades in another.

## 2. Architecture
Sender-side MPTCP scheduler with an online learning component.

## 3. Network
Heterogeneous wireless; endpoint transport.

## 4. Inputs
Per-path state including RTT, delivery rate, congestion window and buffer estimates.

## 5. Decision
Packet-to-subflow assignment learned from observed path behaviour.

## 6. Algorithm
A learning-based scheduler that adapts online, rather than a fixed heuristic.

## 7. Objective
Maximise goodput/latency performance under changing path conditions.

## 8. Constraints
In-order delivery; receive buffer.

## 9. Experimental Setup
Linux MPTCP testbed with emulated dynamic heterogeneous paths. Exact parameters: not
verified from the free record.

## 10. Baselines
Default MPTCP scheduler, BLEST, ECF and other heuristics.

## 11. Metrics
Goodput, latency, reordering, adaptation speed.

## 12. Results
Reports improved performance over heuristic schedulers when path characteristics change.
Exact figures: not verified from the free record.

## 13. Limitations
Learns a scheduling policy but has **no interface to network-level objectives**; evaluation
remains transport-level.

## 14. Reproducibility
Moderate — the paper reports an implementation, but no public artifact was identified in
this session.

## 15. Relevance to my PhD
The closest classical work to "learning scheduler", and therefore the sharpest illustration
of the gap I am targeting: the scheduler learns, but it learns **its own** objective. Nobody
tells it what the network wants.

---

# PAPER 30 — An Improved MPQUIC Scheduler Based on Multi-Agent Reinforcement Learning (IEICE Trans. Inf. Syst. 2025)

## 1. Problem
MPQUIC performance on heterogeneous paths depends heavily on the scheduler; can multiple
learned agents schedule better than heuristics?

## 2. Architecture
Sender-side MPQUIC scheduler with multiple RL agents.

## 3. Network
5G/general heterogeneous paths; endpoint transport.

## 4. Inputs / 5. Decision / 6. Algorithm
Not verified — retrieved at metadata level (IEICE Transactions on Information and Systems,
DOI not resolved in this session). The decision is packet-to-path assignment produced by a
multi-agent RL policy.

## 7. Objective
Improve MPQUIC performance on heterogeneous paths.

## 8. Constraints
Not verified.

## 9. Experimental Setup
Not verified.

## 10–12. Baselines, metrics, results
Not verified.

## 13. Limitations
Multi-agent RL adds coordination complexity; as with the other MPQUIC schedulers, there is
no network-level objective.

## 14. Reproducibility
Not verified.

## 15. Relevance to my PhD
Evidence that multi-agent RL has reached MPQUIC scheduling, which matters for my design
choice: if the transport layer already hosts multiple agents, then the higher-level
orchestrator agent must have a well-defined *authority boundary* with them rather than
issuing raw scheduling decisions.

---

# PAPER 31 — Deep Reinforcement Learning for Access Traffic Splitting in 5G Core System (IEEE 2024)

## 1. Problem
In 5G ATSSS, the split of traffic across 3GPP and non-3GPP access must be decided
dynamically; how can DRL make that decision in the core?

## 2. Architecture
ATSSS decision function in the 5G core; DRL agent produces the split ratio per flow.

## 3. Network
**5G core** (this is the key feature — the multipath decision lives in the network, not in
the endpoint transport).

## 4. Inputs / 5. Decision
Per-flow access traffic split ratio, based on per-access path state (retrieved at metadata
level; details not verified).

## 6. Algorithm
Deep reinforcement learning.

## 7. Objective
Improve aggregate performance/QoS across accesses.

## 8. Constraints
Access availability and policy constraints.

## 9. Experimental Setup
Not verified (metadata-level retrieval; IEEE Xplore document 10826899).

## 10–12. Baselines, metrics, results
Not verified.

## 13. Limitations
Not verified from the free record; the general limitation of this line is that the DRL
objective is local to the split decision.

## 14. Reproducibility
Not verified.

## 15. Relevance to my PhD
**This is the multipath/5G-core intersection**: multipath decisions executed inside the core
by a learned policy. It is the natural place where an orchestrator could supply objectives,
and where slice/SLA awareness would be added — which the paper does not do.

---

# PAPER 32 — Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective RL (IEEE 2025)

## 1. Problem
Access traffic splitting should balance service quality against business return on
investment, not just technical performance.

## 2. Architecture
ATSSS-style decision function in the 5G core driven by multi-objective RL.

## 3. Network
5G core.

## 4. Inputs / 5. Decision
Per-flow access traffic split, evaluated against both QoS and ROI objectives.

## 6. Algorithm
Multi-objective reinforcement learning.

## 7. Objective
Pareto-style balance between QoS and return on investment.

## 8. Constraints
QoS requirements; cost/ROI considerations.

## 9. Experimental Setup
Not verified (metadata-level retrieval; IEEE Xplore document 11133925).

## 10–12. Baselines, metrics, results
Not verified.

## 13. Limitations
Not verified from the free record.

## 14. Reproducibility
Not verified.

## 15. Relevance to my PhD
Important because it is one of very few papers to bring a **business objective** into a
network decision function. That is conceptually close to SLA/business-aware orchestration —
and it is still done without an orchestrator or an LLM in the loop, which is precisely the
combination I propose to study.

---

# PAPER 33 — Tokens, Not Packets: Rethinking the Multipath QUIC Scheduling Interface (ACM Applied Networking Research Workshop 2026)

## 1. Problem
MPQUIC's packet-based scheduling interface constrains what schedulers can express; richer,
flow-level information is needed to schedule well.

## 2. Architecture
Sender-side MPQUIC scheduling interface redesign.

## 3. Network
General/heterogeneous paths; endpoint transport.

## 4. Inputs
The paper's argument is that the interface, not the policy, is the bottleneck.

## 5. Decision
Interface redesign: expose token-based, flow-aware scheduling opportunities instead of raw
per-packet decisions.

## 6. Algorithm
Interface design plus measurement of existing schedulers under the current interface.

## 7. Objective
Enable schedulers to make better-informed, flow-level decisions.

## 8. Constraints
Backwards compatibility with existing MPQUIC implementations.

## 9. Experimental Setup
Measurement study on real MPQUIC implementations.

## 10–12. Baselines, metrics, results
Not verified from the free record beyond the interface argument.

## 13. Limitations
Interface/measurement contribution rather than a new scheduler; very recent.

## 14. Reproducibility
Not verified in this session.

## 15. Relevance to my PhD
**Directly relevant to my proposed architecture.** If I want an orchestrator or an LLM agent
to influence multipath scheduling by expressing network-level objectives, the scheduler
interface must be able to carry that information. This paper is the argument that the
interface is currently too narrow — which supports framing part of my contribution as an
*objective-passing interface* between orchestration and scheduling.

---

# E. LLM / AGENTIC NETWORK MANAGEMENT AND BENCHMARKS

# PAPER 34 — NetConfEval: Can LLMs Facilitate Network Configuration? (ACM CoNEXT / PACMNET 2024)

## 1. Problem
Can LLMs make network configuration more human-friendly and less error-prone, and how
should that be measured?

## 2. Architecture
An offline benchmark suite covering four configuration scenarios: synthesising
configurations from requirements, translating configurations across vendors, specifying
routing algorithms, and configuration repair.

## 3. Network
IP/enterprise network configuration (device configuration and routing).

## 4. Inputs
Natural-language and structured configuration requirements.

## 5. Decision
Generated configuration artefacts.

## 6. Algorithm
Prompting-based generation by multiple LLMs (no agent loop, no execution).

## 7. Objective
Maximise configuration correctness against reference configurations.

## 8. Constraints
Correctness with respect to the reference artefacts.

## 9. Experimental Setup
Offline benchmark; public dataset released on HuggingFace.

## 10. Baselines
Human-written/gold configurations; other LLMs.

## 11. Metrics
Configuration correctness per scenario; task accuracy; partial token-cost reporting.

## 12. Results
Establishes which LLMs can produce usable configurations and where they fail. The key
structural result for my purposes is methodological: **it is possible to build a rigorous,
public, reproducible benchmark for an LLM networking task.**

## 13. Limitations
Static and text-level: correctness is judged against reference configurations rather than by
deploying them, so there is no network behaviour, no service KPI and no closed loop.

## 14. Reproducibility
Strong — public code and public dataset.

## 15. Relevance to my PhD
The template for the benchmark I would build, and evidence that the *configuration* half of
network management is already benchmarked. My contribution must therefore be on the
*outcome* half: deploy the configuration and measure what happens to the service.

---

# PAPER 35 — NIKA: A Network Arena for Benchmarking AI Agents on Network Troubleshooting (arXiv preprint 2025)

## 1. Problem
There is no standard, accessible benchmark for evaluating LLM agents on dynamic network
troubleshooting at low operational effort.

## 2. Architecture
Two components: a **benchmark suite** of curated incidents, and an **orchestration platform**
that connects an agent to a network environment. Incidents are formalised as
`(network scenario, network issue, traffic workload)`, where the issue is
`(device, component, root cause)`. An Agent Access Layer exposes the network via MCP.

## 3. Network
Data centre, campus, ISP and enterprise IP networks — five scenarios, four instantiable at
different topology sizes.

## 4. Inputs
A high-level symptom description; tool outputs (telemetry, probing results).

## 5. Decision
Which telemetry to inspect, which probes to run, and the final diagnosis.

## 6. Algorithm
ReAct-style reasoning agent: reason, call a tool, incorporate the result, repeat.

## 7. Objective
Detect, localise and identify the root cause of the incident.

## 8. Constraints
Access policies restrict which nodes and tools an agent may touch.

## 9. Experimental Setup
**Hundreds of curated incidents over five scenarios covering 54 representative network
issues, yielding 640 distinct troubleshooting incidents**; more than **30 monitoring and
troubleshooting tools** exposed via MCP (sketches, in-band network telemetry, SDN controller
APIs, switch CLIs); three models evaluated (GPT-OSS, GPT-5, GPT-5-mini).

## 10. Baselines
Cross-model comparison; no non-LLM diagnostic baseline reported.

## 11. Metrics
Detection success, fault-localisation accuracy, root-cause identification accuracy, time to
detection, and reasoning-trajectory analysis (tool-usage patterns).

## 12. Results
Larger models are more successful at **detecting** network issues, but they still struggle
to **localise faults and identify root causes**.

## 13. Limitations
Preprint; scenarios are IP/data-centre/campus/ISP — **no 5G core, no RAN, no slices**; scores
diagnosis rather than service outcomes; no token-cost metric.

## 14. Reproducibility
Strong — open-source framework and a public dataset (Zenodo DOI 10.5281/zenodo.17971675) with
more than 900 reasoning traces.

## 15. Relevance to my PhD
Proves that an executable, curated network-agent benchmark is feasible *and* simultaneously
demonstrates the gap: replace "IP incident" with "5G/6G service-degradation incident" and
add SLA-level scoring, and you have a contribution that does not duplicate NIKA.

---

# PAPER 36 — NetArena: Dynamic Benchmarks for AI Agents in Network Automation (ICLR 2026)

## 1. Problem
Static benchmarks are contaminated by pretraining and lack statistical power; how should
network-automation agents be evaluated credibly?

## 2. Architecture
Dynamically generated network scenarios with an agent-with-tools interface over an emulated
network.

## 3. Network
IP/enterprise/data-centre network automation.

## 4. Inputs
Scenario specification and live emulated network state.

## 5. Decision
Configuration, diagnosis or planning actions depending on the task.

## 6. Algorithm
Agent frameworks driving tools; multiple LLM backbones compared.

## 7. Objective
Task correctness, with safety considered separately from correctness.

## 8. Constraints
Step-wise safety is scored, so unsafe intermediate actions are penalised even if the final
answer is correct.

## 9. Experimental Setup
Runtime-generated tasks; the paper reports addressing statistical power and pretraining
contamination explicitly (confidence-interval overlap reduced from 85% to 0).

## 10. Baselines
Multiple LLM agents.

## 11. Metrics
Task correctness, step-wise safety, latency, plus contamination and statistical-power
analysis.

## 12. Results
Demonstrates that dynamic generation is necessary to distinguish agent designs; static
benchmarks overstate differences.

## 13. Limitations
IP/enterprise/datacentre scenarios; the authors concede limited coverage of complex
cross-domain scenarios; no 5G core/RAN/slicing and no SLA-level outcome scoring.

## 14. Reproducibility
Strong — public code repository.

## 15. Relevance to my PhD
**The methodological standard my benchmark must meet.** Any 5G/6G management benchmark I
build in 2026 will be criticised as contamination-prone unless the tasks are dynamically
generated, and unless safety is decoupled from correctness.

---

# PAPER 37 — OperAID: Benchmarking LLM Agents for Autonomous Kubernetes Fault Remediation on a 5G Core (IEEE NetSoft 2026)

## 1. Problem
Can an LLM agent autonomously operate a cloud-native 5G core — diagnosing faults and
remediating them — and how should that be evaluated?

## 2. Architecture
An open-source testbed running **Open5GS + UERANSIM on Kubernetes**, with an agentic loop:
fault injection → agentic diagnosis → remediation → execution-based verification.

## 3. Network
5G core, cloud-native (Kubernetes), no RAN.

## 4. Inputs
Kubernetes and 5G-core operational state (pods, services, configuration).

## 5. Decision
Remediation actions (fixing NetworkPolicy rules, restoring ConfigMaps, scaling deployments).

## 6. Algorithm
Agentic diagnosis-then-remediation with verification, over an operational toolset.

## 7. Objective
Restore correct operation of the 5G core deployment.

## 8. Constraints
The agent's actions are real changes to a running deployment.

## 9. Experimental Setup
Three scenarios: a NetworkPolicy blocking the AMF–SMF SBI interface (port 7777), a missing
SMF ConfigMap causing CrashLoopBackOff, and the UPF scaled to zero. **900 experiments** (5
models × 2 tool conditions × 3 scenarios × 30 runs).

## 10. Baselines
The same agent without tools (7.1% success) and cross-model comparison.

## 11. Metrics
Remediation success rate; per-run cost.

## 12. Results
**Overall 36.0% success; 70.7% with tools versus 7.1% without; best model (Qwen3.5-35B-A3B)
93.3%.** Tool access dominates model choice in importance for this task.

## 13. Limitations
**The faults are Kubernetes-level, not 3GPP protocol-level** — no NAS/NGAP/PFCP/SBI
semantics are exercised, no RAN, and no SLA/service KPI is scored. Venue reporting is
inconsistent between the repository BibTeX and Crossref.

## 14. Reproducibility
Strong — public repository including the Open5GS/UERANSIM Helm charts and scenarios.

## 15. Relevance to my PhD
**This paper defines the boundary of the state of the art precisely.** Infrastructure-level
remediation on a 5G core is now benchmarked; *3GPP-level* management with *service-level*
outcomes is not. That sentence is the gap statement for my benchmark contribution.

---

# PAPER 38 — TeleQnA: A Benchmark Dataset to Assess LLMs' Telecommunications Knowledge (IEEE Network 2026)

## 1. Problem
There is no standard way to measure how much telecommunications knowledge an LLM has.

## 2. Architecture
A multiple-choice question benchmark generated from standards and research literature.

## 3. Network
Telecommunications knowledge generally (not a management task).

## 4. Inputs
Questions; 5. Decision: an answer choice; 6. Algorithm: zero-shot/few-shot QA.

## 7. Objective
Measure telecom knowledge.

## 8. Constraints
Multiple-choice format.

## 9. Experimental Setup
10,000 telecom multiple-choice questions; multiple LLMs evaluated against human experts.

## 10. Baselines
Cross-model comparison and human expert performance.

## 11. Metrics
Answer accuracy.

## 12. Results
Establishes that even strong general models fail a substantial fraction of
specification-related questions.

## 13. Limitations
Static, contamination-prone, knowledge-only; no tool use, no actuation, no network KPI.
Later work (Free-Text Evaluation of LLMs for 5G) argues that MCQ scores overstate
telecom-LLM capability because the format leaks answer cues.

## 14. Reproducibility
Strong — public dataset and code.

## 15. Relevance to my PhD
Shows the **knowledge** benchmark space is crowded and mature. This is why my benchmark
contribution must be about *agents that manage the network*, not about telecom question
answering.

---

# PAPER 39 — TeleCom-Bench: Benchmarking LLMs on Live-Network Operator Agent Trajectories (ACM KDD 2026)

## 1. Problem
How well can LLMs perform the actual procedural work of telecom network operations?

## 2. Architecture
A benchmark built from **authentic live-network operator agent trajectories**, covering six
tasks: intent recognition, entity extraction, event verification, tool invocation,
root-cause analysis and solution generation.

## 3. Network
Production telecom network operations.

## 4. Inputs
Operator-style task descriptions and trajectory context.

## 5. Decision
Per-task outputs, including tool invocations and remediation solutions.

## 6. Algorithm
Task-specific LLM evaluation (22,678 samples).

## 7. Objective
Measure procedural capability, not just language understanding.

## 8. Constraints
Grounded in real operator workflows.

## 9. Experimental Setup
22,678 samples from live-network operator agent trajectories; eight state-of-the-art LLMs
evaluated.

## 10. Baselines
Cross-model comparison.

## 11. Metrics
Per-task accuracy.

## 12. Results
**A "universal Execution Wall": roughly 90% accuracy on linguistic interface tasks versus
roughly 30% on procedural execution tasks.**

## 13. Limitations
Task-level correctness rather than resulting network service quality; dataset is partially
closed (operator-derived).

## 14. Reproducibility
Moderate–strong — public code repository.

## 15. Relevance to my PhD
**This is third-party, independently published confirmation of the gap I am targeting.**
LLMs can talk about network operations far better than they can perform them. Any PhD
proposal in this space can cite this as evidence that the problem is real and measured, not
speculative.

---

# PAPER 40 — Mobile-LLaMA: Instruction Fine-Tuning an Open-Source LLM for Network Analysis in 5G Networks (IEEE Network 2024)

## 1. Problem
General-purpose LLMs are not specialised for 5G network-analysis tasks; can a small
open-source model be fine-tuned to do better?

## 2. Architecture
An instruction-tuned LLaMA-2 13B used for 5G network-analysis code generation (packet
analysis, IP routing, performance analysis).

## 3. Network
5G network analysis (offline analysis of network data, aligned with NWDAF-style tasks).

## 4. Inputs
Natural-language analysis requests plus network data context.

## 5. Decision
Generated analysis code.

## 6. Algorithm
Full instruction fine-tuning (SFT) on 15,111 instruction sets, built from a small
hand-written seed set expanded by self-instruct generation using OpenAI models.

## 7. Objective
Maximise correctness of generated network-analysis code.

## 8. Constraints
Correctness against a 300-point rubric.

## 9. Experimental Setup
15,111 instruction sets (packet analysis: 20 manual + 2,000 self-instruct; IP routing: 100 +
10,000; performance analysis: 30 + 3,000). Training hardware: not reported.

## 10. Baselines
GPT-3.5.

## 11. Metrics
A 300-point code-generation score.

## 12. Results
**247/300 for the fine-tuned 13B model versus 209/300 for GPT-3.5.**

## 13. Limitations
A single code-generation rubric; **no network KPI and no closed-loop performance**; the task
is analysis-code generation rather than online control; training hardware and inference
latency are not reported.

## 14. Reproducibility
Moderate–strong — public repository with data and model.

## 15. Relevance to my PhD
The canonical citation for "fine-tuning an LLM for 5G", and the clearest example of the
limitation I intend to attack: the evaluation is a text rubric, not a network outcome. It
answers "does fine-tuning improve analysis quality?" with yes, and leaves "does fine-tuning
improve *network management decisions*?" completely open.

---

# PAPER 41 — NetIntent: Leveraging LLMs for End-to-End Intent-Based Networking (IEEE OJ-COMS 2025)

## 1. Problem
Can LLMs translate operator intents into network flows and detect conflicts, across
real controller interfaces?

## 2. Architecture
An LLM intent pipeline with a conflict-detection component, integrated with **OpenDaylight
and ONOS** SDN controllers; introduces the **IBNBench** benchmark within the paper.

## 3. Network
Intent-based networking over SDN controllers.

## 4. Inputs
Natural-language intents.

## 5. Decision
Flow rules deployed via the controllers, plus conflict verdicts.

## 6. Algorithm
**No fine-tuning** — in-context/few-shot learning with dynamic example selection (maximal
marginal relevance), over **33 open-source LLMs from 1.1B to 70B parameters**.

## 7. Objective
Maximise intent-translation correctness and conflict-detection quality.

## 8. Constraints
Controller API semantics; benchmark ground truth.

## 9. Experimental Setup
IBNBench: Intent2Flow-ODL (52 pairs), Intent2Flow-ONOS (50 pairs), FlowConflict-ODL and
FlowConflict-ONOS datasets; inference on a Threadripper PRO workstation, no training.

## 10. Baselines
Cross-model comparison across 33 models.

## 11. Metrics
Intent-translation accuracy; conflict-detection performance; per-model runtime.

## 12. Results
Mid-sized models reach up to 95–99% on formal specification tasks with lower latency; and
critically, **model size does not predict quality** — a 22B model beat a 35B model, and 70B
models were marginal and memory-limited.

## 13. Limitations
Translation and conflict detection are evaluated, but the **network outcome of installing
the intent is not scored**; conflict detection ran on a small positive set; no SLA metric.

## 14. Reproducibility
Moderate — benchmark described; artifacts not confirmed public in this session.

## 15. Relevance to my PhD
Two things matter here. First, controller-level execution shows the execution path exists.
Second, **the 33-model study is direct evidence for the "small language model" hypothesis**:
if a 7B–22B model matches a 70B model on intent translation, then a distilled, low-latency
network model is a viable research direction rather than a compromise.

---

# F. MODEL EFFICIENCY: FINE-TUNING, DISTILLATION, COMPRESSION

# PAPER 42 — TelecomGPT (IEEE TMLCN 2025)

## 1. Problem
General LLMs lack telecom-specific knowledge; how should a telecom LLM be built, and does it
beat general models?

## 2. Architecture
A three-stage adaptation recipe: continual pre-training (causal LM) → instruction tuning
(SFT) → alignment tuning via DPO, trained on purpose-built corpora.

## 3. Network
Telecommunications (knowledge, maths and code tasks — **not network management**).

## 4. Inputs
Telecom text, instructions and preference pairs.

## 5. Decision
Text/code outputs.

## 6. Algorithm
Three-stage domain adaptation, including DPO alignment.

## 7. Objective
Maximise telecom task performance.

## 8. Constraints
Hardware limits (the paper cites them as the reason for its model-scale choice).

## 9. Experimental Setup
OpenTelecom (1,679.5M training tokens), TelecomInstruct, TelecomAlign; instruct-tuning took
about **1.5 hours on one 8-GPU node**; three benchmarks are defined (Telecom Math Modelling,
Telecom Open QnA, Telecom Code Tasks).

## 10. Baselines
GPT-4, Llama-3, Mistral.

## 11. Metrics
Task accuracy, including 3GPP technical-document classification.

## 12. Results
**Substantially outperforms GPT-4, Llama-3 and Mistral on Telecom Math Modelling, and
reaches 75.30 versus GPT-4o's 38.94 on 3GPP tdoc classification**, with comparable
performance on TeleQnA.

## 13. Limitations
**Every benchmark measures telecom knowledge or text/code generation — none touches a
network.** The paper itself notes GPT-4o still leads on standard TeleQnA, so the advantage
is domain- and task-specific.

## 14. Reproducibility
Moderate–strong — corpora and recipe documented.

## 15. Relevance to my PhD
The best-documented domain-adaptation recipe available, and the source of the concretely
useful cost figure (~1.5 h on 8 GPUs). Its decisive gap is my research question: the paper
never measures whether the adapted model makes better *network* decisions.

---

# PAPER 43 — Tele-LLMs: A Series of Specialized LLMs for Telecommunications (IEEE Access 2026)

## 1. Problem
Build a family of small telecom-specialised models and test whether parameter-efficient
adaptation is sufficient.

## 2. Architecture
Small open backbones (1B–8B) continually pre-trained and fine-tuned on a purpose-built
telecom corpus, with a companion evaluation suite.

## 3. Network
Telecommunications knowledge and QA.

## 4. Inputs
Telecom corpora (arXiv papers, 3GPP standards) and evaluation questions.

## 5. Decision
Text answers.

## 6. Algorithm
**Continual pre-training with full fine-tuning.** Notably, **LoRA was tested and rejected**:
the authors report that LoRA "quickly saturates" and that gradient norms remained extremely
low on LLaMA-3-8B, so full fine-tuning was required.

## 7. Objective
Maximise telecom evaluation performance.

## 8. Constraints
Compute budget.

## 9. Experimental Setup
Tele-Data (about 90k arXiv papers / 4 GB / 1.08B tokens; 2.8k 3GPP documents) and Tele-Eval;
training used **8 × NVIDIA A6000** (about 5,000 GPU-hours).

## 10. Baselines
The unadapted base models.

## 11. Metrics
LLM-Eval and task accuracy; average relative improvement of about **25% on Tele-Eval** (e.g.
Gemma-2B 13.59 → 17.07).

## 12. Results
Specialisation gives large relative gains at small model sizes, and full fine-tuning
outperforms LoRA for this purpose.

## 13. Limitations
Evaluation is telecom QA/knowledge, not network management; **the LoRA-rejection result
contradicts the common assumption in network-domain papers that LoRA is sufficient**.

## 14. Reproducibility
Strong — public models, data and evaluation code.

## 15. Relevance to my PhD
Two concrete, citable findings for my proposal: (i) small (1B–8B) domain models are viable,
which matters for inference-latency-constrained network control; (ii) **the adaptation
method itself is an open question** — LoRA saturating on small models versus full
fine-tuning working is exactly the kind of trade-off my Area-5 question asks about, and no
paper has measured it against network-decision quality.

---

# PAPER 44 — ORANSight-2.0: Foundational LLMs for O-RAN (IEEE TMLCN 2025)

## 1. Problem
Can open foundational LLMs be specialised for O-RAN, and at what hardware cost?

## 2. Architecture
Fine-tuned LLM family for O-RAN, plus the **RANSTRUCT** instruction dataset and the
**srsRANBench** code benchmark.

## 3. Network
O-RAN (RAN specifications and srsRAN codebase).

## 4. Inputs
O-RAN specification text and srsRAN code.

## 5. Decision
Answers and generated code.

## 6. Algorithm
**QLoRA 4-bit fine-tuning** across model sizes up to 70B.

## 7. Objective
Maximise O-RAN QA and code-generation performance.

## 8. Constraints
Single-GPU memory budget.

## 9. Experimental Setup
**151,500 O-RAN instruction pairs (RANSTRUCT); fine-tuned models up to 70B on a single 24 GB
consumer RTX 4090 for one epoch**; srsRANBench evaluates 18 LLMs (1B–70B) on srsRAN code
generation and codebase understanding.

## 10. Baselines
Base models and prior O-RAN benchmarks (ORAN-Bench-13K, 13,952 MCQs from 116 O-RAN specs).

## 11. Metrics
Accuracy (macro accuracy up to 0.784 for the RAG variant) and code-generation quality.

## 12. Results
Demonstrates that **QLoRA makes 70B-class O-RAN specialisation feasible on a single consumer
GPU**, which is a much lower hardware floor than the field generally assumes.

## 13. Limitations
RAN knowledge and code, not network control; no network KPI and no closed loop.

## 14. Reproducibility
Strong — public dataset and code (ORAN-Bench-13K repository, HuggingFace dataset).

## 15. Relevance to my PhD
Directly answers the practical feasibility question in my Area 5: **a PhD student can
fine-tune an O-RAN-specialised model on one 24 GB GPU.** That removes the hardware objection
to including fine-tuning in my experimental plan.

---

# PAPER 45 — MERLOT: A Distilled LLM-Based Mixture-of-Experts Framework for Scalable Encrypted Traffic Classification (IEEE Globecom Workshops 2025)

## 1. Problem
LLM-based traffic classifiers are too large and slow for deployment; can distillation
preserve accuracy at a fraction of the cost?

## 2. Architecture
A distilled mixture-of-experts classifier with a GPT-2-base backbone.

## 3. Network
Encrypted traffic classification.

## 4. Inputs
Packet/flow features.

## 5. Decision
Traffic class label.

## 6. Algorithm
**Knowledge distillation** with a composite loss (cross-entropy against hard labels plus KL
divergence against the teacher's soft outputs), combined with mixture-of-experts routing.

## 7. Objective
Match teacher accuracy at much lower inference cost.

## 8. Constraints
Latency and memory budget for deployment.

## 9. Experimental Setup
Ten encrypted traffic datasets totalling about 527,600 samples (APP-53 2023, CSIC 2010,
CSTNET 2023, CW-100 2018, ISCX Tor/VPN, and others).

## 10. Baselines
**TrafficLLM (7B)** and **ET-BERT**.

## 11. Metrics
F1 per dataset; inference time; memory usage.

## 12. Results
MERLOT (660M) matches or beats a 7B model on most datasets (e.g. ISCX Tor 2016: 0.9845 vs
0.9810 vs ET-BERT 0.9368) while consuming **85–90% less inference time and memory**. Note:
the paper's parameter accounting is internally inconsistent ("600M" vs "0.66B" vs a "935M"
gating network), which is reported verbatim here rather than resolved.

## 13. Limitations
Classification, not control; evaluation is on traffic-classification F1 rather than network
behaviour.

## 14. Reproducibility
Moderate — method well specified; public artifact not confirmed in this session.

## 15. Relevance to my PhD
The strongest evidence in the corpus that **a distilled model can match a 7B model on a
networking task at ~10% of the cost**. My Area-5 question is whether the same holds for
*decision* quality, which nobody has measured.

---

# PAPER 46 — Toward 6G Edge Intelligence: Lightweight LLMs for Intent-Driven Network Management (IEEE TMC 2026)

## 1. Problem
LLM-based intent management is too heavy to run at the edge; can knowledge distillation
plus a knowledge graph produce a lightweight model with adequate accuracy?

## 2. Architecture
A two-phase pipeline: fine-tune the LLM with knowledge-graph guidance in the cloud, then
distil into a lightweight model deployed at the edge.

## 3. Network
6G edge, intent-driven network management.

## 4. Inputs
Application intents (APPIs) mapped to network configurations.

## 5. Decision
Intent-to-configuration mapping.

## 6. Algorithm
**Knowledge distillation combined with a knowledge graph.**

## 7. Objective
Match teacher accuracy at edge-feasible latency.

## 8. Constraints
Edge compute and latency budget.

## 9. Experimental Setup
KG-derived structured intent training dataset; cloud fine-tuning then edge deployment.
Dataset size and GPU type: not reported in the retrievable source.

## 10. Baselines
DeepSeek and Qwen models.

## 11. Metrics
Accuracy; inference latency.

## 12. Results
**95% accuracy for APPI understanding, surpassing DeepSeek and Qwen by an average of 8
points, with a 60% reduction in inference latency** relative to the undistilled model.

## 13. Limitations
Intent understanding is measured, not the resulting network behaviour; dataset scale and
hardware are not reported, which limits reproducibility.

## 14. Reproducibility
Weak–moderate — key experimental details are not reported in the retrievable source.

## 15. Relevance to my PhD
Combines distillation with the network-management task directly, which is exactly my Area 5
question — and its measured 60% latency reduction is the kind of number that makes edge
deployment of a network agent plausible. Its gap: accuracy is measured on understanding,
not on SLA outcomes.

---

# PAPER 47 — Toward Autonomous O-RAN: A Multi-Scale Agentic AI Framework (arXiv preprint 2026)

## 1. Problem
Which model belongs in which O-RAN control loop, given that non-RT, near-RT and real-time
loops have latency budgets spanning four orders of magnitude?

## 2. Architecture
A **multi-scale** deployment: an LLM (Nvidia Nemotron) as the non-RT rApp, a small language
model (GPT-OSS) as the near-RT xApp, and a tiny on-device model on a Jetson for the real-time
loop — with the LLM supervising the SLM.

## 3. Network
O-RAN on a live 5G testbed based on **srsRAN** with four active slices; E2SM-KPM telemetry
at 5-second granularity.

## 4. Inputs
E2SM-KPM telemetry and slice state.

## 5. Decision
Slice resource allocation; promotion of a slice to VIP status.

## 6. Algorithm
Hierarchical, multi-scale agentic control: **model-size-tiered deployment rather than
compression**.

## 7. Objective
Improve VIP slice throughput while preserving latency for other slices.

## 8. Constraints
Hard per-loop latency budgets (real-time sub-millisecond, near-RT 10 ms–1 s, non-RT > 1 s).

## 9. Experimental Setup
Live srsRAN testbed with four slices; LLM on an H200, SLM on an RTX 5090, tiny model on a
Jetson Xavier NX.

## 10. Baselines
SLM-only control (without LLM supervision).

## 11. Metrics
Measured latency per tier: **0.847 ± 0.04 ms for the real-time tiny model, 793 ms for the
near-RT SLM**; VIP throughput and latency.

## 12. Results
Agentic (SLM + LLM supervision) versus SLM-only: **average VIP throughput +6% after
promoting a slice to VIP, while preserving an average 22 ms latency** for the lower-priority
slice.

## 13. Limitations
Preprint; the gains are modest; the architecture requires three tiers of hardware.

## 14. Reproducibility
Moderate — testbed described (srsRAN-based); artifacts not confirmed public.

## 15. Relevance to my PhD
**The most practically important measurement in this review for my architecture design.** It
demonstrates empirically what the RIC latency budget implies: an LLM cannot sit in the
near-RT or real-time loop (793 ms for the SLM, 0.847 ms for the tiny model), so **the only
viable LLM placement is the non-RT/SMO tier, with smaller distilled models and classical
controllers below it.** That finding directly shapes the tiered architecture I propose.

---

# PAPER 48 — SQLLM: A Secure and Quantized Framework for LLMs in 5G Private Network Operations (IEEE TCE 2026)

## 1. Problem
Deploy LLMs for 5G private-network operations under memory and latency constraints, while
also defending against malicious user queries.

## 2. Architecture
An LLM-based operations assistant for 5G private networks with security filtering.

## 3. Network
5G private network operations and maintenance.

## 4. Inputs
User queries about network operations (including adversarial ones).

## 5. Decision
Classification of queries into normal and three attack categories.

## 6. Algorithm
**LoRA fine-tuning combined with static post-training quantisation**, with two innovations:
a dynamic smoothing factor α that migrates outlier variance from activations to weights, and
hybrid per-tensor/per-token quantisation granularity, both motivated by the way activation
outliers in 5G O&M data degrade low-bit inference.

## 7. Objective
Maintain accuracy, VRAM consumption and inference time under quantisation while rejecting
malicious queries.

## 8. Constraints
VRAM and latency budget of private-network deployment.

## 9. Experimental Setup
**Not retrievable** — the full text is paywalled, and no source reached in this session
discloses the base model, dataset, hardware or numerical results.

## 10. Baselines
The abstract contrasts against "traditional static quantization that uses fixed parameters
and uniform granularity".

## 11. Metrics
Accuracy, VRAM consumption, inference time (all evaluated per the abstract).

## 12. Results
Only a qualitative claim of "excellent performance on all test indicators" is retrievable.
**No numbers.**

## 13. Limitations
Beyond the paywall, the task is query classification for security rather than network
control.

## 14. Reproducibility
**Weak — this is the largest single verification gap in Area 5.** No model identity, dataset,
hardware, compression ratio or accuracy figure is available from open sources.

## 15. Relevance to my PhD
It is the clearest example of quantisation applied to an LLM *for 5G operations*, which is
squarely in my Area 5 target — and it is unverifiable, which is itself a finding: the
quantisation-for-network-management evidence base is thin and often unreadable. Obtaining
institutional access to this paper is one of my first concrete next steps.

---

# PAPER 49 — A Survey on Model Compression for Large Language Models (TACL 2024)

## 1. Problem
Organise the methods for compressing LLMs.

## 2. Architecture
Not applicable — taxonomy of quantisation, pruning, distillation and other compression
families.

## 3. Network
None (generic NLP/ML).

## 4–8. Inputs / decisions / algorithm / objective / constraints
Not applicable.

## 9. Experimental Setup
None.

## 10–12. Baselines / metrics / results
None of its own.

## 13. Limitations
Generic; no networking content.

## 14. Reproducibility
Not applicable.

## 15. Relevance to my PhD
Provides the vocabulary and the taxonomy (quantisation vs pruning vs distillation vs PEFT)
that my Area 5 extraction uses. It is also the reference that lets me state clearly that
**the compression techniques are mature in NLP while their effect on network-decision
quality is unmeasured** — which is precisely the empirical hole my PhD can fill.
