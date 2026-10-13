# The spread-free world at 243 vertices (lab session, started 12 October 2026, 19:20 UTC)

Status on 13 October 11:45 UTC: complete census of the graphs containing the common third: exactly seven (section 6h).
Status on 12 October 21:45 UTC: **four new strongly regular graphs (243,22,1,2) found today, none with a regular spread**: a
fifth (vertex-transitive, Cayley on non-abelian groups, section 6), a sixth (Aut 108, section 6d), a seventh (Aut 162)
and an eighth (Aut 108) (section 6e). With the four covers of BH that makes eight known graphs. Checked by two independent scripts of this session; not audited by a third party; literature not yet
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

**It is a Cayley graph on non-abelian groups** (`regular_subgroups.py`): the Sylow 3-subgroup P of Aut (order 729,
normal, Frattini subgroup of order 27) has 13 maximal subgroups, 9 of them act regularly on the vertices. All nine are
non-abelian; by (number of elements of order 3, of order 9, order of the centre): (26, 216, 3) twice, (80, 162, 3)
three times (two with a derived subgroup of order 9, one of order 3), (134, 108, 9) three times, (188, 54, 3) once.
So there are partial difference sets with the parameters of the Golay one in non-abelian groups of order 243 whose
Cayley graph is not BvLS. In such a group G the centre does not meet the connection set (a central element of order 3
in it would give a regular spread).

`cayley_census.py`: ALL partial difference sets (243,22,1,2) of these nine groups (CryptoMiniSat, 121 variables,
solutions blocked with their conjugates under P). Done at 21:20 UTC for the three groups (134, 108, 9): 84 sets each
up to conjugation, 66 giving the new graph and 18 giving BvLS (one representative of each local invariant tested by
isomorphism), nothing else. The six other groups are running (results to be added).

Literature (web, 12/10 20:38 UTC): Brouwer's table says for (243,22,1,2) "Berlekamp-vanLint-Seidel; not unique"
(credited to Djematene + AI); I found no mention of a graph without regular spread or of a non-abelian Cayley
construction. This is a search of a few minutes, not a bibliography.

What is NOT established: an independent audit (another person / another implementation of the adjacency and of the
checks); a real literature search; the type II census; any statement about graphs without a semiregular Z_3^4.

## 6b. Two tempting regularities, FALSE in general (`parallel_parity.py`)

In BvLS, the twin, Gamma3, Gamma4, Gamma5 and the sixth graph: (P1) two lines parallel to the same line are joined by
0 or 3 edges, never 1 or 2; (P2) the number of lines parallel to a line is even. Both FAIL in the eighth graph
(section 6e): 108 of its lines have 9 parallel lines, and 324 pairs of parallels of a common line are joined by exactly
one edge. So neither is a law of the parameters (1,2); they were artefacts of the first six examples. Recorded so that
nobody (me included) tries to prove them.

## 6c. Sampling with a semiregular Z_3^3, nine orbits (`semireg_sample.py`, `quotient_types.py`)

No normal form, so not a census. 3.76 million clauses. Free diagonal: BvLS twice (8 s each, all |D_ii| = 6), one call
without decision in 170 s. Diagonal (6,6,6,0,0,0,0,0,0): Gamma4 (18 s). Diagonals (6,6,6,6,6,6,0,0,0) and all 0: no
decision in 170 s. The possible 9x9 quotient matrices are constrained by Y = M + 5I - 3J, Y^2 = 9Y (row lists in
`quotient_types.py`; the full list of matrices was not finished in 250 s). Nothing new found this way yet.

## 6d. A SIXTH graph, with a group of order 108, by a trade keeping one third of Gamma5 (`partial_symmetric_trades.py`)

Setting: Gamma5 in its tri-Cayley form; the orbit 0 (81 vertices, a folded Hamming graph H(5,3)/<w>) is kept with ALL
its adjacencies (inside and towards the other 162 vertices); the adjacency inside the 162 other vertices is free but
must be invariant under a subgroup S of the 81 translations.

| S | extra condition | result |
|---|---|---|
| <0010, 0001>, order 9 | none | 12 completions listed (limit): BvLS, Gamma4 and Gamma5 all occur, so **these three graphs share this third and its attachments**; they differ on 648 or 1296 pairs inside the 162 vertices |
| <0010, 0001>, order 9 | not invariant under all 81 translations | **UNSAT** (54 s, repeated 51 s): with this boundary, invariance under S forces invariance under the 81 translations |
| <0001>, order 3 | not invariant under all 81 translations | **SAT in 20 s: a new graph** |

New graph: file `new243_trade_aut108.edges`, sha256 f49476e0726074e3d6328466594b7f32917b00be719a24eb27427f6cba927b2e.
Checks (same scripts as for Gamma5): A^2 = 20I - A + 2J in integers, spectrum 22, 4^132, (-5)^110, lambda = 1 and
mu = 2 pair by pair; lines parallel to a line: 2 (162 lines), 6 (108), 8 (459), 10 (108), 14 (54), never 20: no flat
line, no regular spread (exhaustive search: 0); 17 grids through every vertex; 3240 prisms; **Aut of order 108**, with
trivial vertex stabiliser on the orbit of 108; vertex orbits 27, 54, 54, 108; not isomorphic to BvLS, twin, Gamma3,
Gamma4, Gamma5 (direct tests, controls pass). Holonomy cycle types now include odd cycles (1^8 5 7).
P1 and P2 of section 6b hold in this graph too, but they fail in the eighth graph (section 6e).

So the family is much richer than the four covers: symmetric trades produce new graphs in seconds, and the symmetry
can be lowered step by step (2916, then 108). An enumeration of more completions with one translation is running
(started 21:30 UTC); the search with NO symmetry imposed (13 041 free pairs, about 2 million products) is the
natural route to an asymmetric member.

## 6e. Trades with NO symmetry imposed on 81 vertices; a seventh and an eighth graph (`free_trade.py`, `trade_bfs.py`)

Labelling: the blocks 0..80, 81..161, 162..242 are the three orbits of the tri-Cayley form of Gamma5 (and of the graphs
derived from it). For a graph and a block, everything is kept except the adjacency inside the block (3240 free pairs,
about 3 million clauses, a few seconds per solution, every solution blocked, end = UNSAT = complete list).

| graph | free block | complete list of the completions |
|---|---|---|
| Gamma5 | block 2 (and blocks 0, 1: same counts) | 6: Gamma5 four times (one is the input), Gamma4 twice |
| sixth graph | block 0 | 6: the sixth graph twice, a SEVENTH graph twice, an EIGHTH graph twice |
| sixth graph | block 1, block 2 | rigid (only the input) |
| twin, Gamma3 (stored labelling, cosets x4 = c) | each of the three blocks | rigid |

So Gamma4 and Gamma5 differ only inside ONE block of 81 vertices (648 pairs: at each vertex of the block 8 neighbours
leave and 8 come), a much smaller trade than BvLS -> twin (180 vertices) or BvLS -> Gamma4 (162).
With all 40 translation directions forbidden, the one-block problem on Gamma5 is UNSAT (4 s): each of its completions
keeps some translation.

Seventh graph: `new243_trade_aut162.edges` (sha256 96d91c64...): Aut of order 162, vertex orbits 81, 81, 81; parallels
2 (162 lines), 6 (81), 8 (459), 10 (189); 17 grids per vertex; 3186 prisms; no flat line.
Eighth graph: `new243_trade_aut108_b.edges` (sha256 40877e45...): Aut of order 108, orbits 27, 54, 54, 108; parallels
4 (162), 6 (54), 8 (162), 9 (108), 10 (270), 12 (81), 14 (54); 19 grids per vertex; 3834 prisms; no flat line.
Both: A^2 = 20I - A + 2J in integers by the independent script; pairwise non-isomorphic to the six others (invariants
and direct tests inside `trade_bfs.py`).

The search with 162 free vertices and no symmetry (13 041 free pairs, 8.45 million variables, 29.9 million clauses,
CNF of 674 MB) was started and STOPPED by me after two minutes without verdict: cadical took 3.9 GB and left 0.8 GB of
free memory on the PC. Cost to run it properly: about 5 GB of free RAM for one process; duration unknown. Not a result.

A breadth-first exploration by one-block trades from the fifth and sixth graphs is running since 21:39 UTC
(`trade_bfs.py`, at most 42 minutes); its log will be summarised here.

## 6f. Third trades: the switching that links the graphs (`third_scan.py`, `thirds_bfs.py`)

A THIRD of a graph is a set F of 81 vertices such that each vertex of F has 10 neighbours in F and each other vertex 6
(1_F - 1/3 is an eigenvector for the eigenvalue 4; the blocks of a tri-Cayley graph of type I are thirds). A THIRD
TRADE replaces the adjacency inside F by another strongly regular completion, everything else unchanged, no symmetry
imposed; the list of completions is complete (cadical ends with UNSAT) and takes 10 to 45 seconds.

Links found at 21:53 UTC with the thirds that are unions of orbits of Aut (`third_scan.py`), each line = one third:

| graph | third | completions (complete list) |
|---|---|---|
| Gamma4 | its orbit of 81 | Gamma4 five times, **BvLS** once |
| Gamma5 | each of its three blocks | Gamma5 four times, Gamma4 twice |
| sixth | orbits 27 + 54 (first) | sixth, Gamma5 |
| sixth | orbits 27 + 54 (second) | sixth four times, **Gamma3** twice |
| sixth | block 0 | sixth, seventh, eighth, twice each |
| seventh | its three orbits of 81 | itself (twice); itself and Gamma5; itself (twice) |
| eighth | orbits 27 + 54 (first) | eighth, Gamma4 |
| eighth | orbits 27 + 54 (second) | eighth four times, Gamma3, Gamma4 |
| Gamma3, twin | no union of orbits is a third | - |

So seven of the eight graphs (all but the twin) are connected by trades on 81 vertices: BvLS - Gamma4 - Gamma5 - sixth
- Gamma3, with the seventh and the eighth attached. A cover of BH (Gamma3, Gamma4, BvLS) and a graph without regular
spread can differ on a single third. This is the "census by switching" in a workable form.
A graph has many more thirds than its orbit unions (`thirds_bfs.py` lists them with CryptoMiniSat: Gamma5 has at least
12 classes under Aut, the sixth at least 5, the eighth at least 12; most of those tried so far are rigid). The full
exploration (all thirds of every graph, all completions, new graphs queued) is running since 22:03 UTC, at most 58
minutes; log to be summarised here.

Cayley census (section 6): stopped by its time limit at 21:54 UTC after four of the nine groups: three groups with
(134, 108, centre 9): 84 sets each, only BvLS and Gamma5; one group with (26, 216, centre 3): 15 sets, only Gamma5.

## 6g. State at 22:40 UTC: one boundary, seven graphs; towards an asymmetric member (not found)

* Exploration by third trades (`thirds_bfs.py`, finished 22:22 UTC, 1129 s): 60 thirds tried over six graphs (lists
  of thirds not complete: 25 s per solver call, at most 17 classes per graph). No new graph. Only the special thirds
  are tradeable (the classes of size 2 or 3 under Aut); every other third tried is rigid.
* Sweep of ten other translation directions for the trade on 162 vertices with one translation kept
  (`partial_symmetric_trades.py`, three solutions per direction): Gamma4, Gamma3, the sixth, the seventh, the eighth,
  nothing else. With section 6d this shows that **BvLS, Gamma3, Gamma4, Gamma5, the sixth, the seventh and the eighth
  graph all contain the same third (a folded Hamming graph on 81 vertices) with the same attachments**; only the twin
  is not known to.
* Screening by linear algebra (`support_dims.py`): dimensions (w4, w5) of the eigenvectors supported in a region.
  Tradeable thirds: (20, 10). Blocks 1 and 2 of the sixth graph: (6, 0), and they are rigid, as the criterion says.
  Not sufficient: blocks of the twin (14, 4) and (12, 2) and 54-vertex regions (7, 2) are rigid for the solver.
  Regions of the fifth graph: 108 vertices (27, 16), 135 vertices (40, 30), 162 vertices (61, 50).
* Intermediate regions, NO symmetry imposed (`free_trade.py`): 108 free vertices (27 of block 1 + block 2) and 135
  free vertices (54 of block 1 + block 2) have exactly the 6 completions of the third trade on block 2 (complete
  lists, 50 s and 70 s; 15.6 million clauses for 135).
* 162 free vertices, no symmetry, every translation forbidden: NO DECISION in 1200 s (30 million clauses). Not a
  result. Recalibration: the forty big disjunctions were the likely obstacle; the census now running (22:39 UTC) drops
  them and blocks each completion together with its images under the 972-ish automorphisms of the fifth graph that
  preserve the kept third (`free_trade.py ... sym`); control on one third: 3 classes instead of 6 solutions.
* Alternating projections on the Grassmannian of completions (`dm_trade.py`): on a third (dimension 200) 40 random
  starts out of 40 converge to a completion in about 1.5 s each (Gamma5 23 times, Gamma4 17 times). On 162 vertices
  (dimension 3050) no convergence in 20 000 iterations, from random starts or near the input. So this tool works for
  small regions only, as it stands.
* Asymmetric member: none found. Smallest automorphism group so far: 108.

## 6h. 13 October: COMPLETE census of the graphs containing the common third (`row_clique.py`)

(The PC was switched off during the night; the SAT census of section 6g was lost after four solutions, all known.)

Method, no big SAT instance. Keep the block R = 0..80 of the fifth graph with all its adjacencies; the adjacency inside
the 162 other vertices F is unknown, no symmetry imposed. Every unknown condition is either on ONE row (the
neighbourhood inside F of a vertex f, against the 81 vertices of R, and the degree) or on TWO rows (g in N(f) iff f in
N(g); |N(f) & N(g)| = 2 - #(common neighbours in R) - [f ~ g]). So:

1. the complete list of the rows allowed for one vertex: **930** for the vertex 81 and 930 for the vertex 162
   (CryptoMiniSat on 161 variables, 1 second, list closed by UNSAT); the 81 translations give the lists of all vertices;
2. a completion is exactly one row per vertex, pairwise compatible: depth-first search with forward checking;
3. the row of the vertex 81 runs over one representative of each of the **191** orbits under the 6 automorphisms of
   the input that preserve R and fix that vertex.

Result (205 seconds, log `census_common_third_2026-10-13.log`): all 191 cases finished; 136 have no completion, 55 have
exactly 6. The 330 completions are: the eighth graph 102, the sixth 102, the seventh 66, Gamma3 27, Gamma4 20,
Gamma5 12, BvLS 1; counted with the orbit sizes, 1656 labelled completions. **No other graph.**

So: a strongly regular graph (243,22,1,2) that contains this third with these attachments (81 vertices inducing the
folded Hamming graph H(5,3)/<w>, joined to the 162 others as in BvLS) is one of SEVEN graphs: BvLS, Gamma3, Gamma4,
Gamma5, the sixth, the seventh, the eighth. In particular this boundary has no asymmetric completion; the smallest
group in the family is 108.

Checks: the first case agrees with the SAT census of the same case (6 completions: BvLS once, Gamma4 five times,
349 s with cadical against 3 s here); every completion is rebuilt and checked by A^2 = 20I - A + 2J before being
identified (invariants, then isomorphism test). Not checked: the row lists by a second solver; the whole by a third
party. What it does NOT say: nothing about graphs without such a third (the twin is not known to have one), nor about
thirds attached differently.

Other results of the morning:
* sixth and eighth graphs, block 1 or block 2 kept, 162 vertices free, no symmetry (`free_trade.py ... sym`): complete
  lists in 2 minutes each: only the sixth, seventh and eighth graphs (they differ inside block 0 only);
* the twin has many thirds (classes of 240, 720, 1440 under its group), BvLS too (198 affine ones, and classes of
  3960 up to 51 587): every third tried is rigid for the third trade, except the affine thirds of BvLS (-> Gamma4);
* the line boundary (a line and its 60 neighbours kept, 180 free: the region of the BvLS - twin switch) has too many
  candidate rows for this method as it stands (no list after 280 s): to be recalibrated, not a result.

## 6i. 13 October, continued: other boundaries (`boundary_census.py`), rigidity, data sheet

* **Line boundary of BvLS** (a line and its 60 neighbours kept with all their adjacencies, 180 vertices free, no
  symmetry): each free vertex has exactly 2 candidate rows; the search is complete (558 s, almost all spent listing
  rows): **exactly 2 completions, BvLS and the twin**. So a srg(243,22,1,2) containing a line with its 60 neighbours
  attached as in BvLS is BvLS or the twin. (Line boundaries of the twin, the fifth and the eighth graph: running.)
* Thirds of the twin kept (five classes, among them the small classes 30 and 60): the twin is the only completion.
  Thirds of Gamma3 kept: the class of size 12 has 4 completions (Gamma3 three times, Gamma4 once), the classes of
  size 288 are rigid.
* Random kept sets in the eighth graph: with 81 or 60 random vertices kept, every free vertex tested has exactly ONE
  candidate row (its own); with 45, one row for most vertices, 2 or 4 for a few. So such a graph is determined, row by
  row, by a random window of about 60 vertices with their adjacencies; the non-rigid boundaries are very special sets.
* All 81 translations checked as automorphisms of the fifth graph on all pairs (assumption of section 6h).
* Data sheet of the eight graphs: `NEW_GRAPHS_2026-10-13.md` (table, graph6 files, connection sets); a third,
  set-based check passes for all eight.
* S3: the drat-trim check of the main proof (1.75 GB) is running since 11:56 UTC with a memory guard.

## 6j. A statement without "attachments": graphs containing an induced folded Hamming graph (13 October)

Let X = H(5,3)/<11111> = Cay(Z_3^4, +-{e1, e2, e3, e4, e1+e2+e3+e4}) (81 vertices, valency 10; every edge in one
triangle; two non-adjacent vertices have 0 or 2 common neighbours: 1215 pairs with 0, "distance 3", and 1620 with 2).

**Proposition (hand + one finite check).** If a srg(243,22,1,2) Gamma contains X as an induced subgraph on a set R, then
the adjacency between R and the 162 other vertices is determined up to the names of these vertices.
Proof. (1) Two adjacent vertices of R have their common neighbour inside R (the third point of their triangle), so the
set S(f) of neighbours in R of an outside vertex f is a coclique of X. (2) Two non-adjacent vertices of R have 2 common
neighbours in Gamma, of which 0 or 2 are in R; so two vertices of S(f) are at distance 3 in X, and every pair at
distance 3 has exactly 2 common outside neighbours. (3) Sum of |S(f)| = 81 x 12 = 972 and sum of C(|S(f)|, 2) =
2 x 1215 over 162 vertices: mean 6 and mean square 36, so |S(f)| = 6 for all f. (4) The distance-3 graph of X has
exactly 12 cliques of size 6 through each vertex (`attachment_unique.py`), 162 in all; f -> S(f) is injective (two
outside vertices with the same 6 neighbours would have 6 common neighbours); so the outside vertices are exactly the
162 six-cliques of the distance-3 graph. QED. In particular R is automatically a third and a subspace.

**Consequence, with the exhaustive search of section 6h:** a strongly regular graph (243,22,1,2) containing an induced
folded Hamming graph on 81 vertices is one of exactly seven graphs: BvLS, Gamma3, Gamma4, Gamma5, the sixth, the
seventh, the eighth. The hypothesis is purely graph-theoretic; no symmetry and no spread is assumed. The twin does not
satisfy it: its subspace thirds (classes of 30 and 60) induce other graphs (`subspace_thirds.py`), and Gamma3, Gamma4
also have subspace thirds inducing other graphs (boundary invariants (18,4), (12,2), (14,2), (14,4), (12,0), (16,6),
(14,8), (16,4) against (20,10) for the folded Hamming ones).
Status: the proposition is a hand proof plus the count of cliques; the "exactly seven" rests on row_clique.py (own
code, one run, agreeing with cadical on the first case). Not audited.

Also closed on 13 October:
* line boundaries of the twin: the lines with 2 and with 4 parallel lines are rigid; its flat line (0,1,2) gives the
  twin and BvLS (same boundary as the BvLS line);
* thirds kept, second batch (`boundary_census.py`): fifth graph (11 other classes), Gamma4 (7), sixth (4), seventh
  (3), BvLS (5 non-affine): complete lists, only known graphs;
* type II over Z_3^4 with the transversal constraints: two classes (both BvLS), then NO DECISION in 900 s: still open;
* tri-Cayley over the other groups of order 81 (`groups81.py` builds the 15 groups by extensions, 15 classes of
  invariants found; `tricayley_groups.py`): with the rationality constraint (conjugacy classes in one rational class
  carry the same number of elements of D_00, D_11, D_22, because the eigenspaces are defined over Q) the cyclic group
  has no graph of either type (8 s; without the constraint: no decision in 240 s); the other groups are running.

## 6k. Type II over Z_3^4 closed by a trace argument: the graphs with a semiregular Z_3^4 are BvLS, Gamma4, Gamma5

Type II: D_ii = +-{a_i, b_i}, two projective points of PG(3,3) for each of the three orbits. For a non-trivial
character chi with kernel the hyperplane h, chi(D_ii) = 3 n_i - 2 where n_i = number of the points a_i, b_i in h. The
3x3 Hermitian matrix (chi(D_ij)) has its eigenvalues in {4, -5} (chi-component of A^2 + A - 20I = 2J), so its trace
3 (n_0 + n_1 + n_2) - 6 is 12, 3, -6 or -15: **every hyperplane contains 0, 3 or 6 of the six points a_0, b_0, a_1, b_1,
a_2, b_2**. Exhaustive check (`type2_trace.py`, 608 400 pairs of pairs against 40 hyperplanes): with D_00 fixed the only
possibility is D_11 = D_22 = D_00. Then the translation by a_0 maps every vertex to a neighbour: its orbits are lines,
two of them are joined by 0 or 3 edges, so they form a regular spread whose deck group is that translation, and the
graph is a Z_3-cover of the Brouwer-Haemers graph: one of the four covers (earlier theorem of the project, used with
its status). Among them only BvLS and Gamma4 have 81 dividing the 3-part needed; the twin and Gamma3 have Sylow
3-subgroups of order 27 (`sylow_info.py`), and the only fixed-point-free elements of order 3 of Gamma4 are its 80
translations, whose group is of type I. So type II over Z_3^4 gives BvLS only.
With the type I census of section 5: **a srg(243,22,1,2) with a semiregular elementary abelian group of order 81 is
BvLS, Gamma4 or Gamma5.** (The SAT run for type II had found BvLS twice and then no decision in 900 s; the argument
above replaces it.) The same trace condition for type I reads: every hyperplane contains a number of the 15 frame
points divisible by 3.

## 7. Next

1. finish type II; the other 14 groups of order 81; semiregular groups of order 27 (9 orbits) where the search is
   larger but of the same kind;
2. trades from the new graph (it has no spread to preserve): the 180-vertex region of a line, with the linear
   constraints A[R,F] Delta = 0 written first;
3. what the new graph says locally: the law behind "even number of parallel lines", which of its local patterns can
   exist with 11 replaced by 7 lines per point (Conway);
4. asymmetric members: none known; the censuses by semiregular group find symmetric graphs by construction.
