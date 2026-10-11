"""Sub-case (A) of C1 (note 166): srg(99,14,1,2) as 11 disjoint 3x3 grids with a perfect matching between any two
grids (a 9-fold grid cover of K_11).  Unknowns: the 55 matchings.  Gauge: the matchings from grid 0 to grids 1..10 are
the identity (relabelling the points of grids 1..10).  Uses the same exact model as regluing.py.
Usage: python3 conway_grids.py WORKERS TIME_LIMIT"""
import sys, time, itertools, numpy as np
from ortools.sat.python import cp_model
from regluing import block_model
from lib243 import is_srg, aut
n = 99
cells = [list(range(9 * i, 9 * i + 9)) for i in range(11)]
G = np.zeros((n, n), dtype=np.int64)
for c in cells:                                    # grid K3 x K3 on labels (r, s) -> 3r + s
    for a in range(9):
        for b in range(9):
            if a != b and (a // 3 == b // 3 or a % 3 == b % 3): G[c[a], c[b]] = 1
for j in range(1, 11):                            # gauge: grid 0 -> grid j is the identity
    for a in range(9): G[cells[0][a], cells[j][a]] = G[cells[j][a], cells[0][a]] = 1
free = [(i, j) for i in range(1, 11) for j in range(i + 1, 11)]
m, var, ncons = block_model(G, cells, free, k=14, lam=1, mu=2, forbid_original=False)
# degree is automatic (4 inside + one per other grid)
print(f"model: {len(free)} free matchings, {len(var)//2} edge variables, {ncons} pair constraints", flush=True)
s = cp_model.CpSolver(); s.parameters.num_workers = int(sys.argv[1]); s.parameters.max_time_in_seconds = float(sys.argv[2])
s.parameters.log_search_progress = False
t0 = time.time(); r = s.Solve(m)
print("status:", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True)
if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    H = G.copy()
    for (x, y), v in var.items(): H[x, y] = int(s.Value(v))
    print("srg(99,14,1,2):", is_srg(H, k=14, lam=1, mu=2), "aut:", aut(H)[0], flush=True)
    np.save("CONWAY_CANDIDATE.npy", H)
