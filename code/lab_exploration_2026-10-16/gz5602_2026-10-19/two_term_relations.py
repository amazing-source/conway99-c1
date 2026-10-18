"""Two-term column relations forced by the block equations (LAB 19/10/2026).
The columns of H satisfy sum_{j in P} H_{aj} = 0 for every root a and block P (F1), and H_F = 0 for every grid F (F2).
A vector c in R^21 with H c = 0 for every realisation is any vector of the span W of these relation vectors (exactly:
W = the orthogonal complement of the zero-sum space Z(Jh), whose dimension is kernel_dimension).  We list the pairs of
non-grid rectangles A != B with e_A + e_B in W (H_A = -H_B: 'opposite', as Q03/Q12 in gz 5602) or e_A - e_B in W
(H_A = H_B: 'equal').  Pairs of a block of size 2 give opposite pairs sharing a line.
usage: python two_term_relations.py <catalogue.json.gz> <open.tsv | all>"""
import gzip
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations

recs = json.load(gzip.open(sys.argv[1]))["open"]
sel = None if sys.argv[2] == "all" else {int(l.split()[1]) for l in open(sys.argv[2]) if l.startswith("gz")}
RECT = list(combinations(range(7), 2))
ridx = {q: i for i, q in enumerate(RECT)}


def rref(rows):
    rows = [[Fraction(x) for x in r] for r in rows]
    piv = []
    r = 0
    for c in range(21):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
    return rows[:r], piv


def in_span(basis, piv, v):
    v = [Fraction(x) for x in v]
    for row, c in zip(basis, piv):
        if v[c] != 0:
            f = v[c]
            v = [a - f * b for a, b in zip(v, row)]
    return all(x == 0 for x in v)


stats = Counter(); per = {}
for idx, r in enumerate(recs):
    if sel is not None and idx not in sel:
        continue
    t = r["template"]
    E = {tuple(e) for e in t["nongrid_edges"]}
    rel = []
    for q in RECT:
        if q not in E:
            v = [0] * 21; v[ridx[q]] = 1; rel.append(v)
    for a, groups in enumerate(t["nontrivial_component_groups"]):
        for P in groups:
            v = [0] * 21
            for j in P:
                v[ridx[tuple(sorted((a, j)))]] = 1
            rel.append(v)
    basis, piv = rref(rel)
    opp, eq = [], []
    for A, B in combinations(sorted(E), 2):
        v = [0] * 21; v[ridx[A]] = 1; v[ridx[B]] = 1
        if in_span(basis, piv, v):
            opp.append(("%d%d" % A, "%d%d" % B, "share" if set(A) & set(B) else "disjoint"))
        v[ridx[B]] = -1
        if in_span(basis, piv, v):
            eq.append(("%d%d" % A, "%d%d" % B))
    dim = 21 - len(basis)
    assert dim == t["kernel_dimension"], (idx, dim, t["kernel_dimension"])
    kind = ("opp_disjoint" if any(o[2] == "disjoint" for o in opp) else "opp_share_only" if opp else "no_opp") + ("+eq" if eq else "")
    stats[(t["kernel_dimension"], kind)] += 1
    per[idx] = {"opp": opp, "eq": eq}
for k, v in sorted(stats.items()):
    print(k, v)
json.dump(per, open("two_term_relations_%s.json" % ("open" if sel is not None else "all"), "w"))
