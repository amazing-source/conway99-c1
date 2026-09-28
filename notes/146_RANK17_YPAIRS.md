# 146 — Rank-17 switch: y-pair types in the 8 non-Z¹⁷ lattices V (27/09 night, C1)

Context: GPT-Pro handoff `RANK17_HANDOFF.md` (repo conway99-rank17, d8906ea). The switch was re-derived independently by
structures and by C2:
- U′ = U_H + ⊕ℤ(h_c/2) = ℤ⁷ ⊥ V, with V unimodular of rank 17 (9 types);
- y₁, y₂ ∈ V;
- the 42 w_u lie in K = V ∩ y^⊥, which has rank 15 and det 49.

Lanes: structures owns the search in K. C2 builds a second implementation of V = ℤ¹⁷ (8 y-pair types, handoff Cor. 6.2).
**C1 (this note) classifies the y-pairs of the other 8 V types.**

## Statement classified (necessary conditions only, nothing is excluded here)
- A y-pair is y₁, y₂ ∈ V of norm 7 with (y₁, y₂) = 0.
- Unit bound: for every unit vector e of V, Y(e) = (y₁,e)² + (y₂,e)² ≤ 4. This comes from (PE) with k(e) ≥ 1, which needs
  min U ≥ 2, i.e. the route-(C) envelope.
- The flag `rootless_U_allowed` marks the pairs with Y(e) ≤ 2 for every unit e (the min U ≥ 3 case, handoff Cor. 6.3).
- ⟨y₁, y₂⟩ is automatically primitive (handoff Prop. 4.1).
- Equivalence: Aut(V) × (independent signs of y₁, y₂) × (swap y₁ ↔ y₂).

## Lattices (code/rank17_cores.py, all checked: integral, det 1, root count, no unit vector in the core)
| V | core rank | units m | roots | glue |
|---|---|---|---|---|
| E8 + ℤ⁹ | 8 | 9 | 240 | — |
| D12⁺ + ℤ⁵ | 12 | 5 | 264 | (½)¹² |
| E7²⁺ + ℤ³ | 14 | 3 | 252 | ([1],[1]) |
| A15⁺ + ℤ² | 15 | 2 | 240 | [4] |
| E8² + ℤ | 16 | 1 | 480 | — |
| D16⁺ + ℤ | 16 | 1 | 480 | (½)¹⁶ |
| D8²⁺ + ℤ | 16 | 1 | 224 | (s,v), (v,s) |
| A11E6⁺ | 17 | 0 | 204 | ([2],[1]) |

## Method (code/rank17_ypairs.py)
**Group.** Aut(V) = Aut(core) × (signed permutations of ℤᵐ). The units of V are exactly the ±e_j, since the cores have none.
Aut(core) = W ⋊ Γ, where:
- Γ = 1 for E8, D12⁺, D16⁺;
- Γ = {1, −w₀} for A15⁺ and A11E6⁺, already covered by the global sign because −1 ∈ Aut(V);
- Γ = {1, swap} for E8², E7²⁺, D8²⁺.

**Enumeration.** All core vectors of norm ≤ 7 (both signs), and all z ∈ ℤᵐ with |z_j| ≤ 2. Then:
- y₁ = (dominant core part, sorted |z| profile);
- y₂ runs over the core vectors with the right norm and inner product, kept W_J-dominant, where W_J = Stab_W(c₁) is generated
  by the simple roots orthogonal to c₁;
- the ℤᵐ part is taken up to Stab(z₁).

**Canonical key.**
- Core part: reflect until c₁ is dominant, then reflect in J until c₂ is J-dominant. This is unique per W-orbit of pairs.
- Minimum over Γ (swap), then the ℤᵐ columns (z₁_j, z₂_j) up to simultaneous sign, sorted.
- Minimum over the 8 sign/swap variants.

**Checks.**
- Every representative is re-verified exactly: norms 7 and 7, inner product 0.
- The pure-ℤ⁹ slice of E8 + ℤ⁹ gives exactly the 4 hand-counted types: A–A overlap 6, A–B overlap 2, B–B overlap 0 and 2.
- Two runs with different enumerators give the same class sets (canonical keys) on the 7 finished lattices, with no duplicate
  class within a run.

## Results (data/rank17/ypairs_*.json)
| V | y-pair types | with Y(e) ≤ 2 (rootless U) | y₁ types |
|---|---|---|---|
| E8 + ℤ⁹ | 53 | 34 | 6 |
| D12⁺ + ℤ⁵ | 158 | 122 | 11 |
| E7²⁺ + ℤ³ | 191 | 161 | 17 |
| A15⁺ + ℤ² | 203 | 179 | 18 |
| E8² + ℤ | 12 | 12 | 4 |
| D16⁺ + ℤ | 18 | 18 | 3 |
| D8²⁺ + ℤ | 319 | 302 | 20 |
| A11E6⁺ | 310 | 310 (no units) | 18 |

With ℤ¹⁷ (8), the whole rank-17 search has 1272 (V, y-pair) starting points (1142 when U is rootless: 1138 + the 4 of Z17), against ~10⁷ root-poor pairs
in route (C). Each starting point then needs the rank-15 search (structures' lane): 21 pairs (a, b) with norms (5,5)/(3,7),
7 star equations, Σ(aaᵀ + bbᵀ) = 14 P_W.

## Pass 1 (28/09 night, C2's policy: labels PROVEN / COMPUTED / PATTERN)

**Engine** (`code/rank17_skeleton.py`, `code/rank17_engine.py`, with structures' compiled solver
`conway99-rank17/z17/sbdfs_g.exe`):
1. **Classes.** Take the norm-10 vectors of K by class in K/2K. **L1** (structures): drop w ≡ r mod 4V for any root r of V.
   A class is usable when it contains w, w′ (w′ ≠ ±w) with (w,w′) ∈ {0,±4}.
2. **Skeleton.** The skeleton is g₂..g₇ (g_d = [w_1d]), because ρ: E₇ → K/2K is linear, injective and form-preserving (handoff
   Prop. 5.1, re-checked). The search requires, in this order:
   - pairwise odd classes, independent;
   - all 21 classes usable;
   - **κ ∈ K*** with |κ|² ≤ 5/7 (norms lie in (1/7)ℤ). Parity energy then gives k(p(κ)) = min(o, z+1) ≤ kmax.
     kmax is 0/1/2 for |κ|² ≤ 2/7 / ≤ 4/7 / = 5/7;
   - **unit rule** o ≥ 1 for every unit of V (min U ≥ 2);
   - **M1** (structures): the half a = (w+w′)/2 of each cell has the parity pattern of one endpoint.
3. **Vector level.** Per skeleton, the SPEC_ENGINE §1 domains (M1 orientation, refined L1, sign normalisation) go to
   sbdfs_g, which checks the pairwise rule (w_X,w_Y) = 4(u,v) − r_X·r_Y, star closures and PSD pruning.
4. **Symmetry.** H = ⟨reflections in the roots of K⟩ fixes y₁ and y₂. The smallest skeleton element is taken as the minimum
   of its H-orbit, and classes are ordered by (orbit, class).
5. **Two modes.**
   - Exhaustive (E/D types, rare skeletons).
   - 30 random skeletons, randomised DFS order (A types, abundant skeletons).

**Checks.**
- Bitset DFS against the numpy DFS: the same node count (394,793) on E8²+ℤ #0.
- The cached vectorised domains equal the loop implementation as sets (3 skeletons).

**Results so far.**
- **E8² + ℤ #0, #1:** EXCLUDED, COMPUTED. There is no skeleton; the skeleton search is exhaustive.
- **A11E6⁺ #0:** PATTERN.
  - All 8255 classes are usable, and there are ≥ 200k skeletons.
  - Every tested skeleton (30 random, plus 100+ in DFS order) is EXCLUDED at vector level, always INSIDE STAR 1: depth
    profiles like [1,120,3564,8064,0,…].
  - Node counts repeat across skeletons, so those skeletons are symmetric copies.

**Scale (for pass 2).** For the abundant types (A11E6⁺, A15⁺, and C2's D12⁺/E8⊕ℤ⁹), exhaustion is not feasible as built:
- per skeleton, ~0.5 s × ≥ 10⁶ skeletons per y-pair;
- the global star-1 search (`code/rank17_star1.py`, kept as a tool) finds ~300k shell vectors still compatible after cell
  (1,2), i.e. ~3M candidate cell pairs per first cell, over 1,319 first cells.

Pass 2 there needs one of:
- (a) skeleton canonical forms under the full Aut(V, y), where the orbits may be few;
- (b) a star-1 lemma.

**Star-1 facts** (orient (u,h₁) = +1):
- **the 12 u's of star(1):** norm 3, pairwise (u,u′) ∈ {0,±1}, Σu = 3h₁, so every row of their Gram sums to 3. Each u has
  exactly 10 non-orthogonal u's among all 42.
- **in K:** the 12 w's have cross products in {−5,−1,3}, in-cell products in {0,±4}, and Σw = 0.
- **M1 is automatic on star-1 cells:** (a_1d, w_1e) = (x+y)/2 is odd and (b_1d, w_1e) = (x−y)/2 is even, for x, y ∈ {−5,−1,3}.
- **The whole u-Gram:** A = G_uu − 3I satisfies A² − A = 12I − R, with R = (r_u·r_v) the fixed D₇ pattern. So each row of A
  has 10 non-zero entries: a lattice-free combinatorial core, the Q-equation.
