"""Dump the seven-sets found by the exhaustive search (mode 4) for 044 region pairs 1 and 3, with their cell statistics.
<lab python> -B rp_dump_sevensets.py"""
import sys, os, json, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT
import rp_search as RS
lat = Lattice("044"); G = lat.G
scan = json.load(open(os.path.join(OUT, "scan_044.json")))
regs = [q for q in scan["pairs"] if q["region"]]
for idx in (1, 3):
    p = regs[idx]
    inst = RS.build_instance(lat, np.array(p["y1"]), np.array(p["y2"]), p); pk = RS.pack_instance(inst)
    r = RS.run(pk, 4, node_limit=10 ** 9, maxsol=1000)
    assert not r["node_limit_hit"] and r["solutions"] <= 1000
    sets = pk["Ha"][r["sols"][:r["solutions"]]]                       # (#sets, 7, 24) integer coordinates
    X3o = inst["X3o"]; empt = []
    for S in sets:
        M = (X3o @ G) @ S.T; nz = (M != 0); ne = 0
        for (c, d) in itertools.combinations(range(7), 2):
            others = [e for e in range(7) if e not in (c, d)]
            sel = nz[:, c] & nz[:, d] & (~nz[:, others].any(axis=1)) & (np.abs(M[:, c]) == 1) & (np.abs(M[:, d]) == 1)
            pr = M[sel, c] * M[sel, d]
            ne += int((pr == 1).sum() == 0) + int((pr == -1).sum() == 0)
        empt.append(ne)
    np.savez_compressed(os.path.join(OUT, "sevensets_044_row%d.npz" % p["row"]), sevensets=sets.astype(np.int16), empty_cells_of_42=np.array(empt), G=G.astype(np.int16),
                        y1=np.array(p["y1"], dtype=np.int16), y2=np.array(p["y2"], dtype=np.int16))
    print("044 row", p["row"], "seven-sets", len(sets), "empty cells (of 42) histogram", {int(k): int((np.array(empt) == k).sum()) for k in sorted(set(empt))})
