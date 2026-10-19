"""SCS (first-order) SDP for min / max P with the census LP and saved flag blocks (LAB 19/10/2026).  Floating point.
SCS form: min c^T y  s.t.  A y + s = b,  s in K;  K = nonneg (LP rows, y >= 0) x PSD blocks (svec: LOWER triangle,
column-major, off-diagonal scaled by sqrt 2).  y = x / scale.
usage: python flag_solve3.py <census json> <block files...> [--obj=min,max] [--eps=1e-6] [--maxit=N]"""
import sys, time
import numpy as np
import scipy.sparse as sp
import scs
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
Ablocks = [sp.csc_matrix(-A * svar), sp.csc_matrix(-np.eye(NP))]
bblocks = [b, np.zeros(NP)]
psd = []
def svec_low(M):
    n = M.shape[0]
    idx_i, idx_j = np.tril_indices(n)          # row-major lower triangle; reorder to column-major
    order = np.lexsort((idx_i, idx_j))
    ii, jj = idx_i[order], idx_j[order]
    v = M[ii, jj].copy()
    v[ii != jj] *= np.sqrt(2.0)
    return v
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
        cols[:, p - 1] = svec_low((Pp[i] + Pp[i].T) / 2 * Dm) * svar[p - 1]
    Ablocks.append(sp.csc_matrix(-cols)); bblocks.append(svec_low((P0 + P0.T) / 2 * Dm))
    psd.append(nf)
    print("block %s: size %d" % (f, nf), flush=True)
Aall = sp.vstack(Ablocks).tocsc(); ball = np.concatenate(bblocks)
cone = {"l": A.shape[0] + NP, "s": psd}
for sense in opts.get("obj", "min,max").split(","):
    c = np.zeros(NP); c[0] = 1.0 if sense == "min" else -1.0
    solver = scs.SCS({"A": Aall, "b": ball, "c": c}, cone, verbose=False, eps_abs=float(opts.get("eps", 1e-6)),
                     eps_rel=float(opts.get("eps", 1e-6)), max_iters=int(opts.get("maxit", 100000)))
    sol = solver.solve()
    info = sol["info"]
    print("P %s: %s  P = %.4f  iters %d  [%.0f s]" % (sense, info["status"], sol["x"][0] * svar[0], info["iter"], time.time() - t0), flush=True)
