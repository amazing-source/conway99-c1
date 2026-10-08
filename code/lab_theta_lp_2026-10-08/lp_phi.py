"""C1, lab session, 2026-10-08. Rank 37, exploration: the twin-prism losses charged to Phi = #(prism, far triangle).
  python lp_phi.py <census2 order-10 json> <reps10 json> <max support> [mu ...] [x<a>,<b> ...]   (x6,3 drops the shapes (6,3) and (3,6))
tau <= Phi / 4 (laptop session), Phi a linear form of the order-9 census. If the twin-prism collisions cost at most
c per twin pair, the number of classes is at least R - (c / 4) Phi. Minimises r8 - mu Phi and
r8 + (651/34) r6 - mu Phi over the order-10 polytope (mu = c / 4). Floating point HiGHS. Ceilings to beat at rank 37
(Codex note 189): b4 <= 211010055/13 = 16 231 542.7 and b4 + (651/34) b3 <= 17 153 604.3."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); MAXS = int(sys.argv[3]); EXCL = [tuple(int(y) for y in x[1:].split(",")) for x in sys.argv[4:] if x.startswith("x")]; mus = [float(x) for x in sys.argv[4:] if not x.startswith("x")] or [0.0]
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
c8 = np.zeros(npar); k8 = 0.0; c6 = np.zeros(npar); k6 = 0.0
for k_, f in R.items():
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > MAXS or (a_, b_) in EXCL or (b_, a_) in EXCL: continue
    cc, kk = vec(f)
    if q_ == 8: c8 += cc; k8 += kk
    if q_ == 6: c6 += cc; k6 += kk
cphi, kphi = vec(R["6,3,4"]); orders = np.array([p[0] for p in D["params"]])
for mu in mus:
    for name, c, k0 in (("r8", c8, k8), ("r8 + (651/34) r6", c8 + (651 / 34) * c6, k8 + (651 / 34) * k6)):
        res = linprog(c - mu * cphi, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
        if res.status != 0: print("mu = %g, %s: %s" % (mu, name, res.message[:60])); continue
        x = res.x
        print("mu = %g: min of [%s - mu Phi] = %.6g ; there P = %.5g, Phi = %.6g, special supports by order 6..10: %s  [%.0f s]" % (
            mu, name, res.fun + k0 - mu * kphi, x[0], cphi @ x + kphi, ", ".join("%.5g" % x[orders == o].sum() for o in (6, 7, 8, 9, 10)), time.time() - t0), flush=True)
