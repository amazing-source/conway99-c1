"""Members of the P3NB family among the c3 templates (LAB 19/10/2026): a shared pair (Q_ab, Q_ac), both non-grid, with
H_ab = -H_ac forced (exact rational kernel W), two grids off {a, b, c} sharing a line x (Y-path Q_xy, Q_xz), and a grid
through b and the free line w (Q_bw) or, by the b <-> c symmetry, through c and w (Q_cw).  Q_bc arbitrary.  Witness
(a, b', c', x, y, z, w) with b' the side carrying the B-grid (normal form a->0, b'->1, c'->2, w->3, x->4, y->5, z->6).
Code of W_basis / in_W copied from k3universal_scan.py.
usage: python p3nb_members.py <catalogue.json.gz> <out.json>"""
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
mem = {}
for idx, r in enumerate(recs):
    t = r["template"]; ng = {tuple(e) for e in t["nongrid_edges"]}
    B = None
    for a in range(7):
        for b, c in combinations([v for v in range(7) if v != a], 2):
            A_, B_ = tuple(sorted((a, b))), tuple(sorted((a, c)))
            if A_ not in ng or B_ not in ng:
                continue
            D = [v for v in range(7) if v not in (a, b, c)]
            wit = None
            for x in D:
                ys = [v for v in D if v != x and tuple(sorted((x, v))) not in ng]
                for y, z in combinations(ys, 2):
                    w = next(v for v in D if v not in (x, y, z))
                    for side, other in ((b, c), (c, b)):
                        if tuple(sorted((side, w))) not in ng:
                            wit = [a, side, other, x, y, z, w]; break
                    if wit: break
                if wit: break
            if wit is None:
                continue
            if B is None:
                B = W_basis(t)
            v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
            if not in_W(B, v):
                continue
            if idx not in mem:
                mem[idx] = wit
json.dump({"p3nb": mem}, open(sys.argv[2], "w"))
print("gz templates: P3NB", len(mem))
