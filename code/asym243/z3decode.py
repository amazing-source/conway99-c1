"""Decode a kissat model of z3cnf.py into a graph; report srg, isomorphism class, |Aut|.
Usage: python3 z3decode.py OUT.cnf KISSAT_OUTPUT TAG"""
import sys, pickle, itertools, numpy as np
from lib243 import *
cnf, out, tag = sys.argv[1:4]
mp = pickle.load(open(cnf + ".map", "rb")); X, fpts, base = mp["X"], mp["fpts"], mp["base"]
val = set()
for line in open(out):
    if line.startswith("v "):
        val |= {int(t) for t in line.split()[1:] if int(t) > 0}
G = np.zeros((243, 243), dtype=np.int64)
for f in fpts:
    for a, b in itertools.combinations(f, 2): G[a, b] = G[b, a] = 1
for (P, R), lits in X.items():
    d = [i for i in range(3) if lits[i] in val]; assert len(d) == 1
    c = (base[(P, R)] + d[0]) % 3
    for t in range(3):
        a, b = fpts[P][t], fpts[R][(t + c) % 3]; G[a, b] = G[b, a] = 1
try: known = pickle.load(open("z3classes.pkl", "rb"))
except Exception: known = {}
c = canon_g6(G)
if c not in known:
    o, orb, gens = aut(G); known[c] = (f"Z{len(known)}", o, sorted(len(x) for x in orb))
    np.save(f"{tag}_{known[c][0]}.npy", G); pickle.dump(known, open("z3classes.pkl", "wb")); new = "NEW"
else: new = "seen"
name, o, orbs = known[c]
print(f"srg={is_srg(G)} class={name} {new} |Aut|={o} #orbits={len(orbs)}", flush=True)
