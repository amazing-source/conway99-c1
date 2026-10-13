# Does the coclique frame (sizes 22 and 21) cover C1? (lab session, 13 October 2026)

Question asked before investing more in the family (0,2): what would its exclusion give for C1?

## 1. Logic (no computation)
Codex's line treats cocliques of size 22 (Hoffman bound, the 2-(22,4,2) borders) and maximal cocliques of size 21
(seven profiles, (0,2) first). If ALL these cases were excluded, the conclusion would be: a srg(99,14,1,2) has no
coclique of size 22 and no maximal coclique of size 21, hence its largest coclique has size at most 20.
That is not a contradiction. For sizes <= 20 the defect vector q has no small support (bound 64 at size 20) and the
frame says nothing. So the frame closes C1 only together with a proof that the largest coclique has size >= 21.
No such proof exists in the project (Codex's note, section 1, says so itself), and I do not know one.

## 2. The sister graphs: cocliques at the Hoffman bound are the exception
Hoffman bound for srg(243,22,1,2): 45. A coclique of size 45 <=> x in {0,1}^243 with (A + 5I) x = 5.1.

| graph | coclique of size 45 | largest coclique found by tabu search (lower bound only) |
|---|---|---|
| BvLS (Aut 3 849 120) | YES (found in 0.2 s) | 45 |
| twin | NO: integer program, and exhaustive search per vertex orbit (3 runs, about 0.45 M nodes each) | 39 |
| Gamma3 | NO (integer program) | not run |
| Gamma4 | NO (integer program) | not run |
| Gamma5 (vertex-transitive) | NO: integer program, and exhaustive search through one vertex (467 142 nodes) | 37 |
| 6th | NO (integer program) | not run |
| 7th | NO (integer program) | not run |
| 8th | NO (integer program) | 38 |

* "integer program" = HiGHS branch and bound through scipy (floating point, not a certificate), about 20 s per graph,
  log `hoffman45_milp_2026-10-13.log`; `hoffman45_milp.py`.
* "exhaustive search" = `hoffman45_dfs.py`, integers only, no solver: exact for the twin and Gamma5.
  (Unforced run on the 8th graph: not finished in 270 s.)
* Tabu search (`tabu_coclique.py`, 30 s per size): climbs from 37 to 45 on BvLS; stops at 39 / 37 / 38 on the twin,
  Gamma5 and the 8th graph. A lower bound only: the true maximum there is unknown (between these values and 44).
* Size 44 (the analogue of 21): NOT decided. `near_hoffman_milp.py` (defect law as linear constraints) and
  `defect_vectors_milp.py` (defect vectors first): no decision in 280 s and 270 s on Gamma5.
* Modular ranks, for the record: rank_2(A) = 110 for all eight; rank_3(A - I) = 67 (BvLS), 86, 90, 81, 84, 94, 95, 90.

So in this family the Hoffman coclique is a property of the exceptional member (rank 3 group, Golay cosets), absent
from the seven others. A statement "the largest coclique is at the Hoffman bound, or one below" cannot be a general
fact of the family (false at 243 for the bound itself); at 99 it would need an argument specific to 99.

## 3. Consequence for the plan
* A solver verdict UNSAT on (0,2), or on all seven profiles, would not close C1. Compute bought for it does not buy C1.
* The frame that does cover C1 in our notes is the rank ladder (NOTE of 12/10, 17.101 (6)): at ranks 37, 39, 41 a
  graph has an integral (-4)-eigenvector of norm 18 or 26; at rank 43, norm 18 or 26 or at least 1316 of norm 16.
* The two frames have the same shape: an integral vector u with (A - theta I) u = c.1 and a support S of 18 vertices
  (coclique (0,2): theta = 3, charges 2, 1, -1; norm 18: theta = -4, u = 1_P - 1_Q, A[S,S] bipartite 4-regular, 26
  cores), every outside vertex balanced against S, and H H^t = 12I + 2J - F^2 - F for H = A[S, outside].
  Codex's global model (common binary factorisation, closure lemmas, canonical forms) is written for exactly this
  shape. Pointed at the 26 norm-18 cores instead of the coclique support, each UNSAT would be a brick of C1.

Own code, not audited by a third party.
