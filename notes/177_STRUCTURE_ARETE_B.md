# 177 — The edge structure B_xa of the srg(v,k,1,2) (12/10) — PROVED (§1–2), observed (§3)

*Continuation of note 176, toward a purely combinatorial argument. Code: `code/fx/fx_edges.py`.*

## 1. Lemma (proved, elementary)
Let Γ be a graph with λ = 1 and μ = 2 (every pair at distance 2 has exactly 2 common neighbours), k = 2m, xa an edge,
and T₀ = {x, a, a′} its triangle.
- **Bijection.** Every u ∈ N(x)∖T₀ has **exactly one** neighbour in N(a)∖T₀, namely z_au. Indeed u ≁ a, so u and a
  have exactly 2 common neighbours: x and z_au. Symmetrically, every w ∈ N(a)∖T₀ has exactly one neighbour in N(x)∖T₀.
  Hence u ↦ z_au is a bijection N(x)∖T₀ → N(a)∖T₀.
- **The graph B_xa.** Let 𝒯_x (resp. 𝒯_a) be the m−1 triangles through x (resp. a) other than T₀. Join tri(u) to
  tri(z_au) for every u.

  Each triangle has 2 vertices besides x (resp. a), so **B_xa is a 2-regular bipartite multigraph on (m−1) + (m−1)
  vertices**, i.e. a disjoint union of cycles, each meeting ℓ triangles on each side, with Σℓ = m − 1.
- **Interpretation.**
  - ℓ = 1 (double edge) ⟺ T ∈ 𝒯_x and T′ ∈ 𝒯_a are joined by 3 edges (including xa): a **prism**.
  - A single edge ⟺ a pair of triangles joined by **exactly 2 edges**, xa and one other: a **twisted pair**.
- **Symmetry.** B_ax is the same graph read from the other end (verified on every edge of the 5 known graphs).
- **Link with note 176.** The cycles of B_xa are the alternating cycles of π_a ∪ M_x. The special edges of F_x via a
  are the **far edges** of the triangles of 𝒯_a: F_x is the union of the far edges of the m(m−1) triangles meeting
  N(x) in exactly one point.

## 2. Counting identities (proved)
Let d(e) be the number of double edges of B_e, t₃ the number of prisms, t₂ the number of twisted pairs, E = vk/2.
- Each prism has 3 matching edges, and each sees it as a double edge: **Σ_e d(e) = 3t₃**.
- Each twisted pair has 2 joining edges, and each sees it as a single edge: Σ_e (2(m−1) − 2d(e)) = 2t₂. Hence
  **t₂ = (m−1)E − 3t₃**.

  At 99: t₂ = 4158 − 3t₃, which recovers Makhnev's / Reimbayev's identity ("n₃ = 4158 − 3P") with a transparent proof.

Verified exactly on the 5 graphs:

| graph | t₃ | t₂ |
|---|---|---|
| BvLS | 8,910 | 0 |
| twin | 2,430 | 19,440 |
| Γ₃ | 4,158 | 14,256 |
| Γ₄ | 5,670 | 9,720 |

## 3. Observations (CONJECTURES, all data from the BH-cover family)
Types of B_e (multiset of ℓ, Σℓ = 10 at 243):
- BvLS: 1¹⁰ on all 2,673 edges;
- twin: 1²4² (1,620), 1·3³ (720), 1¹⁰ (333);
- Γ₃: 1⁴3² (1,080), 1⁴6 (864), 1¹⁰ (297), 1⁶4 (216), 1²4² (216);
- Γ₄: 1⁶4 (972), 1¹⁰ (729), 1⁴6 (648), 1⁴3² (324).

Patterns:
- **(L)** the twisted cycles have ℓ ∈ {3, 4, 6}: never 2, never 5.
- **(P) every edge lies in at least one prism**: d(e) ≥ 1 everywhere.

At 99 (Σℓ = 6), (L) and (P) would leave only the types 1⁶, 1³3, 1²4 (3² and 6 would have no prism). With the identities
of §2, (P) gives t₃ ≥ 231 and t₂ ≤ 3465. No contradiction so far. The aim is a second, independent count of t₃ or of
the long cycles that clashes at m = 7.

## 4. Attempt to widen the test bench (12/10, `asym243/s3grid/z3rand.py`, `z3batch.sh`, `canon_cmp.py`)
- I ran 12 Z₃-cover instances (full model restricted to A₃) with 12 random gains imposed. They are **all UNSAT at once**:
  the forced gains clash with the tree gauge and with triangle consistency. This was a design flaw, kept in
  `z3batch_try1_overconstrained.log`.
- I then ran 10 instances varying only the solver seed. **All SAT in 4–6 min, all isomorphic to known graphs** (nauty
  canonical forms): Γ₃ ×8, Γ₄ ×1, twin ×1, never BvLS, never a 5th graph.
- This is empirical support, not a proof, for "4 classes of Z₃-covers". It also means the conjectures of notes 176–177
  cannot be tested outside these 4 graphs this way.

## 5. Status of the hand attack on (L2) (no ℓ = 2 cycle in B_xa)
Suppose B_xa has an ℓ = 2 cycle: T₁, T₂ through x and T′₁, T′₂ through a. This gives an 8-cycle
u₁v₁p₁q₁u₂v₂p₂q₂, alternating triangle edges and B edges, with x and a attached to the two halves. μ = 2 then forces, for
each non-adjacent pair, a second common neighbour at distance 2 from both x and a. Examples: (p₁,q₂) have a and some w;
(u₁,p₁) have v₁ and some y.

The proof must therefore go one level deeper, with possible identifications between these new vertices. This is the
same type of case tree as the classical uniqueness proofs. **Next tool:** a "completion with identification" engine (in
the spirit of Todd–Coxeter) that explores these trees exhaustively at small depth. It is a microscope that produces a
human-readable case analysis, not a solver verdict.
