import itertools, json, sys, glob, os
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, k8, rank_mod, gl_connected
from c1_decouple import Pm
P = 1000000007
for fn in sorted(glob.glob(os.path.join(sys.argv[1], "rank3walk_best_*.json")) + glob.glob(os.path.join(sys.argv[1], "hardwalk_best_seed*.json"))):
    d = json.load(open(fn))
    lab = [frozenset(x) for x in d["labels"]]
    EE = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
    conn, degok = gl_connected(EE)
    G = np.zeros((44, 44), dtype=np.int64)
    for i, j in itertools.combinations(range(44), 2):
        if frozenset((S[i], S[j])) in EE:
            G[i, j] = G[j, i] = 1
    K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
    T8 = 24 * np.eye(44, dtype=np.int64) - 8 * G - K8
    nu = 44 - rank_mod(T8.tolist(), P)
    dlt = 34 - rank_mod((Pm[-1].T @ T8 @ Pm[-1]).tolist(), P) - 3
    eps = 34 - rank_mod((Pm[1].T @ T8 @ Pm[1]).tolist(), P) - 3
    print("%-34s c(l)=1 %s  nu %2d  delta %d  eps %d  mixed %d   lam_min %.3f" % (
        os.path.basename(fn), conn, nu, dlt, eps, nu - 4 - dlt - eps, np.linalg.eigvalsh(T8 / 8.0)[0]))
