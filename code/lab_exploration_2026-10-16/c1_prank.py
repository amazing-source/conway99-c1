"""p-ranks of induced subgraphs on positive c(l) = 1 sides.  Conway: rank_p(A - 3I) = 45 for p = 2, 3, 5 (p-rank theory:
p does not divide r - s = 7, and does not divide k - r = 11, so rank_p(A - rI) = g + 1 = 45), hence EVERY induced
subgraph H has rank_p(A_H - 3I) <= 45.  H56 = N(l) u Y, H59 = l u N(l) u Y.  Q-rank for comparison."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, build_H, gl_connected

def main():
    mx = int(sys.argv[2])
    tab = Counter()
    done = 0
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
            G = np.zeros((44, 44))
            for i, j in itertools.combinations(range(44), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], float)
            if np.linalg.eigvalsh((24 * np.eye(44) - 8 * G - K8) / 8)[0] < -1e-9:
                continue
            row = []
            for wl in (False, True):
                V, A = build_H(EE, with_l=wl)
                M = (A - 3 * np.eye(len(V), dtype=np.int64)).tolist()
                rq = rank_mod(M, 1000000007)
                row += [len(V), rq, rank_mod(M, 2), rank_mod(M, 3), rank_mod(M, 5)]
            tab[tuple(row)] += 1
            done += 1
            if done >= mx:
                break
        if done >= mx:
            break
    print("sides:", done, "   Conway: every p-rank of A_H - 3I is <= 45")
    print("(|H|, rank_Q, rank_2, rank_3, rank_5) for H56 and H59 : count")
    for k, v in sorted(tab.items()):
        print("   H56", k[:5], " H59", k[5:], ":", v)

main()
