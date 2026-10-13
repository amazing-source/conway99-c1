"""Necessary 'word cell' test for the 7-sets found by the DFS (mode 4 by default).

In a frame the 42 words u_o (norm 3, orthogonal to y1,y2) have (h_c, u_o) = -C_co where the 42 columns of C are e_i + e_j and e_i - e_j (i<j) of Z^7:
each word pairs non-trivially with exactly two of the seven h, with values +-1, and for every pair {c,d} and each of the two signs exactly one word
exists.  So a 7-set {h_c} can be part of a frame only if, for each of the 21 pairs {c,d} and each sign (Same: product of the two values = +1,
Opp: = -1), at least one vector u of norm 3 orthogonal to y1, y2 has (h_c,u), (h_d,u) = +-1 and (h_e,u) = 0 for the other five e.
(This is rule 16/18 'empty cells' of the old engine, AE table; it uses only the lattice.)  A further necessary condition checked here: the word must be
compatible with the shadow bound sum_o (b,u_o)^2 >= 10.5: no condition is used, so the test below is weaker than the engine.
<lab python> -B rp_cells.py <lid> <region index> <mode>"""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT
import rp_search as RS

lid = sys.argv[1]; idx = int(sys.argv[2]); mode = int(sys.argv[3]) if len(sys.argv) > 3 else 4
lat = Lattice(lid); G = lat.G
scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
p = [q for q in scan["pairs"] if q["region"]][idx]
y1 = np.array(p["y1"], dtype=np.int64); y2 = np.array(p["y2"], dtype=np.int64)
inst = RS.build_instance(lat, y1, y2, p); pk = RS.pack_instance(inst)
r = RS.run(pk, mode, node_limit=10 ** 9, maxsol=5000)
print("pair row", p["row"], "mode", mode, "solutions", r["solutions"], "exhaustive", not r["node_limit_hit"], flush=True)
Ha = pk["Ha"]
X3o = inst["X3o"]                                       # norm-3 vectors orthogonal to y1, y2 (both signs)
print("norm-3 vectors orthogonal to y1,y2 (both signs):", len(X3o), "(= N3)")
alive = 0; stats = []
pairs7 = list(itertools.combinations(range(7), 2))
for sol in r["sols"][:r["solutions"]]:
    Hs = Ha[sol]
    M = (X3o @ G) @ Hs.T                                # n3 x 7
    assert (np.abs(M) <= 2).all()
    nz = (M != 0)
    ok = True; minc = 10 ** 9; counts = []
    for (c, d) in pairs7:
        others = [e for e in range(7) if e not in (c, d)]
        sel = nz[:, c] & nz[:, d] & (~nz[:, others].any(axis=1)) & (np.abs(M[:, c]) == 1) & (np.abs(M[:, d]) == 1)
        prod = M[sel, c] * M[sel, d]
        same = int((prod == 1).sum()) // 2; opp = int((prod == -1).sum()) // 2       # up to sign of u
        counts.append((same, opp))
        minc = min(minc, same, opp)
        if same == 0 or opp == 0: ok = False
    stats.append((ok, minc, sum(1 for (a, b) in counts if a == 0 or b == 0)))
    alive += ok
print("7-sets with all 42 word cells non-empty:", alive, "of", r["solutions"])
import collections
print("number of empty cells (of 42) per 7-set, histogram:", dict(sorted(collections.Counter(x[2] for x in stats).items())))
