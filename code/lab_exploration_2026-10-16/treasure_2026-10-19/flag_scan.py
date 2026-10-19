"""Scan of flag blocks (LAB 19/10/2026): for every admissible sigma of order k and flags of order m, the smallest
eigenvalue of the (diagonally normalised, facially reduced) block M_sigma at the two LP extreme points (min P, max P)
of the census polytope.  A negative value means the block cuts that LP point off.  Floating point, exploration.
usage: python flag_scan.py <census json> <k> <m> <start> <count> [out.jsonl]"""
import json
import sys
import time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from flag_sdp import Census, build_matrix, flags_of  # noqa: E402
path, k, m, start, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
out = open(sys.argv[6], "a") if len(sys.argv) > 6 else None
t0 = time.time()
cen = Census(path)
NP = cen.NP
rows = []
for (n, key), f in cen.form.items():
    c0 = f.get(0, 0.0); coef = np.zeros(NP)
    for p, val in f.items():
        if p:
            coef[p - 1] = val
    sc = max(abs(c0), np.abs(coef).max(), 1.0)
    rows.append((coef / sc, c0 / sc))
A = np.array([r[0] for r in rows]); b = np.array([r[1] for r in rows])
pts = {}
for sense in ("min", "max"):
    r = linprog(np.eye(NP)[0] * (1 if sense == "min" else -1), A_ub=-A, b_ub=b, bounds=[(0, None)] * NP, method="highs")
    pts[sense] = r.x
d = json.load(open(path))
sig = [rws for key, rws, aut, form in d["types"][str(k)]]
cache = {}
for si in range(start, min(start + count, len(sig))):
    fl = flags_of(sig[si], k, m)
    mats = build_matrix(cen, fl, k, m, cache)
    nf = len(fl)
    M0 = mats.get(0, np.zeros((nf, nf)))
    res = {"sigma": si, "edges": sum(bin(r).count("1") for r in sig[si]) // 2, "flags": nf}
    for sense, x in pts.items():
        M = M0 + sum(x[p - 1] * Mp for p, Mp in mats.items() if p)
        dg = np.diag(M).copy()
        dsc = 1.0 / np.sqrt(np.where(dg > 1e-9, dg, 1.0))
        Mn = M * np.outer(dsc, dsc)
        ev = np.linalg.eigvalsh((Mn + Mn.T) / 2)
        res["mineig_" + sense] = float(ev[0])
    line = json.dumps(res)
    print(line, "[%.0f s]" % (time.time() - t0), flush=True)
    if out:
        out.write(line + "\n"); out.flush()
