"""d-re-ruling / affine line systems: fixed lines of direction h_d, candidates = lines of directions h_m + e h_d.
Each solution is analysed immediately (srg, isomorphism class, |Aut|, cover parity)."""
import sys, time, numpy as np
from ortools.sat.python import cp_model
from linesat import build
from lines_model import *
from lib243 import *
from cover import fibres_of, is_cover, parity_cocycle, is_coboundary
d = int(sys.argv[1]); seed = int(sys.argv[2]); limit = int(sys.argv[3]); tag = sys.argv[4]
hd = HS[d]
fixed = lines_of_direction(hd)
cands = []
for mm in range(11):
    if mm == d: continue
    for e in (0, 1, 2):
        cands += lines_of_direction(add(HS[mm], hd, e))
m, x, cands = build(fixed, cands)
A0 = load_edges("bvls243.edges"); B0 = load_edges("twin243_switched.edges")
known = {canon_g6(A0): "BvLS", canon_g6(B0): "twin"}
fib = [list(f) for f in fixed]
t0 = time.time(); n = 0
while n < limit:
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 7200
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("status", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True); break
    sel = [c for c in cands if s.Value(x[c])]
    G = graph_from_lines(list(fixed) + sel); n += 1
    np.save(f"{tag}_{n}.npy", G)
    c = canon_g6(G); name = known.get(c)
    if name is None:
        name = f"new{len(known)-1}"; known[c] = name
    okc, Qa = is_cover(G, fib)
    cob = is_coboundary(parity_cocycle(G, fib, Qa), 81) if okc else None
    o, orb, gens = aut(G)
    gv, ng = grids_per_vertex(G)
    print(f"[{time.time()-t0:.0f}s] sol {n}: srg={is_srg(G)} class={name} |Aut|={o} #orbits={len(orb)} "
          f"cover={okc} parity_coboundary={cob} grids={ng}", flush=True)
    m.AddBoolOr([x[c_].Not() for c_ in sel])
