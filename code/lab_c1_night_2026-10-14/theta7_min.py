"""Exploration: min and max of a_6, a_7, a_8 at b = 30 under the proved bounds (to see what a lower bound must reach)."""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T
from theta7_c8 import system
for b in (30,):
    MA, MWB, E, e, G, g = system(b, {("a", 2): 462, ("a", 4): 14970}, {("c", 7): 7920, ("c", 8): 360360})
    for n in (5, 6, 7, 8):
        lo = X.optimum(MA[n], E, e, G, g, 15, sense=-1); hi = X.optimum(MA[n], E, e, G, g, 15, sense=1)
        print("b=%d a_%d in [%.4g, %.4g]" % (b, n, float(lo), float(hi)), flush=True)
