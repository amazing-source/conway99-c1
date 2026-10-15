"""Targeted walk on BROKEN structures driven by their h-average (LAB 15/10/2026, task T3, case rank A = 10).

A PSD broken structure of nullity 14 with rank A = 10 needs: average blocks T_0 = (T + hTh)/2, U_0 >= 0 (A, C, A', C'
PSD), rank A = 10, and the mixed block B small enough: tT, tU >= 1 (scale factors as in kernel_sat_measure.py).
Walk (identity group, local SAT re-solves of NFREE labels) on structures whose star matchings are NOT h-related,
score = -3 (rank A - 10)+ - 4 [average blocks not PSD] + 2 min(1, tT, tU) + (nullity bonus), Metropolis.
Reports records of min(tT, tU) at rank A = 10 with PSD average blocks, and any PSD broken structure of nullity >= 14.
usage: python avgwalk.py <start json (labels, edges)> <out prefix> <seconds> [nfree] [temp] [seed]"""
import itertools
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS

startf, out, maxsec = sys.argv[1], sys.argv[2], float(sys.argv[3])
nfree = int(sys.argv[4]) if len(sys.argv) > 4 else 6
temp = float(sys.argv[5]) if len(sys.argv) > 5 else 0.3
rs = int(sys.argv[6]) if len(sys.argv) > 6 else 1
rng = random.Random(rs)
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
sol = Solver(options={"polar": "rnd", "seed": str(rs)})
for c in F.clauses:
    sol.add_clause(c)
Kf = np.array([[kval(a, b) for b in S] for a in S])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
P7 = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
H = np.zeros((n, n))
for i in range(n):
    H[hp[i], i] = 1
Qp = np.linalg.svd((np.eye(n) + H) / 2)[0][:, :22]
Qm = np.linalg.svd((np.eye(n) - H) / 2)[0][:, :22]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
pairs = list(itertools.combinations(range(n), 2))


def root(X):
    w, V = np.linalg.eigh((X + X.T) / 2)
    if w[0] < -1e-8:
        return None, None
    keep = w > 1e-8
    return V[:, keep] / np.sqrt(w[keep]), V[:, ~keep]


def scale(Ab, Bb, Cb):
    Ra, Na = root(Ab)
    Rc, Nc = root(Cb)
    if Ra is None or Rc is None:
        return 0.0
    if Na.shape[1] and np.abs(Bb.T @ Na).max() > 1e-8:
        return 0.0
    if Nc.shape[1] and np.abs(Bb @ Nc).max() > 1e-8:
        return 0.0
    s = np.linalg.norm(Ra.T @ Bb @ Rc, 2)
    return 99.0 if s < 1e-12 else 1.0 / s


def evaluate(G):
    T = 3 * np.eye(n) - G - Kf
    U = P7 - T
    A, B, C = Qp.T @ T @ Qp, Qp.T @ T @ Qm, Qm.T @ T @ Qm
    A2, C2 = Qp.T @ U @ Qp, Qm.T @ U @ Qm
    rkA = int(np.sum(np.abs(np.linalg.eigvalsh(A)) > 1e-8))
    blocks_psd = min(np.linalg.eigvalsh(X)[0] for X in (A, C, A2, C2)) > -1e-8
    tT, tU = scale(A, B, C), scale(A2, -B, C2)
    broken = any(G[i, j] != G[hp[i], hp[j]] for (i, j) in sl)
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ U @ Pp + 50 * (np.eye(n) - Pp))[0])
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    return dict(rkA=rkA, blocks=blocks_psd, tT=tT, tU=tU, broken=broken, psd=min(lt, lu) > -1e-9, nul=nul)


def score(r):
    if not r["broken"]:
        return -50.0
    return (-3.0 * max(0, r["rkA"] - 10) - (0 if r["blocks"] else 4.0) + 2.0 * min(1.0, r["tT"], r["tU"])
            + 0.5 * min(r["nul"], 14))


d = json.load(open(startf))
assert [sorted(l) for l in S] == d["labels"]
G = np.zeros((n, n))
for i, j in d["edges"]:
    G[i, j] = G[j, i] = 1
cur_r = evaluate(G)
cur = score(cur_r)
print("start:", cur_r, "score %.3f" % cur, flush=True)
best = -1.0
t0 = time.time()
mv = 0
hits = 0
while time.time() - t0 < maxsec:
    mv += 1
    R = set(rng.sample(range(n), nfree))
    assum = [e[p] if G[p] else -e[p] for p in pairs if p[0] not in R and p[1] not in R]
    ok, m2 = sol.solve(assum)
    if not ok:
        continue
    G2 = np.zeros((n, n))
    for p in pairs:
        if m2[e[p]]:
            G2[p] = 1
            G2[p[1], p[0]] = 1
    r = evaluate(G2)
    if r["broken"] and r["rkA"] == 10 and r["blocks"]:
        mt = min(r["tT"], r["tU"])
        if mt > best + 1e-6:
            best = mt
            print("move %d: record min(tT, tU) = %.4f at rank A = 10 with PSD average blocks (nullity %d, PSD %s), %.0f s"
                  % (mv, mt, r["nul"], r["psd"], time.time() - t0), flush=True)
    if r["broken"] and r["psd"] and r["nul"] >= 14:
        hits += 1
        json.dump({"labels": d["labels"], "edges": [[i, j] for i, j in pairs if G2[i, j]], "eval": r},
                  open("%s_HIT_%d.json" % (out, hits), "w"))
        print("move %d: AVGWALK TARGET HIT: PSD broken structure of nullity %d" % (mv, r["nul"]), flush=True)
    s2 = score(r)
    if s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
        G, cur, cur_r = G2, s2, r
    if mv % 300 == 0:
        print("move %d: %.0f s, current %s, best min(tT,tU) %.4f" % (mv, time.time() - t0, cur_r, best), flush=True)
print("end: %d moves, best min(tT, tU) at rank A = 10 with PSD average blocks: %.4f, hits %d" % (mv, best, hits), flush=True)
