"""C1, lab session, 2026-10-08. Rank 37: what a better bound on the pairs of grids sharing a line would give.
  python lp_beta.py <census2 order-10 json> <reps10 json> <beta> <gamma> [c ...]
HYPOTHESES (what-if): pairs of grids sharing a line <= beta * rho, and pairs inside the non-grid classes <=
gamma * (P - 6 rho) (gamma = 1 is proved: classes of at most 3; gamma = 1/2 would be "at most one twin").
tau' <= (gamma (P - 6 rho) + beta rho) and 4 tau' <= Phi. Class quotient k = 2: bound = (2 r8 - c tau')/3, all shapes of
support <= 9, b_4 alone (ceiling 15.98M; 14.44M if there is no Fano vector). Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); beta = float(sys.argv[3]); gamma = float(sys.argv[4]); cs = [float(x) for x in sys.argv[5:]] or [16000.0]
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
              csr_matrix(np.append(-(gamma * eP + (beta - 6 * gamma) * eG), 1.0).reshape(1, -1)),
              csr_matrix(np.append(-eP + 6 * eG, 0.0).reshape(1, -1))])          # last row: P - 6 rho >= 0
bext = np.append(const, [kphi, 0.0, 0.0])
for cc in cs:
    res = linprog(np.append(2 * c8 / 3, -cc / 3), A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 1), method="highs-ipm"); x = res.x
    print("beta = %g, gamma = %g, c = %g: bound %.4gM ; there R = %.4gM, P = %.0f, rho = %.1f, Phi = %.0f, tau' = %.0f  [%.0f s]" % (
        beta, gamma, cc, (res.fun + 2 * k8 / 3) / 1e6, (c8 @ x[:npar] + k8) / 1e6, x[0], x[g], cphi @ x[:npar] + kphi, x[npar], time.time() - t0), flush=True)
