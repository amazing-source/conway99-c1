"""C1, lab session, 2026-10-08. Rank 37, exploration: all representatives with support <= 9 EXCEPT the shape (6,3)/(3,6)
(the only one exposed to mass-9 collisions with many pairs per twin pair), with penalties per special support.

  python lp_no63.py <census2 order-10 json> <reps10 json> <l6> <l7> <l8> <l9>   [with63]

Shapes kept: everything with support <= 8, and the 9-sets (9,0)/(0,9) in full. For the pure indicators a mass-9
collision is exactly one pair per twin pair of special 9-supports with the right number of edges. Penalties l6..l9 per
special support of order 6..9. Floating point HiGHS, exploration; no penalty constant is proved here."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); pens = [float(x) for x in sys.argv[3:7]]; with63 = "with63" in sys.argv
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
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const); orders = np.array([p[0] for p in D["params"]])
c8 = np.zeros(npar); k8 = 0.0; c6 = np.zeros(npar); k6 = 0.0
for k_, f in R.items():
    a, b, q = [int(x) for x in k_.split(",")]
    if a + b > 9 or q == 4 or (not with63 and {a, b} == {3, 6}): continue
    for p, v_ in f.items():
        val = float(Fr(v_))
        if q == 8:
            if int(p): c8[int(p) - 1] += val
            else: k8 += val
        else:
            if int(p): c6[int(p) - 1] += val
            else: k6 += val
pen = np.zeros(npar)
for o, l in zip((6, 7, 8, 9), pens): pen[orders == o] = l
res = linprog(c8 + (651 / 34) * c6 - pen, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm"); x = res.x
print("%s, penalties %s: minimum = %.8g ; r6 = %.6g, r8 = %.8g ; supports by order 6..10: %s  [%.0f s]" % (
    "with (6,3)" if with63 else "without (6,3)", pens, res.fun + k8 + (651 / 34) * k6, c6 @ x + k6, c8 @ x + k8, ", ".join("%.6g" % x[orders == o].sum() for o in (6, 7, 8, 9, 10)), time.time() - t0), flush=True)
