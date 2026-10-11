"""Balance <=> tr(alpha^3) + |alpha|^2 = 16, and the operator identity Y_RR^2 = (8/3)(8/27 - a^3 - a^T^3 - 2 a a^T)."""
import sys, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from normal import from_graph
def check(U, name):
    n = U.shape[0] // 8; blk = lambda i: slice(8 * i, 8 * i + 8)
    adj = np.array([[i != j and np.abs(U[blk(i), blk(j)]).max() > 1e-9 for j in range(n)] for i in range(n)])
    part = [-1] * n; p = 0
    for i in range(n):
        if part[i] < 0:
            for j in range(n):
                if not adj[i, j]: part[j] = p
            p += 1
    K = np.kron(np.eye(n), np.diag([1.] * 4 + [-1.] * 4)); N = U - K / 3; Np = N.copy()
    for i in range(n):
        for j in range(n):
            if adj[i, j] and (part[j] - part[i]) % 3 != 1: Np[blk(i), blk(j)] = 0
    R = np.concatenate([np.arange(8 * i, 8 * i + 4) for i in range(n)]); a = Np[np.ix_(R, R)]
    X = Np.T @ Np - 4 / 9 * np.eye(8 * n); Y = X @ K + K @ X; YRR = Y[np.ix_(R, R)]
    rhs = (8 / 3) * (8 / 27 * np.eye(len(R)) - a @ a @ a - a.T @ a.T @ a.T - 2 * a @ a.T)
    print(f"{name}: tr(a^3)+|a|^2 = {np.trace(a @ a @ a) + np.sum(a * a):.12f}   |Y_RR^2 - rhs| = {np.abs(YRR @ YRR - rhs).max():.1e}")
for arg in sys.argv[1:]:
    if arg.endswith(".npy") and "Ucurve" in arg: check(np.load(arg), arg.split("/")[-1])
    else:
        path, pidx = arg.split(":"); check(from_graph(path, int(pidx)), arg)
