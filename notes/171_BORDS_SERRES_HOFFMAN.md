# 171 — External dossiers (Paley 25, BvLS) and tight boundaries: Hoffman cocliques at 243 and at 99 (11/10, evening)

*Status of the external results: produced by another agent (GPT-6, two dossiers forwarded by Dilan), integrated here
**as context**. They are **not reproduced** in this session, at Dilan's request (confidence granted). Their code was
not run here; only the reports were read. Everything marked "here" was computed in this session, with its own code
(`code/asym243/hoffman/`).*

## 1. What the dossiers bring (external)
**Method.** Fixed-boundary reconstruction. With V = S ⊔ F, the blocks C = A[S,S] and Y = A[S,F] are fixed, and the
unknown D = A[F,F] must satisfy:
- YD = (λ−μ)Y + μJ − CY;
- D² = (k−μ)I + (λ−μ)D + μJ − YᵀY;
- D𝟏 = k𝟏 − Yᵀ𝟏.

Each row gets a finite domain; two rows are compatible iff d_i(j) = d_j(i) and d_i·d_j + (YᵀY)_ij = μ + (λ−μ)d_i(j).
The model is **equivalent** to the completion problem. Same algebra as the spectral surgery of note 165.

**Paley(25).** Boundary = a K₅ (a Delsarte clique: every outside vertex has exactly 2 neighbours in it, forced).
- The reconstruction finds **all 15** srg(25,12,5,6), including **both asymmetric ones** (1,999,872 labelled
  completions, count checked class by class by #K₅·5!·2¹⁰/|Aut|).
- Imposing a partition into 5 K₅'s yields only the two symmetric classes (|Aut| 72 and 600): the 13 others, including
  the asymmetric ones, have no such partition.
- Godsil–McKay one-cell switching does not leave the component of Paley.
- Asymmetry certificate: the union U of all the K₅'s is intrinsic; G[U] has a single involution, and it does not extend
  because the attachment profiles of the 10 outside vertices are not preserved.

**BvLS.** Boundary = triangle T + N(T), with the far region (180 vertices) free.
- The far region plus 1 prism (186 free vertices) gives exactly BvLS and the twin (16 matrices).
- The far region plus **2 prisms** (192 free vertices) gives exactly BvLS and the twin (27,648 = 2·(4!)³ matrices), for
  every triangle and every pair of prisms (covered by explicit transports).
- Γ₃, one triangle plus 1 prism: Γ₃ only.
- 3 prisms: **open** (domains 3,645 / 1,895).

This extends our "line threshold" (note 165 §7: 2 candidates per row on the far region of a line) to two prisms.

## 2. What I take from them (mechanisms)
1. **A representation that is too strong blocks asymmetry** (Paley 25: a clique partition exists only in the
   symmetric classes). This applies directly to our searches that impose a partition:
   - the S₃ parity searches impose a regular spread, i.e. a cover of BH;
   - the "new skeleton" grid searches impose a partition into 27 grids, i.e. a cover of K_{9,9,9}.

   They can produce new graphs, but they may be **blind** to the asymmetric ones.
2. **A tight boundary.** A Delsarte clique (or a Hoffman coclique) has **forced** attachments. A reconstruction from such
   a boundary therefore covers *all* graphs that contain one, with no partition imposed. In the λ = 1, μ = 2 family the
   maximal cliques are triangles (the Delsarte bound is not an integer). **The tight object is the Hoffman coclique.**
3. **Local rigidity at several scales** (line → 2 prisms; re-gluing of ≤ 9 grids, note 167): BvLS is far from any other
   graph. A new graph must differ from it on a "large" region.

4. **Transposing the row engine to the gluing models.** In a grid cover, the "row" of a vertex is its set of 18
   partners in the matchings. Its domain under the gluing law is exactly the arc consistency that the compact CNF
   (`grid243_cnf.py`) already propagates. So the engine adds nothing there. **What does transpose is the choice of a
   tight boundary**, which removes the need to impose a partition. Hence §3–§5.

**Incident.** The container restarted at around 18:13. The following searches were lost **without a verdict**:
- Conway sub-case (A), CP-SAT;
- S₃ parity 3a/3b (about 4 h of kissat/CMS);
- skeleton (54,81) (about 3 h of kissat).

Given point 1, they are not relaunched as they stand.

## 3. Hoffman cocliques at 243 (here)
**Bound.** v(−s)/(k−s) = 243·5/27 = **45**. A coclique C of size 45 is a Hoffman coclique ⇔ every outside vertex has
exactly 5 neighbours in C ⇔ **x = 𝟏_C satisfies (A + 5I)x = 5·𝟏** (an exact cover).
- Its outside blocks form a **2-(45,5,2)** design with 198 blocks and r = 22.
- Block intersections are ≤ 2 (λ = 1, μ = 2).

**Census** (CP-SAT, exact formulation, `scratchpad/hoffman243.py`):

| graph | Hoffman cocliques (45) |
|---|---|
| BvLS | **≥ 1,691** (enumeration incomplete after 1200 s) |
| twin | **none** (INFEASIBLE, 378 s) |
| Γ₃ | **none** (INFEASIBLE, 464 s) |
| Γ₄ | **none** (INFEASIBLE, 622 s) |

> The tight structure exists only in BvLS: exactly Paley's phenomenon (clique partitions only in the most symmetric
> classes). Tight sets are a marker of high symmetry in the known family.

BvLS design (one coclique): 198 distinct blocks, intersections 0 / 1 / 2 with multiplicities 10,098 / 8,415 / 990. The
990 pairs meeting in 2 are the C(45,2) point pairs, so they are forced non-edges.

## 4. Reconstruction of 243 from a Hoffman boundary (here)
- Boundary: C (45 vertices) and all its incidences (the design). Free: **the 198 other vertices (81 % of the graph)**.
  No partition, spread or symmetry imposed.
- Row domain: choose 17 blocks covering once each point of the row's own block and twice each other point. Neighbours
  pairwise meet in ≤ 1 point, and meet the row's block in ≤ 1.
- C++ enumerator `hoffman/rowdom.cpp`, exhaustive. Assembly `hoffman/assemble.py`: forward checking, no symmetry
  reduction.

### 4 bis. Result: total rigidity
- Domains: 72 rows of 187 candidates, 90 of 191, 36 of 227 (38,826 candidates in total). The true row of BvLS is in each
  domain (checked).
- Exhaustive assembly, **with no symmetry reduction**: **1 single completion** (277 nodes, 1.8 s). It is a
  srg(243,22,1,2) checked in integers and isomorphic to BvLS (nauty, |Aut| = 3,849,120).

> **Theorem (exhaustive computation).** Every srg(243,22,1,2) containing a Hoffman coclique whose design is this
> 2-(45,5,2) design of BvLS **is BvLS**. More precisely, the boundary determines the 198 other vertices **uniquely**:
> there is no "second solution" here.

**Comparison of rigidities:**

| boundary | free vertices | completions |
|---|---:|---:|
| line + N(T) (note 165, dossier) | 180 | 2 (BvLS, twin) |
| line + N(T) − 2 prisms (dossier) | 192 | 27,648 = 2 classes |
| **Hoffman coclique + design** | **198** | **1 (BvLS)** |

A tight boundary freezes more than a triangle boundary, even though it leaves more vertices free.

**Reading.**
1. The Hoffman coclique is the **most rigidifying** tight structure seen so far.
2. In the known family it exists only in BvLS: the three less symmetric graphs have none (§3).
3. By analogy with Paley 25, an asymmetric srg(243,22,1,2), if one exists, should be sought **without** a Hoffman
   coclique and **without** an imposed partition.
4. At 99 the same mechanism suggests the following. If α(Γ) = 22, Γ would probably be determined by its 2-(22,4,2)
   design, so the sub-case reduces to designs. Hence the interest of the direct exact model of §5.

## 5. Conway-99: the sub-case α = 22 (structure proved here)
**Bound.** 99·4/18 = **22**. A Hoffman coclique C (22) ⇔ (A + 4I)𝟏_C = 4·𝟏. Each of the 77 outside vertices then has
exactly 4 neighbours in C.

Consequences, for Y = the incidence matrix of C × F and D = the graph on F:
1. **Design.** A 2-(22,4,2) design: YYᵀ = 12I + 2J, r = 14, 77 blocks. Intersections are ≤ 2, and the counts are forced:
   **231** pairs at 2 (one per pair of points), **1540** at 1, **1155** at 0.
2. **Equations.** YD = 2J − Y and D² + D = 12I + 2J − YᵀY. Moreover D commutes with N = YᵀY (DN = 8J − N).
   - Hence D = −1 on the 21-dimensional space spanned by the point vectors orthogonal to 𝟏.
   - On ker Y, D ∈ {3, −4} with multiplicities 33 and 22. (This recovers note 104 and explains it.)
3. **Equitable sets.** For each point s, W_s (the 14 blocks through s) is an equitable set of D with quotient
   [[1, 9], [2, 8]]: inside, a perfect matching; outside, exactly 2 neighbours in W_s.
4. **Decomposition of D = M ⊔ T** (proved):
   - the **"mate" edges**: two blocks meeting in exactly one point s, whose triangle is closed by s. There are 154 of
     them, a 4-regular graph, a union over the points of 7K₂ (the matching of N(s));
   - the **triangle edges**: two disjoint blocks. There are 231 of them, forming **77 edge-disjoint triangles**, each
     block in exactly 3, with the three blocks of a triangle pairwise disjoint (12 points).

   Each block then has N_Γ(w) = 4 (point, mate) pairs ⊔ 3 triangle pairs = 7K₂.
   Checks: tr D³ = 462 = 6·77; Σ_{w≠w′}(D²)_{ww′} = 6930.
5. **Rooted reformulation.** Root the vertex-centred model (N(v) = 7K₂, 84 second neighbours indexed by the non-mate
   pairs) at a point v of C. Then α = 22 ⇔ there is a **cubic graph H on N(v)**, disjoint from the matching, such that:
   - the 21 second neighbours corresponding to the edges of H are pairwise non-adjacent;
   - each of the 63 other second neighbours has exactly 4 neighbours among them.

**Literature.** No exclusion of α = 22 was found (quick search; Wilbrink: no automorphism of order 11). The sub-case
appears to be open.

**Exact model and pilot (here).** `hoffman/alpha_cnf.py` builds the CNF "srg(v,k,λ,μ) with a fixed Hoffman coclique":
exact encoding plus WLOG symmetry breaking.
- Positive controls: srg(9,4,1,2) SAT; srg(25,12,5,6) SAT (decoded and checked).
- Conway: 2.04 M variables, 7.17 M clauses, with blocks 22 = {0,1,2,3} and 23 = {0,4,5,6} fixed (WLOG). Kissat
  **pilot** launched (limit 6 h).
  - Exhaustive split, WLOG: point 1 lies in exactly one other block through 0, say block 24 = {0,1,a,b}. Then
    {a,b} ∩ {2,3} = ∅, and at most one of a, b lies in {4,5,6}. Case **A**: 24 = {0,1,4,7}; case **B**:
    24 = {0,1,7,8}. Both run in parallel with the base instance. **SAT** would mean a Conway graph. **UNSAT** would mean α(Γ) ≤ 21 for every
  srg(99,14,1,2): a covering result for one sub-case, which would then need a certificate (DRAT).

## 6. Crash-proof execution (since 19:45)
Kissat cannot save its state, so the α = 22 search is cut into **cubes** (`hoffman/cuberunner.py`):
- Each verdict (UNSAT, SAT, SPLIT) is written as soon as it is known to `hoffman/cubes_alpha99/ledger.jsonl`, with
  fsync and a lock.
- A cube that is not decided within 30 min is **split** by fixing one more block through point 0. The children cover
  it exactly (signature symmetry, see the docstring), so its verdict is never lost.
- A solver killed with its worker leaves no orphan (PDEATHSIG). The cube of a dead worker is taken over automatically.
- `hoffman/autosave.sh` commits and pushes **only** the ledger and `STATUS.txt` every 20 min.
- After a restart: `bash code/asym243/hoffman/resume.sh 3 1800` (idempotent). At most one cube of ≤ 30 min per worker
  can be lost.
- Initial cubes: A and B split immediately into 4 + 4 children (block 25 fixed).
