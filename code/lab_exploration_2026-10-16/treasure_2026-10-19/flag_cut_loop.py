"""Cutting-plane outer approximation (LAB 19/10/2026): min / max P subject to the exact census LP (x_H >= 0 for every
census type, x >= 0) and the flag blocks M_sigma(x) PSD given as sparse amalgam incidences (flag_engine.py).

Every LP iterate is an OUTER bound (max side: upper bound on P; min side: lower bound), up to floating LP tolerance.
At the LP optimum x: xH = F (1, x) (embedding counts of every census type), each block M(x) is assembled, scaled by its
diagonal, eigendecomposed; each eigenvector u with eigenvalue < -tol (up to `per` per block) gives the linear cut
u^T M(x) u >= 0, i.e. sum_H c_H xH(x) >= 0 with c_H = sum over block entries (i, j, H, mult) of u_i u_j mult (doubled
off the diagonal).  Optionally a list of census type ids forced to 0 (--zero=file, one id per line).
usage: python flag_cut_loop.py <forms npz> <T files or directories...> [--obj=max|min] [--maxit=300] [--tol=1e-9]
       [--per=6] [--log=file] [--zero=file]"""
import glob
import json
import os
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
t0 = time.time()
z = np.load(args[0])
ntypes, NP = int(z["ntypes"]), int(z["NP"])
F = sp.csr_matrix((z["vals"], (z["rows"], z["cols"])), shape=(ntypes, NP + 1))
Fc = F[:, 0].toarray().ravel()
Fx = F[:, 1:].tocsr()
sc = np.maximum(np.maximum(np.abs(Fc), abs(Fx).max(axis=1).toarray().ravel()), 1.0)
A_lp = sp.diags(1.0 / sc) @ Fx
b_lp = Fc / sc
eqA, eqb = None, None
if "zero" in opts:
    ids = [int(l) for l in open(opts["zero"]) if l.strip()]
    eqA = sp.diags(1.0 / sc[ids]) @ Fx[ids]
    eqb = -(Fc[ids] / sc[ids])
files = []
for a in args[1:]:
    files += sorted(glob.glob(os.path.join(a, "T_*.npz"))) if os.path.isdir(a) else [a]
blocks = []
for f in files:
    b = np.load(f)
    blocks.append((os.path.basename(f), int(b["nf"]), b["pairs"], b["tids"], b["mult"].astype(float)))
print("LP rows %d, parameters %d, blocks %d (sizes %s)  [%.0f s]" % (ntypes, NP, len(blocks),
      sorted({bl[1] for bl in blocks})[-5:], time.time() - t0), flush=True)
sense = opts.get("obj", "max")
maxit, tol, per = int(opts.get("maxit", 300)), float(opts.get("tol", 1e-9)), int(opts.get("per", 6))
c = np.zeros(NP); c[0] = -1.0 if sense == "max" else 1.0
objname = "P"
if "objtype" in opts:                      # optimise the embedding count x_H of a census type id instead of P
    t_obj = int(opts["objtype"])
    row = Fx[t_obj].toarray().ravel()
    c = -row if sense == "max" else row
    objname = "x_type%d" % t_obj
obj_const = float(Fc[int(opts["objtype"])]) if "objtype" in opts else 0.0
cut_rows, cut_b = [], []
cut_src = []                                   # (block index, u) for an exact re-check
log = open(opts["log"], "a") if "log" in opts else None
hist = []
for it in range(maxit):
    AA = sp.vstack([A_lp] + ([sp.csr_matrix(np.array(cut_rows))] if cut_rows else [])).tocsr()
    bb = np.concatenate([b_lp] + ([np.array(cut_b)] if cut_b else []))
    r = linprog(c, A_ub=-AA, b_ub=bb, A_eq=eqA, b_eq=eqb, bounds=[(0, None)] * NP, method="highs")
    if r.status != 0:
        msg = "iteration %d: LP status %d (%s)  [%.0f s]" % (it, r.status, r.message, time.time() - t0)
        print(msg, flush=True)
        if log:
            log.write(msg + "\n")
        break
    x = r.x
    xH = Fc + Fx @ x
    worst, added = 0.0, 0
    for bidx, (name, nf, pairs, tids, mult) in enumerate(blocks):
        vals = mult * xH[tids]
        M = np.zeros(nf * nf)
        np.add.at(M, pairs, vals)
        M = M.reshape(nf, nf)
        M = M + M.T - np.diag(np.diag(M))
        dg = np.sqrt(np.maximum(np.abs(np.diag(M)), 1e-30))
        Mn = M / np.outer(dg, dg)
        ev, V = np.linalg.eigh(Mn)
        worst = min(worst, ev[0])
        ii, jj = pairs // nf, pairs % nf
        for q in range(min(per, nf)):
            if ev[q] >= -tol:
                break
            u = V[:, q] / dg
            w = u[ii] * u[jj] * np.where(ii == jj, 1.0, 2.0) * mult
            cH = np.bincount(tids, weights=w, minlength=ntypes)
            row = Fx.T @ cH
            cst = float(cH @ Fc)
            s = max(np.abs(row).max(), abs(cst), 1e-300)
            cut_rows.append(row / s); cut_b.append(cst / s); added += 1
            cut_src.append((bidx, u.copy()))
    objv = float(x[0]) if objname == "P" else float(obj_const + (Fx[int(opts["objtype"])] @ x).item())
    line = "iteration %d: %s = %.6f (P = %.4f), worst normalised eigenvalue %.3e, cuts %d (+%d)  [%.0f s]" % (
        it, objname, objv, x[0], worst, len(cut_rows), added, time.time() - t0)
    print(line, flush=True)
    hist.append((it, float(x[0]), float(worst)))
    if log:
        log.write(line + "\n"); log.flush()
    if added == 0:
        msg = "no violated block: SDP optimum reached to tolerance: P %s = %.6f" % (sense, x[0])
        print(msg, flush=True)
        if log:
            log.write(msg + "\n")
        break
if "savecuts" in opts:
    np.savez_compressed(opts["savecuts"], names=np.array([blocks[b][0] for b, _ in cut_src]),
                        u=np.array([u for _, u in cut_src], dtype=object), x=x, allow_pickle=True)
if "out" in opts:
    json.dump({"sense": sense, "history": hist, "final_P": hist[-1][1] if hist else None,
               "blocks": [b[0] for b in blocks]}, open(opts["out"], "w"))
