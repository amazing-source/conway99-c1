# Real (not modular) version of the line Schur complement, checked on BvLS: for a triangle T with ball B = T u N1(T)
# and far set F:  Phi_F = (A_FF - r I) - A_FB (A_BB - r I)^{-1} A_BF  should have rank  mult... = n - m_r - rank(A_BB - rI)
# and inertia fixed by Haynsworth.  For 99 this predicts Phi_F <= 0 of rank 6; here r = 4 (BvLS eigenvalue).
import numpy as np
exec(open('code/x29_bvls_triangle.py').read().split('# a triangle through 0')[0])
v = 243; r = 4
x = 0; nb0 = np.nonzero(A[x])[0]; y = nb0[0]; z = [w for w in nb0 if A[y, w]][0]
T = [x, y, z]
N1 = sorted({w for t in T for w in np.nonzero(A[t])[0]} - set(T))
F = [w for w in range(v) if w not in T and w not in N1]
Bset = T + N1
Af = A.astype(float)
ABB = Af[np.ix_(Bset, Bset)] - r * np.eye(len(Bset))
print('ball size', len(Bset), ' far size', len(F), ' rank(A_BB - rI) =', np.linalg.matrix_rank(ABB))
Phi = Af[np.ix_(F, F)] - r * np.eye(len(F)) - Af[np.ix_(F, Bset)] @ np.linalg.pinv(ABB) @ Af[np.ix_(Bset, F)]
ev = np.linalg.eigvalsh(Phi)
print('rank Phi =', int(np.sum(np.abs(ev) > 1e-8)), ' positive', int(np.sum(ev > 1e-8)), ' negative', int(np.sum(ev < -1e-8)))
print('global: rank(A - rI) =', np.linalg.matrix_rank(Af - r * np.eye(v)))
# projection property: Phi_F = -(r - s) * Pi, Pi = orthogonal projection onto the s-eigenvectors supported on F
s = -5
print('|Phi^2 + (r-s) Phi|_max =', np.abs(Phi @ Phi + (r - s) * Phi).max())
w, U = np.linalg.eigh(Af)
Us = U[:, np.abs(w - s) < 1e-6]                    # s-eigenspace
# s-eigenvectors vanishing on the ball: null space of Us restricted to ball rows
Ball = Us[Bset, :]
_, sv, Vt = np.linalg.svd(Ball)
null = Vt[np.sum(sv > 1e-8):].T
K = (Us @ null)[F, :]                              # restricted to F (they vanish on the ball)
Pi = K @ np.linalg.pinv(K)
print('dim of s-eigenvectors supported on F =', K.shape[1], ' |Phi + (r-s) Pi|_max =', np.abs(Phi + (r - s) * Pi).max())
