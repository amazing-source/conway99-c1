"""Normal forms of the P3-universal family (LAB 19/10/2026): a shared pair with H01 = -H02 forced, Q12 grid, grids 45
and 46 (two grids off {0,1,2} sharing the line 4); lines 3, 5, 6 the rest of D.  For each open c3 template of the family,
every line permutation pi (old -> new) giving this normal form, with the relabelled template, re-checked by the exact
rational kernel.  The K3-universal family is the sub-family where 56 is also a grid.
usage: python p3family_normalize.py <catalogue.json.gz> <open.tsv> <out.json>"""
import gzip, json, sys
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


def relabel(t, pi):
    ng = [tuple(sorted((pi[a], pi[b]))) for a, b in t["nongrid_edges"]]
    groups = [None] * 7
    for a, gs in enumerate(t["nontrivial_component_groups"]):
        groups[pi[a]] = sorted(sorted(pi[j] for j in P) for P in gs)
    return {"nongrid_edges": sorted(map(list, ng)), "nontrivial_component_groups": groups,
            "kernel_dimension": t["kernel_dimension"]}



recs = json.load(gzip.open(sys.argv[1]))["open"]
open_ = {int(l.split()[1]) for l in open(sys.argv[2]) if l.startswith("gz")}
out = []
for idx in sorted(open_):
    t = recs[idx]["template"]; ng = {tuple(e) for e in t["nongrid_edges"]}
    B = W_basis(t); seen = {}
    for a in range(7):
        for b, c in combinations([v for v in range(7) if v != a], 2):
            A_, B_ = tuple(sorted((a, b))), tuple(sorted((a, c)))
            if A_ not in ng or B_ not in ng or tuple(sorted((b, c))) in ng:
                continue
            v = [0] * 21; v[ridx[A_]] = 1; v[ridx[B_]] = 1
            if not in_W(B, v):
                continue
            D = [x for x in range(7) if x not in (a, b, c)]
            for d1 in D:
                others = [x for x in D if x != d1]
                for d2, d3 in permutations(others, 2):
                    if tuple(sorted((d1, d2))) in ng or tuple(sorted((d1, d3))) in ng or d2 > d3:
                        continue
                    d4 = next(x for x in others if x not in (d2, d3))
                    for bb, cc in ((b, c), (c, b)):
                        pi = {a: 0, bb: 1, cc: 2, d4: 3, d1: 4, d2: 5, d3: 6}
                        nt = relabel(t, pi); key = json.dumps(nt, sort_keys=True)
                        nng = {tuple(e) for e in nt["nongrid_edges"]}
                        assert (0, 1) in nng and (0, 2) in nng and (1, 2) not in nng and (4, 5) not in nng and (4, 6) not in nng
                        vv = [0] * 21; vv[ridx[(0, 1)]] = 1; vv[ridx[(0, 2)]] = 1
                        assert in_W(W_basis(nt), vv)
                        seen.setdefault(key, {"template": nt, "permutations": []})["permutations"].append({str(k): v for k, v in pi.items()})
    for key, rec in seen.items():
        out.append({"gz_index": idx, "k3": (5, 6) not in {tuple(e) for e in rec["template"]["nongrid_edges"]}, **rec})
json.dump({"scope": "P3-universal normal forms (H01 = -H02 forced, Q12, Q45, Q46 grids)", "records": out}, open(sys.argv[3], "w"))
print(len(out), "normal forms over", len({r["gz_index"] for r in out}), "open templates;", len({r["gz_index"] for r in out if r["k3"]}), "with 56 grid too (K3)")
