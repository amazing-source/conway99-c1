"""C1, lab session, 2026-10-08. Rank 37, joint LP of lp_joint2.py with WHAT-IF caps on the short shells of L1.
  python lp_joint3.py <census2 order-10 json> <reps10 json> <scenario> [<scenario> ...]
A scenario is a comma-separated list of caps, e.g.  "a8<=2000,a9<=0"  or  "none" ; names a7 a8 a9 a10 b1 b2 b3 tau, and
"b2>=3000" style floors;
"k=<int>" uses the class quotient classes >= 2R/(k+1) - 2C/(k(k+1)) (default k = 2);
"supp10" takes the representatives of support <= 10 instead of <= 9 (r8, r6);
"b3floor=<c6>" adds b_3 >= (2 r6 - c6 tau)/3 (norm-6 representatives of support <= 9, c6 collisions per twin pair). For each scenario the LP is solved at c = 27828 (the certified collision cap per grid twin pair)
and the break-even c is read off the optimal vertex, then refined by Newton steps (the maximum is convex in c).
b_2 floor: the 22 secants of 462 + 41 b_1 + b_1^2/2 at consecutive even b_1 (Codex: b_1 is even). Also P >= 6 rho.
WHAT-IF only: none of the caps is proved. Floating point HiGHS, exploration. One process, memory below 3 GB."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); scen = sys.argv[3:] or ["none"]
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
cphi, kphi = vec(R["6,3,4"]); FORMS = {}                                   # (norm, largest support) -> affine form
for q0 in (6, 8):
    for smax in (9, 10):
        cv = np.zeros(npar); kv = 0.0
        for k_, f in R.items():
            a_, b_, q_ = (int(x) for x in k_.split(","))
            if a_ + b_ > smax or q_ != q0: continue
            cc, kk = vec(f); cv += cc; kv += kk
        FORMS[(q0, smax)] = (cv, kv)
NX = 8; NAMES = ["tau", "a7", "a8", "a9", "a10", "b1", "b2", "b3"]
def row(v, ex): return csr_matrix(np.concatenate([v, ex]).reshape(1, -1))
Z = np.zeros(npar); rows0 = [hstack([-A, csr_matrix((A.shape[0], NX))])]; b0 = list(const)
def add(v, ex, rhs, rows_=rows0, b_=b0): rows_.append(row(v, ex)); b_.append(rhs)
add(-cphi, [4, 0, 0, 0, 0, 0, 0, 0], kphi); add(-(2 * eP + 3 * eG), [1, 0, 0, 0, 0, 0, 0, 0], 0.0); add(-(17 * eP + 105 * eG), [17, 0, 0, 0, 0, 0, 0, 0], 0.0)
add(Z, [1, 0, 0, 0, 0, 0, 0, 0], 1403.0); add(eP + 5 * eG, [0] * 8, 1386.0); add(-(eP + 5 * eG), [1, 0, 0, 0, 0, 0, 0, 0], 17.0)
add(Z, [0, 1, 0, 0, 0, 0, 0, 0], 842.0); add(-(2 / 21) * eF, [0, 1, 0, 0, 0, 0, 0, 0], 0.0); add(Z, [0, 7, 8, 0, 0, 0, 0, 0], 55440.0); add(Z, [0, 0, 0, 0, 0, 1, 0, 0], 44.0)
add(Z, [0, 0, 0, 0, 0, 0, 0, -1], -45898.0); add(-(eP - 6 * eG), [0] * 8, 0.0)   # b_3 floor ; P >= 6 rho
fb = lambda t: 462 + 41 * t + t * t / 2                                      # b_2 >= f(b_1), b_1 even: all secants at consecutive even values
for k in range(0, 44, 2):
    sl = (fb(k + 2) - fb(k)) / 2; add(Z, [0, 0, 0, 0, 0, sl, -1, 0], sl * k - fb(k))
add(Z, [0, 406, 125, 34, 7, -5726, -273, -7], -133154.0)                      # a_11 >= 0
add(Z, [0, -1183, -350, -91, -13, 2429, 476, 21], 736358.0)                  # a_12 >= 0
add(Z, [0, -378, -98, -7, -6, -25830, -70, 7], 1260308.0)                    # a_13 >= 0
def solve(ext, bb, cc):
    c8, k8 = FORMS[(8, SM)]
    obj = np.concatenate([2 * c8 / (KQ + 1), [-2 * cc / (KQ * (KQ + 1)), -2793, -532, -77, -7, 8987, 664, 35]])
    res = linprog(obj, A_ub=ext, b_ub=bb, bounds=[(0, None)] * (npar + NX), method="highs-ipm")
    if res.status != 0: return None
    x = res.x; ex = x[npar:]; r8 = c8 @ x[:npar] + k8
    ceil_ = 14006902 + 2793 * ex[1] + 532 * ex[2] + 77 * ex[3] + 7 * ex[4] - 8987 * ex[5] - 664 * ex[6] - 35 * ex[7]
    return x, ex, r8, ceil_
for s in scen:
    rows_ = list(rows0); b_ = list(b0); SM = 10 if "supp10" in s.split(",") else 9; c6, k6 = FORMS[(6, SM)]
    KQ = ([int(t[2:]) for t in s.split(",") if t.startswith("k=")] or [2])[0]
    fl = lambda r8_, c_, tau_: 2 * r8_ / (KQ + 1) - 2 * c_ * tau_ / (KQ * (KQ + 1))
    cst = lambda r8_, ceil__, tau_: (2 * r8_ / (KQ + 1) - ceil__) * KQ * (KQ + 1) / 2 / max(tau_, 1e-9)
    if s != "none":
        for item in s.split(","):
            if item == "supp10" or item.startswith("k="): continue
            if item.startswith("b3floor="):                                    # what-if: b_3 >= (2 r6 - c6 tau)/3 at the same census point
                q6 = float(item.split("=")[1]); add(2 * c6 / 3, [-q6 / 3, 0, 0, 0, 0, 0, 0, -1], -2 * k6 / 3, rows_, b_)
            elif "<=" in item: nm, val = item.split("<="); e = [0.0] * NX; e[NAMES.index(nm)] = 1.0; add(Z, e, float(val), rows_, b_)
            else: nm, val = item.split(">="); e = [0.0] * NX; e[NAMES.index(nm)] = -1.0; add(Z, e, -float(val), rows_, b_)
    ext = vstack(rows_); bb = np.array(b_); o = solve(ext, bb, 27828.0)
    if o is None: print("scenario %s: LP failed" % s); continue
    x, ex, r8, ceil_ = o; gap = ceil_ - fl(r8, 27828.0, ex[0]); cstar = cst(r8, ceil_, ex[0])
    print("scenario %-28s at c = 27828: max (ceiling - floor) = %+.4gM  [ceiling %.4gM, r8 %.4gM; a_7 %.0f a_8 %.0f a_9 %.0f a_10 %.0f b_1 %.1f b_2 %.0f b_3 %.0f; P %.0f rho %.1f tau %.0f; r6 %.0f]  %s" % (
        s, gap / 1e6, ceil_ / 1e6, r8 / 1e6, ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], x[0], x[g], ex[0], c6 @ x[:npar] + k6, "EXCLUDED" if gap < 0 else "feasible"), flush=True)
    cs_ = cstar
    for _ in range(3):                                                         # the maximum is convex in c: Newton steps on the optimal vertex
        o2 = solve(ext, bb, cs_)
        if o2 is None: break
        g2 = o2[3] - fl(o2[2], cs_, o2[1][0]); cn = cst(o2[2], o2[3], o2[1][0])
        print("      at c = %.0f: max = %+.4gM ; vertex a_7 %.0f a_8 %.0f a_9 %.0f a_10 %.0f b_1 %.1f b_2 %.0f ; rho %.1f tau %.0f ; next c %.0f   [%.0f s]" % (
            cs_, g2 / 1e6, o2[1][1], o2[1][2], o2[1][3], o2[1][4], o2[1][5], o2[1][6], o2[0][g], o2[1][0], cn, time.time() - t0), flush=True)
        if abs(cn - cs_) < 5: break
        cs_ = cn
