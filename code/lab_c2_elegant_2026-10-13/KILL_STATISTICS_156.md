# Kill statistics for the 156 lattices of Route C: how the lattices die, from the records on this machine

Survey of 2026-10-13. Read-only: no record was modified, nothing was re-run, nothing was fetched from the cloud. Every number below is either (i) recomputed by the scripts listed in section 10 from the pair-level result records found on this machine, or (ii) quoted from a lab summary file or note, in which case the file is named. Where the two differ, section 11 says so. Verdict names are the raw strings found in the records; the mapping of these names to kind (a) / kind (b) is mine and is given separately in section 3.

## 0. Summary

- **156 lattices**: 135 have pair-level records on this machine (a set of records per lattice, section 4); 20 are excluded at lattice level with no pair enumerated (packing, criterion (E), Sol 0836, budget; lattice 143 by a hand budget proof); lattice 000 (odd Leech) has 141 pair classes, 86 closed by exact LP certificates and 56 by the exact o24 search (union = 141, two classes in both).
- **Pairs**: the 135 record sets contain **600,910,595 ordered pairs** in all (heterogeneous runs: different symmetry groups and engine versions, so not additive in any deeper sense). By first-fired rule label: swap-covered 246,375,941 (41.0%), characteristic-vector trap 270,456,898 (45.0%), twin bookkeeping (transfer + deferred + canon) 36,913,125, stage 1 empty 26,012,548, local/joint star sums 225,405, dual-minimum rule (T16, E = 8) 13,227,437, DEFERRED pending T18 (E = 9) 5,190,692, DEFERRED pending T20 (E = 10) 2,508,270, INCOMPLETE 279.
- **Split (a)/(b) on the pairs the engine actually decided** (swap and twin bookkeeping removed): kind (a) 20,926,399 of 317,621,529 (6.6%); kind (b) 296,694,851 (93.4%). **This split is biased by rule order** (section 2): the characteristic-vector trap fires before the dual-minimum test and before any T18/T20 witness is looked for, so a pair labelled 'char trap' may also carry a short vector.
- **Record sets and labels**: 135 of the 135 pair-level record sets contain at least one pair whose first-fired rule is a kind (b) rule (sets without any: none); kind (a) verdicts occur in 58 of the 135 sets (those run with engine v10 and the dual-minimum / deferral switches). This is a statement about labels, not about necessity.
- **What the records can say about necessity** comes from two separate censuses, not from the verdict labels: (1) the lab's lemma-only census of the 28 old pair-list lattices (hand_28): for every pair of the y1 left after Corollary Y1 a witness vector with E <= 10 was searched and stored; **17 of the 28 lattices have no pair left at all** (087, 096, 108, 115, 116, 119, 121, 122, 125, 127, 132, 135, 137, 138, 139, 140, 141), 11 have 2,652 pairs with no witness (044, 072, 097, 106, 111, 120, 123, 124, 126, 130, 131); (2) the Corollary-Y1 census over the 102 stream lattices: 42,276 of 54,096 y1 representatives (78.1%) have a root r with (r,y1) = +-2, and for **lattice 149 all 9 do**. So 18 lattices (the 17 plus 149) are, on the records, excluded without any frame search; all of that rests on T16, T18, T20 (statuses as the notes give them, not assessed here) and on the completeness of the y1/y2 enumerations.
- For the 11 lattices with surviving pairs, the notes give the pair-by-pair evaluation: of 2,652 pairs without a witness of energy <= 10, 1,610 are closed by the characteristic-vector rule, 1,004 go to the stage-1 search, 38 by the twin rule (aggregate text in `lemma/PROOF_C2/B_LATTICES.md` section B.6, aws_repo copy; not a per-lattice file).
- **Not found on this machine**: a pair-level lemma-only census for the other 107 pair-level lattices; per-pair verdicts (the records keep verdict counts per chunk, not a verdict per pair); the raw records of the 20 lattice-level exclusions (they have none).

## 1. What was read: files and fields

Roots: `LAB` = `C:\Users\RESEARCHER\Desktop\Recherche_Conway\c2_experimental`, `CODEX` = `C:\Users\RESEARCHER\Desktop\Recherche_Conway\t20-codex`. The local git checkout `LAB\aws_repo` is a partial clone (`blob:none`); I only listed its trees and read blobs that are already local, with `GIT_NO_LAZY_FETCH=1` (no network). All 18,679 result files named `results/<lid>_<k>_<n>.jsonl` on its 255 `origin/run/*` branches were local (0 missing).

| Source | Used for | Fields |
|---|---|---|
| git blobs `results/<lid>_<k>_<n>.jsonl` on `origin/run/*` (LAB\aws_repo, read with `git ls-tree` / `git cat-file`) and the working-tree copies `LAB\aws_repo\resultats_q|resultats|resultats_ci` (all duplicates of the blobs) | per-chunk records: deferral sweep, v10 re-runs, Golay blocks | `id, kind, chunk, range, n_pairs, pairs_total, sha256, producer, verdicts, deferred, not_excluded, telemetry (E_pair_trap, E_pair_search, search_K, trap_Yz), code_sha, chunk_ok, chunk_done, merged, machine, t` |
| `LAB\data\finishC\stream\<lid>\chunks.jsonl` (102 files), `...\golay\<lid>\chunks.jsonl`, `...\sweep\extra\105` | 29/09 stream sweep, Golay v4 blocks, lattice 105 re-run | same fields |
| `LAB\data\finishC\stream\<lid>\plan.json` | number of y1 representatives per lattice (selection of records) | `y1_reps` |
| `LAB\data\finishC\finishC_tracker.json` (live copy, 07/10 and later; differs from the 07/10 snapshot in 53 'by' texts) | status, root system label, number of roots, even neighbours, packing field, method text | `id, roots, nroots, nb1, nb2, status, by, packing, reviewed_by` |
| `LAB\aws_repo\lemma\PROOF_C2\B_TABLE_156.json` (newer copy than `CODEX\lemma\PROOF_C2\B_TABLE_156.json`) | method code per lattice (S, SD, GD, G, H, F, H3, O, P, EP, SP, So, B) | `rows[].id, method` |
| `LAB\logs\coxeter_table.jsonl` (156 lines, lab 02/10) | Coxeter numbers of the two even neighbours | `lid, Phi, P, h` |
| `LAB\aws_repo\measures\hand_28\<lid>.json` (28 files) | lemma-only census of the 28 old pair-list lattices | `y1, y1_with_root_of_product_2, y1_left, pairs, by_min_E, survivors` |
| `LAB\aws_repo\measures\TWIN_RESIDUE_AFTER_Y1_2026-10-07.json` | Corollary-Y1 census of the 102 stream lattices | `y1, y1_with_root_of_product_2` |
| `CODEX\measures\SWEEP_LAB_2026-10-07.json`, `STREAM_RECOUNT_2026-10-07.json`, `LAB\aws_repo\measures\RERUN_28_CHECK_2026-10-07.json`, `RERUN_713_CHECK_2026-10-07.json`, `RERUN_28_MANIFEST`, `RERUN_713_MANIFEST_LAB` | published numbers my selections are validated against (section 2) | `pairs`, class counts, `ok`, job lists |
| `LAB\data\finishC\o24_globallp`, `o24_cloud`, `o24_dfs`, `o24_ypairs.json` | lattice 000 | LP verdicts per class, DFS verdict and counts per class |
| `LAB\c2_cloud_run*\MANIFEST.json` | hashes of the package engines (tier P / L / N of a record) | `engine_code_sha` |
| `CODEX\lemma\upstream\AUDIT_ENGINE_RULES.md`, `BRIDGE.md`, `LATTICE_143.md`, `AUDIT_REDUCTION.md` A.9, `PROOF_C2\B_LATTICES.md` (both copies), `c2_cloud_run_v10\scripts\frame_dfs_next.py`, `hstage_stream_next.py`, `CODEX\q\defer_consumer.py`, `par_consumer.py`, `q\tools\lab_2026-10-07\import_sweep.py`, `stream_recount.py` | meaning and order of the rules, selection rules, special arguments | (text) |

## 2. How to read the numbers

1. **Pairs** are the ordered pairs (y1, y2) streamed by the producer in the run in question, under that run's symmetry group (Gamma-reduced for the 29/09 and deferral sweeps, identity-only up to the Weyl group for the 07/10 re-runs). Counts are not comparable across runs. The pairs removed by the producer's own filters (root with Y > 6, norm-3 vector with Y > 13, new-root conditions) are not in the records at all.
2. **A verdict is the first rule that fired, in the engine's fixed order**: producer filters, then in the stream consumer `swap` (SWAP-COVERED, I(y1) > I(y2)), then the twin rules (only if the characteristic trap does not fire), then in `search`: characteristic-vector trap, dual-minimum rule `Y = 13` (only with FD_MIN97=1), pair set-up (new-root conditions), and finally the frame search (stage 1, Lemma Z, local and joint star sums). In the deferral sweep a pair with a root r with (r,y1)^2 + (r,y2)^2 = 5 (or = 4 if none gives 5) is labelled DEFERRED pending T18 (resp. T20) instead of being searched to the end: in the quick variant (Q_DEFER_NODES=0, used since 07/10) **without any search**, provided neither the trap nor the dual-minimum test fires; in the earlier budget variant (10,000 nodes) only after the engine's own search returned INCOMPLETE. Which variant a given record used is not tabulated here (the field `deferral.defer_nodes` / `merged.defer_nodes` is in the raw records). Therefore a pair labelled 'char trap' may also have a short vector; the labels cannot be read as 'this pair needed a kind (b) rule'.
3. **Selection of records.** Several chunkings and several engines overlap in the stored records. For every lattice I re-implemented the lab's own selection (read from `import_sweep.py`, `stream_recount.py`, the RERUN checkers; not run): deferral lattices (001, 002, 003, 005-009, 011-015) as in the sweep import; the 91 stream lattices as in the 07/10 recount (tiers P/L/N); the 28 old pair-list lattices and 25 stream lattices from the v10 re-run records (chunks k/8, resp. k/16 or one job per representative; each job exists on two machines, counted once). **Validation:** pairs and class counts of my selections equal the published numbers for all 11 stream deferral lattices, all 91 recounted stream lattices (pairs, classes, tiers), all 28 + 25 re-run lattices (pairs and classes), lattice 105 (56,544) and Golay 002, 004, 010. One exception, Golay 001: see section 11.
4. **Primary record set** (the one used in the tables and totals). SD/GD: the deferral sweep; G (004, 010): Golay blocks of 02/10; S: the 29/09 stream records as selected by the recount (**STR**), except the 16 lattices (058, 070, 073-075, 078, 095, 098-102, 104, 107, 112, 114) that the tracker says were re-run as whole lattices with v10 and whose new records supersede the old ones (**R713**); for the 9 others of the 25 re-run lattices (043, 049-052, 055-057, 118) only some y1 representatives were re-run, the primary set stays STR and the re-run is listed under `other_record_sets` in the JSON; H/F/H3 (28 lattices): the v10 whole-lattice re-run (**R28**); 105: its v10 re-run (**X105**). Totals count each lattice once, in its primary set.
5. Rule shares: 'share of all pairs' includes swap and twin bookkeeping; 'share of substantive pairs' is over (a) + (b) + INCOMPLETE only.

## 3. Verdict names found in the records and my mapping

Twelve distinct verdict strings occur in the 19,045 distinct pair-level records (18,638 from git blobs, 407 only in lab chunk files). Counts below are for the primary record sets only.

| Raw verdict name | Class (mine) | Kind | Pairs in primary sets | Sources of the rule / flag |
|---|---|---|---|---|
| `EXCLUDED (char-vector trap)` | char_trap | b | 270,456,898 | frame identity at a norm-16 characteristic vector z: Y_z > 66 impossible (AUDIT_ENGINE_RULES 'Characteristic trap'; no T16/T18/T20). UNCERTAIN kind: requested list puts it in (b) |
| `SWAP-COVERED (I(y1)>I(y2))` | swap | dup | 246,375,941 | symmetry: the swapped pair (y2, y1) is treated in the same stream. Bookkeeping; the requested list puts 'swap' in (b) |
| `TWIN-DEFERRED` | twin_deferred | twin | 32,427,340 | twin lattice U+ has strictly more roots: pair is searched there; dependency on another lattice (1,622 dependencies, no cycle per notes) |
| `EXCLUDED (stage 1 empty: no 7 h)` | stage1_empty | b | 26,012,548 | frame search exhausted: no 7 mutually orthogonal admissible h covering the new roots (kind b) |
| `EXCLUDED (dual min 9/7: norm-3 x with Y=13)` | dual_min_9_7_Y13_E8 | a | 13,227,437 | norm-3 vector x with (x,y1)^2 + (x,y2)^2 = 13, E = 8; needs T16 (BRIDGE, AUDIT_ENGINE_RULES H5). Kind a |
| `DEFERRED (pending T18: root r with (r,y1)^2+(r,y2)^2 = 5)` | deferred_T18_E9 | a | 5,190,692 | root r with (r,y1)^2 + (r,y2)^2 = 5, E = 9; T18 through the bridge theorem. Not an engine exclusion: certificate + lemma. Kind a |
| `TWIN-CANON (k(U+)<k(U))` | twin_canon | twin | 2,863,005 | twin of the same type: canonical-rule bookkeeping |
| `DEFERRED (pending T20: root r with (r,y1)^2+(r,y2)^2 = 4)` | deferred_T20_root_E10 | a | 2,508,270 | root r with (r,y1)^2 + (r,y2)^2 = 4, E = 10; T20. Kind a. (The variant 'norm-4 x with |(x,y1)| = |(x,y2)| = 3' never occurs in the records) |
| `EXCLUDED (twin transfer)` | twin_transfer | twin | 1,622,780 | twin envelope U+ holds the same frame and its type is already excluded in the tracker. Requested list puts it in (b); it rests on another lattice's records |
| `EXCLUDED (no local star sums)` | no_local_star_sums | b | 225,401 | frame search: no local star sums (kind b) |
| `INCOMPLETE` | incomplete | inc | 279 | node limit reached; each of these pairs was searched again and excluded (set checked pair by pair per the notes) |
| `EXCLUDED (no joint star sums)` | no_joint_star_sums | b | 4 | frame search: no joint star sums (kind b) |

Verdict strings that exist in the engine source but occur in none of these records: `EXCLUDED (Lemma Z)`, `EXCLUDED (joint star sums, but (F) fails)` (the H1 census), `DEFERRED (pending T20: norm-4 x ...)`, `EXCLUDED (a y has |(y, beta)| > 3/2 at a new root ...)`, `EXCLUDED (both y hit the same new root ...)`, `EXCLUDED (pair budget)`, `EXCLUDED (too few candidates)`, `EXCLUDED (a root has Y > 6)`. The budget verdicts occurred only in the superseded 28-29/09 h-stage runs (not read here), which were replaced by the v10 re-runs; the rigid-kernel rule and the 'new roots' rule left no separate verdict in the stream records.

## 4. The 156 lattices by method

| Code | Meaning (B_TABLE_156) | Lattices | Primary record set in this survey |
|---|---|---|---|
| S | stream sweep, all pairs through the engine | 91 | STR (75 lattices) or R713 (16) |
| SD | stream sweep with T18/T20 deferral, engine v10 | 11 | DEF |
| GD | Golay pair files with T18/T20 deferral (001, 002) | 2 | DEF (pair tiling) |
| G | Golay pair blocks 02/10 (004, 010) | 2 | GOL4 |
| O | odd Leech, 141 pair classes (000) | 1 | none (O24 files) |
| H | h-stage sweep on C1 pair lists, 28-29/09 (13 lattices incl. 105) | 13 | R28 (12) / X105 (105) |
| F | frame_dfs + Lemma U+ on C1 pair lists, 27/09 | 14 | R28 |
| H3 | h-stage readings on C1 pairs (115, 132) | 2 | R28 |
| P | packing argument of C1 | 10 | none |
| EP | criterion (E) and packing | 3 | none |
| SP | Sol note 0836 and packing | 5 | none |
| So | Sol note 0836 and Theorem R A.9 (153) | 1 | none |
| B | budget identity, hand proof (143) | 1 | none |

Pair-level lattices: S 91 + SD 11 + GD 2 + G 2 + H 13 + F 14 + H3 2 = 135. Lattice-level: P 10 + EP 3 + SP 5 + So 1 + B 1 = 20. Odd Leech: 1. Total 156.

## 5. Totals and shares by rule (point 3)

Counts of pairs by first-fired rule, per record-set group. `twin` = transfer + deferred + canon. `star` = no local + no joint star sums.

| Group | Lattices | Pairs | swap | twin | char trap | stage 1 empty | star sums | E=8 dual min (T16) | E=9 DEFERRED T18 | E=10 DEFERRED T20 | INCOMPLETE |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DEF: deferral sweep (11 stream + Golay 001, 002) | 13 | 373,439,131 | 152,167,932 | 30,321,266 | 168,464,066 | 3,074,834 | 183,934 | 11,528,019 | 5,190,692 | 2,508,270 | 118 |
| STR: 29/09 stream sweep, as recounted | 75 | 218,063,643 | 92,858,258 | 6,101,886 | 96,186,187 | 22,386,790 | 14,536 | 515,825 | 0 | 0 | 161 |
| R713: v10 whole-lattice re-run (16 lattices) | 16 | 2,273,623 | 1,008,851 | 56,275 | 950,618 | 142,696 | 0 | 115,183 | 0 | 0 | 0 |
| R28: v10 whole-lattice re-run of the 28 pair-list lattices | 28 | 6,657,309 | 314,670 | 430,872 | 4,522,626 | 322,867 | 768 | 1,065,506 | 0 | 0 | 0 |
| X105: lattice 105 re-run | 1 | 56,544 | 26,230 | 2,688 | 20,124 | 4,598 | 0 | 2,904 | 0 | 0 | 0 |
| GOL4: Golay 004, 010 | 2 | 420,345 | 0 | 138 | 313,277 | 80,763 | 26,167 | 0 | 0 | 0 | 0 |
| **All 135 primary sets** | 135 | 600,910,595 | 246,375,941 | 36,913,125 | 270,456,898 | 26,012,548 | 225,405 | 13,227,437 | 5,190,692 | 2,508,270 | 279 |

Shares of **substantive pairs** (a + b + INCOMPLETE; swap and twin bookkeeping removed):

| Group | Substantive pairs | char trap | stage 1 empty | star sums | E=8 (T16) | E=9 (T18) | E=10 (T20) | kind (a) total | kind (b) total |
|---|---|---|---|---|---|---|---|---|---|
| DEF | 190,949,933 | 88.2% | 1.6% | 0.1% | 6.0% | 2.7% | 1.3% | 19,226,981 (10.1%) | 171,722,834 (89.9%) |
| STR | 119,103,499 | 80.8% | 18.8% | 0.0% | 0.4% | 0.0% | 0.0% | 515,825 (0.4%) | 118,587,513 (99.6%) |
| R713 | 1,208,497 | 78.7% | 11.8% | 0.0% | 9.5% | 0.0% | 0.0% | 115,183 (9.5%) | 1,093,314 (90.5%) |
| R28 | 5,911,767 | 76.5% | 5.5% | 0.0% | 18.0% | 0.0% | 0.0% | 1,065,506 (18.0%) | 4,846,261 (82.0%) |
| X105 | 27,626 | 72.8% | 16.6% | 0.0% | 10.5% | 0.0% | 0.0% | 2,904 (10.5%) | 24,722 (89.5%) |
| GOL4 | 420,207 | 74.6% | 19.2% | 6.2% | 0.0% | 0.0% | 0.0% | 0 (0.0%) | 420,207 (100.0%) |
| **All** | 317,621,529 | 85.2% | 8.2% | 0.1% | 4.2% | 1.6% | 0.8% | 20,926,399 (6.6%) | 296,694,851 (93.4%) |

Kind (a) verdicts occur in 58 of the 135 sets: 001, 002, 003, 005, 006, 007, 008, 009, 011, 013, 014, 015, 016, 044, 058, 070, 072, 073, 074, 075, 078, 087, 095, 096, 097, 098, 099, 100, 101, 102, 104, 105, 106, 107, 108, 111, 112, 114, 115, 116, 119, 120, 121, 122, 123, 124, 125, 126, 127, 130, 131, 132, 135, 137, 138, 139, 140, 141.
The 13 deferral lattices are the only ones with DEFERRED (T18/T20) verdicts: they carry 373,439,131 of the 600,910,595 pairs (62.1%).

## 6. Per-lattice table (points 1 and 5, first part)

Columns: `N2` roots; `h1/h2` Coxeter numbers of the even neighbours; `code` method code; `set` primary record set; `pairs`; counts by first-fired rule as in section 5 (`tw` = twin transfer + deferred + canon; `star` = star sums); `Y1` = y1 representatives with a root r, (r,y1) = +-2, out of all in the plan (stream lattices: TWIN_RESIDUE_AFTER_Y1; 28 pair-list lattices: hand_28; blank otherwise). Lattice-level lattices and 000 have no pair counts; see sections 7 and 8.

| id | roots | N2 | h1/h2 | code | set | pairs | swap | tw | trap | st1 | star | E8 | E9 | E10 | inc | Y1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 000 | (none) | 0 | 2/0 | O | - | - | - | - | - | - | - | - | - | - | - |  |
| 001 | a_1^8 | 16 | 2/2 | GD | DEF | 117,068 | 0 | 5 | 83,992 | 3,741 | 13,759 | 7,824 | 4,485 | 3,144 | 118 |  |
| 002 | a_1^{12} | 24 | 3/2 | GD | DEF | 718,422 | 0 | 75 | 528,950 | 80,672 | 87,367 | 11,089 | 6,675 | 3,594 | 0 |  |
| 003 | a_2^2a_1^{10} | 32 | 3/3 | SD | DEF | 17,757,312 | 6,916,412 | 2,519,461 | 8,023,462 | 9,217 | 12,647 | 193,261 | 39,642 | 43,210 | 0 | 96/182 |
| 004 | a_1^{16} | 32 | 4/2 | G | GOL4 | 416,383 | 0 | 128 | 310,500 | 79,661 | 26,094 | 0 | 0 | 0 | 0 |  |
| 005 | a_2^4a_1^8 | 40 | 4/3 | SD | DEF | 54,636,369 | 21,627,924 | 6,459,563 | 24,935,454 | 44,165 | 15,083 | 1,002,596 | 297,680 | 253,904 | 0 | 333/569 |
| 006 | a_3^2a_1^{12} | 48 | 4/4 | SD | DEF | 7,051,414 | 2,894,274 | 642,479 | 3,078,310 | 207,252 | 5,882 | 120,115 | 72,717 | 30,385 | 0 | 155/228 |
| 007 | a_3a_2^4a_1^6 | 48 | 4/4 | SD | DEF | 62,629,395 | 25,653,507 | 5,674,718 | 28,011,142 | 83,735 | 3,114 | 1,903,580 | 817,065 | 482,534 | 0 | 795/1234 |
| 008 | a_2^8 | 48 | 4/4 | SD | DEF | 10,026,322 | 4,034,967 | 806,623 | 4,603,536 | 19,801 | 737 | 314,364 | 152,429 | 93,865 | 0 | 106/183 |
| 009 | a_2^6a_1^6 | 48 | 5/3 | SD | DEF | 18,780,847 | 7,336,199 | 1,724,860 | 8,708,886 | 665,775 | 31,104 | 159,613 | 101,399 | 53,011 | 0 | 244/353 |
| 010 | a_1^{24} | 48 | 6/2 | G | GOL4 | 3,962 | 0 | 10 | 2,777 | 1,102 | 73 | 0 | 0 | 0 | 0 |  |
| 011 | a_3^2a_2^4a_1^4 | 56 | 5/4 | SD | DEF | 108,539,672 | 44,840,173 | 7,754,007 | 48,863,446 | 474,189 | 1,928 | 3,725,151 | 1,971,590 | 909,188 | 0 | 2015/2950 |
| 012 | a_2^8a_1^4 | 56 | 6/3 | SD | DEF | 2,624,309 | 992,259 | 202,439 | 1,244,367 | 182,851 | 2,393 | 0 | 0 | 0 | 0 | 76/102 |
| 013 | a_3^4a_2^2a_1^2 | 64 | 5/5 | SD | DEF | 21,063,451 | 8,793,030 | 946,396 | 9,492,478 | 902,506 | 7,527 | 846,801 | 64,761 | 9,952 | 0 | 759/1120 |
| 014 | a_4a_3a_2^4a_1^4 | 64 | 5/5 | SD | DEF | 37,020,901 | 15,757,820 | 1,920,308 | 16,110,189 | 179,834 | 213 | 1,733,911 | 984,326 | 334,300 | 0 | 1368/1877 |
| 015 | a_3^2a_3a_2^4a_1^2 | 64 | 6/4 | SD | DEF | 32,473,649 | 13,321,367 | 1,670,332 | 14,779,854 | 221,096 | 2,180 | 1,509,714 | 677,923 | 291,183 | 0 | 1171/1580 |
| 016 | a_3^4a_1^4a_1^4 | 64 | 6/4 | S | STR | 9,661,027 | 3,955,404 | 500,506 | 4,335,519 | 351,316 | 2,457 | 515,825 | 0 | 0 | 0 | 378/479 |
| 017 | a_3^4a_1^8 | 64 | 6/4 | S | STR | 1,193,626 | 490,889 | 59,830 | 538,192 | 104,152 | 563 | 0 | 0 | 0 | 0 | 67/88 |
| 018 | a_4a_3^2a_3a_2^2a_1^2 | 72 | 6/5 | S | STR | 57,409,330 | 24,338,864 | 2,089,775 | 25,624,704 | 5,348,827 | 7,158 | 0 | 0 | 0 | 2 | 2988/4116 |
| 019 | a_4^2a_2^4a_1^4 | 72 | 6/5 | S | STR | 12,492,920 | 5,387,288 | 453,065 | 5,442,408 | 1,209,127 | 1,032 | 0 | 0 | 0 | 0 | 690/887 |
| 020 | a_3^6 | 72 | 6/5 | S | STR | 1,080,309 | 440,811 | 30,213 | 503,004 | 105,955 | 326 | 0 | 0 | 0 | 0 | 64/100 |
| 021 | a_3^4a_2^4 | 72 | 7/4 | S | STR | 6,720,913 | 2,692,526 | 277,699 | 3,112,494 | 637,814 | 380 | 0 | 0 | 0 | 0 | 391/490 |
| 022 | d_4a_4a_2^6 | 80 | 6/6 | S | STR | 3,719,056 | 1,630,322 | 102,669 | 1,574,590 | 411,373 | 102 | 0 | 0 | 0 | 0 | 394/506 |
| 023 | d_4a_3^4a_1^4 | 80 | 6/6 | S | STR | 2,902,784 | 1,233,838 | 77,992 | 1,246,166 | 344,581 | 202 | 0 | 0 | 0 | 5 | 329/419 |
| 024 | a_5a_3^3a_1^6a_1 | 80 | 6/6 | S | STR | 3,331,604 | 1,433,455 | 102,581 | 1,408,316 | 387,071 | 127 | 0 | 0 | 0 | 54 | 386/473 |
| 025 | a_4^2a_3^2a_3a_1^2 | 80 | 6/6 | S | STR | 12,685,851 | 5,402,694 | 293,848 | 5,672,761 | 1,315,815 | 733 | 0 | 0 | 0 | 0 | 1115/1557 |
| 026 | a_5a_3^2a_2^4a_1 | 80 | 6/6 | S | STR | 5,525,802 | 2,421,561 | 158,777 | 2,348,183 | 597,177 | 80 | 0 | 0 | 0 | 24 | 533/685 |
| 027 | d_4a_3^4a_1^4 | 80 | 6/6 | S | STR | 1,858,950 | 806,679 | 47,086 | 802,700 | 202,423 | 62 | 0 | 0 | 0 | 0 | 184/232 |
| 028 | d_4^2a_1^{16} | 80 | 6/6 | S | STR | 50,646 | 19,524 | 1,989 | 21,006 | 8,084 | 4 | 0 | 0 | 0 | 39 | 18/20 |
| 029 | a_4^2a_3^2a_2^2a_1^2 | 80 | 7/5 | S | STR | 20,342,381 | 8,639,130 | 600,303 | 8,999,727 | 2,102,716 | 505 | 0 | 0 | 0 | 0 | 1747/2241 |
| 030 | a_3^4a_3^2a_1^4 | 80 | 8/4 | S | STR | 1,460,380 | 537,934 | 59,300 | 696,319 | 166,767 | 60 | 0 | 0 | 0 | 0 | 179/202 |
| 031 | a_4^4a_1^4 | 88 | 7/6 | S | STR | 2,051,633 | 892,694 | 37,933 | 899,307 | 221,653 | 46 | 0 | 0 | 0 | 0 | 284/363 |
| 032 | a_5a_4a_3a_3a_2a_2a_1 | 88 | 7/6 | S | STR | 19,608,530 | 8,558,894 | 397,692 | 8,543,747 | 2,108,067 | 130 | 0 | 0 | 0 | 0 | 2501/3250 |
| 033 | a_4^2a_3^4 | 88 | 8/5 | S | STR | 2,049,478 | 845,743 | 42,217 | 945,512 | 215,988 | 18 | 0 | 0 | 0 | 0 | 294/375 |
| 034 | a_4^2a_4a_3a_2^2a_1^2 | 88 | 8/5 | S | STR | 7,280,902 | 3,072,893 | 177,773 | 3,236,690 | 793,510 | 36 | 0 | 0 | 0 | 0 | 1028/1225 |
| 035 | a_5a_4^3a_1^3 | 96 | 7/7 | S | STR | 1,658,601 | 713,916 | 21,917 | 724,128 | 198,626 | 14 | 0 | 0 | 0 | 0 | 377/499 |
| 036 | a_5^2a_3^2a_2^2 | 96 | 7/7 | S | STR | 2,379,274 | 1,042,681 | 31,625 | 1,034,935 | 270,009 | 24 | 0 | 0 | 0 | 0 | 517/672 |
| 037 | a_6a_3^3a_2^3 | 96 | 7/7 | S | STR | 1,438,751 | 640,733 | 29,261 | 585,479 | 183,246 | 2 | 0 | 0 | 0 | 30 | 328/409 |
| 038 | d_4a_4^2a_4a_2^2 | 96 | 8/6 | S | STR | 4,421,657 | 1,903,417 | 59,259 | 1,957,676 | 501,295 | 10 | 0 | 0 | 0 | 0 | 912/1168 |
| 039 | a_5d_4a_3^2a_3a_1^2a_1 | 96 | 8/6 | S | STR | 3,948,897 | 1,707,032 | 66,063 | 1,712,707 | 463,086 | 9 | 0 | 0 | 0 | 0 | 811/971 |
| 040 | a_5^2a_3^2a_1^2a_1^2a_1^2 | 96 | 8/6 | S | STR | 1,720,526 | 735,941 | 32,436 | 747,164 | 204,976 | 9 | 0 | 0 | 0 | 0 | 382/434 |
| 041 | a_5a_4^2a_3a_3a_1 | 96 | 8/6 | S | STR | 4,400,394 | 1,898,206 | 62,031 | 1,949,956 | 490,193 | 8 | 0 | 0 | 0 | 0 | 909/1178 |
| 042 | d_4^2a_3^4 | 96 | 8/6 | S | STR | 546,423 | 233,946 | 5,988 | 242,895 | 63,591 | 3 | 0 | 0 | 0 | 0 | 133/169 |
| 043 | a_4^3a_3^3 | 96 | 9/5 | S | STR | 1,051,604 | 424,540 | 15,967 | 482,078 | 128,996 | 23 | 0 | 0 | 0 | 0 | 250/299 |
| 044 | a_3^8 | 96 | 10/4 | H | R28 | 5,488,960 | 0 | 345,792 | 3,919,936 | 260,096 | 768 | 962,368 | 0 | 0 | 0 | 1152/1168 |
| 045 | a_5^2a_4^2a_1^2 | 104 | 8/7 | S | STR | 2,340,518 | 1,010,569 | 21,956 | 1,033,179 | 274,806 | 8 | 0 | 0 | 0 | 0 | 671/893 |
| 046 | a_6a_4a_4a_3a_2a_1a_1 | 104 | 8/7 | S | STR | 4,087,798 | 1,820,436 | 48,398 | 1,743,885 | 475,079 | 0 | 0 | 0 | 0 | 0 | 1163/1417 |
| 047 | a_5^2a_4a_3a_2^2 | 104 | 9/6 | S | STR | 1,834,000 | 794,803 | 28,334 | 795,893 | 214,970 | 0 | 0 | 0 | 0 | 0 | 543/663 |
| 048 | a_4^4a_3^2 | 104 | 10/5 | S | STR | 301,557 | 117,635 | 6,255 | 141,103 | 36,562 | 2 | 0 | 0 | 0 | 0 | 98/110 |
| 049 | d_5d_4a_3^4 | 112 | 8/8 | S | STR | 296,093 | 128,727 | 3,370 | 119,480 | 44,512 | 2 | 0 | 0 | 0 | 2 | 163/196 |
| 050 | d_5a_5a_3^2a_3a_1^2a_1 | 112 | 8/8 | S | STR | 1,011,185 | 454,437 | 11,215 | 404,121 | 141,408 | 4 | 0 | 0 | 0 | 0 | 463/526 |
| 051 | a_5^2d_4^2a_1^2 | 112 | 8/8 | S | STR | 318,627 | 132,248 | 1,489 | 139,958 | 44,833 | 99 | 0 | 0 | 0 | 0 | 174/230 |
| 052 | a_7a_3^4a_1^4 | 112 | 8/8 | S | STR | 210,503 | 94,653 | 2,232 | 83,240 | 30,359 | 15 | 0 | 0 | 0 | 4 | 106/119 |
| 053 | d_5a_4a_4^2a_2^2 | 112 | 8/8 | S | STR | 1,141,132 | 513,881 | 10,086 | 460,805 | 156,360 | 0 | 0 | 0 | 0 | 0 | 482/590 |
| 054 | a_6d_4a_4^2a_2 | 112 | 8/8 | S | STR | 1,186,218 | 523,372 | 6,669 | 513,121 | 143,056 | 0 | 0 | 0 | 0 | 0 | 547/716 |
| 055 | a_6a_5a_4a_3a_2a_1 | 112 | 9/7 | S | STR | 2,118,801 | 934,263 | 16,600 | 901,631 | 266,226 | 81 | 0 | 0 | 0 | 0 | 856/1062 |
| 056 | a_5^2d_4a_3^2a_1^2 | 112 | 10/6 | S | STR | 802,087 | 328,793 | 7,578 | 351,519 | 114,159 | 38 | 0 | 0 | 0 | 0 | 346/392 |
| 057 | a_5a_5a_4^2a_3 | 112 | 10/6 | S | STR | 854,034 | 360,507 | 6,536 | 383,196 | 103,781 | 14 | 0 | 0 | 0 | 0 | 392/467 |
| 058 | a_5^2d_4a_3^2a_1^2 | 112 | 10/6 | S | R713 | 401,043 | 170,533 | 6,333 | 177,385 | 20,330 | 0 | 26,462 | 0 | 0 | 0 | 174/193 |
| 059 | d_4^4a_1^8 | 112 | 10/6 | S | STR | 2,562,400 | 901,680 | 50,063 | 1,184,880 | 425,633 | 144 | 0 | 0 | 0 | 0 | 1052/1072 |
| 060 | a_7a_4^2a_3^2 | 120 | 9/8 | S | STR | 568,181 | 257,939 | 3,626 | 238,210 | 68,406 | 0 | 0 | 0 | 0 | 0 | 322/401 |
| 061 | a_6^2a_4a_3a_1^2 | 120 | 9/8 | S | STR | 560,384 | 250,339 | 3,509 | 239,750 | 66,782 | 4 | 0 | 0 | 0 | 0 | 340/422 |
| 062 | a_6a_5a_5a_3a_2 | 120 | 10/7 | S | STR | 1,043,635 | 457,105 | 9,632 | 450,650 | 126,248 | 0 | 0 | 0 | 0 | 0 | 618/760 |
| 063 | a_6^2a_3^2a_2^2 | 120 | 10/7 | S | STR | 462,316 | 202,672 | 5,012 | 195,315 | 59,315 | 2 | 0 | 0 | 0 | 0 | 257/299 |
| 064 | a_5^4 | 120 | 10/7 | S | STR | 87,520 | 36,566 | 433 | 40,072 | 10,449 | 0 | 0 | 0 | 0 | 0 | 60/80 |
| 065 | a_7a_5^2a_2^2 | 128 | 9/9 | S | STR | 170,548 | 75,756 | 1,097 | 71,370 | 22,325 | 0 | 0 | 0 | 0 | 0 | 170/216 |
| 066 | a_7a_5a_4^2a_1 | 128 | 10/8 | S | STR | 304,034 | 137,334 | 1,344 | 127,190 | 38,166 | 0 | 0 | 0 | 0 | 0 | 254/319 |
| 067 | a_7a_5d_4a_3a_1a_1a_1 | 128 | 10/8 | S | STR | 559,433 | 246,747 | 4,004 | 235,305 | 73,377 | 0 | 0 | 0 | 0 | 0 | 454/519 |
| 068 | a_6d_5a_4a_4a_2 | 128 | 10/8 | S | STR | 620,319 | 278,763 | 2,902 | 259,930 | 78,724 | 0 | 0 | 0 | 0 | 0 | 512/622 |
| 069 | d_5^2a_3^4 | 128 | 10/8 | S | STR | 64,133 | 29,090 | 428 | 26,631 | 7,984 | 0 | 0 | 0 | 0 | 0 | 61/67 |
| 070 | d_5a_5^2d_4a_1^2 | 128 | 10/8 | S | R713 | 320,989 | 147,782 | 3,928 | 131,443 | 22,782 | 0 | 15,054 | 0 | 0 | 0 | 276/330 |
| 071 | a_5^2a_5d_4a_3a_1 | 128 | 12/6 | S | STR | 171,216 | 59,648 | 3,467 | 81,530 | 26,571 | 0 | 0 | 0 | 0 | 0 | 146/156 |
| 072 | a_5^4a_1^4 | 128 | 12/6 | H | R28 | 577,232 | 157,504 | 28,752 | 303,240 | 27,736 | 0 | 60,000 | 0 | 0 | 0 | 448/456 |
| 073 | a_8a_4^2a_3^2 | 136 | 10/9 | S | R713 | 161,453 | 74,701 | 3,342 | 66,338 | 8,224 | 0 | 8,848 | 0 | 0 | 0 | 159/185 |
| 074 | a_7a_6a_5a_2a_1 | 136 | 10/9 | S | R713 | 367,327 | 163,342 | 5,928 | 156,389 | 24,324 | 0 | 17,344 | 0 | 0 | 0 | 399/513 |
| 075 | a_6a_6a_5a_4a_1 | 136 | 12/7 | S | R713 | 248,990 | 106,424 | 7,260 | 109,711 | 12,392 | 0 | 13,203 | 0 | 0 | 0 | 290/330 |
| 076 | a_7^2d_4a_1^4 | 144 | 10/10 | S | STR | 52,015 | 21,631 | 302 | 22,277 | 7,805 | 0 | 0 | 0 | 0 | 0 | 99/116 |
| 077 | d_6a_5^2a_3^2 | 144 | 10/10 | S | STR | 62,031 | 27,348 | 501 | 23,142 | 11,040 | 0 | 0 | 0 | 0 | 0 | 105/122 |
| 078 | a_8a_5^2a_3 | 144 | 10/10 | S | R713 | 122,411 | 58,715 | 2,156 | 48,300 | 8,220 | 0 | 5,020 | 0 | 0 | 0 | 176/224 |
| 079 | d_6a_5^2a_3^2 | 144 | 10/10 | S | STR | 100,895 | 46,550 | 628 | 38,435 | 15,282 | 0 | 0 | 0 | 0 | 0 | 131/150 |
| 080 | d_6d_4^3a_1^6 | 144 | 10/10 | S | STR | 31,122 | 12,750 | 284 | 11,988 | 6,099 | 0 | 0 | 0 | 0 | 1 | 62/64 |
| 081 | a_7d_5a_5a_3a_1a_1a_1 | 144 | 12/8 | S | STR | 154,990 | 66,373 | 1,391 | 64,863 | 22,363 | 0 | 0 | 0 | 0 | 0 | 226/244 |
| 082 | d_5d_5a_5^2a_1^2 | 144 | 12/8 | S | STR | 90,976 | 38,391 | 541 | 37,973 | 14,071 | 0 | 0 | 0 | 0 | 0 | 144/162 |
| 083 | a_7d_5d_4a_3a_3 | 144 | 12/8 | S | STR | 166,234 | 72,681 | 1,363 | 69,180 | 23,010 | 0 | 0 | 0 | 0 | 0 | 257/288 |
| 084 | a_6a_6d_5a_4 | 144 | 12/8 | S | STR | 169,401 | 74,049 | 650 | 72,736 | 21,966 | 0 | 0 | 0 | 0 | 0 | 302/362 |
| 085 | d_5^2a_5^2a_1^2 | 144 | 12/8 | S | STR | 38,140 | 16,320 | 239 | 16,465 | 5,116 | 0 | 0 | 0 | 0 | 0 | 76/85 |
| 086 | a_6^2a_5^2 | 144 | 13/7 | S | STR | 74,583 | 29,904 | 1,151 | 32,925 | 10,603 | 0 | 0 | 0 | 0 | 0 | 115/130 |
| 087 | d_4^6 | 144 | 14/6 | F | R28 | 184,608 | 0 | 27,576 | 121,680 | 10,992 | 0 | 24,360 | 0 | 0 | 0 | 240/240 |
| 088 | a_8a_6a_5a_2a_1 | 152 | 12/9 | S | STR | 107,203 | 48,361 | 656 | 44,056 | 14,130 | 0 | 0 | 0 | 0 | 0 | 202/243 |
| 089 | a_7^2a_4^2 | 152 | 13/8 | S | STR | 49,570 | 21,052 | 484 | 21,196 | 6,838 | 0 | 0 | 0 | 0 | 0 | 93/109 |
| 090 | a_9a_5d_4a_3a_1a_1 | 160 | 12/10 | S | STR | 60,345 | 27,162 | 445 | 24,975 | 7,763 | 0 | 0 | 0 | 0 | 0 | 142/156 |
| 091 | a_7d_6a_5a_3a_1 | 160 | 12/10 | S | STR | 71,608 | 32,273 | 327 | 29,342 | 9,666 | 0 | 0 | 0 | 0 | 0 | 177/205 |
| 092 | a_8a_6d_5a_2 | 160 | 12/10 | S | STR | 67,915 | 30,617 | 264 | 27,640 | 9,394 | 0 | 0 | 0 | 0 | 0 | 208/261 |
| 093 | d_6d_5a_5^2 | 160 | 12/10 | S | STR | 32,952 | 14,984 | 58 | 12,966 | 4,944 | 0 | 0 | 0 | 0 | 0 | 110/128 |
| 094 | d_5^4 | 160 | 12/10 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 095 | a_8a_7a_4a_3 | 160 | 13/9 | S | R713 | 144,220 | 63,796 | 6,234 | 58,814 | 7,380 | 0 | 7,996 | 0 | 0 | 0 | 337/403 |
| 096 | a_7d_5^2a_3^2 | 160 | 14/8 | H | R28 | 99,236 | 38,976 | 5,800 | 43,084 | 4,944 | 0 | 6,432 | 0 | 0 | 0 | 246/262 |
| 097 | a_7^2d_4^2 | 160 | 14/8 | H | R28 | 90,984 | 39,080 | 3,240 | 40,512 | 5,120 | 0 | 3,032 | 0 | 0 | 0 | 300/332 |
| 098 | a_8^2a_3^2 | 168 | 13/10 | S | R713 | 82,476 | 36,128 | 3,264 | 34,844 | 5,104 | 0 | 3,136 | 0 | 0 | 0 | 272/320 |
| 099 | a_9a_6a_5a_2 | 168 | 13/10 | S | R713 | 93,802 | 42,630 | 3,248 | 38,304 | 5,184 | 0 | 4,436 | 0 | 0 | 0 | 266/328 |
| 100 | a_7^3 | 168 | 14/9 | S | R713 | 58,356 | 23,148 | 1,848 | 26,388 | 5,472 | 0 | 1,500 | 0 | 0 | 0 | 294/378 |
| 101 | d_7a_5^2a_5a_1 | 176 | 12/12 | S | R713 | 62,300 | 27,916 | 3,682 | 22,370 | 4,364 | 0 | 3,968 | 0 | 0 | 0 | 190/210 |
| 102 | a_9d_5^2a_1^2a_1 | 176 | 12/12 | S | R713 | 49,692 | 21,426 | 1,156 | 20,062 | 5,856 | 0 | 1,192 | 0 | 0 | 0 | 256/298 |
| 103 | a_7e_6d_4a_3^2 | 176 | 12/12 | S | STR | 17,228 | 7,816 | 219 | 6,021 | 3,172 | 0 | 0 | 0 | 0 | 0 | 72/79 |
| 104 | e_6a_6^2a_4 | 176 | 12/12 | S | R713 | 70,108 | 32,800 | 3,784 | 24,200 | 5,412 | 0 | 3,912 | 0 | 0 | 0 | 252/288 |
| 105 | e_6d_5a_5^2a_1^2 | 176 | 12/12 | H | X105 | 56,544 | 26,230 | 2,688 | 20,124 | 4,598 | 0 | 2,904 | 0 | 0 | 0 |  |
| 106 | d_6^2d_4^2a_1^4 | 176 | 14/10 | H | R28 | 49,612 | 20,092 | 2,760 | 20,112 | 3,408 | 0 | 3,240 | 0 | 0 | 0 | 172/174 |
| 107 | a_7^2d_6a_1^2 | 176 | 14/10 | S | R713 | 49,804 | 21,380 | 2,128 | 20,064 | 4,216 | 0 | 2,016 | 0 | 0 | 0 | 236/276 |
| 108 | a_7^2d_5d_4 | 176 | 16/8 | H | R28 | 40,252 | 13,612 | 4,356 | 18,100 | 1,814 | 0 | 2,370 | 0 | 0 | 0 | 160/170 |
| 109 | a_{10}a_6a_5a_1 | 184 | 13/12 | S | STR | 16,386 | 7,658 | 80 | 6,714 | 1,934 | 0 | 0 | 0 | 0 | 0 | 90/110 |
| 110 | a_8a_7^2 | 184 | 16/9 | S | STR | 6,920 | 2,952 | 78 | 3,074 | 816 | 0 | 0 | 0 | 0 | 0 | 42/49 |
| 111 | a_9^2a_2^2 | 192 | 13/13 | F | R28 | 30,012 | 12,048 | 1,120 | 13,432 | 2,348 | 0 | 1,064 | 0 | 0 | 0 | 170/222 |
| 112 | d_7a_7d_5a_3 | 192 | 14/12 | S | R713 | 20,846 | 9,392 | 604 | 8,094 | 2,284 | 0 | 472 | 0 | 0 | 0 | 164/184 |
| 113 | a_9d_6a_5a_3 | 192 | 16/10 | S | STR | 12,184 | 4,835 | 195 | 5,012 | 2,142 | 0 | 0 | 0 | 0 | 0 | 64/71 |
| 114 | a_9a_8a_5 | 192 | 16/10 | S | R713 | 19,806 | 8,738 | 1,380 | 7,912 | 1,152 | 0 | 624 | 0 | 0 | 0 | 150/180 |
| 115 | a_7^2d_5^2 | 192 | 18/8 | H3 | R28 | 11,664 | 0 | 3,216 | 7,432 | 568 | 0 | 448 | 0 | 0 | 0 | 64/64 |
| 116 | a_8^2a_7 | 200 | 18/9 | H | R28 | 10,864 | 4,080 | 1,216 | 4,944 | 344 | 0 | 280 | 0 | 0 | 0 | 84/92 |
| 117 | d_8d_4^4 | 208 | 14/14 | EP | - | - | - | - | - | - | - | - | - | - | - |  |
| 118 | a_9d_7a_5a_1a_1 | 208 | 16/12 | S | STR | 11,980 | 5,033 | 0 | 4,880 | 2,067 | 0 | 0 | 0 | 0 | 0 | 102/114 |
| 119 | a_{11}d_5d_4a_3 | 208 | 16/12 | H | R28 | 9,553 | 4,272 | 514 | 3,902 | 649 | 0 | 216 | 0 | 0 | 0 | 90/100 |
| 120 | a_9a_7d_6a_1 | 208 | 18/10 | H | R28 | 10,406 | 3,899 | 1,228 | 4,312 | 537 | 0 | 430 | 0 | 0 | 0 | 92/102 |
| 121 | a_9a_7d_6a_1 | 208 | 18/10 | H | R28 | 6,128 | 2,446 | 412 | 2,686 | 412 | 0 | 172 | 0 | 0 | 0 | 78/86 |
| 122 | d_6^2d_6d_4a_1^2 | 208 | 18/10 | F | R28 | 8,285 | 2,565 | 1,176 | 3,581 | 553 | 0 | 410 | 0 | 0 | 0 | 72/72 |
| 123 | a_{11}a_8a_3 | 216 | 16/13 | F | R28 | 7,618 | 3,450 | 228 | 3,228 | 588 | 0 | 124 | 0 | 0 | 0 | 92/118 |
| 124 | d_8a_7^2 | 224 | 16/14 | F | R28 | 5,136 | 2,296 | 176 | 2,008 | 592 | 0 | 64 | 0 | 0 | 0 | 82/96 |
| 125 | a_{11}d_6a_5a_1 | 224 | 18/12 | F | R28 | 4,284 | 1,894 | 354 | 1,618 | 306 | 0 | 112 | 0 | 0 | 0 | 65/73 |
| 126 | a_{10}e_6a_6 | 224 | 18/12 | F | R28 | 4,168 | 1,852 | 264 | 1,572 | 384 | 0 | 96 | 0 | 0 | 0 | 90/102 |
| 127 | d_7a_7e_6a_3 | 224 | 18/12 | H | R28 | 4,020 | 1,744 | 360 | 1,464 | 356 | 0 | 96 | 0 | 0 | 0 | 68/72 |
| 128 | a_9e_6d_6a_1 | 224 | 18/12 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 129 | e_6^2d_5^2 | 224 | 18/12 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 130 | a_{12}a_7a_4 | 232 | 18/13 | H | R28 | 3,988 | 1,756 | 252 | 1,740 | 188 | 0 | 52 | 0 | 0 | 0 | 52/62 |
| 131 | d_8d_6^2a_1^2a_1^2 | 240 | 18/14 | F | R28 | 2,500 | 992 | 198 | 932 | 354 | 0 | 24 | 0 | 0 | 0 | 50/51 |
| 132 | d_6^4 | 240 | 22/10 | H3 | R28 | 2,416 | 0 | 992 | 1,264 | 104 | 0 | 56 | 0 | 0 | 0 | 32/32 |
| 133 | a_{13}d_6a_3a_1 | 256 | 18/16 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 134 | d_9a_7^2 | 256 | 18/16 | EP | - | - | - | - | - | - | - | - | - | - | - |  |
| 135 | a_{11}d_7d_5 | 256 | 22/12 | F | R28 | 928 | 344 | 148 | 372 | 52 | 0 | 12 | 0 | 0 | 0 | 36/40 |
| 136 | a_{11}^2 | 264 | 22/13 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 137 | a_9e_7a_7 | 272 | 18/18 | F | R28 | 1,208 | 572 | 164 | 312 | 144 | 0 | 16 | 0 | 0 | 0 | 32/34 |
| 138 | e_7d_6d_6d_4a_1 | 272 | 18/18 | F | R28 | 1,026 | 424 | 152 | 303 | 139 | 0 | 8 | 0 | 0 | 0 | 27/27 |
| 139 | d_8^2d_4^2 | 272 | 22/14 | F | R28 | 1,008 | 304 | 230 | 406 | 60 | 0 | 8 | 0 | 0 | 0 | 26/26 |
| 140 | a_{11}d_9a_3 | 288 | 22/16 | F | R28 | 576 | 236 | 68 | 212 | 56 | 0 | 4 | 0 | 0 | 0 | 26/30 |
| 141 | a_{12}a_{11} | 288 | 25/13 | F | R28 | 637 | 232 | 128 | 242 | 23 | 0 | 12 | 0 | 0 | 0 | 27/31 |
| 142 | d_{10}d_6^2a_1^2 | 304 | 22/18 | EP | - | - | - | - | - | - | - | - | - | - | - |  |
| 143 | a_{15}a_8 | 312 | 25/16 | B | - | - | - | - | - | - | - | - | - | - | - |  |
| 144 | a_{16}a_7 | 328 | 25/18 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 145 | d_8^2d_8 | 336 | 30/14 | SP | - | - | - | - | - | - | - | - | - | - | - |  |
| 146 | d_8^3 | 336 | 30/14 | SP | - | - | - | - | - | - | - | - | - | - | - |  |
| 147 | a_{15}d_8 | 352 | 30/16 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 148 | a_{15}e_7a_1 | 368 | 30/18 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 149 | d_{10}e_7d_6a_1 | 368 | 30/18 | S | STR | 44 | 0 | 0 | 0 | 44 | 0 | 0 | 0 | 0 | 0 | 9/9 |
| 150 | d_8e_7^2a_1^2 | 368 | 30/18 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 151 | d_{12}d_8d_4 | 400 | 30/22 | SP | - | - | - | - | - | - | - | - | - | - | - |  |
| 152 | e_8d_8^2 | 464 | 30/30 | SP | - | - | - | - | - | - | - | - | - | - | - |  |
| 153 | d_{12}^2 | 528 | 46/22 | So | - | - | - | - | - | - | - | - | - | - | - |  |
| 154 | a_{23} | 552 | 46/25 | P | - | - | - | - | - | - | - | - | - | - | - |  |
| 155 | d_{16}d_8 | 592 | 46/30 | SP | - | - | - | - | - | - | - | - | - | - | - |  |

Provenance of the old STR records (tiers, from the recount): P = package engine, L = lab-PC version of the 29/09 wrapper (recovered), N = no code version. The per-lattice tier split of pairs is in the JSON (`primary.pairs_by_tier`). The notes say representatives of tier L/N are now covered by Corollary Y1 certificates or by the v10 re-runs.

## 7. Which lattices die entirely by short-vector rules, which need a no-frame rule (point 2)

### 7.1 What the engine labels say

135 of the 135 pair-level record sets contain at least one pair labelled with a kind (b) rule (sets without any: none); characteristic trap absent from: 149; stage 1 empty absent from: none. Since the labels depend on rule order (section 2, item 2), this does not show that a (b) rule was *needed* for any pair. For the 13 deferral lattices the labels are, for the pairs the engine decided (swap and twin removed): kind (a) 19,226,981 (10.1%), kind (b) 171,722,834 (89.9%).

### 7.2 Lemma-only census of the 28 old pair-list lattices (hand_28; the only per-pair necessity data on this machine)

For each of these lattices the lab took every admissible y1 up to the Weyl group (plan of the v10 re-run), removed the y1 that have a root r with (r,y1) = +-2 (Corollary Y1, via T18/T20 whatever y2), and for every pair (y1,y2) of the y1 left stored a witness vector v of norm 2, 3 or 4 with minimal E(v) = 7(v,v) - (v,y1)^2 - (v,y2)^2 (E < 8 contradicts R-vi; E = 8, 9, 10 contradict T16, T18, T20). Source: `measures/hand_28/<lid>.json`; the 'pairs in the y1 killed by Y1' column is the v10 re-run pair count minus the hand_28 pair count (same producer plan; derived by difference).

| id | roots | y1 in plan | y1 with root (Y1) | y1 left | pairs of y1 left | min E <= 8 | E = 9 | E = 10 | no witness (E >= 11) | pairs in y1 killed by Y1 (v10 re-run minus hand_28) | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 044 | a_3^8 | 1168 | 1152 | 16 | 144,256 | 49,216 | 66,816 | 26,304 | 1,920 | 5,344,704 | 1920 pairs need a search / trap |
| 072 | a_5^4a_1^4 | 456 | 448 | 8 | 11,968 | 3,744 | 6,288 | 1,696 | 240 | 565,264 | 240 pairs need a search / trap |
| 087 | d_4^6 | 240 | 240 | 0 | 0 | 0 | 0 | 0 | 0 | 184,608 | all y1 killed by Corollary Y1 (kind a only) |
| 096 | a_7d_5^2a_3^2 | 262 | 246 | 16 | 3,228 | 2,208 | 740 | 280 | 0 | 96,008 | no pair left (kind a only) |
| 097 | a_7^2d_4^2 | 332 | 300 | 32 | 4,584 | 2,096 | 1,976 | 480 | 32 | 86,400 | 32 pairs need a search / trap |
| 106 | d_6^2d_4^2a_1^4 | 174 | 172 | 2 | 364 | 276 | 44 | 12 | 32 | 49,248 | 32 pairs need a search / trap |
| 108 | a_7^2d_5d_4 | 170 | 160 | 10 | 1,876 | 1,300 | 380 | 196 | 0 | 38,376 | no pair left (kind a only) |
| 111 | a_9^2a_2^2 | 222 | 170 | 52 | 3,024 | 1,696 | 576 | 432 | 320 | 26,988 | 320 pairs need a search / trap |
| 115 | a_7^2d_5^2 | 64 | 64 | 0 | 0 | 0 | 0 | 0 | 0 | 11,664 | all y1 killed by Corollary Y1 (kind a only) |
| 116 | a_8^2a_7 | 92 | 84 | 8 | 728 | 480 | 152 | 96 | 0 | 10,136 | no pair left (kind a only) |
| 119 | a_{11}d_5d_4a_3 | 100 | 90 | 10 | 390 | 204 | 144 | 42 | 0 | 9,163 | no pair left (kind a only) |
| 120 | a_9a_7d_6a_1 | 102 | 92 | 10 | 700 | 452 | 176 | 60 | 12 | 9,706 | 12 pairs need a search / trap |
| 121 | a_9a_7d_6a_1 | 86 | 78 | 8 | 312 | 180 | 104 | 28 | 0 | 5,816 | no pair left (kind a only) |
| 122 | d_6^2d_6d_4a_1^2 | 72 | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 8,285 | all y1 killed by Corollary Y1 (kind a only) |
| 123 | a_{11}a_8a_3 | 118 | 92 | 26 | 776 | 348 | 212 | 164 | 52 | 6,842 | 52 pairs need a search / trap |
| 124 | d_8a_7^2 | 96 | 82 | 14 | 416 | 192 | 160 | 48 | 16 | 4,720 | 16 pairs need a search / trap |
| 125 | a_{11}d_6a_5a_1 | 73 | 65 | 8 | 268 | 158 | 76 | 34 | 0 | 4,016 | no pair left (kind a only) |
| 126 | a_{10}e_6a_6 | 102 | 90 | 12 | 244 | 100 | 96 | 40 | 8 | 3,924 | 8 pairs need a search / trap |
| 127 | d_7a_7e_6a_3 | 72 | 68 | 4 | 60 | 44 | 12 | 4 | 0 | 3,960 | no pair left (kind a only) |
| 130 | a_{12}a_7a_4 | 62 | 52 | 10 | 340 | 208 | 84 | 32 | 16 | 3,648 | 16 pairs need a search / trap |
| 131 | d_8d_6^2a_1^2a_1^2 | 51 | 50 | 1 | 26 | 14 | 4 | 4 | 4 | 2,474 | 4 pairs need a search / trap |
| 132 | d_6^4 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 2,416 | all y1 killed by Corollary Y1 (kind a only) |
| 135 | a_{11}d_7d_5 | 40 | 36 | 4 | 12 | 12 | 0 | 0 | 0 | 916 | no pair left (kind a only) |
| 137 | a_9e_7a_7 | 34 | 32 | 2 | 52 | 48 | 0 | 4 | 0 | 1,156 | no pair left (kind a only) |
| 138 | e_7d_6d_6d_4a_1 | 27 | 27 | 0 | 0 | 0 | 0 | 0 | 0 | 1,026 | all y1 killed by Corollary Y1 (kind a only) |
| 139 | d_8^2d_4^2 | 26 | 26 | 0 | 0 | 0 | 0 | 0 | 0 | 1,008 | all y1 killed by Corollary Y1 (kind a only) |
| 140 | a_{11}d_9a_3 | 30 | 26 | 4 | 32 | 24 | 4 | 4 | 0 | 544 | no pair left (kind a only) |
| 141 | a_{12}a_{11} | 31 | 27 | 4 | 52 | 44 | 4 | 4 | 0 | 585 | no pair left (kind a only) |
| **all 28** | | 4,334 | 4,073 | 261 | 173,708 | 63,044 | 78,048 | 29,964 | 2,652 | 6,483,601 | |

- **Kind (a) alone** (no pair without a witness): 17 lattices: 087, 096, 108, 115, 116, 119, 121, 122, 125, 127, 132, 135, 137, 138, 139, 140, 141. For six of them (087, 115, 122, 132, 138, 139) the Corollary-Y1 test already kills every y1.
- **At least one pair needs a no-frame rule** (minimal E >= 11): 11 lattices: 044, 072, 097, 106, 111, 120, 123, 124, 126, 130, 131; 2,652 pairs in all. In the lab's pair-by-pair evaluation (text of B_LATTICES.md B.6, aws_repo copy; not a stored per-pair file) 1,024 + 586 of these pairs are closed by the characteristic-vector rule, 896 + 108 go to the stage-1 search, 38 (in 106, 111, 131) by the twin rule. The v10 re-run itself only stores counts. Per-lattice split is not stored (only for 044: 1,024 trap, 896 search).
- Pairs of the y1 left by minimal E: E <= 8: 63,044 (36.3%), E = 9: 78,048 (44.9%), E = 10: 29,964 (17.2%), none: 2,652 (1.5%).
- Compare with the engine labels of the same 28 lattices in the v10 re-run (R28 row of section 5): the labels put 4,522,626 of 6,657,309 pairs under 'char trap'; the lemma-only census shows that only 2,652 pairs (0.040% of all pairs of these lattices) have no short-vector witness. The label counts therefore say almost nothing about what a computation-free proof needs.

### 7.3 Corollary-Y1 census of the stream lattices (TWIN_RESIDUE_AFTER_Y1)

Over the 102 stream lattices (91 S + 11 SD), 42,276 of 54,096 y1 representatives of the lab's plans (78.1%) have a root r with (r,y1) = +-2, so by Corollary Y1 (T18 + T20) no frame has such a y1, whatever y2. Fractions per lattice are in the Y1 column of section 6. Range: lowest 52.7% (lattice 003), highest 100% (lattice 149 only).

For lattice 149 (roots d_10 e_7 d_6 a_1; 9 y1 representatives, all with such a root) the stored 29/09 record (44 pairs, all 'stage 1 empty', no code version) is therefore not needed: the lattice is excluded by Corollary Y1 alone, i.e. by kind (a), on the records. (The tracker text for 149 still describes the older frame_dfs run on 44 pairs.)

### 7.4 Summary of point 2

| Class | Lattices | Evidence |
|---|---|---|
| Excluded **entirely by kind (a)** on the records (no pair needing a frame search, apart from the lemmas) | 087, 096, 108, 115, 116, 119, 121, 122, 125, 127, 132, 135, 137, 138, 139, 140, 141, 149 (18) | hand_28 lemma-only census (17); Corollary-Y1 census (149) |
| **At least one pair needs a kind (b) rule** (no short-vector witness): confirmed | 044, 072, 097, 106, 111, 120, 123, 124, 126, 130, 131 (11) | hand_28: 2,652 pairs |
| Pair-level, **no per-pair necessity data** | 106 lattices: all other pair-level lattices (the 13 deferral lattices incl. Golay 001, 002; the 90 other stream lattices; Golay 004, 010; 105) | only first-fired labels (sections 5, 6) and the Y1 fraction per lattice |
| Lattice-level, no pairs | 094, 117, 128, 129, 133, 134, 136, 142, 143, 144, 145, 146, 147, 148, 150, 151, 152, 153, 154, 155 (20) | packing / criterion (E) / Sol 0836 / budget; neither (a) nor (b) in the sense of the engine rules |
| O24 classes | 000 | LP certificates and exact o24 search |

The caveat of the 17 + 1: these are conclusions *given* T16, T18, T20 (statuses as the notes give them), the completeness of the producer's y1 and y2 enumerations (compared with an independent enumerator on four lattices only, none of them among the 28 except 135, 140, 141) and of the norm 2, 3, 4 shell lists (certified by the lab's shell check).

## 8. Lattices treated by a special argument (point 4)

- **000** ((none), code O). Odd Leech lattice (no roots, even neighbours Lambda and A_1^24). Not a stream lattice: 141 classes of pairs (y1,y2) (data/finishC/o24_ypairs.json). 86 classes excluded by a whole-class linear program with an exact integer certificate; the others by the exact o24 depth-first search (stage 2 = Lemma Z, local and joint star sums), verdict 'EMPTY (no joint star sums)' (or 'no local star sums'). Source: tracker text, FINAL_STATEMENT section 4 table; counts below recomputed from the files.
- **001** (a_1^8, code GD). Golay family (roots a_1^8, N2=16). Pair files of the Golay frame (golay_work), not the stream producer; swept with the T18/T20 deferral (engine v10). 117,068 pairs; 4,545 pending T18 and 3,169 pending T20, each with an exact certificate (norms 7, orthogonality, witness root). Rigid-kernel audit H2: 18 exposed pairs, all excluded again.
- **002** (a_1^{12}, code GD). Golay family (roots a_1^12, N2=24). Pair files of the Golay frame, swept with the T18/T20 deferral (engine v10). 718,422 pairs; 6,675 pending T18 and 3,594 pending T20, each with a certificate.
- **004** (a_1^{16}, code G). Golay family (a_1^16, N2=32): 416,383 pair classes of the Golay frame, package v4; char trap, twin transfer, exact stage-1 search. No T16/T18/T20 rule in these records.
- **010** (a_1^{24}, code G). Golay family (a_1^24, N2=48): 3,962 pair classes of the Golay frame, package v4; same rules as 004.
- **105** (e_6d_5a_5^2a_1^2, code H). h-stage lattice of 29/09 (14,169 pairs of gpairs_105, 6,310 of them had been excluded by the per-pair budget ILP, i.e. by an LP solver status = Codex hole H4). Replaced on 07/10 by a whole re-run of the W(R)-reduced enumeration with engine v10, without the budget test: 56,544 pairs, all excluded; stream sha256 equal on AWS and on the lab PC. 64 rigid-kernel exposed pairs, all excluded again (characteristic trap).
- **143** (a_{15}a_8, code B). Lattice-level argument, no pair enumerated (roots a_15 a_8, N2=312). Proposition 143 (lemma/upstream/LATTICE_143.md, hand proof refereed by Codex): uses only (R-ii) 42 vectors of norm 3 and (R-v) the frame identity; budget identity sum_f |P_V f|^2 = 7 dim V on V = span of the a_8 roots (dim 8) and on the line l orthogonal to the roots (z of norm 144). The 4096 norm-3 vectors fall in three kinds; at most 28 of the 42 u are of the third kind; the >= 14 others have |P_l u|^2 >= 9/16, so 7 >= 14*9/16 = 63/8, contradiction. Replaces the 28/09 solver-based component-budget test.
- **152** (e_8d_8^2, code SP). Decomposable lattice (roots e_8 d_8^2 = E8 + odd rank-16 lattice with roots d_8^2). Tracker: Sol note 0836 (E8 minuscule weight 0 => span E8 in N-perp) re-read by C1; also C1 packing argument ('42 smallest m sum to 672 > 256 new roots'); also Theorem R A.9 (U indecomposable), AUDIT_REDUCTION.md section A.9.
- **153** (d_{12}^2, code So). Decomposable lattice (roots d_12^2 = D12+ + D12+). Tracker: Sol note 0836 'D>=12', re-read by C1 (notes/139 s.3); packing 'survives' for this lattice, so no packing exclusion; second proof by Theorem R A.9: U is not an orthogonal sum of two nonzero lattices (the 42 norm-3 vectors lie in one summand because they share blocks pairwise via T^2+T = 12I - C^tC; hence the other summand lies in the plane of y1,y2, rank <= 2, unimodular => Z or Z^2 has norm 1, contradiction). The decomposable lattices among the 156 are exactly 152 and 153.

Lattice 000, recomputed from the files: 141 pair classes; LP results file has 141 entries, 86 EXCLUDED with an exact certificate, the other 55 are 'LP FEASIBLE'; DFS records with an EMPTY verdict: 56 classes (47 cloud + 10 lab, {'EMPTY (no joint star sums)': 56, 'EMPTY (no local star sums)': 1}); union of LP-excluded and DFS-empty classes: 141; classes not covered: none; classes in both: [0]. Sums of the `counts` fields over all 57 DFS class records (classes [31] are in both folders, so counted twice): 12,569,368 stage-1 leaves, 12,546,909 pass Lemma Z, 4,031 pass the local star sums, 0 pass the joint star sums (reading of the fields as in the tracker text: 'Lemma Z passes 99.8% of the leaves; the local star sums leave ~50 and the joint star sums 0').

Also with a non-standard record history (not 'special arguments' but worth knowing): the 28 pair-list lattices and 105 were first excluded on the lab PC on 27-29/09 without a code version and re-covered by v10 on 07/10; 143's solver test of 28/09 was replaced by the hand proof; in the 07/10 re-runs the twin rule closed 60,308 + 85,080 pairs whose exclusion rests on another lattice's records (REFEREE/B_LATTICES correction of 20:05 UTC).

### Lattice-level exclusions (no pair enumerated)

| id | roots | N2 | code | what the tracker records |
|---|---|---|---|---|
| 094 | d_5^4 | 160 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 84 > 80 new roots |
| 117 | d_8d_4^4 | 208 | EP | C1 notes/139 s.2 criterion (E): D8 spinor cost 28 > 26; depends on Sol's theta theorems; independently packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing-admissible trap: 8 short dual dims + 0 orthogonal > 2 |
| 128 | a_9e_6d_6a_1 | 224 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 84 > 64 new roots |
| 129 | e_6^2d_5^2 | 224 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 84 > 64 new roots |
| 133 | a_{13}d_6a_3a_1 | 256 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 168 > 128 new roots |
| 134 | d_9a_7^2 | 256 | EP | C1 notes/139 s.2 criterion (E): 36 > 32; independently packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing-admissible trap: 9 short dual dims + 0 orthogonal > 2 |
| 136 | a_{11}^2 | 264 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 84 > 48 new roots |
| 142 | d_{10}d_6^2a_1^2 | 304 | EP | C1 notes/139 s.2 criterion (E): 45 > 38; independently packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 168 > 128 new roots |
| 143 | a_{15}a_8 | 312 | B | open / 28/09 evening C2: component-budget test (lattice level, no pairs; MILP + exact integer enumeration agree; scripts/component_budget.py, exact_budget.py) / 07/10 C2: hand proof replacing the solver record (compute repo lemma/upstream/LATTICE_143.md): from (R-ii) and (R-v), sum_f /P_V f/^2 = 7 dim V; the 4096 vectors of norm |
| 144 | a_{16}a_7 | 328 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 168 > 104 new roots |
| 145 | d_8^2d_8 | 336 | SP | Sol 0836 D8^3; re-read C1 notes/139 (check_d8cube_trap.py); also packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing-admissible trap: 8 short dual dims + 0 orthogonal > 2 |
| 146 | d_8^3 | 336 | SP | Sol 0836 D8^3; re-read C1 notes/139 (check_d8cube_trap.py); also packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing-admissible trap: 24 short dual dims + 0 orthogonal > 2 |
| 147 | a_{15}d_8 | 352 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 84 > 32 new roots |
| 148 | a_{15}e_7a_1 | 368 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 168 > 64 new roots |
| 150 | d_8e_7^2a_1^2 | 368 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 168 > 64 new roots |
| 151 | d_{12}d_8d_4 | 400 | SP | Sol 0836 D>=12 (G18_G20_D12_COLLAGE); re-read C1 notes/139 s.3; also packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 336 > 128 new roots |
| 152 | e_8d_8^2 | 464 | SP | Sol 0836 E8 (minuscule weight 0 => span E8 in N-perp); re-read C1 notes/139 s.2-3; also packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 672 > 256 new roots |
| 153 | d_{12}^2 | 528 | So | Sol 0836 D>=12; re-read C1 notes/139 s.3 |
| 154 | a_{23} | 552 | P | packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 252 > 48 new roots |
| 155 | d_{16}d_8 | 592 | SP | Sol 0836 D>=12; re-read C1 notes/139 s.3; also packing (C1 envelope_pack.py 19af6fb, run + argument re-read by C2): packing: 42 smallest m sum to 672 > 128 new roots |

Packing argument (B_LATTICES.md B.1): the 3/2-hit sets of the 42 u on the new roots are pairwise disjoint, so the 42 smallest values of m(x) = r/8 - E_roots(x) must fit in the number of new roots; 'packing-admissible trap' variants count short dual dimensions. These arguments were reread on 27-28/09 only (status CITED in B_LATTICES.md); on 07/10 only the step 'integrality on the words implies integrality on all frame vectors' was re-derived (Codex).

## 9. Root systems, h1, h2, K, E(y1), E(y2) (point 5)

`roots`, `N2`, even neighbours: tracker. `h1, h2`: `logs/coxeter_table.jsonl` (h = 0 for Leech). `new-root pairs`: `P` field. For every pair the lab proved (CASCADE_STUDY 02/10, P1) **K + E(y1) + E(y2) = 3|Phi|/4 + 8** with E(y) = sum over positive roots of (r,y)^2 and K the number of y-hit points, and K >= 4|h1 - h2|, so K = 0 only if h1 = h2. Below, `C` = 3 N2 / 4 + 8; `E range`, `K searched` and `K=0 pairs` come from the telemetry of the primary record set (pairs that reached the characteristic trap or the search; dual-minimum and DEFERRED pairs carry no E data). K from E is C - E1 - E2. On the data the inequality K >= 4|h1 - h2| held for every lattice with telemetry (104 lattices); K = 0 pairs occur in: 003 (40), 006 (155), 007 (28), 014 (46), 023 (15), 024 (86), 026 (38), 028 (65), 037 (70), 049 (10), 050 (20), 052 (72), 053 (16), all with h1 = h2.

| id | roots | N2 | neighbours | h1 | h2 | new-root pairs | C = K+E1+E2 | E(y) range seen | K searched (min-max) | K=0 pairs | all y1 have root (Y1) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 000 | (none) | 0 | \Lambda; A_1^{24} | 2 | 0 | [24, 0] | 8 | - | - | - |  |
| 001 | a_1^8 | 16 | A_1^{24}; A_1^{24} | 2 | 2 | [16, 16] | 20 | - | - | - |  |
| 002 | a_1^{12} | 24 | A_1^{24}; A_2^{12} | 3 | 2 | [24, 12] | 26 | - | - | - |  |
| 003 | a_2^2a_1^{10} | 32 | A_2^{12}; A_2^{12} | 3 | 3 | [20, 20] | 32 | 0-16 | 8-28 | 40 |  |
| 004 | a_1^{16} | 32 | A_1^{24}; A_3^8 | 4 | 2 | [32, 8] | 32 | - | - | - |  |
| 005 | a_2^4a_1^8 | 40 | A_2^{12}; A_3^8 | 4 | 3 | [28, 16] | 38 | 3-17 | 8-24 | 0 |  |
| 006 | a_3^2a_1^{12} | 48 | A_3^8; A_3^8 | 4 | 4 | [24, 24] | 44 | 2-22 | 4-32 | 155 |  |
| 007 | a_3a_2^4a_1^6 | 48 | A_3^8; A_3^8 | 4 | 4 | [24, 24] | 44 | 0-22 | 8-32 | 28 |  |
| 008 | a_2^8 | 48 | A_3^8; A_3^8 | 4 | 4 | [24, 24] | 44 | 2-20 | 10-26 | 0 |  |
| 009 | a_2^6a_1^6 | 48 | A_2^{12}; A_4^6 | 5 | 3 | [36, 12] | 44 | 2-18 | 8-32 | 0 |  |
| 010 | a_1^{24} | 48 | A_1^{24}; D_4^6 | 6 | 2 | [48, 0] | 44 | - | - | - |  |
| 011 | a_3^2a_2^4a_1^4 | 56 | A_3^8; A_4^6 | 5 | 4 | [32, 20] | 50 | 1-23 | 8-32 | 0 |  |
| 012 | a_2^8a_1^4 | 56 | A_2^{12}; A_5^4D_4 | 6 | 3 | [44, 8] | 50 | 7-19 | 12-26 | 0 |  |
| 013 | a_3^4a_2^2a_1^2 | 64 | A_4^6; A_4^6 | 5 | 5 | [28, 28] | 56 | 0-26 | 4-36 | 0 |  |
| 014 | a_4a_3a_2^4a_1^4 | 64 | A_4^6; A_4^6 | 5 | 5 | [28, 28] | 56 | 2-28 | 0-40 | 46 |  |
| 015 | a_3^2a_3a_2^4a_1^2 | 64 | A_3^8; A_5^4D_4 | 6 | 4 | [40, 16] | 56 | 4-24 | 8-32 | 0 |  |
| 016 | a_3^4a_1^4a_1^4 | 64 | A_3^8; A_5^4D_4 | 6 | 4 | [40, 16] | 56 | 4-24 | 8-30 | 0 |  |
| 017 | a_3^4a_1^8 | 64 | A_3^8; D_4^6 | 6 | 4 | [40, 16] | 56 | 8-24 | 8-32 | 0 |  |
| 018 | a_4a_3^2a_3a_2^2a_1^2 | 72 | A_4^6; A_5^4D_4 | 6 | 5 | [36, 24] | 62 | 3-29 | 4-44 | 0 |  |
| 019 | a_4^2a_2^4a_1^4 | 72 | A_4^6; A_5^4D_4 | 6 | 5 | [36, 24] | 62 | 5-29 | 4-38 | 0 |  |
| 020 | a_3^6 | 72 | A_4^6; D_4^6 | 6 | 5 | [24, 36] | 62 | 3-27 | 8-38 | 0 |  |
| 021 | a_3^4a_2^4 | 72 | A_3^8; A_6^4 | 7 | 4 | [48, 12] | 62 | 7-25 | 12-36 | 0 |  |
| 022 | d_4a_4a_2^6 | 80 | A_5^4D_4; A_5^4D_4 | 6 | 6 | [32, 32] | 68 | 4-34 | 2-46 | 0 |  |
| 023 | d_4a_3^4a_1^4 | 80 | A_5^4D_4; A_5^4D_4 | 6 | 6 | [32, 32] | 68 | 2-34 | 0-48 | 15 |  |
| 024 | a_5a_3^3a_1^6a_1 | 80 | A_5^4D_4; A_5^4D_4 | 6 | 6 | [32, 32] | 68 | 2-34 | 0-48 | 86 |  |
| 025 | a_4^2a_3^2a_3a_1^2 | 80 | A_5^4D_4; A_5^4D_4 | 6 | 6 | [32, 32] | 68 | 4-32 | 4-48 | 0 |  |
| 026 | a_5a_3^2a_2^4a_1 | 80 | A_5^4D_4; A_5^4D_4 | 6 | 6 | [32, 32] | 68 | 0-34 | 0-48 | 38 |  |
| 027 | d_4a_3^4a_1^4 | 80 | D_4^6; A_5^4D_4 | 6 | 6 | [32, 32] | 68 | 6-34 | 2-44 | 0 |  |
| 028 | d_4^2a_1^{16} | 80 | D_4^6; D_4^6 | 6 | 6 | [32, 32] | 68 | 14-34 | 0-36 | 65 |  |
| 029 | a_4^2a_3^2a_2^2a_1^2 | 80 | A_4^6; A_6^4 | 7 | 5 | [44, 20] | 68 | 2-30 | 8-48 | 0 |  |
| 030 | a_3^4a_3^2a_1^4 | 80 | A_3^8; A_7^2D_5^2 | 8 | 4 | [56, 8] | 68 | 10-26 | 16-32 | 0 |  |
| 031 | a_4^4a_1^4 | 88 | A_5^4D_4; A_6^4 | 7 | 6 | [28, 40] | 74 | 5-33 | 8-44 | 0 |  |
| 032 | a_5a_4a_3a_3a_2a_2a_1 | 88 | A_5^4D_4; A_6^4 | 7 | 6 | [28, 40] | 74 | 3-35 | 4-46 | 0 |  |
| 033 | a_4^2a_3^4 | 88 | A_4^6; A_7^2D_5^2 | 8 | 5 | [52, 16] | 74 | 9-31 | 12-40 | 0 |  |
| 034 | a_4^2a_4a_3a_2^2a_1^2 | 88 | A_4^6; A_7^2D_5^2 | 8 | 5 | [52, 16] | 74 | 5-31 | 12-44 | 0 |  |
| 035 | a_5a_4^3a_1^3 | 96 | A_6^4; A_6^4 | 7 | 7 | [36, 36] | 80 | 0-38 | 4-48 | 0 |  |
| 036 | a_5^2a_3^2a_2^2 | 96 | A_6^4; A_6^4 | 7 | 7 | [36, 36] | 80 | 4-38 | 4-48 | 0 |  |
| 037 | a_6a_3^3a_2^3 | 96 | A_6^4; A_6^4 | 7 | 7 | [36, 36] | 80 | 4-40 | 0-56 | 70 |  |
| 038 | d_4a_4^2a_4a_2^2 | 96 | A_5^4D_4; A_7^2D_5^2 | 8 | 6 | [48, 24] | 80 | 4-36 | 8-48 | 0 |  |
| 039 | a_5d_4a_3^2a_3a_1^2a_1 | 96 | A_5^4D_4; A_7^2D_5^2 | 8 | 6 | [48, 24] | 80 | 8-36 | 8-46 | 0 |  |
| 040 | a_5^2a_3^2a_1^2a_1^2a_1^2 | 96 | A_5^4D_4; A_7^2D_5^2 | 8 | 6 | [24, 48] | 80 | 8-36 | 8-48 | 0 |  |
| 041 | a_5a_4^2a_3a_3a_1 | 96 | A_5^4D_4; A_7^2D_5^2 | 8 | 6 | [48, 24] | 80 | 0-36 | 8-48 | 0 |  |
| 042 | d_4^2a_3^4 | 96 | D_4^6; A_7^2D_5^2 | 8 | 6 | [48, 24] | 80 | 12-36 | 8-56 | 0 |  |
| 043 | a_4^3a_3^3 | 96 | A_4^6; A_8^3 | 9 | 5 | [60, 12] | 80 | 8-32 | 16-40 | 0 |  |
| 044 | a_3^8 | 96 | A_3^8; D_6^4 | 10 | 4 | [72, 0] | 80 | 28-28 | 24-24 | 0 |  |
| 045 | a_5^2a_4^2a_1^2 | 104 | A_6^4; A_7^2D_5^2 | 8 | 7 | [32, 44] | 86 | 7-39 | 8-52 | 0 |  |
| 046 | a_6a_4a_4a_3a_2a_1a_1 | 104 | A_6^4; A_7^2D_5^2 | 8 | 7 | [44, 32] | 86 | 7-41 | 4-54 | 0 |  |
| 047 | a_5^2a_4a_3a_2^2 | 104 | A_5^4D_4; A_8^3 | 9 | 6 | [20, 56] | 86 | 3-37 | 12-52 | 0 |  |
| 048 | a_4^4a_3^2 | 104 | A_4^6; A_9^2D_6 | 10 | 5 | [68, 8] | 86 | 19-33 | 20-36 | 0 |  |
| 049 | d_5d_4a_3^4 | 112 | A_7^2D_5^2; A_7^2D_5^2 | 8 | 8 | [40, 40] | 92 | 6-46 | 0-60 | 10 |  |
| 050 | d_5a_5a_3^2a_3a_1^2a_1 | 112 | A_7^2D_5^2; A_7^2D_5^2 | 8 | 8 | [40, 40] | 92 | 2-46 | 2-54 | 20 |  |
| 051 | a_5^2d_4^2a_1^2 | 112 | A_7^2D_5^2; A_7^2D_5^2 | 8 | 8 | [40, 40] | 92 | 10-42 | 8-52 | 0 |  |
| 052 | a_7a_3^4a_1^4 | 112 | A_7^2D_5^2; A_7^2D_5^2 | 8 | 8 | [40, 40] | 92 | 16-46 | 0-50 | 72 |  |
| 053 | d_5a_4a_4^2a_2^2 | 112 | A_7^2D_5^2; A_7^2D_5^2 | 8 | 8 | [40, 40] | 92 | 6-46 | 2-58 | 16 |  |
| 054 | a_6d_4a_4^2a_2 | 112 | A_7^2D_5^2; A_7^2D_5^2 | 8 | 8 | [40, 40] | 92 | 0-42 | 8-52 | 0 |  |
| 055 | a_6a_5a_4a_3a_2a_1 | 112 | A_6^4; A_8^3 | 9 | 7 | [28, 52] | 92 | 6-42 | 8-52 | 0 |  |
| 056 | a_5^2d_4a_3^2a_1^2 | 112 | A_5^4D_4; A_9^2D_6 | 10 | 6 | [64, 16] | 92 | 14-38 | 16-48 | 0 |  |
| 057 | a_5a_5a_4^2a_3 | 112 | A_5^4D_4; A_9^2D_6 | 10 | 6 | [64, 16] | 92 | 12-38 | 16-48 | 0 |  |
| 058 | a_5^2d_4a_3^2a_1^2 | 112 | A_5^4D_4; D_6^4 | 10 | 6 | [64, 16] | 92 | 16-38 | 16-40 | 0 |  |
| 059 | d_4^4a_1^8 | 112 | D_4^6; D_6^4 | 10 | 6 | [64, 16] | 92 | 22-38 | 16-48 | 0 |  |
| 060 | a_7a_4^2a_3^2 | 120 | A_7^2D_5^2; A_8^3 | 9 | 8 | [48, 36] | 98 | 11-47 | 4-60 | 0 |  |
| 061 | a_6^2a_4a_3a_1^2 | 120 | A_7^2D_5^2; A_8^3 | 9 | 8 | [48, 36] | 98 | 7-45 | 8-50 | 0 |  |
| 062 | a_6a_5a_5a_3a_2 | 120 | A_6^4; A_9^2D_6 | 10 | 7 | [60, 24] | 98 | 9-43 | 12-54 | 0 |  |
| 063 | a_6^2a_3^2a_2^2 | 120 | A_6^4; A_9^2D_6 | 10 | 7 | [60, 24] | 98 | 13-43 | 12-52 | 0 |  |
| 064 | a_5^4 | 120 | A_6^4; D_6^4 | 10 | 7 | [24, 60] | 98 | 13-41 | 16-44 | 0 |  |
| 065 | a_7a_5^2a_2^2 | 128 | A_8^3; A_8^3 | 9 | 9 | [44, 44] | 104 | - | - | - |  |
| 066 | a_7a_5a_4^2a_1 | 128 | A_7^2D_5^2; A_9^2D_6 | 10 | 8 | [32, 56] | 104 | - | - | - |  |
| 067 | a_7a_5d_4a_3a_1a_1a_1 | 128 | A_7^2D_5^2; A_9^2D_6 | 10 | 8 | [56, 32] | 104 | - | - | - |  |
| 068 | a_6d_5a_4a_4a_2 | 128 | A_7^2D_5^2; A_9^2D_6 | 10 | 8 | [56, 32] | 104 | - | - | - |  |
| 069 | d_5^2a_3^4 | 128 | A_7^2D_5^2; D_6^4 | 10 | 8 | [32, 56] | 104 | - | - | - |  |
| 070 | d_5a_5^2d_4a_1^2 | 128 | A_7^2D_5^2; D_6^4 | 10 | 8 | [56, 32] | 104 | 10-48 | 8-44 | 0 |  |
| 071 | a_5^2a_5d_4a_3a_1 | 128 | A_5^4D_4; A_{11}D_7E_6 | 12 | 6 | [80, 8] | 104 | 24-40 | 24-40 | 0 |  |
| 072 | a_5^4a_1^4 | 128 | A_5^4D_4; E_6^4 | 12 | 6 | [80, 8] | 104 | 32-40 | 24-32 | 0 |  |
| 073 | a_8a_4^2a_3^2 | 136 | A_8^3; A_9^2D_6 | 10 | 9 | [52, 40] | 110 | 9-53 | 6-42 | 0 |  |
| 074 | a_7a_6a_5a_2a_1 | 136 | A_8^3; A_9^2D_6 | 10 | 9 | [52, 40] | 110 | 9-51 | 8-48 | 0 |  |
| 075 | a_6a_6a_5a_4a_1 | 136 | A_6^4; A_{11}D_7E_6 | 12 | 7 | [16, 76] | 110 | 15-45 | 20-42 | 0 |  |
| 076 | a_7^2d_4a_1^4 | 144 | A_9^2D_6; A_9^2D_6 | 10 | 10 | [48, 48] | 116 | - | - | - |  |
| 077 | d_6a_5^2a_3^2 | 144 | A_9^2D_6; A_9^2D_6 | 10 | 10 | [48, 48] | 116 | - | - | - |  |
| 078 | a_8a_5^2a_3 | 144 | A_9^2D_6; A_9^2D_6 | 10 | 10 | [48, 48] | 116 | 8-54 | 8-48 | 0 |  |
| 079 | d_6a_5^2a_3^2 | 144 | D_6^4; A_9^2D_6 | 10 | 10 | [48, 48] | 116 | - | - | - |  |
| 080 | d_6d_4^3a_1^6 | 144 | D_6^4; D_6^4 | 10 | 10 | [48, 48] | 116 | - | - | - |  |
| 081 | a_7d_5a_5a_3a_1a_1a_1 | 144 | A_7^2D_5^2; A_{11}D_7E_6 | 12 | 8 | [72, 24] | 116 | - | - | - |  |
| 082 | d_5d_5a_5^2a_1^2 | 144 | A_7^2D_5^2; A_{11}D_7E_6 | 12 | 8 | [72, 24] | 116 | - | - | - |  |
| 083 | a_7d_5d_4a_3a_3 | 144 | A_7^2D_5^2; A_{11}D_7E_6 | 12 | 8 | [72, 24] | 116 | - | - | - |  |
| 084 | a_6a_6d_5a_4 | 144 | A_7^2D_5^2; A_{11}D_7E_6 | 12 | 8 | [72, 24] | 116 | - | - | - |  |
| 085 | d_5^2a_5^2a_1^2 | 144 | A_7^2D_5^2; E_6^4 | 12 | 8 | [72, 24] | 116 | - | - | - |  |
| 086 | a_6^2a_5^2 | 144 | A_6^4; A_{12}^2 | 13 | 7 | [84, 12] | 116 | - | - | - |  |
| 087 | d_4^6 | 144 | D_4^6; D_8^3 | 14 | 6 | [96, 0] | 116 | 42-42 | 32-32 | 0 | yes |
| 088 | a_8a_6a_5a_2a_1 | 152 | A_8^3; A_{11}D_7E_6 | 12 | 9 | [68, 32] | 122 | - | - | - |  |
| 089 | a_7^2a_4^2 | 152 | A_7^2D_5^2; A_{12}^2 | 13 | 8 | [80, 20] | 122 | - | - | - |  |
| 090 | a_9a_5d_4a_3a_1a_1 | 160 | A_9^2D_6; A_{11}D_7E_6 | 12 | 10 | [40, 64] | 128 | - | - | - |  |
| 091 | a_7d_6a_5a_3a_1 | 160 | A_9^2D_6; A_{11}D_7E_6 | 12 | 10 | [40, 64] | 128 | - | - | - |  |
| 092 | a_8a_6d_5a_2 | 160 | A_9^2D_6; A_{11}D_7E_6 | 12 | 10 | [64, 40] | 128 | - | - | - |  |
| 093 | d_6d_5a_5^2 | 160 | D_6^4; A_{11}D_7E_6 | 12 | 10 | [64, 40] | 128 | - | - | - |  |
| 094 | d_5^4 | 160 | D_6^4; E_6^4 | 12 | 10 | [64, 40] | 128 | - | - | - |  |
| 095 | a_8a_7a_4a_3 | 160 | A_8^3; A_{12}^2 | 13 | 9 | [76, 28] | 128 | 12-56 | 16-48 | 0 |  |
| 096 | a_7d_5^2a_3^2 | 160 | A_7^2D_5^2; D_8^3 | 14 | 8 | [88, 16] | 128 | 20-52 | 24-44 | 0 |  |
| 097 | a_7^2d_4^2 | 160 | A_7^2D_5^2; D_8^3 | 14 | 8 | [88, 16] | 128 | 28-52 | 24-42 | 0 |  |
| 098 | a_8^2a_3^2 | 168 | A_9^2D_6; A_{12}^2 | 13 | 10 | [72, 36] | 134 | 23-59 | 16-46 | 0 |  |
| 099 | a_9a_6a_5a_2 | 168 | A_9^2D_6; A_{12}^2 | 13 | 10 | [36, 72] | 134 | 17-61 | 12-48 | 0 |  |
| 100 | a_7^3 | 168 | A_8^3; D_8^3 | 14 | 9 | [84, 24] | 134 | 31-55 | 24-44 | 0 |  |
| 101 | d_7a_5^2a_5a_1 | 176 | A_{11}D_7E_6; A_{11}D_7E_6 | 12 | 12 | [56, 56] | 140 | 10-70 | 4-44 | 0 |  |
| 102 | a_9d_5^2a_1^2a_1 | 176 | A_{11}D_7E_6; A_{11}D_7E_6 | 12 | 12 | [56, 56] | 140 | 20-64 | 12-52 | 0 |  |
| 103 | a_7e_6d_4a_3^2 | 176 | A_{11}D_7E_6; A_{11}D_7E_6 | 12 | 12 | [56, 56] | 140 | - | - | - |  |
| 104 | e_6a_6^2a_4 | 176 | A_{11}D_7E_6; A_{11}D_7E_6 | 12 | 12 | [56, 56] | 140 | 0-70 | 8-46 | 0 |  |
| 105 | e_6d_5a_5^2a_1^2 | 176 | E_6^4; A_{11}D_7E_6 | 12 | 12 | [56, 56] | 140 | 22-70 | 8-44 | 0 |  |
| 106 | d_6^2d_4^2a_1^4 | 176 | D_6^4; D_8^3 | 14 | 10 | [32, 80] | 140 | 30-62 | 16-48 | 0 |  |
| 107 | a_7^2d_6a_1^2 | 176 | A_9^2D_6; D_8^3 | 14 | 10 | [80, 32] | 140 | 18-62 | 16-48 | 0 |  |
| 108 | a_7^2d_5d_4 | 176 | A_7^2D_5^2; A_{15}D_9 | 16 | 8 | [104, 8] | 140 | 38-54 | 32-48 | 0 |  |
| 109 | a_{10}a_6a_5a_1 | 184 | A_{11}D_7E_6; A_{12}^2 | 13 | 12 | [64, 52] | 146 | - | - | - |  |
| 110 | a_8a_7^2 | 184 | A_8^3; A_{15}D_9 | 16 | 9 | [100, 16] | 146 | - | - | - |  |
| 111 | a_9^2a_2^2 | 192 | A_{12}^2; A_{12}^2 | 13 | 13 | [60, 60] | 152 | 16-70 | 12-48 | 0 |  |
| 112 | d_7a_7d_5a_3 | 192 | A_{11}D_7E_6; D_8^3 | 14 | 12 | [48, 72] | 152 | 22-70 | 12-48 | 0 |  |
| 113 | a_9d_6a_5a_3 | 192 | A_9^2D_6; A_{15}D_9 | 16 | 10 | [96, 24] | 152 | - | - | - |  |
| 114 | a_9a_8a_5 | 192 | A_9^2D_6; A_{15}D_9 | 16 | 10 | [96, 24] | 152 | 32-64 | 24-46 | 0 |  |
| 115 | a_7^2d_5^2 | 192 | A_7^2D_5^2; D_{10}E_7^2 | 18 | 8 | [120, 0] | 152 | 56-56 | 40-40 | 0 | yes |
| 116 | a_8^2a_7 | 200 | A_8^3; A_{17}E_7 | 18 | 9 | [116, 8] | 158 | 47-61 | 36-46 | 0 |  |
| 117 | d_8d_4^4 | 208 | D_8^3; D_8^3 | 14 | 14 | [64, 64] | 164 | - | - | - |  |
| 118 | a_9d_7a_5a_1a_1 | 208 | A_{11}D_7E_6; A_{15}D_9 | 16 | 12 | [88, 40] | 164 | - | - | - |  |
| 119 | a_{11}d_5d_4a_3 | 208 | A_{11}D_7E_6; A_{15}D_9 | 16 | 12 | [88, 40] | 164 | 36-74 | 16-52 | 0 |  |
| 120 | a_9a_7d_6a_1 | 208 | A_9^2D_6; A_{17}E_7 | 18 | 10 | [112, 16] | 164 | 34-66 | 32-52 | 0 |  |
| 121 | a_9a_7d_6a_1 | 208 | A_9^2D_6; D_{10}E_7^2 | 18 | 10 | [112, 16] | 164 | 38-66 | 32-48 | 0 |  |
| 122 | d_6^2d_6d_4a_1^2 | 208 | D_6^4; D_{10}E_7^2 | 18 | 10 | [112, 16] | 164 | 50-66 | 32-48 | 0 | yes |
| 123 | a_{11}a_8a_3 | 216 | A_{12}^2; A_{15}D_9 | 16 | 13 | [84, 48] | 170 | 43-77 | 16-48 | 0 |  |
| 124 | d_8a_7^2 | 224 | D_8^3; A_{15}D_9 | 16 | 14 | [80, 56] | 176 | 50-82 | 16-48 | 0 |  |
| 125 | a_{11}d_6a_5a_1 | 224 | A_{11}D_7E_6; A_{17}E_7 | 18 | 12 | [104, 32] | 176 | 44-76 | 24-52 | 0 |  |
| 126 | a_{10}e_6a_6 | 224 | A_{11}D_7E_6; A_{17}E_7 | 18 | 12 | [104, 32] | 176 | 32-76 | 26-50 | 0 |  |
| 127 | d_7a_7e_6a_3 | 224 | A_{11}D_7E_6; D_{10}E_7^2 | 18 | 12 | [104, 32] | 176 | 34-76 | 24-52 | 0 |  |
| 128 | a_9e_6d_6a_1 | 224 | A_{11}D_7E_6; D_{10}E_7^2 | 18 | 12 | [104, 32] | 176 | - | - | - |  |
| 129 | e_6^2d_5^2 | 224 | E_6^4; D_{10}E_7^2 | 18 | 12 | [104, 32] | 176 | - | - | - |  |
| 130 | a_{12}a_7a_4 | 232 | A_{12}^2; A_{17}E_7 | 18 | 13 | [40, 100] | 182 | 49-81 | 22-52 | 0 |  |
| 131 | d_8d_6^2a_1^2a_1^2 | 240 | D_8^3; D_{10}E_7^2 | 18 | 14 | [96, 48] | 188 | 54-86 | 16-56 | 0 |  |
| 132 | d_6^4 | 240 | D_6^4; D_{12}^2 | 22 | 10 | [144, 0] | 188 | 70-70 | 48-48 | 0 | yes |
| 133 | a_{13}d_6a_3a_1 | 256 | A_{15}D_9; A_{17}E_7 | 18 | 16 | [88, 64] | 200 | - | - | - |  |
| 134 | d_9a_7^2 | 256 | A_{15}D_9; D_{10}E_7^2 | 18 | 16 | [88, 64] | 200 | - | - | - |  |
| 135 | a_{11}d_7d_5 | 256 | A_{11}D_7E_6; D_{12}^2 | 22 | 12 | [136, 16] | 200 | 64-80 | 42-52 | 0 |  |
| 136 | a_{11}^2 | 264 | A_{12}^2; D_{12}^2 | 22 | 13 | [132, 24] | 206 | - | - | - |  |
| 137 | a_9e_7a_7 | 272 | D_{10}E_7^2; A_{17}E_7 | 18 | 18 | [80, 80] | 212 | 64-100 | 16-44 | 0 |  |
| 138 | e_7d_6d_6d_4a_1 | 272 | D_{10}E_7^2; D_{10}E_7^2 | 18 | 18 | [80, 80] | 212 | 54-102 | 16-48 | 0 | yes |
| 139 | d_8^2d_4^2 | 272 | D_8^3; D_{12}^2 | 22 | 14 | [128, 32] | 212 | 58-90 | 32-48 | 0 | yes |
| 140 | a_{11}d_9a_3 | 288 | A_{15}D_9; D_{12}^2 | 22 | 16 | [48, 120] | 224 | 68-100 | 24-44 | 0 |  |
| 141 | a_{12}a_{11} | 288 | A_{12}^2; A_{24} | 25 | 13 | [156, 12] | 224 | 64-88 | 48-56 | 0 |  |
| 142 | d_{10}d_6^2a_1^2 | 304 | D_{10}E_7^2; D_{12}^2 | 22 | 18 | [112, 64] | 236 | - | - | - |  |
| 143 | a_{15}a_8 | 312 | A_{15}D_9; A_{24} | 25 | 16 | [36, 144] | 242 | - | - | - |  |
| 144 | a_{16}a_7 | 328 | A_{17}E_7; A_{24} | 25 | 18 | [136, 52] | 254 | - | - | - |  |
| 145 | d_8^2d_8 | 336 | D_8^3; D_{16}E_8 | 30 | 14 | [192, 0] | 260 | - | - | - |  |
| 146 | d_8^3 | 336 | D_8^3; E_8^3 | 30 | 14 | [192, 0] | 260 | - | - | - |  |
| 147 | a_{15}d_8 | 352 | A_{15}D_9; D_{16}E_8 | 30 | 16 | [184, 16] | 272 | - | - | - |  |
| 148 | a_{15}e_7a_1 | 368 | A_{17}E_7; D_{16}E_8 | 30 | 18 | [176, 32] | 284 | - | - | - |  |
| 149 | d_{10}e_7d_6a_1 | 368 | D_{10}E_7^2; D_{16}E_8 | 30 | 18 | [176, 32] | 284 | - | - | - | yes |
| 150 | d_8e_7^2a_1^2 | 368 | D_{10}E_7^2; D_{16}E_8 | 30 | 18 | [176, 32] | 284 | - | - | - |  |
| 151 | d_{12}d_8d_4 | 400 | D_{12}^2; D_{16}E_8 | 30 | 22 | [160, 64] | 308 | - | - | - |  |
| 152 | e_8d_8^2 | 464 | E_8^3; D_{16}E_8 | 30 | 30 | [128, 128] | 356 | - | - | - |  |
| 153 | d_{12}^2 | 528 | D_{12}^2; D_{24} | 46 | 22 | [288, 0] | 404 | - | - | - |  |
| 154 | a_{23} | 552 | A_{24}; D_{24} | 46 | 25 | [276, 24] | 422 | - | - | - |  |
| 155 | d_{16}d_8 | 592 | D_{16}E_8; D_{24} | 46 | 30 | [64, 256] | 452 | - | - | - |  |

K and E(y) are per-pair quantities; the table gives their ranges over the pairs that reached the trap or the search. The per-lattice histograms of (E1, E2) are in the JSON (`primary.EK.E_pair_histogram_trap|search`). For the 21 lattices without pair records there are no pairs; for lattice 000, N2 = 0 and h = (2, 0).

## 10. Scripts and outputs (all in this folder)

| Script | What it does |
|---|---|
| `kslib.py` | shared helpers: paths, verdict classification, read-only git access (`GIT_NO_LAZY_FETCH=1`, no network), record compaction |
| `index_records.py` | reads every pair-level record (git blobs, working tree, lab folders), de-duplicates, writes a compact index to the session scratchpad (not kept in this folder: 51 MB; regenerate with the script) |
| `select_sets.py` | re-implements the lab's record selection, adds up raw verdict names, validates against the published numbers |
| `assemble.py` | merges the sets with tracker, B_TABLE, Coxeter table, hand_28, Y1 census, lattice 000 files; writes `kill_statistics_156.json` |
| `make_md.py` | writes this file from the JSON |
| `explore_*.py` | exploration scripts (tracker comparison, file inventories, record shapes, throughput test); they print to the console only |

Machine-readable table: `kill_statistics_156.json` (per lattice: identity, method, primary and other record sets with raw verdict counts, class and kind counts, E/K summary, Y1 census, lemma-only census, special argument text; plus totals and the verdict mapping).

## 11. Limits

**Missing**
- No per-pair verdicts: the records keep one dictionary of verdict counts per chunk (and telemetry histograms, 50 sampled searches per chunk). Rule overlap per pair is not recoverable.
- No lemma-only (necessity) census of pairs for the 107 pair-level lattices outside the 28 of hand_28; the only broader necessity data is the Corollary-Y1 fraction of y1 representatives. A census like hand_28 for them would need a computation (not done; not authorised). The per-lattice split of the 2,652 'no witness' pairs by closing rule (586 + 1,024 trap, 108 + 896 search, 38 twin) is quoted from B_LATTICES.md text (the lab's own pair-by-pair evaluation); only the 044 split is per lattice.
- No raw records for the 20 lattice-level exclusions, and none for 000 beyond the o24 files; their arguments are cited from the tracker and the notes (B_LATTICES.md calls the packing/criterion/Sol arguments CITED, reread 27-28/09 only).
- The superseded 27-29/09 h-stage and frame_dfs records of the 28 old pair-list lattices (`data/finishC/frame_dfs`, `...\gpairs`) were not read: the v10 re-runs cover those lattices entirely (per the tracker), and the old records have no code version. Verdict counts of those old runs are therefore not in the tables.
- Lattice 143: its v10 job was stopped and nothing imported; no pair records. 1,622 twin dependencies between stream lattices are quoted from the notes, not recounted here.

**Could not be parsed or reproduced exactly**
- Golay 001: my pair-range tiling by records (the only way to attach verdict names to pairs) gives 4,485 DEFERRED T18 and 3,144 DEFERRED T20 and keeps 118 INCOMPLETE pairs, while the lab's pair-by-pair best-state computation (reproduced by me: 109,354 excluded, 4,545 T18, 3,169 T20) is finer than any tiling by whole records. The 001 verdict names in the tables are those of the tiling (117,068 pairs, as published); the 4,545 / 3,169 are the authoritative deferred counts. Golay 002 reproduces exactly (6,675 / 3,594).
- My index holds 986 (001) and 3,773 (002) accepted Golay records against 981 and 3,769 in the lab's import; some records seem to have arrived after the import. Pair-level states agree.
- The wrapper-hash checks of the lab's `import_sweep.check` (sha256 of `par_consumer.py` / `defer_consumer.py` against the git history) were not replicated; I replicated the engine-hash, producer, count and deferral-list checks. Results agree with the published numbers wherever a published number exists.
- INCOMPLETE pairs (161 in STR, 118 in 001's tiling, 279 in all): excluded by a second search per the notes; the records of that second search (`incomplete_resolved.jsonl`) were only used to accept chunks, not counted.
- Engine mix: the primary sets contain records from engines v1, v2-v4, v5-v9 and v10 (see `primary.engines_frame_dfs_hash_prefix` in the JSON); the dual-minimum rule exists only in v10 records, so its counts (and E=8 per lattice) reflect which records were selected, not the lattice.
- **Two of my own runs went wrong before I fixed them, and one exceeded the five-minute limit.** The first full index build and then a throughput test blocked in my pipe-based `git cat-file --batch` reader. The first ran past the five-minute cap (about 300 s) before I stopped it; the second was stopped after about two minutes. The cause is not established (a deadlock in my pipe handling, or an attempted lazy fetch from the promisor remote, since `aws_repo` is a `blob:none` partial clone; afterwards all 18,824 result blobs were found to be local). I checked right afterwards that no file under `aws_repo\.git` had been modified in the previous 60 minutes and that no git process was left, so no object was written; I cannot exclude that a network request was started. The reader was replaced by short batch processes with `GIT_NO_LAZY_FETCH=1`; all later runs took 100 s or less.
- The Coxeter numbers, N2 and the root-system labels are those of the lab's files (`coxeter_table.jsonl`, tracker); I did not recompute them. Some tracker root labels are the producer's strings (for example `a_3^2a_3a_2^4a_1^2` for 015), not a canonical notation.

**Counts that do not add up, or differ between sources**
- `B_TABLE_156.json` gives, for 058, 070 and 078, the pair counts of the old STR records (368,757; 295,716; 103,280); my primary sets use the v10 whole-lattice re-runs that the tracker says supersede them (401,043; 320,989; 122,411). For the 13 other whole re-runs old and new totals agree.
- The tracker text of 149 describes a frame_dfs run on 44 pairs (27/09), B_TABLE gives method S; the stored stream record (tier N, 44 pairs) has the same count. Either way the lattice is covered by Corollary Y1 on the Y1 census.
- The live tracker differs from its 07/10 snapshot in 53 'by' texts (later annotations: re-run notes). I used the live copy for text, the lab's published checks for numbers.
- STREAM_RECOUNT (CODEX copy and aws_repo copy have different hashes but identical totals: 220,260,576 pairs for 91 lattices); my STR + R713 sets total 220,337,266 pairs for the same 91 lattices because three of them (058, 070, 078) are taken from their re-runs.
- 'Pairs' of heterogeneous runs are added in the total row for orientation only (section 2).
- Status of lemmas: T16/T18/T20, Theorem R and the engine audit are cited as the project's notes describe them (AI-session proofs, accepted by the user; Codex referee passes), not re-assessed here. T4 and the hypotheses of the task statement are not used by this survey.

