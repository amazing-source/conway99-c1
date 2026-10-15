import json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
from collections import Counter
d = json.load(open(sys.argv[1])); S = [frozenset(l) for l in d["labels"]]; n = len(S)
K = np.array([[kval(a, b) for b in S] for a in S])
picks = [int(x) for x in sys.argv[2].split(",")]
for k in picks:
    s = d["structures"][k]
    G = np.zeros((n, n))
    for i, j in s["edges"]: G[i, j] = G[j, i] = 1
    T = 3*np.eye(n) - G - K
    ev = np.linalg.eigvalsh(T)
    r = np.round(ev, 6)
    c = Counter(r)
    rat = {x: m for x, m in c.items() if abs(8*x - round(8*x)) < 1e-5}
    print(k, s["c"], "rational(1/8) eigenvalues of T:", sorted(rat.items()), "| others:", len(ev) - sum(rat.values()))
