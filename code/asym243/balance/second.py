"""Orthogonal-block model: first-order deformations modulo gauge, and the second-order obstruction.
U = K/3 + (2/9) sum O_AB on Z;  U_AB(eps) = U_AB expm(eps X_AB)."""
import sys, pickle, numpy as np, scipy.sparse as sp
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from lib243 import load_edges
path, pidx = sys.argv[1], int(sys.argv[2])
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
U = np.zeros((N8, N8)); pairs = []
for i in range(n):
    U[blk(i), blk(i)] = K8 / 3
    for j in range(n):
        if Q[i][j]:
            U[blk(i), blk(j)] = (2 / 9) * B[i].T @ G[np.ix_(part[i], part[j])].astype(float) @ B[j]
            if i < j: pairs.append((i, j))
assert np.abs(U @ U - np.eye(N8)).max() < 1e-12
sk = [(k, l) for k in range(8) for l in range(k + 1, 8)]
def skew(x):
    M = np.zeros((8, 8))
    for si, (a, b) in enumerate(sk): M[a, b] = x[si]; M[b, a] = -x[si]
    return M
def dU_of(Xs, power=1):
    D = np.zeros((N8, N8))
    for (i, j), X in zip(pairs, Xs):
        Mx = U[blk(i), blk(j)] @ (np.linalg.matrix_power(X, power) / (1 if power == 1 else 2))
        D[blk(i), blk(j)] = Mx; D[blk(j), blk(i)] = Mx.T
    return D
# full-row Jacobian (Frobenius coordinates), built column by column but only on touched blocks
nadj = [[j for j in range(n) if Q[i][j]] + [i] for i in range(n)]
rows, cols, vals = [], [], []
col = 0
for (i, j) in pairs:
    Uij = U[blk(i), blk(j)]
    for (k, l) in sk:
        X = np.zeros((8, 8)); X[k, l] = 1; X[l, k] = -1
        d = Uij @ X
        Dm = {}
        for c in nadj[i]: Dm[(c, j)] = Dm.get((c, j), 0) + U[blk(c), blk(i)] @ d
        for c in nadj[j]: Dm[(c, i)] = Dm.get((c, i), 0) + U[blk(c), blk(j)] @ d.T
        for c in nadj[j]: Dm[(i, c)] = Dm.get((i, c), 0) + d @ U[blk(j), blk(c)]
        for c in nadj[i]: Dm[(j, c)] = Dm.get((j, c), 0) + d.T @ U[blk(i), blk(c)]
        for (a, b), M in Dm.items():
            nz = np.nonzero(np.abs(M) > 1e-14)
            rows.extend(((a * 8 + nz[0]) * N8 + (b * 8 + nz[1])).tolist()); cols.extend([col] * len(nz[0])); vals.extend(M[nz].tolist())
        col += 1
J = sp.csc_matrix((vals, (rows, cols)), shape=(N8 * N8, col))
JTJ = (J.T @ J).toarray()
ev, EV = np.linalg.eigh(JTJ); tol = 1e-9 * ev.max()
Nul = EV[:, ev < tol]
gs = [(k, l) for k in range(4) for l in range(k + 1, 4)] + [(k, l) for k in range(4, 8) for l in range(k + 1, 8)]
Gm = np.zeros((col, 12 * n))
for ci in range(n):
    for gi, (k, l) in enumerate(gs):
        Y = np.zeros((8, 8)); Y[k, l] = 1; Y[l, k] = -1
        for pi, (i, j) in enumerate(pairs):
            if ci not in (i, j): continue
            O = 4.5 * U[blk(i), blk(j)]
            X = (O.T @ Y @ O if i == ci else 0) - (Y if j == ci else 0)
            for si, (a, b) in enumerate(sk): Gm[pi * 28 + si, ci * 12 + gi] = X[a, b]
r = np.linalg.matrix_rank(Gm, tol=1e-8)
Ug, _, _ = np.linalg.svd(Gm, full_matrices=False); Gimg = Ug[:, :r]
T = Nul - Gimg @ (Gimg.T @ Nul)
u_, s_, _ = np.linalg.svd(T, full_matrices=False); Dirs = u_[:, s_ > 1e-6]
h1 = Dirs.shape[1]
print(f"{path} p{pidx}: tangent {Nul.shape[1]}, gauge orbit {r}, stabiliser {12*n - r}, H1 = {h1}", flush=True)
if h1 == 0: sys.exit()
# second order: w(X) = U D2 + D2 U + D1^2 must lie in range(J) (+ we may add first-order correction)
pinv = EV[:, ev >= tol] @ np.diag(1 / ev[ev >= tol]) @ EV[:, ev >= tol].T
def obstruction(x):
    Xs = [skew(x[28 * p: 28 * p + 28]) for p in range(len(pairs))]
    D1 = dU_of(Xs, 1); D2 = dU_of(Xs, 2)
    w = (U @ D2 + D2 @ U + D1 @ D1).ravel()
    y = pinv @ (J.T @ w)
    return w - J @ y
basis = [Dirs[:, t] for t in range(h1)]
q = {}
for a in range(h1):
    for b in range(a, h1):
        if a == b: q[(a, a)] = obstruction(basis[a])
        else: q[(a, b)] = (obstruction(basis[a] + basis[b]) - obstruction(basis[a]) - obstruction(basis[b])) / 2
for k, v in q.items(): print("  obstruction component", k, "norm", np.linalg.norm(v))
# does some direction a*d0 + b*d1 kill the obstruction?  sample the circle
if h1 == 2:
    vals = []
    for t in np.linspace(0, np.pi, 721):
        c = [np.cos(t), np.sin(t)]
        tot = sum(c[a] * c[b] * (1 if a == b else 2) * v for (a, b), v in q.items())
        vals.append((np.linalg.norm(tot), t))
    print("  min obstruction over unit directions:", min(vals))
q00, q01, q11 = q[(0, 0)], q[(0, 1)], q[(1, 1)]
print("  |q00+q11| =", np.linalg.norm(q00 + q11), " cos(q00,q01) =", q00 @ q01 / np.linalg.norm(q00) / np.linalg.norm(q01))
from scipy.optimize import minimize_scalar
f = lambda t: np.linalg.norm(np.cos(t)**2 * q00 + 2*np.sin(t)*np.cos(t) * q01 + np.sin(t)**2 * q11)
for lo in np.linspace(0, np.pi, 13)[:-1]:
    res = minimize_scalar(f, bounds=(lo, lo + np.pi / 12), method="bounded", options={"xatol": 1e-12})
    if res.fun < 1e-4: print("   local min t=%.10f  |q|=%.3e" % (res.x, res.fun))
np.save(f"{path.split(chr(47))[-1]}_p{pidx}_dirs.npy", Dirs)
