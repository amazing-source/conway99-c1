# Independent model of the exact profile selection (no py_extend / Codex code), solved by CryptoMiniSat.
# Known part from letters: core (paircores8 edges), Q12 grid (if the family has it), Y grids, Q12-Y attachments, sigma.
# Outside options = all sets of known neighbours with the forced counts; filters: letter room, pair room,
# new-to-known mu/lambda bound, own letter quota.  Constraints: one option per outside label; exact counts for every
# known pair, every (known vertex, letter), every known degree; outside pairs: common known <= 2 - shared letters.
import gzip, json, os, sys
from itertools import combinations, product
PYLIB = sys.argv[4]
sys.path.insert(0, PYLIB); os.add_dll_directory(PYLIB)
import pycryptosat

def base(r, f):
    return 2 if r == f else (0 if set(r) & set(f) else 1)

YRS = {"P3": ((4, 5), (4, 6)), "K3": ((4, 5), (4, 6), (5, 6)), "2K2": ((3, 4), (5, 6)), "2K2N": ((3, 4), (5, 6)),
       "P3N": ((4, 5), (4, 6))}

def build(core, bd, fam, att, sigma):
    YR = YRS[fam]
    q12 = fam in ("P3", "K3", "2K2")
    rects = [(0, 1), (0, 2)] + ([(1, 2)] if q12 else []) + list(YR)
    lab = [(2*a + s, 2*b + t) for a, b in rects for s, t in product(range(2), repeat=2)]
    n = len(lab); idx = {l: i for i, l in enumerate(lab)}
    A = [[0]*n for _ in range(n)]
    def e(u, v):
        A[u][v] = A[v][u] = 1
    for u, v in core['edges']:
        e(u, v)
    for a, b in ([(1, 2)] if q12 else []) + list(YR):
        ls = [(2*a + s, 2*b + t) for s, t in product(range(2), repeat=2)]
        for x, y in combinations(ls, 2):
            if len(set(x) & set(y)) == 1:
                e(idx[x], idx[y])
    yoff = 12 if q12 else 8
    for k, m in enumerate(bd):
        for u in range(8):
            if m >> u & 1:
                e(u, yoff + k)
    if q12:
        for g in range(len(YR)):
            for j in range(4):
                e(8 + j, yoff + 4*g + att[g][j])
    if sigma is not None:
        for c in range(4):
            e(yoff + c, yoff + 4 + sigma[c])
    N = [{v for v in range(n) if A[u][v]} for u in range(n)]
    outside = [(2*a + s, 2*b + t) for a, b in combinations(range(7), 2) if (a, b) not in set(rects)
               for s, t in product(range(2), repeat=2)]
    return lab, A, N, outside, q12, YR, yoff
