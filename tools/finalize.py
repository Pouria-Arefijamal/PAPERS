#!/usr/bin/env python3
"""Stage 8: derive the research-matrix flags, relevance/quality ratings and
experimental-parameter rows; emit data/master_full.json for the CSV generator.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
recs = json.load(open(os.path.join(DATA, "master_stage7.json")))

ALL_COLS = ["flow_scheduling", "orchestration", "multipath", "network_optimization",
            "drl", "llm", "agent", "multi_agent", "rag", "tool_calling", "fine_tuning",
            "lora", "qlora", "pruning", "quantization", "distillation", "o_ran",
            "5g_core", "6g", "network_slicing", "closed_loop", "testbed", "simulator",
            "benchmark", "open_code"]

TEXT_FIELDS = ("problem", "architecture", "algorithm", "network_domain", "task", "objective",
               "limitations", "research_gap", "domain", "orchestrator_type", "protocol",
               "network_generation", "ml_method", "optimization", "optimization_method",
               "ml", "agent", "llm", "base_model", "finetuning_method", "model",
               "recommendation_or_execution", "scheduler_location", "evaluation_platform",
               "simulator", "testbed", "benchmark", "dataset", "abstract")


def blob(r):
    return " ".join(str(r.get(f, "")) for f in TEXT_FIELDS).lower()


def yes(rec, *names):
    """True if any of the named fields is a positive marker."""
    for n in names:
        v = rec.get(n)
        if isinstance(v, bool):
            if v:
                return True
            continue
        s = str(v or "").strip().lower()
        if s and s not in ("na", "no", "none", "n/a", "false"):
            return True
    return False


def has(rec, *needles):
    b = blob(rec)
    return any(n in b for n in needles)


# ------------------------------------------------------------------ matrix
for r in recs:
    m = {}
    m["Flow_Scheduling"] = bool(r.get("in_flow")) or has(r, "flow scheduling", "packet scheduling",
                                                         "traffic scheduling", "packet scheduler")
    m["Orchestration"] = bool(r.get("in_orch")) or has(r, "orchestrat")
    m["Multipath"] = bool(r.get("in_multipath")) or has(r, "multipath", "mptcp", "mpquic", "atsss")
    m["Network_Optimization"] = has(r, "optimis", "optimiz")
    m["DRL"] = has(r, "reinforcement learning", " drl", "deep rl", "dqn", "ppo", "a2c", "actor-critic",
                   "maddpg", "q-learning")
    m["LLM"] = bool(r.get("in_llm")) or has(r, "large language model", "llm", "gpt-", "llama", "gemini")
    m["Agent"] = has(r, "agent", "agentic")
    m["Multi_Agent"] = has(r, "multi-agent", "multi agent", "multiple agents", "marl", "number_of_agents")
    m["RAG"] = has(r, "retrieval-augmented", "retrieval augmented", " rag")
    m["Tool_Calling"] = has(r, "tool call", "tool-call", "function call", "mcp", "tools")
    m["Fine_Tuning"] = has(r, "fine-tun", "finetun", "instruction tuning", " sft", "supervised fine")
    m["LoRA"] = has(r, "lora")
    m["QLoRA"] = has(r, "qlora")
    m["Pruning"] = has(r, "prun")
    m["Quantization"] = has(r, "quantis", "quantiz", "int8", "int4", "4-bit")
    m["Distillation"] = has(r, "distill")
    m["O_RAN"] = has(r, "o-ran", "oran", "open ran", "ric", "xapp", "rapp")
    m["5G_Core"] = has(r, "5g core", "upf", "smf", "amf", "pcf", "pdu session", "atsss",
                       "open5gs", "5gc")
    m["6G"] = has(r, "6g")
    m["Network_Slicing"] = has(r, "slic")
    m["Closed_Loop"] = has(r, "closed-loop", "closed loop", "control loop", "feedback loop",
                           "closed_loop")
    m["Testbed"] = has(r, "testbed", "test bed", "real network", "experimental platform",
                       "linux kernel", "prototype", "field trial")
    m["Simulator"] = has(r, "simulat", "ns-3", "ns3", "omnet", "mininet", "simu5g")
    m["Benchmark"] = bool(r.get("benchmark") and str(r["benchmark"]).strip().lower() not in ("na", "no")) \
        or has(r, "benchmark")
    m["Open_Code"] = bool(r.get("github") and str(r["github"]).strip().lower() not in ("na", "no")) \
        or has(r, "github", "gitlab", "public repo")
    r["matrix"] = m

# ------------------------------------------ relevance / quality / follow-up
for r in recs:
    area = r.get("area") or r["paper_id"][0]
    ev = r.get("evidence", "BIB")
    evid = r.get("is_survey")
    # relevance: direct overlap with the PhD intersection
    inter = sum(1 for k in ("Flow_Scheduling", "Orchestration", "Multipath", "LLM", "Agent",
                            "Closed_Loop", "O_RAN", "Network_Slicing", "6G")
                if r["matrix"].get(k))
    if r["matrix"]["LLM"] and (r["matrix"]["Agent"] or r["matrix"]["Orchestration"] or
                               r["matrix"]["Flow_Scheduling"] or r["matrix"]["Closed_Loop"]):
        rel = "HIGH"
    elif inter >= 3 or (r["matrix"]["DRL"] and (r["matrix"]["Flow_Scheduling"] or
                                                r["matrix"]["Multipath"] or r["matrix"]["Orchestration"])):
        rel = "HIGH"
    elif inter >= 2 or r["matrix"]["DRL"] or r["matrix"]["Multipath"] or r["matrix"]["Orchestration"]:
        rel = "MEDIUM"
    else:
        rel = "LOW"
    r["relevance_to_my_phd"] = rel

    # evaluation quality - based on what could actually be verified about the setup
    if evid:
        r["evaluation_quality"] = "NA"
    elif ev == "FULL" and (r["matrix"]["Testbed"] or r["matrix"]["Simulator"]):
        r["evaluation_quality"] = "STRONG"
    elif ev in ("ABS", "SUB") and (r["matrix"]["Testbed"] or r["matrix"]["Simulator"]):
        r["evaluation_quality"] = "MODERATE"
    elif ev == "BIB" and (r["matrix"]["Testbed"] or r["matrix"]["Simulator"]):
        r["evaluation_quality"] = "MODERATE"
    elif r["matrix"]["Simulator"] or r["matrix"]["Testbed"]:
        r["evaluation_quality"] = "MODERATE"
    else:
        r["evaluation_quality"] = "WEAK"

    # reproducibility
    if r["matrix"]["Open_Code"]:
        r["reproducibility_quality"] = "STRONG"
    elif ev == "FULL":
        r["reproducibility_quality"] = "MODERATE"
    elif ev in ("ABS", "SUB"):
        r["reproducibility_quality"] = "MODERATE"
    else:
        r["reproducibility_quality"] = "WEAK"
    r["code_available"] = ("Yes - " + str(r["github"])) if r["matrix"]["Open_Code"] and r.get("github") else (
        "Yes (public repository named in the paper)" if r["matrix"]["Open_Code"] else "NA")

    r["category"] = {"flow": "Flow/packet/traffic scheduling",
                     "orch": "Network/service orchestration",
                     "multipath": "Multipath transport and scheduling",
                     "llm": "LLM / AI agents for network management",
                     "efficiency": "LLM fine-tuning / compression for networking"}.get(area, "Other")
    if r["matrix"]["Open_Code"]:
        r["reproducibility_notes"] = r.get("reproducibility_notes") or \
            "Public artifact named in the paper/source: %s" % r.get("github")
    else:
        r["reproducibility_notes"] = r.get("reproducibility_notes") or (
            "No public artifact identified from the sources retrieved in this session.")

# ------------------------------------------ experimental parameter extraction
PATTERNS = {
    "number_of_users": [r"(\d[\d,]*)\s+(?:mobile\s+)?users", r"(\d[\d,]*)\s+users"],
    "number_of_ues": [r"(\d[\d,]*)\s+UEs", r"(\d[\d,]*)\s+UE"],
    "number_of_gnbs": [r"(\d[\d,]*)\s+gNBs?", r"(\d[\d,]*)\s+base stations?"],
    "number_of_nodes": [r"(\d[\d,]*)\s+nodes?"],
    "number_of_paths": [r"(\d[\d,]*)\s+(?:subflows|paths?)"],
    "number_of_episodes": [r"(\d[\d,]*)\s+episodes?"],
    "number_of_rounds": [r"(\d[\d,]*)\s+(?:rounds?|iterations?|epochs?)"],
    "learning_rate": [r"learning rate[^.\d]{0,20}([\d.eE+-]+)"],
    "discount_factor": [r"discount factor[^.\d]{0,20}([\d.]+)"],
    "batch_size": [r"batch size[^.\d]{0,20}([\d,]+)"],
    "gpu": [r"((?:\d+\s*[x×]\s*)?(?:NVIDIA|AMD|RTX|A100|A6000|H100|H200|V100|Tesla|GeForce)[^.;,)]{0,60})"],
    "simulator": [r"\b(ns-3|ns3|OMNeT\+\+|Simu5G|Mininet|Containernet|Open5GS|UERANSIM|srsRAN|OpenAirInterface|Colosseum|Kathara|GNS3|mobile-env)\b"],
    "testbed": [r"\b(testbed|test bed|real testbed|Open RAN testbed|prototype)\b"],
    "latency_target": [r"(\d+(?:\.\d+)?)\s*ms\s+(?:latency|delay)\s+(?:budget|target|requirement)"],
    "bandwidth": [r"(\d+(?:\.\d+)?)\s*(?:Gbps|Mbps|Gb/s|Mb/s)"],
}


def extract(r):
    text = " ".join(str(r.get(f, "")) for f in list(TEXT_FIELDS) + ["network_scale", "main_results",
                                                                    "network_performance",
                                                                    "training_hardware", "abstract"])
    out = {}
    for field, pats in PATTERNS.items():
        vals = []
        for p in pats:
            for m in re.finditer(p, text, flags=re.I):
                g = m.group(1) if m.groups() else m.group(0)
                g = g.strip()
                if g and g not in vals:
                    vals.append(g)
        out[field] = "; ".join(vals[:4]) if vals else "NA"
    return out


exp_rows = 0
for r in recs:
    text = " ".join(str(r.get(f, "")) for f in list(TEXT_FIELDS) + ["network_scale", "main_results",
                                                                    "network_performance"])
    ex = extract(r)
    r["experiment"] = ex
    if any(v != "NA" for v in ex.values()):
        exp_rows += 1
    r.setdefault("citation", r.get("source_url"))
    r["main_metric_short"] = (r.get("metrics") if str(r.get("metrics", "NA")).lower() != "na"
                              else (r.get("network_metrics") if str(r.get("network_metrics", "NA")).lower() != "na"
                                    else "NA"))
    r["limitation_short"] = (r.get("limitations") if str(r.get("limitations", "NA")).lower() != "na" else "NA")

json.dump(recs, open(os.path.join(DATA, "master_full.json"), "w"), indent=1)
from collections import Counter
print("master_full:", len(recs))
print("matrix true counts:")
c = Counter()
for r in recs:
    for k, v in r["matrix"].items():
        if v:
            c[k] += 1
for k in ALL_COLS:
    key = {"flow_scheduling": "Flow_Scheduling", "orchestration": "Orchestration",
           "multipath": "Multipath", "network_optimization": "Network_Optimization", "drl": "DRL",
           "llm": "LLM", "agent": "Agent", "multi_agent": "Multi_Agent", "rag": "RAG",
           "tool_calling": "Tool_Calling", "fine_tuning": "Fine_Tuning", "lora": "LoRA",
           "qlora": "QLoRA", "pruning": "Pruning", "quantization": "Quantization",
           "distillation": "Distillation", "o_ran": "O_RAN", "5g_core": "5G_Core", "6g": "6G",
           "network_slicing": "Network_Slicing", "closed_loop": "Closed_Loop", "testbed": "Testbed",
           "simulator": "Simulator", "benchmark": "Benchmark", "open_code": "Open_Code"}[k]
    print("  %-22s %d" % (k, c[key]))
print("rows with extracted experimental parameters:", exp_rows)
print("relevance:", Counter(r["relevance_to_my_phd"] for r in recs))
