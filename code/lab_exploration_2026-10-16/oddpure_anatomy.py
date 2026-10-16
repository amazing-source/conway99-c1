"""Margin of ODD-PURE on the data (exploration, LAB 16/10/2026).
Orientation l = {v,0,1}, iota = (2 3).  T44 in the basis U (the 20 labels avoiding 2, 3), P (12 even directions
(e_2a + e_3a)/sqrt2) and R (12 odd directions (e_2a - e_3a)/sqrt2), a in {0, 1, 4..13}.  K = T_UU, C = T_UR, Phi = T_RR.
ODD-PURE (rank D = 9)  <=>  ker(K - C Phi^+ C^t) = ker K  <=>  lambda_max < 1, where lambda_max is the largest generalized
eigenvalue of (C Phi^+ C^t, K) on range(K).  Also prints rank D (D = odd block of F) as a cross-check: delta = 9 - rank D.
Both orientations (the other one uses iota = (0 1), U = labels avoiding 0, 1).
usage: python oddpure_margin.py <root dir>"""
import collections
import itertools
import json
import os
import sys

import numpy as np

MATE = lambda i: i ^ 1


def kval(a, b):
    s = len(a & b)
    m = sum(1 for p in a for q in b if q == MATE(p))
    return (3 * s + m - 2) / 8.0


def analyse(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
    idx = {l: i for i, l in enumerate(S)}
    G = np.zeros((44, 44))
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            G[idx[a], idx[b]] = G[idx[b], idx[a]] = 1
    T = 3 * np.eye(44) - G - np.array([[kval(a, b) for b in S] for a in S])
    et = np.linalg.eigvalsh(T)
    if et[0] < -1e-8:
        return None
    out = []
    for (r1, r2), (p1, p2) in (((2, 3), (0, 1)), ((0, 1), (2, 3))):
        U = [l for l in S if not (l & {r1, r2})]
        others = [a for a in range(14) if a not in (r1, r2)]
        pairs = [(frozenset((r1, a)), frozenset((r2, a))) for a in others if frozenset((r1, a)) in idx]
        n = 44
        B = np.zeros((n, n))
        col = 0
        for l in U:
            B[idx[l], col] = 1
            col += 1
        for x, y in pairs:                       # even
            B[idx[x], col] = B[idx[y], col] = 1 / np.sqrt(2)
            col += 1
        nP = len(pairs)
        for x, y in pairs:                       # odd
            B[idx[x], col] = 1 / np.sqrt(2)
            B[idx[y], col] = -1 / np.sqrt(2)
            col += 1
        assert col == n and np.allclose(B.T @ B, np.eye(n))
        Tb = B.T @ T @ B
        nU = len(U)
        K = Tb[:nU, :nU]
        C = Tb[:nU, nU + nP:]
        Phi = Tb[nU + nP:, nU + nP:]
        ep, Vp = np.linalg.eigh(Phi)
        Phip = (Vp[:, ep > 1e-9] / ep[ep > 1e-9]) @ Vp[:, ep > 1e-9].T
        M = C @ Phip @ C.T
        ek, Vk = np.linalg.eigh(K)
        rng = Vk[:, ek > 1e-9]
        Kh = rng / np.sqrt(ek[ek > 1e-9])        # K^{+1/2} on range(K)
        Mr = Kh.T @ M @ Kh
        emr, Vmr = np.linalg.eigh(Mr)
        lam = float(emr[-1]) if Mr.size else 0.0
        uu = Kh @ Vmr[:, -1]
        # mirror under the other swap (p1 p2) restricted to U: label {p1,s} <-> {p2,s}
        pos = {l: i for i, l in enumerate(U)}
        mir = np.zeros_like(uu)
        for i, l in enumerate(U):
            img = frozenset(p2 if t == p1 else p1 if t == p2 else t for t in l)
            mir[pos[img]] = uu[i]
        odd_other = float(np.dot(uu, mir) / np.dot(uu, uu))
        rankK = int(np.sum(ek > 1e-9))
        K1 = K - M
        rankK1 = int(np.sum(np.linalg.eigvalsh(K1) > 1e-8))
        out.append({"lam": lam, "delta": rankK - rankK1, "rankK": rankK, "odd_other": odd_other})
    return out


root = sys.argv[1]
seen = set()
hist = collections.Counter()
worst = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(dp, f)))
            L = [frozenset(x) for x in d["labels"]]
            E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
        except Exception:
            continue
        key = frozenset(E)
        if key in seen:
            continue
        seen.add(key)
        r = analyse(L, E)
        if r is None:
            continue
        for s in r:
            hist[(s["delta"], round(s["lam"], 2))] += 1
            worst.append((s["lam"], s["delta"], round(s["odd_other"], 3), os.path.join(dp, f)))
worst.sort(reverse=True)
print("(delta = 9 - rank D, lambda_max rounded): counts")
for k, v in sorted(hist.items()):
    print("  ", k, v)
top = [w for w in worst if w[1] == 0][:25]
print("top near-saturations (lambda, delta, <u, mirror u>/<u,u> under the other swap, file):")
for w in top:
    print("  ", round(w[0], 6), w[1], w[2], os.path.basename(w[3]))
import collections as _c
print("odd_other histogram for lambda >= 0.99:", _c.Counter(round(w[2], 1) for w in worst if w[1] == 0 and w[0] >= 0.99))
print("sides with delta > 0:", sum(1 for w in worst if w[1] > 0))
