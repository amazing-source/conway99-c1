"""Exploration: for each rank b, the smallest a_2, a_3, a_4 and the largest a_2 allowed by the exact programme with
the rigorous constraints a_2 >= 462, a_4 >= 14970, c_7m >= a_m (NOTE_NIGHT 19)."""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T


def system(b, nmax=40, low=None):
    low = low or {2: 462, 4: 14970}
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
    for n, L in low.items():
        G.append(MA[n]); g.append(L)
    return MA, MWB, E, e, G, g


if __name__ == "__main__":
    for b in range(26, 44, 2):
        MA, MWB, E, e, G, g = system(b)
        out = []
        for n in (1, 2, 3, 4):
            v = X.optimum(MA[n], E, e, G, g, 15, sense=-1)
            out.append("min a_%d = %s" % (n, "%.1f" % float(v) if v not in (None, "unbounded") else v))
        v = X.optimum(MWB[7], E, e, G, g, 15, sense=-1)
        out.append("min c_7 = %s" % ("%.1f" % float(v) if v not in (None, "unbounded") else v))
        print("b = %d: " % b + ", ".join(out), flush=True)
