"""Exact automorphism group order and vertex orbits of a graph given as an edge list, for any strongly regular graph
(plain 2-dim Weisfeiler-Leman initial colours, no assumption on mu), and pairwise isomorphism between several graphs.
Reuses the refinement and search of work/asym_paley_2026-10-14 (pairgroup243.py / firstorder.py); every map found is
checked edge by edge. (14/10/2026)
usage: python srg_group.py file1.edges [file2.edges ...]"""
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "asym_paley_2026-10-14"))
sys.path.insert(0, os.path.join(HERE, "..", "spreadfree_243_2026-10-12"))
import firstorder as FO
import pairgroup243 as PG
import aut_tools as T


def load(path):
    E = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
    n = 1 + max(max(e) for e in E)
    A = np.zeros((n, n), dtype=np.int64)
    for a, b in E:
        A[a, b] = A[b, a] = 1
    return A


def params(A):
    n = len(A)
    k = set(A.sum(1).tolist())
    C = A @ A
    lam = set(C[A == 1].tolist())
    off = (A == 0) & ~np.eye(n, dtype=bool)
    mu = set(C[off].tolist())
    return n, k, lam, mu


def iso(A1, A2):
    n = len(A1)
    if len(A2) != n:
        return None
    C1, C2 = T.wl2([A1, A2], [A1 + 2 * np.eye(n, dtype=np.int64), A2 + 2 * np.eye(n, dtype=np.int64)])
    c1, c2 = np.diag(C1).copy(), np.diag(C2).copy()
    if not np.array_equal(np.sort(c1), np.sort(c2)):
        return None

    def rec(c1, c2):
        r = T.refine2(A1, c1, A2, c2)
        if r is None:
            return None
        c1, c2 = r
        cnt = np.bincount(c1)
        if len(cnt) == n:
            inv = np.empty(n, dtype=np.int64)
            inv[c2] = np.arange(n)
            f = inv[c1]
            return f.tolist() if np.array_equal(A1, A2[np.ix_(f, f)]) else None
        big = np.nonzero(cnt > 1)[0]
        c = big[np.argmin(cnt[big])]
        x = int(np.nonzero(c1 == c)[0][0])
        for y in np.nonzero(c2 == c)[0]:
            a1, a2 = T.joint(c1, C1[x], c2, C2[int(y)])
            f = rec(a1, a2)
            if f is not None:
                return f
        return None
    return rec(c1, c2)


if __name__ == "__main__":
    As = []
    for p in sys.argv[1:]:
        A = load(p)
        t = time.time()
        o, gens = FO.group_plain([A])
        orbs = T.vertex_orbits(len(A), gens)
        print("%s: params %s; |Aut| = %d; vertex orbits %s (%.0f s)"
              % (os.path.basename(p), params(A), o, sorted(len(x) for x in orbs), time.time() - t), flush=True)
        As.append((os.path.basename(p), A))
    for i in range(len(As)):
        for j in range(i + 1, len(As)):
            print("%s ~ %s: %s" % (As[i][0], As[j][0], iso(As[i][1], As[j][1]) is not None), flush=True)
