"""notes/104: p-adic integrality of the order-8 hierarchy, one elimination per (p, e) with symbolic right-hand side.
t = (3 u1, t2) parametrises the valid order-7 lattice (lcm of denominators 3, t1 = 0 mod 3).  Rows (M | c0, c1, c2)
over Z/p^e with minimal-valuation pivots; rows whose M-part vanishes give affine congruences on (u1, t2) mod p^e."""
import pickle, itertools, sys
from fractions import Fraction
from subgraph_lp import Types

n, k, lam, mu = 99, 14, 1, 2
D7 = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
C8 = pickle.load(open('../data/order8_coeffs.pkl', 'rb'))
var7, z0, V = D7['var'], D7['z0'], D7['V']
a, aut7, N8 = C8['a'], C8['aut7'], C8['N8']
T = Types(lam, mu, k, 7)
idx7 = {v: q for q, v in enumerate(var7)}
eqs = []
for i, F in enumerate(T.reps[7]):
    q7 = idx7[(7, i)]
    for U in [()] + [(u,) for u in range(7)] + list(itertools.combinations(range(7), 2)):
        if len(U) == 0: b = n - 7
        elif len(U) == 1: b = k - F.degree(U[0])
        else:
            u, w = U; b = (lam if F.has_edge(u, w) else mu) - len(set(F[u]) & set(F[w]))
        coef = aut7[i] * b
        c0 = Fraction(coef) * Fraction(z0[q7]); c1 = 3 * Fraction(coef) * Fraction(V[q7][0]); c2 = Fraction(coef) * Fraction(V[q7][1])
        assert c0.denominator == 1 and c1.denominator == 1 and c2.denominator == 1, (c0, c1, c2)
        eqs.append((dict(a.get((i, U), {})), (int(c0), int(c1), int(c2))))
print('equations', len(eqs), flush=True)

def val(x, p):
    if x == 0: return 99
    v = 0
    while x % p == 0: x //= p; v += 1
    return v

def conditions(p, e):
    q = p ** e
    piv = {}                                  # column -> (row dict, rhs triple), pivot entry has minimal valuation seen
    conds = []
    for row, r in eqs:
        vec = {j: c % q for j, c in row.items() if c % q}
        rr = [x % q for x in r]
        while True:
            if not vec: break
            # choose column with minimal valuation in this row
            j = min(vec, key=lambda jj: (val(vec[jj], p), jj))
            if j in piv:
                pv, pr = piv[j]
                vp, vr = val(pv[j], p), val(vec[j], p)
                if vr >= vp:
                    f = (vec[j] // p ** vp) * pow(pv[j] // p ** vp, -1, q) % q
                    for jj, cc in pv.items():
                        nv = (vec.get(jj, 0) - f * cc) % q
                        if nv: vec[jj] = nv
                        else: vec.pop(jj, None)
                    rr = [(x - f * y) % q for x, y in zip(rr, pr)]
                else:                              # swap: new row becomes the pivot, old pivot row is reduced
                    piv[j] = (vec, rr); vec, rr = pv, pr
            else:
                piv[j] = (vec, rr); vec = None; break
        if vec is not None and not vec and any(rr):
            conds.append(tuple(rr))
    return conds

for p, e in [(2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (5, 1), (7, 1), (7, 2)]:
    cs = conditions(p, e)
    q = p ** e
    sol = [(u1, t2) for u1 in range(q) for t2 in range(q) if all((c0 + c1 * u1 + c2 * t2) % q == 0 for c0, c1, c2 in cs)]
    print(f'p^e = {p}^{e}: {len(cs)} condition rows; solvable (u1, t2) classes: {len(sol)} of {q*q}', flush=True)
