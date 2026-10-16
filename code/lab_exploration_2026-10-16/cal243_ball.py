"""Calibration of the four-star dictionary on the four KNOWN srg(243,22,1,2) (exploration, LAB 16/10/2026 night).
Analogue of Conway's (3, -4, p = 7): here eigenvalues 4 and -5, 4 - (-5) = 9, p = 3.  For a vertex v and a pair of lines
(l, m) at v, W = N[v] u N(l) u N(m) is the four-star ball (1 + 22 + 76 = 99 vertices).  Positivity transfer holds as in
Conway: every 4-eigenvector of A_W is a global 4-eigenvector (Schur complement T' >= 0), every -5-eigenvector of A_W is
a global -5-eigenvector (A + 5I >= 0).  Per pair we record
  n4  = dim ker_Q(A_W - 4I)                 rational 4-eigenvectors carried by the ball
  n5  = dim ker_Q(A_W + 5I)                 rational -5-eigenvectors carried by the ball
  b5  = those -5-eigenvectors that vanish on N[v]   (Conway's b)
  nF3 = dim ker_F3(A_W - 4I)                mod-3 kernel (4 = -5 = 1 mod 3)
  glue = nF3 - n4 - n5                     (7-adic sigma of Conway, here 3-adic)
and the global forced bound dim(ker_F3(A - 4I) restricted to W) >= (243 - rank_F3(A - 4I)) - 144.
usage: python cal243_ball.py <edges file> [max vertices]"""
import collections
import itertools
import sys

import numpy as np

P1, P2 = 1000003, 999983


def rank_np(M, p):
    A = np.array(M, dtype=np.int64) % p
    n, m = A.shape
    r = 0
    for c in range(m):
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0:
            continue
        piv = r + nz[0]
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r, c]), p - 2, p)) % p
        col = A[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if nzr.size:
            A[nzr] = (A[nzr] - np.outer(col[nzr], A[r]) % p) % p
        r += 1
        if r == n:
            break
    return r


def rank_q(M):
    a, b = rank_np(M, P1), rank_np(M, P2)
    return max(a, b), a == b


path = sys.argv[1]
maxv = int(sys.argv[2]) if len(sys.argv) > 2 else 4
n = 243
A = np.zeros((n, n), dtype=np.int64)
for line in open(path):
    if line.strip():
        i, j = map(int, line.split())
        A[i, j] = A[j, i] = 1
adj = [set(np.nonzero(A[i])[0].tolist()) for i in range(n)]
R3 = rank_np(A - 4 * np.eye(n, dtype=np.int64), 3)
print("%s: rank_F3(A - 4I) = %d, dim ker_F3 = %d, forced on a 99-ball >= %d" % (path.split("/")[-1], R3, n - R3,
                                                                             (n - R3) - 144))


def lines_at(v):
    out, seen = [], set()
    for a in sorted(adj[v]):
        if a in seen:
            continue
        b = next(iter(adj[a] & adj[v]))
        seen |= {a, b}
        out.append((a, b))
    return out


def corner(x, y, v):
    c = (adj[x] & adj[y]) - {v}
    return next(iter(c))


def is_grid(v, l, m):
    (a, a2), (b, b2) = l, m
    w = {(p, q): corner(p, q, v) for p in (a, a2) for q in (b, b2)}
    need = [((a, b), (a, b2)), ((a2, b), (a2, b2)), ((a, b), (a2, b)), ((a, b2), (a2, b2))]
    return all(w[q] in adj[w[p]] for p, q in need)


# vertex representatives by grid count
gc = {}
for v in range(n):
    L = lines_at(v)
    gc[v] = sum(is_grid(v, l, m) for l, m in itertools.combinations(L, 2))
reps = {}
for v in range(n):
    reps.setdefault(gc[v], v)
print("grid pairs per vertex (of 55):", dict(collections.Counter(gc.values())))
bad = 0
for g, v in sorted(reps.items())[:maxv]:
    L = lines_at(v)
    agg = collections.Counter()
    for l, m in itertools.combinations(L, 2):
        W = sorted({v} | adj[v] | adj[l[0]] | adj[l[1]] | adj[m[0]] | adj[m[1]])
        assert len(W) == 99
        AW = A[np.ix_(W, W)]
        I = np.eye(99, dtype=np.int64)
        r4, ok4 = rank_q(AW - 4 * I)
        r5, ok5 = rank_q(AW + 5 * I)
        Nv = [W.index(u) for u in ({v} | adj[v])]
        Ez = np.zeros((len(Nv), 99), dtype=np.int64)
        for t, c in enumerate(Nv):
            Ez[t, c] = 1
        rb, okb = rank_q(np.vstack([AW + 5 * I, Ez]))
        rf = rank_np(AW - 4 * I, 3)
        bad += 0 if (ok4 and ok5 and okb) else 1
        n4, n5, b5, nf = 99 - r4, 99 - r5, 99 - rb, 99 - rf
        agg[("grid" if is_grid(v, l, m) else "non-grid", n4, n5, b5, nf, nf - n4 - n5)] += 1
    print(" vertex %d (%d grid pairs): (pair, n4, n5, b5, nF3, glue): count" % (v, g))
    for k, c in sorted(agg.items()):
        print("    ", k, c)
print("prime disagreements:", bad)
