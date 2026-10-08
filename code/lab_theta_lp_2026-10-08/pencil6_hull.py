"""C1, lab session, 2026-10-08. Canonical six-pencil: are the Gram-rank shortfalls TRUE relations mod 7?
  python pencil6_hull.py
NEW FACT USED (laptop session): a relation among grid classes is a combination of grid indicators (and 1) of the form
(A + 4I) y mod 7; Gram rank = dim C - dim Hull(C) for the code C spanned by the grid indicators and 1.
Here the 99 vertices are explicit (canonical column solution): 3 points of Theta, 36 prism vertices (k, column, row),
60 far names; grids P_k and A(r, d) as vertex sets (independent of the unknown rows). For y supported on the ball of
Theta and constant on every rung (so that (A + 4I) y does not depend on the unknown rows either), (A + 4I) y is
explicit. Printed for each pattern: number of generators n (grids + 1), dim C, Gram rank, dim Hull, and
REL = dim( {(A + 4I) y} cap C ) = relations certified TRUE in this model (lower bound), against the number x6 of lines
in six grids of the pattern (the pencil relations)."""
import random
from itertools import combinations, permutations
pts = range(6); duads = [frozenset(d) for d in combinations(pts, 2)]
synth = [frozenset(a) for a in combinations(duads, 3) if len(frozenset().union(*a)) == 6]
total = next(t for t in combinations(synth, 5) if len(frozenset().union(*t)) == 15)
out = [s for s in synth if s not in total]
names = [(x, lam) for x in range(10) for lam in permutations(range(3))]
def col(nm, k):
    x, lam = nm; ds = sorted(out[x], key=sorted)
    return next(lam[t] for t in range(3) if k in ds[t])
CB = [[col(nm, k) for k in pts] for nm in names]
TH = lambda c: c
PV = lambda k, c, s: 3 + k * 6 + c * 2 + s
BV = lambda i: 39 + i
def vecP(k):
    v = [0] * 99
    for c in range(3): v[TH(c)] = 1
    for c in range(3):
        for s in range(2): v[PV(k, c, s)] = 1
    return v
def vecA(r, d):
    v = [0] * 99; v[TH(r)] = 1; i, j = sorted(d)
    for k in (i, j):
        for s in range(2): v[PV(k, r, s)] = 1
    far = [b for b in range(60) if CB[b][i] == r and CB[b][j] == r]; assert len(far) == 4
    for b in far: v[BV(b)] = 1
    return v
def rank7(M):
    M = [[x % 7 for x in r] for r in M]; rk = 0; ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((i for i in range(rk, len(M)) if M[i][c]), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; inv = pow(M[rk][c], 5, 7); M[rk] = [(x * inv) % 7 for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % 7 for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
# images (A + 4I) y for the basis of rung-constant y on the ball: 3 (theta) + 18 (k, column)
IM = []
for c0 in range(3):
    y = [0] * 99; img = [0] * 99
    for c in range(3): img[TH(c)] = 4 if c == c0 else 1
    for k in pts:
        for s in range(2): img[PV(k, c0, s)] = 1
    IM.append(img)
for k0 in pts:
    for c0 in range(3):
        img = [0] * 99; img[TH(c0)] = 2
        for c in range(3):
            for s in range(2): img[PV(k0, c, s)] = (4 + 1) if c == c0 else 2          # itself 4 + rung mate 1 ; other columns: the two row mates... one per row
        for c in range(3):
            if c != c0:
                for s in range(2): img[PV(k0, c, s)] = 1                                  # (k0, c, s) is adjacent to (k0, c0, s) only
        for b in range(60):
            if CB[b][k0] == c0: img[BV(b)] = 1
        IM.append(img)
SH = {"nothing": [], "perfect matching": [(0, 1), (2, 3), (4, 5)], "hexagon": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)], "two triangles": [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)],
      "K_3,3": [(a, b) for a in (0, 1, 2) for b in (3, 4, 5)], "star": [(0, x) for x in range(1, 6)], "double star": [(0, x) for x in range(1, 6)] + [(1, x) for x in range(2, 6)], "K_6": list(combinations(range(6), 2))}
random.seed(3)
print("pattern at 1/2/3 points | n = grids + 1 | dim C | Gram rank | dim Hull | REL (true, lower bound) | x6 | n - dimC + REL - x6 (extra true relations)")
for name, E in SH.items():
    for npts in ((0,) if not E else (1, 2, 3)):
        seen = {}
        for _ in range(1 if not E else 60):
            Hs = []
            for r in range(3):
                if r < npts: pi = random.sample(range(6), 6); Hs.append([frozenset((pi[a], pi[b])) for a, b in E])
                else: Hs.append([])
            gens = [vecP(k) for k in pts] + [vecA(r, d) for r in range(3) for d in Hs[r]] + [[1] * 99]
            n = len(gens); dC = rank7(gens); G = [[sum(a * b for a, b in zip(u, v)) for v in gens] for u in gens]; gr = rank7(G)
            rel = rank7(IM) + dC - rank7(IM + gens)
            x6 = 1 + sum(1 for r in range(3) for k in pts if sum(1 for d in Hs[r] if k in d) == 5)   # Theta, and columns in 1 + 5 grids
            key = (n, dC, gr, dC - gr, rel, x6, n - dC + rel - x6); seen[key] = seen.get(key, 0) + 1
        for key, cnt in sorted(seen.items()): print("%-18s %d pt | %2d | %2d | %2d | %d | %d | %d | %+d   (%d positions)" % ((name, npts) + key + (cnt,)))
