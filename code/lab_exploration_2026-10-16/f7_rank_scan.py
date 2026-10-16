"""Arithmetic measure on the four-star blocks (exploration, LAB 16/10/2026).
For each PSD structure: rank over Q of 8T_S (= 44 - nu), rank over F_7, F_3, F_5, grid flag, c(l), c(m).
In a Conway graph rank_F7(8T_S) <= rank_F7(8T) <= 28 (global F7 bound L4/L23/L22, LAB 14/10, accepted by Codex) while
rank_Q <= 30.  Question: is there a sharp ARITHMETIC law on the non-grid blocks (e.g. rank_F7 >= 29 whenever min c <= 4)?
usage: python f7_rank_scan.py <root dir> [max structures]"""
import collections
import itertools
import json
import os
import sys

import numpy as np

MATE = lambda i: i ^ 1


def rank_mod(M, p):
    A = np.array(M, dtype=np.int64) % p
    n, m = A.shape
    r = 0
    for c in range(m):
        piv = None
        for i in range(r, n):
            if A[i, c]:
                piv = i
                break
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        col = A[:, c].copy()
        col[r] = 0
        nz = np.nonzero(col)[0]
        if nz.size:
            A[nz] = (A[nz] - np.outer(col[nz], A[r])) % p
        r += 1
        if r == n:
            break
    return r


def analyse(L, E):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
    idx = {l: i for i, l in enumerate(S)}
    G = np.zeros((44, 44), dtype=np.int64)
    for a, b in itertools.combinations(S, 2):
        if frozenset((a, b)) in E:
            G[idx[a], idx[b]] = G[idx[b], idx[a]] = 1
    T8 = np.zeros((44, 44), dtype=np.int64)
    for i, a in enumerate(S):
        for j, b in enumerate(S):
            s = len(a & b)
            m = sum(1 for p in a for q in b if q == MATE(p))
            T8[i, j] = (24 if i == j else 0) - 8 * G[i, j] - 3 * s - m + 2
    ev = np.linalg.eigvalsh(T8.astype(float))
    if ev[0] < -1e-6:
        return None
    rq = int(np.sum(ev > 1e-6))
    # line components and grid flag (as in q_scan.py)
    def comps(p, q):
        verts = [("L", s) for s in range(14) if s not in (p, q)] + [l for l in S if l & {p, q}]
        adj = {x: set() for x in verts}
        for s in range(14):
            if s in (p, q):
                continue
            adj[("L", s)].add(("L", MATE(s)))
            for r in (p, q):
                lab = frozenset((r, s))
                adj[("L", s)].add(lab)
                adj[lab].add(("L", s))
        labs = [x for x in verts if not isinstance(x, tuple)]
        for x, y in itertools.combinations(labs, 2):
            if frozenset((x, y)) in E:
                adj[x].add(y)
                adj[y].add(x)
        seen, cs = set(), []
        for x in verts:
            if x in seen:
                continue
            st, comp = [x], set()
            seen.add(x)
            while st:
                u = st.pop()
                comp.add(u)
                for w in adj[u]:
                    if w not in seen:
                        seen.add(w)
                        st.append(w)
            cs.append(comp)
        return cs
    cl, cm = comps(0, 1), comps(2, 3)
    grid = any(len(c) == 6 and ("L", 2) in c for c in cl)
    return {"rq": rq, "r7": rank_mod(T8, 7), "r3": rank_mod(T8, 3), "r5": rank_mod(T8, 5), "grid": grid,
            "c": (len(cl), len(cm))}


root = sys.argv[1]
maxs = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
seen = set()
agg = collections.Counter()
n = 0
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".json") or n >= maxs:
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
        n += 1
        cmin = min(r["c"])
        agg[("G" if r["grid"] else "NG", "cmin<=4" if cmin <= 4 else "cmin>=5", r["rq"], r["r7"])] += 1
print("PSD structures:", n)
print("(grid?, min c, rank_Q, rank_F7): count")
for k, v in sorted(agg.items()):
    print("  ", k, v)
ng = [(k, v) for k, v in agg.items() if k[0] == "NG" and k[1] == "cmin<=4"]
print("non-grid, min c <= 4: min rank_F7 =", min(k[3] for k, v in ng) if ng else None,
      "; with rank_F7 <= 28:", sum(v for k, v in ng if k[3] <= 28))
