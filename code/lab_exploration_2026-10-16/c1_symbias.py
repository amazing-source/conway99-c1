"""mult_3(A_H56) and rank_3(A_Omega) versus the (01) and (23) symmetry of the block (data bias check)."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, k8, rank_mod, relabel, build_H, gl_connected

def swapped(EE, a, b):
    f = lambda l: frozenset(b if x == a else a if x == b else x for x in l)
    return set(frozenset((f(x), f(y))) for x, y in (tuple(e) for e in EE))

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
            s01 = swapped(EE, 0, 1) == EE
            s23 = swapped(EE, 2, 3) == EE
            V, A = build_H(EE)
            m56 = len(V) - rank_mod((A - 3 * np.eye(len(V), dtype=np.int64)).tolist(), 1000000007)
            V9, A9 = build_H(EE, with_l=True)
            r3 = rank_mod(A9.tolist(), 3)
            tab[(s01, s23, m56, r3)] += 1
            done += 1
            if done >= mx:
                break
        if done >= mx:
            break
    print("sides:", done)
    print("((01)-sym, (23)-sym, mult_3(A_H56) [Conway >= 11], rank_3(A_Omega) [Conway <= 45]) : count")
    for k, v in sorted(tab.items()):
        print("   ", k, v)

main()
