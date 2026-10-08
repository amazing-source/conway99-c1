"""C1, lab session, 2026-10-08. Floating-point LP over the order-10 census polytope (EXPLORATION, not a certificate).

  python lp_order10.py <census2 order-10 json>      (needs numpy and scipy; my own JSON, my own modules)

Variables: the 57 + 492 numbers of copies of the types of minimum degree >= 3 (orders 6 to 10). Constraints: the embedding
count of every admissible type of order 6 to 10 is >= 0 (census2.py). Objectives: the signed number Q6 of representatives
of norm 6 of the family (5,5), i.e. twice the number of unordered anticomplete pairs of 5-sets with 6 edges (bowtie or
house), and a few other quantities for orientation. HiGHS in floating point: the values are indications; any bound to be
used must be re-derived with exact rationals from the dual solution."""
import sys, json, time
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); npar = len(D["params"]); print("loaded: %d parameters  [%.0f s]" % (npar, time.time() - t0), flush=True)
key10 = {}
rows_i = []; cols_i = []; vals = []; const = []; r = 0; forms = {}
for n in ("6", "7", "8", "9", "10"):
    for key, rows, aut, form in D["types"][n]:
        f = {int(p): Fr(v_) for p, v_ in form.items()}; forms[(int(n), key)] = f
        const.append(float(f.get(0, 0)))
        for p, v_ in f.items():
            if p: rows_i.append(r); cols_i.append(p - 1); vals.append(float(v_))
        r += 1
A = csr_matrix((vals, (rows_i, cols_i)), shape=(r, npar)); const = np.array(const); print("constraints: %d  [%.0f s]" % (r, time.time() - t0), flush=True)
BOW = [(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4)]; HOUSE = [(0, 1), (0, 2), (1, 2), (1, 3), (3, 4), (4, 0)]
def union(e1, e2):
    rows = [0] * 10
    for a, b in e1: rows[a] |= 1 << b; rows[b] |= 1 << a
    for a, b in e2: rows[a + 5] |= 1 << (b + 5); rows[b + 5] |= 1 << (a + 5)
    return rows
obj = {}
for nm, (e1, e2) in (("bowtie+bowtie", (BOW, BOW)), ("bowtie+house", (BOW, HOUSE)), ("house+house", (HOUSE, HOUSE))):
    rows = union(e1, e2); key, _ = C2.canon(10, rows); aut = C2.aut_order(10, rows); f = forms[(10, key)]
    print("  %-14s |Aut| = %d, constant term of N = %s, %d parameters involved" % (nm, aut, f.get(0, 0) / aut, len(f) - (0 in f)))
    for p, v_ in f.items(): obj[p] = obj.get(p, 0) + 2 * v_ / aut
c = np.zeros(npar)
for p, v_ in obj.items():
    if p: c[p - 1] = float(v_)
c0 = float(obj.get(0, 0)); print("Q6 of (5,5) = %.6g + (linear form in %d parameters)" % (c0, int(np.count_nonzero(c))), flush=True)
def run(cvec, c00, label, sense=1):
    res = linprog(sense * cvec, A_ub=-A, b_ub=const, bounds=[(0, None)] * npar, method="highs")
    if res.status != 0: print("  %s: status %d (%s)" % (label, res.status, res.message), flush=True); return None
    val = sense * res.fun + c00; print("  %s = %.9g   (P = %.6g, H = %.6g)  [%.0f s]" % (label, val, res.x[0], res.x[1], time.time() - t0), flush=True); return res
run(c, c0, "minimum of Q6(5,5) over the order-10 polytope")
e0 = np.zeros(npar); e0[0] = 1.0; run(e0, 0.0, "maximum of P", -1)
e1 = np.zeros(npar); e1[1] = 1.0; run(e1, 0.0, "maximum of H", -1)
