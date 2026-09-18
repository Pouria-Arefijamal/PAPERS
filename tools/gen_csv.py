#!/usr/bin/env python3
"""Generate the 8 deliverable CSVs from data/master_full.json.

master_full.json records are dicts with (at least) the keys used below.
Missing keys become "NA". Controlled vocabularies are enforced where the user
asked for them (relevance_to_my_phd, evaluation_quality, reproducibility_quality,
and the 0/1 research-matrix flags).
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")
OUT = ROOT

with open(os.path.join(DATA, "master_full.json")) as fh:
    R = json.load(fh)

by_id = {r["paper_id"]: r for r in R}


def g(rec, key, default="NA"):
    v = rec.get(key, default)
    if v is None or v == "":
        return "NA"
    if isinstance(v, (list, tuple)):
        return "; ".join(str(x) for x in v) if v else "NA"
    if isinstance(v, bool):
        return "Yes" if v else "No"
    return str(v)


def write(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for row in rows:
            w.writerow(row)
    print("wrote %-34s %d rows" % (name, len(rows)))


# ------------------------------------------------------------------ 01 flow
FLOW = """paper_id title authors year venue doi peer_reviewed network_generation network_domain architecture
scheduler_location problem input_parameters decision_variables actions objective constraints algorithm
optimization_method ml_method simulator testbed dataset traffic_model network_scale baselines metrics
main_results limitations research_gap github code_available reproducibility_notes source_url""".split()

flow_rows = [[g(r, c) for c in FLOW] for r in R if r.get("in_flow")]
write("01_flow_schedulers.csv", FLOW, flow_rows)

# ------------------------------------------------------- 02 orchestrators
ORCH = """paper_id title authors year venue doi peer_reviewed network_generation domain orchestrator_type
architecture control_plane managed_resources input output interfaces centralized_or_distributed
single_or_multidomain closed_loop sla_support network_slicing cloud_native kubernetes oran optimization ml
agent llm evaluation_platform network_scale baselines metrics main_results limitations research_gap github
source_url""".split()
orch_rows = [[g(r, c) for c in ORCH] for r in R if r.get("in_orch")]
write("02_orchestrators.csv", ORCH, orch_rows)

# ---------------------------------------------------- 03 multipath
MP = """paper_id title authors year venue doi peer_reviewed protocol network_generation architecture
number_of_paths path_type scheduler_location input_parameters path_metrics decision_type packet_or_flow
reordering_handling congestion_control objective algorithm ml_method simulator testbed traffic_model
baselines metrics main_results limitations research_gap source_url""".split()
mp_rows = [[g(r, c) for c in MP] for r in R if r.get("in_multipath")]
write("03_multipath_schedulers.csv", MP, mp_rows)

# ---------------------------------------------------- 04 llm agents
LLM = """paper_id title authors year venue doi peer_reviewed network_domain task model model_size
open_or_closed prompting rag tool_calling function_calling agent_architecture number_of_agents planner
executor critic memory network_tools network_actions recommendation_or_execution closed_loop benchmark
dataset metrics llm_comparisons network_metrics hallucination_evaluation latency token_cost baselines
code_available limitations research_gap source_url""".split()
llm_rows = [[g(r, c) for c in LLM] for r in R if r.get("in_llm")]
write("04_llm_network_agents.csv", LLM, llm_rows)

# ---------------------------------------------------- 05 efficiency
EFF = """paper_id title authors year venue doi peer_reviewed network_task base_model model_size
fine_tuning finetuning_method dataset training_data_size pruning pruning_method quantization distillation
peft lora qlora training_hardware training_cost inference_latency model_size_after accuracy
network_performance baseline main_results limitations research_gap code_available source_url""".split()
eff_rows = [[g(r, c) for c in EFF] for r in R if r.get("in_eff")]
write("05_llm_efficiency_networking.csv", EFF, eff_rows)

# ---------------------------------------------------- 06 master
MASTER = """paper_id title authors year venue doi peer_reviewed category subcategory
relevance_to_my_phd research_problem method network_layer ai_method optimization_method
evaluation_quality reproducibility_quality potential_followup source_url""".split()
master_rows = [[g(r, c) for c in MASTER] for r in R]
write("06_master_literature.csv", MASTER, master_rows)

# ---------------------------------------------------- 07 research matrix
MATRIX = """Paper Flow_Scheduling Orchestration Multipath Network_Optimization DRL LLM Agent Multi_Agent RAG
Tool_Calling Fine_Tuning LoRA QLoRA Pruning Quantization Distillation O_RAN 5G_Core 6G Network_Slicing
Closed_Loop Testbed Simulator Benchmark Open_Code Main_Metric Main_Limitation""".split()


def flag(rec, key):
    v = rec.get("matrix", {}).get(key)
    if v is None:
        return "0"
    return "1" if v else "0"


matrix_rows = []
for r in R:
    row = [r["title"]]
    for c in MATRIX[1:-2]:
        if c == "Paper":
            continue
        row.append(flag(r, c))
    row.append(g(r, "main_metric_short"))
    row.append(g(r, "limitation_short"))
    matrix_rows.append(row)
write("07_research_matrix.csv", MATRIX, matrix_rows)

# ---------------------------------------------------- 08 experimental parameters
EXP = """paper_id number_of_users number_of_ues number_of_gnbs number_of_nodes number_of_paths bandwidth
packet_size traffic_rate arrival_rate latency_target throughput_target simulation_time number_of_episodes
number_of_rounds learning_rate discount_factor epsilon batch_size model model_parameters gpu cpu ram
simulator testbed other_parameters citation""".split()
exp_rows = [[g(r, c) for c in EXP] for r in R if r.get("experiment")]
write("08_experimental_parameters.csv", EXP, exp_rows)

print("\ncounts: flow=%d orch=%d multipath=%d llm=%d eff=%d master=%d exp=%d" % (
    len(flow_rows), len(orch_rows), len(mp_rows), len(llm_rows), len(eff_rows),
    len(master_rows), len(exp_rows)))
