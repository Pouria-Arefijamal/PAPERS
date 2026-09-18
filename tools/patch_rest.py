#!/usr/bin/env python3
"""Stage 9: drop residual off-topic records and characterise the remaining
network-relevant papers (the additions made from targeted search).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
recs = json.load(open(os.path.join(DATA, "master_full.json")))
by = {r["paper_id"]: r for r in recs}

DROP = {"L18", "L19", "L21", "L23", "L26", "L28", "L30", "L35", "L40", "L41",
        "L43", "L44", "L13", "L39", "L25", "L22", "L28"}
recs = [r for r in recs if r["paper_id"] not in DROP]
by = {r["paper_id"]: r for r in recs}

C = {}

C["F07"] = dict(is_survey=False, evaluation_quality="NA", reproducibility_quality="WEAK",
                limitations="Magazine article: identifies enablers and challenges for RAN slicing in verticals without new experiments.",
                research_gap="Defines vertical requirements (isolation, scheduling, SLA) that AI-native orchestration must satisfy.")

C["L01"] = dict(in_llm=True, network_domain="Network configuration",
                task="Benchmarking LLMs on network configuration: synthesising configurations from requirements, translating configurations across vendors, specifying routing algorithms, and configuration repair",
                model="Multiple LLMs compared", open_or_closed="Both",
                prompting="Task-specific prompting with structured inputs", rag="No", tool_calling="No",
                agent_architecture="Single-model prompting (offline benchmark)",
                network_actions="Generates configuration text; not deployed to a live network",
                recommendation_or_execution="Recommendation only (offline benchmark)",
                closed_loop="No", benchmark="NetConfEval (four configuration scenarios)",
                dataset="Public HuggingFace dataset (NetConfEval/NetConfEval)",
                metrics="Configuration correctness against reference configurations; task accuracy; partial token-cost reporting",
                llm_comparisons="Yes - multiple models against each other and against human-written configurations",
                code_available="Yes - https://github.com/RedHatResearch/conext24-NetConfEval",
                limitations="Static text-level benchmark: correctness is judged against reference configurations rather than by deploying them; no network KPI or SLA outcome.",
                research_gap="Network-configuration correctness is now benchmarked; the resulting network behaviour is not.")
C["L02"] = dict(in_llm=True, is_survey=True, network_domain="Networking (general)",
                task="Survey of LLM applications, enabling techniques and challenges in networking",
                limitations="Survey in IEEE Network: breadth over measured depth.",
                research_gap="Provides the task taxonomy used in this review and confirms that closed-loop control is under-explored.")
C["L03"] = dict(in_llm=True, in_eff=True, network_domain="5G network analysis",
                task="Instruction fine-tuning an open-source LLM for 5G network analysis (packet analysis, IP routing, performance analysis code generation)",
                model="LLaMA 2 13B", model_size="13B", open_or_closed="Open",
                fine_tuning="Yes", finetuning_method="Full instruction fine-tuning (SFT) with self-instruct data expansion",
                dataset="Own 5G network-analysis instruction set", training_data_size="15,111 instruction sets (packet analysis 20 manual + 2,000 self-instruct; IP routing 100 + 10,000; performance analysis 30 + 3,000)",
                training_hardware="NA", training_cost="NA", inference_latency="NA",
                peft="No", lora="No", qlora="No", pruning="No", quantization="No", distillation="No",
                accuracy="Network-analysis code-generation score 247/300 versus GPT-3.5 at 209/300",
                baseline="GPT-3.5", network_performance="NA",
                metrics="300-point code-generation rubric", network_metrics="No (no network KPI measured)",
                code_available="Yes - https://github.com/DNLab2024/Mobile-LLaMA",
                limitations="A single 300-point code-generation rubric; no network KPI and no closed-loop performance; the task is analysis-code generation rather than online control.",
                research_gap="The canonical demonstration that a fine-tuned open LLM can outperform a general-purpose model on a 5G analysis task - but the task is offline analysis, not action selection under a latency budget.")
C["L04"] = dict(in_llm=True, in_eff=True, network_domain="Telecommunications (general)",
                task="Building a telecom-specific LLM (three-stage recipe) and evaluating on telecom maths, QA and code tasks",
                model="General-purpose instruction-tuned LLM (specific checkpoint not reported)", open_or_closed="Open",
                fine_tuning="Yes", finetuning_method="Three stages: continual pre-training (causal LM), instruction tuning (SFT), alignment tuning via DPO",
                dataset="OpenTelecom (pre-training), TelecomInstruct (instruction), TelecomAlign (DPO)",
                training_data_size="1,679.5M training tokens for the pre-training corpus",
                training_hardware="NA (the paper cites hardware limits as the reason for its model choice)",
                training_cost="About 1.5 h of instruct-tuning on one 8-GPU node (per the source retrieved)",
                peft="No", lora="No", qlora="No", pruning="No", quantization="No", distillation="No",
                accuracy="Outperforms GPT-4, Llama-3 and Mistral on the Telecom Math Modelling benchmark; comparable on TeleQnA and 3GPP technical-document classification (75.30 versus GPT-4o 38.94 for tdoc classification)",
                baseline="GPT-4, Llama-3, Mistral", metrics="Task accuracy including 3GPP document classification",
                network_metrics="No (telecom text/knowledge tasks, not network management)",
                limitations="Measures telecom knowledge and text tasks rather than network-management quality; no network KPI and no closed loop.",
                research_gap="A well-documented domain-adaptation recipe, but the evaluation never touches a network. The 'does fine-tuning improve network-management performance?' question is left open by this paper.")
C["L05"] = dict(in_llm=True, network_domain="Networking (multimodal: video streaming, wireless scheduling, cuOpt)",
                task="Adapting large language models to networking tasks (NetLLM), covering viewport prediction for video streaming and adaptive bitrate, link scheduling in wireless networks, and cluster job scheduling",
                model="LLM backbone with task-specific lightweight adapters", open_or_closed="Open",
                prompting="Task-specific input encoders feeding the LLM", rag="No", tool_calling="No",
                fine_tuning="Partly (lightweight adapters trained per task)",
                agent_architecture="Single-model multi-task adaptation",
                evaluation_platform="Simulation environments per task",
                metrics="Task-specific performance (prediction accuracy, streaming QoE, scheduling performance)",
                code_available="Yes (public repository per the paper)",
                limitations="Each task needs its own adapter and input encoder, so it is not a general-purpose network agent; no closed-loop network control and no SLA-level evaluation.",
                network_metrics="Task-level QoE/scheduling metrics rather than end-to-end SLA compliance",
                research_gap="NetLLM established the 'adapt an LLM to a networking task' pattern; what is missing is a single model that acts on network state in a closed loop and is scored on service outcomes.")
C["L06"] = dict(in_llm=True, network_domain="Zero-touch network configuration management",
                task="Using LLMs for zero-touch network configuration management",
                limitations="Magazine article retrieved at metadata level; evaluation depth unverified.",
                research_gap="Configuration generation is the most mature LLM-for-networking application; verification and rollback safety remain open.")
C["L07"] = dict(in_llm=True, network_domain="O-RAN radio resource management",
                task="LLM-empowered radio resource management delivered as an O-RAN xApp",
                agent_architecture="xApp hosting LLM-based decision logic in the near-RT RIC",
                closed_loop="Yes (xApp control loop)",
                limitations="Short venue paper; whether LLM inference latency can meet near-RT RIC budgets (10 ms to 1 s) is not resolved.",
                research_gap="Placing an LLM inside a near-RT xApp raises a hard latency-feasibility question that only small or distilled models can answer.")
C["L08"] = dict(in_llm=True, network_domain="O-RAN resilience and slice resource allocation",
                task="LLM-driven agentic AI for O-RAN resilience, allocating resources across slices with distinct QoS requirements",
                agent_architecture="Agentic AI framework over O-RAN",
                closed_loop="Intended",
                limitations="Preprint-level evidence retrieved (TechRxiv); peer-reviewed venue and experimental depth unverified.",
                research_gap="O-RAN resilience plus slice resource allocation is precisely the intersection this PhD targets; the evaluation depth must be established before treating it as prior art.")
C["L09"] = dict(in_llm=True, network_domain="5G core management and orchestration (intent-based)",
                task="Semantic routing to improve LLM-assisted intent-based 5G core management and orchestration",
                prompting="Semantic routing of intents over candidate actions",
                rag="Partly (semantic routing over a candidate set)",
                agent_architecture="LLM intent translator with semantic routing",
                recommendation_or_execution="Intent-to-action translation (no end-to-end execution demonstrated)",
                closed_loop="No", metrics="Intent-translation accuracy and efficiency versus unrouted prompting",
                llm_comparisons="Yes",
                limitations="Translates intents but does not demonstrate the resulting network behaviour; no SLA measurement.",
                research_gap="Semantic routing addresses LLM scalability; verifying that translated intents achieve the intended service outcomes in a running core remains open.")
C["L10"] = dict(in_llm=True, network_domain="5G core intent management",
                task="LLMs for intent extraction in 5G core networks towards intent-based network management",
                agent_architecture="Single-model intent extraction", closed_loop="No",
                limitations="Intent extraction only; retrieved at metadata level.",
                research_gap="Intent extraction is a prerequisite step; assurance of extracted intents is the open part.")
C["L11"] = dict(in_llm=True, is_survey=True, network_domain="Network engineering automation",
                task="Survey of the state of the art and research directions for LLMs in network engineering automation",
                limitations="Survey; DOI not resolved in this session (NOMS 2026 record retrieved via OpenAlex).",
                research_gap="Most recent consolidated view of LLMs for network engineering automation.")
C["L12"] = dict(in_llm=True, is_survey=True, network_domain="Network management and operations",
                task="Comprehensive survey of LLM-based network management and operations",
                limitations="Survey (Wiley International Journal of Network Management).",
                research_gap="Confirms that LLM-based network management is dominated by advisory and knowledge tasks.")
C["L14"] = dict(in_llm=True, network_domain="NFV management and orchestration",
                task="Intent-based automated NFV management using LLMs to ensure service level objectives",
                agent_architecture="LLM-based intent automation for NFV management",
                closed_loop="Intended (SLO assurance is the stated aim)",
                limitations="Retrieved at abstract level; experimental depth unverified.",
                research_gap="Intent-based NFV management with SLO objectives is close to this PhD's target; the strength of its network-level evidence needs verification.")
C["L15"] = dict(in_llm=True, network_domain="Telecommunications industry",
                task="Discussion of the forthcoming impact of LLMs on the telecom industry",
                limitations="Magazine article: industry outlook rather than an experimental contribution.",
                research_gap="Frames industry expectations that the research literature has not yet met on closed-loop management.")
C["L17"] = dict(in_llm=True, network_domain="Telecommunications knowledge",
                task="TeleQnA benchmark for telecom knowledge of LLMs",
                benchmark="TeleQnA", dataset="Public - HuggingFace netop/TeleQnA",
                code_available="Yes - https://github.com/netop-team/TeleQnA",
                limitations="Static multiple-choice knowledge test; not a management benchmark.",
                research_gap="Telecom knowledge benchmarks are mature; management benchmarks are not.")
C["L20"] = dict(in_llm=True, network_domain="5G core on Kubernetes (autonomous fault remediation)",
                task="Benchmarking LLM agents for autonomous Kubernetes fault remediation on a 5G core",
                agent_architecture="Agentic diagnosis and remediation loop",
                recommendation_or_execution="Execution (remediation of a live deployment)",
                closed_loop="Yes - fault injection, diagnosis, remediation, execution-based verification",
                benchmark="OperAID scenarios (NetworkPolicy blocking AMF-SMF SBI, missing SMF ConfigMap, UPF scaled to zero)",
                metrics="Remediation success rate; per-run cost",
                llm_comparisons="Yes - 5 models x 2 tool conditions x 3 scenarios x 30 runs = 900 experiments",
                code_available="Yes - https://github.com/EricssonResearch/operaid",
                limitations="Faults are Kubernetes-level, not 3GPP protocol-level; no RAN; no SLA/KPI scoring.",
                research_gap="The closest existing closed-loop 5G-core benchmark; it defines the boundary of what remains unbenchmarked.")
C["L32"] = dict(in_llm=True, network_domain="Optical network automation",
                task="Telemetry and agentic AI as foundations for optical network automation",
                agent_architecture="Agentic AI over streaming telemetry",
                limitations="Article-level (TechRxiv) evidence; network-specific evaluation depth unverified.",
                research_gap="Optical networks are ahead of 5G cores in telemetry-driven agentic automation - a useful template.")
C["L34"] = dict(in_llm=True, network_domain="Network configuration synthesis",
                task="Tackling ambiguity in user intent for LLM-based network configuration synthesis",
                benchmark="Ambiguity-handling evaluation for configuration synthesis (ACM workshop)",
                limitations="Workshop paper focused on intent ambiguity, not network outcomes.",
                research_gap="Intent ambiguity is a real obstacle for autonomous network agents and is rarely handled in 5G/6G management work.")
C["L37"] = dict(in_llm=True, is_survey=True, network_domain="Telecommunication network operation and management",
                task="Survey of LLM-powered troubleshooting for telecom network operation and management (37 works screened)",
                limitations="Preprint survey (SSRN); organizes a scattered literature but reports no primary experiments.",
                research_gap="Confirms that telecom troubleshooting with LLMs is scattered across sub-domains without a unified problem formulation or benchmark.")

C["E04"] = dict(in_eff=True, network_task="Generic method (no network task) - foundational PEFT technique",
                base_model="Any transformer LLM", model_size="N/A (method)", fine_tuning="Yes",
                finetuning_method="Quantised low-rank adaptation: 4-bit NormalFloat quantisation, double quantisation, paged optimisers, LoRA adapters",
                quantization="Yes", peft="Yes", lora="Yes", qlora="Yes",
                training_hardware="Reported in the paper (single-GPU fine-tuning of large models); exact configuration not re-verified here",
                limitations="Generic ML method with no networking evaluation; included because networking papers cite it as their compression recipe.",
                research_gap="QLoRA makes fine-tuning accessible, but its effect on network-decision quality (as opposed to text quality) is unmeasured.")
C["E07"] = dict(in_eff=True, network_task="Generic method (no network task) - distillation",
                fine_tuning="Yes", finetuning_method="Transformer distillation (two-stage: general + task-specific)",
                distillation="Yes", model_size="BERT-base teacher to a much smaller student",
                accuracy="Retains most of BERT-base accuracy at a fraction of the size (exact figures in the paper)",
                limitations="Generic NLP method; no networking evaluation.",
                research_gap="Provides the distillation template that network-domain work adapts, but the model-size versus network-decision-quality curve remains unmeasured.")
C["E15"] = dict(in_eff=True, network_task="Intrusion detection in the Internet of Vehicles",
                base_model="BERT-based hybrid model", fine_tuning="Yes",
                peft="Partly (BERT-based adaptation)", dataset="Vehicular network intrusion datasets",
                limitations="Security classification rather than network management; compression is not the paper's focus.",
                research_gap="Shows BERT-class models remain competitive for network security tasks, but does not address management decisions.")
C["E26"] = dict(in_eff=True, network_task="Generic method (no network task) - foundational PEFT technique",
                fine_tuning="Yes", finetuning_method="Low-rank adaptation: freeze the pretrained weights and inject trainable rank-decomposition matrices into each layer",
                peft="Yes", lora="Yes",
                limitations="Generic ML method; no networking evaluation. Included because it is the adaptation technique used by most network-domain fine-tuning papers.",
                research_gap="LoRA is the default adaptation method in telecom-LLM work, yet at least two telecom studies report that it saturates on small models and prefer full fine-tuning - a tension that is unresolved for network-management tasks.")
C["E35"] = dict(in_eff=True, network_task="Network traffic classification",
                base_model="Transformer student distilled from a larger transformer teacher",
                distillation="Yes", finetuning_method="Knowledge distillation",
                model_size_after="4.61% of teacher parameters", inference_latency="0.93 ms per packet",
                accuracy="99.10% of teacher F1", network_performance="99.10% of teacher F1 at 4.61% of parameters, 7.33% of memory and 14.3x faster",
                limitations="Traffic classification rather than management; all figures are relative to an unspecified absolute baseline in the retrieved source.",
                research_gap="The best compression-to-quality ratio found in the networking corpus - evidence that distillation works for network *classification*, with no equivalent evidence for network *control decisions*.")
C["E37"] = dict(in_eff=True, is_survey=True, network_task="Generic method survey (compression for LLMs)",
                fine_tuning="Surveyed", pruning="Surveyed", quantization="Surveyed", distillation="Surveyed",
                peft="Surveyed", lora="Surveyed",
                limitations="Survey of generic LLM compression (TACL 2024); no networking content.",
                research_gap="Provides the taxonomy of compression methods that network-domain papers apply piecemeal.")
C["E38"] = dict(in_eff=True, network_task="Generic method (no network task) - structural LLM pruning",
                pruning="Yes", pruning_method="Structural pruning of LLM components (including attention heads) guided by the effect on the output",
                limitations="Generic NLP method; no networking evaluation.",
                research_gap="Structural pruning of genuine LLMs is established in NLP; no networking paper in this corpus prunes a billion-parameter LLM and evaluates the network task.")

C["O28"] = dict(in_orch=True, network_generation="6G", domain="RAN and core",
                orchestrator_type="F/E - agentic orchestration architecture (hierarchical agentic RAN and core)",
                architecture="Autonomous hierarchical agentic orchestration spanning RAN and core for AI-native 6G",
                closed_loop="Intended", limitations="Journal of limited visibility; retrieved at metadata level in this session.",
                research_gap="Hierarchical agentic orchestration across RAN and core is exactly the cross-domain combination this PhD targets; the paper's evaluation depth needs verification.")
C["O34"] = dict(in_orch=True, network_generation="6G", domain="6G network/application services",
                orchestrator_type="E/F - agentic AI management of 6G services",
                architecture="Agentic AI framework for autonomous management of 6G network and application services",
                closed_loop="Intended", limitations="Retrieved at metadata level (IEEE Xplore document 11318854).",
                research_gap="Agentic 6G service management is appearing in 2025-2026; SLA-level evaluation is the open part.")
C["O35"] = dict(in_orch=True, network_generation="5G", domain="End-to-end slicing",
                orchestrator_type="B - optimisation/learning algorithm for collaborative slice orchestration",
                architecture="Intelligent and collaborative orchestration of network slices",
                closed_loop="Partly", limitations="Retrieved at metadata level (IEEE Xplore document 9793722).",
                research_gap="Collaborative slice orchestration across domains remains thinly evaluated.")
C["O36"] = dict(in_orch=True, network_generation="5G", domain="Multi-domain",
                orchestrator_type="B/D - ML-based multi-domain actuation orchestration for end-to-end service quality assurance",
                architecture="Machine-learning-based multi-domain actuation orchestration supporting end-to-end service quality assurance",
                closed_loop="Yes (assurance loop)", sla_support="Yes",
                limitations="Retrieved at metadata level (IEEE Xplore document 9983829).",
                research_gap="Directly targets the multi-domain assurance loop that AI-native orchestration must close; comparison against LLM-based approaches is an open opportunity.")
C["O37"] = dict(in_orch=True, network_generation="B5G", domain="Multi-domain slices",
                orchestrator_type="B - SafeRL-based multi-domain slice orchestration",
                architecture="SafeSCHEMA: multi-domain slice orchestration using safe reinforcement learning",
                ml="Safe RL", closed_loop="Yes (RL loop)", network_slicing="Yes",
                limitations="Retrieved at metadata level (IEEE Xplore document 10001219).",
                research_gap="Safety-constrained RL orchestration is a key ingredient for trustworthy AI-native management and is rarely combined with LLM planning.")
C["O39"] = dict(in_orch=True, network_generation="5G/6G", domain="Network slicing",
                orchestrator_type="F - LLM-driven multi-agent slice management",
                architecture="LLM-driven multi-agent framework for autonomous network slice management, representing infrastructure as a graph",
                agent="Yes (multi-agent)", llm="Yes", closed_loop="Intended", network_slicing="Yes",
                limitations="Retrieved at abstract level (IEEE Xplore document 11573048).",
                research_gap="Multi-agent LLM slice management is the closest published combination to this PhD's target; its SLA-level evaluation needs verification.")
C["O40"] = dict(in_orch=True, network_generation="6G", domain="Core network",
                orchestrator_type="E/F - feasibility-shielded agentic framework for self-healing core networks",
                architecture="Agentic AI with a feasibility shield for 6G self-healing core networks",
                agent="Yes", closed_loop="Yes (self-healing loop)",
                limitations="Retrieved at metadata level (IEEE Xplore document 11577510).",
                research_gap="Feasibility shielding is precisely the safety mechanism that agentic network control needs; combining it with optimisation-based feasibility (rather than learned shields) is open.")

C["M38"] = dict(in_multipath=True, protocol="MPTCP", network_generation="4G",
                architecture="DAPS: delay-aware packet scheduling for multipath transport",
                scheduler_location="Sender-side MPTCP scheduler",
                input_parameters="Per-path delay estimates and delivery-rate estimates",
                path_metrics="Delay, delivery rate", decision_type="Packet-to-subflow assignment minimising expected delivery delay",
                packet_or_flow="Packet-level", reordering_handling="Delay-aware assignment reduces reordering",
                objective="Minimise delivery delay across paths",
                algorithm="DAPS heuristic (compare estimated delivery times across subflows)",
                ml_method="No", simulator="NA", testbed="Linux MPTCP implementation",
                baselines="Default lowest-RTT-first scheduler",
                limitations="Heuristic; no learning; transport-level objective only.",
                research_gap="One of the earliest delay-aware MPTCP schedulers and a standard baseline for latency-oriented multipath work.")
C["M42"] = dict(in_multipath=True, protocol="MPQUIC", network_generation="5G",
                architecture="Improved MPQUIC scheduler based on multi-agent reinforcement learning",
                scheduler_location="Sender-side MPQUIC scheduler",
                decision_type="Packet-to-path assignment learned by multiple agents",
                packet_or_flow="Packet-level", ml_method="Yes (multi-agent RL)",
                objective="Improve MPQUIC performance on heterogeneous paths",
                limitations="Retrieved at metadata level (IEICE Transactions on Information and Systems).",
                research_gap="One of the few multi-agent RL MPQUIC schedulers; no network-level (orchestrator/slice) objective.")
C["M43"] = dict(in_multipath=True, protocol="ATSSS over 5G core", network_generation="5G",
                architecture="Deep reinforcement learning for access traffic splitting decision-making in the 5G core",
                scheduler_location="5G core (ATSSS decision function)",
                decision_type="Access traffic split ratio per flow",
                packet_or_flow="Flow-level splitting", ml_method="Yes (DRL)",
                closed_loop="Yes (core-level decision loop)", network_generation_extra="",
                limitations="Retrieved at metadata level (IEEE Xplore document 10826899).",
                research_gap="This is the multipath/5G-core intersection: DRL decides splitting in the core. Coupling it to a higher-level orchestrator objective is not addressed.")
C["M44"] = dict(in_multipath=True, protocol="ATSSS over 5G core", network_generation="5G",
                architecture="Autonomous access traffic splitting via the 5G core, balancing QoS and return on investment with multi-objective reinforcement learning",
                scheduler_location="5G core (ATSSS decision function)",
                decision_type="Access traffic split balancing QoS and ROI",
                packet_or_flow="Flow-level splitting", ml_method="Yes (multi-objective RL)",
                objective="Balance QoS against return on investment", closed_loop="Yes",
                limitations="Retrieved at metadata level (IEEE Xplore document 11133925).",
                research_gap="Brings a business objective (ROI) into multipath splitting - a step towards SLA/business-aware multipath control, still without an orchestrator or LLM in the loop.")
C["M45"] = dict(in_multipath=True, protocol="MPTCP", network_generation="5G",
                architecture="Reinforcement-learning-based multipath scheduling for heterogeneous wireless networks",
                scheduler_location="Sender-side scheduler with an RL agent",
                decision_type="Packet-to-subflow assignment", packet_or_flow="Packet-level",
                ml_method="Yes (RL)",
                limitations="Retrieved at metadata level (IEEE Xplore document 10152217).",
                research_gap="Reinforcement learning is now a standard tool for multipath scheduling; the missing ingredient is network-level objective provision.")
C["M46"] = dict(in_multipath=True, protocol="MPQUIC", network_generation="5G/B5G + satellite (hybrid)",
                architecture="PRISM: PPO-based intelligent scheduling for multipath QUIC in heterogeneous hybrid 5G/B5G-satellite networks",
                scheduler_location="Sender-side MPQUIC scheduler",
                number_of_paths="Multiple (terrestrial and satellite paths)",
                path_type="Heterogeneous terrestrial + non-terrestrial",
                decision_type="Packet-to-path assignment", packet_or_flow="Packet-level",
                ml_method="Yes (PPO)", closed_loop="Yes (online learning)",
                limitations="Very recent (2026, Computer Communications); evaluation depth not verified in this session.",
                research_gap="Non-terrestrial plus terrestrial multipath with PPO is an emerging combination; integration with 6G orchestration and SLA objectives is open.")
C["M47"] = dict(in_multipath=True, protocol="MPQUIC", network_generation="5G",
                architecture="MobStream: reinforcement-driven mobile streaming over multipath QUIC",
                scheduler_location="Sender-side MPQUIC scheduler",
                decision_type="Scheduling decisions for streaming traffic", packet_or_flow="Packet/segment-level",
                ml_method="Yes (RL)", objective="Improve streaming QoE over multipath",
                limitations="Application-specific (streaming); retrieval at metadata level only.",
                research_gap="Streaming QoE objectives for multipath schedulers are application-level; mapping network-level SLA objectives into the scheduler is unexplored here.")

C["F45"] = dict(is_survey=True, evaluation_quality="NA", reproducibility_quality="WEAK",
                limitations="Survey of SDN routing and traffic engineering; no primary experiments.",
                research_gap="Provides the classical TE taxonomy that AI-native TE must be positioned against.")
C["F46"] = dict(is_survey=True, evaluation_quality="NA", reproducibility_quality="WEAK",
                limitations="Survey of DRL for TE in SDN; no primary experiments.",
                research_gap="Consolidates DRL-for-TE results and shows that most evaluations use custom simulators with limited realism.")

for k, v in C.items():
    if k not in by:
        continue
    v.setdefault("evidence", by[k].get("evidence", "SUB"))
    by[k].update(v)
    by[k]["_recompute"] = True

json.dump(recs, open(os.path.join(DATA, "master_full.json"), "w"), indent=1)
print("stage9: characterised", len(C), "| dropped", len(DROP), "| total", len(recs))
