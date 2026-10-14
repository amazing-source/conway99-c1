"""Exploration only (not a proof): how far would extra lower bounds on a_3 (vectors of norm 6 in A) push the ranks?
usage: python theta7_explore.py"""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T


def run(b, extra, nmax=40):
    s = -Fraction(7) ** (11 - b // 2) if b <= 22 else -Fraction(1, 7 ** (b // 2 - 11))
    MA = T.MA_ALL[:nmax]
    MWB = [[s * x for x in row] for row in T.MW_ALL[:nmax]]
    E, e, G, g = [MA[0], MWB[0]], [1, 1], [], []
    for n in range(1, 7):
        E.append(MWB[n]); e.append(0)
    for n in range(1, nmax):
        G.append(MA[n]); g.append(0)
        if n >= 7:
            G.append(MWB[n]); g.append(0)
    G.append(MA[2]); g.append(462)
    for m in range(1, (nmax - 1) // 7 + 1):
        G.append([c - a for a, c in zip(MA[m], MWB[7 * m])]); g.append(0)
    for n, L in extra.items():
        G.append(MA[n]); g.append(L)
    return X.feasible(E, e, G, g, 15)[0]


for L in (0, 2000, 6000, 10000, 15000):
    res = [b for b in range(24, 44, 2) if not run(b, {3: L})]
    print("a_3 >=", L, ": infeasible ranks among b = 24..42:", res, flush=True)
