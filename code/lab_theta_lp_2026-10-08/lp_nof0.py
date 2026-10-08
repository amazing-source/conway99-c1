"""C1, lab session, 2026-10-08. Rank 37: the budget when sub-families of (6,3) are dropped.
  python lp_nof0.py <census2 order-10 json> <reps10 json> <drop> <k> [c ...]
     drop: comma-separated sub-families of (6,3) to remove, among 730 (W with 7 edges, far triangle), 820 (W with 8
           edges, far induced path), 831 (W with 8 edges, triangle with one edge to W); "none" keeps everything.
tau' an LP variable with 4 tau' <= Phi, tau' <= 2P + 3 rho, 17 tau' <= 17 P + 105 rho (Codex, note 194).
Bound: 2 R/(k+1) - 2 c tau'/(k(k+1)) with R = r8 of all shapes of support <= 9 minus the dropped sub-families (both
signs). b_4 alone; ceiling 15.975M. Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); drop = [] if sys.argv[3] == "none" else [tuple(int(ch) for ch in x) for x in sys.argv[3].split(",")]
k = int(sys.argv[4]); cs = [float(x) for x in sys.argv[5:]] or [8000.0]
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
if drop:
    for key, rows, aut, form in D["types"]["9"]:
        e_tot = sum(pc(x) for x in rows) // 2
        if e_tot < 10: continue
        cnt = 0
        for W in combinations(range(9), 6):
            wm = sum(1 << i for i in W); ym = 511 & ~wm; ew = sum(pc(rows[i] & wm) for i in W) // 2; cross = sum(pc(rows[i] & ym) for i in W); ey = e_tot - ew - cross
            if (ew, ey, cross) in drop: cnt += 1
        if not cnt: continue
        for p, v_ in form.items():
            val = 2.0 * float(Fr(v_)) * cnt / aut
            if int(p): c8[int(p) - 1] -= val
            else: k8 -= val
ext = vstack([hstack([-A, csr_matrix((A.shape[0], 1))]), csr_matrix(np.append(-cphi, 4.0).reshape(1, -1)),
              csr_matrix(np.append(-(2 * eP + 3 * eG), 1.0).reshape(1, -1)), csr_matrix(np.append(-(17 * eP + 105 * eG), 17.0).reshape(1, -1))])
bext = np.append(const, [kphi, 0.0, 0.0])
for cc in cs:
    res = linprog(np.append(2 * c8 / (k + 1), -2 * cc / (k * (k + 1))), A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 1), method="highs-ipm"); x = res.x
    print("dropped %s, k = %d, c = %g: bound %.4gM ; there R = %.4gM, P = %.0f, rho = %.1f, tau' = %.0f  [%.0f s]" % (
        sys.argv[3], k, cc, (res.fun + 2 * k8 / (k + 1)) / 1e6, (c8 @ x[:npar] + k8) / 1e6, x[0], x[g], x[npar], time.time() - t0), flush=True)
