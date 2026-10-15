"""Kernel of fake-symmetric structures (LAB 15/10/2026, task T3, exact).
g = h p with p an involution of the outer letters that does NOT preserve mates (e.g. p = (4 6)).  If Gamma is
g-invariant, then g T g^-1 = T + D with D = K - gKg^-1 FIXED (depends only on p; for p = (4 6) it has rank 2 and
eigenvalues +-1) and T_s = (T + gTg^-1)/2 >= 0 has kernel N n gN; nullity T <= nullity T_s + 1.  Prints, exactly:
nullity T, dim(N n gN), dim(N n hN), rank D, and whether the structure is g-invariant.
usage: python fake_kernel.py <cycles of p, e.g. 4,6> <json> [...]"""
import json, sys
sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int
p = {i: i for i in range(14)}
for c in sys.argv[1].split(";"):
    c = [int(t) for t in c.split(",")]
    for k in range(len(c)):
        p[c[k]] = c[(k + 1) % len(c)]
g = dict(p); g.update({0: 1, 1: 0, 2: 3, 3: 2})
hmap = {i: i for i in range(14)}; hmap.update({0: 1, 1: 0, 2: 3, 3: 2})
def rank_frac(rows):
    from fractions import Fraction as Fr
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    if not A: return 0
    m = len(A[0])
    for c in range(m):
        q = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if q is None: continue
        A[r], A[q] = A[q], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r
for f in sys.argv[2:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    gl = [idx[frozenset(g[y] for y in s)] for s in S]
    hl = [idx[frozenset(hmap[y] for y in s)] for s in S]
    ginv = all((frozenset((S[gl[a]], S[gl[b]])) in E) == (frozenset((S[a], S[b])) in E) for a in range(n) for b in range(a + 1, n))
    K8 = [[int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
    M8 = [[(24 if a == b else 0) - 8 * (1 if frozenset((S[a], S[b])) in E else 0) - K8[a][b] for b in range(n)] for a in range(n)]
    D8 = [[K8[a][b] - K8[gl[a]][gl[b]] for b in range(n)] for a in range(n)]
    N = nullspace_int(M8)
    def inter(perm):
        Np = [[v[perm.index(i)] if False else 0 for i in range(n)] for v in N]
        # image of v under the label permutation: (perm v)[perm[i]] = v[i]
        imgs = []
        for v in N:
            w = [0] * n
            for i in range(n):
                w[perm[i]] = v[i]
            imgs.append(w)
        return len(N) + len(imgs) - rank_frac(N + imgs)
    print("%s: g-invariant %s, nullity %d, dim(N n gN) = %d, dim(N n hN) = %d, rank D = %d"
          % (f, ginv, len(N), inter(gl), inter(hl), rank_frac(D8)))
# g-parity split of N (appended): number of g-even and g-odd kernel vectors
import itertools as _it
def split(f):
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    gl = [idx[frozenset(g[y] for y in s)] for s in S]
    K8 = [[int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
    M8 = [[(24 if a == b else 0) - 8 * (1 if frozenset((S[a], S[b])) in E else 0) - K8[a][b] for b in range(n)] for a in range(n)]
    N = nullspace_int(M8)
    ev, od = [], []
    for v in N:
        w = [0] * n
        for i in range(n):
            w[gl[i]] = v[i]
        ev.append([v[i] + w[i] for i in range(n)])
        od.append([v[i] - w[i] for i in range(n)])
    print("   g-even part of N: dim %d ; g-odd part: dim %d" % (rank_frac(ev), rank_frac(od)))
for f in sys.argv[2:]:
    split(f)
