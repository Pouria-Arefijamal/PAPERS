#!/usr/bin/env python3
"""Targeted OpenAlex searches constrained to specific high-quality venues."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from litlib import openalex_search, alex_rows

TOPIC_QUERIES = [
    # AREA 1 - flow scheduling
    "flow scheduling 5G core network",
    "packet scheduling 5G new radio",
    "traffic scheduling deterministic network 5G",
    "QoS flow 5G scheduler optimization",
    "network slicing scheduling radio resource allocation",
    "UPF placement selection 5G core",
    "SRv6 segment routing traffic engineering",
    "intent-based traffic steering 5G",
    "latency-aware scheduling URLLC",
    "DRL scheduling wireless network",
    # AREA 2 - orchestration
    "network service orchestration 5G NFV",
    "multi-domain orchestration network slicing",
    "O-RAN service management orchestration",
    "zero touch network service management automation",
    "intent based networking orchestration LLM",
    "cloud native network function orchestration Kubernetes",
    "MEC orchestration service placement",
    "digital twin network management orchestration",
    "E2E network slicing orchestration optimization",
    "autonomous network management closed loop",
    # AREA 3 - multipath
    "multipath TCP scheduler",
    "multipath QUIC scheduling",
    "multipath transport 5G heterogeneous network",
    "access traffic steering switching splitting ATSSS",
    "multi connectivity scheduling 5G",
    "packet scheduling multipath reinforcement learning",
    "congestion control multipath",
    "multipath video streaming scheduling",
    "network coding multipath transmission",
    "path selection multipath routing QoE",
    # AREA 4 - LLM/agents
    "large language model network management",
    "large language model network configuration",
    "large language model intent based networking",
    "LLM agent network automation",
    "LLM O-RAN 6G",
    "LLM traffic engineering",
    "foundation model wireless network",
    "multi agent LLM network operations",
    "generative AI telecom network",
    "LLM network troubleshooting root cause analysis",
    "retrieval augmented generation network management",
    "LLM resource allocation wireless",
    # AREA 5 - efficiency
    "fine tuning large language model telecom",
    "parameter efficient fine tuning network management",
    "knowledge distillation network management model",
    "model compression network management",
    "quantization large language model edge inference",
    "lightweight language model networking",
    "domain adaptation language model telecommunication",
    "LoRA large language model telecom",
]

VENUE_FILTERS = [
    "primary_location.source.id:S4306420789",  # placeholder, replaced below
]

# journals / venues used as a soft check (matched on returned venue string)
GOOD = [
    "ieee transactions", "ieee journal", "ieee/acm transactions", "acm transactions",
    "ieee network", "ieee communications", "ieee wireless", "ieee internet of things",
    "ieee open journal", "proceedings of the ieee", "computer networks",
    "journal of network and computer applications", "future generation computer",
    "computer communications", "ieee communications magazine", "ieee communications surveys",
    "acm sigecomm", "sigcomm", "infocom", "nsdi", "conext", "imc", "mobicom", "mobisys",
    "icnp", "cnsm", "noms", "netsoft", "globecom", "icc ", "wcnc", "ifip",
    "ieee access", "sensors", "electronics", "applied sciences", "future internet",
    "pacific", "ieee conference", "ieee symposium", "ieee international conference",
    "ieee transactions on machine learning in communications",
]


def good(v):
    if not v:
        return None
    lv = v.lower()
    return any(g in lv for g in GOOD)


def run(q):
    r = openalex_search(q, per_page=25)
    return q, alex_rows(r)


out = {}
with ThreadPoolExecutor(max_workers=4) as ex:
    for q, rows in ex.map(run, TOPIC_QUERIES):
        out[q] = rows
        print("done: %-58s -> %d" % (q[:58], len(rows)), flush=True)

json.dump(out, open(sys.argv[1], "w"), indent=1)

seen = {}
for q, rows in out.items():
    for r in rows:
        k = (r.get("title") or "").lower().strip()
        if k and k not in seen:
            r["_q"] = [q]
            seen[k] = r
        elif k:
            seen[k]["_q"].append(q)
print("\n=== UNIQUE:", len(seen))
ranked = sorted(seen.values(), key=lambda r: -(r.get("cited_by") or 0))
for r in ranked:
    g = good(r.get("venue"))
    if g is False:
        continue
    print("%5s | %-4s | %-46s | %s" % (r.get("cited_by"), r.get("year"),
                                      (r.get("venue") or "(none)")[:46],
                                      (r.get("title") or "")[:100]))
