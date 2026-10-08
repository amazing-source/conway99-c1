"""C1, lab session, 2026-10-08. Rank 37: the ceiling INSIDE the same LP as the census (suggested by the laptop session).
  python lp_joint2.py <census2 order-10 json> <reps10 json> [c ...]
Variables: the 549 census parameters, tau', and (a_7, a_8, a_9, a_10, b_1, b_2, b_3). Theta side, by the laptop session's
exact identities at rank 37 (a relaxation of the full positivity polytope: only a_11, a_12, a_13 >= 0 are kept):
    b_4  = 14 006 902 + 2793 a_7 + 532 a_8 + 77 a_9 + 7 a_10 - 8987 b_1 - 664 b_2 - 35 b_3
    a_11 =   -133 154 -  406 a_7 - 125 a_8 - 34 a_9 -  7 a_10 + 5726 b_1 + 273 b_2 +  7 b_3  >= 0
    a_12 =    736 358 + 1183 a_7 + 350 a_8 + 91 a_9 + 13 a_10 - 2429 b_1 - 476 b_2 - 21 b_3  >= 0
    a_13 =  1 260 308 +  378 a_7 +  98 a_8 +  7 a_9 +  6 a_10 + 25830 b_1 + 70 b_2 -  7 b_3  >= 0
Caps and floors: a_7 <= 842, a_7 <= (2/21) N(F10) [census], 7 a_7 + 8 a_8 <= 55440, b_1 <= 44, b_2 >= 462 + 41 b_1,
b_3 >= 45898. Census side: positivity of all counts, 4 tau' <= Phi, tau' <= 2P + 3 rho, 17 tau' <= 17 P + 105 rho,
tau' <= 1403, P + 5 rho <= 1386, tau' <= P + 5 rho + 17. Floor: b_4 >= (2 r8 - c tau')/3 (all shapes of support <= 9).
The LP maximises  b_4(identity) - floor ; rank 37 is excluded (for that c) when the maximum is negative.
Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); cs = [float(x) for x in sys.argv[3:]] or [18000.0]
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
g = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18][0]; F10 = 437
eP = np.zeros(npar); eP[0] = 1.0; eG = np.zeros(npar); eG[g] = 1.0; eF = np.zeros(npar); eF[F10] = 1.0
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
NX = 8                                                                     # extra variables: tau', a7, a8, a9, a10, b1, b2, b3
def row(v, ex): return csr_matrix(np.concatenate([v, ex]).reshape(1, -1))
Z = np.zeros(npar); rows_ = [hstack([-A, csr_matrix((A.shape[0], NX))])]; b_ = list(const)
def add(v, ex, rhs): rows_.append(row(v, ex)); b_.append(rhs)              # v.theta + ex.x <= rhs
add(-cphi, [4, 0, 0, 0, 0, 0, 0, 0], kphi); add(-(2 * eP + 3 * eG), [1, 0, 0, 0, 0, 0, 0, 0], 0.0); add(-(17 * eP + 105 * eG), [17, 0, 0, 0, 0, 0, 0, 0], 0.0)
add(Z, [1, 0, 0, 0, 0, 0, 0, 0], 1403.0); add(eP + 5 * eG, [0] * 8, 1386.0); add(-(eP + 5 * eG), [1, 0, 0, 0, 0, 0, 0, 0], 17.0)
add(Z, [0, 1, 0, 0, 0, 0, 0, 0], 842.0); add(-(2 / 21) * eF, [0, 1, 0, 0, 0, 0, 0, 0], 0.0); add(Z, [0, 7, 8, 0, 0, 0, 0, 0], 55440.0); add(Z, [0, 0, 0, 0, 0, 1, 0, 0], 44.0)
add(Z, [0, 0, 0, 0, 0, 41, -1, 0], -462.0); add(Z, [0, 0, 0, 0, 0, 0, 0, -1], -45898.0)
add(Z, [0, 406, 125, 34, 7, -5726, -273, -7], -133154.0)                      # a_11 >= 0
add(Z, [0, -1183, -350, -91, -13, 2429, 476, 21], 736358.0)                  # a_12 >= 0
add(Z, [0, -378, -98, -7, -6, -25830, -70, 7], 1260308.0)                    # a_13 >= 0
ext = vstack(rows_); bext = np.array(b_)
for cc in cs:
    for withF in (1, 0):
        e2 = ext.tolil(copy=True) if not withF else ext
        if not withF:
            e2 = vstack([r_ for i_, r_ in enumerate(rows_) if i_ != 8]); bb = np.array([x for i_, x in enumerate(b_) if i_ != 7 + len(const) - len(const) + 0]) if False else np.array(b_[:len(const) + 7] + b_[len(const) + 8:])
        else: bb = bext
        obj = np.concatenate([2 * c8 / 3, [-cc / 3, -2793, -532, -77, -7, 8987, 664, 35]])
        res = linprog(obj, A_ub=e2, b_ub=bb, bounds=[(0, None)] * (npar + NX), method="highs-ipm")
        if res.status != 0: print("c = %g: %s" % (cc, res.message[:60])); continue
        x = res.x; ex = x[npar:]; floor = (2 * (c8 @ x[:npar] + k8) - cc * ex[0]) / 3; ceil_ = 14006902 + 2793 * ex[1] + 532 * ex[2] + 77 * ex[3] + 7 * ex[4] - 8987 * ex[5] - 664 * ex[6] - 35 * ex[7]
        print("c = %g, %s: max (ceiling - floor) = %.4gM  [ceiling %.4gM, floor %.4gM; a_7 = %.0f, a_8 = %.0f, a_9 = %.0f, a_10 = %.0f, b_1 = %.1f, b_2 = %.0f, b_3 = %.0f; N(F10) = %.0f, P = %.0f, rho = %.1f, tau' = %.0f]  %s  [%.0f s]" % (
            cc, "with a_7 <= (2/21) N(F10)" if withF else "without the Fano coupling", (ceil_ - floor) / 1e6, ceil_ / 1e6, floor / 1e6, ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], x[F10], x[0], x[g], ex[0],
            "EXCLUDED at this c" if ceil_ - floor < 0 else "feasible", time.time() - t0), flush=True)
