"""Targeted flag blocks with flags of DIFFERENT sizes (LAB 19/10/2026).  sigma = a labelled line (triangle 0,1,2) or a
labelled vertex; flags = sigma itself (v = 1) plus all admissible extensions of size m1 and m2 (lists given by size).
The amalgam of F1 (size a) and F2 (size b) over sigma has at most a + b - k vertices.  Output: sparse incidence like
flag_engine (T_*.npz) so that flag_cut_loop.py can use it.
usage: python flag_targeted.py <census json> <sigma: line|vertex|edge|nonedge> <sizes comma list> <out npz>"""
import itertools, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "census2_code"))
import census2 as C2  # noqa: E402
from flag_engine import load_types  # noqa: E402
from flag_sdp import admissible, flags_of  # noqa: E402

def amalgams_mixed(F1, F2, k):
    a, b = len(F1), len(F2)
    X1, X2 = list(range(k, a)), list(range(k, b))
    low = (1 << k) - 1
    for d in range(0, min(len(X1), len(X2)) + 1):
        for D1 in itertools.combinations(X1, d):
            for D2 in itertools.permutations(X2, d):
                pairs = list(zip(D1, D2))
                if not all((F1[p] & low) == (F2[q] & low) for p, q in pairs):
                    continue
                if any((F1[p1] >> p2 & 1) != (F2[q1] >> q2 & 1) for (p1, q1), (p2, q2) in itertools.combinations(pairs, 2)):
                    continue
                free1 = [x for x in X1 if x not in D1]
                free2 = [y for y in X2 if y not in D2]
                n = a + len(free2)
                idx2 = {v: v for v in range(k)}
                idx2.update({y: a + i for i, y in enumerate(free2)})
                idx2.update({q: p for p, q in pairs})
                base = list(F1) + [0] * len(free2)
                for y in free2:
                    for zz in range(b):
                        if F2[y] >> zz & 1:
                            u, w = idx2[y], idx2[zz]
                            base[u] |= 1 << w; base[w] |= 1 << u
                slots = [(p, idx2[y]) for p in free1 for y in free2]
                for bits in range(1 << len(slots)):
                    rows = base[:]
                    for t, (u, w) in enumerate(slots):
                        if bits >> t & 1:
                            rows[u] |= 1 << w; rows[w] |= 1 << u
                    yield n, rows

path, kind, sizes, out = sys.argv[1], sys.argv[2], [int(s) for s in sys.argv[3].split(",")], sys.argv[4]
d, tid, forms = load_types(path)
maxn = max(int(n) for n in d["types"])
sigma = {"line": [6, 5, 3], "vertex": [0], "edge": [2, 1], "nonedge": [0, 0], "path3": [6, 1, 1], "ei": [2, 1, 0], "indep3": [0, 0, 0]}[kind]
k = len(sigma)
flags = [list(sigma)]
for s in sizes:
    flags += flags_of(sigma, k, s)
nf = len(flags)
t0 = time.time()
pairs, tids, mult = [], [], []
cache = {}
for i in range(nf):
    for j in range(i, nf):
        if len(flags[i]) + len(flags[j]) - k > maxn:
            raise SystemExit("amalgam too large for the census")
        acc = {}
        for n, rows in amalgams_mixed(flags[i], flags[j], k):
            key = (n, tuple(rows))
            t = cache.get(key, -2)
            if t == -2:
                t = tid.get((n, C2.canon(n, list(rows))[0]), -1) if admissible(n, rows) else -1
                cache[key] = t
            if t >= 0:
                acc[t] = acc.get(t, 0) + 1
        for t, c in acc.items():
            pairs.append(i * nf + j); tids.append(t); mult.append(c)
np.savez_compressed(out, nf=nf, pairs=np.array(pairs, dtype=np.int64), tids=np.array(tids, dtype=np.int32),
                    mult=np.array(mult, dtype=np.int32), k=k, m=max(sizes), sigma=-1)
print("%s sigma, sizes %s: %d flags, %d entries  [%.0f s]" % (kind, sizes, nf, len(pairs), time.time() - t0))
