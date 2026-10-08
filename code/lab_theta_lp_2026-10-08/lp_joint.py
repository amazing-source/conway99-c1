"""C1, lab session, 2026-10-08. Rank 37: coupling the ceiling to the census through the Fano cap a_7 <= (2/21) N(F10).
  python lp_joint.py <census2 order-10 json> <reps10 json> [c ...]
The exact ceiling of b_4 is a concave function of the cap on a_7: 14.44M at a_7 = 0 and 15.98M at a_7 = 842; it is
replaced here by the LINEAR majorant 14.44M + s * a_7 with s = 1900 (slightly above the chord slope 1829; to be redone
exactly). Since a_7 <= (2/21) N(F10) (NOTE 17.20; F10 = parameter found below), rank 37 is excluded if, over the
order-10 polytope,   min [ floor(theta) - s (2/21) N_F10(theta) ]  >  14.44M,
floor = (2 r8 - c tau')/3 (class quotient k = 2), tau' as in lp_budget.py. Prints that minimum and the point.
Floating point HiGHS, exploration: what-if on the size of the coupling, not a bound."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); cs = [float(x) for x in sys.argv[3:]] or [16000.0]
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
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
keep = [i for i in range(7) if i not in (0,)] ; rows14 = [0] * 14
for j, L in enumerate(LINES):
    for i in range(7):
        if i not in L: rows14[i] |= 1 << (7 + j); rows14[7 + j] |= 1 << i
b1, b2 = 7, 8; common = [i for i in range(7) if rows14[i] >> b1 & 1 and rows14[i] >> b2 & 1]; drop = set([b1, b2] + common); vs = [x for x in range(14) if x not in drop]
rows = [sum(1 << vs.index(y) for y in vs if rows14[x] >> y & 1) for x in vs]; key, perm = C2.canon(10, rows)
f10 = [i for i, p in enumerate(D["params"]) if p[0] == 10 and p[1] == key][0]
g = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18][0]
print("F10: parameter index %d (0-based), %d edges" % (f10, sum(pc(x) for x in rows) // 2), flush=True)
eP = np.zeros(npar); eP[0] = 1.0; eG = np.zeros(npar); eG[g] = 1.0; eF = np.zeros(npar); eF[f10] = 1.0
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
ext = vstack([hstack([-A, csr_matrix((A.shape[0], 1))]), csr_matrix(np.append(-cphi, 4.0).reshape(1, -1)),
              csr_matrix(np.append(-(2 * eP + 3 * eG), 1.0).reshape(1, -1)), csr_matrix(np.append(-(17 * eP + 105 * eG), 17.0).reshape(1, -1))])
bext = np.append(const, [kphi, 0.0, 0.0]); s = 1900.0 * 2 / 21
for cc in cs:
    for withF in (0, 1):
        obj = np.append(2 * c8 / 3 - withF * s * eF, -cc / 3)
        res = linprog(obj, A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 1), method="highs-ipm"); x = res.x
        print("c = %g, %s: min = %.4gM (to compare with %s) ; there N(F10) = %.0f (a_7 <= %.0f), P = %.0f, rho = %.1f, tau' = %.0f, R = %.4gM  [%.0f s]" % (
            cc, "with the Fano coupling" if withF else "without coupling", (res.fun + 2 * k8 / 3) / 1e6, "14.44M" if withF else "15.98M", x[f10], 2 * x[f10] / 21, x[0], x[g], x[npar], (c8 @ x[:npar] + k8) / 1e6, time.time() - t0), flush=True)
