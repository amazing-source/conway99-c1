# The spread-free world at 243 vertices (lab session, started 12 October 2026, 19:20 UTC)

Status at 20:40 UTC: **a fifth strongly regular graph (243,22,1,2) has been found, and it has no regular spread**
(section 6). Checked by two independent scripts of this session; not audited by a third party; literature not yet
searched for it. Everything else here is own derivation of 12/10 unless a source is given.
Direction (user, direct, 12/10): after Z3 (the four cyclic covers) and S3 (no other cover, certification postponed),
look at the strongly regular graphs (243,22,1,2) WITHOUT regular spread, starting with a census by switching.

## 1. Why this is the twin of Conway's question

A REGULAR SPREAD of a srg(v,k,1,2) is a partition into v/3 triangles, two of them joined by 0 or 3 edges. Its quotient
is then a srg(v/3, k-2, 1, 6). For the five feasible orders of the family (k = 4, 14, 22, 112, 994):

| v | quotient | multiplicity of the negative eigenvalue | regular spread possible | known graphs |
|---|---|---|---|---|
| 9 | triangle | - | yes | Paley(9) |
| 99 | srg(33,12,1,6) | 44/7 | NO | none |
| 243 | srg(81,20,1,6) = BH | 20 | yes | four with a regular spread, **one without (section 6)** |
| 6273 | srg(2091,110,1,6) | 16830/21 | NO | none |
| 494019 | srg(164673,992,1,6) | 4776480/63 | NO | none |

So Conway's graph, if it exists, has no regular spread. Before today every known member of the family had one. The
question "does (lambda, mu) = (1,2) force a regular spread?" is now answered: NO (section 6). Consequence for 99: no
proof of non-existence can go through "every srg(v,k,1,2) has a regular spread"; conversely there is now one explicit
graph of Conway's kind whose local structure can be examined.

These graphs are exactly Cameron's partial quadrangles PQ(2, t, 2) (lines of size 3, t + 1 = k/2 lines per point, no
triangle of lines, two non-collinear points with 2 common neighbours): t = 1, 6, 10, 55, 496.

## 2. Classical switching does not exist here (hand)

Godsil-McKay switching with one switching set C (|C| = 2m, induced r-regular, every outside vertex with 0, m or 2m
neighbours in C): counting the edges leaving C gives 2m(22 - r), counting the pairs of C through their outside common
neighbours gives at most 2m(2m - 1); as every outside vertex with neighbours in C has at least m of them,
(m - 1)(22 - r) <= 4m - 2, i.e. r >= 17, which forces at least (17^2 + 2)/2 = 145 vertices in C and then m >= 73 > 22.
So no such set exists. The same counting kills the WQH switching on two pairs.

## 3. Trades: what a difference between two graphs must look like (hand, checked numerically)

Let G, G' be two srg(243,22,1,2) on the same vertex set, Delta = A' - A, F = the set of vertices incident to a changed
pair, R the rest. Then Delta is supported on F x F and:

* (support criterion) Delta = 9 (E' - E), E, E' the projections on the 4-eigenspaces. For r in R, E' e_r = E e_r, so
  the two 4-eigenspaces share span{E e_r}, and what moves is inside W_4(F) + W_-5(F), the eigenvectors of A SUPPORTED
  IN F. A non-trivial trade on F needs eigenvectors of BOTH eigenvalues supported in F. The spectrum of Delta is
  symmetric, in [-9, 9] (principal angles).
* (thickness) A[R,F] Delta = 0: every vertex of R adjacent to F has at least two neighbours in F, and its F-neighbours
  gain and lose the same number of neighbours in every changed vertex.
* (small regions) a set of at most 11 vertices is rigid (each vertex keeps a private outside neighbour, since two
  vertices share at most 2 neighbours).
* (closed neighbourhood) F = {p} + N(p) is rigid in every srg(v,k,1,2): the 220 outside vertices are the pairs of
  non-collinear neighbours of p, a re-completion gives a graph with the same line graph as the cocktail-party graph on
  N(p), and Whitney's theorem returns a relabelling. (This is the case cadical could not decide with the heavy
  encoding: 200 s, 1.4 million variables.)

Numerical check on the stored graphs (`delta_spectrum.py`, same labelling):

| pair | vertices touched | rank of Delta | spectrum of Delta | eigenvectors supported in F (4 / -5) |
|---|---|---|---|---|
| BvLS -> twin | 180 = the vertices non-adjacent to one line L | 64 | +-3 sqrt 5, 32 each | 72 / 50 |
| BvLS -> Gamma4 | 162 = two cosets of a hyperplane | 32 | +-9, 16 each | 61 / 50 |

For ANY line L of ANY srg(243,22,1,2) the 180 vertices non-adjacent to L carry a 122-dimensional space of such
eigenvectors (72 + 50): {L, N(L), rest} is equitable, quotient eigenvalues 22, 4, -5. The Gamma4 trade is an exchange
of two 16-dimensional subspaces between the two eigenspaces (all principal angles 90 degrees).
`trade_census.py` (free a region, ask for another completion): a line and a 3x3 grid of BvLS are rigid (UNSAT in
0.3 s and 27.9 s), consistent with the above.

## 4. Holonomy of a line (own definition) and flat lines

For a line L = {p, u, u*}, each neighbour x of p off L has exactly one neighbour among the neighbours of u off L
(mu = 2). Going round L gives a permutation tau_L of the 20 neighbours of p off L. A fixed point of tau_L is a line
PARALLEL to L (joined to L by a perfect matching, i.e. a prism K3 x K2). L is FLAT when tau_L = identity (20 parallel
lines). Facts:

* every line of a regular spread is flat; a regular spread is the same thing as a set of pairwise disjoint flat lines
  closed under "parallel to";
* the 60 neighbours of L induce a cubic graph (mates + the 2-factor of the transverse edges); the 180 other vertices
  are in bijection with the pairs of non-mate neighbours of p off L, and also of u, and of u*;
* number of lines meeting L in 0 points with j edges to L: j = 3: f, j = 2: 60 - 3f, j = 1: 480 + 3f, j = 0: 320 - f,
  where f = number of fixed points of tau_L;
* two lines through p span a 3x3 grid iff each sees the two points of the other as fixed points.

| graph | Aut | vertex orbits | grids per vertex | lines parallel to a line (value: lines) | flat lines | regular spreads | prisms |
|---|---|---|---|---|---|---|---|
| BvLS | 3 849 120 | 243 | 55 | 20: 891 | 891 | 11 | 8910 |
| twin | 4320 | 3, 60, 180 | 55 / 19 / 13 | 2: 240, 4: 540, 20: 111 | 111 | 1 | 2430 |
| Gamma3 | 864 | 27, 108, 108 | 23 | 4: 162, 8: 216, 10: 432, 20: 81 | 81 | 1 | 4158 |
| Gamma4 | 3888 | 81, 162 | 31 | 8: 108, 12: 486, 14: 216, 20: 81 | 81 | 1 | 5670 |
| **new (section 6)** | **2916** | **243** | **25** | **8: 243, 10: 486, 14: 162** | **0** | **0** | **4536** |

(`line_holonomy.py`, `aut_tools.py`; the orders 3 849 120, 864, 3888 agree with the known / stored values; 4320 for the
twin is computed here.) The 30 flat lines of the twin outside its spread are the lines through its three special
vertices. Observation, not proved: the number of lines parallel to a line is even in all five graphs. It is NOT because
fixed points come in mate pairs (`holonomy_mates.py`: false in Gamma3, Gamma4 and the new graph).

## 5. Census of the graphs with a semiregular group Z_3^4 (`tricayley_census.py`)

Gamma4 is invariant under 81 translations of F_3^5 (a hyperplane; `translations_check.py`), so it is a "tri-Cayley"
graph: vertices (i, g), i in {0,1,2}, g in H = Z_3^4, (i,g) ~ (j,h) iff h - g in D_ij. This suggested the census of
ALL srg(243,22,1,2) with a semiregular elementary abelian group of order 81.

* The matrix (|D_ij|) has eigenvalues 22 and two of {4, -5}, and |D_ii| is even: only TYPE I (|D_ii| = 10,
  |D_ij| = 6) and TYPE II (|D_ii| = 4, |D_ij| = 9).
* Type I: D_00 is a set of 5 projective points of PG(3,3) with no three collinear and no point on two secants, i.e.
  a frame; unique under GL(4,3). Normal form D_00 = +-{e1,e2,e3,e4,e1+e2+e3+e4}, 0 in D_01, 0 in D_02.
* Type II: D_00 = +-{e1,e2}, each orbit is 9 disjoint 3x3 grids, D_01 is a transversal of <e1,e2>; normal form
  0, e3, e4 in D_01, 0 in D_02.
* cadical; each solution is rebuilt, checked strongly regular, identified, and all its normal-form images (orbit
  permutations, linear maps, translations) are blocked.

**Type I: complete.** 253 476 variables, 894 515 clauses; three classes, then UNSAT (12.9 s) after 2592 blocking
clauses; whole run 30 s:

1. BvLS (72 images),
2. **a new graph** (1440 images),
3. Gamma4 (1080 images).

So, subject to the correctness of the encoding and of the solver (no proof certificate kept yet): a srg(243,22,1,2)
with a semiregular Z_3^4 of type I is BvLS, Gamma4 or the new graph.
**Type II: not finished.** Two classes found, both BvLS (1296 and 216 images, 37 s and 50 s), then NO DECISION in
150 s on the third call. To be recalibrated (transversal constraints, longer run).

## 6. The new graph (provisional name Gamma5)

File `new243_tricayley_Z3x4_grids25.edges`, sha256 817145d53f75b85f52a2ad9a278bbbe26ae4bac3c4b5ec9270e65c8ca37fccf0.
Vertex 81 i + (index of g in the lexicographic order of F_3^4). Connection sets (digits of g):

    D_00 = +-{0001, 0010, 0100, 1000, 1111}        D_01 = {0000, 0112, 1022, 1201, 2121, 2210}
    D_11 = +-{0001, 0012, 0102, 1002, 1112}        D_02 = {0000, 0112, 1021, 1202, 2120, 2211}
    D_22 = +-{0010, 0012, 0120, 1020, 1121}        D_12 = {0112, 0221, 1010, 1101, 2022, 2200}

Three frames; no direction is common to the three, so no translation has all its orbits on lines.

Checks done (all by this session):

| check | script | result |
|---|---|---|
| A^2 = 20 I - A + 2 J in integer arithmetic, 243 vertices, 2673 edges, degree 22 | `verify_new_graph.py` (imports nothing of the census) | True |
| spectrum | same | 22 (1), 4 (132), -5 (110) |
| lambda = 1, mu = 2 pair by pair | `trade_census.is_srg` inside the census | True |
| lines parallel to a line | `verify_new_graph.py` and `line_holonomy.py` (two codes) | 8 (243 lines), 10 (486), 14 (162); never 20 |
| regular spreads, exhaustive search | `verify_drg.spreads` | 0 |
| isomorphic to BvLS / twin / Gamma3 / Gamma4 | `iso_check.py` (positive controls pass) | False, four times |
| automorphism group | `aut_tools.py` (controls 864, 3888, 3 849 120 reproduced) | order 2916 = 4 x 729, transitive on the 243 vertices |

No flat line, hence no regular spread (section 4), independently of the Z3 and S3 results. Holonomy cycle types:
1^10 2^3 4 (486 lines), 1^8 2^6 (243), 1^14 2^3 (162). 25 grids through each vertex, 675 grids, 4536 prisms.
A transitive 3-group of order 729 acts; its central elements of order 3 have cocliques as orbits (a central element
with lines as orbits would give a regular spread).

What is NOT established: an independent audit (another person / another implementation of the adjacency and of the
checks); whether this graph is already in the literature (Brouwer's table lists (243,22,1,2) as not unique); whether it
is a Cayley graph; the type II census; any statement about graphs without a semiregular Z_3^4.

## 7. Next

1. finish type II; the other 14 groups of order 81; semiregular groups of order 27 (9 orbits) where the search is
   larger but of the same kind;
2. trades from the new graph (it has no spread to preserve): the 180-vertex region of a line, with the linear
   constraints A[R,F] Delta = 0 written first;
3. what the new graph says locally: the law behind "even number of parallel lines", which of its local patterns can
   exist with 11 replaced by 7 lines per point (Conway);
4. asymmetric members: none known; the censuses by semiregular group find symmetric graphs by construction.
