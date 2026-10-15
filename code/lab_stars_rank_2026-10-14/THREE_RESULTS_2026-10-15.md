# The three results behind the last step of (H-MATCH) => no Conway: what they are and what they imply
LAB, 15/10/2026, 18:30-19:00 UTC.  User (18:30): "the last step relies on 3 results; why not study them
intensively, understand them and what they imply".  Sources read for this note: Codex's notes 00 (foundations),
30 (lemmas L1, L15, L16), 94 (literature, full texts), 100 (synthesis of L1-L23), 105 (L8), 108 (L10, L11, D1, D2)
in C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-asymmetry-audit\notes; the catalogue
work/asym_paley_2026-10-14/CONWAY_CONSTRAINTS.md; my audit AUDIT_EXCLUSIONS_2026-10-15.md; my theta-LP note
work/c1_theta_lp_2026-10-07/NOTE.md; Codex's export codex_c55_excluded_after774.txt.  Nothing here is re-proved
unless marked; statuses are those of the sources.

## 1. The three results (and the relatives used in the quantitative form)
Vocabulary (Codex, note 00): at a vertex x, tau_a = our star matching M_a (perfect matching of the 12 letters other
than a, a^1); a letter a TWISTS the class {b, b^1} if tau_a(b) != b^1; |W(x)| = number of twisted (letter, class)
pairs at x (0..84); a pair of classes {l, m} at x spans a 3x3 GRID iff tau_a(b) = b^1, tau_{a^1}(b) = b^1,
tau_b(a) = a^1, tau_{b^1}(a) = a^1; a PRISM is K3 x K2 (two lines and a matching); t(l) = number of prisms through
the line l = number of transversals of l in any four-star block containing l (a line invariant).
Identities: P = sum_l t(l) / 2 = 1386 - sum_x |W(x)| / 6 (L15, G10); |W(x)| = sum over the 7 lines at x of
(12 - t(l)); grid-full <=> tau = mate everywhere <=> 231 grids.

- L1 = MAKHNEV 1988 (Mat. Zametki 44(5), 667-672, Thm 2; full text read by Codex, note 94 s.3.1).  Condition (*):
  two triangles joined by at least two edges are joined by three (= untwisted = grid-full).  (99,14,1,2) does not
  satisfy (*).  Makhnev's proof: under (*) the triangles 3-joined to a triangle Delta form an srg(33,12,1,6) with (*),
  excluded by his Thm 1 (lambda = 1 and (*) => mu <= 3 or (27,10,1,5)).  Independent proof (Codex, note 30, L1):
  transport the lines along edges; the universal cover of the triangle-square complex is H(7,3), so 99 |G| = 3^7.
  Status: literature + independent proof.
- L8 (Codex, note 105, 25/09): no Hamming point, i.e. no vertex all of whose 21 pairs of classes span grids.  Proof
  (no solver, four exhaustive finite checks): at a Hamming point Gamma_2(x) splits into 21 squares Q_P joined by
  bijections along the Kneser graph K(7,2); the number l(t) of lines above a Kneser triangle t is |Fix theta_t| in
  {0, 2, 4}; Petersen matchings force type A/B pairs; the skeleton l is one of the 30 Fano functions; a section X is
  parallel along the 84 off-pencil edges; a B/C lemma leaves 35 configurations, all contradictory (F2 systems,
  certificates of 3 to 9 equations).  Status P (Codex), also SAT (14/10 night, T1).
- rho <= 191 (catalogue C6): every grid contains 6 prisms and a prism lies in at most one grid, so rho <= P / 6, and
  P <= 1151 by L16 (Krein condition for lines: 12 P = 13860 - 64 || sum_L u_L^(x)3 ||^2, plus Cauchy-Schwarz with
  points; note 70).  Strengthened: P <= 852 by order-9 positivity (Codex's exact certificate P <= 11088/13, found
  independently by my LP, c1_theta_lp NOTE line 901), P + 5 rho <= 1386, hence rho <= 126 (catalogue C5, C6).
- Relatives: L10 (g(x) <= 17 grids per vertex, note 108, slot counting, by hand); D1 (at every vertex the set of
  incomplete pairs contains two DISJOINT pairs); D2 (the path configuration is impossible); L11.

## 2. What they are: torsion FLOORS, and only floors
All of them forbid structures that are too close to the Hamming (untwisted, grid-rich) side.  Codex's note 100 s.4
(25/09) proves that the 'maximal torsion' profile (every tau_a loopless at every vertex: P = 0, no grid, |W| = 84,
k = 28) satisfies every lemma L1-L21 simultaneously, these three included.
[CORRECTED 19:05 UTC, after the user's objection and Codex's independent answer (message to 849): my sentence 'no
combination of these results can ever exclude Conway' was NOT justified.  Codex: the profile of note 100 only shows
that the displayed AGGREGATE consequences (numbers P, g, |W|, k) do not contradict each other; it is not a common
model of the STRUCTURAL lemmas, still less of the newer constraints, so it does not prove that their proofs or
their combinations can never contribute to an exclusion.  What remains true: none of the STATEMENTS, as stated,
gives a lower bound on P or on grids (no ceiling) today.]  A CEILING is still required by the present statements
(an upper bound on torsion = a lower bound on prisms, grids or h-relations).  (H-MATCH) is such a ceiling (it forces tau = mate at a vertex); the transversal bridge (T8)/(T15)
(AUDIT O3) is a much weaker ceiling that also suffices together with P <= 852.

## 3. What they imply for the four-star blocks of a putative Conway graph (PROVED from the cited inputs)
(a) There are 99 x 21 = 2079 four-star blocks (vertex, pair of lines); a grid has 9 vertices and spans exactly one
    pair at each of them, so the grid blocks number 9 rho.
(b) Non-grid blocks: at least 4 at every vertex (L10), hence at least 396 in total, and at every vertex they contain
    two disjoint pairs (D1).  With rho <= 191: at least 360; with rho <= 126: at least 945 (45 % of all blocks).
    Even Makhnev alone gives at least one non-grid block somewhere.
(c) Prisms and transversals: each line lies in 18 blocks, so the sum over the blocks of t(l) + t(m) equals 36 P;
    the mean of t(l) + t(m) over the 2079 blocks is <= 14.75 with P <= 852 (<= 19.93 with L16 only); the mean of
    t(l) over the 231 lines is <= 7.38; the mean torsion |W(x)| is >= 32.4.
(d) Hence any law 'every PSD four-star block of nullity >= 14 has t(l) + t(m) >= 15' excludes Conway (sum the 2079
    block inequalities: 18 sum_l t(l) >= 15 x 2079, P >= 866.25 > 852).  This is AUDIT O3 (T15), already known.

## 4. Confrontation with the four-star data (t_odd_scan.py, exact structures, numerical spectra; 558 distinct
T, U PSD structures of nullity 14 in the top-level corpus; log hmatch_tools_2026-10-15/t_odd_scan.log)
- 532 are GRID pairs; the 26 non-grid ones all belong to the G1 c55 lineage (t = (8,8)), and Codex proved that the
  whole non-grid G1 c55 family has rank_F7(8 T_S) >= 29 > 28, so it never extends to Conway (export
  codex_c55_excluded_after774.txt; status C).
- t >= 8 on both lines in all 558 (min t(l) + t(m) = 16); grid with b = 2 (ODD9 sector) gives t = (12,12) in all 474
  cases; the 58 ODD9 failures (b = 3) are grids with t = (10,10).  At nullity 13 the minimum is t = (6,8)
  (sq8_id_disc_c55_PSD_2, c55 lineage).
- Earlier targeted searches (AUDIT, 15/10 night): no PSD structure of nullity 14 with t <= 7 (77 939 PSD visits); the
  no-grid walks started from the Z5h seeds (nosq_*) never reached T, U >= 0 at all.  No no-grid walk was ever started
  from the c55 lineage.
READING: the PSD nullity-14 world we know sits where a Conway graph cannot live: almost only grid blocks with many
transversals.  The regime that Makhnev, L8, L10 and rho <= 126 make unavoidable (non-grid blocks, at least 4 per
vertex; lines with at most 7.38 prisms on average) is represented by ONE symmetric lineage, itself excluded by the
7-adic rank.

## 5. Consequences for the program
- Weakest local statements that close Conway together with these results: (T15) (O3) with P <= 852; (H-MATCH) with
  L8; and the focused form (NG14): 'no non-grid PSD four-star structure of nullity >= 14 passes the Conway-block
  tests (rank_F7(8 T_S) <= 28, DISC, extension of the outer labels)', which excludes Conway with Makhnev alone.
  (NG14) is the restriction of block non-existence to the regime the floors make obligatory: not easier in
  principle (the F7 and DISC tests also kill grid blocks: rank_7 is 25, 29 or 30 on the 331 rank-30 objects and
  none passes DISC), but it says WHERE the missing data are.
- Concrete next step (cheap): trivial-group walks from the c55 objects with NOSQUARE (stay non-grid) and the b1
  objective (nullity 14), one of them with TPEN (push t below 8); every non-grid PSD nullity-14 hit outside the c55
  family is tested by rank_F7 and DISC.  Success criterion: a non-grid PSD nullity-14 structure outside the c55
  family (then its F7 / DISC status); failure (none in about 40 minutes per walk) is evidence for (NG14) and (T15).

## 6. (19:00-19:20 UTC) A sharper decisive target found in the non-grid regime: (N9-NG)
STATEMENT (CONJECTURE, OPEN).  (N9-NG): every admissible four-star structure with T, U >= 0 and NO grid on (l, m)
satisfies   nullity(T_S4) <= 9 + min(c(l), c(m))   (c = spectral c = 23 - rank T_X = number of parts of H_l).
This is (N9) of N9_REDUCTION_2026-10-15.md restricted to non-grid pairs.  (N9) itself was refuted at 01:14 and 02:01
UTC by GRID objects only (fourstar_psd_grid_Z5h_c62: grid, c = (6,2), nullity 14; fourstar_psd_rank30_c33_h: c =
(3,3), nullity 14, a grid as well: no non-grid PSD structure of nullity 14 other than the c55 type is known).
IMPLICATION (PROVED, given (N9-NG) and P <= 852 (or rho <= 126)): (N9-NG) => no Conway graph.
Proof.  Let l be a line and x a point of l.  If l has a non-grid partner m at x, the block (x; l, m) is an admissible
PSD four-star structure of nullity >= 14 (P1, P10, G9), so (N9-NG) gives c(l) >= 5.  Otherwise all six pairs of l at
x are grids, so the six parts of H_l are singletons and c(l) = 6.  In both cases c(l) >= 5, hence g(l) >= 4 (P8/P9:
c <= g + floor((6 - g)/2), g != 5).  Each grid through l gives two prisms through l and distinct grids give distinct
prisms (two grids meet in 0, 1 or 3 points), so t(l) >= 8 for every line: P = sum t / 2 >= 924 > 852 (and
rho = sum g / 6 >= 154 > 126).  Note: L10 and D1 are not even needed; only the census bound and the trivial fact that
a line whose pairs at a point are all grids has c = 6.
WEAKEST FORM USED: only nullity >= 14 matters, so it suffices that every non-grid PSD four-star structure of nullity
>= 14 has c(l) >= 5 and c(m) >= 5 ('(NG5)').
EVIDENCE (exact structures, numerical spectra): all 97 distinct non-grid PSD structures on file (top-level corpus and
the kernel-class dumps of 19:00 UTC) satisfy (N9-NG), with EQUALITY in 56 cases covering every value of the minimum:
(nu, c) = (10, (1,1)) 3, (10, (1,2)) 1, (10, (2,1)) 2, (10, (3,1)) 4, (11, (2,2)) 2, (11, (2,3)) 1, (12, (3,3)) 1,
(13, (4,4)) 7, (13, (4,5)) 2, (14, (5,5)) 33; slacks -4 .. 0, no violation.  Also the 83 000 PSD visits of the
night's schur walks (which minimised rank T_S4 - rank T_X, i.e. maximised nu - c) never went below 12 in the
non-grid lineages they explored.  Kernel classes (complete): c55 (642 structures, 6 PSD: all nullity 14, c = (5,5),
non-grid, 4 of them NOT G1-invariant, all failing F7 and DISC); sq8_id_disc_c55 (742, PSD nullity 14 only with
c = (5,5)); harv_h_c55 (642, PSD nullity 13, c = (4,4)).
CAVEAT (lesson of 01:14 UTC): the non-grid data come from few lineages (G1-descended c55, c44/c34, c31, c21, c11, an
asymmetric c31); a genuinely different family broke (N9) for grids in minutes.  The decisive test is a new family.

## 7. (19:00-19:30 UTC) Independent check by Codex, the narrower target (NG7), and the campaign so far
CODEX (messages after 849 and 850, status C, the 254 argument re-read by me step by step): (i) the profile of note 100
only shows that aggregate numbers are compatible; it does not prove that the proofs or combinations can never exclude
Conway (my 'never' is withdrawn, section 2); (ii) P = 0 survives even the integrality of the order <= 9 census (an
integer point with 6435 non-negative counts); (iii) every Conway graph has at least 254 NON-GRID blocks with
min(t(l), t(m)) <= 7 (lines with t <= 7: m >= 18 from P <= 852; grid flags per such line <= 9; incidences
I >= 6m + 216; intersection-graph eigenvalue 7 gives e(L) <= 7m/2 + m^2/42; N >= 254, minimum at m = 18); hence the
sufficient lemma can be (NG7): no non-grid block with min t <= 7 passes the Conway-block conditions; (iv) the
implication (NG5) => no Conway is correct (checked by Codex); t <= 7 => g <= 3 => c <= 4, so (NG5) => (NG7).
REFORMULATION (PROVED, bookkeeping): for a non-grid block, nu = 2 + c(l) + c(m) + mu (2 star differences, c(l) + c(m)
component vectors, mu mixed relations), so (N9-NG) <=> mu <= 7 - max(c(l), c(m)); every tight case on file has
exactly mu = 7 - max c ((5,5): 2, (4,4): 3, (3,3): 4, (2,2): 5, (1,1): 6).  In a Conway graph (N9-NG) would mean at
most 2 mixed relations in every non-grid block (against 9 in the c22 grid objects).
CAMPAIGN (tools of the previous days; all searches numerical, enumerations COMPLETE where stated):
- tool bug found and fixed: sym4g.py NOSQUARE was applied only on warm starts; a cold Z5h walk therefore produced grid
  objects (moved to hmatch_tools_2026-10-15/invalid_n9ng_z5h_grid, NOT a counterexample).  With the clause, the Z5h
  group has NO admissible structure at all: any element fixing the four star letters and moving every outer letter
  forces tau_0(2) = 3 etc., i.e. the grid.  Families able to test (N9-NG) must have a letter-0 stabiliser exchanging 2, 3.
- kernel classes (kernel_sat_enum.py, new options DUMPPSD and NOSQ): c55 (642, complete: 6 PSD nullity 14, all
  (5,5)/(8,8), 4 not G1-invariant, all rank_7 = 30 > 28 and DISC failing); sq8_id_disc_c55 (742 complete; with NOSQ
  488 complete, also after dropping any single kernel basis vector: every single-drop class is the same 488, a
  rigidity); c1_G1_c34 (nullity 12, c (4,4), t (6,6)) single drops: incomplete classes of 1 640-1 989 structures whose
  PSD nullity-14 members are again (5,5)/(8,8) non-grid.
- walks: NOSQUARE + b1 from c55 (trivial group): stays in the G1 family; NOSQUARE + b1 from c34 and schur-c11: stay at
  nullity 12 (2 000 PSD visits each); schur + NOSQUARE from the asymmetric c11 (3 617 PSD visits): Schur rank never
  below 12 (no violation), nullity 9-11; cold schur + NOSQUARE in the Klein group <(0 1)M, (2 3)(4 6)(5 7)(8 10)(9 11)>:
  no PSD structure in 7 minutes (five further Klein groups queued).
- corpus: the only non-grid structures with T >= 0 (U arbitrary) and nullity >= 13 are of the c55 lineage.
STATE: no counterexample to (N9-NG), (NG5) or (NG7); at nullity 14 every non-grid PSD structure produced by any tool
has c = (5,5) and t = (8,8) and fails F7 and DISC.  Family bias remains the main caveat.

## 8. (19:30 UTC) (N9-NG) splits into two non-grid laws, both holding on every datum
Rank formula (Codex's corrected form): nu = 12 + c(l) + d_l - e_l, d_l = 9 - (odd gain of the ten m-odd vectors beyond
X_l), e_l = even gain of the ten m-even vectors g_y = 1_2y + 1_3y beyond X_l + m-odd.  (N9) on side l <=> e_l - d_l >= 3.
The two original halves of (N9) were ODD9 (d = 0) and EVEN3 (e >= 3); both fail, but ONLY on grid blocks (the 58 ODD9
failures are grids; EVEN3 fails on the c22 / c62 grid objects with e = 0).
DATA (even3_ng.log, exact gains by odd9_check.gain on every distinct non-grid T, U PSD structure on file, ~100,
including tonight's class dumps): on BOTH sides the odd gain is 9 (ODD9 holds for every non-grid structure) and the
even gain is >= 3, with minimum exactly 3 (attained at nullity 14 by all 39 c55-type structures, at 13, 12, 11, 10).
So the decisive conjecture is the conjunction of two NON-GRID laws: (ODD9-NG) and (EVEN3-NG), or just their combined
form e_l - d_l >= 3 for non-grid blocks.
PROVED (bookkeeping): every component W of H_m gives the side relation kappa_W^m in ker T, i.e. sum over the outer
letters w of W of g_w is congruent to 0 modulo span(X_l) (the l-component also contains the C4 labels, which lie in
X_l).  In a NON-GRID block every part W of H_m contains outer letters, so these are c(m) independent relations on
the g's: e_l = 10 - c(m) - (rank of the m-even profiles of the mixed relations modulo the part indicators) <= 10 - c(m).
In a GRID block the part {0, 1} of H_m has no outer letter, so only c(m) - 1 such relations exist and e_l <= 11 - c(m):
the bookkeeping already differs by one between the two cases.  So (EVEN3-NG) <=> in a non-grid block the m-even
profiles of the mixed relations have rank <= 7 - c(m) - d_l (modulo the part indicators).  Grid blocks escape here
(c22 grid objects: 9 mixed relations with c(m) = 2).

## 9. (19:30-19:45 UTC) (N9-NG) contains (B'); positivity-free evidence inside kernel classes
- A grid on (l, m) makes {m} a singleton part of H_l and {l} one of H_m, so c(l), c(m) >= 2.  Hence every block with
  min(c) = 1 is NON-GRID, and (N9-NG) at min c = 1 reads 'nullity <= 10': this is (B') (AUDIT O1/O7) in sharpened form.
  The night's data for (B'): 280 424 logged PSD visits with a c = 1 line, maximal nullity exactly 10 = 9 + 1.  So the
  min c = 1 case of (N9-NG) has, besides the ~100 saved structures, this large walk support (one lineage, c11/c21/c31).
- Positivity-free test (kernel_sat_enum.py new option CREPORT: c, grid flag, T and U signs, slack nu - 9 - min c, over
  ALL members of a class): c55 class (642, complete): 418 non-grid members (6 PSD, 216 with T >= 0 only, 196 with
  neither), all with nu = 14, c = (5,5), slack 0; the 224 grid members have slack 1-2.  sq8_id_disc_c55 class (742,
  complete), harv_h_c55 class (642, complete), c1_G1_c34 class (stopped) and two c34 single-drop classes with NOSQ
  (2 113 stopped, 2 308 complete): several thousand non-grid members, PSD or not, T >= 0 or not, ALL with slack <= 0
  (equality at (13, (4,4)), (13, (4,5)), (14, (5,5))); every violation of the (N9) bound in these classes is a grid.
  Caveat: these classes impose a 12- to 14-dimensional kernel close to the c55 / c34 lineages, and without T >= 0 the
  component vectors are not automatically in ker T (G21 needs T_S >= 0 for the Y-rows), so a positivity-free theorem is
  not yet suggested beyond these classes.  The new walk mode 'n9ng' (sym4g.py, positivity ignored) collapses to
  nullity 4 at once: the objective is too flat without positivity.
- Grid-forcing groups: with the no-square clause the Z5h group (order 10) has no admissible structure (an element
  fixing the four star letters and moving every outer letter forces tau_0(2) = 3, tau_1(2) = 3, tau_2(0) = 1,
  tau_3(0) = 1); the HB_1 KHOMOG class and the obj53 class contain no non-grid member at all (complete).

## 10. (19:35 UTC) Campaign results (all tools of the previous days), and state
- Klein groups, cold schur walks with the no-grid clause (7 min each; kng_*.log, klein_ng.log): <(0 1)M, (2 3)(4 6)(5 7)
  (8 10)(9 11)>, <(0 1)(4 6)(5 7)(8 10)(9 11)(12 13), (2 3)(same)>, <(0 1)(4 5)(6 7)(8 9)(10 11)(12 13), (2 3)(4 5)(6 7)
  (8 10)(9 11)(12 13)>: admissible non-grid structures exist but T, U >= 0 was never reached; <(0 1)(4 5)(6 7),
  (2 3)(8 9)(10 11)> and <(0 1)(4 6)(5 7), (2 3)(8 10)(9 11)>: no admissible non-grid structure at all;
  <(0 1)(4 6)(5 7)(8 10)(9 11), (2 3)(4 6)(5 7)(8 10)(9 11)> (group 3): 201 PSD visits, Schur rank >= 14, no violation.
- Sub-kernel sweeps with NOSQ (39 single drops from sq8_id_disc_c55, c1_G1_c34, schur_h_c11; drop_ng.log): PSD members
  of nullity 14 only from the first two seeds, 15 distinct structures in all (with the class dumps), every one of type
  non-grid c = (5,5), t = (8,8), and every one fails F7 (rank_7 = 30 > 28) and DISC (r7_scan.py, disc_scan.py; files
  hmatch_tools_2026-10-15/ng14_distinct/).
- STATE: (N9-NG), (NG5), (NG7) OPEN, no counterexample; non-grid PSD nullity-14 world known = the c55 type only (G1
  family + h-invariant relatives), none a Conway block.  ODD9-NG and EVEN3-NG hold on every non-grid datum.  The main
  caveat is unchanged: the non-grid families reachable by our tools are few; cold starts in new non-grid families
  rarely reach positivity.
