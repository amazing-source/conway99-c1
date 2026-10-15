"""dim(ker T + g ker T) for frame elements g (LAB 15/10/2026): is the bound 14 special to h = (0 1)(2 3)?
usage: python sum_test.py <json or dir> [...]"""
import glob, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from stars_rank import kval
G_LIST = {
    "h=(01)(23)": {0: 1, 1: 0, 2: 3, 3: 2},
    "(01)": {0: 1, 1: 0},
    "(23)": {2: 3, 3: 2},
    "tau=(02)(13)": {0: 2, 2: 0, 1: 3, 3: 1},
    "(45)": {4: 5, 5: 4},
    "h(45)": {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4},
    "M (all flips)": {y: y ^ 1 for y in range(4, 14)},
    "hM": dict([(0, 1), (1, 0), (2, 3), (3, 2)] + [(y, y ^ 1) for y in range(4, 14)]),
    "(01)M": dict([(0, 1), (1, 0)] + [(y, y ^ 1) for y in range(4, 14)]),
    "(45)(67) swap lines": {4: 6, 6: 4, 5: 7, 7: 5},
}
files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
tab = {k: Counter() for k in G_LIST}
for f in files:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    K = np.array([[kval(a, b) for b in S] for a in S])
    w, V = np.linalg.eigh(3 * np.eye(n) - G - K)
    N = V[:, np.abs(w) < 1e-7]; nu = N.shape[1]
    for name, gm in G_LIST.items():
        perm = [idx[frozenset(gm.get(y, y) for y in s)] for s in S]
        gN = N[np.argsort(perm), :]
        dimsum = int(np.sum(np.linalg.svd(np.hstack([N, gN]), compute_uv=False) > 1e-7))
        inv = bool(np.array_equal(G[np.ix_(perm, perm)], G))
        tab[name][(nu, dimsum, "structure g-invariant" if inv else "not g-invariant")] += 1
for name in G_LIST:
    print("%-22s" % name, sorted(tab[name].items(), key=lambda kv: (-kv[0][0], -kv[0][1])))
