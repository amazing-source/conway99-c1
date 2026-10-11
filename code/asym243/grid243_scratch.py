"""srg(243,22,1,2) built from scratch as grid covers of K_{9,9,9} (27 grids, three parts of 9; perfect matchings
between grids of different parts; no edges between grids of the same part).  No affine structure, no line spread is
imposed.  Gauge: matchings from grid 0 to all grids of the other two parts, and from grid 9 (part 2) to the grids of
part 1 other than 0, are the identity.  Each solution is analysed: srg, iso class, |Aut|, regular line spreads.
Usage: python3 grid243_scratch.py SEED WORKERS TLIMIT NSOL [nudge]"""
import sys, time, pickle, random, numpy as np
from ortools.sat.python import cp_model
from regluing import block_model
from ortools.sat.python import cp_model as _cp
from lib243 import *
from spreads import regular_spreads
seed, workers, tl, nsol = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
n = 243
cells = [list(range(9 * i, 9 * i + 9)) for i in range(27)]
part = [i // 9 for i in range(27)]
G = np.zeros((n, n), dtype=np.int64)
for c in cells:
    for a in range(9):
        for b in range(9):
            if a != b and (a // 3 == b // 3 or a % 3 == b % 3): G[c[a], c[b]] = 1
free = [(i, j) for i in range(27) for j in range(i + 1, 27) if part[i] != part[j]]
m, var, ncons = block_model(G, cells, free, k=22, lam=1, mu=2, forbid_original=False)
from gridgauge import add_gauge
ref = {j: 0 for j in range(9, 27)}; ref.update({j: 9 for j in range(1, 9)})
add_gauge(m, var, cells, ref)
print(f"model: {len(free)} free matchings, {len(var)//2} vars, {ncons} constraints", flush=True)
rng = random.Random(seed)
if len(sys.argv) > 5:          # random hints to diversify
    for (x, y), v in var.items():
        if x < y: m.AddHint(v, rng.random() < 1 / 9)
known = {}
for f in ["bvls243.edges", "twin243_switched.edges", "aff0_1.npy", "stab_S3_3888.npy"]:
    H = np.load(f) if f.endswith(".npy") else load_edges(f); known[canon_g6(H)] = f.split(".")[0]
for it in range(nsol):
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.max_time_in_seconds = tl
    s.parameters.random_seed = seed + it
    t0 = time.time(); r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("status", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True); break
    H = G.copy()
    for (x, y), v in var.items(): H[x, y] = int(s.Value(v))
    c = canon_g6(H); new = c not in known
    if new:
        o = aut(H)[0]; known[c] = f"GS{len(known)}_{o}"; np.save(f"{known[c]}.npy", H)
    sp, _ = regular_spreads(H, 20)
    print(f"[{time.time()-t0:.0f}s] sol {it+1}: srg={is_srg(H)} class={known[c]} {'NEW' if new else ''} "
          f"regular line spreads={len(sp)}", flush=True)
    m.AddBoolOr([v.Not() for (x, y), v in var.items() if x < y and s.Value(v)])
