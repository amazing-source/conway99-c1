"""rank_3(A_Omega) and mult_3 over Q on cache c(l) = 1 sides with NO rectangle having exactly 3 internal edges
(at the 6 l-rectangles and the 6 m-rectangles), positive or not."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, build_H, gl_connected
from c1_hidden import comps_m

def e3_free(EE):
    for (r0, r1) in ((0, 1), (2, 3)):
        for j in range(7):
            if 2 * j in (r0, r1):
                continue
            Q = [frozenset((r, s)) for r in (r0, r1) for s in (2 * j, 2 * j + 1)]
            if sum(1 for a, b in itertools.combinations(Q, 2) if frozenset((a, b)) in EE) == 3:
                return False
    return True

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
            if not (conn and degok) or not e3_free(EE):
                continue
            G = np.zeros((44, 44))
            for i, j in itertools.combinations(range(44), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], float)
            psd = np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0] > -1e-9
            V9, A9 = build_H(EE, with_l=True)
            r3 = rank_mod(A9.tolist(), 3)
            nu = 59 - rank_mod((A9 - 3 * np.eye(59, dtype=np.int64)).tolist(), 1000000007)
            cm, _ = comps_m(EE)
            tab[(bool(psd), cm, r3, nu)] += 1
    print("E3-free c(l)=1 sides of the cache: (positive, c(m), rank_3(A_Omega) [Conway <= 45], mult_3 over Q [Conway >= 14]) : count")
    for k, v in sorted(tab.items()):
        print("   ", k, v)


if __name__ == '__main__':
    main()
