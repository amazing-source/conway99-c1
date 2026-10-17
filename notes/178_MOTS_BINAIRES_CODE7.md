# 178 — Binary words of the F₇-kernel of A + 4I (ChatGPT dossier C1_CODE7_MOTS_BINAIRES), audit and overlaps (12/10)

## 1. Theorem (ChatGPT; proof checked by hand here, using only the srg equations)
Let T = A + 4I for a srg(99,14,1,2). Then T𝟏 = 18𝟏 and T² = 7T + 2J.

**For x ∈ {0,1}⁹⁹ with Tx ≡ 0 (mod 7), the weight w is 0, 63 or 77:**
- **w = 63:** S = supp x induces a 10-regular graph, and every vertex outside has 7 neighbours in S. Equivalently,
  Ax = 3x + 7𝟏: an equitable partition (63, 36) with quotient [[10,4],[7,7]]. The complement H satisfies
  A𝟏_H = 3·𝟏_H + 4·𝟏.
- **w = 77:** the complement is a **Hoffman coclique of size 22**. Conversely, α = 22 ⇔ there is a binary word of weight
  77 in ker₇(T). This direction uses only regularity and positivity.

**Proof** (two moments, checked line by line). Write w = 7t, and let d(v) be the number of neighbours in S. Then
d ∈ {3, 10} on S and d ∈ {0, 7, 14} outside S.
- The first moment gives u + v₇ + 2v₁₄ = 11t.
- The second moment, Σd² = xᵀA²x, gives 2u + v₇ + 4v₁₄ = 2t².
- Hence v₇ = 2t(11 − t) and u + 2v₁₄ = t(2t − 11). Together with v₇ ≤ 99 − 7t this forces t ∈ {9, 10, 11}:
  - t = 10 is impossible (88 < 90);
  - t = 9 and t = 11 are saturated cases.

If both exist, |S ∩ C| = 14, by orthogonality of the eigenvectors 𝟏_S − (7/11)𝟏 and 𝟏_C − (2/9)𝟏. Not claimed: the
existence of a non-zero binary word, any bound on non-binary words, K7, α = 22. Also proved:
dim(code of differences) = rank₇(T) − 1 ≤ 44.

## 2. Corrections to the report "Asymétrie des graphes fortement réguliers" (ChatGPT audit, checked)
- **All three** new srg(243,22,1,2) are non-vertex-transitive. Their orbits are [3,60,180], [27,108,108] and [81,162];
  Γ₄ is non-transitive even though 243 divides 3888.
- Non-uniqueness does not refute a "forced symmetry" (many non-isomorphic Cayley graphs can share parameters).
- Dvořák–Dell–Grohe–Rattan is about **homomorphism** counts, not induced counts. Example: the 4×4 rook graph and the
  Shrikhande graph have 36 vs 12 induced C₄ but the same hom(C₄) = 1536.
- **Piste 3 of the report** (LP on Reimbayev's order-7 counts, "to launch first") **is already done in the repo**: notes
  60 and 90 with `code/reimbayev7.py`. Non-negativity gives only 0 ≤ n₃ ≤ 4158 and 2n₃ ≤ z₁₁ ≤ 4n₃: "counting up to
  order 7 does not bound the torsion". This piste is obsolete.

## 3. Overlaps of notes 176–177 with older notes (my oversight)
- π_a (note 176) = **τ_a** (notes 30, 90).
- The opposite-corner map τ = **point reflection σ_x** (note 90, Bondarenko–Radchenko). Note 90 already states that in
  C1 no σ_x is an automorphism.
- The identity t₂ = (m−1)E − 3t₃ (note 177 §2) is the identity **n₃ = 3(P_max − P)** of note 60 / L15. Note 177 gives
  another proof (via B_xa), not a new result.
- Lou–Murin (2014, note 60): around a line L, the 36 outside neighbours form a 2-factor whose cycle lengths are multiples
  of 3, whose triangles are the prisms. This is close to B_xa (note 177): the per-edge version of the same structure.

What notes 176–177 add without duplicates, as far as I can tell:
- the 2-factor F_x of Δ_x and its data (number of 4-cycles = number of grids);
- B_xa as a 2-regular bipartite graph and the distribution of its types on the five known graphs;
- the conjectures (G), (E), (L), (P) and the failure of the local tools (signs, Euclidean, SAT by type).
