"""Independent check of the parity step of the Z_3 theorem (no BvLS, no kissat).
BH is built as VO^-(4,3): vertices F_3^4, x ~ y iff q(x-y) = 0, q = x1^2 + x2^2 + x3*x4 (elliptic).
Claim: no Z_2-cochain eps on the edges of BH, even on every triangle, makes some non-adjacent pair 3/3
(three of its six 2-paths odd) while every non-adjacent pair is 6/0 or 3/3.
WLOG (rank 3 + gauge): pair (0, R0) is 3/3, eps vanishes on a BFS tree rooted at 0, and the odd-path pattern at
(0,R0) is one representative per orbit of the pair stabiliser on 3-subsets of the common neighbours modulo
complement.  Each case must be INFEASIBLE.  Positive control: drop the condition on all other pairs -> FEASIBLE."""
import itertools, collections, sys, numpy as np
from ortools.sat.python import cp_model
sys.path.insert(0, ".")
from lib243 import aut, is_srg

V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
n = 81
Q = np.zeros((n, n), dtype=np.int64)
for a in V:
    for b in V:
        d = tuple((u - w) % 3 for u, w in zip(a, b))
        if a != b and q(d) == 0: Q[I[a], I[b]] = 1
assert is_srg(Q, k=20, lam=1, mu=6), "not BH"
nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
R0 = min(R for R in range(1, n) if not Q[0, R])
CN = sorted(nb[0] & nb[R0])
# orbits of the stabiliser of (0,R0) on 3-subsets of CN modulo complement
o, orb, gens = aut(Q, partition=[[0], [R0], [x for x in range(n) if x not in (0, R0)]])
canon = lambda S: min(frozenset(S), frozenset(set(CN) - set(S)), key=sorted)
classes, seen = [], set()
for S in itertools.combinations(CN, 3):
    k = canon(S)
    if k in seen: continue
    orbit, stack = set(), [k]
    while stack:
        T = stack.pop()
        if T in orbit: continue
        orbit.add(T)
        for g in gens: stack.append(canon([g[x] for x in T]))
    seen |= orbit; classes.append(sorted(min(orbit, key=sorted)))
# under the tree gauge, the path through the BFS parent of R0 is always even: pick, in each class, the
# representative (pattern or complement) that makes it even.
_t, _s, _dq = [], {0}, collections.deque([0])
while _dq:
    u = _dq.popleft()
    for v in sorted(nb[u]):
        if v not in _s: _s.add(v); _dq.append(v); _t.append((u, v))
parent = [u for u, v in _t if v == R0][0]
classes = [c if parent not in c else sorted(set(CN) - set(c)) for c in classes]
print(f"BH = VO^-(4,3) ok; |Stab(0,R0)| = {o}; parent(R0) = {parent}; pattern classes: {classes}")

def model(pattern, all_pairs=True):
    m = cp_model.CpModel(); eps = {}
    for P in range(n):
        for R in nb[P]:
            if P < R: eps[(P, R)] = eps[(R, P)] = m.NewBoolVar("")
    tree, seen_, dq = [], {0}, collections.deque([0])
    while dq:
        u = dq.popleft()
        for v in sorted(nb[u]):
            if v not in seen_: seen_.add(v); dq.append(v); tree.append((u, v))
    for u, v in tree: m.Add(eps[(u, v)] == 0)
    for P in range(n):
        for R in nb[P]:
            for S in nb[P] & nb[R]:
                if P < R < S: m.AddBoolXOr([eps[(P, R)], eps[(R, S)], eps[(P, S)], True])
    for P in range(n):
        for R in range(P + 1, n):
            if Q[P, R]: continue
            if not all_pairs and (P, R) != (0, R0): continue
            pp = []
            for Z in sorted(nb[P] & nb[R]):
                b = m.NewBoolVar(""); m.AddBoolXOr([eps[(P, Z)], eps[(Z, R)], b.Not()]); pp.append((Z, b))
            if (P, R) == (0, R0):
                for Z, b in pp: m.Add(b == (1 if Z in pattern else 0))
            else:
                k = m.NewIntVar(0, 2, ""); m.Add(sum(b for _, b in pp) == 3 * k)
    return m

for pat in classes:
    for full in (True, False):
        s = cp_model.CpSolver(); s.parameters.num_workers = 2; s.parameters.max_time_in_seconds = 3600
        r = s.Solve(model(pat, full))
        print(f"pattern {pat} {'all pairs constrained' if full else 'control (other pairs free)'}: {s.StatusName(r)}",
              flush=True)
