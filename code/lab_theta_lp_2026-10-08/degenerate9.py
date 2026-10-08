"""C1, lab session, 2026-10-08. The injective family of 2-degenerate sets: pure indicators 1_W.

  python degenerate9.py <census2 order-10 json>

Two indicators 1_W, 1_W' of sets of the same size give the same vector of M (t = 0) only if W - W' induces a graph of
minimum degree >= 3. So the 2-DEGENERATE sets (every induced subgraph has a vertex of degree <= 2) of a given size give
pairwise distinct classes. Q(1_W) = 3n + n^2/9 - 2 e(W): n = 6: 22 - 2e; n = 9: 36 - 2e.
Output: the numbers of 2-degenerate 9-sets with 16, 15, 14 edges (norms 4, 6, 8) and of all 9-sets with those numbers
of edges, as affine forms (constant terms shown), and their minima over the order-10 polytope (floating point HiGHS,
exploration). Needs numpy and scipy."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); pc = lambda x: bin(x).count("1")
def two_degenerate(n, rows):
    alive = (1 << n) - 1
    while alive:
        for v in range(n):
            if alive >> v & 1 and pc(rows[v] & alive) <= 2: alive &= ~(1 << v); break
        else: return False
    return True
forms = {}
for key, rows, aut, form in D["types"]["9"]:
    e = sum(pc(r) for r in rows) // 2
    if e not in (14, 15, 16): continue
    td = two_degenerate(9, rows)
    for tag in (("all", e),) + ((("2deg", e),) if td else ()):
        acc = forms.setdefault(tag, {})
        for p, v_ in form.items(): acc[int(p)] = acc.get(int(p), 0) + Fr(v_) / aut
    forms.setdefault(("types", e), [0, 0]); forms[("types", e)][0] += 1; forms[("types", e)][1] += td
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
for e in (16, 15, 14):
    nt = forms[("types", e)]
    for tag in ("all", "2deg"):
        f = forms.get((tag, e), {}); c = np.zeros(npar)
        for p, v_ in f.items():
            if p: c[p - 1] = float(v_)
        res = linprog(c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
        res2 = linprog(-c, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs-ipm")
        print("9-sets with %d edges (norm %d), %s: %d types%s; constant term %s; minimum %.9g, maximum %.9g  [%.0f s]" % (
            e, 36 - 2 * e, tag, nt[0] if tag == "all" else nt[1], "" if tag == "all" else " (2-degenerate)", f.get(0, 0),
            res.fun + float(f.get(0, 0)) if res.status == 0 else float("nan"), -res2.fun + float(f.get(0, 0)) if res2.status == 0 else float("inf"), time.time() - t0), flush=True)
