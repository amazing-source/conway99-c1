"""Step 4: write KILL_STATISTICS_156.md from kill_statistics_156.json (and a few small census files). READ-ONLY on every source.
Every number in the tables is computed here from the JSON; the narrative text is typed."""
import sys, os, json, collections, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kslib as K

J = json.load(open(K.OUT + r"\kill_statistics_156.json"))
L = J["lattices"]; T = J["totals"]
Y1 = json.load(open(K.REPO + r"\measures\TWIN_RESIDUE_AFTER_Y1_2026-10-07.json"))
f = lambda n: "{:,}".format(n)
pc = lambda a, b: ("%.1f%%" % (100.0 * a / b)) if b else "-"
SETABB = {"DEFERRAL": "DEF", "STREAM": "STR", "RERUN713": "R713", "RERUN28": "R28", "EXTRA105": "X105", "GOLAY_OLD": "GOL4", None: "-"}
STAR = ("no_local_star_sums", "no_joint_star_sums", "lemmaZ", "joint_F_fails")
TWIN = ("twin_transfer", "twin_deferred", "twin_canon")

def cc_row(cc):
    g = lambda k: cc.get(k, 0)
    return {"swap": g("swap"), "twin_transfer": g("twin_transfer"), "twin_def": g("twin_deferred"), "twin_canon": g("twin_canon"), "trap": g("char_trap"), "st1": g("stage1_empty"),
            "star": sum(g(k) for k in STAR), "E8": g("dual_min_9_7_Y13_E8"), "E9": g("deferred_T18_E9"), "E10": g("deferred_T20_root_E10") + g("deferred_T20_norm4_E10"),
            "inc": g("incomplete"), "oth": sum(n for c, n in cc.items() if c.startswith("other") or c in ("invalid", "root_Y_gt_6", "pair_budget", "too_few_candidates", "new_root_setup"))}

out = []; w = out.append
pl = {l: e for l, e in L.items() if e.get("primary")}
ALLC = collections.Counter()
for l, e in pl.items(): ALLC.update(e["primary"]["class_counts"])
ALLP = sum(e["primary"]["pairs"] for e in pl.values())
r_all = cc_row(ALLC); sub_all = r_all["trap"] + r_all["st1"] + r_all["star"] + r_all["E8"] + r_all["E9"] + r_all["E10"] + r_all["inc"] + r_all["oth"]
a_all = r_all["E8"] + r_all["E9"] + r_all["E10"]; b_all = r_all["trap"] + r_all["st1"] + r_all["star"]
DEFg = T["set_DEFERRAL"]; rD = cc_row(DEFg["class_counts"]); subD = rD["trap"] + rD["st1"] + rD["star"] + rD["E8"] + rD["E9"] + rD["E10"] + rD["inc"]
aD = rD["E8"] + rD["E9"] + rD["E10"]; bD = rD["trap"] + rD["st1"] + rD["star"]
a_lat = [l for l, e in pl.items() if e["primary"]["kind_counts"].get("a", 0) > 0]
y1tot = sum(v["y1"] for v in Y1.values()); y1root = sum(v["y1_with_root_of_product_2"] for v in Y1.values())
H = {l: e["lemma_only_census"] for l, e in L.items() if "lemma_only_census" in e}
h_pairs_left = sum(h.get("pairs", 0) for h in H.values()); h_y1 = sum(h["y1"] for h in H.values()); h_y1root = sum(h["y1_with_root_of_product_2"] for h in H.values())
h_nopair = sorted(l for l, h in H.items() if h.get("pairs", 0) == 0 or h.get("survivors", 0) == 0)
h_surv = sorted(l for l, h in H.items() if h.get("survivors", 0) > 0)
h_y1only = sorted(l for l, h in H.items() if h["y1_left"] == 0)
h_surv_n = sum(H[l]["survivors"] for l in h_surv)
mE = collections.Counter()
for h in H.values():
    for k, n in (h.get("by_min_E") or {}).items(): mE[k] += n
y1_all_killed = sorted(l for l, v in Y1.items() if v["y1"] == v["y1_with_root_of_product_2"])

# ============================================================================================================== header
w("# Kill statistics for the 156 lattices of Route C: how the lattices die, from the records on this machine")
w("")
w("Survey of 2026-10-13. Read-only: no record was modified, nothing was re-run, nothing was fetched from the cloud. Every number below is either (i) recomputed by the scripts listed in section 10 from the pair-level result records found on this machine, or (ii) quoted from a lab summary file or note, in which case the file is named. Where the two differ, section 11 says so. Verdict names are the raw strings found in the records; the mapping of these names to kind (a) / kind (b) is mine and is given separately in section 3.")
w("")
# ============================================================================================================== 0
w("## 0. Summary")
w("")
w("- **156 lattices**: 135 have pair-level records on this machine (a set of records per lattice, section 4); 20 are excluded at lattice level with no pair enumerated (packing, criterion (E), Sol 0836, budget; lattice 143 by a hand budget proof); lattice 000 (odd Leech) has 141 pair classes, 86 closed by exact LP certificates and 56 by the exact o24 search (union = 141, two classes in both).")
w("- **Pairs**: the 135 record sets contain **%s ordered pairs** in all (heterogeneous runs: different symmetry groups and engine versions, so not additive in any deeper sense). By first-fired rule label: swap-covered %s (%s), characteristic-vector trap %s (%s), twin bookkeeping (transfer + deferred + canon) %s, stage 1 empty %s, local/joint star sums %s, dual-minimum rule (T16, E = 8) %s, DEFERRED pending T18 (E = 9) %s, DEFERRED pending T20 (E = 10) %s, INCOMPLETE %s." % (
    f(ALLP), f(r_all["swap"]), pc(r_all["swap"], ALLP), f(r_all["trap"]), pc(r_all["trap"], ALLP), f(r_all["twin_transfer"] + r_all["twin_def"] + r_all["twin_canon"]), f(r_all["st1"]), f(r_all["star"]), f(r_all["E8"]), f(r_all["E9"]), f(r_all["E10"]), f(r_all["inc"])))
w("- **Split (a)/(b) on the pairs the engine actually decided** (swap and twin bookkeeping removed): kind (a) %s of %s (%s); kind (b) %s (%s). **This split is biased by rule order** (section 2): the characteristic-vector trap fires before the dual-minimum test and before any T18/T20 witness is looked for, so a pair labelled 'char trap' may also carry a short vector." % (f(a_all), f(sub_all), pc(a_all, sub_all), f(b_all), pc(b_all, sub_all)))
_nb = [l for l, e in pl.items() if e["primary"]["kind_counts"].get("b", 0) == 0]
w("- **Record sets and labels**: %s of the 135 pair-level record sets contain at least one pair whose first-fired rule is a kind (b) rule (sets without any: %s); kind (a) verdicts occur in %d of the 135 sets (those run with engine v10 and the dual-minimum / deferral switches). This is a statement about labels, not about necessity." % (135 - len(_nb), ", ".join(_nb) or "none", len(a_lat)))
w("- **What the records can say about necessity** comes from two separate censuses, not from the verdict labels: (1) the lab's lemma-only census of the 28 old pair-list lattices (hand_28): for every pair of the y1 left after Corollary Y1 a witness vector with E <= 10 was searched and stored; **17 of the 28 lattices have no pair left at all** (%s), 11 have %s pairs with no witness (%s); (2) the Corollary-Y1 census over the 102 stream lattices: %s of %s y1 representatives (%s) have a root r with (r,y1) = +-2, and for **lattice 149 all 9 do**. So 18 lattices (the 17 plus 149) are, on the records, excluded without any frame search; all of that rests on T16, T18, T20 (statuses as the notes give them, not assessed here) and on the completeness of the y1/y2 enumerations." % (
    ", ".join(h_nopair), f(h_surv_n), ", ".join(h_surv), f(y1root), f(y1tot), pc(y1root, y1tot)))
w("- For the 11 lattices with surviving pairs, the notes give the pair-by-pair evaluation: of 2,652 pairs without a witness of energy <= 10, 1,610 are closed by the characteristic-vector rule, 1,004 go to the stage-1 search, 38 by the twin rule (aggregate text in `lemma/PROOF_C2/B_LATTICES.md` section B.6, aws_repo copy; not a per-lattice file).")
w("- **Not found on this machine**: a pair-level lemma-only census for the other 107 pair-level lattices; per-pair verdicts (the records keep verdict counts per chunk, not a verdict per pair); the raw records of the 20 lattice-level exclusions (they have none).")
w("")
# ============================================================================================================== 1
w("## 1. What was read: files and fields")
w("")
w("Roots: `LAB` = `C:\\Users\\RESEARCHER\\Desktop\\Recherche_Conway\\c2_experimental`, `CODEX` = `C:\\Users\\RESEARCHER\\Desktop\\Recherche_Conway\\t20-codex`. The local git checkout `LAB\\aws_repo` is a partial clone (`blob:none`); I only listed its trees and read blobs that are already local, with `GIT_NO_LAZY_FETCH=1` (no network). All 18,679 result files named `results/<lid>_<k>_<n>.jsonl` on its 255 `origin/run/*` branches were local (0 missing).")
w("")
w("| Source | Used for | Fields |")
w("|---|---|---|")
w("| git blobs `results/<lid>_<k>_<n>.jsonl` on `origin/run/*` (LAB\\aws_repo, read with `git ls-tree` / `git cat-file`) and the working-tree copies `LAB\\aws_repo\\resultats_q|resultats|resultats_ci` (all duplicates of the blobs) | per-chunk records: deferral sweep, v10 re-runs, Golay blocks | `id, kind, chunk, range, n_pairs, pairs_total, sha256, producer, verdicts, deferred, not_excluded, telemetry (E_pair_trap, E_pair_search, search_K, trap_Yz), code_sha, chunk_ok, chunk_done, merged, machine, t` |")
w("| `LAB\\data\\finishC\\stream\\<lid>\\chunks.jsonl` (102 files), `...\\golay\\<lid>\\chunks.jsonl`, `...\\sweep\\extra\\105` | 29/09 stream sweep, Golay v4 blocks, lattice 105 re-run | same fields |")
w("| `LAB\\data\\finishC\\stream\\<lid>\\plan.json` | number of y1 representatives per lattice (selection of records) | `y1_reps` |")
w("| `LAB\\data\\finishC\\finishC_tracker.json` (live copy, 07/10 and later; differs from the 07/10 snapshot in 53 'by' texts) | status, root system label, number of roots, even neighbours, packing field, method text | `id, roots, nroots, nb1, nb2, status, by, packing, reviewed_by` |")
w("| `LAB\\aws_repo\\lemma\\PROOF_C2\\B_TABLE_156.json` (newer copy than `CODEX\\lemma\\PROOF_C2\\B_TABLE_156.json`) | method code per lattice (S, SD, GD, G, H, F, H3, O, P, EP, SP, So, B) | `rows[].id, method` |")
w("| `LAB\\logs\\coxeter_table.jsonl` (156 lines, lab 02/10) | Coxeter numbers of the two even neighbours | `lid, Phi, P, h` |")
w("| `LAB\\aws_repo\\measures\\hand_28\\<lid>.json` (28 files) | lemma-only census of the 28 old pair-list lattices | `y1, y1_with_root_of_product_2, y1_left, pairs, by_min_E, survivors` |")
w("| `LAB\\aws_repo\\measures\\TWIN_RESIDUE_AFTER_Y1_2026-10-07.json` | Corollary-Y1 census of the 102 stream lattices | `y1, y1_with_root_of_product_2` |")
w("| `CODEX\\measures\\SWEEP_LAB_2026-10-07.json`, `STREAM_RECOUNT_2026-10-07.json`, `LAB\\aws_repo\\measures\\RERUN_28_CHECK_2026-10-07.json`, `RERUN_713_CHECK_2026-10-07.json`, `RERUN_28_MANIFEST`, `RERUN_713_MANIFEST_LAB` | published numbers my selections are validated against (section 2) | `pairs`, class counts, `ok`, job lists |")
w("| `LAB\\data\\finishC\\o24_globallp`, `o24_cloud`, `o24_dfs`, `o24_ypairs.json` | lattice 000 | LP verdicts per class, DFS verdict and counts per class |")
w("| `LAB\\c2_cloud_run*\\MANIFEST.json` | hashes of the package engines (tier P / L / N of a record) | `engine_code_sha` |")
w("| `CODEX\\lemma\\upstream\\AUDIT_ENGINE_RULES.md`, `BRIDGE.md`, `LATTICE_143.md`, `AUDIT_REDUCTION.md` A.9, `PROOF_C2\\B_LATTICES.md` (both copies), `c2_cloud_run_v10\\scripts\\frame_dfs_next.py`, `hstage_stream_next.py`, `CODEX\\q\\defer_consumer.py`, `par_consumer.py`, `q\\tools\\lab_2026-10-07\\import_sweep.py`, `stream_recount.py` | meaning and order of the rules, selection rules, special arguments | (text) |")
w("")
# ============================================================================================================== 2
w("## 2. How to read the numbers")
w("")
w("1. **Pairs** are the ordered pairs (y1, y2) streamed by the producer in the run in question, under that run's symmetry group (Gamma-reduced for the 29/09 and deferral sweeps, identity-only up to the Weyl group for the 07/10 re-runs). Counts are not comparable across runs. The pairs removed by the producer's own filters (root with Y > 6, norm-3 vector with Y > 13, new-root conditions) are not in the records at all.")
w("2. **A verdict is the first rule that fired, in the engine's fixed order**: producer filters, then in the stream consumer `swap` (SWAP-COVERED, I(y1) > I(y2)), then the twin rules (only if the characteristic trap does not fire), then in `search`: characteristic-vector trap, dual-minimum rule `Y = 13` (only with FD_MIN97=1), pair set-up (new-root conditions), and finally the frame search (stage 1, Lemma Z, local and joint star sums). In the deferral sweep a pair with a root r with (r,y1)^2 + (r,y2)^2 = 5 (or = 4 if none gives 5) is labelled DEFERRED pending T18 (resp. T20) instead of being searched to the end: in the quick variant (Q_DEFER_NODES=0, used since 07/10) **without any search**, provided neither the trap nor the dual-minimum test fires; in the earlier budget variant (10,000 nodes) only after the engine's own search returned INCOMPLETE. Which variant a given record used is not tabulated here (the field `deferral.defer_nodes` / `merged.defer_nodes` is in the raw records). Therefore a pair labelled 'char trap' may also have a short vector; the labels cannot be read as 'this pair needed a kind (b) rule'.")
w("3. **Selection of records.** Several chunkings and several engines overlap in the stored records. For every lattice I re-implemented the lab's own selection (read from `import_sweep.py`, `stream_recount.py`, the RERUN checkers; not run): deferral lattices (001, 002, 003, 005-009, 011-015) as in the sweep import; the 91 stream lattices as in the 07/10 recount (tiers P/L/N); the 28 old pair-list lattices and 25 stream lattices from the v10 re-run records (chunks k/8, resp. k/16 or one job per representative; each job exists on two machines, counted once). **Validation:** pairs and class counts of my selections equal the published numbers for all 11 stream deferral lattices, all 91 recounted stream lattices (pairs, classes, tiers), all 28 + 25 re-run lattices (pairs and classes), lattice 105 (56,544) and Golay 002, 004, 010. One exception, Golay 001: see section 11.")
w("4. **Primary record set** (the one used in the tables and totals). SD/GD: the deferral sweep; G (004, 010): Golay blocks of 02/10; S: the 29/09 stream records as selected by the recount (**STR**), except the 16 lattices (058, 070, 073-075, 078, 095, 098-102, 104, 107, 112, 114) that the tracker says were re-run as whole lattices with v10 and whose new records supersede the old ones (**R713**); for the 9 others of the 25 re-run lattices (043, 049-052, 055-057, 118) only some y1 representatives were re-run, the primary set stays STR and the re-run is listed under `other_record_sets` in the JSON; H/F/H3 (28 lattices): the v10 whole-lattice re-run (**R28**); 105: its v10 re-run (**X105**). Totals count each lattice once, in its primary set.")
w("5. Rule shares: 'share of all pairs' includes swap and twin bookkeeping; 'share of substantive pairs' is over (a) + (b) + INCOMPLETE only.")
w("")
# ============================================================================================================== 3
w("## 3. Verdict names found in the records and my mapping")
w("")
w("Twelve distinct verdict strings occur in the 19,045 distinct pair-level records (18,638 from git blobs, 407 only in lab chunk files). Counts below are for the primary record sets only.")
w("")
w("| Raw verdict name | Class (mine) | Kind | Pairs in primary sets | Sources of the rule / flag |")
w("|---|---|---|---|---|")
vcount = collections.Counter()
for e in pl.values(): vcount.update(e["primary"]["verdict_counts"])
src = {"char_trap": "frame identity at a norm-16 characteristic vector z: Y_z > 66 impossible (AUDIT_ENGINE_RULES 'Characteristic trap'; no T16/T18/T20). UNCERTAIN kind: requested list puts it in (b)",
       "swap": "symmetry: the swapped pair (y2, y1) is treated in the same stream. Bookkeeping; the requested list puts 'swap' in (b)",
       "twin_deferred": "twin lattice U+ has strictly more roots: pair is searched there; dependency on another lattice (1,622 dependencies, no cycle per notes)",
       "twin_canon": "twin of the same type: canonical-rule bookkeeping",
       "twin_transfer": "twin envelope U+ holds the same frame and its type is already excluded in the tracker. Requested list puts it in (b); it rests on another lattice's records",
       "stage1_empty": "frame search exhausted: no 7 mutually orthogonal admissible h covering the new roots (kind b)",
       "no_local_star_sums": "frame search: no local star sums (kind b)", "no_joint_star_sums": "frame search: no joint star sums (kind b)",
       "dual_min_9_7_Y13_E8": "norm-3 vector x with (x,y1)^2 + (x,y2)^2 = 13, E = 8; needs T16 (BRIDGE, AUDIT_ENGINE_RULES H5). Kind a",
       "deferred_T18_E9": "root r with (r,y1)^2 + (r,y2)^2 = 5, E = 9; T18 through the bridge theorem. Not an engine exclusion: certificate + lemma. Kind a",
       "deferred_T20_root_E10": "root r with (r,y1)^2 + (r,y2)^2 = 4, E = 10; T20. Kind a. (The variant 'norm-4 x with |(x,y1)| = |(x,y2)| = 3' never occurs in the records)",
       "incomplete": "node limit reached; each of these pairs was searched again and excluded (set checked pair by pair per the notes)"}
for v, n in sorted(vcount.items(), key=lambda t: -t[1]):
    c, k = K.classify(v)
    w("| `%s` | %s | %s | %s | %s |" % (v, c, k, f(n), src.get(c, "")))
w("")
w("Verdict strings that exist in the engine source but occur in none of these records: `EXCLUDED (Lemma Z)`, `EXCLUDED (joint star sums, but (F) fails)` (the H1 census), `DEFERRED (pending T20: norm-4 x ...)`, `EXCLUDED (a y has |(y, beta)| > 3/2 at a new root ...)`, `EXCLUDED (both y hit the same new root ...)`, `EXCLUDED (pair budget)`, `EXCLUDED (too few candidates)`, `EXCLUDED (a root has Y > 6)`. The budget verdicts occurred only in the superseded 28-29/09 h-stage runs (not read here), which were replaced by the v10 re-runs; the rigid-kernel rule and the 'new roots' rule left no separate verdict in the stream records.")
w("")
# ============================================================================================================== 4
w("## 4. The 156 lattices by method")
w("")
w("| Code | Meaning (B_TABLE_156) | Lattices | Primary record set in this survey |")
w("|---|---|---|---|")
meth = collections.defaultdict(list)
for l, e in L.items(): meth[e["method_code"]].append(l)
mm = {"S": ("stream sweep, all pairs through the engine", "STR (75 lattices) or R713 (16)"), "SD": ("stream sweep with T18/T20 deferral, engine v10", "DEF"), "GD": ("Golay pair files with T18/T20 deferral (001, 002)", "DEF (pair tiling)"),
      "G": ("Golay pair blocks 02/10 (004, 010)", "GOL4"), "O": ("odd Leech, 141 pair classes (000)", "none (O24 files)"), "H": ("h-stage sweep on C1 pair lists, 28-29/09 (13 lattices incl. 105)", "R28 (12) / X105 (105)"),
      "F": ("frame_dfs + Lemma U+ on C1 pair lists, 27/09", "R28"), "H3": ("h-stage readings on C1 pairs (115, 132)", "R28"), "P": ("packing argument of C1", "none"), "EP": ("criterion (E) and packing", "none"),
      "SP": ("Sol note 0836 and packing", "none"), "So": ("Sol note 0836 and Theorem R A.9 (153)", "none"), "B": ("budget identity, hand proof (143)", "none")}
for c in ("S", "SD", "GD", "G", "O", "H", "F", "H3", "P", "EP", "SP", "So", "B"):
    w("| %s | %s | %d | %s |" % (c, mm[c][0], len(meth[c]), mm[c][1]))
w("")
w("Pair-level lattices: S 91 + SD 11 + GD 2 + G 2 + H 13 + F 14 + H3 2 = 135. Lattice-level: P 10 + EP 3 + SP 5 + So 1 + B 1 = 20. Odd Leech: 1. Total 156.")
w("")
# ============================================================================================================== 5
w("## 5. Totals and shares by rule (point 3)")
w("")
w("Counts of pairs by first-fired rule, per record-set group. `twin` = transfer + deferred + canon. `star` = no local + no joint star sums.")
w("")
hdr = "| Group | Lattices | Pairs | swap | twin | char trap | stage 1 empty | star sums | E=8 dual min (T16) | E=9 DEFERRED T18 | E=10 DEFERRED T20 | INCOMPLETE |"
w(hdr); w("|---|---|---|---|---|---|---|---|---|---|---|---|")
def grow(name, g):
    r = cc_row(g["class_counts"])
    return "| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (name, g["lattices_with_pair_records"], f(g["pairs"]), f(r["swap"]), f(r["twin_transfer"] + r["twin_def"] + r["twin_canon"]), f(r["trap"]), f(r["st1"]), f(r["star"]), f(r["E8"]), f(r["E9"]), f(r["E10"]), f(r["inc"]))
for nm, key in (("DEF: deferral sweep (11 stream + Golay 001, 002)", "set_DEFERRAL"), ("STR: 29/09 stream sweep, as recounted", "set_STREAM"), ("R713: v10 whole-lattice re-run (16 lattices)", "set_RERUN713"),
                ("R28: v10 whole-lattice re-run of the 28 pair-list lattices", "set_RERUN28"), ("X105: lattice 105 re-run", "set_EXTRA105"), ("GOL4: Golay 004, 010", "set_GOLAY_OLD"), ("**All 135 primary sets**", "all_pair_level_primary_sets")):
    w(grow(nm, T[key]))
w("")
w("Shares of **substantive pairs** (a + b + INCOMPLETE; swap and twin bookkeeping removed):")
w("")
w("| Group | Substantive pairs | char trap | stage 1 empty | star sums | E=8 (T16) | E=9 (T18) | E=10 (T20) | kind (a) total | kind (b) total |")
w("|---|---|---|---|---|---|---|---|---|---|")
for nm, key in (("DEF", "set_DEFERRAL"), ("STR", "set_STREAM"), ("R713", "set_RERUN713"), ("R28", "set_RERUN28"), ("X105", "set_EXTRA105"), ("GOL4", "set_GOLAY_OLD"), ("**All**", "all_pair_level_primary_sets")):
    g = T[key]; r = cc_row(g["class_counts"]); s = r["trap"] + r["st1"] + r["star"] + r["E8"] + r["E9"] + r["E10"] + r["inc"]; a = r["E8"] + r["E9"] + r["E10"]; b = r["trap"] + r["st1"] + r["star"]
    w("| %s | %s | %s | %s | %s | %s | %s | %s | %s (%s) | %s (%s) |" % (nm, f(s), pc(r["trap"], s), pc(r["st1"], s), pc(r["star"], s), pc(r["E8"], s), pc(r["E9"], s), pc(r["E10"], s), f(a), pc(a, s), f(b), pc(b, s)))
w("")
nlat_a = len(a_lat)
w("Kind (a) verdicts occur in %d of the 135 sets: %s." % (nlat_a, ", ".join(sorted(a_lat))))
w("The 13 deferral lattices are the only ones with DEFERRED (T18/T20) verdicts: they carry %s of the %s pairs (%s)." % (f(DEFg["pairs"]), f(ALLP), pc(DEFg["pairs"], ALLP)))
w("")
# ============================================================================================================== 6 per-lattice table
w("## 6. Per-lattice table (points 1 and 5, first part)")
w("")
w("Columns: `N2` roots; `h1/h2` Coxeter numbers of the even neighbours; `code` method code; `set` primary record set; `pairs`; counts by first-fired rule as in section 5 (`tw` = twin transfer + deferred + canon; `star` = star sums); `Y1` = y1 representatives with a root r, (r,y1) = +-2, out of all in the plan (stream lattices: TWIN_RESIDUE_AFTER_Y1; 28 pair-list lattices: hand_28; blank otherwise). Lattice-level lattices and 000 have no pair counts; see sections 7 and 8.")
w("")
w("| id | roots | N2 | h1/h2 | code | set | pairs | swap | tw | trap | st1 | star | E8 | E9 | E10 | inc | Y1 |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for lid in sorted(L):
    e = L[lid]; p = e.get("primary")
    y = ""
    if "y1_census" in e: y = "%d/%d" % (e["y1_census"]["with_root_r_with_(r,y1)=+-2"], e["y1_census"]["y1_representatives_in_plan"])
    elif "lemma_only_census" in e: y = "%d/%d" % (e["lemma_only_census"]["y1_with_root_of_product_2"], e["lemma_only_census"]["y1"])
    rt = e["roots"].replace("|", "/")
    if p:
        r = cc_row(p["class_counts"])
        w("| %s | %s | %d | %d/%d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (lid, rt, e["nroots_N2"], e["h1"], e["h2"], e["method_code"], SETABB[e["primary_record_set"]], f(p["pairs"]), f(r["swap"]), f(r["twin_transfer"] + r["twin_def"] + r["twin_canon"]),
              f(r["trap"]), f(r["st1"]), f(r["star"]), f(r["E8"]), f(r["E9"]), f(r["E10"]), f(r["inc"]), y))
    else:
        w("| %s | %s | %d | %d/%d | %s | - | - | - | - | - | - | - | - | - | - | - | %s |" % (lid, rt, e["nroots_N2"], e["h1"], e["h2"], e["method_code"], y))
w("")
w("Provenance of the old STR records (tiers, from the recount): P = package engine, L = lab-PC version of the 29/09 wrapper (recovered), N = no code version. The per-lattice tier split of pairs is in the JSON (`primary.pairs_by_tier`). The notes say representatives of tier L/N are now covered by Corollary Y1 certificates or by the v10 re-runs.")
w("")
# ============================================================================================================== 7 (a)/(b)
w("## 7. Which lattices die entirely by short-vector rules, which need a no-frame rule (point 2)")
w("")
w("### 7.1 What the engine labels say")
w("")
no_b = sorted(l for l, e in pl.items() if e["primary"]["kind_counts"].get("b", 0) == 0)
no_trap = sorted(l for l, e in pl.items() if e["primary"]["class_counts"].get("char_trap", 0) == 0)
no_st1 = sorted(l for l, e in pl.items() if e["primary"]["class_counts"].get("stage1_empty", 0) == 0)
w("%d of the 135 pair-level record sets contain at least one pair labelled with a kind (b) rule (sets without any: %s); characteristic trap absent from: %s; stage 1 empty absent from: %s. Since the labels depend on rule order (section 2, item 2), this does not show that a (b) rule was *needed* for any pair. For the 13 deferral lattices the labels are, for the pairs the engine decided (swap and twin removed): kind (a) %s (%s), kind (b) %s (%s)." % (
    135 - len(no_b), ", ".join(no_b) or "none", ", ".join(no_trap) or "none", ", ".join(no_st1) or "none", f(aD), pc(aD, subD), f(bD), pc(bD, subD)))
w("")
w("### 7.2 Lemma-only census of the 28 old pair-list lattices (hand_28; the only per-pair necessity data on this machine)")
w("")
w("For each of these lattices the lab took every admissible y1 up to the Weyl group (plan of the v10 re-run), removed the y1 that have a root r with (r,y1) = +-2 (Corollary Y1, via T18/T20 whatever y2), and for every pair (y1,y2) of the y1 left stored a witness vector v of norm 2, 3 or 4 with minimal E(v) = 7(v,v) - (v,y1)^2 - (v,y2)^2 (E < 8 contradicts R-vi; E = 8, 9, 10 contradict T16, T18, T20). Source: `measures/hand_28/<lid>.json`; the 'pairs in the y1 killed by Y1' column is the v10 re-run pair count minus the hand_28 pair count (same producer plan; derived by difference).")
w("")
w("| id | roots | y1 in plan | y1 with root (Y1) | y1 left | pairs of y1 left | min E <= 8 | E = 9 | E = 10 | no witness (E >= 11) | pairs in y1 killed by Y1 (v10 re-run minus hand_28) | outcome |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|")
tot = collections.Counter()
for lid in sorted(H):
    h = H[lid]; e = L[lid]; bm = h.get("by_min_E") or {}
    re_p = e["primary"]["pairs"]; hp = h.get("pairs", 0)
    out_ = "no pair left (kind a only)" if h.get("survivors", 0) == 0 else "%d pairs need a search / trap" % h["survivors"]
    if h["y1_left"] == 0: out_ = "all y1 killed by Corollary Y1 (kind a only)"
    w("| %s | %s | %d | %d | %d | %s | %s | %s | %s | %s | %s | %s |" % (lid, e["roots"], h["y1"], h["y1_with_root_of_product_2"], h["y1_left"], f(hp), f(bm.get("8", 0)), f(bm.get("9", 0)), f(bm.get("10", 0)), f(bm.get(">=11", 0)), f(re_p - hp), out_))
    for k, v in (("y1", h["y1"]), ("y1r", h["y1_with_root_of_product_2"]), ("left", h["y1_left"]), ("pairs", hp), ("e8", bm.get("8", 0)), ("e9", bm.get("9", 0)), ("e10", bm.get("10", 0)), ("e11", bm.get(">=11", 0)), ("rerun", re_p)): tot[k] += v
w("| **all 28** | | %s | %s | %s | %s | %s | %s | %s | %s | %s | |" % (f(tot["y1"]), f(tot["y1r"]), f(tot["left"]), f(tot["pairs"]), f(tot["e8"]), f(tot["e9"]), f(tot["e10"]), f(tot["e11"]), f(tot["rerun"] - tot["pairs"])))
w("")
w("- **Kind (a) alone** (no pair without a witness): %d lattices: %s. For six of them (%s) the Corollary-Y1 test already kills every y1." % (len(h_nopair), ", ".join(h_nopair), ", ".join(h_y1only)))
w("- **At least one pair needs a no-frame rule** (minimal E >= 11): %d lattices: %s; %s pairs in all. In the lab's pair-by-pair evaluation (text of B_LATTICES.md B.6, aws_repo copy; not a stored per-pair file) 1,024 + 586 of these pairs are closed by the characteristic-vector rule, 896 + 108 go to the stage-1 search, 38 (in 106, 111, 131) by the twin rule. The v10 re-run itself only stores counts. Per-lattice split is not stored (only for 044: 1,024 trap, 896 search)." % (len(h_surv), ", ".join(h_surv), f(h_surv_n)))
w("- Pairs of the y1 left by minimal E: E <= 8: %s (%s), E = 9: %s (%s), E = 10: %s (%s), none: %s (%s)." % (f(tot["e8"]), pc(tot["e8"], tot["pairs"]), f(tot["e9"]), pc(tot["e9"], tot["pairs"]), f(tot["e10"]), pc(tot["e10"], tot["pairs"]), f(tot["e11"]), pc(tot["e11"], tot["pairs"])))
w("- Compare with the engine labels of the same 28 lattices in the v10 re-run (R28 row of section 5): the labels put %s of %s pairs under 'char trap'; the lemma-only census shows that only %s pairs (%.3f%% of all pairs of these lattices) have no short-vector witness. The label counts therefore say almost nothing about what a computation-free proof needs." % (
    f(cc_row(T["set_RERUN28"]["class_counts"])["trap"]), f(T["set_RERUN28"]["pairs"]), f(tot["e11"]), 100.0 * tot["e11"] / tot["rerun"]))
w("")
w("### 7.3 Corollary-Y1 census of the stream lattices (TWIN_RESIDUE_AFTER_Y1)")
w("")
w("Over the 102 stream lattices (91 S + 11 SD), %s of %s y1 representatives of the lab's plans (%s) have a root r with (r,y1) = +-2, so by Corollary Y1 (T18 + T20) no frame has such a y1, whatever y2. Fractions per lattice are in the Y1 column of section 6. Range: lowest %s (lattice %s), highest 100%% (lattice %s only)." % (
    f(y1root), f(y1tot), pc(y1root, y1tot), "%.1f%%" % (100 * min(v["y1_with_root_of_product_2"] / v["y1"] for v in Y1.values())), min(Y1, key=lambda l: Y1[l]["y1_with_root_of_product_2"] / Y1[l]["y1"]), ", ".join(y1_all_killed)))
w("")
w("For lattice 149 (roots d_10 e_7 d_6 a_1; 9 y1 representatives, all with such a root) the stored 29/09 record (44 pairs, all 'stage 1 empty', no code version) is therefore not needed: the lattice is excluded by Corollary Y1 alone, i.e. by kind (a), on the records. (The tracker text for 149 still describes the older frame_dfs run on 44 pairs.)")
w("")
w("### 7.4 Summary of point 2")
w("")
ent = sorted(set(h_nopair) | set(y1_all_killed))
w("| Class | Lattices | Evidence |")
w("|---|---|---|")
w("| Excluded **entirely by kind (a)** on the records (no pair needing a frame search, apart from the lemmas) | %s (%d) | hand_28 lemma-only census (17); Corollary-Y1 census (149) |" % (", ".join(ent), len(ent)))
w("| **At least one pair needs a kind (b) rule** (no short-vector witness): confirmed | %s (%d) | hand_28: %s pairs |" % (", ".join(h_surv), len(h_surv), f(h_surv_n)))
others = sorted(l for l, e in pl.items() if l not in H and l not in y1_all_killed)
w("| Pair-level, **no per-pair necessity data** | %d lattices: all other pair-level lattices (the 13 deferral lattices incl. Golay 001, 002; the 90 other stream lattices; Golay 004, 010; 105) | only first-fired labels (sections 5, 6) and the Y1 fraction per lattice |" % len(others))
w("| Lattice-level, no pairs | 094, 117, 128, 129, 133, 134, 136, 142, 143, 144, 145, 146, 147, 148, 150, 151, 152, 153, 154, 155 (20) | packing / criterion (E) / Sol 0836 / budget; neither (a) nor (b) in the sense of the engine rules |" % ())
w("| O24 classes | 000 | LP certificates and exact o24 search |")
w("")
w("The caveat of the 17 + 1: these are conclusions *given* T16, T18, T20 (statuses as the notes give them), the completeness of the producer's y1 and y2 enumerations (compared with an independent enumerator on four lattices only, none of them among the 28 except 135, 140, 141) and of the norm 2, 3, 4 shell lists (certified by the lab's shell check).")
w("")
# ============================================================================================================== 8 special
w("## 8. Lattices treated by a special argument (point 4)")
w("")
for lid in ("000", "001", "002", "004", "010", "105", "143", "152", "153"):
    e = L[lid]
    w("- **%s** (%s, code %s). %s" % (lid, e["roots"], e["method_code"], e.get("special_argument", "")))
w("")
O = J["lattice_000_o24"]
w("Lattice 000, recomputed from the files: %d pair classes; LP results file has %d entries, %d EXCLUDED with an exact certificate, the other %d are 'LP FEASIBLE'; DFS records with an EMPTY verdict: %d classes (47 cloud + 10 lab, %s); union of LP-excluded and DFS-empty classes: %d; classes not covered: %s; classes in both: %s. Sums of the `counts` fields over all 57 DFS class records (classes %s are in both folders, so counted twice): %s stage-1 leaves, %s pass Lemma Z, %s pass the local star sums, %s pass the joint star sums (reading of the fields as in the tracker text: 'Lemma Z passes 99.8%% of the leaves; the local star sums leave ~50 and the joint star sums 0')." % (
    O["pair_classes"], O["lp_entries_in_results_file"], O["lp_excluded_classes"], sum(O["lp_non_excluded_verdicts"].values()), O["dfs_classes_with_EMPTY_verdict"], str(O["dfs_verdicts"]), O["classes_covered_by_union_of_LP_and_DFS"], O["classes_not_covered"] or "none", O["classes_covered_by_both_LP_and_DFS"],
    O["dfs_classes_in_both_folders"] or "none", f(O["dfs_counts_sum_over_all_records_both_folders"]["leaves"]), f(O["dfs_counts_sum_over_all_records_both_folders"]["lemmaZ"]), f(O["dfs_counts_sum_over_all_records_both_folders"]["local_star_sums"]), f(O["dfs_counts_sum_over_all_records_both_folders"]["joint_star_sums"])))
w("")
w("Also with a non-standard record history (not 'special arguments' but worth knowing): the 28 pair-list lattices and 105 were first excluded on the lab PC on 27-29/09 without a code version and re-covered by v10 on 07/10; 143's solver test of 28/09 was replaced by the hand proof; in the 07/10 re-runs the twin rule closed 60,308 + 85,080 pairs whose exclusion rests on another lattice's records (REFEREE/B_LATTICES correction of 20:05 UTC).")
w("")
w("### Lattice-level exclusions (no pair enumerated)")
w("")
w("| id | roots | N2 | code | what the tracker records |")
w("|---|---|---|---|---|")
for lid in sorted(L):
    e = L[lid]
    if e["method_code"] in ("P", "EP", "SP", "So", "B"):
        txt = e["lattice_level_text"][:330].replace("|", "/").replace("\n", " ")
        w("| %s | %s | %d | %s | %s |" % (lid, e["roots"], e["nroots_N2"], e["method_code"], txt))
w("")
w("Packing argument (B_LATTICES.md B.1): the 3/2-hit sets of the 42 u on the new roots are pairwise disjoint, so the 42 smallest values of m(x) = r/8 - E_roots(x) must fit in the number of new roots; 'packing-admissible trap' variants count short dual dimensions. These arguments were reread on 27-28/09 only (status CITED in B_LATTICES.md); on 07/10 only the step 'integrality on the words implies integrality on all frame vectors' was re-derived (Codex).")
w("")
# ============================================================================================================== 9 EK
w("## 9. Root systems, h1, h2, K, E(y1), E(y2) (point 5)")
w("")
w("`roots`, `N2`, even neighbours: tracker. `h1, h2`: `logs/coxeter_table.jsonl` (h = 0 for Leech). `new-root pairs`: `P` field. For every pair the lab proved (CASCADE_STUDY 02/10, P1) **K + E(y1) + E(y2) = 3|Phi|/4 + 8** with E(y) = sum over positive roots of (r,y)^2 and K the number of y-hit points, and K >= 4|h1 - h2|, so K = 0 only if h1 = h2. Below, `C` = 3 N2 / 4 + 8; `E range`, `K searched` and `K=0 pairs` come from the telemetry of the primary record set (pairs that reached the characteristic trap or the search; dual-minimum and DEFERRED pairs carry no E data). K from E is C - E1 - E2. On the data the inequality K >= 4|h1 - h2| held for every lattice with telemetry (%d lattices); K = 0 pairs occur in: %s, all with h1 = h2." % (
    sum(1 for e in pl.values() if e["primary"].get("EK")), ", ".join("%s (%d)" % (l, e["primary"]["EK"]["K_from_E_zero_pairs"]) for l, e in sorted(pl.items()) if e["primary"].get("EK") and e["primary"]["EK"]["K_from_E_zero_pairs"] > 0)))
w("")
w("| id | roots | N2 | neighbours | h1 | h2 | new-root pairs | C = K+E1+E2 | E(y) range seen | K searched (min-max) | K=0 pairs | all y1 have root (Y1) |")
w("|---|---|---|---|---|---|---|---|---|---|---|---|")
for lid in sorted(L):
    e = L[lid]; p = e.get("primary"); ek = p.get("EK") if p else None
    c = 3 * e["nroots_N2"] // 4 + 8
    er = "-"; ks = "-"; k0 = "-"
    if ek:
        er = "%d-%d" % (ek["E_each_min"], ek["E_each_max"]); ks = "%s-%s" % (ek["K_searched_min"], ek["K_searched_max"]) if ek["K_searched_min"] is not None else "-"; k0 = f(ek["K_from_E_zero_pairs"])
    y1k = ""
    if "y1_census" in e and e["y1_census"]["all_killed_by_corollary_Y1"]: y1k = "yes"
    elif "lemma_only_census" in e and e["lemma_only_census"]["y1_left"] == 0: y1k = "yes"
    w("| %s | %s | %d | %s | %d | %d | %s | %d | %s | %s | %s | %s |" % (lid, e["roots"], e["nroots_N2"], "; ".join(e["neighbours"]), e["h1"], e["h2"], e["new_root_pairs_per_coset"], c, er, ks, k0, y1k))
w("")
w("K and E(y) are per-pair quantities; the table gives their ranges over the pairs that reached the trap or the search. The per-lattice histograms of (E1, E2) are in the JSON (`primary.EK.E_pair_histogram_trap|search`). For the 21 lattices without pair records there are no pairs; for lattice 000, N2 = 0 and h = (2, 0).")
w("")
# ============================================================================================================== 10
w("## 10. Scripts and outputs (all in this folder)")
w("")
w("| Script | What it does |")
w("|---|---|")
w("| `kslib.py` | shared helpers: paths, verdict classification, read-only git access (`GIT_NO_LAZY_FETCH=1`, no network), record compaction |")
w("| `index_records.py` | reads every pair-level record (git blobs, working tree, lab folders), de-duplicates, writes a compact index to the session scratchpad (not kept in this folder: 51 MB; regenerate with the script) |")
w("| `select_sets.py` | re-implements the lab's record selection, adds up raw verdict names, validates against the published numbers |")
w("| `assemble.py` | merges the sets with tracker, B_TABLE, Coxeter table, hand_28, Y1 census, lattice 000 files; writes `kill_statistics_156.json` |")
w("| `make_md.py` | writes this file from the JSON |")
w("| `explore_*.py` | exploration scripts (tracker comparison, file inventories, record shapes, throughput test); they print to the console only |")
w("")
w("Machine-readable table: `kill_statistics_156.json` (per lattice: identity, method, primary and other record sets with raw verdict counts, class and kind counts, E/K summary, Y1 census, lemma-only census, special argument text; plus totals and the verdict mapping).")
w("")
# ============================================================================================================== 11
w("## 11. Limits")
w("")
w("**Missing**")
w("- No per-pair verdicts: the records keep one dictionary of verdict counts per chunk (and telemetry histograms, 50 sampled searches per chunk). Rule overlap per pair is not recoverable.")
w("- No lemma-only (necessity) census of pairs for the 107 pair-level lattices outside the 28 of hand_28; the only broader necessity data is the Corollary-Y1 fraction of y1 representatives. A census like hand_28 for them would need a computation (not done; not authorised). The per-lattice split of the 2,652 'no witness' pairs by closing rule (586 + 1,024 trap, 108 + 896 search, 38 twin) is quoted from B_LATTICES.md text (the lab's own pair-by-pair evaluation); only the 044 split is per lattice.")
w("- No raw records for the 20 lattice-level exclusions, and none for 000 beyond the o24 files; their arguments are cited from the tracker and the notes (B_LATTICES.md calls the packing/criterion/Sol arguments CITED, reread 27-28/09 only).")
w("- The superseded 27-29/09 h-stage and frame_dfs records of the 28 old pair-list lattices (`data/finishC/frame_dfs`, `...\\gpairs`) were not read: the v10 re-runs cover those lattices entirely (per the tracker), and the old records have no code version. Verdict counts of those old runs are therefore not in the tables.")
w("- Lattice 143: its v10 job was stopped and nothing imported; no pair records. 1,622 twin dependencies between stream lattices are quoted from the notes, not recounted here.")
w("")
w("**Could not be parsed or reproduced exactly**")
w("- Golay 001: my pair-range tiling by records (the only way to attach verdict names to pairs) gives 4,485 DEFERRED T18 and 3,144 DEFERRED T20 and keeps 118 INCOMPLETE pairs, while the lab's pair-by-pair best-state computation (reproduced by me: 109,354 excluded, 4,545 T18, 3,169 T20) is finer than any tiling by whole records. The 001 verdict names in the tables are those of the tiling (117,068 pairs, as published); the 4,545 / 3,169 are the authoritative deferred counts. Golay 002 reproduces exactly (6,675 / 3,594).")
w("- My index holds 986 (001) and 3,773 (002) accepted Golay records against 981 and 3,769 in the lab's import; some records seem to have arrived after the import. Pair-level states agree.")
w("- The wrapper-hash checks of the lab's `import_sweep.check` (sha256 of `par_consumer.py` / `defer_consumer.py` against the git history) were not replicated; I replicated the engine-hash, producer, count and deferral-list checks. Results agree with the published numbers wherever a published number exists.")
w("- INCOMPLETE pairs (161 in STR, 118 in 001's tiling, 279 in all): excluded by a second search per the notes; the records of that second search (`incomplete_resolved.jsonl`) were only used to accept chunks, not counted.")
w("- Engine mix: the primary sets contain records from engines v1, v2-v4, v5-v9 and v10 (see `primary.engines_frame_dfs_hash_prefix` in the JSON); the dual-minimum rule exists only in v10 records, so its counts (and E=8 per lattice) reflect which records were selected, not the lattice.")
w("- **Two of my own runs went wrong before I fixed them, and one exceeded the five-minute limit.** The first full index build and then a throughput test blocked in my pipe-based `git cat-file --batch` reader. The first ran past the five-minute cap (about 300 s) before I stopped it; the second was stopped after about two minutes. The cause is not established (a deadlock in my pipe handling, or an attempted lazy fetch from the promisor remote, since `aws_repo` is a `blob:none` partial clone; afterwards all 18,824 result blobs were found to be local). I checked right afterwards that no file under `aws_repo\\.git` had been modified in the previous 60 minutes and that no git process was left, so no object was written; I cannot exclude that a network request was started. The reader was replaced by short batch processes with `GIT_NO_LAZY_FETCH=1`; all later runs took 100 s or less.")
w("- The Coxeter numbers, N2 and the root-system labels are those of the lab's files (`coxeter_table.jsonl`, tracker); I did not recompute them. Some tracker root labels are the producer's strings (for example `a_3^2a_3a_2^4a_1^2` for 015), not a canonical notation.")
w("")
w("**Counts that do not add up, or differ between sources**")
w("- `B_TABLE_156.json` gives, for 058, 070 and 078, the pair counts of the old STR records (368,757; 295,716; 103,280); my primary sets use the v10 whole-lattice re-runs that the tracker says supersede them (401,043; 320,989; 122,411). For the 13 other whole re-runs old and new totals agree.")
w("- The tracker text of 149 describes a frame_dfs run on 44 pairs (27/09), B_TABLE gives method S; the stored stream record (tier N, 44 pairs) has the same count. Either way the lattice is covered by Corollary Y1 on the Y1 census.")
w("- The live tracker differs from its 07/10 snapshot in 53 'by' texts (later annotations: re-run notes). I used the live copy for text, the lab's published checks for numbers.")
w("- STREAM_RECOUNT (CODEX copy and aws_repo copy have different hashes but identical totals: 220,260,576 pairs for 91 lattices); my STR + R713 sets total %s pairs for the same 91 lattices because three of them (058, 070, 078) are taken from their re-runs." % f(T["set_STREAM"]["pairs"] + T["set_RERUN713"]["pairs"]))
w("- 'Pairs' of heterogeneous runs are added in the total row for orientation only (section 2).")
w("- Status of lemmas: T16/T18/T20, Theorem R and the engine audit are cited as the project's notes describe them (AI-session proofs, accepted by the user; Codex referee passes), not re-assessed here. T4 and the hypotheses of the task statement are not used by this survey.")
w("")
open(K.OUT + r"\KILL_STATISTICS_156.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("written", sum(len(x) for x in out), "chars,", len(out), "lines")
