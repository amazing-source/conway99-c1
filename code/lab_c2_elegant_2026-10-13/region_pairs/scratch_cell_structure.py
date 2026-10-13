import sys, os, json, itertools, collections
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\c2_elegant_2026-10-13\region_pairs")
import numpy as np
from rp_lib import Lattice, OUT
import rp_search as RS
lid = sys.argv[1]; idx = int(sys.argv[2])
lat = Lattice(lid); G = lat.G
scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
p = [q for q in scan["pairs"] if q["region"]][idx]
y1 = np.array(p["y1"]); y2 = np.array(p["y2"])
inst = RS.build_instance(lat, y1, y2, p); pk = RS.pack_instance(inst)
r = RS.run(pk, 4, node_limit=10**9, maxsol=5000)
Ha = pk["Ha"]; X3o = inst["X3o"]
pairs7 = list(itertools.combinations(range(7), 2))
emp = collections.Counter(); sh = collections.Counter()
for n_, sol in enumerate(r["sols"][:r["solutions"]]):
    Hs = Ha[sol]; M = (X3o @ G) @ Hs.T; nz = (M != 0)
    supp = nz.sum(axis=1)
    cells = {}
    for (c, d) in pairs7:
        others = [e for e in range(7) if e not in (c, d)]
        sel = nz[:, c] & nz[:, d] & (~nz[:, others].any(axis=1)) & (np.abs(M[:, c]) == 1) & (np.abs(M[:, d]) == 1)
        prod = M[sel, c] * M[sel, d]
        cells[(c, d)] = (int((prod == 1).sum()) // 2, int((prod == -1).sum()) // 2)
    empties = [(k, 'Same' if v[0] == 0 else 'Opp') for k, v in cells.items() for _ in [0] if v[0] == 0] + [(k, 'Opp') for k, v in cells.items() if v[1] == 0]
    key = tuple(sorted(e[1] for e in empties))
    emp[key] += 1
    if n_ < 3:
        print("solution", n_, "support-size histogram of the", len(X3o), "words:", dict(sorted(collections.Counter(supp.tolist()).items())))
        print("   cell counts (same,opp) up to sign:", [cells[k] for k in pairs7])
        print("   empty cells:", empties)
        vals = collections.Counter(map(tuple, np.sort(np.abs(M), axis=1)[:, ::-1][supp == 2][:, :2].tolist()))
        print("   support-2 words by |values|:", dict(vals))
print("empty-cell type histogram over all solutions:", dict(emp))
