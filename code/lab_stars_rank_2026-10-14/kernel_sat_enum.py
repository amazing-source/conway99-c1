"""Kernel-imposed SAT enumeration (LAB 15/10/2026, (H-MATCH) test; faster than kernel_enum.py's MILP).

All admissible four-star structures (stars_rank.build: C1, C1', C2 in CNF) whose kernel contains the kernel N of a
given structure: 8 Gamma n = 8 (3I - K) n for every n in N, i.e. for every label i the linear equation
sum_j n_j x_ij = r_i over the 0/1 edge variables, encoded by a forward partial-sum (DP) encoding: y[t][v] = "the first
t terms sum to v" with x_t & y[t-1][v] -> y[t][v + c_t], ~x_t & y[t-1][v] -> y[t][v], y[0][0] true, and every final
value other than r_i forbidden (the true partial sums are forced, so a final value r_i is reached iff the equation
holds).  Enumeration with blocking clauses on the edge variables until UNSAT (COMPLETE).  For each structure:
numerical nullity, T and U PSD (numerical, on the complement of the star vectors), star-matching h-asymmetry.
Saves every PSD structure of nullity >= 14 whose star matchings are not h-related (_KS_k.json).
usage: python kernel_sat_enum.py <structure json> [max structures] [max seconds]"""
import itertools
import json
import os
import random
import sys
import time
from collections import Counter

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from cls_decomp import nullspace_int

f = sys.argv[1]
cap = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 6
maxsec = float(sys.argv[3]) if len(sys.argv) > 3 else 3000
d = json.load(open(f))
rng = random.Random(5)
S, idx, e, F = build([0, 1, 2, 3], rng)
n = len(S)
assert [sorted(l) for l in S] == d["labels"]
E0 = {tuple(sorted(x)) for x in d["edges"]}
K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
G0 = [[1 if tuple(sorted((a, b))) in E0 else 0 for b in range(n)] for a in range(n)]
M = [[(24 if a == b else 0) - 8 * G0[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
N = nullspace_int(M)
if os.environ.get("DROPIDX"):                 # impose only part of the kernel (drop the listed basis vectors)
    dd = {int(t) for t in os.environ["DROPIDX"].split(",")}
    N = [v for q, v in enumerate(N) if q not in dd]
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
nv = [F.n]


def newvar():
    nv[0] += 1
    return nv[0]


neq = 0
naux = 0
for vec in N:
    for i in range(n):
        tot = sum((24 if i == j else 0) * vec[j] - K8[i][j] * vec[j] for j in range(n))
        assert tot % 8 == 0, "non-integral right-hand side"
        r = tot // 8
        terms = [(e[(i, j)], vec[j]) for j in range(n) if j != i and vec[j]]
        if not terms:
            assert r == 0
            continue
        neq += 1
        # suffix ranges for pruning: values reachable from layer t to the end
        k = len(terms)
        lo_suf = [0] * (k + 1)
        hi_suf = [0] * (k + 1)
        for t in range(k - 1, -1, -1):
            c = terms[t][1]
            lo_suf[t] = lo_suf[t + 1] + min(0, c)
            hi_suf[t] = hi_suf[t + 1] + max(0, c)
        layer = {0: None}                     # value -> variable (None = constant true at layer 0)
        for t, (x, c) in enumerate(terms):
            nxt = {}
            for v, yv in layer.items():
                for val, lit in ((v, -x), (v + c, x)):
                    rem_lo, rem_hi = lo_suf[t + 1], hi_suf[t + 1]
                    if not (val + rem_lo <= r <= val + rem_hi):
                        # this branch can never reach r: forbid it
                        cl = [-lit] if yv is None else [-yv, -lit]
                        sol.add_clause(cl)
                        continue
                    if val not in nxt:
                        nxt[val] = newvar()
                        naux += 1
                    cl = [-lit, nxt[val]] if yv is None else [-yv, -lit, nxt[val]]
                    sol.add_clause(cl)
            layer = nxt
        for v, yv in layer.items():
            if v != r:
                sol.add_clause([-yv])
print("%s: kernel %d vectors, %d equations, %d auxiliary variables" % (f, len(N), neq, naux), flush=True)
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
Kf = np.array([[kval(a, b) for b in S] for a in S])
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
pairs = list(itertools.combinations(range(n), 2))
t0 = time.time()
hist = Counter()
found = 0
saved = 0
complete = False
while found < cap and time.time() - t0 < maxsec:
    ok, model = sol.solve()
    if not ok:
        complete = True
        break
    found += 1
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in pairs])
    G = np.zeros((n, n))
    for (i, j) in pairs:
        if model[e[(i, j)]]:
            G[i, j] = G[j, i] = 1
    T = 3 * np.eye(n) - G - Kf
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    psd = min(lt, lu) > -1e-9
    masym = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
    hist[(psd, nul, masym > 0)] += 1
    if psd and nul >= 14 and masym > 0:
        saved += 1
        out = os.path.basename(f).replace(".json", "") + "_KS_%d.json" % saved
        json.dump({"labels": d["labels"], "edges": [[i, j] for i, j in pairs if G[i, j]], "masym": masym,
                   "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul}, open(out, "w"))
        print("KERNEL-SAT TARGET: PSD, nullity %d, matchings not h-related (%d pairs), saved %s" % (nul, masym, out),
              flush=True)
    if found % 1000 == 0:
        print("progress: %d structures, %.0f s, %s" % (found, time.time() - t0, dict(hist)), flush=True)
print("%d structures (%s), %.0f s" % (found, "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
print("(PSD, numerical nullity, matchings broken): count")
for k, v in sorted(hist.items(), reverse=True):
    print("  ", k, v)
