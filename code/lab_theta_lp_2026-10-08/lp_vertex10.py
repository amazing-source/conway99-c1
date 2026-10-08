"""C1, lab session, 2026-10-08. Raw numbers of norm-8 representatives at the grid-rich end of the census polytope, by
maximal support (9 or 10) and by shape.
  python lp_vertex10.py <census2 order-10 json> <reps10 json>
Minimises r8 (support <= 9, then <= 10) over the order-10 polytope with rho >= 125.9 (floating point HiGHS), and prints
the composition by shape at the support-10 optimum. Exploration: these are raw counts, no collision is removed."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); npar = len(D["params"]); pc = lambda x: bin(x).count("1")
ri = []; ci = []; va = []; const = []; r = 0; seen = set()
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
eG = np.zeros(npar); eG[g] = 1.0
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
Aub = vstack([-A, csr_matrix(-eG.reshape(1, -1))]); bub = np.append(const, -125.9)
shapes = {k_: vec(f) for k_, f in R.items() if k_.endswith(",8")}
for S in (9, 10):
    c = sum(v[0] for k_, v in shapes.items() if sum(int(x) for x in k_.split(",")[:2]) <= S); k0 = sum(v[1] for k_, v in shapes.items() if sum(int(x) for x in k_.split(",")[:2]) <= S)
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * npar, method="highs-ipm"); x = res.x
    print("support <= %d, rho >= 125.9: min r8 = %.5gM (P = %.0f, rho = %.1f)  [%.0f s]" % (S, (res.fun + k0) / 1e6, x[0], x[g], time.time() - t0), flush=True)
    res2 = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    print("   without the condition on rho: min r8 = %.5gM (rho = %.1f)" % ((res2.fun + k0) / 1e6, res2.x[g]), flush=True)
for k_ in sorted(shapes, key=lambda s_: (sum(int(y) for y in s_.split(",")[:2]), s_)):
    a_, b_ = (int(y) for y in k_.split(",")[:2])
    if a_ >= b_: print("   shape (%d,%d): %.5gM (one sign)" % (a_, b_, (shapes[k_][0] @ x + shapes[k_][1]) / 1e6))
