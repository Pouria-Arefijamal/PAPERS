#!/usr/bin/env python3
"""Stage 7: efficiency / fine-tuning / compression (Area 5) characterizations.

Facts are taken from llm-net-papers/papers.json, whose entries record the source
URL used for each field, plus the companion compression report. Where that source
says "not reported" / "not verified", this script writes NA.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
DOCS = os.path.join(HERE, "..", "..", "llm-net-papers")

recs = json.load(open(os.path.join(DATA, "master_stage6.json")))
by = {r["paper_id"]: r for r in recs}
papers = json.load(open(os.path.join(DOCS, "papers.json")))["papers"]

AREA5_ID = {
    1: "E02", 2: "E01", 3: "E18", 4: "L50", 5: "E40", 6: "E41", 7: "E42",
    8: "E43", 9: "E44", 10: "E45", 11: "E46", 12: "L58", 13: "E47", 14: "E48",
    15: "O41", 16: "E28", 17: "E29", 18: "E39", 19: "E30", 20: "E31",
    21: "E32", 27: "E33", 28: "E49", 29: "L53", 30: "E50", 31: "L54",
    32: "E27", 33: "E34", 34: "E36", 35: "E51",
}

# new records that do not exist in master yet
NEW = {
    "E40": dict(paper_id="E40", area="efficiency",
                title="Harnessing the Power of LLMs, Informers and Decision Transformers for Intent-driven and Energy-efficient Network Slicing",
                venue="arXiv preprint", year=2025, doi=None, arxiv="2505.01841", peer_reviewed=False,
                authors=["Ali", "et al."],
                source_url="https://arxiv.org/abs/2505.01841", evidence="SUB"),
    "E41": dict(paper_id="E41", area="efficiency",
                title="Leveraging Multi-Agent System (MAS) and Fine-Tuned Small Language Models for Telecom Network Troubleshooting",
                venue="arXiv preprint", year=2025, doi=None, arxiv="2511.00651", peer_reviewed=False,
                authors=[], source_url="https://arxiv.org/abs/2511.00651", evidence="SUB"),
    "E42": dict(paper_id="E42", area="efficiency",
                title="Edge-Deployable LLM Fine-Tuning on a Single GPU for Telecom Network Troubleshooting",
                venue="arXiv preprint", year=2026, doi=None, arxiv="2607.02523", peer_reviewed=False,
                authors=[], source_url="https://arxiv.org/abs/2607.02523", evidence="SUB"),
    "E43": dict(paper_id="E43", area="efficiency",
                title="LLM-Based Emulation of the Radio Resource Control Layer: Towards AI-Native RAN Protocols",
                venue="arXiv preprint (submitted)", year=2026, doi=None, arxiv="2505.16821", peer_reviewed=False,
                authors=[], source_url="https://arxiv.org/abs/2505.16821", evidence="SUB"),
    "E44": dict(paper_id="E44", area="efficiency",
                title="Network Self-Configuration Based on Fine-Tuned Small Language Models",
                venue="IEEE Open Journal of the Communications Society", year=2026, doi="10.1109/OJCOMS.2026.3695460",
                authors=[], source_url="https://doi.org/10.1109/OJCOMS.2026.3695460", evidence="SUB"),
    "E45": dict(paper_id="E45", area="efficiency",
                title="Lightweight LLMs for 3GPP Specifications: Fine-Tuning, Retrieval-Augmented Generation and Quantization",
                venue="IEEE International Conference on Network Softwarization (NetSoft)", year=2025,
                doi="10.1109/NETSOFT64993.2025.11080581", authors=[],
                source_url="https://doi.org/10.1109/NETSOFT64993.2025.11080581", evidence="SUB"),
    "E46": dict(paper_id="E46", area="efficiency",
                title="Toward Autonomous O-RAN: A Multi-Scale Agentic AI Framework for Real-Time Network Control",
                venue="arXiv preprint", year=2026, doi=None, arxiv="2602.14117", peer_reviewed=False,
                authors=[], source_url="https://arxiv.org/abs/2602.14117", evidence="SUB"),
    "E47": dict(paper_id="E47", area="efficiency",
                title="Telecom Foundation Models: Applications, Challenges, and Future Trends",
                venue="arXiv preprint", year=2024, doi=None, arxiv="2408.03964", peer_reviewed=False,
                authors=[], source_url="https://arxiv.org/abs/2408.03964", evidence="SUB"),
    "E48": dict(paper_id="E48", area="efficiency",
                title="Think Less, Label Better: Multi-Stage Domain-Grounded Synthetic Data Generation for Telecom Troubleshooting",
                venue="arXiv preprint (ICC 2026 submission per author comment)", year=2026, doi=None,
                arxiv="2509.25736", peer_reviewed=False, authors=[],
                source_url="https://arxiv.org/abs/2509.25736", evidence="SUB"),
    "E49": dict(paper_id="E49", area="efficiency",
                title="Understanding Telecom Language Through Large Language Models",
                venue="IEEE Global Communications Conference (GLOBECOM)", year=2023,
                doi="10.1109/GLOBECOM54140.2023.1043772", authors=[],
                source_url="https://doi.org/10.1109/GLOBECOM54140.2023.1043772", evidence="SUB"),
    "E50": dict(paper_id="E50", area="efficiency",
                title="SPEC5G: A Dataset for 5G Cellular Network Protocol Analysis",
                venue="Findings of the Association for Computational Linguistics: IJCNLP-AACL", year=2023,
                doi="10.18653/v1/2023.findings-ijcnlp.3", authors=[],
                source_url="https://doi.org/10.18653/v1/2023.findings-ijcnlp.3", evidence="SUB"),
    "E51": dict(paper_id="E51", area="efficiency",
                title="TelecomGPT-R1: A Unified Open-Source Reasoner for the Telecom Domain",
                venue="arXiv preprint", year=2026, doi=None, arxiv="2608.26126", peer_reviewed=False,
                authors=[], source_url="https://arxiv.org/abs/2608.26126", evidence="SUB"),
}

for k, v in NEW.items():
    if k not in by:
        recs.append(v)
        by[k] = v

NRT = {"not reported", "not verified", "not applicable", "n/a", "none", None, ""}


def clean(v):
    if v is None:
        return "NA"
    if isinstance(v, list):
        v = "; ".join(str(x) for x in v)
    s = str(v).strip()
    if s.lower() in NRT or s.lower().startswith("not reported") or s.lower().startswith("not verified"):
        return "NA"
    return s


COUNT = 0
for p in papers:
    pid = AREA5_ID.get(p["id"])
    if not pid:
        continue
    r = by.get(pid)
    if not r:
        continue
    method = clean(p.get("method"))
    lowm = method.lower()
    r.update(dict(
        in_eff=True,
        network_task=clean(p.get("group", "")) + " :: " + clean(p.get("dataset_name")),
        base_model=clean(p.get("base_model")),
        model_size=clean(p.get("base_model_params")),
        fine_tuning=("Yes" if any(w in lowm for w in ["fine-tun", "sft", "lora", "qlora", "instruct", "pre-train", "dpo", "grpo", "rft"]) else "NA"),
        finetuning_method=method,
        dataset=clean(p.get("dataset_name")),
        training_data_size=clean(p.get("dataset_size")),
        pruning=("Yes" if "prun" in lowm or "spars" in lowm else "No"),
        pruning_method=(method if ("prun" in lowm or "spars" in lowm) else "No"),
        quantization=("Yes" if "quant" in lowm or "4-bit" in lowm or "int8" in lowm else "No"),
        distillation=("Yes" if "distill" in lowm else "No"),
        peft=("Yes" if any(w in lowm for w in ["lora", "qlora", "peft", "adapter", "freeze-tun"]) else "No"),
        lora=("Yes" if "lora" in lowm and "qlora" not in lowm else ("Yes" if "qlora" in lowm else "No")),
        qlora=("Yes" if "qlora" in lowm else "No"),
        training_hardware=clean(p.get("gpu_hardware")),
        training_cost=clean(p.get("training_time")),
        inference_latency=clean(p.get("inference_latency")),
        model_size_after=clean(p.get("model_size_after_compression")),
        accuracy=clean(p.get("main_results")),
        network_performance=clean(p.get("main_results")),
        baseline=clean(p.get("baselines")),
        main_results=clean(p.get("main_results")),
        limitations=clean(p.get("main_limitation")),
        code_available=("Yes - " + clean(p.get("code_data_url"))) if clean(p.get("code_data_url")) != "NA" else "No",
        github=(clean(p.get("code_data_url")) if clean(p.get("code_data_url")) != "NA" else "NA"),
        source_url=clean((p.get("sources_retrieved") or [None])[0]) if p.get("sources_retrieved") else r.get("source_url"),
        evidence="SUB",
    ))
    COUNT += 1

json.dump(recs, open(os.path.join(DATA, "master_stage7.json"), "w"), indent=1)
print("stage7: characterised", COUNT, "efficiency papers; total", len(recs))
