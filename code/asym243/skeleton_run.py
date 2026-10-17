"""Positive control + search for the skeleton model, starting from Gamma3's deck-1 grid representation.
mode 'control': fix every matching to Gamma3 (relabelled) -> must be feasible.
mode 'search' : keep Gamma3's skeleton, forbid Gamma3's exact matchings, look for other solutions."""
import sys, pickle, itertools, time, numpy as np
from ortools.sat.python import cp_model
from skeleton_model import build, skeleton_of
from lib243 import *
import validate_gridmodel_lib as V
mode, workers, tl = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
H, order = V.relabel("aff0_1.npy", 2)
cells = [list(range(9 * i, 9 * i + 9)) for i in range(27)]
skel = skeleton_of(H, cells)
skel = {t: v for t, v in skel.items()}
print("skeleton:", sorted(collections_counter := __import__("collections").Counter(skel.values()).items()), flush=True)
t0 = time.time(); m, var, G0, _ = build(skel); print(f"model built {time.time()-t0:.0f}s", flush=True)
if mode == "control":
    for (x, y), v in var.items():
        if x < y: m.Add(v == int(H[x, y]))
else:
    m.AddBoolOr([v.Not() for (x, y), v in var.items() if x < y and H[x, y]])
s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tl
r = s.Solve(m); print(mode, s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE) and mode == "search":
    K = G0.copy()
    for (x, y), v in var.items(): K[x, y] = int(s.Value(v))
    known = {}
    for f in ["bvls243.edges", "twin243_switched.edges", "aff0_1.npy", "stab_S3_3888.npy"]:
        Hh = np.load(f) if f.endswith(".npy") else load_edges(f); known[canon_g6(Hh)] = f
    c = canon_g6(K); print("srg:", is_srg(K), "class:", known.get(c, "NEW"), "aut:", aut(K)[0], flush=True)
    if c not in known: np.save("SKEL_NEW.npy", K)
