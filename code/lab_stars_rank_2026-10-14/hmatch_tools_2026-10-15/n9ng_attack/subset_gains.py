"""f(A) = gain of the m-side outer blocks C_mn, n in A, over V_X, for every subset A of the 5 outer lines; also per star.
usage: python subset_gains.py <json> [...]"""
import json, sys, itertools
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
LINES = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
def rk(M):
    w = np.linalg.eigvalsh(M); return int(np.sum(w > 1e-7))
for f in sys.argv[1:]:
    d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    X = [i for i in range(n) if S[i] & {0, 1}]
    base = rk(T[np.ix_(X, X)])
    blocks = [[idx[frozenset((s, y))] for s in (2, 3) for y in ln] for ln in LINES]
    byk = {}
    for k in range(6):
        vals = []
        for A in itertools.combinations(range(5), k):
            cur = X + sum((blocks[j] for j in A), [])
            vals.append(rk(T[np.ix_(cur, cur)]) - base)
        byk[k] = sorted(set(vals))
    # star 2 only blocks (2y,2y') and both
    print("%s: f by |A|: %s" % (f.split('/')[-1], " ".join("%d:%s" % (k, byk[k]) for k in range(6))))
