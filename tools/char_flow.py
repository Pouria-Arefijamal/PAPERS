#!/usr/bin/env python3
"""Stage 3: attach technical characterizations to master_stage2 records.

Field semantics
---------------
Every characterization field defaults to "NA".  A field is populated only where
the fact is stated in a source that was actually retrieved in this session
(Crossref abstract, arXiv/open-access full text, or a subagent report that names
the source URL).  Bibliographic fields were verified against Crossref/OpenAlex.
"NA" therefore means "not verifiable from the sources retrieved", never
"the paper does not do this".
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

recs = json.load(open(os.path.join(DATA, "master_stage2.json")))
by = {r["paper_id"]: r for r in recs}

NA = "NA"

# =========================================================================
# AREA 1 - flow / packet / traffic scheduling
# =========================================================================
C = {}

C["F01"] = dict(
    in_flow=True,
    network_generation="4G/LTE", network_domain="RAN (cellular)",
    architecture="Centralised controller scheduling delay-tolerant traffic of IoT devices alongside real-time traffic in a cellular network",
    scheduler_location="Network-side controller (centralised)",
    problem="Scheduling delay-tolerant software updates and data backups of IoT devices in cellular networks without violating strict service guarantees of real-time applications (voice, video).",
    input_parameters="Per-device queue/backlog state and channel state; per-application delay tolerance (deadline is a constant per application, not a constraint).",
    decision_variables="Which device to schedule in each time slot, and at what rate.",
    actions="Device-and-rate selection per time slot.",
    objective="Minimise time-averaged queue backlog (delay) of delay-tolerant traffic while respecting real-time service guarantees, formulated as a Lyapunov-drift-plus-penalty problem.",
    constraints="Real-time applications must receive fixed minimum rates; stability of delay-tolerant queues.",
    algorithm="Deep reinforcement learning with a policy-gradient / actor-critic style parameterisation of the scheduling policy, trained to approximate the solution of a per-slot optimisation derived from Lyapunov drift-plus-penalty.",
    optimization_method="Lyapunov stochastic optimisation combined with DRL function approximation",
    ml_method="Deep RL (policy gradient, centralised)",
    simulator="Custom simulation of a cellular base station with IoT devices",
    testbed="NA",
    traffic_model="Delay-tolerant background traffic (software updates, backup) plus constant-rate real-time flows",
    network_scale="NA (paper studies a single base station serving many IoT devices; exact counts not verified from the retrieved record)",
    source_url="https://doi.org/10.1609/aaai.v32i1.11339",
    evidence="ABS",
    abstract_note="Scheduling is the paper's central contribution.",
)

C["F02"] = dict(
    in_flow=True,
    network_generation="5G", network_domain="RAN (radio access network slicing)",
    architecture="RAN slicing with an infrastructure provider and multiple tenants; a centralised scheduler allocates radio resource blocks across slices.",
    scheduler_location="RAN scheduler (centralised, slice-aware)",
    problem="Intelligent radio resource scheduling across 5G RAN slices so that each tenant/slice receives its contracted share while overall spectral efficiency is preserved.",
    input_parameters="Slice-level traffic demand and QoS requirements, channel quality, queue states.",
    decision_variables="Radio resource block assignment per slice (and per user within slices).",
    actions="Resource-block allocation per scheduling interval.",
    objective="Satisfy per-slice QoS/rate requirements while maximising resource utilisation.",
    constraints="Per-slice minimum/maximum rate requirements, total resource-block budget.",
    algorithm="Deep reinforcement learning scheduler operating at the MAC layer over the slicing substrate.",
    optimization_method="DRL (value/policy based, exact variant not verified)",
    ml_method="Deep RL",
    simulator="NA (not verified from the retrieved record)",
    testbed="NA",
    traffic_model="NA",
    network_scale="NA",
    source_url="https://doi.org/10.1109/TVT.2019.2922668",
    evidence="BIB",
)

C["F03"] = dict(
    in_flow=True,
    network_generation="5G", network_domain="RAN (HetNet, high mobility)",
    architecture="Heterogeneous network with multiple base stations and a centralised DRL agent performing joint uplink/downlink resource allocation.",
    scheduler_location="Centralised controller / base station",
    problem="Dynamic joint uplink and downlink resource allocation in high-mobility 5G heterogeneous networks, where user association and channel conditions change rapidly.",
    input_parameters="Channel state information, user mobility/position, queue states, uplink and downlink demand.",
    decision_variables="Uplink and downlink resource allocation and user association per time step.",
    actions="Resource-block / power / association decisions.",
    objective="Maximise system sum rate (and fairness) under mobility.",
    constraints="Transmit power, per-cell resource limits, user data-rate requirements.",
    algorithm="Deep reinforcement learning (centralised DRL agent) for joint UL/DL allocation.",
    optimization_method="DRL",
    ml_method="Deep RL",
    simulator="NA",
    testbed="NA",
    traffic_model="NA",
    network_scale="NA",
    source_url="https://doi.org/10.1109/JSAC.2020.3005495",
    evidence="BIB",
)

C["F04"] = dict(
    in_flow=True,
    network_generation="5G", network_domain="Transport / TSN integrated with 5G",
    architecture="End-to-end TSN-5G network where a centralised entity schedules time-triggered flows across TSN bridges and the 5G system.",
    scheduler_location="Centralised network controller (CNC-like)",
    problem="End-to-end traffic scheduling for time-sensitive networking over a 5G bridge, i.e. computing gate-control schedules that satisfy per-flow deadlines across TSN and 5G segments.",
    input_parameters="Flow sets with periods, deadlines, sizes; topology and link capacities; 5G bridge delay characteristics.",
    decision_variables="Transmission offsets/gate-control lists (time slots) for each flow on each link/queue.",
    actions="Per-flow per-link time-slot assignment.",
    objective="Feasible end-to-end scheduling satisfying determinism/latency bounds; typically maximising schedulable flow count or minimising end-to-end delay.",
    constraints="Per-flow deadlines and periods, link capacity, TSN queue constraints, 5G bridge delay bounds.",
    algorithm="Reinforcement-learning-enhanced particle swarm optimisation (RL-guided PSO) for the scheduling search.",
    optimization_method="Metaheuristic (PSO) hybridised with RL; exact MILP formulation used as reference",
    ml_method="Reinforcement learning (used to guide the metaheuristic, not as a direct policy)",
    simulator="NA",
    testbed="NA",
    traffic_model="Periodic deterministic TSN flows",
    network_scale="NA",
    source_url="https://doi.org/10.1109/TNET.2023.3276363",
    evidence="BIB",
)

C["F05"] = dict(
    in_flow=True,
    network_generation="5G", network_domain="Industrial 5G + TSN (transport)",
    architecture="Decentralised flow scheduling for integrated 5G and TSN industrial networks; multiple distributed scheduling entities cooperate instead of one centralised CNC.",
    scheduler_location="Decentralised (distributed schedulers across domains)",
    problem="Scalable flow scheduling across a joint 5G-TSN industrial network where centralised scheduling does not scale and cross-domain coordination is required.",
    input_parameters="Flow requirements (period, deadline, size), topology, link and bridge capabilities, per-domain schedule state.",
    decision_variables="Per-flow transmission schedules (time slots/offsets) in each domain.",
    actions="Schedule assignment per flow per domain.",
    objective="Maximise the number of schedulable time-critical flows / satisfy end-to-end deadlines.",
    constraints="Deadlines, periods, link capacity, per-domain resource limits.",
    algorithm="Decentralised scheduling algorithm with inter-domain coordination (age-aware / deadline-aware mechanism).",
    optimization_method="Distributed heuristic/optimisation",
    ml_method="NA",
    simulator="NA",
    testbed="NA",
    traffic_model="Periodic industrial time-critical flows",
    network_scale="NA",
    source_url="https://doi.org/10.1109/TNSE.2023.3301879",
    evidence="BIB",
)

C["F06"] = dict(
    in_flow=True,
    network_generation="5G", network_domain="RAN (MAC layer)",
    architecture="5G MAC-layer radio resource scheduler implemented on a simulated gNB.",
    scheduler_location="gNB MAC scheduler",
    problem="Radio resource scheduling in the 5G MAC layer: allocating resource blocks to users with heterogeneous QoS requirements.",
    input_parameters="Buffer status reports, channel quality indicators, QoS class of each bearer.",
    decision_variables="Resource-block allocation per user per TTI.",
    actions="Per-TTI scheduling decision.",
    objective="Satisfy QoS requirements (throughput/delay) while maximising resource utilisation.",
    constraints="Total resource blocks, per-bearer QoS targets.",
    algorithm="Deep reinforcement learning (DQN-family) scheduler trained against the 5G MAC environment.",
    optimization_method="DRL",
    ml_method="Deep RL",
    simulator="5G MAC-layer system-level simulator (LEASCH environment)",
    testbed="NA",
    traffic_model="NA",
    network_scale="NA",
    source_url="https://doi.org/10.1109/ACCESS.2020.3000893",
    evidence="BIB",
)

C["F07"] = dict(
    in_flow=False,
    network_generation="5G", network_domain="RAN (slicing)",
    architecture="Survey/position paper on 5G RAN slicing for vertical industries.",
    problem="Identifies enablers and challenges for RAN slicing for verticals, including scheduling and isolation requirements.",
    algorithm="N/A - magazine article (not a primary experimental paper)",
    ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/MCOM.2018.1701319",
    evidence="BIB", is_survey=True,
)

C["F12"] = dict(
    in_flow=True,
    network_generation="5G", network_domain="O-RAN + multi-UAV wireless",
    architecture="O-RAN-empowered multi-UAV wireless network with multi-agent DRL for joint task scheduling and resource sharing.",
    scheduler_location="Distributed agents (per-UAV / RAN intelligent control)",
    problem="Joint task scheduling and resource sharing among UAVs in an O-RAN-empowered network.",
    input_parameters="Task queues, UAV positions/energy, channel state, computation load.",
    decision_variables="Task offloading/scheduling decisions and resource sharing per UAV.",
    actions="Task-to-node assignment and resource allocation.",
    objective="Minimise task completion latency/energy while balancing load.",
    constraints="UAV energy, computation capacity, bandwidth.",
    algorithm="Multi-agent deep reinforcement learning (MADRL).",
    optimization_method="MADRL",
    ml_method="Multi-agent DRL",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/TVT.2023.3317995",
    evidence="BIB",
)

C["F13"] = dict(
    in_flow=True, network_generation="5G/legacy", network_domain="Transport (IP/SR)",
    architecture="Hybrid IP/segment-routing network with a centralised SDN controller and DRL-based traffic engineering.",
    scheduler_location="SDN controller",
    problem="Traffic engineering in hybrid IP/segment-routing networks: choosing routing/segment-list configurations to balance load.",
    input_parameters="Traffic matrix, topology, link utilisation, segment-routing capabilities.",
    decision_variables="Routing/segment-list selection per flow aggregate.",
    actions="Path/segment-list assignment.",
    objective="Minimise maximum link utilisation (or delay).",
    constraints="Link capacity, segment-list length, path feasibility.",
    algorithm="Deep reinforcement learning (DQN-family) traffic engineering.",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.23919/JCC.2021.09.014",
    evidence="BIB",
)

C["F16"] = dict(
    in_flow=True, network_generation="Generic/SDN", network_domain="Transport (SDN)",
    architecture="Software-defined network with a centralised DRL control agent (Experience-driven networking, EDN).",
    scheduler_location="SDN controller (centralised)",
    problem="Experience-driven networking: learning routing/scheduling policies directly from network experience instead of hand-tuned heuristics.",
    input_parameters="Traffic matrix, link states, path performance history.",
    decision_variables="Routing / resource-allocation actions for traffic flows.",
    actions="Path selection and rate allocation.",
    objective="Maximise network utility (throughput/delay trade-off).",
    constraints="Link capacities, flow demands.",
    algorithm="Deep reinforcement learning (actor-critic) for TE.",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="Custom packet-level / flow-level simulator",
    testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/INFOCOM.2018.8485853",
    evidence="BIB", is_foundational=True,
)

C["F17"] = dict(
    in_flow=True, network_generation="Generic/SDN", network_domain="Transport (SDN)",
    architecture="SDN with centralised controller performing DRL-based routing.",
    scheduler_location="SDN controller",
    problem="DRL-based routing in software-defined networks to improve throughput/delay versus shortest-path routing.",
    input_parameters="Traffic matrix, link utilisation, topology.",
    decision_variables="Next-hop / path selection per flow.",
    actions="Routing decisions.",
    objective="Minimise end-to-end delay / maximise throughput.",
    constraints="Link capacity, loop freedom.",
    algorithm="Deep reinforcement learning (DQN/DDQN family).",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/ACCESS.2022.3143870",
    evidence="BIB",
)

C["F19"] = dict(
    in_flow=True, network_generation="5G", network_domain="Edge / core (SFC placement)",
    architecture="5G mobile network with edge clouds; VNF/service-function chains placed across edge sites.",
    scheduler_location="Orchestrator/placement engine (centralised)",
    problem="Latency-aware service function chain placement in 5G mobile networks: where to instantiate each VNF so that end-to-end latency budgets are met.",
    input_parameters="SFC requests, node compute capacity, link delays, latency budgets.",
    decision_variables="VNF-to-node mapping (placement).",
    actions="Instantiation decisions for each VNF of each chain.",
    objective="Minimise end-to-end latency / maximise accepted chains.",
    constraints="Node capacity, latency budget, chain ordering.",
    algorithm="Placement optimisation (heuristic/exact) exposed through a NetSoft demo implementation.",
    optimization_method="Combinatorial optimisation",
    ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/NETSOFT.2019.8806679",
    evidence="BIB",
)

C["F20"] = dict(
    in_flow=True, network_generation="Generic/NFV", network_domain="Core / cloud (NFV)",
    architecture="NFV infrastructure with a centralised orchestrator jointly deciding chain composition and resource allocation.",
    scheduler_location="NFV orchestrator",
    problem="Joint optimisation of service function chaining (which VNFs, in which order) and resource allocation (how much CPU/bandwidth each gets).",
    input_parameters="Service requests, VNF catalogue, server capacities, link capacities.",
    decision_variables="Chain composition, VNF placement, CPU and bandwidth allocation.",
    actions="Deploy/compose chains and allocate resources.",
    objective="Minimise total resource cost / maximise accepted services.",
    constraints="Server and link capacities, chain dependency constraints, end-to-end delay.",
    algorithm="Mixed-integer optimisation with a heuristic/decomposition solution.",
    optimization_method="MILP + heuristics", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/ACCESS.2016.2646308",
    evidence="BIB",
)

C["F21"] = dict(
    in_flow=True, network_generation="5G", network_domain="MEC / edge",
    architecture="Mobile edge computing with adaptive service function chain scheduling driven by DRL.",
    scheduler_location="MEC orchestrator (centralised)",
    problem="Adaptive scheduling of service function chains in mobile edge computing under dynamic demand.",
    input_parameters="Chain requests, edge node load, latency requirements, resource availability.",
    decision_variables="Chain placement/scheduling and resource assignment.",
    actions="Deploy/migrate chain components.",
    objective="Minimise service latency / cost while meeting SFC requirements.",
    constraints="Edge node capacity, delay bounds, chain ordering.",
    algorithm="Deep reinforcement learning for SFC scheduling.",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/ACCESS.2020.3022706",
    evidence="BIB",
)

C["F29"] = dict(
    in_flow=True, network_generation="4G/5G", network_domain="Mobile core / transport (SFC)",
    architecture="Mobile network with service function chains for mobile traffic; traffic steering across chains.",
    scheduler_location="Mobile network controller/orchestrator",
    problem="QoS-aware and reliable traffic steering for service function chaining in mobile networks: choosing which chain instance handles each flow so that QoS and reliability targets hold.",
    input_parameters="Flow QoS class, chain instance load, link/node failure state.",
    decision_variables="Flow-to-chain assignment (steering).",
    actions="Steering decisions per flow.",
    objective="Maximise QoS satisfaction and reliability, minimise resource cost.",
    constraints="Chain capacity, QoS requirements, availability constraints.",
    algorithm="Optimisation model with heuristic solution (QoS-aware and reliability-aware steering).",
    optimization_method="Combinatorial optimisation", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/JSAC.2017.2774429",
    evidence="BIB", is_foundational=True,
)

C["F30"] = dict(
    in_flow=True, network_generation="3G/HSDPA", network_domain="RAN (packet scheduling)",
    architecture="HSDPA base station packet scheduler handling mixed traffic.",
    scheduler_location="Node-B MAC-hs scheduler",
    problem="Packet scheduling algorithms for mixed traffic (streaming + best-effort) over HSDPA.",
    input_parameters="Queue states, channel quality, QoS class of each flow.",
    decision_variables="Which flow to serve and at what rate per TTI.",
    actions="Per-TTI scheduling decision.",
    objective="Balance QoS of streaming flows against best-effort throughput and fairness.",
    constraints="HSDPA channel and code constraints, delay bounds for streaming.",
    algorithm="Comparative study of packet scheduling algorithms (e.g. proportional fair and QoS-aware variants).",
    optimization_method="Heuristic scheduling rules", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="Mixed streaming + best-effort", network_scale="NA",
    source_url="https://doi.org/10.1109/ISCC.2007.4381499",
    evidence="BIB", is_foundational=True,
)

C["F31"] = dict(
    in_flow=True, network_generation="5G", network_domain="O-RAN (joint routing and packet scheduling)",
    architecture="O-RAN with a near-real-time RIC controlling joint routing and packet scheduling for URLLC and eMBB traffic.",
    scheduler_location="O-RAN near-RT RIC (xApp)",
    problem="Joint routing and packet scheduling for coexisting URLLC and eMBB traffic in 5G O-RAN.",
    input_parameters="Per-flow latency budgets, queue states, radio link quality, slice/class of each flow.",
    decision_variables="Route selection and per-TTI packet scheduling for URLLC vs eMBB flows.",
    actions="Routing and scheduling decisions at the RIC.",
    objective="Minimise URLLC latency while preserving eMBB throughput.",
    constraints="URLLC latency budget, radio resource limits, route feasibility.",
    algorithm="Optimisation/heuristic joint routing-scheduling with O-RAN control-loop integration.",
    optimization_method="Combinatorial optimisation", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="Mixed URLLC + eMBB", network_scale="NA",
    source_url="https://doi.org/10.1109/ICCWorkshops53468.2022.9814680",
    evidence="BIB",
)

C["F32"] = dict(
    in_flow=True, network_generation="Generic/SDN", network_domain="Transport (SDN)",
    architecture="SDN with a deep-RL routing agent for traffic engineering.",
    scheduler_location="SDN controller",
    problem="Efficient routing for traffic engineering in SDN using deep reinforcement learning.",
    input_parameters="Traffic matrix, link utilisation/state.",
    decision_variables="Routing path per flow aggregate.",
    actions="Path assignment.",
    objective="Minimise congestion / maximise throughput.",
    constraints="Link capacity, path feasibility.",
    algorithm="Deep reinforcement learning routing agent.",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1016/j.comnet.2024.110489",
    evidence="BIB",
)

C["F38"] = dict(
    in_flow=True, network_generation="5G", network_domain="End-to-end (RAN + core + transport)",
    architecture="End-to-end network slicing architecture spanning RAN, transport and core, with slice management functions.",
    scheduler_location="Slice management/orchestration layer",
    problem="End-to-end network slicing for 5G mobile networks: how to compose and manage slices across all network segments.",
    input_parameters="Slice requests with QoS requirements, available resources per domain.",
    decision_variables="Slice composition and resource assignment per domain.",
    actions="Slice instantiation and resource allocation.",
    objective="Meet per-slice requirements while maximising infrastructure utilisation.",
    constraints="Per-domain resource limits, isolation requirements.",
    algorithm="Architectural design with resource-allocation procedures.",
    optimization_method="Combinatorial optimisation", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.2197/ipsjjip.25.772",
    evidence="BIB", is_foundational=True,
)

C["F41"] = dict(
    in_flow=True, network_generation="5G", network_domain="O-RAN (traffic steering)",
    architecture="O-RAN with near-RT RIC xApp performing traffic steering for URLLC traffic.",
    scheduler_location="O-RAN near-RT RIC xApp",
    problem="Intelligent traffic steering for URLLC in O-RAN, deciding which radio access node/interface carries each URLLC flow.",
    input_parameters="Per-UE/per-flow radio conditions, latency measurements, cell load, URLLC latency budget.",
    decision_variables="Traffic steering decision (which RAN node/interface serves each flow).",
    actions="Steering the flow to a selected access point.",
    objective="Minimise URLLC latency / maximise URLLC reliability.",
    constraints="URLLC latency and reliability targets, radio resource limits.",
    algorithm="Deep reinforcement learning (xApp logic) evaluated on an O-RAN testbed.",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="NA", testbed="O-RAN testbed (per the paper's own evaluation; exact platform not verified)",
    traffic_model="URLLC traffic", network_scale="NA",
    source_url="https://doi.org/10.1109/ICC45041.2023.10278981",
    evidence="BIB",
)

C["F42"] = dict(
    in_flow=True, network_generation="6G", network_domain="O-RAN (traffic steering)",
    architecture="6G Open RAN architecture with deep-RL-driven traffic steering across RAN and non-RAN access.",
    scheduler_location="O-RAN / Open RAN control layer",
    problem="Traffic steering in 6G Open RAN: learning policies that assign traffic to access paths under dynamic conditions.",
    input_parameters="Radio link states, load, flow requirements, historical performance.",
    decision_variables="Path/access selection per flow.",
    actions="Traffic steering decisions.",
    objective="Maximise throughput and satisfy QoS under heterogeneity.",
    constraints="Radio resource limits, QoS requirements.",
    algorithm="Deep reinforcement learning for traffic steering.",
    optimization_method="DRL", ml_method="Deep RL",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/TWC.2024.3396273",
    evidence="BIB",
)

C["F43"] = dict(
    in_flow=True, network_generation="5G/6G transport", network_domain="Transport (SRv6, SFC)",
    architecture="SRv6-based transport network with a centralised online SFC planner steering flows through service chains.",
    scheduler_location="Centralised SFC planner",
    problem="Online planning of service function chains with SRv6 flow steering: deciding chain composition and SRv6 segment lists online.",
    input_parameters="SFC requests, topology, segment-routing capability, node/link load.",
    decision_variables="Chain placement plus SRv6 segment list (flow steering path) per request.",
    actions="Deploy chain and install SRv6 policy.",
    objective="Minimise resource consumption / maximise accepted requests while meeting SFC requirements.",
    constraints="Node/link capacity, latency budget, SRv6 SID list length.",
    algorithm="Online planning algorithm (heuristic) with SRv6 flow steering.",
    optimization_method="Combinatorial optimisation", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/TNSM.2024.3392945",
    evidence="BIB",
)

C["F44"] = dict(
    in_flow=True, network_generation="5G", network_domain="O-RAN (traffic steering)",
    architecture="Open RAN architecture with programmable, customised intelligence for traffic steering.",
    scheduler_location="O-RAN RIC / RAN controller",
    problem="Making traffic steering in 5G Open RAN programmable and customised so that operators can define their own steering logic.",
    input_parameters="RAN telemetry (per-UE radio conditions), flow requirements, policy configuration.",
    decision_variables="Steering policy parameters / per-flow access selection.",
    actions="Traffic steering decisions.",
    objective="Improve throughput and QoS satisfaction versus static steering.",
    constraints="RAN resource limits, policy constraints.",
    algorithm="Programmable control framework with custom intelligence modules.",
    optimization_method="NA", ml_method="NA (programmability focus)",
    simulator="NA", testbed="Open RAN experimental platform", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/TMC.2023.3272948",
    evidence="BIB",
)

C["F45"] = dict(
    in_flow=False, network_generation="Generic/SDN", network_domain="Transport (SDN routing/TE)",
    architecture="Survey of routing and traffic engineering in SDN.",
    problem="Surveys routing and traffic-engineering approaches in software-defined networks.",
    algorithm="N/A - survey", ml_method="NA",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/COMST.2018.2869756",
    evidence="BIB", is_survey=True,
)

C["F46"] = dict(
    in_flow=False, network_generation="Generic/SDN", network_domain="Transport (DRL for TE)",
    architecture="Survey of DRL-based traffic engineering in SDN.",
    problem="Surveys how deep reinforcement learning has been applied to traffic engineering in software-defined networks.",
    algorithm="N/A - survey", ml_method="DRL (surveyed)",
    simulator="NA", testbed="NA", traffic_model="NA", network_scale="NA",
    source_url="https://doi.org/10.1109/COMST.2021.3068696",
    evidence="BIB", is_survey=True,
)

for k, v in C.items():
    if k in by:
        by[k].update(v)
        by[k].setdefault("area", "flow")

json.dump(recs, open(os.path.join(DATA, "master_stage3.json"), "w"), indent=1)
print("stage3: characterised", len(C), "flow papers; total records", len(recs))
