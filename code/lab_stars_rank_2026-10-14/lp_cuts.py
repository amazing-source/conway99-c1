"""Continuous relaxation of the star PSD condition, by Kelley cutting planes (14/10/2026).

x in [0,1]^pairs with (C1) exact star counts and (C2) caps (linearised), T(x) = 3I - G(x) - K_S. The star vectors are
always in ker T(x) (the (C1) equalities suffice). Let lambda_perp(x) = smallest eigenvalue of T(x) on the orthogonal
complement of the star vectors. We bound  max_x lambda_perp(x)  from above by the LP
      max t   s.t.  c_k^T T(x) c_k >= t  for unit vectors c_k orthogonal to the stars (cuts accumulated),
adding at each step the eigenvector of lambda_perp at the LP solution. The LP value t* decreases to the SDP value.
If t* < 0, NO admissible structure (even fractional) has T_S >= 0: then no Conway graph exists with this local
structure... which would be an exclusion, to be certified exactly before any claim.
usage: python lp_cuts.py <stars> <iterations> <out prefix>
"""
import itertools
import json
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix, vstack, hstack

from stars_rank import LABELS, kval, count_needed


def main():
    stars = [int(t) for t in sys.argv[1].split(",")]
    iters, out = int(sys.argv[2]), sys.argv[3]
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
    # star vectors and the projector onto their orthogonal complement
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    eq_rows, eq_b = [], []
    E = lil_matrix((n * len(stars), nv))
    r = 0
    for i, l in enumerate(S):
        for y in stars:
            for t in range(n):
                if t != i and y in S[t]:
                    E[r, X(i, t)] = 1
            eq_b.append(count_needed(l, y))
            r += 1
    E = E.tocsr()
    U = lil_matrix((nv - 1 - nx + nx, nv))
    ub = []
    r = 0
    for p in pairs:                       # -p + x_it + x_jt <= 1
        i, j = p
        for k, t in enumerate(thirds[p]):
            U[r, poff[p] + k] = -1
            U[r, X(i, t)] = 1
            U[r, X(j, t)] = 1
            ub.append(1)
            r += 1
    for p in pairs:                       # sum_t p + x_ij <= 2 - shared
        i, j = p
        for k in range(len(thirds[p])):
            U[r, poff[p] + k] = 1
        U[r, X(i, j)] = 1
        ub.append(2 - len(S[i] & S[j]))
        r += 1
    U = U.tocsr()
    bounds = [(0, 1)] * (nv - 1) + [(None, None)]
    cvec = np.zeros(nv)
    cvec[tvar] = -1                       # maximise t
    cuts, cut_b = [], []
    t0 = time.time()
    hist = []
    for it in range(iters):
        if cuts:
            Acut = csr_matrix(np.array(cuts))
            A_ub = vstack([U, Acut]).tocsr()
            b_ub = np.concatenate([ub, cut_b])
        else:
            A_ub, b_ub = U, np.array(ub, float)
        bnds = list(bounds)
        if not cuts:
            bnds[tvar] = (None, 10)
        res = linprog(cvec, A_ub=A_ub, b_ub=b_ub, A_eq=E, b_eq=np.array(eq_b, float), bounds=bnds, method="highs")
        if res.status != 0:
            print("iteration %d: LP status %d %s" % (it, res.status, res.message), flush=True)
            return
        x = res.x[:nx]
        tstar = res.x[tvar]
        G = np.zeros((n, n))
        for (i, j), k in pid.items():
            G[i, j] = G[j, i] = x[k]
        T = 3 * np.eye(n) - G - Ks
        # eigen-decomposition on the complement of the stars
        Pp = np.eye(n) - Qz @ Qz.T
        M = Pp @ T @ Pp
        ev, V = np.linalg.eigh(M)
        # discard the star directions (eigenvalue 0 with eigenvector in span Z)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        evk = ev[keep]
        lam = evk.min()
        hist.append((it, tstar, lam))
        if it % 10 == 0 or it < 5:
            frac = float(np.mean((x > 1e-6) & (x < 1 - 1e-6)))
            print("iteration %d: LP bound t* = %.5f, lambda_perp(x*) = %.5f, fractional share %.2f, cuts %d (%.0f s)"
                  % (it, tstar, lam, frac, len(cuts), time.time() - t0), flush=True)
        if tstar < -1e-6:
            print("LP bound negative at iteration %d: t* = %.6f -> no fractional admissible x has T_S >= 0 on the"
                  " complement of the stars (to certify exactly)" % (it, tstar), flush=True)
            json.dump({"stars": stars, "iterations": it, "tstar": tstar, "cuts": len(cuts)}, open(out + "_neg.json", "w"))
            np.save(out + "_cuts.npy", np.array(cuts))
            return
        # add cuts for the 4 smallest eigenvalues on the complement
        order = np.argsort(evk)[:4]
        for o in order:
            c = V[:, keep[o]]
            row = np.zeros(nv)
            for (i, j), q in pid.items():
                row[q] = 2 * c[i] * c[j]
            row[tvar] = 1
            cuts.append(row)
            cut_b.append(3 * c @ c - c @ Ks @ c)
    print("end: t* = %.5f, lambda_perp = %.5f after %d iterations" % (hist[-1][1], hist[-1][2], iters), flush=True)
    json.dump({"stars": stars, "history": hist}, open(out + "_hist.json", "w"))


if __name__ == "__main__":
    main()
