"""C1, lab session, 2026-10-08. Maximum of a targeted count (census_target.py) over the order-10 polytope enlarged by the
new parameters of the closure and the positivity of the closure types. Floating point HiGHS, exploration.
  python lp_target.py <census2 order-10 json> <target json> [divisor]
Prints the maximum of N(target) and of N(target) / divisor (e.g. 12 for prism+house: 12 tau <= N; 1 for prism+prism)."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); Tg = json.load(open(sys.argv[2])); div = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
npar0 = len(D["params"]); nnew = len(Tg["newparams"]); npar = npar0 + nnew; ri = []; ci = []; va = []; const = []; r = 0; seen = set()
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
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)
c = np.zeros(npar); k0 = 0.0
for p, v_ in Tg["form"].items():
    if int(p): c[int(p) - 1] = float(Fr(v_)) / Tg["aut"]
    else: k0 = float(Fr(v_)) / Tg["aut"]
res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
if res.status != 0: print("target %s: %s" % (Tg["target"], res.message[:80]))
else: print("target %s: %d + %d constraints, %d + %d parameters; maximum of N = %.8g, i.e. %.6g after division by %g; at the optimum P = %.5g  [%.0f s]" % (
    Tg["target"], r0, r - r0, npar0, nnew, -res.fun + k0, (-res.fun + k0) / div, div, res.x[0], time.time() - t0))
res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
if res.status == 0: print("   minimum of N = %.8g" % (res.fun + k0))
