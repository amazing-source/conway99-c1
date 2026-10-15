import json, sys, glob
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval
res = []
for f in glob.glob(sys.argv[1]):
    d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = len(S)
    G = np.zeros((n, n))
    for i, j in d["edges"]: G[i, j] = G[j, i] = 1
    T = 3*np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    ev = np.sort(np.abs(np.linalg.eigvalsh(T)))
    res.append((ev[13], f, d.get("masym", d.get("hasym")), ev[12]))
res.sort()
for r in res[:8]: print("14th smallest |ev| %.5f  (13th %.2e)  %s  asym %s" % (r[0], r[3], r[1], r[2]))
print(len(res), "files")
