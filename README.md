# PhD Literature Review — AI-Native Network Management and Orchestration for 5G/6G

A verified academic literature review across five research areas:

1. **Flow / packet / traffic scheduling** in 4G/5G/6G (RAN, 5G core, transport, TSN-5G, O-RAN)
2. **Network and service orchestration** (NFV/SDN, slicing, multi-domain, O-RAN SMO, cloud-native)
3. **Multipath transport and scheduling** (MPTCP, MPQUIC, ATSSS, multi-connectivity)
4. **LLM / AI agents for network management** and their benchmarks
5. **LLM fine-tuning, pruning, quantisation and distillation** for networking

**162 papers**, bibliographically verified against Crossref/OpenAlex. **117 carry a DOI, and
116 of those were confirmed by title match** in a final verification pass.

---

## Deliverables

| File | Contents |
|---|---|
| `01_flow_schedulers.csv` | 32 papers where scheduling is a central contribution — 34 extracted fields |
| `02_orchestrators.csv` | 26 orchestration papers, each classified as true orchestrator / optimisation engine / controller / architecture / agent / LLM orchestrator / survey |
| `03_multipath_schedulers.csv` | 33 multipath papers — 31 fields (protocol, paths, scheduler location, reordering, congestion control, baselines, results) |
| `04_llm_network_agents.csv` | 35 LLM/agent papers and benchmarks — 39 fields (model, tools, agent architecture, closed loop, benchmark, cost, hallucination) |
| `05_llm_efficiency_networking.csv` | 36 fine-tuning / pruning / quantisation / distillation papers — 33 fields |
| `06_master_literature.csv` | All 162 papers with category, relevance, evaluation quality and reproducibility quality |
| `07_research_matrix.csv` | 162 papers × 25 binary capability flags |
| `08_experimental_parameters.csv` | 161 rows of literally extracted parameters (users, UEs, gNBs, paths, bandwidth, latency targets, episodes, learning rates, GPU, simulator, testbed) |
| `09_paper_summaries.md` | 49 paper-by-paper summaries in a fixed 15-section structure |
| `10_gap_report.md` | Landscape analysis, benchmark landscape, platform comparison, cross-area matrix, 10 gaps, 10 candidate research questions, reading order |
| `11_search_log.md` | Method statement: tooling, queries, provenance model, quality control, limitations, DOI verification |
| `12_key_papers.md` | Key papers, the 20-paper learning-order sequence, and the proposed PhD architecture with a 4–8 week plan |

---

## How to read the evidence levels

Automated retrieval of IEEE Xplore returns HTTP 202 with an empty body, and ACM DL,
ScienceDirect, SSRN and HAL were variously blocked. For paywalled papers with no
open-access version, technical fields therefore come from the abstract only.

Every record carries an evidence level:

| Level | Meaning |
|---|---|
| `BIB` | Bibliographic data verified; technical fields limited to what the title/venue/type support |
| `ABS` | Publisher abstract retrieved and read |
| `FULL` | Open-access full text (arXiv, institutional repository, accepted manuscript) retrieved and read |
| `SUB` | Reported by a research subagent that names its source URL; bibliographic fields independently Crossref-verified |

**`NA` in a technical field means "not verifiable from a source retrieved in this session" —
never "the paper does not do this".** The 91% `NA` rate in `08_experimental_parameters.csv`
is a finding about reporting practice in this subfield, not a defect in the extraction.

Because OpenAlex rate-limited the final discovery wave, **every negative statement in these
reports is phrased as "not found in this search", never "does not exist".**

---

## Headline findings

- **No peer-reviewed benchmark was found that evaluates LLM/agent performance on 5G/6G
  network management with SLA-level outcome metrics in a closed loop.** Roughly 30 benchmark
  efforts exist for networking and telecom generally; the nearest 5G-core effort (OperAID,
  IEEE NetSoft 2026) injects Kubernetes-level faults and scores remediation success.
- **There is no type-(A) true orchestrator implementation in the corpus.** What is called
  orchestration is mostly resource allocation or architecture.
- **Zero papers combine a multipath scheduler with O-RAN.** The multipath literature is
  endpoint-local and cannot receive network-level objectives.
- **No paper reports a size-versus-quality trade-off for network-domain LLMs measured on
  network decisions.** Every such curve found uses an NLP proxy metric.
- **Latency forces a tiered architecture:** measured values range from 0.847 ms (on-device) to
  35 s (intent translation), against near-RT budgets of 10 ms–1 s.

### Bibliographic corrections made

Six DOIs in circulation resolved to *different, unrelated papers* and were corrected: ECF,
CMT-QA, TinyBERT, Telco-RAG, LiveStream Meta-DAMS and DAPS. Eleven further DOIs did not
resolve and are recorded as `NA` with a note. Two titles in circulation **do not exist** and
were replaced with verified substitutes. Full detail in `11_search_log.md` §7.

---

## Repository layout

```
*.csv, *.md              the 12 deliverables
data/                    machine-readable verified records (master_full.json, per-area JSON, DOI QC)
tools/                   the scripts used: Crossref/OpenAlex verification, matrix QC, CSV generation
sources_*_research/      the raw extraction reports behind the characterisations
```

Downloaded PDFs and HTML captures (~110 MB) are excluded via `.gitignore`; the extracted
findings are all in the committed reports.

## Reproducing the tables

```bash
python3 tools/verify2.py data/seed_titles.json data/seed_verified.json   # title verification
python3 tools/get_meta.py data/dois.txt data/crossref_meta.json          # Crossref enrichment
python3 tools/qc_matrix.py                                               # capability matrix
python3 tools/gen_csv.py                                                 # regenerate all CSVs
```
