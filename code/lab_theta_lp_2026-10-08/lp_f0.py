"""C1, lab session, 2026-10-08. The shape (6,3) at norm 8 split into sub-families, and what a clean sub-family adds.
  python lp_f0.py <census2 order-10 json> <reps10 json> [c_F0 ...]
Sub-family key (e(W), e(Y), cross): psi = 1_W - 1_Y, |W| = 6, |Y| = 3, e(W) + e(Y) - cross = 10.
F0 = (7, 3, 0): W with 7 edges, Y a triangle far from W. Counts are numbers of pairs (W, Y) (one sign).
Prints the composition of (6,3) at the unpenalised optimum, the minimum of each sub-family alone, and then
    min over the polytope of  [ r8 without (6,3),(3,6)  +  2 N(F0)  -  ((3228 + c_F0) / 4) Phi ]
for the given c_F0 (collisions of F0 per twin pair of prisms, both signs), supports <= 9. Floating point HiGHS."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); cs = [float(x) for x in sys.argv[3:]] or [0.0]
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
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)
sub = {}
for key, rows, aut, form in D["types"]["9"]:
    e_tot = sum(pc(x) for x in rows) // 2; tally = {}
    if e_tot < 10: continue
    for W in combinations(range(9), 6):
        wm = sum(1 << i for i in W); ym = 511 & ~wm; ew = sum(pc(rows[i] & wm) for i in W) // 2; cross = sum(pc(rows[i] & ym) for i in W); ey = e_tot - ew - cross
        if ew + ey - cross == 10: tally[(ew, ey, cross)] = tally.get((ew, ey, cross), 0) + 1
    for k_, cnt in tally.items():
        acc = sub.setdefault(k_, [np.zeros(npar), 0.0])
        for p, v_ in form.items():
            val = float(Fr(v_)) * cnt / aut
            if int(p): acc[0][int(p) - 1] += val
            else: acc[1] += val
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
c8 = np.zeros(npar); k8 = 0.0
for k_, f in R.items():
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > 9 or q_ != 8 or (a_, b_) in ((6, 3), (3, 6)): continue
    cc, kk = vec(f); c8 += cc; k8 += kk
cphi, kphi = vec(R["6,3,4"]); call, kall = vec(R["6,3,8"])
def solve(c): 
    res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm"); return res
tot = sum(v_[0] for v_ in sub.values()); totk = sum(v_[1] for v_ in sub.values())
print("check: sum of the sub-families = shape (6,3) at norm 8: constants %.6g vs %.6g, max coefficient difference %.3g" % (totk, kall, np.abs(tot - call).max()))
res = solve(c8 + 2 * call); x0 = res.x
print("unpenalised optimum of r8 (supports <= 9): %.6g ; composition of (6,3), one sign, and minimum of each sub-family alone:" % (res.fun + k8 + 2 * kall))
for k_ in sorted(sub):
    c, k0 = sub[k_]; m = solve(c)
    print("   (e(W), e(Y), cross) = %s: %.6g at the optimum ; alone min %.6g  [%.0f s]" % (k_, c @ x0 + k0, m.fun + k0, time.time() - t0), flush=True)
cF, kF = sub[(7, 3, 0)]
for cf in cs:
    mu = (3228 + cf) / 4; res = solve(c8 + 2 * cF - mu * cphi); x = res.x
    print("c_F0 = %g: min of [r8 without (6,3) + 2 N(F0) - ((3228 + c_F0)/4) Phi] = %.6g ; there P = %.5g, Phi = %.6g, 2 N(F0) = %.6g  [%.0f s]" % (
        cf, res.fun + k8 + 2 * kF - mu * kphi, x[0], cphi @ x + kphi, 2 * (cF @ x + kF), time.time() - t0), flush=True)
