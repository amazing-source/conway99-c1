"""Two full-pivot sib blocks c, d: on D = star(d) - star(c) (10 orbits indexed by the 10 labels R of the other 5 blocks),
T = 0, so Z^(c)|_D = -K r K^T must have rank <= 2 mod 7 (notes/131).  With Sigma = cross block T_{(c,w),(d,y)}
(each row/column: two +1, two -1), Rm = Sigma + 2(I - P_pi), M_D = I - J + 2P_pi + Rm^T (5I + 4P_pi) Rm (mod 7).
Random search over Sigma: distribution of rank_7(M_D) and of rank_7 of its symmetric counterpart (Sigma^T)."""
import random
import numpy as np
from collections import Counter
P = 7
n = 10
Ppi = np.zeros((n, n), int)
for i in range(n):
    Ppi[i, i ^ 1] = 1
I = np.eye(n, dtype=int)
J = np.ones((n, n), int)


def rank_mod(M):
    M = [[int(x) % P for x in r] for r in M]
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [x * inv % P for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        r += 1
    return r


def MD(S):
    Rm = S + 2 * (I - Ppi)
    return (I - J + 2 * Ppi + Rm.T @ (5 * I + 4 * Ppi) @ Rm) % P


def rand_sigma(rng):
    # 4 permutation matrices with pairwise disjoint supports: +P1 +P2 -P3 -P4
    while True:
        perms = []
        used = set()
        ok = True
        for _ in range(4):
            for _t in range(200):
                p = list(range(n))
                rng.shuffle(p)
                if all((i, p[i]) not in used for i in range(n)):
                    break
            else:
                ok = False
                break
            perms.append(p)
            used |= {(i, p[i]) for i in range(n)}
        if ok:
            break
    S = np.zeros((n, n), int)
    for k, p in enumerate(perms):
        for i in range(n):
            S[i, p[i]] += 1 if k < 2 else -1
    return S


rng = random.Random(7)
hist = Counter()
best = 99
for t in range(20000):
    S = rand_sigma(rng)
    r1 = rank_mod(MD(S))
    r2 = rank_mod(MD(S.T))
    hist[(r1, r2)] += 1
    best = min(best, max(r1, r2))
print('rank pairs (M_D, M_C) over 20000 random Sigma:', sorted(hist.items())[:12], '... min max-rank', best)
print('fraction with both ranks <= 2:', sum(v for (a, b), v in hist.items() if a <= 2 and b <= 2) / 20000)
