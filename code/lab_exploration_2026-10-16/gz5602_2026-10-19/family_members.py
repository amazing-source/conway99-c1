"""Members of a GEN family among the c3 templates (LAB 19/10/2026): a forced shared pair (Q_ab, Q_ac), both non-grid,
H_ab = -H_ac (exact rational kernel W), and a line bijection a->0, b->1, c->2, D->{3,4,5,6} (b <-> c allowed) mapping
every grid of the PATTERN (normal-form names, e.g. 45,46,13) onto a grid of the template.  Q_bc arbitrary.
Witness (a, b, c, [template lines of 3, 4, 5, 6]).  Code of W_basis / in_W copied from k3universal_scan.py.
usage: python family_members.py <catalogue.json.gz> <pattern e.g. 45,46,13> <out.json>"""
import gzip, json, sys
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
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
PAT = [tuple(sorted((int(g[0]), int(g[1])))) for g in sys.argv[2].split(",")]
assert all(not (set(F) & {0}) for F in PAT)
mem = {}
for idx, r in enumerate(recs):
    t = r["template"]; ng = {tuple(e) for e in t["nongrid_edges"]}
    B = None
    for a in range(7):
        for b, c in permutations([v for v in range(7) if v != a], 2):
            A_, B_ = tuple(sorted((a, b))), tuple(sorted((a, c)))
            if A_ not in ng or B_ not in ng:
                continue
            D = [v for v in range(7) if v not in (a, b, c)]
            wit = None
            for perm in permutations(D):
                inv = {0: a, 1: b, 2: c, 3: perm[0], 4: perm[1], 5: perm[2], 6: perm[3]}
                if all(tuple(sorted((inv[x], inv[y]))) not in ng for x, y in PAT):
                    wit = [a, b, c, list(perm)]; break
            if wit is None:
                continue
            if B is None:
                B = W_basis(t)
            v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
            if not in_W(B, v):
                continue
            if idx not in mem:
                mem[idx] = wit
json.dump({"pattern": sys.argv[2], "members": mem}, open(sys.argv[3], "w"))
print("pattern", sys.argv[2], "gz templates:", len(mem))
