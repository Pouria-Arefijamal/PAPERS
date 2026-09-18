#!/usr/bin/env python3
"""Stage 6: LLM/agent (Area 4) and efficiency (Area 5) characterizations.

Area 4 facts come from the benchmark-landscape research report
(netllm-bench/llm-network-benchmarks-survey.md) and from full texts read in this
session. Area 5 facts come from llm-net-papers/papers.json, whose entries name
the source URL used for each field, plus the compression report.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
recs = json.load(open(os.path.join(DATA, "master_stage5.json")))
by = {r["paper_id"]: r for r in recs}

NR = "NA"
C = {}

# ============================== AREA 4 =====================================
C["L46"] = dict(
    in_llm=True, network_domain="Network configuration (device config, routing algorithms)",
    task="Network configuration synthesis and validation; comparing LLM configurations against ground truth",
    model="Multiple LLMs (specific set per paper)", model_size="NR", open_or_closed="Both",
    prompting="Zero-shot and few-shot templates", rag="No", tool_calling="No", function_calling="No",
    agent_architecture="Single-model prompting (no agent loop)",
    number_of_agents="1", planner="No", executor="No", critic="No", memory="No",
    network_tools="No (text-to-configuration only)",
    network_actions="Generates device configurations for evaluation; not applied to a live network",
    recommendation_or_execution="Recommendation only (offline benchmark)",
    closed_loop="No",
    benchmark="NetConfEval (four configuration scenarios: synthesising configurations from requirements, translating configurations across vendors, specifying routing algorithms, configuration repair)",
    dataset="Public dataset released with the paper (HuggingFace NetConfEval)",
    metrics="Configuration correctness/quality against ground truth; task-specific accuracy",
    llm_comparisons="Yes - multiple LLMs compared against each other and against human-written configurations",
    network_metrics="No (no live network KPIs)",
    hallucination_evaluation="Partly - incorrect configurations are counted as errors, but no dedicated hallucination metric",
    latency="Not a primary metric", token_cost="Partly reported",
    baselines="Human-written/gold configurations; other LLMs",
    code_available="Yes - https://github.com/RedHatResearch/conext24-NetConfEval and a public HuggingFace dataset",
    limitations="Static, text-level benchmark: correctness is judged against reference configurations, not by deploying them; no closed-loop interaction with a network; no SLA/KPI outcome.",
    research_gap="NetConfEval measures configuration correctness, not network behaviour. A benchmark that deploys the configuration and measures the resulting service quality is still missing.",
    source_url="https://doi.org/10.1145/3656296", evidence="ABS",
)

C["L47"] = dict(
    in_llm=True, network_domain="Network troubleshooting / incident diagnosis (data centre to ISP networks)",
    task="Benchmarking LLM agents on network incident detection, fault localisation and root-cause identification",
    model="GPT-OSS, GPT-5, GPT-5-mini (as evaluated)", model_size="NR", open_or_closed="Both",
    prompting="ReAct-style reasoning agent with a system prompt listing available tools",
    rag="No", tool_calling="Yes - Model Context Protocol (MCP)", function_calling="Yes (MCP tools)",
    agent_architecture="ReAct reasoning agent connected to a network environment through an Agent Access Layer",
    number_of_agents="1 (monolithic; the paper notes more complex agent graphs are supported)",
    planner="Implicit (ReAct reasoning)", executor="Yes (tool calls executed in the emulated network)",
    critic="No (the evaluator scores the final answer)", memory="Conversation history",
    network_tools="More than 30 monitoring and troubleshooting tools: sketches, In-band Network Telemetry, SDN controller APIs, switch CLIs",
    network_actions="Read-only diagnosis in the benchmarked incidents (enable INT, query telemetry, probe paths) - detection, localisation and root-cause tasks",
    recommendation_or_execution="Execution of diagnostic actions against an emulated network; not remediation of a production network",
    closed_loop="Yes for diagnosis (agent actions change telemetry collection), but no automated remediation loop",
    benchmark="NIKA - hundreds of curated incidents over five network scenarios, 54 representative network issues, 640 distinct troubleshooting incidents",
    dataset="Public dataset of agent behaviour with more than 900 reasoning traces (Zenodo DOI 10.5281/zenodo.17971675)",
    metrics="Detection success, fault localisation accuracy, root-cause identification accuracy, time to detection, tool usage patterns",
    llm_comparisons="Yes - three models compared",
    network_metrics="Diagnostic outcomes rather than service KPIs (no SLA/latency/throughput scoring)",
    hallucination_evaluation="Partly - wrong root causes are scored as errors",
    latency="Reported indirectly via time to detection", token_cost="No",
    baselines="Cross-model comparison; no non-LLM diagnostic baseline reported",
    code_available="Yes - https://github.com/sands-lab/nika",
    limitations="Preprint (arXiv:2512.16381); incidents are IP/data-centre/campus/ISP scenarios - no 5G core, RAN or slice management; scores diagnosis, not service outcomes; no cost metric.",
    research_gap="NIKA proves a curated, executable troubleshooting benchmark is feasible - and simultaneously shows that no equivalent exists for 5G/6G core or RAN management with SLA-level scoring.",
    source_url="https://arxiv.org/abs/2512.16381", evidence="FULL", peer_reviewed=False, arxiv="2512.16381",
)

C["L48"] = dict(
    in_llm=True, network_domain="Network automation and configuration (IP networks)",
    task="Dynamic benchmarking of AI agents on network automation tasks (configuration synthesis, fault diagnosis, traffic engineering, capacity planning)",
    model="Multiple LLM agents evaluated", model_size="NR", open_or_closed="Both",
    prompting="Agent-specific", rag="No", tool_calling="Yes", function_calling="Yes",
    agent_architecture="Agent-with-tools over emulated network scenarios",
    number_of_agents="1 per task (agent frameworks compared)", planner="Agent-dependent", executor="Yes",
    critic="No", memory="Agent-dependent",
    network_tools="Emulated network control and telemetry APIs",
    network_actions="Configuration and diagnosis actions applied in the emulated environment",
    recommendation_or_execution="Execution in emulation",
    closed_loop="Yes within the emulated scenario",
    benchmark="NetArena - dynamically generated tasks designed to resist pretraining contamination, with stated attention to statistical power",
    dataset="Generated at runtime (dynamic by design)",
    metrics="Task correctness, step-wise safety, latency; contamination and statistical-power analysis",
    llm_comparisons="Yes", network_metrics="Emulated network outcomes rather than SLA guarantees",
    hallucination_evaluation="Safety is decoupled from correctness and scored, which catches unsafe steps",
    latency="Yes", token_cost="NR",
    baselines="Multiple LLM agents", code_available="Yes - https://github.com/Froot-NetSys/NetArena",
    limitations="Peer-reviewed at ICLR 2026, but the scenarios are IP/enterprise/datacentre; the authors concede limited coverage of cross-domain scenarios; no 5G core, RAN, slicing or SLA-level outcome scoring.",
    research_gap="NetArena is the strongest methodological template (dynamic generation, contamination control, safety decoupled from correctness) that a 5G/6G management benchmark should imitate.",
    source_url="https://arxiv.org/abs/2506.03231", evidence="SUB",
)

C["L49"] = dict(
    in_llm=True, network_domain="5G Core (cloud-native, Kubernetes) network operations",
    task="Autonomous operation of a 5G core: fault injection, agentic diagnosis, remediation and execution-based verification",
    model="Five models evaluated, best reported as Qwen3.5-35B-A3B", model_size="NR (35B class for the best model)",
    open_or_closed="Both (open-weight model performs best)",
    prompting="Agent prompting over an operational toolset", rag="No", tool_calling="Yes",
    function_calling="Yes", agent_architecture="Agentic operator with diagnosis-then-remediation loop and execution-based verification",
    number_of_agents="1", planner="Yes (diagnosis planning)", executor="Yes (remediation commands)",
    critic="Verification step (execution-based)", memory="Run history",
    network_tools="Kubernetes and 5G-core operational tools (pod/service inspection, configuration inspection, scaling)",
    network_actions="Real remediation of a running Open5GS + UERANSIM deployment on Kubernetes",
    recommendation_or_execution="Execution (closed loop against a live 5G core deployment)",
    closed_loop="Yes - fault injection, diagnosis, remediation, verification",
    benchmark="OperAID scenarios: NetworkPolicy blocking AMF-SMF SBI (port 7777), missing SMF ConfigMap causing CrashLoopBackOff, UPF scaled to zero",
    dataset="Scenarios and Helm charts in the public repository",
    metrics="Remediation success rate, cost per run",
    llm_comparisons="Yes - 5 models x 2 tool conditions x 3 scenarios x 30 runs = 900 experiments",
    network_metrics="Deployment-level health rather than 3GPP service KPIs",
    hallucination_evaluation="No", latency="Partly (run cost reported)", token_cost="Yes (per-run cost)",
    baselines="Same agent without tools; cross-model comparison",
    code_available="Yes - https://github.com/EricssonResearch/operaid",
    limitations="Faults are Kubernetes-level (NetworkPolicy, ConfigMap, replica scaling), not 3GPP protocol-level (NAS/NGAP/PFCP/SBI semantics are not exercised); no RAN; no SLA/KPI scoring; venue reported inconsistently between the repository BibTeX and Crossref.",
    research_gap="OperAID is the closest existing closed-loop 5G-core benchmark and it defines the boundary precisely: infrastructure remediation on a 5G core is benchmarked, 3GPP-level management with service-level outcomes is not.",
    source_url="https://doi.org/10.1109/NetSoft70012.2026.11603505", evidence="SUB",
)

C["L50"] = dict(
    in_llm=True, network_domain="Telecommunications knowledge (general, incl. standards)",
    task="Assessing telecom knowledge of LLMs through multiple-choice questions",
    model="Multiple LLMs including GPT-3.5/GPT-4 class models", model_size="NR", open_or_closed="Both",
    prompting="Zero-shot and few-shot question answering", rag="No", tool_calling="No", function_calling="No",
    agent_architecture="Single-model QA", number_of_agents="1", planner="No", executor="No", critic="No", memory="No",
    network_tools="No", network_actions="None", recommendation_or_execution="Neither - knowledge assessment",
    closed_loop="No", benchmark="TeleQnA - a large set of telecom multiple-choice questions generated from standards and research literature",
    dataset="Public - HuggingFace netop/TeleQnA", metrics="Question-answering accuracy",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="No",
    latency="No", token_cost="No", baselines="Cross-model comparison and human expert performance",
    code_available="Yes - https://github.com/netop-team/TeleQnA",
    limitations="Static multiple-choice knowledge test - explicitly not a network-management benchmark; contamination-prone; no tool use, no actuation and no network KPI. Later work (Free-Text Evaluation of LLMs for 5G) argues MCQ scores overstate telecom-LLM capability.",
    research_gap="Knowledge benchmarks are now mature for telecom; the missing object is the closed-loop management benchmark, not another QA set.",
    source_url="https://doi.org/10.1109/MNET.2025.3576035", evidence="SUB",
)

C["L51"] = dict(
    in_llm=True, network_domain="Telecommunications (reasoning, optimisation scenarios)",
    task="Static reasoning and knowledge evaluation of LLMs in telecom, including network-optimisation scenario questions",
    model="Multiple LLMs evaluated", model_size="NR", open_or_closed="Both",
    prompting="Task-specific (conceptual QA, math/logic reasoning, optimisation scenarios)",
    rag="No", tool_calling="No", function_calling="No", agent_architecture="Single-model evaluation",
    number_of_agents="1", planner="No", executor="No", critic="No", memory="No", network_tools="No",
    network_actions="None", recommendation_or_execution="Neither - evaluation suite", closed_loop="No",
    benchmark="LDOT - a multi-part benchmark for evaluating LLMs in telecom",
    dataset="NR (dataset URL not verified)", metrics="Accuracy per task category",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="No", latency="No", token_cost="No",
    baselines="Cross-model comparison", code_available="NR",
    limitations="Static suite published in IEEE JSAC; scenarios are posed as questions rather than executed; no closed loop, no service-level outcomes.",
    research_gap="Even the JSAC-level benchmark for telecom LLMs is static. That strengthens the case that an executable, SLA-scored 5G/6G management benchmark is a genuine contribution rather than a duplication.",
    source_url="https://doi.org/10.1109/JSAC.2025.3641905", evidence="SUB",
)

C["L52"] = dict(
    in_llm=True, network_domain="Network troubleshooting",
    task="Symptom-aware diagnostic escalation for LLM-based network troubleshooting (an agent design evaluated on NIKA)",
    model="LLMs per the paper", model_size="NR", open_or_closed="NR",
    prompting="Symptom-aware escalation strategy", rag="NR", tool_calling="Yes", function_calling="Yes",
    agent_architecture="Agent that escalates diagnostic actions based on observed symptoms",
    number_of_agents="1", planner="Yes (escalation planning)", executor="Yes", critic="NR", memory="NR",
    network_tools="Diagnostic tools exposed by NIKA", network_actions="Diagnostic actions in the emulated network",
    recommendation_or_execution="Execution of diagnostics (not remediation)", closed_loop="Within a diagnostic episode",
    benchmark="NIKA", dataset="NIKA dataset", metrics="Diagnostic accuracy and escalation efficiency",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="No", latency="NR", token_cost="NR",
    baselines="Baseline agents on NIKA", code_available="NR",
    limitations="An agent-design paper rather than a benchmark; inherits NIKA's scope (IP-network troubleshooting, no 5G core, no SLA scoring).",
    research_gap="Shows agent design (how to sequence diagnostics) materially affects troubleshooting performance - a design axis that any 5G/6G management agent evaluation must control for.",
    source_url="https://doi.org/10.1109/LCN67947.2026.11660797", evidence="SUB",
)

C["L53"] = dict(
    in_llm=True, network_domain="3GPP standards understanding",
    task="LLM understanding of 3GPP specifications; dataset construction and RAG evaluation",
    model="GPT-4 class and others", model_size="NR", open_or_closed="Both",
    prompting="Zero-shot with retrieved specification text", rag="Yes (the paper's focus is RAG over specifications)",
    tool_calling="No", function_calling="No", agent_architecture="Retrieval-augmented QA",
    number_of_agents="1", planner="No", executor="No", critic="No", memory="Retrieved context",
    network_tools="No", network_actions="None", recommendation_or_execution="Neither - knowledge/RAG evaluation",
    closed_loop="No", benchmark="TSpec-LLM dataset (about 30,137 3GPP documents, 13.5 GB)",
    dataset="Public - HuggingFace rasoul-nikbakht/TSpec-LLM",
    metrics="QA accuracy with and without retrieval", llm_comparisons="Yes",
    network_metrics="No", hallucination_evaluation="No", latency="NR", token_cost="NR",
    baselines="No-retrieval baselines", code_available="Dataset public",
    limitations="Static standards QA; no network action, no execution, no SLA metric.",
    research_gap="Shows RAG over 3GPP is workable and materially improves accuracy - the enabling component for a standards-grounded management agent.",
    source_url="https://doi.org/10.1109/GCWkshp64532.2024.11101012", evidence="SUB",
)

C["L54"] = dict(
    in_llm=True, network_domain="Telecommunications standards / knowledge",
    task="Retrieval-augmented generation over telecom standards (3GPP)",
    model="Open LLMs with retrieval", model_size="NR", open_or_closed="Open",
    prompting="RAG-specific prompting and retrieval strategy", rag="Yes (core contribution)",
    tool_calling="No", function_calling="No", agent_architecture="RAG pipeline tailored to telecom documents",
    number_of_agents="1", planner="No", executor="No", critic="No", memory="Retrieved chunks",
    network_tools="No", network_actions="None", recommendation_or_execution="Neither - text generation/QA",
    closed_loop="No", benchmark="Telecom standards QA", dataset="NR", metrics="Retrieval and answer quality",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="Partly (retrieval grounding)",
    latency="NR", token_cost="NR", baselines="Vanilla RAG", code_available="NR",
    limitations="Text-level; no network action; telecom documents differ from operational telemetry.",
    research_gap="Telecom-specific RAG is being solved; the unsolved part is grounding *actions* (not answers) in standards and verifying them against network state.",
    source_url="https://doi.org/10.1109/GLOBECOM52923.2024.10901155", evidence="SUB",
)

C["L55"] = dict(
    in_llm=True, network_domain="Telecommunications standards / knowledge",
    task="RAG and LLM-based question answering over telecom standards",
    model="Open LLMs", model_size="NR", open_or_closed="Open",
    prompting="RAG prompting", rag="Yes", tool_calling="No", function_calling="No",
    agent_architecture="RAG pipeline", number_of_agents="1", planner="No", executor="No", critic="No",
    memory="Retrieved context", network_tools="No", network_actions="None",
    recommendation_or_execution="Neither - QA", closed_loop="No",
    benchmark="Telecom standards QA", dataset="NR", metrics="Answer accuracy",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="Partly", latency="NR", token_cost="NR",
    baselines="Standard RAG", code_available="NR",
    limitations="Knowledge/QA contribution; no management action, no evaluation of network outcomes.",
    research_gap="Confirms that retrieval over standards is maturing while standards-grounded *action generation and verification* remains open.",
    source_url="https://doi.org/10.1145/3711992.3711996", evidence="SUB",
)

C["L56"] = dict(
    in_llm=True, network_domain="5G Core management and orchestration (intent-based)",
    task="Intent-based 5G core management: mapping natural-language intents to management and orchestration actions using an LLM with semantic routing",
    model="LLM-based with semantic routing over candidate intents", model_size="NR", open_or_closed="NR",
    prompting="Semantic routing of intents to reduce prompt complexity", rag="Partly (semantic routing over candidate actions)",
    tool_calling="NR", function_calling="NR", agent_architecture="LLM intent translator with a semantic routing layer",
    number_of_agents="1", planner="Intent planner", executor="NR", critic="No", memory="NR",
    network_tools="5G core management/orchestration APIs (conceptual)", network_actions="Management/orchestration actions derived from intents",
    recommendation_or_execution="Intent-to-action translation (execution not demonstrated end to end)",
    closed_loop="No", benchmark="Intent translation accuracy", dataset="NR",
    metrics="Intent-translation accuracy and efficiency versus non-routed prompting",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="No", latency="Partly", token_cost="Partly",
    baselines="Direct prompting without semantic routing", code_available="NR",
    limitations="Translates intents into management actions but does not demonstrate the resulting network behaviour; no SLA or service-level measurement.",
    research_gap="Semantic routing addresses LLM scalability for intent translation; the missing link is verifying that translated intents produce the intended service outcomes in a running 5G core.",
    source_url="https://doi.org/10.1109/GLOBECOM52923.2024.10901065", evidence="BIB",
)

C["L57"] = dict(
    in_llm=True, network_domain="O-RAN radio resource management (xApp)",
    task="LLM-empowered radio resource management delivered as an O-RAN xApp",
    model="LLM-based xApp", model_size="NR", open_or_closed="NR", prompting="NR", rag="NR",
    tool_calling="NR", function_calling="NR", agent_architecture="xApp hosting an LLM decision component",
    number_of_agents="1", planner="NR", executor="NR", critic="NR", memory="NR",
    network_tools="O-RAN E2 interface (xApp position)", network_actions="Radio resource management decisions in the RIC",
    recommendation_or_execution="Execution within the RIC control loop (per the paper's placement of the LLM in an xApp)",
    closed_loop="Yes (xApp control loop)", benchmark="NR", dataset="NR", metrics="NR",
    llm_comparisons="NR", network_metrics="RAN KPIs", hallucination_evaluation="No", latency="NR", token_cost="NR",
    baselines="Conventional xApp/optimisation baselines", code_available="NR",
    limitations="Short venue paper; the central open question for LLM-in-xApp designs is whether LLM inference latency can meet near-real-time (10 ms-1 s) RIC budgets - this is not resolved here.",
    research_gap="Placing an LLM inside a near-RT xApp raises a hard latency-feasibility question that only small/distilled models can answer; that trade-off is largely unmeasured.",
    source_url="https://doi.org/10.14722/futureg.2025.23057", evidence="BIB",
)

C["L58"] = dict(
    in_llm=True, network_domain="Intent-based networking (end-to-end)",
    task="End-to-end intent-based networking with LLMs, including intent translation and conflict detection; introduces the IBNBench benchmark inside the paper",
    model="33 LLMs evaluated (1.1B-70B)", model_size="1.1B to 70B",
    open_or_closed="Mostly open-weight", prompting="Task-specific intent-translation prompting", rag="NR",
    tool_calling="Yes (interaction with ODL/ONOS controllers per the report)", function_calling="NR",
    agent_architecture="LLM intent pipeline with controller integration",
    number_of_agents="1 per task", planner="Intent decomposition", executor="Controller actions",
    critic="Conflict detection component", memory="NR",
    network_tools="OpenDaylight / ONOS controller APIs",
    network_actions="Intent deployment to SDN controllers",
    recommendation_or_execution="Execution against controllers (intent installation)",
    closed_loop="Partly", benchmark="IBNBench (within NetIntent)", dataset="NR",
    metrics="Intent translation accuracy, conflict detection performance",
    llm_comparisons="Yes - 33 models, 1.1B-70B",
    network_metrics="No service-level metrics", hallucination_evaluation="No", latency="NR", token_cost="NR",
    baselines="Cross-model comparison", code_available="NR",
    limitations="Translation and conflict detection are evaluated; the network outcome of installing the intent is not scored. The paper's own finding that model size is a weak predictor of intent-translation quality is important.",
    research_gap="A 33-model study is exactly the kind of evidence needed for model selection in network agents - and it shows larger is not reliably better, which motivates small/distilled network models.",
    source_url="https://doi.org/10.1109/OJCOMS.2025.3642642", evidence="SUB",
)

C["L59"] = dict(
    in_llm=True, network_domain="Network engineering automation (general)",
    task="Survey of LLMs for network engineering automation",
    model="N/A (survey)", model_size="N/A", open_or_closed="N/A", prompting="Surveyed", rag="Surveyed",
    tool_calling="Surveyed", function_calling="Surveyed", agent_architecture="Surveyed",
    number_of_agents="N/A", planner="Surveyed", executor="Surveyed", critic="Surveyed", memory="Surveyed",
    network_tools="Surveyed", network_actions="Surveyed", recommendation_or_execution="Surveyed",
    closed_loop="Surveyed", benchmark="Surveyed", dataset="Surveyed", metrics="Surveyed",
    llm_comparisons="Surveyed", network_metrics="Surveyed", hallucination_evaluation="Surveyed",
    latency="Surveyed", token_cost="Surveyed", baselines="N/A", code_available="N/A",
    limitations="Survey; venue/DOI not fully resolved in this session (IEEE Xplore document 11668163 retrieved without a resolvable DOI).",
    research_gap="Provides the most recent consolidated view of LLMs for network engineering; should be re-checked once the DOI resolves.",
    source_url="https://ieeexplore.ieee.org/document/11668163", evidence="BIB", is_survey=True,
)

C["L60"] = dict(
    in_llm=True, network_domain="Network operations (NetOps) knowledge",
    task="Empirical study of the NetOps capability of pretrained LLMs (NetEval) - the earliest dedicated NetOps benchmark",
    model="26 LLMs evaluated", model_size="NR", open_or_closed="Both",
    prompting="Question answering", rag="No", tool_calling="No", function_calling="No",
    agent_architecture="Single-model QA", number_of_agents="1", planner="No", executor="No", critic="No", memory="No",
    network_tools="No", network_actions="None", recommendation_or_execution="Neither - knowledge evaluation",
    closed_loop="No", benchmark="NetEval - 5,732 NetOps questions across five NetOps sub-domains",
    dataset="Public - HuggingFace NASP/neteval-exam", metrics="Accuracy",
    llm_comparisons="Yes - 26 LLMs; only GPT-4 was found human-competitive",
    network_metrics="No", hallucination_evaluation="No", latency="No", token_cost="No",
    baselines="Human expert performance", code_available="Dataset public",
    limitations="Preprint (arXiv:2309.05557), static QA, no agentic tool use and no 5G/6G specificity.",
    research_gap="Establishes that NetOps knowledge evaluation predates the agent era; the field moved from knowledge to tool use, but not yet to closed-loop service outcomes.",
    source_url="https://arxiv.org/abs/2309.05557", evidence="SUB", peer_reviewed=False, arxiv="2309.05557",
)

C["L61"] = dict(
    in_llm=True, network_domain="Telecom network operations (operator agent trajectories)",
    task="Benchmarking LLMs on authentic live-network operator agent trajectories: intent recognition, entity extraction, event verification, tool invocation, root-cause analysis, solution generation",
    model="Eight state-of-the-art LLMs evaluated", model_size="NR", open_or_closed="Both",
    prompting="Task-specific", rag="NR", tool_calling="Yes (tool invocation is one of the six tasks)",
    function_calling="NR", agent_architecture="Agent trajectory evaluation",
    number_of_agents="1", planner="Evaluated", executor="Evaluated (tool invocation task)", critic="No",
    memory="Trajectory context", network_tools="Operator agent tools (live-network trajectories)",
    network_actions="Tool invocation and solution generation are scored; not executed against a live network by the benchmark itself",
    recommendation_or_execution="Mixed - includes procedural execution tasks in the trajectory",
    closed_loop="No", benchmark="TeleCom-Bench - 22,678 samples across six tasks",
    dataset="Built from authentic live-network operator agent trajectories",
    metrics="Per-task accuracy, including a reported 'universal Execution Wall': about 90% on linguistic interface tasks versus about 30% on procedural execution",
    llm_comparisons="Yes - eight SOTA LLMs", network_metrics="No", hallucination_evaluation="No",
    latency="NR", token_cost="NR", baselines="Cross-model comparison",
    code_available="Yes - https://github.com/ZTE-AICloud/TeleCom-Bench",
    limitations="KDD 2026 benchmark built from operator trajectories with a partially closed dataset; scores task-level correctness rather than resulting network service quality.",
    research_gap="The 'Execution Wall' (strong language understanding, weak procedural execution) is third-party evidence for exactly the gap this survey identifies: LLMs can talk about network operations far better than they can perform them.",
    source_url="https://doi.org/10.1145/3770855.3817480", evidence="SUB",
)

C["L62"] = dict(
    in_llm=True, network_domain="Cross-domain orchestration",
    task="Cross-domain orchestration task automation with a multi-agent LLM framework",
    model="LLM-based multi-agent", model_size="NR", open_or_closed="NR", prompting="Agent role prompting",
    rag="NR", tool_calling="Yes", function_calling="NR",
    agent_architecture="Multi-agent LLM framework for orchestration tasks",
    number_of_agents="Multiple (exact count NR)", planner="Yes", executor="Yes", critic="NR", memory="NR",
    network_tools="Orchestration APIs (NR)", network_actions="Orchestration task execution",
    recommendation_or_execution="Execution of orchestration tasks", closed_loop="Partially",
    benchmark="NR", dataset="NR", metrics="Task automation success", llm_comparisons="NR",
    network_metrics="No", hallucination_evaluation="No", latency="NR", token_cost="NR", baselines="NR",
    code_available="NR",
    limitations="Retrieved at metadata level only in this session; the extent to which orchestration actions are executed on real infrastructure versus simulated is not verified.",
    research_gap="Multi-agent LLM orchestration across domains is being attempted, but with limited evidence on real multi-domain infrastructure and no SLA-level scoring.",
    source_url="https://ieeexplore.ieee.org/document/11047162", evidence="BIB",
)

C["L63"] = dict(
    in_llm=True, network_domain="Intent-driven network configuration (management plane)",
    task="LLM-empowered intent-driven network configuration generation",
    model="LLM-based", model_size="NR", open_or_closed="NR", prompting="Intent-to-configuration prompting",
    rag="NR", tool_calling="NR", function_calling="NR",
    agent_architecture="Intent-driven configuration generator",
    number_of_agents="1", planner="Intent parsing", executor="Configuration generation", critic="NR", memory="NR",
    network_tools="Configuration/validation tooling (NR)", network_actions="Generation of device/network configuration",
    recommendation_or_execution="Configuration generation (deployment not verified)", closed_loop="No",
    benchmark="NR", dataset="NR", metrics="Configuration generation quality", llm_comparisons="NR",
    network_metrics="No", hallucination_evaluation="NR", latency="NR", token_cost="NR", baselines="NR",
    code_available="NR",
    limitations="A method paper (IEEE TNSM 2026), not a benchmark; whether generated configuration was deployed and validated on live equipment is not verified in this session.",
    research_gap="Confirms that IEEE TNSM now publishes LLM-for-management methods; the benchmark/closed-loop side remains thinner than the method side.",
    source_url="https://doi.org/10.1109/TNSM.2026.3675409", evidence="SUB",
)

C["L64"] = dict(
    in_llm=True, network_domain="High-performance network orchestration",
    task="Using an LLM to select which optimisation algorithm to apply for network orchestration problems",
    model="LLM-based algorithm selector", model_size="NR", open_or_closed="NR", prompting="Algorithm-selection prompting",
    rag="NR", tool_calling="NR", function_calling="NR", agent_architecture="LLM as meta-optimiser",
    number_of_agents="1", planner="Yes (algorithm selection)", executor="Classical optimiser", critic="NR", memory="NR",
    network_tools="Classical optimisation solvers (behind the LLM)", network_actions="Selection of the solver to run",
    recommendation_or_execution="Recommendation (the solver performs the action)", closed_loop="No",
    benchmark="NR", dataset="NR", metrics="Solution quality / runtime of the selected solver",
    llm_comparisons="NR", network_metrics="NR", hallucination_evaluation="No", latency="NR", token_cost="NR",
    baselines="Fixed algorithm choice", code_available="NR",
    limitations="Retrieved at metadata level only; the amount of network-specific grounding in the algorithm-selection prompts is not verified.",
    research_gap="This is the 'LLM + constrained optimisation' pattern the survey asked about: the LLM chooses the optimiser rather than performing the optimisation. It is promising but evaluated on solution quality rather than network outcomes.",
    source_url="https://ieeexplore.ieee.org/document/11358365", evidence="BIB",
)

C["L65"] = dict(
    in_llm=True, network_domain="Network management (multimodal: topology + troubleshooting)",
    task="Evaluating multimodal LLMs on network management tasks including topology understanding and troubleshooting",
    model="Multimodal LLMs", model_size="NR", open_or_closed="NR", prompting="Multimodal (image+text) prompting",
    rag="NR", tool_calling="NR", function_calling="NR", agent_architecture="Multimodal model evaluation",
    number_of_agents="1", planner="No", executor="No", critic="No", memory="NR", network_tools="No",
    network_actions="None (evaluation only)", recommendation_or_execution="Neither - evaluation", closed_loop="No",
    benchmark="Multimodal network-management evaluation (NOMS 2026)", dataset="NR", metrics="Multimodal task accuracy",
    llm_comparisons="Yes", network_metrics="No", hallucination_evaluation="NR", latency="NR", token_cost="NR",
    baselines="Cross-model comparison", code_available="NR",
    limitations="Evaluation study at a management-symposium venue; no execution against a network and no SLA scoring.",
    research_gap="Multimodal understanding of topology diagrams is a real operational requirement and is only starting to be benchmarked.",
    source_url="https://doi.org/10.1109/NOMS69089.2026.11668270", evidence="SUB",
)

C["L66"] = dict(
    in_llm=True, network_domain="Wireless network planning",
    task="Tool-augmented small-model AI agents for wireless network planning",
    model="Small language models with tools", model_size="Small (exact size NR)",
    open_or_closed="NR", prompting="Tool-augmented agent prompting", rag="NR", tool_calling="Yes",
    function_calling="NR", agent_architecture="Tool-augmented small-model agent",
    number_of_agents="1", planner="Yes", executor="Tools", critic="NR", memory="NR",
    network_tools="Planning tools/calculators", network_actions="Planning decisions (offline)",
    recommendation_or_execution="Recommendation (planning)", closed_loop="No",
    benchmark="NR", dataset="NR", metrics="Planning quality versus larger models",
    llm_comparisons="Yes - small models versus larger ones", network_metrics="Planning KPIs",
    hallucination_evaluation="NR", latency="NR", token_cost="NR", baselines="Larger general-purpose LLMs",
    code_available="NR",
    limitations="Magazine article on planning, not operations; planning is offline so latency constraints are relaxed relative to closed-loop control.",
    research_gap="Important signal for the 'small language model for network management' hypothesis: the paper argues small tool-augmented models can match larger ones on planning - which needs testing under closed-loop latency budgets.",
    source_url="https://doi.org/10.1109/MCOM.001.2500402", evidence="SUB",
)

C["L67"] = dict(
    in_llm=True, network_domain="Network and service management (zero-touch)",
    task="AI-driven zero-touch network and service management - challenges and research directions",
    model="N/A (architecture/agenda paper)", model_size="N/A", open_or_closed="N/A",
    prompting="N/A", rag="No", tool_calling="No", function_calling="No",
    agent_architecture="Closed-loop automation architecture (pre-LLM)",
    number_of_agents="N/A", planner="N/A", executor="N/A", critic="N/A", memory="N/A",
    network_tools="Management-plane telemetry and control", network_actions="Automated management actions",
    recommendation_or_execution="Architecture for execution", closed_loop="Yes (conceptual)",
    benchmark="N/A", dataset="N/A", metrics="N/A", llm_comparisons="N/A", network_metrics="N/A",
    hallucination_evaluation="N/A", latency="N/A", token_cost="N/A", baselines="N/A", code_available="N/A",
    limitations="Agenda article: defines the zero-touch ZSM target without an implementation or measurements.",
    research_gap="Defines the requirements against which LLM/agent-based management should be judged (closed loops at multiple time scales, intent assurance, conflict resolution).",
    source_url="https://doi.org/10.1109/MNET.001.1900252", evidence="SUB", is_foundational=True,
)

C["L68"] = dict(
    in_llm=True, network_domain="Communication, network and service management",
    task="Survey of LLMs for communication, network and service management",
    model="N/A (survey)", model_size="N/A", open_or_closed="N/A", prompting="Surveyed", rag="Surveyed",
    tool_calling="Surveyed", function_calling="Surveyed", agent_architecture="Surveyed",
    number_of_agents="N/A", planner="Surveyed", executor="Surveyed", critic="Surveyed", memory="Surveyed",
    network_tools="Surveyed", network_actions="Surveyed", recommendation_or_execution="Surveyed",
    closed_loop="Surveyed", benchmark="Surveyed", dataset="Surveyed", metrics="Surveyed",
    llm_comparisons="Surveyed", network_metrics="Surveyed", hallucination_evaluation="Surveyed",
    latency="Surveyed", token_cost="Surveyed", baselines="N/A", code_available="N/A",
    limitations="Survey; the field moves faster than the publication cycle, so 2026 work is under-represented.",
    research_gap="The consolidated view confirms the field's centre of gravity is advisory assistance rather than closed-loop control.",
    source_url="https://doi.org/10.1109/COMST.2025.3548039", evidence="SUB", is_survey=True,
)

C["L69"] = dict(
    in_llm=True, network_domain="Next-generation network management (intent)",
    task="Intent-based management of next-generation networks with an LLM-centric approach",
    model="LLM-centric framework", model_size="NR", open_or_closed="NR", prompting="Intent prompting",
    rag="NR", tool_calling="NR", function_calling="NR", agent_architecture="LLM intent engine",
    number_of_agents="1", planner="Intent processing", executor="NR", critic="No", memory="NR",
    network_tools="Management functions (conceptual)", network_actions="Management actions from intents",
    recommendation_or_execution="Framework for execution", closed_loop="No", benchmark="NR", dataset="NR",
    metrics="NR", llm_comparisons="NR", network_metrics="No", hallucination_evaluation="No",
    latency="NR", token_cost="NR", baselines="NR", code_available="NR",
    limitations="IEEE Network magazine framework paper; no measured deployment or network-level evaluation.",
    research_gap="Establishes intent-based LLM management as a research direction; the assurance question (did the intent hold?) is left open.",
    source_url="https://doi.org/10.1109/MNET.2024.3420120", evidence="BIB",
)

C["L70"] = dict(
    in_llm=True, network_domain="Networking (general)",
    task="Survey of LLM applications, enabling techniques and challenges in networking",
    model="N/A (survey)", model_size="N/A", open_or_closed="N/A", prompting="Surveyed", rag="Surveyed",
    tool_calling="Surveyed", function_calling="Surveyed", agent_architecture="Surveyed",
    number_of_agents="N/A", planner="Surveyed", executor="Surveyed", critic="Surveyed", memory="Surveyed",
    network_tools="Surveyed", network_actions="Surveyed", recommendation_or_execution="Surveyed",
    closed_loop="Surveyed", benchmark="Surveyed", dataset="Surveyed", metrics="Surveyed",
    llm_comparisons="Surveyed", network_metrics="Surveyed", hallucination_evaluation="Surveyed",
    latency="Surveyed", token_cost="Surveyed", baselines="N/A", code_available="N/A",
    limitations="Survey in IEEE Network; breadth over depth.",
    research_gap="Confirms the taxonomy of LLM-for-networking tasks used throughout this review.",
    source_url="https://doi.org/10.1109/MNET.2024.3435752", evidence="BIB", is_survey=True,
)

C["L71"] = dict(
    in_llm=True, network_domain="Zero-touch network configuration management",
    task="Using LLMs for zero-touch network configuration management",
    model="LLM-based configuration assistant", model_size="NR", open_or_closed="NR",
    prompting="Configuration-generation prompting", rag="NR", tool_calling="NR", function_calling="NR",
    agent_architecture="LLM configuration assistant", number_of_agents="1", planner="NR",
    executor="Configuration generation", critic="NR", memory="NR",
    network_tools="Configuration management interfaces (NR)", network_actions="Configuration generation",
    recommendation_or_execution="Configuration generation", closed_loop="No", benchmark="NR", dataset="NR",
    metrics="NR", llm_comparisons="NR", network_metrics="No", hallucination_evaluation="NR",
    latency="NR", token_cost="NR", baselines="NR", code_available="NR",
    limitations="Magazine article; retrieved at metadata level, so the evaluation depth is unverified.",
    research_gap="Zero-touch configuration is the most mature LLM-for-networking application; the open part is verification and rollback safety.",
    source_url="https://doi.org/10.1109/MCOM.001.2300630", evidence="BIB",
)

C["L72"] = dict(
    in_llm=True, network_domain="O-RAN resilience",
    task="LLM-driven agentic AI for enhanced O-RAN resilience; efficient resource allocation across network slices with distinct QoS requirements",
    model="LLM-driven agentic framework", model_size="NR", open_or_closed="NR", prompting="Agentic prompting",
    rag="NR", tool_calling="NR", function_calling="NR", agent_architecture="Agentic AI framework for O-RAN slice resource allocation",
    number_of_agents="NR", planner="Yes", executor="NR", critic="NR", memory="NR",
    network_tools="O-RAN interfaces (per the paper)", network_actions="Slice resource allocation decisions",
    recommendation_or_execution="Allocation decisions within an agentic loop", closed_loop="Intended",
    benchmark="NR", dataset="NR", metrics="NR", llm_comparisons="NR", network_metrics="QoS/resilience metrics",
    hallucination_evaluation="No", latency="NR", token_cost="NR", baselines="NR", code_available="NR",
    limitations="Abstract-level evidence only in this session (the Crossref record retrieved is a TechRxiv preprint version); the peer-reviewed venue and the experimental depth are unverified.",
    research_gap="O-RAN resilience plus slice resource allocation is exactly the intersection this PhD targets; the paper's evaluation depth needs to be established before it can be treated as prior art.",
    source_url="https://doi.org/10.36227/techrxiv.174284755.59863143/v1", evidence="ABS",
)

for k, v in C.items():
    if k in by:
        by[k].update(v)

json.dump(recs, open(os.path.join(DATA, "master_stage6.json"), "w"), indent=1)
print("stage6: characterised", len(C), "LLM/agent papers; total", len(recs))
