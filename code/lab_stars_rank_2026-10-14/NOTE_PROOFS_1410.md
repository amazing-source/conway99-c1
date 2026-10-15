# Status board for the 49-vertex route (14/10/2026, evening; LAB with Codex)

User's rule (direct, about 18:45 UTC): prove, refute, and study the weak version; "absolutely everything". Tags:
PROVED (written proof) / VERIFIED (exact reproducible computation) / EVIDENCE / OPEN. Nothing moves up without a proof.

Notation. G = srg(99,14,1,2), v a vertex, letters = N(v) (mates x, x'), labels = far vertices z_xy (x, y non-mates),
L_x = star of x. A line l = {v,a,a'}; X_l = L_a u L_a' (24 labels); m = {v,b,b'} another line; S3 = X_l u L_b
(34 labels); S4 = X_l u X_m (44 labels); C4 = X_l n X_m = {ab, ab', a'b, a'b'}. T = 3I - Gamma - K on the 84 labels
(Schur complement of 3I - A after N[v]); T_S its principal submatrices. Admissible = (C1) star counts, (C1') partial
counts towards the other letters, (C2) lambda/mu caps inside S.

## PROVED
- P1. T^2 = 7T (hand proof via P^-1 1_{N[v]} = -2 e_v - 1/2 1_{N(v)}), so every T_S is PSD, <= 7I, rank <= 30.
  D T = 0 (star relations), hence T <= 7 Pi with Pi the projector onto ker D (Codex); U = 7 Pi - T is PSD.
- P2 (Lemma 0; Codex's self-contained proof: the block 3I - A[N[v]] is invertible, T is the global Schur complement,
  restriction to labels is an isomorphism E_3 -> ker T). For every line l, dim(E_3 supported on N[l]) = c(l) + 1,
  where c(l) = number of components of Codex's multigraph Q(v,l); this number does not depend on which point of l is
  called v. Line l is SPECIAL iff c(l) >= 2.
- P3 (Codex, sum of squares). For q = (f,g) on X_l orthogonal to the two star vectors:
  q^T T_X q = sum over the 24 edges of the 2-regular graph Gamma_X of (q_y - q_z)^2 + 1/2 |f - g|^2
  + 1/8 sum over mate pairs (s_x - s_x')^2, s = f + g. Hence T_X >= 0 always, rank T_X = 23 - c(l), and the relations
  carried by X_l are spanned by the two stars and the indicators of l x M_i, M_i the components of Q(v,l).
- P4 (closed configurations). For a set M of mu lines through v (l not in M), Y = l x M (4 mu labels):
  T 1_Y = 0 iff (i) every label of Y has exactly 2 neighbours in Y, (ii) the labels {a,x}, {a',x} with x outside M
  have none, (iii) every label {p,q} with p,q off l has exactly mu - c neighbours in Y, c = |{p,q} n letters(M)|.
  Equivalently the vector w with w_v = -mu, w = mu/2 on a, a', w = 1 - mu/2 on the letters of M, w = -mu/2 on the
  other letters of v, w = 1 on Y and 0 elsewhere is a 3-eigenvector of A (direct check of (Aw)_u = 3 w_u).
  (i)+(ii) say that Y is a union of cycles of Gamma_X (each label of X_l has exactly one tau- and one sigma-neighbour
  inside X_l); under positivity (iii) is forced (a relation of a principal PSD block is a relation of the whole).
  mu = 1: a closed square C4, straight (3x3 grid) or twisted (sigma swaps the two letters of m); both give T 1_C4 = 0.
- P5 (symmetry). If a letter permutation h fixing v, a, a', b preserves the three-star structure and moves some letter
  of N(v) - l, then l is special: pi_a, pi_a', sigma are h-equivariant, so the set of h-fixed letters (which contains
  b, b' and is a union of lines) is invariant, hence a union of components of Q. So symmetric families cannot produce
  counterexamples to (A).
- P6 (MIXED RELATIONS, mine; under review by Codex, message 722). In a Conway graph, for every vertex v and lines
  l != m through v: nullity T_S4 >= 14; ker T_{X_l}, ker T_{X_m} lie in ker T_S4 (PSD), of dimensions c_l + 1, c_m + 1;
  their intersection is span(1_C4) if C4 is a closed square and 0 otherwise (by P3 a kernel vector supported on C4
  forces {m} to be a component of Q(v,l)). Hence the number of MIXED relations (outside ker_l + ker_m) is
  >= 12 - c_l - c_m + [square(l,m)] >= 1 (c <= 6, and c_l = 6 forces a square with every other line).
  At least 1 mixed relation for every pair of lines at every vertex; at least 10 if both lines are non-special.
- P7 (Codex). Exact downdate criterion: from T PSD of rank 30 with kernel <stars, q>, a star-preserving rectangle
  T' = T - sigma(ab^T + ba^T) gives, with r = a.q, s = b.q, delta = -2 sigma r s > 0, w = s a - r b:
  eta = delta - w^T T^+ w > 0: PSD rank 31; = 0: PSD rank 30 with a new relation; < 0: indefinite.
- Earlier today: flip theorem and Codex's majority theorem (NOTE_ASYM_WINDOW.md sections 3 and 6).

- P8 (special = disconnected; interlacing). For a line l, the 36 vertices adjacent to l (off l) induce a cubic graph
  H_l (each has its line-mate and one neighbour in each of the two other groups). l is special iff H_l is
  disconnected iff lambda_2(H_l) = 3. Proof: lambda_2(H_l) <= lambda_2(A) = 3 by interlacing; if equal, the second
  eigenvector y (orthogonal to 1) extended by zero has Rayleigh quotient 3 and is orthogonal to 1, so it lies in E_3
  (Courant-Fischer equality, 14 > 3 > -4); conversely a 3-eigenvector of A supported on N(l) - l is constant on the
  components of H_l. Components have 6 mu vertices (mu lines through each point of l) and every vertex at distance 2
  from l has exactly mu neighbours in each component. (Same count as Codex's c(l): components of H_l project onto the
  orbits of <mates, pi_a, pi_a', sigma>.) Spectral corollary: the 60 vertices far from l induce an 8-regular graph with
  eigenvalue 3 of multiplicity exactly 18 and -4 of multiplicity exactly 7 + c(l) (eigenvalue correspondence
  theta <-> -1 - theta between complementary vertex sets of an srg; checked with trace and trace of squares).
- P9 (no twisted squares). A 6-vertex component (mu = 1) is always a straight 3x3 grid: in the twisted square, z_ab
  would be adjacent to z_ab' and to z_a'b', two labels containing b', while mu(z_ab, b') = 2 allows exactly one (the
  second common neighbour after b). The generator's partial counts (C1') exclude it.

- P10 (spectral form of our positivity conditions; LAB, message 731 to Codex). For Sigma = N[v] u S (S a set of labels)
  and A_Sigma the induced graph: nullity T_S = multiplicity of 3 in A_Sigma; T_S >= 0 iff lambda_2(A_Sigma) <= 3;
  U_S = 7 Pi_S - T_S is the Schur complement of 4I + A_Sigma with respect to N[v], so U_S >= 0 iff lambda_min(A_Sigma)
  >= -4 and nullity U_S = multiplicity of -4. Proof: Haynsworth inertia; A[N[v]] = F7 (windmill) has spectrum
  (1 +- sqrt 57)/2, 1^6, -1^7, so 3I - F7 has exactly one negative eigenvalue and 4I + F7 > 0;
  (3 - X)^-1 + (4 + X)^-1 = 7 (12 - X - X^2)^-1 and the letter block of (12 - X - X^2)^-1 is (11I + J - Mt)^-1 =
  (D D^T)^-1, hence T + Schur(4I + A) = 7 Pi. Consequences: (i) interlacing gives, in a Conway graph, mult_3(A_Sigma) >=
  |Sigma| - 45 and mult_-4(A_Sigma) >= |Sigma| - 55; (ii) for F = {p : N(p) contained in Sigma}, the vectors
  (A + 4I)(e_p - e_q) and (A - 3I)(e_p - e_q), p, q in F, are eigenvectors of A_Sigma for 3 and -4 (direct check using
  A^2 = 12I - A + 2J on the columns of F); at three stars F = {v, a, a', b} gives 3 + 3, so the only forced excess is ONE
  3-eigenvector (four stars: ten, as P6); (iii) every eigenvector of A_Sigma for 3 or -4 that is orthogonal to 1 is a
  global eigenvector in any extension (Rayleigh), whence column conditions on both sides. Second subconstituent form:
  Gamma (84 labels) preserves St = span(1_{L_x}); Conway iff D Gamma = 2J - D - Mt D and Gamma^2 + Gamma - 12I =
  2J - D^T D; on ker D, Gamma has only the eigenvalues 3 (x40) and -4 (x30).
- P11 (grids are perfect codes). A 3x3 grid G (induced K3 x K3) in a Conway graph is mu-closed, so no outside vertex has
  two neighbours in G (adjacent pair: lambda; non-adjacent pair: mu); counting 9 x 10 = 90 = 99 - 9, every outside vertex
  has EXACTLY one neighbour in G. Equitable partition {g} u O_g (O_g = the 10 outside neighbours of g): O_g - O_h is a
  perfect matching if g ~ h and 2-regular bipartite if g, h are non-adjacent; quotient spectrum 14, 3^9, -4^8.
  11 * 1_G - 1 lies in E_3; N pairwise disjoint grids need N <= 9 (Gram matrix in E_3).
- P12 (F2 code; Codex's lemma, checked by hand, strengthened). A = E1 (mod 2) since E1 = (A + 4I)(A - 14I)/(-77) is
  2-integral and 14 E0 - 4 E2 = 14J/99 - 2(A - 3I)(A - 14I)/63 is even; so C = im_F2(A) = Fix(A) has dimension exactly 54,
  F2^99 = C + ker_F2(A) (orthogonal), every primitive integral 3-eigenvector has >= 8 odd coordinates (Codex: words of C
  have even weight w >= 2 + (k - 2)/mu = 8), and ker_F2(A) also has minimum weight >= 8.
- P13 (rank form of specialness). With N_l the 36 x 60 incidence between H_l and the far set of l:
  N_l N_l^T = 12I - A_H - A_H^2 + 2J - P_groups, which equals (3 - A_H)(4 + A_H) on the group-sum-zero space (A_H
  preserves it), so rank N_l = 35 - c(l) and ker N_l (dimension 25 + c(l)) is the sum of the 3- and -4-eigenspaces of the
  far graph D_l. Remark: the coincidence 'degree of H_l = eigenvalue r = 3' happens only for k = 14 in the family
  srg(k^2/2 + 1, k, 1, 2); for k = 22 (243 graphs) the analogous factor (4 - A_H)(5 + A_H) is definite, so 'special'
  (H_l disconnected) has no spectral meaning there.

- P14 (binary relations at three stars; ChatGPT session shown by the user, 14/10 about 20:30 UTC; every step re-checked
  by LAB). Stars 0, 1 (mates) and 2 (mate 3). If the base L_0 u L_1 is connected (c = 1), then
  ker T n {0,1}^34 = {0, 1_L0, 1_L1, 1_L0 + 1_L1, 1_L2}, using only (C1) and Gamma >= 0 (no positivity, no C1', no C2).
  With T >= 0 and c components there are exactly 2^c + 2^(c-1) + 2 binary relations (unions of base components Y,
  Z - 1_Y with C4 in Y, Z = sum of the three stars, and the two stars L_0, L_1), spanning dimension c + 2.
  Key identity, valid for EVERY integral q in ker T: (Gamma q)_ij = 3 q_ij + (2w - t_i - t_j)/8, with w = sum q,
  d_i = sum of q over the labels containing i, t_i = 3 d_i + d_i'. The letter graph of S is connected with the triangle
  0, 2, 4, so all t_i are congruent mod 8, 2t = 2w (mod 8), d_i = d_i' (mod 4), w = 0 (mod 4); for binary q the outer
  pairs are all even or all odd, and a finite case analysis (parity of the matching tau_0 on L_0 n supp(Z - q) kills the
  profile (m_0, m_1) = (4, 4)) gives the classification. LAB complement: (t_i - w)/8 is exactly the value of the global
  3-eigenvector on the letter i and -w/4 its value on v (w_i + w_j = g_i + g_j on every label, letter graph connected
  and not bipartite), so the extension of an integral relation is integral iff t = w (mod 8), and otherwise all 14
  letter values are half-integers. Scope: binary relations only; (A) needs ALL rational relations (ChatGPT's example
  M = v v^T / 2, v = (1, 2, -3), shows positivity alone does not make a kernel binary-spanned). Consistent with Codex's
  exclusions of relations z = 2q + u with few odd entries (messages 728-732).

## LITERATURE (checked 14/10 evening; statuses are those of the sources, not re-proved here)
- Makhnev, Mat. Zametki 44(5) (1988) 667-672 'Strongly regular graphs with lambda = 1': according to Reimbayev
  (arXiv 2409.10620, 2508.03377), srg(99,14,1,2) does not exist if every pair of triangles joined by two edges is joined
  by three (i.e. n_2 = 0 below). With n_e = number of pairs of disjoint lines joined by e edges, a Conway graph has
  n_2 + 3 n_3 = 4158 (= 2 x 2079 quadrangles; checked), hence n_2 > 0 and at most 1385 prisms. Not read in the original.
- Lou and Murin (MIT PRIMES 2014, 'On the strongly regular graph of parameters (99,14,1,2)', Thm 2.1): the 3x3 grid
  minus an edge is not an induced subgraph (completion lemma via the Wilbrink-Brouwer identity). High-school report,
  proof not re-checked. It does NOT exclude grids.
- Reimbayev (arXiv 2508.03377): all 6-vertex induced subgraph counts of srg(n,k,1,2) are affine in one free parameter
  (n_2 in our notation); 7-vertex counts (arXiv 2608.19410) in two parameters.
- Thakkar-Severini (arXiv 2608.11211): the 84-vertex reduction, CP-SAT inconclusive, interlacing listed as future work.
- No source found on 3x3 grids, special lines, or spectral positivity of local objects.

## STATEMENT (A) IS FALSE (VERIFIED exactly, 14/10 about 20:55 UTC)
- counterexample_A_1.json: admissible three-star structure (stars 0, 1 mates and 2) with c(l) = 1, rank T = 30,
  T >= 0 and U >= 0. Exact independent verifier verify_counterexample.py (Fractions only, K re-derived from its
  formula, Pi from D, no search code imported): (C1) exact towards 0, 1, 2, (C1') towards the other letters, (C2)
  caps; the three stars in ker T; rank T_X = 22 so c(l) = 1; rank T = 30 with a 30 x 30 principal submatrix positive
  definite (exact LDL pivots), hence T >= 0; U = 7 Pi_S - T of rank 31 with a 31 x 31 positive definite principal
  submatrix; nullity 4 = three stars + one relation. 52 distinct candidates of the same kind (numerically PSD) in
  counterexamples_A_all.json (entry 38 = the verified one); all in the family invariant under
  h3 = (0 1)(4 5)(6 7)(8 9)(10 11)(12 13), relation in the even sector.
- How it was found (the user's 'look at why the door closes'): (i) det(8T[J,J]) = 2^73 x a random-looking integer of
  about 1e10, divisible by 3, 5, 7, 11, 13 at random rates (det_primes.py): no arithmetic mechanism; (ii) without
  positivity, c(l) = 1 rank-30 structures appear within seconds under the swap a <-> a' (sym_exact.py; Codex found
  non-symmetric ones of weights 16 and 24); (iii) the swap is the only symmetry compatible with c(l) = 1 (P5); it
  splits T into even/odd sectors, the extra relation lives in the even sector, whose B-part is constant on mate pairs
  (a 4 x 4 determinant), and the even sector can be PSD; (iv) a sector-targeted walk (mode zero) found PSD ones.
- The counterexample does NOT extend: outside labels {4,6}, {4,7}, {5,6}, {4,12} have 5335, 5675, 5675, 4963 local
  profiles and none of norm exactly 20 (colnorm_arith.py; each label alone is fatal), like z2b, the Z5 objects and
  dec_81..84. The values norm - 20 have 2-adic valuation >= 2 with a geometric tail: no arithmetic pattern.
- Four stars, partial-star identity (PROVED; checked numerically on 5 structures): for the outer letters x and
  d_x = indicator of the labels of S4 containing x, D T D^T = 6I + 2(J - Mt) - E with
  E[x][y] = #{(a,b) in {0,1,2,3}^2 : ax ~ by} (sum of K over the 16 pairs = -2 + 6[x=y] + 2[y=x']). So T >= 0 forces
  E <= 4 on mate-symmetric vectors orthogonal to 1 and E <= 8 on mate-antisymmetric ones. The four-star structures
  closest to positivity saturate E = 4 exactly; their remaining negative direction lies in the fine space ker D_S
  (lambda_max of the compressed Gamma = 3.0046 > 3).
- Consequence: the route '(A) => every line special => Case I enumeration' is closed. Remaining local candidates:
  H4' (two non-special lines at a vertex: four-star object with c(l) = c(m) = 1, T, U >= 0, nullity >= 14) - under a
  Z2 x Z2 symmetry, without positivity, exact nullity 11 reached (sym4g.py); and H4 (no PSD four-star structure at
  all, which would exclude Conway): full model, 160 500 Z5-invariant structures, best -0.0041, no PSD; searches in six
  symmetry classes running (h4_*).

## H4 IS FALSE (VERIFIED exactly, 14/10 about 21:12 UTC); new candidate (A4) (EVIDENCE only)
- psd4_candidate_1.json (= lab_exchange psd4_H4_false_1.json): admissible four-star structure (stars 0,1,2,3) with
  T >= 0 (rank 34) and U >= 0 (rank 40), exact certificates (verify_counterexample.py ... edges 0,1,2,3);
  c(l) = 3, c(m) = 4, nullity 10. Not a Conway object (rank must be <= 30), but positivity alone is possible.
  Found in G1 = <(0 1)(4 5)(6 7)(8 9)(10 11)(12 13), (2 3)(4 5)(6 7)(8 9)(10 11)(12 13)> (sym4g.py psd anyc);
  that family then gave more than 250 numerically PSD structures, ALL with c(l), c(m) >= 3 (mostly (4,4), components
  mu = (1,1,1,3), i.e. three grids per line; psd4_candidate_1 has two grids on l and three on m).
- With c(l) = 1 forced (sym4g.py psd cl1, families G1, G1c, h3, line swaps): best min(lambda_T, lambda_U) about
  -0.07 (c(m) = 4) after thousands of moves; no PSD. T alone reaches -0.003 with c = (1,1) but U stays at -0.16.
- Exact nullities of the first 400 PSD four-star structures (G1 family): c = (4,4) gives nullity 11 (141) or 12 (257)
  while the base components give 10, so 1 or 2 MIXED relations come with positivity; c = (3,4) gives nullity 10
  (9 local + 1 mixed). The real local condition of a Conway graph (T, U >= 0 and nullity >= 14) is still 2 short.
  Fine-space spectrum (fine_scan.py): all 111 tested (4,4) PSD structures have spec(Gamma_F) in [-4,3]; with c = (1,1)
  only 1 of 19 near-PSD structures does, so the fine spectrum alone does not explain (A4).
- Sector-targeted search (sym4g.py modes sector / urepair; sector_spec.py gives exact nullities per character block
  (++, -+, +-, --) of G1), 14/10 21:36-21:45 UTC. Exact facts (Fractions):
  sc_7_null14.json: c = (5,5) (four grids + one mu = 2 component per line), nullity 14 = (10,1,1,2), RANK 30, T >= 0
  (lambda_T = 0.2378), U NOT PSD: -0.0746 in the -+ and +- blocks only.
  sc_2_null14.json: c = (6,6), nullity 16 = (11,1,1,3), T >= 0 (0.8377 = 4 - sqrt 10), U = 3 - sqrt 10 in -+ and +-.
  sc_6_null14.json: c = (6,6), nullity 14 = (11,1,1,1), T = U = 2 - sqrt 5 (in -- for T, in -+/+- for U).
  null13.json: c = (5,5), (10,1,1,1), T -0.19 (-+) and -0.03 (--), U -0.0105 (-+). h4g_2_PSD_171: (9,1,1,1), PSD.
  Reading (EVIDENCE, G1 only): T wants many grids, U breaks with many grids, always in the -+/+- blocks; the U-negative
  direction is spread over all line pairs (no small forbidden subgraph). Walking on the plateau 'nullity >= 14 and
  T >= 0' (urepair) never raised lambda_U above -0.0746. The real local condition (T, U >= 0, rank <= 30) is neither
  found nor excluded; in asymmetric families positivity at four stars was never reached at all.
- FORCED-PROPERTY PROGRAMME (user, 14/10 about 21:50 UTC: no more 'nothing says Conway must...'; find what every Conway
  graph MUST have and why). Exact forced identity (G9 of CONWAY_CONSTRAINTS): rank T_S4 = 30 - delta, delta = mult of -4
  on the 40 outer labels, so mixed relations = 12 - c(l) - c(m) + [grid] + delta exactly; rank T_S3 = 30 - delta'.
  Bridge target (OPEN): transversals t(l) = fixed points of sigma_l, P = (1/2) sum t(l) <= 852 (Codex's order-9 census,
  11088/13) forces mean t <= 7.38. If the four-star condition (T, U >= 0, rank <= 30) forced t(l) + t(m) >= 15 at every
  pair of lines, summing over the 21 pairs at each vertex gives sum_l t(l) >= 1732.5, i.e. P >= 867 > 852: no Conway.
  Data (G1 only): every PSD four-star structure has t(l) + t(m) >= 10 ((4,6) once, (6,6) 89 times); with t <= 4 per
  line no PSD after 10 000 moves (tcap2, tcap4a/b), with t <= 6 PSD but nullity <= 12; the rank-30 T-PSD structure
  has (8,8). Caveat: in G1 relations come from grids (two transversals per grid); in an asymmetric graph rank 30 could
  come from mixed coincidences without transversals; the no-symmetry runs with forced transversals (nosym_t*) test
  the positivity part. odd_gram.py: the T-Gram of e_x = 1_{0x} - 1_{1x}, f_y = 1_{2y} - 1_{3y} is
  [[6I - J/2 - P_tau0 - P_tau1 + P_sigma + P_sigma^T, -C], [-C^T, ...]] (transversals add 2 on the diagonal); the
  resulting nuclear-norm inequality ||C||_* <= sqrt((66 + 2t(l))(66 + 2t(m))) is forced but far from binding (30-44
  vs 66-86).
- WHY local spectral statements keep failing (analysis, 14/10 22:10 UTC). For a symmetric matrix M on a label set, the
  local conditions 'T_S >= 0, U_S >= 0, rank T_S <= 30, rank U_S <= 40' are the necessary conditions for M to be a
  principal block of SOME real matrix 7P (P an orthogonal projector of rank 30 inside the 70-dimensional fine space),
  and by the dilation theorem for contractions they are close to sufficient for such a REAL extension (the precise
  completion statement with the fixed Pi is not proved here). So the local conditions test 'spectral realizability'; the real
  obstruction of the Conway problem is that the dilation must also have the 0/1 shape of an srg. This is why every
  purely spectral local statement we tested ((A), H4) turned out satisfiable once a symmetry made the coincidences
  cheap, and why random searches without symmetry never even reach positivity at four stars (the spectrum of a
  'random' piece is spread, the dilation needs it concentrated in [0,7]). Consequence for the method: a contradiction
  must use the 0/1 structure (codes, counts, extension conditions) together with the spectrum, e.g. the bridge
  'positivity => transversals' combined with the census bound P <= 852.
- No-symmetry four-star searches (identity group, psd mode, about 6000 moves, cooled): best min(lambda_T, lambda_U)
  -0.38 with no constraint; -0.49 / -0.51 with 6 / 8 transversals imposed per line (prisms alone do not help);
  -0.20 / -0.17 / -0.14 with 2 / 3 / 4 grids imposed per line (FORCE_GRID_L/M; one 3-grid structure has U >= 0);
  forced (2,2,2) closed configurations without grids stay near -1.0 (their column conditions are not met by random
  moves: a kernel vector of T_X with T_{B,X} y != 0 makes T_S4 indefinite, so PSD requires the P4 column conditions).
  No PSD four-star structure without symmetry so far. G1 transversal caps (tcap*): t <= 2 or 4 per line never PSD in
  15 000 moves; t <= 6 PSD with nullity <= 12. EVIDENCE for the grid bridge, not a proof.
- Sanity check of the complementary identity G9 on a real srg(243,22,1,2) (twin243_switched, v = 0, three pairs of
  lines): dim(E_4 n R^Sigma) = 5 = |Sigma| - 111 + mult_-5(complement) = 99 - 111 + 17 in all three cases.
- NEXT (Codex, message 754 reply, not re-audited): in G1 the 44 labels form 11 regular Klein-4 orbits, four character
  blocks of size 11; stars give nullities (2,1,1,0) in (++,-+,+-,--); the trivial block has rank >= 6 - min(c_l, c_m),
  so rank T <= 30 forces the three non-trivial blocks to carry nullity >= 9 - min(c_l, c_m); ten minimal targets
  (1+a, 1+b, c), a + b + c = 3 for c = (4,4). To do at restart: target these sector nullities in sym4g.py (blocks
  B^t T B / 4 of Codex's four_star_g1_sectors.py), warm starts h4g_2_PSD_171.json (nullity 12) and null13.json.
- (A4) FALSE (E4, 14/10 23:30 UTC): T, U >= 0 at four stars does NOT force c(l), c(m) >= 2 (an exact PSD structure
  has c(m) = 1). Had it been true it would have made every line of a Conway graph
  special, i.e. exclude the 'generic, prism-poor' regime that no local lemma touches (CONWAY_CONSTRAINTS.md, F).
  Combined with the known grid bounds (rho <= 126 grids, g(x) <= 17 per vertex, no Hamming point, kk5/kk6) a
  stronger form ('at least three grids per line') would give at least 11 grids per vertex by parity (the sum over
  the 7 lines at x of their grid counts is even), hence rho >= 121: not yet a contradiction.

## VERIFIED (exact computations; files in this folder)
- line_pairs.py on the eight srg(243,22,1,2): n_2 = 0 only for BvLS (8910 prisms, 1485 grids, every prism in a grid);
  the seven others have n_2 = 9720 to 19440 and 405 to 837 grids, yet every line is special in all eight. So the census
  below is not an artefact of the extreme case n_2 = 0; but by P13 it has no spectral analogue for 99 either.
- Census (line_components.py): in the EIGHT known srg(243,22,1,2) every one of the 891 lines is special, and every line
  lies in at least one grid (a 6-vertex component of H_l). Caveat: the eight graphs are related (covers, trades); the
  similar observations of notes 176-177 (grids, prisms) stayed unproved and may be artefacts of the construction.
  Paley 9 (m = 2): every H_l is connected (one 6-vertex component).
- Four stars, positivity: forced grid on (l, m) (best lambda_perp -0.35), both lines forced decomposable (best -0.31 to
  -0.47): still never PSD; the only PSD four-star structure seen came from the Z5 enumeration with the old model (being
  re-checked with C1' and U).
- Z5-invariant three-star structures: rank 30 by the forced grid; 595 PSD and 572 with T and U PSD among the first
  10 000 (z5_valid_all.json). Codex's column filter kills all 572 (75 by a cap, 496 empty domain at {3,4}, 1 at {3,5}),
  plus EX0, EX2, V0, V7, V15 earlier.
- H3 ("rank 30 at three stars forces the grid") is FALSE: z2b.json (rho = (4 6)(5 7)(8 10)(9 11)), admissible
  (C1, C1', C2 re-checked), T and U PSD, exact rank 30, no grid; its relation is 1_Y with Y = l x M, M = two lines
  (an 8-cycle): a closed configuration with mu = 2 (P4). Its 49-vertex object does not extend: Codex's column {3,4}
  has no profile of norm exactly 20 (0 of 1112).
- Four stars: random, annealing and extension never reach T >= 0; Z5 enumeration (old model, without C1') found ONE
  PSD structure (lambda_perp 0.032, exact rank 39) after about 110 000; being reproduced with the full model.
- Without positivity, mixed relations exist: Z5 four-star structures with nullity 6 (5 of 300), parity pattern.

## 14/10 LATE EVENING (22:25 UTC 14/10 to 00:00 UTC 15/10): positivity at four stars is satisfiable; every witness fails another forced condition (rank 30, rank_7 <= 28, or extension)
- E1 (VERIFIED exactly; verify_counterexample.py night_urep_PSD_100.json edges 0,1,2,3): an ADMISSIBLE four-star
  structure with T >= 0 of rank EXACTLY 30 (30 x 30 block positive definite, LDL) and U >= 0 of rank 40, c = (5,5),
  family G1, sector nullities (10,1,1,2) (found by the U-repair walk sym4g.py urepair from sc_7; 586 hits, one
  spectral fingerprint). So admissibility + T, U >= 0 + rank <= 30 at ONE four-star object cannot exclude Conway.
- E2 (VERIFIED exactly; ext4.py, log ext4_urep100.log): rank 30 means the 44 vectors span the whole 30-space, so every
  outer label u has its vector fixed by its profile nb = N(u) n S4: (Tr) p = T(S,u) orthogonal to ker T_S (exact integer
  test) and (Tn) p^T T_S^+ p = 5/2 (Fractions). For ALL 40 outer labels: 995 to 3055 admissible profiles, 0 to 16 pass
  (Tr), 0 pass (Tn). The object is in no Conway graph. (This is the star-complement reconstruction for the eigenvalue
  3: N[v] u I with T_I nonsingular is a star complement, 45 = 99 - 54 vertices.)
- E3 (VERIFIED; disc_test.py and latdisc.py agree): lattice of the 44 vectors, Gram 8T: disc = 2^73 3 5^5 17^2;
  Gram 15U (rank 40): disc = 2^12 3^42 5^35 7^11 17. Mod 7: rank_7(8T_S4) = 30.
- NOT NEW (principle): Codex's L17 (det K_-4 = 2^21 7^k, det K_3 = 3^8 5^6 7^k, notes/80, 25/09) gives for the label
  lattice disc(Lambda_8T(v)) = 2^69 7^(30-k) and disc(Lambda_15U(v)) = 3^32 5^34 7^(40-k); L4/L23 (notes/102) give
  rank_7 of every principal block of 8T <= k <= 28 (L22). Any full-rank label set S then has disc = (that) x square
  (same square-class test as Codex's note 217 on eight far points). I re-derived disc in {2,7}-only from T^2 = 7T and
  checked it on two real srg(243,22,1,2) (disc243_check.py: all-label lattice 3^100 5^76 and 3^114 5^76, only the
  primes of 9c = 135; random full-rank subsets give index 1).  Applied to our objects (new use, old lemmas): the
  four-star object fails at 3, 5, 7, 17 and has rank_7 = 30 > 28; all 52 three-star (A) structures fail T-DISC and
  have rank_7 in {29, 30} > 28. Sample of 3500 saved PSD four-star structures: rank_7 in 30..34, never <= 28.
- CONSEQUENCE / TARGET (OPEN): a Conway four-star structure needs T, U >= 0, rank_Q <= 30 AND rank_7(8T_S4) <= k <= 28.
  Our searches never imposed the 7-adic condition. 'PSD at four stars forces rank_7 >= 29' would exclude Conway
  (k <= 28); 'forces rank_7 >= 23' would exclude k = 22 (r = 37).
- E4 (VERIFIED exactly, 14/10 23:30 UTC; verify_counterexample.py + mixed_view.py): fourstar_psd_c31_mix4.json and
  fourstar_psd_c21_mix4.json, found by the PSD-first walk sym4g.py mix3 (MIXT=4) in the group <(0 1)(2 3)> warm-started
  from a G1 structure: admissible four-star structures with T >= 0, U >= 0, c(m) = 1 (m NON-special), no grid on (l,m),
  c(l) = 3 resp. 2, nullity 10 resp. 9, i.e. FOUR mixed relations (ker_l + ker_m has dimension 6 resp. 5).
  REFUTES (A4) ('PSD at four stars forces c >= 2') and every universal cap 'mixed <= 3'. The G1 data (mixed <= 2,
  c >= 3) were an artefact of the symmetry. Still far from Conway on these flags: c = (3,1) needs nullity 14 + delta
  (eight mixed relations), these have nullity 10 (four mixed).
- E5 (VERIFIED exactly, 14/10 23:55 UTC): fourstar_psd_c11_mix6.json (same walk, group <(0 1)(2 3)>): admissible
  four-star structure with c(l) = c(m) = 1 (BOTH lines non-special), T >= 0 of rank 34, U >= 0 of rank 40, nullity 10
  = 4 local + SIX mixed relations. The 'generic' configuration is PSD-compatible at four stars; for Conway it would
  need nullity 14 (ten mixed relations), rank 30 and rank_7 <= k. Walk statistics (5208 PSD structures with >= 4
  mixed): c = (1,1) nullity 8-10, (1,2) 9-10, (2,2) 10-11, (3,3) 12, (4,4) 12. rank_7 over about 6500 PSD structures
  (G1 and non-G1): always >= 30.
- CONJECTURE (N9) (15/10 00:00 UTC, EVIDENCE only, under stress test): every admissible four-star structure with
  T, U >= 0 has nullity(T_S4) <= 9 + min(c(l), c(m)); equivalently rank T_S4 - rank T_X >= 12 for both lines;
  equivalently mixed <= 7 - max(c(l), c(m)) + [grid(l,m)]. Data: about 6000 PSD structures (G1, <(0 1)(2 3)>,
  subgroups, near-symmetric), minimum exactly 12, attained by c55 (rank 30), c11 (rank 34), c31; never below.
  U >= 0 is essential: sc_2_null14.json (T >= 0, U = 3 - sqrt 10 < 0, c = (6,6)) has nullity 16 > 15.
  CONSEQUENCE (proved reduction): in a Conway graph rank T_S4 - rank T_X_l = 7 + c(l) - delta (G9, P3), so (N9) would
  force c(l) >= 5 + delta for EVERY line, hence >= 4 grids on every line, 6 rho >= 924, rho >= 154 > 126 (Codex's exact
  census certificate): Conway excluded. Caution: the refuted caps of E4 looked equally solid inside G1. Stress test:
  sym4g.py mode 'schur' (PSD-first walk minimising the Schur rank), six runs from 00:00 UTC.
  Stress test status 00:25 UTC: about 30 000 PSD visits in eight runs (h, identity, g2, from c11, c31, c55, c44;
  two runs with a forced grid on (l,m) not yet PSD): minimum still 12. Among about 830 saved structures that are NOT
  h-symmetric, the minimum is also exactly 12, attained by fourstar_psd_asym_c31.json (VERIFIED exactly: c = (3,1),
  rank 34, 4 mixed relations, h-asymmetry 16). In every h-symmetric structure the 12 splits as 9 (the m-odd vectors
  f_y, i.e. no relation has a non-trivial h-odd part) + at least 3 (the m-even vectors), see the board text above.
- Decomposition beyond symmetry (EVIDENCE, 900 NON-h-symmetric PSD structures, 00:45 UTC): the ten m-odd vectors
  f_y = 1_by - 1_b'y (pure swap b <-> b', y outer) ALWAYS add exactly 9 to the rank beyond X_l, whether they are added
  before or after the ten m-even vectors 1_by + 1_b'y, which add 4 to 7. Equivalently every relation of T_S4 has a
  constant m-odd part on the outer letters (and, by symmetry, a constant l-odd part): relations are pure-swap even
  modulo the star differences. (N9) = (this ODD9 law) + (the even vectors add >= 3).
- ODD QUOTIENT (odd_quotient.py, 15/10 00:20 UTC): for an h-symmetric structure the h-odd eigenvectors of the 59-vertex
  graph live on 24 orbits (a^, b^, 10 + 10 label orbits, two C4 orbits); their signed adjacency A^- has spectrum in
  [-4, 3] exactly when T and U are PSD on that sector, and mult_3(A^-) = h-odd nullity (two star differences forced:
  e_a^ + (1/3) 1_N(a^) has Rayleigh quotient exactly 3). 'ODD-h' (mult_3 = 2) holds on all data but is CLOSE to
  failing: walks (mode oddgap) push the third odd eigenvalue of T down to 0.002 with T, U PSD. If ODD-h fails, (N9) can
  still hold (the even part must then compensate); not decided.
- (NOGRID) (EVIDENCE only): no PSD four-star structure with a grid on (l,m) has been found: earlier forced-grid runs
  best -0.35; tonight cold forced-grid runs -0.21, repaired seeds (grid_repair.py) -0.51 to -0.57 and walks from them
  about -0.44. (N9) + (NOGRID) together would exclude Conway with NO census input: (N9) forces >= 4 grids on every line,
  hence pairs (l,m) spanning grids, whose four-star structures (PSD in Conway) (NOGRID) forbids. Even a weak cap
  suffices with (NOGRID): grid-free lines have c <= 3, and Conway then needs nullity >= 14 at every pair, while all
  PSD data with c(l), c(m) <= 3 have nullity <= 12.
- E6 (VERIFIED exactly, 15/10 about 01:14 UTC by file times): REFUTES (N9) AND (NOGRID). Group <(4 6 8 10 12)(5 7 9 11 13), (0 1)(2 3)>
  (order 10, rotates the five outer lines; cold PSD walk, final_seedZ5h): fourstar_psd_grid_Z5h_c22.json (grid on
  (l,m), c = (2,2), rank 35, T, U >= 0) and fourstar_psd_grid_Z5h_c62.json (grid on (l,m), c = (6,2), T >= 0 of rank
  EXACTLY 30, U >= 0 of rank 39, nullity 14 > 9 + min(c) = 11). The latter is a second admissible PSD rank-30
  four-star object; rank_7(8T_S4) = 29 > 28 and disc = 2^69 3 5 7 1429^2, so it is not in Conway either.
  The (N9) evidence of the night was an artefact of the G1-descended seeds. Also: no admissible four-star structure
  is invariant under (4 6 8)(5 7 9) (SAT, sym4g.py: no invariant admissible structure).
- Reduction (grid_floor.py, Codex's identity, CONWAY_CONSTRAINTS G14): a cap 'mixed <= 2' would contradict proved
  bounds (rho >= 198 > 191), 'mixed <= 3' the census certificate (rho >= 154 > 126); Codex: every Conway graph has >= 336
  of its 2079 flags with >= 4 mixed relations. By E4 no such universal cap exists: this route needs the rank condition.
- Literature (3 quick web queries, not exhaustive): star complements (Cvetkovic-Rowlinson-Simic 1999; Rowlinson
  2007, 2012) are known; no application to (99,14,1,2) found.
- E6 bis (VERIFIED exactly, ext4.py, log ext4_grid_c62.log, 01:32 UTC by file time): the rank-30 grid object
  fourstar_psd_grid_Z5h_c62.json has NO admissible placement for any of its 40 outer labels (3440 to 4248 admissible
  profiles per label, 0 to 34 pass (Tr), 0 pass (Tn)). The exact (Tn) residues p^T T_S^+ p - 5/2 of the (Tr)
  survivors have both signs and denominators dividing 150045 = 3 5 7 1429, the primes of disc(Lambda_S)
  (ext4_tn.py): no sign pattern to prove.
- E7 (VERIFIED exactly, 15/10 01:22 UTC by file time; verify_counterexample.py + r7_scan.py): REFUTES (R7).
  r7_Z5h_c62_R7_163.json (walk sym4g.py mode r7 in the Z5h group, warm start from the c62 object): admissible, T >= 0
  of rank EXACTLY 30, U >= 0 of rank 35, c = (6,2), rank_7(8T_S4) = 25 <= 28. Three independent r7 walks (from c62,
  from the c22 object, and a cold start) reached rank_7 = 25 within minutes. So the 7-adic rank bound of L4/L22 is
  not a local obstruction at four stars either. The object dies by DISC: det(8T_I) = 2^73 3^5 5^3 7^5 (odd exponents
  at 3 and 5: robust failure, see below). The G1 data (rank_7 >= 30 over 6500 structures) were again an artefact.
- DISC in graph language (PROVED; a reformulation of the square-class principle already used by Codex in notes 205,
  217, 231, 247 and by LAP/LAB on 08/10, not a new principle). LEMMA (any integral symmetric M of rank r): all
  non-zero r x r principal minors det M_H lie in one class of Q*/Q*^2. Proof: on R = M Z^n put b(Mx, My) = x^T M y;
  the M e_h (h in H) span a full-rank sublattice with Gram M_H, so det M_H = disc(R) [R : R_H]^2. (Checked on
  Petersen, cube, Paley 9 (all subsets) and Paley 25 (3000 samples), sc_square_class.py: one class per eigenvalue.; and on a REAL srg(243,22,1,2),
  new243_trade_aut162: det(4I - A_H) = -2 x square for random 111-vertex H and for H containing N[v], sq243_check.py.)
  For M = 3I - A of a Conway graph: (R, b) = (pi_W Z^99, M), W = E_3^perp, so disc R = det(M|W) / det Lambda_3 =
  (-11 7^44) / (11 7^(14+k)) = -7^(30-k) (det Lambda_3 = 7^(14+k) 11: Codex L2; equivalently L22). Hence
  (SQ3) every 45-vertex induced subgraph H of a Conway graph has det(A_H - 3I) = 7^(30-k) n^2, n integer (n = 0 iff
  H is not a star complement); with k even (L2) this is a perfect square divisible by 49.
  (SQ-4) every 55-vertex induced subgraph has det(A_H + 4I) = 2 7^(40-k) n^2.
  Independent local check of the constants for H containing N[v] (LAB, no global lemma except the parity of k):
  det K = 2^21 3^8 5^6 for K = ker D n Z^84 (snf_D.py: elementary divisors of D are 1^13 2, det D D^T = 2^23 3^8 5^6);
  the eigenvalue gap 7 is a unit at 2, 3, 5, so K splits there; integrality of the Grams 8T and 15U (T^2 = 7T,
  U^2 = 7U) puts all of 2 into K_-4 and all of 3, 5 into K_3; K is 7-unimodular, so det K_3 and det K_-4 have the same
  7-part 7^k; hence det(A_H - 3I) = 4 7^(30-k) [Lambda_8T : Lambda_I]^2 and det(A_H + 4I) = 2 7^(40-k) [..]^2, in
  agreement with (SQ3), (SQ-4). Robust part (no Codex lemma at all): primes other than 2 and 7 occur to even powers.
  DISC for a rank-30 four-star object = (SQ3) for H = N[v] u I; disc_scan.py tests it in about 20 ms.
- Z5 families and DISC (PROVED + VERIFIED): if a Z5 (fixing the four stars, two 5-cycles on the outer letters) acts,
  Lambda_S (x) Q = V_triv (+) V_nt, V_nt = Q(zeta5)^m with b = Tr(h), h Hermitian; the trace form of Q(zeta5) has
  det 125, so disc(V_nt) = 5^m mod squares and DISC is a condition on the small quotient: square class of the Gram of
  the 12 orbit sums (rank t, t + 4m = 30) must be 2 (m even) or 10 (m odd). Checked on three Z5h objects (t = 6, m = 6:
  trivial class = full class = 2 3 5 7) and the rank-35 c22 object (t = 7, m = 7: full = trivial x 5).

- ODD9 status (EVIDENCE only, 15/10 01:47-02:00 UTC; odd9_check.py exact, odd9_axioms.py, sym4g.py mode odd9).
  Statement: in every admissible four-star structure with T, U >= 0, the ten m-odd vectors f_y = 1_{2y} - 1_{3y}
  (y outer) add exactly 9 to the rank beyond X_l (and symmetrically). Equivalently the odd Schur complement
  S_f = G_f - C^T T_X^+ C (10 x 10, S_f 1 = 0 always) is non-singular on 1^perp; G_f = 6I - J/2 - Q_m alone is >= 2
  on 1^perp (Q_m a signed 4-regular adjacency). Consequence (PROVED, one direction only; corrected 15/10 after an independent review): ODD9 for
  Conway four-star blocks => c(l) >= 2 + delta for every line and pair (since 23 - c(l) + 9 <= 30 - delta), in
  particular every line is special. The converse is false in general (c = 3, delta = 0 leaves room for an odd gain 8
  plus an even gain 2). In a Conway graph with a non-special line l every m forces an odd gain <= 8.
  Data: ODD9 holds on every PSD structure tested, in every family, including the Z5h objects (where (N9) failed
  through the EVEN part: c62 has even gain 0 beyond X_m), and on 140 random structures satisfying only (C1), (C1)+(C1')
  or the full model (this only shows the generic value). Stress walks: without positivity the least non-trivial
  eigenvalue of S_f drops to 2e-5 within minutes (no exact failure on file: whether ODD9 needs positivity is NOT
  established); with
  T, U >= 0 the walks stay above 0.037 (identity, c11 and c55 seeds), 0.118 (h), 0.147 (Z5h); the earlier h-family
  oddgap walks reached 0.0023 for the related h-odd eigenvalue. No proof; no counterexample.

- E8 (VERIFIED exactly, 15/10 02:01 UTC by file time; verify_counterexample.py, mixed_view.py): REFUTES (LOW).
  fourstar_psd_rank30_c33_h.json (= harv_h_r7_H30_4.json; walk sym4g.py r7 with R7RANKW=3 and SAVE30 in the group
  <(0 1)(2 3)>, warm start from the E7 object): admissible, T >= 0 of rank EXACTLY 30, U >= 0 of rank 35,
  c = (3,3), grid on (l,m), nullity 14 = 7 local + 7 mixed. So rank 30 is reachable with both lines of small c
  (and 'mixed <= 6' is false as well). Harvest of that walk (scan30.py): ten distinct rank-30 PSD objects with
  c = (6,2), (5,3), (4,2), (3,3), (4,4), (5,5); all have rank_7 25 (or 30 for the c55 seed), all fail DISC at 3 and 5,
  all satisfy ODD9. Within one connected cluster of rank-30 PSD objects the square class and rank_7 did not change:
  the arithmetic seems attached to the cluster (its lattice), not to c.
- E8 bis (VERIFIED exactly, ext4.py, log ext4_c33_h.log, 02:21 UTC): the c = (3,3) rank-30 object has no admissible
  placement for any of its 40 outer labels (0 to 24 profiles pass (Tr) per label, none passes (Tn)). Three rank-30
  objects tested by extension (c55, c62, c33): all 40/40 dead.
- E9 (VERIFIED exactly, ext3.py, logs ext3_A52_slow_partial.log (entry 38, all ten labels) and ext3_A52.log (all 52
  entries, 02:31 UTC): for EVERY one of the 52 the first fourth-star label {3,4} already has no profile; none of them
  has a rank-30 four-star completion): fourth-star column test on the three-star counterexamples to (A)
  (stars 0, 1, 2; c(l) = 1; rank 30). For the exactly verified one (entry 38 of counterexamples_A_all.json =
  counterexample_A_1.json) all ten labels {3,y} of the fourth star have 5490 to 5730 admissible profiles, 517 to 761
  pass (Tr), and none has p^T T^+ p = 5/2 exactly (residues p^T T^+ p - 5/2 between -1.01 and +8.98, both signs):
  this three-star object has no rank-30 four-star completion at all, so it cannot be the base of a counterexample
  to (B'). [(B') link: a four-star structure with c(l) = 1 and rank <= 30 contains X_l u L_2 of rank <= 30, i.e.
  a counterexample to (A); if it has rank exactly 30 its fourth-star labels must all pass this test.]
- E10 (VERIFIED exactly, scan30.py, log scan30_all.log, 02:31 UTC): 331 DISTINCT admissible four-star structures with
  T, U >= 0 and T of rank exactly 30 (harvested by sym4g.py SAVE30 in the groups Z5h, h and identity; exact symmetric
  pivoting, so PSD and rank are exact). c distribution: (2,2) 182, (6,2)/(2,6) 86, (3,3) 23, (6,6) 15, (5,3)/(3,5) 9,
  (4,4) 7, (4,2)/(2,4) 7, (5,5) 2. NEVER a line with c = 1. Every one satisfies ODD9 on both sides (odd gains 9, 9),
  so the bound nullity <= 12 + min(c) is attained by all 275 objects with min(c) = 2. rank_7: 25 (127), 29 (202), 30 (2). DISC fails
  for all 331 (robustly, odd exponents at 3 and/or 5). Caveat: three symmetric families plus walks seeded from them;
  in Z5h the only possible values of c are 1, 2, 6, and 1 never occurs.
- OBSERVATION (SQ30) (EVIDENCE only, 02:38 UTC): all 331 rank-30 PSD objects of E10 have det(8T_I) in the square
  class 2 3 5 7^e EXACTLY (e = 1 when rank_7 is 25 or 29, e = 0 when rank_7 = 30; no other prime, cofactor a square),
  while their three-star sub-blocks X_l u L_2 have scattered classes (2 3 7, 5 61, 5 23, 3 5 7 19 23, 5 17 4651, ...)
  and X_l alone has class 1, 3, 5, 2 5 or 2 3 5. sc_7_null14.json (T >= 0 but U NOT PSD, rank 30; so not an admissible PSD object) also has class 2 3 5. A NON-PSD
  rank-30 structure (sc_6_null14.json) has class -2, so the pattern is not forced by rank 30 alone. Two lineages only
  (G1-c55 and Z5h). If 'PSD and rank 30 => class 2 3 5 7^e' were true, no Conway four-star block could have rank 30
  (Conway needs class 2), i.e. delta(v,l,m) >= 1 at every pair; with ODD9 this would give c >= 3 on every line.
  To test first in genuinely new families; no mechanism known.
- Square classes beyond four stars (sqclass_any.py, exact, PSD or not): the 52 three-star (A) structures, the Z5
  rank-30 three-star examples and z2b have scattered classes (odd primes such as 13, 19, 23, 29, 71, 127, 2801, ...;
  v_2 of either parity). The pattern 2 3 5 7^e of the four-star clusters is therefore not a general law. No local
  object of rank 30 found so far passes DISC.

## AUDIT 15/10 (morning, user's request; full text in French: AUDIT_EXCLUSIONS_2026-10-15.md)
- Every refutation witness re-verified exactly (11 four-star objects, all 52 (A) objects, z2b).
- Missed and now recorded: the transversal bridge (G11, 't >= 8 on both lines' => P >= 924 > 852, Codex's certificate)
  is consistent with all 331 rank-30 objects (t = (12,12) x 329, (8,8) x 2) but FRAGILE: in 800 408 logged PSD visits a
  line with t <= 7 reaches nullity 13. (B') alone does not exclude Conway (needs (C)). All 331 objects fail DISC, so the
  population of possible Conway blocks (rank 30 passing DISC, or nullity >= 15) has never been sampled. Z5 families force
  the grid on (l,m), hence c >= 2: the absence of c = 1 there is not evidence; 329/331 rank-30 objects have the grid;
  every PSD visit with a c = 1 line comes from one lineage (c11/c21/c31/asym seeds) and has nullity <= 10.
- New combination: (SQ30) + (N15: no PSD four-star structure of nullity >= 15) would exclude Conway (every block would have
  rank 30 and would have to pass DISC); delta = 0 is the generic case.
- Mechanism seen in the Z5h rank-30 objects (mixed_view.py on seed_rank30_c22.json): the 9 mixed relations are
  (l-even combination on X_l) + 5 (1_{2y} + 1_{3y}) for 9 of the 10 outer letters y: the m-even vectors of the
  transversal-rich line m are absorbed by X_l (each relation lives on N[l] plus the line {y, z_2y, z_3y}, which forms
  a prism with m). In the c11 object (h family) the 6 mixed relations are h-even and spread over many letters.

## 15/10 LOOP (03:00-07:30 UTC; details H_MATCH_REDUCTION_2026-10-15.md, AUDIT_EXCLUSIONS section 5)
- PROVED (reviewed, modulo L8; Makhnev or rho <= 191 also suffice): (H-MATCH) => no Conway graph, where (H-MATCH) =
  'every admissible four-star structure with T, U >= 0 and nullity >= 14 has M_1 = h(M_0) and M_3 = h(M_2)'
  (M_a = matching induced on the 12 labels {a,y}; h = (0 1)(2 3)). Contrapositive, quantitative (modulo L10): every
  vertex of a Conway graph has >= 4 pairs of lines whose block is PSD of nullity >= 14 with broken star matchings.
- (SQ30) explained: the 331 rank-30 objects are all h-invariant; class from integral eigenvalues 3, 5, 7 of T.
- Evidence for (H-MATCH): all 429 distinct saved nullity >= 14 structures are h-invariant (all from h-families or
  short walks from h-invariant seeds); PSD broken record nullity 13; T-only form FALSE (U >= 0 essential); none of the
  129 distinct kernels of the 331 objects carries a PSD broken structure (MILP + complete SAT enumerations).
- srg(243) comparison (CORRECTED 08:00 UTC after a second independent review): the failure of the six-star analogue
  of (H-MATCH) in real srg(243) is automatic (all pairs h-related at v <=> v Hamming, by the same argument), so it
  says nothing about the local law; the (B') comparison used a spectral c that, in srg(243), does not count the
  components of H_l (with the Conway meaning every real line is special); the 243 walks never moved. Structural fact:
  two lines force 5k - 16 - g relations: 10 for Conway, none for any other lambda = 1, mu = 2 parameters.

## OPEN (none of these is established)
- (H-MATCH) [would EXCLUDE Conway; see the 15/10 LOOP section].
- (B') [the live four-star question, 15/10 02:15 UTC] No admissible four-star structure with T, U >= 0 and nullity
  >= 14 (rank <= 30) has a line with c = 1. (B') => every line of a Conway graph is special (c >= 2; corrected
  15/10: not c >= 2 + delta, and not an equivalence).
  ODD9 (odd gain exactly 9 beyond X_l, i.e. the odd Schur block S_f non-singular on 1^perp) implies (B') and gives
  nullity <= 12 + min(c(l), c(m)), attained (c62 cluster: c(m) = 2, nullity 14, even gain 0). Data: every rank-30
  PSD object found has min(c) >= 2, but 329 of the 331 have the grid on (l,m), which forces c >= 2 by itself; only
  the two c55 objects test (B'). Max nullity with a c = 1 line is 10 (280 424 logged PSD visits with a c = 1 line, all
  from the c11/c21/c31/asym lineage); walks mode b1 (from 02:07 UTC) never left min(c) >= 2. Without positivity the
  odd gap gets down to 2e-5 but no exact failure is on file.
- (15/10 night, see N9_REDUCTION_2026-10-15.md; (N9) and (NOGRID) REFUTED at about 01:14 UTC, E6) (N9) nullity(T_S4) <= 9 + min(c(l), c(m)) for every admissible PSD
  four-star structure [would exclude Conway with the census]; its two halves ODD9 (the m-odd vectors add exactly 9
  beyond X_l) [would make every Conway line special] and EVEN3 (the m-even vectors add >= 3); (NOGRID) no PSD
  four-star structure has a grid on (l,m), and (LOW) nullity <= 13 when c(l), c(m) <= 3 (REFUTED by E8) [together: Conway excluded
  with no census]; (R7) PSD four-star structures have rank_7 >= 29 [would exclude Conway via L22] -- REFUTED by E7
  (rank_7 = 25 at rank 30). Remaining local tests at four stars: DISC (SQ3) and the extension; both kill every object
  found so far (four rank-30 objects), and DISC-targeted walks (sym4g.py mode disc) ran from 01:33 UTC.
- [REFUTED 14/10 ~20:55 UTC, 52 exact counterexamples; kept for the record] (A) Every admissible three-star structure with T >= 0, U >= 0 and c(l) = 1 has rank 31 (no relation beyond the
  stars unless l is special). Evidence: no counterexample in 11 seeds x all rectangles (Codex), 6 812 exact
  third-star completions on a connected base (h3pp_inner.py), annealing to |lambda| ~ 1e-5; the residual Schur
  complement R (10 x 10, R 1 = 0) is not a Laplacian (22-40 positive off-diagonal entries of 90), and its second
  eigenvalue gets down to 0.0035 on PSD seeds. 2-adic profile of 8 T[J,J]: always 2^0 (x6), 2^1, 2^2, 2^3 (x20-22),
  and one last factor of valuation 4 to 10 (infinite exactly when l is special): no 2-adic bound visible.
- (B) Every Conway graph has a special line. By P6, its negation forces >= 10 mixed relations at every pair of lines.
- (C) Every Conway graph has a non-special line. (A) + (C) would exclude Conway; (A) alone gives (B).
- (H4) No admissible four-star structure is PSD: REFUTED exactly 14/10 ~21:12 UTC (psd4_candidate_1.json).
- Affordability of the finite route (decomposable bases, third stars, column filter): not estimated.
