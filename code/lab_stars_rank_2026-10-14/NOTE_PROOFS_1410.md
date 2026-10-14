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

## VERIFIED (exact computations; files in this folder)
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
