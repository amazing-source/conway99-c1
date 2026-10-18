"""Codex's Gram-free whole-template model (root_component_z_joint, main 73eca8a3+) on any template, with the DFS row
catalogue (LAB, 18/10/2026).  Codex's build_joint / solve_joint are imported unchanged; only the catalogue comes from
jhat_catalogue.py (identical to Codex's row_catalogue where both run, any kernel dimension).
Flags used by Codex for gz 9744 and c12 sample 364: --row-moments --short-columns --corner-c2 --mate-normalize.
Verdicts are CP-SAT verdicts (INFEASIBLE excludes the whole template; no certificate).
usage: python jhat_zjoint.py <codex dir> <catalogue | keys.gz> <first> <last> <seconds> [--only i,j] [--signed]"""
import json
import sys
import time

codex = sys.argv[1]
sys.path.insert(0, codex)
from root_component_z_joint import build_joint, solve_joint                    # noqa: E402  (Codex, unchanged)
from root_component_row_neighbor_moments import coordinates_for_catalogue      # noqa: E402

from jhat_catalogue import catalogue as dfs_catalogue                           # noqa: E402
from jhat_rows import records                                                    # noqa: E402


def run(t, seconds, signed=False):
    cat = dfs_catalogue(t)
    if any(not r["states"] for r in cat["row_types"]):
        return {"status": "EMPTY_ROW_CATALOGUE"}
    t0 = time.process_time()
    diag = {}
    coords = coordinates_for_catalogue(cat, t)
    kw = dict(row_moment_coordinates=coords, diagnostics=diag, short_columns=True, signed_template=t,
              mate_normalize=True, corner_c2=True)
    if signed:
        kw.update(signed_lines=list(range(7)), signed_mode="boundary")
    model, labels, graph = build_joint(14, cat["row_types"], t["nongrid_edges"], **kw)
    build = time.process_time() - t0
    r = solve_joint(model, labels, graph, 14, seconds)
    return {"status": r["status"], "build_cpu": round(build, 1), "solve_cpu": round(r.get("cpu_seconds", 0), 1),
            "variables": r.get("model_variables"), "exact_srg_verified": r.get("exact_srg_verified")}


if __name__ == "__main__":
    path, first, last, seconds = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
    only = None
    if "--only" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    signed = "--signed" in sys.argv
    for idx, t in enumerate(records(path)):
        if idx < first or (only is not None and idx not in only):
            continue
        if idx >= last:
            break
        t = t.get("template", t)
        out = run(t, seconds, signed)
        out.update(index=idx, dim=t.get("kernel_dimension"), k=21 - len(t["nongrid_edges"]))
        if "key" in t:
            out["key"] = t["key"]
        print(json.dumps(out), flush=True)
