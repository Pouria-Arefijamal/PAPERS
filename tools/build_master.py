#!/usr/bin/env python3
"""Build the master literature database (data/master.json).

Stage 1: load the Crossref/OpenAlex-verified seed papers, drop off-topic
automatic matches, and merge in the verified subagent findings.
Every record carries an `evidence` level so the CSVs can be honest about
which fields were verified from a retrievable source.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data")

# ---------------------------------------------------------------- load seeds
seeds = json.load(open(os.path.join(DATA, "papers_enriched.json")))
seed_by_key = {s["key"]: s for s in seeds}

# verified by inspection to be automatic title-match false positives -> drop
DROP = {"O20", "L16", "L24", "L31", "L33", "L38", "L42", "L45", "E05", "E16",
        "E03", "E06", "E09", "E10", "E12", "E13", "E14", "E17", "E19",
        "E21", "E22", "E25", "E08", "E11", "E23", "E24", "E20",
        "M19", "M26", "M31", "M36", "M40", "F23", "F24", "F27", "F35",
        "F37", "F40", "O11", "O30", "E01", "E02", "E04", "E07", "E15",
        "E18", "F18", "F34"}

# explicitly re-included with corrected or verified bibliographic data
REINCLUDE = {
    "E01": dict(title="TelecomGPT: A Framework to Build Telecom-Specific Large Language Models",
                venue="IEEE Transactions on Machine Learning in Communications and Networking",
                year=2025, doi="10.1109/TMLCN.2025.3593184"),
    "E02": dict(title="Mobile-LLaMA: Instruction Fine-Tuning Open-Source LLM for Network Analysis in 5G Networks",
                venue="IEEE Network", year=2024, doi="10.1109/MNET.2024.3421306"),
    "E04": dict(title="QLoRA: Efficient Finetuning of Quantized LLMs",
                venue="Advances in Neural Information Processing Systems (NeurIPS)", year=2023,
                doi="10.52202/075280-0441"),
    "E07": dict(title="TinyBERT: Distilling BERT for Natural Language Understanding",
                venue="Findings of the Association for Computational Linguistics: EMNLP 2020",
                year=2020, doi="10.18653/v1/2020.findings-emnlp.119"),
    "E15": dict(title="IoV-BERT-IDS: Hybrid Network Intrusion Detection System in IoV Using Large Language Models",
                venue="IEEE Transactions on Vehicular Technology", year=2025, doi="10.1109/TVT.2024.3402366"),
    "E18": dict(title="Tele-LLMs: A Series of Specialized Large Language Models for Telecommunications",
                venue="IEEE Access", year=2026, doi="10.1109/ACCESS.2026.3698683"),
}

DROP -= set(REINCLUDE.keys())

records = []
for s in seeds:
    k = s["key"]
    if k in DROP:
        continue
    if k in REINCLUDE:
        s.update(REINCLUDE[k])
    records.append({
        "src_key": k,
        "title": s.get("title"),
        "authors": s.get("authors") or [],
        "year": s.get("year"),
        "venue": s.get("venue"),
        "doi": s.get("doi"),
        "type": s.get("type"),
        "abstract": s.get("abstract"),
        "source_url": ("https://doi.org/" + s["doi"]) if s.get("doi") else None,
        "evidence": "BIB",
    })

json.dump(records, open(os.path.join(DATA, "master_stage1.json"), "w"), indent=1)
print("stage1 records:", len(records))
from collections import Counter
print(Counter(r["src_key"][0] for r in records))
