"""Readable form of the 7-adic drop: CLASS vectors (exploration, LAB 16/10/2026).
Observation (f7_minsupport.py on 8 grid blocks): every clean minimal drop vector is
    3 (e_{a,b'} - e_{a',b}) + 1_{b,E} - 1_{a,O}            (a in {0,1}, b in {2,3}, ' = mate)
where E is a transversal of the 5 outer mate pairs {4,5},...,{12,13}, O = mate(E), and 1_{r,E} = sum of e_{r,s}, s in E.
Here we test, on every PSD four-star block, the CLASS SPACE V_E (dim 12: the 4 corners and the 8 vectors 1_{r,E}, 1_{r,O})
for all 32 transversals E:  K_E = ker_7(8T_S) restricted to V_E.  The class part of the drop is
    dim span(N_7 + sum_E K_E) - nu,   N_7 = reduction mod 7 of the saturated integral kernel.
It is compared with the full drop rank_Q - rank_F7, per (grid?, rank_Q, rank_F7).
usage: python f7_classform.py <root dir> [max structures] [--show N]"""
import collections
import itertools
import json
import os
import sys
import time
from fractions import Fraction

import numpy as np

MATE = lambda i: i ^ 1
OUTER = list(range(4, 14))
PAIRS = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]


def t8(S, E):
    n = len(S)
    M = np.zeros((n, n), dtype=np.int64)
    for i, a in enumerate(S):
        for j, b in enumerate(S):
            s = len(a & b)
            m = sum(1 for p in a for q in b if q == MATE(p))
            M[i, j] = (24 if i == j else 0) - 8 * (1 if frozenset((a, b)) in E else 0) - 3 * s - m + 2
    return M


def rref_mod(rows, p):
    A = [[int(x) % p for x in r] for r in rows]
    if not A:
        return [], []
    nr, nc = len(A), len(A[0])
    piv, r = [], 0
    for c in range(nc):
        k = next((i for i in range(r, nr) if A[i][c]), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return A[:r], piv


def null_mod(M, p):
    R, piv = rref_mod(M, p)
    nc = len(M[0])
    free = [c for c in range(nc) if c not in piv]
    out = []
    for f in free:
        g = [0] * nc
        g[f] = 1
        for i, c in enumerate(piv):
            g[c] = (-R[i][f]) % p
        out.append(g)
    return out


def int_kernel(M):
    """exact integral kernel basis of an integer matrix (rational RREF, then clear denominators)"""
    A = [[Fraction(int(x)) for x in r] for r in M]
    nr, nc = len(A), len(A[0])
    piv, r = [], 0
    for c in range(nc):
        k = next((i for i in range(r, nr) if A[i][c] != 0), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(nc) if c not in piv]
    out = []
    for f in free:
        g = [Fraction(0)] * nc
        g[f] = Fraction(1)
        for i, c in enumerate(piv):
            g[c] = -A[i][f]
        den = 1
        for x in g:
            den = den * x.denominator // np.gcd(den, x.denominator)
        w = [int(x * den) for x in g]
        gg = 0
        for x in w:
            gg = int(np.gcd(gg, abs(x)))
        out.append([x // gg for x in w])
    return out


def saturate7(K):
    K = [list(v) for v in K]
    while K and len(rref_mod(K, 7)[0]) < len(K):
        Mt = [[K[i][j] for i in range(len(K))] for j in range(len(K[0]))]
        c = null_mod(Mt, 7)[0]
        vec = [sum((c[i] if c[i] <= 3 else c[i] - 7) * K[i][j] for i in range(len(K))) for j in range(len(K[0]))]
        i0 = next(i for i in range(len(c)) if c[i])
        K[i0] = [x // 7 for x in vec]
    return K


def grid_square(S, E):
    c = {frozenset(p) for p in ((0, 2), (0, 3), (1, 2), (1, 3))}
    need = [((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))]
    return all(frozenset((frozenset(a), frozenset(b))) in E for a, b in need)


def class_basis(S, Eset):
    """12 vectors: 4 corners, then 1_{r,E}, 1_{r,O} for r = 0..3"""
    idx = {l: i for i, l in enumerate(S)}
    B = []
    for p in ((0, 2), (0, 3), (1, 2), (1, 3)):
        v = [0] * 44
        v[idx[frozenset(p)]] = 1
        B.append(v)
    O = {MATE(s) for s in Eset}
    for r in range(4):
        for cls in (Eset, O):
            v = [0] * 44
            for s in cls:
                v[idx[frozenset((r, s))]] = 1
            B.append(v)
    return B


def analyse(L, E, show=False):
    S = [l for l in L if l & {0, 1, 2, 3}]
    if len(S) != 44:
        return None
    M = t8(S, E)
    ev = np.linalg.eigvalsh(M.astype(float))
    if ev[0] < -1e-6:
        return None
    rq = int(np.sum(ev > 1e-6))
    nu = 44 - rq
    k7 = null_mod(M.tolist(), 7)
    drop = len(k7) - nu
    res = {"rq": rq, "r7": 44 - len(k7), "drop": drop, "gridsq": grid_square(S, E)}
    if drop == 0:
        res["class_drop"] = 0
        res["nE"] = 0
        return res
    N7 = rref_mod(saturate7(int_kernel(M.tolist())), 7)[0]
    assert len(N7) == nu
    span = [list(r) for r in N7]
    goodE = 0
    Mm = M % 7
    for bits in itertools.product((0, 1), repeat=5):
        Eset = {p[b] for p, b in zip(PAIRS, bits)}
        Bc = np.array(class_basis(S, Eset), dtype=np.int64)  # 12 x 44
        W = (Mm @ Bc.T) % 7  # 44 x 12
        sol = null_mod(W.tolist(), 7)  # coefficient vectors c with W c = 0
        if not sol:
            continue
        vecs = [list((np.array(c, dtype=np.int64) @ Bc) % 7) for c in sol]
        before = len(span)
        span = [list(r) for r in rref_mod(span + vecs, 7)[0]]
        if len(span) > before:
            goodE += 1
    res["class_drop"] = len(span) - nu
    res["nE"] = goodE
    return res


if __name__ == "__main__":
    root = sys.argv[1]
    maxs = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else 10 ** 9
    t0 = time.time()
    seen = set()
    agg = collections.Counter()
    bad = []
    n = 0
    for dp, dn, fn in os.walk(root):
        for f in sorted(fn):
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
            agg[("G" if r["gridsq"] else "NG", r["rq"], r["r7"], r["drop"], r["class_drop"])] += 1
            if r["class_drop"] < r["drop"] and len(bad) < 40:
                bad.append((os.path.join(dp, f), r))
    print("PSD structures: %d  (%.0f s)" % (n, time.time() - t0))
    print("(corner square?, rank_Q, rank_F7, drop, class part of the drop): count")
    for k, v in sorted(agg.items()):
        print("  ", k, v)
    print("blocks whose drop is NOT fully class-type (first 40):")
    for p, r in bad:
        print("  ", p.replace("\\", "/").split("stars_rank_2026-10-14/")[-1], r)
