"""Row-system filters of a root template (LAB, 18/10/2026), no Gram matrix, no budget, no solver.
For a label w in Q_q, its counts z_w(F) = |N(w) cap Q_F| (21 numbers) satisfy the component equations of the 7 root
lines (Codex's row_catalogue: C z = b_q, 0 <= z_F <= 2 if F shares a line with q, <= 4 otherwise).
  FORCED_GRID     : for a non-grid rectangle Q, every integral row of its corners has own count z(Q) = 2, or more
                    generally the set D of possible own counts supports no corner degree histogram of a simple graph
                    with e <= 2 edges ((4,0,0), (2,2,0), (0,4,0), (1,2,1) as (n0, n1, n2)).  Then e(Q) = 4: Q would be a
                    prism, i.e. a grid -- contradiction with the template (E3 also excludes e = 3).
  EMPTY_ROWS      : some rectangle has no integral row at all.
  MOMENT_1RECT    : the one-rectangle count system of single_rect_lemma.py (corner multiset, block symmetry, diagonal
                    moment sum_w C(z_w(Q), 2) = 8 - e(Q), degree histogram) has no solution for some rectangle.
usage: python row_forcing.py <codex dir> <catalogue (open/survivors/templates)> <first> <last> [--moment] > out.jsonl"""
import gzip
import json
import sys
from itertools import combinations
from pathlib import Path

codex, cat, first, last = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
moment = "--moment" in sys.argv
sys.path.insert(0, str(codex.resolve()))
from root_component_z_distribution import row_catalogue     # noqa: E402  (Codex, exact)

RECT = list(combinations(range(7), 2))
OK = [(4, 0, 0), (2, 2, 0), (0, 4, 0), (1, 2, 1)]
raw = Path(cat).read_bytes()
doc = json.loads(gzip.decompress(raw) if cat.endswith(".gz") else raw)
recs = doc.get("open") or doc.get("survivors") or doc.get("templates")
if moment:
    import runpy
    here = Path(__file__).resolve().parent
for idx in range(first, min(last, len(recs))):
    rec = recs[idx]
    t = rec.get("template", rec)
    cat_ = row_catalogue(t, max_free=21)
    out = {"index": idx, "c": t["component_count_by_root_line"], "k": 21 - len(t["nongrid_edges"]),
           "dim": t["kernel_dimension"]}
    if cat_["status"] != "ROW_CATALOGUE_COMPLETE":
        out.update(status=cat_["status"])
        print(json.dumps(out), flush=True)
        continue
    out["free_dimension"] = cat_["free_dimension"]
    nongrid = {tuple(e) for e in t["nongrid_edges"]}
    verdict = None
    for qi, q in enumerate(RECT):
        st = cat_["row_types"][qi]["states"]
        if not st:
            verdict = {"status": "EMPTY_ROWS", "rectangle": q}
            break
        if q in nongrid:
            dom = sorted({s[qi] for s in st})
            if not any(all(n == 0 or v in dom for v, n in enumerate(h)) for h in OK):
                verdict = {"status": "FORCED_GRID", "rectangle": q, "own_counts": dom}
                break
    out.update(verdict or {"status": "PASSES_ROW_FILTERS"})
    print(json.dumps(out), flush=True)
