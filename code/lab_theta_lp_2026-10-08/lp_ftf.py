"""C1, lab session, 2026-10-08. Rank 37: what the sub-family Ftf of (6,3) adds (Codex's request, bridge message of 10:40).
  python lp_ftf.py <census2 order-10 json> <reps10 json>
Ftf = pairs (W, T): W a TRIANGLE-FREE 6-set with 7 edges, T a triangle far from W; psi = +-(1_W - 1_T), norm 8.
Codex's certified losses (both signs): mass 6: 672 tau (192 internal + 480 against (5,2)); mass 7: 716 Omega.
Base families (supports <= 9): B = all shapes except (6,3),(3,6); C = B with (9,0),(0,9) restricted to 2-degenerate sets.
Charged: -((3228 + 672)/4) Phi (4 tau <= Phi; 3228 = Codex's (4,4) and (5,2)), and -716 kappa H for the mass-7 term
under the HYPOTHESIS Omega <= kappa H (H = number of 7-vertex 11-edge supports), kappa = 0, 1, 2.
NOT charged (no constant yet): twin-prism collisions of (7,1), (3,3), (6,0)x(7,1), (2,2)x(4,4), (4,1)x(5,2), of the
non-2-degenerate 9-sets (family B only), norm-6 collisions, masses 8 and 9, windmills, grids.
Prints the minimum of R - penalties for R = r8 and R = r8 + (651/34) r6. Floating point HiGHS, exploration.
Ceilings (Codex, note 192): 15.98M (b_4 alone), 16.85M (coupled)."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2]))
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
def two_degenerate(n, rows):
    alive = (1 << n) - 1
    while alive:
        for v in range(n):
            if alive >> v & 1 and pc(rows[v] & alive) <= 2: alive &= ~(1 << v); break
        else: return False
    return True
z = lambda: [np.zeros(npar), 0.0]
def addf(acc, form, w):
    for p, v_ in form.items():
        val = float(Fr(v_)) * w
        if int(p): acc[0][int(p) - 1] += val
        else: acc[1] += val
c90 = z(); ftf = z(); f0 = z(); wtypes = {}
for key, rows, aut, form in D["types"]["9"]:
    e_tot = sum(pc(x) for x in rows) // 2
    if e_tot == 14 and two_degenerate(9, rows): addf(c90, form, 1.0 / aut)
    if e_tot != 10: continue
    n0 = 0; ntf = 0
    for W in combinations(range(9), 6):
        wm = sum(1 << i for i in W); Y = [i for i in range(9) if not wm >> i & 1]
        ew = sum(pc(rows[i] & wm) for i in W) // 2
        if ew != 7 or any(rows[y] & wm for y in Y): continue           # 7 edges in W, no cross edge, hence Y a triangle
        n0 += 1
        tri = any(rows[a] >> b & 1 and rows[a] >> c & 1 and rows[b] >> c & 1 for a, b, c in combinations(W, 3))
        if not tri:
            ntf += 1; deg = tuple(sorted(pc(rows[i] & wm) for i in W)); wtypes[deg] = wtypes.get(deg, 0) + 1
    if n0: addf(f0, form, n0 / aut)
    if ntf: addf(ftf, form, ntf / aut)
print("triangle-free W inside F0, by degree sequence (number of order-9 types):", wtypes, flush=True)
def vec(form):
    acc = z(); addf(acc, form, 1.0); return acc
fam = {x: {8: z(), 6: z()} for x in "BC"}
def put(names, q, acc, w=1.0):
    for nm in names: fam[nm][q][0] += w * acc[0]; fam[nm][q][1] += w * acc[1]
for k_, f in R.items():
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > 9 or q_ not in (6, 8) or (a_, b_) in ((6, 3), (3, 6)): continue
    v = vec(f); put("B", q_, v)
    if (a_, b_) in ((9, 0), (0, 9)): continue
    put("C", q_, v)
put("C", 8, c90, 2.0)
cphi, kphi = vec(R["6,3,4"]); eH = np.zeros(npar); eH[1] = 1.0
def lp(c): return linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
for nm, acc in (("F0", f0), ("Ftf", ftf)):
    res = lp(acc[0]); res2 = lp(-acc[0]); print("%s (one sign): constant %.6g ; min %.6g ; max %.6g  [%.0f s]" % (nm, acc[1], res.fun + acc[1], -res2.fun + acc[1], time.time() - t0), flush=True)
mu0 = 3228 / 4; mu1 = (3228 + 672) / 4
for nm in "BC":
    for label, c, k0 in (("r8", fam[nm][8][0], fam[nm][8][1]), ("coupled", fam[nm][8][0] + (651 / 34) * fam[nm][6][0], fam[nm][8][1] + (651 / 34) * fam[nm][6][1])):
        res = lp(c - mu0 * cphi); base = res.fun + k0 - mu0 * kphi; out = []
        for kap in (0, 1, 2):
            res = lp(c + 2 * ftf[0] - mu1 * cphi - 716 * kap * eH); x = res.x
            out.append("kappa=%d: %.4gM (2 Ftf = %.4gM, Phi = %.0f, P = %.0f, H = %.0f)" % (kap, (res.fun + k0 + 2 * ftf[1] - mu1 * kphi) / 1e6, 2 * (ftf[0] @ x + ftf[1]) / 1e6, cphi @ x + kphi, x[0], x[1]))
        print("family %s, %-7s without Ftf: %.4gM ; with Ftf: %s  [%.0f s]" % (nm, label, base / 1e6, " | ".join(out), time.time() - t0), flush=True)
