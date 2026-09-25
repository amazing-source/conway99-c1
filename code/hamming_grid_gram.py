"""notes/103: at a Hamming point x the 21 grids G_P (one per class pair) are complete, so eta_P = 11*1_{G_P} - 1 lies
in Lambda_3.  Gram mod 7: 3 on the diagonal, 2|G_P cap G_Q| - 1 off it (|cap| = 3 if P, Q share a class, 1 if disjoint).
Its rank r_g bounds dim U' = 40 - k from below:  r_g <= 40 - k, with a sign condition at equality (U' is split)."""
import itertools
import numpy as np
from beta_form_check import rank_leg

pairs = list(itertools.combinations(range(7), 2))
n = len(pairs)
G = np.zeros((n, n), dtype=np.int64)
for a, P in enumerate(pairs):
    for b, Q in enumerate(pairs):
        if a == b:
            G[a, b] = 990                      # |eta|^2 = 121*9 - 22*9 + 99
        else:
            cap = 1 + (2 if set(P) & set(Q) else 0)
            G[a, b] = 121 * cap - 2 * 99 + 99  # eta_P.eta_Q = 121|cap| - 11*9 - 11*9 + 99
print('Gram exact: diag', G[0, 0], ' share-class', G[0, 1], ' disjoint', G[0, pairs.index((2, 3))])
print('mod 7 (rank, Legendre of nondeg part):', rank_leg((G % 7).tolist(), 7))
print('rational rank:', np.linalg.matrix_rank(G.astype(float)))
