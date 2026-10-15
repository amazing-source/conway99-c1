import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
from collections import Counter
d = json.load(open(sys.argv[1])); S = [frozenset(l) for l in d["labels"]]; n = len(S)
idx = {s: i for i, s in enumerate(S)}
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
H = np.zeros((n, n))
for i in range(n): H[hp[i], i] = 1
Pplus = (np.eye(n) + H) / 2; Pminus = (np.eye(n) - H) / 2
K = np.array([[kval(a, b) for b in S] for a in S])
structs = d["structures"] if "structures" in d else [d]
cnt = Counter()
for s in structs:
    G = np.zeros((n, n))
    for i, j in s["edges"]: G[i, j] = G[j, i] = 1
    T = 3*np.eye(n) - G - K
    w, V = np.linalg.eigh(T)
    N = V[:, np.abs(w) < 1e-8]
    kp = np.linalg.matrix_rank(Pplus @ N, tol=1e-7) if N.size else 0
    km = np.linalg.matrix_rank(Pminus @ N, tol=1e-7) if N.size else 0
    # kernels of the h-even and h-odd compressions
    def nul_comp(P):
        Q = np.linalg.svd(P)[0][:, :int(round(np.trace(P)))]
        return int(np.sum(np.abs(np.linalg.eigvalsh(Q.T @ T @ Q)) < 1e-8))
    cnt[(N.shape[1], kp, km, nul_comp(Pplus), nul_comp(Pminus), tuple(s.get("c", [])))] += 1
print("(nullity, rank of h-even part of ker, rank of h-odd part of ker, nullity of T on E+, nullity of T on E-, c): count")
for k, v in sorted(cnt.items()): print("  ", k, v)
