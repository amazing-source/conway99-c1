import sys, os, json, itertools, collections, time
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\c2_elegant_2026-10-13\region_pairs")
import numpy as np
from rp_lib import Lattice, OUT
import rp_search as RS
lid = sys.argv[1]; idx = int(sys.argv[2]); lim = int(float(sys.argv[3]))
lat = Lattice(lid); G = lat.G
scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
p = [q for q in scan["pairs"] if q["region"]][idx]
inst = RS.build_instance(lat, np.array(p["y1"]), np.array(p["y2"]), p); pk = RS.pack_instance(inst)
print("pair row", p["row"], "s", pk["s"], "admissible", pk["n"])
# (a) exact cover without orthogonality
pk2 = dict(pk); n = pk["n"]
full = np.zeros_like(pk["orthbits"]); 
for w in range(n):
    full[:, w >> 6] |= np.uint64(1) << np.uint64(w & 63)
for v in range(n): full[v, v >> 6] &= ~(np.uint64(1) << np.uint64(v & 63))
pk2["orthbits"] = full
t = time.time()
r = RS.run(pk2, 0, node_limit=lim, maxsol=5)
print("7 admissible h with disjoint hit sets covering all E=11.5 classes, NO orthogonality required:", r["solutions"], "nodes", r["nodes"], "limit_hit", r["node_limit_hit"], round(time.time()-t,1), "s")
# also exact cover with fewer than 7 sets? (hit-set sizes)
t11 = np.array([bin(int(x)).count("1") for x in pk["h11"]])
print("hit-set sizes: min", t11.min(), "max", t11.max(), "s =", pk["s"])
# (b) with orthogonality, exhaustive E11
t = time.time()
r = RS.run(pk, 0, node_limit=lim, maxsol=5)
print("WITH orthogonality: solutions", r["solutions"], "nodes", r["nodes"], "limit_hit", r["node_limit_hit"], round(time.time()-t,1), "s")
