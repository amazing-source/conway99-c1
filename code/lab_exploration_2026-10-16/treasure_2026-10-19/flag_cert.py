"""Exact certificate for an upper bound on P from census rows + E3 zeros + integer flag cuts (LAB 19/10/2026).

Input: census JSON (exact forms), E3 zero ids, the saved cuts (flag_cut_exact.py --save): block file names and
integer vectors u.  Steps:
  1. every cut  sum_H c_H x_H(x) >= 0  is rebuilt EXACTLY (c_H = sum over block entries u_i u_j (2 off the diagonal)
     mult, Python integers; x_H(x) = exact affine form of the census);  valid for every srg(99,14,1,2) because
     M_sigma = sum_theta v_theta v_theta^T is PSD;
  2. the LP  max P  over these rows is solved in floating point (HiGHS) and its duals are taken;
  3. the duals are rounded to rationals and the bound is proved EXACTLY:
        P = -sum_r y_r (a_r . x - b_r) - sum_e w_e (a_e . x - b_e) - s . x  - sum_r y_r b_r - sum_e w_e b_e
     with y_r >= 0, s_p = -(e_P + sum y a + sum w a_e)_p; components with s_p < 0 are paid with an exact a priori upper
     bound x_p <= U_p (U_p = C(99, n_p) for a parameter type of order n_p, an unlabelled count), so
        P <= B := -sum y b - sum w b_e + sum_{p : s_p < 0} |s_p| U_p .
Output: the exact bound B (a Fraction) and a JSON certificate.
usage: python flag_cert.py <census json> <e3 ids> <cuts npz> <T dir> <out json> [--scale=1e9]"""
import json, math, os, sys, time
from fractions import Fraction as Fr
import numpy as np
import scipy.sparse as sp
import highspy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flag_engine import load_types  # noqa: E402

path, e3path, cutpath, tdir, outpath = sys.argv[1:6]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
SCALE = int(float(opts.get("scale", "1e9")))
t0 = time.time()
d, tid, forms = load_types(path)
NP = len(d["params"]); ntypes = len(forms)
exact = [{int(p): Fr(v) for p, v in f.items()} for f in forms]          # x_H = sum_p exact[H][p] x_p (x_0 = 1)
zero = [int(l) for l in open(e3path) if l.strip()]
cz = np.load(cutpath, allow_pickle=True)
cut_blocks, cut_u = list(cz["blocks"]), list(cz["u"])
print("census %d types, %d parameters; %d cuts  [%.0f s]" % (ntypes, NP, len(cut_u), time.time() - t0), flush=True)
cache = {}
cuts_exact = []                                                         # list of dict param -> Fraction (affine)
for name, u in zip(cut_blocks, cut_u):
    if name not in cache:
        b = np.load(os.path.join(tdir, str(name)))
        cache[name] = (int(b["nf"]), b["pairs"], b["tids"], b["mult"])
    nf, pairs, tids, mult = cache[name]
    u = [int(v) for v in u]
    cH = {}
    for pr, t, m in zip(pairs.tolist(), tids.tolist(), mult.tolist()):
        i, j = divmod(pr, nf)
        w = u[i] * u[j] * (1 if i == j else 2) * m
        if w:
            cH[t] = cH.get(t, 0) + w
    cut = {}
    for t, c in cH.items():
        for p, v in exact[t].items():
            cut[p] = cut.get(p, 0) + c * v
    cuts_exact.append(cut)
print("cuts rebuilt exactly  [%.0f s]" % (time.time() - t0), flush=True)
# floating LP: rows = types (>= 0), E3 rows (= 0), cuts (>= 0); maximise P = x_1
def to_row(aff):
    s = max([abs(float(v)) for v in aff.values()] + [1.0])
    row = np.zeros(NP); c0 = 0.0
    for p, v in aff.items():
        if p == 0:
            c0 = float(v) / s
        else:
            row[p - 1] = float(v) / s
    return row, c0, s
rows, consts, scales, kinds = [], [], [], []
for t in range(ntypes):
    r, c0, s = to_row(exact[t]); rows.append(r); consts.append(c0); scales.append(s)
    kinds.append("eq" if t in set(zero) else "type")
for cut in cuts_exact:
    r, c0, s = to_row(cut); rows.append(r); consts.append(c0); scales.append(s); kinds.append("cut")
A = sp.csr_matrix(np.array(rows)); c0 = np.array(consts)
h = highspy.Highs(); h.setOptionValue("output_flag", False)
inf = highspy.kHighsInf
h.addVars(NP, np.zeros(NP), np.full(NP, inf))
cost = np.zeros(NP); cost[0] = 1.0
h.changeColsCost(NP, np.arange(NP, dtype=np.int32), cost)
h.changeObjectiveSense(highspy.ObjSense.kMaximize)
lo = -c0; hi = np.array([(-c0[i] if kinds[i] == "eq" else inf) for i in range(len(kinds))])
h.addRows(len(kinds), lo, hi, A.nnz, A.indptr[:-1].astype(np.int32), A.indices.astype(np.int32), A.data)
h.run()
sol = h.getSolution()
Pf = float(sol.col_value[0])
rd = np.array(sol.row_dual)
print("floating LP: P max = %.6f, status %s  [%.0f s]" % (Pf, h.modelStatusToString(h.getModelStatus()), time.time() - t0),
      flush=True)
# exact verification.  For max P with rows a.x >= b (b = -c0): duals of >= rows are <= 0 in HiGHS's convention for a
# maximisation; we take y = max(0, -rd) for inequality rows, w = -rd for equality rows, then compute the residual.
y = []
for i, k in enumerate(kinds):
    v = -rd[i]
    if k != "eq" and v < 0:
        v = 0.0
    y.append(Fr(round(v * SCALE), SCALE))
resid = [Fr(0)] * (NP + 1)                                              # e_P + sum y_r (affine_r / scale_r)
resid[1] += 1
src = [(exact[t], scales[t]) for t in range(ntypes)] + [(cut, scales[ntypes + k]) for k, cut in enumerate(cuts_exact)]
for yi, (aff, s) in zip(y, src):
    if yi == 0:
        continue
    f = yi / Fr(s).limit_denominator(10 ** 12) if not float(s).is_integer() else yi / int(s)
    for p, v in aff.items():
        resid[p] += f * v
# P = (e_P . x)  and  e_P = resid_lin - sum y a  =>  P = resid . (1,x) - resid_0 - sum y_r affine_r(x) ...
# bound: P <= -resid_0' + sum_{p: resid_p > 0} resid_p U_p  where resid_0' = constant part handled below
from math import comb
U = {}
for idx, (n, key, rws) in enumerate(d["params"]):
    U[idx + 1] = comb(99, n)
B = -resid[0] + 1 * 0
# P x-coefficient identity:  sum y_r affine_r(x) = resid(x) - P  =>  P = resid(x) - sum y_r affine_r(x) <= resid(x)
# resid(x) = resid_0 + sum_p resid_p x_p <= resid_0 + sum_{resid_p > 0} resid_p U_p
B = resid[0] + sum(resid[p] * U[p] for p in range(1, NP + 1) if resid[p] > 0)
print("EXACT: P <= %s = %.6f   (positive residual parameters: %d)" % (B, float(B), sum(1 for p in range(1, NP + 1) if resid[p] > 0)),
      flush=True)
json.dump({"bound": str(B), "bound_float": float(B), "floating_lp": Pf, "cuts": len(cuts_exact),
           "positive_residual_params": [p for p in range(1, NP + 1) if resid[p] > 0]}, open(outpath, "w"), indent=1)
