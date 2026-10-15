"""Which eigen-directions of the average does the twist couple?  (LAB 15/10/2026, mechanism A, question (i))
T = T_0 - Delta/2, U = U_0 + Delta/2 with T_0, U_0 h-invariant (functions of Gamma_0) and Delta = Gamma - h Gamma h
(odd <-> even).  In the h-even / h-odd splitting T_0 = A (+) C and U_0 = A' (+) C', B = -(Delta/2)_{+-}.
For a structure: spectra of A, C (on the complement of the star vectors), the coupling Delta/2 written in the
eigenbases of T_0 (even eigenvalue a, odd eigenvalue c), the largest entries, and the generalised couplings
|<x+, Delta/2 x->| / sqrt(a c)  (T-side, must be <= 1 on the support)  and  / sqrt((7-a)(7-c))  (U-side).
usage: python coupling_spectrum.py <json>"""
import json, sys
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, '..')
from stars_rank import kval, LABELS
hm = {0: 1, 1: 0, 2: 3, 3: 2}
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
G = np.zeros((n, n))
for a, b in d["edges"]:
    G[a, b] = G[b, a] = 1
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
Ph = np.zeros((n, n))
for i in range(n):
    Ph[hp[i], i] = 1
K = np.array([[kval(a, b) for b in S] for a in S])
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
T = 3 * np.eye(n) - G - K
T0 = (T + Ph @ T @ Ph) / 2
Dl = G - Ph @ G @ Ph
U0 = 7 * PiS - T0
Z = np.array([[1.0 if y in s else 0.0 for s in S] for y in (0, 1, 2, 3)]).T
# even / odd projectors, minus the star vectors
Pe = (np.eye(n) + Ph) / 2; Po = (np.eye(n) - Ph) / 2
Zq, _ = np.linalg.qr(Z)
Pz = np.eye(n) - Zq @ Zq.T
def basis(P):
    w, V = np.linalg.eigh(P)
    return V[:, w > 0.5]
Be = basis(Pe @ Pz @ Pe) if False else None
# star vectors: 1_L0 + 1_L1, 1_L2 + 1_L3 are even, the differences odd: remove them inside each parity
def parity_basis(Pp):
    M = Pp @ Pz @ Pp
    w, V = np.linalg.eigh((M + M.T) / 2)
    return V[:, w > 0.5]
Be, Bo = parity_basis(Pe), parity_basis(Po)
# Pi restricted (needed for U on even vectors; on odd vectors Pi = identity on V0-)
def gen_eig(M, Bs, Pm):
    # eigen-decomposition of Bs^T M Bs relative to Bs^T Pm Bs (Pm = Pi_S, positive definite on the complement)
    Mb = Bs.T @ M @ Bs; Nb = Bs.T @ Pm @ Bs
    L = np.linalg.cholesky((Nb + Nb.T) / 2)
    Li = np.linalg.inv(L)
    w, V = np.linalg.eigh(Li @ Mb @ Li.T)
    X = Bs @ Li.T @ V          # columns: Pi-orthonormal eigenvectors
    return w, X
a, Xe = gen_eig(T0, Be, PiS)
c, Xo = gen_eig(T0, Bo, PiS)
print("even spectrum of T_0 (Pi-normalised, 7 = top):", np.round(a, 3))
print("odd  spectrum of T_0 (Pi-normalised):        ", np.round(c, 3))
Cp = Xe.T @ (Dl / 2) @ Xo
print("|coupling| Frobenius^2 = %.4f" % (Cp ** 2).sum())
# T-side and U-side normalised couplings
ta = np.where(a > 1e-9, a, np.nan); tc = np.where(c > 1e-9, c, np.nan)
Tn = Cp / np.sqrt(np.outer(ta, tc)); Un = Cp / np.sqrt(np.outer(np.clip(7 - a, 1e-12, None), np.clip(7 - c, 1e-12, None)))
print("T-side normalised coupling: operator norm %.4f (must be <= 1)" % np.linalg.norm(np.nan_to_num(Tn), 2))
print("U-side normalised coupling: operator norm %.4f (must be <= 1)" % np.linalg.norm(Un, 2))
# which pairs carry the U excess
uu, ss, vv = np.linalg.svd(Un)
print("top U-side singular values:", np.round(ss[:6], 4))
for k in range(2):
    ie = np.argsort(-np.abs(uu[:, k]))[:4]; io = np.argsort(-np.abs(vv[k]))[:4]
    print("  singular pair %d: even eigen-directions (a, weight) %s ; odd (c, weight) %s" % (
        k, [(round(a[i], 3), round(uu[i, k] ** 2, 3)) for i in ie], [(round(c[i], 3), round(vv[k, i] ** 2, 3)) for i in io]))
