"""Square-class lemma on a REAL srg(243,22,1,2) (LAB 15/10/2026): det(4I - A_H) for star complements H of the eigenvalue
4 (|H| = 243 - 132 = 111), random H and H containing N[v]; the squarefree part (sign included) must be the same.
usage: python sq243_check.py <edges file> [random samples, default 3]"""
import math
import random
import sys

import numpy as np

from sc_square_class import det_int

E = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
nv = 1 + max(max(e) for e in E)
A = [[0] * nv for _ in range(nv)]
for i, j in E:
    A[i][j] = A[j][i] = 1
samples = int(sys.argv[2]) if len(sys.argv) > 2 else 3
rng = random.Random(5)


def sqfree(d):
    s = -1 if d < 0 else 1
    d = abs(d)
    out = 1
    for p in (2, 3, 5, 7, 11, 13):
        e = 0
        while d % p == 0:
            d //= p
            e += 1
        if e % 2:
            out *= p
    rest_sq = math.isqrt(d) ** 2 == d
    return s * out, rest_sq


def detH(H):
    return det_int([[(4 if i == j else 0) - A[i][j] for j in H] for i in H])


res = []
tries = 0
while len([r for r in res if r[0] == "random"]) < samples and tries < 20:
    tries += 1
    H = sorted(rng.sample(range(nv), 111))
    d = detH(H)
    if d:
        res.append(("random", sqfree(d)))
Nv = [0] + [u for u in range(nv) if A[0][u]]
rest = [u for u in range(nv) if u not in Nv]
tries = 0
while len([r for r in res if r[0] == "contains N[v]"]) < 2 and tries < 20:
    tries += 1
    H = sorted(Nv + rng.sample(rest, 111 - len(Nv)))
    d = detH(H)
    if d:
        res.append(("contains N[v]", sqfree(d)))
for kind, (cls, ok) in res:
    print("%s: squarefree part over {2,3,5,7,11,13} = %d, remaining cofactor a perfect square: %s" % (kind, cls, ok))
