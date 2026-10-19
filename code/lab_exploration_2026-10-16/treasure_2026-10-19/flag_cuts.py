"""Cutting-plane outer approximation of  min / max P  subject to the census LP and saved flag blocks (LAB 19/10/2026).
Every iterate is an LP (HiGHS) over x_H >= 0, x >= 0 and the linear cuts u^T M(x) u >= 0 collected so far, so the
LP value is always a VALID outer bound for the SDP (max side: upper bound; min side: lower bound), up to floating LP
tolerance.  At the LP optimum x, every block M(x) is eigendecomposed and each eigenvector with eigenvalue < -tol gives
a cut.  Stops when no block is violated or after maxit iterations.
usage: python flag_cuts.py <census json> <block files...> [--obj=max|min] [--maxit=200] [--tol=1e-9] [--log=f]"""
import json, sys, time
import numpy as np
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
blocks = []
for f in args[1:]:
    z = np.load(f)
    P0, Pp, ps = z["P0"], z["Pp"], z["params"]
    if P0.shape[0]:
        blocks.append((f, (P0 + P0.T) / 2, [(int(p), (Pp[i] + Pp[i].T) / 2) for i, p in enumerate(ps)]))
sense = opts.get("obj", "max")
maxit, tol = int(opts.get("maxit", 200)), float(opts.get("tol", 1e-9))
cutsA, cutsb = [], []
c = np.zeros(NP); c[0] = -1.0 if sense == "max" else 1.0
log = open(opts["log"], "a") if "log" in opts else None
for it in range(maxit):
    AA = np.vstack([A] + ([np.array(cutsA)] if cutsA else []))
    bb = np.concatenate([b] + ([np.array(cutsb)] if cutsb else []))
    r = linprog(c, A_ub=-AA, b_ub=bb, bounds=[(0, None)] * NP, method="highs")
    if r.status != 0:
        print("iteration %d: LP status %d (%s)" % (it, r.status, r.message), flush=True)
        break
    x = r.x
    worst, added = 0.0, 0
    for f, M0, terms in blocks:
        M = M0 + sum(x[p - 1] * Mp for p, Mp in terms)
        dg = np.sqrt(np.maximum(np.abs(np.diag(M)), 1e-30))
        Mn = M / np.outer(dg, dg)
        ev, V = np.linalg.eigh(Mn)
        worst = min(worst, ev[0])
        for j in range(min(8, len(ev))):
            if ev[j] >= -tol:
                break
            u = V[:, j] / dg                     # cut on the unnormalised matrix: u^T M(x) u >= 0
            row = np.zeros(NP)
            for p, Mp in terms:
                row[p - 1] = u @ Mp @ u
            cst = u @ M0 @ u
            s = max(np.abs(row).max(), abs(cst), 1e-300)
            cutsA.append(row / s); cutsb.append(cst / s); added += 1
    line = "iteration %d: P = %.6f, worst normalised eigenvalue %.3e, cuts %d (+%d)  [%.0f s]" % (
        it, x[0], worst, len(cutsA), added, time.time() - t0)
    print(line, flush=True)
    if log:
        log.write(line + "\n"); log.flush()
    if added == 0:
        print("no violated block: SDP optimum reached (to tolerance): P %s = %.6f" % (sense, x[0]), flush=True)
        break
