"""C1, lab session, 2026-10-08. Rank 37, exploration: how much collision loss PER SPECIAL SUPPORT can be afforded?

  python lp_penalty10.py <census2 order-10 json> <reps10 json> [lambda ...]
  python lp_penalty10.py <census2 order-10 json> <reps10 json> orders <max support> <l6> <l7> <l8> <l9> <l10>
      second form: only the representatives with support <= max support, and a penalty l_o per special support of order o

A t = 0 collision between two 0/+-1 representatives needs a positive support of minimum degree >= 3 (binary case), i.e.
a copy of one of the 549 parameter types (orders 6 to 10). If every copy of such a type costs at most lambda colliding
pairs, the number of classes is at least  R(theta) - lambda * sum_p theta_p  (theta_p = number of copies of the type p).
This script minimises, over the order-10 census polytope, the coupled form
    [r8 + (651/34) r6](theta) - lambda * (sum of all parameters)
for several lambda, and also prints the shape-by-shape composition at lambda = 0. Floating point, exploration only: no
per-support bound lambda is proved here, and the weighted (windmill) and t = 1 (grid) channels are not included."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); BYORD = len(sys.argv) > 3 and sys.argv[3] == 'orders'
lams = [0.0] if BYORD else ([float(x) for x in sys.argv[3:]] or [0, 1e3, 1e4, 1e5])
MAXS = int(sys.argv[4]) if BYORD else 10
npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set()
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
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
shape = {k_: vec(f) for k_, f in R.items() if int(k_.split(',')[0]) + int(k_.split(',')[1]) <= MAXS}
c8 = sum(v_[0] for k_, v_ in shape.items() if k_.endswith(",8")); k8 = sum(v_[1] for k_, v_ in shape.items() if k_.endswith(",8"))
c6 = sum(v_[0] for k_, v_ in shape.items() if k_.endswith(",6")); k6 = sum(v_[1] for k_, v_ in shape.items() if k_.endswith(",6"))
orders = np.array([p[0] for p in D["params"]])
for lam in lams:
    pen = np.array([float(sys.argv[5 + (o - 6)]) for o in orders]) if BYORD else lam * np.ones(npar)
    c = c8 + (651 / 34) * c6 - pen
    res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    if res.status != 0: print("lambda = %g: status %d (%s)" % (lam, res.status, res.message[:70]), flush=True); continue
    x = res.x
    print("penalties %s: minimum of [r8 + (651/34) r6 - penalties] = %.6g ; r6 = %.6g, r8 = %.6g ; numbers of special supports by order 6..10: %s  [%.0f s]" % (
        (sys.argv[5:10] if BYORD else lam), res.fun + k8 + (651 / 34) * k6, c6 @ x + k6, c8 @ x + k8, ", ".join("%.6g" % x[orders == o].sum() for o in (6, 7, 8, 9, 10)), time.time() - t0), flush=True)
    if lam == 0:
        for k_ in sorted(shape, key=lambda s: (int(s.split(",")[2]), int(s.split(",")[0]) + int(s.split(",")[1]), s)):
            if not k_.endswith(",4"): print("     shape (%s): %.6g" % (k_, shape[k_][0] @ x + shape[k_][1]))
