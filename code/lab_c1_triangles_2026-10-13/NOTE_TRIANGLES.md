# C1, triangle (line) Gram: what it gives and why it is a reformulation (lab session, 13 October 2026)

Status: checked by machine in its general form on two real graphs (243,22,1,2) (`check_line_gram.py`); the conclusions
below are hand arguments. Context: exchange with Codex on the coclique-21 profile (0,2); bridge messages 593, 595, 596.

## Facts (srg(99,14,1,2), 231 lines, N = points x lines, N N^t = 7I + A)

* 7 * 1_L^t E_- 1_M = 4 (L = M), 0 (L, M meet), 1 - j (disjoint, j edges). G = 4I + C_0 - C_2 - 2C_3 = 21 * projector of
  rank 44. Per line, f = number of parallel lines: n_3 = f, n_2 = 36 - 3f, n_1 = 144 + 3f, n_0 = 32 - f.
* 11 * 7 * 1_L^t E_+ 1_M = 180, 70, 11j - 18. Kernel of N: 210 * P_ker = 120I - 20B - 6C_0 + C_1 + 8C_2 + 15C_3.
* For a coclique C of 21 and q = 4*1 - (A+4I)1_C: E_- 1_C = 1_C + q/7 - (5/21) 1, and the line charge
  lambda_L = 7 * 1_L^t E_- 1_C = q_L - 5 + 7|L & C|; sum of lambda^2 = 2352, i.e. the variance budget 240.
* Delsarte-type positivity on the 231 unit vectors (inner products 1/4, 0, -1/4, -1/2 in dimension 44): degree 3 gives
  average f <= 10; degrees 4, 5 give nothing.

## Why none of this is a new constraint

* First order: X lambda = 17 lambda (X = C_0 - C_2 - 2C_3) is the vertex law A u = -4u in disguise; worked out on the
  negative triangle {e, f, t}: both sides equal -119.
* Spectral cuts on families of triangles: I = P_1 + P_+ + P_- + P_ker. P_- >= 0 and P_+ >= 0 on a family are the vertex
  cuts (3I - A + J/9 >= 0, A + 4I - 2J/11 >= 0) carried by N. P_ker >= 0 is, by Schur complement,
  7I + A - N_S N_S^t >= 0 = Gram of the lines not taken, implied by the count "open edges + triangles at v <= 7".
  So the upper cut G_S <= 21 I that I first announced as new is implied. (Retracted in message 596.)
* Example: m pairwise non-adjacent triangles: the E_+ cut gives m <= 11 (my first bound, 16, was weaker).

Conclusion: the line Gram is a reformulation of what the vertex cuts and the line counting already say. Anything
specific to triangles would have to be non-spectral. No such statement found.

## Addendum, 13 October 2026, 16:55 UTC: Codex's integral closure lemma, and his conjectures of notes 176-177

### A. Matrix form of the column identity (Codex's note, section 59)
Hypotheses as there: A = [[B, D], [D^t, E]] binary, symmetric, k-regular, k^2 = mu(n-1), both diagonal blocks of
T = A^2 + A - (k-mu)I - mu J zero, G = mixed block. Checked by an independent derivation: the column identity
||G_u||^2 = D_u^t (2B+I) G_u and the lemma "a column in the 0 or -1 eigenspace of B vanishes" are correct.
The matrix statement is the symmetrised one. With M = D^t G (symmetric, because D^t G = G^t D):

    G^t G = M + E M + M E.

Proof: G^t G = G^t (BD + DE + D - mu J), G^t B = (BG)^t = E G^t, G^t 1 = 0. Consequences:
(a) G^t G commutes with E; (b) M^2 = G^t G ((k-mu)I - E^2 - E); (c) G = 0 iff M = 0, and G vanishes on every
eigenvector of E whose eigenvalue is outside the open interval (s, r) = (-4, 3); (d) on a common eigenvector (E: t,
G^t G: sigma^2), sigma <= |2t+1| sqrt((k-mu) - t^2 - t), at most 49/4 for Conway.
Exact check on the pentagonal prism: `check_defect_matrix_identity.py` (all True; the bound (d) is attained there).
Scope: like the lemma itself, this constrains false defects of a partial model. It says nothing about true graphs.

### B. Test of the conjectures (G), (E), (L), (P) outside the family of covers
`fx_test.py`, log `fx_test_2026-10-13.log`. The implementation reproduces the table of note 176 on BvLS, the twin,
Gamma3 and Gamma4 (cycle types of F_x and types of (x,a)). On the four graphs without regular spread:

| graph | grids at x | long cycles of F_x | types of (x,a) not seen on the covers |
|---|---|---|---|
| Gamma5 | 25 | 20 | none |
| 6th | 17 | 8, 12, 20, 28, 32, 36, 40, 68, 72 | 1^3 3 4, 1^3 7 |
| 7th | 17 | 8, 16, 24, 40, 48, 64 | 1^3 3 4, 1^3 7, 1^5 5 |
| 8th | 19 | 8, 16, 20, 28, 32, 36, 40 | 1^3 3 4, 1^3 7, 1^5 5, 1^7 3 |

* (L) for l = 5: REFUTED (7th graph, 324 pairs (x,a); 8th graph, 432). l = 7 occurs too.
* l = 2 ("alternating square"): absent on all eight graphs.
* (G): holds on the four (number of 4-cycles of F_x = number of grids at every vertex).
* (E): holds on the four (no odd cycle).
* (P): holds on the four (every (x,a) has at least two components l = 1).
Caveat: seven of the eight graphs contain the same induced third, so the sample is not independent.

Link with C1: the type of (x,a) is the cycle partition of Codex's section 17 around an edge (induced 2-regular graph on
(N(x) u N(a)) minus the line, cycles of length 4l). If "no l = 2" and (P) were theorems, the eleven partitions of 6
would reduce to 51, 411, 3111, 1^6. They are NOT theorems.

### C. Attempt at "no alternating square": not closed
l = 2 at the edge x~a means two lines through x and two through a with each of the four cross pairs joined by exactly
2 edges. `square_pattern.py`, log `square_pattern_2026-10-13.log`: the same pattern for two NON-adjacent points x, y
occurs in the 8th graph (108 configurations), never for adjacent points (twin, 7th, 8th graphs). So no argument using
only the pairwise edge counts of these lines (their Gram in the -4 eigenspace) can prove the statement; the line x a
itself and the third layer must enter. The 10-vertex configuration is consistent with lambda = 1, mu = 2 locally, so
a proof must also use regularity. No proof and no counterexample found.
