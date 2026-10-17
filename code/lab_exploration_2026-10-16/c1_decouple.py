"""Is ker T_S = (ker cap W_odd) + (ker cap W_even) on all c(l)=1 sides?  i.e. nu = 4 + delta + eps (mixed = 0)."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, k8, rank_mod, relabel, gl_connected
P = 1000000007
Pm = {}
for sgn in (-1, 1):
    M = np.zeros((44, 34), dtype=np.int64)
    for a, l in enumerate(XL):
        M[S.index(l), a] = 1
    for k, s in enumerate(range(4, 14)):
        M[S.index(frozenset((2, s))), 24 + k] = 1
        M[S.index(frozenset((3, s))), 24 + k] = sgn
    Pm[sgn] = M
def main():
    tab = Counter()
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
            G = np.zeros((44, 44), dtype=np.int64)
            for i, j in itertools.combinations(range(44), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
            T8 = 24 * np.eye(44, dtype=np.int64) - 8 * G - K8
            psd = bool(np.linalg.eigvalsh(T8 / 8.0)[0] > -1e-9)
            nu = 44 - rank_mod(T8.tolist(), P)
            dlt = 34 - rank_mod((Pm[-1].T @ T8 @ Pm[-1]).tolist(), P) - 3
            eps = 34 - rank_mod((Pm[1].T @ T8 @ Pm[1]).tolist(), P) - 3
            tab[(psd, nu - 4 - dlt - eps)] += 1
    print("(positive, mixed = nu - 4 - delta - eps) : count")
    for k, v in sorted(tab.items()):
        print("   ", k, v)


if __name__ == '__main__':
    main()
