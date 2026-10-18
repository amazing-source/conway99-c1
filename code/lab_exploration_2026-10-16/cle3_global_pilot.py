"""Pilot of the global stage on open c <= 3 root templates (LAB, 18/10/2026).
Uses Codex's root_component_global.build (read-only import from his repository): exact unseeded model on the 84 labels,
all C1/C2 equations, the template's component equations, R linked to the graph, trace <= 28 dim ker C, root prism
budget 51 (budget root).  The Gram stays variable.  One CP-SAT worker.  INFEASIBLE = solver verdict for the template.
usage: python cle3_global_pilot.py <templates json(.gz) with 'open' or 'templates'> <seconds> <i1> [i2 ...]"""
import ctypes
import gzip
import json
import sys
import time

sys.path.insert(0, r"C:\Users\RESEARCHER\Desktop\Recherche_Conway\c1-asymmetry-audit\code\codex")
from ortools.sat.python import cp_model  # noqa: E402
from root_component_global import build  # noqa: E402

try:
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
except Exception:
    pass
src, secs = sys.argv[1], float(sys.argv[2])
data = json.load(gzip.open(src) if src.endswith(".gz") else open(src))
items = data.get("open") or [{"template": t} for t in data["templates"]]
for i in map(int, sys.argv[3:]):
    t = items[i]["template"]
    t0 = time.time()
    model, graph, info = build(t, {"cuts": [], "root_prism_budget": 51})
    tb = time.time() - t0
    if model is None:
        print(json.dumps({"index": i, "status": info["status"], "build_s": round(tb, 1)}), flush=True)
        continue
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = secs
    st = solver.solve(model)
    print(json.dumps({"index": i, "grids": items[i].get("grids"), "kernel_dimension": t["kernel_dimension"],
                      "c_by_line": t["component_count_by_root_line"], "forced_edges": info.get("template_forced_edges"),
                      "status": solver.status_name(st), "build_s": round(tb, 1), "solve_s": round(solver.wall_time, 1),
                      "conflicts": solver.num_conflicts}), flush=True)
