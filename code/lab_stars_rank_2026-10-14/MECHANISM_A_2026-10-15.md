# Mechanism A: why breaking the star matchings costs a relation (LAB, 15/10/2026, from 14:35 UTC)

User (14:35 UTC): the mechanism WITHOUT symmetry is the most important statement of the campaign; irreproachable
rigour; see and understand everything, ask why / why not, dig.  Split: LAB = A (this file) and B (asymmetric search);
Codex = C (ODD9); D (extension-first route) parked.

Status words: PROVED (written proof, checked), EXACT (exact computation, SAT completeness without certificate unless
stated), EVIDENCE (numerical / partial data), OPEN, FALSE (explicit counterexample).

## 1. Setting and notation (all objects are those of stars_rank.py)
- Letters 0..13, mates y^1; star letters 0,1 (line l) and 2,3 (line m); outer letters 4..13.  S = the 44 labels meeting
  {0,1,2,3}: X_l = labels meeting {0,1} (24), X_m (24), C4 = X_l n X_m = {02, 03, 12, 13}, Y_l = X_l \ C4 = {0y, 1y : y
  outer} (20), Y_m = {2y, 3y} (20).
- Gamma admissible: (C1) exact counts towards the four stars, (C1') caps towards the outer letters, (C2) caps on
  common neighbours inside S.  T = 3I - Gamma - K, U = 7 Pi_S - T, nu = nullity T, N = ker T.  "PSD" = T >= 0 and U >= 0.
- h = (0 1)(2 3) on letters (outer letters fixed), acting on labels and label vectors ((h n)(x) = n(h x)).
  Delta = Gamma - h Gamma h.  N_h := N n hN = N n ker(Delta) (since hN = ker(hTh) and hTh = T + Delta).
- Star matchings M_a (a = 0..3).  l-half: M_1 = h(M_0) (as letter pairs, h acting as s_m on the letters other than 0,1);
  m-half: M_3 = h(M_2).  (H-MATCH): PSD and nu >= 14 => both halves.
- H_l: letters other than 0,1 joined by mates, M_0, M_1, sigma_l; components W (unions of lines), c(l).  A TWIST of the
  l-half on a component W: M_1|W != h(M_0)|W.  The l-half fails iff some component carries a twist.

## 2. Candidate statements (to be tested for necessity of every hypothesis before any proof attempt)
- (S0) = (H-MATCH).  (S0-l): l-half only.
- (S1) kernel symmetry: nu >= 14 => dim N_h >= 14 (all mixed relations h-homogeneous).  Positivity needed or not?
- (S2) from kernel symmetry to matchings: PSD, nu = 14, N = hN => no twist.
- (S-comp) a twist on a component W of H_l with m not in W => (PSD) nu <= 13.
(S1) and (S2) together give (S0).  Known: (S2) needs U >= 0 (kmilp_obj53_ambig.json: T >= 0 exactly, nu = 14, N = hN,
both halves twisted, U not PSD).  The T-only form of (S0) is FALSE (same witness).

## 3. Proved ingredients
- G21 (side relations h-homogeneous, for every admissible structure).
- Lemma 6h (true symmetries h p, p != id, block absorption; needs ODD9 and (H_g)).
- Rank formula: nu = 21 + c(l) - og_l - e_l (og = odd gain of the f_y over X_l, e = even gain of the g_y); ODD9 = og = 9.

## 4. Experiments and results
(filled below as they come)
### E1 (15:15 UTC): dimension of N_h = N n hN in three COMPLETE neighbourhoods, no positivity assumed
(kernel_sat_enum.py with NHREPORT; numerical SVD rank for N_h; logs hmatch_tools_2026-10-15/nh_*.log)
- KHOMOG class of asy_best11 (3 036 structures): every nu = 14 structure (16 PSD + 680 non-PSD) has N_h = 14 and
  h-related matchings; every broken nu = 13 structure (16 PSD + 160 non-PSD) has N_h = 12; h-related nu = 13: N_h = 13.
- KHOMOG class of HB_1 (672): identical pattern (nu = 14: 8 PSD + 340 non-PSD, all N_h = 14, h-related; broken nu = 13:
  4 PSD + 28 non-PSD, all N_h = 12).
- Kernel class of obj53 (15 936): broken nu = 14: 8 688, all N_h = 14 (h-invariant kernel); broken nu = 15: 480 with
  N_h = 15 and 240 with N_h = 14; h-related nu = 15: 2 880 (N_h = 15); none of these is PSD (96 PSD, all h-related, nu 14).
READING.  Two kinds of breaking:
- TYPE II (neighbourhoods of the walk lineages): breaking destroys two h-homogeneous relations (N_h <= 12) and creates
  at most one inhomogeneous ('saturated') direction, so nu <= 13, WITHOUT positivity.
- TYPE I (special kernels, obj53): the breaks are invisible to the kernel (N = hN, nu = 14 or 15, even with one
  saturation on top of 14); only positivity (U) excludes them.
(S0) needs both: a combinatorial argument for type II and a positivity argument for type I.
### E2 (15:20 UTC): twisted cycles and ties (hmatch_tools_2026-10-15/twist_ties.py, exact)
TIE LEMMA (PROVED, elementary).  Let C be an alternating cycle of M_0 and h(M_1) (a twist of the l-half), y in C with
cycle neighbours y+ = M_0(y), y- = h(M_1)(y).  In row {0,y} of Delta = Gamma - h Gamma h the L_0-part is
e_{0y+} - e_{0y-} (since Gamma(0y, 0y+) = 1 and Gamma(1hy, 1hy+) = [M_1(hy) = hy+] = 0, and symmetrically for y-).
Every h-even kernel vector n is in N n hN, hence in ker Delta, so
    n(0y+) - n(0y-) + sum_{x not in L_0} Delta(0y, x) n(x) = 0.
If the row is PURE (Gamma(0y, x) = Gamma(1hy, hx) for all x outside L_0), every n in N+ takes equal values on the orbits
of y+ and y-.  Same on the m-side with rows {2, y}.
DATA.  HB_1: one twisted 4-cycle (4,7,6,5) on l and one (4,9,6,7) on m; the rows {0,7} (Delta = +04 -06) and {2,7}
(Delta = -24 +26) are pure: ties u_4 = u_6 and g_4 = g_6; the profile of N+ on each cycle has dimension 3 instead of 4;
dim N+ = 10 = 12 - 2 (the other rows of the cycles are compensated by cross terms).  asy_best11: same two cycles and
pure rows, dim N+ = 8.  obj53 near-miss (type I): one twisted 10-cycle on each side; EVERY row is compensated by exactly
one swap of two cross edges into L_2 (e.g. row {0,4}: L_0 part -011 +013, L_2 part +210 -212), no tie, dim N+ = 12.
So type I = 'every twisted row compensated'; this forces the even kernel to satisfy one affine identity
n(0a) - n(0b) + n(2c) - n(2d) = 0 per twisted row, which a generic kernel does not.
OPEN QUESTIONS: (Q1) can compensation be complete without forcing an h-invariant kernel (type I)?  (Q2) why does U fail
in type I?  (Q3) why at most one saturated direction in type II?
### E3 (15:25 UTC): census of twists in the HB_1 neighbourhood (all 96 broken structures of nullity >= 12 of the
complete KHOMOG class; hmatch_tools_2026-10-15/twist_census.py, exact; dumps in hmatch_tools_2026-10-15/dump_HB1)
(nu, dim N_h, dim N+, PSD, broken halves, cycle lengths l / m, pure rows l / m): count
   (13, 12, 10, -, l m, (4)/(4), 1/1) 28      (13, 12, 10, PSD, l m, (4)/(4), 1/1) 4
   (12, 12, 10, -, l only, (4)/(), 2/0) 24    (12, 12, 10, -, m only, ()/(4), 0/2) 20
   (12, 12, 10, -, l m, (4)/(4), 1/1) 16      (12, 12, 10, PSD, l m, (4)/(4), 1/1) 4
- In EVERY broken structure: exactly two pure twisted rows in total (one per side, or two on the single broken side),
  dim N+ = 12 - 2 = 10, dim N_h = 12, and nu = 12 + (0 or 1 saturated direction); the saturation occurs only when BOTH
  halves are broken.
- TELESCOPING (PROVED, elementary): on a twisted cycle y_1 .. y_2k the L_0-parts of the rows alternate,
  part(y_j) = e(y_{j+1}) - e(y_{j-1}) up to the orientation, so the sum over the odd-indexed rows (and over the even ones)
  of the L_0-parts is 0.  Hence for every even kernel vector n: sum_{j odd} cross_j(n) = 0 and sum_{j even} cross_j(n) = 0,
  where cross_j(n) = sum_{x outside L_0} Delta(0y_j, x) n(x).  A twist therefore always produces either ties (pure rows)
  or pure cross constraints on the m-values.
- General form (PROVED): for T >= 0, ker A(Gamma_0) = N+ is contained in V_Delta = {n even : sum over N(r) of n =
  sum over N'(r) of n for every label r}, N'(r) = h(N(hr)) the neighbourhood of r in h Gamma h.  So N+ is the set of even
  vectors on which Gamma and h Gamma h act identically AND which are killed by the averaged even block.
### E4 (15:23 UTC): census of other twist patterns (twist_census.py)
- obj53 near-misses (55, type I): nu = 14, N_h = 14, N+ = 12, both halves twisted along ONE 10-cycle each, 0 pure rows.
- <Z5, hM> PSD members (192): (nu 9, N_h 5, N+ 3, both halves twisted, 10-cycles, 0 pure rows) 128; (nu 9, N_h 9, N+ 7,
  one half twisted, 10-cycle, 0 pure rows) 16 + 16; (nu 5, N_h 5, N+ 3, both, 0 pure) 32.
CORRECTION / LESSON: 'at most one saturated direction' (question Q3) is FALSE in general: the 128 c22 members of
<Z5, hM> have nu - dim N_h = 4 saturated directions with respect to h (their kernel is invariant under the TRUE symmetry
hM instead: profile (7,2)), while nu stays at 9.  So the split 'ties + saturations' relative to h is not the right
invariant in general; what holds in all data is nu <= 13 for broken PSD structures.  The relevant involution seems to
be the one under which the KERNEL is invariant (h for type I, the fake h(4 6) for the HB_1 lineage, hM for <Z5, hM>).
### E5 (15:30 UTC): KERNEL symmetry (hmatch_tools_2026-10-15/kernel_hp_scan.py; candidates p = outer permutations
relating the matchings, plus p = id; numerical SVD)
- dump_HB1 (96 broken, nu 12-13): nu = 12 (64): ker T is h-INVARIANT although the structure is broken; nu = 13 (32): ker T
  invariant under the fake g = h (4 6) (the structure too).
- asy_best11 (no whole h-type symmetry): ker T IS invariant under the fake g = h (4 6) (9 g-even + 2 g-odd), although the
  structure is not (fake_kernel.py: dim(N n gN) = 11 = nu).
- obj53 near-misses (55): ker T h-invariant (type I).
- <Z5, hM> (40 sampled): ker T invariant under h, or under h p with p a product of four flips (true symmetries).
EMPIRICAL LAW (KER-SYM), OPEN: the kernel of every structure seen (PSD or not, nu >= 9) is invariant under SOME
involution g = h p (p an involution of the outer letters, mate-preserving or not), even when the structure is not.
If it were a theorem, (S0) would reduce to finitely many symmetry types: p = id (type I, U must fail), p a true symmetry
(lemma 6h-type absorption bounds), p fake (defect analysis: N n ker(Delta_g + D'_g), Delta_g = g Gamma g - Gamma,
D'_g = gKg - K fixed).  CAVEAT: all these structures descend from h-symmetric lineages; a test on unbiased data is needed.
### E6 (15:45 UTC): where the lemma of 6h stops, and the frontier
- Lemma 6h bounds nu <= 12 + min(c(l), c(m)) - k for a TRUE symmetry h p with k two-cycles of p on the outer letters
  (under (H_g) on both sides and ODD9).  It excludes nu = 14 only when k >= 5 (or k >= 4 with min c <= 5 ...): for p a
  single flip (k = 1) it allows nu = 14 as soon as min c >= 3.  So true symmetries with SMALL k (1 to 4) are the
  frontier: half-size families (cheap rank drops, kernel split) whose members are h-broken, not covered by the lemma.
- Known: <h, (4 5)> has no admissible structure (so no h-invariant object is (4 5)-invariant); cold walks in <h (4 5)>
  never reached positivity; G1'' (contains h (4 5)) is too large for complete enumeration.
- Type I U-violations (near-misses and kmilp_obj53_ambig, u_violation_cycle.py): the most negative direction of U is
  mainly ODD (coordinates up to 1.8 against about 0.3 for the even ones), spread over the whole twisted 10-cycles of BOTH
  sides, degenerate (lambda = -0.0486 twice for the near-misses: a Z5-type Fourier pair); for kmilp_obj53_ambig
  lambda_min(U) = -0.604 simple.
### E7 (15:55 UTC): (KER-SYM) REFUTED outside h-type lineages
In the h-free family <Z5, tau> (tau = (0 2)(1 3) swaps the lines; no h-type element), the first 40 PSD members of
nullity 9 (enum_cubes.py, SAVEMIN = 9, complete enumeration of the 5 cubes running) have kernels invariant under NO
h p: exhaustive test over all 9 496 involutions p of the outer letters (kernel_inv_all.py): max dim(N n gN) = 5.
(asy_best11 is invariant under exactly one: p = (4 6).)  SCOPE (corrected 16:10 UTC after the user's remark and Codex's):
this refutes only the UNIVERSAL version (all nullities); it says nothing about the version that matters,
(KER-SYM-14): 'nu >= 14 => ker T is invariant under some h p'.  Every known structure of nullity >= 14 (PSD or not:
the 331 objects, the harvests, the obj53 class including its nu = 15 members, the nu-14 members of the KHOMOG classes)
satisfies it; it remains OPEN and can still carry a proof of (S0).  My 15:55 wording 'artefact, cannot carry a proof'
was a hasty conclusion and is withdrawn.
### E8 (16:02 UTC): <Z5, tau> (h-free, tau swaps the lines), cubes 0, 2, 4 COMPLETE (51 934 structures each, 30 PSD each,
max PSD nullity 9); cubes 1, 3 running.  PSD members found: nu = 9 (broken: (nu 9, N_h 5, N+ 3, twisted 10-cycles on both
sides, 0 pure rows) 26 of 30 checked; h-related but not h-invariant: 4) and nu = 13 in cube 3 (6 files: mate-aligned
matchings, h-related, kernel invariant under 312 involutions h p: the Hamming-like grid objects).  So in this h-free
family as well, broken PSD members stop far below 14 (9), and the only nu = 13 members are h-related.

## 5. STATUS OF A at 16:05 UTC (honest summary)
PROVED: tie lemma and telescoping (E2, E3); G21; lemma 6h (true symmetries, with ODD9 and (H_g)); for T >= 0:
N_h = ker A + ker C and nu = 2 + dim N+ + s (s = multiplicity of the singular value 1 of K = A^-1/2 B C^-1/2), so with an
h-invariant kernel nu = 14 forces every twisted row to be compensated (type I).
REFUTED (my own intermediate conjectures, scope stated): 'at most one saturated direction' for ALL nullities (E4: s = 4
at nu = 9 in <Z5, hM> and <Z5, tau>; nothing is known against it at nu >= 13); the UNIVERSAL kernel-symmetry law (E7, at
nu = 9).  STILL OPEN and consistent with all data: (KER-SYM-14) and 's <= 1 when nu >= 13'.
EVIDENCE (no exception anywhere): broken + PSD => nu <= 13; regimes seen: type I (N+ 12, s 0, nu 14, U fails),
HB_1 lineage (N+ 10, s 0 or 1, nu 12-13), Z5 families (N+ 3, s 4, nu 9; or N+ 7, s 0, nu 9).
EQUIVALENT TARGET (exact reformulation): for T >= 0, nu = 2 + nullity(S_A), S_A = A - B C^+ B^T; nu <= 13 <=> the 22 even
orbit vectors (Gram vectors w(x) + w(hx)) have rank >= 11 modulo the 20-dimensional span of the odd ones.
NOT YET UNDERSTOOD: (i) why full compensation (type I) is incompatible with U >= 0; (ii) why, without full compensation,
the even span cannot fall far enough into the odd span to restore nullity 14 (the saturation mechanism).
### E9 (16:15 UTC): what full compensation (type I) forces on the kernel
Case nu = 14, c(m) = 2 (fiber of the u-profile of N+ = the two even X_m-relations, so N+ -> R^10, n -> b = (n(0y))_y, is
ONTO) and N+ = {(b, L b + fiber)}: L = the mixed-relation map (m-even coefficients as a function of the l-even ones).
- PROVED (linear algebra): if a twisted l-row {0,y} is compensated by a single cross swap +e(2c) - e(2d) in L_2 (as in
  every row of the obj53 near-misses), the constraint b(y+) - b(y-) + (Lb)_c - (Lb)_d = 0 holds for ALL b in R^10, hence
  L_c - L_d = e(y-) - e(y+) (rows of L).  Full compensation of a twisted cycle therefore forces L to be a PERMUTATION
  matrix up to signs and a common correction along the cycle structure.
- DATA (kernel_shape.py, exact, rewritten modulo Sum g = 0): the obj53 class (the only class with broken members)
  has u_y = -g_{y^1} + (2/5) G_odd for y even and u_y = -g_{y^1} - (2/5) G_odd for y odd (G_odd = sum of g_z over
  odd z): a mate permutation plus a rank-one correction.  An ordinary class (obj0, no broken member) has e.g.
  u_4 = g_4 + g_6 + g_7 + (2/5) G_odd: several g per u, no permutation structure, so no full compensation is possible.
READING: type I lives only on kernels whose mixed map is a permutation (mod rank one); for every other kernel a twist
forces ties.  Remaining for type I: show U fails, using this explicit kernel structure.
