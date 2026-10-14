"""Positive and negative control of the encoder srg_sat.encode on a real graph with lambda = 1, mu = 2:
the graph on 243 vertices (coset graph of the ternary Golay code): vertices F_3^5, x ~ y iff x - y = +-h_i for
one of the 11 columns h_i of a parity-check matrix. The script first verifies that the graph it built is
srg(243,22,1,2) by direct counting; then
  good: all adjacencies fixed to their true values except NFREE random pairs left free  -> must be SAT;
  bad : the same with one fixed adjacency flipped                                         -> must be UNSAT.
usage: python control_243.py good.cnf bad.cnf nfree seed
"""
import itertools
import random
import sys

import srg_sat as S

A6x5 = [(1, 1, 1, 1, 1), (0, 1, 2, 2, 1), (1, 0, 1, 2, 2), (2, 1, 0, 1, 2), (2, 2, 1, 0, 1), (1, 2, 2, 1, 0)]
cols = [tuple((-a) % 3 for a in row) for row in A6x5]            # columns of -A^T are the negated rows of A
cols += [tuple(1 if i == j else 0 for i in range(5)) for j in range(5)]
conn = set()
for h in cols:
    conn.add(h)
    conn.add(tuple((-c) % 3 for c in h))
assert len(conn) == 22
verts = list(itertools.product(range(3), repeat=5))
index = {v: i for i, v in enumerate(verts)}
n = len(verts)
adj = [[False] * n for _ in range(n)]
for v in verts:
    for h in conn:
        w = tuple((a + b) % 3 for a, b in zip(v, h))
        adj[index[v]][index[w]] = True
# direct verification of the parameters
nb = [set(j for j in range(n) if adj[i][j]) for i in range(n)]
assert all(len(s) == 22 for s in nb)
for i in range(n):
    for j in range(i + 1, n):
        c = len(nb[i] & nb[j])
        assert c == (1 if adj[i][j] else 2), (i, j, c)
print("graph verified: srg(243,22,1,2)", flush=True)

good, bad, nfree, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
free = set(rng.sample(pairs, nfree))
fixed = {p: adj[p[0]][p[1]] for p in pairs if p not in free}
enc, e = S.encode(n, 22, 1, 2, fixed)
S.write_dimacs(enc, good)
print("good instance: free pairs %d, variables %d, clauses %d" % (nfree, enc.nv, len(enc.clauses)), flush=True)
flip = rng.choice([p for p in pairs if p not in free])
fixed[flip] = not fixed[flip]
enc, e = S.encode(n, 22, 1, 2, fixed)
S.write_dimacs(enc, bad)
print("bad instance: one adjacency flipped at", flip, "clauses", len(enc.clauses), flush=True)
