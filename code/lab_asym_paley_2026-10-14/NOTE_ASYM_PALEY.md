# Asymmetry campaign: Paley 9 and Paley 25 (started 14/10/2026, about 10:40 UTC)

User's request (direct, 14/10): study "ultra microscopically" why Paley 9's parameters force symmetry and why Paley
25's family contains asymmetric graphs, keeping in mind ALL constraints accumulated on Conway's srg(99,14,1,2)
(list: CONWAY_CONSTRAINTS.md). Data: Spence's lists (maths.gla.ac.uk/~es/SRGs/, downloaded 14/10, sha256 in
section 0). All code here is mine, exact (no floating point, no external graph library).

## 0. Data and tools
* ../asym_paley_data_2026-10-14/spence/*.txt (sha256: 9-4-1-2 3231681e..., 25-12-5-6 9dfb06d5..., 26-10-3-4
  7052922c..., 29-14-6-7 d139e0a6..., 13-6-2-3 82a19b7a..., 17-8-3-4 e7134145...).
* srglib.py: reader, srg check, equitable refinement, exact automorphism group order (orbit-stabiliser chain with
  individualisation-refinement and backtracking), vertex orbits, canonical form.
  Controls: |Aut(Paley 9)| = 72, |Aut(Paley 13)| = 78, |Aut(Paley 17)| = 136, |Aut(Paley 25)| = 600 (all correct).

## 1. Facts (exact)
**1.1 Groups** (groups.py). srg(9,4,1,2): one graph (Paley 9 = 3 x 3 rook graph), |Aut| = 72, vertex-transitive.
srg(25,12,5,6): 15 graphs with |Aut| = 2, 1, 3, 1, 2, 2, 6, 6, 3, 6, 72, 2, 6, 72, 600 (Spence's order): two
ASYMMETRIC graphs (#2, #4); Paley 25 is #15. srg(26,10,3,4): 10 graphs, |Aut| = 4, 6, 6, 6, 2, 3, 39, 120, 2, 1
(one asymmetric, #10).
So the premise "Paley 9 is asymmetric" is reversed: srg(9,4,1,2) FORCES symmetry; asymmetry appears in the family of
Paley 25, not in Paley 25 itself.

**1.2 Microscopic invariants** (invariants.py, log inv25.log). Per graph: local graph types G[N(v)], lambda- and
mu-graph types, K4, maximum cliques/cocliques, spreads, 5-rank of A + 3I.
| graph | |Aut| | max cliques (size 5) | max cocliques | spreads | K4 | 5-rank(A+3I) | distinct local types |
|---|---|---|---|---|---|---|---|
| #15 Paley 25 | 600 | 15 | 15 | 3 | 75 | 9 | 1 |
| #14 | 72 | 15 | 3 | 3 | 79 | 11 | 3 |
| #11 | 72 | 3 | 15 | 0 | 79 | 11 | 3 |
| #10, #13 | 6 | 3 | 3 | 0 | 73 | 11 | 7, 8 |
| #7, #8 | 6 | 3 | 3 | 0 | 83 | 12 | 7, 7 |
| #3, #9 | 3 | 3 | 3 | 0 | 90 | 12 | 6, 5 |
| #1, #6 | 2 | 3 | 3 | 0 | 87 | 12 | 12, 12 |
| #5, #12 | 2 | 3 | 3 | 0 | 89 | 12 | 11, 10 |
| #2, #4 (asymmetric) | 1 | 3 | 3 | 0 | 89 | 12 | 17, 15 |
The geometric graphs (Latin square / net structure: 15 cliques, 3 parallel classes) are the most symmetric;
asymmetric ones have no spread, the maximal 5-rank seen (12) and many distinct local types.
Paley 9: local 2K_2, lambda-graph K_1, mu-graph 2K_1, 6 lines, 6 maximum cocliques, 2 spreads, 3-rank(A+2I) = 4.

**1.3 THE MECHANISM: regular two-graphs** (twographs.py, logs tw25.log, tw29.log). For a conference graph
(k = 2 mu) G on v points, G + an isolated point generates a regular two-graph T on v + 1 points; the descendant T_y
(switch to isolate y, delete y) is again a conference srg, T_x ~ T_y iff x, y are in one Aut(T)-orbit, and
Aut(T_x) = Stab_{Aut(T)}(x). Verified exactly: |orbit| x |Aut(descendant)| is constant = |Aut(T)| on every orbit.
* v = 9: ONE regular two-graph on 10 points, |Aut(T)| = 720, transitive: the descendant is unique (Paley 9) and has
  720 / 10 = 72 automorphisms. Symmetry of Paley 9 = point stabiliser of a transitive group of order 720.
* v = 25: FOUR regular two-graphs on 26 points: |Aut| = 15600 (Paley two-graph, transitive -> Paley 25 with 600),
  72 (orbits 12, 1, 12, 1 -> #10, #11, #13, #14), 39 (orbits 13, 13 -> #3, #9), and 6 (orbits 3, 6, 6, 3, 3, 1, 1,
  3 -> #1, #2, #4, #5, #6, #7, #8, #12). The two asymmetric graphs are exactly the descendants at the two REGULAR
  orbits (size 6 = |Aut(T)|) of the two-graph with the smallest group.
* v = 29: six two-graphs on 30 points, same law (many asymmetric descendants: two-graphs with groups 2, 6, 9).
**Statement.** In a conference family, a member is asymmetric iff it is the descendant at a point lying in a regular
orbit of the automorphism group of its two-graph. Paley 9's parameters cannot produce asymmetry because the only
two-graph on 10 points is transitive with point stabiliser of order 72. (Classical theory of Seidel-Taylor; the
verification and the orbit table are ours.)

**1.4 Local moves** (gm_switch.py, log gm25.log). Godsil-McKay switchings with a set of size 4 connect #1-#9, #12
(groups 1, 2, 3, 6) in one web that contains both asymmetric graphs; #10 <-> #13; #11, #14 only to themselves;
PALEY 25 HAS NO SWITCHING SET OF SIZE 4. Paley 9 has 18, all returning Paley 9.

**1.5 Refinement.** In every srg, individualising one vertex gives the equitable partition {v}, N(v), rest and nothing
more (checked on all 15 + Paley 9: always 3 cells): asymmetry is invisible to colour refinement at depth one; at
least two individualised vertices are needed.

## 2. The (1,2) family itself: torsion versus symmetry (torsion.py)
Torsion at x = number of pairs (neighbour a, other line through x) for which the matching M_a does not respect the
line (out of k (k/2 - 1)); 0 everywhere = Hamming points (affine structure).
| graph | |Aut| | mean torsion (of 220) | grids per vertex |
|---|---|---|---|
| Paley 9 (k = 4) | 72 | 0 (of 4: forced, a matching of 2 points is unique) | 1 |
| BvLS | 3 849 120 | 0 | 55 |
| Gamma4 | 3888 | 80 | 31 |
| 5th | 2916 | 108 | 25 |
| Gamma3 | 864 | 117.3 | 23 |
| 8th | 108 | 125.3 | 19 |
| 6th | 108 | 140 | 17 |
| 7th | 162 | 141.3 | 17 |
| twin | 4320 | 160 (3 Hamming points, 60 at 144, 180 at 168) | 55 / 19 / 13 |
Lower symmetry goes with higher torsion (the twin is the exception: a switched cover with three Hamming points). A
random choice of matchings would give about 208 of 220. Conway: torsion out of 84 per vertex; L8 forbids 0, L16
forces mean >= 14.2, the coherent profile of note 100 is maximal torsion 84; random matchings would give about 76.

## 3. What this says about Conway (with CONWAY_CONSTRAINTS.md)
1. The mechanism that produces asymmetric members at 25 (two-graph descendants, Godsil-McKay moves) is ABSENT for
   Conway: k = 14 != 2 mu (B7), and GM switching of size 4 is impossible in the family (1,2) for k >= 14 (B8). An
   asymmetric Conway graph cannot be reached from a symmetric graph by these local moves: it would be an isolated,
   intrinsically asymmetric object.
2. In the (1,2) family, symmetry decreases as torsion grows (section 2), Paley 9 sits at forced torsion 0, and Conway
   is forced away from 0 (L8, L16) and is asymmetric (B5): consistent with "asymmetry = high torsion".
3. Open question raised by 1.3: is there a "parent" object for (1,2) graphs (like the two-graph for conference
   graphs) whose point stabilisers are the automorphism groups? At 243 the regular-spread members are covers of BH
   srg(81,20,1,6); Conway has no regular spread (B6).

## 4. Next steps (proposed)
* 4.1 Ultra-microscopic study of the two-graph T6 (|Aut| 6) on 26 points: its triples, its orbits, how its regular
  orbits arise, and how T6 relates to the Paley two-graph (trades of triples).
* 4.2 The GM web: for each switching set, what it changes locally (local types, cliques), and which moves strip the
  last automorphisms.
* 4.3 In the (1,2) family: look for a parent structure (extension of the partial quadrangle by one point, Delsarte
  cliques of the extension) and test it on Paley 9 (extension = two-graph on 10 points?) and on the 243 graphs.

# Part 2 (14/10/2026, 11:10-12:10 UTC): how the automorphisms die, and the same law inside Conway's family

## 5. srg(25,12,5,6): the parents, explicitly (anatomy25.py -> anatomy25.log, anatomy26.py -> anatomy26.log)
**5.1 The parent groups as permutation groups on 26 points** (Aut(T)_p = Aut(T_p), plus one isomorphism T_p -> T_q
per point q of the orbit, extended by p -> q; every element checked on the coherent triples).
* T6: order 6, non-abelian = S3. Its 3 involutions each fix 6 points (5, 8 and one point of each orbit of size 3);
  its 2 elements of order 3 fix exactly the points 5 and 8. Orbits: 6, 6 (regular) -> #4, #2 (Aut 1); 3, 3, 3, 3 ->
  #5, #6, #12, #1 (Aut 2 = the involution fixing the point); 1, 1 -> #7, #8 (Aut 6 = all of S3).
* T39: Frobenius group 13:3 (26 elements of order 3, 12 of order 13); orbits 13, 13 -> #9, #3 (Aut 3).
* T72: non-abelian of order 72 (element orders 1:1, 2:21, 3:26, 4:18, 6:6); orbits 12, 12, 1, 1 -> #10, #13 (Aut 6),
  #11, #14 (Aut 72).
* Paley two-graph: order 15600 (= |PSigmaL(2,25)|), transitive -> #15 (Aut 600).
* The two-graph on 10 points behind Paley 9: order 720 with the element-order statistics of S6 exactly
  (1:1, 2:75, 3:80, 4:180, 5:144, 6:240; PGL(2,9) and M10 have elements of order 8): Aut(Paley 9) = point stabiliser
  of S6 on 10 points, order 72.

**5.2 Complements.** #2 <-> #4, #7 <-> #8, #1 <-> #6, #5 <-> #12, #3 <-> #9, #10 <-> #13, #11 <-> #14, #15 self.
So there is ONE asymmetric srg(25,12,5,6) up to complementation.

**5.3 The srg(26,10,3,4) in the switching classes.** T72: #1, #2; T6: #3, #4, #5, #9, #10; T39: #6, #7; Paley: #8.
The asymmetric srg(26,10,3,4) #10 also lies in T6. **Every asymmetric graph at 25 and 26 comes from the one parent
T6 = S3, by a choice (a point, or a regular graph of the class) in a regular orbit of S3.**

**5.4 Godsil-McKay moves obey the same law.** For every switching set D (170 sets), the stabiliser of D in Aut(G) is
contained in Aut(G') (0 violations): it is the group common to G and G'. Moves also CREATE symmetry: #1 -> #3 (Stab 1,
target Aut 3), #3 -> #7 (Stab 3, target 6), #1 -> #8 (Stab 2, target 6). The asymmetric #2 is one move away from
graphs with automorphisms of order 2 (#1, #6, #12) and 3 (#3, #9).

**5.5 A hand-checkable proof of asymmetry.** Colour each vertex by the isomorphism type of its local graph G[N(v)]
(12 vertices): #2 gets 17 colours (12 singletons), #4 gets 15 (11 singletons); equitable refinement of this colouring
is discrete, so every automorphism fixes every vertex. In all 15 graphs the refinement of the local-type colouring
equals the orbit partition exactly.

## 6. The same law inside Conway's family: srg(243,22,1,2) (pairgroup243.py, boundary243.py, firstorder.py)
Tools: 2-dim WL with the geometric initial colours of my aut_tools.py (12/10), refinement by all layers, every map
checked on every layer. All runs below take about one second each (logs pair243.log, pair243_twin.log,
boundary243.log, firstorder243.log).

**6.1 Trades (same labelled vertex set): group common to G and G' = stabiliser of the trade in Aut(G).**

| pair | pairs changed | vertices touched | lines exchanged | Aut(G), Aut(G') | common |
|---|---|---|---|---|---|
| BvLS -> twin | 1440 | 180 | 240 | 3849120, 4320 | 4320 (all of Aut(twin)) |
| fifth -> sixth | 1620 | 162 | 360 | 2916, 108 | 54 |
| fifth -> seventh | 2268 | 243 | 468 | 2916, 162 | 27 |
| fifth -> eighth | 2268 | 243 | 468 | 2916, 108 | 54 |
| sixth -> seventh | 648 | 81 | 108 | 108, 162 | 27 |
| sixth -> eighth | 648 | 81 | 108 | 108, 108 | 54 |
| seventh -> eighth | 648 | 81 | 108 | 162, 108 | 27 |

* The twin is "BvLS switched at a line L" (the 180 vertices far from L) and Aut(twin) = Stab_{Aut BvLS}(L)
  (3849120 / 891 lines = 4320): the exact analogue, in Conway's family, of a two-graph descendant (Aut = stabiliser of
  the chosen element), with a line in place of a point. BvLS is line-transitive, so this twin is unique.
* The fifth to eighth graphs share a common group of order 27 (9 orbits of 27): a core that no trade removed; each
  trade kept half or a sixth of the symmetry and created the rest (sixth: 54 kept, 54 new; seventh: 27 kept, 135 new).

**6.2 Boundary group versus number of completions** (block = 81 vertices; its inner pairs erased and the block marked;
completion counts from my exhaustive lists of 13/10; block stabilisers by blockstab243.py).

| graph, erased block | Aut(boundary) | completions | each completion keeps at least |
|---|---|---|---|
| fifth, block 2 (block 0 the same) | 3888 | 6 (fifth x4 = one orbit, Gamma4 x2) | 648 (the fifth: exactly 972 = its block stabiliser) |
| sixth, block 0 | 108 | 6 (sixth, seventh, eighth, twice each) | 18 (the sixth: exactly 54, orbit of 2) |
| sixth, block 1 | 54 | 1 | 54 (rigid) |

This is why every trade of 12-13/10 kept symmetry (and why "all 40 translations forbidden" was UNSAT on one block).

**6.3 Where the symmetry of a vertex lives: matchings (first order) or outer lines (second order).**
F_x = x, its lines, the outer vertices with their inner neighbours and the matchings M_a (the graph minus the edges
of the outer lines). Always Aut(G)_x <= Aut(F_x); the ratio is a lower bound for the number of completions of F_x.

| graph | Aut(G)_x versus Aut(F_x), by vertex orbit |
|---|---|
| BvLS (Hamming points) | 15840 vs 81749606400 = 2^11 11! (ratio 5160960) |
| twin | Hamming points 1440 vs 2^11 11!; orbit 60: 72 vs 1152; orbit 180: 24 vs 48 |
| Gamma3 | 32 vs 64; 8 vs 16; 8 vs 16 |
| Gamma4 | 48 vs 192; 24 vs 48 |
| fifth, sixth, seventh, eighth (no flat line, mean torsion 108-141 of 220) | EQUAL at every vertex (12; 4, 2, 2, 1; 2, 2, 2; 4, 2, 2, 1) |

At a Hamming point the matchings are fully symmetric and only the outer lines break the symmetry; in the high-torsion
graphs the matchings alone already carry exactly the stabiliser (including the trivial stabilisers of the orbits
of 108).

## 7. Three short proofs
**7.1 Forced-symmetry principle.** Let H be a partial structure (some pairs decided, the others free) and C(H) its
set of labelled completions. Aut(H) permutes C(H), and for X in C(H) the stabiliser of X in Aut(H) consists of
automorphisms of X. Orbit-stabiliser: |Stab(X)| >= |Aut(H)| / |C(H)|. Hence: if |C(H)| < |Aut(H)|, every completion
is symmetric; an ASYMMETRIC graph X satisfies |C(H)| >= |Aut(H)| for every partial structure H obtained from X by
freeing pairs (a nontrivial element of Aut(H) fixing X is a nontrivial automorphism of X).
Instances: Paley 9 (7.3: H = local skeleton, |C| = 1); two-graph descendants; GM moves (5.4); block trades (6.2);
first-order data (6.3).

**7.2 No Godsil-McKay switching set in the family (1,2) for k >= 14 (any size).** Let D, |D| = 2m >= 4, induce a
delta-regular graph, every vertex outside D having 0, m or 2m neighbours in D (n_0, n_m, n_2m such vertices).
Counting edges leaving D: n_m = 2(k - delta) - 2 n_2m. Counting pairs of D with a common neighbour outside D
(lambda = 1 for the m delta adjacent pairs, mu = 2 for the others, minus the 2m C(delta,2) paths inside D):
n_m C(m,2) + n_2m C(2m,2) = 2m(2m - 1) - m delta^2. Together:

    (k - delta)(m - 1) + m n_2m = 4m - 2 - delta^2.

For 2 <= m <= k the left side minus the right side is at least k(m - 1) - (m - 1)^2/4 - (4m - 2) > 0 when k >= 14
(at k = 14 it is 10m - 12 - (m-1)^2/4 >= 7.75 on [2, 14]; at k = 22 the same holds on [2, 22]); for m > k every
outside vertex has 0 neighbours in D, so D is a union of components: D = V and nothing is switched. (|D| = 2 only
swaps two vertices: an isomorphic graph.) At k = 4 the equation has the
solutions delta = 2 (D an induced C4) and delta = 1, n_4 = 1 (D = N(y)); all such switchings return Paley 9 (1.4).
This covers the GM switchings with one switching class (the form used in 1.4 and 5.4); switchings with several
classes C_1, ..., C_t (t >= 2) are NOT covered by this count.

**7.3 Why Paley 9 is forced.** In srg(9,4,1,2), N(x) = 2K2: two lines {x,a,a'}, {x,c,c'}. A non-neighbour y of x
has two common neighbours with x, not on one line (else y would be the third point of that line, i.e. x), so the 4
non-neighbours are the pairs [a,c], [a,c'], [a',c], [a',c']; the second line through a must be {a, [a,c], [a,c']}
(a has degree 4 and N(a) = 2K2), and the same at a', c, c'. Everything is forced: the 3 x 3 grid. The local group
(swap a, a'; swap c, c'; exchange the two lines; order 8) preserves this unique completion, so it lies in Aut, and
all vertices look alike: |Aut| = 9 x 8 = 72. In the language of 6.3: torsion is forced to 0, F_x has the full local
symmetry and a unique completion.

## 8. Confrontation with Conway (CONWAY_CONSTRAINTS.md, all items)
1. The two mechanisms that create asymmetry at 25-26 are impossible for Conway: no two-graph (k != 2 mu, B7) and no
   GM switching set of any size (7.2, B8).
2. The mechanism of Conway's own family at 243 (trades, line switchings) keeps the stabiliser of the move; to reach an
   asymmetric graph it needs a seed. For Conway no symmetric member exists at all (B5: literature + C2 + C3), so an
   asymmetric Conway graph cannot be reached from a symmetric one by ANY move; it would be an "orphan", unlike every
   asymmetric graph of section 5 (all children of S3).
3. The certificate of 5.5 is void for Conway: every local graph is 7K2 (A2) and all 4-vertex statistics are forced
   (A7). Vertices can first differ at the level of the matchings (torsion, A4). Paley 9 is the case torsion = 0 forced
   (7.3); Conway is forced away from it (no Hamming point, L8; mean torsion >= 14.2 of 84, L16).
4. 6.3 shows that in the high-torsion regime the matchings carry the whole vertex stabiliser. For Conway, by 7.1 (with
   Aut = 1): at every vertex x the matching data F_x has at least |Aut(F_x)| distinct completions (|W(B7)| = 645120
   is the largest possible group). If the outer lines are determined by the matchings at one vertex (unknown; at 243
   it holds up to symmetry in the four high-torsion graphs), then every matching system of a Conway graph is rigid
   under W(B7).
5. Usable form for exclusions: any piece H that is FORCED in a Conway graph and has c completions must have
   |Aut(H)| <= c; a forced piece with a unique completion must be rigid. A forced piece with more symmetry than
   completions excludes C1.

## 9. Next steps (proposed, nothing launched)
* (a) At 243: do the matchings at one vertex determine the graph? One solver run per vertex: about 23 650 free pairs
  and 5 million products, beyond a five-minute check; needs the user's go.
* (b) At 243: an asymmetric member of Conway's family, by freeing regions whose boundary group is small (6.2 says
  where: the sixth graph, around the orbit of 108 with trivial stabiliser). One-block runs take seconds.
* (c) For Conway: apply 7.1 to the forced pieces of the coclique / co-Heawood frames (a frame with at most 2
  completions must have a group of order at most 2).
