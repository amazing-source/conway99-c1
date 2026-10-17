"""Decode a kissat model of grid243_cnf.py; report srg, class, |Aut|, regular line spreads, grid partitions."""
import sys, pickle, numpy as np
from lib243 import *
cnf, outp = sys.argv[1], sys.argv[2]
X = pickle.load(open(cnf + ".map", "rb"))
val = set()
for line in open(outp):
    if line.startswith("v "): val |= {int(t) for t in line.split()[1:] if int(t) > 0}
STD = np.zeros((9, 9), dtype=np.int64)
for a in range(9):
    for b in range(9):
        if a != b and (a // 3 == b // 3 or a % 3 == b % 3): STD[a, b] = 1
G = np.zeros((243, 243), dtype=np.int64)
for i in range(27): G[9 * i:9 * i + 9, 9 * i:9 * i + 9] = STD
for (i, j), M in X.items():
    for a in range(9):
        for b in range(9):
            if M[a][b] in val: G[9 * i + a, 9 * j + b] = G[9 * j + b, 9 * i + a] = 1
print("srg:", is_srg(G), flush=True)
known = {}
for f in ["bvls243.edges", "twin243_switched.edges", "aff0_1.npy", "stab_S3_3888.npy"]:
    H = np.load(f) if f.endswith(".npy") else load_edges(f); known[canon_g6(H)] = f
c = canon_g6(G); cls = known.get(c, "NEW")
o, orb, gens = aut(G)
from spreads import regular_spreads
sp, _ = regular_spreads(G, 20)
print("class:", cls, "|Aut| =", o, "orbits:", sorted(len(x) for x in orb)[:10], "regular line spreads:", len(sp), flush=True)
np.save(sys.argv[3] if len(sys.argv) > 3 else "grid243_found.npy", G)
