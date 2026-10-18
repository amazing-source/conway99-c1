"""Features of the c = 3 templates (gz catalogue) still open in the ledger versus the excluded ones (LAB 18/10/2026).
usage: python survivor_features.py <c3_open_templates_k3_12.json.gz> <open.tsv>"""
import gzip, json, sys
from collections import Counter
recs = json.load(gzip.open(sys.argv[1]))["open"]
open_ = {int(l.split()[1]) for l in open(sys.argv[2]) if l.startswith("gz")}
def feats(t):
    cc = t["component_count_by_root_line"]
    groups = t["nontrivial_component_groups"]
    sizes = [len(b) for g in groups for b in g]
    deg = Counter()
    for a, b in t["nongrid_edges"]:
        deg[a] += 1; deg[b] += 1
    return {"k": 21 - len(t["nongrid_edges"]), "dim": t["kernel_dimension"], "pairs": sizes.count(2),
            "big": max(sizes) if sizes else 0, "n3": sizes.count(3), "n4": sizes.count(4),
            "allgrid": cc.count(6), "c3lines": cc.count(3), "cprof": "".join(map(str, sorted(cc))),
            "mindegJ": min(deg[i] for i in range(7)), "maxdegJ": max(deg[i] for i in range(7))}
F = {i: feats(r["template"]) for i, r in enumerate(recs)}
O = [F[i] for i in F if i in open_]; X = [F[i] for i in F if i not in open_]
print("open", len(O), "excluded", len(X))
for key in ["k", "dim", "pairs", "big", "n3", "n4", "allgrid", "c3lines", "mindegJ", "maxdegJ"]:
    co = Counter(f[key] for f in O); cx = Counter(f[key] for f in X)
    vals = sorted(set(co) | set(cx))
    print(key.ljust(8), " ".join("%s:%d/%d(%.0f%%)" % (v, co[v], co[v] + cx[v], 100 * co[v] / (co[v] + cx[v])) for v in vals))
co = Counter(f["cprof"] for f in O); cx = Counter(f["cprof"] for f in X)
print("c-profiles (open/total), most frequent among open:")
for v, n in co.most_common(15):
    print("   ", v, "%d/%d" % (n, n + cx[v]))
# joint: dim x pairs
print("dim x pairs survival (open/total):")
for d in sorted({f["dim"] for f in F.values()}):
    row = []
    for p in range(0, 12):
        o = sum(1 for f in O if f["dim"] == d and f["pairs"] == p); t = o + sum(1 for f in X if f["dim"] == d and f["pairs"] == p)
        if t: row.append("p%d:%d/%d" % (p, o, t))
    print("  dim", d, " ".join(row))
