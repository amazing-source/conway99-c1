"""Check (C1, 28/09): in BvLS = srg(243,22,1,2) with sigma = -1, dimension of the space of sigma-odd eigenvectors for the
smallest eigenvalue -5 that vanish outside T = labels meeting exactly one of blocks {1,2} (the m = 11 analogue of the
n = 5 dual witness), and whether it contains a +-1 vector on T. Pure linear algebra on a known graph."""
import sys, itertools
import numpy as np
sys.path.insert(0, 'C:/home/researcher/Desktop/conway99-involution/code/z2')
from control_bvls import bvls
A, V, ix, cols, neg = bvls()
n, m = 243, 11
x0 = ix[(0,) * 5]; inner = {}
for i, c in enumerate(cols): inner[ix[c]] = (i + 1, 0); inner[ix[neg(c)]] = (i + 1, 1)
lab = {}
for v in range(n):
    if v == x0 or v in inner: continue
    nb = sorted(inner[w] for w in np.flatnonzero(A[v]) if w in inner); lab[v] = nb
S = {1, 2}
T = [v for v in lab if len({b for b, _ in lab[v]} & S) == 1]
print('|T| =', len(T))
ev, U = np.linalg.eigh(A.astype(float))
E = U[:, np.abs(ev + 5) < 1e-6]; print('mult(-5) =', E.shape[1])
P = np.zeros((n, n))
for v in range(n): P[v, ix[neg(V[v])]] = 1
Eodd = E @ np.linalg.svd(E.T @ (np.eye(n) - P) @ E)[0][:, :] if False else None
# sigma-odd part of E: project onto odd subspace
Q = E @ E.T; Qo = Q @ (np.eye(n) - P) / 2
w, Z = np.linalg.eigh(Qo); Eo = Z[:, w > 0.5]; print('odd -5 eigenspace dim =', Eo.shape[1])
out = [v for v in range(n) if v not in set(T)]
M = Eo[out, :]
s = np.linalg.svd(M, compute_uv=False); null = int((s < 1e-8).sum()) + max(0, Eo.shape[1] - len(out))
print('dim of odd -5 eigenvectors vanishing off T =', Eo.shape[1] - int((s > 1e-8).sum()))
# generalisation: support on the union of the stars of a block set S (vanish on labels avoiding S), |S| = 1..4
for k in range(1, 6):
    Sk = set(range(1, k + 1))
    keep = [v for v in lab if {b for b, _ in lab[v]} & Sk]
    outk = [v for v in range(n) if v not in set(keep)]
    s = np.linalg.svd(Eo[outk, :], compute_uv=False)
    print('k =', k, '| labels meeting S:', len(keep), '| odd -5 eigvecs vanishing on labels avoiding S (and interior):', Eo.shape[1] - int((s > 1e-8).sum()))
