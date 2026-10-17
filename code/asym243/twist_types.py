"""Twist type of a matching sigma between two grids: the relative position of the grid A and the transported grid
sigma^*B on the same 9 points.  Invariant: (number of common edges, sorted degree sequence of the common-edge graph,
number of common lines).  Statistics over all grid partitions of the known srg(243,22,1,2), and the gluing law check
sum_C P(rho_C) = 2J - I - Adj(A) - Adj(sigma*B)."""
import sys, pickle, os, itertools, collections, numpy as np
from lib243 import *
from gridcover_anatomy import grid_partitions
def twist(Aadj, Badj):
    common = Aadj & Badj
    lines_common = 0
    for t in itertools.combinations(range(9), 3):
        if all(Aadj[a, b] and Badj[a, b] for a, b in itertools.combinations(t, 2)): lines_common += 1
    return (int(common.sum()) // 2, tuple(sorted(common.sum(1).tolist())), lines_common)
for path in sys.argv[1:]:
    G = np.load(path) if path.endswith(".npy") else load_edges(path)
    parts = pickle.load(open(path + ".gridparts.pkl", "rb")) if os.path.exists(path + ".gridparts.pkl") else grid_partitions(G)
    pickle.dump(parts, open(path + ".gridparts.pkl", "wb"))
    stats = collections.Counter(); law_ok = True
    for part in parts:
        m = len(part)
        for i in range(m):
            for j in range(m):
                if i < j and G[np.ix_(part[i], part[j])].sum():
                    A_ = part[i]; B_ = part[j]
                    sig = {a: B_[int(np.nonzero(G[a, B_])[0][0])] for a in A_}
                    sinv = {b: a for a, b in sig.items()}
                    Aadj = G[np.ix_(A_, A_)].astype(bool)
                    Badj = np.array([[bool(G[sig[a], sig[b]]) for b in A_] for a in A_])
                    stats[twist(Aadj, Badj)] += 1
                    # gluing law
                    M = np.zeros((9, 9), dtype=int)
                    for k in range(m):
                        if k in (i, j) or not G[np.ix_(part[i], part[k])].sum() or not G[np.ix_(part[j], part[k])].sum(): continue
                        C_ = part[k]
                        sAC = {a: C_[int(np.nonzero(G[a, C_])[0][0])] for a in A_}
                        sCB = {c: B_[int(np.nonzero(G[c, B_])[0][0])] for c in C_}
                        for ia, a in enumerate(A_):
                            M[ia, A_.index(sinv[sCB[sAC[a]]])] += 1
                    target = 2 * np.ones((9, 9), int) - np.eye(9, dtype=int) - Aadj.astype(int) - Badj.astype(int)
                    if not (M == target).all(): law_ok = False
    print(path, "gluing law holds:", law_ok)
    for k, v in sorted(stats.items(), key=lambda t: -t[1]): print("   twist (common edges, degrees, common lines) =", k, ":", v)
