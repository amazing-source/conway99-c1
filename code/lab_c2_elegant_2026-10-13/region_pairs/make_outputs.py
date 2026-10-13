"""Assemble region_pairs.json and print the markdown tables used in REGION_PAIRS_REPORT.md.  Plain python (no numba needed).
  python -B make_outputs.py            (reads scan_*.json, task2_results.jsonl, batch_results.jsonl, design_test.json, extra_fits.json)"""
import json, glob, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda n: json.load(open(os.path.join(HERE, n)))

scans = {os.path.basename(f)[5:8]: json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "scan_*.json")))}
design = J("design_test.json"); fits = J("extra_fits.json")
t2 = [json.loads(l) for l in open(os.path.join(HERE, "task2_results.jsonl"))]
batch_all = [json.loads(l) for l in open(os.path.join(HERE, "batch_results.jsonl"))]
batch = {}
for r in batch_all: batch[(r["lid"], r["region_index"])] = r          # last record wins (111 and 131 were re-run with a larger E11 node limit)

# ---------------------------------------------------------------- lattices / census
lat = {}
tot = collections.Counter()
for lid, d in scans.items():
    nreg = d["n_region"]; ntrap = d["n_trap_violation_no_witness"]
    lat[lid] = {"N2_roots": d["N2_lattice"], "shell_counts_norm2_3_4": d["shell_counts"], "shadow_counts_norm2_4": d["shadow_counts"],
                "stored_pairs": d["stored_pairs"], "no_witness_pairs(stored survivors)": d["survivors"], "witness_found_by_recheck": d["n_witness_found_by_recheck"],
                "trap_violation": ntrap, "region_pairs": nreg}
    tot["survivors"] += d["survivors"]; tot["trap"] += ntrap; tot["region"] += nreg; tot["witness"] += d["n_witness_found_by_recheck"]
for lid in design: lat[lid]["shadow_roots_form_spherical_2_design"] = design[lid]["gram_proportional"]
for r in t2: lat[r["lid"]]["rigid_lattice"] = r["rigid_lattice"]

# ---------------------------------------------------------------- task 1
KEYS = ["N2", "I12", "I13", "I15", "N3", "S13"]
allreg = []; idsum = collections.Counter(); idtrap = collections.Counter(); types = collections.Counter()
for lid, d in scans.items():
    for p in d["pairs"]:
        holds = {k: v["holds"] for k, v in p["identities"].items()}
        if p["region"]:
            for k, v in holds.items(): idsum[(k, v)] += 1
            allreg.append({"lid": lid, "row": p["row"], "o": p["o"], "n11": p["n11"], "s": p["s"], "N2": p["N2"], "N3": p["N3"], "I12": p["I12"], "I13": p["I13"],
                           "I14": p["I14"], "I15": p["I15"], "I16": p["I16"], "S13": p["S13"], "S15": p["S15"], "minE_U": p["minE_U"], "min_4E_shadow": p["min_4E_shadow"],
                           "all_six_identities_hold": all(holds.values())})
            types[(lid, p["n11"], p["s"], p["N2"], p["N3"], p["I12"], p["I13"], p["I15"], p["S13"])] += 1
        elif p["trap_violation"] and not p["witness"]:
            for k, v in holds.items(): idtrap[(k, v)] += 1
chosen = []
for r in t2:
    p = [q for q in scans[r["lid"]]["pairs"] if q["row"] == r["row"]][0]
    chosen.append({"lid": r["lid"], "region_index": r["region_index"], "row": p["row"], "o": p["o"], "y1": p["y1"], "y2": p["y2"],
                   "n11": p["n11"], "I12": p["I12"], "I13": p["I13"], "I14": p["I14"], "I15": p["I15"], "I16": p["I16"], "N2": p["N2"], "N3": p["N3"],
                   "s": p["s"], "S13": p["S13"], "S15": p["S15"],
                   "raw_cosets_both_signs_E11_12_13_14_15_16": p["cosets_E_both_signs"], "raw_window_counts_by_norm": p["raw_window_by_norm"],
                   "raw_shadow_norm2_vectors_with_products_1/2,3/2": p["s_vectors"],
                   "raw_shadow_window_cosets_by_4E_both_signs": p["shadow_cosets_by_4E_both_signs"], "min_E_over_norm_2_3_4": p["minE_U"], "min_4E_over_shadow_norm_2_4": p["min_4E_shadow"],
                   "identities": p["identities"]})
task1 = {"all_region_pairs": allreg,
         "identity_summary_region_pairs": {"%s:%s" % (k, v): c for (k, v), c in sorted(idsum.items())},
         "identity_summary_trap_violators_without_witness": {"%s:%s" % (k, v): c for (k, v), c in sorted(idtrap.items())},
         "types": [{"lid": k[0], "n11": k[1], "s": k[2], "N2": k[3], "N3": k[4], "I12": k[5], "I13": k[6], "I15": k[7], "S13": k[8], "pairs": c} for k, c in sorted(types.items())],
         "chosen_pairs": chosen, "extra_relations_exact_on_all_1042": fits}

# ---------------------------------------------------------------- task 2
bsum = collections.defaultdict(list)
for (lid, idx), r in sorted(batch.items()):
    bsum[(lid, r["n11"], r["s"], r["admissible"], r["H4"])].append(r)
bs = []
for k, v in sorted(bsum.items()):
    eh = collections.Counter()
    for x in v:
        for kk, vv in x.get("cells_test", {}).get("empty_cells_histogram", {}).items(): eh[int(kk)] += vv
    bs.append({"lid": k[0], "n11": k[1], "s": k[2], "admissible": k[3], "H4": k[4], "pairs_tested": len(v),
               "E11_only_solutions_min_max": [min(x["E11"]["solutions"] for x in v), max(x["E11"]["solutions"] for x in v)],
               "E11_only_search_exhaustive_for_pairs": sum(1 for x in v if not x["E11"]["node_limit_hit"]),
               "E11+E13_solutions_min_max": [min(x["E11+E13cap3odd"]["solutions"] for x in v), max(x["E11+E13cap3odd"]["solutions"] for x in v)],
               "E11+E13_search_exhaustive_for_pairs": sum(1 for x in v if not x["E11+E13cap3odd"]["node_limit_hit"]),
               "E11+E13+exact3_solutions_min_max": [min(x["E11+E13cap3odd+exact3nonflex"]["solutions"] for x in v), max(x["E11+E13cap3odd+exact3nonflex"]["solutions"] for x in v)],
               "sevensets_tested_by_cells": sum(x.get("cells_test", {}).get("sevensets_tested", 0) for x in v),
               "sevensets_with_all_42_cells_nonempty": sum(x.get("cells_test", {}).get("all_42_cells_nonempty", 0) for x in v),
               "empty_cells_of_42_histogram_over_all_sevensets": dict(sorted(eh.items()))})
task2 = {"chosen_pairs_detailed": t2, "batch_pairs": [batch[k] for k in sorted(batch)], "batch_summary_by_type": bs,
         "orthogonal_set_upper_bound": {"value": 21, "reason": "22 pairwise orthogonal norm-4 vectors of K = <y1,y2>^perp (rank 22, det 49) would span a sublattice of index^2 = 4^22/49, not an integer square"}}

meta = {"date": "2026-10-13", "python_for_enumeration": r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c2_experimental\.venv\Scripts\python.exe -B (numba 0.67, numpy 2.5.3)",
        "campaign_code_copied": "fp_enum, ldl, short, solve_mod2 from c2_cloud_run_v10/scripts/frame_dfs_next.py (copied into rp_lib.py, not imported)",
        "campaign_data_read": ["t20-codex/measures/hand_28/<lid>.json (basis of U)", "t20-codex/measures/hand_28/<lid>_pairs.npz (pairs, integer coordinates)",
                               "t20-codex/measures/SHELL_COUNTS_EXACT_2026-10-07.json (completeness certificate)"],
        "census_totals": dict(tot), "peak_working_set_MiB_measured": 718}
out = {"meta": meta, "lattices": lat, "task1": task1, "task2": task2}
json.dump(out, open(os.path.join(HERE, "region_pairs.json"), "w"), indent=1)
print("wrote region_pairs.json", os.path.getsize(os.path.join(HERE, "region_pairs.json")), "bytes")
print("census totals", dict(tot))
print("identity summary region:", task1["identity_summary_region_pairs"])
print("identity summary trap:", task1["identity_summary_trap_violators_without_witness"])
for r in bs: print(r)
