import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
from collections import Counter
d = json.load(open(sys.argv[1])); S = [frozenset(l) for l in d["labels"]]; n = len(S)
K = np.array([[kval(a, b) for b in S] for a in S])
tally = Counter(); srcs = Counter()
for k, s in enumerate(d["structures"]):
    G = np.zeros((n, n))
    for i, j in s["edges"]: G[i, j] = G[j, i] = 1
    ev = np.linalg.eigvalsh(3*np.eye(n) - G - K)
    irr = [x for x in ev if abs(8*x - round(8*x)) > 1e-6]
    c = Counter(np.round(irr, 5))
    key = (tuple(sorted(Counter(c.values()).items())), s.get("gens"), s.get("source", "")[:12])
    tally[(tuple(sorted(Counter(c.values()).items())))] += 1
    srcs[(s.get("gens"),)] += 1
    if k in (0, 4, 278, 288) :
        print(k, s["c"], s.get("gens"), s.get("source"), "irrational eigenvalue multiplicities:", sorted(c.items())[:30])
print("multiplicity pattern tally:", tally)
print("gens tally:", srcs)
