"""X1c -- 2- and 3-ranks of the groups feeding the far lattices of a line (rank 8 for K_{-4}(L), 18 for K_3(L)).
For random admissible balls: q-rank (number of Smith invariants divisible by q, kernel excluded) at q = 2, 3 of
  L_G = 3I - A_G (critical group of G(L)),  A_G + 4I,  and M M^T = 12I + 2J - A_G - A_G^2 - B_J (torsion of coker).
Nikulin needs l(D(K_{-4}(L))_2) <= 8.  At q = 2, 3 the U-part and saturation corrections are not controlled, so a large
rank here is a signal to examine, not yet a contradiction."""
import sys, os, random
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'c1_recherche', 'code'))
import line_ball as lb
import padic_py as pp

def qrank(M, q):
    vals, E = pp.smith_vals(M, q)
    return sum(1 for v in vals if 0 < v < E)

rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 400
I = np.eye(36, dtype=np.int64); J = np.ones((36, 36), dtype=np.int64)
BJ = np.zeros((36, 36), dtype=np.int64)
for p in range(3):
    BJ[12 * p:12 * (p + 1), 12 * p:12 * (p + 1)] = 1
hist = {key: Counter() for key in ('K2', 'K3', 'A4_2', 'A4_3', 'MM2', 'MM3')}
n = 0
for _ in range(trials):
    ta, tb = lb.random_matching(rng), lb.random_matching(rng)
    perm = lb.others[:]; rng.shuffle(perm); sigma = {b: perm[i] for i, b in enumerate(lb.others)}
    if not lb.local_ok(ta, tb, sigma):
        continue
    G = lb.cubic_graph(ta, tb, sigma)
    if lb.ncomp(G) != 1:
        continue
    n += 1
    MM = 12 * I + 2 * J - G - G @ G - BJ
    hist['K2'][qrank(3 * I - G, 2)] += 1; hist['K3'][qrank(3 * I - G, 3)] += 1
    hist['A4_2'][qrank(G + 4 * I, 2)] += 1; hist['A4_3'][qrank(G + 4 * I, 3)] += 1
    hist['MM2'][qrank(MM, 2)] += 1; hist['MM3'][qrank(MM, 3)] += 1
print(f'connected admissible balls: {n}')
for key, c in hist.items():
    print(f'  {key}: ' + ', '.join(f'{r}:{m}' for r, m in sorted(c.items())))
