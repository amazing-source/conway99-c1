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

## F. What is NOT known
No exclusion of C1; no ceiling on torsion beyond the 7-adic window; no forced small substructure of bounded search
size; the generic (high torsion, prism-poor) regime is untouched by every local lemma.
