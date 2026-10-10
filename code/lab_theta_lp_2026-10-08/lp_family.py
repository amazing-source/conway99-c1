"""C1, lab session, 2026-10-08. Rank 37: joint LP (census + theta identities) for a FAMILY of representatives.
  python lp_family.py <census2 order-10 json> <reps10_pf json> <scenario> [...]
Scenario "m<M>s<S>k<K>[all]": representatives of norm 8 with min(|W|,|Y|) <= M and support <= S; class "pf"
(neither W nor Y contains an induced prism) unless "all" is appended ("x63": all classes except the (6,3) and (3,6) representatives whose 6-set is a prism,
i.e. the collection of Codex's notes 195-198; an "n" after the class drops the shapes (9,0) and (0,9); a "z" keeps only the shapes of sum 0 or +-3; a final "r<X>" adds the what-if cap rho <= X); class quotient
   classes >= 2 R/(K+1) - 2 C/(K(K+1)),  C <= c tau   (K = 1: classes >= R - C).
For prism-free representatives a twin-prism collision is two-sided (1 <= |A|, |B| <= 5); c is the number of such
colliding pairs charged per twin pair: UNKNOWN here, the script prints the break-even value of c.
Env COLLISION_FORM=<json>:<key> subtracts a census form bounding the colliding pairs inside the LP (coupled optimum).
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
import os
for p_ in [int(x) for x in os.environ.get("ZERO_PARAMS", "").split(",") if x]:      # census parameters forced to zero (e.g. types excluded by the rank-free cores, NOTE 17.71)
    e_ = np.zeros(npar); e_[p_ - 1] = 1.0; add(e_, [0] * 8, 0.0)
if os.environ.get("PCAP"): add(eP, [0] * 8, float(os.environ["PCAP"]))                 # what-if / case split: number of prisms P <= PCAP
if os.environ.get("A7CAP") is not None: add(Z, [0, 1, 0, 0, 0, 0, 0, 0], float(os.environ["A7CAP"]))   # a_7 <= A7CAP (A7CAP=0: no integral vector of norm 14, lemma N14 of NOTE 17.95)
if os.environ.get("A8CAP") is not None: add(Z, [0, 0, 1, 0, 0, 0, 0, 0], float(os.environ["A8CAP"]))   # what-if: a_8 <= A8CAP
ext = vstack(rows0); bb = np.array(b0)
for s in scen:
    m_ = re.match(r"m(\d+)s(\d+)k(\d+)(all|x63)?(n)?(z)?(?:r(\d+))?$", s); M, S, K, allc, x63 = int(m_.group(1)), int(m_.group(2)), int(m_.group(3)), bool(m_.group(4)), m_.group(4) == "x63"
    no90 = bool(m_.group(5)); zsum = bool(m_.group(6)); rcap = float(m_.group(7)) if m_.group(7) else None; ext = vstack(rows0 + ([row(eG, [0] * 8)] if rcap is not None else [])); bb = np.array(b0 + ([rcap] if rcap is not None else []))
    NL = 0
    if os.environ.get("EXTRA_ROWS"):                                           # exact equations  census form = sum_c lambda_c cnt_c  (core_type_equations.py, NOTE 17.71)
        EX = json.load(open(os.environ["EXTRA_ROWS"])); NL = EX["nlam"]; er, ec, ev, eb = [], [], [], []
        for k_, rw in enumerate(EX["rows"]):
            f_ = {int(p_): float(Fr(v_)) for p_, v_ in rw["p"].items()}; sc_ = max([abs(x_) for x_ in f_.values()] + [1.0])
            for p_, v_ in f_.items():
                if p_: er.append(k_); ec.append(p_ - 1); ev.append(v_ / sc_)
            for c_, v_ in rw["lam"].items(): er.append(k_); ec.append(npar + NX + int(c_)); ev.append(-float(v_) / sc_)
            eb.append(-f_.get(0, 0.0) / sc_)
        E_ = csr_matrix((ev, (er, ec)), shape=(len(EX["rows"]), npar + NX + NL))
        ext = vstack([hstack([ext, csr_matrix((ext.shape[0], NL))]), E_, -E_]); bb = np.concatenate([bb, np.array(eb), -np.array(eb)])
    cv = np.zeros(npar); kv = 0.0; used = []
    for k_, f in R.items():
        a_, b_, q_, cl = k_.split(","); a_, b_, q_ = int(a_), int(b_), int(q_)
        if q_ != 8 or a_ + b_ > S or min(a_, b_) > M or (cl != "pf" and not allc): continue
        if x63 and cl == "fp" and (a_, b_) in ((6, 3), (3, 6)): continue          # Codex's collection: (6,3) only with e(W) <= 8
        if zsum and abs(a_ - b_) not in (0, 3): continue                            # "z": sums 0 and +-3 only (no change of sum possible in a collision)
        if no90 and (a_, b_) in ((9, 0), (0, 9)): continue                         # "n": without the 9-set indicators (Codex's note 195, caps 22 422 / 23 150)
        cc, kk = vec(f); cv += cc; kv += kk; used.append(k_)
    cF = np.zeros(npar); kF = 0.0; sF = [1.0]; shown = []
    if os.environ.get("COLLISION_FORM"):                                       # coupled LP: classes >= 2R/(K+1) - 2 C(x)/(K(K+1)) with C(x) a census form bounding the colliding pairs (file, key)
        fn_, key_ = os.environ["COLLISION_FORM"].rsplit(":", 1); FF_ = json.load(open(fn_)); cF, kF = vec(FF_[key_]["form"])
        shown = [(k2, vec(FF_[k2]["form"])) for k2 in os.environ.get("SHOW_FORMS", "").split(",") if k2]      # other forms of the same file, evaluated at the optimum
    def solve(cc):
        obj = np.concatenate([2 * cv / (K + 1) - 2 * sF[0] * cF / (K * (K + 1)), [-2 * cc / (K * (K + 1)), -2793, -532, -77, -7, 8987, 664, 35], np.zeros(NL)])
        res = linprog(obj, A_ub=ext, b_ub=bb, bounds=[(0, None)] * (npar + NX + NL), method="highs-ipm")
        if res.status != 0: return None
        x = res.x; ex = x[npar:npar + NX]; r8 = cv @ x[:npar] + kv
        ceil_ = 14006902 + 2793 * ex[1] + 532 * ex[2] + 77 * ex[3] + 7 * ex[4] - 8987 * ex[5] - 664 * ex[6] - 35 * ex[7]
        return x, ex, r8, ceil_, ceil_ - (2 * r8 / (K + 1) - 2 * cc * ex[0] / (K * (K + 1)) - 2 * sF[0] * (cF @ x[:npar] + kF) / (K * (K + 1))), cF @ x[:npar] + kF
    o = solve(0.0)
    if o is None: print("scenario %s: LP failed" % s); continue
    print("scenario %-12s (%d forms) at c = 0: max (ceiling - floor) = %+.4gM  [ceiling %.4gM, R %.4gM; a_7 %.0f a_8 %.0f a_9 %.0f b_1 %.0f; P %.0f rho %.1f tau %.0f]" % (
        s, len(used), o[4] / 1e6, o[3] / 1e6, o[2] / 1e6, o[1][1], o[1][2], o[1][3], o[1][5], o[0][0], o[0][g], o[1][0]), flush=True)
    if os.environ.get("COLLISION_FORM"):
        print("      coupled with the collision form %s: its value at this optimum %.4gM" % (os.environ["COLLISION_FORM"].rsplit(":", 1)[1], o[5] / 1e6))
        if shown: print("      values at this optimum: " + "; ".join("%s = %.5g" % (k2, c2_ @ o[0][:npar] + k0_) for k2, (c2_, k0_) in shown))
        if o[4] >= 0:                                                          # break-even scale: the maximum is convex and non-decreasing in the scale s of the form
            lo_, hi_, flo_, fhi_ = 0.0, 1.0, None, o[4]; sF[0] = 0.0; o0_ = solve(0.0); flo_ = o0_[4]
            if flo_ < 0:
                for _ in range(8):
                    sF[0] = lo_ - flo_ * (hi_ - lo_) / (fhi_ - flo_); om_ = solve(0.0)
                    if om_ is None: break
                    if om_[4] < 0: lo_, flo_ = sF[0], om_[4]
                    else: hi_, fhi_ = sF[0], om_[4]
                    if hi_ - lo_ < 1e-4 * hi_ or abs(om_[4]) < 500: break
                print("      break-even scale of this form: about %.4f (secant from below on a convex function; last value %+.0f): the exclusion would need the bound divided by about %.1f" % (lo_, flo_, 1 / max(lo_, 1e-12)))
            else: print("      no exclusion even with the form scaled to zero")
            sF[0] = 1.0
    if o[4] >= 0: print("      not excluded" + ("" if os.environ.get("COLLISION_FORM") else " even without any collision")); continue
    lo, hi = 0.0, None; cc = 4000.0
    for _ in range(6):                                                         # the maximum is convex and non-decreasing in c: bracket, then secant
        o2 = solve(cc)
        if o2 is None: break
        if o2[4] < 0: lo = cc; cn = (2 * o2[2] / (K + 1) - o2[3]) * K * (K + 1) / 2 / max(o2[1][0], 1e-9)
        else: hi = cc; cn = (2 * o2[2] / (K + 1) - o2[3]) * K * (K + 1) / 2 / max(o2[1][0], 1e-9)
        last = o2
        if abs(cn - cc) < 3: break
        cc = cn
    print("      break-even c about %.0f  (bracket %s .. %s); vertex there: R %.4gM ceiling %.4gM P %.0f rho %.1f tau %.0f   [%.0f s]" % (
        cc, "%.0f" % lo, "%.0f" % hi if hi else "?", last[2] / 1e6, last[3] / 1e6, last[0][0], last[0][g], last[1][0], time.time() - t0), flush=True)
