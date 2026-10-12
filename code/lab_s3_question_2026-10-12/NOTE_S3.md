# The S3 question at 243 vertices: first attack by the lab session (12 October 2026, 12:55 UTC)

Status: bounded computations and hand derivations by the lab session; **nothing is decided**; not audited.
Context: the user's direction of 12/10 is the family srg(v,k,1,2) and its asymmetric members. By
`work/audit_v7_2026-10-12/THEOREM_Z3_COVERS.md` the Z3-covers of the Brouwer-Haemers graph BH = srg(81,20,1,6) that
are srg(243,22,1,2) are the four known graphs, all with an automorphism of order 3. What is left for a graph with a
regular spread is an **S3-cover** (gains not gaugeable into A3), which note 175 of branch `claude/v7-simultaneous`
leaves OPEN (solvers without verdict) and which would "generically be asymmetric". A necessary condition is a
non-trivial **parity skeleton**: eps on the 810 edges of BH, even on the 270 lines, the six path parities of every
non-adjacent pair of weight 0, 3 or 6 (equivalently (A_eps + I)^2 = 0 mod 3, note 175), not a coboundary.
Sources used: notes 165 (section 6) and 175 of that branch (their statements, not re-verified, except where said).

## 1. Structure found (hand; the counts of (a) checked by a script)

(a) **BH around a line** l = {P0, P1, P2}. Layers L_i = N(P_i) minus l (18 vertices each), 24 far vertices.
The 270 lines are: l; 27 tangent lines (a point of l and two points of its layer); 18 transversal lines (one point
in each layer: the two other rows of the nine grids containing l); 216 mixed lines (two points in two different
layers and one far point: 72 for each pair of layers); 8 lines inside the far set. A layer vertex has 5 neighbours
in each other layer; a far vertex has 6 neighbours in each layer and 2 far neighbours.

(b) **Line gauge.** By switching, all edges of l, all edges P_i - L_i (hence the tangent lines) and one edge of every
far vertex are positive: one representative per switching class (80 conditions). Then for u in L_i and j != i the
pair (P_j, u) has the path through P_i even, so **u has 0 or 3 negative edges to L_j**; a far vertex has 0, 3 or 6
negative edges to each layer. A non-trivial class has a split pair, which can be taken as (P1, u0), u0 in L_0.

(c) **A local identity.** With f_P the number of flat (6/0) pairs at P: the number of flat pairs among the 180
non-adjacent pairs inside N(P) is exactly 3 f_P (two ways of computing (A_eps^4)_PP, using
A_eps^2 = 20 I + A_eps + 6 T, T the signed adjacency of the flat pairs).

(d) **H^1 as a module over the translations.** H^1(BH lines; F_2) tensor F_4 splits over the 80 non-trivial
characters chi of F_3^4: multiplicity 8 for the 20 characters whose kernel is a tangent hyperplane of the ovoid,
5 for the 60 others (20 * 8 + 60 * 5 = 460, the dimension of note 165).

## 2. Computations (one process, at most five minutes each)

| what | result |
|---|---|
| `parity_line.py free` + cadical (positive control: no assumption) | SAT at once (the trivial class) |
| `parity_line.py all` (u0 has exactly three negative edges to L_1): 12 158 variables, 134 618 clauses; cadical | no decision in 270 s (3.0 million conflicts, 92 % of the variables still active) |
| the same with the signs of the nine grids through l fixed at random (54 unit clauses) | UNSAT in 1 s, twice |
| the same with six of the nine grids fixed (36 unit clauses) | UNSAT in 42 s; no decision in 55 s |
| `paritydfs.c` (depth-first search with unit propagation, order of the Z3 search), Knuth estimate, 20 000 dives | about 4.7e18 nodes; no pruning before decision 47 |
| the same in the line order (l, layers, far) | about 1.2e25 nodes |

So neither a CDCL solver on the whole instance nor a plain exhaustive search decides the parity skeleton: the Z3 case
fell in 4.6e10 nodes because its first moments are linear, and the parity layer has no such linear part.
This reproduces, with numbers, the conclusion of note 175 ("the tree only grows").

## 3. What would reduce it (not done)

* the 233 280 automorphisms of BH (a factor of at most 2e5), with note 165's fact that no non-trivial class is fixed
  by an element of odd order (solver result of the cloud session, not re-verified);
* branching on the TYPES of the pairs with Gaussian elimination over F_2 (a flat pair gives five linear equations,
  the type of a pair is itself the linear form L of note 165);
* the lifting conditions of an S3-cover on top of the parity skeleton (Codex's `NOTE_RELEVEMENT_S3_QUADRATIQUE.md`):
  per pair they cut 98 % of the gain patterns against 66 % for the parities alone.

Files: `parity_line.py` (CNF generator in line gauge, cubes, checker), `cube_probe.py`, `paritydfs.c`.

## 4. Addendum (12:57 UTC): the order of the search matters by a factor of a thousand, not yet by enough

Knuth estimates of the same search (unit propagation only) with other orders (`paritydfs.c`, options in its header):

| order | estimated number of nodes |
|---|---|
| vertices by number of placed neighbours (order of the Z3 search) | 4.7e18 (20 000 dives) |
| line order (l, layers, far) | 1.2e25 |
| vertices closing pairs first: placed non-neighbours with >= 6 / 5 / 4 / 3 placed common neighbours (PARITY_CLOSE) | 1.2e17 / 1.3e17 / 4.7e18 / **1.6e16** |
| dynamic choice of the edge lying in the most advanced pairs, weights 4^k / 8^k (PARITY_DYN=1 / 2; 3000 dives) | 7.6e17 / 8.2e16 |

These estimates are noisy (heavy tails), but the range 1e16 to 1e17 for the better orders is stable. The credits
available on AWS on 12/10 (about one core-year) correspond to roughly 1e13 nodes of this search. Missing factor:
about a thousand. Candidates, in the order I would try them: Gaussian elimination over F_2 on the type equations
(a flat pair makes its six path parities equal: five linear equations that unit propagation does not see); the
stabiliser of a split pair (order 48) and of the line; the lifting conditions. Nothing launched on AWS.
