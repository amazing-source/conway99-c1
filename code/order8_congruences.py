"""notes/104: integrality of the order-8 counting hierarchy.  Equations (i order-7 type, U subset, |U|<=2):
    sum_j a(i,U,j) z8_j = aut7_i * b(i,U) * z7_i(t),   z7 = z0 + V t  (t = 2 free order-7 counts).
For each prime p: for which t (mod p) is the system solvable mod p?  Congruences on (P, S) that no LP sees."""
import pickle, itertools
from fractions import Fraction
from math import lcm
import networkx as nx
from subgraph_lp import Types

n, k, lam, mu = 99, 14, 1, 2
D7 = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
C8 = pickle.load(open('../data/order8_coeffs.pkl', 'rb'))
var7, z0, V = D7['var'], D7['z0'], D7['V']
a, aut7, N8 = C8['a'], C8['aut7'], C8['N8']
T = Types(lam, mu, k, 7)
idx7 = {v: q for q, v in enumerate(var7)}
rows, rhs = [], []          # rhs = affine function of t: (c0, c1, c2) rationals
for i, F in enumerate(T.reps[7]):
    q7 = idx7[(7, i)]
    for U in [()] + [(u,) for u in range(7)] + list(itertools.combinations(range(7), 2)):
        if len(U) == 0: b = n - 7
        elif len(U) == 1: b = k - F.degree(U[0])
        else:
            u, w = U; b = (lam if F.has_edge(u, w) else mu) - len(set(F[u]) & set(F[w]))
        coef = aut7[i] * b
        rows.append(dict(a.get((i, U), {})))
        rhs.append((Fraction(coef) * Fraction(z0[q7]), Fraction(coef) * Fraction(V[q7][0]), Fraction(coef) * Fraction(V[q7][1])))
print('equations', len(rows), ' unknowns z8', N8)
# valid lattice for t: all z7(t) integral.  Search t mod M0 for M0 = lcm of denominators.
den = 1
for q in range(len(var7)):
    for x in (z0[q], V[q][0], V[q][1]):
        den = lcm(den, Fraction(x).denominator)
print('lcm of denominators of z7(t):', den)
valid = [(t1, t2) for t1 in range(den) for t2 in range(den)
         if all((Fraction(z0[q]) + Fraction(V[q][0]) * t1 + Fraction(V[q][1]) * t2).denominator == 1 for q in range(len(var7)))]
print('valid t classes mod', den, ':', len(valid), valid[:6])

def solvable_mod_p(p, t):
    y = []
    for (c0, c1, c2) in rhs:
        val = c0 + c1 * t[0] + c2 * t[1]
        assert val.denominator == 1
        y.append(int(val) % p)
    # Gaussian elimination on augmented rows mod p (sparse dict rows)
    piv = {}
    for r, row in enumerate(rows):
        vec = {j: c % p for j, c in row.items() if c % p}
        yy = y[r]
        while vec:
            j = max(vec)
            if j in piv:
                pv, py = piv[j]
                f = vec[j] * pow(pv[j], -1, p) % p
                for jj, cc in pv.items():
                    nv = (vec.get(jj, 0) - f * cc) % p
                    if nv: vec[jj] = nv
                    else: vec.pop(jj, None)
                yy = (yy - f * py) % p
            else:
                piv[j] = (vec, yy); break
        if not vec and yy % p:
            return False
    return True

# test t values: valid classes shifted over a few periods, for each prime
for p in (2, 3, 5, 7, 11):
    res = {}
    for t in valid:
        for s1 in range(p):
            for s2 in range(p):
                tt = (t[0] + den * s1, t[1] + den * s2)
                res[(tt[0] % (den * p), tt[1] % (den * p))] = solvable_mod_p(p, tt)
    ok = sum(res.values())
    print(f'p={p}: solvable for {ok} of {len(res)} valid t classes mod {den*p}', flush=True)
