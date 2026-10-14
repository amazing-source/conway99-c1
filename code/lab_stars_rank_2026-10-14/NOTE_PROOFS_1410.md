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
- (A4) (OPEN, robust): T, U >= 0 at four stars forces c(l), c(m) >= 2. It would make every line of a Conway graph
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

## OPEN (none of these is established)
- (A) Every admissible three-star structure with T >= 0, U >= 0 and c(l) = 1 has rank 31 (no relation beyond the
  stars unless l is special). Evidence: no counterexample in 11 seeds x all rectangles (Codex), 6 812 exact
  third-star completions on a connected base (h3pp_inner.py), annealing to |lambda| ~ 1e-5; the residual Schur
  complement R (10 x 10, R 1 = 0) is not a Laplacian (22-40 positive off-diagonal entries of 90), and its second
  eigenvalue gets down to 0.0035 on PSD seeds. 2-adic profile of 8 T[J,J]: always 2^0 (x6), 2^1, 2^2, 2^3 (x20-22),
  and one last factor of valuation 4 to 10 (infinite exactly when l is special): no 2-adic bound visible.
- (B) Every Conway graph has a special line. By P6, its negation forces >= 10 mixed relations at every pair of lines.
- (C) Every Conway graph has a non-special line. (A) + (C) would exclude Conway; (A) alone gives (B).
- (H4) No admissible four-star structure is PSD: probably false (see VERIFIED).
- Affordability of the finite route (decomposable bases, third stars, column filter): not estimated.
