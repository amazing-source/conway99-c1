"""Decode a cadical solution of rooted_pq.py into a graph and check it (srg identity, exact).
usage: python rooted_decode.py <cnf> <solution> <out.edges>"""
import json, sys, itertools
import numpy as np
meta = json.load(open(sys.argv[1] + ".meta.json")); v, k, mu, n = meta["v"], meta["k"], meta["mu"], meta["n"]
val = {}
for line in open(sys.argv[2]):
    if line.startswith("v"):
        for x in line.split()[1:]:
            x = int(x)
            if x: val[abs(x)] = x > 0
A = np.zeros((v, v), dtype=np.int64)
for i in range(k):
    A[0, i + 1] = A[i + 1, 0] = 1
for i in range(0, k, 2):
    A[i + 1, i + 2] = A[i + 2, i + 1] = 1
for i in range(k):
    for o in range(n):
        if val.get(meta["a"][i][o]): A[i + 1, k + 1 + o] = A[k + 1 + o, i + 1] = 1
for key, var in meta["e"].items():
    o, p = map(int, key.split(","))
    if val.get(var): A[k + 1 + o, k + 1 + p] = A[k + 1 + p, k + 1 + o] = 1
I = np.eye(v, dtype=np.int64); J = np.ones((v, v), dtype=np.int64)
ok = np.array_equal(A @ A, k * I + 1 * A + mu * (J - I - A))
print("decoded graph on %d vertices: degrees %s; srg(%d,%d,1,%d) identity: %s" % (v, sorted(set(A.sum(1).tolist())), v, k, mu, ok))
with open(sys.argv[3], "w") as fh:
    for a in range(v):
        for b in range(a + 1, v):
            if A[a, b]: fh.write("%d %d\n" % (a, b))
