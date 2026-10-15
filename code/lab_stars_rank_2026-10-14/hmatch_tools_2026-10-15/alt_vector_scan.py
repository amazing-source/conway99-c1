"""Is the alternating odd vector a -4 eigenvector?  (LAB 15/10/2026, mechanism A, question (i))

w(eps, theta) = sum_y eps_y (f_y + theta e_y), eps_{y^1} = -eps_y (32 sign patterns), theta = +-1, f_y = 1_0y - 1_1y,
e_y = 1_2y - 1_3y (zero on C4).  w lies in V0- (h-odd, D w = 0).  For each structure: multiplicity of -4 for Gamma_0 on
V0-, the (eps, theta) with Gamma w = -4 w EXACTLY (integer check, as 44-vectors, Gamma itself, not only Gamma_0), the
same for Gamma_0, and the residual pattern otherwise.
usage: python alt_vector_scan.py <json or dir> [...]"""
import glob, itertools, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.')
sys.path.insert(0, '..')

hm = {0: 1, 1: 0, 2: 3, 3: 2}
OUT = list(range(4, 14))
files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
tab = Counter()
for f in files:
    d = json.load(open(f))
    if "labels" not in d:
        continue
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n), dtype=int)
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    G2 = G + G[np.ix_(hp, hp)]                                  # 2 Gamma_0
    sols, sols0 = [], []
    for bits in itertools.product((1, -1), repeat=5):
        eps = {}
        for k, y in enumerate(range(4, 14, 2)):
            eps[y], eps[y + 1] = bits[k], -bits[k]
        for th in (1, -1):
            w = np.zeros(n, dtype=int)
            for y in OUT:
                w[idx[frozenset((0, y))]] = eps[y]; w[idx[frozenset((1, y))]] = -eps[y]
                w[idx[frozenset((2, y))]] = th * eps[y]; w[idx[frozenset((3, y))]] = -th * eps[y]
            if not np.any(G @ w + 4 * w):
                sols.append((bits, th))
            if not np.any(G2 @ w + 8 * w):
                sols0.append((bits, th))
    # each solution comes with its negative (eps -> -eps); count up to sign
    tab[(d.get("psd"), int(round(d.get("nullity_numeric", d.get("nullity", -1)) or -1)), len(sols) // 2, len(sols0) // 2)] += 1
print("(psd flag, nullity field, #alternating w with Gamma w = -4w (up to sign), # with Gamma_0 w = -4w): count")
for k, v in sorted(tab.items(), key=lambda kv: -kv[1]):
    print("  ", k, v)
