"""C1, lab session, 2026-10-08. Rank 37: the budget for the total twin loss per twin pair, with Codex's new cut and
its class quotient.
  python lp_budget3.py <census2 order-10 json> <reps10 json> <k> <tau cap> [c ...]
(variant of lp_budget.py with a constant cap on tau', Codex's census cut P + 5 rho <= 1386 and its coupled bound tau <= P + 5 rho + 17)
tau' is an LP variable with 4 tau' <= Phi, tau' <= 2P + 3 rho and 17 tau' <= 17 P + 105 rho (Codex, from the structure
theorem of NOTE 17.26 and at most 17 grids through a vertex). Objective (Codex, note 186): for an integer k >= 1 the
number of classes is at least 2R/(k+1) - 2C/(k(k+1)), R = raw number of representatives, C = number of colliding pairs
<= c tau'. Prints the minimum over the order-10 polytope of 2 r8/(k+1) - 2 c tau'/(k(k+1)) for all shapes of support
<= 9 (b_4 alone; ceiling 15.98M). Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); k = int(sys.argv[3]); TAUCAP = float(sys.argv[4]); cs = [float(x) for x in sys.argv[5:]] or [8000.0]
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
ext = vstack([hstack([-A, csr_matrix((A.shape[0], 1))]), csr_matrix(np.append(-cphi, 4.0).reshape(1, -1)),
              csr_matrix(np.append(-(2 * eP + 3 * eG), 1.0).reshape(1, -1)), csr_matrix(np.append(-(17 * eP + 105 * eG), 17.0).reshape(1, -1)),
              csr_matrix(np.append(np.zeros(npar), 1.0).reshape(1, -1)), csr_matrix(np.append(eP + 5 * eG, 0.0).reshape(1, -1)),
              csr_matrix(np.append(-(eP + 5 * eG), 1.0).reshape(1, -1))])
bext = np.append(const, [kphi, 0.0, 0.0, TAUCAP, 1386.0, 17.0])
for cc in cs:
    res = linprog(np.append(2 * c8 / (k + 1), -2 * cc / (k * (k + 1))), A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 1), method="highs-ipm"); x = res.x
    print("k = %d, c = %g: bound %.4gM ; there R = %.4gM, P = %.0f, rho = %.1f, Phi = %.0f, tau' = %.0f  [%.0f s]" % (
        k, cc, (res.fun + 2 * k8 / (k + 1)) / 1e6, (c8 @ x[:npar] + k8) / 1e6, x[0], x[g], cphi @ x[:npar] + kphi, x[npar], time.time() - t0), flush=True)
