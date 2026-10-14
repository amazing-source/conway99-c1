"""Exploration: smallest c_8 (vectors of norm 16 in B) allowed at b = 28 and b = 30 under the proved bounds."""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T


def system(b, low, up, nmax=40):
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
    for m in range(1, (nmax - 1) // 7 + 1):
        G.append([c - a for a, c in zip(MA[m], MWB[7 * m])]); g.append(0)
    for (side, n), L in low.items():
        G.append((MA if side == "a" else MWB)[n]); g.append(L)
    for (side, n), U in up.items():
        G.append([-x for x in (MA if side == "a" else MWB)[n]]); g.append(-U)
    return MA, MWB, E, e, G, g


if __name__ == "__main__":
 for b in (28, 30):
   for low in ({("a", 2): 462, ("a", 4): 14970}, {("a", 2): 462, ("a", 3): 930, ("a", 4): 14970, ("a", 5): 1625}):
     MA, MWB, E, e, G, g = system(b, low, {("c", 7): 7920, ("a", 1): 56})
     v = X.optimum(MWB[8], E, e, G, g, 15, sense=-1)
     print("b=%d low=%s: min c_8 = %s" % (b, sorted(low.items()), float(v) if v not in (None, "unbounded") else v), flush=True)
