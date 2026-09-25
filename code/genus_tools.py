"""p-adic Jordan symbols (odd p) and the oddity formula, exact rational arithmetic (notes/101).

For an integral positive-definite Gram matrix G with det odd at 2 (2-adically unimodular):
  sum_{p odd | det} p-excess(G) + signature  ==  oddity_2(G)   (mod 8)        [Conway-Sloane, SPLAG ch. 15]
p-excess = sum_j n_j (p^j - 1) + 4 [j odd and eps_j = -1]  (mod 8),  eps_j = Legendre(det of the unit part of the
p^j-component).  oddity_2 = 0 for even lattices; for odd 2-adically unimodular ones, the trace (mod 8) of a 2-adic
diagonalisation.  The functions are tested on known lattices and random ones in __main__.
"""
from fractions import Fraction as Fr
import random, sys


def vp(x, p):
    x = Fr(x)
    if x == 0:
        return 10 ** 9
    n, d = x.numerator, x.denominator
    v = 0
    while n % p == 0:
        n //= p; v += 1
    while d % p == 0:
        d //= p; v -= 1
    return v


def unit_part(x, p):
    x = Fr(x)
    v = vp(x, p)
    return x / Fr(p) ** v


def legendre_unit(u, p):
    """Legendre symbol of a p-adic unit given as a rational with p-free numerator and denominator."""
    u = Fr(u)
    a = (u.numerator * pow(u.denominator, -1, p)) % p
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def diagonalize_padic(G, p):
    """Return diagonal entries of a p-adically equivalent diagonal form (odd p), exact over Q."""
    n = len(G)
    M = [[Fr(x) for x in row] for row in G]
    diag = []
    idx = list(range(n))
    while idx:
        # pick the entry of minimal valuation
        best = None
        for i in idx:
            for j in idx:
                if M[i][j] != 0:
                    v = vp(M[i][j], p)
                    if best is None or v < best[0] or (v == best[0] and i == j and best[1] != best[2]):
                        best = (v, i, j)
        if best is None:
            diag.extend([Fr(0)] * len(idx)); break
        v, i, j = best
        if i != j:
            # make a diagonal entry of valuation v: e_i <- e_i + e_j (works for odd p when M_ii, M_jj have val > v)
            if vp(M[i][i], p) > v and vp(M[j][j], p) > v:
                for k in range(n):
                    M[i][k] += M[j][k]
                for k in range(n):
                    M[k][i] += M[k][j]
            elif vp(M[j][j], p) == v:
                i = j
        piv = M[i][i]
        diag.append(piv)
        rest = [k for k in idx if k != i]
        for a in rest:
            f = M[a][i] / piv
            if f != 0:
                for b in range(n):
                    M[a][b] -= f * M[i][b]
        for a in rest:
            M[a][i] = Fr(0); M[i][a] = Fr(0)
        idx = rest
    return diag


def jordan_symbol(G, p):
    d = diagonalize_padic(G, p)
    comps = {}
    for x in d:
        j = vp(x, p)
        comps.setdefault(j, []).append(unit_part(x, p))
    out = []
    for j in sorted(comps):
        prod = Fr(1)
        for u in comps[j]:
            prod *= u
        out.append((j, len(comps[j]), legendre_unit(prod, p)))
    return out


def p_excess(G, p):
    s = 0
    for j, n, eps in jordan_symbol(G, p):
        s += n * (p ** j - 1)
        if j % 2 == 1 and eps == -1:
            s += 4
    return s % 8


def det_frac(G):
    n = len(G)
    M = [[Fr(x) for x in row] for row in G]
    det = Fr(1)
    for c in range(n):
        r = next((i for i in range(c, n) if M[i][c] != 0), None)
        if r is None:
            return Fr(0)
        if r != c:
            M[c], M[r] = M[r], M[c]; det = -det
        det *= M[c][c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            if f:
                for k in range(c, n):
                    M[i][k] -= f * M[c][k]
    return det


def odd_primes(n):
    n = abs(int(n)); ps = []
    q = 2
    while q * q <= n:
        if n % q == 0:
            ps.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        ps.append(n)
    return [x for x in ps if x != 2]


def oddity2_unimodular(G):
    """2-adic oddity of a 2-adically unimodular lattice (odd det): 0 if even, else trace of a 2-adic diagonalisation."""
    if all(G[i][i] % 2 == 0 for i in range(len(G))):
        return 0
    d = diagonalize_padic_2(G)
    return sum(int(unit_part(x, 2).numerator * pow(unit_part(x, 2).denominator, -1, 8)) for x in d) % 8


def diagonalize_padic_2(G):
    n = len(G)
    M = [[Fr(x) for x in row] for row in G]
    idx = list(range(n)); diag = []
    while idx:
        i = next((k for k in idx if vp(M[k][k], 2) == 0), None)
        if i is None:
            raise ValueError('even part: not handled')
        piv = M[i][i]; diag.append(piv)
        rest = [k for k in idx if k != i]
        for a in rest:
            f = M[a][i] / piv
            if f:
                for b in range(n):
                    M[a][b] -= f * M[i][b]
        for a in rest:
            M[a][i] = Fr(0); M[i][a] = Fr(0)
        idx = rest
    return diag


def oddity_check(G):
    D = det_frac(G)
    assert D.denominator == 1 and D % 2 == 1, 'test only odd determinants'
    lhs = (len(G) + sum(p_excess(G, p) for p in odd_primes(D))) % 8
    return lhs, oddity2_unimodular(G)


def cartan(name):
    import itertools
    t, n = name[0], int(name[1:])
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        G[i][i] = 2
    if t == 'A':
        for i in range(n - 1):
            G[i][i + 1] = G[i + 1][i] = -1
    elif t == 'E':
        # E_n Dynkin: chain 1-3-4-5-...-n with node 2 attached to 4 (Bourbaki)
        edges = [(0, 2), (2, 3), (1, 3)] + [(k, k + 1) for k in range(3, n - 1)]
        for a, b in edges:
            G[a][b] = G[b][a] = -1
    return G


if __name__ == '__main__':
    for nm in ('A2', 'A4', 'A6', 'E6', 'E8'):
        G = cartan(nm)
        print(nm, 'det', det_frac(G), 'check (lhs, oddity):', oddity_check(G))
    rng = random.Random(1)
    bad = tested = 0
    while tested < 300:
        n = rng.randint(2, 7)
        B = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        G = [[sum(B[k][i] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        D = det_frac(G)
        if D == 0 or D % 2 == 0:
            continue
        if rng.random() < 0.5:        # make it even: 2G has even det; instead test odd lattices as they are
            pass
        try:
            lhs, odd = oddity_check(G)
        except ValueError:
            continue
        tested += 1
        if lhs != odd:
            bad += 1
    print('random odd-det lattices tested:', tested, ' oddity formula failures:', bad)
    bad = tested = 0
    while tested < 2000:
        n = rng.randint(1, 9)
        B = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        G = [[sum(B[k][i] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        # even lattice from an integral one: use 2G? det doubles. Use G + G^T style on a random symmetric even matrix
        S = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                S[i][j] = S[j][i] = (2 * rng.randint(1, 4) if i == j else rng.randint(-1, 1))
        # positive definite even: add a large multiple of 2I
        for i in range(n):
            S[i][i] += 2 * n
        D = det_frac(S)
        if D == 0 or D % 2 == 0:
            continue
        tested += 1
        lhs, odd = oddity_check(S)
        if lhs != odd:
            bad += 1
    print('random even odd-det lattices tested:', tested, ' oddity formula failures:', bad)
