"""C1, lab session, 2026-10-08. Rank 37: where the representative counts stand AT the twin-prism corner.
  python lp_corner.py <census2 order-10 json> <reps10 json>
For several values of mu, minimises [R - mu Phi] and prints R itself at the optimum, for four families of supports <= 9:
  A = all shapes;  B = all except (6,3),(3,6);  C = B with (9,0),(0,9) restricted to 2-degenerate sets;
  D = C plus the two large sub-families of (6,3): (7,3,0) and (8,2,0) (both signs).
R is r8 (b_4 alone) or r8 + (651/34) r6. Floating point HiGHS, exploration. The point: the total weight c of ALL
twin-prism collisions per twin pair (mu = c/4) that each family can afford against the ceilings 15.98M / 16.85M."""
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
c90 = z(); sub = {(7, 3, 0): z(), (8, 2, 0): z()}
def addf(acc, form, w):
    for p, v_ in form.items():
        val = float(Fr(v_)) * w
        if int(p): acc[0][int(p) - 1] += val
        else: acc[1] += val
for key, rows, aut, form in D["types"]["9"]:
    e_tot = sum(pc(x) for x in rows) // 2
    if e_tot == 14 and two_degenerate(9, rows): addf(c90, form, 1.0 / aut)
    if e_tot < 10: continue
    cnt = {}
    for W in combinations(range(9), 6):
        wm = sum(1 << i for i in W); ym = 511 & ~wm; ew = sum(pc(rows[i] & wm) for i in W) // 2; cross = sum(pc(rows[i] & ym) for i in W); ey = e_tot - ew - cross
        if (ew, ey, cross) in sub: cnt[(ew, ey, cross)] = cnt.get((ew, ey, cross), 0) + 1
    for k_, m in cnt.items(): addf(sub[k_], form, m / aut)
def vec(form):
    acc = z(); addf(acc, form, 1.0); return acc
fam = {x: {8: z(), 6: z()} for x in "ABCD"}
def put(names, q, acc, w=1.0):
    for nm in names: fam[nm][q][0] += w * acc[0]; fam[nm][q][1] += w * acc[1]
for k_, f in R.items():
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > 9 or q_ not in (6, 8): continue
    v = vec(f); put("A", q_, v)
    if (a_, b_) in ((6, 3), (3, 6)): continue
    put("B", q_, v)
    if (a_, b_) in ((9, 0), (0, 9)): continue
    put("CD", q_, v)
put("CD", 8, c90, 2.0); put("D", 8, sub[(7, 3, 0)], 2.0); put("D", 8, sub[(8, 2, 0)], 2.0)
cphi, kphi = vec(R["6,3,4"])
for nm in "ABCD":
    for label, c, k0 in (("r8", fam[nm][8][0], fam[nm][8][1]), ("coupled", fam[nm][8][0] + (651 / 34) * fam[nm][6][0], fam[nm][8][1] + (651 / 34) * fam[nm][6][1])):
        out = []
        for mu in (0, 500, 1000, 2000, 4000):
            res = linprog(c - mu * cphi, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm"); x = res.x
            out.append("c=%d: %.4gM (R=%.4gM, Phi=%.0f)" % (4 * mu, (res.fun + k0 - mu * kphi) / 1e6, (c @ x + k0) / 1e6, cphi @ x + kphi))
        print("family %s, %-7s  %s  [%.0f s]" % (nm, label, " | ".join(out), time.time() - t0), flush=True)
