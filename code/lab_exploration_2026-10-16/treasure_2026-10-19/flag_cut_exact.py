"""Robust cutting planes with INTEGER eigenvector cuts and warm-started HiGHS (LAB 19/10/2026).

Same problem as flag_cut_loop.py (max or min P over the census LP + E3 zeros + flag blocks PSD), but:
  * normalisation of a block by its diagonal uses a floor (1e-8 of the largest diagonal entry), so eigenvectors stay
    bounded (the AWS run showed normalised eigenvalues down to -1e23, i.e. near-zero diagonals);
  * every cut vector u is rescaled to max |u| = 1 and ROUNDED to integers u_int = round(2^20 u): the cut
    u_int^T M(x) u_int >= 0 is then exactly valid for every srg(99,14,1,2) and its type weights
    c_H = sum over block entries of u_i u_j (2 off the diagonal) mult are exact integers (int64);
  * the cut is added only if the ROUNDED cut is violated at the current point;
  * the LP is kept inside one Highs object and re-solved after adding rows (dual simplex warm start).
All cuts (block file, u_int) are saved (--save=file.npz) for an exact certificate later.
usage: python flag_cut_exact.py <forms npz> <T files or dirs...> [--obj=max|min] [--maxit=60] [--per=2]
       [--zero=file] [--save=cuts.npz] [--log=file]"""
import glob, os, sys, time
import numpy as np
import scipy.sparse as sp
import highspy

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
t0 = time.time()
z = np.load(args[0]); ntypes, NP = int(z["ntypes"]), int(z["NP"])
F = sp.csr_matrix((z["vals"], (z["rows"], z["cols"])), shape=(ntypes, NP + 1))
Fc = F[:, 0].toarray().ravel(); Fx = F[:, 1:].tocsr()
sc = np.maximum(np.maximum(np.abs(Fc), abs(Fx).max(axis=1).toarray().ravel()), 1.0)
files = []
for a in args[1:]:
    files += sorted(glob.glob(os.path.join(a, "T_*.npz"))) if os.path.isdir(a) else [a]
blocks = []
for f in files:
    b = np.load(f)
    blocks.append((os.path.basename(f), int(b["nf"]), b["pairs"], b["tids"], b["mult"].astype(np.int64)))
zero = [int(l) for l in open(opts["zero"])] if "zero" in opts else []
sense = opts.get("obj", "max"); maxit = int(opts.get("maxit", 60)); per = int(opts.get("per", 2))
log = open(opts["log"], "a") if "log" in opts else None

def say(s):
    print(s, flush=True)
    if log:
        log.write(s + "\n"); log.flush()

h = highspy.Highs()
h.setOptionValue("output_flag", False)
inf = highspy.kHighsInf
# variables x >= 0
h.addVars(NP, np.zeros(NP), np.full(NP, inf))
cost = np.zeros(NP); cost[0] = 1.0
h.changeColsCost(NP, np.arange(NP, dtype=np.int32), cost)
h.changeObjectiveSense(highspy.ObjSense.kMaximize if sense == "max" else highspy.ObjSense.kMinimize)
# rows: (Fc + Fx x) / sc >= 0  ->  Fx x / sc >= -Fc / sc ; E3 rows equal to zero
A = (sp.diags(1.0 / sc) @ Fx).tocsr()
lo = -Fc / sc; hi = np.full(ntypes, inf)
for t in zero:
    hi[t] = lo[t]
h.addRows(ntypes, lo, hi, A.nnz, A.indptr[:-1].astype(np.int32), A.indices.astype(np.int32), A.data)
saved_blocks, saved_u = [], []
for it in range(maxit):
    h.run()
    st = h.getModelStatus()
    if st != highspy.HighsModelStatus.kOptimal:
        say("iteration %d: LP status %s  [%.0f s]" % (it, h.modelStatusToString(st), time.time() - t0))
        break
    x = np.array(h.getSolution().col_value)
    xH = Fc + Fx @ x
    worst, added = 0.0, 0
    new_rows = []
    for bi, (name, nf, pairs, tids, mult) in enumerate(blocks):
        M = np.zeros(nf * nf); np.add.at(M, pairs, mult * xH[tids]); M = M.reshape(nf, nf)
        M = M + M.T - np.diag(np.diag(M))
        d = np.diag(M).copy()
        floor = max(d.max(), 1.0) * 1e-8
        dg = np.sqrt(np.maximum(d, floor))
        ev, V = np.linalg.eigh(M / np.outer(dg, dg))
        worst = min(worst, ev[0])
        ii, jj = pairs // nf, pairs % nf
        for q in range(min(per, nf)):
            if ev[q] >= -1e-9:
                break
            u = V[:, q] / dg
            u = u / np.abs(u).max()
            ui = np.rint(u * (1 << 20)).astype(np.int64)
            w = ui[ii] * ui[jj] * np.where(ii == jj, 1, 2) * mult          # exact int64
            cH = np.bincount(tids, weights=w.astype(np.float64), minlength=ntypes)  # float for the LP row
            row = Fx.T @ cH; cst = float(cH @ Fc)
            if cst + row @ x >= -1e-9 * max(np.abs(row).max(), abs(cst), 1.0):
                continue                                                    # rounded cut not violated
            s = max(np.abs(row).max(), abs(cst), 1e-300)
            new_rows.append((row / s, -cst / s))
            saved_blocks.append(bi); saved_u.append(ui)
            added += 1
    if new_rows:
        R = sp.csr_matrix(np.array([r for r, _ in new_rows]))
        h.addRows(len(new_rows), np.array([b for _, b in new_rows]), np.full(len(new_rows), inf), R.nnz,
                  R.indptr[:-1].astype(np.int32), R.indices.astype(np.int32), R.data)
    say("iteration %d: P = %.6f, worst normalised eigenvalue %.3e, cuts %d (+%d)  [%.0f s]" % (
        it, x[0], worst, len(saved_u), added, time.time() - t0))
    if added == 0:
        say("no violated block (rounded cuts): P %s = %.6f" % (sense, x[0]))
        break
if "save" in opts:
    np.savez_compressed(opts["save"], blocks=np.array([blocks[b][0] for b in saved_blocks]),
                        u=np.array(saved_u, dtype=object), allow_pickle=True)
