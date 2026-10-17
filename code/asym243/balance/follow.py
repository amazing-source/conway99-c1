"""Follow a second-order-unobstructed deformation direction of the orthogonal-block configuration.
Gauss-Newton with minimum-norm steps (lsqr), multiplicative update U_AB <- U_AB expm(Delta_AB).
Reports residual floor vs eps (true curve => machine precision) and the balance data along the way."""
import sys, pickle, numpy as np, scipy.sparse as sp
from scipy.linalg import expm
from scipy.sparse.linalg import lsqr
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges
path, pidx, dirfile, t = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
epss = [float(e) for e in sys.argv[5].split(",")]
G = np.load(path) if path.endswith(".npy") else load_edges(path)
part = pickle.load(open(path + ".gridparts.pkl", "rb"))[pidx]
n = len(part); N8 = 8 * n
Q = [[i != j and bool(G[np.ix_(part[i], part[j])].sum()) for j in range(n)] for i in range(n)]
B = []
for c in part:
    w, V = np.linalg.eigh(G[np.ix_(c, c)].astype(float))
    B.append(np.hstack([V[:, np.abs(w - 1) < 1e-8], V[:, np.abs(w + 2) < 1e-8]]))
K8 = np.diag([1.] * 4 + [-1.] * 4)
blk = lambda i: slice(8 * i, 8 * i + 8)
U0 = np.zeros((N8, N8)); pairs = []
for i in range(n):
    U0[blk(i), blk(i)] = K8 / 3
    for j in range(n):
        if Q[i][j]:
            U0[blk(i), blk(j)] = (2 / 9) * B[i].T @ G[np.ix_(part[i], part[j])].astype(float) @ B[j]
            if i < j: pairs.append((i, j))
sk = [(k, l) for k in range(8) for l in range(k + 1, 8)]
nadj = [[j for j in range(n) if Q[i][j]] + [i] for i in range(n)]
def skew(x):
    M = np.zeros((8, 8))
    for si, (a, b) in enumerate(sk): M[a, b] = x[si]; M[b, a] = -x[si]
    return M
def apply(U, x):
    U = U.copy()
    for p, (i, j) in enumerate(pairs):
        M = U[blk(i), blk(j)] @ expm(skew(x[28 * p: 28 * p + 28])); U[blk(i), blk(j)] = M; U[blk(j), blk(i)] = M.T
    return U
def jac(U):
    rows, cols, vals = [], [], []; col = 0
    for (i, j) in pairs:
        Uij = U[blk(i), blk(j)]
        for (k, l) in sk:
            X = np.zeros((8, 8)); X[k, l] = 1; X[l, k] = -1
            d = Uij @ X; Dm = {}
            for c in nadj[i]: Dm[(c, j)] = Dm.get((c, j), 0) + U[blk(c), blk(i)] @ d
            for c in nadj[j]: Dm[(c, i)] = Dm.get((c, i), 0) + U[blk(c), blk(j)] @ d.T
            for c in nadj[j]: Dm[(i, c)] = Dm.get((i, c), 0) + d @ U[blk(j), blk(c)]
            for c in nadj[i]: Dm[(j, c)] = Dm.get((j, c), 0) + d.T @ U[blk(i), blk(c)]
            for (a, b), M in Dm.items():
                nz = np.nonzero(np.abs(M) > 1e-15)
                rows.extend(((a * 8 + nz[0]) * N8 + (b * 8 + nz[1])).tolist()); cols.extend([col] * len(nz[0])); vals.extend(M[nz].tolist())
            col += 1
    return sp.csr_matrix((vals, (rows, cols)), shape=(N8 * N8, col))
Ridx = np.concatenate([np.arange(8 * i, 8 * i + 4) for i in range(n)])
def balance(U):
    ev = np.linalg.eigvalsh(U[np.ix_(Ridx, Ridx)])
    m = int(np.sum(ev > 1 - 1e-6)); mp = int(np.sum(ev < -1 + 1e-6)); inner = ev[(ev <= 1 - 1e-6) & (ev >= -1 + 1e-6)]
    return m, mp, inner.sum(), ev.sum()
D = np.load(dirfile)
if D.shape[1] == 2: d = np.cos(t) * D[:, 0] + np.sin(t) * D[:, 1]
else: d = D @ np.random.default_rng(int(t)).standard_normal(D.shape[1])
d /= np.linalg.norm(d)
print("base balance (m, m', sum cos2, trace):", balance(U0), flush=True)
for eps in epss:
    U = apply(U0, eps * d)
    for it in range(12):
        F = (U @ U - np.eye(N8)).ravel(); res = np.linalg.norm(F)
        print(f"  eps={eps} it={it} residual={res:.3e}", flush=True)
        if res < 1e-12: break
        J = jac(U); step = lsqr(J, -F, atol=1e-15, btol=1e-15, iter_lim=20000)[0]
        U = apply(U, step)
    dist = np.linalg.norm(U - U0)
    print(f"eps={eps}: final residual {res:.3e}, |U-U0| = {dist:.4e}, balance (m, m', sum cos2, trace) = {balance(U)}", flush=True)
    np.save(f"Ucurve_{path.split(chr(47))[-1]}_{eps}_{t:.4f}.npy", U)
