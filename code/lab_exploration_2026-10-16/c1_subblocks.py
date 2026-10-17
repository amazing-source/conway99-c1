"""Margin on sub-blocks.  B_U = X_l u (union of the m-rectangles Q_1j, j in U), |U| = k, 24 + 4k labels.
Conway: nu(T_{B_U}) >= 24 + 4k - 30 = 4k - 6 (interlacing).  Known kernel inside B_U: z_0, z_1 (stars of l).
So Conway needs hidden(B_U) := nu - 2 >= 4k - 8  (k = 3: 4, k = 4: 8, k = 5: 12 incl. the 2 trivial 1_Y2, 1_Y3).
margin(B_U) = (4k - 6) - nu.  Monotone: margin can only grow with k.  We print the data distribution."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, k8, rank_mod, relabel, gl_connected

P = 1000000007
def main():
    mx = int(sys.argv[2])
    tab = {k: Counter() for k in (2, 3, 4, 5)}
    worst = {k: 99 for k in (2, 3, 4, 5)}
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
            n = 44
            G = np.zeros((n, n), dtype=np.int64)
            for i, j in itertools.combinations(range(n), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.array([[k8(a, b) for b in S] for a in S], dtype=np.int64)
            T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
            if np.linalg.eigvalsh(T8 / 8.0)[0] < -1e-9:
                continue
            ixl = [S.index(l) for l in XL]
            rect = {j: [S.index(frozenset((a, s))) for a in (2, 3) for s in (2 * j, 2 * j + 1)] for j in range(2, 7)}
            for k in (2, 3, 4, 5):
                for U in itertools.combinations(range(2, 7), k):
                    ids = ixl + [i for j in U for i in rect[j]]
                    nu = len(ids) - rank_mod(T8[np.ix_(ids, ids)].tolist(), P)
                    m = (4 * k - 6) - nu
                    tab[k][m] += 1
                    worst[k] = min(worst[k], m)
            done += 1
            if done >= mx:
                break
        if done >= mx:
            break
    print("positive c=1 sides:", done)
    for k in (2, 3, 4, 5):
        print("k = %d rectangles of m (%d labels): Conway nu >= %d; margin (Conway - data) histogram %s; worst %d" % (
            k, 24 + 4 * k, 4 * k - 6, dict(sorted(tab[k].items())), worst[k]))

main()
