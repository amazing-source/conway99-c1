"""Ranks of the h-even compression A, of S_A = A - B C^+ B^T and of B (LAB 15/10/2026, task T3).
nullity T = 2 + nullity(S_A) when nullity C = 2.  usage: python hblock_ranks.py <json or bundle> [...]"""
import json, sys, glob
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
from collections import Counter

def items(f):
    d = json.load(open(f))
    if "structures" in d:
        for s in d["structures"]:
            yield d["labels"], s["edges"]
    else:
        yield d["labels"], d["edges"]

cnt = Counter()
files = []
for pat in sys.argv[1:]:
    files += glob.glob(pat)
for f in files:
    for labels, edges in items(f):
        S = [frozenset(l) for l in labels]; n = len(S); idx = {s: i for i, s in enumerate(S)}
        hm = {0: 1, 1: 0, 2: 3, 3: 2}
        hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
        H = np.zeros((n, n))
        for i in range(n): H[hp[i], i] = 1
        Qp = np.linalg.svd((np.eye(n) + H) / 2)[0][:, :22]; Qm = np.linalg.svd((np.eye(n) - H) / 2)[0][:, :22]
        G = np.zeros((n, n))
        for i, j in edges: G[i, j] = G[j, i] = 1
        T = 3*np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
        A = Qp.T @ T @ Qp; C = Qm.T @ T @ Qm; B = Qp.T @ T @ Qm
        rk = lambda X: int(np.sum(np.abs(np.linalg.eigvalsh((X + X.T) / 2)) > 1e-8))
        SA = A - B @ np.linalg.pinv(C, rcond=1e-9) @ B.T
        nulT = n - rk(T)
        D84 = np.zeros((14, 84))
        for jj, l in enumerate(LABELS):
            for y in l: D84[y, jj] = 1
        Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
        pos = {l: ii for ii, l in enumerate(LABELS)}
        PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
        Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
        Qz, _ = np.linalg.qr(Z); Pp = np.eye(n) - Qz @ Qz.T
        lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
        lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
        psd = "TU" if min(lt, lu) > -1e-9 else ("T" if lt > -1e-9 else "-")
        cnt[(nulT, rk(A), rk(SA), int(np.linalg.matrix_rank(B, tol=1e-8)), 22 - rk(C), psd)] += 1
print("(nullity T, rank A, rank S_A, rank B, nullity C, PSD): count")
for k, v in sorted(cnt.items(), key=lambda t: (-t[0][0], t[0])):
    print("  ", k, v)
