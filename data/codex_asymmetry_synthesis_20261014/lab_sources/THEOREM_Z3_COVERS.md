# The Z3-covers of the Brouwer-Haemers graph that are srg(243,22,1,2): exactly four

Lab session, 12 October 2026. Status: exhaustive computation with an orbit count; programs and outputs in this folder;
not yet reproduced by another session. It proves, and strengthens, the conjecture of note 165 s.4 bis of branch
`claude/v7-simultaneous` ("only four affine Z3-covers").

## Statement

Let Gamma be a srg(243,22,1,2) with a regular spread (a partition into 81 lines, two lines joined by 0 or 3 edges).
By lemma 1 of note 165 its quotient is the Brouwer-Haemers graph BH = srg(81,20,1,6), and Gamma is a 3-fold cover of
BH with gains in S3. Call the cover a Z3-cover if the fibres can be oriented so that every gain is a rotation
(the parity class of the gains is trivial).

**Theorem.** A srg(243,22,1,2) that is a Z3-cover of BH is isomorphic to one of four graphs: the
Berlekamp-van Lint-Seidel graph, the twin, Gamma3 (|Aut| = 864), Gamma4 (|Aut| = 3888).

**Corollary.** Any other srg(243,22,1,2), in particular an asymmetric one, has no regular spread, or is a cover of BH
with non-trivial parity class (then its monodromy is S3, by Codex's remark of 12/10). The Z3 route is closed.

## Proof

1. *Formulation* (Codex, `NOTE_RELEVEMENT_S3_QUADRATIQUE.md`, commit d9bc91a; the trivial-signing case, checked here
   on BvLS by `z3_linear.py`). Gains t -> t + b_xy, b in F_3, b_yx = -b_xy. The cover is a srg(243,22,1,2) iff
   (T) b_xy + b_yz + b_zx = 0 on each of the 270 lines of BH, and (L) for each of the 2430 non-adjacent pairs P, R the
   six values c_Z = b_PZ + b_ZR are 0, 1, 2 twice each. Gain functions differing by b'_xy = b_xy + a_y - a_x give the
   same cover; b and -b give isomorphic covers.
2. *Linear part* (`z3_linear.py`). Over F_3 the equations (T) have rank 270, with the first moments sum_Z c_Z = 0
   rank 657; the gauge has rank 80. In the gauge "b = 0 on a spanning tree" the solutions of the linear part form a
   space of dimension 73.
3. *Exhaustive search* (`z3_classify.py` writes the model, `z3cov.c` searches). The edges are ordered so that each is
   either determined by earlier ones or free; depth-first search over the 73 free edges; a pair is rejected as soon as
   one value occurs three times among its known c_Z, so a complete assignment has each value exactly twice. Symmetry
   b -> -b: the first non-zero free value is 1. The search is cut into the 64 944 alive assignments of the first 12
   free edges, run in nine slices that partition them (`OUTPUT_z3cov_run.txt`): 4.62e10 nodes, 1893 s of one core,
   **1154 solutions**, all distinct, hence 2308 gain functions in tree gauge.
4. *Orbit count* (`z3_orbit_check.py`, own stabiliser-chain routine). Aut(BH) x {+-1} acts on the gauge classes. The
   stabiliser of the class of a cover (Gamma, S) is Aut(Gamma)_S / Z3: an automorphism preserving the spread induces
   (g, e) with b_{gx,gy} = e b_xy + a_y - a_x, the a being determined up to a constant, and no fibrewise reflection over
   the identity exists for a connected cover. Each gauge class has exactly one representative in tree gauge. With
   |Aut(BH)| = 233 280 the four known graphs account for

   | graph | Aut | regular spreads (orbits) | stabiliser of a spread | gain functions predicted | found (flat grids) |
   |---|---|---|---|---|---|
   | BvLS | 3 849 120 | 11 (one orbit) | 349 920 | 4 | 2 x 2 (405) |
   | twin | 4320 | 1 | 4320 | 324 | 2 x 162 (45) |
   | Gamma3 | 864 | 1 | 864 | 1620 | 2 x 810 (117) |
   | Gamma4 | 3888 | 1 | 3888 | 360 | 2 x 180 (189) |
   | total | | | | 2308 | 2 x 1154 |

   The number of flat grids of BH (grids on which the gains are a coboundary) is an invariant of the orbit; for each of
   its four values the number of solutions found equals the size of the orbit of the known graph, so every solution
   lies in one of the four orbits. (`OUTPUT_z3_classify.txt`: the 1154 solutions split 162 / 810 / 180 / 2; one
   representative per value rebuilt as a 243-vertex graph and audited: parameters, 405 / 621 / 837 / 1485 grids, group
   orders 4320 / 864 / 3888 / 3 849 120.)

## What it depends on

* The equivalence in point 1 (Codex's lemma; elementary, re-checked on BvLS: all 2430 pairs give 0,0,1,1,2,2).
* The uniqueness of srg(81,20,1,6) (Brouwer and Haemers, 1992), used through lemma 1 of note 165: every regular
  spread gives this quotient.
* My programs. Controls: the search finds the four known covers with exactly the predicted multiplicities, which
  tests the model, the gauge, the search and the group orders at once; the Python original of the search and the C
  program agree on the first branch (92 solutions).

## What it does not say

Nothing about covers with non-trivial parity (S3-covers), nothing about graphs without a regular spread, nothing
about Conway's graph (which has no regular spread at all).
