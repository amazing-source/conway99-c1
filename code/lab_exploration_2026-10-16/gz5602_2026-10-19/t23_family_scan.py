"""Detector of the family closed by Codex (main 7d95ad5e, touching23_exclusion_manifest.json): nonzero opposite
DISJOINT columns H_A = -H_B (exact rational kernel of the grid and block relations), the three rectangles on the
three complementary lines all grids, exactly two of the four X rectangles (A x B) grids, sharing a line, and the two
non-grid X rectangles sharing a line.  Lists every gz template of the c3 catalogue with this structure (LAB 19/10/2026).
usage: python t23_family_scan.py <catalogue.json.gz> <out.json>"""
import gzip, json, sys
from itertools import combinations
from fractions import Fraction
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


recs = json.load(gzip.open(sys.argv[1]))["open"]
hits = []
for idx, r in enumerate(recs):
    t = r["template"]; ng = {tuple(e) for e in t["nongrid_edges"]}
    B = None
    for A_, B_ in combinations(sorted(ng), 2):
        if set(A_) & set(B_):
            continue
        X = set(A_) | set(B_); C = [v for v in range(7) if v not in X]
        if any(e in ng for e in combinations(C, 2)):
            continue
        xr = [tuple(sorted((p, q))) for p in A_ for q in B_]
        g = [e for e in xr if e not in ng]; n = [e for e in xr if e in ng]
        if len(g) != 2 or not (set(g[0]) & set(g[1])) or not (set(n[0]) & set(n[1])):
            continue
        if B is None:
            B = W_basis(t)
        v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
        if in_W(B, v):
            hits.append(idx); break
json.dump(hits, open(sys.argv[2], "w"))
print(len(hits), "templates of the gz catalogue in the family;", hits[:40])
