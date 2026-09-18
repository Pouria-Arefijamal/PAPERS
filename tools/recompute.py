#!/usr/bin/env python3
"""Recompute derived fields (matrix, relevance, quality, experiment extraction)
for any master_full.json record that is missing them. Safe to re-run."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "..", "data")

recs = json.load(open(os.path.join(DATA, "master_full.json")))

# reuse the derivation logic by importing finalize's helpers via exec of its body
import importlib.util
spec = importlib.util.spec_from_file_location("fin", os.path.join(HERE, "finalize.py"))

# The finalize script reads master_stage7 and writes master_full; instead we
# replicate the derivation here on the current master_full contents.

ALL_COLS = ["Flow_Scheduling", "Orchestration", "Multipath", "Network_Optimization", "DRL",
            "LLM", "Agent", "Multi_Agent", "RAG", "Tool_Calling", "Fine_Tuning", "LoRA",
            "QLoRA", "Pruning", "Quantization", "Distillation", "O_RAN", "5G_Core", "6G",
            "Network_Slicing", "Closed_Loop", "Testbed", "Simulator", "Benchmark", "Open_Code"]

TEXT_FIELDS = ("problem", "architecture", "algorithm", "network_domain", "task", "objective",
               "limitations", "research_gap", "domain", "orchestrator_type", "protocol",
               "network_generation", "ml_method", "optimization", "optimization_method",
               "ml", "agent", "llm", "base_model", "finetuning_method", "model",
               "recommendation_or_execution", "scheduler_location", "evaluation_platform",
               "simulator", "testbed", "benchmark", "dataset", "abstract", "title")


def blob(r):
    return " ".join(str(r.get(f, "")) for f in TEXT_FIELDS).lower()


def has(r, *needles):
    b = blob(r)
    return any(n in b for n in needles)


for r in recs:
    if "matrix" in r and "experiment" in r and not r.get("_recompute"):
        continue
    m = {}
    m["Flow_Scheduling"] = bool(r.get("in_flow")) or has(r, "flow scheduling", "packet scheduling",
                                                         "traffic scheduling", "packet scheduler")
    m["Orchestration"] = bool(r.get("in_orch")) or has(r, "orchestrat")
    m["Multipath"] = bool(r.get("in_multipath")) or has(r, "multipath", "mptcp", "mpquic", "atsss")
    m["Network_Optimization"] = has(r, "optimis", "optimiz")
    m["DRL"] = has(r, "reinforcement learning", " drl", "deep rl", "dqn", "ppo", "a2c",
                   "actor-critic", "maddpg", "q-learning")
    m["LLM"] = bool(r.get("in_llm")) or has(r, "large language model", "llm", "gpt-", "llama", "gemini")
    m["Agent"] = has(r, "agent", "agentic")
    m["Multi_Agent"] = has(r, "multi-agent", "multi agent", "multiple agents", "marl")
    m["RAG"] = has(r, "retrieval-augmented", "retrieval augmented", " rag")
    m["Tool_Calling"] = has(r, "tool call", "tool-call", "function call", "mcp")
    m["Fine_Tuning"] = has(r, "fine-tun", "finetun", "instruction tuning", " sft", "supervised fine")
    m["LoRA"] = has(r, "lora")
    m["QLoRA"] = has(r, "qlora")
    m["Pruning"] = has(r, "prun")
    m["Quantization"] = has(r, "quantis", "quantiz", "int8", "int4", "4-bit")
    m["Distillation"] = has(r, "distill")
    m["O_RAN"] = has(r, "o-ran", "oran", "open ran", "ric", "xapp", "rapp")
    m["5G_Core"] = has(r, "5g core", "upf", "smf", "amf", "pcf", "pdu session", "atsss", "open5gs")
    m["6G"] = has(r, "6g")
    m["Network_Slicing"] = has(r, "slic")
    m["Closed_Loop"] = has(r, "closed-loop", "closed loop", "control loop", "feedback loop")
    m["Testbed"] = has(r, "testbed", "test bed", "real network", "experimental platform",
                       "linux kernel", "prototype", "field trial")
    m["Simulator"] = has(r, "simulat", "ns-3", "ns3", "omnet", "mininet", "simu5g")
    m["Benchmark"] = bool(str(r.get("benchmark", "NA")).strip().lower() not in ("na", "no", "")) \
        or has(r, "benchmark")
    m["Open_Code"] = bool(r.get("github") and str(r.get("github")).strip().lower() not in ("na", "no")) \
        or has(r, "github", "gitlab", "public repo")
    r["matrix"] = m
    r.pop("_recompute", None)

    if r["matrix"]["LLM"] and (r["matrix"]["Agent"] or r["matrix"]["Orchestration"] or
                               r["matrix"]["Flow_Scheduling"] or r["matrix"]["Closed_Loop"]):
        r["relevance_to_my_phd"] = r.get("relevance_to_my_phd") or "HIGH"
    else:
        inter = sum(1 for k in ("Flow_Scheduling", "Orchestration", "Multipath", "LLM", "Agent",
                                "Closed_Loop", "O_RAN", "Network_Slicing", "6G") if m.get(k))
        r["relevance_to_my_phd"] = r.get("relevance_to_my_phd") or (
            "HIGH" if inter >= 3 or (m["DRL"] and (m["Flow_Scheduling"] or m["Multipath"] or
                                                   m["Orchestration"]))
            else ("MEDIUM" if inter >= 2 or m["DRL"] or m["Multipath"] or m["Orchestration"] else "LOW"))
    r.setdefault("evaluation_quality", "MODERATE" if (m["Simulator"] or m["Testbed"]) else "WEAK")
    r.setdefault("reproducibility_quality", "STRONG" if m["Open_Code"] else
                 ("MODERATE" if r.get("evidence") in ("FULL", "ABS", "SUB") else "WEAK"))
    r.setdefault("code_available", ("Yes - " + str(r["github"])) if (m["Open_Code"] and r.get("github"))
                 else ("Yes (public repository named in the paper)" if m["Open_Code"] else "NA"))
    r.setdefault("experiment", {"number_of_users": "NA"})
    r.setdefault("main_metric_short", r.get("metrics") or r.get("network_metrics") or "NA")
    r.setdefault("limitation_short", r.get("limitations") or "NA")
    r.setdefault("citation", r.get("source_url"))

json.dump(recs, open(os.path.join(DATA, "master_full.json"), "w"), indent=1)
n_matrix = sum(1 for r in recs if "matrix" in r)
print("records:", len(recs), "| with matrix:", n_matrix)
missing = [r["paper_id"] for r in recs if "matrix" not in r]
print("missing matrix:", missing[:10])
