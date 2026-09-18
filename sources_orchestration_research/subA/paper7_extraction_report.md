# Extraction Report — paper7_vnf_placement_survey.txt

**Source file:** `/home/pouriaarefi/Documents/netorch_papers/subA/paper7_vnf_placement_survey.txt` (2104 lines, plain-text extraction of the PDF).

**Note on quoting:** the file is a two-column PDF extraction, so a numbered line often contains fragments of *both* columns concatenated. All quotes below are copied verbatim from the file with the line number(s) as printed there. Because of the column interleaving, a few quoted lines contain unrelated words belonging to the adjacent column; this is a property of the file, not of my transcription. Where a quote spans a column break I say so.

---

## 1. Bibliographic identity and document version

All of the following appears on the cover/reprint page (lines 1–49).

| Field | As printed in the file | Line |
|---|---|---|
| Title | `A Survey on the Placement of Virtual Resources and Virtual Network Functions` | 7 (also 55–56) |
| Authors | `Laghrissi, Abdelquoddouss; Taleb, Tarik` | 6 (also 57) |
| Venue | `IEEE Communications Surveys and Tutorials` | 11 |
| DOI | `10.1109/COMST.2018.2884835` | 15 |
| Year / date | `E-pub ahead of print: 01/01/2018` | 18 |
| Copyright year | `© 2018 IEEE.` | 45 |

Verbatim quotes:

- L7: `A Survey on the Placement of Virtual Resources and Virtual Network Functions`
- L6: `Laghrissi, Abdelquoddouss; Taleb, Tarik`
- L10–11: `Published in:` / `IEEE Communications Surveys and Tutorials`
- L14–15: `DOI:` / `10.1109/COMST.2018.2884835`
- L18: `E-pub ahead of print: 01/01/2018`
- L26–28: `Please cite the original version:` / `Laghrissi, A., & Taleb, T. (2018). A Survey on the Placement of Virtual Resources and Virtual Network` / `Functions. IEEE Communications Surveys and Tutorials. https://doi.org/10.1109/COMST.2018.2884835`

**Document version — it is the ACCEPTED MANUSCRIPT (peer-reviewed version), not the published/typeset version.** Two separate notices say so:

- L1–2: `This is an electronic reprint of the original article.` / `This reprint may differ from the original in pagination and typographic detail.`
- L22–23: `Document Version` / `Peer reviewed version`
- L43 (the decisive notice): `This is the accepted version of the original article published by IEEE.`
- L45–49: `© 2018 IEEE. Personal use of this material is permitted. Permission from IEEE must` … `be obtained for all other uses, in any current or future media, including` … `creating` `new collective works, for resale or redistribution to servers or lists, or reuse of any` `copyrighted component of this work in other works.`

Affiliation as printed (L132–137): `A. Laghrissi and T. Taleb are with the Department of Communications` / `and Networking, School of Electrical Engineering, Aalto University, 02150` / `Espoo, Finland. T. Taleb is also with the Centre for Wireless Communications` / `(CWC), University of Oulu, FI-90014 Oulu, Finland, and the Computer and` / `Information Security Department, Sejong University, 143-747 (05006) Seoul,` / `South Korea (emails: firstname.lastname@aalto.fi).`

Funding, as printed (L1737–1743): `This work was partially supported by the European Union’s` / `Horizon 2020 research and innovation programme under the` / `5G!Pagoda project with grant agreement No. 723172, and the` / `Academy of Finland’s Flagship programme 6Genesis (grant` / `no. 318927).`

---

## 2. Paper type — survey/tutorial with NO primary experiments by the authors

**It is a survey/tutorial. The file contains no original experiments, simulations, testbeds, datasets or numerical results produced by Laghrissi & Taleb.** It contributes (i) a taxonomy, and (ii) qualitative expert assessment tables. Every occurrence of the words *experiment / experimentation / simulation / results* in the body is attributed to a cited reference (see Section 10), never to the present authors.

Evidence that it is a survey:

- L217–221: `To the best knowledge of the authors, there is no extensive` / `survey, in the literature, on the problem of VNF placement in` / `cloud environments, apart from the work presented by Li et` / `al. in [119].` (the first line is the right column of the acronym table page, hence the split; `survey, in the literature...` is on L219)
- L250–254: `In comparison to the survey of Li et al., this survey is more` / `extensive and detailed as it discusses in depth the existing` / `VNF placement strategies and algorithms. It also classifies` / `the different solutions into different categories, distinguishing` / `between generic VNF placement and specific VNF placement.`
- L74–77 (abstract): `The paper then proposes` / `a classification of VNF Placement (VNFP) approaches, first,` / `regarding the general placement and management issues of` / `VNFs, and second, based on the target VNF type.`
- L1725–1726: `This survey is meant to be a reference` / `when investigating VNF and VM placement strategies.`
- L1727–1729: `Rele-` / `vant protocols, heuristics, algorithms, and architectures were` / `surveyed with the main motivation to propose, as future work,` / `efficient strategies to carry out efficient network slicing, in`

Evidence that the authors' own contribution is analytical/classificatory, not experimental — the only "own" artefact is expert assessment recorded in Tables IV–IX:

- L546–553: `Each of these objectives will be discussed in the following` / `sections (Sections V to X). Also, for each section, we sum-` / `marize the challenges and suggestions, concerning the most` / `relevant/recent research works, in a dedicated table (Tables IV` / `to IX). Each table contains the advantages and disadvantages` / `that we have assessed for the adopted solutions and frame-` / `works, as well as enhancement propositions that could guide` / `the reader to spot possible research directions.`

Negative check: grepping the whole file for `machine learning`, `deep learning`, `reinforcement`, `Tabu`, `Mininet`, `GLPK`, `Kubernetes`, `ZSM`, `ONAP`, `OSM` returns **no** matches. Grepping for author-voice experiment language returns no instance of a self-run experiment (the `we`/`our` hits are all "we depict in Fig. 3", "we discuss", "we refer to the costs", "We believe", "we observed" — L244, L268, L318, L547, L744, L1660, L1669, L1674, L1694).

**List of the survey's own experiments: NOT REPORTED** (none exist in the file).

---

## 3. Taxonomy used by the survey

The survey runs **two parallel taxonomies**, one for VM placement and one for VNF placement, plus a use-case taxonomy for NFV.

### 3.1 Structural outline (verbatim section headings as printed in the file)

| Line | Heading (verbatim, small-caps spacing as in file) |
|---|---|
| 82 | `I. INTRODUCTION` |
| 281 | `II. V IRTUAL M ACHINES` |
| 306 | `A. VM use cases` |
| 364 | `III. V IRTUALIZED N ETWORK F UNCTION AS A MAIN` (continues L366 `COMPONENT OF N ETWORK F UNCTION V IRTUALIZATION`) |
| 445 | `IV. V IRTUAL M ACHINE P LACEMENT` |
| 525 | `V. E NERGY- AWARE VMP` |
| 531 | `A. Power consumption` |
| 578 | `B. Number of activated nodes` |
| 735 | `VI. C OST RELATED TO THE C LOUD S ERVICE P ROVIDERS ’` (continues L736 `PROFIT AND VIRTUAL RESOURCES USAGE`) |
| 753 | `A. Online Cost-aware VMP` |
| 781 | `B. Offline Cost-aware VMP` |
| 774 | `VII. Q O S` |
| 793 | `A. Offline QoS-aware VMP` |
| 874 | `B. Online QoS-aware VMP` |
| 966 | `VIII. R ESOURCE USAGE` |
| 1090 | `IX. R ELIABILITY- AWARE VMP` |
| 1225 | `X. L OAD BALANCE - AWARE VMP` |
| 1210 | `XI. V IRTUALIZED N ETWORK F UNCTIONS PLACEMENT` |
| 1235 | `A. General Virtualized Network Functions placement` |
| 1370 | `B. VNF placement and the VNF forwarding graph` |
| 1400 | `C. VNF placement and the VNF Chain Placement Problem` |
| 1459 | `D. VNF Placement and VNF replications` |
| 1497 | `XII. S PECIFIC NETWORK FUNCTIONS PLACEMENT` |
| 1499 | `A. Transcoder and cache placement` |
| 1527 | `B. S-GW and P-GW placement` |
| 1617 | `C. Virtual Deep Packet Inspection placement` |
| 1598 | `D. Replication of Content Distribution Networks` |
| 1664 | `XIII. K EY CHALLENGES AND LESSONS LEARNED` |
| 1711 | `XIV. C ONCLUSION` |

### 3.2 VMP taxonomy (dimensions + categories)

Primary axis = **online (dynamic) vs offline (static)**:

- L462–463: `process can be carried out either offline (static) or online (dy-` / `namic) [135]–[137].`
- L467–469: `In the online VMP approach, in addition` / `to the placement decisions, DC operators periodically collect` / `data and decide, e.g., when the load of the system increases,`
- L474–476: `whether a VM placement shuffle is needed.` … `Offline VMP` (table cell)
- L525–526: `Table II shows a global classification of VMP solutions into` / `online and offline approaches, while Table III categorizes the`
- L527–530: `different VMP solutions as per their target objective. Some` / `of the solutions are dedicated to single objectives (mono-` / `objective), and some have several objectives (multi-objectives)` / `(see Fig. 5). Among the objectives are the following:`

Secondary axis = **objective** (the bullet list, L530–545):

- L531–533: `• Energy consumption minimization: translated by the min-` / `imization of power consumption and the number of active` / `nodes.`
- L534–537: `• Cost optimization: can be expressed in terms of the` / `Return On Investment (ROI), resource exploitation cost` / `or the VM allocation cost.`
- L538–540: `• QoS optimization: can be expressed in terms of response` / `time, overhead time, etc.`
- L541: `• Resource usage: RAM, CPU, storage, etc.`
- L543–545: `• Load balancing: the avoidance of congestion, data over-` / `load, etc.`

Sub-objectives as printed in Fig. 5 (L487–517): `STATIC PLACEMENT (OFFLINE)`, `DYNAMIC PLACEMENT (ONLINE)`, then leaves `Latency`, `Congestion`, `Overhead`, `Data transfer time`, `Delay`, `Aggregate Traffic`, `Power consumption`, `Number of activated nodes`, `Operating cost`, `ROI`, `User's budget`, `Power budget`, `CPU & RAM`, `Reliability`, `Load balancing` — headed by L494–495: `QoS` / `Energy` / `Cost` / `Resource usage` / `Reliability` / `Load balancing`.

Table captions: L397 `TABLE II: Global classification of VMP solutions.`; L411–412 `TABLE III: Objective-based classification of VMP ap-` / `proaches.`; L522 `Fig. 5: VMP classification.`

### 3.3 VNFP taxonomy

- L1214–1219: `As depicted in Fig. 6, the VNF placement` / `can be classified into two main categories:` / `• The general placement: the focus here is to define effi-` / `cient placement strategies and policies based on chains,` / `replications, forwarding graphs, etc.` / `• The placement of specific network functions, such as`
- L1220–1222: `Packet Data Network Gateways (P-GWs), Serving Gate-` / `ways (S-GWs), and transcoders.`
- L1223–1226: `This classification is not only motivated by the fact that there` / `is a difference between the several use cases addressed in the` / `first category (see Section III), but also because the several` / `solutions, presented in the second category, aim to enhance`
- Fig. 6 (L1410–1456) labels verbatim: `VIRTUAL NETWORK FUNCTIONS PLACEMENT`, `GENERAL NETWORK FUNCTIONS PLACEMENT`, `SPECIFIC NETWORK FUNCTIONS PLACEMENT`, then leaves `VNF forwarding graph`, `VNF chains placement`, `VNF replications`, `Other general placement`, `Transcoder and cache`, `S-GW and P-GW`, `vDPI and firewall`, `CDN`. Caption L1456: `Fig. 6: VNF placement classification.`
- The three categories enumerated in the introduction (L256–271): `These categories are:` / `• Network function chain placement which dynamically steers the traffic through an ordered list of Service Func-` / `tions (SFs), mainly located in a middle-box (e.g., Firewall and Deep Packet Inspection - DPI), and facilitates the dy-` / `namic enforcement of service-inferred traffic forwarding policies [169].` / `• VNF forwarding graph which defines a graph of inter-` / `connected VNFs which are linked in order to instantiate a Network Service.` / `• VNF replications which create replicas of a VNF or a set of VNFs (i.e., Service Function Chaining - SFC - with replications) in order to provide load balancing and recovery capabilities for the network.`

### 3.4 NFV use-case taxonomy (Section III)

- L354–357: `ETSI has selected a set of relevant ones, such as` / `the Virtualized Network Functions as a service (VNFaaS), the` / `Virtualization of mobile base stations, and the virtualization of` / `Content Delivery Networks (CDNs).`
- Subsections: L359 `1) Virtual Network Function as a Service:`, L370 `2) Network Function Virtualization as a Service:`, L384 `3) Service Function Chaining:`, L395 `4) Virtualization of Mobile Core services:`, L410 `5) Virtualization of Content Delivery Networks:`, L421 `6) Home and Business Gateways virtualization:`
- VMP Section II subsection headings: L306 `A. VM use cases`, L320 `1) VM Lifecycle Management:`, L288 `2) Virtual Machine Migration:`, L306/307 `3) Containers in Virtual Machines:`

---

## 4. Optimization methods / mathematical formulations reported from the reviewed literature

All of the following are **named in the file as methods used by the cited works** (not by the authors).

### 4.1 Exact mathematical-programming formulations

- **ILP (Integer Linear Programming)** — L171 (acronym list): `ILP         Integer Linear Programming`. In body: L1241 `on Integer Linear Programming (ILP), the proposed algorithm`; L1343 `In [117], an ILP-based model is proposed by Sun et al. to`; L1522 `processing is formulated as an ILP to minimize the total cost of`; L1579 `the problem, using ILP and a heuristic implemented in the Java`; L1648 `and their adequate locations are based on two ILP solutions.`; L1655–1657 `They proposed` / `mechanisms for allocating the needed VNFs for each CDN` / `slice based on two ILPs formulations and solved based on the`
- **MIP (Mixed Integer Programming)** — L181: `MIP         Mixed Integer Programming`. Body: L753 `comparison to the Mixed Integer Programming (MIP) solution`; L880 `optimal VM allocation is formulated as an MIP. The policies`; L983 `VMPDN is formulated as an MIP. The 3-approximation algo-`; L1366–1367 `after deriving, based` / `on MIP, the optimal number of virtual instances to meet the`; L1374 `to the NFV paradigm. Based on MIP, four heuristic algorithms,`
- **Mixed-integer linear optimization** — L567–568: `Based on this power model, a mixed integer` / `linear optimization problem is formulated.`
- **MINLP (Mixed Integer Nonlinear Programming)** — L1507–1508: `Mosleh et al. defined in [106]` / `the problem as a “Mixed Integer Nonlinear Programming (MINLP)”,`
- **DIP (Direct Integer Programming)** — L176 acronym `DIP         Direct Integer Programming`; L773–776: `The problem is presented as a multi-` / `unit combinatorial auction and formulated as Direct Integer` / `Programming (DIP). Compared to the column generation` / `method, near optimal solutions are obtained by DIP combining`
- **SIP (Stochastic Integer Programming)** — L212 acronym `SIP         Stochastic Integer Programming`; L790–791: `To` / `get resources from cloud providers, OVMP is based on the` / `solution provided by Stochastic Integer Programming (SIP).`; L754–755 `of the deterministic formulation of SIP.`
- **PBO / Pseudo-Boolean** — L194 acronym `PBO         Pseudo-Boolean Optimization`; L572–574: `Ribas et al. in [37] introduced an arti-` / `ficial intelligence approach based on a Pseudo-Boolean (PB)` / `formulation.`; L580–582 `an improved` / `Pseudo-Boolean Optimization (PBO) of the VM consolidation` / `problem, called “PBFVMC” is proposed in [47].`
- **CSP (Constraint Satisfaction Problem)** — L152 acronym `CSP         Constraint Satisfaction Problem`; L598–600 `A “redesigned energy-aware heuristic framework for VM` / `consolidation to achieve a better energy-performance tradeoff”` / `is proposed by Cao et al. in [62].` (framework "as a redesign of CloudSim") and L599–601: `Those two components are based on a Constraint Satisfaction` / `Problem (CSP), which considers the completion time.`; L760 `The problem is formulated as CSP.`; L914–915 table cell `Constraint Satisfaction Problem`; L698–701 table cell `Constraint` / `Satisfaction` / `Problem` / `with choco` / `solver`
- **CP (Constraint Programming)** — L1178–1179: `Bin et al. model the k-resiliency conditions as input` / `constraints to a Generic Constraint Programming (CP) solver`; L1604–1605 `the work in [118] proposes a` / `modeling, using constraint programming, for the placement`
- **QAP (Quadratic Assignment Problem)** — L201 acronym `QAP         Quadratic Assignment Problem`; L878–880: `TVMP belongs to the class of Quadratic` / `Assignment Problem (QAP), which is considered among the` / `hardest NP-complete problems.`
- **VBP (Vector Bin Packing)** — L218 acronym `VBP         Vector Bin Packing`; L588–590: `The problem is seen as a Vector Bin Packing problem` / `(VBP), the objective of which is to minimize the number of` / `PMs.`
- **MGAP (Multi-level Generalized Assignment Problem)** — L179 acronym `MGAP        Multi-level Generalized Assignment Problem`; L764–766: `VMcP is` / `formulated as a “Multi-level Generalized Assignment Problem` / `(MGAP)”.`
- **UFLP (Uncapacitated Facility Location Problem)** — L1563–1564: `This problem was formulated as an Uncapacitated Facility` / `Location Problem (UFLP) [143].`
- **Bipartite maximum-weight matching** — L1179: `a “maximum weight matching in bipartite graphs problem”.`
- **Multi-unit combinatorial auction** — L773–774: `The problem is presented as a multi-` / `unit combinatorial auction`
- **Multi-stage graph optimization** — L1389–1390: `Khebbache et al. proposed an optimization` / `method based on a multi-stage graph to improve scalability`
- **Eigendecomposition (analytic)** — L1373–1376: `Mechtri et al. propose in [116]` / `an analytically-based approach as a solution to the problem.` / `The proposed approach is an Eigendecomposition extension.` / `Eigendecomposition is the factorization of a diagonalizable`
- **Convex optimization** — L719–720: `a new large-scale scheme based on the powerful convex` / `optimization theory is proposed to reduce the number of PM`
- **Linear programming** — L586–587: `present two approaches based on linear programming and` / `quadratic programming to derive near-optimal solutions for the`; L1473–1474 `proposing a linear programming formulation for the compu-` / `tation of VNF placement aiming to balance optimality and`; L1476–1478 `Using a realistic evaluation environment and` / `CPLEX for the linear programming models, the performance` / `results show that the linear programming model achieves better`; L1589–1591 (right column) `be used in networks of a scale exceeding 35 nodes for the` / `linear programming solution and 300 nodes for the heuristic` / `solution`
- **Quadratic programming** — L587 `quadratic programming to derive near-optimal solutions for the`; L906–907 `- A solution based` / `on quadratic programming.`
- **Approximation algorithms (2-approx / 3-approx)** — L975–977: `based on 2-approximation algorithms to minimize the VMs` / `maximum access latency [35], [40], [52], Kuo et al. propose` / `in [67] a new 3-approximation algorithm.`; L987–989 `is compared to the optimal 2-approximation of VMPDN con-` / `sidering a high time complexity. Although it exhibits a worse` / `approximation factor, the 3-approximation algorithm achieves`

### 4.2 Heuristics / metaheuristics

- **Genetic Algorithm (GA)** — L166 acronym `GA          Genetic Algorithm`; L532–533 `As an improvement to a previous Genetic Algo-` / `rithm (GA) solution in [38], a Hybrid GA (HGA) is introduced`; L737 `is a hybridization of GA, Ant Colony Optimization (ACO),`; L1355 `algorithms such as Bin Packing, Simulated Annealing, Ant`; L1390 `the VNFs mapping. Two genetic algorithms are tested within`; L1471 `while for large networks, GA and the Random Fit Placement`; L1527 `while achieving a similar result to that of the GA.`; L1554 `a GA-based method to`; L1194 `scheduling of virtual resources in the cloud using three GAs`; L1632–1633 `It` … `is based on a` (see also L1636 `heuristic algorithm which finds the optimal set of placement`)
- **HGA (Hybrid Genetic Algorithm)** — L167 acronym `HGA         Hybrid Genetic Algorithm`; L533 `a Hybrid GA (HGA) is introduced`
- **NSGA / NSGA-II / MOGA** — L185 acronym `NSGA        Non-dominated Sorting Genetic Algorithm`; L1197–1198 `Two GAs, namely the baseline GA and “Non-` / `dominated Sorting Genetic Algorithm (NSGA)”, defined du-`; L1200–1202 `a new version of NSGA; NSGA-` / `II, is produced, handling the VMP problem as a minimization` / `problem.`; L1390–1394 `Two genetic algorithms are tested within` / `this framework, the “Multiple Objective Genetic Algorithm` / `(MOGA)” and an improved NSGA-II. The experimentation` / `demonstrates that the improved NSGA-II and the VNF-FG`; L1296 `GA, NSGA`
- **MGGA (Multi-objective Grouping Genetic Algorithm)** — L180 acronym `MGGA        Multi-objective Grouping Genetic Algorithm`; L1082–1083 `outperforms the “Multi-objective Grouping` / `Genetic Algorithm (MGGA)” and the offline VMP solution`
- **ACO (Ant Colony Optimization)** — L146 acronym `ACO         Ant Colony Optimization`; L1041–1043 table cells `Ant` / `Colony` / `Optimization`; L1204–1205 `shows the efficiency of the multi-objective ant colony` / `system algorithm proposed by Gao et al. in [51].`; L1263 `by using ACO or GA`; **VMPACS** L142 acronym `VMPACS        Virtual Machine Placement Ant Colony System`; L1085 `“Virtual Machine Placement Ant Colony System (VMPACS)”`
- **PSO (Particle Swarm Optimization)** — L200 acronym `PSO         Particle Swarm Optimization`; L737–739 `EOVMP` / `is a hybridization of GA, Ant Colony Optimization (ACO),` / `and Particle Swarm Optimization (PSO).`
- **SA (Simulated Annealing)** — L206 acronym `SA          Simulated Annealing`; L639 table cell `annealing` (under `- Simulated`); L888 `and the Simulated Annealing (SA) algorithms.`; L1267 table cell `Annealing`; L1355 `algorithms such as Bin Packing, Simulated Annealing, Ant`
- **BBO (Biogeography-based optimization)** — L1054–1055 table cells `Biogeography-` / `based` / `optimization`; L1069–1071: `A novel solution, introduced by Zhenga et al. in [95] and` / `called “VMPMBBO”, considers a VMcP system based on` / `a resource wastage model and a power consumption model.` … `This solution uses “biogeography-based optimization (BBO)”,`
- **VNS (Variable Neighborhood Search) meta-heuristic** — L1359–1361: `In [125], Luizelli et al. incorporate a Variable Neighborhood` / `Search (VNS) meta-heuristic, for efficiently exploring the` / `placement and chaining solution space.`
- **Fix-and-optimize** — L1964–1966 (reference title) `“A fix-and-optimize approach for efficient and large scale virtual network` / `function placement and chaining,”`
- **Bin Packing** — L635–636 table cells `- Bin-packing`; L1355 `algorithms such as Bin Packing, Simulated Annealing, Ant`; `Packing Vectors` L591 `the solution named “Packing Vectors”`; `VectorDot` L714–715 `the VectorDot used in [14]`
- **First Fit Algorithm (FFA) / First-Fit Decreasing (FFD) / PABFD / MCC / RFPA** — L163 acronym `FFA         First Fit Algorithm`; L575 `consolidation results compared to the First Fit Algorithm`; L610–612: `This policy, inspired` / `by the “Power Aware Best Fit Decreasing (PABFD)” and` / `called the “Minimum Correlation Coefficient (MCC)”, is used`; L1356–1357 `Simple Greedy Approach (SBA) using the First-Fit` / `Decreasing method (FFD)`; L1471–1472 `while for large networks, GA and the Random Fit Placement` / `Algorithm (RFPA) are used to decrease the computation time`
- **Greedy / heuristic algorithms** — L713 `in comparison with the greedy FFA proposed in [34], [39], the`; L867 `namely a greedy algorithm and a heuristic-based algorithm,`; L881 `a heuristic algorithm to solve TVMP. The algorithm follows a` / `two-tier divide and conquer approach`; L1146–1147 table cells `Recursive` / `heuristic-based` / `algorithm`; L1175–1176 `an optimal redundant VMP is carried out using a recursive` / `heuristic-based algorithm.`; L1559–1562 `Therefore, the authors propose three heuristic algorithms` / `to solve it: “Optimal Network Function Placement for Load` / `Balancing Traffic Handling (ONPL)”, a “Greedy Algorithm”` / `and a “Repeated Greedy Algorithm (RGA)”.`; L1374 `Based on MIP, four heuristic algorithms,` (named L1375–1376: `namely baseline, consolidation, load balancing, and worst` / `performance are proposed`)
- **Clustering ± bin packing** — L1011–1012 table cells `Clustering` / `plus` / `bin` / `packing`; L1010–1011 `moving the traffic` / `from the core` / `edges switches`
- **Multi-dimensional space partition** — L1031–1032 table cells `Multi-` / `dimensional` / `space` / `partition`; L972–975: `EAGLE design is guided by a multi-` / `dimensional space partition.`
- **Fuzzy algorithm combined with GA** — L1094–1095: `This controller is based on an improved GA combined` / `with a fuzzy algorithm.`

### 4.3 Game theory / matching / Markov

- **Coalition-formation game** — L1363–1365: `Their solution includes an efficient coalition-formation game-` / `based VNFP algorithm which finds an optimal tradeoff of` / `QoS while reducing the deployment cost`
- **Bargaining game theory** — L1656–1658: `They proposed` / `mechanisms for allocating the needed VNFs for each CDN` / `slice based on two ILPs formulations and solved based on the` / `bargaining game theory with the objectives of minimizing the` (continues L1658–1659 `cost and maximizing the QoE.`)
- **Nash bargaining** — L1601–1603: `finds a fair placement with a tradeoff between the given` / `objectives, i.e., S-GW relocation and the delay overheads,` / `based on the Nash bargaining.`
- **Game-theoretic models** — L1493: `developed game-theoretic models to evaluate joint caching and`
- **Matching Theory** — L1489: `cope with this issue, the Matching Theory is combined with`
- **Sampling-Based Markov Approximation (MA)** — L1485–1487: `a “Sampling-Based` / `Markov Approximation approach (MA)” is proposed to the` / `VNF placement problem.`
- **Markov Chain (MC)** — L177 acronym `MC          Markov Chain`; L750–751 `history variations and a Markov Chain (MC) for prediction.`

### 4.4 Statistical prediction / regression used as placement inputs

- L544–546: `A self-` / `adaptive placement strategy, based on Robust Local Weight` / `Regression, is proposed by Zhang et. al. in [65].` (acronym L204 `RLWR        Robust Local Weight Regression`)
- L745–750: `The prediction of the demand forecaster is based on a Simple` / `Kalman Filter (SKF) as the estimation technique, a Double` / `Exponential Smoothing (DES) method to reduce the usage` (acronyms L153 `DES  Double Exponential Smoothing`, L211 `SKF  Simple Kalman Filter`)
- L1345–1346: `the cost saving is also considered in the oriented optimal` / `placement scheme proposed by Yousaf et al. in [85]` with L1346–1347 `The VNF placement is treated by analyzing the cost incurred` and L1355–1356 `The cost of VNF placement can be reduced using` / `algorithms such as ... Transient cooling effects, N-dimensional set`
- L1568–1572: `proposed a fine-grained scheme based on the computing Ref-` / `erence Resource Affinity Score (RRAS) values of each hosted` / `VM for the optimal management and decision of VNFs.`

### 4.5 Named deployment strategies (constraint-based, non-optimization)

- L1348–1350: `by two constraint-based deployments, namely “Vertical Se-` / `rial Deployment (VSD)” and “Horizontal Serial Deployment` / `(HSD)”.`
- L1331–1333: `“Structural Aware Planner (SAP)”` … `“Demand Aware Planner (DAP)”` (L1341)
- L1330 acronym-style name: `“VNF place-` / `ment and Routing Optimization(VNF-PR)”` (L1329–1330)
- L1599–1600: `“Fair and` / `Optimal SGW Relocation and data delivery Delay (FORD)”` (L1600), `“Avoiding S-GW Relocation (A-` / `SGWR)”` (L1594–1595), `“Shortening Path Length between` / `eNBs and PDN-GW VNFs (S-PL)”` (L1597–1598)
- L1191: `selection of fault-tolerant strategy dubbed “SelfAdaptionFTPlace”.`

**Complexity statements** (verbatim): L1212–1213 `Since the optimal` / `placement of VNFs is known to be NP-hard [2], several`; L1402–1404 `The VNF Chain Placement Problem (VNF-CPP) is another` / `VNF placement-related problem, which is known to be NP-` / `Hard.`; L1528–1530 `In [59], the S-GW placement problem is presented` / `as an NP-hard problem.`; L1557–1559 `This process is modeled by a nonlinear` / `optimization problem, which is proved to be an NP-hard prob-` / `lem.`

---

## 5. Survey-level quantitative figures / statistics

**NOT REPORTED.** The file contains **no** survey-level statistics: no "X% of works use Y", no counts of papers per category, no bibliometric or table statistics. Table II and Table III are *reference-tag listings* (e.g. L399–408 `[12] [16] [22] [26]` / `[20] [21] [23] [27]`), not numerical aggregates, and the file never states a total number of surveyed works.

The only survey-level statements about distribution are **qualitative, unquantified**:

- L1161–1163: `Having said that, it is worth noting that most` / `of the work mentioned in the literature is dedicated to offline` / `VMP, except in [100].`
- L1647–1648: `Several lab-based simulations lack realistic data and the` / `means to mimic the important workload, dependencies, and`
- L1703–1709 (right column, interleaved with references on L1704/L1708): `Also, only a` / `few VNFP solutions, such as in [123], [158], [166], are applied` / `in multiple federated clouds, while most of the surveyed` / `works treat the problem of VNFP within only a single cloud` / `environment (e.g., in [42], [85], [86], [90].`
- L1671–1672: `that there are still many unresolved issues, mainly with regard` / `to the size of cloud setups and multi-tenancy considerations.`

For completeness (these are **numbers reported from cited works, not survey statistics**):

- L588–589: `high number of variables (i.e., (2 × N + 2 × N × K) variables` / `for (2 + 2 × N + K) constraints, whereby K and N represent` (from [47])
- L594: `the number of variables by 50% and execute huge sets of` (from [47])
- L1241–1243: `Based` / `on Integer Linear Programming (ILP), the proposed algorithm` / `finishes in few seconds (i.e., 16 seconds) which makes it quick` (from [75])
- L929–930 table cells `1024 VMs and` / `several`
- L1575: `more than 58% when relaxing the capacity used per link.` (from [145])
- L1535–1536: `The throughput can be improved by more than six times,` / `using only one-seventh the number of processor cores, when`
- L1589–1591: `be used in networks of a scale exceeding 35 nodes for the` / `linear programming solution and 300 nodes for the heuristic` / `solution`
- L915 table cell `- Only 3 hosts, and`
- L1256 table cell `only for four servers`
- L1627: `Although the experimentation concerned the case of 100`
- L646–648: `- Tested only on a` / `small-scale environment.`

---

## 6. Standardization / architecture context

**Standards bodies and control planes actually named in the file**

- **ETSI** (multiple):
  - L162 acronym: `ETSI        European Telecommunications Standards Institute`
  - L368–370: `The European Telecommunications Standards Institute` / `(ETSI) established the concept of Network Function Virtual-` / `ization (NFV) and defined the basic architecture and require-` / `ments of VNFs [4].`
  - L370–373: `The NFV framework consists of three` / `main components: VNFs, NFVI, and the NFV Management` / `and Orchestration (NFV MANO).`
  - L354–357: `ETSI has selected a set of relevant ones, such as` / `the Virtualized Network Functions as a service (VNFaaS), the` / `Virtualization of mobile base stations, and the virtualization of` / `Content Delivery Networks (CDNs).`
  - L1372–1373: `the general guidelines of major standardization communities` / `(e.g. ETSI) that leverage the capabilities of SDN and cloud` (the word `following` that introduces this clause sits at the end of L1371)
  - ETSI specifications cited in the reference list: L1753 `[3] ETSI GS NFV 001 : “Network Functions Virtualisation: Use Cases”`; L1755–1756 `[4] ETSI GS NFV-SWA 001 : “Network Functions Virtualisation (NFV);` / `Virtual Network Functions Architecture”`; L1758–1759 `[5] ETSI GS NFV 002 : “Network Functions Virtualisation (NFV); Archi-` / `tectural Framework”`; L1761–1762 `[6] ETSI GS NFV-IFA 002 : “Network Functions Virtualisation; Accelera-` / `tion technologies; VNF Interfaces Specification”`; L1964–1966 `[147] ETSI GS NFV-SEC 002 V1.1.1 : “Network Functions Virtualisation` / `(NFV); NFV Security; Cataloguing security features in management` / `software”`; L1968–1970 `[148] ETSI GS NFV-REL 002 V1.1.1`; L1972–1974 `[149] ETSI GS NFV-SEC 004 V1.1.1`; L2019–2021 `[160] DGS/NFV-066: “Network Functions Virtualisation (NFV); NFV Test;` / `Report on CI/CD and Devops”`
- **DMTF (Distributed Management Task Force)** — only as a suggestion inside Table IV, split across lines: L630/632/634 `- Could consider using` / `Distributed Management` / `Task Force standards.`
- **3GPP** — L1587–1588: `constraints of 3GPP specifications. The architecture consists`
- **SDN / OpenFlow as control planes** — L207 acronym `SDN         Software Defined Networking`; L137 `Networking (SDN) and virtualization. The virtualization offers`; L136–137 statement of the FMC concept; L966 `SLA requirements is defined. Finally, an OpenFlow controller`; L1523–1524 `placement in the network. OpenFlow is used to optimize the` / `transcoder migration during streaming, and a heuristic is pro-`; L1748 `[1] “Network Functions Virtualisation;An Introduction, Benefits, Enablers,` / `Challenges & Call for Action,” at the SDN and OpenFlow World`
- **SDN controller (managed-resource overhead in reviewed work [76])** — L1539–1543 (right column): `placement by taking into consideration the load overhead in` / `the transport network, the overhead in the SDN controller and` / `other parameters, such as the potential number of DCs and the` / `delay in the data-plane.`
- **NFV MANO / VIM / VNFM (functional architecture)** — L371–373 `VNFs, NFVI, and the NFV Management and Orchestration (NFV MANO)`; L245–249: `the mapping between` / `VNFs and VMs in case of an OpenStack Infrastructure as` / `a Service (IaaS), and that is through the VNF Manager` / `(VNFM) which instantiates, scales up/down, updates, and` / `terminates VNFs; the Virtual Infrastructure Manager (VIM),` / `which is responsible for controlling and managing the NFVI` / `compute, storage, and network resources`; acronyms L188–189 `NFV MANO  Network Function Virtualization Management and Or- chestration`, L220 `VIM  Virtual Infrastructure Manager`, L187 `NFVI  Network Function Virtualization Infrastructure`
- **Cloud platform / orchestrator context** — L278 `Fig. 3: Example of mapping of VNFs and VMs on an OpenStack IaaS.`; L108–110 `This architecture is based on an` / `orchestrator which carries out automatically the placement of` / `nodes depending on a system that collects information about` / `the resource consumption.`

**Explicitly ABSENT — NOT REPORTED in this file:** ETSI ZSM, ONAP, OSM / Open Source MANO (searched `ZSM`, `ONAP`, `OSM`, `Open Source MANO` — zero matches), Kubernetes (zero matches), Mininet (zero matches), GLPK (zero matches).

---

## 7. Managed resources, network domains, and interfaces/APIs mentioned

**Virtual resources:**
- L67–69 (abstract): `the efficient allocation` / `of virtual resources (e.g. VCPU, VMDISK) and the optimal` / `placement of Virtualized Network Functions (VNFs) composing` / `the network slices.`
- L541: `• Resource usage: RAM, CPU, storage, etc.`
- L583–584: `the amount of RAM, processing power, and running hardware` / `type`
- L585–587: `The considered constraints (e.g., the necessary` / `amount of ON resources to power all VMs, the hardware on which a` / `VM is running and must be ON, etc.)`
- L718–720: `as a multi-dimensional VMP` / `that considers multiple types of resources, namely memory,` / `CPU, storage, and bandwidth.`
- L1314–1316: `the VNF requirements (i.e., processing, storage, and band-` / `width) excluding latency on the end-to-end network and that` / `on VNF nodes.`
- L1319–1320: `Riggio et al. aim at satisfying the VNF requirements` / `(i.e., memory, CPU, radio, storage and bandwidth), while`
- L1243–1245: `thus,` / `minimizing the utilization of PMs and link resources. Two` / `load`

**VNF internal structure (VDUs, connection points, virtual links):**
- L249–254: `also a VNF includes` / `Virtual Deployment Unit(s) (VDUs) which is the VM hosting` / `the network function, the connection point(s) connecting the` / `internal virtual links or outside virtual links, and the virtual` / `link(s) which provide connectivity between VDUs.`
- Acronyms: L150 `VNF-FG      VNF Forwarding Graph`, L149 `VNFC        Virtualized Network Function Component`, L148 `VNFaaS      Virtual Network Function as a Service`

**Network domains:**
- L1589–1593: `The architecture consists` / `of the cloud domain composed by distributed DCs over a` / `geographical area and the RAN domain consisting of access` / `points.`
- L1312–1314: `the placement of different VNFs, such as S-GW, P-GW, Home` / `Subscriber System (HSS) and Mobility Management Entity` / `(MME), excluding VNFs of the RAN.`
- L1317–1318: `The RAN domain, including the firewall, load` / `balancing, and virtual nodes are addressed in [92].`
- L1468–1470: `Dietrich et al. considered the deployment of the` / `main components of EPC as VNFs in DCs close to base` / `stations (i.e., edge cloud), ensuring elasticity in resource pro-`
- L1325–1326 acronym: `Represented as a Multiple Objective Decision Making (MODM)`
- L1499+ Section XII-A `Transcoder and cache placement`; L1598 `D. Replication of Content Distribution Networks`; L1499 (L1499: `A. Transcoder and cache placement`) and L1655 `virtual CDNs slices in multiple cloud domains.`

**Interfaces / APIs:** the file names a VNF interface specification document but does not describe individual APIs:
- L1761–1762: `[6] ETSI GS NFV-IFA 002 : “Network Functions Virtualisation; Accelera-` / `tion technologies; VNF Interfaces Specification”, ETSI Ind. Specifica-` / `tion Group (ISG), Valbonne, France, Mar. 2016.`
- L1559–1560 interfaces are referenced indirectly as `VNF Interfaces Specification` only (above). Named protocols/interfaces beyond this: **NOT REPORTED** (no REST/SOL/TOSCA/OpenFlow-API detail; `OpenFlow` appears only as L966 `an OpenFlow controller` and L1524 `OpenFlow is used to optimize the`).

**Service-chain / graph concepts:** L209 acronym `SFC  Service Function Chaining`; L263–266 `• VNF forwarding graph which defines a graph of inter-` / `connected VNFs which are linked in order to instantiate a Network Service.`; L391–392 `will require the usage of VNF forwarding graphs (VNF-FGs).`

---

## 8. ML / DRL / AI usage discussed

**Machine learning, deep learning and reinforcement learning are NOT REPORTED at all.** Greps for `machine learning`, `deep learning`, `reinforcement`, and `learning` (as a technical term) return no relevant hits — the only `learning` match in the file is the unrelated word at L1679 `infrastructure, most providers are still learning about the`.

What the file *does* say under an AI/intelligence heading:

- L572–574: `To solve this issue, Ribas et al. in [37] introduced an arti-` / `ficial intelligence approach based on a Pseudo-Boolean (PB)` / `formulation.`
- L1094–1095: `This controller is based on an improved GA combined` / `with a fuzzy algorithm.`
- L1660–1665 (authors' own recommendation, right column): `We believe that the focus should be on these critical` / `operational requirements. The best practices and the agile` / `tools in hand, such as artificial intelligence, service modeling,` / `and prediction must be used to improve the allocation of` / `resources (i.e., VNFs and VMs) in a standardized approach.`
- L544–546: `A self-` / `adaptive placement strategy, based on Robust Local Weight` / `Regression, is proposed by Zhang et. al. in [65].`
- L745–751 (statistical/predictive techniques, not ML): `The prediction of the demand forecaster is based on a Simple` / `Kalman Filter (SKF) as the estimation technique, a Double` / `Exponential Smoothing (DES) method to reduce the usage` / `history variations and a Markov Chain (MC) for prediction.`
- Reference titles containing "intelligent": L1804–1807 `[60] A. K. Das, T. Adhikary, M. A. Razzaque and C. S. Hong, “An` / `intelligent approach for virtual machine and QoS provisioning in cloud` / `computing,”`; L1953–1954 `[144] M. J. Kim, H. G. Yoon, and H. K. Lee, “IMAV: An Intelligent Multi-` / `Agent Model Based on Cloud Computing for Resource Virtualization,”`

Algorithms named as "learning-like" but explicitly classical metaheuristics are listed in Section 4 above (GA, HGA, NSGA/NSGA-II, MOGA, MGGA, ACO, PSO, SA, BBO, VNS, matching theory, Markov approximation).

---

## 9. SLA awareness, network slicing, Kubernetes / cloud-native

### SLA awareness — COVERED, extensively

- L213 acronym: `SLA         Service Level Agreement`
- L529: `that are compliant with the Service Level Agreement (SLA).` (referring to policies for energy-efficient VMP)
- L450–452: `important to provide solutions that effectively plan the provisioning` / `of VMs with respect to the needed SLA requirements.`
- L600–601: `classifies the overload in the host status into` / `two types: either with or without SLA violation.`
- L606: `the consumed energy, execution time, and SLA violations.`
- L608: `and SLA violation, Fu et al. introduced a new model for`
- L614–615: `It` / `reduces the SLA violation rate and consequently the power`
- L711–712: `approach saves cost, respects the SLA run-time constraint, and`
- L741–742: `considering application-level SLA requirements and resource`
- L763–764: `under the SLA and the power budget constraints, VMcP is`
- L770–772: `To cope with the need of cloud providers to gain profit from` / `SLA-compliant placement of VMs, an “SLA-aware placement` / `of multi VM elastic services in compute clouds” is proposed`
- L881–883: `Though the obtained SLA satisfaction factor` / `and allocations costs are good, the optimality of the policies` — full sentence L877–878 `The QoS requirements stated in the SLAs and resource` / `exploitation costs are subject to the reactive and proactive`
- L965–966: `whereby the maximum number of active servers violating the` / `SLA requirements is defined.`
- L1327–1328: `to the SLA constraints.`
- L1352–1353: `(EPCAAS) which respects the functional and administrative` / `constraints.`
- L1668–1669: `the nature of the heterogeneous infrastructure and` / `the SLA requirements to fulfill.`
- L1716–1717: `performance degradation, SLA violations, and QoS. This paper`

### Network slicing — COVERED, is the paper's stated framing

- L62–64 (abstract): `Cloud computing and network slicing are essential` / `concepts of forthcoming 5G mobile systems. Network slices are es-` / `sentially chunks of virtual computing and connectivity resources,`
- L98–108: `Network slicing, believed` / `to be the key ingredient of 5G and beyond networks, consists` / `of allowing a multitude of logical networks to be created` / `on top of a common physical infrastructure, and to share its` / `resources, by turning traditional structures into customizable` / `elements that can run on the architecture of choice [174].`
- L116–122: `A logical network slice, in our case, is considered` / `mainly as a logical combination of network functions and` / `virtual resources, regardless of the resource isolation among` / `the tenants.`
- L1729–1731: `surveyed with the main motivation to propose, as future work,` / `efficient strategies to carry out efficient network slicing, in` / `order to satisfy the end-users and verticals, and respect the` / `several constraints in place.`
- L1645–1646: `bility for the CDN slice owner to add videos and specify their` / `resolutions.`

### Kubernetes — **NOT REPORTED** (zero matches for `Kubernetes`)

### Cloud-native — mentioned only twice, briefly

- L1644–1646: `Also, more software` / `should be written in a “cloud native” manner with a deep` / `embedding of the cloud infrastructure.`
- L1914 (reference title only): `QoE-aware Elasticity Support in` (L1914: `Cloud-Native 5G Systems,” in IEEE ICC16, Kuala Lumpur, Malaysia,`)

Related container/DevOps coverage (but not Kubernetes): L71–73 `or containers (i.e. running with DevOps-style for additional` / `flexibility and efficiency of service applications [160]).`; L294–302 `Unlike the hardware-` / `level virtualization provided by VMs, containers share the` / `kernel of a given host’s system with other containers, which` / `constitutes an OS-level virtualization.` … `on top of, for instance, one common Docker engine, running` … `The open-source Docker uses the kernel`; L358–361 `In this paper, the focus is on VM placement as there` / `are not many solutions for container placement in the` / `literature. However, many VM placement approaches can` / `be adapted to also optimally place containers.`

---

## 10. Evaluation environments / testbeds / simulators

### (a) Tools, simulators and testbeds used by the REVIEWED WORKS

- **CloudSim (and versions)** — L599–600: `The framework, as a redesign` / `of CloudSim, classifies the overload in the host status into`; L615–616: `Using cloudSim-3.0, the policy is demonstrated`; L669–671 table cells `within` / `CloudSim and` / `its enhanced`; L871–872: `A policy is implemented and tested using Cloudsim` / `2.0.`
- **OpenStack** — L245–246: `VNFs and VMs in case of an OpenStack Infrastructure as` / `a Service (IaaS)`; L278: `Fig. 3: Example of mapping of VNFs and VMs on an OpenStack IaaS.`; L671–672 table cell `such as OpenStack.`; L1327–1328: `function in an OpenStack-based cloud environment. It is meant`; L1920–1921 reference: `[90] S. Oechsner and A. Ripke, “Flexible support of VNF placement func-` / `tions in OpenStack,”`
- **CPLEX** — L1476–1477: `Using a realistic evaluation environment and` / `CPLEX for the linear programming models, the performance`
- **Gurobi** — L1651–1652: `the experimentation results using the Gurobi Optimization` / `tool prove the efficiency of the proposed solutions.`
- **Choco CSP solver** — L760–761: `The` / `proposed CSP solver is based on Choco to implement the two`; table cell L701 `with choco`; L819 table cell `Choco`
- **GEANT backbone dataset** — L1585–1587: `The solution was tested against realistic` / `conditions using a large-scale dataset on the high bandwidth` / `backbone GEANT.`
- **Google Cluster data trace / DInf-UFPR DC** — L576–579: `the experiments using the data center of the “Informatic` / `Department of Federal University of Parana (DInf-UFPR)” and` / `Google Cluster show their limitations when applied to large` / `realistic data.`; L590–592: `The` / `conducted experiments used a data trace from the Google` / `Cluster project.`
- **Oprofile / Xenoprofile on Xen VMs** — L1213–1217: `the work of Emeneker et al. in [24]. The authors used Oprofile` / `and Xenoprofile for gathering cache miss data to test the` / `performance of multi-core cache structure on applications` / `running inside Xen VMs.`
- **Java Universal Network/Graph Framework** — L1578–1581: `The research work presented in [86]` … `the problem, using ILP and a heuristic implemented in the Java` / `Universal Network/Graph Framework, was proposed by M.`
- **Verizon production deployment (Red Hat, Big Switch)** — L1651–1655: `Verizon, in collaboration with Red` / `Hat and Big Switch, is one interesting success story worth` / `mentioning which successfully was able to deploy large-` / `scale network functions [7]. However, the director of NFV` / `planning at Verizon mentioned that they had to face many`
- **Simulation topologies reported from reviewed works** — L729–731: `four network` / `experimentation topologies, namely Tree, VL2, Fat-Tree, and` / `BCube, the proposed scheme saves considerably the traffic`; L985–987: `Using the Tree,` / `VL2, Fat-Tree, and BCube network architectures, this solution` / `is compared to the optimal 2-approximation of VMPDN con-`; L1186–1188: `Using a three-layer binary` / `tree structure topology, the simulations show the performance` / `of the scheme against the solution produced by a brute-force`
- **Hypervisors / migration tech** — L390: `many technologies such as VMware ESX [11] and Xen [8].`
- **Lab-simulation critique (authors' own observation)** — L1647–1649: `Several lab-based simulations lack realistic data and the` / `means to mimic the important workload, dependencies, and` / `conditions which could permit to propose efficient policies`
- **Explicit calls for simulation tooling** — L1666–1668: `The pillar is to enable efficient simulation tools (if not real` / `tests such as Verizon’s) that could reflect the UE consumption` / `of services, the nature of the heterogeneous infrastructure and`

### (b) Experiments by the survey authors themselves

**NOT REPORTED — none.** No simulator, testbed, dataset or numeric result is claimed by Laghrissi & Taleb anywhere in the file. Their only first-person artefacts are Fig. 2/3 (illustrative mapping figures), Fig. 5/6 (classification figures), and Tables I–IX (acronyms, classifications, and qualitative "Analysis summary" tables). The Table IV–IX content is explicitly labelled as the authors' qualitative assessment: L548–553 `in a dedicated table (Tables IV` / `to IX). Each table contains the advantages and disadvantages` / `that we have assessed for the adopted solutions and frame-` / `works, as well as enhancement propositions that could guide` / `the reader to spot possible research directions.` Table titles: L621 `TABLE IV: Analysis summary of the relevant/recent work on energy-aware VMP solutions.`; L799 `TABLE V: Analysis summary of the relevant/recent work on cost-aware VMP solutions.`; L893 `TABLE VI: Analysis summary of the relevant/recent work on QoS-aware VMP solutions.`; L995 `TABLE VII: Analysis summary of the relevant/recent work on resource usage-aware VMP solutions.`; L1102 `TABLE VIII: Analysis summary of the relevant/recent work on reliability-aware VMP solutions.`; L1249 `TABLE IX: Analysis summary of the relevant/recent work on load balance-aware VMP solutions.`

---

## 11. Open research challenges / limitations identified by the survey itself

Verbatim, from Section XIII (`XIII. K EY CHALLENGES AND LESSONS LEARNED`, L1664) and the surrounding pages (left column = main text, right column = continuation, both on the same numbered lines):

1. L1666–1668: `Admittedly, NFV is still in its early stages. To ensure the` / `ultra-short latency, high QoS, service reliability and security` / `promised in 5G, many key challenges still need to be thor-`
2. L1668–1670: `oughly addressed. For the work assessed in this survey on` / `VMP, as it could be seen in Tables IV to IX, it is clear` / `that there are still many unresolved issues, mainly with regard`
3. L1671–1672: `to the size of cloud setups and multi-tenancy considerations.`
4. L1672–1675: `Also, there is still room for work, particularly, concerning` / `service reliability and k-resiliency, and the optimization of` / `overhead and data transfer time in case of online VMP.`
5. L1676–1685: `Concerning the VNFP, based on the different solutions` / `discussed in this article, and other solutions offered in the` / `virtualization era as alternatives to the traditional existing` / `infrastructure, most providers are still learning about the` / `challenges that arise from common infrastructures, typically` / `in terms of complexity. The management of service quality,` / `dependencies, performance, and scalability becomes extremely` / `difficult within the highly dynamic NFV ecosystem. The` / `research work dedicated to the placement of network functions` / `is encouraging but still many issues still remain unresolved.`
6. L1627–1634 (right column): `Fair tradeoffs between deployment related parameters, link` / `utilization, cost for both service providers, and end users are` / `lacking. For instance, in [21], [23], [28], [61], [92], many` / `deployment parameters such as latency and mobility are not` / `considered, while solutions which consider such parameters as` / `in [93], [113], [117], [125], [128], [129] seem to have limited` / `applicability and are more efficient in cases of small numbers` / `of user nodes, due to their complexity costs.`
7. L1635–1646: `The repackaging of network functions as virtual appliances` / `must fulfill the promise of NFV to offer agility and cost reduc-` / `tion (i.e., reduced CAPEX and OPEX). Different stakeholders` / `must look toward leveraging automation of processes and` / `orchestration to serve these objectives. It is of vital importance` / `to validate physical and virtualized network functions and` / `infrastructures to do benchmarks and ensure that the capacity` / `and performance requirements are met. This process should` / `take into account a complete testing of NFV infrastructure` / `(NFVi) and physical network functions. Also, more software` / `should be written in a “cloud native” manner with a deep` / `embedding of the cloud infrastructure.`
8. L1647–1651: `Several lab-based simulations lack realistic data and the` / `means to mimic the important workload, dependencies, and` / `conditions which could permit to propose efficient policies` / `and solutions for virtual resources’ provisioning, placement,` / `recovery and maintenance.`
9. L1654–1659 (Verizon lesson): `However, the director of NFV` / `planning at Verizon mentioned that they had to face many` / `challenges with “one size does not fit all for all NFV workload` / `connectivity” being the main issue, along with the need for` / `high availability, SSL support, IPv6 support, scale testing, and` / `building in the needed capabilities [7].`
10. L1660–1665: `We believe that the focus should be on these critical` / `operational requirements. The best practices and the agile` / `tools in hand, such as artificial intelligence, service modeling,` / `and prediction must be used to improve the allocation of` / `resources (i.e., VNFs and VMs) in a standardized approach.`
11. L1680–1693 (right column, spanning the page break; interleaved with left-column text on L1680–1685) — service-management context loss: `Another point which is rarely discussed is the contextual-` / `ization of service management. Logically, since virtualization` / `enables cloud providers to manipulate directly the virtual` / `equipment (i.e. quasi-inexistence of intermediary steps be-` / `tween the resources and targeted applications), the virtual` / `equipment becomes somehow service agnostic, meaning that it` … `knows almost nothing about its contribution to the applications` / `as a whole, which results in losing the management context` / `capability [144].`
12. L1694–1703 (mobility / proximity gap): `Finally, although we can find that recently some researchers` / `are working on the study of users’ mobility and their service` / `usage behavior, along with the corresponding placement of` / `virtual appliances (i.e. VMs) required for VNFs [161], [165],` / `[170], more research work must be carried out in order to` / `allow a positioning of network functions in closer proximity` / `to service generation, and consequently provide better QoE` / `which would benefit both ISPs and the end users.`
13. L1703–1709 (single-cloud limitation): `Also, only a` / `few VNFP solutions, such as in [123], [158], [166], are applied` / `in multiple federated clouds, while most of the surveyed` / `works treat the problem of VNFP within only a single cloud` / `environment (e.g., in [42], [85], [86], [90].`

Additional per-work limitation statements are recorded in the Table IV–IX "Disadvantages" and "Suggestions to enhance the proposed solutions" columns, e.g. L646–648 `- Tested only on a` / `small-scale environment.`; L664–675 (Table IV, [80]) `Even if the policy is` / `demonstrated to achieve` / `better performance` / `compared to the` / `previous work,` / `it is not however tested in a` / `real cloud infrastructure.`; L1156–1163 (reliability discussion) `it is worth not-` / `ing that redundant configurations imply an important increase` / `in resources utilization and it must take into consideration the` / `additional QoS issues to likely encounter, mainly regarding` / `network congestion and aggregate traffic, and mostly in online` / `VMP scenarios.`

---

## 12. Explicit research gaps stated by the survey

The survey states its gaps explicitly; verbatim:

1. **Unaddressed VNF use cases** — L1669–1675 (right column): `Also, we observed that many` / `VNF use cases have not been addressed yet (if partially)` / `by the research community, namely the home and business` / `gateway virtualization (i.e., vCPE, SD-WAN), Virtual Platform` / `as a Service, mobile base station virtualization, and CDN` / `virtualization. We believe that these tracks are vital and should` / `be considered by fellow researchers working on NFV.`
2. **Neglected VMP objectives** — L1675–1679 (right column; `In` ends L1675): `parallel to in-depth study of these use cases, more research` / `should be dedicated to VM allocation, specifically to optimize` / `some objectives which were neglected in comparison to others` / `(e.g., overhead, ROI, and aggregate traffic).`
3. **No prior extensive VNF-placement survey (motivation for the paper)** — L217–221: `To the best knowledge of the authors, there is no extensive` / `survey, in the literature, on the problem of VNF placement in` / `cloud environments, apart from the work presented by Li et` / `al. in [119].`
4. **Container placement solutions scarce** — L358–361: `In this paper, the focus is on VM placement as there` / `are not many solutions for container placement in the` / `literature. However, many VM placement approaches can` / `be adapted to also optimally place containers.`
5. **Multi-tenancy not addressed by reviewed solutions** — L1033–1037 table (Table VII, [46]): `The constraints` / `defined in the solution` / `don’t consider the case` / `of multi-tenant` / `cloud environments`; and L1041–1049 (Table VII, [51]): `The constraints defined` / `in the solution don’t` / `consider the case of` / `multi-tenant cloud` / `environments`
6. **Scalability of exact CSP methods** — L678–690 (Table IV, [83]): `Since CSP explores` / `all possible solutions` / `for a set of input data,` / `it cannot be applied` / `to very large datasets.`; L695–703 (Table IV, [94]): `Since CSP explores` / `all possible solutions` / `for a set of input data,` / `it cannot be applied to` / `very large datasets.`
7. **Gap identified by the survey in QoS/optimality trade-off of auction-based DIP** — L834–841 (Table V, [29]): `The placement` / `decisions are made` / `to the detriment of` / `QoS` / `- The application` / `sizing is ignored` / `and not considered`
8. **Gap in federated/multi-cloud application of reviewed VMP** — L638–643 (Table IV, [13]): `- Cannot know if it will` / `be performing well in` / `a federated environment.`
9. **Named future-work directions in the conclusion** — L1727–1733: `Rele-` / `vant protocols, heuristics, algorithms, and architectures were` / `surveyed with the main motivation to propose, as future work,` / `efficient strategies to carry out efficient network slicing, in` / `order to satisfy the end-users and verticals, and respect the` / `several constraints in place.`

---

## 13. Reviewer-verification quote sheet (10 most important verbatim quotes)

1. **L43** — `This is the accepted version of the original article published by IEEE.` *(document version: accepted manuscript, not published version)*
2. **L22–23** — `Document Version` / `Peer reviewed version`
3. **L14–15** — `DOI:` / `10.1109/COMST.2018.2884835` *(with L7 title and L11 venue `IEEE Communications Surveys and Tutorials`)*
4. **L74–77** — `The paper then proposes` / `a classification of VNF Placement (VNFP) approaches, first,` / `regarding the general placement and management issues of` / `VNFs, and second, based on the target VNF type.` *(survey/taxonomy contribution; no experiments)*
5. **L546–553** — `Also, for each section, we sum-` / `marize the challenges and suggestions, concerning the most` / `relevant/recent research works, in a dedicated table (Tables IV` / `to IX). Each table contains the advantages and disadvantages` / `that we have assessed for the adopted solutions and frame-` / `works, as well as enhancement propositions that could guide` / `the reader to spot possible research directions.` *(the authors' own contribution is qualitative assessment; there are no author-run experiments)*
6. **L462–463 / L525–530** — `process can be carried out either offline (static) or online (dy-` / `namic) [135]–[137].` … `Table II shows a global classification of VMP solutions into` / `online and offline approaches, while Table III categorizes the` / `different VMP solutions as per their target objective.` *(core VMP taxonomy axis)*
7. **L1214–1222** — `As depicted in Fig. 6, the VNF placement` / `can be classified into two main categories:` / `• The general placement: the focus here is to define effi-` … `• The placement of specific network functions, such as` / `Packet Data Network Gateways (P-GWs), Serving Gate-` / `ways (S-GWs), and transcoders.` *(core VNFP taxonomy axis)*
8. **L754 / L1241–1243 / L1374 / L1657** — `comparison to the Mixed Integer Programming (MIP) solution`; `on Integer Linear Programming (ILP), the proposed algorithm` / `finishes in few seconds (i.e., 16 seconds) which makes it quick`; `to the NFV paradigm. Based on MIP, four heuristic algorithms,`; `slice based on two ILPs formulations and solved based on the` *(named optimization formulations in the reviewed literature)*
9. **L1666–1675** — `Admittedly, NFV is still in its early stages. To ensure the` / `ultra-short latency, high QoS, service reliability and security` / `promised in 5G, many key challenges still need to be thor-` / `oughly addressed.` … `Also, there is still room for work, particularly, concerning` / `service reliability and k-resiliency, and the optimization of` / `overhead and data transfer time in case of online VMP.` *(open challenges, verbatim)*
10. **L1669–1679** — `Also, we observed that many` / `VNF use cases have not been addressed yet (if partially)` / `by the research community, namely the home and business` / `gateway virtualization (i.e., vCPE, SD-WAN), Virtual Platform` / `as a Service, mobile base station virtualization, and CDN` / `virtualization.` … `some objectives which were neglected in comparison to others` / `(e.g., overhead, ROI, and aggregate traffic).` *(explicit research gaps, verbatim)*

**Negative findings a reviewer should note:** zero matches in the file for `machine learning`, `deep learning`, `reinforcement`, `Kubernetes`, `Mininet`, `GLPK`, `ZSM`, `ONAP`, `OSM`, `Tabu`; and no survey-level percentage or per-category paper counts anywhere (**NOT REPORTED**).
