"""For every family found by the stage-1 search (irregular kept set inside block 0), the graph induced on the 81 block
vertices: is it again the folded Hamming graph X = H(5,3)/<11111>? If yes, NOTE_SPREADFREE 6j + 6h apply (attachments
forced, completions = the seven known graphs). Invariants first (degrees, triangles, common-neighbour profile), then an
exact isomorphism test with plain 2-dim WL + individualisation (pairgroup243 tools), every map checked edge by edge.
usage: python irregular_blocks.py <edge file> <size> <seed> <cap>   (environment PYLIB)"""
import itertools
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pairgroup243 as PG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T
import boundary_census as BC

path, size, seed, cap = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
A = T.load(path)
n = len(A)
adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
rng = random.Random(seed)
R = sorted(rng.sample(range(81), size))
Rs = set(R)
F = [v for v in range(n) if v not in Rs]
freed = [v for v in range(81) if v not in Rs]
rows = {f: [frozenset(N) for N in BC.rows_of(adj, R, Rs, F, f, cap)] for f in freed}
own = {f: frozenset(adj[f] - Rs) for f in freed}


def compatible(f, Nf, g, Ng):
    if (g in Nf) != (f in Ng):
        return False
    need = (1 if g in Nf else 2) - len(adj[f] & adj[g] & Rs)
    return len(Nf & Ng) == need


order = sorted(freed, key=lambda f: len(rows[f]))
fams = []


def rec(i, pick, dom):
    if i == len(order):
        fams.append(dict(pick))
        return
    f = order[i]
    for c in dom[f]:
        Nf = rows[f][c]
        newdom = {}
        ok = True
        for g in order[i + 1:]:
            d = [e for e in dom[g] if compatible(f, Nf, g, rows[g][e])]
            if not d:
                ok = False
                break
            newdom[g] = d
        if ok:
            pick[f] = Nf
            rec(i + 1, pick, {**dom, **newdom})
            del pick[f]


rec(0, {}, {f: list(range(len(rows[f]))) for f in freed})


def block_graph(pick):
    B = np.zeros((81, 81), dtype=np.int64)
    for u in range(81):
        for w in range(81):
            if u == w:
                continue
            if u in Rs or w in Rs:
                B[u, w] = A[u, w]                     # kept pair (R x everything)
            else:
                B[u, w] = 1 if w in pick[u] else 0    # both freed: the chosen rows
    assert (B == B.T).all()
    return B


def stats(B):
    deg = tuple(sorted(B.sum(1).tolist()))
    tri = int(np.trace(B @ B @ B)) // 6
    C = B @ B
    prof = {}
    for u in range(81):
        for w in range(u + 1, 81):
            key = (int(B[u, w]), int(C[u, w]))
            prof[key] = prof.get(key, 0) + 1
    return deg[0], deg[-1], tri, dict(sorted(prof.items()))


def iso(B1, B2):
    """exact isomorphism test between two graphs on 81 vertices: individualisation-refinement on the disjoint
    union is avoided; instead search a map with plain refinement on each graph separately (colours compared)."""
    n1 = len(B1)
    init1 = B1 + 2 * np.eye(n1, dtype=np.int64)
    init2 = B2 + 2 * np.eye(n1, dtype=np.int64)
    C1, C2 = T.wl2([B1, B2], [init1, init2])
    col1, col2 = np.diag(C1).copy(), np.diag(C2).copy()
    if not np.array_equal(np.sort(col1), np.sort(col2)):
        return None

    def rec2(c1, c2):
        r = T.refine2(B1, c1, B2, c2)
        if r is None:
            return None
        c1, c2 = r
        cnt = np.bincount(c1)
        if len(cnt) == n1:
            inv = np.empty(n1, dtype=np.int64)
            inv[c2] = np.arange(n1)
            f = inv[c1]
            return f.tolist() if np.array_equal(B1, B2[np.ix_(f, f)]) else None
        big = np.nonzero(cnt > 1)[0]
        c = big[np.argmin(cnt[big])]
        x = int(np.nonzero(c1 == c)[0][0])
        for y in np.nonzero(c2 == c)[0]:
            a1, a2 = T.joint(c1, C1[x], c2, C2[int(y)])
            f = rec2(a1, a2)
            if f is not None:
                return f
        return None
    return rec2(col1, col2)


X = block_graph({f: own[f] for f in freed})
sx = stats(X)
print("input block: min/max degree %d/%d, triangles %d, pair profile (adjacent, common neighbours) %s" % sx, flush=True)
for p in fams:
    ch = [f for f in freed if p[f] != own[f]]
    if not ch:
        continue
    Bp = block_graph(p)
    s = stats(Bp)
    same = s == sx
    f = iso(Bp, X) if same else None
    print("family changing %2d vertices: invariants %s; isomorphic to the folded Hamming block: %s"
          % (len(ch), "equal" if same else "DIFFERENT %s" % (s,), f is not None), flush=True)
