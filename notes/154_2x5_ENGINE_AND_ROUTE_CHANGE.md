# 154 — 2|5 cut engine (J2, R5): measurements, and the route change to per-class witness filters (28/09 ~19:00, C1)

## 1. What was built (code/r6/j2/)
- **Patterns and symmetry.** j2_patterns.py, j2_orbits.py and gen_sym.py.
  - J2 has 344 sign patterns in 6 orbits. The stabilisers fixing star(0) have 4–24 elements.
  - R5 has 712 patterns in 4 orbits: SSXSS ×2, SXXXS and XXXXX. The stabilisers are big: 48–480 permutations of star(0).
- **Star level.** star0_count.c counts the survivors of Q0, Π0 and P_σ∩star(0) under the tests (all necessary conditions).
  - Profile table (notes/151 §2ter).
  - **F-test (new):** q = α^T A0^+ α ≤ |a|²/28. It holds because F = Σ a_L f_L has |F|² = 28|a|² and ⟨F, f_L⟩ = 28 a_L, so
    |proj_{span f_star0} F|² = 784 q ≤ |F|². The bound is 6/7 for J2 and 5/7 for R5.
  - λ/μ of v and σv on star(0).
  - odd V-test: Gram{star0, V, F} PSD.
  - even V-test: component kernels of Q∪Π∪S, and residual ≥ 0.
  - P3 / P3+ tests.
- **Facts used.**
  - The star Gram A_c = 11I + S − J + 4(Π − Q) (c-reps) is ALWAYS PSD of rank exactly 11, with kernel 1. On 1^⊥ it is at least
    11 − 1 − 8 = 2. So the star alone never kills.
  - Each star's residual space (E_c = eigenvectors vanishing on star(c)) is 4-dimensional.
  - Pair design: the 60 roots outside star(c) are in bijection with the 60 non-Q_c pairs of O_{c+}, through their O_{c+}
    incidence pair. This is μ = 2 with the common neighbour c+. From the viewpoint of base vertex c+, it is just its own D₇
    root structure.
  - Mixed-pair capacities come from λ/μ of (r, −r'): 2 − [same cell] − [star(c) common nbrs], or 1 − [inner apex] for a
    Π_c edge, or 2·[D-partner outside] for r' = r.
- **Search.** j2_engine.c; mode V=1 for J2, V=0 for R5.
  - Base: star(0) + P_σ∩star(0).
  - Unknowns: each cut1 label's column (2+2 root incidences into star(0)), its P_σ status, and the star(1) relations.
  - Pruning:
    - residual Gram of F, V and the cut1 labels over span f_star0: rank ≤ 4 tested EXACTLY mod p = 2^31−1 (rank mod p ≤ rank
      over Q), plus PSD in floating point with a robust margin;
    - pair design, mixed capacities, cut0 C/B budgets, Z-root star(1) slots, star(1) partner slots and types, σ_own targets,
      P_σ∩star(1) = 2+2, λ/μ (cut1–cut1, v/σv).

## 2. Measurements (orbit 0 of J2)
- **Star level, J2 orbit 0.** 1.08e8 (Q0,Π0) → 1.14e7 after the F-test → 3.6e7 (S0, P_σ) after all star tests. That is about
  2.2e6 up to symmetry. The other 5 orbits give 1.9e7–7.5e7 (count_*.out).
- **Columns per cut1 label** (col_census*.c): median 60–100, product about 1e17 per S0.
- **Search, J2.** Mean 1.3 s per (S0, P_σ), about 15k nodes, 0 survivors in the samples.
  - The anchors F and V fix 2 of the 4 residual dimensions. Two more labels complete the basis, so the cost is ~N² nodes with an
    ~N scan each.
  - Total ≈ 3e6 s per orbit: **not feasible as is**. It needs about 100× (better per-node code gives ~10×).
- **Search, R5.** Only F is an anchor, so the depth-3 branching is ~N³ per S0. A first sample did not finish in 10 min:
  **not feasible**.
- **Where this engine IS efficient:** cells with ≥ 3 anchors. R8 k=2 (F + three ±2 labels) spans the 4-dim residual space at
  once, so each candidate column is an O(1) exact test. R8 k=3 has F + two ±2 labels.

## 3. Route change (with structures, 28/09 ~19:00)
- structures: R8 k=1 support enumeration is ~1e12 leaves. Of the 754 classes, 199 have no n=6 witness; 96 of those have an n=5
  witness; 83 are min-8 A11E6p classes.
- **Per-class witness filter (structures' idea; C1 checked the logic).** For every short κ ∈ K* (7|κ|² = n), a_u = (κ, w_u) is
  an integer eigenvector whose cut is fixed by the skeleton, through the parities (κ, g_c). Its values per label are forced:
  - n=5: ±1 on the 20 labels of a 2|5 cut, 0 on the other 22. This uses min N*, row capacity and PE.
  - n=6: k ∈ {2,3} since J0, J1a, J1b are closed. k=3 gives 24 ±1 and 18 zeros; k=2 gives 20 ±1 and one ±2.
  - n=8: k=0 is dead; non-cut labels are in {0,±2} with 5/3/2 of them at ±2; ±3 dies by row capacity.
  - Every frame vector candidate w_u ∈ K must satisfy these values for EVERY witness. On A11E6p:12 this removes about 20% of
    the norm-10 vectors per label; for n=5 classes the effect is far larger (22 labels orthogonal to κ).
- **Decision.** The per-class, witness-filtered frame search (structures, wfe.c) becomes the main route. It bypasses the general
  R5/R6/R8 theorems. It is validated first on the engine-excluded classes. Order: the 412 classes with an n=5 witness, then n=6
  with k=3, then min-8.
- C1's 2|5 engine stays as the tool for the anchored cells: R8 k=2 and k=3, and J2 if it is made 100× faster.
