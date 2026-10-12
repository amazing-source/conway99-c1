"""Lab session, 2026-10-12. Small words of the dual of the split-pattern code C (see parity_code.py).
A set W of pairs is a dual word iff the functionals L_p (p in W) sum to zero on H^1; then the number of split pairs of W
is even in every parity skeleton. If |W| is odd, W contains a flat pair.
This script reads the functionals (rho460.txt of quad_setup.py: L_p = sum of the five rho_i) and finds ALL dual words of
weight 2, 3, 4, and all those of weight 5 containing the first pair (Aut(BH) is transitive on the pairs).
python dual_small.py <rho file>"""
import sys, itertools, collections
from local_lib import *
Lp = {}
for line in open(sys.argv[1]):
    t = line.split(); a, b = int(t[0]), int(t[1]); v = 0
    for h in t[2:]: v ^= int(h, 16)
    Lp[(a, b)] = v
pairs = sorted(Lp); vals = [Lp[p] for p in pairs]; N = len(pairs)
print("%d pairs; zero functionals: %d; distinct functionals: %d" % (N, sum(1 for v in vals if v == 0), len(set(vals))))
index = collections.defaultdict(list)
for i, v in enumerate(vals): index[v].append(i)
w2 = [(i, j) for v, l in index.items() for i, j in itertools.combinations(l, 2)]
print("dual words of weight 2: %d" % len(w2))
w3 = 0; ex3 = None
sums2 = collections.defaultdict(list)
for i in range(N):
    vi = vals[i]
    for j in range(i + 1, N):
        s = vi ^ vals[j]
        if s in index:
            for k in index[s]:
                if k > j: w3 += 1; ex3 = ex3 or (i, j, k)
        sums2[s].append((i, j))
print("dual words of weight 3: %d%s" % (w3, "" if not ex3 else "; example %s" % [ (V[pairs[t][0]], V[pairs[t][1]]) for t in ex3]))
w4 = 0; ex4 = None
for s, l in sums2.items():
    if len(l) > 1:
        for (a, b), (c, d) in itertools.combinations(l, 2):
            if len({a, b, c, d}) == 4: w4 += 1; ex4 = ex4 or (a, b, c, d)
w4 //= 3
print("dual words of weight 4: %d%s" % (w4, "" if not ex4 else "; example %s" % [(V[pairs[t][0]], V[pairs[t][1]]) for t in ex4]))
# weight 5 through the first pair: L_0 + L_a + L_b = L_c + L_d
w5 = 0; ex5 = None; v0 = vals[0]
for a in range(1, N):
    va = v0 ^ vals[a]
    for b in range(a + 1, N):
        s = va ^ vals[b]
        if s in sums2:
            for (c, d) in sums2[s]:
                if len({0, a, b, c, d}) == 5: w5 += 1; ex5 = ex5 or (0, a, b, c, d)
print("dual words of weight 5 through the first pair (each counted 6 times): %d%s" % (w5, "" if not ex5 else "; example %s" % [(V[pairs[t][0]], V[pairs[t][1]]) for t in ex5]))
