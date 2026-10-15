# What is known about a putative srg(99,14,1,2) (compiled 14/10/2026 for the asymmetry campaign)

Compiled once from: my memory files (c1-start, asymmetric-srg-campaign, route-c, mission-c2-without-compute),
Codex's synthesis note 100 (lemmas L1-L23, conway99-c1 branch codex/c1-arithmetic-audit), my night note of 14/10
(work/c1_night_2026-10-14/NOTE_NIGHT.md) and the headlines of Codex's repository c1-asymmetry-audit (git log).
Status column: P = proof (who), M = machine with certificates, S = solver verdict without certificate,
C = Codex result not re-derived by me, H = heuristic/observation. Items are statements, not reproofs.

## A. Parameters, local geometry
| # | statement | status |
|---|---|---|
| A1 | srg(99,14,1,2): eigenvalues 14, 3 (x54), -4 (x44); Seidel matrix S = J - I - 2A with S^2 = 49 (I + J) | P |
| A2 | lambda = 1: every neighbourhood is 7K_2; 231 lines (triangles), 7 per point: partial quadrangle PQ(2,6,2) | P |
| A3 | mu = 2: every non-adjacent pair lies in exactly one induced quadrangle (2079 quadrangles) | P |
| A4 | local view at x: 14 inner vertices in 7 blocks, 84 outer vertices = edges of the cocktail party CP(7); the 14 "matchings" M_a (perfect matchings on 12 points) and 140 outer lines determine the graph | P |
| A5 | grids (3 x 3 rook subgraphs) are perfect codes; f_S = 7E 1_S has norm 14(18 - e(S)) for 9-sets | P (night) |
| A6 | N9: no 9-set spans exactly 17 edges (generalises "grid minus an edge forces the grid", Codex note 105 s.2) | P (night) |
| A7 | 4-vertex induced subgraph counts are forced: C4 2079, paw 8316, triangle+K1 13860, claw 27720, P4 91476, P3+K1 507276, 2K2 126819, K2+2K1 1517670, 4K1 1469160 | P (night, checked on srg(243,22,1,2)) |

## B. Symmetry
| # | statement | status |
|---|---|---|
| B1 | Literature (external input, summarised in work/LITERATURE.md and INVENTORY_C2_CAMPAIGNS.md F1, not re-proved): Makhnev-Minakova 2004 (an involution forces |Aut| to divide 42), Behbahani-Lam 2011 (prime orders), Crnkovic-Maksimovic 2020 (no group of order 6 or 9), Cesarz-Woldar 2025 (2 divides |Aut| => |Aut| divides 6; 7 divides |Aut| => Aut = Z7). Project inventory: |Aut| is 1, 2 or 3 | literature (corrected 14/10: the earlier line "a prime dividing |Aut| is 2 or 3" was my shorthand, not a quoted statement) |
| B2 | C2: no automorphism of order 2 (the project's Route C, 156/156, papers written) | P + M (project) |
| B3 | C3: no automorphism of order 3 (proof written; external review by Woldar-Cesarz in progress) | P (under review) |
| B4 | C7 excluded (memory: "with C2, C3, C7 excluded and Behbahani-Lam, every srg(99,14,1,2) is asymmetric") | P (project) |
| B5 | Hence Aut = 1: a Conway graph, if it exists, is ASYMMETRIC | follows from B1-B4 (whether the inventory line in B1 already uses C7 is not checked) |
| B6 | No regular spread: the quotient would be srg(33,12,1,6), multiplicity 44/7 not an integer; regular spreads occur in the (1,2) family only at v = 9 and 243 | P (12/10) |
| B7 | Not a conference graph (k = 14 != 2 mu = 4): no regular two-graph structure (this campaign, 14/10) | P |
| B8 | No Godsil-McKay switching set of ANY size (one switching class) in srg(v,k,1,2) for k >= 14: (k - delta)(m - 1) + m n_2m = 4m - 2 - delta^2 has no solution (NOTE_ASYM_PALEY 7.2); at k = 4 (Paley 9) such sets exist and return Paley 9. Several classes (t >= 2): not covered | P (this campaign, 14/10) |
| B9 | Forced-symmetry principle: for every partial structure H of a Conway graph (pairs freed), the number of completions of H is at least |Aut(H)|; a piece with a unique completion is rigid. At a vertex x, the matching data F_x has at least |Aut(F_x)| completions (|Aut(F_x)| <= 645120) | P (orbit-stabiliser + B5; NOTE 7.1, 8.4) |
| B10 | No symmetric srg(99,14,1,2) exists (B5), so an asymmetric one cannot arise from a symmetric one by any move (switching, trade): unlike every asymmetric srg at 25-26 (all children of the two-graph with group S3) and unlike the trades at 243 (which keep the stabiliser of the move) | P (consequence) |

## C. Torsion and grids (Codex's lemma corpus, note 100 and later notes)
| # | statement | status |
|---|---|---|
| C1 | L1 (Makhnev 1988): not grid-full | literature |
| C2 | L8: no Hamming point (no vertex on 21 grids); L7: a Hamming point is not fixed by an involution | P (Codex note 105; also by SAT on 14/10 night, T1) |
| C3 | L10 / notes 108-109: g(x) <= 17 grids per vertex; L11: torsions touch >= 4 classes; L12, L13, L14 (|C| = 2 by hand; 3, 4 by SAT) | P / S |
| C4 | L15: P = 1386 - sum_x |W(x)| / 6 (P = prisms, |W(x)| = twisted pairs at x, out of 84) | P |
| C5 | L16: P <= 1151 (cubic Cauchy-Schwarz); later P <= 1150 (Codex), P <= 852 by order-9 positivity, P + 5 rho <= 1386 | P / C |
| C6 | grids rho <= 191 (six prisms per grid), <= 126 (order-9 positivity) | P / C |
| C7 | H + 3P = 213444 (Reimbayev formula, note 123) | C |
| C8 | prism closure: the three completing vertices of a prism never induce a path (N9) | P (Codex, re-derived) |
| C9 | twin prisms: <= 2871 pairs (Codex); structure theorem of twins via grids (08/10) | C / P |
| C10 | kk6: no vertex on 15 grids spanned by six of its lines; kk5: five lines pairwise in grids force the grid on the other two | S / M (DRAT) |
| C11 | 598 of the 790 local types of a line with 12 prisms are impossible (Codex 14/10) | C |

## D. Arithmetic, lattices, 7-adic
| # | statement | status |
|---|---|---|
| D1 | L2, L4: k = rank_7(A - 3I) - 15 is even, the same at every vertex; L22: k <= 28; window r = rank_7(A + 4I) in {37, 39, 41, 43} (r = 35 excluded 08/10) | P + M |
| D2 | K_- (integral -4-eigenvectors): min norm >= 14; norm 14 = co-Heawood (incidence of the (7,4,2) biplane); at most 792 such vectors (Codex 14/10), |f.g| in {0,1,2,4} between them, orthogonal families <= 12 | P / C |
| D3 | norm-16 integral eigenvectors: 1_P - 1_N with P, N cocliques of size 8, bipartite 4-regular skeleton | P (night) |
| D4 | integral 3-eigenvectors: entries <= 2 imply support >= 12 (equality: twin prisms); full classification for |h|_1 <= 16 (48 configurations, <= 911178 signed kernels) | P (night) / C |
| D5 | binary words of ker_7(A + 4I) have weight 0, 63 or 77 (note 178) | C (checked by Codex) |
| D6 | p-ary codes of the lines contain their duals (p = 2, 3, 5) | C |
| D7 | theta-LP (07/10): window r in {35..43} with a_7 <= 990 / 842, a_8 <= 27720, b_4 >= 2.73 million; night 14/10: rank_7(A + 4I) >= 35 by exact LP + certificates (a rediscovery, weaker than D1) | M (memory c1-start, NOTE_NIGHT) |
| D8 | Global attack 12/10: co-Heawood configurations without the rank condition leave about 3e22 second rows per base; norm 18 vectors are not killed by positivity; "critical path = norm 18 or 26 at every rank" | M / H (memory c1-start) |

## E. Cocliques, boundaries, completions (Codex's asymmetry repository, 12-14/10)
| # | statement | status |
|---|---|---|
| E1 | alpha <= 22 (Hoffman); a 22-coclique is a 2-(22,4,2) design structure; the coclique frame closes C1 only with alpha >= 21 | P |
| E2 | uniform 21-to-22 extension lemma; six-point Hoffman extensions excluded; radius-two family excluded | C |
| E3 | global integral completion criterion; rank-two reconstruction rigidity; positive 43-vertex boundary completion <= 8192 sign assignments; co-Heawood-free completion <= 2 sign choices | C |
| E4 | "complete grid star" excluded by symplectic reduction (= T1/L8) | C |

## G. Star objects at a vertex (added 14/10 evening; details and proofs in work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md)
| # | statement | status |
|---|---|---|
| G1 | T = 3I - Gamma - K on the 84 labels of x satisfies T^2 = 7T (rank 30); for Sigma = N[x] u S, T_S >= 0 iff lambda_2(A_Sigma) <= 3, U_S = 7 Pi_S - T_S >= 0 iff lambda_min(A_Sigma) >= -4, nullities = multiplicities of 3 and -4 (Haynsworth) | P |
| G2 | line l special (c(l) >= 2) iff H_l (cubic graph on the 36 neighbours of l) is disconnected iff lambda_2(H_l) = 3; components = closed configurations, mu = 1 components are straight 3 x 3 grids; rank of the H_l-far incidence = 35 - c(l) | P |
| G3 | binary 3-eigenvector code: dim 54, words of even weight >= 8 (Codex), F2^99 = C + C^perp | P |
| G4 | three stars (a, a' mates, b), c(l) = 1: the only binary relations are the stars (ChatGPT session shown by the user, checked); every PSD rank-30 three-star structure tested dies at its first outside label (Codex's column filter) | P / M |
| G5 | statement (A) 'T, U >= 0 and c(l) = 1 at three stars force rank 31' is FALSE: exact counterexample (52 found, all exactly verified 15/10; entry 38 non-extendable at the outside label {4,6} (colnorm), and all 52 have no rank-30 four-star completion: no profile for the fourth-star label {3,4}, ext3.py) | M (exact certificates) |
| G6 | H4 'no four-star structure is PSD' is FALSE: exact PSD structure, c = (3,4), rank 34 (Conway needs rank <= 30) | M (exact certificates) |
| G7 | four stars: D T D^T = 6I + 2(J - Mt) - E on outer partial stars (T >= 0 forces E <= 4 / <= 8 on the symmetric / antisymmetric sectors); U is positive definite on these sectors (Codex: a zero would give Gamma q = -16/5 q or -8/3 q) | P |
| G8 | (A4) 'T, U >= 0 at four stars forces c(l), c(m) >= 2': FALSE (14/10 23:30 UTC, fourstar_psd_c31_mix4.json has c(m) = 1, rank 34). [15/10 audit: the remark 'every PSD four-star structure found has c >= 3' of 14/10 is OBSOLETE: PSD structures with c = 1 (rank 34-35) and rank-30 ones with c = (2,2) exist; with a c = 1 line the nullity never exceeded 10 in 280 424 logged PSD visits, all from one lineage (G17).] | H |
| G9 | EXACT counts (forced in every Conway graph): for every vertex v and lines l, m through v, rank T_S4 = 30 - delta and rank U_S4 = 40 - epsilon, where delta = multiplicity of -4 and epsilon = dim of (E_0 + E_3)-vectors of the graph induced on the 40 'outer' labels (both letters off l and m); so the number of mixed relations is exactly 12 - c(l) - c(m) + [l, m span a grid] + delta. Same at three stars with the 50 complementary labels: rank T_S3 = 30 - delta'. Why: dim(E_3 n R^Sigma) = |Sigma| - 45 + dim((E_0 + E_-4) n R^(complement)); v has no neighbour among labels (kills E_0); -4 is the smallest eigenvalue of A, so -4-eigenvectors of an induced subgraph are global ones | P (LAB, 14/10 evening) |
| G10 | transversals: t(l) = fixed points of sigma_l (letters x with z_ax ~ z_a'x), P = (1/2) sum_l t(l), so C5 (P <= 852) forces the average t(l) <= 7.38; |W(x)| = sum over the 7 lines at x of (12 - t(l)) (consistent with C4) | P |
| G11 | bridge to aim at (OPEN): does the four-star local condition (T, U >= 0, rank <= 30) force many transversals? In the symmetric family G1 the rank-30 structures with T >= 0 have t = (8,8), the PSD rank-32 ones (6,6), the never-PSD c(l) = 1 ones 0 to 2. 't >= 8 on both lines' would give P >= 924 > 852 | H [15/10 audit: all 331 exact rank-30 PSD objects (two lineages, G1-c55 and Z5h, rank30_psd_objects_2026-10-15.json) have t = (12,12) (329) or (8,8) (2): the bridge 't >= 8 on both lines' (=> P >= 924 > 852, Codex's exact order-9 certificate) is CONSISTENT with every datum; caveat: none of these objects passes DISC, so none is a Conway block; targeted search with t <= 7 launched 03:00 UTC] |
| G12 | the four-star level ALONE is satisfiable: exact admissible four-star structure with T >= 0 of rank 30 and U >= 0 of rank 40 (c = (5,5), G1; night_urep_PSD_100.json). It is in no Conway graph: all 40 outer labels have no valid placement (ext4.py: (Tr) exact + (Tn)), and rank_7(8T_S4) = 30 > 28 | M (exact) |
| G13 | 7-adic and discriminant tests on star objects (principle = Codex's L4/L17/L22/L23 and note 217, NOT new): rank_7 of every principal block of 8T is <= k <= 28; a full-rank label set S has disc(8T_S lattice) = 2^69 7^(30-k) x square and disc(15U_S lattice) = 3^32 5^34 7^(40-k) x square. Codex (14/10, 23:50 UTC, codex_c55_mod7.json): the WHOLE G1 c55 non-grid family with T, U PSD has rank_7 >= 29, so it never extends to Conway | P (lemmas) / C (Codex enumeration, 145152 cases) |
| G14 | mixed-relation reduction (LAB grid_floor.py, Codex's identity): sum over the 21 pairs at v of mixed = 126 - 5 e(G_v) + 3 o_v + 6 h_v + Delta_v (G_v = grid graph on the 7 lines at v), so sum over all 2079 pairs >= 12474 - 45 rho >= 6804 (average >= 36/11). If every PSD four-star structure had <= 2 mixed relations: every vertex would need >= 18 grids, rho >= 198 > 191 (proved bound), and with L8, L10, kk5, kk6 no grid graph at a vertex is admissible at all; <= 3 mixed: >= 14 grids per vertex, rho >= 154 > 126 (census certificate). the cap is FALSE: exact PSD four-star structures with FOUR mixed relations and c(m) = 1 exist (fourstar_psd_c31_mix4.json, c21; group <(0 1)(2 3)>), so the route needs the rank condition; G1 data (<= 2) were biased | P (reduction) / M (cap refuted) |
| G15 | REFUTED 15/10 about 01:14 UTC (exact witness fourstar_psd_grid_Z5h_c62.json: grid, c = (6,2), rank 30, nullity 14 > 11; also (NOGRID) false) -- conjecture (N9): every admissible four-star structure with T, U >= 0 has nullity <= 9 + min(c(l), c(m)) (rank gain of the second line >= 12). PROVED reduction: (N9) => every Conway line has c >= 5 => rho >= 154 > 126 (census). ODD9 half (m-odd vectors add exactly 9) alone => every Conway line special. (NOGRID) + (LOW) would exclude Conway with no census. Evidence: about 100 000 PSD visits, bound attained exactly by c55 (rank 30), c11, c31 and h-asymmetric witnesses; U >= 0 essential (sc_2: T >= 0 only, nullity 16 > 15). Details: work/stars_rank_2026-10-14/N9_REDUCTION_2026-10-15.md | P (reductions) / REFUTED (conjectures) |
| G16 | (SQ3) every 45-vertex induced subgraph H of a Conway graph has det(A_H - 3I) = 7^(30-k) n^2 (a perfect square, divisible by 49 when non-zero); every 55-vertex induced subgraph has det(A_H + 4I) = 2 7^(40-k) n^2. Proof: all non-zero r x r principal minors of an integral symmetric matrix of rank r lie in one square class, equal to disc(MZ^n) (5-line lattice argument, LAB 15/10), and disc((3I-A)Z^99) = -11 7^44 / det Lambda_3 = -7^(30-k) (Codex L2/L22); constants for H containing N[v] re-derived locally (det K = 2^21 3^8 5^6, snf_D.py). Same principle as Codex notes 205/217/231/247 (not new). Use: the DISC test of a rank-30 four-star object (disc_scan.py). Status of the local four-star tests on 15/10: positivity, rank 30, rank_7 <= 28 all SATISFIABLE (exact witnesses incl. fourstar_psd_r7_25_Z5h.json, rank_7 = 25, refuting (R7)); every rank-30 object found fails DISC at 3 and 5 and/or the extension (40/40 outer labels for c55 and c62) | P (SQ3) / V (witnesses) |
| G17 | OPEN (B'): no admissible four-star structure with T, U >= 0 and rank <= 30 has a line with c = 1; it implies 'every line of a Conway graph is special' (c >= 2; PROVED implication via rank T_S4 = 30 - delta and rank T_X = 23 - c; corrected 15/10: not an equivalence, not c >= 2 + delta). Implied by ODD9 (the ten m-odd vectors add exactly 9 beyond X_l), which gives nullity <= 12 + min(c), attained by the c62 cluster. Evidence (15/10): ODD9 exact on every PSD structure in every family tested (G1, h, Z5h, identity), on all rank-30 objects (min c >= 2 always), and on the analogue in four real srg(243,22,1,2); without positivity the least eigenvalue of the odd Schur block gets down to 2e-5 (no exact failure on file). Max nullity seen with a c = 1 line: 10 (Conway needs 14). Details: work/stars_rank_2026-10-14/NOTE_PROOFS_1410.md (OPEN, ODD9 status) [15/10, corrected after review: in srg(243) the spectral c is not the component count of H_l; with the Conway meaning every tested real line is special, so the srg(243) comparison says nothing against (B')] | OPEN (E = evidence) |
| G18 | (PROVED modulo L8; LAB 15/10, reviewed) for every vertex v of a Conway graph some pair of lines (l, m) at v has a four-star block (T, U >= 0, nullity >= 14) whose star matchings are NOT h-related (M_1 != h(M_0) or M_3 != h(M_2), h = (0 1)(2 3), M_a = matching induced on the 12 labels {a,y}): otherwise every M_a is mate-aligned and v lies on 21 grids (Hamming point, L8). Same end with Makhnev (C1) or rho <= 191 (C6) applied at all vertices; variant: the 15 pairs among six lines + kk5 (M) + L8. work/stars_rank_2026-10-14/H_MATCH_REDUCTION_2026-10-15.md | P (modulo L8) |
| G19 | OPEN (H-MATCH): every admissible four-star structure with T, U >= 0 and nullity >= 14 has h-related star matchings. By G18 it would EXCLUDE Conway. Evidence (15/10): all 429 distinct saved structures of nullity >= 14 are h-invariant, but all come from h-families or short walks from h-invariant seeds; PSD with broken matchings reaches nullity 13 (hm_id_c22_HB_1.json); with T >= 0 alone the law is FALSE (kernel MILP: T exactly PSD, rank 30, broken matchings, U not PSD); none of the 129 kernels of the 331 rank-30 objects carries a PSD broken structure (MILP + complete SAT); two lines force 5k - 16 - g = 10 relations only for Conway among lambda = 1, mu = 2 parameters, so srg(243) is no test of it | OPEN (E) |
| G20 | (SQ30) explained (15/10): all 331 rank-30 PSD objects are invariant under h; their square class 2 3 5 7^e comes from integral eigenvalues 3, 5, 7 of T (the irrational part has class 1 in 319/331), and ker T = 12 h-even + 2 h-odd (the star differences). (SQ30) is therefore not evidence about Conway blocks, which need not be h-invariant (and by G18 cannot all be) | M (exact eigenspaces) / E |

## F. What is NOT known
No exclusion of C1; no ceiling on torsion beyond the 7-adic window; no forced small substructure of bounded search
size; the generic (high torsion, prism-poor) regime is untouched by every local lemma.
