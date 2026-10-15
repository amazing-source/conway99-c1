import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
d = json.load(open(sys.argv[1]))
labs = d["labels"]; S = [frozenset(l) for l in labs]; n = len(S)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
K = np.array([[kval(a, b) for b in S] for a in S])
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Qp = np.linalg.svd(np.eye(n) - Qz @ Qz.T)[0][:, :n-4]   # basis of Z^perp
from collections import Counter
cnt = Counter()
for k, s in enumerate(d["structures"][:int(sys.argv[2]) if len(sys.argv) > 2 else None]):
    G = np.zeros((n, n))
    for i, j in s["edges"]: G[i, j] = G[j, i] = 1
    T = 3*np.eye(n) - G - K
    U = 7*PiS - T
    Tp, Up, Pp = Qp.T @ T @ Qp, Qp.T @ U @ Qp, Qp.T @ (7*PiS) @ Qp
    rT = int(np.sum(np.linalg.eigvalsh(Tp) > 1e-7)); rU = int(np.sum(np.linalg.eigvalsh(Up) > 1e-7))
    # generalized eigenvalues of T relative to 7 Pi on Z^perp
    L = np.linalg.cholesky(Pp); Li = np.linalg.inv(L)
    ev = np.linalg.eigvalsh(Li @ Tp @ Li.T)
    n0 = int(np.sum(ev < 1e-7)); n1 = int(np.sum(ev > 1 - 1e-7))
    mid = sorted(set(np.round(ev[(ev > 1e-7) & (ev < 1 - 1e-7)], 4)))
    key = (rT, rU, n0, n1, len(mid))
    cnt[key] += 1
    if k < 6 or cnt[key] == 1:
        print(k, s["c"], "rank T", rT, "rank U", rU, "| pencil: zeros", n0, "ones", n1, "| distinct middle", mid[:12])
print(cnt)
