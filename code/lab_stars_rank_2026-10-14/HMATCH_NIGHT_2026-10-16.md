# (H-MATCH), single target, 16/10/2026 02:40 - 08:00 UTC (LAB; Codex on the proof side)

Frame agreed by the user at 02:40 UTC ("Ok vasy. parle avec codex"):
  - one target, (H-MATCH): every four-star block with T, U >= 0 and nullity >= 14 has M_1 = h(M_0) and M_3 = h(M_2);
  - only two outcomes count:
    * a written proof;
    * an exact broken block (star matchings not h-related, T, U >= 0, nullity >= 14).
  - At 08:00, with neither outcome, the local route is declared exhausted.
(H-MATCH) => no Conway is proved and reviewed (H_MATCH_REDUCTION_2026-10-15.md, section 2).

## 1. What was already known (not redone)
- Cold walks in the true-symmetry families h(4 5), h(4 5)(6 7), h(4 6)(5 7) and hM (hs_*.log, 15/10 morning, 22 to 37
  minutes each) never reached T, U >= 0.  My 02:45 relaunch of three of them was redundant and was stopped after a few
  minutes; Codex was told (message 866).
- Twist walks (tw_*.log), low-rank walks with HREQ (hq_low_*.log), HBREAK / HMATCH / HIDDENPEN walks: broken PSD
  structures reach nullity 13 at most (the 13-wall), and 11 at most without any h-type symmetry.
- 287 complete kernel classes of nullity-14 objects: only obj53 has broken members, none PSD.
- KHOMOG classes of HB_1 and asy_best11 (complete): broken => nullity <= 13 there.

## 2. New exact sweeps tonight (SAT enumerations are complete but carry no certificate)
- Fake two-generator group <h(4 6), h(8 10)>: no invariant admissible structure (SAT).
- Case I (the h-average has a 12-dimensional even kernel, i.e. rank A = 10): harvest of new h-invariant nullity-14
  objects (hmatch_tools_2026-10-16/harv/, warm starts c33 and c55, 45 min each), then complete enumeration of every new
  kernel class.  A PSD broken member would be a counterexample.
- Case II with one saturated direction: the 80 distinct kernels of the h-invariant T, U PSD structures of nullity
  exactly 13 (hmatch_tools_2026-10-16/nu13/), each class enumerated completely (ksat_nu13.log).  A member of nullity 14
  with broken matchings and T, U PSD would be a counterexample.
- Case II near every known broken lineage:
  * 119 distinct broken T, U PSD structures of nullity >= 11 on file;
  * they have 16 distinct homogeneous parts N n hN;
  * 8 of these are new (the dump members lie inside classes already enumerated);
  * KHOMOG classes of the 8 (hmatch_tools_2026-10-16/brk/, khomog_brk.log).
RESULTS: see section 4 (filled at the end).

## 3. Proof side (analysis only; nothing proved beyond what is listed)
Notation: T = T_0 - Delta/2 and U = U_0 + Delta/2, with T_0, U_0 the h-averages and Delta = Gamma - h Gamma h.
In the basis (h-even, h-odd): T_0 = diag(A, C) and U_0 = diag(A', C'), with A + A' = 7 Pi_+ and C + C' = 7 Pi_-.
Delta is off-diagonal, with block D.
- T >= 0 iff D/2 = A^{1/2} K C^{1/2} with ||K|| <= 1.  U >= 0 iff D/2 = A'^{1/2} K' C'^{1/2} with ||K'|| <= 1.
- nu(T) = nu(A) + nu(C) + n_1(K), where n_1(K) is the number of singular values of K equal to 1.  (Elementary block
  fact.)
- For a saturated direction (K c = a): x = (A^{-1/2} a, C^{-1/2} c) lies in ker T, and the U-energy of h x equals
  7|Pi x|^2 - x^T Delta x, which is >= 0 automatically.  The pencil gives no contradiction by itself: in the scalar
  model, T and U are both PSD and singular whenever alpha + gamma <= 7.
- The segment T_t = T_0 - t Delta/2, t in [-1, 1], stays PSD by convexity; its interior nullity is dim(N n hN), and the
  endpoints gain n_1(K).  A counterexample needs either dim(N n hN) = 14 with Delta != 0 (case I), or n_1(K) >= 1 with
  dim(N n hN) = 13, or n_1(K) >= 2 with dim(N n hN) = 12 (the HB_1 lineage has (12, 1)).
No mechanism forcing n_1(K) <= 13 - dim(N n hN) was found.

## 4. Results and verdict
- 03:05 UTC, nullity-13 classes (ksat_nu13.log):
  * 80 distinct kernels of the h-invariant T, U PSD structures of nullity exactly 13; all 80 classes enumerated, 79
    COMPLETE (newk_3 = c1_G1_c55_PSD_2 stopped after 22 729 structures in 300 s);
  * 41 979 structures in all, ZERO with broken star matchings, PSD or not;
  * 314 PSD members of nullity 14, all h-related; non-PSD members reach nullity 17.
  So no broken structure at all exists in these classes: the 13-wall holds there even without positivity.
- Profile of every broken PSD structure on file (broken_profile.py, 119 distinct, nullity 11-13):
  * nu(C) = 2 always, rank D = 4 (6 at most);
  * n_1(K) <= 2, and the decompositions met are (13 = 10 + 2 + 1) and (13 = 9 + 2 + 2);
  * ||K'|| = 0.95-0.99 everywhere, i.e. U is nearly tight.  This is a selection effect of the walks, with no monotone
    link to n_1.
  Identity used: U >= 0 iff ||Phi_A K Phi_C|| <= 1, with Phi_A = (A~ (7 - A~)^-1)^(1/2), A~ = Pi_+^(-1/2) A Pi_+^(-1/2),
  and Phi_C likewise.
  CORRECTION (Codex, message 869): in raw coordinates A + A' = 7 Pi_+, not 7I, even orthogonally to the four stars.
  Example: q = sum_c (e_{c,y} - e_{c,y^1}) has Pi q = (2/3) q.  The identity holds only after the congruence by
  Pi_+^(-1/2) and restriction to its support.  On the odd sector minus the two odd stars, Pi_- = I.  The numerical
  profile above was computed from the raw blocks of U directly and is unaffected.
- 03:11 UTC, KHOMOG classes of the 8 not yet enumerated broken lineages (khomog_brk.log):
  * the lineages are fake46_b1, fake46_hb, fake513, hm2_a, oddw_o9b_HB_1, oddw_smoke and sum_hb1_SUM_1;
  * the imposed N n hN has dimension 11 or 12; the classes have 672 to 6 852 structures; ALL 8 are COMPLETE;
  * in every class, the broken members have nullity <= 13, PSD or not.  No broken structure of nullity 14 exists in any
    of them.
- Broken nullity >= 14 structures on file (obj53 class and near53 near-misses, 775 distinct):
  * all have T >= 0 numerically, and 295 also have C' >= 0;
  * the best lambda_min(U) is -0.0486 (near53/n_45.json: nu 14, A' >= 0, C' >= 0, U fails only through the
    coupling D).
  Sent to Codex for his re-pairing test (message 870).
- Codex (871-874): the re-pairing route (change the outer mate pairing, Gamma fixed) is CLOSED for both seeds.
  He uses U(M) <= 4I + Gamma for every pairing M, on all of R^44, with integer witnesses:
  * n_45: Rayleigh quotient <= -4 - 5/874;
  * b_29: w^T (4I + Gamma) w = -96 with B w = 0.
  So lambda_min(4I + Gamma_S) >= 0 is a necessary condition for U >= 0 and is a cheap filter.
- U-repair walks from n_45 / n_1 (urep2 + HREQ, hard and then soft plateau SOFTPLAT = 0.1, 40 000 + 14 000 moves): the
  record lambda_U stayed at -0.04858.  The walks stay inside the near-miss family; stopped.
- 03:49 UTC, nullity-12 classes (13 distinct h-invariant T, U PSD kernels; ksat_nu12.log):
  * 10 COMPLETE, 3 stopped at 600 s (newk_1 = c1_G1_c55_PSD_3, newk_10, newk_12); 165 959 structures;
  * broken members have nullity <= 13: 4 PSD at 12, 4 PSD at 13, 43 353 non-PSD at 12, 826 non-PSD at 13;
  * every structure of nullity 14 to 17 (57 PSD, 35 570 non-PSD) has h-related matchings.
- 03:58 UTC, Case I: 104 new h-invariant nullity-14 objects harvested; 100 of them define NEW kernel classes (301 were
  known).  All 100 classes enumerated COMPLETELY (17 400 structures, 400 PSD): not a single broken member.
- Codex (875 answer):
  * no realistic short-term proof of (H-MATCH) is in sight.  The abstract contractions allow the broken case; what is
    missing is a binary / C1 / C2 argument that excludes their simultaneous saturation;
  * scope of his certificates: they cover only the two graphs n_45 and b_29 (every pairing M, every relabelling), not
    the whole obj53 class;
  * proposed next step: write up the reduction (theorems, the conditional implication, finite evidence separated);
    then a GLOBAL pilot.  The 21 four-star blocks at one vertex must be restrictions of one 84-label Gamma, and every
    local kernel vector q extends by zero, which imposes on the 40 remaining rows R:
      8 Gamma_RS q = 2 (1^T q) 1_R - B_R^T (3I + M) B_S q, i.e. Gamma_RS q = 0 when B_S q = 0.
    Target: the coexistence of the >= 4 broken blocks per vertex forced by G18.  Bounded pilot first; no feasibility
    claimed.
- 04:46 UTC, second harvest (seeds Z5h c22 and h42): 218 objects, 215 NEW kernel classes (401 known before).  All 215
  enumerated COMPLETELY (14 055 structures, 455 PSD): no broken member.
- TOTAL of the night (complete SAT enumerations, no certificate):
  * 416 kernel classes, 412 complete, about 253 600 structures;
  * nullity-14 classes: 315 new ones, no broken member at all;
  * nullity-13 and nullity-12 classes, and the homogeneous classes of every known broken lineage: broken members only
    up to nullity 13.
  So no broken structure of nullity >= 14 exists in any of them, PSD or not.
  The four stopped classes (G1 c55 and relatives) are being rerun with 6 600 s caps (ksat_big_*.log).
- 05:05 UTC, big_a (the nullity-13 class of c1_G1_c55_PSD_2): COMPLETE, 70 336 structures (1 133 s), no broken member.
  The nullity-13 sweep is therefore 80 / 80 complete, 89 586 structures, with no broken structure at all.
- 06:36 UTC, two of the three large nullity-12 classes, rerun with 6 600 s caps; both still NOT complete:
  * big_b (class of c1_G1_c55_PSD_3): 344 891 structures; broken members up to nullity 13 (6 at 13, all non-PSD);
  * big_c/newk_0 (nu12/newk_10): 312 191 structures; broken members up to nullity 13 (1 128 at 13, non-PSD); 48 PSD
    members of nullity 14, all h-related.
  So no broken structure of nullity >= 14 appears in about 657 000 further structures.  The last class (nu12/newk_12,
  rerun as big_c/newk_1) started at 06:36 UTC with the same cap and ends at about 08:27 UTC.
- 05:15 UTC, a small structural fact behind the rigidity (profile_ties.py, numerical 1e-7).
  * In all 892 distinct T, U PSD structures of nullity >= 14 on file (853 grid, 39 non-grid), no two labels of the
    same star have identical kernel profiles.
  * A PURE matching twist (Delta-rows e_{0a} - e_{0b} inside L_0) preserves the kernel only if x(0a) = x(0b) for every
    kernel vector.
  * So no pure twist exists in the class of any known object.  Broken class members, as in obj53, need combined
    twists (l-block + cross + m-block).
  This is data, not a lemma.  A proof that same-star profiles are distinct at nullity >= 14 would exclude pure twists
  in Case I, and only them.
  Threshold (profile_ties_all.py, whole corpus, PSD or not):
  * same-star profile ties are COMMON at every nullity from 6 to 13, PSD or not (for example 100 of the 126 TU
    structures of nullity 13, and the HB_1 lineage);
  * they NEVER occur at nullity >= 14 (578 TU, 60 + 720 + 1 T-only at nullity 14, 15, 16, 2 non-PSD), the broken obj53
    members of nullity 14-15 included.
  So the separation of same-star labels by the kernel switches on exactly at the H-MATCH threshold, independently of
  positivity.  It is unexplained.  Distinct-profile counts at nullity 14 are a candidate first lemma towards
  rigidity, but they do not exclude combined twists.
- Codex (msg after 877, commit 431c6c7): a PROVED criterion for pure rematchings.
  * Setting: a star with matching P, and W = proj_star(ker T) n ker(P + I).
  * If replacing P by P' alone keeps T PSD, then P' v = -v for every v in W, even when the kernel or the rank changes.
    Proof: for q in ker T with restriction v, q^T T' q = -v^T (I + P') v <= 0.
  * Switch form: T' = T - (u v^T + v u^T) PSD forces u|ker and v|ker to be both 0, or nonzero and negatively
    proportional.
  * Applied to two seeds (urep100, hv_h_c22_H30_23): in each of the 4 stars the only opposite pairs are the 6 old edges,
    so no pure rematching of any star is possible, whatever the new kernel.
  * Scope: the criterion is general, the blocking is proved for those two seeds only; combined modifications stay
    open.
- Codex, constructive side (messages of 07:15 and 07:45; commits up to 1d7fae3; his results, not re-audited by me):
  * HB_1's unlabelled graph, relabelled ("promoted"), gives blocks with T of rank 30 (nullity 14) and U of rank 39;
  * all 120 admissible geometries he found at nullity >= 14 keep (H-MATCH);
  * the promoted block does NOT extend: the outer vertex (4,6) has no compatible column (exact Farkas certificate);
  * he is now attempting a joint construction towards a 99-vertex graph (44 -> 84 -> 99).  He relays the user's
    reminder not to stop at closing families.  No srg(99) has been built so far.
- 07:48 UTC, final state of the class sweeps:
  * 416 classes, 413 complete, about 853 000 structures; no broken structure of nullity >= 14 in any of them, PSD or
    not;
  * counted without double counting: each stopped class counts once, by its largest run;
  * the last large nullity-12 class (nu12/newk_12) is still running past 08:00 (ends about 08:27 UTC).  Its 600 s
    run had 40 063 structures, with broken members only up to nullity 13.

## 5. Reading of the night
- The 13-wall holds in every class we can enumerate completely.  In most classes there is no broken structure at all,
  even without positivity: the kernel determines the structure up to h.  Broken members appear only in classes with a
  very large kernel symmetry group (obj53: |G_N| = 1 920).  There, positivity kills them, through U.  The closest one
  misses by lambda_min(U) = -0.0486, and Codex's witness shows that no relabelling repairs it.
- No mechanism was found that forces the wall:
  * the pair of contractions (T and U), the sign lemmas and the side-relation lemma are all satisfiable by abstract
    data of nullity 14 with broken matchings;
  * what kills the actual structures is combinatorial rigidity (sparse +-1 row differences orthogonal to the kernel
    exist only for very symmetric kernels), together with U in those rare cases.
- So (H-MATCH) remains a well-supported conjecture.  Its proof needs either an idea we do not have or an exhaustive
  enumeration whose size we cannot estimate: PSD four-star structures are reached only near symmetric seeds, so the
  space cannot be sampled uniformly.

## 6. Verdict (08:00 UTC, as agreed)
Neither outcome has been reached: no proof of (H-MATCH), and no exact broken PSD block of nullity >= 14.  Per the
agreed frame, the local route is declared exhausted.
The night strengthened the evidence: the 13-wall holds in every class we can enumerate, and pure rematchings are
blocked by Codex's criterion.  It brought no mechanism.  Options for the user:
  1. write up the reduction (C1_REDUCTION_OUTLINE_2026-10-16.md);
  2. Codex's global or constructive line: the coexistence of the >= 4 forced broken blocks per vertex, or his
     extension attempt towards 99 vertices;
  3. stop C1 or move to a bounded project (C2 without computation).
