# 176 — The 2-factor F_x of the second subconstituent: a purely combinatorial invariant (12/10)

*Goal (Dilan): look for a clean combinatorial argument, without solvers or lattices. Here the computer is a microscope
for formulating lemmas that are then to be proved by hand. Code: `code/fx/` (`fx_cycles.py`, `fx_detail.py`,
`fx_checks.py`).*

## 1. Definition (proved, elementary)
Let Γ = srg(v,k,1,2), k = 2m, and x a vertex. N(x) = m mate pairs (the triangles through x). Δ_x = vertices at distance 2,
in bijection with the non-adjacent pairs {a,b} ⊂ N(x) taken from two different triangles: z_ab.
|Δ_x| = 2m(m−1), which gives 84 at 99, 220 at 243 and 4 at 9.

For z = z_ab, the **special neighbour via a** is the third vertex s_a(z) of the unique triangle on the edge z–a. It lies
in Δ_x, it equals z_{a,π_a(b)} for a perfect matching π_a of N(x)∖{a,a′}, and s_a(s_a(z)) = z.

The two special neighbours of z are distinct: a common one would be a third common neighbour of a and b. Hence the
special edges form a **2-factor F_x of Δ_x**, i.e. a disjoint union of cycles. The other Δ_x-edges form
|Δ_x|(k−4)/6 triangles, 140 at 99. A cycle of F_x is a cyclic sequence (a_i) of N(x) with a_{i+1} = π_{a_i}(a_{i−1}).

A quadruple Q_ef that forms a 3×3 grid through x gives a 4-cycle (a, b, a′, b′) of F_x.

## 2. Data (computed: Paley(9), BvLS, twin, Γ₃, Γ₄)
| graph | cycles of F_x (number of vertices x) |
|---|---|
| Paley(9) | 1×4 (9) |
| BvLS | 55×4 (243) |
| twin | 13×4 + 6×8 + 4×30 (180); 19×4 + 12×12 (60); 55×4 (3) |
| Γ₃ | 23×4 + 4×16 + 2×32 (108); 23×4 + 8×16 (108); 23×4 + 16×8 (27) |
| Γ₄ | 31×4 + 6×16 (162); 31×4 + 12×8 (81) |

Local structure of π_a against the mate matching on N(x)∖{a,a′}. Their union consists of alternating cycles carrying ℓ
mate pairs each. Observed: ℓ ∈ {1, 3, 4, 6} only. Types per (x,a):
- BvLS: 1¹⁰;
- twin: 1²4², 1·3³, 1¹⁰;
- Γ₃: 1⁴3², 1⁴6, 1¹⁰, 1⁶4, 1²4²;
- Γ₄: 1⁶4, 1¹⁰, 1⁴6, 1⁴3².

## 3. Observed regularities (CONJECTURES to prove by hand; NOT proved)
- **(G)** the 4-cycles of F_x are exactly the grid quadruples. Observed: number of 4-cycles = number of 3×3 grids
  through x (13, 19, 55; 23; 31) on all 5 graphs.
- **(E)** every cycle of F_x has even length. Observed: 4, 8, 12, 16, 30, 32. In particular there is no length 6, and
  the shortest non-grid cycle has length 8.
- **(L)** in π_a ∪ M, no alternating cycle carries ℓ = 2 (an "alternating square") or ℓ = 5 mate pairs.
- Refuted: "Σ_x (non-grid part of Δ_x) = 2·n₃". It holds for the twin (38,880 = 2·19,440) but fails for Γ₃
  (31,104 vs 2·14,256) and Γ₄ (23,328 vs 2·9,720).

**Caveat:** the four 243-vertex graphs all come from the **same construction** (3-fold covers of Brouwer–Haemers).
Regularities common to these five graphs may be artefacts of that construction. Only a proof counts.

## 4. Why this is relevant at 99
- At 99, |Δ_x| = 84 = 4·g_x + (lengths of the non-grid cycles), and π_a ∪ M lives on 6 mate pairs. Makhnev 1988 and
  Keramatipour: "all grid" is impossible, so some F_x has long cycles.
- With (L), the local types at 99 would be restricted to ℓ-partitions of 6 avoiding 2 and 5: 1⁶, 1³3, 3², 1²4 and 6.
- The plan is to prove (G), (E) and (L), or their correct versions, by local double counting with λ = 1 and μ = 2, then
  look for a counting or parity incompatibility specific to m = 7, the analogue of the "21 = 21" tightness of K₇.
  Each lemma must hold on the 5 known graphs (non-regression test).
