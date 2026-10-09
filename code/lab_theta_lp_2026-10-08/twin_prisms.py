"""C1, lab session, 2026-10-09. Twin prisms (two disjoint prisms X, Y with no edge between them) in an srg(99,14,1,2).

Hand part. X + Y induces a cubic graph, so 1_X - 1_Y is a sum-zero 3-eigenvector of the induced graph: equality case
of the positivity of 3I - A_H + J/9, hence a 3-eigenvector of A, and every vertex outside X + Y has as many neighbours
in X as in Y. Inside a prism the pairs (x_i, x_j'), i != j, already have two common neighbours, and the edges of the
two triangles have their third point inside; so an outside vertex meets a prism in nothing, one point, or one rung
(then it is the third point of that rung's line). Hence the three rung apices of X are the three rung apices of Y.

Machine part. The support X + Y + {a1, a2, a3} (15 points; a_i on rung i of both prisms) with e = 0, 1, 2 or 3 edges
among the apices (e = 3: the apices form a line, the two prisms are two grids through that line minus the line) is
tested with support_masks.verdict; exact certificates for the infeasible cases with certify_supports.certify.
  python twin_prisms.py"""
import json
import support_masks as S
import certify_supports as C
names = ["x1", "x2", "x3", "x1'", "x2'", "x3'", "y1", "y2", "y3", "y1'", "y2'", "y3'", "a1", "a2", "a3"]; ix = {s: i for i, s in enumerate(names)}
E0 = []
for p in ("x", "y"):
    for i, j in ((1, 2), (1, 3), (2, 3)):
        E0.append((ix["%s%d" % (p, i)], ix["%s%d" % (p, j)])); E0.append((ix["%s%d'" % (p, i)], ix["%s%d'" % (p, j)]))
    for i in (1, 2, 3):
        E0.append((ix["%s%d" % (p, i)], ix["%s%d'" % (p, i)])); E0.append((ix["a%d" % i], ix["%s%d" % (p, i)])); E0.append((ix["a%d" % i], ix["%s%d'" % (p, i)]))
out = {}
for label, extra in (("no edge among the apices", []), ("one edge a1-a2", [("a1", "a2")]), ("two edges a1-a2, a2-a3", [("a1", "a2"), ("a2", "a3")]),
                     ("three edges: the apices form a line (two grids on a line)", [("a1", "a2"), ("a2", "a3"), ("a1", "a3")])):
    E = E0 + [(ix[u], ix[v]) for u, v in extra]
    r = S.verdict(len(names), E); st = r["status"]
    if st.startswith("INFEASIBLE"):
        st, cert = C.certify(len(names), E); out[label] = {"status": st, "certificate": cert}
    else: out[label] = {"status": st}
    print("%-58s : %s%s" % (label, st, (" (masks %d, ranks %d %d)" % (r["masks"], r["rank_minus"], r["rank_plus"])) if "masks" in r else ""), flush=True)
json.dump(out, open("twin_prisms_certificates.json", "w"))
