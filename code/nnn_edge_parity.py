"""notes/103 §13: at a non-isometric Kneser edge P-P', is the number of all-non-isometric pages even?
Test with the signed (K) condition at P-P' alone: sum over the 3 pages R of the holonomy Theta_R
(signed 3x3 permutation on the characters A, pi_1, pi_2 of P) must equal 2E_A + 2E_{X0} - I,
X0 = character of P sent to A(P') by phi_{PP'}."""
import itertools
from collections import defaultdict

pts = [(a, b) for a in (0, 1) for b in (0, 1)]
def add(u, v): return (u[0] ^ v[0], u[1] ^ v[1])
maps = [dict(zip(pts, img)) for img in itertools.permutations(pts)]   # all 24 bijections of F_2^2
def comp(f, g): return {u: f[g[u]] for u in pts}                      # f o g
def inv(f): return {v: u for u, v in f.items()}
def iso(f): return all(add(f[u], f[add(u, (1, 1))]) == (1, 1) for u in pts)
chars = [(1, 1), (1, 0), (0, 1)]          # A, pi_first (depends on first coord), pi_second
def ch(l, u): return (-1) ** ((l[0] & u[0]) ^ (l[1] & u[1]))
def signed_matrix(f):
    """matrix of g -> g o f^{-1} on characters: rows = target char, cols = source char"""
    M = [[0] * 3 for _ in range(3)]
    fi = inv(f)
    for c, l in enumerate(chars):          # source character chi_l on the domain
        vals = {v: ch(l, fi[v]) for v in pts}      # chi_l o f^{-1} on the codomain
        for r, l2 in enumerate(chars):
            s = sum(vals[v] * ch(l2, v) for v in pts) // 4
            M[r][c] = s
    return tuple(tuple(row) for row in M)

stats = defaultdict(int)
bad = 0
for f in maps:
    if iso(f):
        continue
    # phi_{PP'} = f.  X0 = source character mapped to A by f
    Mf = signed_matrix(f)
    X0 = next(c for c in range(3) if Mf[0][c] != 0)
    target = [[0] * 3 for _ in range(3)]
    for c in range(3):
        target[c][c] = -1
    target[0][0] += 2
    target[X0][X0] += 2
    target = tuple(tuple(r) for r in target)
    fi = inv(f)
    per_page = set()
    for g in maps:          # phi_{PR}
        for h in maps:      # phi_{RP'}
            theta = comp(fi, comp(h, g))      # P -> R -> P' -> P
            st = (0 if iso(g) else 1, 0 if iso(h) else 1)
            per_page.add((st, signed_matrix(theta)))
    per_page = sorted(per_page)
    for a, b, c in itertools.combinations_with_replacement(per_page, 3):
        S = tuple(tuple(a[1][r][s] + b[1][r][s] + c[1][r][s] for s in range(3)) for r in range(3))
        if S != target:
            continue
        sts = sorted([a[0], b[0], c[0]])
        if (0, 0) in sts and any(s != (0, 0) for s in sts):
            pass
        nnn = sum(1 for s in sts if s == (1, 1))
        stats[(tuple(sts), nnn % 2)] += 1
for k, v in sorted(stats.items()):
    print(k, v)
