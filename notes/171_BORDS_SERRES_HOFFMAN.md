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
3. ~~By analogy with Paley 25, an asymmetric srg(243,22,1,2), if one exists, should be sought **without** a Hoffman
   coclique and **without** an imposed partition.~~ **Withdrawn (§7):** this inference is false in general. An
   asymmetric srg(25,12,5,6) has three Hoffman cocliques, and Paley(25) and an asymmetric graph share one Hoffman
   coclique together with all its incidences. Rigidity was shown for one BvLS design only, not for every 2-(45,5,2).
4. At 99, the α = 22 sub-case does reduce to designs plus completions (§5), but uniqueness of the completion is
   **not** to be expected in general. By the extension lemma (§7), the completions with an asymmetric graph form free
   orbits under Aut(design). The direct exact model of §5 makes no assumption either way.

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
- `hoffman/autosave.sh` copies the live ledger (ignored by git) to `ledger_snapshot.jsonl` every 20 min, then commits and
  pushes only that snapshot and `STATUS.txt`. `resume.sh` restores the ledger from the snapshot if the container was lost.
- After a restart: `bash code/asym243/hoffman/resume.sh 3 1800` (idempotent). At most one cube of ≤ 30 min per worker
  can be lost.
- Initial cubes: A and B split immediately into 4 + 4 children (block 25 fixed).

## 7. External dossier HOFFMAN_UPDATE (ChatGPT, 11 Oct 2026): integration and correction
These results were read for context and are recorded as reported. They were not reproduced here. The dossier has its
own reviewer and a fresh-folder reproduction, but no DRAT or Lean certificates.

**Closed (as reported).** Under the hypothesis α = 22, the design of the coclique can have neither of the following.
- **A transitive Z/22 action.** There are 80 normalised selections, 8 of which have a triple intersection; the other
  72 have no completion.
- **A group of order 21 fixing one point and regular on the other 21.** C21 is impossible directly: it would repeat the
  unique short block orbit. For C7⋊C3 there are 236 selections, 37 of which have a triple intersection; the other 199
  have no completion, and 12 of them already have an empty row domain.

No symmetry is imposed on the completion D: each of the 77 rows has its own domain, and the pair rule (P) is the one
of §5. The 72 and 199 are normalised labelled presentations, **not** isomorphism classes. Designs without these
actions, asymmetric designs in particular, are not covered. These two families are sub-cases of the cube search of §6.
If that search returns SAT, the design found cannot belong to them.

**Correction to §4 bis (HOF-003).** "A Hoffman coclique excludes asymmetry" is false. See the counterexample in
§4 bis.3: an asymmetric srg(25,12,5,6) has exactly three Hoffman cocliques of size 5. Moreover Paley(25) and an
asymmetric graph share the same coclique {4,8,12,16,20} with all its incidences, a 2-(5,3,6) design with each block
repeated. What the BvLS computation of §4 bis shows is **one design ⇒ one completion**. It does not show that every
2-(45,5,2) design behaves this way. The 1,691 cocliques are a lower bound from an interrupted enumeration.

**Extension lemma.** Let H = Aut(Y) act on the completions by D ↦ QDQᵀ. Then Stab_H(D) = Aut(Γ)_C. Consequences:
- a unique completion of a design with H ≠ 1 gives a non-asymmetric graph;
- the completions whose graph is asymmetric form free H-orbits, so their labelled number is a multiple of |H|;
- Aut(Γ)_C = 1 does not imply Aut(Γ) = 1, since an automorphism can move C.

For C1 this means: an asymmetric Conway graph with α = 22 has a design Y whose completions come in at least |Aut(Y)|
labelled copies. A rigid design (unique completion) is compatible with C1 only if Aut(Y) = 1.

**Check of the A/B split of §5.** The dossier confirms that cases A and B cover everything (THEORIE §6). It also
confirms that YYᵀ = 12I + 2J; a coefficient of 18 given in an earlier ChatGPT answer was a mistake on its side.

### 7.1 The Gram matrix Q, and what it is (derived here)
The dossier introduces Q = 9I − 3D − N + J (N = YᵀY), with Q² = 21Q, QYᵀ = 0, Q𝟏 = 0 and diag 6. Off-diagonal
entries: −3 for a mate edge, −2 for an edge between disjoint blocks, −1/0/1 for a non-edge with intersection 2/1/0.

**Identification.** R⁷⁷ = 𝟏 ⊕ Yᵀ(𝟏^⊥) ⊕ ker Y, of dimensions 1 + 21 + 55. The eigenvalues are as follows.
- D: 10 on 𝟏 (D𝟏 = 10·𝟏); −1 on Yᵀ(𝟏^⊥), since DYᵀ = 2J − Yᵀ; and 3 or −4 on ker Y, since D² + D = 12 there.
- N: 56 on 𝟏; 12 on Yᵀ(𝟏^⊥); 0 on ker Y.
- J: 77 on 𝟏; 0 on the other two.

So Q vanishes on 𝟏 (9 − 30 − 56 + 77) and on Yᵀ(𝟏^⊥) (9 + 3 − 12). It equals 9 − 3·3 = 0 on the 3-eigenspace and
9 + 12 = 21 on the −4-eigenspace of D in ker Y. Hence

  **Q = 21·P₋₄**, where P₋₄ is the orthogonal projector onto the (−4)-eigenspace of D, of dimension 22.

This is the part of the 44-dimensional (−4)-eigenspace of A that is supported on F. The 77 vectors vᵢ = √21·P₋₄eᵢ
have norm 6 and sum 0, with Σ vᵢvᵢᵀ = 21·I₂₂: they form a tight frame and a spherical 2-design in R²².

**Lattice.** Let L = ⟨vᵢ⟩_Z. Then L is even (norms 6), positive definite, of rank 22. Its dual L* satisfies 21L* ⊆ L.
Moreover L*/L ≅ the torsion of coker Q, so the Smith invariants of Q lie in {1, 3, 7, 21}. Set a = 22 − rank₃(Q) and
b = 22 − rank₇(Q). Then det L = 3ᵃ7ᵇ.

**Elementary necessary conditions.** These are derived here and have not been tested by computation.
1. *Parity.* An even lattice of even rank n with odd determinant d satisfies (−1)^{n/2}d ≡ 1 (mod 4). With n = 22 this
   gives 3ᵃ7ᵇ ≡ 3 (mod 4), that is, **a + b odd**. Milgram's formula adds a sign condition on the Legendre symbols of the
   3- and 7-parts.
2. *a depends only on the design.* Mod 3, Q ≡ J − N ≡ Yᵀ(J₂₂ − I)Y; entrywise this is 16 − |B_b ∩ B_c|. Since
   (J₂₂ − I)𝟏 = 21·𝟏 ≡ 0, we get rank₃(Q) ≤ 21, so a ≥ 1.
3. *b is tied to a graph invariant.* The Schur complement of the block 4I (invertible mod 7) gives
   rank₇(A + 4I) = 22 + rank₇(D + 4I − 2N). Also 2Q ≡ (D + 4I − 2N) + 2J (mod 7), with Q𝟏 = 0 and 𝟏ᵀ𝟏 ≡ 0 mod 7.
   So rank₇(A + 4I) = 22 + rank₇(Q) + ε, with ε ∈ {−1, 0, +1}:
   - ε = +1 if 𝟏 ∉ Im₇Q;
   - otherwise, writing 𝟏 = Qw, ε = 0 if 𝟏ᵀw ≠ 1 and ε = −1 if 𝟏ᵀw = 1.

   Note also that (A + 4I)² ≡ 2J mod 7, since (A − 3I)(A + 4I) = 2J; this gives rank₇(A + 4I) ≤ 50.

**Reading.** On its own the parity condition is no contradiction: it ties the 3-rank of the design to the 7-rank of
the completion. It is a filter on designs that a lattice classification (even lattices of rank 22 and level 21, generated
by norm-6 vectors forming a 2-design with inner products in {−3, …, 1}) could sharpen. The search stays open. This is
the most structured new lead for α = 22, and it is complementary to the cube search of §6, which remains the covering
route.
