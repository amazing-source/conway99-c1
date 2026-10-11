"""Real relaxation of grid covers: orthogonal-block configurations on a quotient graph Q.
U = alpha K + beta sum_{A~B} O_AB on Z = (+)_A (R_A + S_A), O_AB in O(2d), U^2 = I.  Levenberg-Marquardt with the
analytic Jacobian (multiplicative updates O <- O expm(X)).  Random orthogonal starts (both determinant classes).
  python3 relax.py K n d alpha trials seed      (complete quotient K_n)
  python3 relax.py tri c d alpha trials seed    (complete tripartite K_{c,c,c})"""
import sys, numpy as np
from scipy.linalg import expm
from scipy.stats import ortho_group
kind, c, d, alpha, trials, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(eval(sys.argv[4])), int(sys.argv[5]), int(sys.argv[6])
n = 3 * c if kind == "tri" else c
adj = np.array([[(i // c != j // c) if kind == "tri" else (i != j) for j in range(n)] for i in range(n)])
deg = adj[0].sum(); beta = np.sqrt((1 - alpha ** 2) / deg)
pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if adj[i, j]]
D = 2 * d; N = n * D; sk = [(k, l) for k in range(D) for l in range(k + 1, D)]; ns = len(sk)
K = np.kron(np.eye(n), np.diag([1.] * d + [-1.] * d))
blk = lambda i: slice(D * i, D * i + D)
iu = np.triu_indices(N, 1)
def U_of(O):
    U = alpha * K.copy()
    for (i, j), M in zip(pairs, O): U[blk(i), blk(j)] = beta * M; U[blk(j), blk(i)] = beta * M.T
    return U
def jac(U):
    J = np.zeros((len(iu[0]), len(pairs) * ns))
    col = 0
    for (i, j) in pairs:
        Uij = U[blk(i), blk(j)]
        for (k, l) in sk:
            dU = np.zeros((N, N)); X = np.zeros((D, D)); X[k, l] = 1; X[l, k] = -1
            dm = Uij @ X; dU[blk(i), blk(j)] = dm; dU[blk(j), blk(i)] = dm.T
            J[:, col] = (U @ dU + dU @ U)[iu]; col += 1
    return J
rng = np.random.default_rng(seed)
for t in range(trials):
    O = [ortho_group.rvs(D, random_state=rng) for _ in pairs]
    mu = 1e-2; U = U_of(O); F = (U @ U - np.eye(N))[iu]; r = np.linalg.norm(F)
    for it in range(400):
        J = jac(U); g = J.T @ F; A = J.T @ J
        while True:
            step = np.linalg.solve(A + mu * np.eye(A.shape[0]), -g)
            O2 = [M @ expm(np.array([[0] * 0]) if False else _sk) for M, _sk in zip(O, [None] * 0)] if False else None
            O2 = []
            for p, M in enumerate(O):
                X = np.zeros((D, D))
                for s, (k, l) in enumerate(sk): X[k, l] = step[p * ns + s]; X[l, k] = -step[p * ns + s]
                O2.append(M @ expm(X))
            U2 = U_of(O2); F2 = (U2 @ U2 - np.eye(N))[iu]; r2 = np.linalg.norm(F2)
            if r2 < r: O, U, F, r = O2, U2, F2, r2; mu = max(mu / 3, 1e-12); break
            mu *= 4
            if mu > 1e8: break
        if r < 1e-12 or mu > 1e8: break
    Ridx = np.concatenate([np.arange(D * i, D * i + d) for i in range(n)])
    msg = f"trial {t}: residual {r:.3e} after {it} its"
    if r < 1e-9:
        ev = np.sort(np.linalg.eigvalsh(U[np.ix_(Ridx, Ridx)]))
        m = int(np.sum(ev > 1 - 1e-6)); mp = int(np.sum(ev < -1 + 1e-6)); inn = ev[(ev <= 1 - 1e-6) & (ev >= -1 + 1e-6)]
        sym = np.abs(np.sort(inn) + np.sort(inn)[::-1]).max() if len(inn) else 0
        msg += f"  SOLUTION m={m} m'={mp} sum_inner={inn.sum():.6f} m-m'+sum={m - mp + inn.sum():.6f} sym={sym:.1e}"
    print(msg, flush=True)
