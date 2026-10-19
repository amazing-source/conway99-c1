"""Solve min / max P with the census LP (x_H >= 0) plus saved flag blocks (LAB 19/10/2026).  Floating point.
usage: python flag_solve.py <census json> <block files...> [--solver=CLARABEL|SCS] [--obj=min,max]"""
import json, sys, time
import numpy as np
import cvxpy as cp
from scipy.optimize import linprog
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from flag_sdp import Census  # noqa: E402
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
t0 = time.time()
cen = Census(args[0]); NP = cen.NP
rows = []
for (n, key), f in cen.form.items():
    c0 = f.get(0, 0.0); coef = np.zeros(NP)
    for p, val in f.items():
        if p:
            coef[p - 1] = val
    sc = max(abs(c0), np.abs(coef).max(), 1.0)
    rows.append((coef / sc, c0 / sc))
A = np.array([r[0] for r in rows]); b = np.array([r[1] for r in rows])
ref = linprog(np.zeros(NP), A_ub=-A, b_ub=b, bounds=[(0, None)] * NP, method="highs")
svar = np.maximum(np.abs(ref.x), 1.0)
y = cp.Variable(NP)
cons = [A @ cp.multiply(svar, y) + b >= 0, y >= 0]
for f in args[1:]:
    z = np.load(f)
    P0, Pp, ps = z["P0"], z["Pp"], z["params"]
    nf = P0.shape[0]
    if nf == 0:
        continue
    Mref = P0 + sum(ref.x[p - 1] * Pp[i] for i, p in enumerate(ps))
    dg = np.diag(Mref).copy()
    dsc = 1.0 / np.sqrt(np.where(dg > 1e-9 * max(dg.max(), 1.0), dg, max(dg.max(), 1.0)))
    Dm = np.outer(dsc, dsc)
    B = np.zeros((nf * nf, NP))
    for i, p in enumerate(ps):
        B[:, p - 1] = (Pp[i] * Dm).reshape(-1) * svar[p - 1]
    c = (P0 * Dm).reshape(-1)
    Mx = cp.reshape(B @ y + c, (nf, nf), order="C")
    cons.append((Mx + Mx.T) / 2 >> 0)
    print("block %s: size %d" % (f, nf), flush=True)
for sense in opts.get("obj", "min,max").split(","):
    pr = cp.Problem(cp.Minimize(y[0]) if sense == "min" else cp.Maximize(y[0]), cons)
    try:
        pr.solve(solver=opts.get("solver", "CLARABEL"))
        print("P %s: %s %s  [%.0f s]" % (sense, pr.status, None if y.value is None else y.value[0] * svar[0], time.time() - t0), flush=True)
    except Exception as ex:
        print("P %s: ERROR %s" % (sense, str(ex)[:200]), flush=True)
