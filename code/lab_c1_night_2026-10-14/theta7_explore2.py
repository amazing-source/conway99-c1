"""Exploration: rank b = 24..30 with a_3 >= L (norm-6 vectors of A) and optionally a_1 <= 56 (Codex, roots A_1^r)."""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T


def run(b, low, up, nmax=40):
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
    for n, L in low.items():
        G.append(MA[n]); g.append(L)
    for n, U in up.items():
        G.append([-x for x in MA[n]]); g.append(-U)
    return X.feasible(E, e, G, g, 15)[0]


if __name__ == "__main__":
  for low, up in (({3: 930}, {}), ({}, {1: 56}), ({3: 930}, {1: 56}), ({3: 1200}, {1: 56}), ({3: 1500}, {})):
      res = [b for b in range(24, 32, 2) if not run(b, low, up)]
      print("low", low, "up", up, ": infeasible ranks among 24..30:", res, flush=True)
