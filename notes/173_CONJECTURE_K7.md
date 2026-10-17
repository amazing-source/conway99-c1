# 173 — α = 22: the K₇ conjecture at a coclique point (open)

11 Oct 2026. This is a structural lead for the α = 22 sub-case. It has strong evidence at 243, but it is **not proved
at 99**. Scripts are in `code/asym243/hoffman/k7/`.

## 1. The statement
Let C be a Hoffman coclique (22 points) and c ∈ C. Then N(c) consists of 14 blocks forming 7 mate pairs (the 7 triangles
through c). Each other point x has exactly two neighbours in N(c), namely the two blocks through {c, x}. Two cases:
- they always lie in two different mate pairs;
- they are never mates, since a common neighbour of two mates other than c would break λ = 1.

Hence the 21 points are the edges of a **cubic graph Γ_c** on the 14 blocks, with no edge inside a mate pair. Contracting
the mate matching M_c gives a 6-regular loopless multigraph Γ_c/M_c on 7 vertices with 21 edges.

**Conjecture K7.** Γ_c/M_c is simple, i.e. Γ_c/M_c ≅ K₇: each pair of triangles through c carries exactly one point.

Failure means a pair of mate-edges e, f carries two points. There are two configurations:
- **(i)** x = z_{ab} and y = z_{ab′}: one block a has two Γ_c-neighbours that are mates;
- **(ii)** x = z_{ab} and y = z_{a′b′}: an alternating 4-cycle of Γ_c ∪ M_c.

## 2. Evidence and limits
- **BvLS (243, Hoffman coclique of size 45).** Here Γ_c/M_c is 8-regular on 11 vertices. Over the 45 points and
  45·55 = 2,475 pairs of mate-edges, the distribution of points per pair is {0: 495, 1: 1,980}, so a pair never carries
  two points (`local_bvls.py`).
- **The reason at 243 is the grids.** In BvLS every quadruple Q_{ef} (the 4 vertices adjacent to e∖c and f∖c) induces a
  4-cycle, i.e. lies in a 3×3 grid through c (13,365 = 1,485·9). A 4-cycle can contain only diagonal pairs of points,
  and the grid structure excludes those too.
- **No general mechanism.** In twin243, Γ₃ and Γ₄, the quadruples are 4-cycles, empty, or a single "side" edge. They are
  never diagonal, and never 2 or 3 edges (`quad_all.py`). So "quadruples are grids" is BvLS-specific.
- **Paley(9) violates the statement** (configuration (ii)). That case is degenerate: its 2-(3,2,2) design has repeated
  blocks, which is impossible at 99 and 243.

## 3. What the conjecture would give
- Γ_c is then a cubic 2-cover of K₇ along M_c. It is determined, for each of the 7 mate pairs, by a 3+3 split of the
  other 6. That gives 20⁷ labelled choices, or **2,141 classes** of (Γ_c, M_c) up to isomorphism (`k7covers.py`, then
  nauty `labelg`; `classes.g6`).
- For each class, the 14 blocks through point 0 are **fully fixed** (294 units, `mkclass.py`).

## 4. Tests run here (Kissat, full α = 22 model of note 171 §5)
| instance | result |
|---|---|
| configuration (i) forced (`caseI.units`) | UNKNOWN after 1,428 s |
| configuration (ii) forced (`caseII.units`) | UNKNOWN after 1,434 s |
| K₇ class #0 (14 blocks fixed) | UNKNOWN after 1,237 s |
| K₇ class #1000 (14 blocks fixed) | UNKNOWN after 1,236 s |

So the conjecture is not refuted locally. Even under the conjecture, one class takes more than 20 minutes, so 2,141
classes is more than 700 CPU-hours: not feasible here.

## 5. Status
- **Open:** a proof of K7, which must use the Hoffman property (Paley(9) shows it is not automatic). I found no proof.
- If K7 is proved, it should be combined with the ternary classification of note 172 §5 (six types). It could also be
  imposed at **all** 22 points at once, a far stronger constraint than one point.

## 6. Addendum, 12 Oct 2026: ChatGPT dossier C1_K7_RESULTATS_PARTIELS
Read, not reproduced. **K7 remains open**: neither (i) nor (ii) is excluded in general.
- **Theorem 1 (proved; I checked the proof by hand). Γ_c ∪ M_c is connected, for every c ∈ C**, with no ternary
  hypothesis.
  - On W = N(c), Q[W,W] = 6I − 3M − G is the Laplacian of Γ_c (weight 1) ∪ M_c (weight 3).
  - Suppose S is a proper component and u = 1_S. Then uᵀQu = 0, and Q² = 21Q gives Qu = 0.
  - But Yu is even: its c-coordinate is |S|, which is even, and its other coordinates are 0 or 2. Hence Nu is even.
  - For a ∈ S and b ∉ S, the vertex z_ab is a block with Du = 1 there, so (Qu)_z = |S| − 3 − (Nu)_z is odd.
    Contradiction.

  Corollaries: rank Q[W,W] = 13; the Schur complement on the 63 other blocks has rank 9; the split 3 + 4 of the 7
  fibres is excluded.
- **Reformulation.** Let w_e = v_a + v_{a′}. Then the Gram of the 7 vectors w_e is 6I − (n_ef). So **K7 ⇔ the w_e form a
  regular simplex (Gram 7I − J)**. The defects are exactly the norms 8, 6, 4 of the 21 labelled sums w_e + w_f, with
  Σ binom(n_ef, 2) = I_c + J_c.
- **Theorem 2 (conditional, ternary type (7,15,0)).** At the 7 points of S = C∖Z we have n_ef ≤ 3 (n = 4 is excluded),
  with an exact mixed/pure table. Nothing is claimed at the 15 points of Z or for the other types.
- The local fixture (n_ef = 4, connected union) **is not a counterexample**: it leaves 3,276 edges undetermined.
- My remark: K7 at every point ⇔ Σ_c Σ_{e<f} n_ef² = 22·21. This is a global quantity, but it involves the Hadamard
  product M = D ∘ N. So it cannot be computed from the polynomial identities in D and N alone, which is why the
  arithmetic of notes 172 and 175 cannot see it.
