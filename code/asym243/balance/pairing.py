import sys, numpy as np
U = np.load(sys.argv[1]); n = U.shape[0] // 8
blk = lambda i: slice(8 * i, 8 * i + 8)
adj = np.array([[i != j and np.abs(U[blk(i), blk(j)]).max() > 1e-9 for j in range(n)] for i in range(n)])
part = [-1] * n; p = 0
for i in range(n):
    if part[i] < 0:
        for j in range(n):
            if not adj[i, j]: part[j] = p
        p += 1
Ridx = np.concatenate([np.arange(8 * i, 8 * i + 4) for i in range(n)])
cellR = np.repeat(np.arange(n), 4)
C = U[np.ix_(Ridx, Ridx)]; ev, V = np.linalg.eigh(C)
inner = np.where((ev < 1 - 1e-6) & (ev > -1 + 1e-6))[0]
print("inner eigenvalues and part-weights (part0, part1, part2):")
for k in inner:
    w = [np.sum(V[np.array(part)[cellR] == q, k] ** 2) for q in range(3)]
    print(f"  {ev[k]:+.5f}   " + "  ".join(f"{x:.4f}" for x in w))
K = np.kron(np.eye(n), np.diag([1.] * 4 + [-1.] * 4)); N = U - K / 3
Npl = N.copy()
for i in range(n):
    for j in range(n):
        if adj[i, j] and (part[j] - part[i]) % 3 != 1: Npl[blk(i), blk(j)] = 0
al = Npl[np.ix_(Ridx, Ridx)]
Vi = V[:, inner]; Pin = Vi @ Vi.T
A_in = Vi.T @ al @ Vi; C_in = Vi.T @ C @ Vi
print("|[alpha, C]| on inner part:", np.linalg.norm(A_in @ C_in - C_in @ A_in), "  |alpha| there:", np.linalg.norm(A_in))
s = np.linalg.svd(A_in, compute_uv=False); print("singular values of alpha on inner part:", np.round(s[:6], 5), "...", np.round(s[-4:], 5))
print("does alpha map inner -> inner?  |(I-Pin) alpha Pin| =", np.linalg.norm((np.eye(len(Ridx)) - Pin) @ al @ Pin))
ev_a = np.linalg.eigvals(A_in); print("eigenvalues of alpha on inner part (moduli, args/pi):", np.round(sorted(np.abs(ev_a))[:6], 4), np.round(sorted(np.angle(ev_a) / np.pi)[:8], 4))
