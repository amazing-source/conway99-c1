import sys, numpy as np
f = sys.argv[1]; U = np.load(f); n = U.shape[0] // 8
blk = lambda i: slice(8 * i, 8 * i + 8)
adj = np.array([[i != j and np.abs(U[blk(i), blk(j)]).max() > 1e-9 for j in range(n)] for i in range(n)])
# parts = classes of mutually non-adjacent cells
part = [-1] * n; p = 0
for i in range(n):
    if part[i] < 0:
        for j in range(n):
            if not adj[i, j]: part[j] = p
        p += 1
assert p == 3 and all(x >= 0 for x in part), part
K = np.kron(np.eye(n), np.diag([1.] * 4 + [-1.] * 4))
N = U - K / 3
Np = N.copy()
for i in range(n):
    for j in range(n):
        if adj[i, j]: Np[blk(i), blk(j)] *= (1 if (part[j] - part[i]) % 3 == 1 else -1)
H = (U @ K + K @ U) / 2
print("I1  |N'^T N' - (2/3)(1+H)| =", np.abs(Np.T @ Np - (2 / 3) * (np.eye(8 * n) + H)).max())
print("I2  |{K-U, N'}| =", np.abs((K - U) @ Np + Np @ (K - U)).max())
Ridx = np.concatenate([np.arange(8 * i, 8 * i + 4) for i in range(n)]); Sidx = np.concatenate([np.arange(8 * i + 4, 8 * i + 8) for i in range(n)])
C = U[np.ix_(Ridx, Ridx)]; ev, V = np.linalg.eigh(C)
inner = (ev < 1 - 1e-7) & (ev > -1 + 1e-7)
Vi = V[:, inner]; Pi = Vi @ Vi.T
def test(name, Psi):
    A = Pi @ (Psi @ C + C @ Psi) @ Pi; s = np.linalg.norm(Pi @ Psi @ Pi)
    print(f"  {name:28s} |Pi(Psi C + C Psi)Pi| = {np.linalg.norm(A):.3e}   |Pi Psi Pi| = {s:.3e}")
NRR = Np[np.ix_(Ridx, Ridx)]; NRS = Np[np.ix_(Ridx, Sidx)]; X = U[np.ix_(Ridx, Sidx)]
test("N'_RR", NRR)
test("N'_RS N'_SR", NRS @ NRS.T)
test("X N'_SR", X @ NRS.T)
test("N'_RS X^T", NRS @ X.T)
test("X N'_SR + N'_RS X^T", X @ NRS.T + NRS @ X.T)
test("C N'_RR", C @ NRR)
test("[C, N'_RR]", C @ NRR - NRR @ C)
print("--- intertwiners R -> S :  C_S T = T C  on paired parts (inner(C_S) = -inner(C))")
CS = U[np.ix_(Sidx, Sidx)]; evS, VS = np.linalg.eigh(CS)
innS = (evS < 1 - 1e-7) & (evS > -1 + 1e-7); PiS = VS[:, innS] @ VS[:, innS].T
print("  inner(C_S) == inner(C)?", np.abs(np.sort(evS[innS]) - np.sort(ev[inner])).max())
I8 = np.eye(8 * n)
cands = {"N'_SR": Np, "U N'": U @ Np, "N' U": Np @ U, "K N'": K @ Np, "N' K": Np @ K, "U N' U": U @ Np @ U,
         "N' (K+U)": Np @ (K + U), "(K+U) N'": (K + U) @ Np, "N'^2-part": Np @ Np, "[U,K]": U @ K - K @ U,
         "[U,K] N'": (U @ K - K @ U) @ Np, "N' [U,K]": Np @ (U @ K - K @ U)}
for name, Mx in cands.items():
    T = Mx[np.ix_(Sidx, Ridx)]
    T = PiS @ T @ Pi
    if np.linalg.norm(T) < 1e-9: print(f"  {name:12s} vanishes on paired parts"); continue
    print(f"  {name:12s} |C_S T - T C| / |T| = {np.linalg.norm(CS @ T - T @ C) / np.linalg.norm(T):.3e}")
print("--- cyclic decomposition N = N+ + N+^T  (N+ : part p+1 -> part p)")
Npl = (N + Np) / 2
print("  |N+ N+^T - 4/9| =", np.abs(Npl @ Npl.T - 4 / 9 * I8).max(), "  |N+^T N+ - 4/9| =", np.abs(Npl.T @ Npl - 4 / 9 * I8).max())
print("  |N+^2 + (1/3){K, N+^T}| =", np.abs(Npl @ Npl + (K @ Npl.T + Npl.T @ K) / 3).max())
