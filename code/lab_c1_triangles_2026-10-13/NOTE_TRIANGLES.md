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
