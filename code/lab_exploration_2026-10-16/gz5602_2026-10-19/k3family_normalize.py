"""Normal form of the family (dim 6, shared opposite pair Q_ab/Q_ac, Q_bc grid, the grids among the 6 rectangles of
D = lines off {a, b, c} forming a triangle) for Codex (LAB 19/10/2026).  Normal form: a = 0, b = 1, c = 2, the D-triangle
on {4, 5, 6}, the fourth line of D = 3; so the core is Q01 + Q02, the extra grid Q12, the D-grids 45, 46, 56.
For every open template of the family (cover-free or > 30000 Grams, as in the hard-core census) and every admissible
choice (a, b, c, triangle order) the script writes the line permutation pi (old line -> new line) and the relabelled
template (non-grid edges, blocks); one record per (template, choice), choices with the same relabelled template merged.
Each relabelled template is re-checked: Q01, Q02 non-grid, H01 = -H02 forced (exact rational kernel of the block and
grid relations), Q12 grid, 45/46/56 grids, 34/35/36 non-grid.
usage: python k3family_normalize.py <catalogue.json.gz> <open.tsv> <hard list json | all> <out.json>"""
import gzip
import json
import sys
from fractions import Fraction
from itertools import combinations, permutations

recs = json.load(gzip.open(sys.argv[1]))["open"]
open_ = {int(l.split()[1]) for l in open(sys.argv[2]) if l.startswith("gz")}
hard = None if sys.argv[3] == "all" else set(json.load(open(sys.argv[3])))
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


def relabel(t, pi):
    ng = [tuple(sorted((pi[a], pi[b]))) for a, b in t["nongrid_edges"]]
    groups = [None] * 7
    for a, gs in enumerate(t["nontrivial_component_groups"]):
        groups[pi[a]] = sorted(sorted(pi[j] for j in P) for P in gs)
    return {"nongrid_edges": sorted(map(list, ng)), "nontrivial_component_groups": groups,
            "kernel_dimension": t["kernel_dimension"]}


out = []
for idx in sorted(open_):
    if hard is not None and idx not in hard:
        continue
    t = recs[idx]["template"]
    if t["kernel_dimension"] != 6:
        continue
    ng = {tuple(e) for e in t["nongrid_edges"]}
    B = W_basis(t)
    seen = {}
    for a, b, c in permutations(range(7), 3):
        if b > c:
            continue
        A_, B_ = tuple(sorted((a, b))), tuple(sorted((a, c)))
        if A_ not in ng or B_ not in ng or tuple(sorted((b, c))) in ng:
            continue
        v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
        if not in_W(B, v):
            continue
        D = [x for x in range(7) if x not in (a, b, c)]
        dg = [e for e in combinations(D, 2) if e not in ng]
        tri = sorted({x for e in dg for x in e})
        if len(dg) != 3 or len(tri) != 3:
            continue
        d4 = next(x for x in D if x not in tri)
        for order in permutations(tri):
            pi = {a: 0, b: 1, c: 2, d4: 3, order[0]: 4, order[1]: 5, order[2]: 6}
            nt = relabel(t, pi)
            key = json.dumps(nt, sort_keys=True)
            nng = {tuple(e) for e in nt["nongrid_edges"]}
            assert (0, 1) in nng and (0, 2) in nng and (1, 2) not in nng
            assert all(e not in nng for e in [(4, 5), (4, 6), (5, 6)]) and all(e in nng for e in [(3, 4), (3, 5), (3, 6)])
            vv = [0] * 21; vv[ridx[(0, 1)]] = 1; vv[ridx[(0, 2)]] = 1
            assert in_W(W_basis(nt), vv)
            seen.setdefault(key, {"template": nt, "permutations": []})["permutations"].append({str(k): v for k, v in pi.items()})
    for key, rec in seen.items():
        out.append({"gz_index": idx, **rec})
json.dump({"scope": __doc__, "records": out}, open(sys.argv[4], "w"))
print(len(out), "normalised records over", len({r["gz_index"] for r in out}), "templates")
