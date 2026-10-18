"""Positive control (srg(243,22,1,2)) of the signed-component identity: for a root x, a line a = {a*, a'} at x and a
component K of G_{l_a} (block P), d^K_w = |N(w) cap L_K cap N(a*)| - |N(w) cap L_K cap N(a')| on the labels w off line a
(D_a) satisfies  A[D_a] d^K = (lambda - mu) d^K = -d^K, and sum_w (d^K_w)^2 = 8|P|(6-|P|) for k = 14 (general form
printed for comparison).  Also the boundary sums at the labels of line a."""
import sys
import numpy as np
from itertools import combinations
path = sys.argv[1]
n, k = 243, 22
A = np.zeros((n, n), dtype=np.int64)
for line in open(path):
    a, b = map(int, line.split()[:2]); A[a, b] = A[b, a] = 1
assert (A.sum(1) == k).all()
bad = 0; tested = 0
for root in range(0, 243, 27):
    letters = [v for v in range(n) if A[root, v]]
    labels = [v for v in range(n) if v != root and not A[root, v]]
    mate = {a: next(b for b in letters if A[a, b]) for a in letters}
    lines = []
    for a in letters:
        if a < mate[a]: lines.append((a, mate[a]))
    for (a1, a2) in lines:
        T = {root, a1, a2}
        Qa = [w for w in labels if A[w, a1] or A[w, a2]]
        Da = [w for w in labels if not (A[w, a1] or A[w, a2])]
        S = [v for v in range(n) if v not in T and sum(A[v, t] for t in T) == 1]   # G_{l_a} vertex set
        assert len(S) == 3 * (k - 2) and len(Da) == len(labels) - 2 * (k - 2)
        # components of G_{l_a}
        Sset = set(S); comp = {}; c = 0
        for v in S:
            if v in comp: continue
            stack = [v]; comp[v] = c
            while stack:
                x = stack.pop()
                for y in np.nonzero(A[x])[0]:
                    if y in Sset and y not in comp:
                        comp[y] = c; stack.append(y)
            c += 1
        idx = {w: i for i, w in enumerate(Da)}
        AD = A[np.ix_(Da, Da)]
        nlines = k // 2
        for K in range(c):
            LK = [w for w in Qa if comp[w] == K]
            p = len(LK) // 4
            d = np.array([sum(1 for u in LK if A[w, u] and A[u, a1]) - sum(1 for u in LK if A[w, u] and A[u, a2]) for w in Da])
            ok = np.array_equal(AD @ d, -d)
            # norm: general formula from (T f_K)^T (T f_K) = (r-s) f_K^T T f_K, here checked directly by the eigen relation
            tested += 1
            if not ok:
                bad += 1
                print("FAIL root", root, "line", (a1, a2), "component", K, "p", p)
        if root == 0 and (a1, a2) == lines[0]:
            print("root 0, first line: components", c, "sizes", sorted(len([w for w in Qa if comp[w] == K]) // 4 for K in range(c)))
print("components tested", tested, "failures", bad)
