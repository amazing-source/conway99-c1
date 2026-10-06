"""Schur complement of (rI - A) over the rigid block N[v]: T = M_LL - M_L,N[v] M_N[v]^{-1} M_N[v],L on the
non-neighbours of v.  Predicted: T^2 = (r - s) T  (so T/(r-s) is an orthogonal projection) and rank T = rank(rI-A) - |N[v]|.
Closed form for lambda=1, mu=2: T = rI - Gamma - K, K_ll' = alpha|l&l'| + beta m(l,l') + gamma with
alpha = (1/(2(r+1)) + 1/(2(r-1))), beta = (-1/(2(r+1)) + 1/(2(r-1))), gamma = -2/(k(r-1)) * ... (checked numerically)."""
import numpy as np
from fractions import Fraction
from graphs_test import bvls243
A = bvls243(); n, k, r, s = 243, 22, 4, -5
v = 0; Nv = list(np.nonzero(A[v])[0]); U = [v] + Nv; L = [w for w in range(n) if w not in U]
M = r * np.eye(n) - A
P = M[np.ix_(U, U)]; T = M[np.ix_(L, L)] - M[np.ix_(L, U)] @ np.linalg.solve(P, M[np.ix_(U, L)])
print("rank T =", np.linalg.matrix_rank(T), " predicted", np.linalg.matrix_rank(M) - len(U))
print("max |T^2 - (r-s)T| =", np.abs(T @ T - (r - s) * T).max())
# closed form check: mates in N(v)
mate = {}
for a in Nv:
    b = [c for c in Nv if A[a, c]][0]; mate[a] = b
lab = [tuple(sorted(c for c in Nv if A[w, c])) for w in L]
det = r * (r - 1) - k
alpha = Fraction(1, 2 * (r + 1)) + Fraction(1, 2 * (r - 1)); beta = -Fraction(1, 2 * (r + 1)) + Fraction(1, 2 * (r - 1))
gamma = -Fraction(1, k * (r - 1)) + Fraction(r, k * det)
Kc = np.zeros((len(L), len(L)))
for i, li in enumerate(lab):
    for j, lj in enumerate(lab):
        inter = len(set(li) & set(lj)); m = sum(1 for x in li for y in lj if mate[x] == y)
        Kc[i, j] = float(4 * gamma + alpha * inter + beta * m)
Tc = r * np.eye(len(L)) - A[np.ix_(L, L)] - Kc
print("max |T - (rI - Gamma - K)| =", np.abs(T - Tc).max(), " (alpha, beta, 4gamma) =", alpha, beta, 4 * gamma)
