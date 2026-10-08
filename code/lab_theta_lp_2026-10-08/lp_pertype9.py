"""C1, lab session, 2026-10-08. Rank 37, exploration: supports <= 9 with a PER-TYPE penalty on the order-9 special
supports instead of a uniform one.

  python lp_pertype9.py <census2 order-10 json> <reps10 json> <l6> <l7> <l8> <dense9>

For a 14-edge special 9-support X (degrees 3^8 4) a mass-9 collision of the family (6,3) needs a triangle in X or in its
twin: at most t_X p_Y + t_X t_Y + p_X t_Y per twin pair (t = triangles, p = induced 2-paths of degree-3 vertices), plus
1 for the indicators (9,0). With at most 2 twins per support and the pair charged to both members, the penalty used
here for such a type is 2 (t_X (Pmax + Tmax) + p_X Tmax + 1), where Tmax, Pmax are the maxima over the 14-edge special
types. Special 9-supports with 15 edges or more get the constant <dense9>. Orders 6, 7, 8 get l6, l7, l8 per support.
Floating point, exploration: none of these constants is proved (the 15+ edge types and mass 8 are guesses)."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
t0 = time.time(); D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); l6, l7, l8, dense9 = [float(x) for x in sys.argv[3:7]]
npar = len(D["params"]); ri = []; ci = []; va = []; const = []; r = 0; seen = set(); pc = lambda x: bin(x).count("1")
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
info = []
for i, (n, key, rows) in enumerate(D["params"]):
    e = sum(pc(x) for x in rows) // 2; deg = [pc(x) for x in rows]
    t = sum(1 for a in range(n) for b in range(a + 1, n) for c in range(b + 1, n) if rows[a] >> b & 1 and rows[a] >> c & 1 and rows[b] >> c & 1)
    p = sum(1 for m in range(n) if deg[m] == 3 for a in range(n) for b in range(a + 1, n) if rows[m] >> a & 1 and rows[m] >> b & 1 and not rows[a] >> b & 1 and deg[a] == 3 and deg[b] == 3)
    info.append((n, e, t, p))
T14 = max(t for n, e, t, p in info if n == 9 and e == 14); P14 = max(p for n, e, t, p in info if n == 9 and e == 14)
pen = np.zeros(npar); hist = {}
for i, (n, e, t, p) in enumerate(info):
    if n == 6: pen[i] = l6
    elif n == 7: pen[i] = l7
    elif n == 8: pen[i] = l8
    elif n == 9:
        pen[i] = 2 * (t * (P14 + T14) + p * T14 + 1) if e == 14 else dense9
        hist.setdefault(e, []).append((t, int(pen[i])))
print("order-9 special types by number of edges: %s; Tmax = %d, Pmax = %d" % ({e: len(v_) for e, v_ in sorted(hist.items())}, T14, P14))
print("14-edge special 9-types: (triangles, penalty) = %s" % sorted(hist.get(14, [])))
def vec(form):
    c = np.zeros(npar)
    for p, v_ in form.items():
        if int(p): c[int(p) - 1] = float(Fr(v_))
    return c, float(Fr(form.get("0", 0)))
c8 = np.zeros(npar); k8 = 0.0; c6 = np.zeros(npar); k6 = 0.0
for k_, f in R.items():
    a, b, q = [int(x) for x in k_.split(",")]
    if a + b > 9 or q == 4: continue
    c, k0 = vec(f)
    if q == 8: c8 += c; k8 += k0
    else: c6 += c; k6 += k0
orders = np.array([x[0] for x in info]); edges = np.array([x[1] for x in info])
res = linprog(c8 + (651 / 34) * c6 - pen, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm"); x = res.x
print("penalties l6 = %g, l7 = %g, l8 = %g, per type at order 9 (dense: %g): minimum = %.8g ; r6 = %.6g, r8 = %.8g ; supports: order 6 %.5g, order 7 %.5g, order 8 %.6g, order 9 with 14 edges %.6g (penalised %.6g), with >= 15 edges %.6g  [%.0f s]" % (
    l6, l7, l8, dense9, res.fun + k8 + (651 / 34) * k6, c6 @ x + k6, c8 @ x + k8, x[orders == 6].sum(), x[orders == 7].sum(), x[orders == 8].sum(),
    x[(orders == 9) & (edges == 14)].sum(), (pen * x)[(orders == 9) & (edges == 14)].sum(), x[(orders == 9) & (edges >= 15)].sum(), time.time() - t0), flush=True)
