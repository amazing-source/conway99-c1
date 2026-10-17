"""p-adic profile of det(3I - A_H) for H46 = N(l) u Y_x (x = 2 and x = 3), on all c(l) = 1 cache sides.
Conway: det = 0 (lambda_2 = 3).  Exact integer determinant by Bareiss."""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from c1_margin56 import S, XL, Y, k8, relabel, gl_connected

def bareiss(M):
    A = [list(map(int, r)) for r in M]
    n = len(A); sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]

def v(nm, p):
    if nm == 0:
        return 99
    c = 0
    while nm % p == 0:
        nm //= p; c += 1
    return c

def H46(EE, x):
    Yx = [l for l in Y if x in l]
    Vt = [("L", a) for a in range(2, 14)] + XL + Yx
    pos = {t: i for i, t in enumerate(Vt)}
    n = len(Vt)
    A = np.zeros((n, n), dtype=np.int64)
    def e(a, b):
        A[pos[a], pos[b]] = A[pos[b], pos[a]] = 1
    for a in range(2, 14, 2):
        e(("L", a), ("L", a + 1))
    for w in XL + Yx:
        for a in w:
            if a >= 2:
                e(("L", a), w)
    for a, b in itertools.combinations(XL + Yx, 2):
        if frozenset((a, b)) in EE:
            e(a, b)
    return A

def main():
    tab = Counter(); dmod = Counter()
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
            for x in (2, 3):
                A = H46(EE, x)
                D = bareiss((3 * np.eye(46, dtype=np.int64) - A).tolist())
                tab[(v(D, 2), v(D, 3), v(D, 5), D < 0)] += 1
                if D:
                    core = D
                    for p in (2, 3, 5):
                        while core % p == 0:
                            core //= p
                    dmod[(abs(core) % 3, abs(core) % 7 == 0, abs(core) % 11 == 0)] += 1
            done += 1
        if done >= int(sys.argv[2]):
            break
    print("c=1 sides:", done, " (two hubs each)")
    print("(v2, v3, v5 of det(3I - A_H46), det < 0) : count    [Conway: det = 0]")
    for k, c in sorted(tab.items()):
        print("   ", k, c)
    print("(core mod 3, 7 | core, 11 | core):", dict(sorted(dmod.items())))

if __name__ == '__main__':
    main()
