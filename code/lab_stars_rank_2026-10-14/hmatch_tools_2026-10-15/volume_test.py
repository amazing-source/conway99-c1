"""Codex's nullity-volume filter (message of ~10:40 UTC 15/10, codex_h_nullity_volume.py), re-implemented in floats
(LAB 15/10/2026, task T3).  For a structure Gamma with average Gamma_0: T_0 = diag(A, C), U_0 = diag(A', C') on
E_+ / E_-; S = A' shorted to range A, Q = C' shorted to range C; alpha_j = increasing generalised eigenvalues of
(A, S) on range A, beta_j those of (C, Q) on range C.  If T, U >= 0 for some orientation with nullity T >= nullity T_0
+ p, then prod_{j<=p} alpha_j beta_j <= 1.  Prints nullity T_0 and the products for p = 1, 2, 3.
usage: python volume_test.py <json> [...]"""
import json, random, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS
S_, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S_)
Kf = np.array([[kval(a, b) for b in S_] for a in S_])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
P7 = 7 * Pi[np.ix_([pos[l] for l in S_], [pos[l] for l in S_])]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S_]
H = np.zeros((n, n))
for i in range(n):
    H[hp[i], i] = 1
Qp = np.linalg.svd((np.eye(n) + H) / 2)[0][:, :22]
Qm = np.linalg.svd((np.eye(n) - H) / 2)[0][:, :22]
TOL = 1e-8


def short_gen(Xt, Xu):
    """range W0 of Xt, U-block shorted to W0; if the shorted block has a kernel Z (B must vanish on it for U >= 0),
    saturations of T live in the Xt-orthogonal complement of Z inside W0: restrict there.  Returns the increasing
    generalised eigenvalues of (Xt, short) on that support, nullity of Xt, dim Z, min eig of the short on W0."""
    w, V = np.linalg.eigh(Xt)
    R, Nk = V[:, w > TOL], V[:, w <= TOL]
    At = R.T @ Xt @ R
    Su = R.T @ Xu @ R - R.T @ Xu @ Nk @ np.linalg.pinv(Nk.T @ Xu @ Nk, rcond=1e-10) @ Nk.T @ Xu @ R
    ws, Vs = np.linalg.eigh((Su + Su.T) / 2)
    if ws[0] < -1e-7:
        return None, int(np.sum(w <= TOL)), 0, float(ws[0])
    Zb = Vs[:, ws <= 1e-7]                          # ker of the short inside W0 (coordinates of R)
    if Zb.shape[1]:
        # At-orthogonal complement of Zb in W0
        M = Zb.T @ At                               # rows: functionals x -> z^T At x
        u, sv, vt = np.linalg.svd(M)
        Wb = vt[np.sum(sv > 1e-9):].T                # basis of {x : z^T At x = 0 for z in Zb}
        At2, Su2 = Wb.T @ At @ Wb, Wb.T @ Su @ Wb
    else:
        At2, Su2 = At, Su
    L = np.linalg.cholesky((Su2 + Su2.T) / 2)
    Li = np.linalg.inv(L)
    g = np.sort(np.linalg.eigvalsh(Li @ At2 @ Li.T))
    return g, int(np.sum(w <= TOL)), int(Zb.shape[1]), float(ws[0])


for f in sys.argv[1:]:
    d = json.load(open(f))
    G = np.zeros((n, n))
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    G0 = (G + G[np.ix_(hp, hp)]) / 2
    T0 = 3 * np.eye(n) - G0 - Kf
    U0 = P7 - T0
    A, C = Qp.T @ T0 @ Qp, Qm.T @ T0 @ Qm
    A2, C2 = Qp.T @ U0 @ Qp, Qm.T @ U0 @ Qm
    T = 3 * np.eye(n) - G - Kf
    nulT = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < TOL))
    al, nA, zA, sA = short_gen(A, A2)
    be, nC, zC, sC = short_gen(C, C2)
    if al is None or be is None:
        print("%s: the shorted U block is NOT PSD (min eig %.3f / %.3f): no orientation of this average has U >= 0" % (f, sA, sC))
        continue
    prods = [float(np.prod(al[:p]) * np.prod(be[:p])) for p in (1, 2, 3)]
    print("%s: nullity T %d, nullity T_0 = %d + %d = %d; ker of the shorts: %d / %d; alpha_1..3 = %s, beta_1..3 = %s; "
          "products p=1,2,3: %s" % (f, nulT, nA, nC, nA + nC, zA, zC, np.round(al[:3], 4).tolist(), np.round(be[:3], 4).tolist(),
                                     np.round(prods, 4).tolist()))
