"""notes/102: sign of the 27-point edge block S = B_1(x) + B_1(y) (y a label), Q = A - 3I + 3J mod 7, per type of
tau_y (loops; cycle lengths of the class multigraph).  Extremal case rank Q_SS = 14 + k forces a non-split sign."""
import itertools
from collections import defaultdict
import numpy as np
from beta_form_check import rank_leg

p = 7
labels = list(range(14)); mate = lambda b: b ^ 1          # lines {0,1}, {2,3}, ..., y = 0, ybar = 1
y = 0; rest = [b for b in labels if b not in (0, 1)]       # 12 labels, 6 classes {2,3}..{12,13}


def matchings(L):
    if not L:
        yield []; return
    a = L[0]
    for i in range(1, len(L)):
        for m in matchings(L[1:i] + L[i + 1:]):
            yield [(a, L[i])] + m


def ctype(m):
    adj = defaultdict(list)
    for a, b in m:
        adj[a // 2].append(b // 2); adj[b // 2].append(a // 2)
    seen = set(); loops = 0; cyc = []
    for c in range(1, 7):
        if c in seen: continue
        if adj[c].count(c) == 2:
            loops += 1; seen.add(c); continue
        comp = {c}; stack = [c]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in comp: comp.add(v); stack.append(v)
        seen |= comp; cyc.append(len(comp))
    return (loops, tuple(sorted(cyc)))


# vertices: 0 = x, 1..14 = labels 0..13, 15..26 = star(y) pairs {y, b}, b in rest
res = defaultdict(set)
for m in matchings(rest):
    A = np.zeros((27, 27), dtype=np.int64)
    for b in labels:
        A[0, 1 + b] = A[1 + b, 0] = 1
        A[1 + b, 1 + mate(b)] = 1
    for i, b in enumerate(rest):
        v = 15 + i
        for u in (1 + y, 1 + b):
            A[v, u] = A[u, v] = 1
    for a, b in m:
        i, j = 15 + rest.index(a), 15 + rest.index(b)
        A[i, j] = A[j, i] = 1
    Q = (A - 3 * np.eye(27, dtype=np.int64) + 3) % p
    import line_ball as lb
    rA = lb.rank_mod((A - 3 * np.eye(27, dtype=np.int64)) % p)
    res[ctype(m)].add((rA, ) + rank_leg(Q.tolist(), p))
for t in sorted(res):
    print(t, sorted(res[t]))
