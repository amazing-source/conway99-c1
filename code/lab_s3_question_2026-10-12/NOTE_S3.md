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

# Second attack (12 October 2026, 13:20 to 15:56 UTC): own derivation, no earlier note used

Status of this part: derivations by hand and exhaustive solver runs of a few seconds (cadical, UNSAT answers without
proof certificate); **the S3 question is still NOT decided**; what is proved is listed in section 9. Not audited.

## 5. The local problem at one vertex, and types

Gauge at a vertex P: all edges at P positive; every far vertex R (60 of them, "blocks") has a positive edge to its
first common neighbour with P. The conditions carried by the pairs {P, R} and by the 180 non-adjacent pairs {a, b}
inside N(P) ("inner pairs") involve only the 360 edges between N(P) and the far vertices: each block has a STATE, flat
or one of the ten partitions 3+3 of Oct(R) = N(P) & N(R); each inner pair lies in exactly five blocks and must be
separated by 0 or 3 of them. This is exact for the squares through P (`local_vertex.py`, `local_cnf2.py`,
`local_lib.py`).

Grid pairs: the six common neighbours of {x, y} are three pairs {z, x + y - z} (the three grids through x, y).
A split pair is of **type A** if its three grid pairs are separated (its three grid squares are odd) and of
**type B** if exactly one is. The type is intrinsic to the pair (the same seen from x, from y, or as an inner pair
of a common neighbour). For an inner pair {a, b} at P: grid block a + b - P, and two "partner pairs" of blocks
{v, a + b - v}; type A = separated by the grid block and by one block of each partner pair.

Model (own): N(P) = the 20 rank-one Hermitian 2x2 matrices u u* over F_9, i.e. (F_9^2 - 0) / mu_4; the 60 blocks = the
non-degenerate Hermitian forms h; Oct(h) = the unit vectors of h modulo mu_4, an octahedron whose three antipodal
pairs are the orthonormal frames of h (the grid pairs); B(uu*, ww*) = N(det[u, w]); the four isotropic points of h
are the four type A partitions (partition of Oct(h) by the quadratic character of det[u, d]), the six type B
partitions are "one unit vector with a frame not containing it".
The ten LINE SOLUTIONS: for an isotropic direction d, the split blocks are the 24 far R with B(R - P, d) = 0, each with
the partition of Oct(R) by the value of B(Z - P, d); all 24 are of type A; the 72 split inner pairs are the {a, b} with
B(a - P, d) = -B(b - P, d) non-zero, and they are all of type B, their odd grid square being the one through P.

Counting identities at P (hand): with n_A, n_B the numbers of blocks of type A, B and alpha', beta'_1, beta'_0 the
numbers of inner pairs of type A, of type B separated by their grid block, of type B not separated by it:
alpha' + beta'_1 = 3 n_A + n_B and beta'_0 = 2 n_B.

## 6. Solver results on the local problem (all complete, seconds)

| statement | run | result |
|---|---|---|
| (C1) local solutions without a block of type B | `local_cnf2.py nontrivial noB` | exactly 10, the line solutions; UNSAT after them (3.4 s) |
| (C2) a line solution at P together with the local problem at a neighbour Z of P off the line | `local_glue.py neighbour` | UNSAT for each of the 18 neighbours (under 1 s each) |
| (C3) local solutions in which every split inner pair is of type A | `local_cnf2.py nontrivial pairsA` | none (0.1 s) |
| (C4) a block of type B while every split inner pair is of type B | `local_cnf2.py typeB=0 pairsB` | none (31 s) |
| (C5) a block R0 of type B while no other block is of type B, or only blocks meeting Oct(R0) in 3 points, or only the 25 blocks "R0, those, and the blocks through the non-grid pairs separated by R0" | `explore_typeB2.py`, `explore_typeB4.py` | none (0.7 s, 0.3 s, 23 s) |
| (C6) a local solution with a block of type B invariant under an automorphism fixing P | `sym_local.py` | none for 19 of the 22 conjugacy classes of the stabiliser (order 2880); NO DECISION (90 s) for the three classes of involutions without fixed point on N(P) |
| the local problem with a block of type B, no other assumption | `local_cnf2.py typeB=0`, `typeB_cubes.py`, `local_enum2.c` | NO DECISION (cadical 150 s to 285 s; own search not finished) |

(C2) was checked for one direction d; the stabiliser of P is transitive on the ten directions.
In (C2) the contradiction at Z already follows from the eight split pairs {Z, Z'} (Z' in N(P)) alone
(`core_neighbour.py`), not from fewer than about seven of them (`core_neighbour2.py`).

## 7. Consequences for a parity skeleton on BH (global)

* (G1) If no pair is of type B, every pair is flat and the skeleton is trivial (by C3; also by C1 + C2).
* (G2) If no pair is of type A, the skeleton is trivial (C4 at every vertex, then no split block at all).
* (G3) Every vertex with a split pair has a split pair of type B (C1 + C2), and then an inner pair of type A (C4).
* So a non-trivial skeleton has pairs of both types; **what remains is to exclude one pair of type B**
  (exactly one odd grid square). Neither cadical on the local problem, nor on the local problems at several vertices
  glued by the pair states (`local_glue.py typeb`, `grid_types.py`), nor on the complete problem in the hybrid
  encoding (`full_hybrid.py`, 54 270 variables) decided it within the five-minute bound.
* The hypothesis H(delta) of the first hours (the same line direction at every vertex) is contradictory for a simple
  reason now visible: in a line solution the split inner pairs are of type B, so their endpoints are not of line type.

## 8. Reformulations found on the way

(a) **Distance-regular graphs.** A srg(243,22,1,2) with a regular spread (81 triangles, two of them joined by 0 or 3
edges) minus the spread edges is a distance-regular graph with intersection array {20,18,4,1; 1,2,18,20}, an antipodal
3-cover of the srg(81,20,1,6) (trivial holonomy on the lines is forced: lambda = 1), and conversely such a
distance-regular graph plus its antipodal triangles is a srg(243,22,1,2). Proof by hand in the lab session (counting
of common neighbours); the Krein parameters of the array (`drg_krein.py`, exact) vanish only where the antipodal
structure forces it. So the S3 question is: **is every distance-regular graph with this array a cyclic cover of BH?**
`verify_drg.py` (own script, exhaustive search of the regular spreads on the stored edge lists): BvLS has 11 regular
spreads, the three other graphs (twin, Gamma3, Gamma4) exactly one each; in all cases the quotient is srg(81,20,1,6),
the graph minus the spread is distance-regular with that array, and the cover is cyclic. The four graphs are pairwise
non-isomorphic (numbers of 3x3 grids through a vertex: 55; 13/19/55 on 180/60/3 vertices; 23; 31). Hence **four
pairwise non-isomorphic distance-regular graphs with intersection array {20,18,4,1; 1,2,18,20}**. Literature looked up
on 12/10 (web): distanceregular.org lists for this array only the coset graph of the shortened ternary Golay code and
makes no uniqueness statement; Brouwer's table of strongly regular graphs lists (243,22,1,2) as "not unique", citing
Djematene + AI. I found no statement on non-cyclic covers.

(b) **Two-eigenvalue form.** With rho the 2-dimensional representation of S3, the gains give a real symmetric
162x162 matrix A_rho (blocks rho(g_xy)) and the cover is a srg(243,22,1,2) iff A_rho^2 = A_rho + 20 I. In complex
coordinates A_rho v = H v + S conj(v), H Hermitian (cube roots of unity on the edges with a rotation), S symmetric
(cube roots of unity on the edges with a reflection), and the condition is
    H^2 + S S* = H + 20 I,      H S + (H S)^T = S.
Reduced modulo the prime 1 - omega these two equations are exactly the parity skeleton; modulo 3 they add the first
moments. Consequences: the spectrum of H lies in [-4, 5]; it is {5^(36-m), (-4)^(45-m)} together with m pairs
{theta, 1 - theta}; rank S = 2m; the number of reflection edges is the sum of (5 - theta)(4 + theta) over the m pairs.
For a cyclic cover S = 0. No contradiction derived from this yet.

(c) In a 3-cover the grid squares on a pair have holonomies of classes (e,e,e), (e,c,c), (c,c,c) for a flat pair,
(r,r,r) for type A, (r,c,c) for type B (c a rotation, r a reflection): never exactly one non-trivial holonomy.

## 9. What is proved, what is not

Proved (hand + the runs of section 6, to be audited): G1, G2, G3; the distance-regular reformulation; the four
distance-regular graphs. NOT proved: that a pair of type B is impossible, hence that every parity skeleton is trivial,
hence that every regular-spread srg(243,22,1,2) is one of the four graphs. No S3-cover was constructed either.
Possible next steps, with their nature: (i) an exhaustive cube-and-conquer of the local problem with a block of type
B (1560 variables; size unknown: the restriction of type B to 25 blocks falls in 23 s, to 45 blocks not in 285 s);
(ii) the same with the gains in S3 (`s3_local.py`, heavier); (iii) a proof from the equations of 8(b).

## 10. Addendum (16:16 UTC): no symmetry, no trivial vertex

Complete problem in the hybrid encoding (`full_hybrid.py`: the 810 edge variables, so that all relations between
cycles are present, plus one-hot states for the 2430 pairs).

(S) **No non-trivial parity skeleton class is invariant under a non-identity automorphism of BH.**
`sym_global_all.py`: Aut(BH) (order 233 280 = 2^6 3^6 5) has 41 conjugacy classes of non-identity elements; every
element has a power of order 2, 3 or 5; for one representative sigma of each of the ten classes of elements of prime
order (five of order 2, four of order 3, one of order 5), the complete problem with "the state of (sigma x, sigma y) is
the image of the state of (x, y)" (the states do not depend on the gauge) and "some pair is split" is UNSAT, in 0.8 s
to 6 s each. (The cloud note 165 had this for odd order from its own solver runs; this is an independent encoding and
covers the involutions.)
Consequence: let G be a distance-regular graph with intersection array {20,18,4,1;1,2,18,20} that is not a cyclic
cover of BH. An automorphism of G preserves the antipodal classes, induces an automorphism of BH fixing the parity
class of the gains, hence the identity of BH; it is then a deck transformation; the monodromy group is S3 (transitive
on the three sheets because G is connected, and not inside A3), whose centraliser in Sym(3) is trivial. So
**Aut(G) = 1: a non-cyclic cover, if it exists, is an asymmetric distance-regular graph**, and the corresponding
srg(243,22,1,2) has no non-identity automorphism preserving that spread (it is asymmetric as soon as the regular
spread is unique, as it is in the three graphs other than BvLS).

(D) **In a non-trivial parity skeleton every vertex has a split pair** (hence, by G3, a split pair of type B).
`dead_point.py` (local, 0.4 s, complete): a local solution in which the 18 blocks through one point u of N(P) are flat
is trivial or the line solution of direction u. So a neighbour Z of a trivial vertex x is trivial or of line type
along Zx, and line type is excluded by C2; by connectivity everything is trivial. Cross-check with the complete
encoding: `global_tests.py trivialP` is UNSAT in 0.2 s.
Same local lemma, other reading: for every edge {P, u} of BH some pair {P, R} with R adjacent to u is split.

Not decided (120 s each): `global_tests.py allsplit` (no flat pair at all: a signing of BH with eigenvalues 5 and -4
only) and `noflatP` (no flat pair at one vertex). The solver settles in seconds every case with enough flat pairs or
with a symmetry, and none of the cases rich in split pairs.
