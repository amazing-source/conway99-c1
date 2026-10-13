"""Independent verification of 7-sets found by the DFS, from scratch, on the full shells (no window, no class bookkeeping).

  <lab python> -B rp_verify_solution.py <lid> <region index> <mode> [number of solutions to verify=20]

For each found 7-set {h_1..h_7} (integer coordinate rows) it checks, with exact integer arithmetic:
  (1) (h_c, h_d) = 4 delta_cd, (h_c, y1) = (h_c, y2) = 0;
  (2) sum_c h_c in 2 Z^24 (so (1/2) sum h_c is in U);
  (3) for EVERY shadow vector b of norm 2 and of norm 4 (both signs, not only window representatives):
        (b, h_c) is an integer, sum_c (b, h_c) is odd, sum_c (b, h_c)^2 <= E(b) - 10.5;
  (4) for EVERY vector v of norm 2, 3, 4 of U: sum_c (v, h_c)^2 <= E(v)   (consequence of the frame identity (F), since the 42 u-terms are >= 0).
Shadow vectors of norm >= 6 are NOT checked (16.8 million of norm 6; the Bessel inequality sum_c (b,h_c)^2 <= 4 E(b)/7 shows the condition
is automatic for E(b) >= 24.5, but 17.5 <= E(b) <= 23.5 is not covered here)."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rp_lib import Lattice, OUT
import rp_search as RS

lid = sys.argv[1]; idx = int(sys.argv[2]); mode = int(sys.argv[3]); nver = int(sys.argv[4]) if len(sys.argv) > 4 else 20
lat = Lattice(lid); G = lat.G
scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
p = [q for q in scan["pairs"] if q["region"]][idx]
y1 = np.array(p["y1"], dtype=np.int64); y2 = np.array(p["y2"], dtype=np.int64)
inst = RS.build_instance(lat, y1, y2, p); pk = RS.pack_instance(inst)
r = RS.run(pk, mode, node_limit=10 ** 9, maxsol=nver)
print("pair row", p["row"], "mode", mode, "solutions", r["solutions"], "exhaustive", not r["node_limit_hit"], flush=True)
Ha = pk["Ha"]
nbad = 0
for sol in r["sols"][:nver]:
    Hs = Ha[sol]                                                  # 7 x 24
    assert (Hs @ G @ Hs.T == 4 * np.eye(7, dtype=np.int64)).all()
    assert (Hs @ G @ y1 == 0).all() and (Hs @ G @ y2 == 0).all()
    assert ((Hs.sum(axis=0)) % 2 == 0).all(), "sum h not in 2U"
    for k in (2, 4):
        V = lat.S[k]                                                # rows 2b
        P2 = lat.SG[k] @ Hs.T                                      # 2 (b, h_c)
        assert (P2 % 2 == 0).all()
        Pb = P2 // 2
        assert (Pb.sum(axis=1) % 2 != 0).all(), "sum of (b,h_c) not odd"
        p1 = lat.SG[k] @ y1; p2 = lat.SG[k] @ y2
        fourE = 28 * k - p1 * p1 - p2 * p2                          # 4 E(b)
        ss = (Pb ** 2).sum(axis=1)
        bad = int((4 * ss > fourE - 42).sum())                      # 4 sum <= 4E - 42
        nbad += bad
        if bad: print("  violation among shadow vectors of norm", k, ":", bad)
    for k in (2, 3, 4):
        P = lat.XG[k] @ Hs.T
        a = lat.XG[k] @ y1; b = lat.XG[k] @ y2
        E = 7 * k - a * a - b * b
        bad = int(((P ** 2).sum(axis=1) > E).sum()); nbad += bad
        if bad: print("  violation among U vectors of norm", k, ":", bad)
print("verified %d solutions on the full shells; violations: %d" % (min(nver, r["solutions"]), nbad))
