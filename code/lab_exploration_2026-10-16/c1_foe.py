"""Size of the odd-even block of F (Schur of T_S onto Y) in the basis f_s = (1_{2s}-1_{3s})/sqrt2, g_s = (1_{2s}+1_{3s})/sqrt2,
on c(l)=1 sides; also for c(l) >= 2 sides for comparison; and whether ker F splits."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, gl_connected
sys.path.insert(0, r"C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16")
from gg_test import line_graph, components
ix = [S.index(l) for l in XL]; iy = [S.index(l) for l in Y]
Yl = list(Y)
O = np.zeros((20, 10)); E = np.zeros((20, 10))
for k, s in enumerate(range(4, 14)):
    O[Yl.index(frozenset((2, s))), k] = 1 / np.sqrt(2); O[Yl.index(frozenset((3, s))), k] = -1 / np.sqrt(2)
    E[Yl.index(frozenset((2, s))), k] = 1 / np.sqrt(2); E[Yl.index(frozenset((3, s))), k] = 1 / np.sqrt(2)
stats = Counter(); mx = {}
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    for side in (0, 1):
        L, EE = relabel(S0, E0, side)
        V, pos, A = line_graph(L, EE)
        if not all(sum(r) == 3 for r in A):
            continue
        c = components(A)
        G = np.zeros((44, 44))
        for i, j in itertools.combinations(range(44), 2):
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
        K8 = np.array([[k8(a, b) for b in S] for a in S], float)
        T = (24 * np.eye(44) - 8 * G - K8) / 8
        F = T[np.ix_(iy, iy)] - T[np.ix_(ix, iy)].T @ np.linalg.pinv(T[np.ix_(ix, ix)], rcond=1e-10) @ T[np.ix_(ix, iy)]
        Foe = O.T @ F @ E
        key = "c=1" if c == 1 else "c>=2"
        mx[key] = max(mx.get(key, 0), np.abs(Foe).max())
        stats[(key, np.abs(Foe).max() < 1e-9)] += 1
print("max |F_oe| :", {k: round(v, 4) for k, v in mx.items()})
print("(c, F_oe == 0) :", dict(stats))
