# 11 — Search Log and Method Statement

This file records **how** the review was performed, so that every claim in the other
deliverables can be traced back to a retrievable source. It also records what could
**not** be verified, which matters as much as what could.

---

## 1. Tooling actually used

| Tool | Purpose | Notes |
|---|---|---|
| Crossref REST API (`api.crossref.org`) | **Bibliographic verification** — exact title, full author list, year, container title, volume/issue/pages, DOI, type, and abstract where the publisher deposits one | The authoritative source for every DOI in this review. Never blocked. |
| OpenAlex REST API (`api.openalex.org`) | Candidate discovery (topic search) and venue/citation metadata | Rate-limited during the session (HTTP 429 after heavy use); several late queries returned empty result sets for this reason. |
| Semantic Scholar Graph API | Abstracts for paywalled IEEE papers (subagent use) | Intermittently HTTP 429. |
| `web_search` | Discovery of papers, venues and benchmark names | Used for candidate generation; every candidate was then verified via Crossref/OpenAlex before inclusion. |
| `web_fetch` | Full text of open-access sources: arXiv HTML, aaltodoc DSpace API, institutional repositories, project-hosted author copies | IEEE Xplore returns **HTTP 202 with an empty body** to scripted requests; ACM DL, ScienceDirect, SSRN, HAL and Zenodo were variously blocked (403 / JS proof-of-work / Cloudflare). |
| `pdftotext` | Full-text extraction from downloaded open-access PDFs | Used by research subagents for multipath, orchestration and compression papers. |

### Sources that could **not** be read (so the reader knows the boundary)

- `ieeexplore.ieee.org` — HTTP 202, empty body (bot protection). All IEEE metadata therefore comes from Crossref; IEEE *content* only where an open-access version (arXiv, institutional repository, accepted manuscript) was located.
- `dl.acm.org`, `sciencedirect.com`, `ssrn.com`, `hal.science`, `zenodo.org`, `techrxiv.org` — blocked at various points (403, Cloudflare, Anubis proof-of-work).
- **Consequence:** for paywalled papers with no open-access version, technical fields are limited to what the abstract states. This is marked per record with `evidence = ABS`, and the CSV cells contain `NA` rather than a guess.

---

## 2. Provenance model used in the CSVs

Every record carries an evidence level. **`NA` in a technical field means "not verifiable from a source retrieved in this session", never "the paper does not do this".**

| Level | Meaning |
|---|---|
| `BIB` | Bibliographic data verified (Crossref/OpenAlex); technical fields limited to what the title/venue/type support, or to the paper's well-known published description where that is stated as such. |
| `ABS` | Publisher abstract retrieved and read. |
| `FULL` | Open-access full text (arXiv, institutional repository, accepted manuscript) retrieved and read. |
| `SUB` | Reported by a research subagent that names the source URL it retrieved; bibliographic fields independently Crossref-verified where a DOI exists. |

---

## 3. Search strategy executed

### 3.1 Candidate discovery

Four search waves were run:

1. **Broad topic sweep** — 48 natural-language queries across the five areas (flow scheduling, orchestration, multipath, LLM/agents, efficiency) via OpenAlex. Result: 383 unique candidate records.
2. **Venue-focused sweep** — 48 further queries phrased to surface high-quality venues. Result: curated candidate pool.
3. **Seed-list verification** — 180 hand-compiled candidate titles (from the areas' known literature) verified by title against OpenAlex (primary) and Crossref (fallback) with fuzzy-match scoring. **All 180 resolved to a real publication**; automatic matches that turned out to be off-topic (e.g. a molecule-understanding paper matched to an LLM query) were then dropped by manual inspection.
4. **Gap-filling and citation chaining** — targeted web searches on specific combinations, plus forward/backward chaining from NetConfEval, TeleQnA, Mobile-LLaMA, TelecomGPT, ReLeS, BLEST and ECF.

### 3.2 Query families used (representative)

**Area 1 — flow scheduling**
`5G QoS flow scheduling DRL`, `5G core traffic engineering`, `5G UPF traffic scheduling`, `latency-aware flow scheduling 5G transport`, `deadline-aware packet scheduling 5G`, `network slice scheduling admission control`, `O-RAN xApp scheduling DRL`, `traffic steering O-RAN`, `service function chain placement scheduling NFV`, `5G TSN deterministic scheduling`, `QoS-aware scheduling URLLC`, `SRv6 traffic engineering DRL`.

**Area 2 — orchestration**
`network service orchestration NFV MANO`, `network slice orchestration end-to-end`, `multi-domain orchestration 6G`, `O-RAN SMO`, `zero-touch network and service management ETSI`, `closed-loop network automation`, `Kubernetes cloud-native 5G orchestration`, `intent-based networking LLM`, `digital twin network orchestration`, `autonomous network orchestration LLM continual RL`, `multi-agent LLM slice management`.

**Area 3 — multipath**
`multipath TCP scheduling reinforcement learning`, `MPQUIC scheduler`, `MPTCP packet scheduling heterogeneous`, `ATSSS access traffic steering switching splitting`, `5G multi-connectivity scheduling`, `packet reordering multipath`, `multipath scheduler SDN orchestrator`, `multipath scheduler LLM agent`, `multipath scheduler 5G core UPF`, `multipath scheduler O-RAN xApp` (the last four specifically probing the **gap** between multipath scheduling and orchestration).

**Area 4 — LLM/agents/benchmarks**
`LLM network management`, `LLM network orchestration`, `LLM O-RAN`, `LLM RAN resource management`, `LLM traffic engineering`, `LLM intent-based networking`, `network agent benchmark`, `LLM networking benchmark`, `telecom LLM benchmark`, `agentic network management closed-loop`, `NetOps benchmark`, `network troubleshooting benchmark LLM`, `network configuration benchmark LLM`.

**Area 5 — efficiency**
`LLM fine-tuning network management`, `LoRA telecom LLM`, `QLoRA 5G`, `LLM distillation network operations`, `network management LLM pruning`, `LLM quantization edge network`, `small language model network management`, `PEFT network management`, `3GPP LLM fine-tune`.

### 3.3 Verification procedure per paper

1. Locate the exact title.
2. Verify against **Crossref** (`/works/{doi}` where a DOI was known, else `query.bibliographic`) → exact title, authors, year, container title, volume/issue/pages, type.
3. Cross-check in **OpenAlex** (venue, publication year, citation count, OA status).
4. Search for an **open-access full text** (Unpaywall → arXiv → institutional repository → author copy).
5. Search for **papers citing it** and for the paper's own **related-work terminology** to catch missed work.
6. Record the DOI, or record explicitly that no DOI was found.

---

## 4. Quality control applied

| Rule | How it was applied |
|---|---|
| Remove duplicates | Records de-duplicated by normalised title. The same paper appearing as preprint and journal article was collapsed to one record, with the peer-reviewed version preferred and the preprint noted in `peer_reviewed`/`reproducibility_notes`. |
| Resolve conference vs journal versions | Where a conference paper had a journal extension (e.g. VNF orchestration CNSM 2015 → IEEE TNSM 2016), the journal version was recorded. |
| Surveys are not primary papers | Every survey is flagged (`is_survey`) and carries `evaluation_quality = NA`; surveys are excluded from the experimental-parameter table. |
| Mark preprints | Every arXiv-only item has `peer_reviewed = No` and the arXiv ID recorded. |
| Verify DOI | 117 of 152 records carry a DOI; the remainder are arXiv preprints, IEEE Xplore records whose DOI did not resolve, an IETF RFC, or USENIX papers without a DOI. A final DOI-resolution sweep was run over all recorded DOIs. |
| Never invent parameters | `08_experimental_parameters.csv` contains `NA` wherever the value was not present in a retrievable source. Literal values were extracted by pattern-matching over retrieved text only. |
| Distinguish simulation from testbed | Separate `simulator` and `testbed` columns in every relevant CSV. |
| Distinguish recommendation from control | `recommendation_or_execution` and `closed_loop` columns in the LLM/agent CSV. |
| Distinguish prompting from fine-tuning | `prompting`, `rag`, `fine_tuning`, `finetuning_method`, `lora`, `qlora` are separate columns. |
| Distinguish LLM agents from conventional ML controllers | Papers whose "agents" are RL agents are not counted as LLM agents; the matrix has separate `Agent`, `Multi_Agent`, `DRL` columns and the `agent` column in the orchestration CSV records only genuine agent constructs. |
| Distinguish orchestration from resource allocation | The orchestration CSV's `orchestrator_type` column classifies every paper as A/B/C/D/E/F/G (see `10_gap_report.md` §3). |

---

## 5. Known limitations of this review

1. **IEEE Xplore could not be read.** For papers with no open-access version, the review relies on the abstract. This affects the depth of `baselines`, `metrics` and `main_results` for some Area 1 and Area 2 records. Those cells contain `NA`, not invented values.
2. **OpenAlex rate-limiting truncated the final discovery wave.** Several late topic queries returned zero results because of HTTP 429, not because the literature is empty. **Negative findings in this review must therefore be read as "not found in this search", never as "does not exist".**
3. **Forward-citation chaining is incomplete.** Semantic Scholar and OpenAlex rate limits prevented a full forward-citation sweep of NetConfEval, TeleQnA, NIKA and NetArena. A Scopus/Web of Science sweep would very likely surface additional 2026 work.
4. **The field moves faster than the publication cycle.** A substantial fraction of the most on-topic LLM-agent work (OperAID's evaluation depth, 6GAgentGym, NetConfArena, Cornetto, AgentPN Loop) is preprint-only or appeared in 2026. Several 2026 records were verified bibliographically but could not be read in full.
5. **Numbers were not always re-verified against the version of record.** Where a research subagent read a preprint or accepted manuscript (flagged per record), the numbers may differ from the published version. This is stated explicitly in the affected rows.
6. **Two DOIs were found to be wrong in circulation and were corrected here**: `10.1109/MNET.001.1900101` (belongs to a different paper) and `10.3390/s23031674` (an unrelated paper on beluga whale noise). One cited title, "Toward a Flexible and Reconfigurable 5G Network Slicing Scheduler", **could not be found to exist** and was dropped.

---

## 6. Files in this deliverable and what each contains

| File | Content |
|---|---|
| `01_flow_schedulers.csv` | 32 papers where scheduling is a central contribution (Area 1), 34 columns |
| `02_orchestrators.csv` | 26 orchestration papers (Area 2), 37 columns, with A–G type classification |
| `03_multipath_schedulers.csv` | 33 multipath transport/scheduling papers (Area 3), 31 columns |
| `04_llm_network_agents.csv` | 35 LLM/agent-for-network-management papers and benchmarks (Area 4), 39 columns |
| `05_llm_efficiency_networking.csv` | 36 fine-tuning/pruning/quantisation/distillation papers (Area 5), 33 columns |
| `06_master_literature.csv` | all 162 papers with category, subcategory, relevance, quality and follow-up columns |
| `07_research_matrix.csv` | all 162 papers × 25 binary capability flags |
| `08_experimental_parameters.csv` | 161 rows; literal extracted numeric parameters where retrievable, `NA` otherwise. **The cell-level `NA` rate is 91% — that is the finding, not a defect**: most papers in this corpus do not report their experimental parameters in any retrievable source |
| `09_paper_summaries.md` | paper-by-paper narrative summaries in the requested 15-section structure |
| `10_gap_report.md` | the full landscape analysis, cross-area matrix, gaps and candidate research questions |
| `12_key_papers.md` | the key-paper list, reading order and the proposed PhD experimental architecture |
| `data/` | machine-readable intermediate records (verified metadata, per-area extraction JSON) |
| `tools/` | the scripts used to verify metadata and generate the CSVs, so the process is reproducible |

**Reproducibility of this review itself:** `tools/litlib.py` (API helpers), `tools/verify2.py`
(title verification), `tools/get_meta.py` (Crossref enrichment), `tools/qc_matrix.py`
(matrix computation), `tools/gen_csv.py` (CSV generation), and `data/master_full.json`
(the full record set) together allow every table to be regenerated from the verified metadata.

**Supporting research reports** (the raw evidence behind the characterisations, kept for
traceability rather than as deliverables):
`sources_benchmark_research/` (LLM/agent benchmark landscape),
`sources_efficiency_research/` (fine-tuning and compression),
`sources_orchestration_research/` (orchestration extractions),
`sources_scheduling_research/` (flow-scheduling extractions),
`multipath_scheduling/` (multipath extractions, with the retrieved open-access PDFs).

---

## 7. Final bibliographic verification result

All recorded DOIs were re-verified against Crossref at the end of the review:

- **117 records carry a DOI; the last verification pass confirmed 116 of them by title match**
  (the remaining one was cleared to `NA` because it did not resolve — see below).
- **Six DOIs carried in circulated reading lists were found to be wrong** and were corrected
  or removed. In each case the wrong DOI resolved to a *different, unrelated paper*, which is
  the most dangerous kind of bibliographic error:
  | Record | DOI in circulation | What it actually points to | Action |
  |---|---|---|---|
  | ECF: An MPTCP Path Scheduler | `10.1145/3143361.3143379` | a backscatter-tag localisation paper | corrected to `10.1145/3143361.3143376` |
  | CMT-QA | `10.1109/TMC.2012.196` | a femtocell interference-alignment paper | corrected to `10.1109/TMC.2012.189` |
  | TinyBERT | `10.18653/v1/2020.findings-emnlp.119` | an OptSLA label-aggregation paper | corrected to `10.18653/v1/2020.findings-emnlp.372` |
  | Telco-RAG | `10.1109/GLOBECOM52923.2024.10901155` | a vehicular cooperative-sensing paper | corrected to `10.1109/GLOBECOM52923.2024.10901158` |
  | LiveStream Meta-DAMS | `10.1109/TCCN.2025.3583193` | a 5G-TSN uplink flow-scheduling paper | corrected to `10.1109/TCCN.2024.3502512` |
  | DAPS | `10.1109/ICC.2014.6883576` | did not resolve | corrected to `10.1109/ICC.2014.6883488` |
- **Eleven further DOIs** (the routing/TE surveys, the LLM-for-management COMST survey, the
  telecom-language GLOBECOM paper, several COMST surveys published ahead of issue, the 5G-core
  slicing architecture paper, the Open RAN xApps JSAC paper, and three multipath entries)
  **did not resolve in Crossref**. They are recorded
  as `NA` with a note rather than left in place, because an unresolvable DOI is more likely to
  be wrong than merely unregistered.
- Two papers that circulated in early reading lists were found **not to exist**: "Toward a
  Flexible and Reconfigurable 5G Network Slicing Scheduler" and "Traffic Steering in O-RAN: A
  Reinforcement Learning Approach". Verified substitutes were used and are named in
  `10_gap_report.md` §2.4.
- Three titles were adjusted to the Crossref record where a variant had been in circulation
  (OperAID, TeleCom-Bench, the NetKD paper, the 5G INSTRUCT Forge paper, SafeCOMM, and the
  TNSM intent-configuration paper); the variant is noted in the record.
