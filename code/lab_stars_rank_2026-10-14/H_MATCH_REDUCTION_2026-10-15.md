# (H-MATCH): a local symmetry law that would exclude Conway (LAB, 15/10/2026, ~06:00 UTC)

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
  60 vertices each, 17 or 25 grids per vertex) NEITHER half holds at ANY pair, grids included. So in real
  lambda = 1, mu = 2 graphs h-related local matchings go with the grid-full (Hamming) regime, which L8 forbids for
  Conway; the high-nullity local objects we can find are all of that BvLS-like kind.

- CALIBRATION on srg(243,22,1,2) (stars_gen.py = the same model for general k, r, s; it reproduces stars_rank.build
  and kval exactly for (14, 3, -4)): there T = 4I - Gamma - K, U = 9 Pi - T, rank T <= 110 - 22 = 88, so a SIX-star
  block (three lines, 108 labels) has forced nullity >= 20, the analogue of the four-star nullity >= 14 for Conway.
  Real blocks (real_block243.py, vertex 0, three lines): BvLS: admissible, PSD, nullity exactly 20, matchings
  h-related for the three pairs; new243_trade_aut108: admissible, PSD, nullity exactly 20, matchings NOT h-related
  (44-48 asymmetric star pairs per pair of lines). So the ANALOGUE of (H-MATCH) is FALSE in a real lambda = 1,
  mu = 2 graph: forced-nullity PSD blocks with broken matchings exist there. (H-MATCH), if true for Conway, would be
  specific to the Conway parameters (and then equivalent in effect to non-existence).
  Search calibration running: walk_gen.py (same HMATCH walk as for Conway) from the BvLS block, looking for broken
  nullity-20 PSD blocks, which do exist (cal243/cal_bvls_f*.log; control from the aut108 block: finds itself at once);
  kernel_sat_gen.py on the BvLS kernel (cal243/ksat_bvls.log).

## 4. Tests running (06:45 UTC)
kernel_milp_all.py over the 331 objects (modes match and hfull, no PSD cuts; PSDCUTS=1 adds eigenvector cutting planes
for T and U, symmetrised under the object's group, but converges slowly), HMATCH walks hm2_d, hm3_c1, hm3_c2
(the last two reward large c), walks in the twisted involution groups <h s> (s = M, (4 6)(5 7), (4 5), (4 5)(6 7))
with HREQ (from cold), enumerations enumZ5hM, enumZ5sM, local enumeration loc16b_HB1.
Scripts used for the evidence: work/stars_rank_2026-10-14/hmatch_tools_2026-10-15/ (copied from the scratchpad).
