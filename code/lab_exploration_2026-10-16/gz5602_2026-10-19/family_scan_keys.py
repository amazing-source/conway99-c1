"""Apply the closed / candidate family detectors to c <= 2 survivor keys (LAB 19/10/2026): C4C3 (grid pattern only,
true at every vertex), T23 and K3-universal / P3-universal (forced pair by the exact rational kernel of the template's
grid and block relations).  Counts hits by kernel dimension.
usage: python family_scan_keys.py <keys glob> <max keys>"""
import glob, gzip, json, sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
sys.path.insert(0, "..")
from jhat_fg_keys import decode
RECT = list(combinations(range(7), 2))
ridx = {q: i for i, q in enumerate(RECT)}


def W_basis(t):
    ng = {tuple(e) for e in t["nongrid_edges"]}
    rows = []
    for q in RECT:
        if q not in ng:
            v = [0] * 21; v[ridx[q]] = 1; rows.append(v)
    for a, groups in enumerate(t["nontrivial_component_groups"]):
        for P in groups:
            v = [0] * 21
            for j in P:
                v[ridx[tuple(sorted((a, j)))]] = 1
            rows.append(v)
    rows = [[Fraction(x) for x in r] for r in rows]
    piv, r = [], 0
    for c in range(21):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [x / rows[r][c] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    return rows[:r], piv


def in_W(basis, v):
    rows, piv = basis
    v = [Fraction(x) for x in v]
    for row, c in zip(rows, piv):
        if v[c] != 0:
            f = v[c]; v = [x - f * y for x, y in zip(v, row)]
    return all(x == 0 for x in v)



def killed(grid):
    """grid: set of frozenset edges among 0..6 that are grid rectangles"""
    for Y in combinations(range(7), 3):
        if not all(frozenset(p) in grid for p in combinations(Y, 2)):
            continue
        X = [v for v in range(7) if v not in Y]
        # 4-cycles on X: 3 of them; diagonals = the 2 non-cycle pairs
        for a, b, c, d in [(X[0], X[1], X[2], X[3]), (X[0], X[1], X[3], X[2]), (X[0], X[2], X[1], X[3])]:
            cyc = [frozenset((a, b)), frozenset((b, c)), frozenset((c, d)), frozenset((d, a))]
            if all(e in grid for e in cyc):
                diag = [frozenset((a, c)), frozenset((b, d))]
                if not all(e in grid for e in diag):
                    return (Y, (a, b, c, d))
    return None



def fams(t):
    ng = {tuple(e) for e in t["nongrid_edges"]}
    grid = {frozenset(p) for p in RECT} - {frozenset(e) for e in ng}
    out = set()
    if killed(grid):
        out.add("C4C3")
    B = None
    for A_, B_ in combinations(sorted(ng), 2):
        sh = set(A_) & set(B_)
        if sh:
            (a,) = sh; b = (set(A_) - {a}).pop(); c = (set(B_) - {a}).pop()
            if tuple(sorted((b, c))) in ng:
                continue
            D = [v for v in range(7) if v not in (a, b, c)]
            dg = {e for e in combinations(D, 2) if e not in ng}
            tri = any(all(e in dg for e in combinations(T, 2)) for T in combinations(D, 3))
            p3 = any(len(set(e) & set(f)) == 1 for e, f in combinations(dg, 2))
            if not p3:
                continue
            kinds = {"P3"} | ({"K3"} if tri else set())
        else:
            X = set(A_) | set(B_); C = [v for v in range(7) if v not in X]
            if any(e in ng for e in combinations(C, 2)):
                continue
            xr = [tuple(sorted((p, q))) for p in A_ for q in B_]
            g = [e for e in xr if e not in ng]; n = [e for e in xr if e in ng]
            if not (len(g) == 2 and set(g[0]) & set(g[1]) and set(n[0]) & set(n[1])):
                continue
            kinds = {"T23"}
        if kinds <= out:
            continue
        if B is None:
            B = W_basis(t)
        v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
        if in_W(B, v):
            out |= kinds
    return out

pat, mx = sys.argv[1], int(sys.argv[2])
cnt = Counter(); bydim = Counter(); n = 0
for f in sorted(glob.glob(pat)):
    with gzip.open(f, "rt") as fh:
        for line in fh:
            key = line.strip()
            if not key:
                continue
            t, _ = decode(key)
            n += 1
            fs = fams(t)
            for x in fs:
                cnt[x] += 1
            if fs & {"C4C3", "T23"}:
                bydim[("closed", t.get("kernel_dimension"))] += 1
            if "P3" in fs:
                bydim[("P3", t.get("kernel_dimension"))] += 1
            if n >= mx:
                break
    if n >= mx:
        break
print("keys", n, "family hits", dict(cnt)); print(dict(sorted(bydim.items(), key=str)))
