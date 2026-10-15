"""Pencil spectra of the h-even and h-odd compressions (LAB 15/10/2026, T3): eigenvalues of A relative to 7 Pi_+ and of C
relative to 7 Pi_- on the complements of the star vectors (generalised eigenproblem A x = lambda 7 Pi_+ x).
If the h-even spectrum is {0, 1} only, T >= 0 and U >= 0 force B = 0.  usage: python hpencil.py <bundle or json> [max]"""
import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
from collections import Counter
d = json.load(open(sys.argv[1]))
structs = d["structures"] if "structures" in d else [d]
mx = int(sys.argv[2]) if len(sys.argv) > 2 else len(structs)
S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
H = np.zeros((n, n))
for i in range(n): H[hp[i], i] = 1
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l: D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
K = np.array([[kval(a, b) for b in S] for a in S])
def pencil(T, P, Q):
    # restrict to range of Q, then to the range of P there (P > 0 off the stars)
    Pq = Q.T @ P @ Q; w, V = np.linalg.eigh(Pq); keep = w > 1e-9
    R = V[:, keep] / np.sqrt(w[keep])
    return np.sort(np.linalg.eigvalsh(R.T @ (Q.T @ T @ Q) @ R))
cnt = Counter()
for k, s in enumerate(structs[:mx]):
    G = np.zeros((n, n))
    for i, j in s["edges"]: G[i, j] = G[j, i] = 1
    T = 3*np.eye(n) - G - K
    Qp = np.linalg.svd((np.eye(n) + H) / 2)[0][:, :22]; Qm = np.linalg.svd((np.eye(n) - H) / 2)[0][:, :22]
    ep = pencil(T, 7*PiS, Qp); em = pencil(T, 7*PiS, Qm)
    rp = tuple(sorted(Counter(np.round(ep, 4)).items())); rm = tuple(sorted(Counter(np.round(em, 4)).items()))
    if k < 4:
        print(k, s.get("c"), "\n  h-even pencil:", rp, "\n  h-odd pencil:", rm)
    cnt[(sum(1 for x in ep if abs(x) < 1e-6), sum(1 for x in ep if abs(x - 1) < 1e-6), sum(1 for x in ep if 1e-6 < x < 1 - 1e-6))] += 1
print("(h-even: #0, #1, #middle): count", dict(cnt))
