"""Escalating re-gluing of a grid-cover representation.  Free sets: 2 grids (same part / different parts),
3 grids (a quotient triangle / a coclique), 9 grids (a whole part of K_{9,9,9})."""
import sys, pickle, itertools, numpy as np
from regluing import solve
from lib243 import *
path, pidx, workers = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
G = np.load(path) if path.endswith(".npy") else load_edges(path)
part = pickle.load(open(path + ".gridparts.pkl", "rb"))[pidx]
m = len(part)
Qd = [[bool(G[np.ix_(part[i], part[j])].sum()) for j in range(m)] for i in range(m)]
# parts of the complete tripartite quotient
cls = []
for i in range(m):
    for c in cls:
        if not Qd[i][c[0]]: c.append(i); break
    else: cls.append([i])
print("quotient parts:", [len(c) for c in cls], flush=True)
a0, a1 = cls[0][0], cls[0][1]; b0 = cls[1][0]; c0 = cls[2][0]
sets = {"2 same part": [a0, a1], "2 adjacent": [a0, b0], "3 triangle": [a0, b0, c0], "3 coclique": cls[0][:3],
        "4 mixed": [a0, a1, b0, c0], "9 whole part": cls[0]}
known = {canon_g6(G): "self"}
for f in ["bvls243.edges", "twin243_switched.edges", "aff0_1.npy", "stab_S3_3888.npy"]:
    H = np.load(f) if f.endswith(".npy") else load_edges(f); known.setdefault(canon_g6(H), f.split(".")[0])
for name, fl in sets.items():
    free = sorted({(min(i, j), max(i, j)) for i in fl for j in range(m) if j != i and Qd[i][j]})
    for i in fl:
        j0 = next(j for j in range(m) if Qd[i][j] and j not in fl)
        if (min(i, j0), max(i, j0)) in free: free.remove((min(i, j0), max(i, j0)))
    res = solve(G, part, free, limit=6, workers=workers, tlimit=1200, known=known, tag="RG")
    print(f"[{name}] free matchings {len(free)}: {res}", flush=True)
