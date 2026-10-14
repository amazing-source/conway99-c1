"""Why the srg(378,52,1,8) of the S3 hemisystem is rigid: the CONCENTRATION CRITERION (14/10/2026).

Lemma. Let A, A' be srg(v,k,lambda,mu) with eigenvalues r > s, equal on every pair meeting R = V - F. Let Y (resp. Y')
be the space of s-eigenvectors of A (resp. A') vanishing on R, and P, P' the orthogonal projections onto them. Then
  (1) A' - A = (r - s) (P - P')   [Delta = (r-s)(E_s - E'_s), and E_s, E'_s agree on span{E_s e_x : x in R}];
  (2) P and P' have the same diagonal (Delta has zero diagonal);
  (3) every changed pair {i,j} satisfies 1 <= |Delta_ij| <= 2 (r - s) sqrt(P_ii P_jj), i.e. P_ii P_jj >= 1/(2(r-s))^2;
  (4) the number of changes at a vertex i is at most 4 (r-s)^2 P_ii.
The same holds with the r-eigenspace. Here r - s = 15: a pair can change only if P_ii P_jj >= 1/900.
This script: for regions F (unions of X_m, random sets), computes w = dim Y and the largest P_ii P_jj (i != j), and
says whether the criterion alone proves rigidity. Then it looks for SHORT (-11)-eigenvectors (l1-minimal vectors with
a prescribed coordinate, linear programming), whose supports are the places where trades could live.
usage: python rigidity378.py <gq.json> <hemi.json> <edges>"""
import json
import random
import sys
import time

import numpy as np
from scipy.optimize import linprog

gqf, hf, ef = sys.argv[1], sys.argv[2], sys.argv[3]
G = json.load(open(gqf))
H = json.load(open(hf))
E = [tuple(map(int, l.split())) for l in open(ef) if l.strip()]
n = 1 + max(max(e) for e in E)
A = np.zeros((n, n))
for a, b in E:
    A[a, b] = A[b, a] = 1
w, V = np.linalg.eigh(A)
Q11 = V[:, np.abs(w + 11) < 1e-6]
Q4 = V[:, np.abs(w - 4) < 1e-6]
print("eigenspace dimensions: 4 -> %d, -11 -> %d" % (Q4.shape[1], Q11.shape[1]), flush=True)


def supported(Q, F):
    R = np.array([v for v in range(n) if v not in F])
    if len(R) == 0:
        return Q
    M = Q[R, :]
    u, sv, vt = np.linalg.svd(M, full_matrices=True)
    rank = int((sv > 1e-8).sum())
    N = vt[rank:].T
    return Q @ N


def report(label, F):
    Y = supported(Q11, F)
    d = (Y ** 2).sum(1) if Y.shape[1] else np.zeros(n)
    top = np.sort(d)[-2:]
    prod = float(top[0] * top[1]) if Y.shape[1] else 0.0
    Y4 = supported(Q4, F)
    d4 = (Y4 ** 2).sum(1) if Y4.shape[1] else np.zeros(n)
    top4 = np.sort(d4)[-2:]
    prod4 = float(top4[0] * top4[1]) if Y4.shape[1] else 0.0
    verdict = "RIGID by the criterion" if (prod < 1 / 900 - 1e-12 or prod4 < 1 / 900 - 1e-12) else "not excluded"
    print("%-38s |F| = %3d: dim Y(-11) = %3d, max P_ii = %.4f, best pair product %.5f (needs >= %.5f); "
          "dim Y(4) = %3d -> %s" % (label, len(F), Y.shape[1], float(d.max()) if Y.shape[1] else 0.0, prod, 1 / 900,
                                   Y4.shape[1], verdict), flush=True)
    return Y


lines = [set(l) for l in G["lines"]]
Hs = set(H)
nonH = [i for i in range(len(lines)) if i not in Hs]
X = {m: {kk for kk, h in enumerate(H) if lines[h] & lines[m]} for m in nonH}
rng = random.Random(7)
for j in (2, 3, 4, 5, 6):
    for c in range(2):
        ms = rng.sample(nonH, j)
        report("union of %d sets X_m" % j, set().union(*[X[m] for m in ms]))
for size in (250, 270, 280, 285, 290, 300, 310):
    report("random region", set(rng.sample(range(n), size)))

# short (-11)-eigenvectors: minimise ||x||_1 with x = Q11 c and x_i = 1
print("\nshort (-11)-eigenvectors (l1 minimisation, x_i = 1):", flush=True)
d = Q11.shape[1]
for i in rng.sample(range(n), 6):
    t0 = time.time()
    # variables: c (d, free), t (n, >= 0); minimise sum t; -t <= Qc <= t; (Qc)_i = 1
    cobj = np.concatenate([np.zeros(d), np.ones(n)])
    Aub = np.block([[Q11, -np.eye(n)], [-Q11, -np.eye(n)]])
    bub = np.zeros(2 * n)
    Aeq = np.concatenate([Q11[i], np.zeros(n)])[None, :]
    res = linprog(cobj, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=[1.0],
                  bounds=[(None, None)] * d + [(0, None)] * n, method="highs")
    x = Q11 @ res.x[:d]
    supp = np.abs(x) > 1e-7
    xs = x / np.abs(x[supp]).min()
    conc = float((x[i] ** 2) / (x @ x))
    vals = sorted(set(np.round(np.abs(xs[supp]), 3).tolist()))
    print("  vertex %3d: support %3d, |entries| (scaled) %s, concentration x_i^2/|x|^2 = %.4f (%.1f s)"
          % (i, int(supp.sum()), vals[:8], conc, time.time() - t0), flush=True)
