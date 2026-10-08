"""C1, lab session, 2026-10-08. Largest value of each census parameter of small order when the graph has no prism (P = 0).
  python census_param_max.py <census2 order-10 json> <out json> <max order of the parameters> [pcap]
Parameters = unlabelled counts of the admissible types of minimum degree >= 3 (census2.py). Polytope: every induced count
of orders 6 to 10 is non-negative, plus P <= pcap (default 0). Floating LP (HiGHS), diagnostic; used to size the collision
channels that survive without prisms (NOTE 17.73 A). One process, below 2 GB."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import linprog
t0 = time.time(); C = json.load(open(sys.argv[1])); npar = len(C["params"]); maxo = int(sys.argv[3]); pcap = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
ri, ci, va, const = [], [], [], []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in C["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v)) for p, v in form.items()}; sc = max(abs(x) for x in f.values()); const.append(f.get(0, 0.0) / sc)
        for p, v in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(-v / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); b = np.array(const); bounds = [(0, pcap)] + [(0, None)] * (npar - 1); out = {}
for i, (order, key, rows) in enumerate(C["params"]):
    if order > maxo: continue
    c = np.zeros(npar); c[i] = -1.0; o = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs-ipm")
    deg = sorted(bin(x).count("1") for x in rows); out[i + 1] = {"order": order, "key": key, "edges": sum(deg) // 2, "degrees": deg, "max": None if o.status else round(-o.fun, 1)}
    print("parameter %d: order %d, %d edges, degrees %s, key %d: max %s   [%.0f s]" % (i + 1, order, sum(deg) // 2, "".join(map(str, deg)), key, out[i + 1]["max"], time.time() - t0), flush=True)
json.dump({"pcap": pcap, "params": out}, open(sys.argv[2], "w"), indent=0)
