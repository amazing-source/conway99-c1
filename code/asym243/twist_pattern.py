"""Joint law: twist type of sigma_AB  x  pattern of the 9 transversal lines through (A,B)."""
import sys, pickle, itertools, collections, numpy as np
from lib243 import *
from twist_types import twist
tot = collections.Counter()
for path in sys.argv[1:]:
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    parts = pickle.load(open(path + ".gridparts.pkl", "rb"))
    tri = triangles(G)
    for part in parts:
        cell = {p: i for i, g in enumerate(part) for p in g}
        cnt = collections.Counter()
        for t in tri:
            cs = tuple(sorted(cell[p] for p in t))
            if len(set(cs)) == 3: cnt[cs] += 1
        pairpat = collections.defaultdict(list)
        for (a, b, c), v in cnt.items():
            for pr in ((a, b), (a, c), (b, c)): pairpat[pr].append(v)
        for (i, j), vs in pairpat.items():
            A_, B_ = part[i], part[j]
            sig = {a: B_[int(np.nonzero(G[a, B_])[0][0])] for a in A_}
            Aadj = G[np.ix_(A_, A_)].astype(bool)
            Badj = np.array([[bool(G[sig[a], sig[b]]) for b in A_] for a in A_])
            tw = twist(Aadj, Badj)
            tot[((tw[0], tw[2]), tuple(sorted(vs, reverse=True)))] += 1
for k, v in sorted(tot.items()): print("twist (common edges, common lines) =", k[0], " pattern", k[1], ":", v)
