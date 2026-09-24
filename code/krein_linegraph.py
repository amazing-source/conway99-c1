"""Krein-type conditions for the idempotents of the LINE graph A_L of srg(99,14,1,2) (pure mathematics).
A_L (231 lines, adjacent = meeting) has eigenvalues 18, 7 (54), 0 (44), -3 (132); idempotents
  E18 = J/231, E7 = G3/770 (E_3 part), E0 = K/21 (E_-4 part), Em3 = F = projection on ker N (line functions with
  zero sum at every point).  Entries by pair type: self / meeting / disjoint with e edges (notes/70).
For PSD X, Y, Z:  sum_ij X_ij Y_ij Z_ij = tr((X o Y) Z) >= 0.  Per-line counts: 1 self, 18 meeting,
n0 = 32-pi, n1 = 144+3pi, n2 = 36-3pi, n3 = pi; sum over lines of pi = 2P.
"""
from fractions import Fraction as Fr
from itertools import combinations_with_replacement
import sympy as sp

E = {
    '18': {'s': Fr(1, 231), 'm': Fr(1, 231), 0: Fr(1, 231), 1: Fr(1, 231), 2: Fr(1, 231), 3: Fr(1, 231)},
    '7': {'s': Fr(180, 770), 'm': Fr(70, 770), **{e: Fr(11 * e - 18, 770) for e in range(4)}},
    '0': {'s': Fr(4, 21), 'm': Fr(0), **{e: Fr(1 - e, 21) for e in range(4)}},
    '-3': {'s': Fr(120, 210), 'm': Fr(-20, 210), **{e: Fr(7 * e - 6, 210) for e in range(4)}},
}
# sanity: the four idempotents sum to the identity entrywise
for key in ['s', 'm', 0, 1, 2, 3]:
    tot = sum(E[a][key] for a in E)
    assert tot == (1 if key == 's' else 0), (key, tot)

P = sp.symbols('P')
pi = 2 * P / 231
cnt = {'s': 1, 'm': 18, 0: 32 - pi, 1: 144 + 3 * pi, 2: 36 - 3 * pi, 3: pi}
print('Krein-type triple sums  T(a,b,c) = sum_{L,M} Ea Eb Ec  (must be >= 0), as functions of P:')
for a, b, c in combinations_with_replacement(['18', '7', '0', '-3'], 3):
    T = sp.nsimplify(231 * sum(cnt[k] * sp.Rational(E[a][k] * E[b][k] * E[c][k]) for k in cnt))
    T = sp.expand(T)
    c0, c1 = T.subs(P, 0), T.coeff(P)
    note = ''
    if c1 != 0:
        root = -c0 / c1
        note = f'   => P {"<=" if c1 < 0 else ">="} {float(root):.2f}'
    elif c0 < 0:
        note = '   => CONTRADICTION'
    print(f'  ({a:>3},{b:>3},{c:>3}): {float(c0):+.6e} {float(c1):+.6e}*P{note}')
