# Order 2, Part I written in full: status (lab session, 13 October 2026, 23:01 UTC)

File: `order2_part1.tex` (866 lines, 14 pages; compiles with pdflatex, no warning, no overfull line; PDF beside it).
It is the hand part of the order-2 paper (`order2.tex`, draft of 7 October, Sections 3 to 6) written without gaps:
from an involution to Theorem R (a frame in an odd unimodular lattice of rank 24 without vectors of norm 1, every
vector outside the plane of the normals of energy at least 8). Same mathematics as the paper; the audit that
motivated it is `AUDIT_ORDER2_PAPER.md`.

## What is different from the paper
* The fixed vertex is called x_0, the vertices are never called u; the 49 orbits are indexed by a set Omega = I u O
  with explicit representatives (Lemma 4.1 gives the labelling the paper leaves to a figure caption).
* Proposition 3.1 is in seven steps; the double count n_2 = 2 sum r_x, the trace formula and the table of triples are
  displayed.
* Lemma 5.1 proves every property of S that the paper states in one sentence (symmetry, block form, the ten non-zero
  entries of a row of T, multiplicities).
* Lemma 7.2 proves det K = 7^g (the paper asserts it).
* Section 9 states the oddity formula in the exact form used, with the definition of the 7-excess, and separates:
  the parity computation (Lemma 9.1: the characteristic vector has norm 6 modulo 8), the Jordan decomposition at 7,
  the conclusion. The two forms over F_7 are defined intrinsically.
* The overlattice N_max is built from an explicit basis (Corollary 9.4), and the gluing map is explicit:
  the matrix (2 3; -3 2), with 2^2 + 3^2 = 13 = -1 modulo 7. The paper's appeal to "an anisotropic plane and its
  negative both have square determinant" is no longer needed there. The gluing lemma is proved in the text.

## What I checked
Every step was re-derived by hand twice (once when auditing the paper, once when writing). The statement of the
oddity formula was tested on five small lattices (Z^n, E_8, A_2, <7>, <7> + <7>): the two sides agree.

## Not verified, to check before showing the text to anyone
* The oddity formula and the definition of the p-excess are quoted from memory of Conway-Sloane, Chapter 15; the
  section numbers are not given and the wording must be compared with the book. The classification of quadratic
  forms over a finite field is cited as Serre, Chapter IV, section 1.7, also from memory.
* No one else has read the text. No numerical check on a real example was made (there is no graph to test on; the
  rook's graph 3x3 and the graph on 243 vertices of the same family could serve for the parts that do not use 99).
* The existence of a Jordan decomposition over Z_(7) is used as part of the cited theory.

## Not covered by Part I
The consequences of Theorem R used by the computer part (Lemmas 6.3 to 6.8 of the paper: generation, indecomposability,
new roots, characteristic vectors of norm 16, twins), the list of witnesses of energy 8, 9, 10, the three lemmas
T16, T18, T20, and the 156 lattices.
