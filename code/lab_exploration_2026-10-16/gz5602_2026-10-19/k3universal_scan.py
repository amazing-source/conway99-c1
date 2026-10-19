"""Members of the K3-universal family among the c3 templates (LAB 19/10/2026): some shared pair (Q_ab, Q_ac) with
H_ab = -H_ac forced (exact rational kernel W of the grid and block relations), Q_bc a grid, and three grids forming a
triangle on three of the four lines off {a, b, c} (the other rectangles unconstrained).  Also the larger P3-universal
family (two grids sharing a line among the six rectangles off {a, b, c}).  Writes the member lists with one witness
(a, b, c, triangle) each.
usage: python k3universal_scan.py <catalogue.json.gz> <out.json>"""
import gzip, json, sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
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
k3, p3 = {}, {}
for idx, r in enumerate(recs):
    t = r["template"]; ng = {tuple(e) for e in t["nongrid_edges"]}
    B = None
    for a in range(7):
        for b, c in combinations([v for v in range(7) if v != a], 2):
            A_, B_ = tuple(sorted((a, b))), tuple(sorted((a, c)))
            if A_ not in ng or B_ not in ng or tuple(sorted((b, c))) in ng:
                continue
            D = [v for v in range(7) if v not in (a, b, c)]
            dg = {e for e in combinations(D, 2) if e not in ng}
            tri = next((T for T in combinations(D, 3) if all(e in dg for e in combinations(T, 2))), None)
            p3ok = any(len(set(e) & set(f)) == 1 for e, f in combinations(dg, 2))
            if not (tri or p3ok):
                continue
            if B is None:
                B = W_basis(t)
            v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
            if not in_W(B, v):
                continue
            if tri and idx not in k3:
                k3[idx] = [a, b, c, list(tri)]
            if p3ok and idx not in p3:
                p3[idx] = [a, b, c]
json.dump({"k3": k3, "p3": p3}, open(sys.argv[2], "w"))
print("gz templates: K3-universal", len(k3), "P3-universal", len(p3))
