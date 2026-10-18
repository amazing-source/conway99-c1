"""Cross-check of a LAB Gram cover (gram_cover_enum.py / gram_cover_enum2.py) against Codex's own enumerator
(LAB, 18/10/2026).
Codex's root_component_gram_enumeration.enumerate_grams is run unchanged on the same template (its component graph
is given in Codex's keys, built as in cle3_gram.template_graph).  Codex does not use E3 (it allows R_ii = 2 under the
budget) nor the connectivity cuts.  So, rebuilding each full R from Codex's anchor block with Codex's own lift:
  - every LAB R must be in Codex's list ('only_lab' = 0);
  - every Codex R with all R_ii != 2 that the LAB list lacks must violate a LAB constraint; each one is tested
    constraint by constraint, and 'unexplained' counts those that violate none (must be 0: else the LAB cover misses
    an allowed R and is not complete).
usage: python gram_cover_crosscheck.py <codex dir> <catalogue> <template index> <LAB cover json> <seconds> <out.json>"""
import gzip
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

codex, cat, ti, lab_path, secs, out = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), sys.argv[4], float(sys.argv[5]), sys.argv[6]
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
lab = json.load(gzip.open(lab_path, "rt") if lab_path.endswith(".gz") else open(lab_path))
assert lab["template_index"] == ti and [tuple(e) for e in lab["edges"]] == edges
assert lab["anchors"] == rec["anchors"], (lab["anchors"], rec["anchors"])
anchors, pairs = rec["anchors"], rec["anchor_pairs"]
d, m = len(anchors), len(edges)
lift = [[Fraction(p, q) for p, q in row] for row in rec["lift_matrix"]]
labset = {tuple(R[anchors[a]][anchors[b]] for a, b in pairs) for R in lab["grams"]}
incs = [[i for i, ends in enumerate(links) if node in ends] for node in range(len(nodes))]


def violated(R):
    why = set()
    for i in range(m):
        if R[i][i] not in (4, 6, 8):
            why.add("diag")
        for j in range(i):
            common = set(edges[i]) & set(edges[j])
            if not (-8 <= R[i][j] <= (0 if common else 4)):
                why.add("bounds")
            if common:
                root = next(iter(common))
                same = any(r == root and all((set(e) - {root}) <= set(part) for e in (edges[i], edges[j])) for r, part in nodes)
                if not same and R[i][j] != 0:
                    why.add("zero")
            if R[i][j] ** 2 > R[i][i] * R[j][j]:
                why.add("minor")
    for inc in incs:
        if any(sum(R[i][j] for i in inc) for j in range(m)):
            why.add("CR")
        if len(inc) >= 3:
            for size in range(1, len(inc)):
                for U in combinations(inc, size):
                    if inc[0] in U and sum(R[e][f] for e in U for f in inc if f not in U) > -2:
                        why.add("connectivity")
    if sum(R[i][i] for i in range(m)) > 28 * d:
        why.add("trace")
    if not psd([[Fraction(x) for x in row] for row in R]):
        why.add("psd")
    if not psd([[Fraction(28 * (i == j) - R[i][j]) for j in range(m)] for i in range(m)]):
        why.add("upper28")
    return why


kept, dropped, reasons, unexplained = set(), 0, Counter(), 0
for vals in rec["gram_anchor_values"]:
    X = [[0] * d for _ in range(d)]
    for (a, b), v in zip(pairs, vals):
        X[a][b] = X[b][a] = v
    R = [[sum(lift[i][a] * X[a][b] * lift[j][b] for a in range(d) for b in range(d)) for j in range(m)] for i in range(m)]
    assert all(x.denominator == 1 for row in R for x in row)
    R = [[int(x) for x in row] for row in R]
    if any(R[i][i] == 2 for i in range(m)):
        dropped += 1
        continue
    kept.add(tuple(vals))
    if tuple(vals) not in labset:
        why = violated(R)
        reasons["+".join(sorted(why)) or "NONE"] += 1
        unexplained += not why
res = {"template_index": ti, "codex_status": rec["status"], "codex_exhaustive": rec["exhaustive"],
       "codex_gram_count": rec["gram_count"], "codex_with_R_ii_2": dropped, "codex_after_E3": len(kept),
       "lab_status": lab["status"], "lab_gram_count": len(labset), "equal": kept == labset,
       "only_codex": len(kept - labset), "only_lab": len(labset - kept), "only_codex_reasons": dict(reasons),
       "unexplained": unexplained, "codex_seconds": round(rec["seconds"], 1),
       "verdict": ("LAB_COVER_CONFIRMED" if rec["exhaustive"] and not (labset - kept) and unexplained == 0
                   else "NOT_CONFIRMED")}
json.dump(res, open(out, "w"))
print(json.dumps(res))
