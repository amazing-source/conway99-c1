"""X14g -- exact reduction of the triangle-support Rayleigh condition to T <= Psi (12 x 12, universal).
S = 3I + (11/99)J - A_W >= 0 on W = R (x + 14 labels) + P (12 pairs).  A_R, A_RP universal; A_PP = T.
Schur: T <= Psi := 3I + (11/99)J_P - S_PR S_RR^+ S_RP  (S_RR is PSD; range condition checked).
Prints Psi's distinct entries by relation type of the two pairs and its spectrum (with multiplicities)."""
import itertools
from fractions import Fraction as Fr
import numpy as np

LAB = [(c, s) for c in range(7) for s in (0, 1)]
tri = (0, 1, 2)
pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
R = ['x'] + LAB
nR, nP = len(R), len(pairs)
A_R = np.zeros((nR, nR)); A_RP = np.zeros((nR, nP))
for i, l in enumerate(LAB):
    A_R[0, 1 + i] = A_R[1 + i, 0] = 1
    A_R[1 + i, 1 + LAB.index((l[0], 1 - l[1]))] = 1
for j, P in enumerate(pairs):
    for u in P:
        A_RP[1 + LAB.index(u), j] = 1
c = 11 / 99
S_RR = 3 * np.eye(nR) + c * np.ones((nR, nR)) - A_R
S_RP = c * np.ones((nR, nP)) - A_RP
ev = np.linalg.eigvalsh(S_RR)
print('S_RR eigenvalues min:', round(ev.min(), 6), '(PSD needed)')
Pinv = np.linalg.pinv(S_RR, rcond=1e-10)
K = S_RP.T @ Pinv @ S_RP
Psi = 3 * np.eye(nP) + c * np.ones((nP, nP)) - K
# range condition: S_RP columns in range(S_RR)
res = np.linalg.norm(S_RR @ Pinv @ S_RP - S_RP)
print('range condition residual:', f'{res:.2e}')
def rel(P, Q):
    if P == Q: return 'same'
    if P & Q: return 'share a label'
    mates = sum(1 for u in P for v in Q if u[0] == v[0])
    return f'disjoint, {mates} mate-relations'
vals = {}
for a, b in itertools.product(range(nP), repeat=2):
    vals.setdefault(rel(pairs[a], pairs[b]), set()).add(round(Psi[a, b], 6))
for k, v in vals.items():
    print(f'Psi entries, {k}: {sorted(v)}')
w = np.linalg.eigvalsh(Psi)
from collections import Counter
print('Psi spectrum:', sorted(Counter(np.round(w, 6)).items()))
np.save('data/psi_triangle.npy', Psi)
