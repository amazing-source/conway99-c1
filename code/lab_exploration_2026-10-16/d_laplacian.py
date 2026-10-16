"""Is the odd-odd block D of F a weighted graph Laplacian?  (exploration, LAB 16/10/2026)
F = Q + J/12 (Codex: PSD, F1 = 0, ker F = profiles).  With R g = (g, -g) on Y = (2s | 3s), s = 4..13:
D = R^T F R = F_22 - F_23 - F_32 + F_33 (10 x 10), D 1 = 0.  If every off-diagonal entry of D is <= 0, D is a weighted
Laplacian and rank D = 10 - (number of components of its weighted graph).
Prints, per PSD structure and side: max off-diagonal entry, rank D, number of components of the graph of negative
off-diagonal entries, grid flag.  Aggregates over a directory.
usage: python d_laplacian.py <root dir> [max structures]"""
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
    verts = ["v"] + [("L", s) for s in range(14)] + S
    pos = {x: i for i, x in enumerate(verts)}
    n = len(verts)
    A = np.zeros((n, n))
    for s in range(14):
        A[pos["v"], pos[("L", s)]] = A[pos[("L", s)], pos["v"]] = 1
        A[pos[("L", s)], pos[("L", MATE(s))]] = 1
    for l in S:
        for s in l:
            A[pos[l], pos[("L", s)]] = A[pos[("L", s)], pos[l]] = 1
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    iS = [pos[l] for l in S]
    T = 3 * np.eye(44) - A[np.ix_(iS, iS)] - np.array([[kval(a, b) for b in S] for a in S])
    if np.linalg.eigvalsh(T)[0] < -1e-8:
        return None
    out = []
    for (p, q), (r1, r2) in (((0, 1), (2, 3)), ((2, 3), (0, 1))):
        Nset = [("L", s) for s in range(14) if s not in (p, q)] + [l for l in S if l & {p, q}]
        cols = [s for s in range(14) if s not in (0, 1, 2, 3)]
        Yset = [frozenset((r1, s)) for s in cols] + [frozenset((r2, s)) for s in cols]
        iN = [pos[x] for x in Nset]
        iY = [pos[x] for x in Yset]
        ev, V = np.linalg.eigh(3 * np.eye(36) - A[np.ix_(iN, iN)])
        inv = (V[:, ev > 1e-9] / ev[ev > 1e-9]) @ V[:, ev > 1e-9].T
        AYN = A[np.ix_(iY, iN)]
        Q = 3 * np.eye(20) - A[np.ix_(iY, iY)] - AYN @ inv @ AYN.T
        F = Q + np.ones((20, 20)) / 12.0
        D = F[:10, :10] - F[:10, 10:] - F[10:, :10] + F[10:, 10:]
        off = D - np.diag(np.diag(D))
        mx = off.max()
        sv = np.linalg.eigvalsh(D)
        rk = int(np.sum(sv > 1e-7))
        # components of the graph of strictly negative off-diagonal entries
        adj = off < -1e-9
        seen, comps = set(), 0
        for i in range(10):
            if i in seen:
                continue
            comps += 1
            st = [i]
            seen.add(i)
            while st:
                u = st.pop()
                for w in range(10):
                    if adj[u, w] and w not in seen:
                        seen.add(w)
                        st.append(w)
        null = V[:, ev < 1e-9]
        i0 = Nset.index(("L", r1))
        same = [j for j in range(36) if np.allclose(null[j], null[i0], atol=1e-8)]
        out.append({"max_off": mx, "rankD": rk, "comps": comps, "rowsum": float(np.abs(D.sum(1)).max()),
                    "grid": len(same) == 6})
    g = out[0]["grid"] or out[1]["grid"]
    for r in out:
        r["grid"] = g
    return out


root = sys.argv[1]
maxs = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
agg = collections.Counter()
worst = {}
seen = set()
nst = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".json") or nst >= maxs:
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
        rs = analyse(L, E)
        if rs is None:
            continue
        nst += 1
        for r in rs:
            tag = "G" if r["grid"] else "NG"
            lap = r["max_off"] <= 1e-9
            agg[(tag, "laplacian" if lap else "not-laplacian", r["rankD"], r["comps"])] += 1
            if tag not in worst or r["max_off"] > worst[tag][0]:
                worst[tag] = (r["max_off"], os.path.join(dp, f))
print("PSD structures:", nst)
for k, v in sorted(agg.items()):
    print("  ", k, v)
print("largest off-diagonal entry of D:", worst)
