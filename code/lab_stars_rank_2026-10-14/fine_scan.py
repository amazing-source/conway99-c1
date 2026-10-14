"""Fine-space spectrum of Gamma for many saved four-star structures, grouped by (c(l), c(m)) (14/10/2026).
For F = ker D_S (labels of S with zero sum on every letter), T and U >= 0 force spec(Gamma_F) in [-4, 3].
usage: python fine_scan.py <json files with labels and edges (and optionally c)> ..."""
import json
import sys
from collections import defaultdict
import numpy as np
from stars_rank import kval

rows = defaultdict(list)
for f in sys.argv[1:]:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if "edges" not in d:
        continue
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    G = np.zeros((n, n))
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    Dm = np.array([[1.0 if y in l else 0.0 for l in S] for y in range(14)])
    U_, s_, Vt = np.linalg.svd(Dm)
    F = Vt[int(np.sum(s_ > 1e-9)):].T
    ev = np.linalg.eigvalsh(F.T @ G @ F)
    T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
    X = [i for i in range(n) if S[i] & {0, 1}]
    Xm = [i for i in range(n) if S[i] & {2, 3}]
    cl = 23 - np.linalg.matrix_rank(8 * T[np.ix_(X, X)], tol=1e-6)
    cm = 23 - np.linalg.matrix_rank(8 * T[np.ix_(Xm, Xm)], tol=1e-6)
    rows[(min(cl, cm), max(cl, cm))].append((ev[0], ev[-1], f))
for key in sorted(rows):
    r = rows[key]
    lo = min(x[0] for x in r)
    hi = max(x[1] for x in r)
    ok = sum(1 for x in r if x[0] >= -4 - 1e-9 and x[1] <= 3 + 1e-9)
    print("c = %s: %d structures, Gamma_F spectrum within [-4,3] for %d; overall range [%.3f, %.3f]; "
          "best max %.4f, best min %.4f" % (key, len(r), ok, lo, hi, min(x[1] for x in r), max(x[0] for x in r)))
