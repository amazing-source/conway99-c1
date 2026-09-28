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

## 3. Next
- J1a: push the rigid structure to a contradiction or to an explicit local model. A model would have to be tested against BvLS
  and Paley 9: supports on at most 4 stars exist at m = 11 (dimension 4).
- J2: the 2|5 cut plus one ±2. Redo notes/150's class analysis with the modified balance.
- J3: class-by-class, class 0 (product) first.
