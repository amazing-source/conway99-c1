"""Enumerate ALL admissible four-star structures whose kernel contains the kernel N of a given structure (LAB 15/10/2026).
Same linear model as kernel_milp.py (C1, C1', 8 Gamma n = 8 (3I - K) n for n in N, lazy C2 cuts), feasibility MILP
with no-good cuts on the 946 edge variables, until infeasible (COMPLETE) or the cap.  For each structure: numerical
nullity, PSD (T and U on the complement of the star vectors), star-matching asymmetry (pairs), full h-asymmetry.
DROP=k drops the last k vectors of the exact kernel basis (weaker condition, larger set).
usage: python kernel_enum.py <structure json> [max structures] [time limit s]"""
import itertools
import json
import os
import sys
import time
from collections import Counter

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

from stars_rank import kval, count_needed, LABELS
from cls_decomp import nullspace_int

f = sys.argv[1]
cap = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
tlim = float(sys.argv[3]) if len(sys.argv) > 3 else 1200
d = json.load(open(f))
S = [frozenset(l) for l in d["labels"]]
n = len(S)
idx = {s: i for i, s in enumerate(S)}
E0 = {tuple(sorted(e)) for e in d["edges"]}
K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
Kf = np.array([[kval(a, b) for b in S] for a in S])
G0 = [[1 if tuple(sorted((a, b))) in E0 else 0 for b in range(n)] for a in range(n)]
M = [[(24 if a == b else 0) - 8 * G0[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
N = nullspace_int(M)
drop = int(os.environ.get("DROP", "0"))
if drop:
    N = N[:len(N) - drop]
if os.environ.get("DROPIDX"):                 # drop the listed basis vectors (comma-separated indices)
    dd = {int(t) for t in os.environ["DROPIDX"].split(",")}
    N = [v for q, v in enumerate(N) if q not in dd]
print("%s: kernel basis used: %d vectors" % (f, len(N)), flush=True)
pairs = list(itertools.combinations(range(n), 2))
pid = {p: t for t, p in enumerate(pairs)}
P = len(pairs)
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
sl = [p for p in pairs if S[p[0]] & S[p[1]] & {0, 1, 2, 3}]
rows, lo, hi = [], [], []


def add(co, l, u):
    rows.append(co)
    lo.append(l)
    hi.append(u)


def e(i, j):
    return pid[(min(i, j), max(i, j))]


for i in range(n):
    for y in range(14):
        lits = [e(i, t) for t in range(n) if t != i and y in S[t]]
        if not lits:
            continue
        c = count_needed(S[i], y)
        add({v: 1 for v in lits}, c if y < 4 else 0, c)
for vec in N:
    for i in range(n):
        rhs = sum((24 if i == j else 0) * vec[j] - K8[i][j] * vec[j] for j in range(n))
        co = {e(i, j): 8 * vec[j] for j in range(n) if j != i and vec[j]}
        if co:
            add(co, rhs, rhs)
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
t0 = time.time()
found = 0
hist = Counter()
complete = False
best = None
while found < cap and time.time() - t0 < tlim:
    A = lil_matrix((len(rows), P))
    for r, co in enumerate(rows):
        for v, c in co.items():
            A[r, v] = c
    res = milp(np.zeros(P), constraints=LinearConstraint(A.tocsr(), np.array(lo, float), np.array(hi, float)),
               integrality=np.ones(P), bounds=Bounds(0, 1), options={"time_limit": max(10.0, tlim - (time.time() - t0))})
    if res.x is None:
        complete = res.status == 2
        print("MILP status %d: %s" % (res.status, res.message), flush=True)
        break
    x = np.rint(res.x).astype(int)
    G = np.zeros((n, n), dtype=int)
    for (i, j), t in pid.items():
        if x[t]:
            G[i, j] = G[j, i] = 1
    viol = False
    for i, j in pairs:
        s_ = len(S[i] & S[j])
        com = [t for t in range(n) if t != i and t != j and G[i, t] and G[j, t]]
        if G[i, j] and len(com) > 1 - s_:
            Cp = com[:2 - s_]
            co = {e(i, j): 1}
            for t in Cp:
                co[e(i, t)] = co.get(e(i, t), 0) + 1
                co[e(j, t)] = co.get(e(j, t), 0) + 1
            add(co, -np.inf, 2 * len(Cp))
            viol = True
        elif not G[i, j] and len(com) > 2 - s_:
            Cp = com[:3 - s_]
            co = {e(i, j): -1}
            for t in Cp:
                co[e(i, t)] = co.get(e(i, t), 0) + 1
                co[e(j, t)] = co.get(e(j, t), 0) + 1
            add(co, -np.inf, 2 * len(Cp) - 1)
            viol = True
    if viol:
        continue
    found += 1
    # no-good cut
    add({t: (-1 if x[t] else 1) for t in range(P)}, 1 - int(x.sum()), np.inf)
    T = 3 * np.eye(n) - G - Kf
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
    psd = min(lt, lu) > -1e-9
    masym = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
    hasym = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
    hist[(psd, nul, masym > 0, hasym > 0)] += 1
    if found % 50 == 0:
        print("progress: %d structures, %.0f s, %s" % (found, time.time() - t0, dict(hist)), flush=True)
    if nul >= 14 and masym > 0 and psd:
        out = os.path.basename(f).replace(".json", "") + "_KE_%d.json" % found
        json.dump({"labels": d["labels"], "edges": [[i, j] for i, j in pairs if G[i, j]], "psd": psd, "masym": masym,
                   "nullity_numeric": nul}, open(out, "w"))
        print("KERNEL-ENUM TARGET: nullity %d, matchings broken (%d), PSD %s, saved %s" % (nul, masym, psd, out),
              flush=True)
print("%d structures (%s), %.0f s" % (found, "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
print("(PSD, nullity, matchings broken, h broken): count")
for k, v in sorted(hist.items(), reverse=True):
    print("  ", k, v)
