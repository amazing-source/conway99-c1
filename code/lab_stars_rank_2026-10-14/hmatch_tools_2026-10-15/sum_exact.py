"""Exact dim(N + hN), dim(N n hN), even / odd kernel parts (LAB 15/10/2026, SUM14 test).  usage: python sum_exact.py <json> [...]"""
import json, sys
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int
hm = {0: 1, 1: 0, 2: 3, 3: 2}


def rank(rows):
    B = [[Fr(x) for x in r] for r in rows]
    rk = 0
    if not B:
        return 0
    for c in range(len(B[0])):
        p = next((i for i in range(rk, len(B)) if B[i][c] != 0), None)
        if p is None:
            continue
        B[rk], B[p] = B[p], B[rk]
        for i in range(len(B)):
            if i != rk and B[i][c] != 0:
                f = B[i][c] / B[rk][c]
                B[i] = [a - f * b for a, b in zip(B[i], B[rk])]
        rk += 1
    return rk


for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {tuple(sorted(x)) for x in d["edges"]}
    G = [[1 if tuple(sorted((a, b))) in E else 0 for b in range(n)] for a in range(n)]
    M8 = [[(24 if a == b else 0) - 8 * G[a][b] - int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
    N = nullspace_int(M8)
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    hN = [[v[hp[i]] for i in range(n)] for v in N]
    dsum = rank(N + hN)
    ev = [[v[i] + v[hp[i]] for i in range(n)] for v in N]
    od = [[v[i] - v[hp[i]] for i in range(n)] for v in N]
    print("%s: exact nullity %d, dim(N + hN) = %d, dim(N n hN) = %d, saturated s = %d, dim P+(N) = %d, dim P-(N) = %d"
          % (f, len(N), dsum, 2 * len(N) - dsum, dsum - len(N), rank(ev), rank(od)))
