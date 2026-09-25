# notes/110 sec. 5 (third derivation of L17 / notes/102 sec. 2).
# Verify: (1) M_x M^T = M^T(35I + 7P + 35J) given MH = -M - PM + 2J (only (MH)^T = H M^T is used);
# (2) det of the saturated row lattice of M (= det K_Z) = 2^21 3^8 5^6.
import itertools, sympy as sp
labels = [(c, s) for c in range(7) for s in range(2)]
li = {l: i for i, l in enumerate(labels)}
verts = [(a, b) for a, b in itertools.combinations(labels, 2) if a[0] != b[0]]
assert len(verts) == 84
M = sp.zeros(14, 84)
for j, (a, b) in enumerate(verts):
    M[li[a], j] = 1; M[li[b], j] = 1
P = sp.zeros(14, 14)
for (c, s) in labels:
    P[li[(c, s)], li[(c, 1 - s)]] = 1
J14 = sp.ones(14, 14); J84 = sp.ones(84, 84); J1484 = sp.ones(14, 84)
MH = -M - P * M + 2 * J1484          # the srg identity (block N(x) x Delta of A^2)
HMt = MH.T
lhs = HMt + 4 * M.T + 3 * M.T * M * M.T + M.T * P * M * M.T + 5 * J84 * M.T
rhs = M.T * (35 * sp.eye(14) + 7 * P + 35 * J14)
print('M_x M^T == M^T(35I+7P+35J):', lhs == rhs)
G = M * M.T
print('MM^T == 11I + J - P:', G == 11 * sp.eye(14) + J14 - P, ' det =', sp.factorint(G.det()))
# saturation of the row lattice: Hermite/Smith form of M (rows span R); elementary divisors of M
from sympy.matrices.normalforms import smith_normal_form
snf = smith_normal_form(M, domain=sp.ZZ)
d = [snf[i, i] for i in range(14)]
print('elementary divisors of M:', d)
