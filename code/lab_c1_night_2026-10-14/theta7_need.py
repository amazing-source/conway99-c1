"""Exploration: at a given rank b, with the proved bounds, the forced ranges of the first shells of A and B."""
import sys
from fractions import Fraction
import exact_lp as X
import theta7_lp as T
from theta7_c8 import system

b = int(sys.argv[1])
low = {("a", 2): 462, ("a", 3): 930, ("a", 4): 14970, ("a", 5): 1625}
up = {("c", 7): 7920, ("c", 8): 360360, ("a", 1): 56}
MA, MWB, E, e, G, g = system(b, low, up)
for name, row in [("a%d" % n, MA[n]) for n in (1, 2, 3)] + [("c%d" % n, MWB[n]) for n in (7, 8, 9, 10, 11, 12)]:
    lo = X.optimum(row, E, e, G, g, 15, sense=-1)
    hi = X.optimum(row, E, e, G, g, 15, sense=1)
    f = lambda v: "%.4g" % float(v) if v not in (None, "unbounded") else str(v)
    print("b=%d %s in [%s, %s]" % (b, name, f(lo), f(hi)), flush=True)
