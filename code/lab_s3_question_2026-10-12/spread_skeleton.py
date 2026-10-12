"""Lab session, 2026-10-12. A candidate GLOBAL non-trivial parity skeleton on the Brouwer-Haemers graph, read off from the
solutions of the local problem (local_vertex.py): at a vertex P the split pairs (P, R) are those with R far from one line
through P. Globally: take a parallel class of lines (direction delta, an isotropic vector: its 27 lines are a regular
spread of BH; the hyperplanes B(x, delta) = c are three "layers" of nine lines each; two lines of different layers are
joined by a perfect matching, two lines of the same layer are not joined).
Hypothesis H(delta):
  * a pair (P, R) in the same layer, on different lines, is SPLIT, its three common neighbours in the next layer giving
    one parity and its three common neighbours in the previous layer the other parity;
  * every other non-adjacent pair is FLAT.
All these conditions, and evenness on the 270 lines, are LINEAR over F_2 in eps (810 unknowns). This script solves the
system by Gaussian elimination and reports the dimension of the solution space modulo coboundaries, and writes one
solution (810 bits, edges in the order of this file) if there is one.

python spread_skeleton.py [out file]"""
import sys, itertools

V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}; n = 81
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
Bf = lambda x, y: (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
S = [v for v in V if any(v) and q(v) == 0]
nb = [sorted(I[add(V[i], s)] for s in S) for i in range(n)]; nbs = [set(a) for a in nb]
edges = [(i, j) for i in range(n) for j in nb[i] if i < j]; eid = {e: k for k, e in enumerate(edges)}
E = lambda a, b: eid[(a, b) if a < b else (b, a)]
lines = sorted({tuple(sorted((i, j, next(iter(nbs[i] & nbs[j]))))) for (i, j) in edges})
delta = (0, 0, 0, 1); assert q(delta) == 0
layer = [Bf(V[i], delta) for i in range(n)]                  # B(x, delta) = x2
fib = [min(i, I[add(V[i], delta)], I[add(V[i], add(delta, delta))]) for i in range(n)]

rows = []                                                    # each equation: (set of edge indices, right-hand side)
def eq(es, rhs):
    s = set()
    for e in es: s ^= {e}
    rows.append((s, rhs))
for t in lines: eq([E(t[0], t[1]), E(t[1], t[2]), E(t[0], t[2])], 0)
nsplit = nflat = 0
for a in range(n):
    for b in range(a + 1, n):
        if b in nbs[a]: continue
        cn = sorted(nbs[a] & nbs[b]); paths = {z: [E(a, z), E(z, b)] for z in cn}
        if layer[a] == layer[b] and fib[a] != fib[b]:
            nsplit += 1
            up = [z for z in cn if layer[z] == (layer[a] + 1) % 3]; dn = [z for z in cn if layer[z] == (layer[a] + 2) % 3]
            assert len(up) == 3 and len(dn) == 3
            for g in (up, dn):
                for z in g[1:]: eq(paths[g[0]] + paths[z], 0)
            eq(paths[up[0]] + paths[dn[0]], 1)
        else:
            nflat += 1
            for z in cn[1:]: eq(paths[cn[0]] + paths[z], 0)
print("pairs declared split: %d, flat: %d; equations: %d" % (nsplit, nflat, len(rows)))

# Gaussian elimination over F_2 with integers as bit sets (bit 810 = right-hand side)
piv = {}; inconsistent = False
for s, rhs in rows:
    v = sum(1 << e for e in s) | (rhs << 810)
    while v & ((1 << 810) - 1):
        p = (v & ((1 << 810) - 1)).bit_length() - 1
        if p in piv: v ^= piv[p]
        else: piv[p] = v; break
    else:
        if v >> 810: inconsistent = True
rank = len(piv)
print("rank of the linear part: %d of 810; consistent: %s" % (rank, not inconsistent))
if not inconsistent:
    # one solution: free variables 0, back substitution
    sol = [0] * 810
    for p in sorted(piv):
        v = piv[p]; val = (v >> 810) & 1
        for e in range(p):
            if (v >> e) & 1: val ^= sol[e]
        sol[p] = val
    # verification on the original conditions
    for t in lines: assert (sol[E(t[0], t[1])] + sol[E(t[1], t[2])] + sol[E(t[0], t[2])]) % 2 == 0
    w3 = 0
    for a in range(n):
        for b in range(a + 1, n):
            if b in nbs[a]: continue
            w = sum((sol[E(a, z)] + sol[E(z, b)]) % 2 for z in nbs[a] & nbs[b]); assert w in (0, 3, 6); w3 += w == 3
    print("solution found and verified: a parity skeleton with %d split pairs; negative edges %d" % (w3, sum(sol)))
    print("dimension of the solution space: %d (coboundaries have dimension 80, so %d modulo switching)" % (810 - rank, 810 - rank - 80))
    if len(sys.argv) > 1: open(sys.argv[1], "w", newline="\n").write("".join(map(str, sol)) + "\n")
