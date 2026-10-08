"""C1, lab session, 2026-10-08. Rank 37: the lower bound on the families whose collisions have a method.
  python lp_route37.py <census2 order-10 json> <reps10 json>
Kept: all shapes of support <= 9 except (6,3), (3,6); the pure 9-sets (9,0), (0,9) only when 2-DEGENERATE (pure
indicators of 2-degenerate sets of one size are pairwise distinct at t = 0, so no mass-9 collision is left, and no
mass-8 collision inside (9,0)). Twin-prism losses at norm 8 charged as -(3228/4) Phi (Codex's constants for (4,4) and
(5,2); Phi = #(prism, far triangle), 4 tau <= Phi). Optional penalty per special 8-support (argument: lambda8 ...), to
see what the mass-8 channel of (4,4) and (7,1) can cost: a cubic 8-support has at most |far set| / 8 twins.
Prints the minimum of r8 and of r8 + (651/34) r6 over the order-10 polytope. Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); lam8 = [float(x) for x in sys.argv[3:]] or [0.0]
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
c90 = np.zeros(npar); k90 = 0.0
for key, rows, aut, form in D["types"]["9"]:
    if sum(pc(x) for x in rows) // 2 != 14 or not two_degenerate(9, rows): continue
    for p, v_ in form.items():
        val = float(Fr(v_)) / aut
        if int(p): c90[int(p) - 1] += val
        else: k90 += val
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
c8 = 2 * c90; k8 = 2 * k90; c6 = np.zeros(npar); k6 = 0.0; comp = {}
for k_, f in R.items():
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > 9 or (a_, b_) in ((6, 3), (3, 6), (9, 0), (0, 9)): continue
    cc, kk = vec(f)
    if q_ == 8: c8 = c8 + cc; k8 += kk; comp[k_] = (cc, kk)
    if q_ == 6: c6 = c6 + cc; k6 += kk
comp["9,0,8 (2-degenerate, both signs)"] = (2 * c90, 2 * k90)
cphi, kphi = vec(R["6,3,4"]); orders = np.array([p[0] for p in D["params"]]); mu = 3228 / 4
cubic8 = np.array([1.0 if (p[0] == 8 and sum(pc(x) for x in p[2]) // 2 == 12) else 0.0 for p in D["params"]])
for l8 in lam8:
    for name, c, k0 in (("r8", c8, k8), ("r8 + (651/34) r6", c8 + (651 / 34) * c6, k8 + (651 / 34) * k6)):
        res = linprog(c - mu * cphi - l8 * cubic8, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
        if res.status != 0: print(name, res.message[:60]); continue
        x = res.x
        print("penalty %g per cubic 8-support: min of [%s - 807 Phi - penalty] = %.6g ; there P = %.5g, Phi = %.6g, cubic 8-supports = %.6g, all 8-supports = %.6g  [%.0f s]" % (
            l8, name, res.fun + k0 - mu * kphi, x[0], cphi @ x + kphi, cubic8 @ x, x[orders == 8].sum(), time.time() - t0), flush=True)
        if l8 == lam8[0] and name == "r8":
            for k_ in sorted(comp, key=lambda s: (len(s), s)): print("      shape %s: %.6g" % (k_, comp[k_][0] @ x + comp[k_][1]))
