"""Decode a cadical solution of the 3-ovoid CNF and report the induced graph's parameters (lambda, mu distribution).
usage: python ovoid9_check.py <gq9.json> <solution> [<out.json>]"""
import itertools, json, sys
from collections import Counter
import numpy as np
G = json.load(open(sys.argv[1])); lines = G["lines"]
val = {}
for line in open(sys.argv[2]):
    if line.startswith("v"):
        for x in line.split()[1:]:
            x = int(x)
            if x: val[abs(x)] = x > 0
O = [p for p in range(729) if val.get(p + 1)]
A = np.zeros((729, 729), dtype=np.int64)
for L in lines:
    for a, b in itertools.combinations(L, 2): A[a, b] = A[b, a] = 1
S = A[np.ix_(O, O)]; S2 = S @ S
n = len(O); iu = np.triu_indices(n, 1)
adj = S[iu] == 1
lam = Counter(S2[iu][adj].tolist()); mu = Counter(S2[iu][~adj].tolist())
print("|O| = %d, degrees %s, lambda %s, mu %s" % (n, sorted(set(S.sum(1).tolist())), dict(lam), dict(sorted(mu.items()))))
if len(sys.argv) > 3: json.dump(O, open(sys.argv[3], "w"))
