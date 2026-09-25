"""X15f -- far-block criterion.  For the line L_c = {x, c0, c1} and a set S of far vertices with ball profile n
(n_b = # neighbours of b in S, b in N(L)), with n_perp = n - (|S|/6) 1:
   (U) 2 e(S) <= 3|S| + |S|^2/12 - n_perp^T (3I - A_G)^{-1} n_perp
   (L) 2 e(S) >= -4|S| + |S|^2/5 + n_perp^T (A_G + 4I)^{-1} n_perp
(derived from A_F = B0 - 7 Pi_{-4} = B1 + 7 Pi_3, notes E3).  Here S = one far block (e(S) = 0) in the Fano-tight model.
Cross-check against the compression test of X15."""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
from x15_fano_tight import *

def ball(D, c):
    """N(L) order: 12 labels != c, 12 pairs {c0, v}, 12 pairs {c1, v}; A_G."""
    labs = [u for u in LAB if u[0] != c]
    N = [('l', u) for u in labs] + [('y', frozenset({(c, 0), u})) for u in labs] + [('y', frozenset({(c, 1), u})) for u in labs]
    n = len(N)
    AG = np.zeros((n, n))
    for i, (ti, a) in enumerate(N):
        for j, (tj, b) in enumerate(N):
            if ti == 'l' and tj == 'l':
                AG[i, j] = b == mate(a)
            elif ti == 'l' and tj == 'y':
                AG[i, j] = a in b
            elif ti == 'y' and tj == 'l':
                AG[i, j] = b in a
            elif ti == 'y' and tj == 'y':
                AG[i, j] = b in D['spec'][a]
    return N, AG

def profile(D, N, R):
    n = []
    for t, a in N:
        if t == 'l':
            n.append(2 if a[0] in R else 0)
        else:
            if R & blk(a):
                n.append(sum(1 for z in D['spec'][a] if blk(z) == R))
            else:
                n.append(D['gen'][a][R])
    return np.array(n, float)

def criterion(AG, n, size, e2):
    np_ = n - size / 6
    U = np.zeros_like(AG); nN = len(AG)
    Q = np.eye(nN) - np.kron(np.eye(3), np.ones((12, 12)) / 12)   # projector on U^perp (part-sum-zero)
    assert abs(np_.sum()) < 1e-9 and np.allclose(np.kron(np.eye(3), np.ones((1, 12))) @ np_, 0)
    w, V = np.linalg.eigh(AG)
    # (3 - A_G)^{-1} on U^perp: eigenvalue 3 eigenvectors must be orthogonal to n_perp
    coef = V.T @ np_
    up = sum(c * c / (3 - l) for c, l in zip(coef, w) if abs(3 - l) > 1e-9)
    assert all(abs(c) < 1e-7 for c, l in zip(coef, w) if abs(3 - l) <= 1e-9)
    lo = sum(c * c / (l + 4) for c, l in zip(coef, w))
    slackU = 3 * size + size ** 2 / 12 - up - e2
    slackL = e2 - (-4 * size + size ** 2 / 5 + lo)
    return slackU, slackL

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    ncfg = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    got = 0
    while got < ncfg:
        tau = fano_tau(rng)
        sigma, c, D = anneal(rng, tau)
        if c != 0:
            continue
        got += 1
        print('config', got)
        for cc in range(7):
            N, AG = ball(D, cc)
            out = []
            for R in BLOCKS:
                if cc in R:
                    continue
                n = profile(D, N, R)
                sU, sL = criterion(AG, n, 4, 0)
                typ = 'I ' if PHI[tuple(sorted(R))] == cc else 'II'
                out.append((typ, tuple(sorted(R)), round(sU, 4), round(sL, 4)))
            bad = [o for o in out if min(o[2], o[3]) < -1e-9]
            print(f'  class {cc}: type I slacks', [(o[1], o[2], o[3]) for o in out if o[0] == 'I '],
                  f'| type II violating {sum(1 for o in bad if o[0] == "II")}/12')
