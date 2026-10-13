"""Lean batch: for a range of region pairs of one lattice, H4 / admissible counts and the exhaustive searches (modes 0, 1, 4).

  <lab python> -B rp_batch.py <lid> <idx list a,b,c or range a-b or 'every k'> <node_limit> [budget seconds=250]
Appends one JSON line per pair to batch_results.jsonl."""
import sys, os, json, time, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT
import rp_search as RS

LIM0 = 3_000_000

def parse(spec, total):
    if spec.startswith("every"):
        k = int(spec[5:]); return list(range(0, total, k))
    if "-" in spec:
        a, b = spec.split("-"); return list(range(int(a), min(int(b), total - 1) + 1))
    return [int(x) for x in spec.split(",")]

def main():
    global LIM0
    lid = sys.argv[1]; lim = int(float(sys.argv[3])); budget = float(sys.argv[4]) if len(sys.argv) > 4 else 250.0
    LIM0 = int(float(sys.argv[5])) if len(sys.argv) > 5 else 3_000_000
    t_start = time.time()
    lat = Lattice(lid)
    scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
    regs = [q for q in scan["pairs"] if q["region"]]
    idxs = parse(sys.argv[2], len(regs))
    done = 0
    for idx in idxs:
        if time.time() - t_start > budget:
            print("time budget reached; next idx would be", idx, flush=True); break
        p = regs[idx]
        y1 = np.array(p["y1"], dtype=np.int64); y2 = np.array(p["y2"], dtype=np.int64)
        t0 = time.time()
        inst = RS.build_instance(lat, y1, y2, p)
        pk = RS.pack_instance(inst)
        out = {"lid": lid, "region_index": idx, "row": p["row"], "o": p["o"], "n11": p["n11"], "s": p["s"], "N2": p["N2"], "S13": p["S13"],
               "H4": int(len(inst["H"])), "admissible": int(pk["n"]), "E13_flex_classes": int(inst["flex13"].sum())}
        for md, name in ((0, "E11"), (1, "E11+E13cap3odd"), (4, "E11+E13cap3odd+exact3nonflex")):
            r = RS.run(pk, md, node_limit=(min(lim, LIM0) if md == 0 else lim), maxsol=(5000 if md == 4 else 2))
            sols = r.pop("sols")
            out[name] = r
            if md == 4:
                # word-cell test on every 7-set found (necessary condition: all 42 cells (pair of h, Same/Opp) contain a norm-3 vector orthogonal to y1, y2)
                G = lat.G; X3o = inst["X3o"]; Ha = pk["Ha"]
                alive = 0; emptyhist = {}
                for sol in sols[:min(r["solutions"], 5000)]:
                    M = (X3o @ G) @ Ha[sol].T
                    nz = (M != 0); nemp = 0
                    for (c, d) in itertools.combinations(range(7), 2):
                        others = [e for e in range(7) if e not in (c, d)]
                        sel = nz[:, c] & nz[:, d] & (~nz[:, others].any(axis=1)) & (np.abs(M[:, c]) == 1) & (np.abs(M[:, d]) == 1)
                        pr = M[sel, c] * M[sel, d]
                        nemp += int((pr == 1).sum() == 0) + int((pr == -1).sum() == 0)
                    emptyhist[nemp] = emptyhist.get(nemp, 0) + 1
                    alive += (nemp == 0)
                out["cells_test"] = {"sevensets_tested": int(min(r["solutions"], 5000)), "all_42_cells_nonempty": int(alive),
                                     "empty_cells_histogram": {str(k): v for k, v in sorted(emptyhist.items())}, "truncated": bool(r["solutions"] > 5000)}
        out["seconds"] = round(time.time() - t0, 1)
        with open(os.path.join(OUT, "batch_results.jsonl"), "a") as f: f.write(json.dumps(out) + "\n")
        done += 1
        print(lid, idx, "row", p["row"], "n11", p["n11"], "s", p["s"], "adm", pk["n"],
              "| E11:", out["E11"]["solutions"], ("(limit)" if out["E11"]["node_limit_hit"] else "(exh)"),
              "| +E13:", out["E11+E13cap3odd"]["solutions"], ("(limit)" if out["E11+E13cap3odd"]["node_limit_hit"] else "(exh)"),
              "| +exact3:", out["E11+E13cap3odd+exact3nonflex"]["solutions"], ("(limit)" if out["E11+E13cap3odd+exact3nonflex"]["node_limit_hit"] else "(exh)"),
              "| cells:", out.get("cells_test", {}).get("all_42_cells_nonempty"), "of", out.get("cells_test", {}).get("sevensets_tested"),
              "|", out["seconds"], "s", flush=True)
    print("pairs done:", done)

if __name__ == "__main__":
    main()
