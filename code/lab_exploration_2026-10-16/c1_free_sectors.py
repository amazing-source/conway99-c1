"""For lemma-free c(l)=1 sides with hidden > 0: odd/even sector decomposition of ker T_S (exact ranks mod a big prime).
W_odd = R^{X_l} + span(f_s = 1_{2s} - 1_{3s}) (34 dims, known kernel z0, z1, z2 - z3): delta = dim(ker cap W_odd) - 3.
W_even = R^{X_l} + span(g_s = 1_{2s} + 1_{3s}) (34 dims, known kernel z0, z1, z2 + z3): eps = dim(ker cap W_even) - 3."""
import itertools, json, sys
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, rank_mod, relabel, gl_connected
from c1_hidden import comps_m
P = 1000000007
want = {(a, b) for a, b, *_ in json.load(open(sys.argv[2]))}
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    for side in (0, 1):
        if (d.get("src"), side) not in want:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
        L, EE = relabel(S0, E0, side)
        n = 44
        G = np.zeros((n, n), dtype=np.int64)
        for i, j in itertools.combinations(range(n), 2):
            if frozenset((S[i], S[j])) in EE:
                G[i, j] = G[j, i] = 1
        K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
        T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        nu = n - rank_mod(T8.tolist(), P)
        out = []
        for sgn in (-1, 1):
            Pm = np.zeros((n, 34), dtype=np.int64)
            for a, l in enumerate(XL):
                Pm[S.index(l), a] = 1
            for k, s in enumerate(range(4, 14)):
                Pm[S.index(frozenset((2, s))), 24 + k] = 1
                Pm[S.index(frozenset((3, s))), 24 + k] = sgn
            M = (Pm.T @ T8 @ Pm)
            out.append(34 - rank_mod(M.tolist(), P) - 3)
        cm, _ = comps_m(EE)
        print("%-28s side %d: nu %d  c(m) %d  hidden %d  | odd-window delta %d  even-window eps %d" % (
            d.get("src")[:28], side, nu, cm, nu - 3 - cm, out[0], out[1]))
