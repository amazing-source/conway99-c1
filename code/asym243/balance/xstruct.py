import sys, numpy as np
U = np.load(sys.argv[1]); n = U.shape[0] // 8; blk = lambda i: slice(8 * i, 8 * i + 8)
adj = np.array([[i != j and np.abs(U[blk(i), blk(j)]).max() > 1e-9 for j in range(n)] for i in range(n)])
part = [-1] * n; p = 0
for i in range(n):
    if part[i] < 0:
        for j in range(n):
            if not adj[i, j]: part[j] = p
        p += 1
K = np.kron(np.eye(n), np.diag([1.] * 4 + [-1.] * 4)); N = U - K / 3; Npl = N.copy()
for i in range(n):
    for j in range(n):
        if adj[i, j] and (part[j] - part[i]) % 3 != 1: Npl[blk(i), blk(j)] = 0
I = np.eye(8 * n); X = Npl.T @ Npl - 4 / 9 * I
R = np.kron(np.eye(n), np.diag([1.] * 4 + [0.] * 4)); S = I - R
nm = lambda M: np.linalg.norm(M)
print("|X| =", nm(X), " |{N+,X}| =", nm(Npl @ X + X @ Npl))
print("|X_RR| =", nm(R @ X @ R), " |X_SS| =", nm(S @ X @ S), " |X_RS| =", nm(R @ X @ S))
print("|[X,K]| =", nm(X @ K - K @ X), " |{X,K}| =", nm(X @ K + K @ X))
cd = max(nm(X[blk(i), blk(i)]) for i in range(n)); print("max cell-diagonal block of X:", cd)
