"""Triangle frame theorem, checked on BvLS srg(243,22,1,2) (eigenvalues r=4 mult 132, s=-5 mult 110).
Triangle {v,a,a'}; ball = N[v] u N[a] u N[a'] (3 + 3*(k-2) vertices); C = ball minus the triangle; far = the rest.
Claims: F_s = {f in E_s : f|ball = 0}, F_r likewise, both restricted to far, lie in Z = ker(B_C^T);
dim F_s = mult(s) - rank(E_s on ball), dim F_r = mult(r) - rank(E_r on ball); Z = F_s + F_r when ranks are generic;
A_far f = s f on F_s, A_far g = r g on F_r."""
import numpy as np
from graphs_test import bvls243
A = bvls243(); n, k, r, s = 243, 22, 4, -5
w, V = np.linalg.eigh(A.astype(float))
Es = V[:, np.abs(w - s) < 1e-6]; Er = V[:, np.abs(w - r) < 1e-6]
v = 0; a = int(np.nonzero(A[v])[0][0]); ap = [c for c in np.nonzero(A[v])[0] if A[a, c]][0]
ball = sorted(set([v, a, ap]) | set(np.nonzero(A[v])[0]) | set(np.nonzero(A[a])[0]) | set(np.nonzero(A[ap])[0]))
tri = [v, a, ap]; C = [u for u in ball if u not in tri]; far = [u for u in range(n) if u not in ball]
print("|ball| =", len(ball), "|C| =", len(C), "|far| =", len(far))
def dim_vanishing(E, S):
    # dimension of {f in span(E) : f|S = 0}
    return E.shape[1] - np.linalg.matrix_rank(E[S, :], tol=1e-8)
ds, dr = dim_vanishing(Es, ball), dim_vanishing(Er, ball)
BC = A[np.ix_(C, far)]
rkB = np.linalg.matrix_rank(BC.astype(float)); dimZ = len(far) - rkB
print("dim F_s =", ds, " dim F_r =", dr, " rank B_C =", rkB, " dim Z =", dimZ, " (F_s + F_r =", ds + dr, ")")
# bases of F_s, F_r restricted to far
def basis_vanishing(E, S):
    U, sv, Vt = np.linalg.svd(E[S, :]); nul = Vt[np.sum(sv > 1e-8):].T
    return E @ nul
Fs = basis_vanishing(Es, ball)[far]; Fr = basis_vanishing(Er, ball)[far]
print("max |B_C^T-image| of F_s, F_r :", np.abs(BC @ Fs).max(), np.abs(BC @ Fr).max())
Af = A[np.ix_(far, far)].astype(float)
print("max |A_far f - s f| on F_s:", np.abs(Af @ Fs - s * Fs).max(), "  on F_r:", np.abs(Af @ Fr - r * Fr).max())
print("rank [F_s F_r] =", np.linalg.matrix_rank(np.hstack([Fs, Fr]), tol=1e-8), " vs dim Z", dimZ)
