"""Two-direction re-ruling: fixed lines of directions h_a and h_b; every other line of BvLS (direction h_m) may stay
or be re-ruled to h_m +- h_a or h_m +- h_b (any affine line of those 45 directions).  We force at least one line of
each re-ruled family, so a solution is neither an h_a- nor an h_b-re-voltaging of BvLS."""
import sys, time, pickle, numpy as np
from ortools.sat.python import cp_model
from linesat import build
from lines_model import *
from lib243 import *
from cover import is_cover
a, b, seed, limit, tag = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
fixed = lines_of_direction(HS[a]) + lines_of_direction(HS[b])
fam = {"plain": [], "A": [], "B": []}
for mm in range(11):
    if mm in (a, b): continue
    fam["plain"] += lines_of_direction(HS[mm])
    for e in (1, 2):
        fam["A"] += lines_of_direction(add(HS[mm], HS[a], e))
        fam["B"] += lines_of_direction(add(HS[mm], HS[b], e))
cands = fam["plain"] + fam["A"] + fam["B"]
m, x, cl = build(fixed, cands)
m.AddBoolOr([x[c] for c in fam["A"]]); m.AddBoolOr([x[c] for c in fam["B"]])
print("model built:", len(cl), "candidates", flush=True)
A0 = load_edges("bvls243.edges")
fibA = [list(f) for f in lines_of_direction(HS[a])]; fibB = [list(f) for f in lines_of_direction(HS[b])]
t0 = time.time(); n = 0
while n < limit:
    s = cp_model.CpSolver(); s.parameters.num_workers = 4; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 7200
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("status", s.StatusName(r), f"{time.time()-t0:.0f}s", flush=True); break
    sel = [c for c in cl if s.Value(x[c])]
    G = graph_from_lines(list(fixed) + sel); n += 1
    np.save(f"{tag}_{n}.npy", G)
    o, orb, gens = aut(G)
    ca, _ = is_cover(G, fibA); cb, _ = is_cover(G, fibB)
    nA = sum(1 for c in fam["A"] if s.Value(x[c])); nB = sum(1 for c in fam["B"] if s.Value(x[c]))
    print(f"[{time.time()-t0:.0f}s] sol {n}: srg={is_srg(G)} |Aut|={o} #orbits={len(orb)} reruled A={nA} B={nB} "
          f"cover_a={ca} cover_b={cb}", flush=True)
    m.AddBoolOr([x[c].Not() for c in sel])
