"""C1, lab session, 2026-10-08. Rank 37: the NORM-6 floor from prism-free representatives, inside the joint LP.
  python lp_n6.py <census2 order-10 json> <reps10_pf json> <S6>:<c6>:<c8> [...]
b_3 >= R6 - c6 tau, R6 = prism-free representatives of norm 6 and support <= S6 (quotient k = 1), c6 = norm-6 colliding
pairs charged per twin pair (UNKNOWN); norm-8 floor (2 r8 - c8 tau)/3 with ALL representatives of support <= 9
(c8 = 27828 is Codex's certified mass-six cap). Prints max (ceiling - floor): negative = excluded for these constants.
Header of lp_family.py below.
Scenario "m<M>s<S>k<K>[all]": representatives of norm 8 with min(|W|,|Y|) <= M and support <= S; class "pf"
(neither W nor Y contains an induced prism) unless "all" is appended; class quotient
   classes >= 2 R/(K+1) - 2 C/(K(K+1)),  C <= c tau   (K = 1: classes >= R - C).
For prism-free representatives a twin-prism collision is two-sided (1 <= |A|, |B| <= 5); c is the number of such
colliding pairs charged per twin pair: UNKNOWN here, the script prints the break-even value of c.
Theta side and census cuts as in lp_joint3.py (secants for b_2, P >= 6 rho, Fano coupling). Floating HiGHS, exploration."""
import sys, json, time, re
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); scen = sys.argv[3:]
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
R0 = json.load(open(sys.argv[2].replace("reps10_pf", "reps10"))); cphi, kphi = vec(R0["6,3,4"])
NX = 8
def row(v, ex): return csr_matrix(np.concatenate([v, ex]).reshape(1, -1))
Z = np.zeros(npar); rows0 = [hstack([-A, csr_matrix((A.shape[0], NX))])]; b0 = list(const)
def add(v, ex, rhs): rows0.append(row(v, ex)); b0.append(rhs)
add(-cphi, [4, 0, 0, 0, 0, 0, 0, 0], kphi); add(-(2 * eP + 3 * eG), [1, 0, 0, 0, 0, 0, 0, 0], 0.0); add(-(17 * eP + 105 * eG), [17, 0, 0, 0, 0, 0, 0, 0], 0.0)
add(Z, [1, 0, 0, 0, 0, 0, 0, 0], 1403.0); add(eP + 5 * eG, [0] * 8, 1386.0); add(-(eP + 5 * eG), [1, 0, 0, 0, 0, 0, 0, 0], 17.0)
add(Z, [0, 1, 0, 0, 0, 0, 0, 0], 842.0); add(-(2 / 21) * eF, [0, 1, 0, 0, 0, 0, 0, 0], 0.0); add(Z, [0, 7, 8, 0, 0, 0, 0, 0], 55440.0); add(Z, [0, 0, 0, 0, 0, 1, 0, 0], 44.0)
add(Z, [0, 0, 0, 0, 0, 0, 0, -1], -45898.0); add(-(eP - 6 * eG), [0] * 8, 0.0)
fb = lambda t: 462 + 41 * t + t * t / 2
for k in range(0, 44, 2):
    sl = (fb(k + 2) - fb(k)) / 2; add(Z, [0, 0, 0, 0, 0, sl, -1, 0], sl * k - fb(k))
add(Z, [0, 406, 125, 34, 7, -5726, -273, -7], -133154.0); add(Z, [0, -1183, -350, -91, -13, 2429, 476, 21], 736358.0); add(Z, [0, -378, -98, -7, -6, -25830, -70, 7], 1260308.0)
r8v = np.zeros(npar); r8k = 0.0
for k_, f in R.items():
    a_, b_, q_, cl = k_.split(","); a_, b_, q_ = int(a_), int(b_), int(q_)
    if q_ == 8 and a_ + b_ <= 9: cc, kk = vec(f); r8v += cc; r8k += kk
for s in scen:
    S6, c6, c8 = s.split(":"); S6 = int(S6); c6 = float(c6); c8 = float(c8); cv = np.zeros(npar); kv = 0.0; comp = {}
    for k_, f in R.items():
        a_, b_, q_, cl = k_.split(","); a_, b_, q_ = int(a_), int(b_), int(q_)
        if q_ != 6 or a_ + b_ > S6 or cl != "pf": continue
        cc, kk = vec(f); cv += cc; kv += kk; comp[k_] = (cc, kk)
    rows_ = list(rows0); b_ = list(b0)
    rows_.append(row(cv, [-c6, 0, 0, 0, 0, 0, 0, -1])); b_.append(-kv)          # R6 - c6 tau - b3 <= 0
    ext = vstack(rows_); bb = np.array(b_)
    obj = np.concatenate([2 * r8v / 3, [-c8 / 3, -2793, -532, -77, -7, 8987, 664, 35]])
    res = linprog(obj, A_ub=ext, b_ub=bb, bounds=[(0, None)] * (npar + NX), method="highs-ipm")
    if res.status != 0: print("scenario %s: %s" % (s, res.message[:70])); continue
    x = res.x; ex = x[npar:]; r8 = r8v @ x[:npar] + r8k; r6 = cv @ x[:npar] + kv
    ceil_ = 14006902 + 2793 * ex[1] + 532 * ex[2] + 77 * ex[3] + 7 * ex[4] - 8987 * ex[5] - 664 * ex[6] - 35 * ex[7]
    gap = ceil_ - (2 * r8 - c8 * ex[0]) / 3
    print("S6 = %d, c6 = %g, c8 = %g: max (ceiling - floor) = %+.4gM  %s  [ceiling %.4gM, r8 %.4gM, R6(pf) %.0f, b_3 %.0f; a_7 %.0f a_8 %.0f a_9 %.0f b_1 %.0f; P %.0f rho %.1f tau %.0f]  [%.0f s]" % (
        S6, c6, c8, gap / 1e6, "EXCLUDED for these constants" if gap < 0 else "feasible", ceil_ / 1e6, r8 / 1e6, r6, ex[7], ex[1], ex[2], ex[3], ex[5], x[0], x[g], ex[0], time.time() - t0), flush=True)
    print("      norm-6 pf composition there: " + ", ".join("(%s) %.0f" % (k_[:-5], cc @ x[:npar] + kk) for k_, (cc, kk) in sorted(comp.items()) if abs(cc @ x[:npar] + kk) > 0.5), flush=True)
