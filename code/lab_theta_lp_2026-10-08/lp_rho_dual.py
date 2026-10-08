"""C1, lab session, 2026-10-08. Which type counts bound the number rho of 3 x 3 grids at 126? (dual of max rho)
  python lp_rho_dual.py <census2 order-10 json>
Prints the maximum of rho over the order-10 polytope and the tight constraints with the largest multipliers
(order, number of edges, degree sequence, constant term and coefficient of rho in N_H). Floating point HiGHS (dual simplex)."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); pc = lambda x: bin(x).count("1")
ri = []; ci = []; va = []; const = []; meta = []; r = 0; seen = set()
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); f = {int(p): float(Fr(v_)) for p, v_ in form.items()}; sc = max(abs(x) for x in f.values())
        const.append(f.get(0, 0.0) / sc); meta.append((int(n), rows, f, sc))
        for p, v_ in f.items():
            if p: ri.append(r); ci.append(p - 1); va.append(v_ / sc)
        r += 1
A = csr_matrix((va, (ri, ci)), shape=(r, npar)); const = np.array(const)
g = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18][0]
c = np.zeros(npar); c[g] = -1.0
res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ds")
print("max rho = %.9g, status %d  [%.0f s]" % (-res.fun, res.status, time.time() - t0), flush=True)
m = -res.ineqlin.marginals; order = np.argsort(-np.abs(m))
print("tight constraints with the largest multipliers (multiplier refers to the scaled row):")
for i in order[:14]:
    if abs(m[i]) < 1e-9: break
    n, rows, f, sc = meta[i]; e = sum(pc(x) for x in rows) // 2; deg = sorted(pc(x) for x in rows)
    nz = sorted(((abs(v_), p) for p, v_ in f.items() if p), reverse=True)[:4]
    print("  multiplier %.5g: order %d, %d edges, degrees %s ; x_H = %.6g %s (%d parameters)" % (m[i], n, e, deg, f.get(0, 0.0), " ".join("%+.6g*p%d" % (f[p], p) for _, p in nz), len(f) - (0 in f)))
x = res.x; nzp = [(i + 1, D["params"][i][0], x[i]) for i in range(npar) if x[i] > 1e-6]
print("non-zero parameters at the optimum (index, order, value):", [(i, o, round(v, 2)) for i, o, v in nzp][:30], "... total", len(nzp))
