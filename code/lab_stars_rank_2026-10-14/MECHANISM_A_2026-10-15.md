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

## 5. STATUS OF A at 16:05 UTC (honest summary) [SUPERSEDED by the status at 17:30 UTC at the end of this file: 's <= 1 when nu >= 13' was refuted at 17:00 UTC (E12), ODD9 too]
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
### E10 (16:20-16:50 UTC): <Z5, tau> complete; where U fails in type I; the alternating -4 vector; a sign lemma
(a) <Z5, tau> COMPLETE (enum_cubes.py, 5 cubes, cryptominisat UNSAT per cube, no certificate; logs Z5s_solve_*.log):
253 212 invariant admissible structures, 160 with T, U PSD; maximal PSD nullity 13, reached only in cube 3 (45 476
structures, 40 PSD); cubes 0, 1, 2, 4: 51 934 structures and 30 PSD each, maximum 9.  Census of the 70 PSD members of
cubes 1 and 3 (twist_census.py): nu 13: 16, ALL with both halves h-related (N_h = 13, N+ = 11, no twist); nu 9 broken
(both halves, 10-cycles, N_h 5, N+ 3): 50; nu 9 h-related: 4.  So in this h-free family the broken PSD members stop at 9
and the only nullity-13 members are h-related.
(b) Where U fails in type I.  Framework (NOT NEW): P10 of NOTE_PROOFS_1410 (T >= 0 <=> lambda_2(H) <= 3, U >= 0 <=>
lambda_min(H) >= -4, nu = mult_3(H), H = the 59-vertex graph N[v] + S) and the odd quotient (odd_quotient.py).  Its
restriction to V0 = ker D (dim 30): K = D^T Q D and Pi = I - D^T (D D^T)^-1 D act trivially there, so EXACTLY
T = 3 - Gamma and U = 4 + Gamma on V0; an h-odd x has D x = (al, -al, be, -be, 0..0), the star differences cover those
directions, so the odd sector is PSD iff spec(Gamma_0 | V0-) is in [-4, 3] (identities checked to 1e-14,
odd_block_u.py).  Results (odd_block_u.py, v0_spectrum.py, coupling_spectrum.py, h59.py; numerical eigenvalues of exact
structures):
- 55 near-misses (nu 14, T >= 0, N = hN, both halves twisted): U >= 0 on the even sector (lambda_min 0.180) AND on the
  odd sector (lambda_min exactly 0: Gamma_0 has the eigenvalue -4 on V0-, vector of (c)); Gamma | V0 has spectrum in
  [-4, 3]; U fails only through the coupling with the ten outer letter directions 1_0y + 1_1y + 1_2y + 1_3y:
  lambda_min(H) = -4.0474.  In the T_0-eigenbasis the violation is carried by an even pair (T_0-eigenvalue 5.111) and an
  odd pair at 6.966, i.e. 0.034 below the ceiling 7: U-normalised coupling 1.4946 > 1, while the T-normalised coupling
  is 0.8673 <= 1.  NOT LOCAL: greedy + pruning needs 33 vertices of H to get below -4 (h59_local.py; minimality not
  proved).
- 720 broken nu = 15 members of the obj53 class (dump_obj53): three groups of 240 (U fails on the even sector only /
  odd only / both); in all of them Gamma already leaves [-4, 3] on V0 (lambda_min -4.189, -4.346, -4.236).
  kmilp_obj53_ambig: lambda_min(Gamma | V0) = -4.518, lambda_min(H) = -4.594.
- HB_1 neighbourhood dump (96 broken, nu 12-13, 8 PSD): every non-PSD member already fails on V0 (lambda_min -4.04 to
  -4.69).
READING (question (i)): in the obj53 class the failure is visible on the pure-label space V0 (U = 4 + Gamma), mostly
on the averaged odd sector; the near-misses are the borderline case (odd sector exactly at -4) where the excess comes
from the letter directions.  The failure is global (no small induced certificate), with a small margin (-4.047).  So
(i) is a quantitative spectral fact of this single kernel class; I found no structural reason that would extend to
unknown kernels.  STATUS: EXACT location, no proof route for a general type-I exclusion.
(c) The alternating -4 vector (alt_vector_scan.py, u_odd_kernel.py; integer check Gamma w = -4 w on all of S).
w(eps, theta) = sum_y eps_y (f_y + theta e_y), eps_{y^1} = -eps_y, theta = +-1 (f_y = 1_0y - 1_1y, e_y = 1_2y - 1_3y,
zero on C4); w is h-odd with D w = 0.  Gamma w = -4 w holds for 285 of the 287 kernel-class objects (127/129 reps, 18/18
newk1, 140/140 newk2), for all 55 near-misses (with Delta w = 0), for 144 of the 148 nu-9 PSD members of the Z5 families
on file, for the 8 PSD members of the HB_1 dump; it fails for the 16 nu-13 PSD members of <Z5, tau> (Hamming-like),
asy_best11, kmilp_obj53_ambig, the 720 broken nu = 15.  Local law, the same in every case where it holds: each of the
40 labels of Y_l u Y_m has exactly six Gamma-neighbours in S, all in Y_l u Y_m, five with the opposite w-sign and one
with the same (-5 + 1 = -4); in the grid case C4 is an isolated 4-cycle of Gamma_S.  Meaning in a Conway graph (P10
(iii), G9): w would be a global -4-eigenvector supported on Y_l u Y_m, so mult_-4(H) >= 5 and rank U_S <= 39 (epsilon
>= 1 in G9).  mult_-4(H) is 9 for 75 of the 129 reps, 5 for 52, 4 for 2.  STATUS: EVIDENCE, frequent but not forced (it
is absent from some PSD structures); it plays no role in excluding type I (the near-misses keep it, with Delta w = 0).
(d) SIGN LEMMA (PROVED, elementary).  K and Pi are h-invariant, so hTh = T + Delta and hUh = U - Delta.  If T >= 0, then
for n in N = ker T: n^T Delta n = n^T (hTh) n >= 0, with equality iff n in N n hN.  So Delta is PSD on N, its radical
there is N_h, and the number of saturated directions is s = nu - dim N_h = rank(Delta | N).  Likewise Delta is NSD on
ker U (if U >= 0).  Since h Delta h = -Delta, Delta has p = rank(Delta) / 2 positive eigenvalues, hence s <= p.  Data:
rank Delta = 8 for HB_1 (s = 1 <= 4), 12 for asy_best11, 16 for the near-misses and kmilp_obj53_ambig (s = 0).
A clean form of (ii), but the bound s <= p is far from what is needed.
### E11 (16:50-17:00 UTC): a unifying conjecture, SUM14 = dim(ker T + h ker T) <= 14
STATEMENT (CONJECTURE, OPEN).  For every admissible four-star structure with T >= 0 and U >= 0:
    dim(N + hN) <= 14,   N = ker T,  h = (0 1)(2 3).
Equivalent forms: nu + s <= 14 (since dim(N + hN) = 2 nu - dim(N n hN) = nu + s); rank T - s >= 30; the parallel sum
T : hTh = T (T + hTh)^+ hTh (PSD, h-invariant, kernel EXACTLY N + hN, range = range T n range hTh) has nullity <= 14;
dim P+(N) + dim P-(N) <= 14 (even and odd projections of the kernel).
WHAT IT WOULD GIVE: at s = 0 it is (N15) (no PSD structure of nullity >= 15, O6 of AUDIT_EXCLUSIONS, open); at
nu = 14 it forces s = 0, i.e. N = hN (statement (S1)); at nu = 13 it gives s <= 1 (the saturation law of type II).
So (H-MATCH) <= SUM14 + (S2), and the 13-wall (HB_1: nu 13, s 1, sum 14) and the rank-30 h-invariant objects
(nu 14, s 0) are its two kinds of tight cases.  Like (N15) itself, it is a nonexistence-strength statement.
EVIDENCE (sat_frontier.py, numerical nullities of exact structures; distinct structures):
- all 1 184 distinct structures of the top-level corpus: T, U PSD broken (329): max nu + s = 14 (HB_1 only); list
  (N+, N-, s, nu) = (10,2,1,13), (9,2,1,12), (8,2,1,11), (7,2,1,10), (8,2,0,10), (3,2,4,9) x 256, (7,2,0,9),
  (3,2,0,5); T, U PSD h-related (726): nu <= 14 (500 of (12,2,0,14), 58 of (11,3,0,14)).
- dumps: HB_1 KHOMOG class (96 broken), asy_best11 KHOMOG class (1 036 broken of nullity >= 8, COMPLETE class):
  N+ <= 10, s <= 1, nu + s <= 14 for ALL of them, PSD OR NOT (here the bound holds combinatorially).
- U IS NECESSARY: with T >= 0 only, the obj53 class gives (N+, s, nu) = (12, 1, 15) (sum 16) and (13, 0, 15), and an
  h-invariant T-only structure of nullity 16 exists on file.
- SPECIFIC TO THE IN-LINE SWAPS (sum_test.py): for the 129 kernel-class representatives (h-invariant, nu 14),
  dim(N + gN) = 14 for g = h, (0 1), (2 3), but 15-18 for tau = (0 2)(1 3), outer flips, M, hM, (0 1)M, line
  swaps.  For broken PSD structures (HB_1, asy_best11, Z5 families) the sums for h, (0 1), (2 3) coincide.
LEMMA (PROVED, grid case).  If (l, m) is a grid pair (C4 is an isolated 4-cycle 02-03-13-12 of Gamma_S), every h-even
kernel vector n has n(02) = n(03).  Proof: rows 02 and 03 of T n = 0 read 3 n(02) - 2 n(03) = (K n)(02) and
3 n(03) - 2 n(02) = (K n)(03); K n = D^T Q D n and D n takes equal values on the letters 2, 3 (n is h-even), Q is
h-invariant, so (K n)(02) = (K n)(03); subtracting, 5 (n(02) - n(03)) = 0.  Hence for h-invariant kernels N, N is also
invariant under (0 1) and (2 3) (on h-odd kernel vectors spanned by the star differences this is immediate).
TEST RUNNING (16:57-17:37 UTC, two walks in the trivial group, sym4g.py b1 with the new option SUMOBJ: smooth
objective = the SUMT-th smallest eigenvalue of T : hTh, SUMT = 15; logs sum_hb1.log (warm start HB_1, sum 14) and
sum_z5s.log (warm start Z5s_c0_P9_1, nu 9, s 4, sum 13); saves _SUM_k.json for sum >= 15 or (s >= 2, nu >= 11)).
### E12 (17:00-17:10 UTC): two refutations, exact scope, and what they change
(a) SUM14 REFUTED at nullity 13 (exact).  The SUMOBJ walk from HB_1 (sum_hb1.log) reached at move 6447
sum_hb1_SUM_1.json (50 saved structures, all of the same type): verify_counterexample.py: admissible, T >= 0 (exact
rank 31), U >= 0 (exact rank 39), nullity 13; sum_exact.py (exact kernels): dim(N + hN) = 15, dim(N n hN) = 11, s = 2,
(N+, N-, s) = (9, 2, 2).  Twist census: the same twisted 4-cycles and pure rows as HB_1; the structure is EXACTLY
invariant under the fake involution g = h (4 6) and its kernel is g-invariant (kernel_hp_scan.py).  SCOPE: refutes the
general SUM14 (nu + s <= 14) and the law 's <= 1 at nullity 13'.  NOT touched: the nullity-14 statement (nu = 14 =>
N = hN, i.e. (S1)) and (N15).  Reading: relative to g, the involution fixing the kernel, there is no saturation at
all; the saturation count relative to h is not an intrinsic quantity (consistent with the KER-SYM picture).
(b) ODD9 REFUTED (exact) -- the target of task C.  odd9_fail_scan.log (exact gains, ranks over Q, every T, U PSD
distinct structure of the top-level corpus): 58 distinct structures with odd gain 8 beyond X_l AND beyond X_m, all
h-invariant, nullity 14 (rank 30), (N+, N-) = (11, 3), c-types (2,2) 7, (3,2) 14, (4,2) 9, (5,2) 2, (2,3) 4,
(3,3) 13, (4,3) 5, (2,4) 2, (3,4) 2; plus r7_Z5h_cold1_PSD_1.json (c = (2,2), nullity 9, odd gain 5 on both sides).
Exact certificates (verify_counterexample.py: admissible, T and U PSD with exact ranks and positive definite principal
minors; odd9_check.py: exact gains) for hv_h_c22_H30_23.json (c = (2,2): odd 8 / 8, even 1 / 1), hv_h_c22_H30_10.json
(c = (3,2)), hm3_c2_H30_1.json (c = (5,2)), r7_Z5h_cold1_PSD_1.json.  An extra h-odd kernel vector always gives odd
gain <= 8 (it has a non-constant m-odd part, otherwise it would be an odd relation inside X_l, i.e. a multiple of the
star difference).  Origin: the <h> harvests of 09:38 UTC (hv_h_*) and hm3_*; ODD9 had been validated before them, and
my 09:15 note (rank A = 11 with nullity C = 3) already showed the symptom without the conclusion being drawn.
SCOPE: refutes universal ODD9, also restricted to c = (2,2), to h-invariant structures and to nullity 14.  NOT touched:
all PSD members of <Z5, hM> on file have gains 9 / 9 (so lemma 6h, which needs ODD9 for the structure at hand, still
explains that family's ceiling 9), asy_best11, the HB_1 lineage and sum_hb1_SUM_1 (9 / 9).  The kernel classes of the
58 are all enumerated completely (55 lie in the newk1 / newk2 / reps129 classes, zero broken members; the other
three, hm3_c2_H30_1, hm3_c2_H30_2, sq8_id_disc_c22_H30_2, are singleton classes, kernel_sat_enum.py, 17:20 UTC),
so none of these ODD9 failures carries a twist.
Consequences for A: (1) the identity nu = 2 + dim N+ + s (E5, E9, section 5) assumed nullity C = 2; in general
nu = dim N+ + dim N- + s, and E9 holds under the explicit hypothesis nullity C = 2 (now a hypothesis, not a law);
(2) lemma 6h must be applied only where ODD9 and (H_g) are checked; (3) (B') no longer follows from ODD9 (still OPEN).
ARCHITECTURE of a proof of (H-MATCH) after today (every item OPEN unless marked): (KER-SYM-14) nu = 14 => ker T is
invariant under some h p; then p = id: (S2) (type I must fail U; now also with nullity C = 3 allowed); p fake: a bound
nu <= 13 for fake-invariant kernels (all data); p true and != id: lemma 6h (PROVED, under ODD9 and (H_g) for the
structure).
### E13 (17:10-17:20 UTC): (KER-SYM-13) on the whole corpus; walks stopped; exchange with Codex
- kersym13_scan.py (all 9 496 involutions p of the outer letters, numerical SVD; distinct structures; log
  kersym13_scan.log): the 653 distinct T, U PSD structures of nullity >= 13 of the top-level corpus all have a kernel
  invariant under some h p: p = id for 651 (558 of nullity 14 and 75 of nullity 13 h-invariant; 18 of nullity 13 not
  h-invariant, the Hamming-like <Z5, tau> members), the fake p = (4 6) for 2 (HB_1 and the SUM14 counterexample).
  No exception to (KER-SYM-13) in these data (family-biased as always).
- The two SUMOBJ walks were stopped at 17:09 UTC (RAM 90 % with the user's game open; the HB_1 walk only re-saved the
  same nullity-13, s = 2 type; the Z5s walk stayed at sum 13).
- Codex (message 844, after 843): withdraws universal ODD9 from his active statuses; identity under h: odd gain_l =
  odd gain_m = 11 - nu_-, nu_- = dimension of the h-odd kernel (so gains 8 and 5 <-> nu_- = 3 and 6); exact form
  even residual gain_l = 12 + c_l - nu + d_l with d_l = 9 - odd gain_l.  Data for him (exact odd kernel bases of
  hv_h_c22_H30_23 and hv_h_c22_H30_10): hmatch_tools_2026-10-15/for_codex/odd9_counterexamples_2026-10-15.json.
- NEW SEARCH TARGET suggested by the ODD9 failures: nu = N+ + N- + s; the broken HB_1 lineage sits at
  (10, 2, 1) = 13; one extra h-odd relation (N- = 3, as in the 58 ODD9 failures) on a broken structure would give 14,
  i.e. a counterexample to (H-MATCH).  Walk option ODDW (below) rewards the third odd eigenvalue going to 0 while the
  matchings stay broken.
### E14 (17:14-17:20 UTC): a second, independent broken lineage at the 13-wall, again fake-symmetric
Walk ODDW (new sym4g.py option: on broken PSD structures, reward the third smallest eigenvalue of the h-odd sector of
T going to 0; ODDW = 3, trivial group, HBREAK + HMATCH; logs oddw_hb1.log from HB_1 and oddw_o9b.log from the ODD9
failure hv_h_c22_H30_23.json; the first o9 run with HBSAVEMIN = 14 did not save, the deterministic rerun o9b with
HBSAVEMIN = 13 reproduced it).  At move 161 of o9b: oddw_o9b_HB_1.json, EXACT (verify_counterexample.py): admissible,
T >= 0 rank 31, U >= 0 rank 39, nullity 13, c = (2,2) (grid lineage, t = (8,8)), both halves twisted along ONE
4-cycle each (l: (5,12,13,11), m: (4,13,8,5)), one pure row per side, (N+, N-, s) = (9, 2, 2) (sum_exact.py),
odd gains 9 / 9 (the extra odd relation of the seed is lost when the matchings break).  The structure is EXACTLY
invariant under the fake involution g = h (5 13) (5, 13 non-mates; kernel_hp_scan.py), and (5 13) is the common
reflection of the two twisted 4-cycles that exchanges M_0 and h(M_1) (resp. M_2 and h(M_3)).
READING: two independent lineages (HB_1: c = (5,2), t = (10,10), g = h (4 6); this one: c = (2,2), t = (8,8),
g = h (5 13)) stop at 13 in the same way: a twisted 4-cycle on each side, the two cycles sharing a reflection p, the
whole structure invariant under the fake g = h p.  Candidate statement (FAKE-13, OPEN): if Gamma is invariant under
g = h (y z) with y, z non-mates and T >= 0, then nullity <= 13.  Known: gTg = T + D with D = K - gKg of rank 2; if
N = gN then D N = 0, i.e. N is orthogonal to the two letter-sum vectors spanning range D (one condition on g-even, one
on g-odd kernel vectors); Codex (10:57 UTC) showed that this linear condition alone does not cap the nullity at 13, so
a proof needs combinatorial input.
LEMMA (PROVED, elementary; makes E14 automatic).  Let p = (y z) with y, z outer non-mates, g = h p, Gamma g-invariant.
Then M_1 = s_m p (M_0) as sets of letter pairs (g maps {0, w} to {1, s_m p(w)}), so h(M_1) = p(M_0), and the l-half is
h-related iff p(M_0) = M_0 iff {y, z} is in M_0 (if {y, a} is in M_0 with a != z, p sends it to {z, a}, which cannot be
in M_0 as a is already matched to y).  Otherwise M_0 contains {y, a}, {z, b} (a != b, a, b not in {y, z}) and
M_0 Delta h(M_1) is exactly the 4-cycle y - a - z - b - y, of which p is the reflection fixing a and b.  Same on the
m-side with M_2.  Moreover Delta = Gamma - h Gamma h = Gamma - p Gamma p (h Gamma h = p (g Gamma g) p), supported on
the rows and columns of the eight labels {s y, s z : s = 0..3} (so rank Delta <= 16; HB_1: 8).
### E15 (17:25-17:35 UTC): ties act on BOTH parities; why the extra odd relation dies when the matchings break
LEMMA (PROVED, one line).  Every h-homogeneous kernel vector n (n in N n hN, even OR odd) satisfies Delta n = 0
(hTh n - T n = Delta n).  Hence a PURE twisted row {0, y} (Delta-row supported in L_0, equal to e(0y+) - e(0y-))
forces n(0y+) = n(0y-) for every n in N_h, not only for the even ones: an h-odd relation with l-odd profile beta
(n(0w) = beta_w = -n(1w)) must have beta_{y+} = beta_{y-}.  The star differences (beta constant, resp. 0) always pass.
APPLICATION (exact data, hmatch_tools_2026-10-15/for_codex/odd9_counterexamples_2026-10-15.json): the extra h-odd
relation of the ODD9 failure hv_h_c22_H30_23 has l-odd profile beta = (4: -24, 5: 3, 6: 2, 7: 16, 8: 23, 9: 1, 10: 1,
11: -13, 12: -2, 13: -7) and m-odd profile e = beta o pi with pi = (4 12)(5 13)(8 11) (an l <-> m correspondence of
the outer letters).  Its broken descendant oddw_o9b_HB_1 has a pure l-row tying 5 and 13 (cycle (5,12,13,11)) and a
pure m-row tying 13 and 5 (cycle (4,13,8,5)); beta_5 = 3 != beta_13 = -7, so the relation cannot survive: this is why
the odd gain went back to 9 / 9 when the matchings broke.
CONSEQUENCE FOR (H-MATCH) (counting, c(m) = 2, s = 0): nu = dim N+ + dim N-; each independent tie lowers the rank of
the u-profile of N+ (so dim N+ <= 12 - tau), and every extra odd relation (dim N- - 2 of them) must satisfy all the
ties.  A broken structure of nullity 14 with s = 0 therefore needs, for every tau independent ties, at least tau extra
odd relations satisfying them (or full compensation, tau = 0: type I).  The data: extra odd relations exist only in
h-related structures; under a twist they die (o9b), so far.

## 6. STATUS OF A at 17:30 UTC (replaces section 5)
PROVED: tie lemma, now for every h-homogeneous kernel vector of either parity (E2, E15); telescoping (E3); G21; sign
lemma (Delta PSD on ker T with rank s, NSD on ker U; E10 d); grid lemma (h-even kernel vectors take equal values on 02
and 03, so h-invariant grid kernels are also (0 1)- and (2 3)-invariant; E11); fake-transposition lemma (h (y z)
invariance forces each half to be h-related or twisted along exactly one 4-cycle through y, z; E14); E9 linear algebra
(under the now explicit hypothesis nullity C = 2); lemma 6h (true symmetries, under ODD9 and (H_g) for the structure).
REFUTED (exact, scope stated): ODD9 universal (58 rank-30 h-invariant objects with odd gain 8, one nullity-9 object
with gain 5; E12); SUM14 in general and 's <= 1 at nullity 13' (s = 2 at nullity 13, two lineages; E12, E14);
universal KER-SYM (nullity 9, E7); 'at most one saturation' for all nullities (E4).
OPEN, consistent with all data: (S1) nu = 14 => N = hN; (KER-SYM-13/14) (653 / 653 at nullity >= 13); (FAKE-13)
ker T invariant under a fake h p => nullity <= 13 (the kernel version is what (S1) needs; the data only show
structure-invariant cases: two lineages, walks in <h (4 6)> and <h (5 13)> never above 13); (S2) N = hN,
nu = 14, PSD => no twist (type I fails U globally in the only class where it exists); (N15).
(H-MATCH) <= (S1) + (S2) [and (S1) <= (KER-SYM-14) + (FAKE-13) + lemma 6h-type bounds for true p, which are empty in
the nullity-14 data: every PSD nullity-14 kernel on file is h-invariant].
NOT UNDERSTOOD: why U excludes type I (global, kernel-class specific); why fake symmetry costs exactly one relation
(the rank-2 defect D gives the right condition but linear algebra alone does not cap at 13, Codex 10:57 UTC).
### E16 (17:35 UTC): what the fake-transposition defect asks of the kernel (PROVED, linear algebra)
g = h (y z), y' = y^1, z' = z^1, Gamma g-invariant, N = gN.  K = inc^T Q inc (inc = letter-label incidence on S, Q the
letter block of the windmill inverse, Q = alpha I + beta Mt + gamma J), so D = K - gKg = inc^T (Q - gQg) inc with
Q - gQg = beta (Mt - g Mt g) = beta x (signed 4-cycle y y' (+), y' z (-), z z' (+), z' y (-)), rank 2; inc^T is
injective on letter vectors, so D n = 0 <=> sigma_y(n) = sigma_z(n) and sigma_{y'}(n) = sigma_{z'}(n), where
sigma_a(n) = sum of n over the labels containing the letter a.  For g-even n the first equality is automatic and the
condition is sigma_{y'}(n) = sigma_{z'}(n); for g-odd n the second is automatic and the condition is sigma_y(n) = 0.
Side relations pass automatically: a component of H_l (or H_m) meeting {y, y', z, z'} is a union of lines mapped by p
to a union of lines through the same letter, hence contains all four letters, and sigma_w(kappa_C) = 2 [w in W].
So the cost of fake symmetry falls on the MIXED relations: with c(m) = 2 and the u-profile onto, the g-even mixed
relations n_b = (b, L b, ...) need (e + L)_{y'} = (e + L)_{z'} as rows (sigma_w(n_b) = 2 (b_w + (L b)_w)), one
linear condition on L of the same type as the compensation identities of E9.
### E17 (17:57 UTC): outcome of the evening walks (all numerical searches, nothing complete)
- ODDW from HB_1 (oddw_hb1, stopped 17:18 UTC): the third odd eigenvalue went down to 0.095, but only at nullity 11;
  no broken structure with an extra odd relation.
- ODDW from the ODD9 failure hv_h_c22_H30_23 (oddw_o9b, 2 400 s, 22 268 PSD visits): broken structures never above
  nullity 13 (the single distinct saved type, (N+, N-, s) = (9, 2, 2), fake h (5 13)); the 49 visits at nullity 14 are
  the h-related neighbourhood of the seed (penalised); no broken structure with an extra odd relation.
- Fake group <h (5 13)> from oddw_o9b_HB_1 (fake513, 1 800 s, 6 839 PSD visits, FAKEOK): best exact nullity 13
  (6 792 visits at 13).  Together with the 5 500 PSD visits in <h (4 6)> (10:44 UTC): (FAKE-13) never violated.
- No counterexample to (H-MATCH) found.  Summary logs: hmatch_tools_2026-10-15/{sum_hb1,sum_z5s,oddw_hb1,oddw_o9b,
  fake513}_summary.log.
