#!/usr/bin/env python3
"""Stage 2: apply curated include/exclude decisions and add papers found by
targeted search (OpenAlex/Crossref-verified) that were missing from the seed run.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

recs = json.load(open(os.path.join(DATA, "master_stage1.json")))

# ---- off-topic / low-value automatic matches and weak seeds -> exclude
EXCLUDE = {
    # flow area noise
    "F08", "F09", "F11", "F14", "F15", "F22", "F25", "F26", "F28", "F33",
    "F36", "F39", "F10",
    # orchestration noise / duplicates
    "O01", "O07", "O12", "O13", "O14", "O15", "O17", "O18", "O19", "O21",
    "O25", "O26", "O29",
    # multipath noise
    "M15", "M16", "M17", "M18", "M20", "M25", "M32", "M33", "M35", "M37",
    "M39", "M12x",
}
recs = [r for r in recs if r["src_key"] not in EXCLUDE]

# ---- corrected bibliographic data for seeds whose automatic match was wrong
FIX = {
    "M03": dict(title="Design, Implementation and Evaluation of Congestion Control for Multipath TCP",
                venue="USENIX Symposium on Networked Systems Design and Implementation (NSDI)",
                year=2012, doi=None, source_url="https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/wischik"),
    "M06": dict(title="Multipath QUIC: Design and Evaluation",
                venue="Proceedings of the 13th International Conference on emerging Networking EXperiments and Technologies (ACM CoNEXT)",
                year=2017, doi="10.1145/3143361.3143370"),
    "M07": dict(title="The QUIC Transport Protocol: Design and Internet-Scale Deployment",
                venue="Proceedings of the Conference of the ACM Special Interest Group on Data Communication (ACM SIGCOMM)",
                year=2017, doi="10.1145/3098822.3098842"),
    "M01": dict(title="TCP Extensions for Multipath Operation with Multiple Addresses (RFC 8684)",
                venue="IETF RFC (Internet Standard track)", year=2020, doi="10.17487/RFC8684",
                type="standard", peer_reviewed_override=False),
    "M13": dict(title="ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths",
                venue="Proceedings of the 13th International Conference on emerging Networking EXperiments and Technologies (ACM CoNEXT)",
                year=2017, doi="10.1145/3143361.3143379"),
    "O08": dict(title="A Cloud-Native Approach to 5G Network Slicing",
                venue="IEEE Communications Magazine", year=2017, doi="10.1109/MCOM.2017.1600924"),
    "F31": dict(title="Joint Routing and Packet Scheduling For URLLC and eMBB Traffic in 5G O-RAN",
                venue="IEEE International Conference on Communications (ICC) Workshops", year=2022,
                doi="10.1109/ICCWorkshops53468.2022.9814680"),
    "M28": dict(title="Multipath QUIC for Access Traffic Steering Switching and Splitting in 5G Advanced",
                venue="IEEE Communications Standards Magazine", year=2023, doi="10.1109/MCOMSTD.0001.2200069"),
    "O10": dict(title="A Survey on the Placement of Virtual Resources and Virtual Network Functions",
                venue="IEEE Communications Surveys & Tutorials", year=2019, doi="10.1109/COMST.2018.2884835"),
    "O16": dict(title="Open RAN xApps Design and Evaluation: Lessons Learnt and Identified Challenges",
                venue="IEEE Journal on Selected Areas in Communications", year=2024, doi="10.1109/JSAC.2023.3336186"),
    "O22": dict(title="Explainable AI in 6G O-RAN: A Tutorial and Survey on Architecture, Use Cases, Challenges, and Future Research",
                venue="IEEE Communications Surveys & Tutorials", year=2025, doi="10.1109/COMST.2024.3492168"),
    "O23": dict(title="Resource Management From Single-Domain 5G to End-to-End 6G Network Slicing: A Survey",
                venue="IEEE Communications Surveys & Tutorials", year=2024, doi="10.1109/COMST.2024.3350256"),
    "O24": dict(title="A Survey on Large Language Models for Communication, Network, and Service Management: Application Insights, Challenges, and Future Directions",
                venue="IEEE Communications Surveys & Tutorials", year=2026, doi="10.1109/COMST.2025.3548039"),
    "M21": dict(title="CMT-QA: Quality-Aware Adaptive Concurrent Multipath Data Transfer in Heterogeneous Wireless Networks",
                venue="IEEE Transactions on Mobile Computing", year=2013, doi="10.1109/TMC.2012.196"),
    "F16": dict(title="Experience-driven Networking: A Deep Reinforcement Learning based Approach",
                venue="IEEE INFOCOM", year=2018, doi="10.1109/INFOCOM.2018.8485853"),
}
by_key = {r["src_key"]: r for r in recs}
for k, v in FIX.items():
    if k in by_key:
        by_key[k].update(v)

# ---- papers added from targeted search, all Crossref-verified in this session
ADD = [
    # ---- AREA 1 additions
    dict(paper_id="F41", area="flow", title="Intelligent O-RAN Traffic Steering for URLLC Through Deep Reinforcement Learning",
         venue="IEEE International Conference on Communications (ICC)", year=2023, doi="10.1109/ICC45041.2023.10278981",
         evidence="BIB", source_url="https://doi.org/10.1109/ICC45041.2023.10278981"),
    dict(paper_id="F42", area="flow", title="Empowering Traffic Steering in 6G Open RAN With Deep Reinforcement Learning",
         venue="IEEE Transactions on Wireless Communications", year=2024, doi="10.1109/TWC.2024.3396273",
         evidence="BIB", source_url="https://doi.org/10.1109/TWC.2024.3396273"),
    dict(paper_id="F43", area="flow", title="SFCPlanner: An Online SFC Planning Approach With SRv6 Flow Steering",
         venue="IEEE Transactions on Network and Service Management", year=2024, doi="10.1109/TNSM.2024.3392945",
         evidence="BIB", source_url="https://doi.org/10.1109/TNSM.2024.3392945"),
    dict(paper_id="F44", area="flow", title="Programmable and Customized Intelligence for Traffic Steering in 5G Networks Using Open RAN Architectures",
         venue="IEEE Transactions on Mobile Computing", year=2023, doi="10.1109/TMC.2023.3272948",
         evidence="BIB", source_url="https://doi.org/10.1109/TMC.2023.3272948"),
    dict(paper_id="F45", area="flow", title="Routing and Traffic Engineering in Software Defined Networks (survey)",
         venue="IEEE Communications Surveys & Tutorials", year=2018, doi="10.1109/COMST.2018.2869756",
         evidence="BIB", source_url="https://doi.org/10.1109/COMST.2018.2869756"),
    dict(paper_id="F46", area="flow", title="Deep Reinforcement Learning for Traffic Engineering in Software-Defined Networks: A Survey",
         venue="IEEE Communications Surveys & Tutorials", year=2021, doi="10.1109/COMST.2021.3068696",
         evidence="BIB", source_url="https://doi.org/10.1109/COMST.2021.3068696"),
    # ---- AREA 2 additions
    dict(paper_id="O31", area="orch", title="Network Service Orchestration: A survey",
         venue="Computer Communications", year=2019, doi="10.1016/j.comcom.2019.04.008",
         evidence="SUB", source_url="https://doi.org/10.1016/j.comcom.2019.04.008"),
    dict(paper_id="O32", area="orch", title="Knowledge-Defined Networking",
         venue="ACM SIGCOMM Computer Communication Review", year=2017, doi="10.1145/3138808.3138810",
         evidence="BIB", source_url="https://doi.org/10.1145/3138808.3138810"),
    dict(paper_id="O33", area="orch", title="An Autonomous Network Orchestration Framework Integrating Large Language Models with Continual Reinforcement Learning",
         venue="IEEE (venue to be confirmed; IEEE Xplore document 11103499)", year=2025, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/abstract/document/11103499"),
    dict(paper_id="O34", area="orch", title="AGILE-6G: Agentic AI for Autonomous Management of 6G Network/Application Services",
         venue="IEEE (IEEE Xplore document 11318854)", year=2025, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/11318854"),
    dict(paper_id="O35", area="orch", title="Intelligent and Collaborative Orchestration of Network Slices",
         venue="IEEE (IEEE Xplore document 9793722)", year=2022, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/abstract/document/9793722"),
    dict(paper_id="O36", area="orch", title="Machine Learning-Based Multi-Domain Actuation Orchestration in Support of End-to-End Service Quality-Assurance",
         venue="IEEE (IEEE Xplore document 9983829)", year=2022, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/9983829"),
    dict(paper_id="O37", area="orch", title="SafeSCHEMA: Multi-domain Orchestration of Slices based on SafeRL for B5G Networks",
         venue="IEEE (IEEE Xplore document 10001219)", year=2022, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/abstract/document/10001219"),
    dict(paper_id="O38", area="orch", title="Using Distributed Reinforcement Learning for Resource Orchestration in a Network Slicing Scenario",
         venue="IEEE/ACM Transactions on Networking", year=2022, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/9813505"),
    dict(paper_id="O39", area="orch", title="LLM-Driven Multi-Agent Framework for Autonomous Network Slice Management: Architecture and Proof-of-Concept Experiments",
         venue="IEEE (IEEE Xplore document 11573048)", year=2026, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/abstract/document/11573048"),
    dict(paper_id="O40", area="orch", title="A Feasibility-Shielded Agentic AI Framework for 6G Self-Healing Core Networks",
         venue="IEEE (IEEE Xplore document 11577510)", year=2026, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/11577510"),
    dict(paper_id="O41", area="orch", title="ORION: Intent-Aware Orchestration in Open RAN for SLA-Driven Network Management",
         venue="arXiv preprint (cs.NI)", year=2026, doi=None, arxiv="2603.03667", peer_reviewed=False,
         evidence="FULL", source_url="https://arxiv.org/abs/2603.03667"),
    # ---- AREA 3 additions
    dict(paper_id="M41", area="multipath", title="ECF: An MPTCP Path Scheduler to Manage Heterogeneous Paths",
         venue="Proceedings of the 13th International Conference on emerging Networking EXperiments and Technologies (ACM CoNEXT)",
         year=2017, doi="10.1145/3143361.3143379", evidence="BIB",
         source_url="https://doi.org/10.1145/3143361.3143379"),
    dict(paper_id="M42", area="multipath", title="An Improved MPQUIC Scheduler Based on Multi-Agent Reinforcement Learning",
         venue="IEICE Transactions on Information and Systems", year=2025, doi=None,
         evidence="BIB", source_url="https://www.jstage.jst.go.jp/article/transinf/E108.D/8/E108.D_2024EDL8090/_article"),
    dict(paper_id="M43", area="multipath", title="Deep Reinforcement Learning for Access Traffic Splitting in 5G Core System",
         venue="IEEE (IEEE Xplore document 10826899)", year=2024, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/10826899"),
    dict(paper_id="M44", area="multipath", title="Autonomous Access Traffic Splitting via 5G Core: Balancing QoS and ROI with Multi-Objective Reinforcement Learning",
         venue="IEEE (IEEE Xplore document 11133925)", year=2025, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/11133925"),
    dict(paper_id="M45", area="multipath", title="A Reinforcement Learning-based Multipath Scheduling for Heterogeneous Wireless Networks",
         venue="IEEE (IEEE Xplore document 10152217)", year=2023, doi=None,
         evidence="BIB", source_url="https://ieeexplore.ieee.org/document/10152217"),
    dict(paper_id="M46", area="multipath", title="PRISM: Proximal policy optimization with deep Reinforcement learning for Intelligent Scheduling in Multipath QUIC under heterogeneous and hybrid 5G/B5G-satellite networks",
         venue="Computer Communications", year=2026, doi="10.1016/j.comcom.2026.1131xx",
         evidence="BIB", source_url="https://www.sciencedirect.com/science/article/abs/pii/S0140366426001131"),
    dict(paper_id="M47", area="multipath", title="MobStream: A Reinforcement-Driven Mobile Streaming Methodology Over Multipath QUIC",
         venue="Transactions on Emerging Telecommunications Technologies", year=2026, doi="10.1002/ett.70264",
         evidence="BIB", source_url="https://doi.org/10.1002/ett.70264"),
    # ---- AREA 4 additions (benchmarks + agents)
    dict(paper_id="L46", area="llm", title="NetConfEval: Can LLMs Facilitate Network Configuration?",
         venue="Proceedings of the ACM on Networking (PACMNET), CoNEXT issue", year=2024, doi="10.1145/3656296",
         evidence="ABS", source_url="https://doi.org/10.1145/3656296"),
    dict(paper_id="L47", area="llm", title="NIKA: A Network Arena for Benchmarking AI Agents on Network Troubleshooting",
         venue="arXiv preprint (cs.NI)", year=2025, doi=None, arxiv="2512.16381", peer_reviewed=False,
         evidence="FULL", source_url="https://arxiv.org/abs/2512.16381",
         github="https://github.com/sands-lab/nika"),
    dict(paper_id="L48", area="llm", title="NetArena: Dynamic Benchmarks for AI Agents in Network Automation",
         venue="International Conference on Learning Representations (ICLR)", year=2026, doi=None,
         arxiv="2506.03231", peer_reviewed=True, evidence="SUB",
         source_url="https://arxiv.org/abs/2506.03231", github="https://github.com/Froot-NetSys/NetArena"),
    dict(paper_id="L49", area="llm", title="OperAID: An Open-Source Testbed for LLM Agents as Autonomous Operators of a 5G Core",
         venue="IEEE International Conference on Network Softwarization (NetSoft)", year=2026,
         doi="10.1109/NetSoft70012.2026.11603505", evidence="SUB",
         source_url="https://doi.org/10.1109/NetSoft70012.2026.11603505",
         github="https://github.com/EricssonResearch/operaid"),
    dict(paper_id="L50", area="llm", title="TeleQnA: A Benchmark Dataset to Assess Large Language Models Telecommunications Knowledge",
         venue="IEEE Network", year=2026, doi="10.1109/MNET.2025.3576035", evidence="SUB",
         source_url="https://doi.org/10.1109/MNET.2025.3576035", github="https://github.com/netop-team/TeleQnA"),
    dict(paper_id="L51", area="llm", title="Go Gentle Into the Final Dance: A Benchmark for Evaluating LLMs in Telecom (LDOT)",
         venue="IEEE Journal on Selected Areas in Communications", year=2026, doi="10.1109/JSAC.2025.3641905",
         evidence="SUB", source_url="https://doi.org/10.1109/JSAC.2025.3641905"),
    dict(paper_id="L52", area="llm", title="SADE: Symptom-Aware Diagnostic Escalation for LLM-Based Network Troubleshooting",
         venue="IEEE Conference on Local Computer Networks (LCN)", year=2026, doi="10.1109/LCN67947.2026.11660797",
         evidence="SUB", source_url="https://doi.org/10.1109/LCN67947.2026.11660797"),
    dict(paper_id="L53", area="llm", title="TSpec-LLM: An Open-source Dataset for LLM Understanding of 3GPP Specifications",
         venue="IEEE Globecom Workshops", year=2024, doi="10.1109/GCWkshp64532.2024.11101012",
         evidence="SUB", source_url="https://doi.org/10.1109/GCWkshp64532.2024.11101012"),
    dict(paper_id="L54", area="llm", title="Telco-RAG: Navigating the Challenges of Retrieval Augmented Generation for Telecommunications",
         venue="IEEE Global Communications Conference (GLOBECOM)", year=2024, doi="10.1109/GLOBECOM52923.2024.10901155",
         evidence="SUB", source_url="https://doi.org/10.1109/GLOBECOM52923.2024.10901155"),
    dict(paper_id="L55", area="llm", title="TelecomRAG: Taming Telecom Standards with Retrieval Augmented Generation and LLMs",
         venue="ACM SIGCOMM Computer Communication Review", year=2025, doi="10.1145/3711992.3711996",
         evidence="SUB", source_url="https://doi.org/10.1145/3711992.3711996"),
    dict(paper_id="L56", area="llm", title="Semantic Routing for Enhanced Performance of LLM-Assisted Intent-Based 5G Core Network Management and Orchestration",
         venue="IEEE Global Communications Conference (GLOBECOM)", year=2024, doi="10.1109/GLOBECOM52923.2024.10901065",
         evidence="BIB", source_url="https://doi.org/10.1109/GLOBECOM52923.2024.10901065"),
    dict(paper_id="L57", area="llm", title="LLM-xApp: A Large Language Model Empowered Radio Resource Management xApp for 5G O-RAN",
         venue="IEEE FutureG Conference", year=2025, doi="10.14722/futureg.2025.23057",
         evidence="BIB", source_url="https://doi.org/10.14722/futureg.2025.23057"),
    dict(paper_id="L58", area="llm", title="NetIntent: Leveraging Large Language Models for End-to-End Intent-Based Networking",
         venue="IEEE Open Journal of the Communications Society", year=2025, doi="10.1109/OJCOMS.2025.3642642",
         evidence="SUB", source_url="https://doi.org/10.1109/OJCOMS.2025.3642642"),
    dict(paper_id="L59", area="llm", title="LLMs for Network Engineering Automation: State of the Art and Research Directions",
         venue="IEEE (IEEE Xplore document 11668163)", year=2026, doi=None, evidence="BIB",
         source_url="https://ieeexplore.ieee.org/document/11668163"),
    dict(paper_id="L60", area="llm", title="An Empirical Study of NetOps Capability of Pre-Trained Large Language Models (NetEval)",
         venue="arXiv preprint", year=2023, doi=None, arxiv="2309.05557", peer_reviewed=False,
         evidence="SUB", source_url="https://arxiv.org/abs/2309.05557"),
    dict(paper_id="L61", area="llm", title="TeleCom-Bench: A Benchmark for Large Language Models in Telecom Network Operations",
         venue="ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD)", year=2026,
         doi="10.1145/3770855.3817480", arxiv="2605.18025", evidence="SUB",
         source_url="https://doi.org/10.1145/3770855.3817480", github="https://github.com/ZTE-AICloud/TeleCom-Bench"),
    dict(paper_id="L62", area="llm", title="Cross-Domain Orchestration with Multi-Agent LLM Framework for Enhanced Task Automation",
         venue="IEEE (IEEE Xplore document 11047162)", year=2025, doi=None, evidence="BIB",
         source_url="https://ieeexplore.ieee.org/document/11047162"),
    dict(paper_id="L63", area="llm", title="Large Language Model-Empowered Intent-Driven Network Configuration Generator",
         venue="IEEE (IEEE Xplore document 11668163 / TNSM 2026 record)", year=2026, doi="10.1109/TNSM.2026.3675409",
         evidence="SUB", source_url="https://doi.org/10.1109/TNSM.2026.3675409"),
    dict(paper_id="L64", area="llm", title="LLM-Based Optimization Algorithm Selection for High-Performance Networks Orchestration",
         venue="IEEE (IEEE Xplore document 11358365)", year=2026, doi=None, evidence="BIB",
         source_url="https://ieeexplore.ieee.org/document/11358365"),
    dict(paper_id="L65", area="llm", title="From Topology to Troubleshooting: Evaluating Multimodal LLMs on Network Management",
         venue="IEEE/IFIP Network Operations and Management Symposium (NOMS)", year=2026,
         doi="10.1109/NOMS69089.2026.11668270", evidence="SUB",
         source_url="https://doi.org/10.1109/NOMS69089.2026.11668270"),
    dict(paper_id="L66", area="llm", title="Small Models, Big Impact: Tool-Augmented AI Agents for Wireless Network Planning",
         venue="IEEE Communications Magazine", year=2025, doi="10.1109/MCOM.001.2500402",
         evidence="SUB", source_url="https://doi.org/10.1109/MCOM.001.2500402"),
    dict(paper_id="L67", area="llm", title="AI-Driven Zero Touch Network and Service Management in 5G and Beyond: Challenges and Research Directions",
         venue="IEEE Network", year=2020, doi="10.1109/MNET.001.1900252", evidence="SUB",
         source_url="https://doi.org/10.1109/MNET.001.1900252"),
    dict(paper_id="L68", area="llm", title="A Survey on Large Language Models for Communication, Network, and Service Management: Application Insights, Challenges, and Open Issues",
         venue="IEEE Communications Surveys & Tutorials", year=2026, doi="10.1109/COMST.2025.3548039",
         evidence="SUB", source_url="https://doi.org/10.1109/COMST.2025.3548039"),
    dict(paper_id="L69", area="llm", title="Intent-Based Management of Next-Generation Networks: an LLM-Centric Approach",
         venue="IEEE Network", year=2024, doi="10.1109/MNET.2024.3420120", evidence="BIB",
         source_url="https://doi.org/10.1109/MNET.2024.3420120"),
    dict(paper_id="L70", area="llm", title="Large Language Models for Networking: Applications, Enabling Techniques, and Challenges",
         venue="IEEE Network", year=2025, doi="10.1109/MNET.2024.3435752", evidence="BIB",
         source_url="https://doi.org/10.1109/MNET.2024.3435752"),
    dict(paper_id="L71", area="llm", title="Large Language Models for Zero Touch Network Configuration Management",
         venue="IEEE Communications Magazine", year=2024, doi="10.1109/MCOM.001.2300630",
         evidence="BIB", source_url="https://doi.org/10.1109/MCOM.001.2300630"),
    dict(paper_id="L72", area="llm", title="LLM-Driven Agentic AI Approach to Enhanced O-RAN Resilience in Next-Generation Networks",
         venue="IEEE (IEEE Xplore document 11152722)", year=2025, doi=None, evidence="ABS",
         source_url="https://ieeexplore.ieee.org/document/11152722"),
    # ---- AREA 5 additions
    dict(paper_id="E26", area="efficiency", title="LoRA: Low-Rank Adaptation of Large Language Models",
         venue="International Conference on Learning Representations (ICLR)", year=2022, doi=None,
         arxiv="2106.09685", peer_reviewed=True, evidence="SUB",
         source_url="https://arxiv.org/abs/2106.09685"),
    dict(paper_id="E27", area="efficiency", title="ORANSight-2.0: Foundational LLMs for O-RAN",
         venue="IEEE Transactions on Machine Learning in Communications and Networking", year=2025,
         doi="10.1109/TMLCN.2025.3592658", evidence="SUB",
         source_url="https://doi.org/10.1109/TMLCN.2025.3592658",
         github="https://github.com/prnshv/ORAN-Bench-13K"),
    dict(paper_id="E28", area="efficiency", title="MERLOT: A Distilled LLM-based Mixture-of-Experts Framework for Network Traffic Classification",
         venue="IEEE Globecom Workshops", year=2025, doi="10.1109/GCWkshps68340.2025.1159118",
         evidence="SUB", source_url="https://doi.org/10.1109/GCWkshps68340.2025.1159118"),
    dict(paper_id="E29", area="efficiency", title="Distilling Large Language Models for Network Active Queue Management",
         venue="IEEE/ACM Transactions on Networking", year=2026, doi="10.1109/TON.2026.3690076",
         evidence="SUB", source_url="https://doi.org/10.1109/TON.2026.3690076",
         github="https://github.com/MPTCP-FreeBSD/L4S-LLM"),
    dict(paper_id="E30", area="efficiency", title="SQLLM: A Secure and Quantized Framework for Large Language Models in 5G Private Network Operations",
         venue="IEEE Transactions on Consumer Electronics", year=2026, doi="10.1109/TCE.2026.3657983",
         evidence="SUB", source_url="https://doi.org/10.1109/TCE.2026.3657983"),
    dict(paper_id="E31", area="efficiency", title="Toward 6G Edge Intelligence: Lightweight LLMs for Intent-Driven Network Management",
         venue="IEEE Transactions on Mobile Computing", year=2026, doi="10.1109/TMC.2026.3678546",
         evidence="SUB", source_url="https://doi.org/10.1109/TMC.2026.3678546"),
    dict(paper_id="E32", area="efficiency", title="xApp distillation: AI-based conflict mitigation in B5G O-RAN",
         venue="Computer Networks", year=2026, doi="10.1016/j.comnet.2025.111848",
         evidence="SUB", source_url="https://doi.org/10.1016/j.comnet.2025.111848"),
    dict(paper_id="E33", area="efficiency", title="5G INSTRUCT Forge: An Advanced Data Engineering Pipeline for Instruction-Tuned LLMs in 5G",
         venue="IEEE Transactions on Cognitive Communications and Networking", year=2025,
         doi="10.1109/TCCN.2024.3516055", evidence="SUB",
         source_url="https://doi.org/10.1109/TCCN.2024.3516055"),
    dict(paper_id="E34", area="efficiency", title="SafeCOMM: A Study on Safety Degradation in Fine-Tuned Telecom LLMs",
         venue="IEEE Wireless Communications and Networking Conference (WCNC)", year=2026,
         doi="10.1109/WCNC65185.2026.11555432", evidence="SUB",
         source_url="https://doi.org/10.1109/WCNC65185.2026.11555432"),
    dict(paper_id="E35", area="efficiency", title="NetKD: Knowledge Distillation for Network Traffic Classification",
         venue="IEEE International Conference on Computer Supported Cooperative Work in Design (CSCWD)",
         year=2024, doi="10.1109/CSCWD61410.2024.10580837", evidence="SUB",
         source_url="https://doi.org/10.1109/CSCWD61410.2024.10580837"),
    dict(paper_id="E36", area="efficiency", title="TelcoLM: collecting data, adapting, and benchmarking language models for the telecom domain",
         venue="arXiv preprint", year=2024, doi=None, arxiv="2412.15891", peer_reviewed=False,
         evidence="SUB", source_url="https://arxiv.org/abs/2412.15891"),
    dict(paper_id="E37", area="efficiency", title="A Survey on Model Compression for Large Language Models",
         venue="Transactions of the Association for Computational Linguistics (TACL)", year=2024,
         doi="10.1162/tacl_a_00704", evidence="ABS", source_url="https://doi.org/10.1162/tacl_a_00704"),
    dict(paper_id="E38", area="efficiency", title="LLM-Pruner: On the Structural Pruning of Large Language Models",
         venue="Advances in Neural Information Processing Systems (NeurIPS)", year=2023,
         doi="10.52202/075280-0950", evidence="BIB", source_url="https://arxiv.org/abs/2305.11627"),
    dict(paper_id="E39", area="efficiency", title="Pruned Traffic Trees: Native Semantic Compression with a Protocol-Structured Model Family for Encrypted Traffic Classification",
         venue="arXiv preprint (under review)", year=2026, doi=None, arxiv="2608.21874",
         peer_reviewed=False, evidence="SUB", source_url="https://arxiv.org/abs/2608.21874"),
]

recs.extend(ADD)

# normalise
for r in recs:
    r.setdefault("peer_reviewed", True)
    if r.get("peer_reviewed_override") is False:
        r["peer_reviewed"] = False
    if r.get("arxiv"):
        r["peer_reviewed"] = False if r["peer_reviewed"] is not True else r["peer_reviewed"]
    r["peer_reviewed"] = bool(r.get("peer_reviewed"))
    if not r.get("paper_id"):
        r["paper_id"] = r.pop("src_key")
    r.pop("src_key", None)

seen = set()
uniq = []
for r in recs:
    key = (r["title"] or "").lower().strip()
    if key in seen:
        continue
    seen.add(key)
    uniq.append(r)

json.dump(uniq, open(os.path.join(DATA, "master_stage2.json"), "w"), indent=1)
print("stage2 records:", len(uniq))
from collections import Counter
print(Counter(r["area"] if r.get("area") else r["paper_id"][0] for r in uniq))
