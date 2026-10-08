"""C1, lab session, 2026-10-08. The twin-prism corner is the grid corner: numbers.
  python lp_grid.py <census2 order-10 json> <reps10 json>
Structure (NOTE 17.26): a prism X whose three rung apices form a triangle Theta is X = G - Theta for a 3 x 3 grid G, and
its twins are the other grids through the line Theta; a prism whose apices do not form a triangle has at most 2 twins.
So tau <= (P - 6 rho) + rho_2, rho = number of grids, rho_2 = number of pairs of grids sharing a line <= 15 rho.
Prints: the parameter index of the grid, max rho, min and max of P - 6 rho, rho at the penalised optima, and the
penalised minima with tau' <= min(Phi/4, P + 9 rho, 2P + 3 rho) (tau' an extra LP variable) for all shapes of support
<= 9 and for all shapes except (6,3). Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); npar = len(D["params"]); pc = lambda x: bin(x).count("1")
ri = []; ci = []; va = []; const = []; r = 0; seen = set()
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
grid = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18]
print("9-vertex parameters with 18 edges:", grid, "|Aut| =", [C2.aut_order(9, D["params"][i][2]) for i in grid], flush=True)
g = grid[0]; eP = np.zeros(npar); eP[0] = 1.0; eG = np.zeros(npar); eG[g] = 1.0
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
def lp(c, Aub=None, bub=None, nv=npar):
    return linprog(c, A_ub=-A if Aub is None else Aub, b_ub=const if bub is None else bub, bounds=[(0, None)] * nv, method="highs-ipm")
res = lp(-eG); print("max rho = %.6g (P = %.5g there)" % (-res.fun, res.x[0]))
res = lp(eP - 6 * eG); print("min (P - 6 rho) = %.6g" % res.fun); res = lp(-(eP - 6 * eG)); print("max (P - 6 rho) = %.6g" % -res.fun, flush=True)
cphi, kphi = vec(R["6,3,4"]); fam = {}
for nm, excl in (("all shapes", ()), ("without (6,3)", ((6, 3), (3, 6)))):
    c8 = np.zeros(npar); k8 = 0.0
    for k_, f in R.items():
        a_, b_, q_ = (int(x) for x in k_.split(","))
        if a_ + b_ > 9 or q_ != 8 or (a_, b_) in excl: continue
        cc, kk = vec(f); c8 += cc; k8 += kk
    fam[nm] = (c8, k8)
# extended LP with one extra variable t (= tau'): 4 t <= Phi ; t <= P + 9 rho ; t <= 2P + 3 rho
ext = vstack([hstack([-A, csr_matrix((A.shape[0], 1))]),
              csr_matrix(np.append(-cphi, 4.0).reshape(1, -1)), csr_matrix(np.append(-(eP + 9 * eG), 1.0).reshape(1, -1)), csr_matrix(np.append(-(2 * eP + 3 * eG), 1.0).reshape(1, -1))])
bext = np.append(const, [kphi, 0.0, 0.0])
for nm, (c8, k8) in fam.items():
    for cc in (4000.0, 8000.0, 16000.0):
        res = lp(np.append(c8, -cc), ext, bext, npar + 1); x = res.x
        res0 = lp(c8 - (cc / 4) * cphi); x0 = res0.x
        print("%s, c = %g: with Phi only: %.4gM (P = %.0f, rho = %.1f, Phi = %.0f) ; with the three bounds on tau: %.4gM (P = %.0f, rho = %.1f, Phi = %.0f, tau' = %.0f)  [%.0f s]" % (
            nm, cc, (res0.fun + k8 - (cc / 4) * kphi) / 1e6, x0[0], x0[g], cphi @ x0 + kphi, (res.fun + k8) / 1e6, x[0], x[g], cphi @ x[:npar] + kphi, x[npar], time.time() - t0), flush=True)
