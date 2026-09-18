# Extraction spec (READ FULLY BEFORE STARTING)

You are extracting detailed technical characterizations of peer-reviewed papers on
MULTIPATH TRANSPORT AND SCHEDULING (MPTCP, MPQUIC, multipath in 5G/6G) for a PhD
literature review on AI-native network management.

## HARD RULES (violating these ruins the deliverable)

1. NEVER invent numbers, baselines, testbeds, results, DOIs, or venues.
2. If a field is not stated in the source you actually retrieved, write exactly:
   `NOT REPORTED`
3. If you could only retrieve the ABSTRACT (not the full text), you MUST say so
   explicitly in field 21 and ONLY report what the abstract states. Do not fill
   fields from memory, from the title, or by plausible inference.
4. Do NOT use your prior/training knowledge as a source. Only report what is in a
   document you actually fetched in this session.
5. Distinguish TESTBED from SIMULATION (e.g. "Linux kernel testbed with real
   WiFi+LTE" vs "ns-3 simulation" vs "emulated with tc/netem"). Never blur these.
6. Distinguish PACKET-LEVEL scheduling (per-segment path assignment) from
   FLOW-LEVEL / path selection / routing.
7. Quote exact sentences (in quotation marks) whenever you give a number or an objective.
   If you paraphrase a number, still give the exact figure.
8. If two sources disagree about venue/year, report both and say which you trust and why.

## HOW TO RETRIEVE (network access works; curl + pdftotext are available)

- Prefer OPEN ACCESS full text: arXiv, USENIX, IETF RFCs, ACM OpenTOC, HAL,
  university repositories (DiVA, UCL Discovery, KTH, Karlstad), J-STAGE, IEEE Access
  (gold OA), MDPI, ResearchGate author copies, author homepages, Semantic Scholar
  (`https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=title,abstract,openAccessPdf,venue,year,externalIds`),
  OpenAlex (`https://api.openalex.org/works/doi:<doi>` -> `best_oa_location.pdf_url`),
  Unpaywall (`https://api.unpaywall.org/v2/<doi>?email=research@example.org`).
- Download PDFs to your assigned pdf dir and convert with:
  `pdftotext -layout file.pdf file.txt`
  Then use the read/grep tools on the .txt.
- For IEEE Xplore paywalled papers, try in this order: (a) OpenAlex/Unpaywall OA link,
  (b) arXiv preprint (search arxiv.org), (c) author homepage / lab page PDF,
  (d) university repository, (e) Semantic Scholar `openAccessPdf`. If none works,
  retrieve the IEEE Xplore abstract page HTML and say ABSTRACT ONLY.
- Verify exact venue + year + DOI from a bibliographic API (Crossref:
  `https://api.crossref.org/works/<doi>`, or OpenAlex), not from a search snippet.

## OUTPUT FORMAT (exact, repeat for every paper assigned to you)

### <Paper title>
- **Authors / Year / Venue / DOI / peer-reviewed or preprint**
- **1. Number and type of paths**
- **2. Network architecture**
- **3. Transport protocol**
- **4. Scheduler location**
- **5. Scheduler inputs**
- **6. Path metrics used**
- **7. Scheduling decision**
- **8. Packet-level or flow-level scheduling**
- **9. Reordering handling**
- **10. Congestion-control interaction**
- **11. Objective**
- **12. Algorithm**
- **13. ML/DRL usage**
- **14. Simulator / testbed**
- **15. Traffic model**
- **16. Baselines**
- **17. Metrics**
- **18. Main result**
- **19. Limitation**
- **20. Research gap this suggests**
- **21. Best URL you actually retrieved, and whether you read full text or only abstract**

Field meanings:
- 1: WiFi/LTE/5G mmWave/satellite/datacenter; homogeneous or heterogeneous; exact count
- 2: end-to-end path topology, proxy? middlebox? MPTCP-capable server? 5G core?
- 3: MPTCP v0/v1, MPQUIC, CMT, custom, ATSSS
- 4: kernel, userspace, proxy, core network, RAN
- 5: exact signals: SRTT/RTT, cwnd, delivery rate, queue occupancy, loss rate, buffer estimate, BLEST-style "penalisation", send-buffer...
- 6: e.g. RTT, one-way delay, bandwidth, loss, energy, cost
- 7: exact action space (e.g. "select path i for next segment", "split ratio", "steer X% to 3GPP access")
- 8: packet-level vs flow-level vs path selection
- 9: how reordering is detected/handled, penalty term, receive-buffer/ATD
- 10: which CC (LIA, OLIA, wVegas, BALIA, BBR, Cubic) and the interaction mechanism
- 11: quote the objective if stated
- 12: exact algorithm
- 13: yes/no + exact DRL variant + network architecture (layers, neurons) if stated
- 14: exact simulator/testbed
- 15: bulk transfer, web, video, synthetic
- 16: exact baseline names as the paper names them
- 17: exact metrics
- 18: EXACT numbers with the comparison, quoted
- 19: limitations as stated by authors + methodological limitations you observe
- 20: research gap
- 21: URL + "FULL TEXT" or "ABSTRACT ONLY"

Write your output to the exact file path your prompt assigns. Do not write anything
else to that directory. Report back with: file path, papers completed, and a list of
any paper where you got ABSTRACT ONLY.
