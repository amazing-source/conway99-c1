"""The Payne-derived generalized quadrangle P(W(9), x0) of order (8,10), built from W(3,9) (14/10/2026), and the
3-ovoids that are orbits of index-3 subgroups of the elation group (a quick validation of the 3-ovoid model of the
srg(243,22,1,2) family; see NOTE_LAMBDA1 section 5).

W(3,9): points of PG(3,9), symplectic form b(x,y) = x1y2 - x2y1 + x3y4 - x4y3, x0 = (1,0,0,0). Points of P(W(9),x0):
points y with b(x0,y) = y2 != 0, normalised y = (a,1,b,c) (729 points). Lines: (i) totally isotropic lines of W(3,9)
not through x0, minus their point in x0-perp (9 points each, 810 lines); (ii) the lines of PG(3,9) through x0 and a
point y with y2 != 0 (hyperbolic lines {x0,y}^perp-perp), minus x0 (9 points each, 81 lines). Order (8,10), checked.
F_9 = F_3[i], i^2 = -1; element a + b i stored as the integer a + 3b.
usage: python payne9.py <out dir>    -> gq9.json (points, lines), and the test of the 120 subgroup orbits
"""
import itertools
import json
import os
import sys

import numpy as np

# ---- F_9 arithmetic
ADD = [[0] * 9 for _ in range(9)]
MUL = [[0] * 9 for _ in range(9)]
for x in range(9):
    for y in range(9):
        a, b = x % 3, x // 3
        c, d = y % 3, y // 3
        ADD[x][y] = (a + c) % 3 + 3 * ((b + d) % 3)
        # (a + b i)(c + d i) = (ac - bd) + (ad + bc) i
        MUL[x][y] = (a * c - b * d) % 3 + 3 * ((a * d + b * c) % 3)
NEG = [next(y for y in range(9) if ADD[x][y] == 0) for x in range(9)]
INV = [None] + [next(y for y in range(9) if MUL[x][y] == 1) for x in range(1, 9)]


def add(x, y):
    return ADD[x][y]


def sub(x, y):
    return ADD[x][NEG[y]]


def mul(x, y):
    return MUL[x][y]


def normalise(v):
    for c in v:
        if c:
            iv = INV[c]
            return tuple(mul(iv, x) for x in v)
    return None


def form(x, y):          # x1y2 - x2y1 + x3y4 - x4y3
    t = sub(mul(x[0], y[1]), mul(x[1], y[0]))
    t = add(t, sub(mul(x[2], y[3]), mul(x[3], y[2])))
    return t


def span_points(u, v):
    pts = set()
    for s in range(9):
        for t in range(9):
            if s == 0 and t == 0:
                continue
            w = tuple(add(mul(s, a), mul(t, b)) for a, b in zip(u, v))
            pts.add(normalise(w))
    return pts


def build():
    allpts = sorted({normalise(v) for v in itertools.product(range(9), repeat=4) if any(v)})
    assert len(allpts) == 820
    x0 = (1, 0, 0, 0)
    P = [p for p in allpts if form(x0, p) != 0]
    assert len(P) == 729
    pidx = {p: i for i, p in enumerate(P)}
    lines = set()
    # (i) totally isotropic lines not through x0
    for p in P:
        perp = [q for q in allpts if q != p and form(p, q) == 0]
        for q in perp:
            L = frozenset(span_points(p, q))
            if x0 in L:
                continue
            lines.add(frozenset(r for r in L if form(x0, r) != 0))
    nl_i = len(lines)
    # (ii) hyperbolic lines through x0
    for p in P:
        L = span_points(x0, p)
        lines.add(frozenset(r for r in L if r != x0))
    lines = sorted(sorted(pidx[r] for r in L) for L in lines)
    assert all(len(L) == 9 for L in lines)
    assert len(lines) == 891, (len(lines), nl_i)
    on = [[] for _ in P]
    for li, L in enumerate(lines):
        for p in L:
            on[p].append(li)
    assert {len(x) for x in on} == {11}
    # collinearity graph must be srg(729,88,7,11)
    A = np.zeros((729, 729), dtype=np.int64)
    for L in lines:
        for a, b in itertools.combinations(L, 2):
            A[a, b] = A[b, a] = 1
    A2 = A @ A
    I = np.eye(729, dtype=np.int64)
    J = np.ones((729, 729), dtype=np.int64)
    assert np.array_equal(A2, 88 * I + 7 * A + 11 * (J - I - A)), "collinearity graph is not srg(729,88,7,11)"
    return P, lines, A


def elations(P):
    """the elation group about x0: symplectic matrices fixing x0, acting on the points (a,1,b,c); found by search over
    matrices M = [[1,al,p,q],[0,1,0,0],[0,be,1,0],[0,ga,0,1]] (acting on column vectors)."""
    def apply(M, y):
        return tuple(add(add(add(mul(M[r][0], y[0]), mul(M[r][1], y[1])), mul(M[r][2], y[2])), mul(M[r][3], y[3]))
                     for r in range(4))
    basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    G = []
    for al in range(9):
        for be in range(9):
            for ga in range(9):
                found = None
                for p in range(9):
                    for q in range(9):
                        M = [[1, al, p, q], [0, 1, 0, 0], [0, be, 1, 0], [0, ga, 0, 1]]
                        if all(form(apply(M, u), apply(M, v)) == form(u, v) for u in basis for v in basis):
                            found = M
                            break
                    if found:
                        break
                assert found, (al, be, ga)
                G.append(found)
    pidx = {p: i for i, p in enumerate(P)}
    perms = [tuple(pidx[normalise(apply(M, p))] for p in P) for M in G]
    return perms


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    P, lines, A = build()
    print("P(W(9),x0): %d points, %d lines of 9, 11 lines per point; collinearity graph srg(729,88,7,11) checked"
          % (len(P), len(lines)), flush=True)
    json.dump({"points": [list(p) for p in P], "lines": lines}, open(os.path.join(out, "gq9.json"), "w"))
    E = elations(P)
    ident = tuple(range(729))
    assert len(set(E)) == 729 and ident in E
    # regular action
    assert all(len({g[p] for g in E}) == 729 for p in [0, 5, 100])
    print("elation group: 729 elements, regular on the points", flush=True)
    # index-3 subgroups: (be, ga) compose additively (lower-left entries of the unipotent matrices), so for every
    # nonzero F_3-linear functional phi on (be, ga) in F_9^2 = F_3^4 (up to sign: 40 of them) the set
    # H_phi = {g : phi(be, ga) = 0} is a subgroup of order 243.
    params = [(al, be, ga) for al in range(9) for be in range(9) for ga in range(9)]
    def vec(be, ga):
        return (be % 3, be // 3, ga % 3, ga // 3)
    phis = []
    for f in itertools.product(range(3), repeat=4):
        if any(f) and next(c for c in f if c) == 1:
            phis.append(f)
    assert len(phis) == 40
    subs = []
    for f in phis:
        H = [E[i] for i, (al, be, ga) in enumerate(params) if sum(a * b for a, b in zip(f, vec(be, ga))) % 3 == 0]
        assert len(H) == 243
        subs.append(H)
    print("index-3 subgroups: %d" % len(subs), flush=True)
    on = [[] for _ in range(729)]
    for li, L in enumerate(lines):
        for p in L:
            on[p].append(li)
    results = []
    for H in subs:
        seen = set()
        for start in range(729):
            if start in seen:
                continue
            orb = sorted({h[start] for h in H})
            seen |= set(orb)
            O = set(orb)
            counts = {sum(1 for p in L if p in O) for L in lines}
            mu = None
            if counts == {3}:
                Oi = sorted(O)
                sub = A[np.ix_(Oi, Oi)]
                S2 = sub @ sub
                mus = {int(S2[i, j]) for i in range(len(Oi)) for j in range(i + 1, len(Oi)) if sub[i, j] == 0}
                lam = {int(S2[i, j]) for i in range(len(Oi)) for j in range(i + 1, len(Oi)) if sub[i, j] == 1}
                mu = (sorted(lam), sorted(mus))
                if mus == {2}:
                    with open(os.path.join(out, "ovoid_%d.json" % len(results)), "w") as fh:
                        json.dump(Oi, fh)
            results.append((sorted(counts), mu))
    from collections import Counter
    print("orbits of the 40 subgroups (120 orbits of 243 points): line intersection counts / (lambda, mu) values:")
    for key, c in Counter((tuple(a), str(b)) for a, b in results).items():
        print("   %s x %d" % (key, c))
