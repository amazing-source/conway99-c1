import sys, os, json, collections
sys.path.insert(0, r"C:\Users\RESEARCHER\Downloads\conway_c2_researcher2_start_2026_09_30\conway_c2_researcher2_start_2026_09_30\work\c2_elegant_2026-10-13\region_pairs")
import numpy as np
from rp_lib import Lattice, OUT
import rp_search as RS
out = {}
for lid in sys.argv[1:]:
    lat = Lattice(lid)
    scan = json.load(open(os.path.join(OUT, "scan_%s.json" % lid)))
    regs = [q for q in scan["pairs"] if q["region"]]
    res = []
    for idx, p in enumerate(regs):
        inst = RS.build_instance(lat, np.array(p["y1"]), np.array(p["y2"]), p)
        adm = inst["adm"]
        t = (np.abs(inst["P11"][adm]) == 1).sum(axis=1)
        res.append((int(t.min()), int(t.max()), p["s"]))
    c = collections.Counter(res)
    print(lid, "pairs", len(regs), "(min admissible hit-set size, max, s) -> number of pairs:", dict(c), "; 7*min > s for all:", all(7 * a > s for (a, b, s) in res))
