"""Orthogonal-block model at 243: U = K/3 + (2/9) sum O_AB on Z (216-dim), O_AB in O(8), U^2 = I.
Tangent space at a real graph's grid partition: X_AB skew, dU_AB = U_AB X_AB.  Compare nullity with gauge rank."""
import sys, pickle, numpy as np, scipy.sparse as sp
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges
path, pidx = sys.argv[1], int(sys.argv[2])
G = np.load(path) if path.endswith(".npy") else load_edges(path)
part = pickle.load(open(path + ".gridparts.pkl", "rb"))[pidx]
n = len(part)
Q = [[i != j and bool(G[np.ix_(part[i], part[j])].sum()) for j in range(n)] for i in range(n)]
B = []
for c in part:
    w, V = np.linalg.eigh(G[np.ix_(c, c)].astype(float))
    R = V[:, np.abs(w - 1) < 1e-8]; S = V[:, np.abs(w + 2) < 1e-8]
    assert R.shape[1] == 4 and S.shape[1] == 4
    B.append(np.hstack([R, S]))
K8 = np.diag([1.] * 4 + [-1.] * 4)
U = np.zeros((8 * n, 8 * n))
blk = lambda i: slice(8 * i, 8 * i + 8)
pairs = []
for i in range(n):
    U[blk(i), blk(i)] = K8 / 3
    for j in range(n):
        if Q[i][j]:
            U[blk(i), blk(j)] = (2 / 9) * B[i].T @ G[np.ix_(part[i], part[j])].astype(float) @ B[j]
            if i < j: pairs.append((i, j))
print("pairs", len(pairs), " |U^2 - I| =", np.abs(U @ U - np.eye(8 * n)).max())
sk = [(k, l) for k in range(8) for l in range(k + 1, 8)]
nadj = [[j for j in range(n) if Q[i][j]] + [i] for i in range(n)]
rows, cols, vals = [], [], []
col = 0
for (i, j) in pairs:
    Uij = U[blk(i), blk(j)]
    for (k, l) in sk:
        X = np.zeros((8, 8)); X[k, l] = 1; X[l, k] = -1
        dUij = Uij @ X                       # block (i,j); block (j,i) = dUij.T
        D = {}
        # (U dU)_{c,j} += U_{c,i} dU_ij ; (U dU)_{c,i} += U_{c,j} dU_ji
        for c in nadj[i]: D[(c, j)] = D.get((c, j), 0) + U[blk(c), blk(i)] @ dUij
        for c in nadj[j]: D[(c, i)] = D.get((c, i), 0) + U[blk(c), blk(j)] @ dUij.T
        # (dU U)_{i,c} += dU_ij U_jc ; (dU U)_{j,c} += dU_ji U_ic
        for c in nadj[j]: D[(i, c)] = D.get((i, c), 0) + dUij @ U[blk(j), blk(c)]
        for c in nadj[i]: D[(j, c)] = D.get((j, c), 0) + dUij.T @ U[blk(i), blk(c)]
        for (a, b), M in D.items():
            if a > b: continue
            for p in range(8):
                for q in range(8):
                    if a == b and q < p: continue
                    v = M[p, q] if a != b else (M[p, q] + (M[q, p] if p != q else 0)) / (1 if p == q else 1)
                    if abs(v) > 1e-13: rows.append((a * 8 + p) * 8 * n + (b * 8 + q)); cols.append(col); vals.append(v)
        col += 1
# symmetric result: for a<b we used entry (a,b) only, but (a,b) also receives contributions recorded under (b,a); fix by symmetrising
r = np.array(rows); c_ = np.array(cols); v = np.array(vals)
J = sp.csr_matrix((v, (r, c_)), shape=((8 * n) ** 2, col))
J = J[np.unique(r)]
print("J", J.shape, "nnz", J.nnz, flush=True)
JTJ = (J.T @ J).toarray()
ev = np.linalg.eigvalsh(JTJ)
null = int(np.sum(ev < 1e-9 * ev.max()))
print("nullity of linearised U^2=I :", null, "  smallest nonzero ev", ev[ev >= 1e-9 * ev.max()][:3])
# gauge: Y_c in so(4)+so(4) per cell  ->  X_ij = O_ij^T Y_i O_ij - Y_j  (O = (9/2) U_ij)
gs = [(k, l) for k in range(4) for l in range(k + 1, 4)] + [(k, l) for k in range(4, 8) for l in range(k + 1, 8)]
Gm = np.zeros((col, 12 * n))
for ci in range(n):
    for gi, (k, l) in enumerate(gs):
        Y = np.zeros((8, 8)); Y[k, l] = 1; Y[l, k] = -1
        for pi, (i, j) in enumerate(pairs):
            O = 4.5 * U[blk(i), blk(j)]
            X = (O.T @ Y @ O if i == ci else 0) - (Y if j == ci else 0)
            if isinstance(X, np.ndarray):
                for si, (a, b) in enumerate(sk): Gm[pi * 28 + si, ci * 12 + gi] = X[a, b]
print("gauge rank", np.linalg.matrix_rank(Gm, tol=1e-8), " -> nontrivial infinitesimal deformations:", null - np.linalg.matrix_rank(Gm, tol=1e-8))
