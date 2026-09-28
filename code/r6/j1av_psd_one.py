# CHECK (single explicit configuration, exact rational arithmetic; not a search):
# J1a type (v), case (I) B+={p,q,r}, each G_k = two internal Q-edges. Odd test M = 12I + 4G - RR^T (PSD needed),
# even test M' = 6I - 2G - |R||R|^T + J (PSD needed; D_UU = 0 in J1a).
import sympy as sp
blocks = ['c', 'p', 'q', 'r', 's', 't', 'u']; bi = {b: i for i, b in enumerate(blocks)}
a = {'p': 1, 'q': 1, 'r': 1, 's': -1, 't': -1, 'u': -1}
labels = [(b, t) for b in 'pqrstu' for t in (1, -1)] + ['V1', 'V2', 'V3']
idx = {L: i for i, L in enumerate(labels)}
def rvec(L):
    v = [0] * 7
    if L == 'V1': v[bi['p']] = 1; v[bi['q']] = -1
    elif L == 'V2': v[bi['q']] = 1; v[bi['r']] = -1
    elif L == 'V3': v[bi['r']] = 1; v[bi['p']] = -1
    else:
        b, t = L; v[0] = a[b]; v[bi[b]] = t
    return v
def cfg(Q, P, groups):
    n = len(labels); G = sp.zeros(n, n)
    for (x, y) in Q + P:
        G[idx[x], idx[y]] = 1; G[idx[y], idx[x]] = 1
    for k, Gk in enumerate(groups):
        for L in Gk:
            G[idx[L], idx['V%d' % (k + 1)]] = 1; G[idx['V%d' % (k + 1)], idx[L]] = 1
    for x, y in [('V1', 'V2'), ('V2', 'V3'), ('V1', 'V3')]:
        G[idx[x], idx[y]] = 1; G[idx[y], idx[x]] = 1
    R = sp.Matrix([rvec(L) for L in labels]); Ra = R.applyfunc(abs)
    avec = sp.Matrix([1] * 12 + [2] * 3)
    assert G * avec == 4 * avec, 'Perron check failed'
    assert R.T * avec == sp.zeros(7, 1)
    Modd = 12 * sp.eye(n) + 4 * G - R * R.T
    Mev = 6 * sp.eye(n) - 2 * G - Ra * Ra.T + sp.ones(n, n)
    eo = sorted(float(x) for x in Modd.eigenvals(multiple=True))
    ee = sorted(float(x) for x in Mev.eigenvals(multiple=True))
    return eo, ee
P1, M1, P2, M2 = ('p', 1), ('p', -1), ('q', 1), ('q', -1)
Q = [(('p', 1), ('s', 1)), (('q', -1), ('t', 1)), (('p', -1), ('s', -1)), (('r', -1), ('u', 1)), (('q', 1), ('t', -1)), (('r', 1), ('u', -1))]
P = [(('p', 1), ('r', -1)), (('p', -1), ('q', 1)), (('q', -1), ('r', 1)), (('s', 1), ('u', -1)), (('s', -1), ('t', 1)), (('t', -1), ('u', 1))]
groups = [[('p', 1), ('q', -1), ('s', 1), ('t', 1)], [('p', -1), ('r', -1), ('s', -1), ('u', 1)], [('q', 1), ('r', 1), ('t', -1), ('u', -1)]]
eo, ee = cfg(Q, P, groups)
print('odd  eigenvalues:', [round(x, 3) for x in eo])
print('even eigenvalues:', [round(x, 3) for x in ee])

import numpy as np
def mats(Q, P, groups):
    n = len(labels); G = np.zeros((n, n))
    for (x, y) in Q + P:
        G[idx[x], idx[y]] = G[idx[y], idx[x]] = 1
    for k, Gk in enumerate(groups):
        for L in Gk:
            G[idx[L], idx['V%d' % (k + 1)]] = G[idx['V%d' % (k + 1)], idx[L]] = 1
    for x, y in [('V1', 'V2'), ('V2', 'V3'), ('V1', 'V3')]:
        G[idx[x], idx[y]] = G[idx[y], idx[x]] = 1
    R = np.array([rvec(L) for L in labels], dtype=float)
    return G, R
G, R = mats(Q, P, groups)
M = 12 * np.eye(15) + 4 * G - R @ R.T
w, V = np.linalg.eigh(M)
z = V[:, 0]; z = z / np.max(np.abs(z))
print('min eig', w[0])
for L, zz in zip(labels, z):
    print('  ', L, round(zz, 3))
print('z^T G z / |z|^2 =', z @ G @ z / (z @ z), '  |R^T z|^2/|z|^2 =', np.sum((R.T @ z) ** 2) / (z @ z))
print('R^T z =', np.round(R.T @ z, 3))
