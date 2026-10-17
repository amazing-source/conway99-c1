import itertools, json, sys
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, gl_connected, rank_mod, build_H
from c1_h46_padic import H46, bareiss
from c1_hidden import comps_m
for line in open(sys.argv[1]):
    d = json.loads(line)
    if len(d["labels"]) != 44:
        continue
    S0 = [frozenset(x) for x in d["labels"]]
    E0 = [(frozenset(a), frozenset(b)) for a, b in d["edges"]]
    for side in (0, 1):
        L, EE = relabel(S0, E0, side)
        conn, degok = gl_connected(EE)
        if not (conn and degok):
            continue
        for x in (2, 3):
            A = H46(EE, x)
            ev = np.linalg.eigvalsh(A.astype(float))[::-1]
            if abs(ev[1] - 3) < 1e-6 or abs(ev[0] - 3) < 1e-6:
                G = np.zeros((44, 44))
                for i, j in itertools.combinations(range(44), 2):
                    if frozenset((S[i], S[j])) in EE:
                        G[i, j] = G[j, i] = 1
                K8 = np.array([[k8(a, b) for b in S] for a in S], float)
                lam = np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0]
                m3 = 46 - rank_mod((A - 3 * np.eye(46, dtype=np.int64)).tolist(), 1000000007)
                cm, _ = comps_m(EE)
                V9, A9 = build_H(EE, with_l=True)
                nu = 59 - rank_mod((A9 - 3 * np.eye(59, dtype=np.int64)).tolist(), 1000000007)
                print("%s side %d hub %d: lambda_1 %.4f lambda_2 %.6f lambda_3 %.4f mult_3(H46) %d ; lambda_min(T_S) %.4f ; c(m) %d ; nu(T_S) %d" % (
                    d.get("src"), side, x, ev[0], ev[1], ev[2], m3, lam, cm, nu))
