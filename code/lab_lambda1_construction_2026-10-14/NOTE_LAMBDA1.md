# Constructing an asymmetric strongly regular graph with lambda = 1 (started 14/10/2026, about 15:00 UTC)

User (direct, 14/10): "personne ne parle de trouver un tel lambda 1 existant, je parle d'en construire 1, un SRG
asymetrique de parametre lambda 1. La 2eme condition, 2, pas necessaire pour l'instant." Codex works on the same goal
(bridge 653-663): mixed and random windows at 243 and on the 378 graph below, global lazy SAT at 243.

## 1. Landscape (feasible_lambda1.py + A. E. Brouwer's tables, read 14/10)
lambda = 1 means a partial quadrangle PQ(2,t,mu) (lines of size 3). Feasible parameter sets up to 3000 (integrality,
Krein, absolute bound): 19. Status in Brouwer's tables (v <= 1300):
| srg | status |
|---|---|
| (9,4,1,2), (15,6,1,3), (27,10,1,5), (81,20,1,6), (729,112,1,20) | exist, unique (GQ(2,1), GQ(2,2), GQ(2,4), Brouwer-Haemers, Games graph) |
| (57,14,1,4), (289,54,1,12), (507,44,1,4), (630,68,1,8) | do not exist (Wilbrink-Brouwer; Bondarenko-Radchenko; Koval + AI 2026) |
| (99,14,1,2), (115,18,1,3), (495,38,1,3) | open |
| (243,22,1,2) | exist, not unique (eight known, all |Aut| >= 108) |
| (378,52,1,8) | exist ("+", Cossidente-Penttila hemisystem) |
So only 243 and 378 have several known graphs.

## 2. The 378 family: hemisystems (ftwkb5.py, srg_group3.py, pq_invariants.py)
A hemisystem of lines of a GQ of order (25,5) (half of the lines through every point) gives srg(378,52,1,8)
(Cameron-Delsarte-Goethals; vertices = lines of the hemisystem, adjacent = concurrent). Bamberg-Giudici-Royle
(arXiv 1012.3819, Theorem 1.1, Tables 7-8): complete classification in the two known GQs of order (25,5): H(3,25): 2
hemisystems (stabilisers 15600, 15120); FTWKB(5): 3 complementary pairs (stabilisers 600, 120, 6 = S3).
Built here exactly: FTWKB(5) by the Knarr model over GF(5) (3276 points, 756 lines, axioms checked); hemisystem CNF
(756 variables, exactly 3 of 6 lines at each point, 98 280 clauses), cadical SAT in seconds; decoded graphs are
srg(378,52,1,8) (degrees 52, lambda {1}, mu {8}). Exact groups (WL alone is blind here: every mu-graph is a coclique;
initial colours = numbers of parallel lines and of lines joined by two edges): seed 1: |Aut| = 6 (vertex orbits 1,
2 x4, 3 x5 and 59 regular orbits of 6); seed 3: |Aut| = 600. The complementary hemisystem of seed 1 gives a graph with
the same line statistics but 342 pair colours against 347: not isomorphic to seed 1.
These are the least symmetric lambda = 1 srgs we know (243: at least 108). By the classification, no hemisystem of
the known GQs of order (25,5) gives an asymmetric graph: an asymmetric srg(378,52,1,8) must leave the hemisystem world.

## 3. Trades on the S3 graph (census_general.py = boundary census for any (v,k,lambda,mu); trade378.py, scan378.py)
X_m = hemisystem lines meeting a GQ line m outside the hemisystem (78 vertices): |N(v) & X_m| = 2 inside, 13 outside
(checked), so 1_{X_m} - 1_{X_m'} is a (-11)-eigenvector on 138 vertices (support criterion met). Complete censuses,
every pair meeting the kept set fixed:
| free region | free / kept | candidate rows per free vertex | completions |
|---|---|---|---|
| X_m u X_m' (opposite lines) | 138 / 240 | 1 | only the input |
| union of 3 sets X_m | 184 and 196 / ~190 | 1 | only the input |
| union of 4 sets X_m | 228 and 229 / 150 | 1 | only the input |
| random | 290 / 88 | row listing did not finish in 290 s | - |
The graph is rigid down to 150 structured kept vertices. Codex runs random kept sets of 90 and 75 on it.
