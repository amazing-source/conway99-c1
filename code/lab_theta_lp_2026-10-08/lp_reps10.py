"""C1, lab session, 2026-10-08. BEST-CASE test for rank 37: minimum over the order-10 census polytope of the number of
0/+-1 representatives of small norm with support <= 10 (no collision removed). Floating point, exploration only.

  python lp_reps10.py <census2 order-10 json> <reps10 json> <objective> [method]
  objective: r8 | r6 | coupled (r8 + (651/34) r6) | r4 ; method: highs (default), highs-ipm, highs-ds

If even this best-case minimum is below the rank-37 ceiling (16.47 million for r8 at b_3 = 45528; 17.40 million for the
coupled form), the family approach with supports <= 10 cannot conclude; if it is far above, the question is only how many
representatives collide."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); what = sys.argv[3]; method = sys.argv[4] if len(sys.argv) > 4 else "highs"
npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue                              # an empty form is a type whose count vanishes identically
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values()) or 1.0
        const.append(f.get(0, 0.0) / sc)
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)
tot = {4: {}, 6: {}, 8: {}}
for k_, f in R.items():
    q = int(k_.split(",")[2])
    for p, v_ in f.items(): tot[q][int(p)] = tot[q].get(int(p), 0) + Fr(v_)
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if p: c[p - 1] = float(v_)
    return c, float(form.get(0, 0))
c8, k8 = vec(tot[8]); c6, k6 = vec(tot[6]); c4, k4 = vec(tot[4])
print("constraints %d (distinct forms), parameters %d; constants: r4 %.6g, r6 %.6g, r8 %.6g  [%.0f s]" % (r, npar, k4, k6, k8, time.time() - t0), flush=True)
if what == "r8": c, k0 = c8, k8
elif what == "r6": c, k0 = c6, k6
elif what == "r4": c, k0 = c4, k4
else: c, k0 = c8 + (651 / 34) * c6, k8 + (651 / 34) * k6
res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method=method)
print("objective %s, method %s: status %d (%s)" % (what, method, res.status, res.message[:60]), flush=True)
if res.status == 0:
    x = res.x; print("  minimum = %.9g ; at the optimum: r4 = %.6g, r6 = %.6g, r8 = %.6g ; P = %.6g, H = %.6g ; smallest constraint value %.3g  [%.0f s]" % (
        res.fun + k0, c4 @ x + k4, c6 @ x + k6, c8 @ x + k8, x[0], x[1], float((A @ x + const).min()), time.time() - t0), flush=True)
    np.save(sys.argv[2] + "." + what + ".npy", x)
