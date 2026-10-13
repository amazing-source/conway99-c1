"""Task 2 driver: statistics + exact searches for selected region pairs.

  <lab python> -B rp_task2_run.py <lid> <idx[,idx...]> <modes> <node_limit> [time_budget_seconds=250]

idx = index in the list of region pairs of scan_<lid>.json (in file order).  modes = string of digits from MODES (0 E11 only, 1 E11+E13 cap&odd,
2 cap only, 3 odd only).  Appends one JSON line per (pair, mode-set) to task2_results.jsonl.
"""
import sys, os, json, time, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT
import rp_search as RS


def hist(a):
    u, c = np.unique(a, return_counts=True)
    return {str(int(k)): int(v) for k, v in zip(u, c)}


def greedy_clique(orth, tries, rng):
    n = len(orth); best = []
    for _ in range(tries):
        cand = np.ones(n, bool); cl = []
        while cand.any():
            idx = np.flatnonzero(cand)
            # prefer vertices with many neighbours inside cand (random tie-break)
            samp = rng.choice(idx, min(len(idx), 40), replace=False)
            sc = [(orth[v] & cand).sum() + rng.random() for v in samp]
            v = int(samp[int(np.argmax(sc))])
            cl.append(v); cand &= orth[v]
        if len(cl) > len(best): best = cl
    return best


def rigid_flag(lat):
    """rigid lattice (campaign definition): no norm-3 vector x with |(x,beta)| = 3/2 at a shadow root beta"""
    S2 = lat.S[2]
    P = lat.X[3] @ lat.G @ S2.T                      # = 2 (x, beta)
    return bool(not (np.abs(P) == 3).any())


def main():
    lid = sys.argv[1]; idxs = [int(x) for x in sys.argv[2].split(",")]; modes = [int(c) for c in sys.argv[3]]; lim = int(float(sys.argv[4]))
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 250.0
    t_start = time.time()
    lat = Lattice(lid)
    rigid = rigid_flag(lat)
    scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
    regs = [q for q in scan["pairs"] if q["region"]]
    rng = np.random.default_rng(13)
    for idx in idxs:
        if time.time() - t_start > budget:
            print("time budget reached before idx", idx, flush=True); break
        p = regs[idx]
        y1 = np.array(p["y1"], dtype=np.int64); y2 = np.array(p["y2"], dtype=np.int64)
        t0 = time.time()
        inst = RS.build_instance(lat, y1, y2, p)
        G = lat.G
        H = inst["H"]; P11, P13, P15 = inst["P11"], inst["P13"], inst["P15"]
        m11 = np.abs(P11).max(axis=1); m13 = np.abs(P13).max(axis=1); m15 = np.abs(P15).max(axis=1)
        adm = inst["adm"]
        q13 = np.einsum("ij,jk,ik->i", inst["V13"], G, inst["V13"])
        out = {"lid": lid, "region_index": idx, "row": p["row"], "rigid_lattice": rigid,
               "n11": p["n11"], "s": p["s"], "N2": p["N2"], "N3": p["N3"], "S13": p["S13"], "S15": p["S15"],
               "E13_root_classes": int((q13 == 8).sum()), "E13_norm4_classes": int((q13 == 16).sum()),
               "E13_flex_classes": int(inst["flex13"].sum()), "E13_flex_root_classes": int((inst["flex13"] & (q13 == 8)).sum()),
               "H4": int(len(H)), "admissible": int(adm.sum()),
               "fail_E11.5": int((m11 >= 2).sum()), "fail_only_E13.5": int(((m11 <= 1) & (m13 >= 2)).sum()),
               "max_abs_prod_hist_E11.5_all_H4": hist(m11), "max_abs_prod_hist_E13.5_all_H4": hist(m13), "max_abs_prod_hist_E15.5_all_H4": hist(m15),
               "admissible_violating_E15.5_bound2": int((adm & (m15 >= 3)).sum())}
        # design identity: sum over the new-root classes (all norm-2 shadow classes) of (b,h)^2 versus |S2| (h,h)/24
        S2all = lat.S[2]
        P2 = (H @ G) @ S2all.T                       # 2 (h, beta)
        sq = (P2 ** 2).sum(axis=1)                   # = 4 sum over both signs of (h,beta)^2
        # sum over both signs (beta and -beta) of (h,beta)^2 = sq/4
        out["design_check_sum_over_all_norm2_shadow_vectors_of_(h,b)^2_equals_|S2|*(h,h)*2/24"] = bool((sq * 24 == lat.S[2].shape[0] * 2 * 4 * 4).all())
        pk = RS.pack_instance(inst)
        n = pk["n"]; s = pk["s"]
        Q11 = np.abs(inst["P11"][adm]); Q13 = np.abs(inst["P13"][adm])
        hitm = (Q11 == 1)
        t11 = hitm.sum(axis=1)
        out["hit_set_size_hist_admissible"] = hist(t11)
        per = hitm.sum(axis=0)
        out["admissible_hitters_per_E11_class"] = {"min": int(per.min()), "max": int(per.max()), "hist": hist(per)}
        out["E11_classes_without_admissible_hitter"] = int((per == 0).sum())
        t13 = (Q13 == 1).sum(axis=1)
        out["E13_hit_count_hist_admissible"] = hist(t13)
        # orthogonality graph
        orth = pk["orth"]
        deg = orth.sum(axis=1)
        out["orth_graph_admissible"] = {"vertices": int(n), "edges": int(orth.sum() // 2), "density": round(float(orth.sum()) / (n * (n - 1)), 4),
                                         "degree_min_max": [int(deg.min()), int(deg.max())]}
        cl = greedy_clique(orth, 60, rng)
        Ha = pk["Ha"]; Xc = Ha[cl]
        assert (Xc @ G @ Xc.T == 4 * np.eye(len(cl), dtype=np.int64)).all()
        out["orth_set_lower_bound_found"] = len(cl)
        out["orth_set_upper_bound_rank"] = 22
        # all of H4 (not only admissible): greedy lower bound for pairwise orthogonal set
        orthall = ((H @ G @ H.T) == 0); np.fill_diagonal(orthall, False)
        cla = greedy_clique(orthall, 30, rng)
        out["orth_set_lower_bound_found_all_H4"] = len(cla)
        out["prep_seconds"] = round(time.time() - t0, 1)
        out["searches"] = {}
        for md in modes:
            r = RS.run(pk, md, node_limit=(min(lim, 3_000_000) if md == 0 else lim), maxsol=20)
            sols = r.pop("sols")
            name = {0: "E11_partition", 1: "E11_partition+E13_cap3_odd", 2: "E11_partition+E13_cap3", 3: "E11_partition+E13_odd", 4: "E11_partition+E13_cap3_odd+exact3_on_nonflex_E13"}[md]
            r["exhaustive"] = (not r["node_limit_hit"])
            if r["solutions"]:
                chk = []
                for sol in sols[:min(len(sols), r["solutions"])]:
                    X = Ha[sol]
                    assert (X @ G @ X.T == 4 * np.eye(7, dtype=np.int64)).all()
                    chk.append(True)
                r["first_solutions_verified_orthonormal_norm4"] = len(chk)
            out["searches"][name] = r
            print(lid, idx, name, {k: v for k, v in r.items()}, flush=True)
        out["total_seconds"] = round(time.time() - t0, 1)
        with open(os.path.join(OUT, "task2_results.jsonl"), "a") as f:
            f.write(json.dumps(out) + "\n")
        print("done", lid, idx, "row", p["row"], "H4", out["H4"], "adm", out["admissible"], "secs", out["total_seconds"], flush=True)


if __name__ == "__main__":
    main()
