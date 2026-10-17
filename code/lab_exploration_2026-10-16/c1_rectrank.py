"""Rank of F (Schur of T_S onto the far labels Y of l) restricted to unions of m-rectangles, exact (mod a large prime of
the integer matrix 8T on X_l u U, minus the 22 = rank of the X_l block, since nu(T_{X_l u U}) = 2 + dim ker F_U).
Also: is the 2x2 quotient by rectangles informative?  For each rectangle R_j: rank F_{R_j} (4x4), and the increments."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, k8, rank_mod, relabel, gl_connected

P = 1000000007
def main():
    mx = int(sys.argv[2])
    single, pair, inc = Counter(), Counter(), Counter()
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
            rX = rank_mod(T8[np.ix_(ixl, ixl)].tolist(), P)
            rect = {j: [S.index(frozenset((a, s))) for a in (2, 3) for s in (2 * j, 2 * j + 1)] for j in range(2, 7)}
            def rF(U):
                ids = ixl + [i for j in U for i in rect[j]]
                return rank_mod(T8[np.ix_(ids, ids)].tolist(), P) - rX
            r1 = {j: rF((j,)) for j in range(2, 7)}
            for j in r1:
                single[r1[j]] += 1
            for i, j in itertools.combinations(range(2, 7), 2):
                r2 = rF((i, j))
                pair[(r2, r1[i] + r1[j] - r2)] += 1
            # greedy increments in the order 2..6
            prev = 0
            for k in range(1, 6):
                cur = rF(tuple(range(2, 2 + k)))
                inc[(k, cur - prev)] += 1
                prev = cur
            done += 1
            if done >= mx:
                break
        if done >= mx:
            break
    print("positive c=1 sides:", done, " (rank of the X_l block mod p is 22 = 24 - 2 when c(l) = 1)")
    print("rank F on ONE m-rectangle (4 labels):", dict(sorted(single.items())))
    print("rank F on TWO m-rectangles (8 labels), and overlap r(i)+r(j)-r(ij):", dict(sorted(pair.items())))
    print("increments of rank F adding the m-rectangles of lines 2,3,4,5,6 in turn (k, increment):", dict(sorted(inc.items())))
    print("Conway: rank F on ANY union of m-rectangles <= 8")

main()
