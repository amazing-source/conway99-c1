# 175 — Is every srg(243,22,1,2) with a regular spread symmetric? (S₃ question, 12/10, night) — OPEN

*Continuation of note 165 §6. Code: `code/asym243/s3grid/`.*

## 0. The question
A srg(243,22,1,2) with a regular spread (81 triangles, partition equitable) is a 3-fold cover of Brouwer–Haemers
BH = srg(81,20,1,6), with S₃ gains g_e on the 810 edges (note 165). Either:
- (a) the gains can be gauged into A₃, i.e. a Z₃-cover. The graph then has a fixed-point-free automorphism of order 3
  (BvLS, the twin, Γ₃, Γ₄);
- (b) the monodromy is all of S₃, i.e. an "S₃-cover", and its graphs would generically be **asymmetric**.

**Goal:** exclude (b), which would give the theorem "any asymmetric srg(243,22,1,2) has no regular spread". Alternatively,
find a (b) cover.

## 1. Exact reformulations (proved here)
1. **Full model ⇔ spectrum.** Let 𝒜 = I⊗(J₃ − I₃) + Σ_e E_e ⊗ Perm(g_e), and split C³ = triv ⊕ std.
   - The triv part is 2I + A_BH, which automatically has spectrum {22, 4, −5}.
   - The std part is −I + A_ρ, where A_ρ is the 162×162 matrix of 2×2 blocks ρ(g_e). It must have spectrum {4, −5}.

   So **srg ⇔ A_ρ² = A_ρ + 20I** (multiplicities 72 and 90). Locally this means:
   - triangle holonomy is trivial;
   - for each non-adjacent pair, the 6 path products g_ZR∘g_PZ have Σ Perm = 2J. Brute force over all multisets of size 6
     leaves exactly **3 multisets**: S₃ once each; A₃ twice each; the 3 reflections twice each.
2. **Grid formulation of the parity skeleton.** Take a non-adjacent pair (P,R) of BH.
   - Its 6 common neighbours form 3 pairs, one per 3×3 grid P + ⟨v,w⟩ through P and R.
   - With ε = sign(g), "weight of the 6 path parities ∈ {0,3,6}" holds iff the number of **odd grid squares** with
     diagonal (P,R) is 0, 1 or 3, **never 2**, plus two compatibility conditions on the twisted quadrangles.
   - Checked on all 64 bit patterns (`s3grid.py`, `unit_test`).
   - In each grid, the odd squares form a 3×3 F₂ matrix with zero row and column sums: 0, a rectangle, or a 6-set
     (16 patterns, dim 4).
3. **Ternary-code formulation.** Let A_ε be the signed adjacency of BH. Then:

   **parity skeleton ⇔ A_ε triangle-balanced and (A_ε + I)² ≡ 0 (mod 3).**

   Equivalently, the 81 signed closed neighbourhoods are pairwise orthogonal mod 3: they span a self-orthogonal ternary
   code of length 81.
   - For BH itself (ε = 0), (A + I)² ≡ 0 and rank₃(A + I) = **19**: a self-orthogonal [81,19] code.
   - A random balanced signing fails (3,130 nonzero entries mod 3).
   - Mod 3, ρ is uniserial (triv ⊂ W ⊂ F₃³, with factors triv, sign, triv). This explains why the sign layer only sees
     (A_ε + I)² ≡ 0.

   **(b) exists ⇒ BH has a non-trivial (not switching-equivalent) signing with a self-orthogonal signed-neighbourhood
   code.**

## 2. Computations (all with positive controls)
| model | instance | result |
|---|---|---|
| full S₃ (99,630 vars, 987k clauses) | **control** (no constraint) | **SAT in 465 s** → decoded: srg(243,22,1,2) checked, all gains even, \|Aut\| = 864, 3 orbits (= Γ₃) |
| full S₃ | pair (0,R₀) of type "S₃ once each" | UNKNOWN, 1,436 s |
| full S₃ + type-S assignment at (0,R₀) | 20 classes up to conjugation; classes 00–03 run | UNKNOWN, 4 × ~1,185 s |
| parity, grid form (CryptoMiniSat, native XOR) | 4 WLOG cases A, B1, B2, B3 | UNKNOWN, 4 × ~1,520 s |
| parity, crash-proof cubes (5 min each) | 18 SPLIT, 0 UNSAT, 5,488 s | stopped: the tree only grows |

Nothing is decided: **no UNSAT is claimed.** Classes 04–19 have not been run.

## 3. Status and next idea
- **OPEN:** existence of an S₃-cover of BH. If none exists, every srg(243,22,1,2) with a regular spread has an
  automorphism of order 3.
- Brute force does not converge in a container that restarts. The ternary-code formulation (§1.3) is the most promising
  lead for a proof:
  - BH's code is a self-orthogonal [81,19]. A non-trivial signing would need another self-orthogonal code, of dimension
    ≤ 40, spanned by the signed neighbourhoods. Mod 3, these are signed sums of the 10 lines through each point.
  - What remains is to show that self-orthogonality forces balance, e.g. via the structure of the ternary code of the
    ovoid ([10,4] two-weight code, whose coset graph is BH).
- Literature: Makhnev, Guo and Paduchikh (Mat. Zametki 86, 2009) study the antipodal distance-regular covers of
  srg(81,20,1,6). That is a different question, which does not settle ours.
