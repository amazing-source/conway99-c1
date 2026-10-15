# (H-MATCH): a local symmetry law that would exclude Conway (LAB, 15/10/2026, ~06:00 UTC)

STATUS (corrected 15/10, 10:00 UTC): (H-MATCH) is OPEN and remains a CANDIDATE ROUTE. The 07:40 wording 'abandoned as
a target' is withdrawn (the user rejected it; nothing refutes the law). Its evidence is family-biased; local searches
have not decided it (the srg(243) comparison, corrected at 08:00, does not test it). Work on it continues (section 6,
task T3; Codex has T2 = ODD9). KEPT: the implication (section 2) and its contrapositive G18 (>= 4 broken blocks per
vertex of a Conway graph, modulo L10). Last results: the largest kernel
class (15 objects) enumerated COMPLETELY (24 144 structures, 96 PSD, none broken), so all 129 kernels are settled
(complete SAT or MILP); sub-kernel sweeps stopped after 189 runs (760 PSD nullity-14 structures, all h-related).

Status: the IMPLICATION below is a proof. Its last step needs ONE of: L8 = "no Hamming point" (catalogue C2, status P,
Codex note 105), Makhnev 1988 "not grid-full" (C1, literature), or rho <= 191 (P part of C6). Independent adversarial
review (06:45 UTC): no error in the proof; status and evidence wording corrected below. The local law (H-MATCH)
itself is OPEN. Evidence is biased (section 3); a matching-broken PSD structure of nullity 13 exists, one below the
threshold; U >= 0 is essential (with T >= 0 alone the law is false, section 3).

## 1. Setting and statement

Four-star structure as in stars_rank.py: letters 0..13, mates y and y^1, lines l = {v,0,1}, m = {v,2,3}, outer letters
4..13; S4 = the 44 labels meeting {0,1,2,3}; Gamma = admissible graph on S4 (C1, C1', C2); T = 3I - Gamma - K,
U = 7 Pi_S - T; "PSD" = T >= 0 and U >= 0; nullity = dim ker T. h = (0 1)(2 3) on letters (outer letters fixed),
acting on labels.

For a star letter a in {0,1,2,3} the matching M_a is the set of pairs {y,z} of letters with {a,y} ~ {a,z} in Gamma.
By (C1) every label {a,y} has exactly one Gamma-neighbour in the star L_a, so M_a is a perfect matching of the 12
letters other than a, a^1. All 12 labels {a,y} lie in S4, so M_0..M_3 are fully visible in a four-star structure.

(H-MATCH) [OPEN]: every PSD four-star structure of nullity >= 14 satisfies M_1 = h(M_0) and M_3 = h(M_2), i.e.
{0,y} ~ {0,z} <=> {1,h(y)} ~ {1,h(z)} and {2,y} ~ {2,z} <=> {3,h(y)} ~ {3,h(z)}.

(H-INV) [OPEN, stronger]: every PSD four-star structure of nullity >= 14 is h-invariant. (H-INV) => (H-MATCH).

## 2. Proposition: (H-MATCH) => there is no srg(99,14,1,2)

Let X be a Conway graph and v a vertex. Its 14 neighbours form 7 lines {v,a,a^1} (lambda = 1), its 84 non-neighbours
are the labels {a,y} (non-mate pairs of neighbours; mu = 2), and N(a) \ {v,a^1} = the 12 labels {a,y}, on which
X induces a perfect matching M_a (lambda = 1). M_a depends only on X and v, not on a second line.

(i) For lines l != m' through v, label the letters so that l = {v,0,1} and m' = {v,2,3}. The induced graph on the 44
labels meeting l u m' is an admissible four-star structure, PSD, of nullity >= 14 (T_S is a principal block of
T = 7 P_V, T^2 = 7T, rank T = 30; U likewise; stars_rank.py docstring, CONWAY_CONSTRAINTS G1). On the letters
other than 0, 1 the map h of this labelling is the transposition s(m') of the two letters of m'. So (H-MATCH) at the
pair (l, m') says: M_{a^1} = s(m')(M_a) for the letters a, a^1 of l.

(ii) Take two lines m', m'' != l. Then s(m')(M_a) = M_{a^1} = s(m'')(M_a), so M_a is invariant under the product
s(m') s(m'') (two disjoint transpositions).

(iii) Claim: M_a pairs every letter y with its mate y^1. Suppose {y,z} in M_a with z != y^1. The lines m_y of y and
m_z of z through v are distinct and both differ from l. Choose a line m''' not in {l, m_y, m_z} (7 lines). By (ii)
M_a is invariant under s(m_y) s(m'''), which maps y to y^1 and fixes z. So {y^1, z} is in M_a as well: the label {a,z}
has two neighbours {a,y}, {a,y^1} in N(a), i.e. the edge a-{a,z} lies in two triangles, contradicting lambda = 1.

(iv) Apply (iii) to all 14 letters. For any two lines l = {v,a,a^1}, m = {v,y,y^1} through v the four labels
{a,y}, {a,y^1}, {a^1,y}, {a^1,y^1} form the 4-cycle given by M_a, M_{a^1}, M_y, M_{y^1}; together with v, a, a^1,
y, y^1 they span a 3 x 3 grid (rows {v,a,a^1}, {y,{a,y},{a^1,y}}, {y^1,{a,y^1},{a^1,y^1}}; it is induced: the two
diagonals of the 4-cycle are non-edges, otherwise an edge {a,y}-{a,y^1} would lie in two triangles). So all 21 pairs
of lines at v lie in grids: v is a Hamming point. This contradicts L8 (no Hamming point; Codex note 105, also SAT,
catalogue C2) and L10 (at most 17 grids per vertex, C3). Applied at every vertex, X would be grid-full (231 grids),
contradicting Makhnev 1988 (C1) and rho <= 191 (C6).

Only (H-MATCH) at the 21 pairs of ONE vertex is used. Contrapositive (PROVED modulo L8): in a Conway graph every
vertex has a pair of lines whose four-star block is a PSD structure of nullity >= 14 with M_1 != h(M_0) or
M_3 != h(M_2) (in the labelling of that pair). [Makhnev alone gives this at one vertex at least; rho <= 191 alone at
18 vertices at least.] No such structure has ever been found (section 3).

Quantitative form (PROVED modulo L10, at most 17 grids per vertex, catalogue C3): for a line l at v let
Q_l = {m' : M_{a^1} = s(m')(M_a)} (the l-half of (H-MATCH) at (l, m')). If |Q_l| >= 3, the argument of (iii), with
the double transpositions s(m_y) s(m''') taken inside Q_l, shows that M_a and M_{a^1} pair y with y^1 for every y on a
line of Q_l. Let E_H be the set of pairs {l, m} at v where both halves hold. A pair of E_H whose two lines have E_H-degree
>= 3 is a grid. If |E_H| >= 18, every line has E_H-degree >= 3 (a line of degree <= 2 misses >= 4 of the 21 pairs),
so v lies on >= 18 grids, contradicting L10. Hence at every vertex of a Conway graph AT LEAST 4 of the 21 pairs of lines
have a four-star block (PSD, nullity >= 14) whose star matchings are not h-related.

Variant of the Proposition: (H-MATCH) at the 15 pairs among six lines l_1..l_6 at v already makes the matchings of
their 12 letters mate-aligned (in step (iii) use the double transpositions inside the six lines; if y is on the seventh
line, argue with the other letter z of the pair; the two letters of the seventh line are then paired together), hence
15 grids among the six lines. Applying kk5 (catalogue C10, status M, DRAT certificate: five lines pairwise in grids
force the grid on the other two) to each of the six 5-subsets gives the grids (l_i, l_7): v is a Hamming point,
contradicting L8. [kk6 would give the contradiction directly, but kk6 is status S (1970 cadical calls, no certificate
kept, NOTE_NIGHT section 14).]

## 3. Evidence (15/10; PSD tests and nullities of the search tools are numerical, double precision; "complete" =
cryptominisat UNSAT, no certificate; exact checks are marked)

- The saved files of numerical nullity >= 14 (806 files, 429 DISTINCT structures before 06:00 UTC, among them the
  331 rank-30 objects; hscan.py skips files storing a "structures" list) are all h-invariant (hscan, 06:00 UTC).
  Every one lies in a family containing h (G1 = <(0 1)M, (2 3)M> contains (0 1)(2 3); <h>; Z5h) or a short
  trivial-group walk from an h-invariant seed: sq8_id_disc_c22_H30_2.json (05:43 UTC, 16 edges from its Z5h seed,
  exactly PSD, rank 30) is h-invariant although h was not imposed. Families without h: Z5M = <Z5, (0 1)M> enumerated
  completely (16 PSD, nullity 13 max); <Z5, (0 1)> has no admissible structure (complete); <Z5, hM, (0 2)(1 3)>
  (order 20, no h): 130 structures, none PSD (complete); Z5hM, Z5sM enumerations running.
- Max numerical nullity over all saved files (mscan, ~1300 files, not the 477 579 archived visits): PSD with matchings
  NOT h-related: 10 before 06:00 UTC; PSD h-broken but matchings h-related: 13 (nl_Z5M family); T >= 0 only, matchings
  broken: 13 (now 14, see the kernel MILP below); not PSD, matchings broken: 12 (now 14).
- 06:00 UTC: the walk hm_id_c22 (identity group, b1 mode, HBREAK + HMATCH, warm start from a rank-30 Z5h object) found
  PSD structures with the matchings NOT h-related and nullity 13 (hm_id_c22_HB_1.json: T and U exactly PSD (checked by
  the reviewer), rank 31, 60 h-asymmetric pairs (the json field 'hasym': 16 counts star pairs only), c = (5,2),
  t = (10,10), class 2 3 7 47). One relation short of the threshold 14. All 450 HB files of the walks are this structure
  or near copies (same spectrum): the walks are stuck there.

- Kernel split (numerical, hmatch_tools_2026-10-15/hparity.py, 06:20 UTC; confirmed by the reviewer): for ALL 331 rank-30 objects, ker T = 12 h-even
  + 2 h-odd dimensions, the h-odd part being only the two star differences 1_{L_0} - 1_{L_1}, 1_{L_2} - 1_{L_3}: the
  ten non-trivial relations are all h-even, and the h-odd compression of T has rank 20 (= 22 - 2). For the broken
  nullity-13 structure: h-even compression nullity 10, h-odd 2. In block form T = [[A, B], [B^T, C]] (E_+, E_-), with
  rank C = 20 one has nullity T = 2 + nullity(A - B C^+ B^T), and B = 0 iff the structure is h-invariant.
- The h-odd compression C has nullity exactly 2 (the star differences) for 300/300 random admissible structures
  (no positivity) and for all but one of 126 saved files (hmatch_tools_2026-10-15/hodd_rank.py). Whenever
  nullity C = 2, ker C is contained in ker B (the star vectors lie in ker T), so for EVERY such structure, PSD or not,
  nullity T = 2 + nullity(A - B C^+ B^T); for h-invariant ones (B = 0) nullity T = 2 + nullity A, i.e. nullity 14
  <=> the 22 x 22 quotient matrix A (h-orbits of labels) has rank 10. Reformulation only, no proof.
- Local exhaustive neighbourhood of hm_id_c22_HB_1 (enum_local.py, 12 free labels on the lines {4,5}, {6,7}, COMPLETE,
  1091 structures): nullity 14 occurs 4 times (2 PSD), always with h-related matchings and all ten outer transversals
  on both lines (hmatch_tools_2026-10-15/show_match_loc12_nul13plus.log); every structure with M_1 != h(M_0) there
  has at most 8 outer l-transversals (twist_trans_loc12.log; max nullity 13).
  This is not a general lemma: a SAT model with all ten outer l-transversals (and the two cross ones) and
  M_1 != h(M_0) is satisfiable (twist_sat.py), so any obstruction is spectral, not combinatorial.
- Z5s = <Z5, (0 2)(1 3)> (no h): 197 764 invariant structures in 2 h (not complete), 116 PSD, max nullity 13.
- 07:52 UTC: <Z5, hM> (no h): 143 390 structures in 2 h (not complete), 72 PSD, max nullity 9; <Z5, (0 2)(1 3)M>
  (no h): 164 907 structures (not complete), 26 PSD, max nullity 13 (10 structures, not h-invariant, c = (6,6),
  t = (12,12), grid). In all four h-free groups studied the maximal PSD nullity is 13 (or 9).

- 06:25 UTC, kernel-imposed MILP (kernel_milp.py, scipy/HiGHS; linear model: C1, C1', ker T >= N i.e.
  Gamma N = (3I - K) N, C2 as lazy cuts; objective = number of star-pair orbits {p, h(p)} with Gamma_p != Gamma_h(p)):
  for object 0 the optimum is 0 (every admissible structure whose kernel contains N_0 has h-related matchings).
  For other objects (e.g. 53) the optimum is 20: admissible structures with T EXACTLY PSD of rank 30 (nullity 14),
  matchings NOT h-related, h-asymmetry 80, but U NOT PSD (lambda_min U about -0.60) (kmilp_obj53_ambig.json, checked
  exactly for T by hsym_check.py and by the reviewer). So the T-only form of (H-MATCH) is FALSE: U >= 0 is essential.
  (The kmilp_obj*_ambig.json files were written by two drivers (modes match and hfull) into the same names; the logs
  kmilp_match_331.log and kmilp_hfull_331.log are authoritative.)
- 07:00 UTC, complete kernel-MILP sweeps (logs kmilp_match_331.log, kmilp_hfull_331.log, kmilp_match_other103.log):
  the 331 rank-30 objects have 129 DISTINCT kernels (kernel_classes_331.json). Match mode: 318/331 objects (128/129
  kernels) admit NO admissible structure with that kernel and broken star matchings; the remaining kernel (shared by
  13 Z5h objects with c = (2,2)) admits broken ones, but the MILP optimum is never PSD (U fails). Full h-asymmetry
  (hfull): 303/331 admit no h-broken structure at all; the other 28 optima are not PSD. The 103 other distinct saved
  structures of nullity >= 14 (nul14_other_structures_2026-10-15.json, PSD or not): 98 kernels admit no broken
  structure, the other 5 again have non-PSD optima. The shared kernel is being enumerated COMPLETELY by SAT
  (kernel_sat_enum.py, DP encoding of the linear kernel equations; validated against kernel_enum.py: same 8
  structures for the 13-dim kernel of hm_id_c22_HB_1): ksat_obj53_full.log. RESULT (07:05 UTC): 15 936 admissible
  structures contain the shared kernel (COMPLETE, 500 s); 96 are PSD, ALL with h-related matchings; the 9 408 with
  broken matchings (8 688 of nullity 14, 720 of nullity 15) are all non-PSD. Hence none of the 129 distinct kernels of
  the 331 rank-30 objects is the kernel of a PSD structure with broken matchings (128 by the MILP optimum 0, ten of
  them re-checked by complete SAT enumeration in kreps_check/ksat_10reps.log; the shared one by complete SAT
  enumeration). A full SAT pass over the 129 kernels is running (ksat_all_kernels.log).
- Sub-kernel sweep (subkernel_sweep.py): for each of the 129 kernels, impose only the 4 star vectors + 8 (resp. 7) of
  the 10 complementary kernel vectors (random choices), and enumerate ALL admissible structures containing that
  12- (resp. 11-) dimensional space; the nullity-14 ones have 2 (resp. 3) kernel directions that are not prescribed.
  Logs subk_drop2.log, subk_drop3.log.
- kernel_enum.py (all admissible structures whose kernel contains the 13-dimensional kernel of hm_id_c22_HB_1):
  8 structures, COMPLETE (MILP infeasible after no-good cuts), all of nullity 13 and broken, 1 PSD (the start).

- Real srg(243,22,1,2) graphs (hmatch_tools_2026-10-15/hmatch243.py; exact, combinatorial): in the
  Berlekamp-van Lint-Seidel graph (built by make_bvls.py, 40 vertices examined) every vertex is a Hamming point (55/55
  pairs of lines are grids) and BOTH halves of the (H-MATCH) relation hold at every pair; in the three new srg(243)
  of the asymmetric campaign (spreadfree_243_2026-10-12: trade_aut108, trade_aut162, tricayley_Z3x4_grids25;
  60 vertices each, 17 or 25 grids per vertex) NEITHER half holds at ANY pair, grids included. [Corrected after the
  second independent review, 08:00 UTC: by the argument of section 2, which uses only lambda = 1 and works for any
  number of lines, 'all pairs at v h-related' is EQUIVALENT to 'v is a Hamming point'. So this observation is a
  consistency check of the Proposition, not evidence about the local law.]

- CALIBRATION on srg(243,22,1,2) (corrected 08:00 UTC after the second independent review; numbers re-checked
  exactly by the reviewer). stars_gen.py is the same model for general (k, r, s); for (14, 3, -4) it reproduces
  stars_rank.build and kval up to renaming of the auxiliary (C2 counter) variables; for (22, 4, -5) its T is the
  Schur complement of 4I - A (checked against BvLS and trade_aut108 at a vertex: T^2 = 9T, rank 88), and U = 9 Pi - T
  is the Schur complement of 5I + A (U^2 = 9U, rank 110). A six-star block (three lines, 108 labels) has forced
  nullity >= 20. Real blocks (real_block243.py, vertex 0, three lines): BvLS: admissible, PSD, nullity exactly 20,
  matchings h-related; trade_aut108: admissible, PSD, nullity exactly 20, matchings NOT h-related.
  WHAT THIS DOES AND DOES NOT SHOW:
  * The failure of the six-star analogue of (H-MATCH) is AUTOMATIC: any srg(243) with a non-Hamming vertex refutes it
    (section 2). It tests the Proposition, not the evidence for the local law.
  * The analogy is loose. Two lines carry 5k - 16 - g forced relations beyond the stars (g = multiplicity of s):
    10 for (99,14,1,2), and none for every other lambda = 1, mu = 2 parameter set (243: -16). Checked on real graphs
    (hmatch_tools_2026-10-15/fourstar243.py): every two-line block has nullity 4 (trade_aut108, 165 pairs) or 5
    (BvLS, 110 pairs). In Conway the 10 forced relations sit on the two lines h acts on; in srg(243) the 14 forced
    relations of a six-star block need a third line, which h_lm fixes. (H-MATCH) concerns a Conway-only phenomenon.
  * (B') calibration: INCONCLUSIVE (my earlier statement 'the analogue of (B') is false' was WRONG). In srg(243) the
    spectral c(l) = 39 - rank T_{X_l} can only be 1 or 2 (H_l is cubic, r = 4 != 3, so 4I - A_{H_l} is invertible) and
    it does not count the components of H_l, as it does in Conway (r = 3 = degree of H_l; P2, P3, P8). With the Conway
    meaning, every tested line of the real srg(243) is special: H_l is disconnected (BvLS 10 components, trade 3-5,
    tricayley 5-6; 330 lines per graph, reviewer).
  * More real blocks (hmatch_tools_2026-10-15/sixstar243_more.log): 36 six-star blocks (4 vertices x 3 triples in
    tricayley, trade_aut162, trade_aut108) have nullity EXACTLY 20 (exact rank of 15 T_S modulo 2^61 - 1 is 88, the
    upper bound; reviewer), lambda_2 = 4, lambda_min = -5, and fail both halves of the h-relation at all three pairs.
    The analogue of (N15) ('no excess nullity') is consistent with real graphs.
  * Walks: the six-star blocks of real srg(243) are RIGID under 6- and 12-label re-solves (the re-solve returns the
    seed or a non-PSD structure; maximum distance from the seed 0 edges; final walk from BvLS: 8 782 moves, no PSD
    broken structure); the aut108 'control' started on a target and only re-found it (not a positive control); the
    walks with 12 and 20 freed labels made no move before being stopped. This does not measure the Conway walks,
    which DO move (PSD broken structures of nullity 13; a new rank-30 object 16 edges from its seed). A real control
    would start from a perturbed (non-PSD or random admissible) neighbour of the aut108 block.

## 4. Lesson of the calibration (corrected 08:00 UTC)
The srg(243) comparison does not test (H-MATCH): the failure of the analogue is automatic, the (B') comparison used a
different c, and the 243 walks never moved. A failed analogue only shows that a law is not a parameter-free
consequence of the local conditions; it cannot separate a family artefact from a Conway-specific mechanism. The one
structural fact it brought out goes the other way: only Conway has forced relations between TWO lines, which is what
(H-MATCH) is about. The evidence for (H-MATCH) therefore stands as before: family-biased, uncontradicted, with the
13-wall in all walks and in all four h-free groups studied.

## 5. Runs (state 08:10 UTC)
All runs finished or stopped. Scripts used for the evidence: work/stars_rank_2026-10-14/hmatch_tools_2026-10-15/.

## 6. Task T3 (absorption / 13-wall), state 09:15 UTC (LAB; Codex has T2 = ODD9)
- Block form along h: T = [[A, B], [B^T, C]], U = 7 Pi - T = [[A', -B], [-B^T, C']] (E_+ / E_- = h-even / h-odd, 22 + 22).
  A, C, A', C' depend only on the average Gamma_0 = (Gamma + h Gamma h)/2; B = -(compression of Delta), with
  Delta = Gamma - h Gamma h (entries 0, +-1). nullity T = nullity C + nullity(A - B C^+ B^T); nullity C = 2 in all data.
- LEMMA (proved, elementary): if T >= 0 and rank A = 10, then ker T contains ker A (12 dimensions, h-even) and the two
  star differences, so nullity T >= 14 and Delta kills ker A. If T, U >= 0 then T_0 = (T + hTh)/2 and U_0 are PSD
  (average of PSD matrices).
- COROLLARY: a complete enumeration of a kernel class (all admissible structures whose kernel contains N) contains every
  PSD structure whose even block has the same 12-dimensional kernel as a member of the class. So the 129 complete
  class enumerations exclude any PSD broken structure 'sharing the even kernel' of a known rank-30 object.
- DATA: all 416 PSD nullity-14 structures on file have B = 0 and rank A = 10 (or rank A = 11 with nullity C = 3).
  In the only class with broken members (the kernel shared by 13 Z5h objects, 15 936 structures, complete), the 9 408
  broken ones all fail positivity, T nearly (scale factor of B in [0.876, 1.247]) but U clearly: 93 % already on the
  h-odd block C' (a pure h-odd vector with x^T U x < 0), 5 % on the h-even block A', 2 % need B at least 1.5 times
  smaller (tU <= 0.669). Broken PSD structures of nullity 13 have rank A = 12 and B saturating one direction.
- So a PSD broken structure of nullity 14 needs either a NEW 12-dimensional h-even kernel (rank A = 10), or rank A > 10
  with B saturating T on two directions (never seen beyond one). Sweep running: harvest new h-invariant rank-30
  objects (sym4g.py in <h>, runs hv_h_*), new kernel classes (new_kernel_classes.py), complete enumeration of each
  (kernel_sat_enum.py), looking for a PSD broken member.

### 6b. T3 update, 10:00 UTC (numerical unless marked exact; "complete" = SAT UNSAT, no certificate)
- Harvest in <h> (sym4g.py b1 anyc, SAVE30, six warm starts c22, r725, cold49, h42, c55, hr7; stopped at 09:38 UTC
  because the user opened a game, rule 'low performance'): 166 distinct PSD structures of numerical nullity 14, all
  h-invariant by construction, with new types c = (4,2) and (3,3). New kernel classes (new_kernel_classes.py, exact
  kernels, exact rank 30): 18 (newk1), then 140 more (newk2) beyond the 196 known. Almost every harvested object is
  a new class: the h-invariant rank-30 world shows no saturation.
- Complete class enumerations (kernel_sat_enum.py via ksat_dir.py): newk1 18/18 complete, NO structure with broken
  matchings at all (PSD or not); typical class = 174 structures (4 PSD) or a singleton. newk2: running; at 09:51 UTC
  50/140 complete, 77 PSD (all h-related), 1530 non-PSD, ZERO broken; most classes are SINGLETONS (the 14-dimensional
  kernel determines the structure).
- Why singletons (exact reasoning): a structure with kernel >= N satisfies, row by row, Gamma_i N = ((3I - K) N)_i, i.e.
  14 linear equations on the ~6 neighbours of label i among 43 candidates. A second structure with the same kernel
  needs, in some row, a {0, +-1} vector Delta_i orthogonal to N with zero sum on every star: an additive coincidence
  among the kernel coordinates of labels. In the rank A = 10 case, N = ker A (+) star differences is h-invariant and the
  even coordinates of r and h(r) coincide, so the even equations only see orbit counts; broken structures with that
  kernel exist only when these orbit-count equations have several solutions (the obj53 class: 9 408 broken, all
  non-PSD).
- Codex (message of ~09:50 UTC, codex_h_mixed_energy.py in C:\Users\RESEARCHER\Desktop\Recherche_Conway\lab_exchange_2026-10-14):
  exact identity ||B||_F^2 = b/2 (b = broken edge orbits {e, h e} with exactly one edge; q = broken orbit blocks,
  q <= b <= 2q); T >= 0 gives B^T ker A = 0, so rank B <= rank A; two necessary tests for a FIXED average, valid for all
  2^b orientations: (1) b/2 <= sum_i lambda_i(S) lambda_i(C') with S = A' shorted to range A; (2) eps^T H eps <= rank A
  with H_kl = tr(S^+ B_k C'^+ B_l^T); a diagonal d with H - diag d >= 0 and sum d > rank A excludes every orientation.
  Independent re-implementation: hmatch_tools_2026-10-15/orient_tests.py (B = sum eps_k B_k checked against the true
  block). On the 47 distinct averages of the 55 obj53 near-misses (orient_near.log): b = 40, rank A = 10; test (1)
  20 vs 151.4 (passes); test (2) inconclusive: H is singular (bound b lambda_min = 0), actual eps^T H eps = 7.108 <= 10
  on all 47, local minima over eps 0 to 2.06. The near-misses fail by the OPERATOR norm (tU = 0.669, i.e.
  ||S^-1/2 B C'^-1/2||_op = 1.495) while ||.||_F^2 = 7.108: the excess is concentrated on one direction, invisible to a
  Frobenius test. No average excluded (and for these 47 the complete class enumeration already covers all admissible
  orientations).
- Break types (break_types.py, exact, combinatorial): for label orbits O, O' the 2 x 2 block [[a,b],[c,d]] is SINGLY
  broken (one of a != d, b != c; even quotient Gamma_+(O,O') a half-integer, B entries +-1/2) or DOUBLY broken (both;
  Gamma_+ integral, B entries 0 and +-1). The obj53 near-misses and kmilp_obj53_ambig: q = b = 40, ALL single, located
  10 in the l-block, 20 across, 10 in the m-block; the l-block breaks are exactly M_0 Delta M_1, two disjoint matchings
  whose union is a 10-cycle on the outer letters with every mate pair at distance 3. hm_id_c22_HB_1 (PSD, nullity 13):
  q = 26 (22 single, 4 double, the doubles all across), b = 30.
- Running at idle priority (game open): the newk2 enumeration, and a walk in <tau>, tau = (0 2)(1 3) (swaps the two
  lines, does NOT contain h; plain b1 objective, CPEN = 0, SAVE30): if it reaches nullity 14 PSD, are those structures
  h-invariant anyway (forcing) or broken (counterexample)?

### 6c. 10:10 UTC
- newk2 FINISHED: 140/140 classes complete, 404 PSD structures (all h-related matchings), 14 960 non-PSD (all h-related),
  ZERO broken structures. Total: 287 kernel classes enumerated completely (129 + 18 + 140); exactly ONE (obj53, Z5h c22)
  contains broken structures at all (9 408, none PSD).
- EXACT remark: if N = ker T is h-invariant (rank A = 10) and the kernel class of N is a singleton, then Gamma is
  h-invariant (h Gamma h is admissible with kernel hN = N). So (H-INV) in the case rank A = 10 is equivalent to: no
  kernel class with an h-invariant kernel contains two PSD members Gamma != h Gamma h. Uniqueness is what the data show
  everywhere except obj53.
- Shape of the forced relations (kernel_shape.py, exact): Z5h lineage (c22, c62, c42): u_y = -sum_z Phi_yz g_z with
  Phi in (1/5)Z, Sum g = 0, c1 + c2 = 0 in the Gram space, i.e. span(u) = span(g) (one 9-dimensional space for both
  lines; u_y = 1_0y + 1_1y, g_z = 1_2z + 1_3z, c1 = 1_02 + 1_13, c2 = 1_03 + 1_12). G1 c55: component relations
  u_8 + u_9 = u_10 + u_11 = u_12 + u_13 = 0, g_4 + g_5 = ... = 0, plus four integral mixed relations. c33: component
  relations g_4 + .. + g_7 = 0, g_8 + .. + g_13 = 0, the rest mixed in fifths.
- Single breaks cost kernel equations (exact reasoning): with an h-invariant kernel, row r of Delta = Gamma - h Gamma h
  must be orthogonal to N; a single break at (O, O') contributes +-phi_+(O') (even kernel coordinates of the orbit), a
  double break 0 or +-2 phi_+(O'). So every row with single breaks needs a signed vanishing sum of even orbit
  coordinates; in the RREF basis the l-outer orbits have coordinates e_y (pivots), so an l-block break must be
  compensated across (lm) by columns of Phi.
- NEW complete enumeration around the 13-wall (kernel_sat_enum.py, new option KHOMOG = impose only N n hN =
  ker(M + hMh)): for hm_id_c22_HB_1 (PSD broken, nullity 13), N n hN has dimension 12; ALL admissible structures
  containing it: 672 (COMPLETE, 27 s): PSD nullity 14: 8 (all h-related); non-PSD nullity 14: 340 (all h-related);
  broken: only nullity 12 or 13 (4 PSD of nullity 13). In this class, broken => nullity <= 13 WITHOUT positivity.
  homog_classes.py on all 450 saved HB files + the 55 near-misses: only 2 distinct homogeneous kernels (this one, and
  the 14-dimensional obj53 kernel): the walks produced a single broken lineage.
- Walks without h (idle priority): Z5 alone from seed_rank30_c22 (HBREAK + HMATCH): stuck on a broken PSD structure
  of nullity 10. <(0 1)M> and <(2 3)M> (M = all outer flips) from the G1 c55 object: about 1 250 PSD visits each in the
  first minutes, ALL with h-related matchings (no broken PSD structure reached).

### 6d. LEMMA (side relations are h-homogeneous) -- PROVED (LAB 15/10, 10:30 UTC; exact check side_check.py)
For ANY admissible four-star structure (h-invariant or not): let C be a component of H_l, with letter set W (a union
of lines other than l, automatically s_m-invariant since m's two letters are mates) and label set C n X_l =
{0y, 1y : y in W}. Then kappa_C = 1_{C n X_l} satisfies T kappa_C = 0 on the rows of X_l, and h kappa_C = kappa_C.
Proof: for x in X_l, x has exactly two Gamma-neighbours in X_l (its M-partner and its sigma_l-partner, C1), both in the
H_l-component of x, so (Gamma kappa)_x = 2 [x in C]; summing K(x, z) = -1/4 + 3/8 |x n z| + 1/8 m(x, z) over the 4k labels
z of C n X_l (k = lines in W) gives -k + 3/8 (2k + 2[y in W]) + 1/8 (2k + 2[y^1 in W]) = [x in C] (W is a union of lines);
so (T kappa)_x = 3[x in C] - 2[x in C] - [x in C] = 0. h maps {0, y} to {1, s_m(y)} and W is s_m-invariant. If T >= 0
(or just T_S >= 0), kappa_C in ker T_{X_l} gives kappa_C in ker T. Together with the star vectors (1_L0 - 1_L1 is h-odd,
the others even) these are 1 + c(l) independent kernel vectors of T_{X_l}, i.e. all of them (rank T_X = 23 - c, G2).
CONSEQUENCE: all side relations (on X_l or on X_m) lie in N n hN. The h-inhomogeneous part of ker T can only come from
the MIXED relations (G9: 12 - c(l) - c(m) + [grid] + delta of them in a Conway graph). Exact check (side_check.py): for
hm_id_c22_HB_1 (broken, PSD, nullity 13; c = (5,2)) and a near-miss (broken, non-PSD) every component vector is in
ker T and h-invariant. Both have m's two letters as a single-line component of H_l and l's as one of H_m: (l, m) is a
3 x 3 grid pair there (and c1 + c2 = 1_02 + 1_03 + 1_12 + 1_13 is the corresponding component vector).

### 6e. Kernel symmetry groups (kernel_sym.py, exact; log kernel_sym_287.log), 10:25 UTC
Frame group = D4 on the star letters x signed permutations of the five outer lines (order 30 720). For a structure,
Aut = its stabiliser, G_N = the stabiliser of its kernel N; class(N) is a union of G_N-orbits, so it contains at least
|G_N| / |Aut| structures. h is central in the frame group, so images of h-invariant structures are h-invariant: broken
members of a class are never images, always 'accidental' solutions. Over the 287 classes: |G_N|/|Aut| = 1 (singleton
orbit) for 55, 2 for 198, 4 for 32, and 96 for exactly TWO classes (|Aut| = 20, |G_N| = 1920): obj 6 (c = (6,6), 15
objects, 24 144 structures, none broken) and obj 53 (c = (2,2), 13 objects, 15 936 structures, the 9 408 broken ones).
A huge kernel group is what makes large classes; it is not sufficient for broken members (class 6 has none).
Projection walk without symmetry or seed (projwalk.py, two runs, about 5 CPU-minutes each at idle priority): never
reached T, U >= 0 (best score 5.6 from 12): an unbiased search cannot reach the PSD world with these moves; PSD four-star
structures are far from random admissible ones (lambda_2 <= 3 against about 2 sqrt 5 for random degree-6 graphs).

### 6f. The 13-wall is a FAKE symmetry (LAB 15/10, 10:45 UTC; exact, hidden_sym.py, fake_kernel.py, mixed_shape.py)
- hm_id_c22_HB_1 (the best broken PSD structure, nullity 13) is EXACTLY invariant under g = h (4 6) = (0 1)(2 3)(4 6),
  an involution of the letters that does NOT preserve mates (4^1 = 5, 6^1 = 7), hence not a frame symmetry. Its star
  matchings satisfy M_1 = s_m (4 6) M_0, M_3 = s_l (4 6) M_2 (M_0 has 47, 56; M_1 has 45, 67; M_2 has 49, 67;
  M_3 has 47, 69). The odd part (for h) of its h-inhomogeneous kernel direction is (5/2)(f_4 - f_6 - e_4 + e_6).
- For any g = h p with p an involution of the outer letters and Gamma g-invariant: g T g = T + D with D = K - gKg FIXED
  (only the mate terms of K change). For p = (4 6), D = (1/8) J_4 (x) Q on the 16 labels {s, y}, y in {4..7}, with Q the
  balanced signed 4-cycle 45(+), 56(-), 67(+), 74(-): rank 2, eigenvalues +1, -1; it couples the g-even vector
  p_+ = (1/2) sum_s (1_s5 - 1_s7) with the g-odd vector q_- = (1/2) sum_s (1_s4 - 1_s6). Hence T = T_s - D/2 with
  T_s = (T + gTg)/2 >= 0, ker T_s = N n gN, and nullity T <= nullity T_s + 1 (a rank-one coupling saturates at most one
  direction); a g-even kernel vector n satisfies D n = 0, i.e. n is orthogonal to p_+ (one extra linear condition
  compared with a true symmetry).
- Data: HB_1 and every PSD nullity-13 structure of a walk in the fake group <h (4 6)> (FAKEOK option of sym4g.py, warm
  start HB_1; about 5 500 PSD visits by 10:44 UTC, max nullity 13) have N = gN exactly, with 11 g-even + 2 g-odd kernel
  vectors (one fewer than the 12 + 2 of h-invariant objects).
- Reading (corrected 10:57 UTC after Codex's exact reduction, codex_h_geometric_defect.py): the walks' broken lineage
  is h-invariant up to a mate-breaking relabelling of two letters. For HB_1, N = gN, so the T-residual of the coupling is
  strictly positive (no saturation) and the 13 is already in the average (11 g-even + 2 g-odd). The rank-2 defect alone
  does NOT force the cap 13 (abstract blocks with the same couplings reach nullity 14); the only constraint forced by D
  is that g-even kernel vectors are orthogonal to p_+. Whether a fake g allows a 12-dimensional g-even kernel is OPEN.
  Codex: for any g = h p, D = (J_4 (x) (Mt - p Mt p))/8 on the 40 labels {s, y}, rank D = 10 - 2c (c = alternating
  components of Mt u p Mt p), and g U g = U - (8/15) D.
- DECISIVE TEST DESIGN: for a TRUE symmetry g = h p (p a mate-preserving involution of the outer letters), D = 0, the
  kernel splits as for h, and g-invariant structures are h-broken unless their matchings are p-invariant. <h, (4 5)> has
  no admissible structure (SAT, earlier); G1'' = <(0 1)M, (2 3)M''> (M = all outer flips, M'' = M without (4 5))
  contains h (4 5) and not h, and has admissible structures. In G1'', M_0 is forced to contain {4,5} (its letters 4, 5
  are the only fixed points of s_m M''), so the l-half is automatically h-related; the m-half holds iff M_2 contains
  {4,5}. A PSD nullity-14 G1''-structure with M_2 not containing {4,5} would REFUTE (H-MATCH). Cold walks in G1'' and in
  G1 (control) running at idle priority since 10:42 UTC.

### 6g. True-symmetry families without h (LAB 15/10, 11:00-12:10 UTC)
- G1'' = <(0 1)M, (2 3)M''> (contains h (4 5), not h): admissible structures exist; M_0 is forced to contain {4,5}
  (the l-half is automatically h-related); level-1 cubes (M_0, M_2): 26 811 = 81 x 331, COMPLETE; per cube more than
  5 000 - 14 000 structures (not finished in 120 - 150 s), ZERO PSD in every sample (about 100 000 structures).
  Codex's exact cuts for PSD members (F = {04,05,14,15} is a forced 4-cycle component, counts of attachments, canonical
  interface up to C2 wr S4, d_P <= 1 for the four outer pairs, hence c(m) <= 3 for broken cubes) do not make the
  cubes small. Methods tried, none conclusive: cold walks (no PSD in G1'' nor in the control G1 in 15 CPU-minutes);
  MILP with exact C2 and positivity cutting planes (psd_milp_group.py; 130 iterations without verdict, and the control G1,
  which contains the c55 objects, found nothing either); SDP relaxation (sdp_relax.py, Clarabel): whole family
  feasible; per cube 2/40 infeasible, 21 feasible, 17 numerical errors (forced kernel kappa_F makes the cone degenerate);
  SDP-guided rounding (sdp_round.py) found no PSD structure even in G1. A complete G1'' test needs an SDP
  branch-and-bound or Codex's analytic reduction. PARKED.
- <Z5, hM> (M = all outer flips; the only Z5 family with a true symmetry h p and no h, since M is the only involution
  commuting with z): earlier enumeration (2 h, incomplete) 143 390 structures, 72 PSD, max nullity 9 (all with a grid
  on (l, m), t = (2, 2) mostly), against nullity 14 in <Z5, h>. Here t(l) is 0, 2, 10 or 12 (outer transversals come in a
  single <z, M>-orbit) and no PSD structure has outer transversals. Level-1 cubes: 25 (COMPLETE); cube 12 complete in
  166 s (9 024 structures, 4 PSD, max nullity 9). COMPLETE enumeration running (3 idle processes, cubes 0-24, logs
  Z5hM_full_*.log).
- 12:14 UTC, cube 12 of <Z5, hM> COMPLETE (9 024 structures, 4 PSD, all of nullity 9; enum_cubes.py, SAVEMIN = 9).
  Exact analysis of Z5hMs_c12_P9_1.json (side_check, balance, kernel_shape): c(l) = 6 (every other line is a
  single-line component, i.e. l spans a grid with all six; t(l) = 12; M_0 = M_1 = the mate matching, so the l-half is
  h-related automatically), c(m) = 2 (components [0,1] and the five outer lines), t(m) = 2; ker T (dimension 9) is
  h-invariant: 7 even + 2 odd, and the 7 even vectors are EXACTLY the side relations (u_y + u_{y^1} for the five outer
  lines, c1 + c2, Sum g; with the star sums), the odd part the star differences: NO mixed relation at all
  ((1 + 6) + (1 + 2) - 1 = 9 = nullity). In the Z5h c22 objects: 5 side relations and 9 mixed ones. Provisional reading:
  replacing h by the true symmetry hM kills every mixed relation. CORRECTED 13:00 UTC: this holds only for the
  c = (6,2) / (2,6) members; the c = (2,2) members (53 of the 72 PSD of the earlier run) have nullity 9 = 5 side
  relations + 4 mixed ones, so hM does NOT kill all mixed relations (check on saved structures pending).
- 12:30 UTC, <Z5, hM>, COMPLETE sub-family enumerations (SAT, no certificate; enum_cubes.py FORCE_TL/FORCE_TM):
  all ten outer transversals of m imposed: 26 340 structures, 16 PSD, all of nullity 9 (c = (2,6), t = (2,12), the
  tau-mirrors of the cube-12 ones; at side l every g_y is transversal yet none is absorbed, residual 1.030); all ten outer
  transversals of BOTH lines imposed (t = (12,12), the configuration of the Z5h nullity-14 objects): 4 788 structures,
  ZERO PSD. Since t_out is 0 or 10 on each line in this family, every PSD member has t_out(l) = 0 or t_out(m) = 0.
  Codex (message ~12:25): under hM alone (no Z5), c(l) = c(m) = 6 is impossible with T, U PSD (on the checkerboard modes
  of the ten grid squares U restricts to [[2I, B], [B^T, 2I]] with B 5 x 5, zero diagonal, +-1 off it; PSD forces
  B B^T = 4I, a conference matrix of odd order 5: two rows share three positions, odd inner product, contradiction).
- 12:59 UTC, <Z5, hM> COMPLETE (all 25 cubes, SAT UNSAT per cube, no certificate): 339 556 invariant admissible
  structures, 192 with T, U PSD, maximal numerical nullity 9 (no structure of nullity >= 10). Compare <Z5, h>: nullity 14
  occurs (185 of 160 087 enumerated, incomplete). Codex (messages ~12:45-12:55, finite proof with 520 integer
  certificates, codex_z5_hm_rank_obstruction.py in his exchange folder): for <z, hM>-invariant structures null_Q T =
  nu0 + 4a + 4b with nu0 in {5, 6}, a, b <= 1, so nullity <= 14, and at nullity 14 rank_F7(8T) >= 29 > 28: no member of
  the family is a Conway block. Our complete enumeration gives the stronger LOCAL ceiling 9 (unexplained).
