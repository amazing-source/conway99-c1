# Region pairs: exact identities (Task 1) and the "seven h" question (Task 2)

Researcher 2 workspace, 2026-10-13. Read-only on all campaign data; everything computed here is under `work/c2_elegant_2026-10-13/region_pairs/`.
Every count below is an exact integer count produced by the scripts listed in section 7. Statements marked **(derived)** are my own short arguments, written out so that they can be checked; statements marked **(observed)** are data only.

## 0. Results in short

1. **Census reproduced.** Re-testing the 2,652 stored no-witness pairs of the 11 lattices directly (all vectors of norm 2, 3, 4 of U, all shadow vectors of norm 2 and 4): none has a witness (E <= 10); 1,610 violate the characteristic trap (a shadow vector with E <= 9.5, i.e. E < 11.5); **1,042 are region pairs**: 044: 896, 072: 96, 111: 32, 106: 16, 131: 2 (097, 120, 123, 124, 126, 130: none). These are exactly the numbers of the earlier survey.
2. **Task 1: all six predicted identities hold on all 1,042 region pairs** (N2 = s - 12, I12 = 4 - n11 + s/2, I13 = 8 - n11 + 3s/2, I15 = 96 - n11 - s, N3 = 688 + 2 n11 - s, S13 = 48 - 2 n11 + s). They take only 8 distinct value patterns (n11, s) in (0,24), (2,24), (0,32), (0,48), (2,48), (4,48), (8,60), (0,64). On the 1,610 trap violators every one of the six identities fails (so the trap condition is needed). Two further exact relations on the 1,042 region pairs: I16 = 164 + 2 n11 + s and S15 = 240 + 6 n11 - s (fitted on the 8 patterns, not proved).
3. **Task 2: seven pairwise orthogonal admissible h with the E = 11.5 hit sets partitioning the s classes exist for some region pairs and not for others.**
   - lattice 106 (all 16 pairs), 111 (all 32), 131 (both), 072 (all 96): no such 7-set (exhaustive search, orthogonality included). For 106 this is pure counting: every admissible h hits at least 8 of the s = 48 classes and 7 x 8 = 56 > 48.
   - lattice 044 (114 of 896 pairs sampled: every 8th, plus rows 1 and 3): the pairs fall in three kinds. Kind A (19 sampled): partitions exist but no 7-set satisfies the E = 13.5 condition (exhaustive). Kinds B (49) and C (46): there **are** 64 resp. 320 seven-sets per pair that satisfy every shadow condition of the frame that I could test (verified on the full shells), and **all** of them (17856 sets) fail the word-cell test (some of the 42 cells (pair {c,d}, Same/Opp) contains no norm-3 vector orthogonal to y1, y2: 6 empty cells in every set of kind B; 1, 2 or 4 in kind C). So for 044 the counting on shadow vectors alone does not exclude the pairs; the exclusion needs the norm-3 words.
4. Not done: the 782 unsampled pairs of 044 (plan in section 6), shadow vectors of norm >= 6, anything about the old engine beyond its "empty cells" rule.

## 1. Data, code, certificates

- Lattice U: the basis `basis` stored in `t20-codex/measures/hand_28/<lid>.json` (this is the LLL basis used by the campaign producer); Gram matrix G = B B^T computed in exact rationals, integral, exact determinant 1, no vector of norm 1. Pairs: the integer coordinates (in that basis) of y1, y2 stored in `<lid>_pairs.npz`; only rows with stored minimum E >= 11 (the "survivors") are used. Each pair is re-validated: (y1,y1) = (y2,y2) = 7, (y1,y2) = 0.
- Enumeration code: `fp_enum`, `ldl`, `short`, `solve_mod2` copied from `c2_experimental/c2_cloud_run_v10/scripts/frame_dfs_next.py` (Fincke-Pohst in floats; the norm of every returned vector is re-checked in int64). Run with the lab venv interpreter (it has numba) with `-B`, so nothing is written next to campaign files.
- **Completeness certificate (independent of the campaign):** for each lattice the shell sizes N2, N3, N4 found by enumeration equal (i) the stored exact counts `SHELL_COUNTS_EXACT_2026-10-07.json` and (ii) the coefficients of the theta series predicted by the Gleason-type theorem for odd unimodular lattices of rank 24 with N1 = 0 (Theta_L = sum_j a_j th3^(24-8j) D8^j; the shadow series is obtained by z -> 1 - 1/z; a_3 = 0 because the shadow has no vector of norm 0; computed in exact rationals in `rp_lib.theta_predictions`). The same series predicts the shadow shells: norm 2 has N2 + 48 vectors and norm 4 a number that depends on N2 only; both equal the enumerated counts (e.g. lattice 044: N2 = 96, N3 = 4096, N4 = 95,952, shadow norm 2: 144, norm 4: 193,152). Since every enumerated vector is exact and distinct, equality of counts means that no vector is missing.
- Exact arithmetic: norms and E in int64; products of shell vectors with y1, y2, h are obtained from float64 matrix products of integer matrices with entries < 2^20 and 24 terms (every partial sum is an integer < 2^53, so the result is exact) and are rounded back to int64 and used as integers.
- Peak memory measured (Windows peak working set, `rp_peakmem.py`): 718 MiB in a Task 2 run on lattice 044 (480 MiB after loading the lattice and its shells), below the 2 GB bound; every run took less than 5 minutes (the scan of lattice 044 took 72 s; the 044 batch was the longest batch).

## 2. Census of the stored no-witness pairs (my recomputation)

| lattice | roots | pairs in hand_28 file | no-witness pairs (stored) | of these: witness found by my recheck | no witness but trap violation | region pairs |
| --- | --- | --- | --- | --- | --- | --- |
| 044 | 96 | 144256 | 1920 | 0 | 1024 | 896 |
| 072 | 128 | 11968 | 240 | 0 | 144 | 96 |
| 097 | 160 | 4584 | 32 | 0 | 32 | 0 |
| 106 | 176 | 364 | 32 | 0 | 16 | 16 |
| 111 | 192 | 3024 | 320 | 0 | 288 | 32 |
| 120 | 208 | 700 | 12 | 0 | 12 | 0 |
| 123 | 216 | 776 | 52 | 0 | 52 | 0 |
| 124 | 224 | 416 | 16 | 0 | 16 | 0 |
| 126 | 224 | 244 | 8 | 0 | 8 | 0 |
| 130 | 232 | 340 | 16 | 0 | 16 | 0 |
| 131 | 240 | 26 | 4 | 0 | 2 | 2 |
| **all** |  |  | 2652 | 0 | 1610 | 1042 |

"Region pair" = no vector of norm 2, 3, 4 with E <= 10 and no shadow vector of norm 2 or 4 with E < 11.5. The stored pairs are the survivors of the campaign's lemma-only census (y1 runs over representatives up to the Weyl group that have no root r with (r,y1) = +-2; y2 is taken up to sign), so "region pair" here means region pair of that list. Whether that list is complete (producer completeness) was not re-proved; the campaign's own caveat stands.

Why the two ranges suffice **(derived)**. Let a = (v,y1), b = (v,y2). Replacing v by v + m y1 + n y2 changes a by 7m and b by 7n, so each coset v + J has exactly one representative with a, b in [-3,3]; its norm is smaller than or equal to that of every other member of the coset (the norm changes by m(7m + 2a) >= 0 for |a| <= 3). E is constant on the coset and 7 N = E + a^2 + b^2 <= E + 18. Hence a coset with E <= 10 has a representative of norm N <= 4, and N = 0 means v in J; N = 1 does not occur. J is primitive and K = J^perp has determinant 49 because a primitive-closure index 7 would give a unimodular rank-2 lattice, i.e. Z^2, with norm-1 vectors. The same argument for the shadow (p_i = 2(b,y_i) odd, shifted by 14 when b moves by y_i, representative with p_i in {-5,...,7}; here the two values +-7 of one product are the same coset and only +7 is counted) gives 4E(b) = 28 k - p1^2 - p2^2 with k the norm of b (even), E(b) in {..., 9.5, 11.5, 13.5, 15.5, 17.5, ...} (4E == 6 mod 8), and N >= 6 forces E(b) >= 42 - 24.5 = 17.5. So shadow norms 2 and 4 contain every coset with E(b) <= 15.5, and the trap test (all E(b) >= 11.5) needs nothing else.

## 3. Task 1: exact identities

Conventions (as in the task): n11 = (number of cosets v + J with E = 11)/2, I12, I13, I15 likewise; cosets are counted by their window representative and the result is divided by 2 for v <-> -v. N2, N3 count vectors of norm 2, 3 orthogonal to y1, y2 with both signs. s = (number of norm-2 shadow vectors with {|(b,y1)|,|(b,y2)|} = {1/2,3/2})/2; S13 = number of shadow cosets with E(b) = 13.5 (norm 2 with products (+-1/2,+-1/2) and norm 4 with products (+-7/2,+-3/2) or (+-3/2,+-7/2)), divided by 2. All of this is also stored for E = 14, 16 (I14, I16) and E(b) = 15.5 (S15).

**Which norms are needed (derived).** With the window, 7N = E + a^2 + b^2 and a^2 + b^2 <= 18. E = 11: N = 3, products {1,3} (N = 4 would need 17 = 1 + 16, |4| > 3). E = 12: N = 2 products (1,1) or N = 3 products (0,3). E = 13: N = 2 (0,1) or N = 3 (2,2). E = 15: N = 2 would need a^2 + b^2 = -1, N = 3 would need 6 (not a sum of two squares), N = 4 needs 13: products {2,3}. So **I15 needs only norm 4**, and norm 5 is not needed for E <= 16: a norm-5 coset has E = 35 - a^2 - b^2 >= 17, the first case being E = 17 with products (+-3,+-3). (For E = 14: only N = 2, products (0,0), so I14 = N2/2; for E = 16: only N = 3, products {1,2}.) For shadow cosets with E = 11.5 only norm 2 occurs (66/4 is not a sum of two odd squares over 4), E = 13.5: norm 2 with (1/2,1/2) and norm 4 with (7/2,3/2).

### 3.1 The ten pairs treated in detail (five lattices)

| lattice | pair (row in <lid>_pairs.npz) | n11 | s | N2 | N3 | I12 | I13 | I15 | S13 | six identities hold |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 044 | 1346 | 0 | 24 | 12 | 664 | 16 | 44 | 72 | 72 | yes (6/6) |
| 044 | 1820 | 0 | 24 | 12 | 664 | 16 | 44 | 72 | 72 | yes (6/6) |
| 044 | 1863 | 2 | 24 | 12 | 668 | 14 | 42 | 70 | 68 | yes (6/6) |
| 072 | 550 | 0 | 32 | 20 | 656 | 20 | 56 | 64 | 80 | yes (6/6) |
| 072 | 2242 | 0 | 32 | 20 | 656 | 20 | 56 | 64 | 80 | yes (6/6) |
| 106 | 32 | 2 | 48 | 36 | 644 | 26 | 78 | 46 | 92 | yes (6/6) |
| 106 | 73 | 4 | 48 | 36 | 648 | 24 | 76 | 44 | 88 | yes (6/6) |
| 106 | 76 | 0 | 48 | 36 | 640 | 28 | 80 | 48 | 96 | yes (6/6) |
| 111 | 267 | 8 | 60 | 48 | 644 | 26 | 90 | 28 | 92 | yes (6/6) |
| 131 | 5 | 0 | 64 | 52 | 624 | 36 | 104 | 32 | 112 | yes (6/6) |

"row" is the row index of the pair in `t20-codex/measures/hand_28/<lid>_pairs.npz` (arrays `o`, `y2`). The pair coordinates y1, y2 are in `region_pairs.json` (task1.chosen_pairs). **All six identities hold for all ten.** (They also hold for each of the 1,042 region pairs, section 3.2.)

Raw counts of the same ten pairs (both signs, before dividing by 2), so that a factor can be traced:

| lattice | row | cosets E=11 (both signs) | E=12 | E=13 | E=14 | E=15 | E=16 | norm-2 shadow vectors with products {1/2,3/2} | shadow cosets 4E=46 (E=11.5), both signs | 4E=54 (E=13.5) | 4E=62 (E=15.5) | min E over norms 2,3,4 | min 4E over shadow norms 2,4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 044 | 1346 | 0 | 32 | 88 | 12 | 144 | 376 | 48 | 48 | 144 | 432 | 12 | 46 |
| 044 | 1820 | 0 | 32 | 88 | 12 | 144 | 376 | 48 | 48 | 144 | 432 | 12 | 46 |
| 044 | 1863 | 4 | 28 | 84 | 12 | 140 | 384 | 48 | 48 | 136 | 456 | 11 | 46 |
| 072 | 550 | 0 | 40 | 112 | 20 | 128 | 392 | 64 | 64 | 160 | 416 | 12 | 46 |
| 072 | 2242 | 0 | 40 | 112 | 20 | 128 | 392 | 64 | 64 | 160 | 416 | 12 | 46 |
| 106 | 32 | 4 | 52 | 156 | 36 | 92 | 432 | 96 | 96 | 184 | 408 | 11 | 46 |
| 106 | 73 | 8 | 48 | 152 | 36 | 88 | 440 | 96 | 96 | 176 | 432 | 11 | 46 |
| 106 | 76 | 0 | 56 | 160 | 36 | 96 | 424 | 96 | 96 | 192 | 384 | 12 | 46 |
| 111 | 267 | 16 | 52 | 180 | 48 | 56 | 480 | 120 | 120 | 184 | 456 | 11 | 46 |
| 131 | 5 | 0 | 72 | 208 | 52 | 64 | 456 | 128 | 128 | 224 | 352 | 12 | 46 |

(Reading: "cosets E=11 (both signs)" = 2 n11; "norm-2 shadow vectors with products {1/2,3/2}" = 2 s; "shadow cosets 4E=54" = 2 S13. Every region pair has min E over norms 2,3,4 equal to 11 or 12 and min 4E over the shadow equal to 46.)

### 3.2 All 1,042 region pairs

Value patterns (each pattern is a set of pairs; all pairs of a row have identical (n11, s, N2, N3, I12, I13, I15, S13)):

| lattice | pairs | n11 | s | N2 | N3 | I12 | I13 | I15 | S13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 044 | 512 | 0 | 24 | 12 | 664 | 16 | 44 | 72 | 72 |
| 044 | 384 | 2 | 24 | 12 | 668 | 14 | 42 | 70 | 68 |
| 072 | 96 | 0 | 32 | 20 | 656 | 20 | 56 | 64 | 80 |
| 106 | 4 | 0 | 48 | 36 | 640 | 28 | 80 | 48 | 96 |
| 106 | 8 | 2 | 48 | 36 | 644 | 26 | 78 | 46 | 92 |
| 106 | 4 | 4 | 48 | 36 | 648 | 24 | 76 | 44 | 88 |
| 111 | 32 | 8 | 60 | 48 | 644 | 26 | 90 | 28 | 92 |
| 131 | 2 | 0 | 64 | 52 | 624 | 36 | 104 | 32 | 112 |

Identity check: each of the six identities holds on 1042 of 1042 region pairs (and fails on none).
On the 1,610 no-witness pairs that violate the trap, each of the six identities fails on 1610 of 1,610 (i.e. on every one; e.g. lattice 106 row 71: n11 = 4, s = 48, N2 = 60 instead of 36).

Further exact relations on the 1,042 region pairs (fit on the 8 patterns above, residual 0): I14 = s/2 - 6 (= N2/2, consistent with N2 = s - 12), I16 = 164 + 2 n11 + s, S15 = 240 + 6 n11 - s. They are observations, not proofs.

### 3.3 Independent checks inside the scan

For every pair the counts n11, ..., I16 were computed twice: by the window filter on the shells and by moving every vector with the target E (all of norm 2, 3, 4, no window) to its window representative with exact integer arithmetic and counting distinct representatives; the two numbers agree for every pair and every E in 11..16 (an assertion in `rp_scan.py`, run on all 2,652 pairs). Every norm-2, 3, 4 vector outside J has E > 0 for every pair (so J is primitive in each case, consistent with the determinant argument).

## 4. Task 2: why no seven h?

### 4.1 Definitions and what was searched

H4 = norm-4 vectors of U orthogonal to y1, y2, up to sign. For a shadow vector b = v/2 and h in U, (b,h) = (v G h)/2 is an integer (checked). It is constant on b + J. "E11" = the s classes {+-b} with E(b) = 11.5, "E13" = the S13 classes with E(b) = 13.5 (norm 2 and norm 4 together), "E15" = the S15 classes with E(b) = 15.5. An h is **admissible** if |(b,h)| <= 1 on all E11 and E13 classes; its **hit set** is the set of E11 classes with |(b,h)| = 1.

A frame 7-set must have: h_c pairwise orthogonal of norm 4 and orthogonal to y1, y2; (1/2) sum h_c in U; for each shadow b: sum_c (b,h_c) odd and sum_c (b,h_c)^2 <= E(b) - 10.5. For the exhaustive searches I used the following successively stronger necessary conditions on the 7-set (all derived from the frame identity (F) at v = b, using only that the 42 words u_o are norm-3 vectors orthogonal to y1, y2 with (b,u_o) in Z + 1/2):

- **E11**: every E11 class is hit by exactly one h (hit sets disjoint, union = all s classes; an h with empty hit set is allowed).
- **E13**: in addition every E13 class is hit by 1 or 3 of the h (never 2, never >= 4).
- **exact 3**: in addition every E13 class b that is **not flex** is hit exactly 3 times, where flex means "some norm-3 vector x orthogonal to y1, y2 has |(x,b)| = 3/2" **(derived)**: if no such x exists then all |(b,u_o)| = 1/2, sum_o (b,u_o)^2 = 10.5 and (F) gives sum_c (b,h_c)^2 = E(b) - 10.5 = 3. For lattice 044 no norm-2 E13 class is flex (the lattice is "rigid" in the campaign's sense); for 072, 106, 111, 131 every E13 class is flex, so "exact 3" adds nothing there.
- Every set found was also tested for (1/2) sum h_c in U (coordinates of the sum even) and independently re-verified from scratch on the full shells (`rp_verify_solution.py`: Gram = 4 I, orthogonal to y1,y2, half-sum in U, and for **every** shadow vector of norm 2 and 4 and every U-vector of norm 2, 3, 4 the integrality, parity and the bound sum_c (v,h_c)^2 <= E; no violation in 20 of 20 sets checked for row 1863 and in all 64 sets of row 1820; shadow vectors of norm >= 6 are not covered).
- **word cells** (necessary, engine rules 16/18): in a frame the 42 words satisfy (h_c,u_o) = -C_co with columns e_i + e_j and e_i - e_j of Z^7. So for each of the 21 pairs {c,d} and each sign (Same: the two values multiply to +1, Opp: to -1) there must be at least one norm-3 vector orthogonal to y1,y2 whose products with the seven h are +-1 at c and d and 0 elsewhere. A 7-set with an empty cell cannot be part of a frame.

The search is an exact cover over the E11 classes with orthogonality, in numba (`rp_search.py`), branching on the uncovered class with the fewest candidates; it was validated against brute force over all 7-subsets on 46 random instances x 5 modes (`rp_search_selftest.py`, including the boundary sizes s = 64 and S13 > 64), and every set it returns has Gram matrix 4 I (re-checked).

### 4.2 Ten pairs, one line each

| lattice | row | rigid | s | |H4| | admissible | fail at E=11.5 | fail only at E=13.5 | orth. edges / vertices (density) | orth. set: found..bound | hit-set sizes of admissible h | admissible h hitting a given E=11.5 class | E=11.5 classes hit by no admissible h | 7-sets: E=11.5 partition | 7-sets: + E=13.5 hits in {1,3} | + exact 3 on non-flex classes | word-cell test (42 cells) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 044 | 1346 | yes | 24 | 5958 | 5384 | 48 | 526 | 6506733 / 5384 (0.449) | 16..21 | 0..13 | 1597..1613 | 0 | >= 5548 (capped at 3e6 nodes) | 0 (exh.) | 0 | - |
| 044 | 1820 | yes | 24 | 5958 | 5386 | 52 | 520 | 6513267 / 5386 (0.449) | 14..21 | 2..14 | 1597..1613 | 0 | 576 (exhaustive) | 64 (exh.) | 64 | 0 of 64 pass; empty cells {'6': 64} |
| 044 | 1863 | yes | 24 | 5964 | 5404 | 54 | 506 | 6559262 / 5404 (0.449) | 15..21 | 2..14 | 1602..1630 | 0 | 8384 (exhaustive) | 320 (exh.) | 320 | 0 of 320 pass; empty cells {'1': 128, '2': 128, '4': 64} |
| 072 | 550 | no | 32 | 5882 | 5224 | 68 | 590 | 6118710 / 5224 (0.449) | 16..21 | 4..18 | 1446..1547 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |
| 072 | 2242 | no | 32 | 5882 | 5232 | 72 | 578 | 6137244 / 5232 (0.449) | 16..21 | 4..19 | 1458..1562 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |
| 106 | 32 | no | 48 | 5736 | 5136 | 96 | 504 | 5903706 / 5136 (0.448) | 16..21 | 8..40 | 1416..1487 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |
| 106 | 73 | no | 48 | 5742 | 5168 | 96 | 478 | 5975934 / 5168 (0.448) | 18..21 | 8..40 | 1428..1514 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |
| 106 | 76 | no | 48 | 5730 | 5108 | 96 | 526 | 5833554 / 5108 (0.447) | 18..21 | 8..40 | 1390..1476 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |
| 111 | 267 | no | 60 | 5640 | 5108 | 126 | 406 | 5828838 / 5108 (0.447) | 15..21 | 8..44 | 1375..1465 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |
| 131 | 5 | no | 64 | 5578 | 4716 | 160 | 702 | 4960998 / 4716 (0.446) | 18..21 | 8..52 | 1234..1314 | 0 | 0 (exhaustive) | 0 (exh.) | 0 | - |

Notes. "orth. set: found..bound": a set of pairwise orthogonal admissible h of the given size was found by a randomized greedy search (60 restarts); the upper bound 21 holds for any set of pairwise orthogonal norm-4 vectors in K = <y1,y2>^perp **(derived)**: 22 of them would generate a sublattice of K (rank 22, det 49) of determinant 4^22 = 49 [K:L]^2, impossible since 4^22/49 is not a perfect square. The exact maximum was not computed (graphs of about 5,000 vertices and density 0.45). In every case at least 14 pairwise orthogonal admissible h exist, so 7 orthogonal admissible h are plentiful; what fails is the combination with the hit-set condition. In the E11 column, "(exhaustive)" is for the full exact-cover tree; for pairs 111/267 and 131/5 it was completed in a later run with a larger node limit (`batch_results.jsonl`).

### 4.3 What goes wrong, in counting terms, by lattice

**Common data (observed on the ten pairs).** |H4| is between 5,578 and 5,964; 84-91 % of them are admissible; the failures are always a product of absolute value 2 (never more): 48-160 h fail at E = 11.5 and 406-702 more fail only at E = 13.5; no admissible h violates the E = 15.5 bound (|(b,h)| <= 2). Every E11 class is hit by 1,234-1,630 admissible h (26-30 % of them), so no class is left without a hitter. The orthogonality graph on the admissible h has density between 0.446 and 0.449. The mod-2 span of the hit vectors (scratch check, `scratch_gf2_span.py`) has rank between 18 and 22 (six pairs checked: 131/5, 111/267, 106/32, 072/550, 044/1346, 044/1863) and always contains the all-ones vector, so there is no linear obstruction mod 2; the obstruction is a genuine exact-cover obstruction.

**Lattice 106 (16 of 16 pairs): pure counting.** Every admissible h hits at least 8 of the s = 48 classes (minimum over all 16 pairs is 8, maximum 40), and 7 x 8 = 56 > 48. Seven hit sets cannot be disjoint inside 48 classes, orthogonality is not even needed (`scratch_min_hit_sizes.py`; the exact cover without orthogonality is also empty, checked on row 32 with `scratch_cover_without_orthogonality.py`).

**Lattices 111 (32 of 32) and 131 (2 of 2): no disjoint cover.** The minimum hit-set size is again 8 (111: s = 60, 131: s = 64), 7 x 8 = 56 does not exceed s, so the size count alone does not decide; but the exact cover of the s classes by 7 admissible hit sets with pairwise disjoint hit sets is already empty without any orthogonality (checked on the first pair of each lattice; with orthogonality empty on all 34 pairs).

**Lattice 072 (96 of 96): orthogonality is what kills.** Minimum hit size 4 (7 x 4 = 28 <= 32). Disjoint exact covers of the 32 classes exist without orthogonality (88,736 for row 550), none is made of pairwise orthogonal vectors (exhaustive for all 96 pairs).

**Lattice 044 (114 of 896 pairs; s = 24, N2 = 12).** Kinds (by n11 and the number of admissible h): A = (n11 = 0, 5,384 admissible), B = (n11 = 0, 5,386), C = (n11 = 2, 5,404); the kind is a property I found by running the search, not a Task 1 invariant. The hit sets of admissible h have sizes between 0 (or 2) and 14. Here the 144 norm-2 shadow vectors ("shadow roots") form a spherical 2-design of R^24 (with v = 2b the coordinate rows used in the code, sum_v (v,x)^2 = 48 (x,x) for all x, i.e. sum over the shadow roots of (b,x)^2 = 12 (x,x), `design_test.json`; false for 072, 106, 111, 131 where the necessary integrality 3 | N2+48 fails or the form is not proportional). Consequently, for **every** h of norm 4 in K, the sum of (b,h)^2 over all 72 norm-2 shadow classes equals 24 **(derived from the design property; the identity sum over all norm-2 shadow vectors of (h,b)^2 = |S2| (h,h)/12 was checked for every h of H4 of the three chosen 044 pairs, key `design_check...` in `task2_results.jsonl`: true for the three 044 pairs, false for the others)**. For a 7-set, the E11 partition contributes 24 and the 48 root classes of E13 must then carry 7 x 24 - 24 = 144 = 3 x 48 hits: **no slack at all**, every root class must be hit exactly 3 times. This is what kills kind A: partitions exist (more than 5,000 per pair in the capped search), but with hits on E13 classes limited to 3 there is none (exhaustive, 19 of 19 sampled pairs; for row 1346 even the cap alone, without the parity condition, gives 0). Kinds B and C pass this stage: 64 (kind B, n11 = 0) and 320 (kind C, n11 = 2) seven-sets per pair, identical numbers in all sampled pairs of the kind. Their E13 hits are 1 or 3 everywhere (exactly 3 on the root classes), half-sum in U holds in all of them. **They are all killed by the word cells**: in kind B every one of the 64 sets has exactly 6 empty cells out of 42; in kind C (row 1863) 128 sets have 1 empty cell, 128 have 2 and 64 have 4 (`sevensets_044_row*.npz`; over all sampled pairs of the kind: {'1': 5888, '2': 5888, '4': 2944}). For row 1863, 244 of the 668 norm-3 vectors orthogonal to y1,y2 have exactly two non-zero products (all +-1) and they populate the 42 cells unevenly (0 to 7 words per cell, up to sign), so a single empty cell suffices.

**What this says about the premise of Task 2.** "No seven h" is true at the level of the shadow-hit counting (E11, E13) for 072, 106, 111, 131 and for kind A of 044, but it is **false** for kinds B and C of 044: there the 7-sets exist and survive all shadow conditions up to E = 15.5, and are removed only by the lattice-level requirement that all 42 word cells be non-empty.

### 4.4 All sampled pairs

| lattice | n11 | s | admissible h | pairs searched | 7-sets with E=11.5 partition (min..max per pair) | + E=13.5 hits in {1,3}, half-sum in 2U | + exact 3 on non-flex E=13.5 classes | 7-sets passing all 42 word cells | empty cells (of 42) per 7-set: histogram |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 044 | 0 | 24 | 5384 | 19 | 5492..7008 (capped) | 0..0 | 0..0 | - | - |
| 044 | 0 | 24 | 5386 | 49 | 576..576 | 64..64 | 64..64 | 0 of 3136 | {'6': 3136} |
| 044 | 2 | 24 | 5404 | 46 | 8384..8384 | 320..320 | 320..320 | 0 of 14720 | {'1': 5888, '2': 5888, '4': 2944} |
| 072 | 0 | 32 | 5224 | 48 | 0..0 | 0..0 | 0..0 | - | - |
| 072 | 0 | 32 | 5232 | 48 | 0..0 | 0..0 | 0..0 | - | - |
| 106 | 0 | 48 | 5108 | 4 | 0..0 | 0..0 | 0..0 | - | - |
| 106 | 2 | 48 | 5136 | 8 | 0..0 | 0..0 | 0..0 | - | - |
| 106 | 4 | 48 | 5168 | 4 | 0..0 | 0..0 | 0..0 | - | - |
| 111 | 8 | 60 | 5108 | 32 | 0..0 | 0..0 | 0..0 | - | - |
| 131 | 0 | 64 | 4716 | 2 | 0..0 | 0..0 | 0..0 | - | - |

(Pairs searched: lattices 072 (96), 106 (16), 111 (32), 131 (2) completely; lattice 044: indices 0, 8, 16, ... of the list of its 896 region pairs, plus indices 1 and 3. The search for the E11-only column on 044 kind A was capped at 3,000,000 nodes, so those numbers are lower bounds.)

### 4.5 Observations that are uniform across the pairs (observed unless marked)

1. All six Task 1 identities, including the cases n11 > 0; none holds on the trap violators.
2. Equal Task 1 invariants do not imply equal Task 2 behaviour: 044 rows 1346 and 1820 have the same (n11, s, N2, N3, ...) but 5,384 vs 5,386 admissible h and 0 vs 64 seven-sets at the E13 level.
3. Every h of H4 has |(b,h)| <= 2 for every shadow class of E <= 15.5 (values 0, 1, 2 only); every admissible h hits at least one E13 class.
4. For 044 the 144 norm-2 shadow vectors form a 2-design, which makes the E11 + E13-root counting exactly tight (24 + 144 = 168 = 7 x 24). In the other four lattices the norm-2 shadow vectors are not a 2-design and no such identity exists. **(derived)** If the roots were a design, "all root classes exactly 3, E11 exactly 1" is possible only when s = |S2|/6; for 044 this reads 24 = 144/6, equality.
5. The minimum hit-set size of an admissible h is 8 in 106, 111 and 131, 4 in 072, 0 or 2 in 044, while s/7 (the average hit-set size a partition needs) is 3.4, 4.6, 6.9, 8.6, 9.1 for 044, 072, 106, 111, 131: for 106 the minimum exceeds the average (hence the pure counting obstruction), for 111 and 131 it is just below it.
6. For 044 the kind of a pair (A, B, C) is not determined by its y1 representative: over the 114 searched pairs every one of the 16 y1 indices carries pairs of at least two kinds (most carry all three); whether the kind is an Aut(U)-orbit invariant was not tested.
7. "Odd number of hits on every E13 class" is equivalent here to "(1/2) sum h_c in U": in every solution of the odd-only search (3,948 sets for 044 row 1346, 416 for row 1820, 8,384 for row 1863) the half-sum was in U.

## 5. Statuses and caveats

- All results depend on: the hand_28 pair lists (producer completeness not re-proved), T16/T18/T20 only through the campaign's choice of pairs (my own witness test uses E <= 10 without invoking these lemmas, because the stored survivors have none), Theorem R only through the frame conditions quoted in the task. Nothing here is Lean-verified.
- The "exact 3 on non-flex classes" and "word cell" conditions are my derivations from the frame identity and R-i..R-iv as quoted in `DIGEST_T16_T18_T20_ENGINE.md` section 4; they are necessary conditions only.
- The word-cell test checks non-emptiness of the 42 cells only; it does not search for 42 compatible words. A 7-set surviving it would not be a frame.
- `rp_cells.py` (an early script) reports the number of pairs {c,d} with at least one empty sign cell (1 or 3 pairs for the 320 sets of row 1863, 6 pairs for the 64 sets of row 1820); the tables use the number of empty cells out of 42 (1, 2 or 4 for row 1863: a pair with both signs empty counts twice).

## 6. Not done and cost plan

- 044: 782 of 896 region pairs not searched. Cost: about 2 s per pair (measured 1.5-3.7 s), i.e. about 30 minutes in six runs of at most 5 minutes each; not launched. The result so far (0 of 17856 seven-sets pass the cells over 95 pairs of kinds B/C) suggests the same outcome, but it is not a proof for the rest.
- Shadow classes of norm 6 (16.8 million vectors; the classes with 17.5 <= E <= 23.5 have products (+-7/2,+-7/2) or (+-7/2,+-5/2)) were not enumerated; the Bessel bound sum_c (b,h_c)^2 <= 4E(b)/7 makes the frame condition automatic only for E >= 24.5.
- Exact maximum orthogonal set among admissible h not computed (found 14-18, bound 21).
- No attempt to derive the identities of Task 1 from theta functions; no attempt to find a counting proof for the 044 word cells (the 6 / 1-2-4 empty cells per set are data, not explained).
- The old engine's other stage-1 rules (stars, joint cells, hitter counts) were not reproduced; the old verdict "stage 1 empty: no 7 h" is therefore neither confirmed nor contradicted beyond the facts above (for 044 kinds B, C the engine must have used a rule stronger than the shadow-hit rules).

## 7. Files and commands (all in `work/c2_elegant_2026-10-13/region_pairs/`)

Interpreter for everything numeric: `C:\Users\RESEARCHER\Desktop\Recherche_Conway\c2_experimental\.venv\Scripts\python.exe -B <script>` (read-only use; numba compiled in memory). `make_outputs.py`, `make_report.py` run with plain Python.

| file | purpose |
|---|---|
| `rp_lib.py` | lattice loading, shells, shadow shells, theta certificate (copied campaign enumeration code) |
| `rp_scan.py <lid>...` | Task 1 scan of all stored survivors; writes `scan_<lid>.json` (11 lattices run: `rp_scan.py 131 106`; `072 097 111 120 123 124 126 130`; `044`) |
| `rp_search.py`, `rp_search_selftest.py` | exact cover DFS and its brute-force self-test |
| `rp_task2.py` | helper functions (window classes, +-pairing); its own `main` was superseded by `rp_task2_run.py` |
| `rp_task2_run.py <lid> <idx list> 01234 1e8` | Task 2 statistics and searches for the ten chosen pairs; appends to `task2_results.jsonl` (044: 0,1,3; 072: 0,18; 106: 0,2,3; 111: 0; 131: 0) |
| `rp_batch.py <lid> <range|everyK> 1e8 <budget> [E11 node limit]` | lean batch with cell test; `batch_results.jsonl` (131 0-1 and 111 0-31 were run twice, second time with E11 limit 2e7; the last record counts) |
| `rp_verify_solution.py 044 3 4 20` | independent verification of found 7-sets on the full shells |
| `rp_cells.py`, `scratch_*.py` | cell test of an early version, cell statistics, exact cover without orthogonality, mod-2 span, minimum hit sizes |
| `rp_dump_and_extras.py`, `rp_dump_sevensets.py` | npz dumps (`pair_data_<lid>_row<row>.npz`: H4, E11/E13 classes, product matrices; `sevensets_044_row1820.npz`, `sevensets_044_row1863.npz`), 2-design test, linear fits |
| `rp_peakmem.py` | peak memory measurement |
| `make_outputs.py`, `make_report.py` | assemble `region_pairs.json` and this report |
| `region_pairs.json` | all numbers (task1: all 1,042 pairs, ten pairs in detail with raw counts; task2: ten pairs, batch records, summaries) |
