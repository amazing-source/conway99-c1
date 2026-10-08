"""C1, lab session, 2026-10-08. The 0/+-1 representatives of norm FOUR of M with support <= 10, over the order-10 census
polytope (floating point HiGHS, exploration).
  python lp_norm4.py <census2 order-10 json> <reps10 json>
Shapes (a,b) with Q = 4 and support <= 10 (hand check: 3n - 2E + ((a-b)/3)^2 = 4 leaves only these):
  (3,0) triangle; (6,0) prism; (6,3) prism minus far triangle; (9,0) 9-set with 16 edges; (8,2) 8-set with 14 edges minus
  far edge. Each count below is the number of pairs (W, Y) (one sign). Prints min and max of each over the polytope, and
  the maximum of Phi = #(prism, far triangle) with the bound tau <= Phi / 4 (laptop session: a prism in a class of m twins
  has at least 2(m-1) far triangles), alone and at the corner P = max."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2]))
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
def opt(c, k0, sign, extra=None):
    Aub, bub = (-A, const)
    if extra is not None:
        from scipy.sparse import vstack
        Aub = vstack([-A, csr_matrix(-extra[0].reshape(1, -1))]); bub = np.append(const, -extra[1])
    res = linprog(sign * c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * npar, method="highs-ipm")
    return (sign * res.fun + k0, res.x) if res.status == 0 else (None, None)
print("shapes with Q = 4 present in the file:", sorted(k_ for k_ in R if k_.endswith(",4")))
for k_ in sorted(k_ for k_ in R if k_.endswith(",4")):
    c, k0 = vec(R[k_]); lo, _ = opt(c, k0, 1); hi, x = opt(c, k0, -1)
    print("  shape (%s): constant %.6g, %d parameters; min %.6g, max %.6g (P = %.5g at the max)  [%.0f s]" % (k_, k0, int((c != 0).sum()), lo, hi, x[0], time.time() - t0), flush=True)
c, k0 = vec(R["6,3,4"]); eP = np.zeros(npar); eP[0] = 1.0
hi, x = opt(c, k0, -1); print("Phi = #(prism, far triangle): max %.6g, so tau <= %.6g" % (hi, hi / 4))
for lam in (4.0, 8.0, 10.0, 12.0):
    hi, x = opt(c - lam * eP, k0, -1); print("  max of Phi - %g P = %.6g (P = %.5g, Phi = %.6g)" % (lam, hi, x[0], c @ x + k0))
for Pmin in (800.0, 850.0):
    hi, x = opt(c, k0, -1, extra=(eP, Pmin)); print("  with P >= %g: max Phi = %.6g, i.e. Phi / P <= %.4g and tau <= %.6g" % (Pmin, hi, hi / Pmin, hi / 4))
