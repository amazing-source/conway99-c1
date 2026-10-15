"""Smallest induced subgraph of H carrying lambda_min < -4 (greedy, by eigenvector weight; then pruning)
(LAB 15/10/2026, mechanism A, question (i)).  usage: python h59_local.py <json>"""
import json, sys
import numpy as np
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S); N = 15 + n
A = np.zeros((N, N), dtype=int)
for y in range(14):
    A[0, 1 + y] = A[1 + y, 0] = 1
    A[1 + y, 1 + (y ^ 1)] = 1
for i, s in enumerate(S):
    for y in s:
        A[1 + y, 15 + i] = A[15 + i, 1 + y] = 1
for a, b in d["edges"]:
    A[15 + a, 15 + b] = A[15 + b, 15 + a] = 1
nm = lambda s: "".join(str(t) if t < 10 else "abcd"[t - 10] for t in sorted(s))
name = ["v"] + ["L%s" % ("0123456789abcd"[y]) for y in range(14)] + [nm(s) for s in S]
w, V = np.linalg.eigh(A.astype(float))
x = V[:, 0]
print("lambda_min(H) = %.5f" % w[0])
order = list(np.argsort(-np.abs(x)))
lmin = lambda sub: np.linalg.eigvalsh(A[np.ix_(sub, sub)].astype(float))[0]
for k in range(5, N + 1):
    sub = order[:k]
    if lmin(sub) < -4 - 1e-9:
        break
print("greedy: %d vertices give lambda_min %.5f" % (k, lmin(sub)))
# prune: remove vertices while staying below -4
sub = list(sub)
changed = True
while changed:
    changed = False
    best = None
    for v in sub:
        t = [u for u in sub if u != v]
        lv = lmin(t)
        if lv < -4 - 1e-9 and (best is None or lv < best[0]):
            best = (lv, v)
    if best:
        sub.remove(best[1]); changed = True
print("pruned: %d vertices, lambda_min %.5f" % (len(sub), lmin(sub)))
print("vertices:", sorted(name[u] for u in sub))
ww, VV = np.linalg.eigh(A[np.ix_(sub, sub)].astype(float))
y = VV[:, 0]; y = y / np.abs(y).max()
print("eigenvector:", sorted(((name[u], round(float(y[i]), 3)) for i, u in enumerate(sub)), key=lambda t: t[0]))
deg = A[np.ix_(sub, sub)].sum(1)
print("degrees inside:", sorted(zip([name[u] for u in sub], deg.tolist())))
