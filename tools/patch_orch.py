#!/usr/bin/env python3
"""Stage 8b: apply the orchestration subagent's verified bibliographic corrections
and add the remaining Area 2 papers that were characterised in its full report.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
recs = json.load(open(os.path.join(DATA, "master_full.json")))
by = {r["paper_id"]: r for r in recs}

FIX = {
    "O10": dict(doi="10.1109/COMST.2018.2884835", year=2019,
                venue="IEEE Communications Surveys & Tutorials"),
    "O22": dict(doi="10.1109/COMST.2024.3510543", year=2025,
                venue="IEEE Communications Surveys & Tutorials"),
    "O24": dict(doi="10.1109/COMST.2025.3548039", venue="IEEE Communications Surveys & Tutorials"),
    "O02": dict(doi="10.1016/j.comnet.2019.106984", year=2020, venue="Computer Networks"),
    "O09": dict(year=2016, doi="10.1109/TNSM.2016.2569020",
                venue="IEEE Transactions on Network and Service Management"),
}

for k, v in FIX.items():
    if k in by:
        by[k].update(v)

# Full characterizations for the orchestration papers read by the subagent
C = {}

C["O02"] = dict(
    orchestrator_type="D - orchestration architecture (multi-domain slicing), survey-adjacent",
    architecture="Multi-domain network slicing orchestration: each domain runs a local orchestrator; a federation/broker layer exchanges slice requests and resource offers across administrative domains.",
    control_plane="3GPP slice management combined with ETSI NFV MANO per domain",
    centralized_or_distributed="Hierarchical (central broker over per-domain orchestrators)",
    closed_loop="No (architectural)",
    evaluation_quality="WEAK",
    limitations="Architecture paper: multi-domain federation described but not experimentally evaluated; no optimisation engine or learning component.",
    research_gap="Multi-domain federation has no standard cross-domain information exchange; the decision engine that would drive it (learning-based or LLM-based) is absent.",
)

C["O31"] = dict(
    orchestrator_type="G - survey/tutorial (defines the orchestration taxonomy used here)",
    architecture="Defines three orchestrator functional scopes: Service Orchestration (service composition, marketplace/OSS-BSS interface), Lifecycle Orchestration (workflows, dependencies, maintaining services per the contracted SLA), and Resource Orchestration (mapping service requests onto virtual/physical resources across NFVO, EMS and SDN controllers).",
    control_plane="ETSI NFV MANO is the anchor; MEF LSO, TM Forum, IETF, OASIS/TOSCA, ONF, ITU, NGMN also covered",
    interfaces="REST-dominant; TOSCA (Simple Profile in YAML v1.2, TOSCA for NFV v1.0); NETCONF/YANG; OpenFlow extensions; ETSI multi-domain reference points Umbrella NFVO and Or-Or",
    managed_resources="Compute, storage and network resources across heterogeneous infrastructures; VNFs; multi-VIM infrastructure; slices ('Slice as a Service')",
    single_or_multidomain="Both, with explicit treatment of multi-technology and multi-administrative-domain orchestration",
    closed_loop="Not formalised",
    sla_support="Yes conceptually - lifecycle orchestration maintains services per the contracted SLA; enforcement mechanism NOT REPORTED",
    cloud_native="Partly (Kubernetes and container orchestration platforms surveyed)",
    limitations="Qualitative taxonomy, snapshot pre-2020, no quantitative benchmarking, and ML/AI-driven orchestration is essentially absent from its coverage.",
    research_gap="The survey states that cross-domain information exchange 'is not a standard' and that orchestrators are largely logically centralised over softwarised infrastructure - leaving open standardised cross-domain intent exchange, closed-loop SLA enforcement with measurable guarantees, and an AI control layer above MANO.",
    evaluation_quality="NA", reproducibility_quality="WEAK",
)

C["O32"] = dict(
    orchestrator_type="D - orchestration architecture (knowledge plane) - position paper, not an implementation",
    architecture="A knowledge plane above the data and control planes, combining ML and reasoning to automate network operation; the plane observes, learns and issues decisions to the control plane.",
    control_plane="Knowledge plane above an SDN control plane",
    closed_loop="Yes conceptually",
    evaluation_platform="Prototype experiments on a small emulated network (about 12 overlay nodes, 19 underlay elements, 72 links) using OMNeT++ with Open vSwitch and Snort on an ESXi host",
    network_scale="12 overlay nodes, 19 underlay elements, 72 links",
    main_results="The learned overlay model reaches a relative error of roughly 1% with 3,000 training samples; the NFV CPU model is presented as a CDF figure without a number.",
    limitations="Vision/position paper with a small prototype; it does not solve how the knowledge plane makes safe or verifiable decisions, nor how it is governed.",
    research_gap="KDN is the conceptual ancestor of LLM/agent orchestrators; its unsolved problem - verifiable autonomous decision-making above the control plane - is exactly what current agentic orchestration still lacks.",
    evidence="FULL", evaluation_quality="MODERATE", reproducibility_quality="MODERATE",
)

C["O33"] = dict(
    orchestrator_type="F - LLM-based orchestrator (LLM planner + RL executors)",
    architecture="ARC: two-tier orchestrator. Tier 1 is a RAG-based LLM (LLaMA 3.1-8B, not fine-tuned) that sequences users and tracks the active objective; Tier 2 is a set of specialised Double Dueling Deep Q-Learning agents (one per action type, Mixture-of-Experts style). Static and Dynamic Knowledge Bases hold service specifications, objective profiles, action profiles, state history and [input, CoT, output] reasoning exemplars.",
    control_plane="Not mapped to any standard management plane (no ETSI ZSM/ONAP/OSM/O-RAN SMO named)",
    managed_resources="Compute (node MIPS), storage, link bandwidth and latency, radio channel assignment, transmit power, routing paths",
    input="Strategist commands; user service requests; semantic QoE feedback; per-(user,service,resource) state; service specifications; action profiles",
    output="Ordered user sequence plus per user: hosting node per functional block, compute and storage allocation, routing path",
    interfaces="Internal LLM prompts only",
    centralized_or_distributed="Hierarchical (one central LLM sequencer, distributed RL agents)",
    single_or_multidomain="Multi-domain (terrestrial + airborne + space)",
    closed_loop="Yes (per time slot: monitor, evaluate QoE, allocate, apply, reward, update)",
    sla_support="Semantic QoE threshold instead of a formal SLA object",
    network_slicing="No", cloud_native="NA", kubernetes="NA", oran="No",
    optimization="Hybrid: LLM reasoning + D3QL RL agents + offline mathematical solvers to bootstrap exemplars",
    agent="Yes (LLM sequencer + RL executors)",
    llm="Yes - LLaMA 3.1-8B, no fine-tuning, RAG + CoT few-shot with contrastive exemplars",
    evaluation_platform="Bespoke numerical simulation",
    network_scale="10 nodes (half non-terrestrial), 10 users, one functional block per service (2-5 MIPS), node capacity 10-100 MIPS, link latency 1-10 ms, link capacity 10-100 Mbps; topology change at iteration 30,000",
    baselines="Optimal solver solution; RU-ARC (reward-unaware); NR-ARC (no RL agents)",
    metrics="Normalised allocation cost; reward = average resource cost / allocated cost; supported user count",
    main_results="Figure-only. The text claims near-optimal cost, recovery after the iteration-30,000 transition where RU-ARC fails, and that NR-ARC fluctuates more because of LLM instability. No numerical values are stated.",
    limitations="Single small-scale simulation (10 nodes/10 users); two figures with no numbers; no external orchestrator or standard DRL/optimisation baseline; exemplar bootstrapping requires an exact solver; no SLA object, no slicing, no standard management-plane mapping, no testbed.",
    research_gap="The clearest published template for LLM-planner + RL-executor orchestration, and it exposes the open problems: quantitative benchmarking against external baselines, standard management-plane grounding, hallucination verification of planner decisions, and SLA-level scoring.",
    evaluation_quality="MODERATE", reproducibility_quality="WEAK",
)

C["O38"] = dict(
    orchestrator_type="B - optimisation/learning algorithm usable by an orchestrator (distributed DRL resource allocation)",
    architecture="Link controllers and node controllers, each with actor-critic pairs per slice class and resource type (bandwidth, compute, memory); a central training manager collects observations offline and broadcasts updated policies.",
    managed_resources="Link bandwidth, node computational capacity, node memory capacity",
    input="Per-flow demand vectors [throughput, compute, memory, delay] with Markov-modulated demand (10 states); local observations",
    output="Per-flow per-timeslot allocated resource vector",
    centralized_or_distributed="Distributed inference with centralised offline training",
    single_or_multidomain="Single domain with hierarchical slices/multiple tenants",
    closed_loop="Yes (per-timeslot reward; online training supported)",
    sla_support="Yes - a performance function F in [0,1] where 1 means the SLA is fully met (smooth concave for eMBB, step function for URLLC)",
    network_slicing="Yes (eMBB and URLLC classes over one infrastructure)",
    optimization="Advantage Actor-Critic (A2C); transfer learning across topologies; genetic algorithms rejected as an online engine",
    agent="Yes (cooperative multi-agent DRL)",
    evaluation_platform="Authors' own simulation; three topologies (Dumbbell, Triangle, Pyramid) plus a harder Pyramid+ variant",
    network_scale="2-6 flows (scalability to 9); link rate 50 Gbps; core node 60 Gbps / 60 Gb; access node 20 Gbps / 20 Gb; propagation delay 0.1 ms; eMBB demand 0.30-42.5 Gbps at 20 ms; URLLC 2.08-10 Gbps at 1 ms; training 3-5x10^4 episodes of 50 slots at T=0.1 s, 500 test episodes",
    baselines="Static allocation; empirical heuristic; cross-topology transfer variants",
    metrics="Expected system utility E[Omega]; per-resource utility; probability Omega exceeds a threshold",
    main_results="DRL keeps Omega > 0.45 in almost 50% of test episodes with a 10% gain over the empirical algorithm; the empirical algorithm reaches Omega > 0.5 in 50% of episodes versus 0.65-0.7 for DRL; DRL trained on one topology generalises to the Pyramid topology without retraining; transfer learning raises E[Omega_c] by more than 5%; in the harder Pyramid+ scenario the heuristic slightly beats DRL.",
    limitations="Static routes assumed; simulation only with 2-6 flows; no admission control; centralised observation database; numbers come from the pre-review 2021 preprint, so the published ToN version may differ.",
    research_gap="Joint routing+placement+allocation, admission control, decentralised training, hard SLA enforcement and cross-domain closed loops remain open.",
    evaluation_quality="MODERATE", reproducibility_quality="MODERATE",
)

C["O42"] = dict(
    paper_id="O42", area="orch", in_orch=True,
    title="Advanced End-to-End Intent-Driven Dynamic Network Slicing: Challenges, Solutions, and Implementation",
    venue="IEEE (IEEE Xplore document 11219256)", year=2025, doi=None, peer_reviewed=True,
    source_url="https://ieeexplore.ieee.org/abstract/document/11219256", evidence="BIB",
    orchestrator_type="D/F - intent-driven end-to-end slicing architecture with implementation",
    network_generation="5G/6G", domain="End-to-end (RAN, transport, core)",
    architecture="End-to-end intent-driven dynamic network slicing with an implementation discussion.",
    control_plane="Intent-driven management across domains",
    managed_resources="Network slices", input="Operator intents", output="Slice configuration",
    closed_loop="Intended (assurance discussed)", sla_support="Yes", network_slicing="Yes",
    limitations="Retrieved at metadata level in this session; experimental depth not verified.",
    research_gap="End-to-end intent-driven slicing is an active 2025-2026 direction; SLA-scored assurance remains the weak point.",
)

for k, v in C.items():
    if k in by:
        by[k].update(v)
    else:
        recs.append(v)
        by[k] = v

json.dump(recs, open(os.path.join(DATA, "master_full.json"), "w"), indent=1)
print("stage8b applied; total records", len(recs))
print("orchestration rows:", sum(1 for r in recs if r.get("in_orch")))
