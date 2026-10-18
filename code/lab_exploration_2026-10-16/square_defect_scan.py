"""Scan S7 key files (or catalogues) with Codex's square-defect detector (root_component_square_defect, main b6492b12):
find_obstruction(template) returns a certificate when a pair square H_ab = H_cd = -H_ac = -H_bd with two grids among the
three complementary rectangles and H_F = H_D (D disjoint) for the third holds; verify_certificate re-checks it exactly.
usage: python square_defect_scan.py <codex dir> <keys.gz | catalogue> <first> <last> <out.jsonl>"""
import json, sys, time
codex = sys.argv[1]
sys.path.insert(0, codex)
from root_component_square_defect import find_obstruction, verify_certificate, squares   # noqa: E402
from jhat_rows import records                                                           # noqa: E402
path, first, last, out = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
t0 = time.time(); n = sq = cert = 0
with open(out, "w") as fo:
    for i, t in enumerate(records(path)):
        if i < first: continue
        if i >= last or time.time() - t0 > 270: break
        t = t.get("template", t)
        n += 1
        s = squares(t)
        if s: sq += 1
        c = find_obstruction(t)
        if c:
            assert verify_certificate(t, c)
            cert += 1
            fo.write(json.dumps({"index": i, "key": t.get("key"), "k": 21 - len(t["nongrid_edges"])}) + "\n")
print(json.dumps({"source": path, "range": [first, i], "templates": n, "with_square": sq, "certificates": cert, "seconds": round(time.time() - t0, 1)}))
