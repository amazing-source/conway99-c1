"""C1, lab session, 2026-10-08. A special 10-support inside every pair of twin prisms, and the bound it gives on tau.
  python lp_b10.py <census2 order-10 json> <reps10 json>
Two far prisms X, X' have the same three rung apices c_1, c_2, c_3. For two of them, say c_1, c_2, the 10 vertices
    c_1, c_2, and the rungs 1 and 2 of X and of X'
induce: two bowties (centres c_1, c_2; triangles = rung triangles) joined by the four prism edges a_1a_2, b_1b_2,
a'_1a'_2, b'_1b'_2, plus the edge c_1c_2 if the apices are adjacent. Every vertex has degree >= 3: a SPECIAL support
B10 (16 edges) or B10+ (17 edges), i.e. a census parameter. Each pair of twin prisms contains 3 of them (one per pair of
apices) and a copy determines the two 4-cycles, hence at most one pair of prisms: 3 tau <= N(B10) + N(B10+).
Prints the parameter indices, the maxima of N(B10), N(B10+) and of their sum over the order-10 polytope, alone and
together with tau' <= Phi/4, and at the corner P >= 750. Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); npar = len(D["params"])
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
# vertices: 0 = c1, 1 = c2, 2,3 = a1,b1 (X), 4,5 = a1',b1' (X'), 6,7 = a2,b2 (X), 8,9 = a2',b2' (X')
base = [(0, 2), (0, 3), (2, 3), (0, 4), (0, 5), (4, 5), (1, 6), (1, 7), (6, 7), (1, 8), (1, 9), (8, 9), (2, 6), (3, 7), (4, 8), (5, 9)]
idx = {}
for name, edges in (("B10", base), ("B10+", base + [(0, 1)])):
    rows = [0] * 10
    for i, j in edges: rows[i] |= 1 << j; rows[j] |= 1 << i
    key, perm = C2.canon(10, rows); found = [i for i, p in enumerate(D["params"]) if p[0] == 10 and p[1] == key]
    print("%s: %d edges, |Aut| = %d, parameter index %s" % (name, len(edges), C2.aut_order(10, rows), found), flush=True)
    if found: idx[name] = found[0]
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
cphi, kphi = vec(R["6,3,4"]); eP = np.zeros(npar); eP[0] = 1.0
cb = np.zeros(npar)
for nm, i in idx.items(): cb[i] = 1.0
def mx(c, k0=0.0, extra=None):
    Aub, bub = -A, const
    if extra: Aub = vstack([-A] + [csr_matrix(-e[0].reshape(1, -1)) for e in extra]); bub = np.append(const, [-e[1] for e in extra])
    res = linprog(-c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * npar, method="highs-ipm")
    return (-res.fun + k0, res.x) if res.status == 0 else (float("nan"), None)
for nm, i in idx.items():
    c = np.zeros(npar); c[i] = 1.0; v, x = mx(c); print("max N(%s) = %.6g (P = %.5g there)  [%.0f s]" % (nm, v, x[0], time.time() - t0), flush=True)
v, x = mx(cb); print("max [N(B10) + N(B10+)] = %.6g, so tau <= %.6g ; there P = %.5g, Phi = %.6g" % (v, v / 3, x[0], cphi @ x + kphi), flush=True)
for Pmin in (500.0, 750.0):
    v, x = mx(cb, extra=[(eP, Pmin)]); print("  with P >= %g: max sum = %.6g, tau <= %.6g (Phi = %.6g)" % (Pmin, v, v / 3, cphi @ x + kphi), flush=True)
# joint: maximise t subject to 3 t <= sum and 4 t <= Phi  (t as an extra variable is avoided: maximise min by a scan)
for lam in (0.25, 0.5, 0.75):
    v, x = mx(lam * cb / 3 + (1 - lam) * cphi / 4, (1 - lam) * kphi / 4); print("  max of %.2f * sum/3 + %.2f * Phi/4 = %.6g (sum/3 = %.6g, Phi/4 = %.6g, P = %.5g)" % (lam, 1 - lam, v, cb @ x / 3, (cphi @ x + kphi) / 4, x[0]), flush=True)
