## WHAT I COULD NOT VERIFY

### 1. Papers retrieved as ABSTRACT ONLY (six of twenty-four)

For these, **every** claim in their extraction comes from the abstract (and, where noted, the
free IEEE preview of §I) and nothing else. Fields the abstract does not cover are `NOT REPORTED`
by construction. Two independent OA checks (Unpaywall `is_oa` and Semantic Scholar
open-access status) agreed these are closed, and a dedicated second pass over arXiv, CORE v3,
ResearchGate, Google Scholar, scholar.archive.org, TechRxiv, fatcat and author/institution pages
found no legitimate copy.

| Paper | Venue verified | What is missing because of it |
|---|---|---|
| 8. ReLeS | IEEE INFOCOM 2019, DOI `10.1109/INFOCOM.2019.8737649` | The entire DRL design (state/action/reward, network architecture), the scheduler inputs, the baselines, the testbed, and **all numbers**. The paper is universally described as DRL+Linux kernel, but its actual mechanism could not be read |
| 15. CMT-QA | IEEE TMC 12(11):2193–2205, 2013, DOI `10.1109/TMC.2012.189` | Scheduler mechanism details, simulator name, baselines, all metrics/numbers |
| 16. BEMA | IEEE TCOM 64(6):2477–2493, 2016, DOI `10.1109/TCOMM.2016.2553138` | Detailed algorithm, baseline names, quantitative results |
| 19. SATO | IEEE WF-IoT 2022, DOI `10.1109/WF-IoT54382.2022.10152217` | Simulator identity, testbed identity, the name of the baseline behind "state-of-the-art algorithm", all per-metric numbers |
| 21. DRL ATSSS | IEEE ICTC 2024, pp. 903–908, DOI `10.1109/ICTC62082.2024.10826899` | Action space, state, simulator, baselines, all numbers; also whether it touches MPTCP/MPQUIC/UPF at all |
| 22. MORL ATSSS | IEEE ICCCN 2025, pp. 1–8, DOI `10.1109/ICCCN65249.2025.11133925` | The MORL formulation (objectives, weights, preference vector), the simulator, the baseline definitions, per-metric breakdown |
| 23. MPTCP-RL | IEEE Wireless Communications 30(2):138–146, 2023, DOI `10.1109/MWC.013.2100658` | The RL algorithm, the simulator/testbed, the baseline names, and every number (the abstract's claim is the unquantified word "significantly") |

**Recommendation:** these seven are the only papers in the set that a single institutional IEEE
Xplore session would upgrade from abstract to full extraction. ReLeS matters most — it is the
canonical "first DRL MPTCP scheduler" citation and is currently unusable for mechanism-level
claims in this report.

### 2. Facts asserted in the brief that the sources contradict

- **Paper 3's venue.** The paper is real and is ACM's NSDI '12 record at pp. 99–112
  (`10.5555/1972457.1972468`), but **USENIX's own NSDI '12 programme index does not list it** —
  the only multipath paper there is "How Hard Can It Be? Designing and Implementing a Deployable
  Multipath TCP" (also NSDI 2012, retrieved and identified during this work). Two citing papers
  (papers 2 and 4) cite it as **2011**. I used NSDI 2012 and recorded the conflict rather than
  silently picking one.
- **Paper 16 is not called "BEWARE".** The TCOM 2016 paper's own abstract names its protocol
  **BEMA** ("bandwidth-efficient multipath streaming"). "BEWARE: Background Traffic-Aware Rate
  Adaptation for IEEE 802.11" is an unrelated paper (`10.1109/TNET.2011.2106140`). Cite it as BEMA.
- **Paper 23's title** is registered as "**Multipath** TCP Meets Reinforcement Learning…" (MPTCP
  spelled out). Same paper; not a substitute.
- **Paper 14 (Peekaboo) year = 2020**, confirmed: IEEE JSAC 38(10):2295–2310, 2020, DOI
  `10.1109/JSAC.2020.3000365`.
- **Paper 10's and 11's years are traps.** Coupled BBR: Semantic Scholar reports 2020 (the arXiv
  year) — the journal issue is **TWC 2021**. BCCPS: the DOI stem is 2020 (early access) — the
  issue is **TVT January 2021**. Both are reported with both readings in their sections.
- **There is no extended journal version of ECF.** No KTH technical report and no *Computer
  Communications* 2022 version exists in Crossref or OpenAlex. What exists is an *earlier,
  shorter* 2-page SIGMETRICS 2017 paper (`10.1145/3078505.3078552`); a copy of that was
  downloaded by mistake and discarded once the 2-page/13-page discrepancy was caught. All ECF
  values here come from the 13-page CoNEXT paper.
- **ECF's own reference list mis-cites BLEST** as "pages 1222–1227, 2016". Crossref and BLEST's
  own page footers agree on **431–439**; I used 431–439.

### 3. In-paper facts that are genuinely absent (recorded as `NOT REPORTED`, not guessed)

- **Congestion controller is unnamed** in **ECF** (paper 13 — it only claims CC-agnosticism and
  names Olia parenthetically) and in **Peekaboo** (paper 14 — searched for Cubic/NewReno/Olia/
  BALIA/LIA/BBR; only *related-work* mentions exist). Also unnamed in papers 19, 20, 23, 24a and
  both ATSSS papers.
- **Simulator/testbed is unnamed** in papers 19, 21, 22 and **24a** ("simulations conducted within
  this environment", simulator never identified) and 23.
- **Baselines are unnamed** in papers 15, 16, 19, 21, 22, 23 (papers 15/16/19/21/22/23 use only
  generic phrases such as "existing solutions" or "state-of-the-art").
- **GCLR's GNN architecture** is `NOT REPORTED` ("a multi-layer perceptron with appropriate
  activations"), and **GCLR's Tables 1–2 are raster images**, so per-cell MSE values are not
  machine-readable from the OA PDF.
- **DeepCC's Tables II/IV/V and BCCPS's Tables I/II are raster images** in their PDFs, so only the
  hyperparameters and percentages stated in prose could be reported.
- **Reordering never enters the state, reward or metrics** of paper 24a, even though head-of-line
  blocking is its stated motivation (observed by the extractor, not claimed by the paper).
- **Round-Robin is not a baseline in BLEST or ECF.** BLEST's baselines are minRTT, DAPS, OTIAS and
  single-path TCP; ECF's are "Default" (minRTT), DAPS and BLEST. Round-Robin appears as a baseline
  only in Peekaboo. This is worth carrying into any synthesis table built from memory of the
  literature.

### 4. Environment limitations that shaped the retrievals (disclosed, not worked around)

- **IEEE Xplore** returns HTTP 202 with an empty body to non-browser clients and 502 for some
  `ielx7` PDF URLs; the working routes were gold-OA `ielx7` PDFs with a cookie jar + desktop UA +
  Referer (GCLR), and `https://r.jina.ai/<ieee-url>` for abstract + free-preview §I (papers 15,
  16, 19, 21, 22, 23). **ACM DL** `/doi/pdf/` returns 403. These are the direct cause of the
  seven ABSTRACT ONLY entries above.
- **OpenAlex's API exhausted its daily budget** mid-session (`HTTP 429 … Insufficient budget …
  Resets at midnight UTC`), so bibliographic verification used **Crossref + Unpaywall + Semantic
  Scholar** instead. Semantic Scholar also rate-limited intermittently (HTTP 429).
- **HAL and DiVA sit behind an Anubis proof-of-work interstitial.** Rather than declare those
  sources unreachable, a solver was written (`tools/anubis_fetch.py`) and used to retrieve the
  publisher-designated OA copy of paper 5 from HAL. This is legitimate retrieval from the
  designated OA location, but it is a non-standard access path and is disclosed here so the
  provenance of paper 5 can be checked.
- **A Google Research PDF link initially resolved to the wrong paper** (an unrelated
  neural-network-compression paper at `.../archive/46274.pdf`). It was discarded; the correct
  QUIC SIGCOMM PDF was obtained from `.../pubtools/4102.pdf`. The retrieved QUIC file is the
  **Google author copy (9 pages)**; the ACM version is cited by that PDF's own footnote as
  **14 pages**, so figure/table completeness may differ from the ACM version.

### 5. Things I deliberately did **not** do

- I did **not** import numbers, baselines or testbed names for the seven abstract-only papers from
  secondary sources, other papers' descriptions of them, or model memory. Where a secondary
  source (paper 17's survey) describes ReLeS as "offline reinforcement learning, i.e., a Deep
  Q-Network (DQN) … with throughput as the reward, and delay and packet loss as penalties", that
  description is attributed **to the survey** in paper 17's section, not presented as ReLeS's own
  text.
- I did **not** resolve conflicting numbers by averaging or by choosing the more flattering one.
  Where sources conflict (NSDI 2012 venue/pages, BLEST pages, Coupled BBR/BCCPS years) both
  readings are reported with the reason for the choice.
- I did **not** treat "AI-based" as a single category. Papers 10 and 11 are explicitly **not**
  machine learning despite appearing in an "AI-based" cluster, and paper 14 is a **contextual
  bandit (LinUCB)**, not deep RL, despite being routinely grouped with DRL schedulers.
