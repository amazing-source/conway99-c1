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
