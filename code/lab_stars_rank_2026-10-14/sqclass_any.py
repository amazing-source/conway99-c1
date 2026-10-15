"""Square class of disc(8T_S4) for four-star structures of rank 30, PSD or not (LAB 15/10/2026).
For any integer 44 x 30 matrix X with det(X^T M X) != 0 (M = 8T_S4 of rank 30), the vectors M x_i span a full sublattice
of R = M Z^44 with form b(Mx, My) = x^T M y, so det(X^T M X) = disc(R) [index]^2: its square class is that of every
non-zero 30 x 30 principal minor (square-class lemma).  Two random X are used as a consistency check.
Prints the exponent parities at 2, 3, 5, 7 and whether the rest is a square.
usage: python sqclass_any.py <json> [...]"""
import json
import math
import random
import sys

import numpy as np

from stars_rank import kval
from z5_enum import exact_rank
from sc_square_class import det_int


def sqclass(d):
    s = -1 if d < 0 else 1
    d = abs(d)
    par = {}
    for p in (2, 3, 5, 7):
        e = 0
        while d % p == 0:
            d //= p
            e += 1
        par[p] = e
    odd = []
    p = 11
    while p < 20000 and d > 1:
        e = 0
        while d % p == 0:
            d //= p
            e += 1
        if e % 2:
            odd.append(p)
        p += 2
    return s, par, odd, (math.isqrt(d) ** 2 == d)


def items(f):
    """single structure (labels, edges) or a collection (structures / found / valid_edges)"""
    dj = json.load(open(f))
    if "edges" in dj:
        yield f, dj
        return
    for coll in ("structures", "found"):
        if coll in dj:
            for k, st in enumerate(dj[coll]):
                yield "%s[%d]" % (f, k), {"labels": dj["labels"], "edges": st["edges"]}
            return
    if "valid_edges" in dj:
        for k, ed in enumerate(dj["valid_edges"]):
            yield "%s[%d]" % (f, k), {"labels": dj["labels"], "edges": ed}


seen = set()
tally = {}
for f, dj in (it for g in sys.argv[1:] for it in items(g)):
    key = tuple(tuple(e) for e in dj["edges"])
    if key in seen:
        continue
    seen.add(key)
    S = [frozenset(l) for l in dj["labels"]]
    n = len(S)
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in dj["edges"]:
        G[i, j] = G[j, i] = 1
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    M = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    r = exact_rank(M.tolist())
    if r != 30:
        print("%s: rank %d (skip)" % (f, r))
        continue
    rng = random.Random(1)
    out = []
    while len(out) < 2:
        X = np.array([[rng.choice((-1, 0, 1)) for _ in range(30)] for _ in range(n)], dtype=object)
        Gm = (X.T.dot(np.array(M, dtype=object))).dot(X)
        dd = det_int([[int(x) for x in row] for row in Gm.tolist()])
        if dd != 0:
            out.append(sqclass(dd))
    (s1, p1, o1, q1), (s2, p2, o2, q2) = out
    same = (s1 == s2 and all(p1[p] % 2 == p2[p] % 2 for p in p1) and o1 == o2 and q1 == q2)
    psd = bool(np.linalg.eigvalsh(M / 8.0).min() > -1e-9)
    print("%s: PSD %s, sign %+d, parities v2 %d v3 %d v5 %d v7 %d, other odd primes %s, cofactor square %s, consistent %s"
          % (f, psd, s1, p1[2] % 2, p1[3] % 2, p1[5] % 2, p1[7] % 2, o1, q1, same), flush=True)
    tk = (n, psd, s1, p1[2] % 2, p1[3] % 2, p1[5] % 2, p1[7] % 2, bool(o1) or not q1)
    tally[tk] = tally.get(tk, 0) + 1
print("tally (labels, PSD, sign, v2, v3, v5, v7 parities, other primes): count")
for k, v in sorted(tally.items()):
    print("  ", k, v)
