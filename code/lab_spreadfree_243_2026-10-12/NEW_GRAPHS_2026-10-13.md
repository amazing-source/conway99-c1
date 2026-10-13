# Eight strongly regular graphs (243,22,1,2): data sheet (lab session, 13 October 2026)

Status: the four graphs `new243_*` were found on 12 October 2026 by this session. Each passes two independent checks
(A^2 = 20I - A + 2J in integer arithmetic; degree 22, lambda = 1, mu = 2 pair by pair with Python sets). They are
pairwise non-isomorphic and not isomorphic to the four known covers of the Brouwer-Haemers graph (different
invariants below, and direct isomorphism tests). None of the four has a regular spread (no line has 20 parallel lines).
Not audited by a third party. Literature: only Brouwer's table was consulted ("not unique").

Files (this folder): `<name>.edges` (one edge "a b" per line, vertices 0..242) and `<name>.g6` (graph6).

| file | srg(243,22,1,2), set-based check | Aut | vertex orbits | lines parallel to a line (value: lines) | flat lines | grids per vertex (value: vertices) | prisms | sha256 (first 16) |
|---|---|---|---|---|---|---|---|---|
| bvls243.edges | True | 3849120 | [243] | 20: 891 | 891 | 55: 243 | 8910 | 504041ee503bd740 |
| twin243_switched.edges | True | 4320 | [3, 60, 180] | 2: 240, 4: 540, 20: 111 | 111 | 13: 180, 19: 60, 55: 3 | 2430 | 90b231b772f789e2 |
| gamma3_aut864.edges | True | 864 | [27, 108, 108] | 4: 162, 8: 216, 10: 432, 20: 81 | 81 | 23: 243 | 4158 | 9aa0c8afd71419e6 |
| gamma4_aut3888.edges | True | 3888 | [81, 162] | 8: 108, 12: 486, 14: 216, 20: 81 | 81 | 31: 243 | 5670 | 53891ea71e212a31 |
| new243_tricayley_Z3x4_grids25.edges | True | 2916 | [243] | 8: 243, 10: 486, 14: 162 | 0 | 25: 243 | 4536 | 817145d53f75b85f |
| new243_trade_aut108.edges | True | 108 | [27, 54, 54, 108] | 2: 162, 6: 108, 8: 459, 10: 108, 14: 54 | 0 | 17: 243 | 3240 | f49476e0726074e3 |
| new243_trade_aut162.edges | True | 162 | [81, 81, 81] | 2: 162, 6: 81, 8: 459, 10: 189 | 0 | 17: 243 | 3186 | 96d91c64cc51528b |
| new243_trade_aut108_b.edges | True | 108 | [27, 54, 54, 108] | 4: 162, 6: 54, 8: 162, 9: 108, 10: 270, 12: 81, 14: 54 | 0 | 19: 243 | 3834 | 40877e459d332aae |

How the new graphs are obtained

* `new243_tricayley_Z3x4_grids25` (fifth): vertices (i, g), i in {0,1,2}, g in Z_3^4 (vertex 81 i + index of g in
  lexicographic order); (i, g) ~ (j, h) iff h - g in D_ij, with D_ji = -D_ij and
  D_00 = +-{0001, 0010, 0100, 1000, 1111}, D_11 = +-{0001, 0012, 0102, 1002, 1112}, D_22 = +-{0010, 0012, 0120, 1020, 1121},
  D_01 = {0000, 0112, 1022, 1201, 2121, 2210}, D_02 = {0000, 0112, 1021, 1202, 2120, 2211}, D_12 = {0112, 0221, 1010, 1101, 2022, 2200}.
  Vertex-transitive; Cayley graph on nine non-abelian regular subgroups of order 243 of its automorphism group.
* `new243_trade_aut108` (sixth), `new243_trade_aut162` (seventh), `new243_trade_aut108_b` (eighth): same vertex set;
  they agree with the fifth graph on every pair that meets the block 0..80 and differ inside the 162 other vertices.
  The sixth is invariant under the translation by 0001 only; the seventh and the eighth agree with the sixth outside
  the pairs inside the block 0..80.

Census facts (computer, this session; details and limits in NOTE_SPREADFREE.md)

* graphs with a semiregular group Z_3^4 with three orbits, type (10 inside, 6 between): BvLS, Gamma4, the fifth;
* graphs containing the block 0..80 of the fifth graph with its attachments (a folded Hamming graph on 81 vertices):
  exactly BvLS, Gamma3, Gamma4 and the fifth to eighth graphs (exhaustive search, 13 October);
* graphs containing a line of BvLS with its 60 neighbours and their attachments: exactly BvLS and the twin.

Check a file:  python -I verify_new_graph.py <name>.edges      (prints the identity, the spectrum, the parallel lines)
