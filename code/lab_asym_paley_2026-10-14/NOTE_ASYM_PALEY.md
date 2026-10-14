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
