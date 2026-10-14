"""Integral search for an admissible star structure with T_S >= 0 (14/10/2026).

Branch-and-cut on  max t  s.t.  c_k^T T(x) c_k >= t  (unit c_k orthogonal to the star vectors), x binary admissible
((C1) exact star counts, (C2) caps linearised). Each round: solve the MILP (time limit), read the integral x*, compute
lambda_perp(x*) (smallest eigenvalue of T(x*) off the star directions); if >= 0, a PSD structure is found and saved;
otherwise add the cuts of the 4 smallest eigenvectors and repeat. When a MILP is solved to optimality its value t* is an
upper bound on max lambda_perp over all integral admissible structures (the LP relaxation alone is useless here:
fractional structures with T_S > 0 exist, lp_cuts.py).
usage: python psd_maxmin.py <stars> <rounds> <seconds per MILP> <out prefix>
"""
import itertools
import json
import sys
import time

import numpy as np
from scipy.optimize import LinearConstraint, Bounds, milp
from scipy.sparse import lil_matrix, csr_matrix, vstack

from stars_rank import LABELS, kval, count_needed


def main():
    stars = [int(t) for t in sys.argv[1].split(",")]
    rounds, secs, out = int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    S = [l for l in LABELS if any(y in l for y in stars)]
    n = len(S)
    pairs = list(itertools.combinations(range(n), 2))
    pid = {p: k for k, p in enumerate(pairs)}
    X = lambda i, j: pid[(i, j) if i < j else (j, i)]
    nx = len(pairs)
    thirds = {p: [t for t in range(n) if t not in p] for p in pairs}
    poff, nv = {}, nx
    for p in pairs:
        poff[p] = nv
        nv += len(thirds[p])
    tvar = nv
    nv += 1
    Ks = np.array([[kval(a, b) for b in S] for a in S])
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    blocks, lo, hi = [], [], []
    E = lil_matrix((n * len(stars), nv))
    r = 0
    for i, l in enumerate(S):
        for y in stars:
            for t in range(n):
                if t != i and y in S[t]:
                    E[r, X(i, t)] = 1
            lo.append(count_needed(l, y)); hi.append(count_needed(l, y)); r += 1
    blocks.append(E.tocsr())
    U = lil_matrix((nv - 1, nv))
    r = 0
    for p in pairs:
        i, j = p
        for k, t in enumerate(thirds[p]):
            U[r, poff[p] + k] = 1; U[r, X(i, t)] = -1; U[r, X(j, t)] = -1
            lo.append(-1); hi.append(np.inf); r += 1
    for p in pairs:
        i, j = p
        for k in range(len(thirds[p])):
            U[r, poff[p] + k] = 1
        U[r, X(i, j)] = 1
        lo.append(-np.inf); hi.append(2 - len(S[i] & S[j])); r += 1
    blocks.append(U.tocsr())
    base = vstack(blocks).tocsr()
    lo, hi = np.array(lo, float), np.array(hi, float)
    integrality = np.concatenate([np.ones(nx), np.zeros(nv - nx)])
    lb = np.zeros(nv); ub = np.ones(nv); lb[tvar] = -10; ub[tvar] = 10
    cobj = np.zeros(nv); cobj[tvar] = -1
    cuts, cut_hi = [], []
    best = -np.inf
    t0 = time.time()
    for rd in range(rounds):
        cons = [LinearConstraint(base, lo, hi)]
        if cuts:
            cons.append(LinearConstraint(csr_matrix(np.array(cuts)), -np.inf, np.array(cut_hi)))
        res = milp(cobj, constraints=cons, integrality=integrality, bounds=Bounds(lb, ub),
                   options={"time_limit": secs, "disp": False, "mip_rel_gap": 1e-4})
        if res.x is None:
            print("round %d: MILP %s (status %d)" % (rd, res.message, res.status), flush=True)
            return
        x = np.round(res.x[:nx]).astype(int)
        tstar = res.x[tvar]
        bound = getattr(res, "mip_dual_bound", None)
        G = np.zeros((n, n))
        for (i, j), k in pid.items():
            G[i, j] = G[j, i] = x[k]
        T = 3 * np.eye(n) - G - Ks
        ev, V = np.linalg.eigh(Pp @ T @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        evk = ev[keep]
        lam = evk.min()
        if lam > best:
            best = lam
            json.dump({"stars": stars, "labels": [sorted(l) for l in S],
                       "gamma": G.astype(int).tolist(), "lambda_perp": float(lam)}, open(out + "_best.json", "w"))
        print("round %d: t* = %.4f (status %d, dual bound %s), lambda_perp(x*) = %.5f, best %.5f, cuts %d (%.0f s)"
              % (rd, tstar, res.status, "%.4f" % -bound if bound is not None else "?", lam, best, len(cuts),
                 time.time() - t0), flush=True)
        if lam >= -1e-9:
            print("PSD admissible structure found (saved in %s_best.json)" % out, flush=True)
            return
        if res.status == 0 and tstar < -1e-6:
            print("MILP optimal with t* < 0: no integral admissible structure has T_S >= 0 (to certify)", flush=True)
            return
        for o in np.argsort(evk)[:4]:
            c = V[:, keep[o]]
            row = np.zeros(nv)
            for (i, j), q in pid.items():
                row[q] = 2 * c[i] * c[j]
            row[tvar] = 1
            cuts.append(row)
            cut_hi.append(3 * c @ c - c @ Ks @ c)
    print("no decision after %d rounds; best lambda_perp %.5f" % (rounds, best), flush=True)


if __name__ == "__main__":
    main()
