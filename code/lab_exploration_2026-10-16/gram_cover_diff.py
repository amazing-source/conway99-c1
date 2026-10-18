"""Explain the Grams that Codex's enumerator lists and the LAB cover does not (LAB, 18/10/2026).
For each such R (rebuilt from Codex's anchor block with Codex's lift), test every constraint of gram_cover_enum.py
separately and report which ones fail.  If one R fails none of them, the LAB enumeration is incomplete (a bug).
usage: python gram_cover_diff.py <codex dir> <catalogue> <template index> <LAB cover json> <seconds>"""
import gzip
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

codex, cat, ti, lab_path, secs = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4], float(sys.argv[5])
sys.path.insert(0, str(codex.resolve()))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cle3_gram as GR                                     # noqa: E402
from root_component_gram_enumeration import enumerate_grams  # noqa: E402


def psd(a):
    """Exact test for a symmetric rational matrix: pivot on the first diagonal entry (zero pivot needs a zero row)."""
    a = [row[:] for row in a]
    while a:
        p = a[0][0]
        if p < 0 or (p == 0 and any(a[0][1:])):
            return False
        if p == 0:
            a = [row[1:] for row in a[1:]]
        else:
            a = [[a[i][j] - a[i][0] * a[0][j] / p for j in range(1, len(a))] for i in range(1, len(a))]
    return True


data = json.load(gzip.open(cat, "rt") if cat.endswith(".gz") else open(cat))
t = dict(data["open"][ti]["template"] if "open" in data else data["templates"][ti])
edges, nodes, links = GR.template_graph(t)
t["component_graph_nodes"] = [[r, list(part)] for r, part in nodes]
t["component_graph_edges"] = [list(link) for link in links]
rec = enumerate_grams(t, secs, False)
lab = json.load(open(lab_path))
anchors, pairs = rec["anchors"], rec["anchor_pairs"]
d, m = len(anchors), len(edges)
lift = [[Fraction(p, q) for p, q in row] for row in rec["lift_matrix"]]
labset = {tuple(R[anchors[a]][anchors[b]] for a, b in pairs) for R in lab["grams"]}
fails = Counter()
unexplained = 0
for vals in rec["gram_anchor_values"]:
    if tuple(vals) in labset:
        continue
    X = [[0] * d for _ in range(d)]
    for (a, b), v in zip(pairs, vals):
        X[a][b] = X[b][a] = v
    R = [[sum(lift[i][a] * X[a][b] * lift[j][b] for a in range(d) for b in range(d)) for j in range(m)] for i in range(m)]
    assert all(x.denominator == 1 for row in R for x in row)
    R = [[int(x) for x in row] for row in R]
    if any(R[i][i] == 2 for i in range(m)):
        continue
    why = []
    for i in range(m):
        if R[i][i] not in (4, 6, 8):
            why.append("diag")
        for j in range(i):
            common = set(edges[i]) & set(edges[j])
            if not (-8 <= R[i][j] <= (0 if common else 4)):
                why.append("bounds")
            if common:
                root = next(iter(common))
                same = any(r == root and all((set(e) - {root}) <= set(part) for e in (edges[i], edges[j])) for r, part in nodes)
                if not same and R[i][j] != 0:
                    why.append("zero")
            if R[i][j] ** 2 > R[i][i] * R[j][j]:
                why.append("minor")
    cut_fail = []
    for node in range(len(nodes)):
        inc = [i for i, ends in enumerate(links) if node in ends]
        if any(sum(R[i][j] for i in inc) for j in range(m)):
            why.append("CR")
        if len(inc) >= 3:
            for size in range(1, len(inc)):
                for U in combinations(inc, size):
                    if inc[0] in U:
                        rest = [f for f in inc if f not in U]
                        w = sum(R[e][f] for e in U for f in rest)
                        if w > -2:
                            cut_fail.append((nodes[node][0], tuple(nodes[node][1]), [edges[e] for e in U], w))
    if cut_fail:
        why.append("connectivity")
    if sum(R[i][i] for i in range(m)) > 28 * d:
        why.append("trace")
    if not psd([[Fraction(x) for x in row] for row in R]):
        why.append("psd")
    if not psd([[Fraction(28 * (i == j) - R[i][j]) for j in range(m)] for i in range(m)]):
        why.append("upper28")
    key = tuple(sorted(set(why)))
    fails[key] += 1
    if not why:
        unexplained += 1
    elif cut_fail and len(fails) <= 3:
        print("example connectivity failure:", cut_fail[0])
print(json.dumps({"template_index": ti, "codex_only_after_E3_by_failed_constraints": {"+".join(k) or "NONE": v for k, v in fails.items()},
                  "unexplained": unexplained}))
