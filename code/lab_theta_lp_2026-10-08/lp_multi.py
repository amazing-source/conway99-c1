"""C1, lab session, 2026-10-08. Maxima of P, H and the totals of special supports over the order-10 polytope enlarged by
a targeted closure (census_multi.py). Floating point HiGHS, exploration.
  python lp_multi.py <census2 order-10 json> <closure json>"""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); Tg = json.load(open(sys.argv[2])); npar0 = len(D["params"]); nnew = len(Tg["newparams"]); npar = npar0 + nnew
ri = []; ci = []; va = []; const = []; r = 0; seen = set()
def addrow(form):
    global r
    sig = tuple(sorted(form.items()))
    if sig in seen or not form: return
    seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values()); const.append(f.get(0, 0.0) / sc)
    for p, v_ in f.items():
        if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
    r += 1
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]: addrow(form)
r0 = r
for nn, kk, form in Tg["closure"]: addrow(form)
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const); orders = np.array([p[0] for p in D["params"]] + [p[0] for p in Tg["newparams"]])
print("constraints %d + %d, parameters %d + %d" % (r0, r - r0, npar0, nnew))
def mx(c, label):
    res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    print("   max %-36s = %s  [%.0f s]" % (label, "%.8g" % (-res.fun) if res.status == 0 else res.message[:50], time.time() - t0), flush=True)
c = np.zeros(npar); c[0] = 1; mx(c, "P")
c = np.zeros(npar); c[1] = 1; mx(c, "H")
for o in (8, 9): mx((orders == o).astype(float), "all order-%d special supports" % o)
