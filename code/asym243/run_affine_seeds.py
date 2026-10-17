"""Diversified sampling of affine line systems with the h_0 spread: first solution for many random seeds,
with a random linear objective to push the solver into different regions."""
import sys, time, pickle, numpy as np
from ortools.sat.python import cp_model
from linesat import build
from lines_model import *
from lib243 import *
d = 0; seeds = range(int(sys.argv[1]), int(sys.argv[2])); workers = int(sys.argv[3]); tag = sys.argv[4]
hd = HS[d]
fixed = lines_of_direction(hd)
cands = []
for mm in range(11):
    if mm == d: continue
    for e in (0, 1, 2):
        cands += lines_of_direction(add(HS[mm], hd, e))
A0 = load_edges("bvls243.edges"); B0 = load_edges("twin243_switched.edges")
try:
    known = pickle.load(open("classes.pkl", "rb"))
except Exception:
    known = {canon_g6(A0): ("BvLS", "3849120"), canon_g6(B0): ("twin", "4320")}
for seed in seeds:
    m, x, cl = build(fixed, cands)
    rng = np.random.default_rng(seed)
    w = rng.integers(-3, 4, size=len(cl))
    m.Minimize(sum(int(wi) * x[c] for wi, c in zip(w, cl)))
    s = cp_model.CpSolver(); s.parameters.num_workers = workers; s.parameters.random_seed = seed
    s.parameters.max_time_in_seconds = 900; s.parameters.stop_after_first_solution = True
    t0 = time.time(); r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"seed {seed}: {s.StatusName(r)} {time.time()-t0:.0f}s", flush=True); continue
    sel = [c for c in cl if s.Value(x[c])]
    G = graph_from_lines(list(fixed) + sel)
    c = canon_g6(G)
    if c not in known:
        o = aut(G)[0]; name = f"A{len(known)}"; known[c] = (name, o); np.save(f"{tag}_{name}.npy", G)
        pickle.dump(known, open("classes.pkl", "wb")); new = " NEW"
    else:
        new = ""
    name, o = known[c]
    print(f"seed {seed}: srg={is_srg(G)} class={name}{new} |Aut|={o} [{time.time()-t0:.0f}s]", flush=True)
