"""Far side of a line in a real srg(v,k,1,2) (LAB 19/10/2026): test of the identities of NOTE_MANDAT section 4.
For a line T = {p,q,s}: N = N(T) (6t vertices, classes N(p)\\T, N(q)\\T, N(s)\\T), G_T the graph induced on N (cubic),
F the far set (vertices with no neighbour in T), E the N x F adjacency, R_T the graph induced on F.  Checked exactly:
  (I1) E E^T = (k-2) I - G_T - G_T^2 + 2 J - J_class         (from A^2 = (k-2) I - A + 2 J, lambda = 1, mu = 2)
  (I2) E R_T = 2 J - E - G_T E
  (I3) R_T^2 + R_T + E^T E = (k-2) I + 2 J
and numerically: the spectrum of R_T, the number c(T) of components of G_T, and dim(E_theta(Gamma) cap R^F) for the two
restricted eigenvalues theta = r, s, compared with the prediction of the trace argument (Conway: 18 and 7 + c(T);
family member with r != 3: independent of c(T)).
usage: python far_frame_check.py <edges file> [n_lines]"""
import sys
from itertools import combinations

import numpy as np

EDG, NL = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6
edges = [tuple(map(int, l.split())) for l in open(EDG) if l.strip()]
v = 1 + max(max(e) for e in edges)
A = np.zeros((v, v), dtype=np.int64)
for a, b in edges:
    A[a, b] = A[b, a] = 1
k = int(A[0].sum())
assert (A.sum(1) == k).all()
A2 = A @ A
J = np.ones((v, v), dtype=np.int64)
assert ((A2 - ((k - 2) * np.eye(v, dtype=np.int64) - A + 2 * J)) == 0).all(), 'not srg(v,k,1,2)'
disc = np.sqrt(1 + 4 * (k - 2))
r, s = (-1 + disc) / 2, (-1 - disc) / 2
ev, evec = np.linalg.eigh(A.astype(float))
lines = sorted({tuple(sorted((a, b, c))) for a in range(v) for b in np.nonzero(A[a])[0] for c in np.nonzero(A[a] * A[b])[0]})
print('srg(%d,%d,1,2): r = %g, s = %g, %d lines' % (v, k, r, s, len(lines)))
for T in lines[:NL]:
    Tset = set(T)
    classes = [[u for u in np.nonzero(A[p])[0] if u not in Tset] for p in T]
    Nl = [u for cl in classes for u in cl]
    Ns = set(Nl)
    F = [u for u in range(v) if u not in Tset and u not in Ns]
    G = A[np.ix_(Nl, Nl)]
    E = A[np.ix_(Nl, F)]
    R = A[np.ix_(F, F)]
    n, f = len(Nl), len(F)
    Jc = np.zeros((n, n), dtype=np.int64)
    off = 0
    for cl in classes:
        Jc[off:off + len(cl), off:off + len(cl)] = 1
        off += len(cl)
    I1 = E @ E.T - ((k - 2) * np.eye(n, dtype=np.int64) - G - G @ G + 2 * np.ones((n, n), dtype=np.int64) - Jc)
    I2 = E @ R - (2 * np.ones((n, f), dtype=np.int64) - E - G @ E)
    I3 = R @ R + R + E.T @ E - ((k - 2) * np.eye(f, dtype=np.int64) + 2 * np.ones((f, f), dtype=np.int64))
    # components of G_T
    seen, comps = set(), 0
    for x in range(n):
        if x in seen:
            continue
        comps += 1
        stack = [x]
        while stack:
            y = stack.pop()
            if y in seen:
                continue
            seen.add(y)
            stack.extend(int(z) for z in np.nonzero(G[y])[0])
    dims = {}
    for th in (r, s):
        P = evec[:, np.abs(ev - th) < 1e-6]
        restr = P[[u for u in range(v) if u not in set(F)], :]
        sv = np.linalg.svd(restr, compute_uv=False)
        dims[round(th, 3)] = P.shape[1] - int((sv > 1e-8).sum())
    spec = np.round(np.linalg.eigvalsh(R.astype(float)), 6)
    vals, cnt = np.unique(spec, return_counts=True)
    print('line %s: c = %d, |N| = %d, |F| = %d, I1 %s, I2 %s, I3 %s, far eigen-dims %s, R_T spectrum %s' % (
        T, comps, n, f, 'ok' if not I1.any() else 'FAIL', 'ok' if not I2.any() else 'FAIL',
        'ok' if not I3.any() else 'FAIL', dims, dict(zip(vals.tolist(), cnt.tolist()))))


def projector_check(T):
    """(r - s) Pi_s = (r I - R_T)(I - E^T (E E^T)^+ E) on the far set, Pi_s = projection onto E_s(Gamma) cap R^F."""
    Tset = set(T)
    Nl = [u for p in T for u in np.nonzero(A[p])[0] if u not in Tset]
    F = [u for u in range(v) if u not in Tset and u not in set(Nl)]
    E = A[np.ix_(Nl, F)].astype(float)
    R = A[np.ix_(F, F)].astype(float)
    P = evec[:, np.abs(ev - s) < 1e-6]
    rest = np.array([u for u in range(v) if u not in set(F)])
    # basis of eigenvectors vanishing on the complement of F
    M = P[rest, :]
    _, sv, vt = np.linalg.svd(M)
    null = vt[(sv > 1e-8).sum():].T if (sv > 1e-8).sum() < P.shape[1] else np.zeros((P.shape[1], 0))
    Wb = (P @ null)[F, :]
    Q, _ = np.linalg.qr(Wb)
    Pi_true = Q @ Q.T
    Pim = E.T @ np.linalg.pinv(E @ E.T) @ E
    Pi_formula = (r * np.eye(len(F)) - R) @ (np.eye(len(F)) - Pim) / (r - s)
    return np.abs(Pi_true - Pi_formula).max(), Q.shape[1]


for T in lines[:NL]:
    err, dim = projector_check(T)
    print('projector identity on line %s: max error %.2e, far s-dimension %d' % (tuple(int(x) for x in T), err, dim))
