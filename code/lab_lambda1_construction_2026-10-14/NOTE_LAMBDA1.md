# Constructing an asymmetric strongly regular graph with lambda = 1 (started 14/10/2026, about 13:00 UTC)

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

## 4. Why the S3 graph is rigid (user's question, 14/10 ~14:00 UTC): the concentration criterion (rigidity378.py)
**Lemma (proved here).** Let A, A' be srg with the same parameters, eigenvalues r > s, equal on every pair meeting
R = V - F. Let P (resp. P') be the orthogonal projection onto the s-eigenvectors of A (resp. A') that vanish on R. Then
(1) A' - A = (r - s)(P - P'); (2) P and P' have the same diagonal; (3) every changed pair {i,j} satisfies
P_ii P_jj >= 1 / (2(r - s))^2; (4) at most 4 (r - s)^2 P_ii pairs change at the vertex i. The same with the
r-eigenvectors.
Proof. A = r E_r + s E_s + (k/v) J and E_r + E_s = I - J/v for both graphs, so Delta = A' - A = (r - s)(E_s - E'_s).
Column x of Delta is 0 for x in R, so E_s e_x = E'_s e_x: the two projections agree on U = span{E_s e_x : x in R},
and Im E_s = U + Y, Im E'_s = U + Y' with Y = {y in Im E_s : y_x = 0 for x in R} (because <y, E_s e_x> = y_x) and the
same for Y'. Hence Delta = (r - s)(P - P') (1). Delta has a zero diagonal (2). Cauchy-Schwarz on the positive
semidefinite P and P' gives |Delta_ij| <= (r - s)(sqrt(P_ii P_jj) + sqrt(P'_ii P'_jj)) = 2 (r - s) sqrt(P_ii P_jj)
(3), and |Delta e_i|^2 <= (r - s)^2 (|P e_i| + |P' e_i|)^2 = 4 (r - s)^2 P_ii (4). QED
(This sharpens the support criterion of NOTE_SPREADFREE section 3: a trade needs eigenvectors of both eigenvalues
supported in F, AND concentrated enough.) Here r - s = 15: a pair can change only if P_ii P_jj >= 1/900.
Data on the S3 graph (s = -11, eigenspace of dimension 104 out of 378):
| region F | |F| | dim of (-11)-eigenvectors on F | best P_ii P_jj | verdict |
|---|---|---|---|---|
| X_m u X_m' | 138 | 1 (entries +-1/sqrt(120)) | 0.00007 | rigid (proved) |
| unions of 3, 4, 5 sets X_m | 183-256 | 2, 3, 4 | <= 0.00055 | rigid (proved) |
| union of 6 sets X_m | 277 / 291 | 5 / 17 | 0.0008 / 0.011 | rigid / not excluded |
| random | <= 270 | 0 | - | rigid (support criterion) |
| random | 280, 285, 290, 300, 310 | 6, 11, 16, 26, 36 | 0.004 - 0.036 | not excluded |
| geometric kept sets: N[v] (53 kept), N[v] u N[w] (98), X_m (78) | | similar to random sets of the same size | | no gain |
So on this graph a trade needs about 280 free vertices or more (98 kept or fewer), whatever the geometry: the
(-11)-eigenspace is small and its vectors are spread out (the X_m differences have support 120 with equal entries;
l1-minimal vectors through a vertex have support 275).
**Second layer (combinatorial).** Even where the criterion allows a trade, each free row is pinned by its counts with
the kept vertices: with 98 kept (N[v] u N[w]) every free vertex tested has ONE candidate row; Codex finds the same with
60, 75, 90 random kept vertices (only at 45 do the row lists stop closing). Information count: with mu = 8 a count with
a kept vertex carries about 3 bits, a row of a free vertex about 190 bits, so about 60 kept vertices determine it.
Conclusion: a local modification of this graph would have to free more than about 85 % of its vertices.

## 5. A unification: both multi-member lambda = 1 families are 3-ovoids of generalized quadrangles
An m-ovoid O of a GQ(s,t) (every line meets O in m points) has m(st + 1) points and induces a regular graph with
k = (t+1)(m-1), lambda = m - 2. For m = 3 (lambda = 1) the srg parameter identity forces mu = 4(t+1)/(3s-2).
GQ(2,2) -> (15,6,1,3), GQ(2,4) -> (27,10,1,5) (O = all points); GQ(5,25) -> (378,52,1,8) (hemisystems, mu automatic
by Cameron-Delsarte-Goethals); GQ(8,10) -> (243,22,1,2) (mu = 44/22 = 2; GQ(8,10) = Payne-derived / Ahrens-Szekeres
for q = 9: Codex's construction of 14/10, mu not automatic there). The families (q,q), (q,q^2), (q-1,q+1), (q^2,q),
(q^2,q^3) give no other integer mu. Conway's (99,14,1,2) is not of this form (st = 32 and 2t = 3s - 4 have no common
solution). So the stabiliser of O in Aut(GQ) acts on the srg (equality for the S3 graph), and an asymmetric member of
either family coming from a 3-ovoid needs a 3-ovoid with trivial stabiliser: at 378 none exists in the two known GQs
(Bamberg-Giudici-Royle classification); at 243 the question is open and is exactly Codex's search.
