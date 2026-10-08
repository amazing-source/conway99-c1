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

## 8. Addendum (22:44 UTC): at most 4 norm-16 vectors per seed; r = 33 needs half a million vectors of norm 18

Three hand proofs, cross-read (Codex's "at most 10", the laptop's "at most 13", and their combination, re-derived by me):
for a seed (p0; U = its four neighbours in Q), let V be the six second common neighbours of the pairs of U.
* If p0 has a partner of overlap 0, V is independent and the configuration is unique (Q minus U = the vertices with three
  neighbours in {p0} + V; then P = the vertices with four neighbours in Q).
* Otherwise exactly one element x of V is outside P; it is adjacent to one of the five others, so V induces K2 or K_{1,2}
  and x is an end of the K2 or the centre: at most 2 choices, and this excludes the first case. For a fixed x the two
  "H" vertices of Q minus U are fixed (second common neighbours of the two pairs of known vertices of P through the ends of
  x's pair), each of the two remaining vertices p', p'' of P has at most 2 candidates, and for a fixed p' at most one p''
  works (the second common neighbour of p' and a suitable known vertex is fixed and would have to be adjacent to the other
  candidate, against "an outside vertex has at most 2 neighbours in Q").
So **a_8 <= 55 440 * 4 / 8 = 27 720**.
`caps16b.py` (`OUTPUT_caps16b_N84.txt`, `certificates_caps16_N84.json`), exact, at r = 33 with a_7 <= 7920 and b_1 <= 3784:

| cap on a_8 | min a_7 | min a_9 | min (a_7 + a_9) |
|---|---|---|---|
| 90 090 | 13.77 | 0 | 5 074 |
| 69 300 | 40.05 | 38 819 | 46 739 |
| 27 720 | 92.61 | 497 122 | 505 042 |

With 4 per seed: **r = 33 needs at least 94 Fano vectors and at least 497 123 vectors of norm 18.** An upper bound
a_9 <= 497 122 would therefore exclude r = 33. For norm 18 the supports have 9 vertices each and may contain up to two
disjoint edges each (8e + (1/2) sum a_p^2 <= 18); the per-seed count is not done.

`tradeoff33.py` (`OUTPUT_tradeoff33_N84.txt`): at r = 33 with a_8 <= 27 720, the forced number of norm-18 vectors as a
function of the cap on a_7: 497 123 (a_7 <= 7920), 854 645 (<= 4000), 1 128 259 (<= 1000), 1 210 890 (<= 94); roughly
1.22 million minus 91 a_7. With independent supports (55 440 seeds, 9 per vector) that is 80 to 197 configurations per seed.

Remark: S = J - I - 2A (Seidel matrix) satisfies S^2 = 49 (I + J) and rank_7(S) = r - 1; the rows of S mod 7 are the vectors
1_{Gamma_2(v)} - 1_{N(v)}, which span the radical code C_0.

## 9. Stronger dual lower bounds (22:57 UTC): r = 33 is infeasible; ladder 18 / 20 / 24 / 24 / 26

Status: counts and proofs by the lab session, sent to Codex for refereeing; not yet refereed.

Distinctness rule used throughout. Two integer vectors psi, psi' (3 | sum) are equal in M iff w = psi - psi' satisfies
(A - 3I) w = (sum w / 9) 1. All families below have sum 0 or +-3, so sum w = 0 and w is an integer 3-eigenvector: either its
entries are 0, +-1 and both supports induce prisms (6 vertices each), or it has an entry +-2 and norm >= 18. Hence two 0/+-1
vectors with supports (s, t), (s', t') and the same sum are distinct as soon as s + t' <= 5 or t + s' <= 5 and
|psi - psi'|^2 < 18. This covers all pairs among the types (1,1), (2,2) (sum 0) and among (3,0), (4,1) (sum 3).
For 0/+-1 vectors with positive support S and negative support T:
Q = 3(s + t) - 2 e(S) - 2 e(T) + 2 e(S,T) + ((s - t)/3)^2.

Norm 8 (b_4), in addition to the 388 080 of section 2:
* (F1) 1_C - e_z, C an induced 4-cycle, z adjacent to no vertex of C: 2079 * 51 * 2 = 212 058. (C has 48 outside
  incidences; exactly 4 outside vertices, the apexes of its edges, have two neighbours in C; none has three: 44 neighbours.)
* (F2) 1_S - e_z, S a paw (triangle abc and w ~ a), z adjacent to no vertex of S: 8316 * 50 * 2 = 831 600. (Neighbours of
  S: the 35 near vertices of the triangle other than w and the 10 far neighbours of w.)
So **b_4 >= 1 431 738**.

Norm 10 (b_5), in addition to the 196 812 independent triples:
* 1_e - 1_e', two disjoint edges with exactly one edge between: 693 * 264 = 182 952 (the second edge joins one of the 24
  vertices adjacent to exactly one end of e to one of its 11 far neighbours).
* +-(1_e - e_x - e_y), x, y non-adjacent among the 72 vertices far from e (366 edges among them): 693 * 2190 * 2 = 3 035 340.
* triangle + far vertex y, minus a vertex z far from the triangle and not adjacent to y: 231 * 60 * 51 * 2 = 1 413 720.
* claw (centre v, three pairwise non-adjacent neighbours: 99 * 280) minus a vertex adjacent to none: 27 720 * 51 * 2 = 2 827 440.
* induced path a-b-c-d (693 * 12 * 11 = 91 476) minus a vertex adjacent to none (at least 50: the path has 50 outside
  incidences and the overcount is at least 5): >= 91 476 * 50 * 2 = 9 147 600.
* 4-cycle minus a vertex with exactly one neighbour in it: 2079 * 40 * 2 = 166 320; paw minus a vertex with exactly one
  neighbour in it: 8316 * 42 * 2 = 698 544.
So **b_5 >= 17 668 728**.

Norm 12 (b_6): e_u + e_v - e_x - e_y, two disjoint non-edges with no edge between (4158 * 2120 = 8 814 960; among the 71
vertices far from a non-edge there are 365 edges); +-(1_e - e_x - e_y), x, y non-adjacent with exactly one edge to e
(693 * 1464 * 2 = 2 029 104); two disjoint edges with no edge between, minus a vertex adjacent to none of the four (at least
49): >= 126 819 * 49 * 2 = 12 428 262. So **b_6 >= 23 272 326**.
Norm 14 (b_7): two disjoint non-edges with exactly one edge between: >= 4158 * 24 * 60 = 5 987 520.

Results (`OUTPUT_ext2_N84.txt`, `OUTPUT_ext3_N84.txt`, `certificates2_N84.json`, 7 certificates re-verified):

| r | set "ext3" alone | with a_7 <= 7920, a_8 <= 27 720 |
|---|---|---|
| 29 | infeasible | |
| 31 | needs a_7 >= 1 725 968 | infeasible (without the rank lemma) |
| 33 | needs a_7 >= 688 | **infeasible** |
| 35 | feasible | feasible; min(L1) <= 18; at least 994 vectors of norm <= 18 |
| 37 | feasible | feasible; min(L1) <= 20 |
| 39, 41 | feasible | feasible; min(L1) <= 24 |
| 43 | feasible | feasible; min(L1) <= 26 |

The certificate for r = 33 uses only b_2 >= 462, b_3 >= 24 948, b_4 >= 1 431 738, a_7 <= 7920, a_8 <= 27 720 and positivity
of a_9, a_10, b_5. Margin (`OUTPUT_threshold33_N84.txt`): the maximum of b_4 compatible with the earlier constraints and
the caps is 1 049 063 (a_8 <= 27 720), 1 159 235 (a_8 <= 69 300), 1 214 320 (a_8 <= 90 090); 5.78 million with no cap on a_8.
So **r >= 35**, conditional on: sections 1, 2, 9 (set-up and counts), a_7 <= 7920 and a_8 <= 27 720 (or 90 090).
Limit of this lever: at r = 35 the maxima of b_4 and b_3 under the caps are 9.8 million and 661 138, far above what small
configurations supply, and the programme only needs 994 vectors of norm <= 18: counting does not reach r = 35.

## 10. Status at 23:07 UTC: r >= 35 audited; what the programme can and cannot do from here

* Codex audited section 9 independently (its note 172, commit d1aeb28 on codex/c1-arithmetic-audit): the families F1, F2,
  their distinctness, direct controls on the rook graph and both 243-vertex graphs, and the certificates. The exclusion of
  r = 33 is the integer identity, valid at d = 32,
  12991 a_9 + 3288 a_10 + 3311 b_5 + 5937575 (b_2 - 462) + 936026 (b_3 - 24948) + 79625 (b_4 - 1431738)
  + 1793806 (7920 - a_7) + 97767 (27720 - a_8) = -5559808184,
  whose left side is a sum of non-negative terms. Accepted in the chain: **r in {35, 37, 39, 41, 43}**, with
  min(L1) <= 18 / 20 / 24 / 24 / 26. The bounds b_5, b_6, b_7 of section 9 and the cap on roots are not dependencies.
* `scenarios.py` (`OUTPUT_scenarios_N84.txt`; uses the non-audited b_5, b_6 of "ext2"): at r = 35, without Fano and
  norm-16 vectors at least 55 172 vectors of norm 18; without Fano vectors at least 5 829 of norm 16 or 18; in general at
  least 994 of norm <= 18. At r = 37, norms <= 18 may be empty, and then at least 574 vectors of norm 20.
* The relation proposed by the laptop session for the sum of the isotropic classes (U_7 theta_L1) is the level-1 trace
  identity and holds identically on the family; at r = 43 its content is a_7k = b_k, already forced. In representation
  terms the O(D)-invariants of the Weil representation are Steinberg at r = 43 and 1 + Steinberg for r <= 41, and
  M_22(Gamma_0(7)) is 1 + Steinberg: the scalar programme contains the whole invariant vector-valued structure.
* Limits. Counting does not reach r = 35 (the programme tolerates millions of dual vectors there and needs fewer than a
  thousand short vectors). r = 43 is the generic case: M has determinant 49, and a random lattice of that determinant
  already has the numbers of short vectors that can be proved. What remains is structural: exclusion of the cores of norm
  <= 18 (r = 35), <= 20 (r = 37), <= 24 (r = 39, 41), <= 26 (r = 43), or a reason bounding the rank from above
  (r <= 45 - k as soon as L1 contains k vectors whose Gram matrix is invertible mod 7).

## 11. The 3-side (23:44 UTC): an even lattice of rank 60 and a second ladder; no exclusion

Idea: the dual lattice on the side of the eigenvalue 3 is forced to contain far more short vectors than a random lattice of
its determinant at every r, so the same method was tried there. Construction (checked independently by Codex, which is
publishing it): K3 = Z^99 cap (E_3 + Q1) = { kappa : (A - 3I) kappa = c 1 }; u = (1/3) 1 has norm 11; K3' = K3 + Z u is an
odd lattice of rank 55, level 7, determinant 7^(r-1), with characteristic vector 1 = 3u of norm 99 = 3 mod 8; the even
neighbour E of K3' + Z^5 is an even lattice of rank 60, level 7, determinant 7^(r-1), so theta_E lies in M_30(Gamma_0(7))
(dimension 21, basis (eta(7tau)^7/eta(tau))^10 t^j). Along u, theta_E = sum_j Phi_j Theta_j with Phi_j the coset theta
series of a fixed even lattice of rank 6 and determinant 11 (theta = 1 + 40q + 122q^2 + ...) and Theta_j the theta series
of the 11 cosets of L_3 = Z^99 cap E_3 (class j = 3c mod 11; projected norm nu = |kappa|^2 - 9c^2/11 >= 9|c|(1 - |c|/11)
for |c| <= 5: grids are c = +-1, nu = 90/11; integer 3-eigenvectors are c = 0, nu >= 12).
`theta3.py`: two self-tests (the same decomposition for Z^11 + Z^5 gives theta of D_16^+ = E_4^2; weight-30 basis and
Fricke formula on E_4^a E_4(7tau)^(7-a) theta_A^2), then the exact LP with unknown shell counts N_j(nu) and the forced
dual vectors (norm 6: 1386 differences of adjacent vertices; norm 8: 8316 + 4158; norm 10: 182 952; ...).
Result (`OUTPUT_theta3_ladder_N26.txt`, N = 26): feasible for all r in the window; second ladder: some class has a vector
of projected norm nu <= 20 at r = 35, <= 266/11 at r = 39, <= 304/11 at r = 43, with at least 667 vectors of nu <= 20 at
r = 35 and nothing forced below 21 for r >= 39. Adding more forced dual vectors does not move it. So the 3-side gives
existence statements (3-eigenvectors, grids, regular sets of small norm) but no exclusion; the over-forcing heuristic that
predicted the (-4)-side well does not carry over, because the 3-side has six classes of unknowns.

## 12. Two more variants, both weaker than the programme of sections 1 to 10 (23:58 UTC)

* 3-side with Codex's proved constraints (`theta3_caps.py`, `OUTPUT_theta3_caps_N24.txt`): number of grids G <= 231 and
  A_7m >= B_m. Same ladder (nu <= 20 at r = 35, nu <= 304/11 at r = 43); at least 1 844 vectors with nu <= 20 at r = 35;
  G = 0 remains possible. No exclusion.
* A (-4)-side programme that keeps the 3-part of the dual (`theta_pi.py`, `OUTPUT_theta_pi_N60.txt`). The vertex vectors
  sqrt7 P e_v (norm 28/9) are not in M; gluing with A_8 gives the even lattice
  Lam = { (sqrt7 P psi, pi(z)) : psi in Z^99, z in Z^9, sum psi = sum z mod 9 } of rank 52, level 7, determinant 7^(45-r),
  in which they have norm 4 (1782 vectors), and its Fricke dual Pi = { (phi - (t/9)1, sqrt7 pi(z')) : (A+4I)phi = 2t 1,
  sum z' = -t mod 9 }, whose shells are a_7 + 72 at norm 14, a_8 at norm 16, and mix the classes t != 0 from norm 18 on.
  Theta series in M_26(Gamma_0(7)), nine free parameters; forced numbers of vectors of Lam computed from all integer
  vectors of support <= 3 (72, 2538, 149 100, 4 499 550, ... for norms 2, 4, 6, 8, ...).
  Result: feasible for r = 31..43, ladder 18 / 20 / 22 / 26 / 26 / 28 / 28. Weaker than the L1 programme (which excludes
  r <= 33 and gives 18 / 20 / 24 / 24 / 26): the extra dual vectors do not compensate for the larger space of forms and for
  the mixing of the classes of L* / L from norm 18 on.
* Codex (note 175) determined exactly, by graphlet identities, all pairs (Q, Qbar) for the vectors of U of norm <= 5, which
  gives b_5 >= 18 001 368, b_6 >= 86 272 956, b_7 >= 208 016 424, b_8 >= 263 126 556; with these and the coupled seed bound
  every r in 35..43 remains feasible.
Conclusion of the evening for the theta method: the window {35, 37, 39, 41, 43} and the ladder 18 / 20 / 24 / 24 / 26 are
what scalar and vector-valued theta series of level 7 give with the short vectors that can be counted. What is not used by
any of these programmes is class-level (glue) information, which is bilinear: e.g. (Codex) each class of M modulo sqrt7 L1
contains at most one vector of norm <= 24, and a norm-4 vector of M other than the 462 triangle vectors has all its
partners in sqrt7 K* of norm >= 38.

## 13. Descent rules and the distribution of the forced short vectors (00:04 UTC)

Descent against the forced vectors of sqrt7 M (mine; (R1) used by Codex to prove that norm 20 is binary; to be refereed).
f_T = 7 P 1_T lies in L1 \ L (norm 28) and (x, f_T) = 7 x(T). Since min L = 14 and min(L1 \ L) = 22:
* (R1) for x in L of norm 2n: x(T) <= (2n + 6)/14. Every integer (-4)-eigenvector of norm <= 20 has all its 231 triangle
  sums in {-1, 0, 1}, exactly 3n at +1 and 3n at -1 (frame identity sum_T x(T)^2 = 3|x|^2).
* (R2) for a prism (T, T'), f_T + f_T' lies in L1 \ L and has norm 28: |x(T) + x(T')| <= 1 for norm <= 20; two triangles of
  sum +1 never form a prism.
Codex (to be published by it): every vector of norm 20 is binary and its supports have at most one edge each; one norm-16
vector per seed; 7 a_7 + 8 a_8 <= 55440; at r = 43 each non-zero class of L1 / sqrt7 M carries a single norm.

`top43.py` (`OUTPUT_top43_N84.txt`, `OUTPUT_top_others_N84.txt`): exact LP minima with the audited bounds, Codex's exact
small shells (b_5 >= 18 001 368, b_6 >= 86 272 956, b_7 >= 208 016 424) and the coupled seed bound.

| r | min (a_8+...+a_13) | norm 18 alone | without norm 18 | norm 26 alone | min of the largest shell |
|---|---|---|---|---|---|
| 43 | 164.5 | 164.5 | 2 250.9 | 2 632 | 138.5 |
| 41 | 1 028.1 | 1 028.1 | 14 067.9 | 18 082.4 | 865.8 |
| 39 | 7 073.5 | 7 073.5 | 106 246 | 126 988.4 | 5 956.6 |
| 37 | 49 391.1 | 49 391.1 | 1 063 860 | infeasible | 45 670.5 |
| 35 | 5 908 747.4 | infeasible | 8 787 534 | infeasible | 4 837 873 |

Norms 16, 20, 22, 24 alone are infeasible at every rank. Norm 18 is the pivotal shell for r >= 37: it alone can satisfy the
programme (166 / 1 030 / 7 074 / 49 392 vectors), and if it is empty the other shells need 14 to 21 times more. (These are
the two pure scenarios, not a dichotomy: mixtures are feasible, e.g. Codex's witness at r = 43 with a_9 = 100,
a_8 = 20826/49, a_13 = 8916/49.) At r = 43 some shell has at least 140
vectors, hence some non-zero class of L1 / sqrt7 M (49 classes) contains at least 18 vectors of the same norm; their
pairwise differences are vectors of sqrt7 M that are not among the forced ones. At r = 35 at least 5.9 million vectors of
norm <= 26 are needed, with at least 4.8 million in one shell: a proof that every shell of norm 16..26 has fewer than
4.8 million vectors would exclude r = 35.

## 14. Difference lemmas (00:13 UTC)

Method (Codex): for two short binary vectors f, h whose difference g is a Fano vector, write R, U for the common positive
and negative vertices; they lie outside the support of g, where every vertex has 0 or 1 neighbour of each sign, and Z_g is
independent; count the edges between R and U in two ways.
* Codex: two norm-16 vectors never differ by a Fano vector (note 173); two norm-18 vectors neither (note 176, re-read by
  me). Hence every vector of norm 16 or 18 is orthogonal to all roots of M.
* **Lemma F (mine, sent to Codex for refereeing): two distinct Fano vectors never differ by a Fano vector.** Here
  r + s = 7, deg_U(r') = 4 - n(B1) in {3, 4} for r' in R, E = e(R,U) = 4r - x_R = 4s - x_U with 3r, 3s <= E <= rs; r = 0
  gives f = h; so {r, s} = {3, 4}, and then E = 12 = rs: R - U is complete bipartite K_{3,4} and two vertices of R have 4
  common neighbours. Contradiction.
  Corollaries: the roots of M are pairwise orthogonal (root system A_1^k, k <= 44), so **b_1 <= 88**; at r = 43 every
  Fano vector is a root of M, so a_7 <= 88 and the Fano vectors are pairwise orthogonal; for any r two distinct Fano
  vectors have |(f, h)| <= 6. In the LP (`roots88.py`) this cap changes neither the forced numbers nor the ladder.
* Lemma A (laptop session, completed by me, sent to Codex): for norm 18 with independent supports, root of type (2,1,1)
  (five second common neighbours in P, one partner of overlap 0, two of overlap 1) and a given missing second common
  neighbour, at most TWO vectors per seed: two such vectors have no sign crossing and differ by a vector of norm 16 or 14;
  a Fano difference is impossible (p0 would be in Z_g, but q3, q4 have no neighbour in P_g); a norm-16 difference has its
  seed at p* determined by f, hence is unique (one norm-16 vector per seed). Not done: different missing vertices, the
  type (1,1,1,1), supports with an edge. The per-seed count for norm 18 is probably of the order of ten, so seed counting
  alone is unlikely to reach the thresholds of section 13.

## 15. The identity behind the forced numbers (00:18 UTC)

Found by Codex at r = 43 from the Farkas certificate; closed form for all ranks checked exactly in my coordinates
(`identity43.py`, `OUTPUT_identity_N40.txt`). With m = (45 - r)/2, identically on the 7-parameter family:

    2 a_8 + 16 a_9 + a_13  =  329 (7^m + 1)  +  7^(m+1) b_1  +  7 a_7  +  7 a_10  +  2 a_11  +  a_12.

(329 (7^m + 1) = 2632, 16 450, 113 176, 790 258, 5 529 832 for r = 43, 41, 39, 37, 35.) So W = 2 a_8 + 16 a_9 + a_13 is at
least 329 (7^m + 1); vectors of norm 14, 20, 22, 24 and roots of M only increase what is needed. With a_8 <= 6930:
16 a_9 + a_13 >= 5 515 972 / 776 398 / 99 316 / 2 590 for r = 35 / 37 / 39 / 41. **A rank is excluded as soon as the numbers
of vectors of norm 18 and of norm 26 of L1 are shown to be too small for this.**
`caps18.py` (`OUTPUT_caps18_N84.txt`), exact LP with a cap on a_9: at r = 35 any cap a_9 <= 10^6 forces a_13 >= 4 837 873
(and a_10 + a_11 + a_12 >= 339 822); at r = 37, a_9 <= 10^4 forces a_13 >= 757 806; at r = 39, a_9 <= 1000 forces
a_13 >= 83 316; at r = 41 (resp. 43), a_9 = 0 forces a_13 >= 11 686 (resp. 1 870).
Norm 26 in L1: binary vectors of L with supports 13 + 13 (at most 4 edges in each support by the counting
2n^2 - 38n + 198 >= 6e + S2), vectors of L with entries +-2, and vectors phi - (1/3)1 of L1 \ L with phi = 1_S - e_z - e_z',
|S| = 35 (for the class L1 \ L: norm 22 is phi = 1_S with |S| = 33 inducing a 2-regular graph, every outside vertex with 6
neighbours in S; norm 24 is 1_S - e_z with |S| = 34; an entry 2 is impossible below norm 28).
