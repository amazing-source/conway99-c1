r"""X1b -- for Conway 99: q-ranks of the groups that X1 predicts as discriminant groups of the far lattices of a line.

For an admissible line ball (tau_a, tau_abar, sigma) with cubic graph G = G(L) on 36 vertices:
  D(K_{-4}(L))_q ~ critical group K(G)_q      (rank K_{-4}(L) = 8)
  D(K_3(L))_q    ~ coker(A_G + 4I)_q           (rank K_3(L)  = 18)
at q not dividing 2*3*7 (clean primes; the U-part numbers are 3-r=0.., |X_i| = 12, 2k-8 = 20, 6k-24 = 60 -> 2,3,5 are
unclean too: 5 | 20).  Nikulin: an even lattice of rank n has l(D_q) <= n.  So a ball with l(K(G)_q) > 8 or
l(coker(A_G+4I)_q) > 18 at a clean prime would be impossible.  Only q <= 37 can reach these lengths.
Also reported: components, d(L) = dim ker_7(A_G - 3I), (tau|7).
"""
import sys, os, random
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'c1_recherche', 'code'))
import line_ball as lb
import padic_py as pp

CLEAN = (11, 13, 17, 19, 23, 29, 31, 37)


def qrank(M, q):
    vals, E = pp.smith_vals(M, q)
    return sum(1 for v in vals if 0 < v < E), sum(1 for v in vals if v >= E)


def main(seed=1, trials=400):
    rng = random.Random(seed)
    I = np.eye(36, dtype=np.int64)
    stats = Counter(); worst = Counter(); n_ok = 0
    for _ in range(trials):
        ta, tb = lb.random_matching(rng), lb.random_matching(rng)
        perm = lb.others[:]; rng.shuffle(perm)
        sigma = {b: perm[i] for i, b in enumerate(lb.others)}
        if not lb.local_ok(ta, tb, sigma):
            continue
        n_ok += 1
        G = lb.cubic_graph(ta, tb, sigma)
        Lap = 3 * I - G
        comps = lb.ncomp(G)
        d7 = 36 - lb.rank_mod(G - 3 * I)
        row = []
        for q in (5, 7) + CLEAN:
            kq, zq = qrank(Lap, q)            # zq = kernel dim (components)
            cq, _ = qrank(G + 4 * I, q)
            row.append((q, kq, cq))
            worst[(q, 'K(G)')] = max(worst[(q, 'K(G)')], kq)
            worst[(q, 'coker(A+4)')] = max(worst[(q, 'coker(A+4)')], cq)
        bad = [(q, kq, cq) for q, kq, cq in row if q in CLEAN and (kq > 8 or cq > 18)]
        stats[(comps, d7, bool(bad))] += 1
    print(f'admissible balls: {n_ok} of {trials} random configurations')
    for key, m in sorted(stats.items()):
        print(f'  components={key[0]} d(L)={key[1]} Nikulin violation={key[2]}: {m}')
    print('  largest q-rank seen:', {f'{q}:{nm}': v for (q, nm), v in sorted(worst.items()) if v})


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1, int(sys.argv[2]) if len(sys.argv) > 2 else 400)
