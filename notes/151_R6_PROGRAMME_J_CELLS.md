# 151 — R6 programme: star-incidence counting, J3 and J1a structure (28/09 afternoon, C1)

**Context.**
- Finish line: R6 ∧ R8 (conway99-rank17/PROOF_OBLIGATION.md). C1 owns R6; structures owns R8.
- R6 says: no integer σ-odd (−4)-eigenvector h of Γ vanishes on x ∪ N(x) and has type n = 6. Its open cells are J1a, J2
  and J3. J0 is closed by min N* ≥ 8/7; J1b by the star bound.

**Labels.** DERIVED = written proof here. CALCUL = exact finite check, no solver.

## 0. Vertex-level setting (PROVEN, standard)
- **Roots.** The 84 roots are r(c^a, d^b) ↔ the D₇ roots a e_c + b e_d. σ acts as −1.
  - O_{c^s} = N(c^s) ∩ roots = {r : r_c = s}, 12 roots.
  - star(c) = O_{c⁺} ∪ O_{c⁻}, 24 roots.
- **(L0) Star incidences.**
  - r ∈ O_{c^s}: r has exactly 1 neighbour in O_{c^s} (its Q_c-partner, via the triangle with c^s) and exactly 1 in O_{c^{−s}}
    (its P_c-partner, since μ(r, c^{−s}) = 2).
  - r ∉ star(c): r has exactly 2 neighbours in O_{c⁺} and 2 in O_{c⁻}.
- **(L1) Support identity.** For every root r and every set S of blocks,
  Σ_{w∼r, w root} |supp(w) ∩ S| = 4|S| − 2|S ∩ supp(r)|.
  This is (L0) summed over c ∈ S.
- **(L2) D₇ coordinates are harmonic on the root layer.** For every root r, the D₇ vectors of its 12 root neighbours sum to 0.
  - In other words, A_R g_c = 0 for g_c(r) = r_c.
  - Equivalently, b_c = −4(e_{c⁺} − e_{c⁻}) + g_c is a (−4)-eigenvector.
  - The same construction at any base point v and any line L ∋ v gives an integer (−4)-eigenvector of norm 56.
- **Eigenvector.** h is σ-odd, Ah = −4h, and h = 0 on x ∪ N(x).
  - Block balance: Σ_{O_{c^s}} h = 0.
  - A D-pair (u adjacent to both v and σv) contributes 0 to every row.

## 1. J3: a = ±1 exactly on a 3|4 cut I|J (DERIVED)
Notation:
- T = the 48 cut roots, with P = {h = +1} and Q = σP.
- Z_I = the 12 roots inside I; Z_J = the 24 roots inside J.
- d(p) = number of P-neighbours of p ∈ P; e = e(P).
- τ(z) = number of P-neighbours of z ∈ Z, which equals its number of Q-neighbours.

Results:
- **Local profile.** From the eigen-equation and (L1) with S = I and S = J, each p ∈ P has:
  - d P-neighbours and d + 4 Q-neighbours;
  - exactly 3 − d neighbours in Z_I and 5 − d in Z_J.
  - Hence **d ≤ 3**.
- **Profile of Z.**
  - z ∈ Z_I: τ ≤ 4, with 4 − τ neighbours in Z_I and 8 − τ in Z_J.
  - z ∈ Z_J: τ ≤ 6, with 6 − τ neighbours in Z_I and 6 − τ in Z_J.
- **Edge counts.** e(Z_I) = e − 12, e(Z_J) = e + 12, Σ_{Z_I} τ = 72 − 2e, Σ_{Z_J} τ = 120 − 2e.
  - The capacity of Z_I gives **e ≥ 12**.
  - The second moment gives Σd² + 9e + Σ_Z τ² = 444 (per orbit), and Cauchy–Schwarz gives **e ≤ 24**.
- **Per-block identities** (A²1_P evaluated at the inner vertices):
  - D_i + Σ_{Z_I ∩ O_{i⁺}} τ = 24 for i ∈ I;
  - D_j + Σ_{Z_J ∩ O_{j⁺}} τ = 30 for j ∈ J;
  - here D_c = Σ_{p ∈ P ∩ star(c)} d(p).
- **Root identity.** (A_R + 5I)φ = c on the roots, where:
  - φ = d on P, d∘σ on Q and τ on Z;
  - c = 37 on T, 40 on Z_I and 42 on Z_J.
- **Quotient spectrum** (CALCUL, sympy). The averaged 7-class quotient has eigenvalues 14, 3², (−4)³ and (5e − 84)/12.
  - Interlacing only gives e ≤ 24.
  - e = 24 is an equitable partition with admissible spectrum.
  - **Conclusion: counting and spectra do not kill J3.** As in notes/150, every quadratic identity is automatic, so the kill
    must be combinatorial.
- **Sign classes.** There are 8 (structures, n6_k3_classes.json). In cell terms each cell is S (p = q) or X (p = −q), with
  S-signs balanced in each row and X-signs balanced in each column.
  - Class 0 is the product pattern h(r) = r_i ε_j with ε = (+,+,−,−).

## 2. J1a: n = 6, cut {c}; twelve ±1 on star(c), three ±2 off star(c) (DERIVED — the structure is forced)
1. **Capacity.**
   - Every U ∈ star(c) needs |outside part| ≥ 2, so it must be T-adjacent to a ±2 label.
   - Each ±2 label V ∉ star(c) has at most 4 nonzeros over star(c) (R2).
   - 3 × 4 = 12, so **each U has exactly one ±2 neighbour label**, and each V has exactly 4, which forces D(V) ∉ star(c).
2. **Signs in star(c).**
   - For each U, a_U · (star part) = −2 and a_U · (outside part) = −2.
   - In local orientation, Q_c joins opposite signs and P_c joins equal signs.
   - At vertex level, **every root of star(c) has both of its star(c)-neighbours of the opposite sign**.
   - There is no D-edge inside star(c): **star(c) is a free star**.
3. **The ±2 vertices.**
   - Write v_k (h = +2) and σv_k (h = −2), k = 1, 2, 3.
   - The eigen-equation at v_k forces its 4 star(c)-neighbours to be −1, and v_k ∼ σv_j, v_k ≁ v_j for j ≠ k.
   - So **the six ±2 vertices induce a C₆**, with T_{V_k V_j} = −1 (a negative triangle at label level).
4. **Groups.**
   - The 12 (−1)-vertices of star(c) split into 3 groups of 4 by their unique v-neighbour; the (+1)-vertices split likewise by σv.
   - Every other neighbour of a star(c) vertex, and of a v_k, is a 0-vertex.
   - For a 0-root m: n_m (its (−1)-neighbours in star(c)) = 2 + #v(m) − #σv(m).
5. **Balance and geometry.**
   - With ρ_k the D₇ vector of v_k (supported off c): (Σ ρ_k)_d = −δ_d ∈ {0, ±1}.
   - So the cell multigraph of ρ₁, ρ₂, ρ₃ has its odd-degree blocks exactly at the X-cells: matching, P₃ + K₂, P₄, K₁,₃,
     triangle, or a double edge + one edge.
   - The D-partner of each V_k is a 0-orbit.
6. **Status.** OPEN. Pair counts (μ between the groups, the v's and the 0-roots) are all consistent so far; they are consequences
   of A² again. Next: exploit the free star(c) (2-regular, sign-bipartite, Q/P-alternating cycles of length ≡ 0 mod 4) together
   with the C₆ apexes and the X-cell interior vertices.

### 2.7 J1a — exhaustive split by the configuration of the three ±2 cells (DERIVED, 28/09 afternoon)
- ρ_k = D₇ vector of v_k, supported on B₀ = [7] ∖ {c}. The balance at d^± forces net_d = Σ_k (ρ_k)_d ∈ {0, ±1} for every
  d ∈ B₀.
- The three cells form a multigraph with 3 edges on the 6 blocks of B₀, and its odd-degree blocks are exactly the X-cells.
  There are exactly six types:
  - (i) matching;
  - (ii) P₃ + K₂;
  - (iii) P₄;
  - (iv) K₁,₃;
  - (v) triangle;
  - (vi) double edge + edge.
- Tools, all consequences of λ = 1:
  - (F1) two adjacent vertices of the same O_ι form a line with ι;
  - (F4) if v_j and v_k share a signed block d^s, then σv_l ∉ O_{d^s}. Otherwise the edge d^s–σv_l would lie in two
    triangles, since σv_l ∼ v_j, v_k.
- **(iv) is DEAD.** net at the centre d is ±1, so two of the ρ's have the same sign s at d and the third has −s. Then v_j, v_k
  and σv_l all lie in O_{d^s}, contradicting (F4).
- **(vi) is DEAD.** Two sibling ±2 labels on {d,e}, with the third needed to repair the net. In both sign cases two v's share an
  inner vertex that also contains σv₃, contradicting (F4).
- **(v) triangle (X = 0), consistent so far.**
  - All 6 C₆ apexes are inner vertices.
  - The m_{jk} are zeros with #v = 2, #σv = 0, so n = 4: all four corners are in A. Exactly one corner lies in G_j, one in G_k,
    and two in G_l, on opposite sides.
  - The D-zeros have n = 2. The two remaining zeros of v_k have n = 3.
  - The inner vertices of the triangle blocks exclude their A-roots from the adjacent groups.
- **Open branches:** (i) (X = 6), (ii) (X = 4), (iii) (X = 2), (v) (X = 0).

### 2.8 J1a — the zero-graph equations (DERIVED, pointwise, not aggregated)
Notation, for each zero root y:
- d(y) = t_v(y) − t_σ(y) = n(y) − 2 (the eigen-condition);
- f(y) = ρ(y)·N, with N = Σ_k ρ_k;
- A_Z = the adjacency among the 54 zeros.

**The two equations.**
- **(A_Z + I) d = −f.** This is μ-counting of y against A, combined with the balance at y's inner neighbours.
- **A_Z f = −Σ_corners f − Σ_{±2 nbrs} f**, since f is a combination of the D₇ coordinates and A_R g_c = 0.

**Consequences by type.**
- **Type (v)** (N = 0): (A_Z + I) d = 0. So d ≠ 0 is a (−1)-eigenvector of the zero graph, because d(m_jk) = 2.
- **Type (i)** (all X-cells): Σ_corners f = 2d and Σ_{±2} f = 2d, so A_Z f = −4d.
  - Hence (A_Z² + A_Z − 4) d = 0: d lives in the eigenspaces (−1 ± √17)/2 of A_Z.
  - Σdf = 4Σd² − 96, and Cauchy–Schwarz gives 15 ≤ Σd² ≤ 39.
- **Interlacing.** A_Z is a principal submatrix of A (54 of 99), so λ₂(A_Z) = … = λ₁₀(A_Z) = 3.
- **Type (i), generic sub-case.**
  - Setting: d = ±2 exactly on m_jk / σm_jk, and every A-vertex is a corner of exactly one m.
  - ‖A_{Zᶜ,Z} d‖² = 8Σd² = 192 is already reached by the S-vertices (96) and the star vertices (96).
  - Hence **every inner vertex e^s has #m = #σm among its zero neighbours**, so Σ_jk ρ(m_jk) = 0: the three m's lie on a
    signed triangle of cells.

### 2.9 J1a — no hubs (all types), and type (i) is DEAD (DERIVED)
**Roles.** For every pair of S-vertices, the common neighbours outside star(c) are:
- (v_i, v_j): {σv_k, m_ij};
- (v_i, σv_i): the D-orbit (2 vertices);
- (v_i, σv_j), an edge of C₆: its apex a_ij.

Each role is either a zero or an inner vertex. An inner vertex arises only when the two ρ's share a signed coordinate.

**No hubs.** Write T(w) for the S-neighbours of a zero w, n(w) = 2 + t_v − t_σ for its number of A-corners, and
c_i(w) = |corners(w) ∩ G_i|. Then:
- c_i + (shared inner vertex with v_i) + (common S/zero neighbours of w and v_i) = 1 if v_i ∈ T(w), and 2 otherwise.
- Every σv_k ∈ T(w) is a common neighbour of w and each v_i with i ≠ k.

These rules kill every |T| ≥ 3:
- {v_i, v_j, σv_k}: c_i = c_j = 0, so c_k = 3 > 2.
- {v_i, v_j, σv_i}: c_j = 0 and c_k ≤ 1, but n = 3.
- All |T| = 4 sets, and {v₁, v₂, v₃, σv_i}: dead (two D-roles, or a common neighbour appears twice).

So **every zero has |T| ≤ 2**. The zeros with t = 2 are exactly the zero-roles, and the number of zeros with t = 1 is
2·#(inner roles).

**Type (i) (matching, X = 6) is DEAD.**
1. All 18 roles are zeros, so v_i's six zeros are exactly m_ij, m_ik, m_i, σm_i, a_ij, a_ik.
2. m_jk has T = {v_j, v_k} and n = 4, so c = (1, 1, 2). It then shares no inner vertex with any v, so both of its sharers are
   σ's and f(m_jk) = −2.
3. Harmonicity. f = ρ·N is a combination of D₇ coordinates, so A_R f = 0. At v_i:
   Σ_{G_i} f (= 4) + f(σv_j) + f(σv_k) (= −4) + Σ_{Nz(v_i)} f = 0.
   Hence f(a_ij) + f(a_ik) = 4, so every apex has f = +2.
4. But σ(a_ij) = a_ji and f is σ-odd, so f(a_ji) = −2. Contradiction. ∎

**J1a now:** types (i), (iv) and (vi) are dead. Types (ii) P₃+K₂, (iii) P₄ and (v) triangle are open.

**General identities (all types).**
- Σ over i of the harmonicity at v_i gives **2 Σ_jk ρ(m_jk) = − Σ_{t=1 zeros u adjacent to a v} ρ(u)**. Type (i) recovers
  Σρ(m) = 0.
- An m_jk that is a zero shares no inner vertex with any v, so its coordinates lie on inner vertices containing no v.
- Pointwise: (A_Z + I)d = −f, and Σ_w d(w)f(w) = 0 (automatic).
- ‖A_{Zᶜ,Z}d‖² = 12Σd² − Σf².
  - In type (iii) this forces the zero-sum Σ_{O_{e^s} ∩ Z} d = 0 at every inner vertex.
  - That is again equivalent to the ρ-identity above, so nothing new.

**Type (ii) (P₃ + K₂, X = 4) is DEAD.**
- Setup: ρ₁ on {d,e}, ρ₂ on {e,f} (opposite at e), ρ₃ on {g,h}.
- Roles: a₁₂ and a₂₁ are inner (e^{±b}); every other role is a zero. The t=1 zeros are u₁ ∼ v₁, u₂ ∼ v₂ and their σ-images.
- The m's avoid e^± (both contain a v), so f(m) ∈ {−2, −1}.
- Summed harmonicity: Σx − 8 + 2Σf(m) + f(u₁) + f(u₂) = 0, with Σx = 8. Hence f(u₁) + f(u₂) = −2Σf(m) ≥ 6 > 4.
  Contradiction. ∎

**J1a open: (iii) P₄ (X = 2) and (v) triangle (X = 0).**
- (iii): m₁₂ ⊂ {d^{−a}, h, i}, m₂₃ ⊂ {g^{−γ}, h, i}, m₁₃ ⊂ {d^{−a}, g^{−γ}, h, i} (μ with σv₁, σv₃).
- The four t=1 zeros satisfy 2Σρ(m) = −Σρ(u).

## 2bis. Row-capacity lemma (DERIVED) and what it kills
- **Facts used.**
  - Each row of T has exactly 10 nonzero entries, each ±1 (diagonal of T² + T = 12I − CᵀC).
  - A label U ∈ star(c) has at most 2 of them inside star(c): its Q_c- and P_c-partners.
  - A label outside star(c) has at most 4 over star(c): (R2), from (L0).
  - A label of value α needs |(Ta)_U| = 4|α|.
- **Dead patterns.**
  - n = 5, k = 1 (twelve ±1 on star(c) + two ±2): every star label needs a ±2 neighbour, but 2 × 4 < 12. This re-proves
    Sol's §7.2.
  - n = 6: J1b.
  - n = 7:
    - "12 ±1 + ±4" (the ±4 gets ≤ 4 < 16);
    - "19 ±1 + ±3" (the ±3 gets ≤ 10 < 12).
  - n = 8:
    - k=1, "12 ±1 + ±4 + ±2" (the ±4 gets ≤ 4 + 2 < 16);
    - k=1, "11 ±1 + ±3 + three ±2" (the ±3 lies in star(c), so it gets ≤ 2 + 6 < 12);
    - k=1, "10 ±1 + two ±3 + ±2";
    - k=2, "19 ±1 + ±3 + ±2" (the ±3 gets ≤ 9 + 2 < 12);
    - k=3, "23 ±1 + ±3" (the ±3 gets ≤ 10 < 12).
  - So R8 is left with **k=0 (eight ±1), k=1 (12 ±1 + five ±2), k=2 (20 ±1 + three ±2), k=3 (24 ±1 + two ±2)**. Sent to
    structures.
- **J1a is the tight case** (3 × 4 = 12), whence §2.

## 2ter. J2: 2|5 cut {c,c'} | X, twenty ±1 + one ±2 (DERIVED)
- **The ±2 label is not in cell (c,c').**
  - A vertex v there has S-incidence 4 = t(v) + 2z₁₂(v) with S = {c,c'}.
  - So it has ≤ 4 cut neighbours, but it needs a difference of 8.
  - Hence V lies in a K₅(X) cell (x₀, y₀).
- **The +2 vertex v.**
  - It has exactly 8 cut neighbours, all −1: 4 in star(c) and 4 in star(c'), 2 on each side.
  - It has no neighbour in cell (c,c'), and 4 K₅-zero neighbours.
  - By σ, σv has 8 cut neighbours, all +1: the set P_σ.
- **Profiles of the P-cut vertices.**
  - P₀ (12 vertices, not adjacent to σv): d ≤ 1, d + 4 Q-neighbours, 1 − d neighbours in Z₁₂.
  - P_σ (8 vertices): d ≤ 2, d + 2 Q-neighbours, 2 − d neighbours in Z₁₂.
- **Capacity of Z₁₂** (the 4 roots of cell (c,c'), each with τ ≤ 2): 28 − 2e_P ≤ 8, so **10 ≤ e_P ≤ 14**. Also
  e(Z₁₂) = e_P − 10.
- **Modified balance.**
  - At x₀^{s₀} (v's side) the cut roots are 1P + 3Q; at x₀^{−s₀}, 3P + 1Q. Same at y₀.
  - Every other x has 2P + 2Q.
- The moment and μ-sum identities are all automatic again (checked for the pair (v, P_cut) and for the Z_X moments).

## 2quater. Methodological finding
Every identity obtained by summing μ/λ counts over classes follows from A² = 12I − A + 2J applied to vectors in the span of the
class indicators. It is therefore automatically consistent. The kills so far all come from **exact local capacities**:
- Z_I, and Z₁₂ in J2;
- the 4-per-star rule in J1a, J2 and the row-capacity lemma;
- the λ = 1 exclusivity in the C₆ of J1a.

The next steps have to be structural, pushing the rigid pieces (C₆, groups, the 8 opposite neighbours of v) until a capacity
breaks.

## 3. Next
- J1a: push the rigid structure to a contradiction or to an explicit local model. A model would have to be tested against BvLS
  and Paley 9: supports on at most 4 stars exist at m = 11 (dimension 4).
- J2: the 2|5 cut plus one ±2. Redo notes/150's class analysis with the modified balance.
- J3: class-by-class, class 0 (product) first.

## 4. STATE AT 28/09 ~18:30 (saved before an auto-compaction): where C1 stands, and what comes next
**Closed in R6** (proofs above):
- J0 (min N*) and J1b (row capacity).
- J1a types (i) matching, (ii) P₃+K₂, (iv) K₁,₃ and (vi) double edge.

**Open.**
- J1a (iii) P₄ and (v) triangle.
  - Both pass every local test: per-coordinate harmonicity at v₁, v₂, v₃ (all 64 group choices of the triangle-cell A-roots),
    star-Gram bounds, structures' E₄ pair lemma, and all summed λ/μ counts (automatic).
  - There is no pinned class for structures' Cauchy–Schwarz step (G5), because every zero touches star(c).
  - In (v) the six ±2 vertices form an A₂ hexagon of D₇ roots, and the C₆ edges are lines through the inner vertices of
    d, e, f. This looks like a "natural" local configuration.
- J2 and J3: only their structure is known (§1, §2ter).

**Data** (conway99-rank17/r6_data, RESULTS_28_09.md, exact, no solver):
- There are no linked n=6 pairs, and 220 of the 555 R6 classes have a single n=6 witness.
- 395 of the 754 open classes contain a short triple k, k', k ∓ k' with all norms ≤ 8: (6,8,8) in 302, (6,6,8) in 157,
  (5,5,6) in 88.

**Next (C1's decision, not started).** Attack the (6,8,8) triple theorem: three eigenvector patterns a1 (n=6: J1a/J2/J3),
a2 and a3 = a1 − a2 (n=8: k=1/2/3, since R8 k=0 is dead).
- Linear coupling, and cut(a3) = cut(a1) + cut(a2).
- In the example where a1 and a2 are both J3 and a1·a2 = 8: e₊ − e₋ = 8 and e₋ = #(±2 in a3). The admissible cuts and overlaps
  are finite.
- If it succeeds, it kills 302 classes. Then do (6,6,8) (157) and (5,5,6) (88).
- Otherwise go back to J1a (iii)/(v) with a new global ingredient.

**Peers.**
- structures = R8 k=1 (TARGETS_AB_STRUCTURES §7: same-sign lemma; anti pairs impossible; aligned-graph types C₅, house, …).
- The pairing R8 k ↔ J_k lets the two sides share kills.
- Protocol: short [RESULTAT] messages, one target at a time, notes in files.

## 5. 28/09 evening: the triple route is dropped (coverage data), back to R6 proper
**Data (CALCUL, exact short vectors, no solver; code/r6/rung_cover.py).**
- Single rungs over the 754 open classes: R8 covers 676, R6 covers 555, R5 covers 412 and R7 covers 274.
  R6 ∧ R8 covers all 754; R5 ∧ R8 misses 38; R7 ∧ R8 misses 44.
- **The 78 classes outside R8** (they have n=6 but no n=8) contain no (6,8,8) or (6,6,8) triple; 12 of them contain a
  (5,5,6) triple. Examples: 4 classes have exactly one short vector (a single ±κ with n=6).
- Short triples: (6,8,8) 302, (6,6,8) 157, (5,5,6) 88; union 395; (6,6,8) adds 67 beyond (6,8,8), (5,5,6) adds 26.

**Consequence (decision).**
- Every (6,8,8) class also has an n=8 witness, so R8 kills it anyway. The triple theorem is therefore off the critical
  path: at best it is insurance for R8.
- R6 is needed **in full**, as a single-vector statement. The 78 classes outside R8 include ones whose only short vector
  is one n=6 κ, so no pair or triple hypothesis is available there.
- C1 goes back to the open R6 cells: J1a (iii) and (v), then J2, then J3.

**Correction (a trap met while re-deriving).** "Two roots of the same cell are never adjacent" is **not** proven. It is
false as a consequence of (L1).
- (c^a, d^b) ~ (c^a, d^{−b}) is locally consistent: the neighbour is then both Q_c and P_d.
- Only r ≁ σr is proven (zero diagonal of N and D).
- So e(Z₁₂) = e_P − 10 in J2 stays a live parameter; J2 keeps 10 ≤ e_P ≤ 14.

## 6. J1a (v): a second integer eigenvector from the zero graph (DERIVED, 28/09 evening)
**Setting.**
- Type (v): the triangle p, q, r; the other blocks s, t, u; N = 0, so f = 0 and (A_Z + I)d = 0 on the 54 zeros.
- d = t_v − t_σ. Its values: +2 on M = {m₁₂, m₁₃, m₂₃}, −2 on σM, +1 on the six t=1 zeros U, −1 on σU, and 0 on the
  D-zeros and on the 30 t=0 zeros. So |d|² = 36.

**Step 1: the star part of h₁ has product form.** In (v) every star(c) cell is S-type, so h₁(c^σ, b^τ) = a_b·σ with
Σ_b a_b = 0.
- Proof: balance at b gives 2a_b·[X-type] + 2·net_b = 0, and net ≡ 0 in (v).

**Step 2: the boundary flux B(w) := Σ_{zeros y∼w} d(y) is forced.**
- At S: B(v_k) = 6 and B(σv_k) = −6.
- At star(c): B(g) = 3 + I_σ(g) − I_v(g) for g ∈ G_i. This is λ/μ of g against the six S-vertices.
  - In (v) each triangle inner vertex b^τ is shared by exactly one v and one σv, and never by g's own v_i.
  - So B = 3 on all of A and B = −3 on σA.
- Then |B|² = 12|d|² − |f|² = 432 forces B = 0 at every inner vertex. (This is the known ρ-identity.)

**Step 3: the new eigenvector.**
- On 1⊥ we have P₋₄ = (3I − A)/7, and AD = −D + B. Hence 4D − B ∈ E₋₄. Here 4D − B = 4d + 3h₁|_star − 3h₁|_S.
- Therefore
  **u := (4D − B − 3h₁)/4 = d − (3/2)·h₁|_S**
  is an integer σ-odd (−4)-eigenvector that vanishes on x, the inner vertices and star(c). Its values: −3 on v_k,
  +3 on σv_k, ±2 on M/σM, ±1 on U/σU.
- Label norm 45; ⟨h₁, u⟩ = −18.
- CHECK, pointwise by hand. Au = −4u holds at:
  - v₁: σv₂, σv₃ give 3 + 3; the zeros give 6; total 12;
  - g ∈ A: −3 + 3 = 0;
  - m₁₂: −6 − 2 = −8;
  - u₁: −3 − 1 = −4;
  - δ: −3 + 3 + 0 = 0;
  - the inner vertices: 0.

**Consequences.**
- Balance of u mod 2 at each block: the six U-labels form an Eulerian multigraph on B₀ (every block has even U-degree).
  Correction: this is only the ρ-identity mod 2, so it is not new.
- u vanishes on star(c), so u ∈ Λ_c (integer eigenvectors off star(c); rank ≥ 3 always).
- ⟨h₁, u⟩ has Gram [[24, −18], [−18, 45]], determinant 756, minimum 24. No short vector, so no contradiction yet.

**Type (iii) analogue.**
- There f = ρ·N ≠ 0, with N = e_d − e_g after normalisation. The same projection gives 4D + f − B ∈ E₋₄.
- Then 4e := 4D + f − B − 3h₁ = 4d + (g_d − g_g) − 6h₁|_S lies in E_ℤ, with parity cut{d, g}.
- Equivalently, U' = (ι_d − ι_g) + d − (3/2)h₁|_S is an integer σ-odd eigenvector in the rank-22 space, ±1 at d±, g±.
  CHECK: at v₁, v₂, v₃ and d⁺.

**General principle (for structures' R8 k=1 as well).**
- If the ±2-set W of a J-type vector gives a zero-graph equation (A_Z + I)d = −f with explicit f, then 4D + f − B is an
  integer eigenvector.
- Whenever B is forced pointwise, subtracting a multiple of h gives a new, often divisible, eigenvector supported off
  star(c).

**Invariant subspaces (CHECK, sympy: code/r6/companion_check.py).**
- (v): span(H = h₁|_star, s, D) is A-invariant, with A H = −2H − 4s − 2D, A s = −H − 2s + D and A D = −3H + 6s − D.
  - Spectrum {3, −4, −4}, diagonalisable, with (−4)-plane span(h₁, u).
  - The 3-eigenvector is φ = −H + 2s + D (integer, label norm 42).
  - Glue relation: 7s = h₁ − u + φ.
- (iii): span(H, s, D, G = g_d − g_g, ι = ι_d − ι_g) is A-invariant, with spectrum {3², (−4)³}, diagonalisable. The third
  (−4) vector is D − 3s + ι.
- **All consistent. No contradiction at this level.**

## 7. J1a: structures' PSD/interlacing test (28/09 late evening; joint with structures)
**The test.** For any label set U, M_U := 12I − 4T_UU − R_U R_Uᵀ = 28(P₋₄)_UU is PSD of rank ≤ 15. (The P₃ version,
T + 4I − RRᵀ/3 ⪰ 0, also holds.)

**J1a with positive representatives.** Every support edge is opposite-sign, so T_UU = −G with G ≥ 0 and G·a = 4a (Perron).
Hence M_U = 12I + 4G − RRᵀ.

**Facts (DERIVED, all J1a types).**
- G_star (the star(c) labels) = Q ∪ P, both perfect matchings.
  - Q switches κ (the c-side of the positive representative); P keeps κ.
  - So the label cycles have length ≡ 0 mod 4, and **G_star is bipartite**.
- In (v), κ = a_b.
- Each star label has exactly one V-neighbour. Each V has 4 star labels (2 in B⁺, 2 in B⁻) and the other two V's (a K₃).
- R e_c|_U is a null vector (g_c).

**Two test families (DERIVED).**
1. **Proper colouring.** Take x a proper 2-colouring of G_star and y = −s/2 on the V's (s_k = Σ_{G_k} x). Then
   z^T M z = 48 − 2Σs_k² − |R^T z|². The twisted sum Σ_b a_b(x_{b+} + x_{b−}) is always 0.
   - This kills unless the groups are colour-balanced.
2. **Group-constant.** Take x = α_k on G_k and y = β_k. Then F = 48|α|² + 12|β|² + 4αᵀEα + 32⟨α,β⟩ + 8e₂(β) − |Σα_k R_k + Σβ_k ρ_k|².
   - Here E_kk = 2e_kk and E_kl = e_kl count the G_star edges within and between groups; R_k = Σ_{G_k} r_L.
   - With α = (1, −1, 0) and β = (−2, 2, 0): violation if 8(e₁₂ − e₁₁ − e₂₂) + |R₁ − R₂ − 2(ρ₁ − ρ₂)|² > 32.

**Where the survivors lie.** A configuration with every G_k = two internal G_star edges (e_kk = 2, e_kl = 2) passes both
families. The candidate survivors are there. structures' sampler: the odd test fails on 398/400 (v) samples, and the even
test kills the other 2.

**Next.** Get the survivors from structures, then find a universal certificate or a λ/μ kill of "G_k ⊇ a G_star edge".

**Update 28/09 late night (structures' sampler + C1 checks).**
- **Sampled survivors.** 13 sampled (v) configurations survive the odd test. They are in
  conway99-rank17/r8_data/j1a_v_odd_survivors.json.
  - The sampler does not impose the pair design, so these are a superset of the true survivors.
  - All 13 die on the even test, 6I − 2G − |R||R|ᵀ + J ⪰ 0 (D_UU = 0 in J1a). Even minima lie in [−1.85, −0.08].
  - C1 reproduced both minima exactly, with positive representatives r_L = a_L(e_c ± e_K).
- **Pattern.** Odd-survivors have high internal group connectivity: e_kk ∈ {2, 3, 4} for every k.
  - The odd test kills cross-dominated configurations: with α = (1,−1,0) and β = (−2,2,0), it violates if
    8(e_kl − e_kk − e_ll) + |R_k − R_l − 2(ρ_k − ρ_l)|² > 32.
  - The even test kills internally dominated ones: with α = β = (1,−1,0), it violates if
    4(e_kk + e_ll − e_kl) + |m_k − m_l + |ρ_k| − |ρ_l||² > 32.
  - Group-constant compression (6-dim): the odd form is PSD on all 13. The even form is negative on 11/13; on the other 2 it
    is exactly 0, and the full test kills them.
- **The G-free combination** 2·even + odd = 36I + 2J − 2|R||R|ᵀ − RRᵀ is PSD in every a-case (min eigenvalue ≈ 18.5).
  So there is no trivial kill.
- **Structural null vectors.** The odd form has κ = R e_c. In case (I) the even form has n₀ = e − 2.5a, where
  e = (Uu − G)a = (−1 on triangle-star labels, +1 on the other star labels, +1 on the V's).
- **Methodological status.** A complete kill of (v) by PSD seems to need optimised vectors per configuration. The margins can
  be as small as −0.08. Without a universal structural certificate, closing (v) this way means an exhaustive exact check
  over configurations, which the user must authorise (solvers and enumeration are banned). Scripts (code/r6/):
  j1av_psd_one.py, j1av_trace.py, groupquot.py, gfree.py.
