"""C1, lab session, 2026-10-08. The eleven special 9-supports with 14 edges: structure and maxima over the order-10 polytope.
  python lp_caps9.py <census2 order-10 json>
For each: degrees, number of triangles, 4-cycles, |Aut|, whether it contains a prism / a copy of D / a cubic 8-support /
any special support of smaller order (if not it is a MINIMAL special support), and the LP maximum of its number of copies
(floating point HiGHS, exploration)."""
import sys, json, time, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set(); pc = lambda x: bin(x).count("1")
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values())
        const.append(f.get(0, 0.0) / sc)
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)
def sub_min3(n, rows, size):
    out = 0
    for S in itertools.combinations(range(n), size):
        m = sum(1 << i for i in S)
        if all(pc(rows[i] & m) >= 3 for i in S): out += 1
    return out
for i, (n, key, rows) in enumerate(D["params"]):
    e = sum(pc(x) for x in rows) // 2
    if n != 9 or e != 14: continue
    tri = sum(1 for a, b, c in itertools.combinations(range(9), 3) if rows[a] >> b & 1 and rows[a] >> c & 1 and rows[b] >> c & 1)
    c4 = sum(1 for a, b in itertools.combinations(range(9), 2) if not rows[a] >> b & 1 and pc(rows[a] & rows[b]) == 2) // 2
    subs = [sub_min3(9, rows, s) for s in (6, 7, 8)]
    c = np.zeros(npar); c[i] = 1.0; res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    print("14-edge 9-support %2d: triangles %d, 4-cycles %d, |Aut| %d, special sub-supports of order 6/7/8: %s%s; LP maximum %.7g  [%.0f s]" % (
        i, tri, c4, C2.aut_order(9, rows), subs, "  MINIMAL" if not any(subs) else "", -res.fun, time.time() - t0), flush=True)
