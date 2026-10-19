"""Native Clarabel SDP for min / max P with the census LP and saved flag blocks (LAB 19/10/2026).  Floating point.
Variables y = x / s (x = census parameters, s = scale from an LP reference point).  Constraints: x_H >= 0 for all types,
x >= 0, and every block M(x) = P0 + sum_p x_p Pp PSD (scaled svec, upper triangle, column-major, as Clarabel expects).
usage: python flag_solve2.py <census json> <block files...> [--obj=min,max] [--maxit=N]"""
import sys, time
import numpy as np
import scipy.sparse as sp
import clarabel
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
As = A * svar                      # in y
blocksA, blocksb, cones = [sp.csc_matrix(-As), sp.csc_matrix(-np.eye(NP))], [b, np.zeros(NP)], \
    [clarabel.NonnegativeConeT(A.shape[0]), clarabel.NonnegativeConeT(NP)]
def svec(M):
    n = M.shape[0]; out = []
    for j in range(n):
        for i in range(j + 1):
            out.append(M[i, j] * (1.0 if i == j else np.sqrt(2.0)))
    return np.array(out)
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
    cols = np.zeros((nf * (nf + 1) // 2, NP))
    for i, p in enumerate(ps):
        cols[:, p - 1] = svec((Pp[i] + Pp[i].T) / 2 * Dm) * svar[p - 1]
    blocksA.append(sp.csc_matrix(-cols)); blocksb.append(svec((P0 + P0.T) / 2 * Dm))
    cones.append(clarabel.PSDTriangleConeT(nf))
    print("block %s: size %d" % (f, nf), flush=True)
Aall = sp.vstack(blocksA).tocsc(); ball = np.concatenate(blocksb)
P = sp.csc_matrix((NP, NP))
for sense in opts.get("obj", "min,max").split(","):
    q = np.zeros(NP); q[0] = 1.0 if sense == "min" else -1.0
    st = clarabel.DefaultSettings(); st.verbose = False; st.max_iter = int(opts.get("maxit", 200))
    solver = clarabel.DefaultSolver(P, q, Aall, ball, cones, st)
    sol = solver.solve()
    print("P %s: %s  P = %s  [%.0f s]" % (sense, sol.status, sol.x[0] * svar[0], time.time() - t0), flush=True)
