# Level-7 theta series and an exact linear programme for srg(99,14,1,2) (lab session, 2026-10-07/08)

Status: derivation and programs by the lab session. Codex checked independently the lattice L1, the bound 22 on its new
vectors, the form Q, the basis and the Fricke formula (its note 167 and `code/codex/theta7_audit.py`); it found no
theta/Fricke programme in the earlier notes. The laptop session supplied part of the list of short dual vectors.
The LP results below have NOT yet been refereed. AI sessions only; nothing formalised. Nothing here proves non-existence.

## 1. Set-up

Gamma a srg(99,14,1,2), A its adjacency matrix, P = (27I - 9A + J)/63 the projector on the (-4)-eigenspace (dimension 44),
r = rank_7(A - 3I).

* L = Z^99 cap ker(A + 4I). Every non-zero vector has norm >= 14 (entries 0, +-1 need two supports of size >= 7; an entry
  of absolute value >= 2 costs norm >= 20). Norm 14 = the Fano configuration (Codex, note 165), which forces r >= 33.
* L1 = L + Z (21 P e_v) = { phi - (s/3) 1 : phi in Z^99, A phi = -4 phi + 6s 1 } (then sum phi = 33 s). Index 3 over L,
  independent of v, even (|phi|^2 - 11 s^2 = sum phi - 11 s = 22 s mod 2), and 7 L1* is contained in L1. A vector outside L
  is phi - (1/3) 1 with sum phi = +-33, so its norm |phi|^2 - 11 is >= 22. Hence L1 is an even lattice of rank 44 and
  level 7, of determinant 7^d with d = r - 1 (given det L = 9 * 7^(r-1), rank7.tex of the earlier work), and
  **L1 and L have the same vectors of norm 14, 16, 18, 20**.
* M = sqrt7 L1*, where L1* = { P psi : psi in Z^99, 3 | sum psi }. Its form is
  Q(psi) = psi^t (3I - A) psi + (sum psi / 3)^2, even, determinant 7^(44-d). sqrt7 M is contained in L1.
* theta_L1 = sum a_n q^n and theta_M = sum b_n q^n (n = norm/2) lie in M_22(Gamma_0(7)) with trivial character (d even;
  d odd is impossible by Milgram's formula, and d = 0, 44 because 44 is not a multiple of 8). Dimension 15, basis
  F_j = G t^j (j = 0..14), G = theta_{x^2+xy+2y^2} (eta(7 tau)^7 / eta(tau))^7 = q^14 + ..., t = (eta(tau)/eta(7 tau))^4,
  all with integer coefficients, and (G t^j)|W_7 = -7^(2j-14) G t^(14-j). If theta_L1 = sum c_j F_j then
  theta_M = sum_j c_j 7^(d/2+2j-25) F_(14-j).
  `theta_lp.py` checks the basis and this formula exactly on E8^a + (sqrt7 E8)^(5-a) + A + A, a = 0..5.
* a_0 = b_0 = 1 and a_1 = ... = a_6 = 0 leave **seven free parameters, which are b_1, ..., b_7**. Every a_n and b_n is an
  explicit affine function of them, for each d.

## 2. Constraints used (set "ext")

| constraint | reason |
|---|---|
| a_n >= 0, b_n >= 0 (n <= N) | counts |
| a_7k >= b_k | sqrt7 M inside L1 |
| b_2 >= 462 | +-t_T, T one of the 231 triangles, Q(1_T) = 4 |
| b_3 >= 24948 | e_u - e_v, u, v non-adjacent (8316); +-(e_u + e_v + e_w) on an induced 2-path (16632) |
| b_4 >= 388080 | e_u - e_v adjacent (1386); +- a triple with exactly one edge (99792); 1_e - 1_e' for two disjoint edges with no edge between (693 * 366 = 253638); 1_T - 1_T' for two triangles with exactly one edge between (33264 + 6 * prisms, the prisms dropped) |
| b_5 >= 196812 | +- an independent triple |

Distinctness in M: two listed psi, psi' are equal in M iff psi - psi' lies in Z^99 cap (E_3 + Q 1); the sums of entries
force it into E_3, and a non-zero integer 3-eigenvector has norm >= 12 if its entries are 0, +-1 (the + support has minimum
degree 3, so at least 6 vertices) and >= 18 otherwise. This separates all the vectors counted above; it does NOT separate the
norm-6 vectors 1_T - 1_T' (no edge between), which can coincide for "twin prisms", so those are not counted.
"a_7 = 0" (when used) is Codex's lemma for r <= 31.

## 3. Results (exact rational simplex, N = 84 coefficients; identical with N = 70)

`theta_lp_exact.py` solves each LP in Fractions and re-verifies what it returns; `certificates.py` stores and re-checks
the Farkas multipliers (15 of 15 verified, `certificates_N84_check.txt`).

| r | set "ext" | with a_7 = 0 | largest minimum of L1 allowed |
|---|---|---|---|
| <= 27 | infeasible (exact certificate) | | |
| 29 | feasible only with a_7 >= 2 558 811 and b_1 >= 174 | infeasible (exact) | 14 |
| 31 | feasible only with a_7 >= 316 | infeasible (exact) | 14 |
| 33 | feasible | then a_8 >= 100 986 | 16 |
| 35, 37 | feasible | feasible | 20 |
| 39, 41 | feasible | feasible | 24 |
| 43 | feasible | then b_2 >= 1000 and b_3 >= 7 561 631 | 26 |

Consequences, each conditional on sections 1 and 2 being right:

1. **r >= 29** from the theta series alone, and **r >= 33** with Codex's lemma (r = 29 and 31 need Fano vectors, which need
   r >= 33). The earlier lower end was 25 (computer-assisted) / 23 (by hand).
2. **A srg(99,14,1,2) has a non-zero vector of L1 of norm <= 26**, more precisely <= 16 if r = 33, <= 20 if r = 35, 37,
   <= 24 if r = 39, 41, <= 26 if r = 43 (`OUTPUT_ladder_N84.txt`). The Hermite-type bound was 44. Norms 14..20 are integer
   (-4)-eigenvectors; norms 22..26 are those or vectors phi - (1/3) 1 with sum phi = 33, |phi|^2 = norm + 11.
   So the "ladder" of support cores is finite and short: norms 14 (one core, Codex), 16 (five cores, Codex), 18, 20, 22, 24, 26.
3. What-if runs (hypotheses, not facts), `OUTPUT_N84.txt`: if M had no root, at most 3234 vectors of norm 4 and at most
   32340 of norm 6, then r = 39, 41, 43 would be infeasible and r = 31 too. With b_1 = 0 and b_2 <= 3234 alone, r = 43
   needs b_3 >= 10 561 586, r = 41 needs b_3 >= 1 390 256, r = 39 needs b_3 >= 80 066. So UPPER bounds on the numbers of
   vectors of M of norm 2, 4, 6 (a classification of the short dual vectors) would close the top of the window.

## 4. Files

`theta_lp.py` (series, basis, Fricke check, affine family; its own main is a floating-point first version, superseded),
`theta_lp_exact.py` (exact simplex and the constraint sets), `certificates.py`, `ladder.py`, `certificates_N84.json`,
`certificates_N84_check.txt`, `OUTPUT_N84.txt`, `OUTPUT_ladder_N84.txt`.
Run: `python theta_lp_exact.py 84 ext`, `python certificates.py 84 check`, `python ladder.py 84` (standard library only, one
process, under a minute each).

## 5. Addendum (22:22 UTC): the weight-26 quartic harmonic adds nothing decisive

Codex audited sections 1 to 3 independently (its note 168, commit b3c4b92: the 15 certificates and the 6 ladder
certificates re-derived in its own coordinates; r >= 33 and min(L1) <= 26 accepted; my finer optima not audited).

`theta_quartic.py`: H(f) = sum_v f_v^4 - (2/69)|f|^4 is harmonic of degree 4, so sum_{f in L1} H(f) q^(|f|^2/2) and its
analogue on M are cusp forms of weight 26 on Gamma_0(7) (dimension 15; basis and Fricke formula checked on
E4^a E4(7tau)^(6-a) theta_A^2). Nine more parameters; constraints lo(n) a_n <= S(n) <= hi(n) a_n with [lo, hi] a proved
range of sum_v f_v^4 on the vectors of norm 2n (exact at norms 14, 16, 18; crude from norm 30 on), same on sqrt7 M.
Result (N = 30): the ladder is unchanged (16 / 20 / 24 / 26, with certificates that do not use the new constraints), the
minima of a_7 at r = 29, 31 are unchanged; only upper ends of ranges shrink, by a factor of about 2
(`OUTPUT_quartic_N30.txt`, `OUTPUT_quartic_ladder_N30.txt`). The quartic would become useful only with the exact
composition of some shells (how many vectors of each coordinate pattern), which is the classification problem again.

## 6. Addendum (22:35 UTC): sign correction, proved caps, forced abundance

* Sign error found by Codex in `theta_quartic.py` (the correction for the 462 triangle vectors relaxed the constraint instead of
  tightening it). Corrected; ladder and minima unchanged (outputs regenerated). Section 5 stands.
* Two proved caps. (a) **a_7 <= 7920**: a Fano vector (P, Q) is determined by a vertex p0 of P and its 4 neighbours in Q
  (pairwise non-adjacent, so in 4 of the 7 triangles on p0: C(7,4) 2^4 = 560 choices): the 6 other vertices of P are the
  second common neighbours of the pairs, then Q; each vector arises from its 7 vertices of P; 99 * 560 / 7 = 7920.
  (b) **b_1 <= 3784**: the roots of the even lattice M form a root system of rank <= 44, the largest being D_44.
  With (a) alone, r = 29 (which needs a_7 >= 2 558 811) is excluded without the rank lemma.
* `abundance.py`, exact minima under the set "ext" and these caps (`OUTPUT_abundance_N84.txt`), numbers of non-zero vectors of
  L1 of norm <= 2m:

| r | norm <= 16 | <= 18 | <= 20 | <= 22 | <= 24 | <= 26 |
|---|---|---|---|---|---|---|
| 33 | 128 | 81 322 | 93 171 | 131 751 | 12.4 M | 68 M |
| 35 | 0 | 0 | 3 357 | 6 117 | 136 011 | 2.9 M |
| 37 | 0 | 0 | 7 | 413 | 16 647 | 49 392 |
| 39 | 0 | 0 | 0 | 0 | 1 974 | 7 074 |
| 41 | 0 | 0 | 0 | 0 | 234 | 1 029 |
| 43 | 0 | 0 | 0 | 0 | 0 | 165 |

  At r = 33 with no Fano vector, a_8 >= 100 986. There are 99 * 560 = 55 440 seeds (p0; four pairwise non-adjacent
  neighbours), and a norm-16 vector has 8 of them, so some seed would lie in at least 14 norm-16 configurations. A proved
  bound "at most 13 per seed" would exclude r = 33 without Fano vectors; not proved. At the top (r >= 39) the forced
  numbers are small: counting cannot conclude there.
* A remark for r = 43 (d = 42): sum_k (a_7k - b_k) q^k is a cusp form of weight 22 for SL_2(Z), hence a multiple of
  Delta E_10, which has coefficients of both signs; as a_7k >= b_k, it is zero: **a_7k = b_k for all k**. Every vector of L1
  whose norm is a multiple of 14 is sqrt7 times a vector of M (the discriminant form is the anisotropic plane), every Fano
  vector is a root of M, and a_7 <= 3784. For r = 43 a random lattice with the determinant of M (49) has about 1.4 million
  vectors of norm 6, so large values of b_3 are not absurd there: the what-if caps of section 3 are not expected to hold.
* Codex (its note 169): the block-rank thresholds of the five norm-16 cores are 17, 15, 19, 17, 15, so they do not force
  r >= 35.

## 7. Addendum (22:40 UTC): r = 33 forces Fano vectors (conditional on a hand bound being refereed)

The laptop session proved by hand (sent to Codex for refereeing; I re-derived its Case I and Steps 1 to 3 and agree, Step 4
only read): a seed (p0 in P; its four neighbours in Q) lies in at most 13 norm-16 configurations, at most 1 when p0 has a
partner of overlap 0 and at most 2 for each of the 6 choices of the missing second common neighbour otherwise. Hence
**a_8 <= 55 440 * 13 / 8 = 90 090**.
`caps16.py` (`OUTPUT_caps16_N84.txt`), set "ext" with a_7 <= 7920, b_1 <= 3784, a_8 <= 90090: at r = 33 the case a_7 = 0 is
infeasible (exact certificate) and the exact minimum of a_7 is 13.77. So **r = 33 requires at least 14 Fano vectors**, and
a_7 + a_9 >= 5075. For r = 35, 37 the cap changes nothing.
With Codex's formula r = 33 + rank(S | ker D2) for a Fano core, r = 33 is reduced to the equality case, with at least seven
Fano configurations present. Remark: rank_7 of every principal submatrix of A - 3I is at most r, so the block bound of a
union of cores must stay <= r; a lemma "two distinct Fano configurations force rank >= 35" would exclude r = 33.
The space Q_r = L1 / (L1 cap 7 L1*) is a non-degenerate quadratic space over F_7 of dimension 45 - r and of minus type
(Witt index (45 - r)/2 - 1); Fano vectors are isotropic in it.
