"""Exploration: for b = 28..42 with a_2 >= 462, a_4 >= 14970, c_7 <= 7920: ranges of a_1, a_2, a_3 and c_7..c_11."""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T
from theta7_ranges import system


def fmt(v):
    return "%.4g" % float(v) if v not in (None, "unbounded") else str(v)


for b in range(28, 44, 2):
    MA, MWB, E, e, G, g = system(b)
    G = G + [[-x for x in MWB[7]]]; g = g + [-7920]
    out = []
    for name, row in (("a1", MA[1]), ("a2", MA[2]), ("a3", MA[3]), ("c7", MWB[7]), ("c8", MWB[8]), ("c9", MWB[9]),
                      ("c10", MWB[10]), ("c11", MWB[11])):
        lo = X.optimum(row, E, e, G, g, 15, sense=-1)
        hi = X.optimum(row, E, e, G, g, 15, sense=1)
        out.append("%s [%s, %s]" % (name, fmt(lo), fmt(hi)))
    print("b = %d: " % b + "; ".join(out), flush=True)
