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

## 16. The programme in readable coordinates (00:20 UTC)

`bfroma.py` (`OUTPUT_bfroma_N40.txt`): the dual shell counts as exact affine functions of (a_7, ..., a_13); the coefficients
do not depend on the rank, only the constant and a power of 7 (m = (45 - r)/2):

    7^(m+1) b_1 = -329 (7^m + 1) - 7 a_7 + 2 a_8 + 16 a_9 - 7 a_10 - 2 a_11 - a_12 + a_13
    7^(m+1) b_2 = C2 + 2016 a_7 + 1139 a_8 - 149 a_9 + 693 a_10 + 233 a_11 + 92 a_12 - 43 a_13
    7^(m+1) b_3 = C3 + 901908 a_7 + 254068 a_8 + 74357 a_9 - 4494 a_10 - 5050 a_11 - 2770 a_12 + 859 a_13
    7^m     b_4 = C4 + 2014208 a_7 - 103618 a_8 - 193316 a_9 - 17472 a_10 + 5716 a_11 + 6407 a_12 - 1500 a_13

| r | C2 | C3 | C4 |
|---|---|---|---|
| 43 | 162 176 | 519 526 000 | 31 252 717 160 |
| 41 | 465 878 | 515 405 884 | 31 258 183 460 |
| 39 | 2 591 792 | 486 565 072 | 31 296 447 560 |
| 37 | 17 473 190 | 284 679 388 | 31 564 296 260 |
| 35 | 121 642 976 | -1 128 520 400 | 33 439 237 160 |

With b_1 >= 0, b_2 >= 462, b_3 >= 24 948:
* (I1) 2 a_8 + 16 a_9 + a_13 >= 329 (7^m + 1) + 7 a_7 + 7 a_10 + 2 a_11 + a_12;
* (I2) 149 a_9 + 43 a_13 <= U_r + 2016 a_7 + 1139 a_8 + 693 a_10 + 233 a_11 + 92 a_12, U_r = C2 - 462 * 7^(m+1) =
  139 538 / 307 412 / 1 482 530 / 9 708 356 / 67 289 138 for r = 43 / 41 / 39 / 37 / 35;
* (I3) binds only for r = 37 (right-hand constant 134.6 million) and r = 35 (4.06 billion).
Eliminating a_13 between (I1) and (I2):
539 a_9 + 1225 a_8 + 1715 a_7 + 392 a_10 + 147 a_11 + 49 a_12 >= 43 * 329 (7^m + 1) - U_r, i.e.
>= 399 938 / 3 384 038 / 24 272 738 / 170 493 638 for r = 41 / 39 / 37 / 35 (negative for r = 43). Since
1715 a_7 + 1225 a_8 <= about 13.6 million (seed bound), r = 37 needs 539 a_9 + 392 a_10 + 147 a_11 + 49 a_12 >= 10.7 million
and r = 35 needs it >= 157 million, in addition to the 4.8 million vectors of norm 26: these two ranks are within reach
of counting on the shells 18 to 24; the ranks 39, 41, 43 are satisfied by small numbers and are not.

## 17. Rank 35 against the 6-subsets: infeasible unless there are at least 43 induced 3 x 3 grids (01:05 UTC, 8 October)

Status: hand derivations of this section, exact LP, formulas tested on the two available graphs of the family. Sent to
Codex (bridge message 150); NOT yet audited by Codex. Scripts: `margins.py`, `sixsets.py`, `r35.py`, `theta3_maxG.py`.

### 17.1 Margins

`margins.py`: for each rank, the exact maximum of each dual shell b_k compatible with the constraints in use (audited
b_2, b_3, b_4, Codex's note-175 b_5..b_8, positivity, a_7k >= b_k, 7 a_7 + 8 a_8 <= 55 440, b_1 <= 88).

| r | max b_3 (bound in use 24 948) | max b_4 (bound in use 1 431 738) |
|---|---|---|
| 35 | 159 686 (x 6.4) | 4 011 586 (x 2.80) |
| 37 | 1 399 492 (x 56) | 27 968 995 (x 19.5) |
| 39 | 7 949 317 (x 319) | 183 220 501 (x 128) |
| 41 | 23 874 240 | 895 452 911 |
| 43 | 32 464 759 | 4 549 220 800 |

A proved b_4 >= 4 011 587 alone excludes r = 35. The option `b<k>=<value>` of the script is a what-if, never a result.

### 17.2 A correction to the distinctness criterion: the classes s and s -+ 9

M is the image of {psi in Z^99 : 3 | sum psi} under sqrt7 P, so psi and psi' give the same vector iff psi - psi' lies in
N' = Z^99 cap (E_3 + R 1) = {phi : (A - 3I) phi = t 1, t in Z}, with sum phi = 9t. N' contains K3 + (multiples of 1 that
are integral) with index 11 (det L = 9 * 7^(r-1) forces every t). So "psi - psi' is an integer 3-eigenvector" is the
criterion only when sum psi = sum psi'. For t = +-1:

**Lemma G.** If phi is integral with (A - 3I) phi = 1, then |phi|^2 >= 9, with equality iff phi = 1_R for an induced
3 x 3 rook's graph R ("grid"). Conversely every induced grid R satisfies (A - 3I) 1_R = 1.
Proof. sum phi = 9, so |phi|^2 >= sum |phi| >= 9, with equality iff phi is the indicator of a 9-set R. Then every vertex
of R has 4 neighbours in R and every outside vertex exactly 1. If x ~ y in R, their common neighbour has two neighbours in
R, so it is in R; if x, y in R are not adjacent, both common neighbours are in R for the same reason: R is an
srg(9,4,1,2). Conversely, in an induced grid an outside vertex has at most one neighbour (two adjacent neighbours would
put it on a line of R, two non-adjacent ones would be a third common neighbour), and the 9 * 10 = 90 outgoing edges
reach the 90 outside vertices once each.

Consequences. (1) The audited dual families have sum psi in {0, +-3}; their differences have sum 0, +-3, +-6: nothing
changes. (2) Any family with sum psi = +-6 or +-9 can coincide with the families of sum -+3 or 0 through grids.
(3) A grid is a relation: Q(1_R) = 0; its three rows satisfy t_T + t_T' + t_T'' = 0 in M.
Notation: P = number of prisms (two disjoint triangles joined by a perfect matching), rho = number of induced grids.
A grid contains 6 prisms and a prism lies in at most one grid: 6 rho <= P <= 1386 (a triangle lies in at most 12 prisms).

### 17.3 Family (a): 1_T - 1_path (sum 0, norm 8)

T a triangle, {u, m, v} an induced path (u ~ m ~ v, u not~ v) disjoint from T with no edge to T. Q = 18 - 2(3 + 2) = 8.
Count. N(T) has 36 vertices (no vertex has two neighbours in T), Far(T) has 60. A far vertex has 2 common neighbours
with each vertex of T, so 6 neighbours in N(T) and 8 in Far(T). A vertex x of N(a) has 3 neighbours in N(T) (its partner
on the triangle through a, one in N(b), one in N(c)) and 10 in Far(T). With n_i = number of triangles disjoint from T
having i vertices in N(T): 240 = 3 n_0 + n_1 (edges of Far), 360 = 2 n_1 + 2 n_2, 36 = n_2 + 3 n_3, and n_3 = P_T (the
prisms on T). Hence n_0 = 32 - P_T, n_1 = 144 + 3 P_T, n_2 = 36 - 3 P_T. Induced paths in Far(T): 60 * 28 - 3 n_0 =
1584 + 3 P_T. Total, two signs: 2 * 231 * 1584 + 6 * 2P = **731 808 + 12 P**.
Distinctness. All these vectors have sum 0, so only K3 matters. A 0/+-1 vector of K3 with positive support X and negative
support Y has deg_X(u) - deg_Y(u) = 3 on X: X has minimum degree 3, so |X| >= 6 with equality only for a prism (a graph
on 6 vertices with minimum degree 3 has 9 edges). For two members, X is inside T + path': an end of path' would need two
neighbours in T. Against 1_T1 - 1_T2 (one cross edge): Y = path + T1 would have to be a prism, but the three vertices of
a path are not a triangle. Against e_u - e_v and edge - far edge: |X| <= 5. The cases where supports overlap give
entries +-2 on a vertex whose neighbour sum would have to be +-6: checked directly, impossible each time.

### 17.4 Family (d): the 6-subsets (sum +-6)

For |W| = 6: Q(1_W) = 18 - 2 e(W) + 4 = 22 - 2 e(W). Norm 4: prisms (9 edges); norm 6: e(W) = 8; norm 8: e(W) = 7.
Distinctness inside the family: 1_W - 1_W' is 0/+-1 with supports of size <= 6, so W and W' are disjoint prisms
("twin prisms"). **All 6-sets with at most 8 edges give pairwise distinct vectors of M**, and 1_W is never -1_W'.
Types (the 6-vertex graphs in which adjacent vertices have at most 1 common neighbour and non-adjacent ones at most 2;
`sixsets.py abstract` confirms the list is complete) and numbers, for a graph with lambda = 1, mu = 2, degree k, with
T = vk/6 triangles, E = vk/2 edges, H = E(k-2) houses (triangle + 4-cycle on one of its edges), B = v C(k/2,2) bowties,
NA non-adjacent pairs; right column for (v,k) = (99,14):

| e | type | number | (99,14) |
|---|---|---|---|
| 7 | T1 bowtie + pendant at the centre | B(k-4) | 20 790 |
| 7 | T2 bowtie + pendant at an outer vertex | 4B(k-4) | 83 160 |
| 7 | T3 triangle and 4-cycle sharing a vertex | v(k/2)[C(k-2,2) - (k-2)/2] | 41 580 |
| 7 | T4 two triangles joined by one edge | 3T(k-2)(k-6)/4 + 3P | 16 632 + 3P |
| 7 | T5 house + pendant at the apex | H(k-4) + 6P | 83 160 + 6P |
| 7 | T6 house + pendant at a vertex of the shared edge | 2H(k-4) | 166 320 |
| 7 | T7 house + pendant at a far vertex | 2H(k-5) + 12P | 149 688 + 12P |
| 7 | T8 triangle and 5-cycle sharing an edge | 3T(k-2)(2k-9) + 6P | 158 004 + 6P |
| 7 | T9 two 4-cycles sharing an edge | E(k-2)(k-5)/2 + 3P | 37 422 + 3P |
| 7 | T10 4-cycle and 5-cycle sharing a 2-path | NA(2k-10) + 6P | 74 844 + 6P |
| 8 | U1 two triangles joined by two edges | 3T(k-2)/2 - 3P | 4158 - 3P |
| 8 | U2 bowtie + second common neighbour of two outer vertices | 4B | 8316 |
| 8 | U3 triangle with 4-cycles on two of its edges | H - 6P | 8316 - 6P |
| 9 | prism | P | P |

**N(6,7) = 831 600 + 36 P,  N(6,8) = 20 790 - 9 P,  N(6,9) = P.**
Sketches. T1: a third neighbour of the centre (k - 4). T2: a neighbour of an outer vertex a other than the centre, its
partner, and the two second common neighbours w_ac, w_ad. T3: two non-adjacent neighbours c, d of v outside the triangle
and their second common neighbour, which is never adjacent to a or b (v and it would have 3 common neighbours). T4: n_1.
T5: N(z) minus the line, minus the second common neighbours of z with p and with q, which coincide exactly when the house
is in a prism (6 houses per prism). T6: N(x) minus y, z, q and the partner of q. T7: N(p) minus y, q, their two partners
and the second common neighbour of z and p (= partner of q iff prism). T8: for z in N(u), x in N(w) non-adjacent, the two
common neighbours of z and x, minus those adjacent to u (k - 2 triples), to w (k - 2), or to t (k - 2 - P_T).
T9: pairs of 4-cycles on an edge, C(k-2,2), minus the pairs with p1 ~ r1 or p2 ~ r2, both at once iff a prism has the
edge as a rung. T10: for u, w non-adjacent with common neighbours m1, m2: s in N(u) not adjacent to m1, m2 (k - 4
choices), its two neighbours in N(w), minus the partners of m1, m2 on w; each correction disappears iff a prism.
U1: n_2. U3: each configuration is seen from two houses.
Test (`sixsets.py`, `OUTPUT_sixsets.txt`): on the rook's graph (k = 4, P = 6) by brute force over the 84 subsets; on
bvls243 (k = 22, P = 8910) through three edges, N = (#edges) * count / e; the 14 type counts agree with the formulas.
Limit of the test: both graphs are prism-saturated (P_T = k - 2), so the coefficient of P and the constant are tested
together, not separately; twin243_switched would separate them but is not edge-transitive (full enumeration about 45
minutes of Python: not run here).

Coincidences with the audited families (Lemma G; these are the only ones):
* norm 8: 1_W = e_z - 1_S in M iff W = (R - S) + z with R a grid, S a 4-cycle (9 per grid) or a paw (36) of R and z an
  outside vertex whose neighbour in R is not in S (50): 2250 per grid; W is then a bowtie or a house of R plus a
  pendant. 1_W = -1_Y iff W = R - Y, Y a 3-set of R with one edge: 36 per grid.
* norm 6: 1_W = -1_Y iff W = R - Y, Y an induced path of R: 36 per grid (W is of type U2).
The case z outside W gives an entry -1 with non-negative neighbours: impossible.

Hence, counting each coincident pair once (an over-subtraction if a set is hit by two grids, harmless for a lower bound):

    b_4 >= 1 431 738 + (731 808 + 12 P) + 2 (831 600 + 36 P - 2286 rho) = 3 826 746 + 84 P - 4572 rho,
    b_3 >= 24 948 + 2 (20 790 - 9 P - 36 rho)                           = 66 528 - 18 P - 72 rho.

Remark. The same argument shows more: for any sets W, W' the classes of 1_W and 1_W' can coincide only if W - W' and
W' - W each contain at least 9 edges (t = 0) or through a relation of N' with t /= 0. The numbers N(6,e) for e <= 6
would feed b_5, b_6, ...; they are not needed below and were not computed.

### 17.5 The LP (`r35.py`, `OUTPUT_r35_N84.txt`): variables b_1..b_7, P, rho

* rho = 0: **r = 35 is infeasible for every P.** Farkas certificate on a_8 >= 0, a_10 >= 0, a_11 >= 0, b_2 >= 462, the two
  bounds above, 7 a_7 + 8 a_8 <= 55 440, b_1 <= 88, P <= 1386. Codex's b_5..b_8 are not used.
* rho free: feasible; the minimum of rho is 42.02 (at P = 1386); P <= 400 is infeasible whatever rho; P = 500 needs
  rho >= 80.8 (of at most 83.3), P = 1000 needs rho >= 58.9.

**Statement (to be audited): rank_7(A - 3I) = 35 implies at least 43 induced 3 x 3 grids and more than 400 prisms.**
r = 37 stays feasible with the new bounds (max b_4 = 27.7 million, 7.2 times the bound).

### 17.6 The 3-side does not bound the grids

In the lattice E of section 11, rho is the shell count N_3(90/11). `theta3_maxG.py` (N = 24, d = 34): the 3-side LP allows
up to 24 459 384 grids. No help.

### 17.7 Open sub-problem

Close r = 35 by one of: a structural upper bound rho <= 42 (or P <= 400) for a hypothetical srg(99,14,1,2), at least under
rank 35; or families that survive grids: bowtie - far edge (at least 399 168 vectors, sum +-3; a coincidence needs a twin
configuration bowtie + two adjacent second common neighbours), far pairs of 4-sets with 4 edges (sum 0, of the order of
millions, count not determined by the parameters), 6-sets with 6 edges for b_5.

### 17.8 Side facts (consequences of sections 15 and 16; consistency checks, no new constraint)

* Eliminating a_13: 7^(m-1) b_2 = [C2 - 14147 (7^m + 1)]/49 + 35 a_7 - 43 * 7^(m-1) b_1 + 25 a_8 + 11 a_9 + 8 a_10 + 3 a_11
  + a_12. For r = 43: b_2 = 1000 - 8 a_7 + 25 a_8 + 11 a_9 + 8 a_10 + 3 a_11 + a_12 (using b_1 = a_7): without Fano
  vectors, M has at least 538 vectors of norm 4 that are not triangles.
* For r = 43, M* / M = F_49 (anisotropic) and M glued to the rank-4 lattice [2,1;1,4]^2 (det 49, level 7) is an even
  unimodular lattice of rank 48, in two inequivalent ways. The degree-2 zonal harmonic identity in weight 26 (a
  one-dimensional space of cusp forms), averaged over the two gluings and with a_7 = 0, reads
  a_13 + 14 b_2 = 16 632 + 348 a_8 + 138 a_9 + 119 a_10 + 44 a_11 + 15 a_12, which is exactly the combination of the
  two relations above (16 632 = 2632 + 14 000). The per-gluing version involves class-refined counts only.

### 17.9 Audit by Codex and the trade-off inequality (01:13 UTC)

Codex (bridge messages of 01:07 to 01:12 UTC) re-derived independently, with the extension identities of its note 175
(62 six-vertex types, 171 equations, rank 61, one free parameter fixed by the prisms): N(6,7) = 831 600 + 36 P,
N(6,8) = 20 790 - 9 P, N(6,9) = P, triangle minus far path = 731 808 + 12 P, and the grid collisions 36 / 36 / 2250. It
validated the exact certificate in its own eta coordinates and added the + 6 P already proved in its note 168 (the
differences of two triangles with one cross edge number exactly 33 264 + 6 P): b_4 >= 3 826 746 + 90 P - 4572 rho. Its
written proofs of the collisions were in progress at that time. With this bound the certificate is one inequality:

    rank 35  =>  101 160 rho + 4329 P >= 10 391 999,

hence rho >= 44 (P <= 1386) and, with 6 rho <= P, P >= 492. `tradeoff35.py` reproduces the three exact minima with my
LP (10 391 999; 878 401/20 232; 10 391 999/21 189). Codex also has N(6,6) = 8 560 860 - 84 P, giving
b_5 >= 35 123 088 - 168 P - 7212 rho, and the further shells up to b_11: the optimal trade-off is unchanged and r = 37
stays feasible with rho = P = 0.

Where the remaining region is (my reading, sent to Codex as message 152; the multiplicities below are not analysed):
* A prism Pi that is not in a grid has 30 far outside vertices spanning 42 + eps edges (eps = number of edges among the
  three thirds of the rungs), each in a triangle disjoint from Pi; with tau_300 / tau_210 the numbers of such triangles
  with no / exactly one edge to Pi: 3 tau_300 + tau_210 >= 30. The vector u_Pi - t_T has norm 4 in the first case and
  norm 6 in the second. If these are distinct in sufficient number, non-grid prisms cost more than they bring and the
  region collapses to "every prism lies in a grid", 82 <= rho <= 231.
* At rho = 231 the local structure is that of a quotient of the Hamming graph H(7,3) (as bvls243 is one of H(11,3)):
  all the local families collapse onto the audited ones, as they must since such graphs exist for other parameters. So
  the last region needs a global argument or counts with one more invariant.
* Standard language: the graph is the collinearity graph of a partial quadrangle PQ(2,6,2) and a grid is a sub-PQ(2,1,2);
  1_R - (1/11) 1 is a 3-eigenvector, so every vector of L sums to 0 on every grid, a 33-set of norm 22 meets every grid
  in 3 points, and the number rho_v of grids through v satisfies sum_{u ~ v} rho_u = 3 rho_v + rho.

### 17.10 Correction of 17.3, and a packing bound on the Fano vectors: a_7 <= 990; rank 35 infeasible (01:20 UTC)

Status: the correction is Codex's; the lemma and the LP runs below are mine and NOT yet audited.

**Correction (Codex, 01:15 UTC).** The distinctness argument of 17.3 covers two vectors of the same orientation only.
1_T - 1_Y and 1_Y2 - 1_T2 differ by (T + T2) - (Y + Y2), which is a 3-eigenvector when T + T2 and Y + Y2 are twin
prisms (a prism splits into two induced paths). Codex: 48 collisions per unordered pair of twin prisms, a class of twin
prisms has at most 6 members, so the number tau of such pairs is at most 5P/2, and the safe bounds are

    family (a) >= 731 808 + 12 P - 48 tau >= 731 808 - 108 P,      b_4 >= 3 826 746 - 30 P - 4572 rho

(with the + 6 P of its note 168). The statements of 17.5 and 17.9 (rho >= 43 or 44, P >= 492) hold only if there are no
twin prisms; unconditionally the same certificate gives 101 160 rho + 6369 P >= 10 391 999, i.e. rho >= 16, P >= 450.

**Lemma (seed packing).** Let (p0; U) and (p0; U') be two different seeds at the same vertex (U, U': four pairwise
non-adjacent neighbours of p0) which both extend to Fano vectors x, x' (p0 in P, U = Q cap N(p0)). Then |U cap U'| <= 2.
Proof. Let U = {q1,q2,q3,q4}, U' = {q1,q2,q3,q4*}, q4* /= q4. In a Fano configuration both common neighbours of two
vertices of Q lie in P, so P = {p0} + {c_ij}, c_ij the second common neighbour of q_i and q_j (a bijection with the six
pairs). So P cap P' contains p0, c_12, c_13, c_23 and Q cap Q' contains q1, q2, q3. P cap Q' is empty: a vertex of P is
p0 or c_ij with i, j <= 3 (in P'), or c_i4, adjacent to q_i in Q' (Q' is independent). Q cap P' is empty: q1, q2, q3 are
in Q', q4 is adjacent to p0 in P', and q5, q6, q7 cannot be a second common neighbour c' of x' since every c' is adjacent
to some q_i with i <= 3 and Q is independent. Hence (x, x') >= 7. x /= x' because q4 is not in Q' (p0 has exactly four
neighbours in Q'). So x - x' is a non-zero vector of L of norm 28 - 2 (x,x') <= 14, hence a Fano vector, against Lemma F
of section 14 (two Fano vectors never differ by a Fano vector).
Lemma F re-proved here: if y, z, y + z are Fano vectors, the supports of y and z overlap in a set D of 7 vertices with
opposite signs, D+ = P_y cap Q_z, D- = Q_y cap P_z, a + b = 7. Two vertices of D+ are two points of the biplane y and two
blocks of the biplane z: their two common neighbours are in Q_y and in P_z, i.e. in D-. A vertex of D- sees at most 4
vertices of D+, so 2 C(a,2) <= 6 b: a <= 4, and by symmetry b <= 4. For (a,b) = (4,3): the 12 incidences force two
vertices of D- adjacent to all four of D+ (the distribution 6+3+3 puts a pair in three neighbourhoods), and those two
have four common neighbours, against mu = 2.

**Corollary.** At p0 there are C(7,3) 2^3 = 280 triples of pairwise non-adjacent neighbours; each lies in at most one
extending seed and an extending seed contains four of them: at most 70 of the 560 seeds at p0 extend, 6930 in all, and
a Fano vector has 7 seeds: **a_7 <= 990** (before: 7920). With the weaker statement for two seeds differing on one line
only, a_7 <= 3960.

**LP** (`fanocap2.py`, `fanocap3.py`, `fanocap.py`; outputs `OUTPUT_fanocap*_N84.txt`), with a_7 <= 990 added:
* r = 35 with Codex's twin-safe b_4 (and even with the audited b_3 >= 24 948 only): **infeasible for all P and rho**, no
  hypothesis on grids or twin prisms. Certificate on a_10, a_11 >= 0, b_2 >= 462, b_3, b_4, 7 a_7 + 8 a_8 <= 55 440,
  b_1 <= 88, P <= 1386, 6 rho <= P, a_7 <= 990.
* Robustness: infeasible for a cap up to 1980, feasible at 2500. The family triangle minus far path is needed: with
  b_4 >= 3 094 938 + 78 P - 4572 rho rank 35 is feasible even at cap 990. With the audited dual bounds alone and the cap
  990, rank 35 is feasible but needs 8.0 million vectors of norm 16 to 26 (5.9 million before).
* With the cap 3960 and the uncorrected bound: rank 35 needs rho >= 201, P >= 1242 and a_7 >= 3201.
* r = 37, 39, 41, 43: unchanged by the cap (feasible with a_7 = 0).

**If the lemma and Codex's twin-safe count are confirmed, the window is {37, 39, 41, 43}.**
Next: the same packing argument for the vectors of norm 16 and 18 (Codex has their seed structure); rank 37 needs
539 a_9 + 392 a_10 + 147 a_11 + 49 a_12 >= 24.27 million - 1715 a_7 - 1225 a_8.

### 17.11 Rank 35 excluded: Codex's exact identity, re-verified here (01:23 UTC)

Codex (bridge, about 01:22 UTC) confirmed the seed-packing lemma with a shorter argument (every other positive vertex of
either Fano vector is the second common neighbour of a pair of its four seed neighbours, hence adjacent to one of the three
shared ones: no sign crossing; at least 4 common positive and 3 common negative vertices) and gave an exact identity in its
own eta coordinates, with no grid or twin parameter left: rho <= P/6, tau <= 5P/2 and P <= 1386 give uniformly
b_4 >= 3 826 746 - 792 P >= 2 729 034, and

    3110 a_9 + 5474 a_10 + 1328 a_11 + 68698 (b_3 - 24948) + 3822 (b_4 - 2729034) + 15559 (55440 - 7 a_7 - 8 a_8)
    + 876897 (990 - a_7) + 18880582 (88 - b_1) = -919 306 710.

`cert35.py` checks it in the coordinates of this directory (theta_lp.family(34)): the seven variable coefficients vanish
and the constant is -919 306 710 (`OUTPUT_cert35_N84.txt`). Every bracket is non-negative, so **no srg(99,14,1,2) has
rank_7(A - 3I) = 35**. Neither b_2 nor the shells beyond b_4 are used.

Inputs of this exclusion, with their status at the time of writing:
* theta set-up, Fricke relation, level and determinant: audited (Codex 168);
* b_3 >= 24 948, 7 a_7 + 8 a_8 <= 55 440, b_1 <= 88 (Lemma F): audited (Codex 172, 173, 176);
* a_7 <= 990: section 17.10, confirmed by Codex by message; its written note 180 was announced, not yet read here;
* b_4 >= 2 729 034: audited part 1 431 738 + 6 P (note 168); 6-sets with 7 edges 2 (831 600 + 36 P - 2286 rho) (17.4;
  counts and grid collisions re-derived by Codex, note 179); triangle minus far path 731 808 + 12 P - 48 tau (17.3 with
  Codex's correction, note 179).
The window is now **r in {37, 39, 41, 43}**.

`needs37.py` (what-if caps, not results): at r = 37 with a_7 <= 990 the LP needs nothing while a_9 is free; with
a_8 <= 866 and a_9 <= 20 000 it needs a_13 >= 621 497; with a_9 <= 1000, a_13 >= 1 064 831. Rank 37 lives on roughly
25 000 or more vectors of norm 18, or on more than 600 000 vectors of norm 26.

### 17.12 After the exclusion: Codex's note 180, and where rank 37 could give (01:28 UTC)

Codex's note 180 (branch codex/c1-arithmetic-audit, commit 7f22098) was read in full here: it states the packing lemma,
a_7 <= 990, the uniform bound b_4 >= 2 729 034 with the grid and twin losses of its note 179, and the integer identity;
its verifier imports no module of this directory and no LP solver. The inputs listed in 17.11 are the ones it uses.

Norm 18 (Codex, message of 01:27 UTC): the per-seed cap 12 covers the types (1,2,5) only, (2,0,6) is empty, the types
(0,4,4) and e = 1 are open; the Fano packing does not transfer as it stands (for a seed of type (0,4,4) only 4 of the 6
second common neighbours are in P, so two vectors sharing a triple may share only p0 on the positive side). No cap on a_9.

The identity of section 15 at r = 37 reads 2 a_8 + 16 a_9 + a_13 = 790 258 + 16 807 b_1 + 7 a_7 + 7 a_10 + 2 a_11 + a_12:
with a_8 <= 6930, rank 37 needs 16 a_9 + a_13 >= 776 398 (`needs37.py` gives the same picture).

Dual side (`frontier37.py`, `OUTPUT_frontier37_N84.txt`; WHAT-IF lower bounds on b_3 and b_4, not results; a_7 <= 990 and
the uniform proved b_5 >= 33 224 268 = 35 123 088 - 168 P - 7212 rho minimised over rho <= P/6, P <= 1386 (Codex's
correction: the first run used 35 million, which is not uniform; the table is the same at this resolution): rank 37 becomes infeasible for b_4 >= 18 million alone, or b_3 >= 150 000 with b_4 >= 15 million, or
b_3 >= 300 000 with b_4 >= 12 million, or b_3 >= 600 000 with b_4 >= 6 million, or b_3 >= 900 000 alone. Proved worst-case
values: 24 948 and 2 729 034.
Candidate source: the family (6,3), 1_W - 1_Y with |W| = 6, |Y| = 3 disjoint, Q = 28 - 2 (e(W) + e(Y) - e(W,Y)): norm 6
for an 8-edge set minus a far triangle, norm 8 for a 7-edge set minus a far triangle and for an 8-edge set minus a far
induced path. Heuristic sizes (not counts): about 7.7 and 7.9 million at norm 8, about 190 000 at norm 6. The 9-vertex
counts are not determined by the parameters and the collisions (prisms formed by a triangle of W and Y', grids, both
signs) are not analysed: proposed to Codex (message 156) as the next use of its census.

### 17.13 Resync on 8 October, and an end-to-end test of Codex's census on the real 243-graphs (07:12 UTC)

After a shutdown of the PC the three sessions resumed about 06:55 UTC with fresh usage. Codex's notes 179 to 184 were
read in full here (179-183 at 9fb98bf, 184 at ba41e4a). State taken from them: exact censuses of induced subgraphs of
orders 7, 8, 9 (208 / 916 / 5311 types; free invariants P, H, then seven dense 8-vertex types, then 48 more);
P <= 852, rho <= 126 (order 9); uniform bounds on distinct vectors b_3 >= 43 848, b_4 >= 3 371 634, b_5 >= 34 087 368;
representatives whose collisions are not yet all audited: (5,2) (audited, note 181), (4,4) F8 >= 2 723 490 (mass 8 done,
note 183), (6,3) N8 >= 10 336 557, (7,1) Q8 = 4 108 104 + 468 P - 512 H + 72 C14 - 12 (C13a + C13b + C13c). Rank 37 is
feasible in the LP: ceiling b_4 <= 16.5 million at b_3 = 43 848.
Split agreed by messages: Codex continues the collision audit of (4,4) then (6,3); the laptop session re-reads the three
lemmas of the rank-35 exclusion and studies the "negative triangle" exception of note 183 par. 5; this session tests the
census on real graphs and studies the family (7,1).

**Test.** `testbeds.py` (brute force: prisms, grids, H, bowtie or house with a far edge, far pairs of 4-sets with 4
edges) and `census_check243.py` (reads Codex's packet `data/codex_census_validation_243.json`, blob 993becea, as data;
measures the parameters with an induced-embedding search written here; counts every connected type with at most
4 million predicted embeddings within 200 s). Outputs: `OUTPUT_testbeds.txt`, `OUTPUT_census_check_*.txt`.

| graph | P | P_T | grids | H | cube | C8_5691760 | C14 | C13a | C13b | types checked | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bvls243 | 8910 | 20 everywhere | 1485 | 0 | 40 095 | 0 | 13 365 | 0 | 0 | 173 | 0 |
| twin243_switched | 2430 | 2 (240), 4 (540), 20 (111) | 405 | 0 | 14 175 | 43 200 | 3645 | 2160 | 6480 | 106 | 0 |
| rook 3 x 3 | 6 | 2 | 1 | 0 | 0 | 0 | 9 | 0 | 0 | 813 | 0 |

Families, packet formula at the measured parameters = separate brute force: bowtie minus far edge 24 057 000 /
23 979 240; house minus far edge 96 228 000 / 97 083 360; F8 685 865 070 / 700 146 990 (bvls / twin).
Hand formulas confirmed on the way (any v, k): bowtie minus far edge = B [(v - 5k + 11)(k - 10) + 4 (k - 6)] + 12 P + 2 H
with B = v C(k/2,2); a house has generically [(v - 5k + 12)(k - 10) + 5k - 28]/2 far edges (103 for (99,14)), and the
coefficient of P in the house count is -12 (k - 11) (-36 for k = 14).
Limits: H, C8_5683824 and C8_245715219 vanish in both 243-graphs, so their coefficients are not tested by real graphs;
sparse and disconnected types are tested only through the families; the packet stops at order 8 and Codex's order 9
uses another canonicalisation, so P <= 852, rho <= 126 and N8 are not covered by this test (an order-9 packet was
requested).

### 17.14 The family (7,1), the laptop session's audit, and a cap for cross-collisions (07:19 UTC)

**Family (7,1).** psi = 1_W - e_y, |W| = 7, y outside W, sum 6: Q = 28 - 2 (e(W) - deg_W(y)). Norm 8: type A (e(W) = 10,
y far from W) or B (e(W) = 11, y with one neighbour in W); norm 6: type C (e(W) = 11, y far). Codex's order-8 census
(note 184) gives the signed numbers of representatives for (99,14):
Q8 = 4 108 104 + 468 P - 512 H + 72 C14 - 12 (C13a + C13b + C13c), Q6 = 132 P + 46 H - 8 C14 (C14, C13x = numbers of its
8-vertex types with minimum degree 3 and 14 or 13 edges). `seven_one.py` counts the three branches by brute force on the
real graphs (all 7-sets with 10 or 11 edges, built from the 6-sets with 8 or 9 edges): twin243 144 996 480 / 1 837 080 /
1 574 640, bvls243 223 248 960 / 6 735 960 / 5 773 680, exactly the packet's predictions at the measured parameters.

Collisions found by hand (sent to Codex, message 169; NOT yet checked against its finite models):
* t = 0 against the 6-sets, same sign. Mass 6: W = prism + x, Z = (twin prism - y) + x: type A 300 per ordered pair of
  twins (x with one neighbour in the prism, y one of the 5 vertices of the twin not adjacent to x), type B 6 per ordered
  pair; in all 1224 tau at norm 8. Mass 7: W = D, Z = D' - y: 4 Omega at norm 8 (y = centre of D'), 24 Omega at norm 6
  (y a non-central vertex, against the 8-edge 6-sets).
* t = 0 among themselves: masses 6, 7, 8 (W = X - y' with X one of the 13- or 14-edge 8-vertex supports); not counted.
* t = 1 against -1_Y (3-set with one edge): W = grid minus a pair, 1620 per grid and per sign; against e_z - 1_S (old
  (4,1)): W = a prism of the grid plus z, S = the third line plus y, 9000 per grid and per sign. So at least 21 240 rho.
* against the negative (5,2): full cancellation impossible; only the uncancelled negative triangle remains.
* against the negative (6,3): four negative coordinates, and a new exception shape: an uncancelled negative 4-cycle
  (any uncancelled negative set must be 2-regular on itself and anticomplete to the positive part).

**Audit by the laptop session (07:20 UTC, relayed to Codex).** Hand re-derivation, no error found, of Lemma G, Lemma F,
the seed-packing lemma and a_7 <= 990, of Codex's note 179 par. 1, 3, 4, 5 and the arithmetic of par. 6, and of note 181
par. 2 to 4 and the assembly of its (3); every pair of norm-8 families behind (3) was listed with both signs and the sums
differing by 9. Not checked by it: the census numbers, the exact identity, the programs, notes 168 / 172 / 175.
On the exception of note 183 par. 5 (uncancelled negative triangle Y): only the sub-family (7,3,0) is concerned; the
positive part is binary; it is equivalent to a 12-set U inside the 60 vertices far from Y, inducing a 4-regular graph,
each of the 36 neighbours of Y having exactly two neighbours in U; it exists locally (three suitable grids), so it
cannot be excluded by local arguments.

**Cap (laptop session).** An injective family meets each projection class at most once. So for any family F and any
injective or already counted family I, classes(F + I) >= classes(F): the cross-collisions against I never cost more
than |I|, and one may take the maximum instead of the sum. For (6,3) against the 6-sets (grids and the triangle
exception together) the cost is at most 1 663 200 + 72 P. What has to be controlled exactly is the internal t = 0
collisions of the large families (same sign; masses 6 to 9).

### 17.15 Rank 37: what the LP optimum lives on; twins as a subgraph count; the 3-side again (07:29 UTC)

**Ceiling.** `ceiling37.py` (`OUTPUT_ceiling37_N84.txt`), with Codex's uniform bounds on distinct vectors
(b_3 >= 43 848, b_4 >= 3 371 634, b_5 >= 34 087 368) and a_7 <= 990: the maximum of b_4 is 16 499 433 and the maximum of
b_4 + (651/34) b_3 is 17 398 653 (the slope of the frontier beyond b_3 = 150 000). The optimum uses a_7 = 990, a_8 = 6063.75
(the whole seed budget), b_1 = 88 roots, about 2.05 million vectors of norm 24 and 4.3 million of norm 26, and no vector of
norm 18, 20, 22. What-if caps (hypothetical, to rank the levers) give for the coupled maximum: b_1 = 0: 17.05 million;
a_8 <= 866: 16.10 million; a_7 <= 500 and a_8 <= 866: 15.19 million; a_7 = 0: 15.41 million; a_7 = 0 and a_8 <= 866:
13.90 million. So a packing bound on the norm-16 vectors is worth about 1.3 million, the absence of Fano vectors about 2
million. Codex (message of 01:27 UTC) explained why the Fano packing does not transfer as it stands to norms 16 and 18.

**Twins are a subgraph count.** For disjoint X, Y of the same size m, Q(1_X - 1_Y) = 6m - 2 (e(X) + e(Y) - e(X,Y)); so
the two indicators have the same projection iff e(X) + e(Y) - e(X,Y) = 3m, and the "balanced outside" condition is a
consequence. In particular two disjoint prisms with no edge between them are always twins: tau = number of unordered
pairs of disjoint anticomplete prisms. Likewise two disjoint copies of D whose only cross edge joins the centres, two
disjoint anticomplete cubic 8-vertex supports, two disjoint grids (always joined by 9 edges). Consequence proposed to
Codex (message 171): a twin of Pi consists of two triangles far from Pi, so 4 tau <= number of pairs (prism, far
triangle), an affine function of the order-9 invariants (half of the signed count of the row "norm 4, e(W) = 9,
e(Y) = 3, no cross edge" of its note 182): a coupled bound on tau to use with tau <= 5P/2.
Order of magnitude of the internal collisions of (6,3) through one pair of twins (heuristic): several thousand; with tau
allowed up to 2130 the family can be wiped out in the twin-rich corner, so the bound on tau is decisive there.

**3-side, negative again.** `theta3_margins.py` (`OUTPUT_theta3_margins_N24.txt`): the largest dual shells
compatible with the 3-side LP are about 1.3 * 10^12 (norm 6) and 3 * 10^12 (norm 8) for r = 37, 4 * 10^14 and 10^15 for
r = 43, the same for N = 22, 24, 27. On that side two dual representatives collide only through a vector of L, so a
census of dense induced bipartite subgraphs would be clean, but the margins make it useless. Do not retry.

### 17.16 Codex's ORDER-9 census tested on the real 243-graphs; state of the collision audit (07:48 UTC)

**Test.** Packet `data/codex_census_validation_243.json` at e5ad4d2 (blob 3029fdfb), with a stage of order 9 (5311
types, 57 parameters: P, H, the seven dense 8-vertex types and 48 nine-vertex types of minimum degree 3).
`census_check243.py` measures the 57 parameters by its own induced-embedding search (about two minutes per graph;
options save= / load= split the work into bounded runs), then counts the connected order-9 types with at most 4 million
embeddings: twin243_switched 276 types, bvls243 40 types, all equal to the packet's formulas.
`six_three.py` counts nine of the ten branches of the family (6,3) by brute force (all 6-sets with 8 or 9 edges, then
the triangles, induced paths and "edge + far vertex" outside) and `six_three_730.py` the branch (7,3,0) on bvls243
through edge-transitivity (26 600 six-sets with 7 edges on an edge, 2 632 560 pairs with a far triangle). Signed counts,
packet prediction = brute force in every case:

| branch | twin243_switched | bvls243 |
|---|---|---|
| (8,3,0) | 19 746 720 | 8 981 280 |
| (8,3,1) | 87 190 560 | 42 340 320 |
| (8,2,0) | 1 485 473 040 | 679 369 680 |
| (9,3,0) | 355 320 | 1 176 120 |
| (9,3,1) | 1 995 840 | 7 698 240 |
| (9,3,2) | 1 547 100 | 5 292 540 |
| (9,2,0) | 29 114 640 | 107 133 840 |
| (9,2,1) | 105 811 920 | 386 836 560 |
| (9,1,0) | 336 639 240 | 1 233 963 720 |
| (7,3,0) | not done | 2 010 523 680 |

Measured parameters: bvls243 has only P = 8910, cube 40 095, C14 13 365, C9_1452856528 = 1 924 560, the grid 1485 and
C9_61547791256 = 160 380 non-zero; the twin has 29 non-zero parameters (23 of the 48 new ones).
Limits: (7,3,0) is not brute-forced on the twin; H, C8_5683824, C8_245715219 and 25 of the nine-vertex parameters vanish
in both graphs, so their coefficients are not tested by real graphs; P <= 852, rho <= 126, tau <= 1890 and the minima of
N8 are statements about (99,14) and are tested only through the code path that produces them.

**Collision audit (Codex's note 185 at d6e2e08, and the laptop session).** Codex: complete loss bound for (4,4),
L44 = 997 920 + 2794 tau + 272 Omega + (668/3) C14 + 72 / 32 / 128 times the three cubic types + 100 / 144 / 64 times the
three 13-edge types; tau <= 2P + 3 rho (a class of six twin prisms forces a grid) and tau <= 1890, N4 <= 17 325 (my bound
8 tau <= N4 is correct, its multiplier is zero in that certificate); for the (6,3) representatives
N8 + (651/34) N6 - 1000 tau >= 12 908 649.6, the same value as without the penalty (the penalty per twin pair is
exploratory, not a proved loss). No uniform gain yet.
Laptop session (hand, not refereed): for twins Pi, Pi' every colliding (6,3) representative is
1_Pi - 1_B - 1_B' + 1_C - 1_K with B in Pi, B' in Pi', C, K outside, |B| = |B'| = |C| = c, |K| = 3 - c, and Q = 8 reads
e(C) + e(K) - e(C,K) + e(B) + e(B') + sum_C g - sum_K g = 1 + 3c with g(v) = d(v) - deg_B(v) - deg_B'(v); all shapes are
listed; only three are rigid, the others contain free outside vertices, so the number of collisions per twin pair is not
a constant ("zero to a few thousand per pair and per sign"), in agreement with the estimate of 17.15. Mass 7: the same
reduction with |B| = |B'| = c + 1, |K| = 2 - c and right-hand side 2 + 3c - [a centre is removed]; it gives back the
7 * 7 of the (5,2) family. Its remarks: restricting (6,3) to e(W) <= 8 removes every collision involving a prism member;
the differences of two far triangles give b_3 >= 73 920 - 20 P - 72 rho - 4 tau.

**L1-side levers (what-if, `ceiling37.py`).** If the 280 independent triples of a vertex were shared between Fano and
norm-16 seeds (7 a_7 + 8 a_8 <= 6930 instead of 55 440), the coupled ceiling would be 15.89 million instead of 17.40; with
no root in addition, 15.54 million. The laptop session was asked to study whether the packing argument transfers to the
norm-16 cores and to mixed pairs (Fano, norm 16).

### 17.17 A 10-vertex family whose size reaches the norm-6 threshold: (5,5) (07:57 UTC)

Proposal sent to Codex (message 174); nothing here is a bound.
psi = 1_X - 1_Y, |X| = |Y| = 5 disjoint, sum 0: Q = 30 - 2 (e(X) + e(Y) - e(X,Y)). The 5-sets with 6 edges are the
bowties and the houses (2079 + 8316). Norm 6: X, Y both with 6 edges and anticomplete. Norm 8: (6, 5, anticomplete) in
both orders, and (6, 6, one cross edge).
Calibration on real graphs (`five_five.py`, `OUTPUT_five_five.txt`): the number of ordered far pairs of bowties/houses
is 170 178 840 on twin243_switched and 172 248 120 on bvls243, i.e. 0.513 and 0.519 times N^2 (f/v)^5. Transferred to
(99,14): about 0.6 million vectors of norm 6. By hand N(5,5) = 332 640 five-sets with 5 edges (33 264 induced pentagons,
41 580 + 91 476 + 83 160 triangles with pendants, 83 160 quadrangles with a pendant), so the anticomplete (6,5) pairs are
of the order of 40 million at norm 8.
Why: at rank 37 the LP is infeasible for b_3 >= 900 000 alone and for b_3 >= 600 000 with b_4 >= 5.91 million. This
family has sum 0 (no grid channel) and would not depend on the collision audit of (6,3).
Needs: an order-10 census (three disconnected types and their minima over the invariant polytope) and the supports of
mass 10. Caveats: the 0.6 million is a heuristic transfer; the minimum over the invariants may be far lower at some
corner; the collisions are not analysed.

Codex, same hour: b_3 >= 45 528 (far-triangle differences 7392 - 2P with 4 collisions per pair of twins, and the
inequality classes >= 2R/(k+1) - 2C/[k(k+1)] for R representatives with C colliding pairs, k = 3), note 186 at bf7cc29;
rank-37 ceiling 16 469 236.

### 17.18 My own census engine: full orders up to 10, all representatives of support <= 10, best case for rank 37 (08:24 UTC)

**Engine.** `census2.py` counts EMBEDDINGS x_H and uses, for a type H with a vertex u of degree <= 2 (G = H - u,
S = N(u)), the identity x_H = c(S) x_G - sum over the admissible strict supersets S' of S of x_(G + S'), with
c(empty) = v - m, c({i}) = k - deg_G(i), c({i,j}) = (1 or 2) - |N_G(i) cap N_G(j)|; every term has fewer vertices or more
edges; the types of minimum degree >= 3 are the parameters. Own canonical form (colour refinement, individualisation, twin
shortcut). Results for (99,14):
* types per order 2..10: 2, 4, 9, 21, 62, 208, 916, 5311, 42 430; new parameters at orders 6..10: 1, 1, 7, 48, 492;
* the type counts sum to C(99, n) identically (checked for n <= 9; skipped at order 10 for time);
* N(6,9) = P, N(6,8) = 20 790 - 9 P, N(6,7) = 831 600 + 36 P, N(6,6) = 8 560 860 - 84 P;
* `compare_census.py`: the 6533 formulas of Codex's packet at e5ad4d2 (orders 2 to 9) are reproduced coefficient by
  coefficient, parameters matched through the canonical form: 0 mismatch. Codex's exhaustive list of 492 ten-vertex
  types of minimum degree 3 agrees in number.
Orders 2..9 take 20 s; the full order 10 takes about 4 minutes (`OUTPUT_census2_99_order10.txt`). The 60 MB JSON of
the order-10 census is not committed (rebuild: `python -I census2.py census 10 99 14 <file> nocheck`).

**All representatives.** `reps10.py`: for every type and every split of all its vertices into W (+1) and Y (-1) with
3 | |W| - |Y|, Q = 3n - 2 (e(W) + e(Y) - e(W,Y)) + (|W| - |Y|)^2 / 9; the number of signed vectors 1_W - 1_Y of norm 4, 6,
8 of every shape as an affine form in the 549 parameters. Constant terms at norm 8: (1,1) 1386; (3,0) 49 896 per sign;
(2,2) 253 638; (4,1) 521 829 per sign; (6,0) 831 600 per sign; (3,3) 765 072; (5,2) 1 056 132 per sign; (7,1) 2 054 052
per sign; (4,4) 3 164 238; (9,0) 4 995 837 per sign; (6,3) 5 288 976 per sign; (8,2) 5 652 801 per sign; (5,5)
93 492 630. They reproduce the totals already known (3 826 746; 5 939 010 with (5,2); 4 108 104 for (7,1)). New shapes:
(9,0) (9-sets with 14 edges) and (8,2).

**Best case for rank 37** (`lp_reps10.py`, `lp_penalty10.py`; floating-point HiGHS, EXPLORATION: no certificate, no
collision removed). Minimum over the full order-10 polytope of r8 + (651/34) r6:
* supports <= 10: 66.6 million (r6 = 188 206, r8 = 63.0 million; (5,5) 12.4, (8,2) 13.5, (6,3) 13.5, (9,0) 10.3, (7,1)
  4.1, (4,4) 3.2 million at the optimum);
* supports <= 9: 39.7 million (r6 = 167 891, r8 = 36.5 million);
against the ceiling 17.40 million. The minimum of the norm-6 count of (5,5) alone is 0 (at P = 783).
At these optima P = H = 0 but the relaxation holds about 16 000 special supports (types of minimum degree >= 3) of order
8, 56 000 of order 9 and 3 to 4 million of order 10. With a penalty per special support the minimum collapses (20 000 per
prism and per D: 4.8 million for supports <= 9; 100 per order-9 support: negative). So the method lives or dies on the
collisions: realistic constants per twin pair at masses 6 and 7, and a bound on the number of twin PAIRS at masses 8 to
10, which the census does not see.

**Two structural remarks.** (1) A collision of mass m between representatives of supports n, n' needs 2m <= n + n'; for
mass 10 and supports 10 there is no free vertex. (2) A pure indicator 1_W collides at t = 0 with another indicator of the
same size only if W contains an induced subgraph of minimum degree >= 3: the 2-degenerate sets of a given size give
pairwise distinct classes (the 6-sets with at most 8 edges; the 2-degenerate 9-sets with 14 edges).

### 17.19 Where the rank-37 argument stands after the full order-10 census (08:38 UTC)

All LP values of this section are floating-point explorations over the full order-10 polytope of `census2.py`
(549 parameters, 46 439 distinct positivity constraints); none is a certificate.

**Caps on the special supports** (`lp_caps10.py`): P <= 852.92 (Codex's 11088/13, found here independently),
H <= 1867.25 (2079 at order 9), grid minus a vertex <= 1134 (= 9 * 126), the three 13-edge 8-vertex types <= 5122, 4158,
4158, the cube <= 3101.7, the two other cubic 8-vertex types <= 29 325 and 18 346; all order-8 supports <= 53 465; all
order-9 supports <= 476 669; all order-10 supports <= 8.86 million.

**Affordable losses** (`lp_penalty10.py`, supports <= 9, coupled form, base 39.7 million, ceiling 17.05 to 17.40
million): with a penalty per special support of 10 000 per prism alone the minimum is 38.5 million; 5000 per D alone:
32.8 million; 200 per order-8 support alone: 31.5 million (1000: negative); 30 per order-9 support alone: 28.2 million
(100: negative); (5000, 2000, 200, 30) together: 22.6 million. So masses 6 and 7 are comfortable; masses 8 and 9 are the
tight ones, because the relaxation holds tens and hundreds of thousands of supports, while a collision needs a TWIN
PAIR of supports.

**2-degenerate 9-sets** (`degenerate9.py`): of the 344 nine-vertex types with 14 edges, 243 are 2-degenerate; none
with 15 or 16 edges is. Number of 2-degenerate 9-sets with 14 edges: constant term 4 995 837, minimum 1 022 353 over the
polytope; all 9-sets with 14 edges: between 3.49 and 5.49 million. So this injective family adds about one million
vectors of norm 8 per sign in the worst case.

**Rigidity of twins of cubic supports.** If X, Y are anticomplete twins and X is 3-regular, every neighbour of a vertex
of Y outside Y is adjacent to X; so Y is a union of connected components of the graph induced on Far(X), all of whose
vertices have exactly 3 far neighbours. For a 9-support with 14 edges, Far(X) has 20 - n_3 vertices (n_3 = outside
vertices with three neighbours in X) and a twin has 8 of its 9 vertices there.

**L1 side: the laptop session's cuts** (its message of 08:30 UTC; hand proofs and a local CP-SAT search, not audited
here): roots are orthogonal to every other vector of norm 14, 16, 18; b_1 <= 78; a_7 + 4 b_1 <= 990;
7 a_7 + 8 a_8 + 273 b_1 <= 55 440; a Fano vector and a norm-16 vector sharing p0 and three negative neighbours have
inner product exactly 6, so their difference is a vector of norm 18 (no exclusivity of seeds). `ceiling37_lap.py`:
with these cuts the coupled ceiling is 17 048 350, the value of "no root"; the optimum then has b_1 = 0, a_7 = 990,
a_8 = 6063.75, a_9 = 28 102, a_13 = 335 434. What remains valuable on that side is a packing bound on a_8.

### 17.20 What was tried on the twin pairs and on the L1 side with the census (09:05 UTC)

All LP values are floating-point explorations over the full order-10 polytope.

* **Clean part** (`lp_clean9.py`): every representative with support <= 8 plus the 2-degenerate 9-sets with 14 edges,
  both signs: joint minimum of the coupled count 18.43 million (r8 = 15.23 million, r6 = 167 459). Above the ceiling by
  about one million only; with 5000 per prism and 2000 per D it is 13.6 million. So (6,3), (8,2), (5,5) are needed.
* **Class sizes.** If every class of M contained at most 2 representatives with support <= 9 (resp. at most 3 with
  support <= 10), rank 37 would be excluded (39.7 / 2 and 66.6 / 3 exceed 17.4 million). No such bound is available:
  the Gram argument on the 3-components only gives 7 (all pairwise masses 9) or 34 (masses >= 8).
* **Mass 9 for (6,3)**, 14-edge supports: the collisions of a twin pair (X, Y) are the pairs (B, B') with B a triangle
  of X avoiding the degree-4 vertex and B' an induced path or a suitable triangle of Y, or B a path and B' a triangle:
  at most t_X p_Y + t_X t_Y + p_X t_Y, zero when neither support has a triangle. `lp_caps9.py`: the eleven special
  9-supports with 14 edges are all MINIMAL (no special sub-support), ten of them contain a triangle, and the polytope
  allows 16 000 to 160 000 copies of each; `lp_pertype9.py`: a penalty per support of this size is not affordable. What
  is missing is a bound on the number of twin PAIRS.
* **The 3-side does not bound the twins** (`theta3_maxK3.py`): the maximum of the number of integer 3-eigenvectors of
  norm 12, 14, 16, 18, 20 compatible with the 3-side LP at rank 37 is 1.8 * 10^11, 1.3 * 10^13, 3.2 * 10^14,
  5.3 * 10^15, 6.6 * 10^16; with the caps tau <= 1890, Omega <= 1867, at most 126 grids the norms 16, 18, 20 still allow
  4.6 * 10^12, 7.9 * 10^13, 9.7 * 10^14. The laptop session found the same independently. Closed.
* **Laptop session, local searches (its message of 08:50 UTC):** twins of the three cubic 8-supports are locally
  possible, for the cube even in a prism-free local world; three norm-16 vectors can share p0 and three negative
  neighbours; four Fano vectors can share p0 and two neighbours. No packing bound on a_8 and no local obstruction to
  twins.
* **A census cap on the Fano vectors** (`fano_census.py`): a Fano configuration contains exactly 21 induced copies of
  one special 10-support F10 (5 + 5 vertices, 16 edges, degrees 3,3,3,3,4 on each side: remove two blocks and their two
  common points), and no other special support of order <= 10. A copy of F10 lies in at most one Fano configuration
  (it contains a full seed). So a_7 <= (2/21) N(F10), and the maximum of N(F10) over the polytope is 8841.7: a_7 <= 842
  (990 before). `norm16_census.py`: the five norm-16 cores of Codex's note 166 contain no special support of order
  <= 10 with a full seed (a 5 + 5 or 6 + 4 part of an 8 + 8 core has too few edges), so the census gives no cap on a_8
  at this order; order 12 (6 + 6 parts) would.
* **Codex's note 188** (cabec2e): for (6,3) with e(W) <= 8, both signs: mass 6 at most 756 tau (norm 6) and 12 814 tau
  (norm 8); mass 7 at most 108 Omega and 3612 Omega. Masses 8, 9 and the old families remain.

### 17.21 The twin-prism corner, and targeted computations above order 10 (09:14 UTC)

Exploratory floating LPs; nothing here is a bound to be used.

* **The dangerous corner is the twin-prism one** (`lp_no63.py`). Without the shape (6,3) the supports <= 9 give a
  coupled minimum of 24.8 million at P = 0; with a penalty of 30 000 per prism the optimum moves to P = 852.9 and the
  value falls to 4.5 million. Codex's proved losses per pair of twin prisms (12 814 for (6,3) at norm 8, 2794 for (4,4),
  432 for (5,2)) with tau <= 2P + 3 rho are of that size. So the number tau of pairs of disjoint anticomplete prisms
  is the decisive quantity.
* **Per prism** (frame identity sum_T (u, t_T)^2 = 84 and sum_T (u, t_T) = 0 for the norm-4 vector u of a prism): with
  tau_j = number of triangles disjoint from the prism and joined to it by j edges,
  3 tau_0 + tau_1 + tau_4 + 3 tau_5 + 6 tau_6 = 36; hence at most 12 far triangles, at most 6 twins (5 by the count of
  far vertices), and 4 tau <= 12 P.
* **Above order 10** (`census_target.py`, `lp_target.py`, `census_multi.py`, `lp_multi.py`; same recursion,
  top-down with memoisation on the full order-10 census): "prism + far house" (order 11) has a closure of only 44 types
  and 32 new parameters; its maximum over the enlarged polytope is 24 579, i.e. tau <= 2048, weaker than Codex's 1890.
  "prism + far prism" (order 12) is itself 3-regular, hence a new free parameter: no information below order 15.
  The closure of "prism + F" for all 21 five-vertex types F (16 815 types of order 11, 747 new parameters, 45 s) leaves
  the caps unchanged: P <= 852.92, H <= 1867.25, order-8 supports <= 53 465.
  Conclusion: neither the twins nor P can be cut further by positivity at orders 11 and 12 with targets of this kind.

### 17.22 Twin prisms charged to a census count; rank 43 in six parameters; profile C is a 22-coclique (10:05 UTC)

Status: hand derivations and floating LPs of the lab session, NOT audited; the rank-43 formulas are the laptop session's
(exact, reproduced by Codex in its own basis, note 191); the three profiles are Codex's (note 191).

**(a) Far triangles of a prism (laptop session).** With n_j = number of triangles disjoint from a prism and joined to
it by j edges: F = n_0 = 40 - n_3 - 3 n_4 - 6 n_5 - 10 n_6 and n_1 = 3 n_3 + 8 n_4 + 15 n_5 + 24 n_6 - 84 >= 0, so
F <= 12. A prism in a class of m twins has F >= 2(m-1), hence **4 tau <= Phi := number of pairs (prism, far triangle)**,
and Phi is a linear form of the order-9 census (the shape (6,3) at norm 4).
`lp_norm4.py` (`OUTPUT_lp_norm4.txt`): max Phi = 8483.3 over the order-10 polytope (tau <= 2120, weaker than Codex's
1890); with P >= 850, Phi <= 7514 (tau <= 1878); max (Phi - 12 P) = 0.

**(b) The twin-prism losses inside the LP** (`lp_phi.py`, `OUTPUT_lp_phi_9.txt`, `OUTPUT_lp_phi_9_no63.txt`). If the
collisions through twin prisms cost at most c per twin pair, the number of classes is at least R - (c/4) Phi. Minima
over the polytope, supports <= 9 (millions):

| c per twin pair | r8, all shapes | coupled, all shapes | r8, without (6,3) | coupled, without (6,3) |
|---|---|---|---|---|
| 0 | 32.42 | 39.69 | 19.79 | 24.78 |
| 3228 (= 2794 + 432, Codex's (4,4) and (5,2)) | | | 15.43 | 22.87 |
| 4000 | 28.64 | 37.87 | | |
| 6000 | | | 9.56 | 17.08 |
| 8000 | 20.20 | 29.86 | | |
| 16000 | 3.23 | 12.94 | | |

Ceilings at rank 37 (Codex, note 189, with a_7 <= 842): b_4 <= 16.23 million, b_4 + (651/34) b_3 <= 17.15 million.
Reading: with Codex's constant 12 814 the shape (6,3) costs more than it brings and should be dropped; without it the
coupled bound keeps 5.7 million of margin after the mass-6 norm-8 losses. Still to be paid from that margin: the norm-6
twin-prism collisions (about 140 per twin pair affordable, since each weighs 651/34), the masses 7 to 9, the
windmills and the grids. With b_4 alone the bound fails (15.43 < 16.23). Rank 37 remains open.
Remark for (6,3): inside the sub-family "Y a triangle far from W, e(W) = 7", a mass-6 collision forces either T, T'
disjoint, each a triangle of one of the twin prisms and W containing the other triangle of the prism of T', or T, T'
meeting in a common rung apex and W containing the 4-cycle of the two other rungs; the pattern 5 + 1 is impossible.
Not counted exactly.

**(c) Norm-4 representatives of support <= 10.** 3n - 2E + ((a-b)/3)^2 = 4 leaves only: triangle; prism; prism minus
far triangle; 9-set with 16 edges; (8-set with 14 edges) minus far edge. All but the triangle lie on a special support.
Maxima over the polytope (one sign): 852.9, 8483.3, 6839.2, 5670.

**(d) A refuted lever: sum-of-squares cuts** (`sos_tri.py`, `sos_flags.py`, `OUTPUT_sos_*.txt`). For a root
configuration sigma and rooted extensions ("flags") F, the matrix M[F,G] = sum over embeddings of c_F c_G is positive
semidefinite and LINEAR in the census counts; positivity of the counts does not imply it. Tested with roots triangle
(flags up to 3 extra vertices, orders <= 9, 124 flags), prism (2 extra, orders <= 10, 109 flags) and house (2 extra,
orders <= 9, 131 flags), at the max-P vertex and at the rank-37 optimum: no negative eigenvalue, no cut. For the
triangle root the whole matrix reduces to 231 * sum_T n3(T)^2 >= (2P)^2 (the order-6 extension counts of a triangle are
affine in n3(T)), which holds at the vertex (pairs of prisms on a common triangle: 8697 >= 5446). Not pursued.

**(e) Rank 43 (laptop session; reproduced by Codex).** With a_0 = b_0 = 1, a_1..a_6 = 0, b_1 = a_7 and a_7k = b_k the
theta series is affine in (a_7, ..., a_12):
    a_13 = 2632 + 56 a_7 - 2 a_8 - 16 a_9 + 7 a_10 + 2 a_11 + a_12
    b_2  = 1000 - 8 a_7 + 25 a_8 + 11 a_9 + 8 a_10 + 3 a_11 + a_12     (agrees with section 16 after b_1 = a_7)
    b_3  = 10648712 + 19388 a_7 + 5150 a_8 + 1237 a_9 + 31 a_10 - 68 a_11 - 39 a_12
    b_4  = 4464109880 + 275744 a_7 - 14374 a_8 - 24188 a_9 - 3996 a_10 + 388 a_11 + 701 a_12
Rank 43 is excluded as soon as one of: 2 a_8 + 16 a_9 + a_13 < 2632; b_2 < 922 (Codex: b_2 >= 462 + 41 b_1 + b_1^2/2
at every rank, hence 922 here); b_3 < 6 696 790. Dual counting cannot do it (millions of norm-6 and billions of norm-8
vectors are forced); a Gaussian count of short vectors of L1 and M agrees in order of magnitude with the forced
numbers, so only the frame can exclude this rank.
At rank 43 every norm-28 vector of L1 lies in 7 L1*, so b_2 = a_14, and the fractional ones have (Codex) three
profiles phi - 1/3: (A) 36 ones and three -1; (B) 33 ones, a 2 at v, -1 at two neighbours a, b of v, no 1 adjacent to
v; (C) 35 ones containing N(v), and -2 at v.

**(f) Profile C = a 22-coclique with a marked vertex (mine).** In profile C let R = {v} u (S - N(v)). The equations
A phi = -4 phi + 6 say: R is a coclique of size 22 and every outside vertex has exactly 4 neighbours in R. Conversely,
22 is the ratio bound 99 * 4 / 18, a coclique of that size has this regularity, and for every v in R the vector
phi = 1_N(v) + 1_(R-v) - 2 e_v has profile C. Hence: **44 norm-28 vectors of L1 per 22-coclique, and none otherwise.**
Formulas: P 1_R = 1_R - (2/9) 1, sigma = P 1_R - 7 P e_v. Consequences:
* points R, blocks the 77 outside vertices: a 2-(22,4,2) design; a block meets 6 blocks in 2 points (non-adjacent,
  no further common neighbour), 40 in one point (4 adjacent), 30 in none (6 adjacent); the graph induced on the 77
  blocks is 10-regular with spectrum 10, 3^33, (-1)^21, (-4)^22 and 77 triangles. No contradiction found.
* two 22-cocliques R, R' meeting in i vertices give the integer (-4)-eigenvector 1_R - 1_R' of norm 2(22 - i): so
  i <= 15, and i = 15 is a Fano vector (switching a coclique along a Fano configuration).
* at rank 43, y = [1_R]/7 lies in M + Z[e_v], has norm 22/9 (the frame vectors have 28/9), (y, [e_x]) = 7/9 on R and
  -2/9 outside, the 22 norm-4 vectors are y - [e_v] (pairwise inner product 1), and Q(y - y') = 2(22 - i)/7 must be an
  even integer: **two 22-cocliques meet in 1, 8 or 15 vertices** (15: a root; 8: an integral norm-28 vector).
Profile B in the same language: R' = S u (N(v) - {a,b}) (45 vertices, v outside), chi = 1_R' - e_v satisfies
A chi = -4 chi + 8, i.e. the degrees into R' are 4 + [x ~ v] on R', 8 + [x ~ v] outside, 12 at v; sigma = chi - 4/9
+ 7 P e_v. Profile A: a triangle Z forces S = N1(Z), so the non-triangle vectors have e(Z) <= 2 and
e(S) = 51 + e(Z), e(S,Z) = 30 + 2 e(Z), e(Z,O) = 12 - 4 e(Z), e(S,O) = 372 - 4 e(Z), e(O) = 228 + 4 e(Z); the prism is
Z = its rung apices, S = prism + its 30 far vertices.
Open: whether a srg(99,14,1,2) can have a 22-coclique.

### 17.23 The 22-cocliques: what they are worth, and what is known (10:20 UTC)

Status: results of the three sessions of the last hour; hand work, not audited unless stated.

* **Every Fano vector contains two 22-cocliques (laptop session).** For g = 1_P - 1_Q the 15 outside vertices Z_g
  without neighbour in the support are independent and anticomplete to P and Q (Codex, note 165), so P + Z_g and
  Q + Z_g are cocliques of size 22 meeting in 15 points. Hence a_7 = 2 * #{pairs of 22-cocliques meeting in 15 points},
  and a graph with at most one 22-coclique has no Fano vector.
* **b_1 <= 44 at every rank; b_2 >= 968 at rank 43 (Codex, being written up; chain re-read here).** For a root, g = sqrt7 r
  is a Fano vector of 7 L1*; for a 22-coclique T, 3 p_T = 3 * 1_T - (2/3) 1 lies in L1, so g(T) is 0 or +-7, and +-7 only
  for the two cocliques of g. The 2k cocliques of k root lines are distinct (if R_i = R_j then P_j lies in Z_i and
  g_j(S_i) = 7 - |Q_j cap Z_i| cannot be 0 or +-7). The centres h_i = p_Ri + p_Si are orthogonal to all roots and
  (9/2) Gram(h) = I mod 2, so k <= 22. At rank 43 the 2k cocliques give 88k profile-C vectors:
  b_2 >= 462 + 170 k + 2 k^2, and with b_2 >= 1000 - 16 k: b_2 >= 968.
* **Exact ceilings at rank 37** (`ceiling37_coclique.py`, `OUTPUT_ceiling37_coclique_N84.txt`): with a_7 <= 842 and
  b_1 <= 44: max b_4 = 16 014 183.8, max b_4 + (651/34) b_3 = 16 978 453.3; with the laptop session's cut
  a_7 + 4 b_1 <= 990 in addition: 15 979 604 and 16 950 588.3. **What-if a_7 = 0: 14 444 540.6 and 15 409 176.2.**
  With no Fano vector the b_4-alone ceiling would be below the b_4-alone lower bound 15.43 million of 17.22(b), so
  no norm-6 collision would have to be controlled.
* **Sub-designs (mine).** Inside a 22-coclique R, a Fano vector with positive support P in R is a 7-subset of R
  containing 7 blocks (a sub-design 2-(7,4,2)); two of them in the same R share at most one point (two common points
  give two common blocks, 6 common points, inner product >= 8, against |(f,h)| <= 6); so R carries at most 9, and
  a_7 <= 9 h with h the number of 22-cocliques.
* **A rank-22 lattice (mine).** W' = { x in E_(-4) : x = 0 on R } has dimension 22; the projector on W', on the 77
  blocks, is Pi[o,o'] = P[o,o'] + 2/63 - |o cap o'|/21, i.e. 2/7 on the diagonal, -1/7 for mates, -2/21 for adjacent
  disjoint blocks, -1/21 for two common points, 0 for one common point (non-adjacent), 1/21 for disjoint non-adjacent
  blocks; 21 Pi = 9 I + J - 3 G - N^t N. Lam = sqrt21 Pi(Z^77) = sqrt3 * (projection of M~ on W') is an even lattice of
  rank 22 generated by 77 vectors of norm 6, Lam* = L_0/sqrt21 with L_0 the integer (-4)-eigenvectors vanishing on R;
  every triangle of the graph projects to a vector of norm 6 of Lam (half of the norm of each triangle vector of M is
  in W'), and (z_T, z_T') = 3 G_T(T,T') - (1/9) u.u' + s s' with u = 1 + 3 * 1_(T cap R) - 3 * 1_(N1(T) cap R) on R and
  s = |T cap R| - 2/3. Determinant 3^a 7^b with a + b odd; not pinned down. Not exploited.
* No obstruction to a 22-coclique is known to any of the three sessions (design 2-(22,4,2); block graph 10-regular with
  spectrum 10, 3^33, (-1)^21, (-4)^22; all counts close). A direct search is the whole 99-vertex problem with one
  extra hypothesis: recorded as a possible computation, not launched (computations are parked).

### 17.24 The shape (6,3) by sub-family, and a certificate in b_4 alone (10:28 UTC)

`lp_f0.py` (`OUTPUT_lp_f0.txt`), floating LP, supports <= 9. The shape (6,3) at norm 8 by (e(W), e(Y), cross), one sign,
at the unpenalised optimum / minimum alone: (7,3,0) [W with 7 edges, Y a far triangle; "F0"] 2.51M / 2.10M;
(8,2,0) [W with 8 edges, Y a far induced path] 3.11M / 1.94M; (8,3,1) 0.56M / 0.40M; the three prism-based ones 0.
Bound in b_4 alone with F0 added to "all shapes except (6,3)", the twin-prism losses charged as
-((3228 + c_F0)/4) Phi (c_F0 = colliding pairs involving +-F0 per twin pair of prisms):
20.59M (c_F0 = 0), 19.53M (500), 18.47M (1000), 16.35M (2000), 12.10M (4000); without F0: 15.43M.
Ceiling in b_4 alone: 15.98M (Codex, note 192). So a certificate that uses no norm-6 vector exists as soon as c_F0 is
below about 2100 and the other channels fit in the remaining margin. Inside F0 a twin-prism collision has only two
patterns (17.22(b)); for the first one, with U, U' the triangles of the two prisms inside W, W', the three other
vertices W_0 of W lie among the 15 vertices having their prism neighbours in U and U' and the 24 vertices far from
both prisms, with e(W_0) + #(W_0 in the 15) = 4. My hand bound for the constant is only "a few hundred to a few
thousand": the exact maximum needs Codex's local-model enumeration (asked, bridge message 187).

### 17.25 The lattice of a 22-coclique: the laptop session's level-21 programme, and b = 2 at rank 43 (10:35 UTC)

Status: the programme and its numbers are the laptop session's (exact rational simplex, not refereed); the index bound
and the norm form are mine (hand); nothing audited.

* Determinant (laptop session, re-derived here): with iota the index in Z^22 of the restriction of L to R,
  det L = det L_0 * det(projection of L on span{P e_r}), the projection having Gram (7/3)(I - J/49) on the
  restrictions, so det L_0 = 3^21 7^(r-21) / iota^2 and **det Lam = 3 * 7^(43-r) * iota^2**; iota = 3^d 7^c.
* **c <= 1 (mine).** The restriction of L to R contains 3(e_r - e_s) (from 7P(e_r - e_s)), 27 e_r + 1 (from 63 P e_r),
  1 - 9 * 1_o (from 63 P e_o) and 7 * 1 (from 9 * 1_R - 2); modulo 3 A_21 these generate exactly
  { y : y = k 1 mod 3, 7 | sum y }, of index 3^21 * 7. Hence iota divides 3^21 * 7, so b := v_7(det Lam) is 43 - r or
  45 - r: 6 or 8 at rank 37, 4 or 6 at rank 39, 2 or 4 at rank 41, and, since at rank 43 every integral eigenvector
  sums to 0 mod 7 on R (c >= 1), **b = 2 exactly at rank 43**.
* The programme (laptop session): theta_Lam in M_11(Gamma_0(21), chi_-3) (dimension 28), Fricke partner theta_L0 with no
  term below q^7, all coefficients >= 0 up to q^34. No exclusion. With c_n the number of vectors of Lam of norm 2n:
  d = 0, b = 2: c_1 = 0 needs c_2 >= 13 953; d = 1, b = 2: c_2 >= 4 432; b = 6 or 8 are feasible with minimum 6;
  b >= 16 (d = 0) and b >= 14 (d = 1) are infeasible. Not run: d >= 2, the two partial duals.
* Norm form (mine): 21 Pi = 9 I + J - 3 G - N^t N, so for n in Z^77 with s = sum n,
  f(n) = |sqrt21 Pi n|^2 = 9 |n|^2 + s^2 - 3 n^t G n - |N n|^2 = 3 * min over real c in R^22 of Q(n on the blocks, c on R),
  the minimum being at c_r = d_r/3 - s/21 (d_r = (N n)_r). If N n = 0 then f(n) = 3 Q(n) >= 6. Sums and differences of
  at most three blocks have f >= 6. A 4-cycle of mates has f = 4 (at most 115 such cycles).
* Caveat: a generic even lattice of rank 22 and determinant 147 has about 2 500 vectors of norm <= 4 (Gaussian count)
  and minimum <= 4 (Hermite), so the thousands of norm-4 vectors asked for by the programme at rank 43 are not
  surprising; an exclusion of 22-cocliques at rank 43 by this route needs a classification of f(n) <= 4 for arbitrary
  n, i.e. of the integer (-4)-eigenvectors 21 Pi n vanishing on R of norm 42 or 84. Open.

### 17.26 CORRECTION of 17.22(b), and a structure theorem: the twin-prism corner is the grid corner (11:15 UTC)

Status: hand proofs and floating LPs of the lab session, sent to Codex and to the laptop session for attack; NOT audited.

**Correction.** The figures of 17.22(b) (22.87 million coupled, 15.43 million in b_4 alone, "5.7 million of margin")
charge the twin-prism losses of (4,4) and (5,2) ONLY, and the family contains all 14-edge 9-sets, including those that
contain a prism (they collide through every twin). With (9,0) restricted to 2-degenerate sets (`lp_route37.py`,
`OUTPUT_lp_route37.txt`) the bounds are 9.62 million (b_4) and 12.62 million (coupled): below the ceilings, before
(7,1), norm 6, masses 7-8, windmills and grids. The sub-family "W triangle-free" of (6,3) (Codex, note 193: 642 tau
+ 710 Omega) does not pay either (`lp_ftf.py`: it brings about 1.0 million and costs about 1.4 million).
Budget (`lp_corner.py`, `lp_grid.py`): with c the total twin-prism loss per twin pair over all shapes, the b_4-alone
bound for all shapes of support <= 9 is 29.23M (c = 4000), 21.68M (8000), 6.56M (16000), so c must stay below about
11 000 (ceiling 15.98M); Codex's proved constants already exceed 16 000. Rank 37 is NOT close with the present counts.

**Notation.** X a prism, Theta its three rung apices, N1 its 60 one-neighbour vertices; u = 1_N1 + 2 * 1_Theta =
(A - 3I) 1_X and (A + 4I) u = 12, so w in N1 has 8 - 2 theta(w) neighbours in N1 (theta = number of apex neighbours)
and an apex c has 4 - 2 theta'(c) neighbours in N1 (theta' = degree in Theta). A class = m pairwise far prisms (same
Theta, same N1, Codex); Z = the 36 - 6m vertices far from all of them.

**Theorem.**
(a) If Theta is a triangle, Theta + X is a 3 x 3 grid G, [1_X] = - t_Theta in M, and the twins of X are exactly the other
    grids through the line Theta (two prisms with the same triangular Theta are automatically far: a vertex outside a
    grid has exactly one neighbour in it; a common vertex forces a common rung and then equality). Class size =
    g(Theta), the number of grids containing the line Theta; g is 0, 1, 2, 3, 4 or 6 (for g prisms the vertices of Z each
    have one apex neighbour and Z is cubic; 6 leftover vertices would be one more prism).
    CORRECTION (laptop session, 11:50 UTC): a triangle inside Z gives a PRISM on Theta, not necessarily a grid (the
    mates of its vertices need not form a triangle), so Z is not always made of "long prisms" and the number of prisms
    on a line can exceed twice its number of grids; "never 5" is unaffected.
(b) If Theta is not a triangle, the class of X has at most 3 prisms. Proof for m >= 3: for w in N1 and an apex c let
    r_c(w) be the number of prisms where the neighbour of w is on the rung of c; r_c(w) <= 2 if w is not adjacent to c
    (common neighbours), r_c(w) = 0 if w ~ c, and the three r add up to m. So no w has two apex neighbours; if w ~ c
    then m <= 4, and for m = 4 the pairs (w, c'), (w, c'') have their two common neighbours on the rungs, so c is
    adjacent to no apex; as c has 4 - 2 theta'(c) neighbours in N1, m = 4 forces theta' in {0, 2} for every apex and
    m >= 5 forces theta' = 2. Finally m = 4 with Theta independent: the common neighbours of two apices lie in Z, each
    apex has exactly 2 neighbours in Z, so two vertices of Z are adjacent to all three apices: 3 common neighbours.
(c) Hence tau = (pairs inside non-grid classes) + (pairs of grids sharing a line) <= (P - 6 rho) + sum over lines of
    C(g, 2), with sum over lines of g = 6 rho; and the twin collisions of grid prisms are consequences of the grid
    relations 1_G = 0 (the sum-9 channel), not an independent channel.

**The LP corner is impossible.** With tau' <= min(Phi/4, P + 9 rho, 2P + 3 rho) as an LP variable (`lp_grid.py`,
`OUTPUT_lp_grid.txt`) every penalised optimum is exactly rho = 126, P = 756 = 6 rho, tau' = 1890 = 15 rho: all prisms
are grid prisms and every line with g > 0 has g = 6. But a line with g = 6 forces g >= 1 on the 18 lines meeting it,
so at that corner all 231 lines would have g = 6 and rho = 231. (The maximum rho = 126 of the order-10 polytope is
attained at a vertex with P = 756, 1134 grids-minus-a-vertex, 1890 of several types: a "pure grid world";
the binding counts are 10-vertex types such as "a line, one further line through each of its points, pairwise far,
plus a far vertex", `lp_rho_dual.py`.)
g(l) is the degree of l in the graph Xi_v on the 7 lines through any point v of l (adjacent = span a grid);
rho = (1/9) sum_v e(Xi_v); pairs of grids sharing a line = (1/3) sum_v #cherries(Xi_v). With graphical degree sequences
only, the maximum under rho <= 126 is still about 1570; if Xi_v is triangle-free it is at most 945; if no line lies
in three grids it is at most 378. A point with Xi_v = K_7 is a "locally Hamming" point: the graph is then the ball of
radius 2 of H(7,3) (1 + 14 + 84 = 99) with each second neighbour (ij; ab) adjacent to exactly one vertex of each of
the 10 grids G_kl with {k,l} disjoint from {i,j}.

**Open (the lock of rank 37 as I now see it):** which graphs Xi_v are possible (triangles? degrees 3, 4, 6?), and
whether a non-grid prism can have two twins. Negative results of the day on tau by census positivity: Phi/4 (2120),
prism + far house (2048), the 10-vertex supports "two prisms sharing a rung / two bowties joined by four edges"
contained three times in every twin pair (parameters 407 and 527 of my census; maxima 6397 and 13 754: tau <= 4615),
sum-of-squares cuts (nothing).

### 17.27 After Codex's cut 17 tau <= 17 P + 105 rho: the budget, the class quotient, the Fano coupling (11:30 UTC)

Status: floating LPs (exploration). Codex checked parts (a), (b) of the theorem of 17.26 and derived, with its bound
"at most 17 grids through a vertex" (its notes 105, 108) and g != 5: sum of C(d, 2) over the 7 lines at a point is at
most (69/17) e(Xi_v), hence pairs of grids sharing a line <= (207/17) rho and **17 tau <= 17 P + 105 rho** (to be
published by Codex).

* `lp_budget.py` (`OUTPUT_lp_budget.txt`): tau' an LP variable with 4 tau' <= Phi, tau' <= 2P + 3 rho,
  17 tau' <= 17 P + 105 rho; all shapes of support <= 9, b_4 alone; c = total number of colliding pairs per twin pair.
  Codex's class quotient (its note 186): classes >= 2R/(k+1) - 2C/(k(k+1)).
  k = 1: 24.32M (c = 8000), 12.05M (16000): affordable c about 13 400.
  k = 2: 16.21M (c = 16000), 12.12M (24000), 8.03M (32000): affordable c about 16 450.   (Ceiling 15.98M.)
  Every optimum is the pure grid point rho = 126, P = 756, tau' = 1534, R = 36.59M.
  Codex's proved constants for (6,3), (4,4), (5,2) add up to 16 040; (7,1), the 9-sets containing a prism, the
  cross-shape pairs and the other masses are not in. Short by a factor of the order of 1.5 (it was 3).
* Pairs of grids give twin structures by intersection: sharing a line (mass 6), a point (mass 8: the two grids minus
  the common point), or disjoint (mass 9: every vertex has exactly one neighbour in a grid). Two grids never share
  exactly 2 points (the difference would have a vertex of degree 2), nor more than a line.
  CORRECTION (Codex, 11:30 UTC): this does NOT mean that all twin structures of the LP's grid point are differences of
  grids; at that point the 8-vertex 13-edge parameter is 1890 (non-zero), so other proper supports are present and
  their twins, and the weighted windmills, must be controlled separately.
* `lp_joint.py` (`OUTPUT_lp_joint.txt`): coupling the ceiling to the census through a_7 <= (2/21) N(F10), with the
  ceiling replaced by the linear majorant 14.44M + 1900 a_7 (what-if, to be redone exactly). At the grid point
  N(F10) <= 3672, i.e. a_7 <= 350: with k = 2 and c = 16 000 the minimum is 15.58M against 14.44M (margin 1.14M
  instead of 0.23M); affordable c about 18 200.
* What would move it most: restrictions on the graphs Xi_v (grids through a vertex). At 3.4 line-sharing pairs per grid
  instead of 6.17 the grid point and the non-grid point (P = 852, rho = 0, tau <= 852) balance and the budget is
  about 24 000 (k = 1) to 30 000 (k = 2).

### 17.28 What a bound on the grids through a line would give (11:40 UTC)

`lp_beta.py` (`OUTPUT_lp_beta.txt`), floating what-if LPs: HYPOTHESES "pairs of grids sharing a line <= beta rho" and
"pairs inside non-grid classes <= gamma (P - 6 rho)"; tau' <= gamma (P - 6 rho) + beta rho, 4 tau' <= Phi; class quotient
k = 2; all shapes of support <= 9; b_4 alone (ceiling 15.98M). c = total number of colliding pairs per twin pair.

| beta, gamma | status | optimum | affordable c |
|---|---|---|---|
| 207/17 = 12.18, 1 | proved (Codex, with the theorem of 17.26; certified tau <= 1534, its note 194) | rho = 126, P = 756, tau' = 1534 | about 16 450 |
| 6, 1 | what-if | P = 853, rho = 53, tau' = 853 | about 30 300 |
| 3, 1 | what-if | P = 780, rho = 0, tau' = 780 | about 32 300 |
| 3, 1/2 | what-if | P = 850, tau' = 425 | about 60 000 |

beta = 6 is exactly "no line lies in 4 or 6 grids" (for degrees d <= 3, C(d,2) <= d, so the number of cherries of Xi_v is
at most 2 e(Xi_v)); below beta = 6.8 the pure grid point is no longer the worst point. So the statement that would
change rank 37 most is **g(l) <= 3 for every line**. For g = 6 the six grids through the line Theta = {v, a, a'} cover
39 vertices, and each of the 60 others is named by a duad of the six other lines from each of v, a, a', the three duads
forming a perfect matching of K_6; for g = 4 the 12 leftover vertices are a_k^+-, y(a, k^+-), y(a', k^+-) for the two
non-grid lines k. Neither is excluded by my counts. The project's earlier notes 103, 105, 108 (read today: no Hamming
point, L8; at most 17 grids through a vertex; the incomplete pairs at a vertex contain two disjoint pairs, D1) work in
the same setting with the "slot" calculus; Codex is asked to push it to "one universal class" and "one class of degree 4".
Also from Codex today: the 27-vertex cube H(3,3) is not an induced subgraph (72 outside vertices against 36 diagonal
triples); a triangle of Xi_v only gives the 19-vertex union of three grids, which passes the local budgets.

### 17.29 Two loss constants: grid twins and non-grid twins (11:40 UTC)

Codex's note 194 (commit 996baa2 of its branch) contains the class theorem of 17.26 with proofs, its cut
17 tau <= 17 P + 105 rho, the certified tau <= 1534 and b_3 >= 45766, and the new ceilings b_4 <= 15 975 390.7,
b_4 + (651/34) b_3 <= 16 851 675.0.

`lp_two.py` (`OUTPUT_lp_two.txt`), floating LP: tau_g = pairs of grids sharing a line, tau_n = pairs inside non-grid
classes, with 17 tau_g <= 207 rho, tau_n <= P - 6 rho, 4 (tau_g + tau_n) <= Phi; bound (2 r8 - c_g tau_g - c_n tau_n)/3
(class quotient k = 2), all shapes of support <= 9, b_4 alone:
(c_g, c_n) = (8000, 30000): 16.57M; (12000, 30000): 16.57M; (16000, 30000): 15.90M; (16000, 20000): 16.21M;
(12000, 40000): 13.98M. So the mass-6 channel closes in b_4 alone when, roughly, c_g <= 16 400 and c_n <= 32 000.
Request sent to Codex: recompute its per-pair maxima separately for the two types of twin pairs (in the grid case the
apices form a triangle, have no neighbour among the 60 one-neighbour vertices, and the collisions are the rewritings
by 1_G - 1_G'). Still outside this budget: masses 7, 8, 9, the weighted windmills, the single-grid (sum-9) channel,
and the exact certificate.

### 17.30 Codex's grid split, and the budget without the sub-family F0 (11:50 UTC)

Codex (exact, script not yet published): for a GRID twin pair the internal constant of (6,3), e(W) <= 8, is 12 182 at
norm 8 (12 814 for a non-grid pair) and 738 at norm 6 (756); F0 = (7,3,0) internal 7 496 (7 564); so the split gains
about 5 %. The 2794 of its note 185 for (4,4) is 2634 + 4 e(Theta) of mass six plus 160 reserved for the disjoint
mass-eight component.
`lp_nof0.py` (`OUTPUT_lp_nof0.txt`): without F0 the raw count at the grid point is 31.57M and the budget is about
10 200 colliding pairs per twin pair (k = 1; 22.37M at c = 6000, 16.23M at c = 10 000; k = 2 gives 15.93M at 10 000).
With F0: 16 450 (k = 2). Known mass-six constants for a grid pair: 12 182 + 2 646 + 432 = 15 260 with F0, about 7 800
without. In both cases only 1 000 to 2 500 pairs per twin pair are left for (7,1), the 9-sets containing a prism and the
cross-shape pairs: the pairwise accounting is too tight at tau = 1534. F0 is roughly break-even (it brings 5.0M and
may lose 7 496 * 1534 = 11.5M pairs).
Remark (mine): the collisions of F0 of the first pattern are genuine and come in classes of size exactly 2: with U a
triangle of W, [psi] = t_U - t_T + [1_W0], and t_U - t_T = t_U' - t_T' exactly when (U, T') and (T, U') are twin prisms;
so re-counting by distinct differences t_U - t_T removes nothing. The lever is tau (the structure of grids through a
line, 17.28), not the bookkeeping.

### 17.31 The window for rank 37 after Codex's note 195, and three more negative tests (12:10 UTC)

* Codex, note 195 (commit 006c793 of its branch, exact certificates): all binary mass-six same-sum channels for the
  shapes of support <= 9 (e(W) <= 8 for (6,3)) cost at most 29 204 colliding pairs per GRID twin pair and 31 976 per
  non-grid pair (22 422 / 23 150 without the 9-set indicators). In F0 the component "T, T' disjoint triangles of the two
  prisms" carries up to 7 304 of the 7 496.
* The window. Classes >= R^2/(R + 2C) (Cauchy-Schwarz; envelope of Codex's inequalities in k). With the ceiling
  b_4 <= 15.975M, rank 37 forces R + 2C >= R^2/15.975M: C >= 25.25M at the grid point (R = 36.59M), C >= 16.9M in the
  best case of the census (R = 32.42M). Certified cap: C <= 29 204 * 1534 = 44.8M. So 25.25M <= C <= 44.8M: the pairwise
  accounting misses by a factor 1.8 before the other channels (masses 7 to 9, windmills, single grid) are added; it
  would need tau <= about 860. It is a diagnostic, not a route. (My idea of counting by distinct differences
  t_U - t_T removes nothing: those collisions are genuine identifications.)
* CORRECTION (Codex, 12:10 UTC): the forced C is the TOTAL number of colliding pairs (all channels: masses 6 to 9,
  windmills, single grids), while 44.8M caps the binary mass-six same-sum channels only. So there is no "window" for
  the mass-six collisions, and nothing follows about rho or tau being near their maxima; and the integer-k family of
  Codex is slightly stronger than the smooth Cauchy-Schwarz expression. What remains true: the bounds proved so far
  are insufficient, by a factor of the order of 1.8 on the mass-six part alone.
* The ceiling side (laptop session's exact sensitivities): b_4 = 13.15M + 839 a_7 - 43.2 a_8 - 80.5 a_9 - 7.3 a_10
  + 2.4 a_11 + 2.7 a_12 - 0.62 a_13 on the feasible family; a cap a_13 <= 10^6 gives b_4 <= 13.4M and a_13 <= 3 * 10^5
  gives 11.0M; with 11.0M the forced C is 42.6M, almost the cap. An upper bound of a few 10^5 on the vectors of norm 26
  of L1 is therefore worth a factor 1.8 on tau. No such bound is known (no census coupling: a 13 + 13 eigenvector
  contains no forced special support of order <= 10; sphere-packing bounds do not exclude 3 million).
* Negative tests (`lp_line.py`, `OUTPUT_lp_line.txt`), suggested by the laptop session: sub-configurations of two grids
  on a common line T that contain T: K_3 x P_3 (order 9), the same plus one vertex of a third row, grid minus a vertex
  of T plus a rung of the other grid (order 10). Maxima 7560, 45 360, 22 680, i.e. 15 rho each time: the order-10
  polytope contains the pure grid world exactly. No cut.
* The laptop session's lattice fact (re-derived here): for every maximal totally isotropic I in D = L1/7L1*
  (q = norm/2 mod 7, dimension 45 - r), the preimage Lam# of I-perp is an even lattice of level 7, determinant 7^42,
  minimum >= 14, whose theta series satisfies the rank-43 relations, and M+ = (preimage of I)/sqrt7 is an even lattice
  of determinant 49 containing M. So every rank contains rank-43-type pairs; the only thing that separates rank 37 from
  rank 43 is the size of b_4 of M itself.

### 17.32 The L1 side again: what rank 37 requires on the shells of norm 18 to 24, in seeds (12:15 UTC)

`needs37b.py` (`OUTPUT_needs37b_N84.txt`), exact rational simplex, N = 84. Constraints: positivity, a_7k >= b_k, Codex's
dual lower bounds (b_2 >= 462, b_3 >= 45766, b_4 >= 3371634, ...), the seed budget 7 a_7 + 8 a_8 <= 55440, a_7 <= 842,
b_1 <= 44. No census, no collision count. Exact minima at rank 37:

| linear form | minimum | where |
|---|---|---|
| 539 a_9 + 392 a_10 + 147 a_11 + 49 a_12 | 15 241 976.8 | a_7 = 842, a_8 = 6193.25, a_9 = 28 278.25 |
| 9 a_9 + 10 a_10 + 11 a_11 + 12 a_12 | 254 504.25 | same point |
| 9 a_9 + ... + 12 a_12 + 13 a_13 | 436 723.9 | a_7 = 0, a_8 = 6930, a_9 = 48 524.9 |
| a_9 + a_10 + a_11 + a_12 | 28 278.25 | |
| a_9 + ... + a_13 | 48 524.9 | |
| 16 a_9 + a_13 | 776 398 | |

(The first line is b_2 >= 462 rewritten with section 16: 1715 a_7 + 1225 a_8 + 539 a_9 + 392 a_10 + 147 a_11 + 49 a_12
>= 24 272 738 + 722 701 b_1.)
Reading in seeds. A seed is (p0, U), U an independent 4-subset of N(p0): 99 * 560 = 55 440 seeds. A binary eigenvector of
norm 2n with independent supports has n positive vertices, each with exactly 4 negative neighbours, i.e. n seeds; the
vectors of norm 14 and 16 use each seed at most once (Codex: 7 a_7 + 8 a_8 <= 55 440). If every seed lies in at most
kappa_n signed eigenvectors of norm 2n, then a_9 <= 6160 kappa_18, a_10 <= 6930 kappa_20 (at least 8 clean seeds: at
most one edge per support, Codex), a_11 <= 5040 kappa_22, a_12 <= 4620 kappa_24 for the binary vectors with independent
supports, and the first line gives:
    **rank 37 is impossible as soon as  3 320 240 kappa_18 + 2 716 560 kappa_20 + 740 880 kappa_22 + 226 380 kappa_24
    (+ the same weights 539, 392, 147, 49 times the numbers of the other types: supports with edges, an entry 2 at norm
    24, the regular 33-sets at norm 22, the (34,1) profile at norm 24)  <  15 241 977.**
Examples: (kappa_18, kappa_20, kappa_22, kappa_24) = (2, 2, 2, 4) gives 14.47M; (3, 1, 2, 4) gives 15.07M; (4, 0, 2, 4)
gives 15.67M (not enough). On average rank 37 needs 4.59 eigenvectors of norm 18 to 24 per seed, in addition to the one
of norm 14 or 16. Known: one vector of norm 16 per seed (Codex); for norm 18 at most two per seed in the sub-case of
Lemma A (section 14); norm 20 is binary with at most one edge per support (Codex). This route is independent of the
grids and of all collision counts: it needs per-seed multiplicity lemmas for the norms 18, 20, 22, 24.

### 17.33 Codex's certified tau <= 1403 and the budget (12:17 UTC)

Codex (certified, to be published): with S = {v : at least 14 grids through v}, the SRG moment identities for the
numbers of neighbours in S and the spectral bound, the Xi degree profiles and the census cut P + 5 rho <= 1386:
tau <= 138943/99, i.e. **tau <= 1403** (1534 before).
`lp_budget2.py` (`OUTPUT_lp_budget2.txt`), floating LP with tau' <= 1403 and P + 5 rho <= 1386 added, all shapes of
support <= 9, b_4 alone: k = 2: 16.55M (c = 16 000), 14.67M (20 000), 10.37M (29 204); k = 1: 19.21M (12 000), 13.59M
(16 000). Optimum at P = 691, rho = 115.2, R = 36.04M. Affordable loss per twin pair about 17 200 (k = 2) against
Codex's joint mass-six constant 29 204: still short by a factor 1.7; tau <= about 830 would be needed.

### 17.34 Correction of the seed counts of 17.32 (Codex, 12:20 UTC)

Codex's precisions on the seed route (its notes 171, 176): a general norm-18 vector has only SIX clean seeds (nine when
the supports are independent), so a_9 <= 9240 kappa_18; proved at norm 18: the type (n0, n1, n2) = (2,0,6) is excluded,
the type (1,2,5) has at most 2 vectors per seed AND per missing point c among six, i.e. at most 12 per seed; the type
(0,4,4) and the supports with one edge are open. At norm 20: ten seeds if there is no edge, SEVEN guaranteed in the
one-edge case, so a_10 <= 7920 kappa_20; no uniqueness is proved. The bound "(x, y) >= 5 hence |x - y|^2 <= 4n - 10" for
two vectors on a common seed needs the absence of opposite-sign intersections outside the seed, proved only in
specific branches.
With these counts the norm-18 term of the threshold of 17.32 is 539 * 9240 kappa_18 = 4.98M kappa_18 against
15.24M: the route needs kappa_18 <= 2 and kappa_20 <= 1 or so, and the proved 12 per seed (one branch) is short by a
factor of at least 4. The examples "(2,2,2,4) suffices" of 17.32 used 9 and 8 seeds per vector and are too optimistic.
The seed route is therefore not closer than the collision route; it would become so only if the factor 6 (choice of
the missing point) could be removed.

### 17.35 Rank 37 in readable coordinates (laptop session), and the reference numbers after Codex's note 196 (12:27 UTC)

Reference numbers from now on (Codex, note 196, commit 1124c0e of its branch): tau <= 1403, b_3 >= 45 898,
b_4 <= 15 972 863.3, b_4 + (651/34) b_3 <= 16 851 675.0, P + 5 rho <= 1386.

The laptop session's exact parametrisation of the rank-37 family in (a_7, a_8, a_9, a_10; b_1, b_2, b_3), integer
coefficients (checked here against the exact LP):
    b_4  = 14 006 902 + 2793 a_7 + 532 a_8 + 77 a_9 + 7 a_10 - 8987 b_1 - 664 b_2 - 35 b_3
    a_11 =  -133 154 -  406 a_7 - 125 a_8 - 34 a_9 -  7 a_10 + 5726 b_1 + 273 b_2 +  7 b_3
    a_12 =   736 358 + 1183 a_7 + 350 a_8 + 91 a_9 + 13 a_10 - 2429 b_1 - 476 b_2 - 21 b_3
    a_13 = 1 260 308 +  378 a_7 +  98 a_8 +  7 a_9 +  6 a_10 + 25830 b_1 + 70 b_2 -  7 b_3
    a_14 = 5 097 168 -  288 a_7 + 98784 b_1 + 343 b_2
Consequences:
* b_4 + 35 b_3 + 664 b_2 + 8987 b_1 = 14 006 902 + 2793 a_7 + 532 a_8 + 77 a_9 + 7 a_10: with caps on a_9 and a_10 a
  vector of norm 6 of M weighs 35 and a vector of norm 4 weighs 664. Eliminating a_9 through a_11 >= 0 gives
  b_4 + (651/34) b_3 + 45.7 b_2 <= 13 705 347 + 1873.5 a_7 + 248.9 a_8 - 8.85 a_10 + 3981 b_1 (the coupled ceiling).
* At the b_4 optimum the adversary has a_7, a_8 at their caps and needs 273 b_2 + 7 b_3 + 5726 b_1 >= 1 249 131, i.e.
  b_2 about 2480: about 2000 non-triangle norm-4 vectors of M. An upper bound on b_2 would cut the ceiling.
* 3 a_11 + a_12 + 11 a_9 + 8 a_10 + 25 a_8 + 35 a_7 = 336 896 + 343 b_2 + 14 749 b_1 (49 times this is the threshold of
  17.32). With the floors b_2 = 462, b_3 = 45 528 and a_9 the only short shell, 91 a_11 + 34 a_12 = 13 413 960: about 29
  vectors of norm 22 or 85 of norm 24 per seed. So on the seed route the lemmas that matter most are at norms 22
  and 24 (and the regular 33-sets), where nothing is proved.
* A cap on a_13 is a floor on b_3: a_13 <= N means 7 b_3 >= 1 260 308 - N + ... ; a_14 >= 5.0 million vectors of norm
  28 in L1 are forced.
The laptop session's local model (CP-SAT, necessary conditions): two vectors of norm 16 on one seed are infeasible
(Codex's kappa_16 = 1 reproduced); two vectors of norm 18 on one seed are feasible with inner product 8 and infeasible
with inner product 5. Tests with 3 to 5 vectors per seed are running there.

### 17.36 Codex's coupled bound tau <= P + 5 rho + 17 (12:27 UTC)

Codex (certified, appended to its note 196): pairs of grids sharing a line <= 11 rho + 17, hence tau <= P + 5 rho + 17.
`lp_budget3.py` (`OUTPUT_lp_budget3.txt`), floating LP with this relation, P + 5 rho <= 1386 and tau' <= 1403: k = 2:
16.87M (c = 16 000), 15.00M (20 000), 10.70M (29 204); k = 1: 19.70M (12 000), 14.09M (16 000). The optimum is again the
vertex rho = 126, P = 756 (tau' = 1403, R = 36.53M). Affordable loss per twin pair about 17 900 (k = 2); the gap to
Codex's joint mass-six constant 29 204 is a factor 1.63.

### 17.37 Proposal: loss constants conditional on the pencil size (12:32 UTC)

Codex confirmed the three integer identities of 17.35 in its own basis and has no global upper bound on b_2. The
optimum of 17.36 multiplies two worst cases that cannot coexist: tau_g = 11 rho + 17 needs most pairs of grids to lie
in large pencils (lines in 6 or 4 grids), whereas the joint constant 29 204 is a maximum over all local profiles of one
twin pair, with free "far" vertices. Inside a pencil of 6 grids the 24 vertices far from a pair (X_i, X_j) are the
four other prisms (pairwise far, each vertex with its only neighbour in G_i and G_j on the line), and each of the 60
other vertices has exactly one neighbour in each prism; e.g. the sub-case of F0's dominant pattern where W_0 is a
triangle with two far vertices is then empty. Proposal sent to Codex (message 201): compute the joint mass-six maxima
c(6), c(4), c(3), c(2) per twin pair conditionally on the pencil size, and bound the loss by the sum over lines of
C(g, 2) c(g) inside its moment LP. If c(6), c(4) are near half of 29 204 the mass-six channel fits the budget
(about 17 900 on average) without a new structure theorem. Not yet computed.

### 17.38 The conditional constants do not drop; the representatives containing a grid prism are redundant (12:35 UTC)

* Codex (first conditional certificates, refined cells): the joint mass-six maximum per twin pair inside a pencil of
  six grids is 29 140 (29 204 before), 22 326 without the 9-set indicators; for a refined generic grid pair 29 144.
  So the proposal of 17.37 does not lower the constant at the level of its present cells. Codex is now MINIMISING the
  joint collision count on the same constraints.
* Hand count for the 9-set part in a pencil of six grids on Theta (rigid: the 60 other vertices induce an 8-regular
  graph with 240 edges, 20 triangles, 1620 induced 2-paths; each has one neighbour in each prism, none on Theta):
  the 9-sets X_i + W_0 with 14 edges and W_0 outside X_j: W_0 = a path among the 60 (1620), an apex with an adjacent
  pair of the 60 (720), an apex with a rung vertex of another prism and one of its neighbours among the 60 (240), two
  of the 60 with their common neighbour in another prism (120), a rung triangle of another prism (12), two apices
  with a vertex of the third rung of another prism (24): 2736 choices, 5472 colliding pairs with both signs, close to
  Codex's certified maximum for that part (about 6800). The maximum is essentially attained.
* Meaning: X_i + Theta is a grid, so [1_(X_i + W_0)] = [1_W0 - 1_Theta] when W_0 avoids Theta: the six 9-sets of the
  pencil are one vector of M, already represented by the shorter shape "W_0 minus the far triangle Theta". In a
  grid-rich graph the representatives containing a whole grid prism (in (9,0), (6,3), (7,1)) are redundant with
  representatives of smaller support through the single-grid relation: the raw count inflates with rho, the number of
  classes does not.
* Consequence (to be confirmed by Codex's minimum): at the vertex rho = 126 the true number of classes among the
  representatives of support <= 9 may be below the ceiling, in which case no accounting can exclude that vertex and
  the exits are a structural exclusion of the grid-rich region (P + 5 rho <= 1386 and tau_g <= 11 rho + 17 are both
  tight there; P + 5 rho <= 1386 says that the torsion sum over vertices is at least 30 rho) or families of support 10.

### 17.39 Codex's conditional audit, and what support 10 would allow (12:55 UTC)

* Codex (exact certificates, its note 197 in preparation): the joint mass-six maximum per grid twin pair conditional on
  the pencil size is c(2) = 29 144, c(3) = 29 142, c(4) = c(6) = 29 140 (non-grid: 31 976); F0's disjoint-triangle
  component 7056, 6970, 6872, 6660 for pencils of 2, 3, 4, 6; a universal LOWER bound of 14 430 mass-six colliding
  pairs per grid pair; uniform total of binary mass-six collisions for supports <= 9: at most 40 889 844.
  So the budget for supports <= 9 (about 25M in all, 17 900 per pair) lies between the certified minimum (20.2M for
  1403 grid pairs) and maximum (40.9M); nothing is decided, and at best about 3 500 pairs per twin pair would remain
  for all the other channels.
* Support 10 (`lp_vertex10.py`, `OUTPUT_lp_vertex10.txt`, floating LP, raw counts): at the grid-rich end (rho >= 125.9)
  r8 >= 36.07M for supports <= 9 and r8 >= 65.57M for supports <= 10 (32.42M and 55.72M over the whole polytope).
  Composition there, one sign: (6,3) 7.22M, (9,0) 4.73M, (7,1) 2.27M, (5,2) 1.05M, (6,0) 0.86M, (4,1) 0.52M;
  both signs: (5,5) 7.47M, (4,4) 2.99M, (3,3) 0.78M, (2,2) 0.25M; new shape (8,2): 10.34M per sign.
  With R = 65.57M the class quotient k = 2 allows 83.2M colliding pairs, about 59 300 per twin pair at tau = 1403:
  about 30 000 per grid pair would be available for everything involving (5,5) or (8,2). Their collision constants are
  not known; asked to Codex. If they are of the order of 60 000 the collision route is closed at this level too.

### 17.40 State of the three routes for rank 37 at 13:15 UTC

* **Collisions, supports <= 9.** Codex (certified, notes 197-198): the 9-set channel is exactly 5376 + 12 t_Z colliding
  pairs per pair of grids on a line (t_Z = number of triangles among the 24 vertices far from both prisms; my count of
  2736 choices in a pencil of six, generalised by first moments of the line types and re-checked here); joint binary
  mass-six constant per grid pair at most 27 828 (was 29 204), at least 14 430; budget about 17 900 per pair. Undecided,
  short by 1.55 on the certified constants; the other channels are not included.
* **Support 10.** Raw count 65.57M at the grid-rich end (17.39); the constants of (5,5) and (8,2) are not computed.
* **Seeds (L1 side).** CLOSED as a method (laptop session, local CP-SAT model with necessary conditions): two vectors of
  norm 16 on a seed are infeasible (as proved), but two vectors of norm 18 are feasible at inner products 7 to 10,
  THREE on one seed are feasible, vectors with different missing points coexist; kappa_18 = 3 alone gives 98 % of the
  need 11 a_9 + 8 a_10 + 3 a_11 + a_12 >= 311 061 and nothing is known at norms 22, 24.
* **A class-level constraint (laptop session).** The form (x, y) mod 7 on L1 factors through D = L1/7L1* of dimension
  45 - r, so the Gram matrix of ANY family of vectors of L1 has rank at most 45 - r modulo 7 (8 at rank 37, 2 at rank
  43): e.g. at rank 37 any nine vectors of L1 have a Gram determinant divisible by 7; at rank 41 orthogonality of
  non-root Fano vectors is transitive; for 22-cocliques the matrix (|C cap C'| - 1) has rank at most 45 - r mod 7 with
  zero diagonal (this is "1, 8, 15" at rank 43). It constrains configurations of the exotic short vectors, not their
  number; no exclusion from it so far.
* **Ceiling.** Needs caps on a_7 (22-cocliques), a_8, or an upper bound on b_2 (about 2000 non-triangle norm-4 vectors
  of M are needed at the b_4 optimum); none available.

### 17.41 The ceiling inside the census LP: the Fano coupling is worth 0.8 million (13:40 UTC)

Suggested by the laptop session. `lp_joint2.py` (`OUTPUT_lp_joint2.txt`), floating LP. Variables: the census
parameters, tau', and (a_7, a_8, a_9, a_10, b_1, b_2, b_3); the three integer identities of 17.35 with a_11, a_12,
a_13 >= 0; caps a_7 <= 842, 7 a_7 + 8 a_8 <= 55440, b_1 <= 44, b_2 >= 462 + 41 b_1, b_3 >= 45898, and the census coupling
a_7 <= (2/21) N(F10) used pointwise; census side with Codex's cuts (tau' <= 1403, P + 5 rho <= 1386,
tau' <= P + 5 rho + 17); floor (2 r8 - c tau')/3 for supports <= 9. Maximum of (ceiling - floor):

| c per twin pair | without the Fano coupling | with a_7 <= (2/21) N(F10) |
|---|---|---|
| 17 000 | -0.40M | -1.23M |
| 19 000 | +0.54M | -0.30M |
| 21 000 | +1.47M | +0.64M |

Break-even: about 17 850 without, about 19 600 with. The optimum stays at rho = 126, P = 756, tau' = 1403, where the
polytope allows only N(F10) <= 3648, i.e. a_7 <= 347; the adversary then has a_8 = 6626, a_9 = 2629, b_1 = 44, b_2 = 2266
and the ceiling is 15.20M instead of 16.0M. So the target for Codex's joint mass-six constant (certified interval
[16 496, 27 828] per pair of grids, note 198) moves from 17 900 to about 19 600. Still undecided.
Laptop session, end of its seed test: four vectors of norm 18 on one seed undecided after 2400 s; three are locally
feasible; the seed route stays closed as a method.

### 17.42 Joint LP: what each lever is worth; prism-free representatives (14:31 UTC)

All LPs below are floating point (HiGHS), exploration, same constraints as 17.41 plus `P >= 6 rho` and Codex's 22
secants of `b_2 >= 462 + 41 b_1 + b_1^2/2` at consecutive even `b_1` (b_1 is even). Nothing here excludes rank 37.

**For Codex's certificate.** `export_joint2.py` -> `joint2_forms.json`: exact rational forms of `r8` (all shapes of
support <= 9, by shape and summed), `Phi`, the parameter list with its numbering, the indices of P, rho, F10 and the
list of constraints of `lp_joint2.py`. Codex (its note 199, commit 5347cbc of its branch, certified): 4 N(F10) + 75 P
+ 96 rho <= 84546, hence a_7 + 13 rho <= 2013 (a_7 <= 374 at rho = 126), and
b_4 + (651/34) b_3 <= 15 457 549 + (450359/272) a_7 at rank 37. The value N(F10) <= 3648 of 17.41 is the value at the
joint optimum, not a uniform cap at rho = 126 (Codex: 3937.5 there).

**Break-even collision constant per twin pair** (`lp_joint3.py`; class quotient k = 2 unless said; the optimum is always
at rho = 126, P = 756, tau = 1403; to be compared with Codex's certified cap 27 828 for supports <= 9):

| scenario | break-even c |
|---|---|
| supports <= 9, as in 17.41 with the secants | 19 728 |
| what-if a_8 = 0 | 23 253 |
| what-if a_8 = a_9 = 0 | 23 813 |
| what-if a_8 = a_9 = a_10 = 0 | 24 238 |
| supports <= 9, quotient k = 3 | 12 130 |
| supports <= 10, k = 2 / 3 / 4 / 5 | 61 756 / 76 384 / 80 177 / 73 138 |

* Caps on the short shells of L1 cannot close the gap alone: without any vector of norm 16, 18, 20 the break-even is
  24 238 < 27 828 (the adversary replaces a_8 by a_9, then a_10, then nothing).
* The b_3 floor inside the same LP (`b3floor=<c6>`: b_3 >= (2 r6 - c6 tau)/3, norm-6 representatives of support <= 9):
  break-even 32 316, 29 444, 26 572 for c6 = 0, 150, 300; i.e. the condition is **c8 + (651/34) c6 <= 32 316**
  (c6 <= 234 at c8 = 27 828); for c6 >= about 550 the floor is not binding. For supports <= 10 and c6 = 0: 91 394.
  r6 = 455 795 at that vertex. No certified c6 is known to me.
* For supports <= 10 the best quotient is k = 4: 80 177 colliding pairs per twin pair would be affordable, if ALL
  same-class pairs (all channels) are counted.

**Laptop session's Lemma N16** (its message of 13:58 UTC; checked by hand here, every step): a vector of norm 16
(binary, independent supports, Codex's note 166) cannot be non-zero at a point p0 with seed lines l_1..l_4 and other
lines l_5, l_6, l_7 when the six pairs of seed lines and the three pairs of other lines all span grids. Tools: x sums
to 0 on every grid (a vertex outside a grid has exactly one neighbour in it, so 1_G - 1/11 is in E_3); corners of two
grids through p0 sharing a line are never adjacent; without a common line each corner has exactly one neighbour among
the corners of the other; counting 3 + pi + nu <= 4 negatives and 6 + nu + pi <= 7 positives and three cases. Its
solver gives the complete list of minimal forbidding sets (7 to 17 grids). Worth: it bites only at points with at
least four lines in six grids; by the table above even a_8 = 0 moves the break-even by 3525 only.

**Prism-free representatives** (`reps10_pf.py`, `reps10_pf.json`, `OUTPUT_reps10_pf.txt`: exact forms). Class "pf":
neither W nor Y contains an induced prism; class "fp": one of them does. If psi and psi' = psi - 1_X + 1_X' are both
binary (X, X' twin prisms), with A = W cap X, B = Y cap X', then psi' has X' minus B in W' and X minus A in Y'. So:
* a collision between two pf representatives through a twin pair is two-sided, 1 <= |A|, |B| <= 5, and each
  representative has ONE partner for that twin pair;
* a full swap (A = X) only involves fp representatives; in a pencil of g grids on Theta the g representatives
  1_(X_k) + rho are one class, equal to the class of rho - 1_Theta (17.38): the fp representatives bring no class
  that a shorter representative does not already give. So the right family is pf, and its natural quotient is k = 1
  (classes >= R - C, exact when the classes have at most two representatives).
* Coefficient of P in the fp counts (representatives containing a given prism, before the corrections by the other
  parameters): (9,0) 3480, (6,3) 2940, (7,1) 1680, (8,2) 9210 per sign. Exact hand count for (7,1): 1200 + 180 + 24
  = 1404 per sign (z among the 60, y among the 24 far vertices, not adjacent: 60 * 24 - 240; z an apex, y among the
  60; z an apex and y one of its 8 far neighbours); (9,0): 2688 + 6 t_Z (17.40).

`lp_family.py` (`OUTPUT_lp_family.txt`, `OUTPUT_lp_family_s10.txt`): joint LP for the pf family; R at the worst
vertex and the break-even number c of two-sided colliding pairs per twin pair:

| family (pf) | R (min over the polytope / at rho = 126) | break-even c, k = 1 | k = 2 |
|---|---|---|---|
| supports <= 9, all shapes | 24.0M / 25.6M | 7 447 | 2 668 |
| supports <= 10, all shapes | 39.4M / 41.3M | 18 616 | 26 404 |
| supports <= 10 without (5,5) | 30.8M / 33.0M | 12 707 | |
| supports <= 10, min(a,b) <= 2 | 17.1M | 1 686 | |
| sign-pure only; min(a,b) <= 1 | 5.3M; 8.0M | not excluded even with c = 0 | |

Reading.
* Supports <= 9: at the grid-rich vertex 25.6M pf representatives against a ceiling of 15.14M. If the pf classes have
  at most two representatives, the number of classes is between 12.8M and 25.6M: the exclusion holds iff fewer than
  82 % of the pf representatives are in a collision (10.45M pairs). Neither side is known. This is the same undecided
  ratio as 19 728 against [16 496, 27 828], but it is now a statement about pf pairs only.
* Supports <= 10: 41.3M pf representatives. "At most two representatives per class" would give 20.6M > 15.2M, an
  exclusion; "at most three" gives 13.8M, nothing.
* NOT handled, and of first order in a grid-rich graph: the single-grid relation. If Y contains exactly four points
  B of a grid G and psi has no other point in G, then psi + 1_G is binary, pf, of support |psi| + 1, in the same
  class: (9,0) with a bowtie of a grid in W <-> (4,4); (0,9) with four points of a grid in Y <-> (5,5); (3,6) <-> (8,2).
  At rho = 126 about 55 % of the squares and paws lie in grids, so a large part of the representatives of support 10
  repeats classes of support 9 and conversely. This relation has sum 9, it is not a twin relation, and it is counted
  per grid, not per twin pair. Any accounting for supports <= 10 must include it; for supports <= 9 it is the
  "single-grid channel" still outside Codex's mass-six totals (17.29, 17.31).

### 17.43 Two more negative tests, and the laptop session's "shortest representative" principle (14:40 UTC)

* **The ceiling side cannot close supports <= 9 at all.** Hand estimate at the vertex (rho = 126, tau = 1403,
  r8 = 36.57M): with NO vector of norm 14 to 20 in L1 and no root (a_7 = a_8 = a_9 = a_10 = 0, b_1 = 0, b_2 = 462,
  b_3 = 45 898) the ceiling is 14 006 902 - 664 * 462 - 35 * 45 898 = 12.09M and the break-even of the k = 2 accounting
  is (2 * 36.57M - 3 * 12.09M)/1403 = about 26 300 < 27 828. So with the certified collision cap, every possible
  progress on a_7, a_8, a_9, a_10, b_1 together is still insufficient: the gain has to come from the floor.
* **Norm-6 floor from prism-free representatives** (`lp_n6.py`, `OUTPUT_lp_n6.txt`): b_3 >= R6(pf) - c6 tau inside the
  joint LP, norm-8 floor with c8 = 27 828. Even with c6 = 0 the maximum of (ceiling - floor) is +2.42M (3.79M without):
  at the vertex the order-10 polytope allows R6(pf) = 60 346 only, for supports <= 9 and <= 10 alike (the (6,3), (5,5),
  (8,2) prism-free counts of norm 6 can be driven to zero there; composition (1,1) 8316, (3,0) 8316 per sign, (3,3)
  5880, (6,0) 13 986 per sign, (9,0) 773 per sign). Not a route in this relaxation.
  Remark: the raw norm-6 count of 17.42 (r6 = 455 795) is inflated by the representatives containing a prism: a
  9-set "prism X of a grid + a triangle T forming a prism with one triangle of X" is the class t_T - t_Theta, one of
  the 7392 - 2P far-triangle differences.
* **Laptop session (14:40 UTC, hand; I agree with the statements I could check).** Classes are cosets psi + K, K the
  kernel lattice; count only the representatives that are SHORTEST in their coset (smallest support for 0/+-1
  vectors): b_4 >= sum over shortest psi of 1/(number of shortest vectors of the coset). psi is a longer copy iff
  some phi in K has 2 (psi, phi) > |phi|^2; two shortest ones differ by a tie 2 (psi, phi) = |phi|^2.
  - phi = 1_G: |phi|^2 = 9 is odd, so a single grid never gives a tie; psi is a copy iff |psi(G)| >= 5. In
    (9,0) <-> (4,4), (0,9) <-> (5,5), (3,6) <-> (8,2) the member with five points of the grid is the copy.
  - phi = 1_G - 1_G' for disjoint grids (|phi|^2 = 18): no tie inside |psi(G)| <= 4.
  - grids meeting in one point: a tie of mass 8 for (4,4) (four points of G - p in W, four of G' - p in Y);
  - grids on a line (twin prisms): tie iff |A| + |B| = 6; copy iff > 6 (a whole prism is the crude case: this is why
    "prism-free" was the right restriction in 17.42).
  So the right numerator is the POOL {Q = 8, support <= 10, |psi(G)| <= 4 for every grid, at most half of every twin
  pair}, and the raw count of support 10 is not: if the pool at rho = 126 is below about twice the ceiling, supports
  <= 10 cannot conclude either. The pool is not an intrinsic condition (it needs the grid around five points), so the
  census does not give it; an upper bound per grid is a local enumeration of the kind Codex does.
  Multiplicity three exists in principle (W with four points of X_i, Y with two points of X_j and two of X_k).

### 17.44 CORRECTION: the break-even of 17.27, 17.41, 17.42 was computed on a larger collection than Codex's cap (14:47 UTC)

Codex (reply to my message 211): its certified interval [16 496, 27 828] per pair of grids on a line is for the
collection "all shapes of support <= 9, with (6,3) and (3,6) restricted to e <= 8 on the 6-set", i.e. WITHOUT the
(6,3) representatives whose 6-set is a prism. My r8 contained them (about 4.1 million at the vertex), and their full
swaps are not in the 27 828. So "19 600 (or 19 728) against [16 496, 27 828], undecided" compared two different
collections. Redone on Codex's collection (`lp_family.py`, scenario `m5s9k2x63`, `OUTPUT_lp_family_x63.txt`):

| collection (supports <= 9), quotient k = 2 | R at the vertex | break-even c per twin pair |
|---|---|---|
| all representatives (what I used) | 36.57M | 19 728 |
| Codex's collection (no prism 6-set in (6,3)) | 32.43M | about 13 900 |
| same, k = 3 | 32.5M | about 3 350 |

The break-even 13 900 is BELOW the certified minimum 16 496: on that collection the pairwise accounting with k = 2
cannot exclude the vertex rho = 126, tau = 1403, whatever the true constant. So this accounting is closed for supports
<= 9, not "undecided". (The parameter numbering of `joint2_forms.json` is identical to Codex's archive; the
single-grid relations are not in its C6; its 738/756 norm-6 numbers concerned (6,3) with e(W) <= 8 only.)

What is left open on the floor side: the pool accounting of 17.42/17.43 (prism-free representatives, quotient by the
real class sizes). Codex's counter-example to "one partner": three prisms X_1, X_2, X_3 of one pencil, an apex theta,
a vertex b among the 60 whose neighbours v_1, v_2, v_3 in the three prisms avoid the column of theta;
psi_i = 1_(X_i - v_i) + 1_theta - 1_b - 1_(v_j) - 1_(v_k): W has 8 edges, Y is a path, no cross edge, Q = 8, both
supports prism-free, psi_i - psi_j = 1_(X_i) - 1_(X_j). So three prism-free representatives in one class, two partners
each (checked by Codex on a 22-vertex fixture, no claim of a global realisation). "At most two per class" is false in
pencils of three or more; the cost has to be computed (Codex is doing it).

### 17.45 Supports <= 9: every accounting falls short; no "rank 37 forces grids" either (15:00 UTC)

* **Status of 17.44.** "13 900 < 16 496, hence closed" is a floating diagnostic: to be a statement it needs an exact
  rational point of the LP (Codex's remark). It is not an exclusion of anything.
* **Codex, certified (its note 200 in preparation), supports <= 9, norm 8, mass six, both signs:**
  - prism-free collisions per pair of grids on a line: 6992 <= C_pf <= 18 244; per non-grid twin pair: 7034 <= C_pf
    <= 19 178;
  - TIES after the two grid filters |psi(G_i)|, |psi(G_j)| <= 4: at most 12 674 per pair of grids (14 426 for a
    non-grid pair, prism-free and equal sizes only); only the shapes (3,3), (4,4), (6,3) survive on the grid side;
  - its three-prism triples of 17.44 are single-grid copies (psi_i - 1_(G_i) has support 6), so they leave the pool;
    in a pencil of six there are four choices of triples, in four different classes, not a class of four.
  Against my break-even of at most 7447 (17.42, before removing the single-grid copies from the numerator): not
  reached. Hand estimate of the copies in (9,0): W = a bowtie of a grid plus a square or paw whose four vertices are
  attached to the bowtie (about 7700 per grid), or a grid minus a path plus a line attached to it (about 1550 per
  grid): about 1.16M per sign at rho = 126, roughly half of the prism-free (9,0) representatives. So the pool for
  supports <= 9 is of the order of the ceiling itself, before any tie.
* **What-if cap on the number of grids** (`lp_family.py` scenarios `m5s9k2x63r<X>`, `OUTPUT_lp_family_rho.txt`; Codex's
  collection, k = 2): break-even 13 900, 14 841, 16 902, 21 259, 25 201 for rho <= 126, 100, 60, 20, 0 (tau = 1403,
  1308, 1161, 924, 780 at the optimum). Even with no grid at all the break-even stays below the certified cap for
  non-grid twin pairs (31 976), so this accounting does not even give "rank 37 forces many grids".
* **Remark on tau_g <= 11 rho + 17** (not used above): the extremal mix of the moment bound (points with three lines
  in six grids, e = 15, 57 cherries, together with grid-free points) is not realisable: a line through a grid-free
  point has g = 0, a line through a three-hub point has g >= 3, so no line joins the two kinds, and every non-adjacent
  pair needs two common neighbours carrying lines of both kinds. With types of about 11.5 pairs of lines each
  ((6,6,3,3,2,2,2): 39 cherries; (6,4,4,4,4,1,1): 39) tau_g would be about 1250-1300 at rho = 126. That is 10 %, far
  from the factor needed; not pursued.

Conclusion for rank 37 at this hour. Supports <= 9: closed on the three accountings tried (pairs with k = 2 on
Codex's collection; prism-free with k = 1; pool with ties). Ceiling side: exhausted (17.43). Support 10: the raw
count is inflated by single-grid copies; the pool and its ties are not computed, and my estimates put pool/2 near
the ceiling. What would be new: an order-11 census (shapes (7,4), (10,1)), which is a real computation and is not
launched; or an invariant other than b_4.

Addendum (Codex, about 15:02 UTC, answer to the laptop session's question of 17.43). The mass-8 tie of two grids meeting in
one point p is already in the component C14 of its note 183, section 4: G minus p is the 8-vertex 14-edge type, the
four transversal edges pair the vertices of degree 4; at most 64 collisions of shape (4,4) per pair of such supports,
and at most (608/3) C14 + 160 tau for the whole component (which contains more than the supports extendable to a
grid). It belongs to L44 of its note 185, NOT to C6 of notes 195-198 nor to the new prism-free / pool bounds: neither
forget it when adding C6, nor count it twice if L44 is used. The prism-free internal (7,1) channel is identically zero
for a pair of grids (the two-sided candidates passing Q = 8 on two adjacent apices contain another prism in their
positive part).

### 17.46 The object behind the missing lemma: a line in six grids, written as a design on 60 points (hand, not audited)

Context: by 17.28 the statement that would change rank 37 most is "no line lies in 4 or 6 grids" (then
tau_g <= 3 * 231 = 693 and rho <= 115). With the corrected numbers of 17.44 this gives about the factor needed and no
margin (13 900 * 1403 / 693 = 28 100 against a certified cap of 27 818 for pencils of three, other channels unpaid), so
it is necessary-looking, not sufficient. This section only fixes the object, so that it can be attacked as such.

Let Theta = {t_1, t_2, t_3} lie in six grids G_k = Theta + X_k (k = 1..6), X_k a prism with rows R_k, R_k' and
columns i = 1, 2, 3 (column i is the line through t_i). Then:
* the 36 vertices of the X_k are exactly the neighbours of Theta; a vertex of X_k has no neighbour in X_j (j != k), so
  it has 10 neighbours among the 60 other vertices B;
* each b in B has exactly one neighbour v_k(b) in each X_k, hence a NAME x(b) in (Z_3 x Z_2)^6 (column and row of
  v_k(b)); mu(b, t_i) = 2 forces every column to be used exactly twice: the six grids are split into three duads,
  one per column;
* for fixed k the six sets N_B(v), v in X_k, partition B into blocks of 10; for k != j a block of k and a block of j
  meet in 1 point if they have the same column and in 2 points otherwise (mu = 2, t_i being a common neighbour in
  the first case);
* lambda(b, v_k(b)) = 1 gives a unique b'_k in B adjacent to b with the same name at k: six perfect matchings
  M_1..M_6 of B, pairwise disjoint; b and b'_k differ at every other coordinate; the seventh line of b lies inside
  B: B is partitioned into 20 triangles, whose three vertices differ at every coordinate; B is 8-regular (240 edges);
* for b and v in X_k, with u = v_k(b): the number of neighbours of b in B lying in the block of v is 1 if v = u,
  1 if v is adjacent to u in the prism (same row or same column), 2 otherwise;
* for b, b' in B: (number of coordinates where the names agree) + (number of common neighbours in B) = 1 if adjacent,
  2 if not. Counting: 360 non-adjacent pairs agree at two coordinates (one for each pair of prism vertices of
  different prisms and different columns) and have no common neighbour in B, 720 agree at one, 450 at none; the
  totals 1620 = 60 * 28 - 60 match, so first and second moments give no contradiction (as the equitable partition
  {3, 36, 60} with quotient eigenvalues 14, 3, -4 already said).
Conversely a system (names, graph on B) with these properties is a strongly regular graph (99,14,1,2) with a line in
six grids. So "no line in six grids" is the non-existence of this design: 60 names in (Z_3 x Z_2)^6 with prescribed
pairwise coordinate statistics, 20 triangles and six matchings. Nothing is known about it here; a blind solver run on
it is the kind of whole-graph sub-case that did not terminate for the laptop session, so none is launched.

Addendum to 17.46 (hand). The COLUMN part of the names has a canonical solution, so no contradiction can come from
the columns alone. A name gives a syntheme of the six grids (three duads) with a bijection of its duads to the three
columns: 15 * 6 = 90 labelled synthemes. The conditions on columns are: each (duad, column) in exactly 4 names; for k, j
in different duads and columns i != i', exactly 8 names. Fix a synthematic total T (five synthemes covering each duad
once): the 10 synthemes outside T cover each duad twice, and for k != j exactly 8 of them do not contain the duad
{k, j}. So "all 60 labelled synthemes outside a total" satisfies both conditions (2 synthemes * 2 labellings = 4;
8 synthemes * 1 labelling = 8). The stabiliser of T is S_5 acting on the six grids as PGL(2,5). Whether other column
solutions exist is not examined. What remains to be decided is the row part (a sign vector in Z_2^6 for each name:
the four names of a (duad, column) carry the four sign pairs once, the eight names of a (k -> i, j -> i') carry each
sign pair twice) together with the 20 triangles and the six matchings. Reminder: the graph has no automorphism in the
project's setting (cases C2, C3 closed), so a solution cannot keep the S_5 symmetry of the columns.

Codex's note 200 (commit a5ee693 of its branch) contains the exact certificates of the bounds quoted in 17.45
(prism-free collisions, ties under the grid filters, the certified triple and its shorter representative; 1440 signed
triples per pencil of six, all removed by the grid filter). No rank excluded.

Addendum to 17.46 (laptop session, exact computation `pencil_det.py` on its side, sympy; its message of about 15:15
UTC; not recomputed here). New fact used: the rank enters the object through a determinant. For U = Theta with its g
prisms the Gram matrix E_UU of the projections is known, so the lattice L_far of integer (-4)-eigenvectors vanishing
on U has rank 44 - rank(E_UU) and determinant det(L) det(Pi) / t^2 (det(L) = 9 * 7^(r-1), Pi the span of the projected
e_x, t >= 1 an index). Exact values: g = 2: rank 31 on 84 vertices; g = 4: rank 21 on 72 vertices; g = 6: rank 13 on
the 60 vertices of B, det(L_far) t^2 = 324 * 5^12 * 7^(r-32) (rank E_UU = 31 for g = 6: two extra 3-eigenvectors appear
only for the full pencil). Hermite with min >= 14: the forced vector on the far set has norm at most 28, 30, 38 for
g = 2, 4, 6 at rank 37: no contradiction (it would contradict a line in six grids only for r <= 31, ranks already
excluded). NEGATIVE; do not recompute.

### 17.47 Open exploration asked by the user: literature after 25/09, and the Petersen graph behind a line in six grids

User (direct, about 15:20 UTC): go and look elsewhere (web, other objects), without duplicating conway99-c1 or
conway99-lab-archive. Duplication check done first: Codex's notes 94 (literature night), 110, 114, 124 read; Codex
checked the archive (its message of about 15:35 UTC): Bamberg-De Clerck-Durante (intriguing sets of partial
quadrangles) is already audited there and credited for L5, and |grid cap 22-coclique| = 2 is the standard
positive/negative intersection, so nothing new from that theorem; the synthematic totals of S_6 appear only in note
103 section 8, for the Hamming point, not for the object below.

**Web, what it adds.**
* A. Keramatipour, "Approaching the Conway-99 problem using SAT solvers", arXiv:2604.23037 (April 2026), read in the
  HTML version (first 100 000 characters). "Paley(9) pattern" = every pair of lines at every vertex spans a 3 x 3
  grid; its Theorem 3.4.2 (no 99-graph follows the pattern) is Makhnev's 1988 theorem (L1) again. Theorem 3.4.3: a
  99-graph cannot contain eleven independent (disjoint) Paley(9) subgraphs, PROOF OMITTED in the paper: not usable as
  stated. Conjecture 3.4.4: no 3 x 3 grid at all. SAT experiments: reported as not concluding. Nothing for rank 37.
* Thakkar-Severini, arXiv:2608.11211: a rooted CP-SAT reduction and a statement on circulants only. Nothing.
So the literature still has no fact on grids beyond Makhnev's theorem; status of each item above: read, not audited.

**A structural identification (mine; checked by `pencil6_petersen.py`, `OUTPUT_pencil6_petersen.txt`).**
In 17.46 the column part of a name is a syntheme of the six grids with a bijection of its three duads to the three
columns. Take the canonical column solution (the 10 synthemes outside a synthematic total, all six labellings each).
Then: the graph on these 10 synthemes "sharing a duad" is the PETERSEN graph; the 15 duads are its 15 edges; each of
the six grids is one of its six perfect matchings (the five duads containing that grid); a syntheme is a vertex with
its three edges. So the 60 far vertices are the 60 ORDERED STARS of the Petersen graph (a vertex p and a bijection of
its three edges to the three points of Theta), the column of b at the grid k being the label of the edge of the
matching F_k at p. Column agreements between two distinct names, by Petersen distance of their vertices: distance 0:
0 (2 names, the rotations) or 2 (3 names); distance 1: 1 (12 names) or 4 (6 names); distance 2: 0 (6), 2 (18), 3 (12).
* Other column solutions exist: at the level of synthemes, W = 4 + (5-dimensional kernel spanned by "-4 on a total, +2
  outside"), i.e. W(T_i cap T_j) = 4 - x_i - x_j with sum x = 0; the canonical one is x = (5, -1, ..., -1), the uniform
  one x = 0. Not classified.
* The obvious symmetric graph on the 60 ordered stars (rotations at a vertex, and along a Petersen edge with the same
  label on that edge) is 8-regular with 240 edges and 20 triangles but violates "exactly two neighbours in the same
  column" in all 360 (name, grid) cases. So the graph on B is not that one.
* Exact search, column-level necessary conditions only (`pencil6_cols_sat.py`: 8-regular; 2 / 3 / 3 neighbours by
  column for every (name, grid); common neighbours between 2 - h - (column agreements) and 2 - h): CP-SAT, 4 threads,
  240 s: UNKNOWN (353 conflicts). Not pursued blindly; the model is heavy (102 660 products) and the column structure
  is one of several.
What this is: a concrete finite description (Petersen, ordered stars) of the only configuration whose exclusion would
give the missing factor; what it is not: a result. Open on it: the rows (signs), the six matchings M_k, the triangles.

### 17.48 A constraint of a new kind (laptop session): the classes of grids live in 56 - r dimensions mod 7

**Statement (laptop session, about 15:40 UTC; argument checked here).** K+ = Z^99 cap (E_3 + <1>) is the orthogonal
complement of L = Z^99 cap E_{-4} in the unimodular Z^99, so disc(K+) = disc(L), whose 7-part is elementary of rank
r - 1; K+ has rank 55, so K+/7K+ modulo the radical of the form has dimension 56 - r. Hence the Gram matrix of ANY
family of kernel vectors (grid indicators, twin differences, ...) has rank at most 56 - r modulo 7: **19 at rank 37**,
17, 15, 13 at ranks 39, 41, 43. For grids the Gram matrix is the intersection matrix (9, 3, 1, 0 for equal, common
line, common point, disjoint). It is the kernel-side twin of "rank <= 45 - r for families of L" (17.40), and the
mechanism of Codex's note 103 section 4 (Hamming point, k <= 26) in general form. It is not a count and not linear
in the census.
Remarks (mine, hand). (A + 4I) e_v = 4 e_v + 1_N(v) lies in K+ and pairs to 8 or 1, i.e. 1 mod 7, with every grid: all of
Im(A + 4I) is a multiple of the class [1] modulo the radical. For a line in six grids,
sum_k 1_(G_k) = (A + 4I) 1_Theta, so sum_k [1_(G_k)] = 5 [1]: with g' = [1_G] - 2 [1] (orthogonal to [1], norm -2,
products -1, -3, -4 for common line, common point, disjoint) the six classes of a pencil of six sum to zero in the
18-dimensional space [1]^perp. The same computation for any grid G and any hub line only gives back the tight-set
property (a grid disjoint from a line meets its far set in 6 points), so the information is in the dimension count.

**Table on the canonical column solution of 17.47** (laptop session, `pencil_rank.py` on its side; RE-COMPUTED
INDEPENDENTLY here: `pencil6_rank7.py`, `OUTPUT_pencil6_rank7.txt`, `OUTPUT_pencil6_rank7_hubs.txt`). Grids: the six
pencil grids P_k and A(r, d) = the grid through theta_r on the columns of the two grids of the duad d, when it exists;
H_r = set of such duads at theta_r. Intersections: A with P_k: 3 if k in d, else 1; A(r,d), A(r,d'): 3 if the duads
meet, else 1; A(r,d), A(r',d') for r != r': 1 if d, d' are disjoint and the syntheme {d, d', rest} is outside the
total, else 0. Number of grids and rank mod 7 (range over random positions):

| H at each of 1 / 2 / 3 points of Theta | grids | rank mod 7 |
|---|---|---|
| nothing (pencil alone) | 6 | 6 |
| perfect matching | 9 / 12 / 15 | 9 / 12 / 12-15 |
| hexagon (every column in 3 grids) | 12 / 18 / 24 | 12 / 15-18 / 20-24: three points impossible at rank 37 |
| K_3,3 (every column in 4 grids) | 15 / 24 / 33 | 15 / 24 / 33: two points impossible |
| two triangles | 12 / 18 / 24 | 11 / 12-16 / 17-21 |
| star (one more line in six grids) | 11 / 16 / 21 | 10 / 10-12 / 18 |
| double star (the point has three lines in six grids) | 15 / 24 / 33 | 13 / 18-20 / 24-27: three points impossible |
| triple star (four lines in six grids) | 18 / 30 / 42 | 15 / 24 / 33: two points impossible |
| K_6 | 21 / 36 / 51 | 15 / 24 / 33: two points impossible |

My two computations agree with the laptop session's values (its ranges are inside mine). Reading: around a line in
six grids the classes of grids are nearly independent mod 7; a hub line whose three points are all "three-hub"
points (the extremal type of tau_g <= 11 rho + 17) is impossible at rank 37, and with two such points at most one
dimension is left for all the other grids of the graph. The laptop session's greedy search finds at most about 21
further grids around the pencil at rank 37.
NOT PROVED: (1) only the canonical column solution (others exist, 17.47); (2) only grids through the three points
of Theta; (3) no general lower bound of the rank in terms of rho or tau_g; (4) lines in four grids; (5) twin
differences of non-grid prisms (norm 12), which the accounting also needs: by 17.45 a cap on rho alone does not
conclude (break-even 25 201 at rho = 0 against 31 976), the total number of twin pairs has to go below about 540.
If a general lemma gives rho of a few dozen and tau of a few hundred at rank 37, the accounting of 17.44 concludes.

Addendum to 17.48 (Codex, about 15:50 UTC, exact computation, certificate in preparation on its side; not recomputed
here). The bound is confirmed. Twin differences inside one pencil are G_i - G_j and add no rank. With UNKNOWN binary
cross intersections (not only the canonical columns): for H^i_ab = the possible grid at t_i between the rungs of the
prisms a, b, two such grids at different apices are disjoint when their pairs meet, and meet in 0 or 1 point when the
pairs are disjoint. If the rung of prism 0 is universal at the three apices, the 21 grids have rank 18 mod 7 (excluded
at ranks 39, 41, 43). Adding at one apex a second universal rung keeps 12 completions of rank <= 19; adding then a
single grid H^1_12 gives rank 20 or 21 in all 108 extensions. Hence, at rank 37: NO configuration "three apices with
three hubs each, one same prism giving an extra hub at all three apices". The pencil of six itself is not excluded.
Targets sent to Codex: excluding six-grid lines only leaves tau_g <= 1134, not enough; what pays is a bound on rho
(tau_g <= 11 rho + 17: rho <= 60 gives 677) and on non-grid twin pairs. Negative (mine): the modular polynomial
method on the centred classes (norm -2, products -1, -3, -4, dimension 18) only gives rho <= C(21,3) = 1330.

Second addendum to 17.48 (Codex's note 202, commit 8fabef6 of its branch; then my exhaustive table on the canonical
model, `OUTPUT_pencil6_rank7_types.txt`).
Codex, GENERAL certificate (no restriction to the Petersen names; 433 non-zero minors of order 20 mod 7 covering the
59 049 binary choices): if the rung of prism 0 is universal at the three apices and the rung of prism 1 universal at
the first, then the rungs of prism 1 at the two other apices lie in exactly two grids. So three apices with three
hubs each sharing a common extra index are excluded at r >= 37. Open in its note: three apices with two extra hubs
each and NO common index (five types of the three pairs).
Canonical model, exhaustive over all positions (hub rungs {a_r, b_r} at apex r, H_r = the 9 duads meeting them):

| extra hub rungs at the three apices | grids | rank mod 7 (all positions) |
|---|---|---|
| 2, 2, 2: common index | 33 | 27 |
| 2, 2, 2: triangle; P3 + K2 | 33 | 27 |
| 2, 2, 2: path P4 | 33 | 25, 26, 27 |
| 2, 2, 2: two identical pairs and a disjoint one | 33 | 25, 27 |
| 2, 2, 2: three disjoint pairs | 33 | 24, 25 |
| 2, 2, 1 (all positions) | 29 | 23, 24 |
| 2, 2, 0 | 24 | 18, 19, 20 |
| 1, 1, 1 | 21 | 18 |

Reading: in the canonical model a line in six grids has at most two three-hub points, and then no extra hub at the
third point; (2,2,0) and (1,1,1) fit in 19 dimensions, so these two patterns CANNOT be excluded by the grids through
the three apices alone (the canonical model is a valid choice of the binary intersections): they need the grids
elsewhere or the non-canonical structure. The five open types of note 202 all have rank 24 to 27 here.

Third addendum to 17.48 (Codex, about 16:00 UTC, exact computation, its note 203 in preparation; not recomputed here).
GENERAL result, no canonical hypothesis: the pattern (2,2,1) of extra hub rungs at the three apices of a line in six
grids is excluded for r >= 37 (the 90 column words with integer multiplicities w; margins 4 and 8; tightness sums 2
for complete duads; w <= 1 when two duads of a word are complete; 7 orbits covering the 1350 placements; 47 integer
column solutions in all, every Gram of rank 23 or 24). Hence (2,2,2) falls for the five remaining types: **on a line
in six grids, if two points have three hub lines each, the third has only one (the line itself).** With n_h = number
of vertices on exactly h lines contained in six grids (h <= 3 because four hubs need 18 grids at a point):
3 n_3 <= 2 n_1 + n_2, so n_3 <= 39. No rank excluded.
What the cut is worth in a moment LP (`profile_lp.py`, `OUTPUT_profile_lp.txt`, floating): with MY list of point
types (586 graphs on the 7 lines: degrees in {0,1,2,3,4,6}, at most 17 edges, D1) the maximum of tau_g is 12.18 rho
without the cut (1534 at rho = 126, the old bound of note 194) and 11.49 rho with it (1448): still above Codex's
11 rho + 17 = 1403, which uses a shorter list of types. So the cut has to be evaluated in Codex's own moment LP; with
my list it brings nothing new. Extremal types with the cut: 16 pairs / 60 cherries / 2 hubs, K_7 minus a 4-cycle
(17 pairs, 69 cherries, 3 hubs), and grid-free points. Expected size of the gain: small; the accounting needs
tau of about 540 to 700, which this cut alone cannot give. The lever is the dimension count itself (how many grids
fit in 19 dimensions), not this consequence.

### 17.49 The one missing statement, with its number (16:10 UTC)

User (relayed by the laptop session as his direct words to it, about 16:00 UTC): find what is missing; getting
through rank 37 is a necessity now. Agreed split: Codex certifies the analysis around a line in six grids, then in
four, with unknown cross intersections; the laptop session takes the twin differences of non-grid prisms and the
September case "every line disconnected"; I give the exact break-even for every bound that gets certified.

**Target.** On Codex's collection (supports <= 9, (6,3) without prism 6-sets), quotient k = 2, joint LP with the Fano
coupling and the secants (`lp_family.py`, scenario m5s9k2x63 at c = 0): the maximum over the whole polytope of
(ceiling - 2 R / 3) is -5.703 million (floating). Since the floor is (2R - C)/3, rank 37 is excluded as soon as the
total number C of colliding pairs satisfies C < 17.1 million. With Codex's certified caps per pair (27 828 for a pair
of grids on a line, 31 976 for a non-grid twin pair), a SUFFICIENT condition is

      27 828 tau_g + 31 976 tau_n + (channels not in C6) < 17.1 million,

tau_g = pairs of grids on a common line, tau_n = non-grid twin pairs. Examples: tau_g < 614 with no non-grid pair;
tau_n < 535 with no grid; tau_g <= 347 (i.e. rho <= 30 with tau_g <= 11 rho + 17) leaves room for tau_n <= 232.
Channels not in C6 and still to be charged inside the 17.1 million: the single-grid relation (a number per grid,
times rho: small if rho is a few dozen), the masses 7 to 9 and the component C14/L44 of Codex's notes 183-185.
To be certified exactly by Codex if the bounds on tau_g and tau_n come; the constant 17.1 million is the only thing
my LP contributes, and it does not depend on where the bounds on tau come from.

**The statement that is missing** (laptop session's formulation, which I adopt): at rank 37 the classes of all grid
indicators and twin differences live in dimension 18 over F_7 (19 with [1]); needed: a lower bound of the rank of
such a system in terms of the number of twin pairs that forces 27 828 tau_g + 31 976 tau_n below 17.1 million.
Done so far towards it: Codex's general certificates (notes 202, 203: on a line in six grids, two three-hub points
force the third to have one hub; n_3 <= 39); the canonical tables of 17.48. Hand facts from the laptop session
(16:05 UTC, not rechecked here): a dependency mod 7 among kernel vectors is an integer combination with coefficients
in {-3..3} lying in L_3 cap 7 L_3*, whose shortest vectors found have norm 42, so every kernel vector of norm < 42 has
a non-zero class; a twin class of size m spans a non-degenerate subspace of dimension m - 1; a line whose cubic
graph has c components contributes c - 1 dimensions by itself; the smallest degenerate triple of grids is "G_1 shares
a line with G_2 and with G_3, G_2 and G_3 disjoint"; in general (W^T W)^2 = - W^T D W mod 7 with W the point-grid
incidence and D >= 0 the matrix of missing grids. Link with September (Codex's note 127): rank 37 is k = 22, where a
generic line has a complete construction and the plan ended on "every line disconnected": 231 lines against 18
dimensions is the same statement from the other side.

Addendum to 17.49: the cut of note 203 in Codex's own moment LP (`profile_lp2.py`, `OUTPUT_profile_lp2.txt`, floating).
Codex exported its profiles (177 refined profiles (e, c, h2, u6)) and the model of its note 196: for each s = 0..73
(number of vertices with e >= 14), variables by profile and by number d of neighbours in that set, with the moment
equalities sum d = 14 s, sum (d^2 + [e>=14] d) = 12 s + 2 s^2 and sum_inside d <= 3 s + s^2/9. Re-implemented here:
without the cut the maximum of the twin bound is 1403.46 (s = 56, rho = 126, P = 756): Codex's 1403 is REPRODUCED.
With the cut 3 n_3 <= 2 n_1 + n_2 (n indexed by the number u6 of lines in six grids): **1354.89** (s = 22, rho = 126);
tau_g as a function of rho: 1354.9 / 1165.2 at rho = 126 / 110, unchanged for rho <= 90 (944.1, 726.1, 515.3, 308.4,
101.5 at rho = 90, 70, 50, 30, 10).
Against the target of 17.49 (tau_g < 614 with no non-grid pair): the cut gives 3.5 %, the target needs a factor
2.2. Useful by-product: for rho <= 30 the moment LP already gives tau_g <= 308, so a bound rho <= 30 would leave room
for 266 non-grid twin pairs.

### 17.50 The missing statement, quantified: at most 10 relations beyond the pencil ones (16:25 UTC)

**Where the classes live (laptop session's 2(a), re-derived here).** Mod 7, A + 4I = A - 3I =: N, of rank r. Im(A + 4I)
lies in K+, and K+/7K+ modulo the column space of N has dimension 55 - r = 18; [1] is in that column space
(N 1 = 11 * 1), and the centred classes g' = [1_G] - 2 [1] live in this 18-dimensional quotient. So
* a relation mod 7 among grid classes is exactly a combination of grid indicators lying in the column space of
  A - 3I mod 7, i.e. orthogonal to every mod-7 solution of A x = 3 x;
* equivalently the class of a grid is the linear form "sum over G" on the 18-dimensional space
  ker_7(A - 3I) / (L mod 7) (3-eigenvectors mod 7 modulo reductions of (-4)-eigenvectors, on which every grid sums to 0);
* the 3-eigenvectors available in every graph, (A + 4I)(sum-zero vector), are in the column space of N: useless as
  witnesses. Only structure-specific kernel vectors (grids, twin differences, components) can certify independence,
  which is what Codex's Gram minors do. Also (laptop session, checked): in a non-degenerate space of dimension 19 a
  family of true dimension d has Gram rank at least 2d - 19 and at least d - 9.
* For every line T (hub or not) the classes of the components C of its cubic graph, 1_C + (|C|/6) 1_T, sum to
  (A + 4I) 1_T = 5 [1]: one relation per line, the pencil relation when all components are prisms.

**Conversion table** (`profile_lp3.py`, `OUTPUT_profile_lp3.txt`; Codex's moment LP with the cut of note 203, plus
rho <= 18 + c + x6 where x6 = number of lines in six grids and c = number of independent relations mod 7 among the
grid classes beyond the pencil relations; floating):

| c | max tau_g | 27 828 tau_g | max rho | all-grid verdict against 17.1M |
|---|---|---|---|---|
| 0 | 388 | 10.80M | 40 | excluded, 6.3M left (197 non-grid pairs) |
| 4 | 477 | 13.27M | 49 | excluded |
| 8 | 566 | 15.75M | 58 | excluded |
| 10 | 608 | 16.92M | 62 | excluded, no margin |
| 12 | 655 | 18.23M | 67 | not enough |
| 20 | 847 | 23.56M | 86 | not enough |
| no dimension constraint | 1354.9 | 37.70M | 126 | not enough |

With c = 0 at the other ranks (dimensions 16, 14, 12): tau_g <= 346, 299, 257 at ranks 39, 41, 43.
**So the missing lemma has a number: at rank 37, the classes of the grids satisfy at most 10 independent relations
mod 7 beyond the pencil relations** (fewer if non-grid twin pairs exist: each non-grid class of size m uses m - 1
further dimensions for at most 3 pairs). The laptop session's own count with a simpler LP gave 13 (h <= 3) or 4
(h <= 4); Codex's profiles have at most three lines in six grids at a point.
Nothing bounds c at present: relations are forced as soon as rho + 1 - x6 > 19, and what has to be certified is that
such forced relations cannot exist, cluster by cluster.

**Codex, note 204 (commit d581508 of its branch), exact certificates:** with the cut of note 203, tau <= 1354
(89423/66, s = 22; all 74 sizes certified); b_3 >= 45 964; C6 <= 38 084 490 (binary mass-six same-sum, was
39 016 712); at rank 37 with b_3 >= 45 964: b_4 <= 15 196 716 at rho = 126. No bound rho <= 50 is justified yet: it
does not count pencil subspaces as independent.

Addendum to 17.50: three reformulations by the laptop session (16:30 UTC; checked here), and a test on the canonical
model (`pencil6_hull.py`, `OUTPUT_pencil6_hull.txt`).
* HULL. C = the F_7-code spanned by the grid indicators and 1. Gram rank = dim C - dim Hull(C), Hull(C) = C cap C^perp
  = the combinations summing to 0 on every grid and over all vertices; the true relations are a subspace of the hull,
  the rest of the hull is the radical of the span (dimension at most 9). Sufficient for the lemma:
  (n - dim C) + dim Hull(C) <= x6 + 10 (n = rho + 1). For EVERY line T the function f_T = (A + 4I) 1_T + 2
  (1 on T, 3 on N(T) - T, 2 elsewhere) is in C^perp (checked: 21 + 7 |T cap G| on a grid, 252 in total); it is in C
  when T lies in six grids.
* CLASSES OF M. y -> (A + 4I) y; a relation is a class whose image is a grid combination mod 7; the pencil relations
  are the classes of the triangle vectors t_T of the hub lines. (Not rechecked in detail.)
* FILTER. (A + 4I)^2 = 7 (A + 4I) + 2J (checked), so (A + 4I) y = F implies |F|^2 = 7 (y, F) + 2 (sum y)^2 and
  sum F = 18 sum y. Also, for every line: (A + 4I)(1_(N(T) - T) - 1_T) = 6 * 1 exactly (mine).
* TEST (canonical six-pencil; all 99 vertices explicit; y supported on the ball of Theta and constant on every rung,
  so that (A + 4I) y does not depend on the unknown rows). For each pattern: generators n = grids + 1, dim C, Gram
  rank, dim Hull, and REL = dim({(A + 4I) y} cap C) - 1 (the -1 removes 6 * 1): the relations certified TRUE.
  - pencil alone, perfect matchings, hexagons, K_3,3 at 1, 2, 3 points: REL = 1 = the pencil relation of Theta, while
    the hull has dimension 1 to 4. So the Gram shortfalls of matchings and hexagons (1 to 3) are NOT relations of this
    kind: degeneracy of the form on the family, or relations whose y is not rung-constant on the ball.
  - star, double star, K_6: REL = x6 exactly (one relation per line in six grids of the pattern).
  - "two triangles" (at an apex, Theta and three columns pairwise in grids, twice): REL = x6 + 1 per apex: ONE extra
    true relation per such apex (2, 3, 4 in all for 1, 2, 3 apices). First example of a relation beyond the pencil
    ones; six grids through a point on four lines pairwise in grids are independent by themselves (Gram of rank 6,
    7 with [1]), so the relation involves the pencil of Theta.
  - K_6 at three points: the 52 indicator vectors have only rank 46 (six linear dependencies among the vectors
    themselves).

### 17.51 CORRECTION to 17.50: relations at ONE vertex exist in every graph; the count "c <= 10" was too optimistic

**The explicit relation asked by Codex** (`OUTPUT_two_triangles_relation.txt`, `two_triangles_relation.json`): in the
canonical model with the two-triangles pattern at theta_0, y = 2 e_(theta_0) + 1 on the four corners of P_0 - 1 on the
columns of theta_0 in the prisms 1 and 2 gives
(A + 4I) y = -(P_0 + P_1 + P_2) - (A_01 + A_12 + A_02) + (A_34 + A_45 + A_35) (mod 7), with [(A + 4I) y] = [1]; in
centred classes: (sum of the six grids on the four lines Theta, m_0, m_1, m_2) = (sum of the three grids on m_3, m_4,
m_5). The pencil of Theta is NOT needed (P_3, P_4, P_5 have coefficient 0).

**It is general** (hand proof, every vertex type checked: v, the points of the seven lines, the corners c(a,b) of
grid pairs and of non-grid pairs): **Lemma (4 + 3).** Let v be a vertex whose seven lines split into four lines pairwise
spanning grids and three lines pairwise spanning grids. With y = -e_v + (indicator of the eight other points of the
four lines), (A + 4I) y = (sum of the 6 grids of the four lines) - (sum of the 3 grids of the three lines) + 1 (mod 7).
Hence, in centred classes, sum over the six = sum over the three: one true relation among nine grids, in ANY
srg(99,14,1,2). (The split 4 + 3 is the hypothesis of the laptop session's Lemma N16.)

**All one-vertex relations** (`vertex_relations.py`, `OUTPUT_vertex_relations.txt`). For y supported on the closed
neighbourhood of v, (A + 4I) y is determined by y in every graph (y_a + y_b at the corner c(a,b)), so
"(A + 4I) y = sum a_G 1_G + k (mod 7) over the grids through v" is a linear system depending only on the grid graph Xi
of v: y constant on each line minus v (value y_l); y_l + y_l' = k on the pairs that do not span a grid; a_G = y_l + y_l'
- k on the grids; one equation per line and one at v. Its non-trivial solutions are true relations. Result over the
types of Codex's profiles (with D1): 500 graphs without relation; with a line in six grids, the pencil relation
(y = 1 on the line) for each such line; and 17 graphs (17 of the 177 profiles) with ONE relation more than their
number of hub lines: 4 + 3 (9 pairs, 15 cherries), and richer types up to K_7 minus a 4-cycle (17 pairs, 3 hubs); the
complement of Xi has a bipartite component there. Three-hub points (K_3 joined to four independent lines) have no
excess.

**Consequence for the count.** In 17.50 only the pencil relations were treated as available to the adversary. Adding
the one-vertex relations as if they were all independent (rho <= 18 + c' + x6 + number of vertices of an excess
type) in Codex's moment LP gives max tau_g = 1331 at c' = 0 (rho = 126, about 53 vertex relations and 55 hub lines):
**the dimension count with these two families of relations assumed independent does not bound tau_g at all.**
So the statement "at most 10 relations beyond the pencil ones" is FALSE as a target: the correct missing statement
is a bound on the number of INDEPENDENT relations of all kinds (pencil, one-vertex, others), i.e. certified ranks
of clusters, which is what Codex's minors do; a global count needs the dependencies between the relations of
neighbouring vertices and lines. What survives: every certified local exclusion (notes 202, 203, 205), the cut
3 n_3 <= 2 n_1 + n_2, tau <= 1354, and the conversion 17.1 million.

### 17.52 Retrospective asked by the user: why bound at all? Rank 37 is an EQUALITY case (16:55 UTC)

User (direct): "vous etes en quete de borner quelque chose depuis ce matin, donc reflechissez bien a pourquoi vous
cherchez a borner, peut etre que la solution se cache dans l'evidence, ou bien peut etre y a-t-il d'autres moyens
que borner".

Why we bound: the day was framed as a COUNT (norm-8 vectors of M against the theta ceiling); a count needs a bound
on duplicates, hence on twin pairs, hence on grids, hence on relations mod 7. Each step replaced one quantity to
bound by another.

What was in front of us (Codex's September notes 124, 126, 127, read today; statuses as written there, not
re-audited here): for a line L with cubic graph G(L), d(L) = dim ker_7 of its Laplacian, the exact identity
      14 + k = (37 - d) + 2 r(L) + rho,  rho >= 0,   k = rank_7(A - 3I) - 15,
i.e. rank_7(A - 3I) = 37 + rank_7(R_L) for a generic line (d = 1), R_L the 60 x 60 Schur residue on the far vertices.
So **rank 37 (k = 22) is the smallest rank a generic line allows: it is the equality case R_L = 0.** In an equality
case nothing has to be bounded: the adjacency among the 60 far vertices is GIVEN mod 7 by the shadows
(A_ww' = 3 - g(N_w, N_w'), "construction complete"), and note 127 records that this forced construction failed in
all 42 tested cases ("etoile complete morte 42/42"). The September chain for k = 22 was:
  (a') uniform: the complete star is impossible for every generic ball at k = 22 (algebraic, open);
  (NT): a 7-torsion of a connected G(L) is never balanced (open, heuristic);
  then every line is disconnected, "to be excluded locally" (open).
Codex's warning stands: "k = 22 => every line disconnected" is conditional on (a') uniform and NT.

How today's work fits, without any bound: a disconnected line carries component vectors 1_C + m 1_T in the kernel
lattice, and at rank 37 all such classes live in 18 dimensions mod 7 (17.48), with an exact determinant character
(Codex's note 205). "Every line disconnected" means 231 lines each contributing at least one class: the question is
no longer "how many grids" but "can 231 disconnected lines coexist in 18 dimensions", which is an exact rank
statement of the kind Codex certifies (notes 202, 203, 205), and the 4 + 3 lemma of 17.51 is one of the exact
relations that such a certificate has to account for.
So the non-bounding route is: (1) rigidity of the generic line at rank 37 (finish (a')), (2) NT, (3) exclusion of
"all lines degenerate" by exact ranks mod 7. The collision count is then not needed at all.
Sent to Codex and to the laptop session as a proposal, with the question of what (a') still needs.

Addendum to 17.51 (Codex's note 206, commit bb36c21 of its branch; exact, not recomputed here). The 4 + 3 lemma is an
exact INTEGER identity, and the one-vertex relations are classified symbolically: with X the grid graph of v, H its
complement, and z a function on the seven lines with z_i + z_j = 0 on every edge of H, put y_v = sum z and y = z_i on
the two other points of line i; then exactly (A + 4I) y = sum over the grids G_ij of (z_i + z_j) 1_(G_ij). The relations
with a witness supported on N[v] have dimension exactly b(H), the number of bipartite components of H (isolated
vertices = lines in six grids included). The 17 excess types are confirmed with a short reason (no vertex of H has
degree 1, so a non-trivial bipartite component has at least 4 vertices, at most one on 7 vertices). Gram formula for
the centred grids at a vertex: Gamma = 4I + 2 C^T C - 3J mod 7 (C the 7 x e incidence matrix), rank Gamma = e -
nullity_7(Q_H), Q_H the signless Laplacian of H; bipartite components give the rational null space, any extra
nullity mod 7 is 7-torsion and need not be a true relation with a witness on the ball.
Consequence certified at rank 43 only: every vertex has e <= 15, tau <= 1326, b_3 >= 46 000 there. Nothing new at
rank 37.

Addendum to 17.52 (17:15 UTC): Codex's answer, and the September source located.
* Codex agrees to prioritise the exact equality obstruction. Its formulation: generic = d(T) = nullity_7(3I - G_T) = 1;
  at r = 37, A_F = 3I + 3J - N^T L^+ N mod 7 exactly (diagonal g = 6, off-diagonal g in {2,3}); uniform target: no
  admissible generic ball with 60 shadows meets this and the exact SRG equations; (a') and NT are separate missing
  lemmas, the genus signs do not give NT; for "every line disconnected" the centred component vectors of one line
  have Gram 6 (Diag(m) + m m^T), rank c - 1, and the cross intersections between lines are needed; finite target
  proposed: a central line and its 18 side lines (19 centred directions against 18 in the P = 0 two-component case).
* The source of "etoile complete morte 42/42" is NOT in conway99-c1 but in amazing-source/conway99-structures-lab:
  NOTE_S24_ASTRA_DOSSIER5.md, NOTE_S26_ASTRA_ETOILES.md, astra/RAPPORT_ASTRA_DOSSIER5(_SUITE).md,
  astra/SUIVI3/4_DOSSIER5.md, scripts/star_shadows.py, star_ablation*.py, random_balls_star_calibration.py and logs.
  As written there (not re-audited): 42 = 35 random admissible generic balls with tau non-square (of 92 tried) + the
  original ball + 6 cyclic triples, each killed by a search of about 10^4 nodes on the complete star of a ball
  vertex (10 far neighbours: 4K_2 + 2K_1); still dead with the Green conditions only; all 96 tested sub-stars of size
  6 feasible; the imposed Gram has rank 10 and non-zero determinant mod 7 (the obstruction is in the 0/1 form of the
  shadows); heuristic expected number of solutions about 10^-15. Proved there: R = 0 implies the exact SRG
  equations; MR = 0 is automatic. Missing: a UNIFORM reason why the complete star fails.

Second addendum to 17.52 (17:25 UTC), the equality route, state of the pieces (statuses as given by their authors).
* Codex (17:15): astra/RAPPORT_ASTRA_SUIVI4_ET_AUDIT_S5.md (structures-lab), message 1: on the cyclic ball (2,4,1) an
  explicit witness of ten shadows passes the two apexes, the ten norms, the integer sum K e_u, lambda/mu and
  M_star M_star^T <= K, and fails only on 19 non-apex pairs. No contradiction from apexes + sum alone; the eight
  paired shadows are needed together. Audit: star_substars.py with full=True on subsets is not a valid search for
  UNSAT cores (use full=False); "only_green" keeps G-dependent capacities. My suggestion to tabulate minimal dying
  sub-stars from the existing logs is void; the valid version is not launched (Codex rebuilds the witness itself).
* Laptop session (17:17, hand, scripts on its side): (1) exact Gram over Z of the component vectors at one vertex
  (same line: [b = b'] 6m + 3 m m'; different lines: 2 |b cap b'| + 4 [j in b][i in b'] + 2 m' [j in b] + 2 m [i in b'] +
  m m'); centred rank at one vertex 4 to 14 over 30 000 random systems: one vertex never contradicts rank 37; the
  cross-apex entries of Codex's "central line + 18 side lines" are not determined by the blocks. (2) For a connected
  line, identities over Z: tau = (9/4) 7^(37-r) t^2 det(L_far), det(4I + A_G) = (256/5) 7^(38-r) t'^2 det(K(F)),
  iota = 2 * 7^(37-r+g) t t'; at r = 37, d = 1: ker_Z N = L_far (+) K(F) orthogonally without glue. Filter: no two
  disjoint families of at most five far vertices with equal shadow sums (6 + 6 only twin prisms). The September star
  search used only conditions mod 7 and combinatorics (NOTE_S24 par.1), so this filter is additional. (3) Negatives:
  pairwise positivity of 7 Pi around a six-grid line forces nothing; (A + 4I)(e_u - e_v) is a grid combination only
  with at least 30 A-grids in the canonical model.

Third addendum to 17.52 (17:30 UTC). Codex rebuilt the apex witness independently (19 non-apex pairs forbidden); the
laptop session's small-exchange filter is automatic inside one star (ten distinct pivots), useful only for coupled
stars; Codex proved the rank-14 ceiling at one vertex uniformly (kappa(i,B) = sum over j in B of the 21 formal
vectors g_ij, Gram 4I + 2C^T C - 3J of rank 14). Flags of the September searches (my reading of the structures-lab
scripts, nothing run): the seven-group exclusion of Astra's ball (verify_astra_d5_seven_shadows.py) uses the
capacities as inequalities only, so it is a valid 7-group core; the complete stars of the 6 cyclic and 35 random
balls use full=True on all 10 groups (valid); only star_substars.py (full=True on subsets) is invalid. Proposed to
Codex, not launched: star_test(full=False) on 10 and 9 groups for one random ball. The laptop session is no longer
reachable from this session (17:30 UTC); its last messages are recorded above.

Fourth addendum to 17.52 (Codex's note 207, commit 241acc8 of its branch). The three seven-group cores (Astra's ball,
cyclic (2,4,1), cyclic (2,4,3)) re-run with full=False (inequality capacities): all UNSAT (27 626, 39 574, 41 826
nodes): valid cores. The local ceiling 14 is a theorem with structure: the 21 formal vectors g_ij modulo the 7
relations C^T z span a HYPERBOLIC space of dimension 14 (C C^T = 5I + J, determinant 5 non-square mod 7), which embeds
isometrically into the centred ambient spaces at ranks 37, 39, 41 (dimensions 18, 16, 14, all hyperbolic). So
component Grams around ONE vertex can exclude none of these ranks. Finer count (note 208 in preparation): with F_v the
graph of component blocks at v, the true local classes have dimension at most n - b(F_v) - 7 <= 14. Consequence: the
equality route at rank 37 must use couplings between vertices or between stars, not single-vertex Grams.

Fifth addendum to 17.52. Codex's note 208 (commit 1cda5e1 of its branch, verified exactly: 441 blocks, 97 461
products): h = n - b(F_v) - 7 bounds the TRUE local classes of component vectors at a vertex (seven integer relations
(A + 4I) y before centring). Codex declined my calibration of 7-group cores on the 35 random balls: the groups v are
fixed by the pairs {u, v} of layer A but the apexes and the 4K_2 matching depend on the chosen shadows, so there is
no canonical "same pattern"; and a surviving 7-tuple would not show that the minimal core is the whole star.
Not launched. Priority: constraints between several vertices / stars, using note 208 for blocks sharing a vertex.

### 17.53 Breaking the wait: the residual case "(6,6) everywhere" as a local-to-global question (17:50 UTC)

User (direct): Codex and I were both waiting for the other. Split sent to Codex (message 235): Codex keeps the generic
side (couplings of stars, (a')); I take the degenerate residual case left open by Codex's note 126 par.3 ter: at
P = S = 0 (no prism; S = number of S events, so every cubic graph G(L) has girth >= 5, note 125) and k = 22, under
(i) NT for connected lines and (ii) the uniform star, the 231 lines all have profile (6,6) (two components, three
lines per point each); "il resterait a exclure (6,6) partout". Status of that reduction: conditional, as written there.

**First fact (hand, with Codex's note 208; to be checked by Codex).**
* Each (6,6) line T gives ONE centred class h_T, that of 1_(C_1) - 1_(C_2) (a 3-eigenvector, norm 36 = 1 mod 7, so
  non-zero and anisotropic). Rank 37: 231 non-zero vectors in the 18-dimensional centred space, hence at least
  231 - 18 = 213 independent linear relations mod 7 among them.
* At a vertex v all seven lines have two blocks of size 3; Codex's graph F_v (one vertex per block, one edge per pair
  {i, j} joining the block of L_i containing L_j to the block of L_j containing L_i) is a SIMPLE CUBIC graph on 14
  vertices. A simple cubic bipartite graph has at least 6 vertices, so b(F_v) <= 2, and the relations among the
  seven h_T at v with a witness supported on the closed neighbourhood of v number at most 2.
* Hence at most 198 relations are vertex-local, and **at least 15 independent relations among the line vectors must
  have non-local witnesses**. "(6,6) everywhere" at rank 37 falls as soon as the relations among the h_T are generated
  by the vertex-local ones up to at most 14 more: a local-to-global (sheaf-type) statement on the geometry of 99
  points and 231 lines, not a bound on a count. Not proved.
Next on my side: the centred Gram entries for meeting lines (note 208 formula with m = m' = 3); a description of the
witnesses y of a relation sum c_T h_T = [(A + 4I) y] by their support (can they be cut into closed-neighbourhood
pieces?); what notes 125, 126 and the scripts x30c, x32 already know about (6,6) components of girth >= 5
(288 labelled components, 15 types, one is the Pappus graph).

Addendum to 17.53 (18:05 UTC).
* Codex (checked here by hand): the reduction of note 126 par.3 ter is correct under (i) NT for connected lines and
  (ii) the uniform generic obstruction, both open; S = number of L18 events, sum_L c4(G(L)) = S + 3P. Correction of my
  numbers: the class of 1_(C_1) - 1_(C_2) has norm 36 = 1 mod 7 (the half-class has norm 2); and **b(F_v) <= 1**: a
  K_3,3 component of F_v uses six distinct lines a_1, a_2, a_3 | b_1, b_2, b_3, each a-line's block in it is
  {b_1, b_2, b_3} and conversely, so the complementary blocks of the a-lines (and of the b-lines) form a triangle in
  F_v; the rest is not bipartite. Hence at most 99 vertex-local relations, and at least 114 relations among the 231
  line vectors must be non-local.
* HONEST READING (mine): this is not a separate lemma. In any graph of the residual case the 231 line vectors lie in 18
  dimensions, so the relations are FORCED; "the relations are generated locally up to 14" is equivalent to "the line
  vectors span at least 118 dimensions", i.e. to the non-existence itself. A proof needs a rank lower bound, which
  needs the Gram entries of DISJOINT lines (unknown): the same nature as the grid case. Recorded so that nobody
  presents it as a reduction.
* Two census tests of the P = S = 0 world (`lp_ps0.py`, `lp_comp66_cycles.py`, outputs; floating, NEGATIVE):
  (1) the order-10 census polytope allows P = 0 together with no Z2 (the 7-vertex configuration of an S event; it is a
  single census parameter, range 0 to 7469); (2) G(L) = Gamma[N(L)], so F_k = sum over lines of the number of k-cycles
  of G(L) is a census form (2 types of order 8 for k = 5, 10 of order 9 for k = 6). The 15 (6,6) component types of
  girth >= 5 have (c5, c6) in {(0,18), (2,12), (4,8), (4,10), (6,4), (6,6), (9,0)}, so "(6,6) everywhere" needs
  F5 in [0, 4158], F6 in [0, 8316] and 2 F5 + F6 in [7392, 8316]; at P = S = 0 the census allows F5 in [0, 4158],
  F6 in [0, 8316], 2 F5 + F6 in [0, 11 781]. No contradiction.

Second addendum to 17.53 (18:20 UTC): the far side of a (6,6) line, exact tests (`comp66_triples.py`,
`comp66_joint.py`, outputs). New fact used: equilibrium (every far vertex meets each component in 3 points) and the
exact pair multiplicities K (far common neighbours) inside a component and across components (1 same layer, 2 else),
plus "a 3-set of N(L) lies in at most one shadow" (mu = 2).
* ONE component: for all 288 labelled (6,6) components of girth >= 5 (all 15 types), a set of 60 distinct admissible
  triples (630 candidates) with exactly the pair multiplicities K exists (CP-SAT, under a second each; row sums of K
  are 20 = 2 * 10 as they must). No component is excluded by its own triple design. (Codex confirms that x32 only
  checked candidate counts per pair, not a simultaneous design.)
* BOTH components (types 0 and 0, 70 308 layer-compatible pairs of triples, 6 642 rows: pair multiplicities in each
  component, cross multiplicities, each triple at most once, each 3-set in at most one shadow): LP relaxation
  feasible; CP-SAT UNKNOWN after 240 s with 4 threads. Beyond a tiny check; NOT pursued further here (the full sweep
  is 120 type pairs). Undecided.
Codex (generic side, being verified there): for an edge uv of G(T) between two layers at P = 0, the stars of u and v
share exactly one shadow, the cross edges between the two other sets of nine shadows form a matching of size
7 + c4(uv), so c4(uv) <= 2; at S = 0 the union is three paths plus at most one cycle of length 8 or 12 (38 abstract
types). And the 60 centred shadows live in a non-degenerate Green space of dimension 33 (not 35) when d(T) = 1.

CORRECTION to 17.53 (Codex, about 18:10 UTC; checked here): each h_T = 1_(C_1) - 1_(C_2) is already an INTEGER
3-eigenvector, so the 231 vectors h_T have rational rank at most 54 and satisfy at least 177 independent integer
relations, whose reductions mod 7 are relations with witness y = 0 (empty support). So "at least 114 relations must
have non-local witnesses" is wrong as stated: the >= 213 relations mod 7 among the classes include >= 177 automatic
rational ones, and what rank 37 adds is only the gap between the rational span (<= 54) and its image in the 18-
dimensional quotient. The local-to-global question concerns the support of the COEFFICIENTS (relations generated by
the at most 99 vertex-incident ones), not the support of y, and 213 against 99 is far from a contradiction.

Addendum (Codex's remark, about 18:15 UTC): my 630 candidate triples missed the filter "every x of C has at most 2
G-neighbours in the triple of a far vertex w (at most 1 if x is in it)" (mu / lambda between x and w; the triple
N_G(x) would give x and w three common neighbours). With it: 612 candidates (exactly the 18 neighbourhoods removed);
the single-component designs still exist for all 288 components; the joint LP for types (0, 0) is still feasible
(63 504 pairs, 6 606 rows). Nothing changes in the conclusions. Codex's note 209 (commit 06ade60 of its branch): the
two-star edge coupling catalogued (38 / 19 / 5 abstract patterns for c4(uv) = 0 / 1 / 2, Gram ranks 15 to 19, none
excluded by the 33-dimensional Green space alone); it needs a JOINT two-star model, not the one-star star_test.

### 17.54 Codex's joint two-star model (note 211): audit and an independent batch (18:30 UTC)

Codex's notes 210, 211 (commits 1b9f9c2, b3e99d4 of its branch): note 210 audits the residual (6,6) case (b(F_v) <= 1,
coefficients versus witness support, the 700 K_3,3 systems, the filter 630 -> 612); note 211 implements the joint
model of two generic stars on an edge uv between layers (common apex enumerated; 18 other shadows; exact sums K e_u,
K e_v; Green products; internal capacities; transversal matching of size 7 + c4; no prism; partial incidence <= K;
all known near/far and far/far common-neighbour ceilings). My audit (each constraint re-derived for a generic line at
rank 37 and P = 0): all necessary; the transversal size 7 + c4 not re-derived, the formula c4 = (G^3)_uv - 5 checked.
The model uses R_T = 0 (g in {2,3}, g(n,n) = 6), so it does not apply as such to (6,6) lines.
Independent batch requested by Codex (`joint_generic_stars.py --apex-start 100 --max-apex 3 --seconds 30`, ball
cyclic (2,4,1), centres 0 and 12; `joint_generic_stars_apex100.json`): apex branches 100, 101, 102 all INFEASIBLE at
presolve (0 search branches, about 0.6 s each); PARTIAL_RUN_NO_GLOBAL_EXCLUSION. That ball was already excluded by one
star: a calibration, not a new exclusion. Proposed to Codex: since every branch dies at presolve, test whether the
linear relaxation already fails; its Farkas multipliers could suggest a uniform identity.

### 17.55 Codex's two-star certificates (note 212) re-run, and extended to three September random balls (18:55 UTC)

* Codex's note 212 (commit f87be43 of its branch): on the cyclic ball (2,4,1), edge (u, v) = (0, 12), branch 100 dies by
  exact propagation (star sums + pairwise compatibility supports, 263 deletions) and branch 0 by an exact integer Farkas
  certificate of the pair-marginal LP (22 339 pair variables; weighted rhs -4589 against box bound -522). Re-run here:
  both `--verify-only` replays pass; the verifier's logic (Farkas with the box 0 <= x <= 1, equalities with free sign,
  inequalities with non-negative multipliers) is correct.
* NEW, mine (`make_random_balls.py` regenerates the September calibration balls, seed 2609, same filters, keeping the
  triangle-free ones; `sweep_two_star_propagation.py` runs Codex's setup / propagate / replay over ALL common-apex
  branches of one ball; outputs in `balls/`):

| ball (edge 0-12) | tau mod 7 | c4(uv) | branches | dead by propagation alone | survivors -> pair LP |
|---|---|---|---|---|---|
| September random ball 5 | 5 | 0 | 368 | 368 | none |
| September random ball 9 | 5 | 1 | 464 | 464 | none |
| September random ball 12 | 6 | 0 | 416 | 412 | 4 (33, 113, 137, 184): all 4 killed by EXACT integer Farkas certificates (`balls/pairlp_ball12_summary.json`) |
| cyclic (2,4,1) | 5 | 0 | 473 | 260 | 213 (not run: about 50 min of LPs) |

  So for three random balls the two-star model excludes every branch with finite exact certificates (propagation
  traces replayed, Farkas vectors checked in integers); about 26 to 39 s per ball for the propagation.
* Structure of the certificates (all five LP certificates so far): only domain normalisations, pair marginals, the
  72 star-sum rows and 24 to 36 degree rows carry weight; no near/near or near/far ceiling beyond the star sums, no
  prism row. So the obstruction is "exact star sums + exact internal and transversal degrees + pairwise Green
  compatibility", already fractionally infeasible at the pair-marginal level.
* Scope: these balls were already excluded by one complete star (September). What is new is a solver-free,
  replayable reason, the same on three balls, with a small fixed set of constraint families: the right object for a
  uniform lemma. Not a uniform lemma, not a new rank exclusion.

### 17.56 Which rows of the two-star certificates are really needed (19:33 UTC)

Object (Codex's notes 211-213): generic line T, P = 0, edge uv of G(T) between two layers, common apex w (the third
point of the line uv) fixed; 9 + 9 other shadows, each labelled by its second point in the layer of its centre;
domains after Codex's exact propagation; pair tables = Green value in {2, 3} plus the pairwise filters of
`joint_star_propagation.setup` (overlap, capacity, saturation, K ceiling on a shared pair). All "EXACT" below =
integer Farkas vectors found and checked by Codex's own `find_bounded_dual` / `verify_farkas` on the reduced matrix.

1. Potentials (note 213) on my four certificates of random ball 12 (branches 33, 113, 137, 184):
   `two_star_potentials.py --drop-degrees` fails on all four; with the degree multipliers kept it gives exact potential
   certificates (gaps 38, 3, 85, 4; `--verify-only` passes; `balls/potentials_ball12_*.json`). In all four the star
   multipliers beta are positive at G-distance <= 2 from their centre and negative beyond
   (`balls/potentials_ball12_comparison.txt`).
2. After re-optimisation the degree rows are NOT needed (`radial_two_star_exact.py`; rows = domain + pair marginals +
   star sums only, aggregated or not):

| ball, branches | star rows kept | result |
|---|---|---|
| ball 12: 33, 113, 137, 184 | 13 sums by G-distance from the centre | EXACT, gaps 704, 1546, 1532, 4383 |
| ball 12: same | 2 classes per side: distance <= 2 / > 2 | EXACT, gaps 1, 1052, 1426, 2727 |
| ball 12: same | 2 classes: distance <= 1 / > 1 | only 184 (which is already infeasible with no star row at all) |
| cyclic (2,4,1): 19 survivors sampled (every 8th) | 2 classes: <= 2 / > 2 | EXACT for 8 (0, 90, 149, 171, 212, 241, 276, 337); FEASIBLE for 11 (33, 57, 75, 104, 124, 137, 182, 193, 230, 260, 314) |
| cyclic: 33, 57, 75, 104, 124, 137, 182, 193 | all distance classes | EXACT only for 104; feasible for the other seven |
| cyclic: 33, 57, 75, 124, 137, 182, 193 | the 72 pointwise star sums, no degree row | EXACT for all seven (gaps 730, 490, 2404, 809, 220, 483, 1405) |
| cyclic: 33, 57 | Codex's full pair LP (`balls/pairlp_cyclic241_apex*.json`) | EXACT (gaps 743, 334) |

3. Direction of the aggregated inequality on ball 12 (`radial_ball_range.py`, floating, diagnostic): let m_s be the number
   of points of the 9 non-apex shadows of side s inside the G-ball of radius 2 around its centre; the star sums force
   (m_u, m_v) = (16, 14). On the pair-marginal polytope: m_u + m_v >= 30.27, 31.22, 31.55 for branches 33, 113, 137
   (target 30). With the pairs inside one star only, neither side is excluded (e.g. m_u in [15.89, 20.70] for 113).
   So there, compatible pairs force TOO MANY shadow points near the centres, and the pairs across the two stars are
   needed at this level of relaxation.

What this establishes: in every surviving branch tested so far (4 of ball 12, 16 of the cyclic ball), "domains + pair
tables + exact pointwise star sums" is already fractionally infeasible, with exact certificates; degree rows, ceilings and
prism rows never carry necessary weight. What it refutes: the distance-aggregated form (my hypothesis from item 1) is
not uniform; it fails on most cyclic branches (230, 260, 314 not tested pointwise). Scope: finite certificates on balls already excluded by one star in
September; no uniform lemma, no new exclusion of rank 37.
Not launched (above the five-minute rule): the pointwise-without-degree certificate on all 213 cyclic survivors, about
213 x 8 s = 30 minutes, one process, below 3 GB.

### 17.57 Minimal supports of the two-star certificates; LAP's real Green identity; a heuristic and its limits (19:55 UTC)

**1. Minimal supports on random ball 12, edge (0,12)** (`min_support_two_star.py`; rows = domain + pair marginals +
pointwise star sums; domains = those of Codex's full propagation; greedy steps decided by floating HiGHS, final vectors
checked in integers by Codex's `verify_farkas` and archived in full in `balls/minsupport_<mode>_ball12_apex<k>.json`).
Removing a shadow turns the star sums of its side into  t(p) - m <= sum <= t(p)  (valid for any sub-family of a solution).

| branch | fewest shadows found (all 72 star rows) | fewest star rows found (all 18 shadows) | those rows, then fewest shadows |
|---|---|---|---|
| 33 | 9: the nine shadows of star v alone (gap 562) | 32 (time budget reached, not reduced) | - |
| 113 | 11: 8 of u + 3 of v (gap 59 891) | 4: star v at points 28, 31, 33, 35 (gap 124 833) | 15: 6 of u + 9 of v |
| 137 | 15: 8 of u + 7 of v (gap 84 468) | 2: star v at points 34, 35 (gap 45 356) | 15: 6 of u + 9 of v |
| 184 | 10: 3 of u + 7 of v (gap 12 159) | 0 (already infeasible with no star row, 17.56) | - |

Reading: the sufficient supports are far from unique (for 137 a first sparse dual used 27 star rows, two suffice) and
few rows cost many shadows: the relaxation is infeasible in many diffuse ways; no single small sub-configuration was
isolated. At the four points of branch 113 no pigeonhole is visible (every shadow of star v has 1 to 10 candidates
through each point). Minimality is for single deletions and numerical; the cores are upper bounds.

**2. LAP's exact real identity (relayed 19:34 UTC; LAP's hand derivation with a trace check; Codex re-derived the first
line; I checked only the consequence Pi 1_{S_u} = 0; items (c), (d) below not audited by anyone else).** For a line with
connected G, at every rank, H^+ the real pseudo-inverse of 3I - G, Pi (rank 8) and Pi' (rank 18) the orthogonal
projectors onto the (-4)- and 3-eigenvectors supported on the far set:
    n_f^T H^+ n_f = 37/12 - 7 Pi_ff,   n_f^T H^+ n_f' = 1/12 - A_ff' - 7 Pi_ff',   n_f^T (4I+G)^(-1) n_f = 138/35 - 7 Pi'_ff,   Pi N^T = 0.
The September conditions (g = 6, g in {2,3}) are its reduction mod 7; rank 37 = "Pi is 7-integral". Lost by the
reduction: (a) real Green norm <= 37/12; (b) a Cauchy-Schwarz bound on pairs; (c) for a star, Sigma = 3I - A_star + J/12
- N_s^T H^+ N_s is positive semidefinite of rank <= 8; (d) a square condition on eight far vertices. Measured by LAP on
four balls: (a) keeps 86 to 95 % of the candidates, (b) removes 37 to 39 % of the mod-7-compatible pairs. True at every
rank, so exact additional filters, not an exclusion.

**3. A heuristic, recorded as such.** `logs/star_expected_count.log` of September (structures-lab) gives 8.6e-16 and
2.2e-15 expected complete stars per ball (product of probabilities assumed independent). With an orbit mass of
(11!!)^3 / 6 = 1.9e11 balls (three layer matchings and three bijections modulo S_12^3 x S_3; a mass, not an exact count
of classes) this gives well below one expected star over all balls. So "42 of 42 balls dead" is what randomness
alone predicts and is not by itself evidence of a structural lemma. Codex's objections, which I accept: the
independence assumption is uncalibrated; the size of an infeasible core does not decide whether a short uniform proof
exists (a pigeonhole or parity argument may need every object); so this is a guide for choosing experiments, not a
verdict on (a'). Order of magnitude only, nothing proposed or launched: an exhaustive certificate over all balls
would need a compiled one-star search (September: 13 s per star in Python, 15 796 nodes) on about 1e10 to 1e11 balls,
i.e. CPU-years, and would cover only generic triangle-free lines (NT and the disconnected case would remain).

### 17.58 Codex's exact pair-filter ablation (note 214) applied to random ball 12 (20:05 UTC)

Codex's note 214 (commit 96e7f23, `two_star_core_ablation.py`, read before running): the pair tables are rebuilt in
cumulative modes (green: Green value in {2,3} only; overlap; capacity; saturation; then K filter within a star or across
the two stars), the propagation is redone in each mode, and the LP has only domains, pair marginals and pointwise star
sums. Feasibility is certified by an exact rational witness (integer masses over 100000, all equalities checked in
integers), infeasibility by an integer Farkas vector. On the cyclic ball Codex found: branch 0 feasible up to capacity,
infeasible from saturation; branch 33 feasible at saturation, infeasible with the K filter (within or across).

Applied here to the four surviving branches of random ball 12, edge (0,12) (`balls/ablation/core_<mode>_ball12_apex<k>.json`):

| branch | green | capacity | saturation | within | across |
|---|---|---|---|---|---|
| 33 | exact rational witness | exact rational witness | EXACT contradiction, gap 763 | gap 1400 | gap 1842 |
| 113 | numerically feasible | exact rational witness | EXACT contradiction, gap 2193 | gap 3896 | gap 3075 |
| 137 | numerically feasible | exact rational witness | EXACT contradiction, gap 1311 | gap 3040 | gap 2010 |
| 184 | exact rational witness | exact rational witness | EXACT contradiction, gap 1385 | gap 4053 | gap 2404 |

`--verify-only` replays pass on capacity and saturation for 113 and 137. So on ball 12 the threshold is the same in all
four branches and the same as Codex's cyclic branch 0: exactly feasible with the Green values, overlaps and capacities,
exactly infeasible once saturation is added. Five branches of six (two balls) have their threshold at saturation.
Branch 184, infeasible with no star row in the full mode (17.56), is exactly feasible in the green and capacity modes:
the Green values alone do not kill it.

Reading (mine, sent to Codex for checking): saturation is the weakest 0/1 form of the near/far block of the SRG
equation, N A_F = 2J - (G + I) N, i.e. for a far vertex i and a near point p the number of far neighbours of i whose
shadow contains p equals 2 - n_i(p) - (G n_i)_p; saturation forbids such a neighbour when this number is 0. The core seen
on two balls is therefore: Green values mod 7 (rank 37) + exact star sums (near/near block N N^T = K) + the near/far
block reduced to "budget exhausted". (I checked by hand that the rank-37 formula A_F = 3I + 3J - N^T H^+ N satisfies the
near/far block automatically modulo 7; the exact 0/1 form is what the relaxation was missing.)
Also recorded, Codex's caveat on 17.57: "the nine shadows of star v alone" (branch 33) is a core of the final relaxation
only; the prior deletions of the propagation may use the nine other shadows.
Scope unchanged: finite certificates on one edge of two balls already excluded in September; no uniform lemma.

### 17.59 The two-star obstruction needs only Green values and star sums: a depth-one, solver-free refutation (20:22 UTC)

Three steps, each sharper than the previous one. Pair tables and propagation are Codex's (`filtered_system`, `propagate`,
commit 96e7f23), rebuilt in each mode; the unary pools (norm 6 mod 7, local filters) and the filters against the common
apex (Green value 3, overlap <= 2) are unchanged in every mode.

1. **Capacity mode (no saturation) + internal collisions** (asked by Codex): for two shadows of the same star, forbid a common
   point p with residual star sum t_s(p) = 1. Ball 12, edge (0,12): branches 113 and 184 exactly infeasible (Farkas gaps
   10 and 1); branches 137 and 33 exactly feasible (rational witnesses). An exact separation: this pairwise consequence
   of the conditioned sums is not enough everywhere. (`capacity_collision.py`, `balls/ablation/core_capacity_plus_internal_collision_*.json`.)
2. **Capacity mode + all conditioned star sums** (each star-sum equation multiplied by "shadow i takes candidate c" and
   linearised with the pair marginals; valid for every integer solution; only the near/near block): exactly infeasible
   on the four branches of ball 12, with the largest possible gap (126 000 = 1000 x (18 + 108): multiplier -1 on every
   normalisation and every star sum, no negative column), i.e. every single candidate is excluded. Positive control:
   with a planted integer solution the lifted LP stays feasible. (`lifted_core.py`.)
3. **No LP at all: assign one shadow, then propagate** (`sac_two_star.py`). Fix shadow i to a candidate c, run Codex's
   exact propagation (pointwise star-sum bounds and pair supports) on the current domains; a contradiction deletes c; an
   empty domain excludes the branch. Integer and deterministic. With the private pair tables in mode GREEN (Green value
   in {2,3} only: no overlap, capacity, saturation, K filter, degree, or real inequality):

| ball, edge (0,12) | common-apex branches | excluded by plain propagation | excluded after assigning ONE shadow | candidates of that shadow (min / mean / max) | time |
|---|---|---|---|---|---|
| September random ball 5 | 368 | 0 | 368 | 6 / 18.7 / 27 | 70 s |
| September random ball 9 | 464 | 0 | 464 | 8 / 20.4 / 28 | 92 s |
| September random ball 12 | 416 | 0 | 416 | 11 / 22.6 / 31 | 91 s |
| cyclic (2,4,1) | 473 | 0 | 473 | 17 / 27.0 / 37 | 133 s |

   In all 1721 branches one round suffices and the pivot is simply the shadow with the smallest domain; each leaf is a
   propagation of 20 to 110 events ending with an empty domain. Positive control: with a planted solution the procedure
   ends alive with every planted candidate present (3 seeds). Outputs `balls/sac_green_*.json` (deletion lists; the
   replay is the recomputation).

What this establishes (pending Codex's audit of the 50-line script): on these four balls the two-star obstruction on
one edge follows from (i) the Green values mod 7 between shadows and (ii) the exact star sums alone, by a proof tree of
depth one (about 450 apexes x 23 candidates = 10^4 propagation leaves per edge). The near/far block (saturation), the K
filter and LAP's real inequalities are alternative strengthenings, not necessary ingredients; Codex's note 215 shows
conversely that the real 3 x 3 PSD filter with the apex kills by propagation alone, without any assignment.
Scope: balls already excluded by one star in September; one edge per ball; finite certificates; no uniform lemma, no new
exclusion of rank 37.

### 17.60 Status of 17.59, and two negative results from the laptop session (20:27 UTC)

* **Audit of `sac_two_star.py` by Codex (in progress, its message of 20:28 UTC).** `restrict()` and the index mapping look
  correct to it, and nothing is inherited from a stronger mode. Certification gap, accepted: `close()` replays Codex's
  trace only when the propagation survives, so the traces of the contradictory leaves are not replayed here. Codex is
  building a `.proofs.jsonl.gz` archive for the four balls (one pivot, every candidate tested from the same base
  domains, independent replay on the original indices). Until then 17.59 is "computed, not certified". The two lifted
  certificates of 17.59 item 2 (3.5 MB and 10 MB) are kept locally only; they are rebuilt in 15 s each.
* **Laptop session, 20:09 UTC (hand): no closed form in G alone for a star.** In the 10 x 10 real block of a star only the
  row sums depend on G alone (everything bilinear in N does: N f(A_F) N^T = f(-(G+I)) K + cJ); already the trace of the
  block depends on a third moment of N (the number of far vertices adjacent to u, w, z). So no invariant of G can be
  tested without a search at that level. Usable form of the star equation: with n_f = e_u + m_f and Q the real Green
  Gram of the ten 5-sets, the largest eigenvalue of P (A_star + Q) P on the sum-zero space is exactly 3; for a sub-star
  only "at most 3" remains. Its derivation of the square condition was relayed to Codex for audit.
* **Laptop session, 20:26 UTC (measured on three random admissible balls, exact rational H^+): no uniform counting
  inequality.** Through a point: about 25 000 candidate shadows, 3 516 to 3 731 of Green norm 6 mod 7 (1/7 within 5 %);
  through a transversal edge: median 3 400 apex candidates, 324 to 468 after "real bound + norm 6", none of the 108 edges
  without a candidate; 0.164 of the pairs compatible mod 7. Counts of single shadows and of pairs are equidistributed and
  never small: what kills is the conjunction (45 pair conditions on 10 choices, then the cover). Idea tested and
  REFUTED by that session: an apex shadow contains two G-adjacent points, so its real energy might exceed 37/12; the
  minimum per edge is 1.87 to 2.02 (bound 3.083). So the strength of Codex's 3 x 3 minor with the apex comes only from
  the two known (zero) adjacencies, not from an apex of small projection.
  Its reasons against a uniform bound of counting type, which I accept: such a bound is a cancellation statement for
  character sums uniform in the quadratic form (false for special G); every second-order average is determined by G and
  automatically consistent; my "340 x 2/49 = 14 candidates" is an expectation over G and says nothing for very
  symmetric balls. So my question of 20:27 UTC is answered negatively; the heuristic of 17.57 item 3 stays a heuristic.
* What remains independent of G, hence the only material for a uniform statement (the laptop session's view, which I
  share): the FORM of the two identities (real: Sigma_X positive semidefinite of rank <= 8 for every X; mod 7: Pi
  7-integral) and the star-sum relations.

### 17.61 It is a ONE-star obstruction: ball 12, the star of vertex 12 alone (20:36 UTC)

Codex's intermediate audit of 17.59 (its message of about 20:30 UTC): ball 5 fully re-derived, 368 of 368 branches, 6882 leaves,
every leaf trace verified on the original indices, my deletion lists identical; planted integer witnesses survive and
four deliberate corruptions are rejected; the three other balls are being replayed (its notes 216, 217 to come). Codex
also confirmed, with an independent reconstruction, the laptop session's square condition and its constants
(tau = (9/4) 7^(37-r) t^2 det(L_far); tau x det(7 Pi_X) a rational square for eight far vertices).

Codex's remark: with the tables BETWEEN the two stars replaced by "all compatible", most of its pilot branches still
die. Checked here on the whole of ball 12 (`one_star_sweep.py`, `balls/onestar_green_ball12_*.json`): Green-only tables
inside each star, no table between the stars, so that the two stars share only the fixed apex w and are independent
problems (nine private shadows, exact sums K e_centre - w, Green value 3 and overlap <= 2 against w, Green value in
{2,3} between them); pivots by increasing domain size, at most four, every candidate of the pivot tested from the same
fresh base domains with Codex's propagation.

| ball 12, edge (0,12), 416 apex candidates | refuted | pivots needed (1st / 2nd / 3rd / 4th) | not refuted within 4 pivots |
|---|---|---|---|
| star of vertex 12 alone | 416 | 384 / 25 / 6 / 1 | 0 |
| star of vertex 0 alone | 398 | 314 / 52 / 28 / 4 | 18 |

Leaves per apex for the star of vertex 12: 11 to 125, mean 26.7 (about 11 000 propagation leaves in all). Plain
propagation refutes no branch. So on this ball the contradiction sits in ONE star: for every apex candidate w of the
star of vertex 12 in the direction of vertex 0 there are no nine further shadows of norm 6 with Green value 3 against
w, mutual Green values in {2,3} and sum K e_12 - w. The links between the two stars are not needed there.
Novelty, stated honestly: that a complete star dies with the Green values alone was already observed by search in
September (`logs/star_ablation_astra.log`: "only_green: dead; nodes 416964"). New here: the shape (apex, one pivot,
propagation), the size (10^4 leaves), and the exact replay Codex is building. Status: a classification, not a certified
archive (leaves not replayed on my side). Only ball 12 was run (6 min 20 s in three pieces).

### 17.62 Codex's audit is complete; the 18 resisting branches of the star of vertex 0 (20:42 UTC)

* **Audit complete (Codex, commit b917050 of its branch, notes 216 and 217).** Note 216: the 1721 branches of 17.59 are
  confirmed with the same pivots and the same deletion lists as mine; 38 518 leaves (6882 + 9484 + 9395 + 12 757), each
  started from the same base domains, every trace verified on the original indices and tables, then every archive
  replayed from disk; planted integer witnesses survive, four corrupted certificates are rejected. It also certified 13
  pilot branches with no table between the stars (349 leaves, every event of each leaf on the side of the pivot): the
  proof is local to one conditioned star. Note 217: independent audit of the laptop session's square condition. So
  17.59 is now CERTIFIED by Codex for the four balls; 17.61 (whole ball 12, one star) remains a classification.
* **Manifest of refuting pivots for ball 12** (asked by Codex): `balls/onestar_green_ball12_manifest.json`.
* **The 18 apexes where the star of vertex 0 resists four pivots** (`pivot_profile.py`, `balls/pivot_profile_ball12_*.json`).
  OBSERVATIONS on this one ball, none of them a general implication:
  1. They are not solutions: an exact search (branch on the smallest domain, Codex's propagation at each node) finds
     no assignment of the nine private shadows with the Green-only tables and the exact sums, in 2 to 4 nodes for each
     of the 18 apexes. The star of vertex 0 is refuted too, at depth two.
  2. No leaf dies by a one-step cover failure: after the Green cut by the pivot candidate, no coordinate has
     need > capacity (0 of 2619 leaves) and no coordinate is even tight (need = capacity). Every refutation is a cascade
     of about 30 to 50 alternating sum and pair deletions. So there is no "profile of tightened targets" to read at depth one.
  3. Survival of a pivot candidate depends sharply on how many coordinates of residual sum ONE it contains (these are the
     points within G-distance 2 of the centre, plus the points already used once by the apex):

| coordinates of residual sum 1 in the candidate | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| survive / refuted (2619 leaves, star of vertex 0) | 87 / 174 | 38 / 936 | 1 / 1057 | 0 / 313 | 0 / 13 |

     For the star of vertex 12 on six of the same apexes: 0 survivors in every column (24, 64, 43, 6 refuted).
  4. The two stars differ in size, not in kind: smallest pivot domain 19 to 24 for vertex 12 against 27 to 39 for
     vertex 0; smallest Green cut 5.0 on average against 7.4 (refuted) and 9.1 (surviving).
  Reading (hypothesis): a candidate through a coordinate of residual sum one removes that coordinate from the eight other
  shadows; with two such coordinates the remaining domains are too small to cover exactly. This is the internal
  collision of Codex's note 214 acting through propagation; it is a counting mechanism, not an identity. It agrees with
  17.56 item 3 (compatible shadows carry too many points near the centre), now seen at the level of single candidates.
* The laptop session (20:39 UTC) lists what is automatic and need not be retested: every first- or second-order
  condition on the apex alone follows from bilinearity (e_v^T K H^+ n_w = 5 mod 7; the sum of the 81 entries of the
  Gram of the nine = 3 mod 7 since (K H^+ K)_vv = 0). It also gives, labelled as a reformulation, an independent
  verifier without H^+: a star is admissible iff the Seidel matrix J - I - 2A of the abstract 49-vertex graph (ball of
  T, ten far vertices joined to their shadows, 4K_2 between them) has rank 36 modulo 7. Not tested here.

### 17.63 CORRECTION of 17.62; Codex's counting lemma; the forced pattern is not excluded by three shadows (20:51 UTC)

* **Correction (found by Codex).** In 17.62 and in my message to Codex I wrote that the star sums K e_v take the value 1 on
  8 points and 2 on 16 points outside the layer of the centre, "from the sums alone". This needs z = 0, where z is the
  number of points outside the layer joined to the centre by two 2-paths of G (4-cycles through the centre). In
  general: K = 1 on 8 - 2z points, K = 2 on 16 + z points, K = 0 on z points. In our balls: ball 5 and ball 9, centres 0
  and 12: 6 / 17 / 1; ball 12: centre 0: 8 / 16 / 0, centre 12: 6 / 17 / 1; cyclic: 8 / 16 / 0 at both centres. So the two
  stars of ball 12 do NOT have the same profile, and observation 4 of 17.62 ("they differ in size, not in kind") is
  withdrawn. Also: the 38 518 leaves of Codex's archive are all refuted, so they cannot test observation 3; and my
  single survivor with two coordinates of residual sum one (apex 187, pivot 0, candidate 17) refutes the algorithmic
  rule "two such coordinates imply a contradiction by plain propagation".
* **Counting lemma (Codex; checked here by hand, independently).** Let z = 0, P = the 8 points outside the layer with
  K = 1, a(n) = |n ∩ P| for a member n of a complete star, and for an apex w and another member n let d_w(n) be the
  number of points of n outside the layer where K e_v - w equals 1. Then some apex w and some other member n have
  d_w(n) >= 2. Proof: each point of P is covered once, so n ∩ P avoids w and d_w(n) >= a(n); if every d were <= 1, the
  two apexes (each contains a transversal neighbour of v, so a >= 1) would have a = 1; for such an apex the coordinates
  of residual sum one number (8 - 1) + (4 - 1) = 10, to be covered once each by nine members with at most one each.
  Only the star sums are used, not the Green values.
  Refinement (mine, to be checked by Codex): d_w(n) >= 2 means (a) a(n) >= 2, or (b) a(n) >= 1 and n ∩ w = {v, x} with
  K_vx = 2; the third possibility, two shared points of K = 2, would give |n ∩ w| >= 3, impossible for two non-adjacent
  far vertices. Local filters also give a(w_i) <= 3.
* **The forced pattern is not excluded by three shadows** (`two_apex_triples.py`, ball 12, centre 0, z = 0). Triples
  (w1, w2, n) with both apexes, which are isolated in the star, so that the three adjacencies are known: 24 058 apex
  pairs pass the mod 7 and sum conditions (10 814 also the real 2 x 2 test); triples passing mod 7: 344 057 with d >= 2
  and 333 489 with d <= 1; passing also the real 3 x 3 positivity (floating, diagnostic): 77 880 and 91 175. The real
  test removes 77 % of the triples but does not single out the pattern.
* **Why the pattern cannot be forbidden without the Green values of the particular G (argument).** In any
  srg(99,14,1,2), for adjacent v and n, each of the 12 other neighbours p of n lies on a quadrilateral (v, q_p, p, n)
  with a unique q_p adjacent to v. Pattern (a) only says that two such p and their q_p lie in the ball of T: a condition
  on the position relative to T, with no content of its own. So the lemma identifies what must be forbidden, but
  forbidding it for every ball is again the uniform statement we do not have.

### 17.64 Scope of the star route: what Codex and I agree on, and what I had overstated (21:12 UTC)

After Codex's note 218 (forced pattern from the unit coordinates: general proof for z = 0, formulas 8 - 2z / 16 + z / z,
two counting counter-models, exact rational check of my triple of 17.63, reconstruction of the hard leaf of apex 187)
I sent Codex a scope argument before taking up patterns A / B. Outcome of the exchange:

* **Agreed.** Stop re-reading the dead examples. No uniform strategy for forbidding A and B is established at present.
* **Not agreed, and Codex is right.** I wrote "by this route (a') is reachable only by enumerating the balls, not by a
  lemma". The absence of a strategy is not an impossibility theorem. Withdrawn in that form.
* **Overstatements of mine, corrected by Codex.**
  - "Counting and the local SRG filters alone cannot give a contradiction": my evidence was the September witness,
    which concerns only the constraints LISTED there, on ONE cyclic ball, and Codex's counter-models of note 218, which
    are abstract incidence matrices without any G. Not a general statement.
  - "Everything bilinear in N is automatic" is false as written: the individual Green products in {2,3} are bilinear in
    two shadows and are not automatic, and the real bound n^T H^+ n <= 37/12 removed 14 apexes of the cyclic ball (note
    215). What is automatic is a family of contractions and sums (star sums against the Green form, degrees, traces).
  - My cost figure (2.6e10 balls x 20 ms = about 16 core-years) is arithmetic under three uncertified hypotheses: an
    orbit MASS is not a count of classes, 35 of 92 is not a certified conditional probability, 20 ms is not a measured
    cost. Neither a lower bound nor a proof that enumeration is needed.
* **What stands.** In the formulation "one generic ball at rank 37", the rank is encoded by R = 0 and the prescribed
  Green values; Codex has no other operational uniform argument on A / B either. Global rank and discriminant
  constraints exist (its note 205, the centred 18-dimensional space, not to be confused with the 33-dimensional Green
  space of the shadows), but no useful translation of A / B into that space has been built.
* **A real limit announced by Codex (to be published with an explicit witness).** Any Green-compatible pair of apexes
  and any compatible third member complete to the abstract Gram of ten vectors over F_7 with the prescribed sum, once
  the 0/1 supports are dropped (Gram 3I + 3J - A(4K_2 + 2K_1), determinant 2; ambient dimension left 28 against 6 to
  realise). So no further abstract Gram test on one star can close the problem: one has to keep the supports, or couple
  neighbourhoods.
* A check of mine that came to nothing and is recorded so that it is not redone: index-7 overlattices of L1 along an
  isotropic class of its 7-discriminant form have the genus of the next rank; averaging their theta series over all
  isotropic lines only reproduces a_{7k} >= b_k, which follows from the modularity already used in the theta programme.

State of rank 37 at this point: counting route closed by its margin (17.44, 17.45, 17.49); star route: exact certified
certificates per ball, one forced pattern valid for every ball with z = 0, no strategy for a uniform contradiction; NT
and the disconnected case untouched today.

### 17.65 Codex's barrier (note 219) checked independently (21:25 UTC)

Codex's note 219 (commit 108784b of its branch). Statement: G generic (rank_7 of H equal to 35), triangle-free, one
neighbour per layer; two apex shadows w1, w2 and one NON-APEX shadow n, all binary (two points per layer, centre once),
of Green norm 6 and mutual Green products 3. Then they extend to ten SIGNED INTEGER vectors with the complete Gram
3I + 3J - A(4K_2 + 2K_1) modulo 7, the exact sum K e_v, every layer sum 2 and central coordinate 1. No hypothesis on
4-cycles. Proof idea as given there: the five vectors (sum, w1, w2, n, dual of the central coordinate) have a
non-degenerate Gram; the complement to realise has dimension 6 inside a non-degenerate ambient complement of dimension
28, and over F_7 a non-degenerate form of dimension 2k represents every non-degenerate form of dimension k; then
corrections by multiples of 7 restore the integer sums.

Independent check here of its explicit witness on my triple of 17.63 (ball 12, centre 0; my own inversion of H + J
modulo 7 and my own K, not Codex's verifier): the Gram modulo 7 equals the target; the row sums equal K e_0 exactly;
all layer sums are 2; the central coordinate is 1 in every column; the first three columns are the binary supports
[0,1,12,13,26,35], [0,2,18,21,24,25], [0,7,22,23,29,32]; the seven others have 17, 29, 28, 31, 25, 30, 34 non-binary
entries, values from -42 to 238. All checks pass.

Meaning: on one star, every condition expressed through the Green form and the sums (norms, pair products, star sum,
layer sums) is satisfiable around such a triple once the shadows are allowed to be integer vectors. A contradiction must
therefore use that the shadows are 0/1 sets, or constraints linking several neighbourhoods. This is a statement about
what cannot work; it excludes nothing and does not show that the remaining options work.

### 17.66 Change of direction reported by Codex; what I could give it (21:54 UTC)

Codex reports (its message; I did not receive this instruction directly) that the user asked it to look for routes to
C1 other than the successive exclusion of ranks, in the manner of routes A / B / C of C2. Codex takes that
investigation and sorts three directions: (1) a global combinatorial obstruction on the three layers (binary N, no
rank hypothesis); (2) a forced configuration followed by a star-complement reconstruction; (3) SRG-preserving
transformations with an extremal argument. It asked for precise objections or earlier results with files. Sent:

* **Direction (1).** I have no witness of a complete binary N (36 x 60, N N^T = K) at m = 12. What exists, all without
  any rank hypothesis: 60-triple designs for each of the 288 (6,6) components separately (17.53); the two components
  together undecided (LP feasible, CP-SAT unknown in 240 s); the six-grid line: column part solved canonically by the
  60 ordered stars of the Petersen graph (17.46, 17.47), row part undecided. Never tried on a connected generic ball.
  General structural fact (hand): two distinct points of the same layer never have a common G-neighbour, so K = 1 on the
  60 unmatched pairs of a layer and 0 on the 6 matched ones; hence in each layer the 60 columns of N are in BIJECTION
  with the 60 unmatched pairs, N is equivalent to two bijections between three copies of these pairs, and the condition
  between two layers is a decomposition of the bipartite multigraph of multiplicities 2J - G_AB - (G^2)_AB into 60
  quadrilaterals. A reformulation. Heuristic only: N N^T = K alone looks heavily over-determined per ball.
* **Direction (2), an objection (hand, checked).** For any two vertices a, b the integer vectors (A - 3I)(e_a - e_b) and
  (A + 4I)(e_a - e_b) are eigenvectors for -4 and for 3 respectively (because (A - 3I)(A + 4I) = 2J kills sum-zero
  vectors), supported on the 26 vertices of N[a] and N[b] that are not common neighbours. An eigenvector supported inside
  a vertex set makes its eigenvalue an eigenvalue of the induced subgraph, so NO star complement, for either
  eigenvalue, contains such a 26-set; in particular none contains the ball of a line, which carries two eigenvectors of
  each kind. "Ball plus 6" or "ball plus 16" far vertices are therefore never star complements, and the reconstruction
  theorem does not apply to a base containing a ball. The exact statement available for a ball is the laptop session's
  identity with its correction term (17.57).
* **Direction (3).** Nothing on my side: no earlier examination of a prism-increasing triangle switch.
* My view, stated to Codex: route C of C2 had an invariant that PARTITIONS the cases into finitely many (the
  involution); none of the objects above does that for C1.

### 17.67 The three routes of C2 re-read at the user's request, and what transposes to C1 (21:58 UTC)

User (direct): Codex looked only at route C; he had asked for routes A, B and C. Source re-read:
`Desktop/c2_experimental/notes/46_LIGNE_D_ARRIVEE_C2.md` (27/09), sections 1-8 (statuses as written there, not re-audited).
("Route A / route B" in T20_PROOF and T20_BOARD are something else: two decompositions of the case n_3 = 2 of lemma T20.)
* Common base of A and B: a counting identity forced by the involution, sum over the 7 blocks of w_c = 84 + 4|Sigma|,
  so some block has w_c >= 12 in every configuration; hence a completeness theorem: the local system I(tau) of the heavy
  block is satisfiable, and if all I(tau) are UNSAT there is no involution. Finite uniform list: 3308 classes of types.
* (A): the LOCAL instances of the types with pivots (1521, then 1507), one SAT instance per type with DRAT certificates.
  Stopped: 77 838 cubes, 32 of 32 unknown at 5 minutes.
* (B): the single GLOBAL residual family: if the heavy block is a free star then the whole configuration is "all-dis"
  (7 free stars). Orbit LP feasible, not killed at that level.
* (C): the lattice envelopes: N of rank 22, det 7^(22-g); an odd unimodular envelope U of rank 24 containing
  N + 7 I_2 with index 49 or 343 exists at g = 18 AS WELL AS at g = 20 and carries the frame; Borcherds: 156 lattices;
  excluding them kills (A), (B) and the rest at once.
Reading sent to Codex (message 258): route C did not separate the values of g, the envelope absorbs the rank into one
finite list; in C1 the same mechanism gives a 7-unimodular overlattice of L1 + 7 I_2 at every rank of the window, but of
rank 46, with no classification (in C2 the involution halves the rank). Our star route is the analogue of (A) without
its two pillars (no finite list of types, no counting identity forcing a heavy type), and "(6,6) everywhere" is the
analogue of (B). Three precise questions for a C2-like route: an object of bounded rank and controlled determinant; a
counting identity that forces non-trivial structure; a finite list of local types (the 177 grid profiles at a vertex are
the only finite catalogue we have).

### 17.68 A rank-free forced configuration with a finite catalogue (Codex), re-derived independently (22:07 UTC, 08/10)

User (direct, about 22:00 UTC on 08/10): C2 needed three routes; the point is not to imitate C2 but not to stay stuck
on one route, here the route "rank by rank", and to come back if the others are worse. Relayed to Codex in his words.

Two alternative organisations were put on the table.
* **Mine, checked in this note before proposing: split by structure (no grid / at least one grid).** Already on record
  (17.45): at rank 37 with rho = 0 the counting on Codex's collection has break-even 25 201 collisions per twin pair,
  against the certified GENERAL cap 31 976 for a non-grid twin pair; nobody computed the cap restricted to grid-free
  graphs. Asked to Codex. Best outcome: "rank 37 forces a grid", a reduction to a rigid rank-free base (a grid is a tight
  set). Not run.
* **Codex's, rank-free (its note 221 in preparation).** By Makhnev's theorem (L1) every srg(99,14,1,2) contains two
  disjoint triangles joined by exactly two edges: S = 012 + 345 with 03, 14 and no 25. Around S the masks and their
  numbers are forced: 8 vertices with two neighbours in S (supports 03, 14, 23, 24, 05, 15, 25, 25), 52 with one
  (9, 9, 8, 9, 9, 8), 33 with none. The core H = S + the 8 doubles (14 vertices) is present in every such graph, at
  every rank. Catalogue: 2299 labelled cores, 373 up to the group of order 8; the exact positivity of the two projector
  blocks 27I - 9A_H + J and 44I + 11A_H - 2J excludes 63 and leaves 310.

**Independent re-derivation here** (`twisted_core_check.py`, `twisted_core_check.json`; Codex's code and data not read):
* forcing, by hand: two disjoint lines are joined by at most 3 edges; if "at least 2" always meant 3, then for two
  lines L1 = {v,a,a'}, L2 = {v,b,b'} and c_ab the second common neighbour of a and b, the line through a and c_ab would
  have a third edge to L2, forcing c_ab ~ c_ab', and symmetrically c_ab ~ c_a'b: every two lines at every vertex would
  span a grid, against Makhnev;
* masks and numbers, by hand: 04 and 13 impossible (two common neighbours already in S); the counts above;
* enumeration: 2299 labelled; the seven pairs of doubles that are never adjacent are (03,23), (03,05), (14,24),
  (14,15), (23,05), (24,15), (25,25), also obtained by hand; 21 optional pairs; 373 orbits;
* exact test (rational symmetric elimination, an integer vector z with z^T Q z < 0 for each failure): 63 excluded, 310
  pass. All 63 exclusions come from the block of E_(-4); the block of E_3 excludes nothing more at 14 vertices. The two
  complementary conditions are automatic: 36I + 9A - J = (63/77)(44I + 11A - 2J) + (7/11) J and
  33I - 11A + 2J = (77/63)(27I - 9A + J) + (7/9) J.
So the covering statement is correct and rank-free: every srg(99,14,1,2) contains one of 310 cores.

Scope, stated to Codex at once: the catalogue classifies 14 vertices of 99; positivity of projector blocks is the
classical interlacing refined by J, weak on small subgraphs. The route is of "type C" only if every core DIES AT SMALL
DEPTH. Proposed decisive measurement, not run: forced closure only (third points of lines, missing common neighbours),
exact positivity at each step, recording the depth of death or the number of survivors per level.

### 17.69 The 174 remaining cores: two bounded pilots, both negative (22:33 UTC, 08/10)

Codex (its note 222, commit cdca3c6 of its branch, entry point RECHERCHE_ACTIVE_C1.md): the simultaneous incidence
equations of the 85 outside vertices on H (mask multiplicities, exact integer certificates) exclude 136 of the 310 cores;
174 remain. Covering of C1 without any rank: 373 -> 310 -> 174. My encoding matched with Codex's (its 310 = my 310;
`codex_unresolved_174_bits.json`). Division of work: Codex the global mask system, I the forced closure.

* **Pilot 1, forced closure** (`twisted_core_closure.py`). Added vertices: only the third points w(s, d) of the edges
  (s in S, d a double through s) with no common neighbour in H; forced, uniquely identified, pairwise distinct (6 to 12
  per core, 26 to 100 free pairs). Pruning: common-neighbour quotas inside H' and exact positivity of the two projector
  blocks after each added vertex. First try on 13 of the 310: one core dead exhaustively (bits 77595264, 339 nodes),
  which is among Codex's 136. On 15 of the 174 (cap 400 000 nodes or 18 s per core): no death, none exhausted, all at
  the cap. Survivors per level, typical: 1,1,1,1,1,1,1,1,1,9,1162,77892; 1,1,1,1,3,69,3077,57102. The first forced
  vertices have a unique adjacency, then the count grows by a factor 20 to 130 per vertex. (`twisted_core_closure_pilot174.json`)
* **Pilot 2, a second-level linear system** (`twisted_core_level2.py`). Variables Y[b, b'] = number of adjacent pairs of
  outside vertices of masks b, b'; exact equations of the pairs (outside vertex, vertex of H); admissible adjacent mask
  pairs filtered by quotas and exact positivity on H + 2. On 29 of the 174: level 1 feasible 29 of 29 (agreement with
  Codex, same numbers of masks), level 2 feasible 29 of 29 in floating point. No gain. (`twisted_core_level2_pilot.json`)
* **Identification (mine, sent to Codex for checking).** S is the object of the two-star model seen without rank: T = 012
  is a line, 3 and 4 are two adjacent near points (a transversal edge of G(T)), 5 is its far apex; the 8 doubles are the
  layer partners of 3 and 4, their other transversal neighbours, and the rest of the shadow of the apex. So the 373
  types are the local types of an "apex branch", and Makhnev's forcing reads "not every transversal edge lies in a prism".

Compared state of the routes (no rank excluded by any): (i) rank-free cores: 373 -> 310 -> 174 certified, then no death
at small depth in these two pilots; (ii) grid / no grid: factor 0.79 missing at rank 37, restricted cap not computed;
(iii) stars at rank 37: certificates per ball, no uniform lemma. Neither campaign is continued on my side.

### 17.70 Reserve route "no grid": one quick variant tested, negative (22:38 UTC, 08/10)

Codex declined my proposal to read the 174 core types on the four old balls (absence on four excluded examples covers
nothing): accepted. It found integer mask multiplicities for 15 of the 174 (no gain from integrality) and is piloting the
coexistence of masks; not duplicated here.
Meanwhile, one check on the reserve route of 17.68 (new fact used: Codex's note 195 gives a much lower certified cap,
23 150 per non-grid twin pair, for the collection WITHOUT the 9-set indicators (9,0), against 31 976 with them).
`lp_family.py` with a new option "n" (drop the shapes (9,0), (0,9)), floating:
* with (9,0), rho = 0: break-even 25 201 (reproduced; R = 32.5 million);
* without (9,0), rho = 0 or free: R = 23.55 million and max(ceiling - floor) = +0.054 million with NO collision at all.
So the 9-set indicators carry about 9 million representatives and cannot be dropped: without them the floor does not
reach the ceiling even before any collision is paid. NEGATIVE; the smaller cap is of no use.
What the grid-free branch would need, for the record: the cap of the collection WITH (9,0) for a non-grid twin pair,
31 976, brought below 25 201 in a grid-free graph, a reduction of 21 %. Codex's refinements of the grid-pair cap moved it
from 29 204 to 27 828 (5 %), and its certified range for a grid pair is [16 496, 27 828] (note 198); the non-grid cap was
never refined. By note 195 the collisions of the (9,0) channel use supports containing a prism, not a grid, so
grid-freeness does not obviously reduce them. Also unpaid in any case: the collisions of masses 7 to 9.

### 17.71 Crossing the 174 cores with the order-10 census: exact, valid, no effect on the counting (22:54 UTC, 08/10)

Codex (its note 223): integer mask multiplicities and the coexistence of masks exclude no further core; it proposed a
double count over ALL motifs S of one graph. Done here in the census, with exact forms.
* `core_double_count.py`: N_2 = 4158 - 3 x_1 (x_1 = number of prisms) and
  T = sum over S of e(D(S)) = 3 x_1 + 6 x_2 - 2 x_3 + 2 x_4 + x_5 + x_6 (six census parameters of orders 6 to 8).
  Ranges over the census polytope (floating): T in [0, 18 649], N_2 in [1599, 4158], T - 4 N_2 in [-16 632, 2017].
  The census forces no mean value of e(D); the cut T <= 4 N_2 implied by the 174 cores removes only a corner.
* `core_forbidden_types.py`: among the sub-configurations "S + j doubles", every pattern with j <= 3 (15 and 43 types)
  still occurs in a surviving core; for j = 4 two of the 130 do not. They are two 4-regular graphs on 10 vertices
  (20 edges), which are census parameters: **x_58 = x_59 = 0 in every srg(99,14,1,2)**, given Codex's certificates for
  the 63 + 136 excluded cores. A small rank-free lemma.
* `core_type_equations.py`: the complete coupling. Unknowns lambda_c >= 0 (number of motifs of core type c, c = 1..174)
  and, for each of the 192 types X = S + j doubles (orders 6 to 10), the exact equation
  m(X) N(X) = sum_c lambda_c cnt_c(X). Self-check passed: for j = 1 the identity m(X) N(X) = cnt N_2 holds as forms.
* Injected into the rank-37 counting LP (`lp_family.py`, new environment options ZERO_PARAMS and EXTRA_ROWS, floating):
  break-even 13 900 -> 13 830 at the grid-rich corner (P = 756, rho = 126, tau = 1403 still attained) and
  25 201 -> 25 214 with no grid. NO EFFECT: the distribution of the 174 core types is compatible with the corner where
  the counting fails. An obstruction of this kind would need motifs with at least five doubles (order >= 11).

Laptop session (22:43 UTC on 08/10; computer-assisted, audited by nobody; repo conway99-c2-aws, folder
c1_rank37_girth5_lines/, commit 15a3cfe3f): at rank 37, a line whose graph G(T) has neither triangle nor 4-cycle is
CONNECTED; so the residual case "(6,6) everywhere" of 17.53 does not occur. Method: for a disconnected line without
torsion the 36 near vectors span a non-degenerate hyperplane of the 36-dimensional space of A - 3I + 3J modulo 7, each
far vertex carries one extra scalar, and the star conditions with that scalar are searched exhaustively (192 + 96 + 288
searches, and 33 784 128 matrices in the torsion case (3,3)); no star. Relayed to Codex with its request for an audit;
I offered to re-implement one witness ball. Not checked here yet. Rank 37 is not excluded by it.

### 17.72 The laptop session's result on girth-5 lines: Codex's audit and my independent witness (23:18 UTC, 08/10)

* **Codex's audit (its note 224, commit e7bba78 of its branch).** Points 1 to 7 of the laptop session's note re-derived
  with no defect found (rank 36 of A - 3I + 3J, non-degenerate quotient, scalar residue, torsion cases 00, 01, 11, 33);
  the 288 normal forms and the 7 types reproduced independently; the end of case (3,3) re-implemented (25 588 -> 44 at
  vertex 1, 44 -> 0 at vertex 6, identical lists). Not replayed by Codex: the initial sweep of GL_3(F_7) at vertex 0 and
  the 576 star searches (engines read, logs checked for coverage and absence of timeouts).
* **My independent witness (`lap_witness_check.py`; scope: this one ball).** Ball type 0 + type 0, identity order of the
  layers, u = 0, c0 = 1. Only the data convention of the component key is shared; the quadratic data are computed
  differently (W = (M0 + z0 z0^T)^(-1) with M0 = 3J - H, g(n, n') = (3.1 + n)^T W (3.1 + n'), instead of the Green
  functions of the two components) and the search is my own (labels by the same-layer point, forward checking, exact-
  cover propagation). Results: 10 584 candidate shadows and 11 232 with a scalar, as announced; the row K e_u agrees;
  **no star**: the 792 root branches are exhausted, branches 0 to 392 in a first run (529 000 nodes, stopped by the
  time limit inside branch 393; console record only) and branches 393 to 791 in a second run (511 676 nodes,
  `lap_witness_check_part2.json`); a later re-run archived branches 0 to 367 (`lap_witness_check_part1.json`). Positive
  control: with the conditions modulo 7 switched off a star is found in 3024 nodes, with cover exactly K e_u.
  The whole check needed two runs of about four minutes each.
* Status of the statement "at rank 37 a line whose graph has girth >= 5 is connected": derivation audited by Codex, one
  star search reproduced independently here, the other searches read but not replayed. Used from now on as a working
  result with that status.
* Priority reported by Codex as an explicit instruction of the user to it (not received directly here): exploration,
  new lemmas and reduction theorems first; no default double verification. The witness check above was already
  complete when this arrived; nothing further is replayed.

Consequence worth aiming at (mine, elementary): if a line T lies in a grid, the six other vertices of the grid form a
prism, which is a cubic graph, hence a whole connected component of G(T): G(T) is disconnected. So a theorem "at rank 37
every line has a connected graph" would give **no grid at all at rank 37**. The laptop session's method decides any
finite family of disconnected profiles; the profiles needed are k prisms plus a rest of 36 - 6k vertices, k = 1, 2, 3,
4, 6 (k = 5 forces k = 6). For a vertex x of a prism component the star is 5 K_2 with no apex, and K e_x is 1 on the ten
other points of its layer outside the prism and 2 on the twenty points of the other layers outside it.

### 17.73 Two reduction targets: prisms are forced by the counting at rank 37; the six-grid line as an integer matrix (23:39 UTC, 08/10)

**A. The counting at rank 37 when prisms are few** (question of the laptop session: at P = 0 there is no twin pair, so
do the uncounted channels need prisms?).
* Classification read in Codex's notes 181, 183, 185 (statuses as written there): a proper difference of two
  representatives of norm 8 has mass at least 6; mass 6 = two twin prisms; mass 7 = two copies of the 7-vertex graph D
  with the same projection (D has no prism; their number H is free, 3P + 2H <= 4158); mass 8 = weighted windmills (3465
  in every graph) and the cubic or nearly cubic induced graphs on 8 vertices (seven types, only the grid minus a vertex
  contains a prism); mass 9 and changes of sum are not classified for the whole collection (note 195 says so).
  So NOT every channel needs a prism, and no certified bound of the channels outside C_6 exists for the collection.
* Margins (`lp_family.py` with the new options ZERO_PARAMS and PCAP; floating; Codex's collection, both signs):

| condition | number of representatives R | theta ceiling | what the collisions must reach to save rank 37 |
|---|---|---|---|
| P = 0 | 32.5 million | 15.8 million | 16.75 million colliding pairs (k = 1), 17.7 million (k = 2) |
| P <= 100 | 32.5 million | 15.9 million | 87 431 per twin pair (certified cap 31 976) |
| P <= 200 | 32.5 million | 15.9 million | 45 402 per twin pair; slack 5.2 million for the other channels |
| P <= 300 | 32.5 million | 15.9 million | 30 697 per twin pair: no longer enough |

  **Target statement: at rank 37 the graph has more than 200 prisms** (in particular the world P = S = 0 of Codex's note
  126 is empty at rank 37). What is missing is only a certified upper bound of the collisions of masses 7, 8, 9 and of
  the changes of sum for the whole collection, as a linear form in census parameters; expected to be far below the slack
  (rare objects times a few hundred pairs), NOT proved. Asked to Codex. Floating LP; nothing is excluded yet.

**B. A line in six grids** (the object of 17.46; the laptop session's statement of 23:24 UTC: at rank 37 the 60 far
vertices carry isotropic vectors of a non-degenerate 5-space over F_7 with an explicit Gram matrix).
* Real Green function of a prism (hand): same vertex 47/180, mates -7/180, same parallel line -1/180, other side and other
  layer -19/180; modulo 7 this is the laptop session's table 1, 0, 4, 6.
* For two far vertices f, g let a be their adjacency and e, m, r, o the numbers of the six coordinates where their names
  are the same vertex / mates / in the same row / other. Then the integer matrix
        q_ff = 91,     q_fg = 43 - 60 a - 22 e - 4 m - 6 r
  is 420 times the projector onto the (-4)-eigenvectors supported on the far set (rank 13; trace check tr(H^+ K) = 94).
* **Lemma (hand): q^2 = 420 q follows identically from the axioms of 17.46.** Diagonal: with the second moments forced
  by the axioms (sums of A^2, E^2, C^2, R^2, AE, AC, AR, EC, ER, CR equal to 8, 78, 300, 594, 6, 12, 18, 132, 174, 324
  per vertex) one gets sum s^2 = 146 856 = 91 x 329 + 116 917 exactly. Off the diagonal: the ten bilinear sums over a
  third vertex are affine in (a, e, m, r, o), the terms in a cancel, and the equation reduces to e + m + r + o = 6.
  So the real identity carries no information on this object (the axioms of 17.46 already are the SRG equations).
* The information is modular. Modulo 7: q_fg = 1 + 3a - e + 3m + r, of rank r - 32 - 2 v_7(t) (5 at rank 37), in
  agreement with the laptop session's determinant det(L_far) t^2 = 324 x 5^12 x 7^(r-32) (17.46; unaudited). The same
  formula gives conditions at EVERY rank at the other primes: modulo 3, q = J - C depends on the columns only and must
  have rank 4 - 2 v_3(t); modulo 5, q_fg = 3 - 2e + m - r depends on the names only (not on the adjacency) and must have
  rank 12 - 2 v_5(t). Test done: the canonical column solution (60 ordered Petersen stars) has rank_3(J - C) = 4: it
  passes, which also confirms the formulas. The test modulo 5 needs the rows (signs) and is the next thing to look at.

Addendum to 17.73 B (23:43 UTC, hand): the conditions modulo 3 and modulo 5 on a six-grid line are AUTOMATIC; do not test them.
* Modulo 3. Let c(f) in F_3^6 be the column vector of the name of f. For x, y in F_3, [x = y] = 1 - (x - y)^2, so the
  number C(f, g) of column agreements is -|c(f) - c(g)|^2 modulo 3; every name uses each column twice, so |c(f)|^2 = 10
  = 1, and q = J - C = c(f).c(g) modulo 3: the Gram matrix of the column vectors. They lie in the hyperplane sum = 0,
  which contains the all-ones vector as a radical direction, so the rank is at most 4 for ANY column data. (This
  explains the 3^4 of the determinant formula; the canonical solution reaches 4.)
* Modulo 5. With s_k(f) = +-1 the row sign and z_k(f) = s_k(f) e_(c_k(f)) in F_5^3, one finds
  q_fg = sum over k of s_k(f) s_k(g) (2 - [same column at k]) = Z_f^T B Z_g with B the direct sum of six blocks 2J_3 - I_3,
  each of rank 2 over F_5 (eigenvalue 5 on the constants). So the rank is at most 12 for ANY names. (This explains 5^12.)
So only the condition modulo 7 carries information on this object, and it involves the far adjacency:
A_B - 3I = J + M' + sigma sigma^T + U U^T + 2 Z Z^T modulo 7 (sigma the sign vectors, U the column indicators, Z as above,
M' the Gram of rank r - 32 of the isotropic vectors). A tempting shortcut is FALSE and is recorded so that it is not
retried: M' vanishes on the reduction of L_far + K_far, not on the whole of ker N modulo 7 (there is glue of dimension
rank M'), so the isotropic vectors are not a linear function of the shadows.

### 17.74 CORRECTION of the expectation in 17.73 A: the collision channels without prisms are not bounded finely enough (23:55 UTC, 08/10)

In 17.73 A I wrote that the channels surviving at P = 0 were "expected to be far below the slack". That had no basis.
Codex has now given a first rigorous and complete linear bound for the sub-collection without change of sum (sums 0,
+3, -3: (1,1), (2,2), (3,3), (4,4) and both signs of (3,0), (4,1), (5,2), (6,3) with e(W) <= 8), conditional on P = 0:
* mass 7: at most 5402 per copy of D;  mass 8: 1872, 1840, 3088 per cubic support of 12 edges, 3512, 3616, 4448 per
  support of 13 edges, and 2592 per windmill, i.e. 8.98 million for the 3465 windmills alone;
* mass 9 ((6,3) against (6,3) only; Codex's lemma: such a difference is binary, two disjoint 9-sets of minimum degree
  3): 39 types with coefficients 58 to 1301.
Numbers computed here (floating LPs; `lp_family.py` option "z", `census_param_max.py`, `collision_form_lp.py`):

| quantity at P = 0 | value |
|---|---|
| margin of the sub-collection, k = 1 (k = 2 and 3 do not exclude) | 3.84 million colliding pairs |
| same without the (6,3) family (supports <= 8) | no exclusion: R = 7.5 million < ceiling 15.9 million |
| supports <= 9 without (9,0) | 8.95 million (brings back changes of sum) |
| complete collection | 16.75 million |
| largest number of copies of D | 1867 |
| largest counts of the six prism-free types of order 8 with minimum degree 3 | 5122, 4158, 4158, 2821, 29 323, 16 846 |
| Codex's mass-9 bound maximised with orders 6 to 9 / 6 to 10 | 193.5 million (its own figure, reproduced) / 149.2 million |

The mass-9 bound is 40 times the budget and no single type dominates (the six largest terms are 17.9, 13.2, 11.2, 11.0,
9.4, 8.5 million): what is too large is the shape "weight squared per support", which charges every support as if it
had partners. The true sizes are unknown. **So the counting does NOT give "rank 37 implies P > 0" at present, and it is
not established that it will.** The margins of 17.73 A are correct; what has to be paid is not bounded finely enough.
With the sub-collection at P <= 200 the break-even is 8244 per twin pair, below the caps of the mass-6 channels.
A collision of mass 9 is a pair (U, V) of disjoint 9-sets of minimum degree 3 joined by exactly 2e(U) - 27 edges, every
outside vertex seeing as many points of U as of V; counting such pairs is not within a census of order 10.

Permission received from the user (direct, about 23:48 UTC): local runs on the lab PC may use up to 80% of the processor
and of the memory, falling back to low performance when Discord, FiveM, Valorant or similar opens. `guarded_pool.py` runs
a list of commands with at most 12 workers and a single one while such a program is running (resumable log). Offered to
the laptop session for a share of its sweeps; nothing launched yet.

### 17.75 Lemma: two weighted windmills never have the same projection; the far set of a support (00:01 and 00:30 UTC, 09/10)

Hand proofs, valid in every srg(99,14,1,2), with no hypothesis on P or on the rank. Sent to Codex (message 268); Codex
used the lemma in its note 227 (new mass-8 form without constant). Not audited by a third party.

A weighted windmill is u = 2 e_v + 1_L, L the six points of three lines through v ("leaves").

**Lemma (windmills).** If W_1, W_2 are disjoint weighted windmills, u_1 - u_2 is not an eigenvector of eigenvalue 3.
Proof. Suppose A(u_1 - u_2) = 3(u_1 - u_2).
1. At v_1 the neighbours sum to 6 minus the weight seen in W_2, and this must be 6: v_1 has no neighbour in W_2. At a
   leaf a of W_1: 2 + 1 minus the weight seen in W_2 must be 3. So W_1 and W_2 are anticomplete; v_1, v_2 are not adjacent.
2. For x outside both supports, s_1(x) = s_2(x), where s_i(x) = 2 [x ~ v_i] + number of leaves of W_i adjacent to x.
3. v_1, v_2 have exactly two common neighbours c, c'. Neither is a leaf (a leaf of W_1 has no neighbour in W_2), and
   c, c' are not adjacent (the adjacent pair c, c' would have the two common neighbours v_1, v_2).
4. Let cbar be the third point of the line {v_1, c, cbar}. It is not a leaf of W_1 (its line contains c), it is not in
   W_2 (it is adjacent to v_1), and it is not adjacent to v_2 (it would be c or c'; it is not c, and it is adjacent to c
   while c' is not).
5. s_1(cbar) = 2: it sees v_1 and no leaf of W_1 (two neighbours of v_1 on different lines are not adjacent).
6. cbar and v_2 are not adjacent, so they have exactly two common neighbours, and c is one of them. The leaves of W_2
   adjacent to cbar are common neighbours too. Hence s_2(cbar) <= 1 < 2 = s_1(cbar), against 2.  QED.
Consequence: a class of supports of mass 8 with the same projection contains at most one windmill; the only relations
involving a windmill are windmill against cubic support (not excluded; Codex's note 228 reduces them to 359 rooted
types with forced cells).

**Far set of a support.** For an induced cubic 8-set U let n_k be the number of outside vertices with k neighbours in U
and Z(U) the set of outside vertices with none. Counting edges out of U and common neighbours of pairs of U
(sum k n_k = 88, sum C(k,2) n_k = 20 for every cubic type) gives
        |Z(U)| = 23 - sum over k >= 3 of C(k-1, 2) n_k <= 23.
For a weighted windmill W with centre v, every vertex y not adjacent to v has exactly two neighbours among the 14
neighbours of v, and Z(W) (no neighbour in W) is the set of the y whose two neighbours lie on the four other lines:
|Z(W)| = 24 exactly, in bijection with the 24 pairs of points on two different ones of these four lines.
If 1_U - 1_V (or 1_U - u_W) is an eigenvector of eigenvalue 3 then U and V are anticomplete and every outside vertex
sees as much of U as of V; so V lies in Z(U) and no vertex of Z(U) outside V has a neighbour in V:
**every other member of the class of U is a union of connected components of the graph induced on Z(U)** (one component,
since the three cubic types and the windmill are connected), and two of them are disjoint. Hence a class without
windmill has at most 3 members (8 + 8 <= 23 < 24) and a class with a windmill at most 3 cubic members (Codex's bound
was 4 and 3, from "at least 61 common outside vertices"); with three cubic members and a windmill all the inequalities
are equalities (n_k = 0 for k >= 3, Z(W) is exactly the union of the three). No numerical gain on Codex's coefficients:
their tight cases are those with a windmill.

**Night run for the laptop session (user's direct allowance of 80% of the machine).** Profile (4,8) at P = 0 of its
sweep "rank 37, P = 0: disconnected lines": 245 877 balls in 12 000 parts, its code at commit 6a334970a of
conway99-c2-aws (read before running), in `work/c1_lap_sweep48_2026-10-09/`. Component types regenerated here
(81 959, same counts and hash as the laptop's); the first three balls reproduce its expected lines exactly. Started
23:59 UTC with 12 workers, stopped after 37 parts because the total load averaged 79% with peaks at 84%, restarted at
00:04 UTC with 11 workers (load 70 to 76%, memory 44%); `guarded_pool.py` drops to one worker while Discord, FiveM,
Valorant or similar runs. Rate 20 parts per minute: about 10 hours. Nothing but dead balls and TORSION lines so far
(777 balls at the restart). The result is the laptop session's to interpret; I only return the log and the counts.

### 17.76 Coupled LP with Codex's collision bounds at P = 0: a charge per support is 20 to 35 times too large (00:30 UTC, 09/10)

Question (Codex, 00:07 UTC): put its new mass-8 form (no constant, thanks to the windmill lemma) into the rank-37 LP
together with the mass-7 and mass-9 bounds, instead of maximising each form separately. Done: `collision_forms_build.py`
translates the three bounds into exact forms of my census parameters (H = parameter 2; six types of order 8; 39 types
of order 9), `lp_family.py` with COLLISION_FORM subtracts the form inside the LP (classes >= R - C(x), k = 1) and
reports the scale s at which max(ceiling - R + s C) crosses zero. Sub-collection "sums 0, +3, -3" (scenario m4s9k1z,
12 forms), P = 0, floating LP. Reference without collisions reproduced: -3.837 million.

| collision form | max (ceiling - R + C) | value of the form there | the bound would have to be divided by |
|---|---|---|---|
| C7 = 5402 H | +5.54 million | 10.08 million (H = 1865) | 2.2 |
| C8, new form | +115.9 million | 122.5 million | 23.4 |
| C9 | about +111 million | 118.4 million | 22.3 |
| C7 + C8 + C9 | +177.7 million | 185.2 million (7.0 + 108.3 + 69.9) | 34.6 |

At the coupled optimum of the total the mass-8 part is carried by ONE type: the cubic graph with two triangles
(Codex code 5691760: triangles abc, def, edge cf, paths a-x-d, b-y-e, edge xy), 27 935 copies at 2840 each, i.e. 79
of the 108 million; then the cubic type 5683824 (14 702 copies, 12 million) and the 13-edge type 128354469 (10 million).
So removing the constant 8.98 million changes nothing in the conclusion, mass 8 is as much a lock as mass 9, and mass 7
alone already eats the margin.

Reading. This is the wall already met on 08/10 (17.20: "a penalty per support of this size is not affordable; what is
missing is a bound on the number of twin PAIRS"), now measured with Codex's actual coefficients. The census allows
about 28 000 supports of one type and the budget is 3.84 million colliding pairs of representatives, so any bound of
the form "coefficient times number of supports" needs a coefficient near 100 where the cost of ONE twin pair is already
of the order of 1500. No refinement of the coefficients can bridge that; only a bound on the number of pairs of
supports with the same projection can, and neither the census (a pair has 16 to 18 vertices) nor the 3-side theta LP
(17.20: it allows 10^12 integer 3-eigenvectors of norm 16) gives one. Checked before going further that the
overlattice idea (a nearly unimodular envelope at rank 37) is already recorded as closed (end of 17.64, and 17.67).
The target "rank 37 implies P > 0" by counting stays open and blocked at this precise point.

### 17.77 Pairs of cubic supports with the same projection are exactly the anticomplete pairs; a census test of it, negative (00:51 UTC, 09/10)

Codex's observation (bridge, 00:40 UTC): if two induced cubic 8-sets U, V are anticomplete then 1_U - 1_V is
automatically an eigenvector of eigenvalue 3. Checked by hand, two readings:
* Cauchy-Schwarz. With 7E = 3I - A + J/9: 7 |E 1_U|^2 = 64/9 for every induced cubic 8-set, and 7 <E 1_U, E 1_V> = 64/9
  when U, V are anticomplete, so E 1_U = E 1_V. In general, for disjoint U, V of the same size m,
  7 |E(1_U - 1_V)|^2 = 6m - 2 (e(U) + e(V) - e(U,V)) >= 0: the pairs with the same projection are the pairs reaching
  e(U) + e(V) - e(U,V) = 3m.
* Interlacing. U + G[Z(U)] (disjoint union, no edge between) is an induced subgraph, U carries the eigenvalue 3 and the
  second eigenvalue of the graph is 3: every eigenvalue of the graph induced on Z(U) is <= 3, and the partners of U
  (with any positive weights: cubic sets, windmill with weights (2, 1^6)) are exactly the components of G[Z(U)] of
  spectral radius 3. So "U has a partner" is the local statement det(3I - A_{Z(U)}) = 0 on at most 23 points
  (24 for a windmill, at most 30 for a prism), and e(Z(U)) <= 34.
Consequences already noted by Codex: a cubic set anticomplete to a cubic 8-set has a size multiple of 8 (the >= 48
outside vertices with one neighbour in U); in particular no prism is anticomplete to a cubic 8-set.

Test (`far_edges_lp.py`, floating LP, P = 0, census of order 10). New fact used: a partner puts 12 edges inside Z(U),
so the number of ordered pairs (U, partner) is at most N(U + K_2) / 12, and U + K_2 is an induced type of order 10.
Result, negative: N(U + K_2) >= 12 N(U) on the whole polytope for the three cubic types; the mean number of edges in
Z(U) at the extreme points is 22.7 to 35.7 (cube, at most 2822 copies), 32.3 to 33.3 (type 5683824, at most 16 846),
23.3 to 28.2 (two-triangle type 5691760, at most 29 323). The census does not see whether Z(U) has a cubic component.
By-products: for the cube N(U + K_1) = 23 N(U) identically (|Z(U)| = 23 always); the cut e(Z(U)) <= 34 is valid and
slightly inside the polytope (35.7 allowed for the cube), with no effect on the counting.

**Laptop session, torsion follow-up of the (4,8) profile.** Its commit 0c6057273 (`sweep48t.py`, `fastg4.c`,
`tors_m4.json`; read before running; kept in its own folder `work/c1_lap_sweep48t_2026-10-09/` so that the running
sweep keeps its code). Torsion ranks of the 81 959 large types: 68 372 / 12 811 / 719 / 48 / 9 for ranks 0 to 4.
Checks here: its two expected lines reproduced (rank 1: 3 sub-cases dead, 4.0 s; rank 2: 17 dead, 17.9 s); its list of
torsion types agrees without exception with what `sweep48.py` marks TORSION on the 19 341 balls swept so far (3 248
marked, none missing either way). Queued (a background wait loop starts it when `pool_48.log` reaches 12 000 lines):
rank 1 in 2000 parts, rank 2 in 400, rank 3 in 144, 11 workers under `guarded_pool.py`; rank 4 (27 balls) is left to
the laptop session. Estimate 6 to 7 hours after the main sweep.

Addendum to 17.77 (01:03 UTC): the shortest form of the same fact, and the laptop session's instance of it.
If z is supported on a vertex set S and is an eigenvector of the induced graph on S for the eigenvalue 3, then
A z = 3 z + e with e supported outside S, and A^2 = 12 I - A + 2 J gives |A z|^2 = 9 |z|^2 + 2 (sum z)^2, hence
        |e|^2 = 2 (sum z)^2.
A zero-sum eigenvector of an induced subgraph for the eigenvalue 3 is therefore a global eigenvector; for an induced
cubic graph on s vertices the outside degrees satisfy sum d = 11 s, sum d^2 = 2 s^2 (so s <= 38; for the 36 near points
of a line 3 x 144 + 60 x 36 = 2592). The laptop session's fact (its message of 01:03 UTC): for a line whose near graph
has components C_i with m_i lines per layer, m_j 1_{C_i} - m_i 1_{C_j} is an integer 3-eigenvector and every shadow has
exactly m_i points in C_i, at every rank and with or without torsion; this is the case S = C_i + C_j. So a
disconnected line is a family of integer 3-eigenvectors of small norm (mass 12 for (4,4,4), 18 for (6,6),
2 1_{C_1} - 1_{C_2} for (4,8), twin prisms for components of 6 points).
Laptop session, reported state: profile (4,4,4) closed, 275 multisets of three ordered types, all dead (its commit
784c31c98; computer-assisted, not audited); (6,6) at P = 0 in progress, all dead so far; rank 4 of the (4,8) torsion
balls running there. Main (4,8) sweep here at 01:02 UTC: 25 221 balls, 21 018 dead, 4 203 TORSION, 0 other.

### 17.78 The (4,8) sweep reduced to one ball per isomorphism class; independent check; new division of the torsion ranks (01:33 UTC, 09/10)

Laptop session's reduction (its message of 01:27 UTC, commit cb4ff9ec1 of conway99-c2-aws: `actc.c`, `reps48.py`,
`reps48.txt`). A ball of the profile (4,8) is a pair (s, b), s one of the three small types kept (0, 1, 3), b one of
the 81 959 large ordered types; re-reading the three layers in another order sends (s, b) to (g.s, g.b), so for a fixed
s the large types matter only up to the stabiliser of s (order 6 for s = 0, order 2 for s = 1, 3): 14 424 + 41 736 +
41 736 = 97 896 balls instead of 245 877. "No star at some near vertex" kills the isomorphism class, whatever the test
vertex, so the sweep of the representatives is enough.
Checks here before using it:
* its table rebuilt (`actc.exe`, `reps48.py`): same counts, same hashes (act48.txt 5e8b7f89a6034d0c, reps48.txt
  6f2968daa1c9deb7), file identical to the laptop's;
* independently of its action code (`iso_check_reps48.py`: the two balls are built by the function the sweep itself
  uses and compared by networkx as graphs on 36 vertices with a partition into three layers, the six permutations of
  the layers being tried): random sample of 400 non-representative balls, all isomorphic to their representative;
  negative control, 400 pairs of representatives of different classes, none isomorphic; every ball in exactly one
  class, sizes adding up to 245 877. The complete version (all 147 981 non-representative balls) is queued for when
  the processor is free; until it has run, the reduction is checked on a sample only;
* on the balls already swept in full: 5 076 non-representative balls have their representative swept too, all with
  the same verdict (dead or TORSION), none different. (I first wrote "20 000" to the laptop session without having
  computed it, and corrected it in the next message.)
Switch at 01:30 UTC: the 1763 parts finished before are kept (swept in full), the others run with the filter; at 01:31
UTC 17 448 of the 97 896 representatives were logged (14 497 dead, 2 951 TORSION, 0 other). About 57 parts a minute
at 11 workers (load measured with a single sampler: mean 71%, maximum 78%): end around 04:30 UTC.
Torsion ranks, new division proposed by the laptop session and accepted: rank 1 here on the representatives (15 462
balls), ranks 2, 3, 4 on the laptop with its pair filter (`sweep48tp.py`: for a space B of balanced torsion vectors,
each pair of near points with K_ab = c > 0 needs at least c admissible B-balanced 6-sets through it; it reports that
this removes 95 to 99.6% of the subspaces of dimension 2 and all those of dimension >= 3 on its samples). As a
cross-check of that filter, 65 representative balls of rank 2 are queued here WITHOUT it (parts 0 to 3 of 64).
Laptop session, reported: (6,6) at P = 0, the 2887 torsion-free pairs all dead; torsion pairs running.

### 17.79 A race that can fake a "dead" ball (found by the laptop session on its side); checked here: no trace (03:25 UTC, 09/10)

Reported by the laptop session (03:23 UTC): it cancelled three of its runs by killing the workers before the parent;
orphan workers survived and kept writing instance files under the names the restarted run uses. A solver that opens
a file while another process rewrites it reads zeros and prints "cands 0 ... solutions 0 timeout 0", which a driver
counts as dead. It withdrew its sentence "three balls of T = 4 done, all DEAD", restarted T = 4 and T = 3 from zero,
and put the process id in the names of the temporary files (commit 8f6c57732 of `conway99-c2-aws`).

Checked on the lab PC, 03:24 UTC:
* the stop of 01:30 was `taskkill /PID 21596 /T /F` (the pool and its whole tree), followed by a count before the
  restart: fast.exe 0, python processes running sweep48.py 0 (transcript, 01:30:08 UTC);
* now: 23 python processes = 1 pool + 11 drivers + 11 workers, none whose parent no longer exists, the oldest
  started at 01:30:23 UTC;
* scan of every per-part log (`../c1_lap_sweep48_2026-10-09/scan_race_48.py`): 83 324 lines, 83 324 distinct balls,
  none logged twice; on the torsion-free lines the smallest "cands" is 5184 and the smallest node count 25 690; no
  line with cands < 2000 or nodes < 1000; no line that is neither dead nor TORSION.
So the signature of the race is absent from the balls logged before and after the switch.

Two remarks sent to the laptop session: its fix does not cover `run_both` in `fastlib.py` (line 209), the function
`sweep48.py` calls; and the torsion logs carry totals per ball only, so there the guard is the absence of a second
run, not a scan. Its fixed `sweep48t.py` is installed here for the torsion run (not started yet; the known line
"48t 0 14 | t=1 sub-cases 3 dead 3 ... DEAD" is reproduced). The main sweep is not touched while it runs.
Rate since the restart: about 53 parts a minute, so the main sweep ends about 04:45 UTC (not 04:30).

### 17.80 NOT NEW (it is Codex's L23 of 25/09): the discriminant of V and the number of spanning trees modulo 7; what remains mine is corollary B (03:44 UTC, 09/10)

**CORRECTION (03:49 UTC, 09/10).** I presented the lemma and corollary A below as new, to Codex, to the laptop session and
in one line to the user. They are not: they are exactly **L23 of Codex's note 102** (`notes/102_FORME_BETA_SIGNE.md`,
25/09, sections 0, 1.4, 4, 5), proved there with the form beta, with a control on 300 configurations, and with the
same consequence (k = 22, that is r = 37, forces tau(G(L)) in {0, 3, 5, 6} mod 7 for every line). Its section 8 also
has the Green formulation at rank 37 and the remark that the first moment is automatic. My search of the logs before
writing was done with English key words on notes written in French; the file name appeared in a second listing and I
did not open it. Codex pointed it out at once (its answer to my message 273).
What the text below adds to note 102, and nothing more: (i) a second derivation of the sign by the oddity formula on
Z^99 cap E_{-4}, which agrees; (ii) the exact value det(3J - H) = -3888 tau; (iii) **corollary B** (the class of the
residue c0 is forced in the disconnected cases; Codex records it as a consequence, not as a correction of the
sweeps); (iv) the rule with torsion and the automatic second and third moments, in the addendum at the end.
The sentence 'a filter that removes about half of the generic connected line graphs' is therefore an old filter
(Codex is putting it into its note 230), not a gain of tonight.


New fact used: the genus of the lattice of integer eigenvectors (oddity formula) fixes not only the type of Q_r
(section 7) but also the square class of the OTHER Jordan block, and that block is the space V in which the laptop
session's star searches live. Hand derivation, not audited.

**Lemma.** Let r = rank_7(A - 3I), Q = A - 3I + 3J and V = F_7^99 / ker Q with the form Q (dimension r - 1, non-
degenerate; the space of the laptop session's note, point 1). Then disc(V) is a NON-square modulo 7 when r = 37 or
41, and a square when r = 39 or 43.

Proof. Let L = Z^99 cap E_{-4} (rank 44, even because its vectors have sum zero, positive definite), L* = E_{-4} Z^99.
* 63 E_{-4} = 9 (3I - A) + J is an integer matrix, so 63 L* is inside L: the discriminant group is killed by 63.
  Modulo 7, 63 E_{-4} = -2 Q, so the 7-part of L*/L is elementary of rank rank_7(Q) = r - 1.
* The orthogonal complement of L in Z^99 is, 3-adically, (Z^99 cap E_3) + Z.1 with the first summand unimodular at 3
  (77 E_3 is an integer matrix) and 1.1 = 99: the 3-part of the discriminant has order 9. The 2-part is trivial.
  Hence det L = 9 . 7^(r-1) and, over Z_7, L = U + 7 U' with U, U' unimodular of ranks 45 - r and r - 1.
* Oddity formula (Conway and Sloane, chapter 15): signature + sum of the p-excesses = oddity modulo 8. Here the
  signature is 44, the oddity is 0 (even, odd determinant), the 3-excess is 8 = 0, and the 7-excess is 6 (r - 1) + 4k
  with k = 1 exactly when det U' is a non-residue. So 44 + 6 (r - 1) + 4k = 0 modulo 8: r is odd, and k = 1 exactly
  when r = 1 modulo 4. (Convention checked on the root lattice A_6: rank 6, determinant 7, the formula gives the
  block 7^(-1), and indeed its discriminant form is generated by a vector of norm 6/7 with 6 a non-residue.)
  Since det L / 7^(r-1) = 9 is a square, det U and det U' are in the same class: for r = 37, 39, 41, 43 this gives
  back "Q_r is of minus type" (section 7), which is a second check of the convention.
* V is the block U' : on Z_7^99, Q = -7 E_{-4} + 308 E_14; the image of Z_7^99 in the quotient by the kernel is
  L* + Z_7.1, on which the form is -7 x.y on L* = U + (1/7) U' and a multiple of 7 on 1. Modulo 7 only (1/7) U'
  survives, with the form -u' (u' the unimodular form of U'). So V = (U'/7U', -u') and disc(V) = det u' because the
  dimension r - 1 is even. End of proof.

**Corollary A (rank 37, connected lines).** If G(T) is connected and 7 does not divide its number of spanning trees
tau, then tau is a quadratic NON-residue modulo 7: tau = 3, 5 or 6 (mod 7). So at rank 37 every connected line has
tau(G(T)) in {0, 3, 5, 6} modulo 7.
Proof: the 36 near vectors are then a basis of V with Gram matrix M0 = 3J - H, and det M0 = 108 . (-1)^35 . 36 tau =
-3888 tau = 4 tau modulo 7 (eigenvalue 108 on the constants, -mu on the other eigenvectors of H, product of the
non-zero mu equal to 36 tau). 4 is a square, so tau is in the class of disc(V).

**Corollary B (rank 37, two components without torsion).** With the laptop session's model V = span{p_w} + <n>,
<n, n> = c0: the span has discriminant 3 tau1 tau2 (sum-zero vectors of each component: (-1)^(s-1) s^2 tau; the
constants of the two components: a line of norm 3 s1^2 after removing the radical z0), hence 3 tau1 tau2 c0 is a
non-square and **c0 = tau1 tau2 modulo squares**: only one of the two classes c0 = 1, 3 searched by the laptop
session can occur on a given ball. (Its sweeps try both, which is a superset: nothing to change in a running sweep.)

**Corollary C (other ranks).** For a connected line without torsion at rank r, V = (near span) + R with R of
dimension r - 37 and disc(R) = disc(V) tau modulo squares; at rank 39 the plane R is hyperbolic exactly when tau is
a non-residue. No exclusion follows.

Formula check on graphs only (`disc_tau_check.py`, seed 20261009, 3 seconds): for 200 random connected cubic
layered graphs, det(3J - H) = -3888 tau exactly in all (tau modulo 7: zero 24, residue 97, non-residue 79); for 200
torsion-free balls of the (4,8) profile, the radical of M0 has dimension 1 and the quotient has discriminant
3 tau1 tau2 in all. This checks the two determinant formulas, not the lemma (no graph exists to test it on).

What it is worth: a filter with no search that removes about half of the generic connected line graphs at rank 37
(97 of 176 in the sample above), and half of the residue classes in the disconnected cases. Over F_7 a quadratic
space is determined by its dimension and its discriminant, so one line gives no further invariant of this kind.
It does not exclude rank 37.

Context received while writing this:
* the laptop session (03:34 UTC): 150 random connected balls without prism, 30 with 7 | tau; the 120 others all
  have NO star at vertex 0 (median 867 000 nodes), about 20 s per ball; it estimates 1e10 ordered connected types,
  so the obstacle is the number of types, not the weakness of the test;
* Codex (message after my 443): for a connected line without torsion, a selection of 60 binary shadows with
  N N^T = K, Green(n_f, n_f) = 6, Green(n_f, n_g) in {2, 3} and at most 240 edges in F = 3 - Green is automatically a
  srg(99,14,1,2) of rank 37 (its note 230 in preparation, not read here). With the lemma above: **when tau(G) is a
  quadratic residue modulo 7 no such selection exists**, whatever the search would say.

Addendum to 17.80 (03:49 UTC, 09/10): the rule with torsion, asked by the laptop session; the moments.
* General rule (hand, not audited; a consequence of L23). In the laptop session's model, V = (non-degenerate part
  of the span of the near vectors) + one hyperbolic plane for each direction of the radical of the span + the residue
  R. The non-degenerate part of the span is F_7^36 / R0 with the form M0, whatever the true relations are; call d0
  its discriminant (computed from the ball alone: `disc_mod7` in `disc_tau_check.py` returns the rank 36 - dim R0
  and d0). A hyperbolic plane has discriminant -1, a non-residue. Hence
      disc(R) = (non-residue) . d0 . (-1)^(dim R0 - dim Tr)   modulo squares,   dim R = 2 dim Tr - dim R0.
  For the (4,8) torsion driver (true relations z0 and B, dim B = beta, torsion rank t): dim R0 - dim Tr = t - beta,
  rho = 2 beta - t + 1. rho = 0: the sub-case is possible only if d0 (-1)^(t - beta) is a non-residue; rho = 1:
  c0 is in the class of (non-residue) d0 (-1)^(t - beta); rho = 2: the form <1,1> (discriminant 1) or <1,3>
  (discriminant 3) is the one whose discriminant is in that class. Example t = 1: if d0 is a square, the sub-cases
  left are (beta = 0) and (beta = 1, <1,3>); if d0 is a non-residue, only (beta = 1, <1,1>).
  Checks of the rule against the two cases already written: two components without torsion, d0 = 3 tau1 tau2,
  gives c0 = tau1 tau2; connected without torsion, d0 = 4 tau, gives tau non-residue.
  **Not used in the runs of tonight**: the torsion follow-up queued here keeps the three sub-cases (a superset).
* Moments (hand). With W = M0^(-1), K = N N^T and gamma_ff' = 1_S^T W 1_S' (6 on the diagonal, 2 + A_ff' elsewhere),
  tr((WK)^k) = tr(gamma^k). I computed both sides for k = 1, 2, 3 for a triangle-free G: 3 = 3; 2 = 2 once e(F) = 240;
  6 = 6 once the far graph has 32 triangles (the 32 far lines). So they give e(F) = 240 and 32 far triangles modulo 7
  and nothing on G: no invariant of G alone comes out of the moments up to order 3. (k = 1 is in note 102, section 8.)

Second addendum to 17.80 (03:54 UTC, 09/10): Codex's reading of the two additions (its answer to my message 274; its note 231 in
preparation, not read here).
* Rule B' confirmed by Witt completion, with no test on graphs: for p : F_7^36 -> V, Tr = ker p (dimension b) lies in
  R0 = ker M0 (dimension d); the image has dimension 36 - b, radical of dimension a = d - b and non-degenerate
  quotient of discriminant d0; completing the radical by a hyperbolic planes gives V = W0 + H^a + R, so
  dim R = r - 37 + 2b - d and disc R = disc(V) d0 (-1)^a modulo squares, at every rank with its known disc(V).
  Codex's extra consequence: when dim R = 0 fails by the sign, ALL the subspaces Tr of that dimension are excluded,
  not one choice of basis; the dimension of Tr must then go up by at least 1, and if another bound forbids it the
  ball is eliminated directly. Status of B': derived here, refereed by Codex, still not used in tonight's runs.
* Moments, Codex's general form (it replaces my three computations): with W = M0^(-1) = 5J - H^+ and gamma = N^T W N,
  Sylvester gives chi_gamma(x) = x^24 chi_WK(x); on the three layer constants WK has the values 6, 0, 0, and on
  E = {layer sums zero} WK = H. So tr gamma^k = 6^k + tr (H|E)^k for EVERY k >= 1 in F_7: all the traces follow from
  N N^T = K. They can filter a relaxation that drops this equality; they add nothing to the complete selection.

### 17.81 The (4,8) main sweep is finished: every torsion-free representative ball is dead (04:51 UTC, 09/10)

Run of the laptop session's driver on the lab PC (its model and solver, not audited here; see the README of
`../c1_lap_sweep48_2026-10-09/`). Ended 04:49:07 UTC; 12 000 parts of 12 000, no error code, no presence check
positive during the night.
* Representatives (one ball per isomorphism class, the laptop session's `reps48.txt`): 97 896 of 97 896 logged;
  dead 81 380; TORSION 16 516 (rank 1: 15 462, rank 2: 964, rank 3: 71, rank 4: 19); other 0; missing 0.
* All balls logged (the parts before the switch were swept in full): 117 860 of 245 877; dead 98 163; TORSION
  19 697; other 0.
* Checks on the finished logs: no trace of the race of 17.79 (117 860 distinct balls, smallest cands 5184, smallest
  node count 23 773); the 19 964 non-representative balls swept before the switch all have the verdict of their
  representative (dead 16 783, TORSION 3181, none different); the TORSION flags agree with `tors_m4.json`.
* Raw log in the repository: commit d51ebbd, `lap_sweep48/sweep_48_all.log.gz` (sha256 of the uncompressed file
  b8fac2c90714ef47...).
What it says: in the laptop session's model, at rank 37, a line with components of 12 and 24 points, without prism
and whose large component has no 7-torsion, admits no star at one near point, for both classes of the residue.
What it does not say: nothing on the 16 516 torsion balls (rank 1 running here since 04:49:49 UTC, about 32 s per
part of 8 balls; ranks 2 to 4 on the laptop: rank 4 reported closed, 19 of 19, at 04:51 UTC); nothing on connected
lines; the reduction to representatives is checked on a sample and on the 19 964 balls above, the complete check is
queued. Rank 37 is not excluded.
Reported by the laptop session at 04:19 and 04:51 UTC: at torsion rank 2 some balls come out COMB-ALIVE in the
sub-case where the whole torsion plane is balanced (residue of rank 3, combinatorial test only); it decides them
with a rank test (`fastrD`), the 6 met so far are dead. Its six-grid line: one star with the rank condition EXISTS,
so one star does not decide that line; my own treatment (17.46, 17.47, 17.73 B) is still open, sent to it with the
known degrees between two blocks of a prism for a two-point test.

Addendum to 17.81 (04:57 UTC, 09/10): load of the torsion run. With 11 workers the torsion driver gave a mean load of 75% with
8 samples of 40 above 80% (maximum 93%), above the user's allowance. Stopped at 04:54 UTC (whole process tree; count
afterwards: no driver, no worker, no fastg4.exe; 9 leftover instance files deleted; 100 parts and 844 balls logged,
all DEAD, no ball twice) and restarted at 04:55 UTC with 9 workers, resuming from the log: mean 71%, maximum 80%, no
sample above 80%. The temporary files carry the process id since 03:25 UTC, so the two runs could not share a file
even if a process had survived. New expected end of rank 1: about 06:50 UTC.

### 17.82 Computations stopped on the user's order (05:08 UTC, 09/10)

The user, direct message: "Vasy arrete les calculs vous êtes vraiment pas possibles", after asking whether six hours
had brought no advance (answer given: on the objective, none; rank 37 is not excluded). Stopped at 05:08 UTC: the
torsion run of rank 1 and the queued complete isomorphism check; no computation process left on the lab PC (load 3%).
State kept on disk, resumable, NOT to be restarted without the user's word:
* (4,8) main sweep: finished (17.81).
* Torsion rank 1 (`../c1_lap_sweep48t_2026-10-09/`): 346 parts of 2004 finished, 2792 balls of 15 462 logged, not DEAD: 0.
  The 65 unfiltered balls of rank 2 were not reached.
* Complete isomorphism check of the reduction to representatives: never started. The reduction therefore rests on the
  sample of 400 + 400 pairs (17.78) and on the 19 964 balls swept twice over (17.81).

### 17.83 The two obligatory kernels of one quadrangle: an exact relation between kernel types; it excludes pairs, not types (05:51 UTC, 09/10)

Mission of the user (direct, 05:10 UTC): research on routes to a complete decision, rank-free, with a real attempt
and an honest account. Computation used: single process, runs of at most four minutes (about 20 minutes in all).
Reference state read: Codex's branch at 19ec316 (ten commits after the reference d772db0: its notes 225 to 231).

**Three mechanisms considered.**
1. (chosen) Coherence of several obligatory kernels: a quadrangle carries TWO occurrences of the motif.
2. The complete binary shadow design of one line (60 shadows with N N^T = K, no rank). Not pursued: it needs the
   cubic graph G(T), whose types are too many; no decisive test of bounded size.
3. A link with the arithmetic (sign of blocks, Codex's L23) or with the laptop session's theorem. Not pursued: those
   tools act on blocks of at least 36 determined vertices; a kernel or a union of two has 14 to 20.

**Setting** (Codex's note 221): S = triangles 012, 345, cross edges 03, 14; D = the eight double vertices
(6:{0,3}, 7:{1,4}, 8:{2,3}, 9:{2,4}, 10:{0,5}, 11:{1,5}, 12, 13:{2,5}); H = S + D; 174 surviving types.
In the picture of the line T = 012: 3-4 is a cross edge of G(T), 5 its far apex, 6, 7 the mates of 3, 4.

**Lemma (hand, no hypothesis).** Suppose 6 and 7 are not adjacent. Then:
(a) S* = {0,3,6} + {1,4,7} is again an occurrence of the motif (cross edges 0-1 and 3-4): the quadrangle 0-3-4-1
    has two pairs of opposite edges and each gives a pair of lines; S + S* is the quadrangle with its four third
    points 2, 5, 6, 7. So the kernel H* = S* + D* exists and must be one of the 174 types.
(b) D* = {2, 5, d(1,6), d(4,6), d(0,7), d(3,7), two common neighbours of 6 and 7}. A member is a vertex of H
    exactly in these cases: d(1,6) = 11 if 6~11; d(4,6) = 9 if 6~9; d(0,7) = 10 if 7~10; d(3,7) = 8 if 7~8; a
    common neighbour of 6, 7 is 12 or 13 if that vertex is adjacent to both. Otherwise it is a vertex outside H
    whose neighbours in S are exactly {1}, {4}, {0}, {3} respectively, and a subset of {2,5} other than {2,5} for
    a common neighbour of 6 and 7. (Proof: two neighbours in a triangle are impossible; a second neighbour in S
    would make the vertex one of the eight double vertices, which are all in H.)
(c) Each of the four pairs (2,6), (2,7), (5,6), (5,7) is non-adjacent and has one common neighbour in the
    quadrangle (0, 1, 3, 4 respectively), hence EXACTLY ONE other common neighbour.
Consequences for the types (tau of H, tau* of H*): tau* agrees with tau on the members of D* lying in H; the bits
(6,9), (7,8), (6,11), (7,10) of tau become the bits (6*,9*), (6*,11*), (7*,8*), (7*,10*) of tau* (the two middle ones
exchanged); and by (c), a vertex adjacent to 2, 5 and to exactly one of 6, 7 cannot coexist with a vertex adjacent
to 6, 7 and to exactly one of 2, 5.

**Computation 1: all completions of H u H*** (`quad_partner_kernels.py`, `quad_partner_kernels.json`). For each
of the 140 surviving types with 6 not adjacent to 7 (the 34 others have a prism as partner pair), every labelled
survivor is tried as H* and every adjacency of the new vertices to H is enumerated; kept: common neighbours
<= 2 - adjacency for all pairs, and the two positivity conditions of note 221 on the union (17 to 20 vertices).
* Every type has at least two partner types: **no kernel type is excluded.**
* The relation "tau and tau* can share a quadrangle" has 4177 ordered pairs out of 19 600 (2122 unordered pairs
  out of 9870) and is exactly symmetric (0 asymmetric pair: a control of the program, since the union is the same
  graph read from either side). It has six connected components, of 2, 8, 9, 14, 48 and 59 types.
* In the components of 48 and 59 types, 26 and 22 types are compatible with the whole component and the 22 and 37
  others only with those: two types of the second kind never share a quadrangle.
**Computation 2: the relation is elementary** (`quad_partner_elementary.py`). The relation predicted from the lemma
alone (agreement on common members, forced neighbours of the new members, (c)) is EQUAL to the computed one for all
140 types. So the exclusion of the 7748 unordered pairs is a theorem by hand, and the positivity conditions on the
union together with the search over the new vertices add nothing at the level of types or pairs of types. (The
smallest eigenvalue of 27I - 9A + J on a surviving kernel lies between 0.82 and 2.95 in the two large components:
positivity is far from active.)
**Computation 3: the mask-multiplicity test of note 222 on the union** (`quad_union_mask_lp.py`). Control first:
on the 310 fourteen-vertex kernels my implementation gives Codex's exact statuses in all cases (174 feasible, 136
infeasible) and the same number of admissible masks for every kernel. On the unions (floating LP, numerical
verdicts): type 38: 230 completions, 160 feasible; type 2118: 112 completions, 59 feasible; type 136: 2042 of
19 208 completions tested, 539 feasible. The test removes a large part of the completions and no type; both partner
types of 38 and of 2118 remain. Not run on the other types (thousands of completions each).

**What is new, and what is not.**
* New exact statement, rank-free, covering every candidate: on every quadrangle whose two pairs of opposite lines
  are both joined by exactly two edges, the two kernel types form one of 2122 explicit unordered pairs; in
  particular, with n(.) the numbers of occurrences, n(restricted types) <= n(full types) inside each of the two
  large components (each occurrence of a restricted type is matched with one of a full type on its quadrangle).
* Not obtained: any exclusion among the 174 kernels. The chain of coverage is unchanged: 174 kernels open; ranks
  37, 39, 41, 43 open. This is a negative result on the tested closure, not an exclusion of candidates.
* Refuted expectation: "asking the partner kernel of the same quadrangle to be a survivor, with positivity on the
  union, removes kernel types". Witnesses: one explicit completion for each of the 4177 pairs (in the json).
* Precise obstacle: the two kernels of a quadrangle share only the quadrangle and its four third points; up to six
  vertices are new and attach to H through few edges, so the only binding conditions are the common-neighbour
  counts of the four pairs in (c). The exact covering equations (masks) do bite on the union, but they act on
  completions, which are numerous.
* Next closure identified, not done: every kernel has four further obligatory kernels WITHOUT any hypothesis (the
  cross edges 3-8 and 4-9 of G(T), and 0-10, 1-11 of G(T'): the edge 3-8 is never in a triangle because 3-4 is not).
  Along a cycle of cross edges of G(T) the kernel types must follow the corresponding transition relation, so a
  type lying on no closed walk of admissible length would be excluded. Decisive test: the same enumeration with up
  to seven new vertices; cost of the same order as computation 1. Whether that relation is again elementary is
  not known.

**Addendum (08:39 UTC, 09/10): the union test in its decisive form; the mechanism is closed without exclusion.**
Before running anything I checked whether the natural strengthening (edge counts between mask classes, pairs of
outside vertices) was still open: it is not. Codex's note 223 records my own pilots of message 412 (edge-count
relaxation feasible on the 29 kernels tried; closure by third points stopped at the ceiling on 15 kernels) and
its integer coexistence model (15 kernels, all with a witness). Not repeated.

What was missing from computation 3 above is the decisive question: does a type exist for which NO completion
of H u H* passes the mask-multiplicity test on the union? `quad_union_first_feasible.py` answers it by stopping at
the first feasible completion of each type (a type with none would have been excluded, numerically).

    python quad_union_first_feasible.py <Codex data folder> quad_union_first_feasible.json 250 <the 140 types>
    decided 140 of 140 listed types: feasible 140, no feasible completion 0, undecided 0        [48 s, one process]

For the 31 types with the fewest partner types (2, 6, 8 or 9 partners) the very first completion is feasible;
the largest number of completions tested before a feasible one is 30 (type 9728). A feasible verdict is a
floating LP solution of a necessary condition; it constructs nothing. Outcome: the mask test on the union of
the two kernels of a quadrangle excludes NO kernel type. Both chains unchanged: 174 kernels; ranks 37, 39, 41, 43.
