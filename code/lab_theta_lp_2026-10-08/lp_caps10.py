"""C1, lab session, 2026-10-08. Maxima of the numbers of special supports (types of minimum degree >= 3) over the full
order-10 census polytope. Floating point HiGHS, exploration.
  python lp_caps10.py <census2 order-10 json>
Prints, for P, H, each of the seven 8-vertex parameters, and the totals by order, the maximum allowed by the positivity
of all type counts of orders 6 to 10, with the number of edges and |Aut| of the type."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values())
        const.append(f.get(0, 0.0) / sc)
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const); orders = np.array([p[0] for p in D["params"]])
def mx(c, label):
    res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    print("  max %-34s = %s  [%.0f s]" % (label, "%.8g" % (-res.fun) if res.status == 0 else res.message[:40], time.time() - t0), flush=True)
for i in range(9):
    n, key, rows = D["params"][i]; e = sum(bin(x).count("1") for x in rows) // 2; c = np.zeros(npar); c[i] = 1.0
    mx(c, "order %d, %d edges, |Aut| %d" % (n, e, C2.aut_order(n, rows)))
for o in (8, 9, 10): mx((orders == o).astype(float), "total number of order-%d supports" % o)
