# 153: the four "cut" cells (J2, J3, R8 k=2, R8 k=3). Design of an exhaustive engine (28/09 evening, C1)

**Where we are.**
- R6/J1a is closed (notes/152). R8 k=1 is structures' enumerator, in progress.
- The finish line R6 ∧ R8 now needs four cut cells:
  - 2|5 cut (support = the 20 cut labels of star(c) ∪ star(c′), plus ±2 labels): J2 (one ±2) and R8 k=2 (three ±2);
  - 3|4 cut (24 cut labels): J3 (no ±2) and R8 k=3 (two ±2).

## 1. Why the J1a engine does not transfer directly
- In J1a the support was ONE star plus hubs. Every star label's row inside U was just its two star partners (the Q and P
  matchings), so (a, groups, Q, P) parametrised the whole support Gram. That is 2.7e9 cases.
- In a cut cell, labels of different stars can be adjacent:
  - through a third star (partners in star(x) when the cells share x), or
  - as far neighbours (disjoint cells).
  These cross entries are essentially free. Naively, star(c)'s matchings (~1e8) times the cross block C0 × C1 (10 × 10,
  about 4 non-zeros per row) is at least 1e14 for J2, and worse for J3.

## 2. What we have that is much stronger than before
- **Rank.** The support Gram M_U = 12I − 4T_UU − R_U R_Uᵀ must be PSD of rank ≤ 15 (nullity ≥ 6 for J2, ≥ 9 for J3), with
  eigenvalue 28 on h. The σ-even analogue 6I − 2(|T| + 2D) − |R||R|ᵀ + J must be PSD.
- **CHECK:** structures' CP-SAT two-star relaxation solution for n=5 (n5_local_solution.json, found before the ban) FAILS the
  odd test: λ_min = −7.22, rank 18 > 15. The spectral tests are far stronger than the old local relaxations.
- **Shell completion (notes/152).** Once a seed Gram is known and rank-deficient, every other row must be EXACTLY orthogonal
  to its kernel. A shell label's row to a single star has only 2 + 2 non-zeros (L0), so it has few options, like the m's.
- **Two seeds with known internal structure.** For seeds star(i) and star(i′) whose internal matchings are fixed, the cross
  block X must satisfy:
  - columns ⊥ ker(A₁) and rows ⊥ ker(A₂), exactly;
  - A₂ − XᵀA₁⁺X ⪰ 0 of rank ≤ 15 − rank A₁ (typically ≤ 4). This is a clean test with no unknowns once the rows are chosen.

## 3. Candidate designs
- **(D1) Star-pair engine.**
  - Enumerate the single-star structures (Q, P and h-values), modulo symmetry, keeping those that pass the star-level PSD
    test.
  - For each pair of stars, search the cross block row by row (each row = 2+2 choices), pruning with exact (K) and with the
    residual rank bound ≤ 4 (hereditary).
  - Cost is dominated by the number of star structures squared. It needs a reduction of the single-star structures first,
    from the h-pattern and the (L0)/profile rules.
- **(D2) Common-neighbour classification.** This is the style of structures' R8 k=0 proof.
  - Let C be the same-sign adjacency of the positive cut roots and B the opposite-sign one.
  - Exact identities: (C² + B²)_{ij} + E_{ij} = 1 + [C_ij = 0] and (CB + BC)_{ij} + F_{ij} = 1 + [B_ij = 0], with E, F ≥ 0.
    So any two positive roots have ≤ 2 common support neighbours, and ≤ 1 when adjacent.
  - J3 profile: row sums d ≤ 3 and d + 4. J2 profile: P₀ has d ≤ 1, P_σ has d ≤ 2, e_P ∈ {10, 12, 14}.
  - Then add the PSD/rank tests. The goal is to classify (C, B) by hand-guided search, as B² = 2I + 2J − E was used for k=0.
- **(D3) Frame construction.** Grow the 42 frame vectors in R¹⁵ label by label. Once 15 are independent, each new label is
  determined by its inner products with a basis, i.e. by finitely many T-choices. Very strong late in the search, but the
  seed stage is the bottleneck (same issue as D1).

## 4. Plan
- J2 first: it is sparser (each cut root has ≤ 6 support neighbours).
  - Derive the single-star reductions by hand, then build D1 with the D2 identities as pruning.
  - R8 k=2 is the same engine with three ±2 labels, to hand to structures.
- Then the 3|4 engine for J3 and R8 k=3.
