"""C1, lab session, 2026-10-08. Rank 37, exploration: the "clean" part of the representatives.

  python lp_clean9.py <census2 order-10 json> <reps10 json> [l6 l7 l8]

Clean part = all 0/+-1 representatives of norm 6 and 8 with support <= 8 (their t = 0 collisions involve only special
supports of order <= 8) + the 2-degenerate 9-sets with 14 edges, both signs (no t = 0 collision among indicators).
Minimum over the full order-10 polytope of r8 + (651/34) r6 restricted to that part, minus optional penalties per prism,
per D and per order-8 special support. Floating point HiGHS, exploration: the cross-collisions between sums differing
by 9 (grids) are not removed, and no penalty constant is proved here."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); pens = [float(x) for x in sys.argv[3:6]] if len(sys.argv) > 5 else [0.0, 0.0, 0.0]
npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set(); pc = lambda x: bin(x).count("1")
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
def two_degenerate(n, rows):
    alive = (1 << n) - 1
    while alive:
        for v in range(n):
            if alive >> v & 1 and pc(rows[v] & alive) <= 2: alive &= ~(1 << v); break
        else: return False
    return True
c8 = np.zeros(npar); k8 = 0.0; c6 = np.zeros(npar); k6 = 0.0
for k_, f in R.items():
    a, b, q = [int(x) for x in k_.split(",")]
    if a + b > 8 or q == 4: continue
    for p, v_ in f.items():
        val = float(Fr(v_))
        if q == 8:
            if int(p): c8[int(p) - 1] += val
            else: k8 += val
        else:
            if int(p): c6[int(p) - 1] += val
            else: k6 += val
base8 = k8
for key, rows, aut, form in D["types"]["9"]:
    if sum(pc(x) for x in rows) // 2 == 14 and two_degenerate(9, rows):
        for p, v_ in form.items():
            val = 2 * float(Fr(v_)) / aut
            if int(p): c8[int(p) - 1] += val
            else: k8 += val
pen = np.zeros(npar)
for o, l in zip((6, 7, 8), pens): pen[orders == o] = l
c = c8 + (651 / 34) * c6 - pen
res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm"); x = res.x
print("penalties (prism, D, order-8 support) = %s: minimum of the clean coupled count = %.8g ; r6 = %.6g, r8 = %.8g (constant terms: supports <= 8: %.8g, with the 2-degenerate 9-sets: %.8g); supports by order 6..10: %s  [%.0f s]" % (
    pens, res.fun + k8 + (651 / 34) * k6, c6 @ x + k6, c8 @ x + k8, base8, k8, ", ".join("%.6g" % x[orders == o].sum() for o in (6, 7, 8, 9, 10)), time.time() - t0), flush=True)
