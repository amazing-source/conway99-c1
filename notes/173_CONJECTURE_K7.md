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
