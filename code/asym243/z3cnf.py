"""General Z_3-covers of BH as CNF (kissat), relative to the BvLS voltage.
delta(e) in Z_3 on every oriented edge (one-hot), sum 0 on each line-triangle, gauge 0 on a BFS tree;
for each non-adjacent pair the 6 path values base + delta1 + delta2 take each value exactly twice.
Optional: random unit 'nudges' (assume some delta != 0) to sample different solutions.
Usage: python3 z3cnf.py OUT.cnf [seed nudges]"""
import sys, itertools, collections, random, numpy as np
from cover import *
from lines_model import PTS, IDX, add, HS
A = load_edges("bvls243.edges"); fib = fibres_of(A, 0); ok, Q = is_cover(A, fib)
n = 81; nb = [set(np.nonzero(Q[P])[0].tolist()) for P in range(n)]
hd = HS[0]
fpts = [[IDX[add(PTS[f[0]], hd, t)] for t in range(3)] for f in fib]
fcoord = {fpts[i][t]: t for i in range(n) for t in range(3)}
def bvls_volt(P, R):
    q = [x for x in fpts[R] if A[fpts[P][0], x]][0]; return fcoord[q]
nv = 0; cls = []
def new():
    global nv; nv += 1; return nv
X = {}
for P in range(n):
    for R in nb[P]:
        if P < R:
            X[(P, R)] = [new() for _ in range(3)]
            cls.append(X[(P, R)][:]); cls += [[-a, -b] for a, b in itertools.combinations(X[(P, R)], 2)]
def lit(P, R, val):
    """literal for delta(P->R) == val"""
    return X[(P, R)][val % 3] if P < R else X[(R, P)][(-val) % 3]
tree, seen, dq = [], {0}, collections.deque([0])
while dq:
    u = dq.popleft()
    for v in sorted(nb[u]):
        if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
for u, v in tree: cls.append([lit(u, v, 0)])
for P in range(n):
    for R in nb[P]:
        for S in nb[P] & nb[R]:
            if P < R < S:
                for a in range(3):
                    for b in range(3):
                        c = (-a - b) % 3          # delta(P->R)+delta(R->S)+delta(S->P) = 0
                        cls.append([-lit(P, R, a), -lit(R, S, b), lit(S, P, c)])
for P in range(n):
    for R in range(P + 1, n):
        if Q[P, R]: continue
        vals = []
        for Z in sorted(nb[P] & nb[R]):
            base = (bvls_volt(P, Z) + bvls_volt(Z, R)) % 3
            y = [new() for _ in range(3)]
            for a in range(3):
                for b in range(3):
                    cls.append([-lit(P, Z, a), -lit(Z, R, b), y[(base + a + b) % 3]])
            cls.append(y[:]); cls += [[-p, -q_] for p, q_ in itertools.combinations(y, 2)]
            vals.append(y)
        for v in range(3):
            col = [y[v] for y in vals]
            cls += [[-a, -b, -c] for a, b, c in itertools.combinations(col, 3)]      # at most 2
            cls += [list(c) for c in itertools.combinations(col, 5)]                  # at least 2
if len(sys.argv) > 3:
    rnd = random.Random(int(sys.argv[2]))
    free = [e for e in X if (min(e), max(e)) not in {(min(u, v), max(u, v)) for u, v in tree}]
    for e in rnd.sample(free, int(sys.argv[3])):
        cls.append([-X[e][0]])        # nudge: this edge's voltage differs from BvLS
with open(sys.argv[1], "w") as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
import pickle
pickle.dump({"X": X, "fpts": fpts, "base": {e: bvls_volt(*e) for e in X}}, open(sys.argv[1] + ".map", "wb"))
print("vars", nv, "clauses", len(cls))
