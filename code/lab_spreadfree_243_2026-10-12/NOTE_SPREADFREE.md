# The spread-free world at 243 vertices (lab session, started 12 October 2026, 19:20 UTC)

Status: first facts and first measurements; nothing found, nothing excluded yet. Not audited.
Direction (user, direct, 12/10): after Z3 (the four cyclic covers) and S3 (no other cover, under certification), look at
the strongly regular graphs (243,22,1,2) WITHOUT regular spread, starting with a census by switching.

## 1. Why this is the twin of Conway's question (own derivation, 12/10)

A REGULAR SPREAD of a srg(v,k,1,2) is a partition into v/3 triangles, two of them joined by 0 or 3 edges. Its quotient
is then a srg(v/3, k-2, 1, 6) (same counting as at 243: trivial holonomy on the lines is forced by lambda = 1, and
mu = 2 gives 6 common neighbours). For the five feasible orders of the family (k = 4, 14, 22, 112, 994):

| v | quotient | multiplicity of the negative eigenvalue | regular spread possible | known graphs |
|---|---|---|---|---|
| 9 | triangle | - | yes | Paley(9) |
| 99 | srg(33,12,1,6) | 44/7 | NO | none |
| 243 | srg(81,20,1,6) = BH | 20 | yes | four |
| 6273 | srg(2091,110,1,6) | 16830/21 | NO | none |
| 494019 | srg(164673,992,1,6) | 4776480/63 | NO | none |

So Conway's graph, if it exists, has no regular spread, and the known members of the family sit exactly at the two
orders where a regular spread is arithmetically possible (and all have one). After Z3 + S3, a srg(243,22,1,2) outside
the four graphs has no regular spread either. A proof of "every srg(v,k,1,2) has a regular spread" using only
lambda = 1, mu = 2 would exclude 99; a spread-free srg(243,22,1,2) would be the first graph of Conway's kind.

## 2. Classical switching does not exist here (hand)

Godsil-McKay switching with one switching set C (|C| = 2m, induced r-regular, every outside vertex with 0, m or 2m
neighbours in C): counting the edges leaving C gives 2m(22 - r), counting the pairs of C through their outside common
neighbours gives at most 2m(2m - 1); as every outside vertex with neighbours in C has at least m of them,
(m - 1)(22 - r) <= 4m - 2, i.e. r >= 17, which forces at least (17^2 + 2)/2 = 145 vertices in C and then m >= 73 > 22.
So no such set exists. The same counting kills the WQH switching on two pairs (a vertex adjacent to a must be adjacent
to exactly one of b, b', but two non-adjacent vertices have only two common neighbours). The census is therefore done
with TRADES: free a region F, ask a solver for another completion (`trade_census.py`).

## 3. First measurements (`trade_census.py`, cadical; relabellings of F excluded)

| graph | region F | result |
|---|---|---|
| BvLS | a line (3 vertices) | rigid: UNSAT 0.3 s (new attachments), UNSAT 0.2 s (same attachments, other graph inside F) |
| BvLS | a 3x3 grid (9 vertices) | rigid: UNSAT 27.9 s and 0.8 s |
| BvLS | a closed neighbourhood (23 vertices) | NO DECISION in 200 s (1.4 million variables, 5.5 million clauses: the encoding is too heavy) |

## 4. Plan (in the order I would do it)

1. lighter encoding of the trade problem (the degree and common-neighbour counters dominate), then regions of 23 to 81
   vertices in the four graphs: closed neighbourhoods, unions of fibres, the three cosets of a hyperplane of BvLS with
   all the edges between cosets free ("re-gluing");
2. the mechanism: around a vertex p the second neighbourhood is the set of pairs {u, w} of neighbours of p on different
   lines, and the graph is coded by fixed-point-free involutions sigma_u; two lines through p span a 3x3 grid iff four
   of these involutions agree. What forces that with (1,2) alone?
3. Cayley graphs on the 67 groups of order 243 (partial difference sets (243,22,1,2)): are there vertex-transitive
   members without regular spread? (web search of 12/10: nothing specific found for these parameters.)
