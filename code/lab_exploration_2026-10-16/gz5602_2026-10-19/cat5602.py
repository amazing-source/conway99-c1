"""Row catalogue of gz 5602 (c = 3, dimension 7, J = K7 minus C4 0-1-3-2 and C3 4-5-6), LAB 19/10/2026.
Rows h = base - z on the 14 non-grid rectangles, zero sum at every root (one block per root), boxes of the class."""
import gzip, json, sys
from collections import Counter
sys.path.insert(0, "..")
from jhat_rows import block_graph, RECT
from jhat_catalogue import rows_of_class
cat = json.load(gzip.open("../c3_root_cover/c3_open_templates_k3_12.json.gz"))["open"]
t = cat[5602]["template"]
g = block_graph(t); E = sorted(g[0])
print("non-grid edges", ["%d%d" % e for e in E])
print("blocks", t["nontrivial_component_groups"])
rows = {}
for q in RECT:
    rs = rows_of_class(g, q)
    rows[q] = [tuple(r[e] for e in E) for r in rs]
    print("%d%d" % q, "grid" if q not in E else "    ", len(rows[q]))
json.dump({"edges": ["%d%d" % e for e in E], "rows": {"%d%d" % q: rows[q] for q in RECT}}, open("cat5602.json", "w"))
