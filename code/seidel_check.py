"""notes/102 sec. 7: Seidel form.  When 2r + 1 = 0 mod p (99: r = 3, p = 7; Petersen: r = 1, p = 3), Q = A - rI + cJ is
proportional to the Seidel matrix S = J - I - 2A mod p.  Checks on Petersen: S^2 = p^2 (I + ...), rank_p S = alpha,
all nonzero principal alpha-minors of S have one Legendre symbol, Smith form over Z = 1^alpha p^(n-2alpha) (p^2)^alpha."""
import itertools
import numpy as np
import sympy
from sympy.matrices.normalforms import smith_normal_form
import eigenlattice_check as ec
from beta_form_check import rank_leg

A = np.array(ec.petersen(), dtype=np.int64); n = 10; p = 3
S = np.ones((n, n), dtype=np.int64) - np.eye(n, dtype=np.int64) - 2 * A
print('S^2 =', 'p^2 I' if (S @ S == 9 * np.eye(n, dtype=np.int64)).all() else (S @ S)[0][:4])
alpha = ec.rank_mod((A - np.eye(n, dtype=np.int64)).tolist(), p) - 1
rS, lS = rank_leg(S.tolist(), p)
legs = set()
for I in itertools.combinations(range(n), alpha):
    d = int(round(np.linalg.det(S[np.ix_(I, I)]))) % p
    if d:
        legs.add(1 if pow(d, (p - 1) // 2, p) == 1 else -1)
D = smith_normal_form(sympy.Matrix(S.tolist()), domain=sympy.ZZ)
sd = sorted(abs(int(D[i, i])) for i in range(n))
print(f'alpha={alpha}, rank_p S={rS}, Legendre(nondeg S)={lS}, Legendre of nonzero principal {alpha}-minors: {legs}, '
      f'Smith diag: {sd}')
