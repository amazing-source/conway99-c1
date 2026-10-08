"""C1, lab session, 2026-10-08. Rank 37: separate loss constants for grid twins and non-grid twins.
  python lp_two.py <census2 order-10 json> <reps10 json> <cg,cng> [<cg,cng> ...]
tau_g = pairs of grids sharing a line (twins of grid prisms), tau_n = pairs inside non-grid classes. LP variables with
17 tau_g <= 207 rho (Codex, note 194), tau_n <= P - 6 rho (classes of at most 3), 4 (tau_g + tau_n) <= Phi.
Bound (class quotient k = 2): (2 r8 - cg tau_g - cng tau_n) / 3, all shapes of support <= 9, b_4 alone.
Ceiling (Codex, note 194): 15 975 390.7. Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); pairs = [tuple(float(y) for y in x.split(",")) for x in sys.argv[3:]]
npar = len(D["params"]); pc = lambda x: bin(x).count("1"); ri = []; ci = []; va = []; const = []; r = 0; seen = set()
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
g = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18][0]
eP = np.zeros(npar); eP[0] = 1.0; eG = np.zeros(npar); eG[g] = 1.0
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
cphi, kphi = vec(R["6,3,4"]); c8 = np.zeros(npar); k8 = 0.0
for k_, f in R.items():
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > 9 or q_ != 8: continue
    cc, kk = vec(f); c8 += cc; k8 += kk
row = lambda v, tg, tn: csr_matrix(np.concatenate([v, [tg, tn]]).reshape(1, -1))
ext = vstack([hstack([-A, csr_matrix((A.shape[0], 2))]), row(-207 * eG, 17.0, 0.0), row(-(eP - 6 * eG), 0.0, 1.0), row(-cphi, 4.0, 4.0), row(-(eP - 6 * eG), 0.0, 0.0)])
bext = np.append(const, [0.0, 0.0, kphi, 0.0])
for cg, cn in pairs:
    res = linprog(np.concatenate([2 * c8 / 3, [-cg / 3, -cn / 3]]), A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 2), method="highs-ipm"); x = res.x
    print("c_grid = %g, c_nongrid = %g: bound %.4gM ; there R = %.4gM, P = %.0f, rho = %.1f, tau_g = %.0f, tau_n = %.0f, Phi = %.0f  [%.0f s]" % (
        cg, cn, (res.fun + 2 * k8 / 3) / 1e6, (c8 @ x[:npar] + k8) / 1e6, x[0], x[g], x[npar], x[npar + 1], cphi @ x[:npar] + kphi, time.time() - t0), flush=True)
