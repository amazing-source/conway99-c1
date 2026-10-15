"""Exhaustive test: is ker T invariant under h p for SOME involution p of the outer letters (all 9 496 involutions,
mate-preserving or not)? (LAB 15/10/2026, mechanism A).  usage: python kernel_inv_all.py <json> [...]"""
import json, sys, itertools
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
OUT = list(range(4, 14))


def involutions(elems):
    if not elems:
        yield {}
        return
    a, rest = elems[0], elems[1:]
    for inv in involutions(rest):
        d = dict(inv); d[a] = a
        yield d
    for k, b in enumerate(rest):
        rest2 = rest[:k] + rest[k + 1:]
        for inv in involutions(rest2):
            d = dict(inv); d[a] = b; d[b] = a
            yield d


INVS = list(involutions(OUT))
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    T = 3 * np.eye(n) - G - np.array([[float(kval(a, b)) for b in S] for a in S])
    w, V = np.linalg.eigh(T)
    Nb = V[:, np.abs(w) < 1e-8]
    nu = Nb.shape[1]
    best, hits = -1, []
    for p in INVS:
        g = {0: 1, 1: 0, 2: 3, 3: 2}
        g.update(p)
        perm = [idx[frozenset(g[t] for t in S[i])] for i in range(n)]
        gN = Nb[np.argsort(perm), :]
        sv = np.linalg.svd(np.hstack([Nb, gN]), compute_uv=False)
        inter = 2 * nu - int(np.sum(sv > 1e-7))
        best = max(best, inter)
        if inter == nu:
            hits.append(tuple(sorted((a, b) for a, b in p.items() if a < b)))
    print("%s: nu %d, involutions tested %d, max dim(N n gN) = %d, invariant under %d of them %s"
          % (f, nu, len(INVS), best, len(hits), hits[:4]), flush=True)
