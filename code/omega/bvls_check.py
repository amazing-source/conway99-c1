"""BvLS srg(243,22,1,2), eigenvalue r=4 (multiplicity 132): star complement H of size 111 containing N[v].
Checks exactly: rI - A_H invertible, 1^T R 1 = -n/(k-r) = -27/2, B^T R 1 = -1, B^T R B = rI - A_X."""
import numpy as np, time
from fractions import Fraction
from graphs_test import bvls243, is_srg
from omega_small import inv_frac
A = bvls243(); n, k, r = 243, 22, 4
assert is_srg(A, 243, 22, 1, 2)
v = 0; U = [v] + list(np.nonzero(A[v])[0])
M = A - r * np.eye(n, dtype=int)
H = list(U); rk = np.linalg.matrix_rank(M[H, :].astype(float))
assert rk == len(H)
for w in range(n):
    if w in H: continue
    if np.linalg.matrix_rank(M[H + [w], :].astype(float)) > len(H):
        H.append(w)
    if len(H) == n - 132: break
print("|H| =", len(H))
X = [w for w in range(n) if w not in H]
AH = A[np.ix_(H, H)]; B = A[np.ix_(H, X)]; AX = A[np.ix_(X, X)]
t = time.time(); R = inv_frac(r * np.eye(len(H), dtype=int) - AH); print("exact inverse", round(time.time() - t, 1), "s")
assert R is not None
h = len(H)
one_R_one = sum(sum(row) for row in R)
print("1^T R 1 =", one_R_one, " expected", Fraction(-n, k - r))
R1 = [sum(row) for row in R]
ok1 = all(sum(R1[i] for i in range(h) if B[i, x]) == -1 for x in range(len(X)))
print("B^T R 1 = -1 for all columns:", ok1)
ok2 = True
cols = [[i for i in range(h) if B[i, x]] for x in range(len(X))]
for a in range(len(X)):
    for c in range(a, len(X)):
        val = sum(R[i][j] for i in cols[a] for j in cols[c])
        want = r if a == c else -AX[a, c]
        if val != want:
            ok2 = False; break
    if not ok2: break
print("B^T R B = rI - A_X exactly:", ok2)
