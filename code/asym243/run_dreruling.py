"""d-re-ruling space: keep all lines of direction h_d; for every other line choose any affine line
whose direction lies in {h_m + e h_d}. Enumerate all srg solutions."""
import sys, numpy as np
from linesat import *
from lib243 import *
d = int(sys.argv[1]) if len(sys.argv) > 1 else 0
hd = HS[d]
fixed = lines_of_direction(hd)
cands = []
for mm in range(11):
    if mm == d: continue
    for e in (0, 1, 2):
        cands += lines_of_direction(add(HS[mm], hd, e))
print("d =", d, "fixed", len(fixed), "cands", len(cands))
sols, st = solve_all(fixed, cands, limit=int(sys.argv[2]) if len(sys.argv) > 2 else 10)
import pickle; pickle.dump((fixed, sols), open(f"dreruling_d{d}.pkl", "wb"))
for i, sel in enumerate(sols):
    A = graph_from_lines(list(fixed) + list(sel))
    o, orb, g = aut(A)
    gv, ng = grids_per_vertex(A)
    print(i, "srg", is_srg(A), "aut", o, "orbits", sorted(len(x) for x in orb)[:12], "grids", ng, flush=True)
print("status", st)
