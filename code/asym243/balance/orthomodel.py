"""Orthogonal-block model on a quotient graph Q (cells = vertices of Q), cell space Z_A = R_A (+) S_A (dims d, d).
U = alpha*K + beta*sum_{A~B} O_AB, O_AB in O(2d), U^2 = I.  alpha^2 + beta^2*deg = 1.
Q = 'tri c' (complete tripartite K_{c,c,c}) or 'K n' (complete graph).  Random restarts, least squares.
Report residual and, for solutions, the R-compression spectrum: m, m', sum of inner, symmetry of inner."""
import sys, numpy as np
from scipy.optimize import least_squares
from scipy.linalg import expm
kind, c, d, alpha, trials, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(eval(sys.argv[4])), int(sys.argv[5]), int(sys.argv[6])
if kind == "tri":
    n = 3 * c; adj = [[(i // c) != (j // c) for j in range(n)] for i in range(n)]
else:
    n = c; adj = [[i != j for j in range(n)] for i in range(n)]
deg = sum(adj[0]); beta = np.sqrt((1 - alpha ** 2) / deg)
pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if adj[i][j]]
D = 2 * d; nsk = D * (D - 1) // 2; iu = np.triu_indices(D, 1)
Kc = np.diag([1.] * d + [-1.] * d)
blk = lambda i: slice(D * i, D * i + D)
def build(x):
    U = np.kron(np.eye(n), alpha * Kc)
    for p, (i, j) in enumerate(pairs):
        S = np.zeros((D, D)); S[iu] = x[nsk * p: nsk * (p + 1)]; S = S - S.T
        O = expm(S)
        if x[-len(pairs) + p] < 0: O = O @ np.diag([-1.] + [1.] * (D - 1))   # allow det -1
        U[blk(i), blk(j)] = beta * O; U[blk(j), blk(i)] = beta * O.T
    return U
def res(x, signs):
    U = build(np.concatenate([x, signs])); E = U @ U - np.eye(n * D)
    return E[np.triu_indices(n * D, 1)]
rng = np.random.default_rng(seed); out = []
Ridx = np.concatenate([np.arange(D * i, D * i + d) for i in range(n)])
for t in range(trials):
    signs = rng.choice([-1., 1.], len(pairs))
    x0 = rng.standard_normal(nsk * len(pairs)) * 2
    s = least_squares(res, x0, args=(signs,), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    r = np.linalg.norm(s.fun)
    if r > 1e-8: out.append(("no", round(r, 4))); continue
    U = build(np.concatenate([s.x, signs])); ev = np.sort(np.linalg.eigvalsh(U[np.ix_(Ridx, Ridx)]))
    m = int(np.sum(ev > 1 - 1e-6)); mp = int(np.sum(ev < -1 + 1e-6)); inn = ev[(ev <= 1 - 1e-6) & (ev >= -1 + 1e-6)]
    sym = np.abs(np.sort(inn) + np.sort(inn)[::-1]).max() if len(inn) else 0.0
    out.append(("SOL", m, mp, round(float(inn.sum()), 6), f"sym={sym:.1e}"))
from collections import Counter
print(kind, c, d, "alpha", alpha, "beta", round(beta, 5), "->", Counter(out).most_common(12))
