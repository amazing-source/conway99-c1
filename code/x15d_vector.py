"""X15d -- look at the violating vectors of the star test in X15 (lower side A + 4I - 18J/99)."""
import sys, random, itertools
import numpy as np
sys.path.insert(0, 'scripts')
import x15_fano_tight as X
from x15_fano_tight import *

def compression(D, fam):
    spec, gen, N, BI = D['spec'], D['gen'], D['N'], D['BI']
    free = [y for y in PAIRS if blk(y) in fam]
    const = [R for R in BLOCKS if R not in fam]
    basis = [('x', None)] + [('l', u) for u in LAB] + [('y', y) for y in free] + [('R', R) for R in const]
    n = len(basis)
    size = np.array([1] * (15 + len(free)) + [4] * len(const), float)
    Mx = np.zeros((n, n))
    def cnt(y, R):
        if R & blk(y):
            return sum(1 for z in spec[y] if blk(z) == R)
        return gen[y][R]
    for i, (ti, a) in enumerate(basis):
        for j, (tj, b) in enumerate(basis):
            v = 0
            if ti == 'x' and tj == 'l' or ti == 'l' and tj == 'x':
                v = 1
            elif ti == 'l' and tj == 'l':
                v = 1 if b == mate(a) else 0
            elif ti == 'l' and tj == 'y':
                v = 1 if a in b else 0
            elif ti == 'y' and tj == 'l':
                v = 1 if b in a else 0
            elif ti == 'l' and tj == 'R':
                v = 2 if a[0] in b else 0
            elif ti == 'R' and tj == 'l':
                v = 2 if b[0] in a else 0
            elif ti == 'y' and tj == 'y':
                v = 1 if b in spec[a] else 0
            elif ti == 'y' and tj == 'R':
                v = cnt(a, b)
            elif ti == 'R' and tj == 'y':
                v = cnt(b, a)
            elif ti == 'R' and tj == 'R':
                v = N[BI[a], BI[b]]
            Mx[i, j] = v
    assert np.allclose(Mx, Mx.T)
    return basis, size, Mx

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    while True:
        tau = fano_tau(rng)
        sigma, c, D = anneal(rng, tau)
        if c == 0:
            break
    # pure far-block test: only the 15 blocks avoiding class cc, plus x and labels (no free pairs)
    for cc in range(7):
        basis, size, Mx = compression(D, [])
        keep = [i for i, (t, a) in enumerate(basis) if t != 'R' or cc not in a]
        Mk = Mx[np.ix_(keep, keep)]; sk = size[keep]
        S2 = Mk + 4 * np.diag(sk) - 18 / 99 * np.outer(sk, sk)
        S1 = 3 * np.diag(sk) + 11 / 99 * np.outer(sk, sk) - Mk
        print('far blocks of class', cc, ': lmin lower', round(np.linalg.eigvalsh(S2).min(), 6), ' upper', round(np.linalg.eigvalsh(S1).min(), 6))
    # the star test for class 1: eigenvector
    fam = [R for R in BLOCKS if 1 in R]
    basis, size, Mx = compression(D, fam)
    S2 = Mx + 4 * np.diag(size) - 18 / 99 * np.outer(size, size)
    w, V = np.linalg.eigh(S2)
    v = V[:, 0]
    print('star 1 lower lmin', w[0])
    for (t, a), c in zip(basis, v):
        if abs(c) > 0.05:
            print('  ', t, sorted(a) if a is not None else '', round(c, 3))
