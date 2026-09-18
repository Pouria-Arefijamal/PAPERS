#!/usr/bin/env python3
"""Quality-control pass over master_full.json before CSV generation.

Rebuilds the research matrix from *structured* record fields plus word-boundary
regexes over the prose fields, so that abbreviations such as "LLM" cannot match
inside unrelated words.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
PATH = os.path.join(DATA, "master_full.json")
recs = json.load(open(PATH))

TEXT_FIELDS = ("problem", "architecture", "algorithm", "network_domain", "task", "objective",
               "limitations", "research_gap", "domain", "orchestrator_type", "protocol",
               "network_generation", "ml_method", "optimization", "optimization_method",
               "ml", "agent", "llm", "base_model", "finetuning_method", "model",
               "recommendation_or_execution", "scheduler_location", "evaluation_platform",
               "simulator", "testbed", "benchmark", "dataset", "abstract", "title",
               "network_tools", "network_actions", "agent_architecture", "main_results",
               "network_performance")

PAT = {
    "Flow_Scheduling": r"flow sched|packet sched|traffic sched|scheduling polic|scheduler|resource block|prb allocation|bandwidth allocation|flow placement",
    "Orchestration": r"orchestrat",
    "Multipath": r"multipath|\bmptcp\b|\bmpquic\b|atsss|multi-connectivity|subflow|concurrent multipath",
    "Network_Optimization": r"optimis|optimiz|minimi[sz]e|maximi[sz]e",
    "DRL": r"\bdrl\b|reinforcement learning|\bdqn\b|\bppo\b|\ba2c\b|actor-critic|\bmaddpg\b|q-learning|\bsac\b|\bddpg\b|\bmappo\b",
    "LLM": r"\bllms?\b|large language model|\bgpt-?\d|llama|gemini|qwen|mistral|deepseek|claude|foundation model|language model",
    "Agent": r"\bagents?\b|agentic",
    "Multi_Agent": r"multi-agent|multi agent|multiple agents|\bmarl\b",
    "RAG": r"\brag\b|retrieval[- ]augmented",
    "Tool_Calling": r"tool call|tool-call|tool usefunction call|\bmcp\b|model context protocol|tool invocation|tool interface|tools exposed",
    "Fine_Tuning": r"fine[- ]tun|instruction tun|\bsft\b|supervised fine|domain adapt|continual pre-train|\bdpo\b|\bgrpo\b|\brft\b",
    "LoRA": r"\blora\b",
    "QLoRA": r"\bqlora\b",
    "Pruning": r"\bprun",
    "Quantization": r"quantis|quantiz|\bint8\b|\bint4\b|4-bit",
    "Distillation": r"distill",
    "O_RAN": r"\bo-ran\b|\boran\b|open ran|\bric\b|\bxapp|\brapp\b|near-rt|non-rt",
    "5G_Core": r"\b5g core\b|\b5gc\b|\bupf\b|\bsmf\b|\bamf\b|\bpcf\b|\bnrf\b|pdu session|atsss|open5gs|user plane function",
    "6G": r"\b6g\b|sixth[- ]generation",
    "Network_Slicing": r"\bslic",
    "Closed_Loop": r"closed[- ]loop|control loop|feedback loop|closed loop",
    "Testbed": r"testbed|test bed|real network|experimental platform|linux kernel|field trial|live testbed",
    "Simulator": r"simulat|ns-3|\bns3\b|omnet|mininet|simu5g",
    "Benchmark": r"benchmark",
    "Open_Code": r"github|gitlab|public repo|open[- ]source (?:framework|code|implementation)|code (?:is )?(?:public|available|released)",
}

for r in recs:
    blob = " ".join(str(r.get(f, "")) for f in TEXT_FIELDS).lower()
    gh = str(r.get("github") or "").strip().lower()
    ca = str(r.get("code_available") or "").strip().lower()
    m = {col: bool(re.search(pat, blob)) for col, pat in PAT.items()}
    # structured overrides
    m["LLM"] = m["LLM"] or bool(r.get("in_llm"))
    m["Multipath"] = m["Multipath"] or bool(r.get("in_multipath"))
    m["Flow_Scheduling"] = m["Flow_Scheduling"] or bool(r.get("in_flow"))
    m["Orchestration"] = m["Orchestration"] or bool(r.get("in_orch"))
    m["Open_Code"] = bool(gh and gh not in ("na", "none", "no")) or ca.startswith("yes")
    m["Benchmark"] = m["Benchmark"] or (str(r.get("benchmark") or "na").strip().lower()
                                        not in ("na", "no", "none", ""))
    r["matrix"] = m

    # relevance
    inter = sum(1 for k in ("Flow_Scheduling", "Orchestration", "Multipath", "LLM", "Agent",
                            "Closed_Loop", "O_RAN", "Network_Slicing", "6G") if m[k])
    if m["LLM"] and (m["Agent"] or m["Orchestration"] or m["Flow_Scheduling"] or m["Closed_Loop"]):
        r["relevance_to_my_phd"] = "HIGH"
    elif inter >= 3 or (m["DRL"] and (m["Flow_Scheduling"] or m["Multipath"] or m["Orchestration"])):
        r["relevance_to_my_phd"] = "HIGH"
    elif inter >= 2 or m["DRL"] or m["Multipath"] or m["Orchestration"]:
        r["relevance_to_my_phd"] = "MEDIUM"
    else:
        r["relevance_to_my_phd"] = "LOW"

    if r.get("is_survey"):
        r["evaluation_quality"] = "NA"
    elif r.get("evidence") == "FULL" and (m["Testbed"] or m["Simulator"]):
        r["evaluation_quality"] = "STRONG"
    elif m["Testbed"] or m["Simulator"]:
        r["evaluation_quality"] = "MODERATE"
    else:
        r["evaluation_quality"] = "WEAK"

    if m["Open_Code"]:
        r["reproducibility_quality"] = "STRONG"
    elif r.get("evidence") in ("FULL", "ABS", "SUB"):
        r["reproducibility_quality"] = "MODERATE"
    else:
        r["reproducibility_quality"] = "WEAK"

    if not r.get("code_available") or str(r["code_available"]).strip() == "NA":
        if gh and gh not in ("na", "none", "no"):
            r["code_available"] = "Yes - " + str(r["github"])
        elif m["Open_Code"]:
            r["code_available"] = "Yes (public repository named in the paper)"
        else:
            r["code_available"] = "NA"
    r.setdefault("reproducibility_notes",
                 r.get("reproducibility_notes") or
                 ("Public artifact: " + str(r.get("github")) if m["Open_Code"]
                  else "No public artifact identified from the sources retrieved in this session."))
    r.setdefault("main_metric_short", r.get("metrics") or r.get("network_metrics") or "NA")
    r.setdefault("limitation_short", r.get("limitations") or "NA")
    r.setdefault("citation", r.get("source_url"))

json.dump(recs, open(PATH, "w"), indent=1)

from collections import Counter
c = Counter()
for r in recs:
    for k, v in r["matrix"].items():
        if v:
            c[k] += 1
print("records:", len(recs))
for k in ["Flow_Scheduling", "Orchestration", "Multipath", "Network_Optimization", "DRL", "LLM",
          "Agent", "Multi_Agent", "RAG", "Tool_Calling", "Fine_Tuning", "LoRA", "QLoRA", "Pruning",
          "Quantization", "Distillation", "O_RAN", "5G_Core", "6G", "Network_Slicing",
          "Closed_Loop", "Testbed", "Simulator", "Benchmark", "Open_Code"]:
    print("  %-22s %3d" % (k, c[k]))
print("relevance:", dict(Counter(r["relevance_to_my_phd"] for r in recs)))
print("eval quality:", dict(Counter(r["evaluation_quality"] for r in recs)))
print("repro quality:", dict(Counter(r["reproducibility_quality"] for r in recs)))
