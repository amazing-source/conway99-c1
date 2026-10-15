"""Profile of PSD structures under a true symmetry g (LAB 15/10/2026, task T3, exact).
For each structure: nullity, c(l), c(m) (components of H_l, H_m), t(l), t(m), side relations count
(1 + c(l)) + (1 + c(m)) - (side relations supported on X_l n X_m), mixed = nullity - side, g-profile (dimensions of the
g-even and g-odd parts of ker T, g = h p), and whether every g-odd kernel vector has zero m-even outer coordinates
(hypothesis (H_g) of the absorption lemma, note H_MATCH 6h) and zero l-even outer coordinates (the l-analogue).
usage: python profile_scan.py <cycles of p, e.g. 4,5;6,7;8,9;10,11;12,13> <json> [...]"""
import json, sys
from collections import Counter
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int
p = {i: i for i in range(14)}
for c in sys.argv[1].split(";"):
    c = [int(t) for t in c.split(",")]
    for k in range(len(c)):
        p[c[k]] = c[(k + 1) % len(c)]
g = dict(p); g.update({0: 1, 1: 0, 2: 3, 3: 2})


def rank(rows):
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    if not A: return 0
    for c in range(len(A[0])):
        q = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if q is None: continue
        A[r], A[q] = A[q], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r


def comps(S, E, centre):
    others = [y for y in range(14) if y not in centre]
    par = {y: y for y in others}
    def find(y):
        while par[y] != y:
            par[y] = par[par[y]]; y = par[y]
        return y
    for y in others:
        par[find(y)] = find(y ^ 1)
    X = [i for i in range(len(S)) if S[i] & set(centre)]
    lt = lambda i: [y for y in S[i] if y not in centre][0]
    for i in X:
        for j in X:
            if i < j and frozenset((S[i], S[j])) in E:
                par[find(lt(i))] = find(lt(j))
    return len({find(y) for y in others})


tab = Counter()
for f in sys.argv[2:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    E = {frozenset((S[a], S[b])) for a, b in d["edges"]}
    M8 = [[(24 if a == b else 0) - 8 * (1 if frozenset((S[a], S[b])) in E else 0) - int(round(8 * kval(S[a], S[b])))
           for b in range(n)] for a in range(n)]
    N = nullspace_int(M8)
    gl = [idx[frozenset(g[y] for y in s)] for s in S]
    ev, od = [], []
    for v in N:
        w = [0] * n
        for i in range(n):
            w[gl[i]] = v[i]
        ev.append([v[i] + w[i] for i in range(n)])
        od.append([v[i] - w[i] for i in range(n)])
    de, do = rank(ev), rank(od)
    L = lambda a, b: idx[frozenset((a, b))]
    Hm = all(o[L(2, y)] + o[L(3, y)] == 0 for o in od for y in range(4, 14))
    Hl = all(o[L(0, y)] + o[L(1, y)] == 0 for o in od for y in range(4, 14))
    cl, cm = comps(S, E, (0, 1)), comps(S, E, (2, 3))
    tl = sum(1 for x in range(2, 14) if frozenset((S[L(0, x)], S[L(1, x)])) in E)
    tm = sum(1 for x in [0, 1] + list(range(4, 14)) if frozenset((S[L(2, x)], S[L(3, x)])) in E)
    # side relations: kernel vectors supported on X_l or on X_m
    Xl = [i for i in range(n) if S[i] & {0, 1}]
    Xm = [i for i in range(n) if S[i] & {2, 3}]
    def supp_dim(X):
        Xs = set(X)
        if not X:
            return 0
        sub = [[M8[a][b] for b in X] for a in range(n)]
        return len(X) - rank(sub)
    sl_, sm_ = supp_dim(Xl), supp_dim(Xm)
    sx = supp_dim(sorted(set(Xl) & set(Xm)))
    side = sl_ + sm_ - sx
    key = (len(N), cl, cm, tl, tm, side, len(N) - side, (de, do), Hl, Hm)
    tab[key] += 1
print("(nullity, c(l), c(m), t(l), t(m), side, mixed, g-profile (even, odd), (H_g) on l, (H_g) on m): count")
for k, v in sorted(tab.items(), key=lambda kv: -kv[1]):
    print("  ", k, v)
