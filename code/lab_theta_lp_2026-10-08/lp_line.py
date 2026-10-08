"""C1, lab session, 2026-10-08. Bounds on the pairs of grids sharing a line T from sub-configurations that contain T
(suggested by the laptop session). Two grids G = (T, A, B), G' = (T, A', B') on a common line T induce K_3 x bowtie.
  H9  = T, A, A' (K_3 x P_3 with T in the middle): 4 copies per pair of grids                     -> 4 tau_g <= N(H9)
  H10a = H9 + one vertex of B (adjacent to its column mates in T and A): 24 copies per pair      -> 24 tau_g <= N(H10a)
  H10b = (G minus one vertex of T) + a rung {a', b'} of G' at another vertex of T: 12 copies      -> 12 tau_g <= N(H10b)
(a copy determines the two grids: H9 fixes T, A, A' and the third rows are forced when they exist.)
  python lp_line.py <census2 order-10 json> <reps10 json>
Prints the maxima of the three counts, the maximum of tau_g and of tau_g + tau_n under all linear bounds known today
(17 tau_g <= 207 rho, tau_n <= P - 6 rho, 4 (tau_g + tau_n) <= Phi and the three new ones), and the budget LP
(class quotient k = 2, all shapes of support <= 9). Floating point HiGHS, exploration."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
import census2 as C2
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
def graph(n, edges):
    rows = [0] * n
    for i, j in edges: rows[i] |= 1 << j; rows[j] |= 1 << i
    return rows
# vertices of K_3 x bowtie: T = 0,1,2 ; A = 3,4,5 ; B = 6,7,8 ; A' = 9,10,11 ; B' = 12,13,14 ; column i: i, 3+i, 6+i (grid G) and i, 9+i, 12+i (grid G')
E15 = []
for base in (0, 3, 6, 9, 12): E15 += [(base, base + 1), (base, base + 2), (base + 1, base + 2)]
for i in range(3): E15 += [(i, 3 + i), (i, 6 + i), (3 + i, 6 + i), (i, 9 + i), (i, 12 + i), (9 + i, 12 + i)]
full = graph(15, E15)
def induced(vs):
    idx = {v: k for k, v in enumerate(vs)}
    return [sum(1 << idx[u] for u in vs if full[v] >> u & 1) for v in vs]
def form_of(vs):
    n = len(vs); rows = induced(vs); key, perm = C2.canon(n, rows)
    for k_, rw, aut, form in D["types"][str(n)]:
        if k_ == key:
            a = aut if aut else C2.aut_order(n, rw); c = np.zeros(npar); k0 = 0.0
            for p, v_ in form.items():
                if int(p): c[int(p) - 1] = float(Fr(v_)) / a
                else: k0 = float(Fr(v_)) / a
            return c, k0, sum(pc(x) for x in rows) // 2
    raise SystemExit("type not found")
H = {"H9": (form_of([0, 1, 2, 3, 4, 5, 9, 10, 11]), 4), "H10a": (form_of([0, 1, 2, 3, 4, 5, 9, 10, 11, 6]), 24), "H10b": (form_of([1, 2, 3, 4, 5, 6, 7, 8, 10, 13]), 12)}
g = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18][0]
eP = np.zeros(npar); eP[0] = 1.0; eG = np.zeros(npar); eG[g] = 1.0
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
cphi, kphi = vec(R["6,3,4"])
for nm, ((c, k0, e), m) in H.items():
    res = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
    print("%s: %d edges, %d copies per pair of grids on a line; max N = %.6g, so tau_g <= %.6g (rho = %.1f, P = %.0f there)  [%.0f s]" % (nm, e, m, -res.fun + k0, (-res.fun + k0) / m, res.x[g], res.x[0], time.time() - t0), flush=True)
row = lambda v, tg, tn: csr_matrix(np.concatenate([v, [tg, tn]]).reshape(1, -1))
rows_ = [hstack([-A, csr_matrix((A.shape[0], 2))]), row(-207 * eG, 17.0, 0.0), row(-(eP - 6 * eG), 0.0, 1.0), row(-cphi, 4.0, 4.0), row(-(eP - 6 * eG), 0.0, 0.0)]
b_ = list(const) + [0.0, 0.0, kphi, 0.0]
for nm, ((c, k0, e), m) in H.items(): rows_.append(row(-c, float(m), 0.0)); b_.append(k0)
ext = vstack(rows_); bext = np.array(b_)
for label, obj in (("tau_g", np.concatenate([np.zeros(npar), [-1.0, 0.0]])), ("tau_g + tau_n", np.concatenate([np.zeros(npar), [-1.0, -1.0]]))):
    res = linprog(obj, A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 2), method="highs-ipm"); x = res.x
    print("max %s = %.6g (tau_g = %.0f, tau_n = %.0f, rho = %.1f, P = %.0f)  [%.0f s]" % (label, -res.fun, x[npar], x[npar + 1], x[g], x[0], time.time() - t0), flush=True)
c8 = np.zeros(npar); k8 = 0.0
for k_, f in R.items():
    a_, b2, q_ = (int(x) for x in k_.split(","))
    if a_ + b2 > 9 or q_ != 8: continue
    cc, kk = vec(f); c8 += cc; k8 += kk
for cc in (16000.0, 24000.0, 30000.0):
    res = linprog(np.concatenate([2 * c8 / 3, [-cc / 3, -cc / 3]]), A_ub=ext, b_ub=bext, bounds=[(0, None)] * (npar + 2), method="highs-ipm"); x = res.x
    print("budget LP, c = %g for both kinds, k = 2: bound %.4gM ; there R = %.4gM, P = %.0f, rho = %.1f, tau_g = %.0f, tau_n = %.0f  [%.0f s]" % (
        cc, (res.fun + 2 * k8 / 3) / 1e6, (c8 @ x[:npar] + k8) / 1e6, x[0], x[g], x[npar], x[npar + 1], time.time() - t0), flush=True)
