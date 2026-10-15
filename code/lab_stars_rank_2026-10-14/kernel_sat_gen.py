"""Kernel-imposed SAT enumeration in the generalised star model (LAB 15/10/2026, calibration on srg(243,22,1,2)).
Same method as kernel_sat_enum.py (DP encoding of Gamma n = (rI - K) n for every n in an exact integer basis of
ker T of the given structure; complete enumeration with blocking clauses), for stars_gen.Model(k, r, s).
For each structure: numerical nullity, T and U PSD, star-matching h-asymmetry per pair of lines among the stars.
usage: python kernel_sat_gen.py <structure json from real_block243.py or walk_gen.py> [max structures] [max seconds]"""
import itertools
import json
import random
import sys
import time
from collections import Counter
from fractions import Fraction as Fr

import numpy as np
from pycryptosat import Solver

from stars_gen import Model
from cls_decomp import nullspace_int

f = sys.argv[1]
cap = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 7
maxsec = float(sys.argv[3]) if len(sys.argv) > 3 else 3000
d = json.load(open(f))
M = Model(d["k"], d["r"], d["s"])
stars = d["stars"]
S, idx, e, F = M.build(stars, random.Random(1))
n = len(S)
assert [sorted(l) for l in S] == d["labels"]
K, Pi = M.matrices(S)
den = 1
for a in range(n):
    for b in range(n):
        den = max(den, Fr(K[a, b]).limit_denominator(10 ** 6).denominator)
# common denominator of K (rational entries); exact rational K from the float via limit_denominator
Kq = [[Fr(K[a, b]).limit_denominator(10 ** 6) for b in range(n)] for a in range(n)]
L = 1
for row in Kq:
    for x in row:
        L = L * x.denominator // np.gcd(L, x.denominator)
G0 = np.zeros((n, n), dtype=int)
for i, j in d["edges"]:
    G0[i, j] = G0[j, i] = 1
MT = [[int(L * ((M.r if a == b else 0) - G0[a, b] - Kq[a][b])) for b in range(n)] for a in range(n)]
N = nullspace_int(MT)
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
nv = F.n
neq = 0
for vec in N:
    for i in range(n):
        tot = sum((M.r if i == j else 0) * vec[j] - Kq[i][j] * vec[j] for j in range(n))
        assert tot.denominator == 1, "non-integral right-hand side"
        r = int(tot)
        terms = [(e[(i, j)], vec[j]) for j in range(n) if j != i and vec[j]]
        if not terms:
            assert r == 0
            continue
        neq += 1
        kk = len(terms)
        lo_suf = [0] * (kk + 1)
        hi_suf = [0] * (kk + 1)
        for t in range(kk - 1, -1, -1):
            c = terms[t][1]
            lo_suf[t] = lo_suf[t + 1] + min(0, c)
            hi_suf[t] = hi_suf[t + 1] + max(0, c)
        layer = {0: None}
        for t, (x, c) in enumerate(terms):
            nxt = {}
            for v, yv in layer.items():
                for val, lit in ((v, -x), (v + c, x)):
                    if not (val + lo_suf[t + 1] <= r <= val + hi_suf[t + 1]):
                        sol.add_clause([-lit] if yv is None else [-yv, -lit])
                        continue
                    if val not in nxt:
                        nv += 1
                        nxt[val] = nv
                    sol.add_clause([-lit, nxt[val]] if yv is None else [-yv, -lit, nxt[val]])
            layer = nxt
print("%s: kernel %d vectors, %d equations (K denominator %d)" % (f, len(N), neq, L), flush=True)
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
lines = [(stars[2 * t], stars[2 * t + 1]) for t in range(len(stars) // 2)]
hinfo = []
for (a, a2), (b, b2) in itertools.combinations(lines, 2):
    hm = {a: a2, a2: a, b: b2, b2: b}
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    hinfo.append((hp, [(i, j) for i, j in itertools.combinations(range(n), 2) if S[i] & S[j] & {a, a2, b, b2}]))
pairs = list(itertools.combinations(range(n), 2))
t0 = time.time()
hist = Counter()
cnt = 0
complete = False
while cnt < cap and time.time() - t0 < maxsec:
    ok, model = sol.solve()
    if not ok:
        complete = True
        break
    cnt += 1
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in pairs])
    G = np.zeros((n, n))
    for p in pairs:
        if model[e[p]]:
            G[p] = 1
            G[p[1], p[0]] = 1
    T = M.r * np.eye(n) - G - K
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ ((M.r - M.s) * Pi - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    psd = min(lt, lu) > -1e-9
    broken = max(sum(1 for i, j in sp if G[i, j] != G[hp[i], hp[j]]) for hp, sp in hinfo) > 0
    hist[(psd, nul, broken)] += 1
    if cnt % 500 == 0:
        print("progress: %d structures, %.0f s, %s" % (cnt, time.time() - t0, dict(hist)), flush=True)
print("%d structures (%s), %.0f s" % (cnt, "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
print("(PSD, numerical nullity, matchings broken for some pair): count")
for k2, v in sorted(hist.items(), reverse=True):
    print("  ", k2, v)
