"""rank_7 scan of saved four-star structures (15/10/2026).

For each json (labels, edges): M8 = 8T_S = 24I - 8 Gamma - 8K (integral), exact rank over Q, rank over F_7,
numerical lambda_min of T on the complement of the star vectors and of U = 7 Pi_S - T.  A Conway four-star structure
needs T, U >= 0, rank_Q <= 30 and rank_7(8T_S) <= k <= 28 (Codex L4 + L22).
usage: python r7_scan.py <json> [<json> ...]
"""
import json
import sys

import numpy as np

from stars_rank import kval, LABELS
from z5_enum import exact_rank


def rank_mod(M, p):
    A = [[x % p for x in row] for row in M]
    n, m = len(A), len(A[0])
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(n):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
        if r == n:
            break
    return r


D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {frozenset(l): i for i, l in enumerate(LABELS)}

for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    letters = sorted(set(y for s in S for y in s))
    cnt = {y: sum(1 for s in S if y in s) for y in letters}
    starl = [y for y in letters if cnt[y] == 12]
    Z = np.array([[1.0 if y in s else 0.0 for s in S] for y in starl]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T
    T = M8 / 8.0
    ix = [pos[s] for s in S]
    U = 7 * Pi[np.ix_(ix, ix)] - T
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ U @ Pp + 50 * (np.eye(n) - Pp))[0])
    rq = exact_rank(M8.tolist())
    r7 = rank_mod(M8.tolist(), 7)
    print("%s: n %d, stars %s, rank_Q %d, rank_7 %d, lambda_T %.4f, lambda_U %.4f, c %s"
          % (f, n, starl, rq, r7, lt, lu, d.get("c")), flush=True)
